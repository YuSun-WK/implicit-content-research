"""Export public-model provenance and local versions without paths or weights."""
import argparse
import importlib.metadata
import json
from pathlib import Path
import platform

from stage2_fetch_assets import ASSETS


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    assets = {}
    for group, (repository, revision, _) in ASSETS.items():
        manifest = json.loads((args.assets_dir / group / revision / "asset_manifest.json").read_text())
        if manifest["repository"] != repository or manifest["revision"] != revision or manifest["status"] != "VERIFIED":
            raise ValueError(f"Unverified {group} asset")
        assets[group] = manifest
    report = {"trace_upstream_commit": "83ecb799f897fe275185e082ee9a669f7d04bfaa",
              "ram_source_commit": "7cb804a8609e9f4b1a50b7f31436d2df40bb9481",
              "assets": assets, "python": platform.python_version(),
              "packages": {name: importlib.metadata.version(name) for name in
                           ("torch", "transformers", "tokenizers", "open_clip_torch", "timm",
                            "accelerate", "sentencepiece", "fairscale", "protobuf")},
              "internvl_inference_overlay": {"transformers": "4.49.0", "tokenizers": "0.21.4"}}
    args.output.write_text(json.dumps(report, indent=2) + "\n")


if __name__ == "__main__":
    main()
