"""Pinned release roster, deterministic smoke selection and prediction preflight."""

from collections import Counter, defaultdict
from hashlib import sha256
import json
import random

from stage0_audit_csv import CSV_SHA256, GRADE_FIELDS, audit, read_rows

TASKS = ("release_roster", "joint_decoded", "image_decoded_gold",
         "text_only_eligible", "three_modality_intersection")
VERSION = 1


def pinned_rows(path):
    raw = path.read_bytes()
    summary, _, _, _ = audit(raw)
    if summary["status"] != "PASS":
        raise ValueError("Input is not the pinned, schema-verified Apple release")
    rows, _, _ = read_rows(raw)
    return [
        (row["uuid"], row["web_path"], *(row[field] for field in GRADE_FIELDS),
         "-".join("?" if row[field] == "not_sure" else row[field][0].upper() for field in GRADE_FIELDS), record)
        for record, row in rows
    ]


def smoke_rows(rows):
    rng = random.Random(20261119)
    by_pattern = defaultdict(list)
    for row in sorted(rows):
        by_pattern[row[5]].append(row)
    select = {row[0]: row for group in sorted(by_pattern)
              for row in rng.sample(by_pattern[group], min(2, len(by_pattern[group])))}
    counts = Counter(row[1] for row in rows)
    for row in rows:
        if counts[row[1]] > 1:
            select[row[0]] = row
    return sorted(select.values())


def canonical(data):
    return (json.dumps(data, sort_keys=True, ensure_ascii=False, separators=(",", ":")) + "\n").encode()


def make_manifest(rows, digests, code_sha256):
    cohorts = dict.fromkeys(TASKS)
    cohorts["release_roster"] = sorted(row[0] for row in rows)
    cohorts["joint_decoded"] = sorted(row[0] for row in rows if row[1] in digests)
    cohorts["image_decoded_gold"] = sorted(row[0] for row in rows if row[1] in digests and row[2] != "not_sure")
    cohorts["text_only_eligible"] = cohorts["release_roster"]
    cohorts["three_modality_intersection"] = cohorts["image_decoded_gold"]
    images = {row[0]: digests[row[1]] for row in rows if row[1] in digests}
    return {"version": VERSION, "csv_sha256": CSV_SHA256, "code_sha256": code_sha256,
            "download_snapshot_sha256": sha256(canonical(images)).hexdigest(),
            "image_sha256_by_uuid": images, "cohorts": cohorts}


def validate_predictions(records, manifest_path, expected_sha256, task, *, release_csv):
    """Verify snapshot digest, official roster membership, exact UUID coverage and gold."""
    manifest, uuids = verified_manifest(manifest_path, expected_sha256, release_csv)
    return validate_records(records, set(manifest["cohorts"][task]), uuids, GOLD_FIELDS[task])


GOLD_FIELDS = {"joint_decoded": 4, "image_decoded_gold": 2, "text_only_eligible": 3}


def validate_three_modality_predictions(records_by_task, manifest_path, expected_sha256, *, release_csv):
    """Require all three modality ledgers on the exact frozen Figure 4/5 cohort."""
    if records_by_task.keys() != GOLD_FIELDS.keys():
        raise ValueError("Figure 4/5 requires joint, image and text ledgers")
    manifest, uuids = verified_manifest(manifest_path, expected_sha256, release_csv)
    selected = set(manifest["cohorts"]["three_modality_intersection"])
    return {task: validate_records(records, selected, uuids, GOLD_FIELDS[task])
            for task, records in records_by_task.items()}


def verified_manifest(manifest_path, expected_sha256, release_csv):
    raw = manifest_path.read_bytes()
    if sha256(raw).hexdigest() != expected_sha256:
        raise ValueError("Manifest hash mismatch")
    manifest = json.loads(raw)
    rows = pinned_rows(release_csv)
    uuids = {row[0]: row for row in rows}
    images = manifest["image_sha256_by_uuid"]
    if images.keys() - uuids.keys() or any(
        not isinstance(digest, str) or len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest)
        for digest in images.values()
    ):
        raise ValueError("Invalid image UUID or digest")
    digests = {}
    for uid, digest in images.items():
        url = uuids[uid][1]
        if url in digests and digests[url] != digest:
            raise ValueError("Duplicate URL has inconsistent image digests")
        digests[url] = digest
    if manifest != make_manifest(rows, digests, manifest["code_sha256"]):
        raise ValueError("Manifest does not match the pinned release and image snapshot")
    return manifest, uuids


def validate_records(records, selected, uuids, gold_index):
    records = list(records)
    seen = set()
    for record in records:
        uid = record["uuid"]
        if uid in seen or uid not in selected or record["gold"] != uuids[uid][gold_index]:
            raise ValueError("Unexpected or duplicate UUID or gold mismatch")
        seen.add(uid)
    if selected != seen:
        raise ValueError(f"Missing {len(selected - seen)} planned prediction rows")
    return records
