"""CPU-only acquisition of the pinned VLSU release."""

import argparse
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from contextlib import closing
import errno
import fcntl
from hashlib import sha256
import json
import os
from pathlib import Path
import re
import shutil
import sqlite3
import subprocess
import sys
import time
from urllib.parse import urljoin

import yaml

from stage0_audit_csv import CSV_SHA256
from stage1_manifest import canonical, pinned_rows, smoke_rows
from stage1_transport import Deferred, Failure, Limiter, Pause, resolve, response, retry_after

TERMINAL = {"success_decode", "failed_terminal"}
ETAG = re.compile(r'"[\x21\x23-\x7e]*"')
CONTENT_RANGE = re.compile(r"bytes ([0-9]+)-([0-9]+)/([0-9]+)")
REDIRECTS = {301, 302, 303, 307, 308}
RETRY_HTTP = {408, 425, 429, 500, 502, 503, 504}
ENVIRONMENT_DNS = {"dns_timeout", "dns_resolution", "dns_resolver_error"}
DEFAULT_CONFIG = Path(__file__).resolve().parents[1] / "configs/stage1_download.yaml"


def digest(path):
    with path.open("rb") as stream:
        h = sha256()
        while chunk := stream.read(1024 * 1024):
            h.update(chunk)
    return h.hexdigest()


