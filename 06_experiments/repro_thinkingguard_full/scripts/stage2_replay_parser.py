"""Raw-only, frozen-source replay of a Stage 2 parsing journal."""
import argparse
import collections
import hashlib
import json
from pathlib import Path

from a1_parser_v1 import parse as parse_a1
from d0_parser_v1 import parse as parse_d0
from run_resumeable_inference import ROOT, sha, write


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", choices=("a1", "d0"), required=True)
    ap.add_argument("--predictions", type=Path, required=True)
    ap.add_argument("--output", type=Path, required=True)
    args = ap.parse_args()
    freeze = json.loads((ROOT / f"artifacts/{args.protocol}_protocol_freeze.json").read_text())
    parser_source = ROOT / f"scripts/{args.protocol}_parser_v1.py"
    if sha(parser_source) != freeze["parser_sha256"]:
        raise ValueError("Parser source changed since freeze")
    parser = parse_a1 if args.protocol == "a1" else parse_d0
    rows = [json.loads(line) for line in args.predictions.read_text().splitlines()]
    uids = [r["sample_uid"] for r in rows]
    if len(uids) != len(set(uids)):
        raise ValueError("Duplicate raw prediction")
    results = []
    for row in rows:
        parsed = parser(row["raw_output"])
        results.append({"sample_uid": row["sample_uid"],
                        "saved_status": row["parse_status"],
                        "replayed_status": parsed["parse_status"],
                        "saved_verdict": row["parsed_verdict"],
                        "replayed_verdict": parsed["parsed_verdict"],
                        "structure_complete": parsed["structure_complete"]})
    mismatches = [r for r in results if r["saved_status"] != r["replayed_status"] or
                  r["saved_verdict"] != r["replayed_verdict"]]
    write(args.output, dict(protocol=args.protocol, source_sha256=sha(parser_source),
         raw_journal_sha256=sha(args.predictions), rows=len(rows),
         parsed=sum(r["replayed_verdict"] in ("Safe", "Unsafe") for r in results),
         structure_complete=sum(r["structure_complete"] for r in results),
         status_counts=dict(collections.Counter(r["replayed_status"] for r in results)),
         mismatches=mismatches, sample_results=results,
         ground_truth_used=False, human_review="NOT_RUN"))
    if mismatches:
        raise ValueError(f"Saved/replayed parse mismatch: {len(mismatches)}")


if __name__ == "__main__":
    main()
