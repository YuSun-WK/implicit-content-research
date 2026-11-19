"""Generate aggregate coverage and an immutable private UUID snapshot."""

import argparse
from collections import Counter, defaultdict
from contextlib import closing
import csv
from hashlib import sha256
import json
from pathlib import Path
from statistics import median
from urllib.parse import urlsplit

from stage0_audit_csv import CSV_SHA256, EXTRA, FIGURE9_LEGEND, GRADE_FIELDS
from stage1_download import ENVIRONMENT_DNS, atomic, connect, digest
from stage1_manifest import canonical, make_manifest, pinned_rows, smoke_rows

KEY_PATTERNS = ("S-S-S", "S-S-B", "S-S-U", "U-S-B", "U-S-U", "B-B-U")


def coverage(rows, statuses, attempted):
    counts = Counter()
    for row in rows:
        url = row[1]
        state = statuses[url]
        counts["n"] += 1
        counts["decoded"] += state["state"] == "success_decode"
        counts["failed"] += state["state"] == "failed_terminal"
        counts["not_attempted"] += url not in attempted
        counts["attempted_pending"] += url in attempted and state["state"] not in {
            "success_decode", "failed_terminal"}
    return {k: counts[k] for k in ("n", "decoded", "failed", "not_attempted", "attempted_pending")} | {
        "coverage": counts["decoded"] / counts["n"] if counts["n"] else None}


def classify(rows, statuses, attempted):
    by_pattern = defaultdict(list)
    by_label = defaultdict(list)
    for row in rows:
        by_pattern[row[5]].append(row)
        for field, label in zip(GRADE_FIELDS, row[2:5], strict=True):
            by_label[field, label].append(row)
    pattern = [
        {"pattern": group, "group": ("paper17" if group in FIGURE9_LEGEND else
                                     "release_extra" if group in EXTRA else "image_not_sure"),
         **coverage(by_pattern[group], statuses, attempted)}
        for group in sorted(set(FIGURE9_LEGEND) | set(EXTRA) | {key for key in by_pattern if key[0] == "?"})
    ]
    labels = [{"field": field, "label": label, **coverage(by_label[field, label], statuses, attempted)}
              for field, label in sorted(by_label)]
    return pattern, labels


def smoke_at_gate(rows, events, passed_at):
    states = {row[1]: {"state": "queued"} for row in rows}
    attempted = set()
    for event in events:
        url = event["url"]
        if event["at"] > passed_at or url not in states:
            continue
        kind = event["kind"]
        detail = json.loads(event["data"])
        if kind == "attempt_started":
            attempted.add(url)
            states[url] = {"state": "inflight"}
        elif kind == "failure":
            states[url] = {"state": detail.get("state", "failed_terminal")}
        elif kind == "decoded":
            states[url] = {"state": "failed_terminal" if detail.get("reason") else "success_decode"}
        elif kind == "environment_reopened":
            states[url] = {"state": "queued"}
    return states, attempted


def host_count(urls):
    hosts = set()
    for url in urls:
        try:
            host = urlsplit(url).hostname
        except ValueError:
            continue
        if host:
            hosts.add(host.lower().rstrip("."))
    return len(hosts)


