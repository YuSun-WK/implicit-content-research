"""Evaluate fixed 300/868-pair protocol coverage without dropping missing rows."""
import argparse
import csv
import hashlib
import json
from collections import Counter, defaultdict
from pathlib import Path

from stage2_evaluate import bootstrap, score
from run_resumeable_inference import ROOT, write

FIXED_IDENTITY = ("protocol", "prompt_sha256", "parser_sha256", "expansion_queue_sha256",
                  "config_sha256", "source_tree_sha256", "queues_sha256",
                  "model_audit_sha256", "gates_sha256")


def check_lineages(identities, protocol):
    fixed = {tuple((key, x[key]) for key in FIXED_IDENTITY) for x in identities}
    if len(fixed) != 1:
        raise ValueError("Mixed prompt/parser/config/model/source lineage")
    runners = {x["runner_sha256"] for x in identities}
    if protocol == "a1":
        if len(runners) != 1:
            raise ValueError("Mixed A1 runners")
    else:
        compat = json.loads((ROOT / "artifacts/d0_batch_runner_compatibility.json").read_text())
        if (not runners.issubset({compat["old_runner_sha256"], compat["new_runner_sha256"]})
                or compat["new_runner_sha256"] != hashlib.sha256(
                    (ROOT / "scripts/stage2_inference.py").read_bytes()).hexdigest()
                or compat["patch_sha256"] != hashlib.sha256(
                    (ROOT / "docs/d0_batch_runner_diff.patch").read_bytes()).hexdigest()
                or any(compat[key] != identities[0][key] for key in FIXED_IDENTITY if key != "protocol")
                or any(x["stage"] == "pilot" and x["runner_sha256"] != compat["old_runner_sha256"]
                       for x in identities)
                or any(x["stage"] == "batch" and x["runner_sha256"] != compat["new_runner_sha256"]
                       for x in identities)):
            raise ValueError("Unreviewed D0 runner lineage")
    return {key: identities[0][key] for key in FIXED_IDENTITY} | {"runner_sha256s": sorted(runners)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, choices=(300, 868), required=True)
    ap.add_argument("--protocol", choices=("a1", "d0"), required=True)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("predictions", nargs="+", type=Path)
    args = ap.parse_args()
    expansion = json.loads((ROOT / "artifacts/stage2_expansion_queue_v1.json").read_text())
    expected_pairs = expansion["full_pairs"][:args.pairs]
    expected = {f"{pid}/{side}" for pid in expected_pairs for side in ("safe", "unsafe")}
    with (ROOT / "artifacts/manifests/test_manifest.csv").open() as f:
        manifest = {r["sample_uid"]: r for r in csv.DictReader(f) if r["sample_uid"] in expected}
    if len(manifest) != 2*args.pairs:
        raise ValueError("Frozen pair denominator mismatch")
    observed = {}
    identities = []
    parse_counts = Counter()
    for path in args.predictions:
        file_rows = [json.loads(line) for line in path.read_text().splitlines()]
        if not file_rows:
            continue
        file_identity = file_rows[0]["identity"]
        if any(r["identity"] != file_identity for r in file_rows):
            raise ValueError(f"Mixed identities in one journal: {path}")
        identity_path = path.with_name("identity.json")
        if not identity_path.is_file() or json.loads(identity_path.read_text()) != file_identity:
            raise ValueError(f"Missing or changed run identity: {path}")
        if file_identity["stage"] not in ("pilot", "batch"):
            raise ValueError("Only Pilot and batch predictions enter cumulative Test")
        if file_identity["stage"] == "pilot" and path != args.predictions[0]:
            raise ValueError("Pilot file must be first")
        if file_identity["stage"] == "pilot":
            pilot_expected = {f"{pid}/{side}" for pid in expansion["full_pairs"][:100]
                              for side in ("safe", "unsafe")}
            if {r["sample_uid"] for r in file_rows} != pilot_expected:
                raise ValueError("Frozen Pilot100 is incomplete")
            summary_path = path.with_name("summary.json")
            summary = json.loads(summary_path.read_text()) if summary_path.exists() else {}
            if summary.get("resource_gate") is not True or summary.get("identity") != file_identity:
                raise ValueError("Pilot100 resource summary is missing or changed")
        else:
            snapshot = path.with_name("batch_queue_snapshot.json")
            if (not snapshot.is_file() or hashlib.sha256(snapshot.read_bytes()).hexdigest()
                    != file_identity.get("batch_queue_sha256")
                    or file_identity.get("batch_gates_sha256") != hashlib.sha256(
                        (ROOT / "scripts/stage2_gates.py").read_bytes()).hexdigest()):
                raise ValueError("Batch queue snapshot is missing or changed")
        identities.append(file_identity)
        for r in file_rows:
            uid = r["sample_uid"]
            if uid not in expected:
                continue
            if uid in observed:
                raise ValueError(f"Duplicate prediction: {uid}")
            row = manifest[uid]
            if (r["gt"] != row["ground_truth"] or r["side"] != row["side"]
                    or r["pair_id"] != row["pair_id"]
                    or r["image_sha"] != row["expected_image_sha256"]):
                raise ValueError(f"Manifest mismatch: {uid}")
            identity = r["identity"]
            if identity["protocol"] != args.protocol:
                raise ValueError(f"Wrong protocol prediction: {uid}")
            index = expansion["full_pairs"].index(row["pair_id"])
            if (identity["stage"] == "pilot" and index >= 100) or (
                identity["stage"] == "batch" and not identity["batch_start_pair"] <= index <
                identity["batch_start_pair"] + identity["batch_slice_pairs"]):
                raise ValueError(f"Prediction outside its frozen stage slice: {uid}")
            observed[uid] = r
            parse_counts[r["parse_status"]] += 1
    if not identities or identities[0]["stage"] != "pilot":
        raise ValueError("Frozen Pilot100 evidence is required first")
    lineage = check_lineages(identities, args.protocol)
    groups = defaultdict(list)
    failures = []
    for pid in expected_pairs:
        pair = []
        for side in ("safe", "unsafe"):
            uid = f"{pid}/{side}"
            r = observed.get(uid)
            verdict = (r["parsed_verdict"] if r and r["status"] == "GENERATED"
                       else "INVALID" if r else "MISSING")
            pair.append(verdict)
            if verdict != side.capitalize():
                failures.append({"sample_uid": uid, "ground_truth": side.capitalize(),
                                 "verdict": verdict, "reason": r["parse_status"] if r else "NOT_RUN"})
        groups[manifest[f"{pid}/safe"]["category"]].append(tuple(pair))
    reports = {}
    for name, valid_only in (("strict_full_denominator", False), ("valid_only", True)):
        per = {cat: score(group, valid_only) for cat, group in sorted(groups.items())}
        micro = score([pair for group in groups.values() for pair in group], valid_only)
        f1s = [v["f1_unsafe"] for v in per.values()]
        recalls = [v["unsafe_recall"] for v in per.values()]
        reports[name] = dict(micro=micro,
            macro_f1_nine_categories=sum(f1s)/9 if len(f1s)==9 and all(v is not None for v in f1s) else None,
            macro_recall_nine_categories=sum(recalls)/9 if len(recalls)==9 and all(v is not None for v in recalls) else None,
            per_category=per, stratified_pair_cluster_bootstrap95=bootstrap(list(groups.values()),valid_only))
    write(args.output, dict(protocol=args.protocol, status="COMPLETE" if len(observed)==len(expected)
             else "COVERAGE_IN_PROGRESS", expected_pairs=args.pairs, expected_samples=len(expected),
             observed_samples=len(observed), missing_samples=len(expected)-len(observed),
             parse_status_counts=dict(parse_counts), reports=reports, failures=failures,
             lineage=lineage,
             source_files=[str(p) for p in args.predictions]))


if __name__ == "__main__":
    main()
