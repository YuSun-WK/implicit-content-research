"""Bounded fixed-revision curl fallback in frozen expansion order."""
import argparse
import csv
import hashlib
import json
import subprocess
import time
from pathlib import Path
from urllib.parse import quote

from build_test_manifest import REVISION, verify_image

ROOT = Path(__file__).resolve().parents[1]
BASE = "https://huggingface.co/datasets/Sandy124/TriggerBench/resolve/"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--max-files", type=int, default=80)
    ap.add_argument("--max-seconds", type=int, default=600)
    ap.add_argument("--uids-file", type=Path)
    ap.add_argument("--retry-failed", action="store_true")
    args = ap.parse_args()
    with (ROOT / "artifacts/manifests/test_manifest.csv").open() as f:
        rows = {r["sample_uid"]: r for r in csv.DictReader(f)}
    expansion = json.loads((ROOT / "artifacts/stage2_expansion_queue_v1.json").read_text())
    if args.uids_file:
        selected = json.loads(args.uids_file.read_text())
        if (selected["dataset_revision"] != REVISION
                or selected["source_queue_sha256"] != hashlib.sha256(
                    (ROOT / "artifacts/stage2_expansion_queue_v1.json").read_bytes()).hexdigest()
                or selected["count"] != len(selected["sample_uids"])
                or len(set(selected["sample_uids"])) != selected["count"]
                or not set(selected["sample_uids"]).issubset(rows)):
            raise ValueError("UID list differs from frozen source")
        ordered = selected["sample_uids"]
    else:
        ordered = [f"{pid}/{side}" for pid in expansion["full_pairs"] for side in ("safe", "unsafe")]
    log = ROOT / "runs/stage2_curl_attempts.jsonl"
    attempted = ({json.loads(line)["sample_uid"] for line in log.read_text().splitlines()}
                 if log.exists() and not args.retry_failed else set())
    start = time.monotonic()
    count = 0
    for uid in ordered:
        if count >= args.max_files or time.monotonic()-start >= args.max_seconds:
            break
        row = rows[uid]
        expected = row["expected_image_sha256"]
        path = ROOT / "images" / row["hf_image_path"]
        if path.exists():
            verify_image(path, expected)
            continue
        if row["run_status"] == "READY":
            verify_image(Path(row["image_local_path"]), expected)
            continue
        if uid in attempted:
            continue
        count += 1
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".partial")
        url = f"{BASE}{REVISION}/{quote(row['hf_image_path'])}"
        result = {"sample_uid": uid, "dataset_revision": REVISION,
                  "expected_sha256": expected, "method": "curl_range_resume"}
        started = time.monotonic()
        for attempt in range(2):
            resume = ["--continue-at", "-"] if temporary.exists() and temporary.stat().st_size else []
            completed = subprocess.run(["curl", "-fsSL", "--connect-timeout", "5",
                "--max-time", "20", *resume, url, "-o", str(temporary)],
                capture_output=True, text=True)
            if completed.returncode == 0:
                try:
                    image_sha, _, _ = verify_image(temporary, expected)
                    temporary.replace(path)
                    result.update(status="READY", image_sha256=image_sha)
                    break
                except (OSError, ValueError, SyntaxError) as exc:
                    temporary.unlink(missing_ok=True)
                    result.update(status="DOWNLOAD_INVALID", error=str(exc)[:250])
                    break
            result.update(status="DOWNLOAD_FAILED", curl_exit=completed.returncode,
                          error=completed.stderr[-250:])
            if completed.returncode in (22, 33, 36):
                temporary.unlink(missing_ok=True)
        result["seconds"] = round(time.monotonic()-started, 3)
        with log.open("a") as f:
            f.write(json.dumps(result) + "\n")
            f.flush()
        print(json.dumps(result), flush=True)


if __name__ == "__main__":
    main()
