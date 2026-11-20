"""Bounded fixed-revision Hub fetch for frozen Stage 2 images."""
import argparse
import csv
import json
import shutil
import time
from pathlib import Path

from huggingface_hub import hf_hub_download
from build_test_manifest import REVISION, verify_image

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=("validation", "full"), required=True)
    ap.add_argument("--max-files", type=int, default=100)
    args = ap.parse_args()
    with (ROOT / "artifacts/manifests/test_manifest.csv").open() as f:
        rows = {r["sample_uid"]: r for r in csv.DictReader(f)}
    queues = json.loads((ROOT / "artifacts/stage2_queues_v1.json").read_text())
    ordered = queues["a1_validation"] if args.scope == "validation" else list(rows)
    log = ROOT / "runs/stage2_download_attempts.jsonl"
    count = 0
    for uid in ordered:
        row = rows[uid]
        path = ROOT / "images" / row["hf_image_path"]
        expected = row["expected_image_sha256"]
        if path.is_file():
            verify_image(path, expected)
            continue
        if row["run_status"] == "READY":
            verify_image(Path(row["image_local_path"]), expected)
            continue
        if count >= args.max_files:
            break
        count += 1
        start = time.monotonic()
        result = dict(scope=args.scope, sample_uid=uid, expected_sha256=expected,
                      dataset_revision=REVISION)
        try:
            cached = Path(hf_hub_download("Sandy124/TriggerBench", row["hf_image_path"],
                repo_type="dataset", revision=REVISION, token=False,
                cache_dir=ROOT / ".local/hf_stage2", etag_timeout=7))
            verify_image(cached, expected)
            path.parent.mkdir(parents=True, exist_ok=True)
            temporary = path.with_suffix(".hf_partial")
            shutil.copyfile(cached, temporary)
            verify_image(temporary, expected)
            temporary.replace(path)
            result["status"] = "READY"
        except Exception as exc:
            result.update(status="DOWNLOAD_FAILED", error_type=type(exc).__name__, error=str(exc)[:300])
        result["seconds"] = round(time.monotonic()-start, 3)
        with log.open("a") as f:
            f.write(json.dumps(result) + "\n")
            f.flush()
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
