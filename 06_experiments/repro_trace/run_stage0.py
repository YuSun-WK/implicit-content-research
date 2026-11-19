"""Offline, bounded wrapper around the pinned FHM TRACE ViT-L/14 implementation."""
import argparse
import ast
from contextlib import redirect_stdout
import hashlib
import math
import io
from itertools import islice
import json
import os
from pathlib import Path
import random
import statistics
import subprocess
import sys
import time
from types import FunctionType, SimpleNamespace

import yaml

from data_manifest import FIELDS, SPLITS, identity, image_path, read_rows, summary
from prepare_clip import WeightsBlocked, backbone_spec, digest, inspect_files, load_clip, require_verified

BASE = Path(__file__).resolve().parent
LOCAL = BASE / ".local"
BUDGET = 18 * 1024 ** 3
ORIGINAL = "trace_original"
DIAGNOSTIC = "trace_text_only_diagnostic"
LOSS_CONFIG = {"classification": True, "relevance": True, "contrastive": False}
MODES = {
    ORIGINAL: (FIELDS, LOSS_CONFIG),
    DIAGNOSTIC: (("text",), {**LOSS_CONFIG, "relevance": False}),
}
GROUPS = ("caption_scorer", "clip_model.text_model.encoder.layers.4",
          "clip_model.text_model.encoder.layers.7", "clip_model.text_model.encoder.layers.10",
          "image_projection", "text_projection", "cross_attn", "cross_attn_reverse",
          "pre_output", "classifier", "log_vars")


class DataBlocked(Exception):
    pass


class ManualDataAction(DataBlocked):
    pass


class AuthorCaptionsBlocked(DataBlocked):
    pass


def assert_inputs(cfg):
    if cfg["authorization_confirmed"] is not True:
        raise ManualDataAction("Authorized FHM access and provenance must be confirmed")
    experiment = cfg.get("experiment_mode", ORIGINAL)
    fields, _ = MODES[experiment]
    combined = cfg.get("data_path")
    split_files = cfg.get("split_files") or {}
    if not cfg.get("image_root") or bool(combined) == bool(split_files):
        raise ManualDataAction("Provide an image root and either combined data or split-specific JSONL files")
    try:
        rows = (read_rows(combined) if combined else [
            row for split, path in split_files.items() for row in read_rows(path, split)
        ])
    except (OSError, TypeError, ValueError) as exc:
        raise ManualDataAction(f"FHM input could not be read or normalized ({type(exc).__name__})") from None

    train_split, dev_split = cfg["train_split"], cfg["dev_split"]
    report = summary(rows, cfg["image_root"], verify_splits=(train_split, dev_split))
    if report["unknown_split_rows"]:
        raise ManualDataAction("Unknown split names in FHM input")
    for split in (train_split, dev_split):
        stats = report["splits"][split]
        if (not stats["label_scoring_available"] or stats["images_missing_or_outside_root"]
                or stats["images_unreadable"] or stats["id_missing"] or stats["numeric_id_image_mismatch"]
                or stats["duplicate_id_rows_beyond_first"] or stats["duplicate_resolved_image_rows_beyond_first"]
                or stats["captions"]["text"]["present"] != stats["rows"]):
            raise ManualDataAction(f"Incomplete FHM IDs, images, labels or text in {split}")
    train = [row for row in rows if row["split"] == train_split]
    dev = [row for row in rows if row["split"] == dev_split]
    root = Path(cfg["image_root"]).resolve()
    holdout = [row for row in rows if row["split"] != train_split]
    if ({identity(row) for row in train} & {identity(row) for row in holdout}
            or {image_path(root, row["img"]) for row in train}
            & {image_path(root, row.get("img")) for row in holdout}):
        raise ManualDataAction("Repeated ID or image path across train and a supplied held-out split")

    if experiment == ORIGINAL:
        for split in (train_split, dev_split):
            stats = report["splits"][split]
            if any(stats["captions"][field]["present"] != stats["rows"] for field in fields[1:]):
                raise AuthorCaptionsBlocked(f"Missing or invalid author captions in {split}")
        if cfg.get("caption_provenance_confirmed") is not True:
            raise AuthorCaptionsBlocked("Both original author caption provenances must be confirmed")
    if not cfg.get("model_dir") or not Path(cfg["model_dir"]).is_dir():
        raise WeightsBlocked("Local Hugging Face ViT-L/14 snapshot required")
    return train + dev, Path(cfg["model_dir"]).resolve()


def dataset_digest(rows, fields):
    keys = ("id", "img", "label", "split", *fields)
    serialized = json.dumps([{key: row[key] for key in keys} for row in rows], ensure_ascii=True)
    return hashlib.sha256(serialized.encode()).hexdigest()


def local_path(path):
    path = Path(path).resolve()
    if not path.is_relative_to(LOCAL):
        raise ValueError("Logs and checkpoints must live under the ignored .local directory")
    return path


def check_config(cfg):
    if cfg.get("experiment_mode", ORIGINAL) not in MODES:
        raise ValueError("Unknown experiment_mode")
    if cfg.get("split_files") is not None and (
        not isinstance(cfg["split_files"], dict) or any(split not in SPLITS for split in cfg["split_files"])
    ):
        raise ValueError("split_files must map named FHM splits to local files")
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


