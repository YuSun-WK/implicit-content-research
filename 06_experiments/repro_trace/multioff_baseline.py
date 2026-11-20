"""Adapted TRACE-author MultiOFF projection baseline on official raw splits."""
import argparse
import ast
from collections import Counter
import copy
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import random
import statistics
import subprocess
import time
from types import SimpleNamespace

from data_manifest import image_path, image_readable
from prepare_clip import backbone_spec, digest, inspect_files, load_clip, require_verified
from run_stage0 import BUDGET, check_budget, local_path, restore, rng_state, save_checkpoint

UPSTREAM = "83ecb799f897fe275185e082ee9a669f7d04bfaa"
SOURCE_HASH = "c77ed85a4979e847eb224ec97c413e1c955d83f69c7836fa6198d1c8c6e366fb"
PROTOCOL = "adapted_author_baseline"
SPLITS = {"train": "Training", "dev": "Validation", "test": "Testing"}
LABELS = {"offensive": 1, "Non-offensiv": 0}
SEED = 42
MAX_EPOCHS = 20


def admit(root):
    directory = (root / "Labelled Images").resolve()
    datasets, stats, hashes = {}, {}, {}
    occupied = {}
    for split, filename in SPLITS.items():
        csv_path = root / "Split Dataset" / f"{filename}_meme_dataset.csv"
        with csv_path.open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ["image_name", "sentence", "label"]:
                raise ValueError("Unexpected official CSV columns")
            rows = list(reader)
        labels = Counter(row["label"] for row in rows)
        refs = Counter(row["image_name"] for row in rows)
        samples, content_hashes = [], []
        missing = invalid = unreadable = 0
        for row in rows:
            name, sentence, label = row["image_name"], row["sentence"], row["label"]
            if not name or Path(name).name != name or not sentence or not sentence.strip() or label not in LABELS:
                invalid += 1
                continue
            path = image_path(directory, name)
            if path is None:
                missing += 1
                continue
            if not image_readable(path):
                unreadable += 1
                continue
            checksum = digest(path)
            content_hashes.append(checksum)
            samples.append((path, sentence, LABELS[label]))
            occupied.setdefault(checksum, set()).add(split)
        hashes[split] = {"csv_sha256": digest(csv_path),
                         "ordered_images_sha256": hashlib.sha256("".join(content_hashes).encode()).hexdigest()}
        datasets[split] = samples
        stats[split] = {"rows": len(rows), "offensive": labels["offensive"],
                        "non_offensive": labels["Non-offensiv"],
                        "usable_rows": len(samples), "usable_offensive": sum(row[2] for row in samples),
                        "usable_non_offensive": len(samples) - sum(row[2] for row in samples),
                        "duplicate_names": sum(count - 1 for count in refs.values()),
                        "duplicate_image_bytes": len(content_hashes) - len(set(content_hashes)),
                        "missing_images": missing, "invalid_rows": invalid, "unreadable_images": unreadable}
    overlap = Counter("+".join(sorted(splits)) for splits in occupied.values() if len(splits) > 1)
    return datasets, {"splits": stats, "hashes": hashes, "cross_split_identical_image_hashes": dict(overlap)}


