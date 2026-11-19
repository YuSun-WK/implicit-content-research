"""Acquire or validate only the manifest-pinned official CLIP snapshot."""
import argparse
import hashlib
import json
from pathlib import Path
import time

BASE = Path(__file__).resolve().parent
HUB_ENDPOINT = "https://huggingface.co"


class WeightsBlocked(Exception):
    pass


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def backbone_spec():
    return json.loads((BASE / "upstream_manifest.json").read_text())["backbone"]


def inspect_files(directory, spec):
    files = {}
    for name, expected in spec["files"].items():
        path = directory / name
        if not path.is_file():
            files[name] = {"status": "missing"}
            continue
        sha = digest(path)
        files[name] = {"status": "verified" if sha == expected else "sha_mismatch",
                       "bytes": path.stat().st_size, "sha256": sha}
    return files


def require_verified(files):
    problems = [f"{name}={entry['status']}" for name, entry in files.items()
                if entry["status"] != "verified"]
    if problems:
        raise WeightsBlocked(", ".join(problems))
    return {name: entry["sha256"] for name, entry in files.items()}


def load_clip(directory):
    from transformers import CLIPModel

    model, info = CLIPModel.from_pretrained(
        directory, local_files_only=True, use_safetensors=True,
        attn_implementation="eager", output_loading_info=True)
    if any(info.get(key) for key in ("missing_keys", "mismatched_keys", "error_msgs")):
        raise WeightsBlocked("CLIPModel reported missing, mismatched or failed weights")
    return model, info.get("unexpected_keys", [])


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--download", action="store_true")
    args = parser.parse_args()
    directory = args.model_dir.resolve()
    if args.download and directory.is_relative_to(BASE.parents[1]):
        parser.error("Download the model snapshot to a directory outside the Git worktree")

    started = time.monotonic()
    spec = backbone_spec()
    report = {"repository": spec["repository"], "revision": spec["reference_revision"],
              "download_requested": args.download}
    if args.download:
        from huggingface_hub import hf_hub_download, snapshot_download
        try:
            snapshot_download(spec["repository"], revision=spec["reference_revision"], local_dir=directory,
                              allow_patterns=list(spec["files"]), token=False, endpoint=HUB_ENDPOINT)
        except (OSError, RuntimeError, ValueError) as exc:
            report["snapshot_download_error_type"] = type(exc).__name__
        missing = [name for name in spec["files"] if not (directory / name).is_file()]
        for name in missing:
            try:
                hf_hub_download(spec["repository"], name, revision=spec["reference_revision"],
                                local_dir=directory, token=False, endpoint=HUB_ENDPOINT)
            except (OSError, RuntimeError, ValueError) as exc:
                report.setdefault("file_download_errors", {})[name] = type(exc).__name__
    report["files"] = inspect_files(directory, spec)
    try:
        require_verified(report["files"])
        import torch
        from transformers import CLIPImageProcessor, CLIPTokenizerFast
        with torch.device("cpu"):
            model, unexpected = load_clip(directory)
        tokenizer = CLIPTokenizerFast.from_pretrained(directory, local_files_only=True)
        processor = CLIPImageProcessor.from_pretrained(directory, local_files_only=True)
        parameter = next(model.parameters())
        report["load"] = {"device": str(parameter.device), "dtype": str(parameter.dtype),
                          "clip_parameters": sum(p.numel() for p in model.parameters()),
                          "unexpected_keys": unexpected, "tokenizer": type(tokenizer).__name__,
                          "tokenizer_length": tokenizer.model_max_length, "crop": processor.crop_size}
        report["status"] = "VERIFIED_AND_LOADED"
    except (WeightsBlocked, OSError, ValueError, RuntimeError) as exc:
        report["status"] = "WEIGHTS_BLOCKED"
        report["validation_error_type"] = type(exc).__name__
    report["wall_s"] = round(time.monotonic() - started, 3)
    print(json.dumps(report, indent=2))
    return 0 if report["status"] == "VERIFIED_AND_LOADED" else 4


if __name__ == "__main__":
    raise SystemExit(main())
