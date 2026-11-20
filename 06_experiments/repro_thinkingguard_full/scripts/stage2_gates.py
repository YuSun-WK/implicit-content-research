"""Stage 2 complete-pair batch gate without altering frozen A0 gates."""
from collections import defaultdict


def batch_ready(entries, ordered, tree, revision, verify):
    if not ordered or len(ordered) % 2 or len(ordered) != len(set(ordered)):
        return {"ready": False, "invalid_queue": True, "missing": ordered}
    pairs = defaultdict(list)
    missing = []
    for uid in ordered:
        row = entries.get(uid)
        if row is None:
            missing.append(uid)
            continue
        pairs[row["pair_id"]].append(row)
        if not (row["sample_uid"] == uid == f"{row['pair_id']}/{row['side']}"
                and row["split"] == "test" and row["ground_truth"] == row["side"].capitalize()
                and row["dataset_revision"] == revision and row["run_status"] == "READY"
                and row["image_decode_status"] == "OK"
                and row["image_hash_reference"] == "HF_LFS_SHA256"
                and tree.get(row["hf_image_path"]) == row["expected_image_sha256"] == row["image_sha256"]
                and verify(row)):
            missing.append(uid)
    bad = [pid for pid, rows in pairs.items() if
           sorted(r["side"] for r in rows) != ["safe", "unsafe"] or
           len({(r["text"], r["category"]) for r in rows}) != 1]
    return {"ready": not missing and not bad, "invalid_queue": bool(bad),
            "missing": missing, "invalid_pairs": bad, "total": len(ordered)}
