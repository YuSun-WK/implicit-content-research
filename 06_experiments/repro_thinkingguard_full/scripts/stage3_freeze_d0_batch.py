"""Freeze the available complete pairs in one official D0 expansion slice."""
import argparse
import csv
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from build_test_manifest import verify_image
from run_resumeable_inference import ROOT


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--start-pair", type=int, required=True)
    ap.add_argument("--slice-pairs", type=int, default=100)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--exclude-queue", type=Path, action="append", default=[],
                    help="Previously frozen queue in the same slice; exclude its selected pairs")
    args = ap.parse_args()
    if args.start_pair < 100 or not 1 <= args.slice_pairs <= 100 or args.start_pair+args.slice_pairs > 868:
        raise ValueError("Invalid official expansion slice")
    expansion_path = ROOT / "artifacts/stage2_expansion_queue_v1.json"
    expansion = json.loads(expansion_path.read_text())
    excluded = set()
    for prior_path in args.exclude_queue:
        prior = json.loads(prior_path.read_text())
        if (prior["protocol"] != "d0" or prior["start_pair"] != args.start_pair
                or prior["slice_pairs"] != args.slice_pairs
                or prior["expansion_queue_sha256"] != sha(expansion_path)):
            raise ValueError(f"Prior queue has different slice/source: {prior_path}")
        if excluded.intersection(prior["selected_pairs"]):
            raise ValueError(f"Overlapping prior queues: {prior_path}")
        excluded.update(prior["selected_pairs"])
    with (ROOT / "artifacts/manifests/test_manifest.csv").open() as f:
        rows = {r["sample_uid"]: r for r in csv.DictReader(f)}
    chosen = []
    missing = []
    for pid in expansion["full_pairs"][args.start_pair:args.start_pair+args.slice_pairs]:
        if pid in excluded:
            continue
        status = []
        for side in ("safe", "unsafe"):
            row = rows[f"{pid}/{side}"]
            local = ROOT / "images" / row["hf_image_path"]
            if not local.is_file() and row["run_status"] == "READY":
                local = Path(row["image_local_path"])
            if local.is_file():
                verify_image(local, row["expected_image_sha256"])
                status.append(True)
            else:
                status.append(False)
        (chosen if all(status) else missing).append(pid)
    data = dict(protocol="d0", start_pair=args.start_pair, slice_pairs=args.slice_pairs,
                expansion_queue_sha256=sha(expansion_path),
                manifest_sha256=sha(ROOT / "artifacts/manifests/test_manifest.csv"),
                selected_pairs=chosen, missing_pairs_at_freeze=missing,
                frozen_utc=datetime.now(timezone.utc).isoformat())
    if args.output.exists():
        raise FileExistsError(f"Batch queue already frozen: {args.output}")
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"selected":len(chosen),"missing":len(missing),"sha256":sha(args.output)}))


if __name__ == "__main__":
    main()
