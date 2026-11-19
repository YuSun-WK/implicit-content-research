"""Materialize selected official model artifacts and verify the pinned metadata."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import hashlib
import json
from pathlib import Path
import subprocess
from urllib.parse import quote

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


def stage_file(root, artifact, entry):
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
    url = f"https://huggingface.co/{model}/resolve/{revision}/{quote(name)}?download=true"
    for attempt in range(1, 4):
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
    args = parser.parse_args()
    root = args.root.resolve(strict=True)
    plan = {}
    for artifact in ARTIFACTS:
        metadata = json.loads((root / f"{artifact}.metadata.json").read_text())
        plan[artifact] = locked_files(metadata, artifact)
    with ThreadPoolExecutor(max_workers=5) as pool:
        jobs = {(artifact, entry["rfilename"]): pool.submit(stage_file, root, artifact, entry)
                for artifact, entries in plan.items() for entry in entries}
        results = {artifact: [job.result() for (label, _), job in jobs.items() if label == artifact]
                   for artifact in ARTIFACTS}
    payload = {key: {"model_id": ARTIFACTS[key][0],
                     "revision": SOURCES[ARTIFACTS[key][1]], "files": files}
               for key, files in results.items()}
    (root / "weights_verified.json").write_text(json.dumps(payload, indent=2) + "\n")


if __name__ == "__main__":
    main()
