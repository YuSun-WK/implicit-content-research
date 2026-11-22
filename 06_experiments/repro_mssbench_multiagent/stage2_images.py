"""Verify only the frozen Stage 2 image paths, downloading absent files."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from collections import Counter
import csv
from pathlib import Path

from stage1_data import verify_asset


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--audit", type=Path, required=True)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    with args.manifest.open(newline="") as stream:
        rows = list(csv.DictReader(stream))
    if len(rows) != 200 or len({row["image_path"] for row in rows}) != 200:
        raise ValueError("expected exactly 200 distinct frozen image paths")
    root = args.data_root.resolve(strict=True)
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(lambda row: verify_asset(root, row, args.download), rows))
    with args.audit.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(results[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(results)
    counts = Counter(row["status"] for row in results)
    print("images", dict(counts), "downloaded", sum(row["source"] == "download" for row in results),
          "verified bytes", sum(row["actual_bytes"] or 0 for row in results), flush=True)
    return 0 if counts == {"PASS": 200} else 1


if __name__ == "__main__":
    raise SystemExit(main())