def sync_dir(path):
    fd = os.open(path, os.O_RDONLY | os.O_DIRECTORY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


def atomic(path, data):
    temp = path.with_suffix(path.suffix + ".tmp")
    with temp.open("wb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    temp.replace(path)
    sync_dir(path.parent)


def connect(root):
    db = sqlite3.connect(root / "audit.sqlite", timeout=30)
    db.row_factory = sqlite3.Row
    return db


def initialize(db, rows):
    db.executescript("""
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS release (uuid TEXT PRIMARY KEY, url TEXT NOT NULL,
            image TEXT, text TEXT, joint TEXT, pattern TEXT, csv_row INTEGER);
        CREATE TABLE IF NOT EXISTS source (url TEXT PRIMARY KEY, state TEXT DEFAULT 'queued',
            attempt INTEGER DEFAULT 0, next REAL DEFAULT 0, reason TEXT, category TEXT,
            http_success INTEGER DEFAULT 0, complete_bytes INTEGER DEFAULT 0,
            digest TEXT, started REAL);
        CREATE TABLE IF NOT EXISTS events (id INTEGER PRIMARY KEY, url TEXT NOT NULL,
            attempt INTEGER, at REAL, kind TEXT, data TEXT);
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS cooldown (host TEXT PRIMARY KEY, until REAL);
        CREATE INDEX IF NOT EXISTS events_url ON events(url);
    """)
    with db:
        if "retry_floor" not in {r["name"] for r in db.execute("PRAGMA table_info(source)")}:
            db.execute("ALTER TABLE source ADD COLUMN retry_floor INTEGER NOT NULL DEFAULT 0")
        previous = db.execute("SELECT value FROM meta WHERE key='csv_sha256'").fetchone()
        if previous and previous[0] != CSV_SHA256:
            raise ValueError("State CSV SHA-256 differs")
        db.execute("INSERT OR IGNORE INTO meta VALUES ('csv_sha256',?)", (CSV_SHA256,))
        db.executemany("INSERT OR IGNORE INTO release VALUES (?,?,?,?,?,?,?)", rows)
        db.executemany("INSERT OR IGNORE INTO source(url) VALUES (?)", ((row[1],) for row in rows))
        roster = set(map(tuple, db.execute("SELECT * FROM release")))
        if roster != set(rows) or db.execute("SELECT COUNT(*) FROM source").fetchone()[0] != len({r[1] for r in rows}):
            raise ValueError("Stored release roster differs from pinned CSV")


def event(db, url, attempt, kind, **data):
    db.execute("INSERT INTO events(url,attempt,at,kind,data) VALUES (?,?,?,?,?)",
               (url, attempt, time.time(), kind, json.dumps(data, sort_keys=True)))


def discard(part, meta, note, reason):
    note("partial_discard", reason=reason, bytes=part.stat().st_size if part.exists() else 0)
    meta.unlink(missing_ok=True)
    part.unlink(missing_ok=True)


def length_header(resp):
    values = resp.headers.get_all("Content-Length") or []
    if not values:
        return None
    if len(values) != 1 or not re.fullmatch(r"[0-9]{1,18}", values[0]):
        raise Failure("invalid_content_length")
    return int(values[0])


def partial_info(part, metadata, config, note):
    if not part.exists() and not metadata.exists():
        return {}, 0
    try:
        info = json.loads(metadata.read_bytes())
        n = part.stat().st_size
        if (ETAG.fullmatch(info["etag"]) and 0 < n < info["total"] <= config["max_bytes"]
                and info["final_url"] and info["mime"]):
            return info, n
    except (ValueError, TypeError, KeyError, FileNotFoundError):
        pass
    discard(part, metadata, note, "missing_or_invalid_partial_validator")
    return {}, 0


def transfer(resp, part, meta, config, current, info, offset, note):
    cap = config["max_bytes"]
    length = length_header(resp)
    mime = resp.getheader("Content-Type", "")
    encoding = resp.getheader("Content-Encoding", "identity").lower()
    etag = resp.getheader("ETag", "")
    transfer_encoding = resp.getheader("Transfer-Encoding", "").lower()
    if encoding != "identity" or transfer_encoding not in ("", "chunked") or (transfer_encoding and length is not None):
        raise Failure("unsupported_http_encoding", category="resource")
    if resp.status == 206:
        cr = CONTENT_RANGE.fullmatch(resp.getheader("Content-Range", ""))
        if not cr or any(len(n) > 18 for n in cr.groups()):
            discard(part, meta, note, "invalid_content_range")
            raise Failure("invalid_content_range", retry=True)
        start, end, total = map(int, cr.groups())
        if (not offset or current != info["final_url"] or etag != info["etag"]
                or mime != info["mime"] or start != offset or end != total - 1
                or total != info["total"] or (length is not None and length != total - offset)):
            discard(part, meta, note, "range_validator_mismatch")
            raise Failure("range_validator_mismatch", retry=True)
        note("range_resumed", offset=offset, total=total)
    else:
        if offset:
            discard(part, meta, note, "range_ignored_or_entity_changed")
        offset, total = 0, length
    if total is not None and total > cap:
        raise Failure("image_byte_limit", category="resource")
    if total is not None and ETAG.fullmatch(etag):
        atomic(meta, canonical({"etag": etag, "total": total, "final_url": current, "mime": mime}))
    else:
        meta.unlink(missing_ok=True)
    n = offset
    with part.open("ab" if offset else "wb") as stream:
        try:
            while chunk := resp.read1(65536):
                n += len(chunk)
                if n > cap:
                    raise Failure("image_byte_limit", category="resource")
                stream.write(chunk)
        finally:
            stream.flush()
            os.fsync(stream.fileno())
    if total is not None and n != total:
        raise Failure("incomplete_body", retry=True)
    if not n:
        raise Failure("empty_body", category="format")
    return n, mime


def download(url, part, meta, config, limiter, note, on_request, transport):
    info, offset = partial_info(part, meta, config, note)
    current = url
    chain = []
    for hop in range(config["redirects"] + 1):
        headers = {"User-Agent": "VLSU-Reproduction/1.0", "Accept": "image/*",
                   "Accept-Encoding": "identity", "Connection": "close"}
        range_sent = offset and current == info["final_url"]
        if range_sent:
            headers.update({"Range": f"bytes={offset}-", "If-Range": info["etag"]})
        with transport(current, headers, config, limiter, on_request) as (resp, host):
            status = resp.status
            note("http", status=status, final_url=current, chain=chain, mime=resp.getheader("Content-Type"),
                 etag=resp.getheader("ETag"), last_modified=resp.getheader("Last-Modified"))
            if status in REDIRECTS:
                location = resp.getheader("Location")
                if hop == config["redirects"] or not location:
                    raise Failure("redirect_limit_or_missing_location", category="http")
                if any(c.isspace() or ord(c) < 32 or c == "\\" for c in location):
                    raise Failure("unsafe_redirect", category="security")
                chain = [*chain, current]
                current = urljoin(current, location)
                continue
            if status == 416 and range_sent:
                discard(part, meta, note, "range_416")
                raise Failure("range_416", retry=True, category="http")
            if status not in {200, 206}:
                delay = retry_after(resp.getheader("Retry-After")) if status in RETRY_HTTP else 0
                if delay:
                    until = limiter.defer(host, delay)
                    note("cooldown", host=host, until=until)
                raise Failure(f"http_{status}", retry=status in RETRY_HTTP or status >= 500,
                              category="http", delay=delay)
            if status == 206 and not range_sent:
                raise Failure("unsolicited_partial", retry=True)
            return transfer(resp, part, meta, config, current, info, offset, note)
    raise AssertionError("redirect loop escaped")


def decode(part, mime, config):
    cmd = [sys.executable, str(Path(__file__).with_name("stage1_decode.py")), str(part), mime,
           *(str(config[k]) for k in ("max_bytes", "max_pixels", "decode_memory", "decode_timeout"))]
    try:
        result = subprocess.run(cmd, capture_output=True, timeout=config["decode_timeout"], check=True)
        return json.loads(result.stdout)
    except subprocess.TimeoutExpired:
        return {"reason": "decode_timeout"}
    except (subprocess.CalledProcessError, ValueError):
        return {"reason": "decode_worker_error"}


def save_result(root, part, metadata, config, db, url, attempt, n, mime):
    raw_digest = digest(part)
    decoded = decode(part, mime, config)
    reason = decoded.get("reason")
    if not reason and decoded["sha256"] != raw_digest:
        raise ValueError("Decoder input changed before verification")
    if not reason:
        dest = root / "objects" / raw_digest
        # Keep the completed transfer until database publication is durable.
        try:
            os.link(part, dest)
        except FileExistsError:
            if digest(dest) != raw_digest:
                raise ValueError("Existing object digest mismatch")
        else:
            sync_dir(dest.parent)
    category = None
    if reason:
        category = ("resource" if reason.endswith("_limit") else
                    "format" if reason in {"unsupported_content_type", "image_mime_mismatch", "unidentified_image"}
                    else "decode")
    with db:
        event(db, url, attempt, "decoded", bytes=n, sha256=raw_digest, mime=mime, **{
            k: v for k, v in decoded.items() if k not in {"bytes", "sha256"}})
        db.execute("UPDATE source SET state=?, reason=?, category=?, digest=? WHERE url=?",
                   ("failed_terminal" if reason else "success_decode", reason, category, raw_digest, url))
    metadata.unlink(missing_ok=True)
    part.unlink(missing_ok=True)


def process(root, url, config, limiter, transport=response):
    part = root / "partials" / sha256(url.encode()).hexdigest()
    metadata = part.with_suffix(".json")
    with closing(connect(root)) as db:
        state = db.execute("SELECT * FROM source WHERE url=?", (url,)).fetchone()
        if state["state"] in TERMINAL:
            return
        if state["next"] > time.time():
            return
        if shutil.disk_usage(root).free < config["min_free_bytes"] + config["max_bytes"]:
            raise Pause("disk_reserve")
        attempt = state["attempt"] + 1

        def note(kind, **data):
            with db:
                event(db, url, attempt, kind, **data)
                if kind == "http" and data["status"] in {200, 206}:
                    db.execute("UPDATE source SET http_success=1 WHERE url=?", (url,))
                if kind == "cooldown":
                    db.execute("INSERT OR REPLACE INTO cooldown VALUES (?,?)", (data["host"], data["until"]))

        def on_request(current, host):
            note("request", final_url=current, host=host)

        try:
            if state["state"] == "success_http":
                completed = db.execute(
                    "SELECT data FROM events WHERE url=? AND kind='complete_bytes' ORDER BY id DESC LIMIT 1",
                    (url,),
                ).fetchone()
                details = json.loads(completed[0])
                if part.exists() and digest(part) == details["sha256"]:
                    save_result(root, part, metadata, config, db, url, state["attempt"],
                                details["bytes"], details["mime"])
                    return
                note("recovery", reason="completed_transfer_missing_or_changed")
            with db:
                event(db, url, attempt, "attempt_started")
                db.execute("UPDATE source SET state='inflight',started=COALESCE(started,?) WHERE url=?",
                           (time.time(), url))
            n, mime = download(url, part, metadata, config, limiter, note, on_request, transport)
            raw_digest = digest(part)
            with db:
                event(db, url, attempt, "complete_bytes", bytes=n, mime=mime, sha256=raw_digest)
                db.execute("UPDATE source SET state='success_http',complete_bytes=1,attempt=? WHERE url=?",
                           (attempt, url))
            save_result(root, part, metadata, config, db, url, attempt, n, mime)
        except Deferred as error:
            with db:
                event(db, url, attempt, "deferred", seconds=error.delay)
                db.execute("UPDATE source SET state='deferred',next=? WHERE url=?",
                           (time.time() + error.delay, url))
        except Failure as error:
            cycle_attempt = attempt - state["retry_floor"]
            when = time.time() + max(error.delay, config["backoff"] * 2**(cycle_attempt - 1))
            can_retry = error.retry and cycle_attempt < config["attempts"]
            new_state = ("deferred" if error.delay else "retryable") if can_retry else "failed_terminal"
            with db:
                event(db, url, attempt, "failure", reason=error.reason, category=error.category,
                      retryable=error.retry, state=new_state, next=when)
                db.execute("UPDATE source SET state=?,attempt=?,next=?,reason=?,category=? WHERE url=?",
                           (new_state, attempt, when, error.reason, error.category, url))
        except (Pause, OSError) as error:
            if isinstance(error, OSError) and error.errno not in {errno.ENOSPC, errno.EDQUOT}:
                raise
            note("paused", reason="disk_full" if isinstance(error, OSError) else str(error))
            with db:
                db.execute("UPDATE source SET state='queued' WHERE url=? AND state='inflight'", (url,))
            raise Pause("disk_full" if isinstance(error, OSError) else str(error)) from error


def verify_cache(db, root):
    verified = set()
    with db:
        for url, expected, attempt in db.execute("SELECT url,digest,attempt FROM source WHERE state='success_decode'"):
            path = root / "objects" / expected
            if expected in verified:
                continue
            if path.is_file() and digest(path) == expected:
                verified.add(expected)
                continue
            event(db, url, attempt, "integrity_failure", digest=expected)
            raise ValueError("Verified cache object missing or changed; restore the recorded digest before resuming")
        db.execute("UPDATE source SET state='queued' WHERE state='inflight'")


def dns_controls(config):
    def resolve_control(host):
        try:
            return bool(resolve(host, 443, config["connect_timeout"]))
        except Failure:
            return False

    with ThreadPoolExecutor(2) as executor:
        return any(list(executor.map(resolve_control, ("github.com", "example.com"))))


def resolver_fault_recent(db):
    recent = db.execute("""
        SELECT kind,data FROM events
        WHERE kind IN ('failure','http','decoded') ORDER BY id DESC LIMIT 12
    """).fetchall()
    return (len(recent) == 12 and all(
        row["kind"] == "failure" and json.loads(row["data"])["reason"] in ENVIRONMENT_DNS
        for row in recent))


def reopen_environment_failures(db, urls):
    allowed = set(urls)
    recovered = 0
    with db:
        for row in db.execute("SELECT * FROM source WHERE state='failed_terminal'").fetchall():
            if row["url"] not in allowed or row["reason"] not in ENVIRONMENT_DNS:
                continue
            event(db, row["url"], row["attempt"], "environment_reopened", prior_reason=row["reason"])
            db.execute("UPDATE source SET state='queued',next=0,retry_floor=attempt WHERE url=?", (row["url"],))
            recovered += 1
    return recovered


def run(root, db, urls, config, limiter):
    running = {}
    with ThreadPoolExecutor(max_workers=config["workers"]) as pool:
        try:
            while True:
                if running:
                    closed = [job for job in running if job.done()]
                    for job in closed:
                        job.result()
                        del running[job]
                    if closed and resolver_fault_recent(db) and not dns_controls(config):
                        return "environment_dns_unavailable"
                if len(running) == config["workers"]:
                    wait(running, return_when=FIRST_COMPLETED)
                    continue

                states = {r["url"]: r for r in db.execute("SELECT url,state,next FROM source")}
                active = set(running.values())
                pending = [url for url in urls if url not in active and states[url]["state"] not in TERMINAL]
                now = time.time()
                ready = [url for url in pending if states[url]["next"] <= now]
                for url in ready[:config["workers"] - len(running)]:
                    job = pool.submit(process, root, url, config, limiter)
                    running[job] = url
                if running:
                    wait(running, return_when=FIRST_COMPLETED)
                    continue
                if not pending:
                    return "COMPLETE"
                delay = min(states[url]["next"] for url in pending) - time.time()
                if delay > config["request_timeout"]:
                    return "deferred_cooldown"
                time.sleep(max(0, delay))
        finally:
            for job in running:
                job.cancel()


def load_config(path):
    config = yaml.safe_load(path.read_bytes())
    default = yaml.safe_load(DEFAULT_CONFIG.read_bytes())
    if (not isinstance(config, dict) or config.keys() != default.keys()
            or any(type(value) not in (float, int) or not 0 < value < 10**15 for value in config.values())):
        raise ValueError("Invalid download configuration")
    if any(type(config[k]) is not int for k in
           ("workers", "redirects", "attempts", "max_bytes", "max_pixels", "min_free_bytes",
            "decode_timeout", "decode_memory")):
        raise ValueError("Invalid integer configuration")
    if (any(config[k] > default[k] for k in default if k not in
            {"global_interval", "host_interval", "min_free_bytes", "backoff"})
            or any(config[k] < default[k] for k in ("global_interval", "host_interval", "backoff"))):
        raise ValueError("Download configuration exceeds the audited safety limits")
    return config


def smoke_gate(db, urls):
    states = {r["url"]: r for r in db.execute("SELECT * FROM source")}
    scope = [states[url] for url in urls]
    return (all(r["state"] in TERMINAL for r in scope)
            and any(r["state"] == "success_decode" for r in scope)
            and all(r["digest"] if r["state"] == "success_decode" else r["reason"] for r in scope))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(".local/stage1"))
    parser.add_argument("--config", type=Path, default=DEFAULT_CONFIG)
    parser.add_argument("--phase", choices=("smoke", "full"), default="smoke")
    flag = parser.add_mutually_exclusive_group()
    flag.add_argument("--dry-run", action="store_true")
    flag.add_argument("--execute", action="store_true")
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--retry-environment-dns", action="store_true")
    parser.add_argument("--max-requests", type=int)
    args = parser.parse_args()
    if args.max_requests is not None and args.max_requests < 0:
        parser.error("Request limit must be nonnegative")
    if args.retry_environment_dns and not (args.resume and args.execute):
        parser.error("DNS recovery requires --execute --resume")
    config = load_config(args.config)
    rows = pinned_rows(args.csv)
    smoke = smoke_rows(rows)
    smoke_urls = sorted({row[1] for row in smoke})
    assert 40 <= len(smoke) <= 60
    urls = smoke_urls if args.phase == "smoke" else list(dict.fromkeys(row[1] for row in (*smoke, *rows)))
    print(json.dumps({"phase": args.phase, "dry_run": not args.execute, "resume": args.resume,
                      "selected_uuid": len(smoke) if args.phase == "smoke" else len(rows),
                      "selected_url": len(urls), "config": config, "python": sys.version.split()[0],
                      "csv_sha256": CSV_SHA256, "utc_epoch": time.time()}, sort_keys=True), flush=True)
    if not args.execute:
        return 0
    root = args.root.resolve()
    if not args.resume and (root / "audit.sqlite").exists():
        parser.error("Existing state requires --resume")
    root.mkdir(parents=True, mode=0o700, exist_ok=True)
    for name in ("partials", "objects"):
        (root / name).mkdir(mode=0o700, exist_ok=True)
    with (root / "run.lock").open("a") as lock, closing(connect(root)) as db:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        initialize(db, rows)
        verify_cache(db, root)
        before = smoke_gate(db, smoke_urls)
        if args.phase == "full" and not db.execute("SELECT 1 FROM meta WHERE key='smoke_pass'").fetchone():
            parser.error("BLOCK: Full audit requires successful smoke and no-request resume")
        atomic(root / "smoke_selection.json", canonical([row[0] for row in smoke]))
        limiter = Limiter(config, args.max_requests, dict(db.execute("SELECT * FROM cooldown")))
        try:
            if (args.retry_environment_dns or resolver_fault_recent(db)) and not dns_controls(config):
                result = "environment_dns_unavailable"
            else:
                if args.retry_environment_dns:
                    print(json.dumps({"environment_dns_reopened_urls": reopen_environment_failures(db, urls)}),
                          flush=True)
                result = run(root, db, urls, config, limiter)
        except sqlite3.OperationalError as error:
            if error.sqlite_errorcode != sqlite3.SQLITE_FULL:
                raise
            result = "disk_full"
        except (Pause, KeyboardInterrupt) as error:
            result = str(error) or "interrupted"
        after = smoke_gate(db, smoke_urls)
        if (result == "COMPLETE" and args.phase == "smoke" and args.resume and before and after
                and limiter.requests == 0):
            with db:
                db.execute("INSERT OR IGNORE INTO meta VALUES ('smoke_pass',?)", (str(time.time()),))
        with db:
            db.execute("INSERT OR REPLACE INTO meta VALUES (?,?)", (f"{args.phase}_last_stop", result))
        db.execute("PRAGMA wal_checkpoint(PASSIVE)")
        print(json.dumps({"result": result, "requests_admitted": limiter.requests, "smoke_covered": after,
                          "smoke_pass": bool(db.execute("SELECT 1 FROM meta WHERE key='smoke_pass'").fetchone())}),
              flush=True)
    return 0 if result == "COMPLETE" and (args.phase == "full" or after) else 2


if __name__ == "__main__":
    raise SystemExit(main())
