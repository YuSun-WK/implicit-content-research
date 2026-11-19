"""A0 queue validation and namespace-aware NVIDIA accounting."""
import hashlib
import json
import re
import time
from collections import defaultdict
from pathlib import Path

SIZES = {"smoke": 6, "validation": 36, "pilot": 200, "full": 1736, "diagnostic": 6}
INPUT_FIELDS = ("sample_uid", "pair_id", "side", "ground_truth", "category", "text",
                "dataset_revision", "hf_image_path", "expected_image_sha256")


def identity_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True).encode()).hexdigest()


def queue_hash(entries, ordered):
    return identity_hash([{field: entries[uid][field] for field in INPUT_FIELDS} for uid in ordered])


def queue_ready(stage, entries, ordered, tree, revision, verify=None):
    if len(ordered) != len(set(ordered)) or len(ordered) != SIZES[stage]:
        return {"ready": False, "invalid_queue": True, "missing": list(ordered)}
    pairs = defaultdict(list)
    missing = []
    for uid in ordered:
        row = entries.get(uid)
        if row is None:
            missing.append(uid)
            continue
        expected = tree.get(row["hf_image_path"])
        pairs[row["pair_id"]].append(row)
        ready = (
            row["sample_uid"] == uid == f"{row['pair_id']}/{row['side']}"
            and row["split"] == "test" and row["ground_truth"] == row["side"].capitalize()
            and row["dataset_revision"] == revision
            and row["run_status"] == "READY" and row["image_decode_status"] == "OK"
            and row["image_hash_reference"] == "HF_LFS_SHA256"
            and expected and expected == row["expected_image_sha256"] == row["image_sha256"]
            and bool(row["image_local_path"])
        )
        if not ready or (verify is not None and not verify(row)):
            missing.append(uid)
    bad_pairs = [key for key, group in pairs.items() if
                 sorted(row["side"] for row in group) != ["safe", "unsafe"]
                 or len({(row["text"], row["category"]) for row in group}) != 1]
    return {"ready": not missing and not bad_pairs, "invalid_queue": False,
            "missing": missing, "invalid_pairs": bad_pairs, "total": len(ordered)}


def active_processes(uuid, query):
    selected = {}
    for device, pid, value in query():
        if device != uuid:
            continue
        if not pid.isdecimal() or not value.isdecimal() or pid in selected:
            raise ValueError("Unusable NVIDIA process memory record")
        selected[pid] = int(value)
    return selected


def require_idle(uuid, card, processes):
    snapshot = card(uuid)
    if (snapshot["uuid"] != uuid or "4090" not in snapshot["name"] or snapshot["used_mib"] > 64
            or snapshot["utilization_pct"] or processes()):
        raise ValueError("Selected GPU is occupied or outside the permitted GPU class")
    return snapshot


def bind_pid(processes, allocate, release, namespace_pids, verify_card, delay=time.sleep):
    """Match the unique host PID with a reversible allocation before model load."""
    before = processes()
    if len(before) != 1:
        raise ValueError("Expected exactly one new NVIDIA PID after CUDA context initialization")
    pid, baseline = next(iter(before.items()))
    verify_card(baseline)
    probe = allocate()
    try:
        delay(1)
        during = processes()
    finally:
        del probe
        release()
    delay(1)
    after = processes()
    if set(during) != {pid} or set(after) != {pid}:
        raise ValueError("NVIDIA PID set changed during ownership challenge")
    verify_card(max(during[pid], after[pid]))
    if not 48 <= during[pid] - baseline <= 80 or not 48 <= during[pid] - after[pid] <= 80:
        raise ValueError("NVIDIA PID failed the reversible 64 MiB ownership challenge")
    return {"host_pid": pid, "namespace_pids": sorted(namespace_pids),
            "challenge_mib": {"before": baseline, "during": during[pid], "after": after[pid]},
            "method": "unique_new_host_pid_reversible_64_mib"}


def run_id_valid(run_id):
    return bool(re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9_-]{0,95}", run_id or ""))


def registry_key(base, stage, input_sha):
    return identity_hash({"base": base, "stage": stage, "input_sha": input_sha})


def prior_summary(runs, registry, base, stage, input_sha, read, sha):
    record = registry.get(registry_key(base, stage, input_sha))
    if not record or not run_id_valid(record.get("run_id")):
        raise ValueError(f"No passing registered {stage} for this configuration and queue")
    run_id = record["run_id"]
    path = runs / run_id / "summary.json"
    summary = read(path)
    expected = dict(**base, inputs_sha256=input_sha, stage=stage, run_id=run_id)
    if (sha(path) != record["summary_sha256"] or summary.get("identity") != expected
            or summary.get("resource_gate") is not True
            or summary.get("prediction_count") != SIZES[stage]):
        raise ValueError(f"Registered {stage} summary failed provenance validation")
    return path, summary
