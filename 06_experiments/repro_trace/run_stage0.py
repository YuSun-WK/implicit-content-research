"""Offline, bounded wrapper around the pinned FHM TRACE ViT-L/14 implementation."""
import argparse
import ast
from contextlib import redirect_stdout
import hashlib
import io
from itertools import islice
import json
import os
from pathlib import Path
import random
import subprocess
import sys
import time
from types import FunctionType, SimpleNamespace

import yaml

from data_manifest import FIELDS, identity, image_path, read_rows, summary

BASE = Path(__file__).resolve().parent
LOCAL = BASE / ".local"
BUDGET = 18 * 1024 ** 3
LOSS_CONFIG = {"classification": True, "relevance": True, "contrastive": False}
GROUPS = ("caption_scorer", "clip_model.text_model.encoder.layers.4",
          "clip_model.text_model.encoder.layers.7", "clip_model.text_model.encoder.layers.10",
          "image_projection", "text_projection", "cross_attn", "cross_attn_reverse",
          "pre_output", "classifier", "log_vars")


class DataBlocked(Exception):
    pass


def digest(path):
    sha = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            sha.update(chunk)
    return sha.hexdigest()


def assert_inputs(cfg):
    if cfg["authorization_confirmed"] is not True or cfg["caption_provenance_confirmed"] is not True:
        raise DataBlocked("FHM authorization and both original caption provenances must be confirmed")
    if not cfg["data_path"] or not cfg["image_root"] or not Path(cfg["data_path"]).is_file():
        raise DataBlocked("Local combined FHM JSON/JSONL and image root required")
    rows = read_rows(cfg["data_path"])
    report = summary(rows, cfg["image_root"])
    if report["unknown_split_rows"]:
        raise DataBlocked("Unknown split names in FHM input")
    for split in (cfg["train_split"], cfg["dev_split"]):
        stats = report["splits"][split]
        if (not stats["label_scoring_available"] or stats["images_missing_or_outside_root"]
                or stats["duplicate_id_rows_beyond_first"] or stats["duplicate_image_ref_rows_beyond_first"]
                or any(stats["captions"][field]["present"] != stats["rows"] for field in FIELDS)):
            raise DataBlocked(f"Incomplete FHM rows, captions, labels or images in {split}")
    if not cfg["model_dir"] or not Path(cfg["model_dir"]).is_dir():
        raise DataBlocked("Local Hugging Face ViT-L/14 snapshot required")
    model_dir = Path(cfg["model_dir"]).resolve()
    if not (model_dir / "model.safetensors").is_file():
        raise DataBlocked("The local ViT-L/14 snapshot must contain model.safetensors")
    train = [row for row in rows if row["split"] == cfg["train_split"]]
    dev = [row for row in rows if row["split"] == cfg["dev_split"]]
    train_ids = {key for row in train if (key := identity(row)) is not None}
    dev_ids = {key for row in dev if (key := identity(row)) is not None}
    root = Path(cfg["image_root"]).resolve()
    train_images = {image_path(root, row["img"]) for row in train}
    dev_images = {image_path(root, row["img"]) for row in dev}
    if train_ids & dev_ids or train_images & dev_images:
        raise DataBlocked("Repeated ID or image path across train and the selected dev split")
    return rows, model_dir


def local_path(path):
    path = Path(path).resolve()
    if not path.is_relative_to(LOCAL):
        raise ValueError("Logs and checkpoints must live under the ignored .local directory")
    return path


def check_config(cfg):
    if cfg["mode"] not in {"dry-run", "smoke", "short"}:
        raise ValueError("Unknown mode")
    if cfg["train_split"] != "train" or cfg["dev_split"] not in {"dev_seen", "dev_unseen"}:
        raise ValueError("Use train and one named FHM dev split")
    if cfg["threshold"] not in {"fixed_0.5", "dev_f1"}:
        raise ValueError("Unknown dev threshold policy")
    if cfg["microbatch"] not in (1, 2, 4, 8) or cfg["precision"] not in {"fp32", "bf16", "fp16"}:
        raise ValueError("Unsupported microbatch or precision")
    for key, limit in (("accumulation_steps", 100), ("max_batches", 100), ("checkpoint_every", 25)):
        if type(cfg[key]) is not int or not 1 <= cfg[key] <= limit:
            raise ValueError(f"{key} must be within 1..{limit}")
    if cfg["mode"] == "smoke" and (cfg["accumulation_steps"] != 1 or cfg["resume"]):
        raise ValueError("Smoke requires one update with accumulation_steps=1 and a fresh run")
    if cfg["mode"] == "short" and not cfg["smoke_checkpoint"]:
        raise ValueError("Short mode requires a verified one-batch smoke checkpoint")


