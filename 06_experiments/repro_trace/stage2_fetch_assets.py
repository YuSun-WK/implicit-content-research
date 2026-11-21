"""Fetch pinned public model files outside Git, with LFS SHA-256 verification."""
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
import hashlib
import json
from pathlib import Path
import re
import subprocess
import threading
import time
from urllib.request import urlopen

ASSETS = {
    "internvl": ("OpenGVLab/InternVL2_5-8B", "e9e4c0dc1db56bfab10458671519b7fa3dd29463", (".json", ".py", ".model", ".safetensors")),
    "ram_plus": ("xinyu1205/recognize-anything-plus-model", "84d4aee3a0265c4e0df1f714f0572011d1bf2ec3", (".pth",)),
    "grounding_dino": ("IDEA-Research/grounding-dino-base", "12bdfa3120f3e7ec7b434d90674b3396eccf88eb", (".json", ".safetensors")),
    "openclip_roberta": ("laion/CLIP-ViT-B-32-roberta-base-laion2B-s12B-b32k", "e22e1c12b0a1ba4af9fb6474626585351ea0da25", (".json", ".bin")),
    "bert_tokenizer": ("google-bert/bert-base-uncased", "86b5e0934494bd15c9632b12f734a8a67f723594", ("tokenizer.json", "tokenizer_config.json", "vocab.txt")),
}
CHUNK = 16 * 1024 * 1024
WIRE_CHUNK = 3 * 1024 * 1024


def digest(path):
    result = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(8 * 1024 * 1024), b""):
            result.update(chunk)
    return result.hexdigest()


def lfs_download_action(repo, oid, size):
    body = json.dumps({"operation": "download", "transfers": ["basic"],
                       "objects": [{"oid": oid, "size": size}]}).encode()
    request = __import__("urllib.request", fromlist=["Request"]).Request(
        f"https://huggingface.co/{repo}.git/info/lfs/objects/batch", data=body,
        headers={"Accept": "application/vnd.git-lfs+json", "Content-Type": "application/vnd.git-lfs+json"})
    for attempt in range(10):
        try:
            with urlopen(request, timeout=30) as response:
                result = json.load(response)["objects"][0]
            break
        except Exception:
            if attempt == 9:
                raise
            time.sleep(min(attempt + 1, 5))
    if result["oid"] != oid or result["size"] != size:
        raise RuntimeError("LFS object does not match the pinned manifest")
    return result["actions"]["download"]


