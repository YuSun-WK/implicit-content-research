"""Freeze independent Stage 2 queues and protect pre-existing evidence."""
import csv
import hashlib
import json
import random
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO = ROOT.parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def dump(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(data, indent=2, ensure_ascii=False, sort_keys=True) + "\n"
    if path.exists():
        if path.read_text() != payload:
            raise ValueError(f"Frozen Stage 2 artifact differs: {path}")
        return
    path.write_text(payload)


def main():
    protected = [p for p in subprocess.check_output(
        ["git", "ls-files", "-z", "03_experiments/h1_k0_triggerbench",
         "03_experiments/h1_k2_research_audit"], cwd=REPO).decode().split("\0") if p]
    protected += list(json.loads((ROOT / "artifacts/legacy_immutability.json").read_text())["after"])
    protected += [str(p.relative_to(REPO)) for pattern in (
        "runs/smoke_20261119_recovery/**/*", "runs/validation_20261119_recovery/**/*",
        "artifacts/parser_freeze.json", "artifacts/sample_queues.json",
        "artifacts/model_cache_audit.json", "scripts/official_parser_v3.py")
        for p in (ROOT / pattern.split('/')[0]).glob('/'.join(pattern.split('/')[1:])) if p.is_file()]
    local_model = Path("/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3")
    evidence = {p: sha(REPO / p) for p in sorted(set(protected))}
    evidence.update({str(p): sha(p) for p in sorted(local_model.glob("model-*.safetensors"))})
    dump(ROOT / "artifacts/stage2_protected_before.json", evidence)
    old = json.loads((ROOT / "artifacts/sample_queues.json").read_text())
    rows = list(csv.DictReader((ROOT / "artifacts/manifests/test_manifest.csv").open()))
    pairs = defaultdict(list)
    for row in rows:
        pairs[row["pair_id"]].append(row)
    excluded = set(old["excluded_historical_pair_ids"])
    excluded |= {uid.rsplit("/", 1)[0] for stage in ("smoke", "validation", "pilot") for uid in old[stage]}
    rng = random.Random(20261120)
    categories = sorted({row["category"] for row in rows})
    chosen = []
    for cat in categories:
        eligible = sorted(pid for pid, group in pairs.items() if pid not in excluded and
                          len(group) == 2 and group[0]["category"] == cat)
        chosen.extend(rng.sample(eligible, 2))
    validation = [f"{pid}/{side}" for pid in chosen for side in ("safe", "unsafe")]
    smoke = old["smoke"]
    dump(ROOT / "artifacts/stage2_queues_v1.json", {
        "seed": 20261120, "selection": "uniform_without_replacement_by_category_before_image_availability",
        "exclusions": "historical_H1_36_pairs_A0_smoke_validation_Pilot100",
        "a1_smoke": smoke, "a1_validation": validation,
        "pilot": old["pilot"], "validation_pairs": chosen,
        "ready_at_freeze": [uid for uid in validation if pairs[uid.rsplit('/',1)[0]][0] and
                             next(r for r in pairs[uid.rsplit('/',1)[0]] if r['sample_uid']==uid)['run_status']=='READY'],
    })
    print(json.dumps({"validation": len(validation), "ready_at_freeze": sum(
        next(r for r in pairs[uid.rsplit('/',1)[0]] if r['sample_uid']==uid)['run_status']=='READY'
        for uid in validation), "chosen_pairs": chosen}))


if __name__ == "__main__":
    main()
