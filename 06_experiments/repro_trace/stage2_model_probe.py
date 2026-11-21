"""CPU-only pinned OpenCLIP/TRACE structural probe; emits aggregate JSON."""
import argparse
from collections import Counter
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path

from stage2_train import MODEL_NAME, REVISION, author_class, in_group


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--upstream-dir", type=Path, default=Path("/tmp/trace-s0-reference"))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    import open_clip
    import torch
    from open_clip.tokenizer import HFTokenizer
    directory = args.assets_dir / "openclip_roberta" / REVISION
    manifest = json.loads((directory / "asset_manifest.json").read_text())
    weight = directory / "open_clip_pytorch_model.bin"
    sha = hashlib.sha256(weight.read_bytes()).hexdigest()
    if manifest["files"][weight.name]["sha256"] != sha or manifest["status"] != "VERIFIED":
        raise ValueError("Pinned OpenCLIP weight mismatch")
    base, _, _ = open_clip.create_model_and_transforms(
        MODEL_NAME, pretrained=str(weight), pretrained_hf=False, device="cpu")
    tokenizer = HFTokenizer(str(directory), context_length=77, local_files_only=True)
    classifier, source_sha = author_class(args.upstream_dir, torch)
    with redirect_stdout(io.StringIO()):
        model = classifier(base)
    groups = Counter()
    for name, parameter in model.named_parameters():
        if parameter.requires_grad:
            head = next((group for group in ("clip_model.text", "caption_scorer", "image_projection",
                                             "text_projection", "cross_attn", "cross_attn_reverse",
                                             "pre_output", "classifier") if in_group(name, group)), "other")
            groups[head] += parameter.numel()
    output = {"architecture": "TRACE-InternVL-only-MultiOFF-2caption", "upstream_source_sha256": source_sha,
              "backbone": MODEL_NAME, "backbone_revision": REVISION, "pretrained_sha256": sha,
              "open_clip_version": open_clip.__version__, "torch_version": str(torch.__version__),
              "tokenizer": type(tokenizer.tokenizer).__name__, "tokenizer_context_length": 77,
              "total_parameters": sum(parameter.numel() for parameter in model.parameters()),
              "trainable_parameters": sum(groups.values()), "trainable_groups": dict(groups),
              "visual_trainable_parameters": sum(parameter.numel() for parameter in model.clip_model.visual.parameters()
                                                 if parameter.requires_grad)}
    rendered = json.dumps(output, indent=2) + "\n"
    if args.output:
        args.output.write_text(rendered)
    else:
        print(rendered, end="")


if __name__ == "__main__":
    main()
