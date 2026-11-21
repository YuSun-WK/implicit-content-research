"""One bounded Train/Dev collapse audit of best versus last checkpoint."""
import argparse
from collections import defaultdict
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import statistics

from stage2_train import MODEL_NAME, REVISION, author_class, forward_components, load_rows


def percentile(values, fraction):
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int((len(ordered) - 1) * fraction))]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--caption-manifest", type=Path, required=True)
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    import open_clip
    from open_clip.tokenizer import HFTokenizer
    import torch
    from PIL import Image
    if torch.cuda.device_count() != 1:
        raise RuntimeError("Expose exactly one GPU")
    device = torch.device("cuda:0")
    directory = args.assets_dir / "openclip_roberta" / REVISION
    weight = directory / "open_clip_pytorch_model.bin"
    asset = json.loads((directory / "asset_manifest.json").read_text())
    if asset["files"][weight.name]["sha256"] != hashlib.sha256(weight.read_bytes()).hexdigest():
        raise ValueError("Unverified backbone")
    rows = load_rows(args.data_dir, args.caption_manifest)
    base, _, preprocess = open_clip.create_model_and_transforms(
        MODEL_NAME, pretrained=str(weight), pretrained_hf=False, device="cpu")
    tokenizer = HFTokenizer(str(directory), context_length=77, local_files_only=True)
    classifier, _ = author_class(Path("/tmp/trace-s0-reference"), torch)
    with redirect_stdout(io.StringIO()):
        model = classifier(base).to(device)
    torch.cuda.set_per_process_memory_fraction(min(1.0, 18 * 1024**3 / torch.cuda.get_device_properties(0).total_memory))
    trainable = {name: p for name, p in model.named_parameters() if p.requires_grad}

    def run_split(split):
        probabilities, labels = [], []
        model.eval()
        with torch.inference_mode():
            for offset in range(0, len(rows[split]), 32):
                examples = rows[split][offset:offset + 32]
                images = []
                texts = []
                for path, original, generated, label in examples:
                    with Image.open(path) as image:
                        images.append(preprocess(image.convert("RGB")))
                    texts.extend((original, generated))
                    labels.append(label)
                image = torch.stack(images).to(device)
                token = tokenizer(texts).reshape(len(examples), 2, -1).to(device)
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    logits, _, _ = forward_components(model, image, token, None, 0.1, False, torch)
                probabilities.extend(logits.float().sigmoid().cpu().tolist())
        grouped = defaultdict(list)
        for label, value in zip(labels, probabilities):
            grouped[label].append(value)
        return {"n": len(probabilities), "predicted_positive_at_0_5": sum(p >= 0.5 for p in probabilities),
                "probability_min": min(probabilities), "probability_p10": percentile(probabilities, 0.1),
                "probability_median": statistics.median(probabilities),
                "probability_p90": percentile(probabilities, 0.9), "probability_max": max(probabilities),
                "mean_by_label": {str(label): statistics.mean(values) for label, values in grouped.items()}}

    report = {}
    for checkpoint_name in ("best.pt", "last.pt"):
        state = torch.load(args.run_dir / checkpoint_name, map_location="cpu", weights_only=True)
        with torch.no_grad():
            for name, p in trainable.items():
                p.copy_(state["trainable"][name])
        report[checkpoint_name] = {split: run_split(split) for split in ("train", "dev")}
    events = [json.loads(line) for line in (args.run_dir / "events.jsonl").read_text().splitlines()]
    gradients = [event["gradients"] for event in events if event["event"] == "batch" and event.get("gradients")]
    report["last_10_updates_gradient_norm_mean"] = {
        name: statistics.mean(item[name] for item in gradients[-10:]) for name in gradients[-1]}
    report["scope"] = "train_and_dev_only_no_test_no_retraining"
    args.output.write_text(json.dumps(report, indent=2, allow_nan=False) + "\n")


if __name__ == "__main__":
    main()
