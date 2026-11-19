"""Freeze ordered Stage 1 queues using only category, sample keys and old exposure."""
import argparse
import csv
import json
import random
from collections import defaultdict
from pathlib import Path

SEED = 20261119


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("manifest", type=Path)
    cli.add_argument("legacy", type=Path)
    cli.add_argument("output", type=Path)
    args = cli.parse_args()
    baseline = args.legacy / "03_experiments/h1_k0_triggerbench/runs"
    excluded = set()
    for path in baseline.rglob("sample_manifest.csv"):
        with path.open() as handle:
            excluded.update(row["pair_id"] for row in csv.DictReader(handle))
    groups = defaultdict(lambda: defaultdict(list))
    with args.manifest.open() as handle:
        for row in csv.DictReader(handle):
            if row["pair_id"] not in excluded:
                groups[row["category"]][row["pair_id"]].append(row["sample_uid"])
    rng = random.Random(SEED)
    ordered = []
    for category, group in sorted(groups.items()):
        pairs = sorted(group.values())
        rng.shuffle(pairs)
        ordered.append((category, pairs))
    smoke = [uid for _, pairs in ordered[:3] for uid in pairs[0]]
    validation = [uid for _, pairs in ordered for pair in pairs[1:3] for uid in pair]
    pilot = [
        uid for round_index in range(12) for category_index, (_, pairs) in enumerate(ordered)
        if round_index < 11 or category_index == 0 for uid in pairs[round_index+3]
    ]
    assert len(set(smoke+validation+pilot)) == 242
    result = dict(seed=SEED, excluded_historical_pair_ids=sorted(excluded),
                  smoke=smoke, validation=validation, pilot=pilot)
    args.output.write_text(json.dumps(result, indent=2) + "\n")


if __name__ == "__main__":
    main()
