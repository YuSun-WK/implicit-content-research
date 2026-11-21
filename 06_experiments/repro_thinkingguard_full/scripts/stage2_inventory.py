"""Verify every fixed Test image and publish pair-level coverage status."""
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from build_test_manifest import REVISION, verify_image
from run_resumeable_inference import ROOT, write


def main():
    with (ROOT / "artifacts/manifests/test_manifest.csv").open() as f:
        rows = list(csv.DictReader(f))
    with (ROOT / "artifacts/dataset_source_tree.csv").open() as f:
        tree = {r["path"]: r["lfs_sha256"] for r in csv.DictReader(f)}
    latest = {}
    for name in ("stage2_download_attempts.jsonl", "stage2_curl_attempts.jsonl"):
        path = ROOT / "runs" / name
        if path.exists():
            for line in path.read_text().splitlines():
                attempt = json.loads(line)
                latest[attempt["sample_uid"]] = {"source": name, "status": attempt["status"],
                    "error": attempt.get("error"), "seconds": attempt.get("seconds")}
    items = []
    groups = defaultdict(list)
    for row in rows:
        uid = row["sample_uid"]
        expected = row["expected_image_sha256"]
        if row["dataset_revision"] != REVISION or tree.get(row["hf_image_path"]) != expected:
            raise ValueError(f"Frozen source mismatch: {uid}")
        local = ROOT / "images" / row["hf_image_path"]
        if not local.is_file() and row["run_status"] == "READY":
            local = Path(row["image_local_path"])
        status = "MISSING"
        detail = latest.get(uid)
        if local.is_file():
            try:
                verify_image(local, expected)
                status = "READY"
            except (OSError, ValueError, SyntaxError) as exc:
                status = "INVALID_IMAGE"
                detail = {"error": str(exc)[:300]}
        item = {"sample_uid": uid, "pair_id": row["pair_id"], "category": row["category"],
                "side": row["side"], "status": status, "expected_image_sha256": expected,
                "last_attempt": detail if status != "READY" else None}
        items.append(item)
        groups[row["pair_id"]].append(item)
    pair_rows = []
    for pid, samples in groups.items():
        if len(samples) != 2 or sorted(x["side"] for x in samples) != ["safe", "unsafe"]:
            raise ValueError(f"Broken pair: {pid}")
        pair_rows.append({"pair_id": pid, "category": samples[0]["category"],
            "status": "READY" if all(x["status"] == "READY" for x in samples) else "MISSING_IMAGE",
            "safe_status": next(x["status"] for x in samples if x["side"] == "safe"),
            "unsafe_status": next(x["status"] for x in samples if x["side"] == "unsafe")})
    out = ROOT / "artifacts/stage2_full_image_status.json"
    write(out, {"dataset_revision": REVISION,
        "manifest_sha256": hashlib.sha256((ROOT / "artifacts/manifests/test_manifest.csv").read_bytes()).hexdigest(),
        "image_counts": dict(Counter(x["status"] for x in items)),
        "pair_counts": dict(Counter(x["status"] for x in pair_rows)),
        "missing_samples": [x for x in items if x["status"] != "READY"],
        "per_category": {cat: dict(Counter(x["status"] for x in pair_rows if x["category"] == cat))
                         for cat in sorted({x["category"] for x in pair_rows})}})
    csv_path = ROOT / "artifacts/stage2_test_pair_status.csv"
    with csv_path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(pair_rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(pair_rows)
    print(out.read_text()[:300])


if __name__ == "__main__":
    main()
