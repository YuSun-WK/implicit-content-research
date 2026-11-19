"""Read-only integrity check and private inventory of a stopped acquisition."""

import argparse
from collections import Counter
from contextlib import closing
import fcntl
from hashlib import sha256
import json
from pathlib import Path
import sqlite3

from stage0_audit_csv import CSV_SHA256
from stage1_download import digest
from stage1_manifest import canonical, pinned_rows, verified_manifest


def check_state(root, release_csv):
    root = root.resolve()
    rows = pinned_rows(release_csv)
    db_path = root / "audit.sqlite"
    with (root / "run.lock").open("rb") as lock:
        fcntl.flock(lock, fcntl.LOCK_SH | fcntl.LOCK_NB)
        with closing(sqlite3.connect(f"{db_path.as_uri()}?mode=ro", uri=True)) as db:
            db.execute("BEGIN")
            if db.execute("PRAGMA integrity_check").fetchall() != [("ok",)]:
                raise ValueError("SQLite integrity_check failed")
            metadata = dict(db.execute("SELECT * FROM meta"))
            if metadata.get("csv_sha256") != CSV_SHA256:
                raise ValueError("Stored release digest mismatch")
            if set(rows) != set(db.execute("SELECT * FROM release")):
                raise ValueError("Stored UUID/URL/label roster differs from release")
            states = list(db.execute("SELECT url,state,digest FROM source"))
            if {r[0] for r in states} != {r[1] for r in rows}:
                raise ValueError("Stored URL roster differs from release")
            history_events = db.execute("SELECT COUNT(*) FROM events").fetchone()[0]

        files = {}
        for path in sorted(root.rglob("*")):
            if path.is_symlink():
                raise ValueError("Unexpected symlink in acquisition root")
            if path.is_file() and path.name not in {"run.lock", "audit.sqlite-shm"}:
                if path.name == "audit.sqlite-wal" and path.stat().st_size == 0:
                    continue
                files[path.relative_to(root).as_posix()] = digest(path)

        objects = {name.removeprefix("objects/"): value for name, value in files.items()
                   if name.startswith("objects/")}
        if any(name != value for name, value in objects.items()):
            raise ValueError("An object hash differs from its filename")
        decoded = {hex_digest for _, state, hex_digest in states if state == "success_decode"}
        if decoded - objects.keys():
            raise ValueError("Verified cache objects missing")

        snapshots = [name for name in files if name.startswith("snapshots/") and name.endswith(".json")]
        for name in snapshots:
            snapshot_path = root / name
            if snapshot_path.stem != files[name]:
                raise ValueError("Snapshot digest differs from its filename")
            snapshot, _ = verified_manifest(snapshot_path, files[name], release_csv)
            if set(snapshot["image_sha256_by_uuid"].values()) - objects.keys():
                raise ValueError("A historical snapshot references missing objects")

        summary = {
            "sqlite_integrity": "ok",
            "release_n": len(rows),
            "source_n": len(states),
            "source_states": dict(Counter(r[1] for r in states)),
            "history_events": history_events,
            "verified_decoded_objects": len(decoded),
            "object_files": len(objects),
            "partial_files": sum(name.startswith("partials/") for name in files),
            "verified_snapshots": len(snapshots),
            "inventory_sha256": sha256(canonical(files)).hexdigest(),
        }
        return summary, files


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--root", type=Path, default=Path(".local/stage1"))
    inventory = parser.add_mutually_exclusive_group()
    inventory.add_argument("--write-inventory", type=Path)
    inventory.add_argument("--check-inventory", type=Path)
    args = parser.parse_args()
    if args.write_inventory and args.write_inventory.resolve().is_relative_to(args.root.resolve()):
        parser.error("Write the private inventory outside the acquisition root")
    summary, files = check_state(args.root, args.csv)
    if args.check_inventory:
        if args.check_inventory.read_bytes() != canonical(files):
            raise ValueError("Acquisition inventory differs from its source")
        summary["inventory_comparison"] = "PASS"
    if args.write_inventory:
        with args.write_inventory.open("xb") as stream:
            args.write_inventory.chmod(0o600)
            stream.write(canonical(files))
    print(json.dumps(summary, sort_keys=True))


if __name__ == "__main__":
    main()