def fetch_large(repo, target, size, expected):
    """Use verified LFS ranges; long CDN connections reset on this host."""
    lock = threading.Lock()
    cached = {"config": None, "at": 0.0}

    def current_config(force=False):
        with lock:
            if force or cached["config"] is None or time.monotonic() - cached["at"] > 900:
                action = lfs_download_action(repo, expected, size)
                config = "url = " + json.dumps(action["href"]) + "\n"
                config += "".join("header = " + json.dumps(f"{key}: {value}") + "\n"
                                  for key, value in action.get("header", {}).items())
                cached.update(config=config, at=time.monotonic())
                print(f"LFS_ACTION_REFRESH {target.name}", flush=True)
            return cached["config"]

    current_config()
    parts = target.with_name(target.name + ".lfs-parts")
    parts.mkdir(exist_ok=True)
    ranges = [(i, min(i + CHUNK, size) - 1) for i in range(0, size, CHUNK)]

    def one_part(item):
        start, end = item
        part = parts / f"{start:012d}.part"
        length = end - start + 1
        if part.is_file() and part.stat().st_size == length:
            return part
        stalled = 0
        while True:
            have = part.stat().st_size if part.exists() else 0
            if have >= length:
                break
            begin = start + have
            finish = min(end, begin + WIRE_CHUNK - 1)
            chunk = part.with_suffix(".get")
            headers = part.with_suffix(".headers")
            chunk.unlink(missing_ok=True)
            headers.unlink(missing_ok=True)
            result = subprocess.run(["curl", "-sS", "-f", "--connect-timeout", "8",
                                     "--max-time", "48", "--speed-limit", "4096", "--speed-time", "6",
                                     "--range", f"{begin}-{finish}", "--dump-header", str(headers),
                                     "--output", str(chunk), "--config", "-"], input=current_config(),
                                    capture_output=True, text=True)
            response = headers.read_text(errors="replace") if headers.exists() else ""
            ranges = re.findall(r"(?im)^content-range: bytes (\d+)-(\d+)/(\d+)", response)
            gained = 0
            if ranges and tuple(map(int, ranges[-1])) == (begin, finish, size) and chunk.exists():
                if 0 < chunk.stat().st_size <= finish - begin + 1:
                    with part.open("ab") as output, chunk.open("rb") as source:
                        for block in iter(lambda: source.read(1024 * 1024), b""):
                            output.write(block)
                    gained = chunk.stat().st_size
            chunk.unlink(missing_ok=True)
            headers.unlink(missing_ok=True)
            if gained:
                stalled = 0
            else:
                stalled += 1
                if "403" in result.stderr or stalled % 8 == 0:
                    current_config(force=True)
                if stalled >= 200:
                    raise RuntimeError(f"LFS range stalled: {target.name} {start}-{end}")
                time.sleep(min(3, stalled * 0.3))
        if part.stat().st_size != length:
            raise RuntimeError(f"LFS part length mismatch: {target.name} {start}-{end}")
        return part

    with ThreadPoolExecutor(max_workers=8) as pool:
        futures = [pool.submit(one_part, item) for item in ranges]
        for completed, future in enumerate(as_completed(futures), 1):
            future.result()
            if completed % 25 == 0 or completed == len(ranges):
                print(f"PARTS {target.name} {completed}/{len(ranges)}", flush=True)
    assembled = target.with_name(target.name + ".assembling")
    hasher = hashlib.sha256()
    with assembled.open("wb") as destination:
        for start, _ in ranges:
            with (parts / f"{start:012d}.part").open("rb") as stream:
                for block in iter(lambda: stream.read(8 * 1024 * 1024), b""):
                    destination.write(block)
                    hasher.update(block)
    if assembled.stat().st_size != size or hasher.hexdigest() != expected:
        raise RuntimeError(f"Assembled SHA-256 mismatch: {target.name}")
    assembled.replace(target)
    for part in parts.iterdir():
        part.unlink()
    parts.rmdir()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--group", choices=ASSETS, required=True)
    parser.add_argument("--root", type=Path, required=True, help="Asset directory outside Git")
    args = parser.parse_args()
    repo, revision, suffixes = ASSETS[args.group]
    url = f"https://huggingface.co/api/models/{repo}/tree/{revision}?recursive=true&expand=true"
    with urlopen(url, timeout=30) as response:
        entries = json.load(response)
    files = [entry for entry in entries if entry["path"].endswith(suffixes) and "/" not in entry["path"]]
    if not files:
        raise RuntimeError("No matching official model files")
    directory = args.root / args.group / revision
    directory.mkdir(parents=True, exist_ok=True)
    report = {"repository": repo, "revision": revision, "files": {}}
    for entry in files:
        name = entry["path"]
        target = directory / name
        expected = entry.get("lfs", {}).get("oid")
        size = entry.get("size")
        if target.is_file() and target.stat().st_size == size and (not expected or digest(target) == expected):
            print(f"REUSE {name}", flush=True)
        else:
            source = f"https://huggingface.co/{repo}/resolve/{revision}/{name}"
            if expected and size > CHUNK:
                fetch_large(repo, target, size, expected)
            else:
                result = subprocess.run(["curl", "-sS", "-fL", "--retry", "10", "--retry-all-errors",
                                         "--connect-timeout", "15", "--max-time", "90",
                                         "-o", str(target), source], check=False)
                if result.returncode or target.stat().st_size != size or (expected and digest(target) != expected):
                    raise RuntimeError(f"Could not obtain verified official file: {name}")
        actual = digest(target)
        report["files"][name] = {"bytes": size, "sha256": actual, "lfs_sha256_match": expected is None or actual == expected}
        print(f"VERIFIED {name} {size} {actual}", flush=True)
    report["status"] = "VERIFIED"
    (directory / "asset_manifest.json").write_text(json.dumps(report, indent=2) + "\n")
    print(f"COMPLETE {args.group}", flush=True)


if __name__ == "__main__":
    main()