def upstream(cfg, torch, model_factory):
    root = Path(cfg["upstream_dir"]).resolve()
    manifest = json.loads((BASE / "upstream_manifest.json").read_text())
    head = subprocess.check_output(["git", "-C", root, "rev-parse", "HEAD"], text=True).strip()
    if head != manifest["commit"]:
        raise ValueError("Incorrect upstream commit")
    for path, sha in manifest["files"].items():
        if digest(root / path) != sha:
            raise ValueError(f"Upstream file hash mismatch for {path}")
    sys.path.insert(0, str(root))
    from utils import loss_functions

    # Compile only the unchanged author declarations. Importing the script normally
    # would load a remote processor at module scope and require W&B.
    model_source = root / "clip_vitL_14_ft.py"
    declarations = ast.parse(model_source.read_text(), filename=str(model_source))
    declarations.body = [node for node in declarations.body if getattr(node, "name", None)
                         in {"CLIPClassifier", "collate_fn"}]
    ns = {"torch": torch, "nn": torch.nn, "CLIPModel": SimpleNamespace(from_pretrained=model_factory)}
    exec(compile(declarations, str(model_source), "exec"), ns)
    return ns["CLIPClassifier"], ns["collate_fn"], loss_functions, head


def parameter_manifest(model):
    params = {name: {"shape": list(p.shape), "elements": p.numel(), "trainable": p.requires_grad}
              for name, p in model.named_parameters()}
    return {
        "total": sum(p["elements"] for p in params.values()),
        "trainable": sum(p["elements"] for p in params.values() if p["trainable"]),
        "groups": {group: sum(p["elements"] for name, p in params.items()
                             if p["trainable"] and (name == group or name.startswith(group + ".")))
                   for group in GROUPS},
        "parameters": params,
    }


def author_loss(losses, model, batch, device, is_training):
    """Preserve author focal math, adapting scalar singleton labels and capturing components."""
    original = losses.FocalLoss
    components = []

    class MeasuredFocal(original):
        def forward(self, inputs, targets):
            if inputs.shape == (1,) and targets.ndim == 0:
                targets = targets.reshape(1)
            value = super().forward(inputs, targets)
            components.append(value.detach())
            return value

    author = losses.calculate_loss_gs
    globals_for_call = {**author.__globals__, "FocalLoss": MeasuredFocal}
    measured = FunctionType(author.__code__, globals_for_call, author.__name__, author.__defaults__)
    globals_for_call[author.__name__] = measured
    measured.call_count = 1
    with redirect_stdout(io.StringIO()):
        result = measured(model, batch, device, LOSS_CONFIG, temp=1.0,
                          print_every=1000, is_training=is_training)
    if is_training and len(components) != 2:
        raise RuntimeError("Expected author classification and relevance focal losses")
    return result, components


def data_batches(rows, image_root, processor, collate, torch, size, start=0, limit=None):
    from PIL import Image
    root = Path(image_root).resolve()
    stop = None if limit is None else start + limit
    batches = range(0, len(rows), size)
    for offset in islice(batches, start, stop):
        items = []
        for row in rows[offset:offset + size]:
            with Image.open(image_path(root, row["img"])) as image:
                pixels = processor(images=image.convert("RGB"), return_tensors="pt", padding=True)
            tokens = [processor(text=row[field], padding="max_length", truncation=True,
                                max_length=77, return_tensors="pt") for field in FIELDS]
            items.append({
                "pixel_values": pixels.pixel_values[0],
                "input_ids": [x.input_ids[0] for x in tokens],
                "attention_mask": [x.attention_mask[0] for x in tokens],
                "labels": torch.tensor(row["label"], dtype=torch.float32),
                "image_ids": row["img"],
                "num_captions": len(tokens),
            })
        yield collate(items)


def threshold_for(policy, labels, probs):
    if policy == "fixed_0.5":
        return 0.5
    from sklearn.metrics import precision_recall_curve
    if len(set(labels)) != 2:
        raise ValueError("Dev calibration requires both binary classes")
    precisions, recalls, thresholds = precision_recall_curve(labels, probs)
    return float(max(zip(precisions, recalls, thresholds),
                     key=lambda triplet: (2 * triplet[0] * triplet[1] /
                                         max(triplet[0] + triplet[1], 1e-12), triplet[2]))[2])


