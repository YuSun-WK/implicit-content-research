"""Generate JSON audit, input manifest and a metadata-only Smoke shortlist."""

import argparse
from collections import Counter, defaultdict
import csv
import json
from pathlib import Path
from urllib.parse import quote

from manifest import SOURCES, TASKS, expand_record, record_errors, read_dataset, sha256


def duplicates(items):
    return {key: count for key, count in Counter(items).items() if count > 1}


def write_csv(path, rows):
    with path.open("w", encoding="utf-8", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def file_identity(item):
    if "lfs" in item:
        return "lfs_sha256", item["lfs"]["oid"]
    return "git_blob_oid", item["oid"]


def select_smoke_pairs(rows, images, selected_identities, limit=10):
    # Select one query per record and round-robin risk/task/text strata.
    strata = defaultdict(list)
    for left, right in zip(rows[::2], rows[1::2], strict=True):
        if left["text_index"] == 0 and all(row["image_path"] in images for row in (left, right)):
            key = (left["category"], left["subtask"], left["same_text"])
            strata[key].append((left, right))

    selected = []
    for rank in range(max(map(len, strata.values()), default=0)):
        for key in sorted(strata):
            if rank >= len(strata[key]):
                continue
            pair = strata[key][rank]
            identities = {file_identity(images[row["image_path"]]) for row in pair}
            if len(identities) == 2 and selected_identities.isdisjoint(identities):
                selected.append(pair)
                selected_identities.update(identities)
                if len(selected) == limit:
                    return selected
    return selected


def audit(dataset_path, tree_path, output):
    dataset = read_dataset(dataset_path)
    if set(dataset) != set(TASKS):
        raise ValueError(f"unexpected top-level keys {list(dataset)}")
    tree_bytes = tree_path.read_bytes()
    assets = {item["path"]: item for item in json.loads(tree_bytes) if item["type"] == "file"}
    images = {path: item for path, item in assets.items() if path.split("/")[0] in TASKS}
    groups = defaultdict(list)
    for path, item in images.items():
        groups[file_identity(item)].append(path)
    referenced = set()
    audit = {"dataset_revision": SOURCES["dataset_revision"],
             "combined_json_sha256": SOURCES["combined_json_sha256"],
             "combined_json_bytes": dataset_path.stat().st_size,
             "tree_response_sha256": sha256(tree_bytes), "local_image_decode": "not_run",
             "remote_image_files": len(images), "remote_image_bytes": sum(x["size"] for x in images.values()),
             "tasks": {}}
    manifest = []
    smoke = []
    selected_identities = set()
    for task in TASKS:
        records = dataset[task]
        expansions = defaultdict(list)
        fields = Counter()
        anomalies = []
        record_paths = []
        identical_sides = []
        duplicate_within_record = []
        seen_records = []
        for index, record in enumerate(records):
            fields.update(record.keys())
            seen_records.append(sha256(json.dumps(record, sort_keys=True).encode()))
            errors = record_errors(task, record)
            if errors:
                anomalies.append({"record_index": index, "errors": errors})
                continue
            try:
                queries = list(expand_record(task, record, index))
                intents = list(expand_record(task, record, index, "intent"))
            except ValueError as exc:
                anomalies.append({"record_index": index, "errors": [str(exc)]})
                continue
            expansions["query"] += queries
            expansions["intent"] += intents
            paths = [row["image_path"] for row in intents]
            record_paths += paths
            if paths[0] == paths[1]:
                identical_sides.append(index)
            for side in ("safe", "unsafe"):
                repeated = duplicates(row["text"] for row in queries if row["gold_label"] == side)
                if repeated:
                    duplicate_within_record.append({"record_index": index, "side": side,
                                                    "duplicates": repeated})
        referenced.update(record_paths)
        task_audit = {"records": len(records), "field_presence": dict(sorted(fields.items())),
                      "record_anomalies": anomalies, "duplicate_record_hashes": duplicates(seen_records),
                      "repeated_paths_across_record_slots": duplicates(record_paths),
                      "same_path_pairs_by_record": identical_sides,
                      "same_published_file_identity_pairs_by_record": [
                          row["record_index"] for row, other in zip(expansions["intent"][::2],
                                                                  expansions["intent"][1::2], strict=True)
                          if row["image_path"] in images and other["image_path"] in images
                          and file_identity(images[row["image_path"]])
                          == file_identity(images[other["image_path"]])],
                      "unique_referenced_paths": len(set(record_paths)),
                      "duplicate_text_within_record": duplicate_within_record,
                      "expansion": {}}
        for variant, rows in expansions.items():
            counts = Counter(row["gold_label"] for row in rows)
            left = rows[::2]
            task_audit["expansion"][variant] = {
                "pairs": len(left), "inputs_by_gold_label": dict(counts),
                "same_text_pairs": sum(row["same_text"] for row in left),
                "different_text_pairs": sum(not row["same_text"] for row in left),
                "category_input_counts": dict(Counter(row["category"] for row in rows)),
                "subtask_input_counts": dict(Counter(row["subtask"] for row in rows if row["subtask"])),
                "duplicate_image_text_label_groups": len(duplicates(
                    (row["image_path"], row["text"], row["gold_label"]) for row in rows)),
                "duplicate_exact_pair_groups": len(duplicates(
                    (a["image_path"], a["text"], b["image_path"], b["text"])
                    for a, b in zip(left, rows[1::2], strict=True))),
                "distinct_texts_by_side": {side: len(set(row["text"] for row in rows
                                                        if row["gold_label"] == side))
                                           for side in counts},
                "repeated_text_groups_by_side": {side: len(duplicates(row["text"] for row in rows
                                                                      if row["gold_label"] == side))
                                                 for side in counts},
            }
            for row in rows:
                item = images.get(row["image_path"], {})
                manifest.append({
                    **{key: val for key, val in row.items() if key != "text"},
                    "text_sha256": sha256(row["text"].encode()),
                    "hf_git_blob_oid": item.get("oid", ""),
                    "hf_lfs_sha256": item.get("lfs", {}).get("oid", ""),
                    "hf_size_bytes": item.get("size", ""),
                })
        audit["tasks"][task] = task_audit

        for pair in select_smoke_pairs(expansions["query"], images, selected_identities):
            smoke.extend(pair)

    paper_category_counts = {
        "chat": {"property": 236, "harmful": 508, "offensive": 268, "illegal": 188},
        "embodied": {"property": 640, "harmful": 120},
    }
    audit["paper_table1"] = {}
    for task, paper in paper_category_counts.items():
        counts = audit["tasks"][task]["expansion"]["query"]["category_input_counts"]
        audit["paper_table1"][task] = {
            "paper_inputs": paper, "hf_inputs": counts,
            "hf_minus_paper": {category: counts.get(category, 0) - paper.get(category, 0)
                               for category in sorted(counts.keys() | paper.keys())},
        }
    audit["missing_remote_paths"] = sorted(referenced - images.keys())
    release_delta = any(value for task in audit["paper_table1"].values()
                        for value in task["hf_minus_paper"].values())
    audit["paper_reconciliation"] = "STOP: category counts differ" if release_delta else "PASS"
    audit["unreferenced_remote_paths"] = sorted(images.keys() - referenced)
    audit["equal_remote_metadata_groups"] = [
        {"kind": kind, "identity": identity, "paths": paths}
        for (kind, identity), paths in sorted(groups.items()) if len(paths) > 1
    ]
    url = f"https://huggingface.co/datasets/{SOURCES['dataset']}/resolve/{SOURCES['dataset_revision']}/"
    assets_to_get = {}
    for row in smoke:
        path = row["image_path"]
        image = images[path]
        entry = assets_to_get.setdefault(path, {
            "image_path": path, "pair_ids": [], "url": url + quote(path, safe="/"),
            "expected_bytes": image["size"], "hf_git_blob_oid": image["oid"],
            "hf_lfs_sha256": image.get("lfs", {}).get("oid", ""),
        })
        entry["pair_ids"].append(row["pair_id"])
    audit["smoke"] = {"pairs": len(smoke) // 2, "unique_paths": len(assets_to_get),
                      "expected_bytes": sum(x["expected_bytes"] for x in assets_to_get.values())}
    write_csv(output / "manifest.csv", manifest)
    write_csv(output / "smoke_pairs.csv", [{key: val for key, val in row.items() if key != "text"}
                                         for row in smoke])
    for entry in assets_to_get.values():
        entry["pair_ids"] = "|".join(entry["pair_ids"])
    write_csv(output / "smoke_images.csv", list(assets_to_get.values()))
    report = json.dumps(audit, indent=2, ensure_ascii=False) + "\n"
    (output / "data_audit.json").write_text(report, encoding="utf-8")
    print(json.dumps({"records": {task: v["records"] for task, v in audit["tasks"].items()},
                      "expansion": {task: v["expansion"] for task, v in audit["tasks"].items()},
                      "smoke": audit["smoke"], "missing_remote_paths": audit["missing_remote_paths"]},
                     indent=2))


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", required=True, type=Path)
    parser.add_argument("--tree", required=True, type=Path)
    parser.add_argument("--output", type=Path, default=Path("."))
    args = parser.parse_args()
    audit(args.dataset, args.tree, args.output)
