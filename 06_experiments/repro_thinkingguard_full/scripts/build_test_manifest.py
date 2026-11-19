"""Build the paired Test manifest from one frozen TriggerBench release."""
import argparse
import csv
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
import re
import signal
import time
import subprocess
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path, PurePosixPath
from urllib.parse import quote

from PIL import Image

REVISION = "3ac26e778db94a282711f463f22ba6db99643bee"
DATASET = "https://huggingface.co/datasets/Sandy124/TriggerBench"
COUNTS = dict(ethical_violations=97, illegal_activities=96, misinformation=95,
              offensiveness=95, physical_harm=81, privacy=100, property_damage=100,
              religion_belief=90, violence=114)
SIDES = ("safe", "unsafe")


def digest(data):
    return hashlib.sha256(data).hexdigest()


def normalize(text):
    return " ".join(unicodedata.normalize("NFKC", text).casefold().split())


def dump(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n")


def read_csvs(root):
    rows, inventory = [], []
    for split in ("test", "train"):
        for category in COUNTS:
            source_category = "region_belief" if split == "train" and category == "religion_belief" else category
            for side in SIDES:
                source = f"{split}/text_{split}/{source_category}_{side}.csv"
                contents = (root / source).read_bytes()
                start = len(rows)
                with (root / source).open(encoding="utf-8-sig", newline="") as handle:
                    reader = csv.DictReader(handle)
                    if reader.fieldnames != ["index", "text", "image_path", "category"]:
                        raise ValueError(f"Unexpected schema: {source}")
                    for source_row, record in enumerate(reader, 1):
                        index, text, image, annotation = (record[x] for x in reader.fieldnames)
                        name = PurePosixPath(image).name
                        if (not index or not index.isdecimal() or not text
                                or not re.fullmatch(rf"[^/\s]+_{side}\.png", name)
                                or image.strip() != image):
                            raise ValueError(f"Malformed row: {source}:{source_row}")
                        pair_id = f"{split}/{category}/{index}"
                        rows.append(dict(
                            pair_id=pair_id, sample_uid=f"{pair_id}/{side}", source_row=source_row,
                            source_csv=source, split=split, category=category,
                            source_category=source_category, side=side, ground_truth=side.capitalize(),
                            text=text, source_index=index, source_annotation=annotation,
                            image_source_path=image,
                            hf_image_path=f"{split}/images_{split}/{source_category}/{name}",
                            text_sha256=digest(text.encode()), dataset_revision=REVISION,
                        ))
                inventory.append(dict(path=source, size=len(contents), rows=len(rows)-start,
                                      sha256=digest(contents),
                                      git_blob=hashlib.sha1(f"blob {len(contents)}\0".encode()+contents).hexdigest()))
    return rows, inventory


def verify_image(path, expected):
    data = path.read_bytes()
    sha = digest(data)
    if expected and sha != expected:
        raise ValueError("Published or historical SHA256 mismatch")
    with Image.open(path) as image:
        image.verify()
    with Image.open(path) as image:
        image.load()
        return sha, image.width, image.height


def attach_image(row, roots, image_root, checksums, tree, download):
    relative = row["hf_image_path"]
    expected = tree.get(relative) or checksums.get(relative)
    row.update(image_local_path="", image_sha256="", image_width="", image_height="",
               image_decode_status="NOT_RUN", download_status="MISSING",
               run_status="NOT_READY_MISSING_IMAGE", image_hash_reference="",
               expected_image_sha256=expected or "",
               image_decode_detail="")
    for root in [image_root, *roots]:
        path = root / relative
        if not path.is_file():
            continue
        try:
            sha, width, height = verify_image(path, expected)
        except (OSError, ValueError, SyntaxError) as exc:
            row.update(image_decode_status="FAILED", image_decode_detail=str(exc),
                       download_status="LOCAL_INVALID")
            continue
        row.update(image_local_path=str(path.resolve()), image_sha256=sha, image_width=width,
                   image_height=height, image_decode_status="OK", download_status="REUSED",
                   run_status="READY" if expected is not None else "NOT_READY_UNVERIFIED_IMAGE",
                   image_hash_reference="HF_LFS_SHA256" if tree.get(relative) else
                   ("HISTORICAL_SHA256" if checksums.get(relative) else "OBSERVED_SHA256"))
        return
    if download and relative in tree:
        path = image_root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        temporary = path.with_suffix(path.suffix + ".partial")
        url = f"{DATASET}/resolve/{REVISION}/{quote(relative)}"
        result = subprocess.run(["curl", "-fsSL", "--retry", "1", "--connect-timeout", "10",
                                 "--max-time", "45", url, "-o", str(temporary)], capture_output=True, text=True)
        if result.returncode:
            row.update(download_status="DOWNLOAD_FAILED", image_decode_detail=result.stderr.strip())
            return
        try:
            verify_image(temporary, expected)
            temporary.replace(path)
        except (OSError, ValueError, SyntaxError) as exc:
            row.update(download_status="DOWNLOAD_INVALID", image_decode_detail=str(exc))
            return
        attach_image(row, roots, image_root, checksums, tree, False)
        row["download_status"] = "DOWNLOADED"
        if row["image_hash_reference"] == "OBSERVED_SHA256":
            row.update(run_status="READY", image_hash_reference="OBSERVED_SHA256_PINNED_DOWNLOAD")


def duplicate_groups(items):
    groups = defaultdict(list)
    for key, uid in items:
        if key:
            groups[key].append(uid)
    return [members for members in groups.values() if len(members) > 1]


def load_frozen_tree(path):
    if path.suffix != ".csv":
        return json.loads(path.read_text())
    source = json.loads(path.with_name("source_snapshot.json").read_text())["dataset"]
    if source["tree_sha256"] != digest(path.read_bytes()):
        raise ValueError("Frozen tree file does not match its source snapshot")
    with path.open(newline="") as handle:
        entries = {row["path"]: {"oid": row["git_blob"], "sha256": row["lfs_sha256"] or None}
                   for row in csv.DictReader(handle)}
    return {"revision": source["selected_revision"], "files": entries}


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--csv-root", type=Path, required=True)
    cli.add_argument("--output", type=Path, required=True)
    cli.add_argument("--image-root", type=Path, required=True)
    cli.add_argument("--cache", type=Path, action="append", default=[])
    cli.add_argument("--historical-checksums", type=Path)
    cli.add_argument("--frozen-tree", type=Path, help="JSON entries from the fixed revision, indexed by path")
    cli.add_argument("--download", action="store_true")
    cli.add_argument("--workers", type=int, default=8)
    cli.add_argument("--download-seconds", type=float, help="Stop scheduling downloads after this many seconds")
    cli.add_argument("--attempt-log", type=Path, help="Append per-file transfer statuses for resume diagnostics")
    cli.add_argument("--previous-manifest", type=Path, action="append", default=[],
                     help="Carry prior transport failures forward for still-missing images")
    args = cli.parse_args()
    if args.download and not args.frozen_tree:
        cli.error("Downloading requires a revision-verified tree")
    rows, inventory = read_csvs(args.csv_root)
    checksums = json.loads(args.historical_checksums.read_text()) if args.historical_checksums else {}
    tree_input = load_frozen_tree(args.frozen_tree) if args.frozen_tree else {}
    if tree_input and tree_input["revision"] != REVISION:
        raise ValueError("Tree revision differs from the manifest revision")
    entries = tree_input.get("files", {})
    if args.frozen_tree and any(entries.get(row["path"], {}).get("oid") != row["git_blob"] for row in inventory):
        raise ValueError("Snapshot CSV Git blobs differ from official tree")
    tree = {p: entry.get("sha256") for p, entry in entries.items()}
    if entries and any(row["hf_image_path"] not in tree for row in rows):
        raise ValueError("CSV image reference is missing from the fixed file tree")
    pairs = defaultdict(list)
    for row in rows:
        pairs[row["pair_id"]].append(row)
    bad_pairs = [key for key, group in pairs.items()
                 if Counter(row["side"] for row in group) != Counter(SIDES)
                 or len({row["text"] for row in group}) != 1
                 or len({PurePosixPath(row["hf_image_path"]).stem.rsplit("_", 1)[0] for row in group}) != 1]
    test = [r for r in rows if r["split"] == "test"]
    train = [r for r in rows if r["split"] == "train"]
    if len(test) != 1736 or len(train) != 3864 or bad_pairs:
        raise ValueError(f"Invalid CSV row totals or pairs: {len(test)}, {len(train)}, {bad_pairs[:20]}")
    if Counter(group[0]["category"] for group in pairs.values() if group[0]["split"] == "test") != COUNTS:
        raise ValueError("Test category totals differ from the frozen data")
    for row in test:
        attach_image(row, args.cache, args.image_root, checksums, tree, False)
    if args.download:
        pending = [row for row in test if row["run_status"] != "READY"]
        # A bounded batch avoids hammering an unavailable endpoint.
        stop = False

        def stop_after_batch(_signum, _frame):
            nonlocal stop
            stop = True

        signal.signal(signal.SIGTERM, stop_after_batch)
        start_time = time.monotonic()
        window = max(1, args.workers * 4)
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            for start in range(0, len(pending), window):
                if stop or (args.download_seconds and time.monotonic() - start_time >= args.download_seconds):
                    break
                batch = pending[start:start + window]
                tasks = [pool.submit(attach_image, row, args.cache, args.image_root, checksums, tree, True)
                         for row in batch]
                for task in tasks:
                    task.result()
                print(f"Image fetch {min(start+window,len(pending))}/{len(pending)} attempted, "
                      f"{sum(r['run_status'] == 'READY' for r in batch)}/{len(batch)} ready in batch",
                      flush=True)
                if args.attempt_log:
                    with args.attempt_log.open("a") as log:
                        for row in batch:
                            log.write(json.dumps({key: row[key] for key in (
                                "sample_uid", "download_status", "image_sha256", "image_decode_detail"
                            )}) + "\n")
                if all(row["download_status"] == "DOWNLOAD_FAILED" for row in batch):
                    break

    prior_failures = {}
    for path in args.previous_manifest:
        with path.open(newline="") as handle:
            for row in csv.DictReader(handle):
                if row["dataset_revision"] == REVISION and row["download_status"] in (
                    "DOWNLOAD_FAILED", "DOWNLOAD_INVALID"
                ):
                    prior_failures[(row["sample_uid"], row["hf_image_path"])] = row
    for row in test:
        prior = prior_failures.get((row["sample_uid"], row["hf_image_path"]))
        if prior and row["download_status"] == "MISSING":
            row.update(download_status=prior["download_status"], image_decode_detail=prior["image_decode_detail"])

    def cross_split(key):
        return sorted({key(r) for r in test} & {key(r) for r in train})

    test_groups = [group for group in pairs.values() if group[0]["split"] == "test"]
    category_annotation_mismatches = Counter(
        row["side"] for row in rows if row["source_annotation"]
        and row["source_annotation"].lower().replace(" ", "_") != row["source_category"]
    )
    index_image_mismatches = sum(any(
        row["source_index"] != PurePosixPath(row["hf_image_path"]).stem.rsplit("_", 1)[0]
        for row in group) for group in pairs.values())
    leakage = {
        "test_reused_pair_text": duplicate_groups((g[0]["text"], g[0]["pair_id"]) for g in test_groups),
        "test_reused_source_image_paths": duplicate_groups((r["image_source_path"], r["sample_uid"]) for r in test),
        "test_reused_hf_image_paths": duplicate_groups((r["hf_image_path"], r["sample_uid"]) for r in test),
        "test_reused_observed_sha256": duplicate_groups((r["image_sha256"], r["sample_uid"]) for r in test),
        "train_test_exact_text_count": len(cross_split(lambda r: r["text"])),
        "train_test_normalized_text_count": len(cross_split(lambda r: normalize(r["text"]))),
        "train_test_source_image_paths": cross_split(lambda r: r["image_source_path"]),
        "train_test_hf_image_paths": cross_split(lambda r: r["hf_image_path"]),
        "train_test_normalized_text_pair_overlap_count": len(cross_split(lambda r: (r["category"], normalize(r["text"])))),
        "train_test_verified_image_sha256": sorted(({tree.get(r["hf_image_path"]) for r in train} - {None}) &
                                         ({r["image_sha256"] for r in test} - {""})),
        "train_test_official_lfs_sha256": sorted(
            ({tree.get(r["hf_image_path"]) for r in train} - {None})
            & ({tree.get(r["hf_image_path"]) for r in test} - {None})),
        "test_official_lfs_sha256_reference_count": sum(bool(tree.get(r["hf_image_path"])) for r in test),
        "train_sha256_reference_count": sum(bool(tree.get(r["hf_image_path"])) for r in train),
        "test_observed_sha256_count": sum(bool(r["image_sha256"]) for r in test),
        "scope": "Attached image hashes and frozen-tree LFS references only. No near-duplicate or training-contamination inference.",
    }
    groups = {}
    for name, expected in COUNTS.items():
        group = [p for p in test_groups if p[0]["category"] == name]
        sides = [r for p in group for r in p]
        groups[name] = dict(raw_samples=len(sides), valid_csv_pairs=expected,
                            verified_images=sum(r["run_status"] == "READY" for r in sides),
                            ready_pairs=sum(all(r["run_status"] == "READY" for r in p) for p in group),
                            missing_or_unverified=[r["sample_uid"] for r in sides if r["run_status"] != "READY"])
    output = args.output
    output.mkdir(parents=True, exist_ok=True)
    manifest = output / "test_manifest.csv"
    with manifest.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(test[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(test)
    manifest_sha = digest(manifest.read_bytes())
    (output / "test_manifest.sha256").write_text(f"{manifest_sha}  test_manifest.csv\n")
    dump(output / "data_validation.json", dict(
        revision=REVISION, manifest_sha256=manifest_sha, csv_inventory=inventory,
        csv_official_blobs_verified=bool(entries), test_samples=len(test), test_pairs=len(test_groups),
        train_samples=len(train), train_pairs=len(pairs)-len(test_groups), categories=groups,
        all_split_pairs_with_csv_index_image_number_mismatch=index_image_mismatches,
        category_annotation_mismatches=category_annotation_mismatches,
        image_decode_counts=Counter(r["image_decode_status"] for r in test),
        download_status_counts=Counter(r["download_status"] for r in test),
        run_status_counts=Counter(r["run_status"] for r in test),
        gpu_data_gate=bool(entries) and all(r["run_status"] == "READY" for r in test)))
    dump(output / "leakage_audit.json", leakage)


if __name__ == "__main__":
    main()
