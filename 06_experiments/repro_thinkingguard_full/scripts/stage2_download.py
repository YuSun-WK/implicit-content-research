"""Bounded fixed-revision Hub fetch for frozen Stage 2 images."""
import argparse
import csv
import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

from huggingface_hub import hf_hub_download
from build_test_manifest import REVISION, verify_image

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=("validation", "full"), required=True)
    ap.add_argument("--max-files", type=int, default=100)
    ap.add_argument("--one-uid", help=argparse.SUPPRESS)
    ap.add_argument("--per-file-seconds", type=int, default=75)
    args = ap.parse_args()
    with (ROOT / "artifacts/manifests/test_manifest.csv").open() as f:
        rows = {r["sample_uid"]: r for r in csv.DictReader(f)}
    queues = json.loads((ROOT / "artifacts/stage2_queues_v1.json").read_text())
    expansion = json.loads((ROOT / "artifacts/stage2_expansion_queue_v1.json").read_text())
    ordered = ([args.one_uid] if args.one_uid else queues["a1_validation"]
               if args.scope == "validation" else
               [f"{pid}/{side}" for pid in expansion["full_pairs"] for side in ("safe", "unsafe")])
    log = ROOT / "runs/stage2_download_attempts.jsonl"
    attempted = set()
    if args.scope == "full" and not args.one_uid and log.exists():
        attempted = {json.loads(line)["sample_uid"] for line in log.read_text().splitlines()
                     if json.loads(line)["scope"] == "full"}
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
        if uid in attempted:
            continue
        if count >= args.max_files:
            break
        count += 1
        if not args.one_uid:
            try:
                child = subprocess.run([sys.executable, str(Path(__file__).resolve()),
                    "--scope", args.scope, "--one-uid", uid, "--max-files", "1"],
                    capture_output=True, text=True, timeout=args.per_file_seconds,
                    env=__import__("os").environ.copy())
                result = json.loads(child.stdout.strip().splitlines()[-1])
            except (subprocess.TimeoutExpired, IndexError, json.JSONDecodeError) as exc:
                result = dict(scope=args.scope, sample_uid=uid, expected_sha256=expected,
                              dataset_revision=REVISION, status="DOWNLOAD_FAILED",
                              error_type=type(exc).__name__, error=str(exc)[:300],
                              seconds=args.per_file_seconds)
            with log.open("a") as f:
                f.write(json.dumps(result) + "\n")
                f.flush()
            print(json.dumps(result), flush=True)
            continue
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
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
