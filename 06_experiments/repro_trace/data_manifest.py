"""Local FHM inventory. Output contains aggregate metadata only."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

FIELDS = ("text", "ivl_8b_new_caption", "gemini_caption")
SPLITS = ("train", "dev_seen", "dev_unseen", "test_seen", "test_unseen")
PLACEHOLDERS = {"no caption", "nan", "none", "null", "n/a", "na", "caption unavailable", "no caption available"}
PROVENANCE = (
    "dataset_source", "dataset_revision", "ivl_8b_new_caption_source",
    "ivl_8b_new_caption_model", "ivl_8b_new_caption_revision",
    "gemini_caption_source", "gemini_caption_model", "gemini_caption_revision",
)


def read_rows(path, split=None):
    with Path(path).open(encoding="utf-8-sig") as stream:
        if Path(path).suffix.lower() == ".jsonl":
            rows = [json.loads(line) for line in stream if line.strip()]
        else:
            rows = json.load(stream)
    if not isinstance(rows, list) or any(not isinstance(row, dict) for row in rows):
        raise ValueError("Expected a JSON array or JSONL records")
    if split is not None:
        if split not in SPLITS or any(row.get("split", split) != split for row in rows):
            raise ValueError("Invalid split or conflicting split in split-specific file")
        rows = [dict(row, split=split) for row in rows]
    return rows


def caption_state(value):
    if isinstance(value, str):
        normalized = " ".join(value.casefold().split())
        if not normalized:
            return "missing"
        return "placeholder" if normalized in PLACEHOLDERS else "present"
    if isinstance(value, float) and value != value:
        return "placeholder"
    return "missing" if value is None else "invalid"


def image_candidate(root, value):
    if not isinstance(value, str) or not value.strip():
        return None
    if Path(value).is_absolute():
        return None
    try:
        candidate = (root / value).resolve()
    except (OSError, RuntimeError, ValueError):
        return None
    if not candidate.is_relative_to(root):
        return None
    return candidate


def image_path(root, value):
    candidate = image_candidate(root, value)
    return candidate if candidate is not None and candidate.is_file() else None


def image_readable(path):
    from PIL import Image
    try:
        with Image.open(path) as image:
            image.verify()
        with Image.open(path) as image:
            image.load()
    except (OSError, SyntaxError, ValueError, Image.DecompressionBombError):
        return False
    return True


def label_key(label):
    return str(int(label)) if type(label) in (int, float) and label in (0, 1) else "missing_or_invalid"


def identity(row):
    value = row.get("id")
    if type(value) is int:
        return str(value)
    if isinstance(value, str) and value.strip():
        value = value.strip()
        if value.isascii() and value.isdecimal():
            return value.lstrip("0") or "0"
        return value
    return None


def summary(rows, image_root, tokenizer=None, *, verify_splits=()):
    image_root = Path(image_root).resolve()
    result = {"dataset": "FHM", "input_rows": len(rows), "unknown_split_rows": 0, "splits": {}}
    grouped = {split: [] for split in SPLITS}
    for row in rows:
        split = row.get("split")
        if isinstance(split, str) and split in grouped:
            grouped[split].append(row)
        else:
            result["unknown_split_rows"] += 1
    seen = {"id": Counter(), "image_ref": Counter()}
    image_checks = {}
    for split, items in grouped.items():
        candidates = [image_candidate(image_root, row.get("img")) for row in items]
        images = [path if path is not None and path.is_file() else None for path in candidates]
        resolved = Counter(path for path in images if path is not None)
        unreadable = None
        if split in verify_splits:
            for path in resolved:
                if path not in image_checks:
                    image_checks[path] = image_readable(path)
            unreadable = sum(count for path, count in resolved.items() if not image_checks[path])
        labels = Counter(label_key(row.get("label")) for row in items)
        ids = Counter(key for row in items if (key := identity(row)) is not None)
        refs = Counter(row["img"] for row in items if isinstance(row.get("img"), str) and row["img"].strip())
        mismatched_ids = 0
        for row, path in zip(items, candidates):
            key = identity(row)
            if key is not None and key.isascii() and key.isdecimal() and path is not None:
                # Numeric identifiers may be zero-padded in FHM file names.
                stem = path.stem
                mismatched_ids += not stem.isascii() or not stem.isdecimal() or (stem.lstrip("0") or "0") != key
        exact_rows = Counter(
            hashlib.sha256(json.dumps(row, sort_keys=True).encode()).digest() for row in items
        )
        for bucket, keys in ((seen["id"], ids), (seen["image_ref"], refs)):
            bucket.update(keys.keys())
        counts = {
            "rows": len(items),
            "labels": {key: labels[key] for key in ("0", "1", "missing_or_invalid")},
            "images_missing_or_outside_root": sum(path is None for path in images),
            "images_invalid_path": sum(path is None for path in candidates),
            "images_missing": sum(path is not None and image is None for path, image in zip(candidates, images)),
            "images_unreadable": unreadable,
            "duplicate_resolved_image_rows_beyond_first": sum(count - 1 for count in resolved.values()),
            "id_missing": len(items) - sum(ids.values()),
            "numeric_id_image_mismatch": mismatched_ids,
            "duplicate_id_rows_beyond_first": sum(count - 1 for count in ids.values()),
            "duplicate_image_ref_rows_beyond_first": sum(count - 1 for count in refs.values()),
            "exact_duplicate_rows_beyond_first": sum(count - 1 for count in exact_rows.values()),
            "label_scoring_available": bool(items) and not labels["missing_or_invalid"],
            "captions": {},
            "provenance_fields_present": {
                field: sum(caption_state(row.get(field)) == "present" for row in items)
                for field in PROVENANCE
            },
        }
        for field in FIELDS:
            nonempty = [row[field] for row in items if caption_state(row.get(field)) == "present"]
            states = Counter(caption_state(row.get(field)) for row in items)
            counts["captions"][field] = {
                key: states[key] for key in ("present", "missing", "invalid", "placeholder")
            }
            counts["captions"][field]["max_tokens_before_truncation"] = (
                max((len(tokenizer.encode(x, truncation=False, verbose=False)) for x in nonempty), default=None)
                if tokenizer is not None else None
            )
        result["splits"][split] = counts
    result["cross_split_repeated_keys"] = {
        key: sum(count > 1 for count in counts.values()) for key, counts in seen.items()
    }
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", action="append", default=[], type=Path, help="Combined FHM JSON/JSONL")
    parser.add_argument("--split-file", nargs=2, action="append", default=[], metavar=("SPLIT", "PATH"))
    parser.add_argument("--image-root", required=True, type=Path)
    parser.add_argument("--tokenizer", type=Path, help="Local Hugging Face CLIP tokenizer directory")
    parser.add_argument("--verify-images", action="store_true", help="Verify and decode every referenced image")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    if not args.data and not args.split_file:
        parser.error("Provide --data or --split-file")
    tokenizer = None
    if args.tokenizer:
        from transformers import CLIPTokenizerFast
        tokenizer = CLIPTokenizerFast.from_pretrained(args.tokenizer, local_files_only=True)
    rows = [row for path in args.data for row in read_rows(path)]
    rows.extend(row for split, path in args.split_file for row in read_rows(path, split))
    report = summary(rows, args.image_root, tokenizer, verify_splits=SPLITS if args.verify_images else ())
    if report["unknown_split_rows"]:
        report["schema_status"] = "unrecognized_split_rows"
    rendered = json.dumps(report, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered, encoding="utf-8")
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
