"""Rebuild and verify only the fixed 20-pair manifest."""
import argparse
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import csv
import hashlib
from pathlib import Path
import re
import tempfile
from urllib.parse import quote
from urllib.request import urlopen

from PIL import Image
from manifest import SOURCES, expand_record, local_image, read_dataset, relative_path, sha256

HERE = Path(__file__).parent


def csv_rows(name):
    with (HERE / name).open(newline="", encoding="utf-8") as stream:
        return list(csv.DictReader(stream))


def smoke_inputs(dataset_path):
    dataset = read_dataset(dataset_path)
    pairs = csv_rows("smoke_pairs.csv")
    full = {(r["pair_id"], r["gold_label"]): r for r in csv_rows("manifest.csv")}
    assets = {r["image_path"]: r for r in csv_rows("smoke_images.csv")}
    ids = Counter()
    rows = []
    for pair in pairs:
        key = pair["pair_id"], pair["gold_label"]
        task, index = pair["task"], int(pair["record_index"])
        row = next(r for r in expand_record(task, dataset[task][index], index)
                   if (r["pair_id"], r["gold_label"]) == key)
        asset = assets[row["image_path"]]
        for field, value in pair.items():
            if str(row[field]) != value or full[key][field] != value:
                raise ValueError(f"manifest mismatch for {key}: {field}")
        digest = sha256(row["text"].encode())
        expected_url = (f"https://huggingface.co/datasets/{SOURCES['dataset']}/resolve/"
                        f"{SOURCES['dataset_revision']}/{quote(row['image_path'])}")
        if (digest != full[key]["text_sha256"] or asset["url"] != expected_url
                or key[0] not in asset["pair_ids"].split("|")
                or asset["expected_bytes"] != full[key]["hf_size_bytes"]
                or asset["hf_lfs_sha256"] != full[key]["hf_lfs_sha256"]
                or not re.fullmatch("[0-9a-f]{64}", asset["hf_lfs_sha256"])
                or not 0 < int(asset["expected_bytes"]) <= 32 * 1024 * 1024):
            raise ValueError(f"asset metadata mismatch for {key}")
        rows.append({**row, **asset, "text_sha256": digest})
        ids[key] += 1
    if (len(rows) != 40 or len(assets) != 40 or Counter(
        (r["task"], r["gold_label"]) for r in rows
    ) != {("chat", "safe"): 10, ("chat", "unsafe"): 10,
          ("embodied", "safe"): 10, ("embodied", "unsafe"): 10}
        or len(ids) != 40 or len({k[0] for k in ids}) != 20
        or set(assets) != {r["image_path"] for r in rows}):
        raise ValueError("invalid Smoke denominator")
    return rows


def inspect_image(path, row):
    expected = int(row["expected_bytes"])
    if path.stat().st_size != expected:
        raise ValueError("image size mismatch")
    data = path.read_bytes()
    digest = sha256(data)
    if len(data) != expected or digest != row["hf_lfs_sha256"]:
        raise ValueError("image size or SHA256 mismatch")
    with Image.open(path) as image:
        mime = image.get_format_mimetype()
        if mime not in {"image/jpeg", "image/png", "image/webp"}:
            raise ValueError(f"unexpected MIME {mime}")
        image.verify()
    with Image.open(path) as image:
        image.load()
        width, height = image.size
        image.convert("RGB").load()
    return {"actual_bytes": len(data), "actual_sha256": digest, "mime": mime,
            "width": width, "height": height, "rgb_decoded": True}


def verify_asset(root, row, download):
    image_path = row["image_path"]
    result = {k: row[k] for k in ("image_path", "pair_id", "task", "gold_label",
                                  "expected_bytes", "hf_lfs_sha256")}
    result.update(actual_bytes="", actual_sha256="", mime="", width="", height="",
                  rgb_decoded=False, source="", attempts=0, status="FAIL", errors="")
    try:
        target = root / relative_path(image_path)
        if not target.resolve().is_relative_to(root):
            raise ValueError("asset escapes data root")
        if target.exists() or target.is_symlink():
            result.update(inspect_image(local_image(root, image_path), row),
                          source="local", status="PASS")
            return result
        if not download:
            raise FileNotFoundError(image_path)
        target.parent.mkdir(parents=True, exist_ok=True)
        expected = int(row["expected_bytes"])
        errors = []
        for attempt in range(1, 4):
            result["attempts"] = attempt
            with tempfile.NamedTemporaryFile(dir=target.parent, delete=False) as stream:
                temp = Path(stream.name)
                try:
                    digest = hashlib.sha256()
                    total = 0
                    with urlopen(row["url"], timeout=35) as response:
                        while block := response.read(262144):
                            total += len(block)
                            if total > expected:
                                raise ValueError("download exceeds expected bytes")
                            digest.update(block)
                            stream.write(block)
                    stream.flush()
                    if total != expected or digest.hexdigest() != row["hf_lfs_sha256"]:
                        raise ValueError("downloaded size or SHA256 mismatch")
                    result.update(inspect_image(temp, row), source="download", status="PASS")
                    temp.replace(target)
                    return result
                except (OSError, ValueError) as exc:
                    errors.append(f"{type(exc).__name__}: {exc}")
                    result["errors"] = " | ".join(errors)
                finally:
                    temp.unlink(missing_ok=True)
    except (OSError, ValueError) as exc:
        result["errors"] = f"{type(exc).__name__}: {exc}"
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-root", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    root = args.data_root.resolve(strict=True)
    rows = smoke_inputs(root / "combined.json")
    with ThreadPoolExecutor(max_workers=6) as pool:
        audit = list(pool.map(lambda row: verify_asset(root, row, args.download), rows))
    with args.out.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(audit[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(audit)
    counts = Counter(row["status"] for row in audit)
    print(dict(counts), "decoded bytes", sum(row["actual_bytes"] or 0 for row in audit))
    return int(counts["PASS"] != 40)


if __name__ == "__main__":
    raise SystemExit(main())
