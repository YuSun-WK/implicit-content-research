"""Verify the historical worktree and repaired ThinkingGuard weight index."""
import argparse
import hashlib
import importlib.util
import json
import subprocess
from collections import Counter
from pathlib import Path

from official_parser_v3 import parse


def sha(path):
    with path.open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def write(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def legacy_snapshot(repo):
    listing = subprocess.check_output(["git", "-C", str(repo), "ls-tree", "-rz", "HEAD", "--", "03_experiments"])
    result = {}
    for item in listing.decode().split("\0"):
        if not item:
            continue
        metadata, name = item.split("\t", 1)
        mode, kind, blob = metadata.split()
        path = repo / name
        if kind == "blob" and Path(name).parts[1].startswith("h1_"):
            result[name] = {"blob": blob, "sha256": sha(path)}
    return result


def audit_model(repo, model):
    script = repo / "03_experiments/h1_k0_triggerbench/scripts/audit_model_cache.py"
    spec = importlib.util.spec_from_file_location("legacy_model_verifier", script)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    model_id = "Sandy124/ThinkingGuard-8B"
    official = model / "model.safetensors.index.official.json"
    repaired = model / "model.safetensors.index.json"
    lineage = json.loads((model / "local_index_provenance.json").read_text())
    official_map = json.loads(official.read_text())["weight_map"]
    repaired_map = json.loads(repaired.read_text())["weight_map"]
    metadata = json.loads((model / "official_metadata.json").read_text())
    official_blob = subprocess.check_output(["git", "hash-object", str(official)], text=True).strip()
    published = {row["rfilename"]: row for row in metadata["siblings"]}
    observed, shards = {}, []
    for name, (size, expected) in verifier.SHARDS[model_id].items():
        path = model / name
        keys = {key for key, location in repaired_map.items() if location == name}
        verifier.check_safetensors_header(path, keys)
        with path.open("rb") as handle:
            header_size = int.from_bytes(handle.read(8), "little")
            header = json.loads(handle.read(header_size))
        previous_offset = 0
        data_size = path.stat().st_size - 8 - header_size
        for tensor, data in sorted(
            ((k, v) for k, v in header.items() if k != "__metadata__"),
            key=lambda item: item[1]["data_offsets"],
        ):
            start, end = data["data_offsets"]
            if tensor in observed or start != previous_offset or not start <= end <= data_size:
                raise ValueError(f"Invalid or duplicate tensor: {tensor}")
            observed[tensor] = name
            previous_offset = end
        if previous_offset != data_size:
            raise ValueError(f"Unindexed bytes in {name}")
        actual = sha(path)
        if actual != expected or path.stat().st_size != size:
            raise ValueError(f"Shard hash or size mismatch: {name}")
        if published[name]["lfs"]["sha256"] != actual:
            raise ValueError(f"Archived Hub metadata differs for {name}")
        shards.append(dict(name=name, bytes=size, sha256=actual, tensors=len(keys)))
    changed = sum(location != repaired_map[key] for key, location in official_map.items())
    if (
        observed != repaired_map or official_map.keys() != repaired_map.keys()
        or changed != lineage["changed_locations"] or len(observed) != lineage["tensors"]
        or sha(official) != lineage["official_index_sha256"] or sha(repaired) != lineage["local_index_sha256"]
        or official_blob != published["model.safetensors.index.json"]["blobId"]
    ):
        raise ValueError("Repaired index provenance failed verification")
    processor = {}
    for name in verifier.REQUIRED[model_id]:
        if name == repaired.name:
            continue
        blob = subprocess.check_output(["git", "hash-object", str(model / name)], text=True).strip()
        if published[name]["blobId"] != blob:
            raise ValueError(f"Processor or config blob mismatch: {name}")
        processor[name] = dict(sha256=sha(model/name), git_blob=blob)
    return dict(status="DONE", revision=metadata["sha"], weight_bytes_unchanged=True,
                shards=shards, tensor_count=len(observed), index_changed_locations=changed,
                official_index_sha256=sha(official), local_index_sha256=sha(repaired),
                official_index_git_blob=official_blob, processor_and_configs=processor,
                method="Legacy header verifier, complete index comparison, archived Hub blob/LFS identities",
                archived_model_card_sha256=sha(model / "README.md"))


def historical_results(repo):
    path = repo / "03_experiments/h1_k0_triggerbench/runs/h1_k1_20261117_060147"
    formal = [json.loads(line) for line in (path / "formal_unified/predictions.jsonl").open()]
    joint = [r for r in formal if r["input_condition"] == "joint"]
    counts = Counter((r["ground_truth"].lower(), r["raw_model_output"].strip().lower()) for r in joint)
    by_pair = {}
    for row in joint:
        by_pair.setdefault(row["pair_id"], []).append(
            row["ground_truth"].lower() == row["raw_model_output"].strip().lower())
    old_validation = []
    transcriptions = json.loads((path / "independent_validation.json").read_text())["manual_transcription"]
    reference = {r["raw_sha256"]: r["transcribed_final_verdict"] for r in transcriptions}
    for line in (path / "validation_official/predictions.jsonl").open():
        row = json.loads(line)
        raw = row["raw_model_output"]
        result = parse(raw)
        digest = hashlib.sha256(raw.encode()).hexdigest()
        old_validation.append(dict(pair_id=row["pair_id"], side=row["side"], raw_sha256=digest,
                                   v2=row["parsed_prediction"], v3=result["parsed_verdict"],
                                   audit_transcription=reference[digest], status_v3=result["parse_status"],
                                   structure_complete=result["structure_complete"]))
    return dict(unified_rows=len(formal), joint_rows=len(joint),
                confusion={f"{gt}:{pred}": count for (gt, pred), count in counts.items()},
                joint_pairs=len(by_pair), correct_pairs=sum(all(x) and len(x)==2 for x in by_pair.values()),
                legacy_official_rows=old_validation, legacy_formal_official="NOT_RUN",
                new_holdout=False)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--legacy", type=Path, required=True)
    cli.add_argument("--artifacts", type=Path, required=True)
    cli.add_argument("--model", type=Path)
    cli.add_argument("--baseline", type=Path)
    args = cli.parse_args()
    if args.model:
        write(args.artifacts / "model_cache_audit.json", audit_model(args.legacy, args.model))
    if args.baseline:
        before = json.loads(args.baseline.read_text())
        after = legacy_snapshot(args.legacy)
        changed = [name for name in sorted(before.keys() | after.keys()) if before.get(name) != after.get(name)]
        write(args.artifacts / "legacy_immutability.json",
              dict(legacy_commit="4eb98bee31a6182bcf8e1ee724679460da008686",
                   compared_count=len(after), unchanged=not changed, changed=changed, before=before, after=after))
        if changed:
            raise ValueError(f"Historical files changed: {changed}")
    write(args.artifacts / "legacy_results_audit.json", historical_results(args.legacy))


if __name__ == "__main__":
    main()
