"""Retry unavailable frozen-queue images through the installed Hub client."""
import argparse
import csv
import json
import shutil
import time
from pathlib import Path

from huggingface_hub import hf_hub_download

from build_test_manifest import REVISION, digest, load_frozen_tree, verify_image
from run_resumeable_inference import ROOT


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path)
    parser.add_argument("--stage", choices=("smoke", "validation", "pilot"), required=True)
    parser.add_argument("--cache", type=Path, required=True)
    parser.add_argument("--image-root", type=Path, default=ROOT / "images")
    args = parser.parse_args()
    queued_data = (ROOT / "artifacts/sample_queues.json").read_bytes()
    freeze = json.loads((ROOT / "artifacts/parser_freeze.json").read_text())
    if digest(queued_data) != freeze["queue_sha256"]:
        raise ValueError("Queue hash differs from freeze record")
    queue = json.loads(queued_data)[args.stage]
    entries = load_frozen_tree(ROOT / "artifacts/dataset_source_tree.csv")
    if entries["revision"] != REVISION:
        raise ValueError("Source tree revision mismatch")
    with args.manifest.open() as handle:
        rows = {row["sample_uid"]: row for row in csv.DictReader(handle)}
    for uid in queue:
        row = rows[uid]
        expected = entries["files"][row["hf_image_path"]]["sha256"]
        if not expected or row["expected_image_sha256"] != expected or row["dataset_revision"] != REVISION:
            raise ValueError(f"Manifest does not match frozen image identity: {uid}")
        if row["run_status"] == "READY":
            verify_image(Path(row["image_local_path"]), expected)
            continue
        path = args.image_root / row["hf_image_path"]
        if path.exists():
            verify_image(path, expected)
            continue
        result = {"sample_uid": uid, "expected_image_sha256": expected}
        start = time.monotonic()
        try:
            cached = Path(hf_hub_download("Sandy124/TriggerBench", row["hf_image_path"],
                                         repo_type="dataset", revision=REVISION, token=False,
                                         cache_dir=args.cache, etag_timeout=7))
            observed, _, _ = verify_image(cached, expected)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix(".hf_partial")
            shutil.copyfile(cached, temporary)
            temporary.replace(path)
            result.update(download_status="DOWNLOADED", image_sha256=observed)
        except Exception as exc:
            result.update(download_status="DOWNLOAD_FAILED", error_type=type(exc).__name__)
        result["transfer_seconds"] = round(time.monotonic()-start, 3)
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