def author_loss(losses, model, batch, device, is_training, experiment=ORIGINAL):
    """Preserve author focal math, adapting scalar singleton labels and capturing components."""
    fields, loss_config = MODES[experiment]
    if batch["input_ids"].shape[1] != len(fields):
        raise ValueError("Candidate count does not match experiment mode")
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
        result = measured(model, batch, device, loss_config, temp=1.0,
                          print_every=1000, is_training=is_training)
    if is_training and len(components) != 1 + loss_config["relevance"]:
        raise RuntimeError("Author focal loss components do not match the experiment mode")
    return result, components


def data_batches(rows, image_root, processor, collate, torch, size, start=0, limit=None, *, fields=FIELDS):
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
                                max_length=77, return_tensors="pt") for field in fields]
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
                logits, _ = author_loss(losses, model, batch, device, False, cfg.get("experiment_mode", ORIGINAL))
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
    free, total = torch.cuda.mem_get_info()
    return {"allocated_bytes": used, "reserved_bytes": reserved,
            "device_free_bytes": free, "device_total_bytes": total}


def grad_report(model, torch):
    grad = {}
    for group in GROUPS:
        norms = [p.grad.detach().float().norm() for name, p in model.named_parameters()
                 if p.grad is not None and (name == group or name.startswith(group + "."))]
        grad[group] = torch.stack(norms).norm().item() if norms else 0.0
    grad["frozen_grad_count"] = sum(p.grad is not None for p in model.parameters() if not p.requires_grad)
    return grad


def rng_state(torch, device):
    return {"python": random.getstate(), "cpu": torch.get_rng_state(),
            "cuda": torch.cuda.get_rng_state(device) if device.type == "cuda" else None}


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
    if state["rng"]["cuda"] is not None:
        torch.cuda.set_rng_state(state["rng"]["cuda"], next(model.parameters()).device)
    return state["cursor"], state["updates"]


def train(cfg, model, processor, collate, losses, rows, signature, output, torch, started):
    experiment = cfg.get("experiment_mode", ORIGINAL)
    fields, _ = MODES[experiment]
    required_groups = GROUPS if experiment == ORIGINAL else tuple(
        group for group in GROUPS if group != "caption_scorer")
    device = torch.device("cuda:0")
    optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=1e-4)
    scaler = torch.amp.GradScaler("cuda", enabled=cfg["precision"] == "fp16")
    dtype = {"fp16": torch.float16, "bf16": torch.bfloat16, "fp32": torch.float32}[cfg["precision"]]
    def amp():
        return torch.autocast("cuda", dtype=dtype, enabled=cfg["precision"] != "fp32")

    def record(event, **details):
        with (output / "events.jsonl").open("a", encoding="utf-8") as stream:
            stream.write(json.dumps({"event": event, "experiment_mode": experiment,
                                     "elapsed_s": time.monotonic() - started, **details},
                                    allow_nan=False) + "\n")

    training = [row for row in rows if row["split"] == cfg["train_split"]]
    random.Random(cfg["seed"]).shuffle(training)
    limit = 1 if cfg["mode"] == "smoke" else cfg["max_batches"]
    if len(training) < limit * cfg["microbatch"]:
        raise DataBlocked("Insufficient distinct training rows for the requested batch cap")
    record("start", phase=cfg["mode"], microbatch=cfg["microbatch"], precision=cfg["precision"],
           accumulation_steps=cfg["accumulation_steps"], candidates=list(fields),
           caption_source="original_text" if experiment == DIAGNOSTIC else "original_text_and_author_captions",
           **check_budget(torch))
    cursor, updates = 0, 0
    if cfg["resume"]:
        resume_path = local_path(cfg["resume"])
        cursor, updates = restore(torch, resume_path, model, optimizer, scaler, signature)
        if not 0 < cursor < limit:
            raise ValueError("Resume requires a cursor before the unchanged batch cap")
        record("resumed", batch=cursor, updates=updates)
    model.train()
    batches = data_batches(training, cfg["image_root"], processor, collate, torch, cfg["microbatch"],
                           start=cursor, limit=limit - cursor, fields=fields)
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
            loss, components = author_loss(losses, model, batch, device, True, experiment)
        if not all(torch.isfinite(value).item() for value in [loss, *components]):
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
            if cfg["mode"] == "smoke" and any(gradients[group] <= 0 for group in required_groups):
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
               loss_cls=components[0].item(), loss_rel=components[1].item() if len(components) == 2 else None,
               effective_batch_size=cfg["microbatch"] * divisor if changed else None,
               loss_cont=None, log_vars=model.log_vars.detach().tolist(), gradients=gradients,
               classifier_changed=changed, step_s=time.monotonic() - step_start, **peak)
        if index % cfg["checkpoint_every"] == 0 or index == limit:
            save_checkpoint(torch, checkpoint, {
                "signature": signature, "cursor": index, "updates": updates,
                "trainable": {name: param.detach() for name, param in trainable.items()},
                "pending_grads": {name: param.grad for name, param in trainable.items() if param.grad is not None},
                "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(), "rng": rng_state(torch, device),
            })
            if restore(torch, checkpoint, model, optimizer, scaler, signature) != (index, updates):
                raise RuntimeError("Checkpoint restore returned an incorrect cursor")
            record("checkpoint_restored", batch=index, updates=updates, **check_budget(torch))
    if cfg["mode"] == "short" and (cfg["evaluate_dev"] or cfg["threshold"] == "dev_f1"):
        dev = [row for row in rows if row["split"] == cfg["dev_split"]]
        batches = data_batches(dev, cfg["image_root"], processor, collate, torch, cfg["microbatch"], fields=fields)
        record("dev_calibration", **evaluate_dev(cfg, model, losses, batches, torch, device, amp, started))
    timing = {}
    for line in (output / "events.jsonl").read_text().splitlines():
        event = json.loads(line)
        if event["event"] == "resumed":
            timing = {i: value for i, value in timing.items() if i <= event["batch"]}
        if event["event"] == "train_batch":
            timing[event["batch"]] = event["step_s"]
    if set(timing) != set(range(1, limit + 1)):
        raise RuntimeError("Batch timing log does not match the completed training cursor")
    ordered = sorted(timing.values())
    record("completed", mode=cfg["mode"], batches=limit, updates=updates,
           step_p50_s=statistics.median(ordered), step_p95_s=ordered[math.ceil(len(ordered) * 0.95) - 1],
           **check_budget(torch))


