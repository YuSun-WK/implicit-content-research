"""Materialize selected official model artifacts and verify the pinned metadata."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import re
import shutil
import subprocess
import tempfile
from urllib.parse import quote, urlencode

from manifest import SOURCES, relative_path

ARTIFACTS = {
    "native": ("liuhaotian/llava-v1.6-vicuna-7b", "llava_original_revision",
               {"config.json", "generation_config.json", "tokenizer.model",
                "tokenizer_config.json", "special_tokens_map.json",
                "model.safetensors.index.json", "model-00001-of-00003.safetensors",
                "model-00002-of-00003.safetensors", "model-00003-of-00003.safetensors"}),
    "clip": ("openai/clip-vit-large-patch14-336", "clip_revision",
             {"config.json", "pytorch_model.bin", "preprocessor_config.json"}),
}


MIRRORS = {
    "native": ("AI-ModelScope/llava-v1.6-vicuna-7b", "9bc88088944aefd1a04cb8e60f7799855c680b44"),
    "clip": ("AI-ModelScope/clip-vit-large-patch14-336", "ff5f616e6203df089a05407938e295f4de2bf7ed"),
}


def digest_file(path, algorithm, prefix=b""):
    digest = hashlib.new(algorithm, prefix)
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(4 * 1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def locked_files(metadata, artifact):
    model_id, revision_key, names = ARTIFACTS[artifact]
    revision = SOURCES[revision_key]
    if metadata["id"] != model_id or metadata["sha"] != revision:
        raise ValueError(f"incorrect HF model metadata for {artifact}")
    selected = [entry for entry in metadata["siblings"] if entry["rfilename"] in names]
    if {entry["rfilename"] for entry in selected} != names:
        raise ValueError(f"incomplete model artifact manifest for {artifact}")
    return selected


def verify_file(path, entry):
    size = entry["size"]
    if not path.is_file() or path.stat().st_size != size:
        raise ValueError(f"size mismatch: {path.name}")
    if "lfs" in entry:
        checksum = digest_file(path, "sha256")
        if checksum != entry["lfs"]["sha256"]:
            raise ValueError(f"LFS SHA256 mismatch: {path.name}")
    else:
        oid = digest_file(path, "sha1", f"blob {size}\0".encode())
        if oid != entry["blobId"]:
            raise ValueError(f"Git blob OID mismatch: {path.name}")
        checksum = digest_file(path, "sha256")
    return {"path": entry["rfilename"], "bytes": size, "sha256": checksum}


def validate_range(headers, received, start, end, size):
    # curl dumps the proxy/redirect headers before the final response.
    blocks = re.split(r"\r?\n\r?\n", headers.strip())
    final = blocks[-1].splitlines()
    ranges = [line.split(":", 1)[1].strip() for line in final[1:]
              if line.lower().startswith("content-range:")]
    return (bool(re.match(r"HTTP/\S+ 206(?: |$)", final[0])) if final else False
            ) and ranges == [f"bytes {start}-{end}/{size}"] and received == end - start + 1


def download_ranges(part, url, size, chunk_bytes):
    offset = part.stat().st_size if part.exists() else 0
    if offset > size:
        raise ValueError(f"partial file too large: {part.name}")
    with tempfile.TemporaryDirectory(dir=part.parent) as folder:
        block = Path(folder) / "block"
        headers = Path(folder) / "headers"
        while offset < size:
            end = min(offset + chunk_bytes, size) - 1
            for attempt in range(1, 4):
                block.unlink(missing_ok=True)
                headers.unlink(missing_ok=True)
                result = subprocess.run(
                    ["curl", "-fsSL", "--connect-timeout", "10", "--max-time", "75",
                     "--max-filesize", str(end - offset + 1), "--range", f"{offset}-{end}",
                     "--dump-header", str(headers), "--output", str(block), url],
                    capture_output=True, text=True,
                )
                if (result.returncode == 0 and block.is_file() and headers.is_file()
                        and validate_range(headers.read_text(), block.stat().st_size, offset, end, size)):
                    with block.open("rb") as source, part.open("ab") as destination:
                        shutil.copyfileobj(source, destination)
                    offset = end + 1
                    print(f"{part.name}: accepted range through {offset}/{size}", flush=True)
                    break
                print(f"{part.name}: range {offset}-{end}; attempt {attempt}; "
                      f"curl={result.returncode}; {result.stderr.strip()}", flush=True)
            else:
                raise ValueError(f"range transfer stopped at {offset}/{size}: {part.name}")


def mirror_urls(artifact, entries, manifest):
    model, revision = MIRRORS[artifact]
    files = {row["Path"]: row for row in manifest["Data"]["Files"] if row["Type"] == "blob"}
    urls = {}
    for entry in entries:
        name = entry["rfilename"]
        row = files[name]
        if row["Size"] != entry["size"] or row["Revision"] != revision:
            raise ValueError(f"mirror revision or size mismatch: {artifact}/{name}")
        if "lfs" in entry and row["Sha256"] != entry["lfs"]["sha256"]:
            raise ValueError(f"mirror LFS SHA256 mismatch: {artifact}/{name}")
        query = urlencode({"Revision": revision, "FilePath": name})
        urls[name] = f"https://modelscope.cn/api/v1/models/{model}/repo?{query}"
    return urls


def stage_file(root, artifact, entry, chunk_bytes=0, mirror_url=None):
    model, revision_key, _ = ARTIFACTS[artifact]
    revision = SOURCES[revision_key]
    name = entry["rfilename"]
    target = root / artifact / relative_path(name)
    if not target.resolve().is_relative_to(root.resolve()):
        raise ValueError("model asset escapes cache root")
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        result = verify_file(target, entry)
        print(f"{artifact}/{name}: verified cache", flush=True)
        return result
    part = target.with_suffix(target.suffix + ".part")
    if part.is_symlink() or not part.resolve().is_relative_to(root.resolve()):
        raise ValueError("invalid partial asset path")
    url = mirror_url or f"https://huggingface.co/{model}/resolve/{revision}/{quote(name)}?download=true"
    if chunk_bytes:
        download_ranges(part, url, entry["size"], chunk_bytes)
    for attempt in range(1, 4) if not chunk_bytes else ():
        if part.exists() and part.stat().st_size == entry["size"]:
            break
        cmd = ["curl", "-fsSL", "--connect-timeout", "15", "--max-time", "900", "--speed-limit", "131072", "--speed-time", "35",
               "--max-filesize", str(entry["size"]), "--continue-at", "-", url, "-o", str(part)]
        response = subprocess.run(cmd, capture_output=True, text=True)
        print(f"{artifact}/{name}: attempt {attempt}; curl={response.returncode}; "
              f"bytes={part.stat().st_size if part.exists() else 0}; {response.stderr.strip()}", flush=True)
        if response.returncode == 0:
            break
    result = verify_file(part, entry)
    part.replace(target)
    print(f"{artifact}/{name}: {result['bytes']} bytes, SHA256 {result['sha256']}", flush=True)
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("root", type=Path)
    parser.add_argument("--range-mib", type=int, choices=(1, 4, 16, 64), default=0,
                        help="require exact HTTP 206 ranges for LFS artifacts")
    parser.add_argument("--mirror-metadata", type=Path, help="directory of ModelScope listing JSON")
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    plan = {}
    for artifact in ARTIFACTS:
        metadata = json.loads((root / f"{artifact}.metadata.json").read_text())
        plan[artifact] = locked_files(metadata, artifact)
    urls = {
        key: mirror_urls(key, entries, json.loads(
            (args.mirror_metadata / f"{key}.modelscope.json").read_text()))
        for key, entries in plan.items()
    } if args.mirror_metadata else {}
    with ThreadPoolExecutor(max_workers=4) as pool:
        jobs = {(artifact, entry["rfilename"]): pool.submit(stage_file, root, artifact, entry,
                                  args.range_mib * 2**20 if "lfs" in entry else 0,
                                  urls.get(artifact, {}).get(entry["rfilename"]))
                for artifact, entries in plan.items() for entry in entries}
        results = {artifact: [job.result() for (label, _), job in jobs.items() if label == artifact]
                   for artifact in ARTIFACTS}
    payload = {key: {"model_id": ARTIFACTS[key][0],
                     "revision": SOURCES[ARTIFACTS[key][1]], "files": files}
               for key, files in results.items()}
    with tempfile.NamedTemporaryFile(mode="w", dir=root, delete=False, encoding="utf-8") as stream:
        lock = Path(stream.name)
        json.dump(payload, stream, indent=2)
        stream.write("\n")
    lock.replace(root / "weights_verified.json")


if __name__ == "__main__":
    main()
