"""Freeze a deterministic, provenance-checked private Stage 2 smoke cohort."""

from hashlib import sha256
import random

from stage1_download import digest
from stage1_manifest import verified_manifest
from stage0_audit_csv import read_rows
from stage0_metrics import LABELS


def select_ids(rows, allowed, seed, count):
    if not 10 <= count <= 20 or len(allowed) < count:
        raise ValueError("Smoke requires 10–20 available UUIDs for the configured cohort size")
    candidates = sorted(allowed)
    random.Random(seed).shuffle(candidates)
    selected = []
    patterns = set()
    for index in range(count):
        gold = LABELS[index % len(LABELS)]
        uid = min(candidates, key=lambda u: (
            rows[u][2] == "not_sure", rows[u][4] != gold, rows[u][5] in patterns
        ))
        selected.append(uid)
        patterns.add(rows[uid][5])
        candidates.remove(uid)
    return selected


def freeze(csv, root, manifest_path, manifest_sha256, seed, count):
    snapshot, rows = verified_manifest(manifest_path, manifest_sha256, csv)
    source_rows, _, _ = read_rows(csv.read_bytes())
    queries = {row["uuid"]: row["prompt"] for _, row in source_rows}
    allowed = snapshot["cohorts"]["joint_decoded"]
    order = select_ids(rows, allowed, seed, count)
    subjects = []
    for uid in order:
        image = snapshot["image_sha256_by_uuid"][uid]
        path = root / "objects" / image
        if not path.is_file() or digest(path) != image:
            raise ValueError("Missing or changed selected image object")
        row = rows[uid]
        subjects.append({"uuid": uid, "gold": row[4], "pattern": row[5],
                         "image_sha256": image, "query_sha256": sha256(queries[uid].encode()).hexdigest()})
    return {"stage1_manifest_sha256": manifest_sha256, "seed": seed, "subjects": subjects}, queries, rows


def task_rows(roster, mode, diagnostic_count):
    return roster["subjects"] if mode == "direct" else roster["subjects"][:diagnostic_count]