def evaluate_dev(cfg, model, losses, batches, torch, device, amp, started):
    from sklearn.metrics import accuracy_score, f1_score
    probs, labels = [], []
    model.eval()
    with torch.no_grad():
        for batch in batches:
            if time.monotonic() - started >= 5.8 * 3600:
                raise TimeoutError("Stage 0 wall-clock budget exhausted during dev calibration")
            with amp():
                logits, _ = author_loss(losses, model, batch, device, False)
            probs.extend(logits.float().sigmoid().tolist())
            labels.extend(batch["labels"].tolist())
            check_budget(torch)
    threshold = threshold_for(cfg["threshold"], labels, probs)
    preds = [int(prob >= threshold) for prob in probs]
    return {"split": cfg["dev_split"], "rows": len(labels), "threshold": threshold,
            "threshold_policy": cfg["threshold"], "accuracy": accuracy_score(labels, preds),
            "macro_f1": f1_score(labels, preds, average="macro", zero_division=0)}


def check_budget(torch):
    torch.cuda.synchronize()
    used = torch.cuda.max_memory_allocated()
    reserved = torch.cuda.max_memory_reserved()
    if max(used, reserved) >= BUDGET:
        raise RuntimeError(f"CUDA budget reached: allocated={used} reserved={reserved}")
    return {"allocated_bytes": used, "reserved_bytes": reserved}


def grad_report(model, torch):
    grad = {}
    for group in GROUPS:
        norms = [p.grad.detach().float().norm() for name, p in model.named_parameters()
                 if p.grad is not None and (name == group or name.startswith(group + "."))]
        grad[group] = torch.stack(norms).norm().item() if norms else 0.0
    grad["frozen_grad_count"] = sum(p.grad is not None for p in model.parameters() if not p.requires_grad)
    return grad


def rng_state(torch):
    return {"python": random.getstate(), "cpu": torch.get_rng_state(), "cuda": torch.cuda.get_rng_state()}


def save_checkpoint(torch, path, state):
    temp = path.with_suffix(".tmp")
    with temp.open("wb") as stream:
        torch.save(state, stream)
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(temp, path)


def restore(torch, path, model, optimizer, scaler, signature):
    state = torch.load(path, map_location="cpu", weights_only=True)
    if state["signature"] != signature:
        raise ValueError("Checkpoint run signature mismatch")
    trainable = {name: p for name, p in model.named_parameters() if p.requires_grad}
    if trainable.keys() != state["trainable"].keys():
        raise ValueError("Checkpoint trainable parameter names mismatch")
    with torch.no_grad():
        for name, param in trainable.items():
            param.copy_(state["trainable"][name])
            param.grad = state["pending_grads"][name].to(param) if name in state["pending_grads"] else None
    optimizer.load_state_dict(state["optimizer"])
    scaler.load_state_dict(state["scaler"])
    random.setstate(state["rng"]["python"])
    torch.set_rng_state(state["rng"]["cpu"])
    torch.cuda.set_rng_state(state["rng"]["cuda"])
    return state["cursor"], state["updates"]