def write_parameters(output, model):
    (output / "parameters.json").write_text(json.dumps(parameter_manifest(model), indent=2) + "\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--config", type=Path, default=BASE / "repro_config.yaml")
    args = parser.parse_args()
    started = time.monotonic()
    cfg = yaml.safe_load(args.config.read_text())
    check_config(cfg)
    experiment = cfg.get("experiment_mode", ORIGINAL)
    backbone = backbone_spec()
    if cfg["mode"] != "dry-run":
        rows, model_dir = assert_inputs(cfg)
        backbone_files = require_verified(inspect_files(model_dir, backbone))

    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", WANDB_MODE="disabled")
    import torch
    from transformers import (
        CLIPConfig, CLIPImageProcessor, CLIPModel, CLIPProcessor, CLIPTokenizerFast, __version__
    )

    output = local_path(cfg["output_dir"])
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
        model_factory = lambda _: load_clip(model_dir)[0]
    random.seed(cfg["seed"])
    torch.manual_seed(cfg["seed"])
    classifier, collate, losses, head = upstream(cfg, torch, model_factory)
    output.mkdir(parents=True, exist_ok=True)

    if cfg["mode"] != "dry-run":
        signature = {
            "upstream": head, "dataset_sha256": dataset_digest(rows, MODES[experiment][0]),
            "backbone_files": backbone_files, "backbone_revision": backbone["reference_revision"],
            "experiment_mode": experiment, "candidate_fields": list(MODES[experiment][0]),
            "loss_config": MODES[experiment][1],
            "gpu": props.name, "torch": str(torch.__version__), "transformers": __version__,
            "microbatch": cfg["microbatch"], "precision": cfg["precision"], "seed": cfg["seed"],
            "accumulation": cfg["accumulation_steps"], "max_batches": 1 if cfg["mode"] == "smoke" else cfg["max_batches"],
            "dev_split": cfg["dev_split"], "threshold_policy": cfg["threshold"],
            "image_root": str(Path(cfg["image_root"]).resolve()),
        }
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
                    or evidence[-1].get("experiment_mode") != experiment
                    or not any(row.get("event") == "checkpoint_restored" for row in evidence)
                    or max(evidence[-1]["allocated_bytes"], evidence[-1]["reserved_bytes"]) >= BUDGET):
                raise RuntimeError("Successful smoke and restore log is required")
        if cfg["resume"] and (
            local_path(cfg["resume"]) != output / "last.pt" or not (output / "events.jsonl").is_file()
        ):
            raise ValueError("Resume from the same run directory's last.pt and events.jsonl")
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
            stream.write(json.dumps({"event": "failed", "experiment_mode": experiment,
                                     "error_type": type(exc).__name__,
                                     "oom": isinstance(exc, torch.cuda.OutOfMemoryError),
                                     "allocated_bytes": torch.cuda.max_memory_allocated(),
                                     "reserved_bytes": torch.cuda.max_memory_reserved(),
                                     "elapsed_s": time.monotonic() - started}) + "\n")
        raise


if __name__ == "__main__":
    try:
        main()
    except ManualDataAction as exc:
        print(f"MANUAL_DATA_ACTION_REQUIRED: {exc}", file=sys.stderr)
        raise SystemExit(3)
    except AuthorCaptionsBlocked as exc:
        print(f"AUTHOR_CAPTIONS_BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(3)
    except WeightsBlocked as exc:
        print(f"WEIGHTS_BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(4)
    except DataBlocked as exc:
        print(f"DATA_BLOCKED: {exc}", file=sys.stderr)
        raise SystemExit(3)
