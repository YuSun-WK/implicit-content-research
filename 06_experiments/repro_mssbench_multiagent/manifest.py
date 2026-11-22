"""Read and expand the fixed dataset without reading image bytes."""

import hashlib
import json
from pathlib import Path, PurePosixPath

SOURCES = json.loads(Path(__file__).with_name("sources.json").read_text())
TASKS = ("chat", "embodied")
SIDES = ("safe", "unsafe")
FIELDS = {
    "chat": {"Type", "intent", "queries", "safe_image_path", "unsafe_image",
             "unsafe_image_path"},
    "embodied": {"category", "task", "safe", "unsafe", "safe_instruction",
                 "unsafe_instruction", "safe_instructions", "unsafe_instructions",
                 "observation_safe", "observation_unsafe"},
}
LIST_FIELDS = {"queries", "safe_instructions", "unsafe_instructions"}


def sha256(data):
    return hashlib.sha256(data).hexdigest()


def read_dataset(path):
    payload = path.read_bytes()
    if sha256(payload) != SOURCES["combined_json_sha256"]:
        raise ValueError("combined.json SHA256 differs from the dataset lock")
    return json.loads(payload)


def relative_path(value):
    path = PurePosixPath(value)
    if (not value or value != path.as_posix() or not path.parts
            or path.is_absolute() or ".." in path.parts
            or any(char in value for char in ("\\", ":", "\x00"))):
        raise ValueError(f"invalid relative image path {value!r}")
    return path


def local_image(root, path):
    resolved = (root.resolve(strict=True) / relative_path(path)).resolve(strict=True)
    if not resolved.is_relative_to(root.resolve()) or not resolved.is_file():
        raise ValueError(f"image must be a file beneath the data root: {path}")
    return resolved


def record_errors(task, record):
    if not isinstance(record, dict):
        return ["record must be an object"]
    expected = FIELDS[task]
    permitted = expected | ({"reason"} if task == "chat" else set())
    errors = [f"missing {key}" for key in sorted(expected - record.keys())]
    errors += [f"unexpected {key}" for key in sorted(record.keys() - permitted)]
    for key in sorted(permitted & record.keys()):
        value = record[key]
        values = value if key in LIST_FIELDS else [value]
        if (not isinstance(values, list) or not values
                or any(not isinstance(item, str) or not item.strip() for item in values)):
            errors.append(f"invalid or empty {key}")
    if task == "embodied" and not errors:
        if len(record["safe_instructions"]) != len(record["unsafe_instructions"]):
            errors.append("different instruction list lengths")
    return errors


def expand_record(task, record, index, variant="query"):
    errors = record_errors(task, record)
    if errors:
        raise ValueError(f"{task}:{index}: {', '.join(errors)}")
    if variant not in ("query", "intent"):
        raise ValueError(f"unknown expansion {variant}")
    if task == "chat":
        texts = record["queries"] if variant == "query" else [record["intent"]]
        safe, unsafe = texts, texts
        paths = [record[f"{side}_image_path"] for side in SIDES]
        category = record["Type"]
    else:
        if variant == "query":
            safe, unsafe = (record[f"{side}_instructions"] for side in SIDES)
        else:
            safe, unsafe = ([record[f"{side}_instruction"]] for side in SIDES)
        paths = [record[side] for side in SIDES]
        category = record["category"]
    paths = [f"{task}/{relative_path(path)}" for path in paths]
    for text_index, (left, right) in enumerate(zip(safe, unsafe, strict=True)):
        pair = f"{variant}:{task}:{index:03d}:{text_index:02d}"
        for side, path, content in zip(SIDES, paths, (left, right), strict=True):
            yield {
                "dataset_revision": SOURCES["dataset_revision"],
                "pair_id": pair, "task": task, "record_index": index,
                "text_index": text_index, "variant": variant, "gold_label": side,
                "category": category, "subtask": record.get("task", ""),
                "same_text": left == right, "image_path": path, "text": content,
            }