def csv_report(path, rows, columns):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=columns, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def build(root, out, rows):
    with closing(connect(root)) as db:
        db.execute("BEGIN")
        assert db.execute("SELECT value FROM meta WHERE key='csv_sha256'").fetchone()[0] == CSV_SHA256
        if set(rows) != set(map(tuple, db.execute("SELECT * FROM release"))):
            raise ValueError("Database roster differs from the verified release")
        statuses = {r["url"]: dict(r) for r in db.execute("SELECT * FROM source")}
        events = list(db.execute("SELECT * FROM events ORDER BY id"))
        metadata = dict(db.execute("SELECT * FROM meta"))
        smoke_pass = "smoke_pass" in metadata
    attempted = {r["url"] for r in events if r["kind"] == "attempt_started"}
    requested = {r["url"] for r in events if r["kind"] == "request"}
    release = coverage(rows, statuses, attempted)
    smoke_scope = smoke_rows(rows)
    smoke_states, smoke_attempted = (
        smoke_at_gate(smoke_scope, events, float(metadata["smoke_pass"]))
        if smoke_pass else (statuses, attempted)
    )
    smoke = coverage(smoke_scope, smoke_states, smoke_attempted)
    pattern, labels = classify(rows, statuses, attempted)
    smoke_pattern, _ = classify(smoke_scope, smoke_states, smoke_attempted)
    terminal_fail = {u for u, s in statuses.items() if s["state"] == "failed_terminal"}
    digests = {url: s["digest"] for url, s in statuses.items() if s["state"] == "success_decode"}
    for expected in set(digests.values()):
        if digest(root / "objects" / expected) != expected:
            raise ValueError("Verified download object changed or became unavailable")
    scripts = Path(__file__).parent
    source_files = [*scripts.glob("stage1*.py"), *scripts.glob("stage0*.py")]
    code_hash = sha256(canonical({p.name: digest(p) for p in sorted(source_files)})).hexdigest()
    manifest = make_manifest(rows, digests, code_hash)
    data = canonical(manifest)
    manifest_hash = sha256(data).hexdigest()
    snapshots = root / "snapshots"
    snapshots.mkdir(exist_ok=True, mode=0o700)
    manifest_path = snapshots / f"{manifest_hash}.json"
    if not manifest_path.exists():
        atomic(manifest_path, data)
    if digest(manifest_path) != manifest_hash:
        raise ValueError("Existing manifest digest mismatch")
    failure_groups = defaultdict(set)
    for url in terminal_fail:
        s = statuses[url]
        failure_groups[s["category"], s["reason"]].add(url)
    failure_counts = Counter(statuses[row[1]]["reason"] for row in rows if row[1] in terminal_fail)
    failures = [{"category": category, "reason": reason, "url_n": len(urls),
                 "uuid_n": failure_counts[reason], "original_host_n": host_count(urls)}
                for (category, reason), urls in sorted(failure_groups.items())]
    durations = []
    active = {}
    last_body = {}
    successful_decode_urls = set()
    re_requests = 0
    event_reasons = Counter()
    for event in events:
        url, attempt, kind, at = (event[k] for k in ("url", "attempt", "kind", "at"))
        if kind == "attempt_started":
            active[url, attempt] = at
        if kind in {"decoded", "failure"} and (url, attempt) in active:
            durations.append(max(0, at - active.pop((url, attempt))))
        detail = json.loads(event["data"])
        if kind == "complete_bytes":
            last_body[url] = detail["bytes"]
        if kind == "decoded" and not detail.get("reason"):
            successful_decode_urls.add(url)
        if kind == "request" and url in successful_decode_urls:
            re_requests += 1
        if kind in {"decoded", "failure", "partial_discard"} and detail.get("reason"):
            event_reasons[detail["reason"]] += 1
    durations.sort()
    summary = {
        "status": "FULL" if release["decoded"] + release["failed"] == len(rows) and smoke_pass else "PARTIAL",
        "csv_sha256": CSV_SHA256, "paper_n": 8187, "release_n": len(rows),
        "requestable_uuid": len(rows), "unique_urls": len(statuses),
        "duplicate_url_additional_uuid": len(rows) - len(statuses), "attempted_urls": len(attempted),
        "requested_urls": len(requested), "unattempted_urls": len(statuses) - len(attempted),
        "http_200_or_206_urls": sum(s["http_success"] for s in statuses.values()),
        "complete_body_urls": sum(s["complete_bytes"] for s in statuses.values()),
        "complete_body_bytes": sum(last_body.values()),
        "catalogued_verified_url_rerequests": re_requests,
        "environment_dns_terminal_urls": sum(statuses[u]["reason"] in ENVIRONMENT_DNS for u in terminal_fail),
        "decoded_urls": len(digests), "decoded_unique_content_hashes": len(set(digests.values())),
        "failed_urls": len(terminal_fail), "http_failure_original_host_n": host_count(
            u for u in terminal_fail if statuses[u]["category"] == "http"),
        "decode_or_format_failed_urls": sum(statuses[u]["complete_bytes"] and
            statuses[u]["category"] in {"format", "decode", "resource"} for u in terminal_fail),
        "resource_limit_terminal_urls": sum(statuses[u]["category"] == "resource" for u in terminal_fail),
        "release_uuid": release,
        "smoke_uuid": smoke, "smoke_pass": smoke_pass,
        "smoke_last_stop": metadata.get("smoke_last_stop", "NOT RUN"),
        "full_last_stop": metadata.get("full_last_stop", "NOT RUN"),
        "smoke_unique_urls": len({r[1] for r in smoke_scope}),
        "manifest_sha256": manifest_hash, "download_snapshot_sha256": manifest["download_snapshot_sha256"],
        "cohort_counts": {key: len(value) for key, value in manifest["cohorts"].items()},
        "event_reasons": dict(event_reasons),
        "attempt_seconds": {"n": len(durations), "median": round(median(durations), 3) if durations else None,
                            "p95": round(durations[(95 * len(durations) + 99) // 100 - 1], 3) if durations else None},
        "classification": "NOT RUN",
    }
    out.mkdir(parents=True, exist_ok=True)
    atomic(out / "coverage_summary.json", canonical(summary))
    atomic(out / "coverage_manifest.sha256", f"{manifest_hash}  {manifest_hash}.json\n".encode())
    csv_report(out / "coverage_by_pattern.csv", pattern, list(pattern[0]))
    csv_report(out / "smoke_coverage_by_pattern.csv", smoke_pattern, list(smoke_pattern[0]))
    csv_report(out / "coverage_by_label.csv", labels, list(labels[0]))
    csv_report(out / "coverage_by_failure_type.csv", failures,
               ["category", "reason", "url_n", "uuid_n", "original_host_n"])
    with (root / "private_failure_roster.jsonl").open("wb") as stream:
        for row in rows:
            if row[1] in attempted and statuses[row[1]]["state"] != "success_decode":
                stream.write(canonical({"uuid": row[0], "original_url": row[1], "pattern": row[5],
                                       "state": statuses[row[1]]["state"], "reason": statuses[row[1]]["reason"]}))

    md = [
        "# Stage 1 image coverage",
        "",
        f"**{summary['status']}** · Paper 8,187 (AUTHOR-REPORTED), release {len(rows):,} (PINNED CSV).",
        "",
        f"Smoke gate {'PASS' if smoke_pass else 'BLOCK'}. The smoke includes {smoke['n']} UUIDs and "
        f"{summary['smoke_unique_urls']} unique URLs, with {smoke['decoded']} decoded UUIDs "
        f"and {smoke['failed']} terminal failures at the gate. Observed full-release UUID coverage is "
        f"{release['decoded']}/{len(rows)} ({release['coverage']:.2%}).",
        "",
        f"Unique URLs: {summary['unique_urls']:,} total, {len(attempted):,} attempted under the URL policy, "
        f"{len(requested):,} admitted for network request, {summary['unattempted_urls']:,} not attempted.",
        f"HTTP 200/206: {summary['http_200_or_206_urls']:,}; validated complete bodies: "
        f"{summary['complete_body_urls']:,} bodies ({summary['complete_body_bytes']:,} bytes); "
        f"decoded URL images: {len(digests):,}.",
        f"UUID outcomes: {release['decoded']} decoded, {release['failed']} failed terminally, "
        f"{release['attempted_pending']} attempted and unresolved, {release['not_attempted']} not attempted.",
        "",
        f"Last smoke stop: `{summary['smoke_last_stop']}`. Last full-run stop: `{summary['full_last_stop']}`. "
        f"{summary['environment_dns_terminal_urls']} URLs exhausted the transient DNS attempt budget. "
        "These outcomes remain eligible for the documented environment retry.",
        f"Requests after successful decode for the same URL: {re_requests}.",
        "",
        "| Task cohort | Count | Pinned-release gold ceiling |", "|---|---:|---:|",
    ]
    ceilings = {"release_roster": len(rows), "joint_decoded": len(rows),
                "image_decoded_gold": sum(r[2] != "not_sure" for r in rows),
                "text_only_eligible": len(rows), "three_modality_intersection": sum(r[2] != "not_sure" for r in rows)}
    md.extend(f"| {key} | {n:,} | {ceilings[key]:,} |" for key, n in summary["cohort_counts"].items())
    md.extend(["", "The Figure 4/5 intersection is a pre-inference ceiling. E2, E3 and E5 share the joint list.",
               "", "| Priority pattern | Decoded UUID | Release UUID | Coverage | Terminal failures | Not attempted |",
               "|---|---:|---:|---:|---:|---:|"])
    pmap = {r["pattern"]: r for r in pattern}
    for key in KEY_PATTERNS:
        group = pmap[key]
        rate = f"{group['coverage']:.2%}" if group["n"] else "N/A"
        md.append(f"| {key} | {group['decoded']} | {group['n']} | {rate} | "
                  f"{group['failed']} | {group['not_attempted']} |")
    md.extend(["", "The smoke intentionally oversamples rare patterns. Its outcomes do not estimate "
               "overall image availability. Compare the per-pattern and modality-label tables for observed "
               "failure concentration and incomplete coverage. Image semantics and historical identity are "
               "UNKNOWN. Classification accuracy, F1 and model performance are NOT RUN.",
               "", f"Private immutable UUID manifest SHA-256 `{manifest_hash}`.", ""])
    atomic(out / "Stage1_Image_Coverage.md", "\n".join(md).encode())
    print(json.dumps(summary, sort_keys=True))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(".local/stage1"))
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--out", type=Path, default=Path("reports/stage1"))
    args = parser.parse_args()
    build(args.root, args.out, pinned_rows(args.csv))


if __name__ == "__main__":
    main()
