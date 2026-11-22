"""Freeze 100 deterministic, record-disjoint MSSBench query pairs."""
import csv
from collections import Counter, defaultdict
import hashlib
from pathlib import Path
from urllib.parse import quote

from manifest import SOURCES, expand_record, read_dataset, sha256

HERE = Path(__file__).parent
SEED = "20261120"
CHAT_QUOTAS = {name: 15 for name in ("harmful", "illegal", "offensive", "property")}
EMBODIED_QUOTAS = {
    ("Place", "False", "harmful"): 6,
    ("Place", "False", "property"): 8,
    ("Place", "True", "property"): 4,
    ("Toggle", "False", "property"): 4,
    ("Toggle", "True", "property"): 4,
    ("Pick_Place", "True", "property"): 6,
    ("Drop", "True", "harmful"): 1,
    ("Drop", "True", "property"): 3,
    ("Heat", "True", "property"): 4,
}


def read_csv(path):
    with path.open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def rank(task, record_index):
    return hashlib.sha256(f"{SEED}:{task}:{record_index}".encode()).hexdigest()


def freeze(data_root, output):
    dataset = read_dataset(data_root / "combined.json")
    manifest = read_csv(HERE / "manifest.csv")
    lookup = {(row["pair_id"], row["gold_label"]): row for row in manifest
              if row["variant"] == "query"}
    anchor = read_csv(HERE / "smoke_pairs.csv")
    candidates = defaultdict(list)
    for task in ("chat", "embodied"):
        for index, record in enumerate(dataset[task]):
            expanded = list(expand_record(task, record, index))
            pairs = defaultdict(list)
            for row in expanded:
                pairs[row["pair_id"]].append(row)
            key = (task, index)
            candidates[key] = list(pairs.values())

    selected = []
    seen_records = set()
    seen_content = set()
    exclusions = []

    def add_pair(pair, anchor_flag):
        task, index = pair[0]["task"], pair[0]["record_index"]
        key = task, index
        if key in seen_records:
            raise ValueError("duplicate original record")
        files = [lookup[(row["pair_id"], row["gold_label"])] for row in pair]
        digests = [row["hf_lfs_sha256"] for row in files]
        if len(set(digests)) != 2 or any(digest in seen_content for digest in digests):
            if anchor_flag:
                raise ValueError("anchor has duplicate image content")
            exclusions.append({"task": task, "record_index": index,
                               "reason": "duplicate_image_content_sha256"})
            return False
        for row, file in zip(pair, files, strict=True):
            if (file["text_sha256"] != sha256(row["text"].encode())
                    or file["image_path"] != row["image_path"]
                    or file["category"] != row["category"]):
                raise ValueError("frozen row differs from fixed manifest")
        selected.append((pair, files, anchor_flag))
        seen_records.add(key)
        seen_content.update(digests)
        return True

    anchor_pairs = defaultdict(list)
    anchor_order = []
    for row in anchor:
        if row["pair_id"] not in anchor_pairs:
            anchor_order.append(row["pair_id"])
        anchor_pairs[row["pair_id"]].append(row)
    for pair_id in anchor_order:
        rows = anchor_pairs[pair_id]
        task, index = rows[0]["task"], int(rows[0]["record_index"])
        pair = next(p for p in candidates[(task, index)] if p[0]["pair_id"] == pair_id)
        if [(r["gold_label"], r["image_path"]) for r in pair] != [
                (r["gold_label"], r["image_path"]) for r in rows]:
            raise ValueError("anchor manifest changed")
        add_pair(pair, True)

    def stratum(pair):
        row = pair[0]
        return row["category"] if row["task"] == "chat" else (
            row["subtask"], str(row["same_text"]), row["category"])

    for task, quotas in (("chat", CHAT_QUOTAS), ("embodied", EMBODIED_QUOTAS)):
        for target, quota in quotas.items():
            existing = sum(p[0][0]["task"] == task and stratum(p[0]) == target for p in selected)
            if existing > quota:
                raise ValueError(f"anchor exceeds quota: {task}/{target}")
            pool = [(key, pairs) for key, pairs in candidates.items()
                    if key[0] == task and key not in seen_records and stratum(pairs[0]) == target]
            for key, pairs in sorted(pool, key=lambda item: rank(*item[0])):
                if existing == quota:
                    break
                index = int(rank(*key), 16) % len(pairs)
                if add_pair(pairs[index], False):
                    existing += 1
            if existing != quota:
                raise ValueError(f"quota cannot be filled without duplicate content: {task}/{target}")

    if len(selected) != 100 or Counter(p[0][0]["task"] for p in selected) != {"chat": 60, "embodied": 40}:
        raise ValueError("invalid 100-pair selection")
    output.mkdir(parents=True, exist_ok=True)
    rows = []
    for pair_index, (pair, files, anchor_flag) in enumerate(selected):
        for row, file in zip(pair, files, strict=True):
            rows.append({"pair_index": pair_index, "chunk_id": pair_index // 25,
                         "anchor": anchor_flag, **{k: row[k] for k in (
                             "dataset_revision", "pair_id", "task", "record_index", "text_index",
                             "variant", "gold_label", "category", "subtask", "same_text", "image_path")},
                         "text_sha256": file["text_sha256"],
                         "hf_lfs_sha256": file["hf_lfs_sha256"],
                         "expected_bytes": file["hf_size_bytes"],
                         "url": (f"https://huggingface.co/datasets/{SOURCES['dataset']}/resolve/"
                                 f"{SOURCES['dataset_revision']}/{quote(row['image_path'])}")})
    with (output / "frozen_100_pairs.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    counts = Counter((p[0][0]["task"], stratum(p[0]), p[2]) for p in selected)
    strata = [{"task": task, "stratum": str(target), "anchor": int(anchor_flag), "count": count}
              for (task, target, anchor_flag), count in sorted(counts.items(), key=str)]
    with (output / "strata_counts.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(strata[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(strata)
    with (output / "selection_exclusions.csv").open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=("task", "record_index", "reason"), lineterminator="\n")
        writer.writeheader()
        writer.writerows(exclusions)
    print("pairs", len(selected), "sides", len(rows), "anchors", sum(p[2] for p in selected),
          "duplicate-content exclusions", len(exclusions))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--data-root", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    freeze(args.data_root, args.out)