def train(cfg, model, processor, collate, losses, rows, signature, output, torch, started):
    import math

    device = torch.device("cuda:0")
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=1e-4)
    scaler = torch.amp.GradScaler("cuda", enabled=cfg["precision"] == "fp16")
    dtype = {"fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[cfg["precision"]]
    def amp():
        return torch.autocast("cuda", dtype=dtype, enabled=cfg["precision"] != "fp32")

    def record(event, **fields):
        with (output / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"event": event, "elapsed_s": time.monotonic() - started, **fields},
                                    allow_nan=False) + "\n")

    training = [row for row in rows if row["split"] == cfg["train_split"]]
    random.Random(cfg["seed"]).shuffle(training)
    limit = 1 if cfg["mode"] == "smoke" else cfg["max_batches"]
    if len(training) < limit * cfg["microbatch"]:
        raise DataBlocked("Insufficient distinct training rows for the requested batch cap")
    cursor, updates = 0, 0
    if cfg["resume"]:
        cursor, updates = restore(torch, local_path(cfg["resume"]), model, optimizer, scaler, signature)
        if not 0 < cursor < limit:
            raise ValueError("Resume requires a cursor before the unchanged batch cap")
        record("resumed", batch=cursor, updates=updates)
    model.train()
    batches = data_batches(training, cfg["image_root"], processor, collate, torch, cfg["microbatch"],
                           start=cursor, limit=limit - cursor)
    trainable = {name: p for name, p in model.named_parameters() if p.requires_grad}
    accum = cfg["accumulation_steps"]
    checkpoint = output / "last.pt"
    for index in range(cursor + 1, limit + 1):
        step_start = time.monotonic()
        if step_start - started >= 5.8 * 3600:
            raise TimeoutError("Stage 0 wall-clock budget exhausted")
        batch = next(batches)
        group_start = ((index - 1) // accum) * accum
        divisor = min(accum, limit - group_start)
        with amp():
            loss, components = author_loss(losses, model, batch, device, True)
        if not torch.isfinite(loss):
            raise RuntimeError("Nonfinite loss")
        check_budget(torch)
        scaler.scale(loss / divisor).backward()
        check_budget(torch)
        gradients = None
        changed = None
        if index % accum == 0 or index == limit:
            scaler.unscale_(optimizer)
            gradients = grad_report(model, torch)
            if not all(math.isfinite(x) for x in gradients.values()) or gradients["frozen_grad_count"]:
                raise RuntimeError("Nonfinite gradients or gradients on frozen parameters")
            if cfg["mode"] == "smoke" and any(gradients[group] <= 0 for group in GROUPS):
                raise RuntimeError(f"Missing or zero smoke gradient: {gradients}")
            torch.nn.utils.clip_grad_norm_(trainable.values(), 1.0, error_if_nonfinite=True)
            before = trainable["classifier.weight"].detach().clone()
            scaler.step(optimizer)
            scaler.update()
            changed = bool(torch.ne(before, trainable["classifier.weight"]).any().item())
            if not changed:
                raise RuntimeError("Classifier did not change after optimizer.step")
            updates += 1
            optimizer.zero_grad(set_to_none=True)
        peak = check_budget(torch)
        record("train_batch", batch=index, updates=updates, loss=loss.item(),
               loss_cls=components[0].item(), loss_rel=components[1].item(),
               loss_cont=None, log_vars=model.log_vars.detach().tolist(), gradients=gradients,
               classifier_changed=changed, step_s=time.monotonic() - step_start, **peak)
        if index % cfg["checkpoint_every"] == 0 or index == limit:
            save_checkpoint(torch, checkpoint, {
                "signature": signature, "cursor": index, "updates": updates,
                "trainable": {name: param.detach() for name, param in trainable.items()},
                "pending_grads": {name: param.grad for name, param in trainable.items() if param.grad is not None},
                "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(), "rng": rng_state(torch),
            })
            if restore(torch, checkpoint, model, optimizer, scaler, signature) != (index, updates):
                raise RuntimeError("Checkpoint restore returned an incorrect cursor")
            record("checkpoint_restored", batch=index, updates=updates, **check_budget(torch))
    if cfg["mode"] == "short" and (cfg["evaluate_dev"] or cfg["threshold"] == "dev_f1"):
        dev = [row for row in rows if row["split"] == cfg["dev_split"]]
        batches = data_batches(dev, cfg["image_root"], processor, collate, torch, cfg["microbatch"])
        record("dev_calibration", **evaluate_dev(cfg, model, losses, batches, torch, device, amp, started))
    record("completed", mode=cfg["mode"], batches=limit, updates=updates, **check_budget(torch))


def write_parameters(output, model):
    (output / "parameters.json").write_text(json.dumps(parameter_manifest(model), indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=BASE / "repro_config.yaml")
    args = parser.parse_args()
    started = time.monotonic()
    cfg = yaml.safe_load(args.config.read_text())
    check_config(cfg)
    if cfg["mode"] != "dry-run":
        rows, model_dir = assert_inputs(cfg)

    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", WANDB_MODE="disabled")
    import torch
    from transformers import (
        CLIPConfig, CLIPImageProcessor, CLIPModel, CLIPProcessor, CLIPTokenizerFast, __version__
    )

    output = local_path(cfg["output_dir"])
    backbone = json.loads((BASE / "upstream_manifest.json").read_text())["backbone"]
    if cfg["mode"] == "dry-run":
        def model_factory(_):
            if digest(cfg["model_config"]) != backbone["files"]["config.json"]:
                raise ValueError("Dry-run requires the pinned public CLIP config")
            return CLIPModel(CLIPConfig.from_json_file(cfg["model_config"]))
    else:
        if torch.cuda.device_count() != 1:
            raise RuntimeError("Expose exactly one GPU via CUDA_VISIBLE_DEVICES")
        props = torch.cuda.get_device_properties(0)
        if "RTX 4090" not in props.name:
            raise RuntimeError("Stage 0 requires a single RTX 4090 or 4090D")
        if cfg["precision"] == "bf16" and not torch.cuda.is_bf16_supported():
            raise RuntimeError("BF16 unsupported")
        torch.cuda.set_per_process_memory_fraction(min(1.0, BUDGET / props.total_memory))
        torch.cuda.reset_peak_memory_stats()
        model_factory = lambda _: CLIPModel.from_pretrained(model_dir, local_files_only=True,
                                                            use_safetensors=True, attn_implementation="eager")
    random.seed(cfg["seed"])
    torch.manual_seed(cfg["seed"])
    classifier, collate, losses, head = upstream(cfg, torch, model_factory)
    output.mkdir(parents=True, exist_ok=True)

    if cfg["mode"] != "dry-run":
        signature = {
            "upstream": head, "dataset_sha256": digest(cfg["data_path"]),
            "backbone_files": {name: digest(model_dir / name) for name in backbone["files"]
                               if (model_dir / name).is_file()},
            "gpu": props.name, "torch": str(torch.__version__), "transformers": __version__,
            "microbatch": cfg["microbatch"], "precision": cfg["precision"], "seed": cfg["seed"],
            "accumulation": cfg["accumulation_steps"], "max_batches": 1 if cfg["mode"] == "smoke" else cfg["max_batches"],
            "dev_split": cfg["dev_split"], "threshold_policy": cfg["threshold"],
            "image_root": str(Path(cfg["image_root"]).resolve()),
        }
        for name, sha in backbone["files"].items():
            if signature["backbone_files"].get(name) != sha:
                raise ValueError(f"Local ViT-L/14 snapshot hash mismatch for {name}")
        if cfg["mode"] == "short":
            smoke = local_path(cfg["smoke_checkpoint"])
            expected = {**signature, "accumulation": 1, "max_batches": 1}
            state = torch.load(smoke, weights_only=True, map_location="cpu")
            if state["signature"] != expected or (state["cursor"], state["updates"]) != (1, 1):
                raise RuntimeError("Smoke checkpoint does not match this run")
            del state
            evidence = [json.loads(line) for line in (smoke.parent / "events.jsonl").read_text().splitlines()]
            if (not evidence or evidence[-1].get("mode") != "smoke"
                    or evidence[-1].get("event") != "completed"
                    or not any(row.get("event") == "checkpoint_restored" for row in evidence)
                    or max(evidence[-1]["allocated_bytes"], evidence[-1]["reserved_bytes"]) >= BUDGET):
                raise RuntimeError("Successful smoke and restore log is required")
        if not cfg["resume"] and any((output / name).exists() for name in ("events.jsonl", "last.pt")):
            raise ValueError("Use an empty run directory for a fresh run")

    if cfg["mode"] == "dry-run":
        with torch.device("meta"), redirect_stdout(io.StringIO()):
            model = classifier()
        write_parameters(output, model)
        print("PARAMETER_MANIFEST_WRITTEN")
        return
    try:
        with redirect_stdout(io.StringIO()):
            model = classifier().cuda()
        write_parameters(output, model)
        processor = CLIPProcessor(
            image_processor=CLIPImageProcessor.from_pretrained(model_dir, local_files_only=True),
            tokenizer=CLIPTokenizerFast.from_pretrained(model_dir, local_files_only=True),
        )
        train(cfg, model, processor, collate, losses, rows, signature, output, torch, started)
    except (RuntimeError, TimeoutError) as exc:
        with (output / "events.jsonl").open("a") as stream:
            stream.write(json.dumps({"event": "failed", "error_type": type(exc).__name__,
                                     "oom": isinstance(exc, torch.cuda.OutOfMemoryError),
                                     "allocated_bytes": torch.cuda.max_memory_allocated(),
                                     "reserved_bytes": torch.cuda.max_memory_reserved(),
                                     "elapsed_s": time.monotonic() - started}) + "\n")
        raise


if __name__ == "__main__":
    try:
        main()
    except DataBlocked as exc:
        print(f"DATA_BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(3)