def author_classes(root, torch, factory):
    head = subprocess.check_output(["git", "-C", root, "rev-parse", "HEAD"], text=True).strip()
    path = Path(root) / "MultiOFF/multioff_proj_ft.py"
    if head != UPSTREAM or digest(path) != SOURCE_HASH:
        raise ValueError("Wrong TRACE projection source")
    tree = ast.parse(path.read_text(), filename=str(path))
    tree.body = [node for node in tree.body if getattr(node, "name", None) in {"CLIPClassifier", "FocalLoss", "collate_fn"}]
    namespace = {"torch": torch, "nn": torch.nn, "F": torch.nn.functional, "copy": copy,
                 "AutoModel": SimpleNamespace(from_pretrained=factory)}
    exec(compile(tree, str(path), "exec"), namespace)
    return namespace["CLIPClassifier"], namespace["FocalLoss"], namespace["collate_fn"]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", required=True, type=Path)
    parser.add_argument("--model-dir", type=Path)
    parser.add_argument("--upstream-dir", default="/tmp/trace-s0-reference")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--phase", required=True, choices=("audit", "smoke", "short", "formal"))
    parser.add_argument("--microbatch", type=int, choices=(1, 8, 16, 32), default=1)
    parser.add_argument("--smoke-checkpoint", type=Path)
    parser.add_argument("--short-log", type=Path)
    parser.add_argument("--stop-after", type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--complete-case", action="store_true",
                        help="Explicitly allow exclusion of rows whose official image is absent")
    args = parser.parse_args()
    output = local_path(args.output_dir)
    output.mkdir(parents=True, exist_ok=args.resume)
    rows, audit = admit(args.data_dir.resolve())
    audit["admission_policy"] = "complete_case" if args.complete_case else "full_split"
    (output / "admission.json").write_text(json.dumps(audit, indent=2) + "\n")
    invalid_fields = ["duplicate_names", "invalid_rows", "unreadable_images"]
    if not args.complete_case:
        invalid_fields.append("missing_images")
    if any(not stats["usable_offensive"] or not stats["usable_non_offensive"]
           or any(stats[key] for key in invalid_fields) for stats in audit["splits"].values()
           ) or audit["cross_split_identical_image_hashes"]:
        raise ValueError("Official data admission failed; see aggregate admission.json")
    if args.phase == "audit":
        return
    if args.stop_after is not None and (args.phase != "short" or not 1 <= args.stop_after < 100):
        parser.error("--stop-after requires short phase and an intermediate cursor")

    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", CUBLAS_WORKSPACE_CONFIG=":4096:8")
    import torch
    from PIL import Image
    from sklearn.metrics import accuracy_score, f1_score, roc_auc_score
    from transformers import CLIPImageProcessor, CLIPProcessor, CLIPTokenizerFast, __version__

    started = time.monotonic()
    if torch.cuda.device_count() != 1 or not torch.cuda.is_bf16_supported():
        raise RuntimeError("Expose exactly one BF16 CUDA device")
    device = torch.device("cuda:0")
    gpu = torch.cuda.get_device_properties(0)
    if "RTX 4090" not in gpu.name:
        raise RuntimeError("Use one RTX 4090 or 4090D")
    torch.cuda.set_per_process_memory_fraction(min(1.0, BUDGET / gpu.total_memory))
    torch.cuda.reset_peak_memory_stats()
    torch.use_deterministic_algorithms(True)
    random.seed(SEED)
    torch.manual_seed(SEED)
    spec = backbone_spec()
    hashes = require_verified(inspect_files(args.model_dir, spec))
    classifier, focal, collate = author_classes(args.upstream_dir, torch, lambda _: load_clip(args.model_dir)[0])
    model = classifier(model_path=str(args.model_dir), fusion_type="align",
                       weight_image_loss=0.3, weight_text_loss=0.7).to(device)
    tokenizer = CLIPTokenizerFast.from_pretrained(args.model_dir, local_files_only=True)
    processor = CLIPProcessor(
        image_processor=CLIPImageProcessor.from_pretrained(args.model_dir, local_files_only=True),
        tokenizer=tokenizer,
    )
    trainable = {name: p for name, p in model.named_parameters() if p.requires_grad}
    optimizer = torch.optim.AdamW(trainable.values(), lr=1e-4, weight_decay=1e-4)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.1, patience=2)
    scaler = torch.amp.GradScaler("cuda", enabled=False)
    signature = {"protocol": PROTOCOL, "source": SOURCE_HASH, "revision": spec["reference_revision"],
                 "backbone_sha256": hashes["model.safetensors"], "data": audit["hashes"], "seed": SEED,
                 "admission_policy": audit["admission_policy"],
                 "microbatch": args.microbatch, "torch": str(torch.__version__), "transformers": __version__}
    run_signature = {**signature, "phase": args.phase}
    event_file = output / "events.jsonl"

    def log(event, **details):
        with event_file.open("a") as stream:
            stream.write(json.dumps({"event": event, "protocol": PROTOCOL, "phase": args.phase,
                                     "elapsed_s": time.monotonic() - started, **details}, allow_nan=False) + "\n")

    def require_run_evidence(path, phase):
        events = [json.loads(line) for line in local_path(path).read_text().splitlines()]
        if (events[0].get("signature") != {**signature, "phase": phase}
                or events[-1].get("event") != "completed" or events[-1].get("phase") != phase
                or not any(event["event"] == "checkpoint_restored" for event in events)):
            raise RuntimeError(f"Missing successful {phase} evidence for this configuration")
        if phase == "short" and (events[-1]["batches"] != 100 or not any(
                event["event"] == "resumed" for event in events)):
            raise RuntimeError("Short run must verify interruption and continuation")

    if args.phase in {"short", "formal"}:
        smoke = local_path(args.smoke_checkpoint)
        require_run_evidence(smoke.parent / "events.jsonl", "smoke")
        state = torch.load(smoke, weights_only=True, map_location="cpu")
        if state["signature"] != {**signature, "phase": "smoke"} or (state["cursor"], state["updates"]) != (1, 1):
            raise RuntimeError("Incorrect smoke checkpoint")
        del state
    if args.phase == "formal":
        require_run_evidence(args.short_log, "short")

    def encode(batch):
        examples = []
        for path, text, label in batch:
            with Image.open(path) as image:
                inputs = processor(text=[text], images=image.convert("RGB"), padding=True,
                                   truncation=True, max_length=77, return_tensors="pt")
            examples.append(({key: value.squeeze(0) for key, value in inputs.items()},
                             torch.tensor(label, dtype=torch.float32)))
        result = collate(examples)
        return {"input_ids": result["text_inputs"].to(device),
                "pixel_values": result["image_inputs"].to(device),
                "attention_mask": result["attention_mask"].to(device)}, result["labels"].to(device)

    def evaluate(split):
        model.eval()
        labels, probabilities = [], []
        with torch.no_grad():
            for index in range(0, len(rows[split]), args.microbatch):
                inputs, target = encode(rows[split][index:index + args.microbatch])
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    logits = model(**inputs)["logits"]
                if not torch.isfinite(logits).all():
                    raise RuntimeError("Nonfinite evaluation logits")
                labels.extend(target.tolist())
                probabilities.extend(logits.float().sigmoid().tolist())
        preds = [int(prob >= 0.5) for prob in probabilities]
        return {"split": split, "n": len(labels), "positive": sum(labels), "threshold": 0.5,
                "accuracy": accuracy_score(labels, preds),
                "macro_f1": f1_score(labels, preds, average="macro", zero_division=0),
                "auroc": roc_auc_score(labels, probabilities)}

    checkpoint = output / "last.pt"
    cursor = updates = 0
    best, best_epoch, patience = -1.0, 0, 0
    if args.resume:
        history = [json.loads(line) for line in event_file.read_text().splitlines()]
        if args.phase == "smoke" or any(event["event"] in {"completed", "final_metrics"} for event in history):
            raise ValueError("Resume requires an unfinished short or formal run")
        cursor, updates = restore(torch, checkpoint, model, optimizer, scaler, run_signature)
        metadata = torch.load(checkpoint, map_location="cpu", weights_only=True)["progress"]
        scheduler.load_state_dict(metadata["scheduler"])
        best, best_epoch, patience = metadata["best"], metadata["best_epoch"], metadata["patience"]
        log("resumed", batch=cursor, updates=updates)
    else:
        log("start", signature=run_signature, gpu=gpu.name, precision="bf16",
            effective_batch_cap=512, classification_weights=[1.0, 0.3, 0.7], **check_budget(torch))

    n_train = len(rows["train"])
    if n_train > 512:
        raise ValueError("Official protocol expects one author-sized logical train batch per epoch")
    batches_per_epoch = math.ceil(n_train / args.microbatch)
    limit = {"smoke": 1, "short": 100, "formal": MAX_EPOCHS * batches_per_epoch}[args.phase]
    order = None
    last_batch = cursor
    while last_batch < limit and (args.phase != "formal" or patience < 5):
        if time.monotonic() - started > 5.8 * 3600:
            raise TimeoutError("GPU budget exhausted")
        index = last_batch + 1
        epoch, block = divmod(index - 1, batches_per_epoch)
        if order is None or block == 0:
            order = rows["train"].copy()
            random.Random(SEED + epoch).shuffle(order)
        offset = block * args.microbatch
        batch = order[offset:offset + args.microbatch]
        model.train()
        step_start = time.monotonic()
        inputs, target = encode(batch)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            outputs = model(**inputs)
            loss = model.calculate_loss(outputs, target)
            with torch.no_grad():
                measured_components = {key: focal()(value, target).item() for key, value in outputs.items()}
        if not torch.isfinite(loss):
            raise RuntimeError("Nonfinite projection baseline loss")
        grouping_n = n_train if args.phase == "formal" else min(
            n_train, (limit - epoch * batches_per_epoch) * args.microbatch)
        (loss * (len(batch) / grouping_n)).backward()
        grad_norm = classifier_delta = effective = gradients = None
        if block == batches_per_epoch - 1 or index == limit:
            if args.phase == "smoke":
                gradients = {}
                for name in ("image_map", "text_map", "pre_output", "output", "output_image", "output_text"):
                    norms = [p.grad.detach().float().norm() for p in getattr(model, name).parameters()
                             if p.grad is not None]
                    gradients[name] = torch.stack(norms).norm().item() if norms else 0.0
            grad_norm = torch.nn.utils.clip_grad_norm_(trainable.values(), 1.0, error_if_nonfinite=True).item()
            previous = model.output.weight.detach().clone()
            optimizer.step()
            updates += 1
            classifier_delta = (model.output.weight.detach() - previous).abs().max().item()
            if classifier_delta <= 0 or grad_norm <= 0 or any(p.grad is not None for p in model.clip_model.parameters()):
                raise RuntimeError("Update, gradient or frozen-backbone check failed")
            optimizer.zero_grad(set_to_none=True)
            effective = grouping_n
        peak = check_budget(torch)
        log("batch", batch=index, epoch=epoch + 1, updates=updates, loss=loss.item(),
            loss_components=measured_components, grad_norm=grad_norm, gradients=gradients,
            classifier_delta=classifier_delta, effective_batch=effective,
            seconds=time.monotonic() - step_start, **peak)
        last_batch = index

        formal_epoch_end = args.phase == "formal" and block == batches_per_epoch - 1
        if formal_epoch_end:
            result = evaluate("dev")
            log("epoch_dev", epoch=epoch + 1, **result)
            scheduler.step(result["macro_f1"])
            if result["macro_f1"] > best:
                best, best_epoch, patience = result["macro_f1"], epoch + 1, 0
                save_checkpoint(torch, output / f"best-epoch-{best_epoch}.pt", {"trainable": trainable, "epoch": best_epoch})
            else:
                patience += 1

        if index % 25 == 0 or index == limit or args.stop_after == index or formal_epoch_end:
            save_checkpoint(torch, checkpoint, {
                "signature": run_signature, "cursor": index, "updates": updates,
                "trainable": trainable, "optimizer": optimizer.state_dict(),
                "pending_grads": {name: p.grad for name, p in trainable.items() if p.grad is not None},
                "scaler": scaler.state_dict(), "rng": rng_state(torch, device),
                "progress": {"scheduler": scheduler.state_dict(), "best": best,
                             "best_epoch": best_epoch, "patience": patience},
            })
            if restore(torch, checkpoint, model, optimizer, scaler, run_signature) != (index, updates):
                raise RuntimeError("Checkpoint readback cursor mismatch")
            log("checkpoint_restored", batch=index, updates=updates, **check_budget(torch))
        if args.stop_after == index:
            log("interrupted_at_checkpoint", batch=index, updates=updates)
            return
        if formal_epoch_end and patience >= 5:
            break

    if args.phase == "formal":
        state = torch.load(output / f"best-epoch-{best_epoch}.pt", map_location="cpu", weights_only=True)
        with torch.no_grad():
            for name, p in trainable.items():
                p.copy_(state["trainable"][name])
        for split in ("train", "dev", "test"):
            log("final_metrics", best_epoch=best_epoch, **evaluate(split))
    timing = {}
    for event in map(json.loads, event_file.read_text().splitlines()):
        if event["event"] == "resumed":
            timing = {i: value for i, value in timing.items() if i <= event["batch"]}
        elif event["event"] == "batch":
            timing[event["batch"]] = event["seconds"]
    if set(timing) != set(range(1, last_batch + 1)):
        raise RuntimeError("Timing log does not match final cursor")
    steps = sorted(timing.values())
    log("completed", batches=last_batch, updates=updates, best_epoch=best_epoch or None,
        p50_s=statistics.median(steps), p95_s=steps[math.ceil(len(steps) * 0.95) - 1],
        **check_budget(torch))


if __name__ == "__main__":
    main()
