"""Evaluate fixed 300/868-pair A1 coverage without dropping missing rows."""
import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

from stage2_evaluate import bootstrap, score
from run_resumeable_inference import ROOT, write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pairs", type=int, choices=(300, 868), required=True)
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
    lineages = set()
    parse_counts = Counter()
    for path in args.predictions:
        for line in path.read_text().splitlines():
            r = json.loads(line)
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
            if identity["protocol"] != "a1":
                raise ValueError(f"Non-A1 prediction: {uid}")
            fixed = {k: v for k, v in identity.items()
                     if k not in ("inputs_sha256", "stage", "run_id")}
            lineages.add(json.dumps(fixed, sort_keys=True))
            observed[uid] = r
            parse_counts[r["parse_status"]] += 1
    if len(lineages) != 1:
        raise ValueError("Missing or mixed A1 source lineage")
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
    write(args.output, dict(protocol="a1", status="COMPLETE" if len(observed)==len(expected)
             else "COVERAGE_IN_PROGRESS", expected_pairs=args.pairs, expected_samples=len(expected),
             observed_samples=len(observed), missing_samples=len(expected)-len(observed),
             parse_status_counts=dict(parse_counts), reports=reports, failures=failures,
             source_files=[str(p) for p in args.predictions]))


if __name__ == "__main__":
    main()
