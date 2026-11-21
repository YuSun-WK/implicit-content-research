"""Adapted two-caption TRACE MultiOFF training with fixed-threshold evaluation."""
import argparse
import ast
from collections import Counter
from contextlib import redirect_stdout
import hashlib
import io
import json
import math
import os
from pathlib import Path
import random
import statistics
import subprocess
import time

from stage2_caption import records
from multioff_baseline import LABELS
from run_stage0 import BUDGET, check_budget, local_path, restore, rng_state, save_checkpoint

UPSTREAM = "83ecb799f897fe275185e082ee9a669f7d04bfaa"
MODEL_NAME = "roberta-ViT-B-32"
REVISION = "e22e1c12b0a1ba4af9fb6474626585351ea0da25"
PROTOCOL = "TRACE-InternVL-only-MultiOFF-2caption"


def in_group(name, group):
    return name == group or name.startswith(group + ".")


def author_class(source_dir, torch):
    import torch.nn.functional as F
    source_dir = Path(source_dir)
    if subprocess.check_output(["git", "-C", str(source_dir), "rev-parse", "HEAD"], text=True).strip() != UPSTREAM:
        raise ValueError("Wrong upstream TRACE revision")
    file = source_dir / "MultiOFF/clip_roberta_multioff.py"
    tree = ast.parse(file.read_text(), filename=str(file))
    tree.body = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == "CLIPClassifier"]
    if len(tree.body) != 1:
        raise ValueError("Upstream classifier missing")
    namespace = {"nn": torch.nn, "torch": torch, "F": F}
    exec(compile(tree, str(file), "exec"), namespace)
    return namespace["CLIPClassifier"], hashlib.sha256(file.read_bytes()).hexdigest()


def focal_loss(logits, labels, torch):
    """Author FocalLoss algebra with view(-1), fixing B=1 shape collapse."""
    import torch.nn.functional as F
    logits = logits.reshape(-1).float()
    labels = labels.reshape(-1).float()
    bce = F.binary_cross_entropy_with_logits(logits, labels, reduction="none")
    prob = torch.sigmoid(logits)
    pt = torch.where(labels == 1, prob, 1 - prob)
    alpha = torch.where(labels == 1, 0.25, 0.75)
    return ((alpha * (1 - pt).square() * bce) * 0.9 + 0.1 * bce).mean()


def forward_components(model, images, tokens, labels, tau, training, torch):
    """Author MultiOFF formula with stable B=1/B=2 tensors and private outputs."""
    import torch.nn.functional as F
    batch, candidates, length = tokens.shape
    if candidates != 2:
        raise ValueError("Exactly original + InternVL captions required")
    image = model.clip_model.encode_image(images)
    text = model.clip_model.encode_text(tokens.reshape(batch * candidates, length)).reshape(batch, candidates, -1)
    scores = model.caption_scorer(text).reshape(batch, candidates)
    probabilities = torch.sigmoid(scores)
    mask = F.gumbel_softmax(probabilities, tau=tau, hard=True) if training else F.softmax(probabilities, dim=-1)
    chosen = torch.bmm(mask.unsqueeze(1), text).squeeze(1)
    logits = model.classifier(model.pre_output(model.combine_features(image, chosen))).reshape(-1)
    if not training:
        return logits, scores.detach(), mask.detach()
    cls = focal_loss(logits, labels, torch)
    # The author's contrastive branch re-encodes all captions and uses hard argmax.
    # Consequently its caption scorer receives no gradient from this loss.
    cont_image = model.clip_model.encode_image(images)
    cont_text = model.clip_model.encode_text(tokens.reshape(batch * candidates, length)).reshape(batch, candidates, -1)
    cont_scores = model.caption_scorer(cont_text).reshape(batch, candidates)
    best = cont_text[torch.arange(batch, device=tokens.device), cont_scores.argmax(1)]
    sim = F.normalize(cont_image, dim=-1) @ F.normalize(best, dim=-1).T / 0.07
    targets = torch.arange(batch, device=tokens.device)
    cont = (F.cross_entropy(sim, targets) + F.cross_entropy(sim.T, targets)) / 2
    rel = focal_loss(scores.mean(dim=1), labels, torch)
    total = cls + 0.3 * cont + 0.7 * rel
    return total, {"classification": cls, "contrastive": cont, "relevance": rel}, scores.detach(), mask.detach()


def load_rows(data_dir, caption_manifest):
    source = records(data_dir)
    state = json.loads(caption_manifest.read_text())
    rows = {split: [] for split in ("train", "dev", "test")}
    for row in source:
        caption = state.get(row["key"], {})
        if (caption.get("image_sha256") != row["image_sha256"] or
                caption.get("split") != row["split"] or caption.get("row_number") != row["row_number"]):
            raise ValueError("Caption identity mismatch")
        generated = caption.get("caption")
        if not isinstance(generated, str) or not generated.strip() or generated.strip() == row["sentence"].strip():
            raise ValueError("Missing, empty or copied InternVL caption")
        rows[row["split"]].append((data_dir / "Labelled Images" / row["image_name"],
                                   row["sentence"], generated, LABELS[row["label"]]))
    if {key: len(value) for key, value in rows.items()} != {"train": 444, "dev": 148, "test": 148}:
        raise ValueError("740/740 caption gate failed")
    return rows


def metrics(labels, scores):
    from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_score, recall_score, roc_auc_score
    predictions = [int(value >= 0.5) for value in scores]
    tn, fp, fn, tp = confusion_matrix(labels, predictions, labels=[0, 1]).ravel()
    return {"n": len(labels), "threshold": 0.5, "accuracy": accuracy_score(labels, predictions),
            "precision": precision_score(labels, predictions, zero_division=0),
            "recall": recall_score(labels, predictions, zero_division=0),
            "macro_f1": f1_score(labels, predictions, average="macro", zero_division=0),
            "offensive_f1": f1_score(labels, predictions, pos_label=1, zero_division=0),
            "auroc": roc_auc_score(labels, scores), "confusion": {"tn": int(tn), "fp": int(fp),
                                                             "fn": int(fn), "tp": int(tp)},
            "predicted_positive": sum(predictions)}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--caption-manifest", type=Path, required=True)
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--upstream-dir", type=Path, default=Path("/tmp/trace-s0-reference"))
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--phase", choices=("smoke", "short", "formal"), required=True)
    parser.add_argument("--microbatch", type=int, choices=(1, 2, 4, 8, 16, 32), default=2)
    parser.add_argument("--accumulation", type=int, default=1)
    parser.add_argument("--max-batches", type=int, default=100)
    parser.add_argument("--stop-after", type=int)
    parser.add_argument("--resume", action="store_true")
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()
    if args.accumulation < 1 or args.max_batches > 100 or args.max_batches < 1:
        parser.error("Invalid accumulation or short-run limit")
    output = local_path(args.output_dir)
    output.mkdir(parents=True, exist_ok=args.resume)
    rows = load_rows(args.data_dir, args.caption_manifest)
    caption_hash = hashlib.sha256(args.caption_manifest.read_bytes()).hexdigest()
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", CUBLAS_WORKSPACE_CONFIG=":4096:8")
    import open_clip
    from open_clip.tokenizer import HFTokenizer
    import torch
    from PIL import Image
    started = time.monotonic()
    if torch.cuda.device_count() != 1 or not torch.cuda.is_bf16_supported():
        raise RuntimeError("Expose exactly one BF16 CUDA device")
    gpu = torch.cuda.get_device_properties(0)
    if "RTX 4090" not in gpu.name:
        raise RuntimeError("Use a 4090/4090D")
    device = torch.device("cuda:0")
    torch.cuda.set_per_process_memory_fraction(min(1.0, BUDGET / gpu.total_memory))
    torch.cuda.reset_peak_memory_stats()
    torch.use_deterministic_algorithms(True)
    random.seed(args.seed)
    torch.manual_seed(args.seed)
    directory = args.assets_dir / "openclip_roberta" / REVISION
    weight = directory / "open_clip_pytorch_model.bin"
    manifest = json.loads((directory / "asset_manifest.json").read_text())
    if manifest.get("status") != "VERIFIED" or manifest["files"][weight.name]["sha256"] != hashlib.sha256(weight.read_bytes()).hexdigest():
        raise RuntimeError("OpenCLIP pretrained weight hash gate failed")
    backbone, _, preprocess = open_clip.create_model_and_transforms(
        MODEL_NAME, pretrained=str(weight), pretrained_hf=False, device="cpu")
    tokenizer = HFTokenizer(str(directory), context_length=77, local_files_only=True)
    classifier, source_hash = author_class(args.upstream_dir, torch)
    with redirect_stdout(io.StringIO()):
        model = classifier(backbone).to(device)
    trainable = {name: value for name, value in model.named_parameters() if value.requires_grad}
    if not trainable or any(name.startswith("clip_model.visual.") for name in trainable):
        raise RuntimeError("Text unfreeze or visual freeze gate failed")
    optimizer = torch.optim.AdamW(trainable.values(), lr=1e-4, weight_decay=0.01)
    scheduler = torch.optim.lr_scheduler.ReduceLROnPlateau(optimizer, mode="max", factor=0.1, patience=2)
    scaler = torch.amp.GradScaler("cuda", enabled=False)
    signature = {"protocol": PROTOCOL, "phase": args.phase, "source_sha256": source_hash,
                 "backbone_sha256": manifest["files"][weight.name]["sha256"],
                 "caption_manifest_sha256": caption_hash, "seed": args.seed,
                 "microbatch": args.microbatch, "accumulation": args.accumulation}
    events = output / "events.jsonl"

    def log(event, **detail):
        with events.open("a") as stream:
            stream.write(json.dumps({"event": event, "elapsed_s": time.monotonic() - started,
                                     "phase": args.phase, **detail}, allow_nan=False) + "\n")

    def encode(items):
        images, texts, labels = [], [], []
        for path, original, generated, label in items:
            with Image.open(path) as opened:
                images.append(preprocess(opened.convert("RGB")))
            texts.extend((original, generated))
            labels.append(label)
        token = tokenizer(texts).reshape(len(items), 2, -1)
        return torch.stack(images).to(device), token.to(device), torch.tensor(labels, device=device, dtype=torch.float32)

    def evaluate(split):
        model.eval()
        labels, probabilities = [], []
        chosen = Counter()
        with torch.inference_mode():
            for offset in range(0, len(rows[split]), args.microbatch):
                image, token, target = encode(rows[split][offset:offset + args.microbatch])
                with torch.autocast("cuda", dtype=torch.bfloat16):
                    logits, scores, _ = forward_components(model, image, token, target, 0.1, False, torch)
                probabilities.extend(logits.float().sigmoid().cpu().tolist())
                labels.extend(target.int().cpu().tolist())
                chosen.update(scores.argmax(1).cpu().tolist())
        return {"split": split, **metrics(labels, probabilities),
                "caption_selected": {"original": chosen[0], "internvl": chosen[1]}}

    checkpoint = output / "last.pt"
    cursor = updates = 0
    best = -1.0
    best_epoch = patience = 0
    if args.resume:
        cursor, updates = restore(torch, checkpoint, model, optimizer, scaler, signature)
        progress = torch.load(checkpoint, weights_only=True, map_location="cpu")["progress"]
        scheduler.load_state_dict(progress["scheduler"])
        best, best_epoch, patience = progress["best"], progress["best_epoch"], progress["patience"]
        log("resumed", cursor=cursor, updates=updates)
    else:
        log("start", signature=signature, gpu=gpu.name, torch=str(torch.__version__),
            open_clip=open_clip.__version__, trainable_parameters=sum(p.numel() for p in trainable.values()),
            total_parameters=sum(p.numel() for p in model.parameters()),
            trainable_groups={group: sum(p.numel() for name, p in trainable.items() if in_group(name, group))
                              for group in ("clip_model.text", "caption_scorer", "image_projection",
                                            "text_projection", "cross_attn", "cross_attn_reverse",
                                            "pre_output", "classifier")}, **check_budget(torch))

    per_epoch = math.ceil(444 / args.microbatch)
    limit = 1 if args.phase == "smoke" else args.max_batches if args.phase == "short" else 20 * per_epoch
    timings = []
    accum = args.accumulation
    while cursor < limit and (args.phase != "formal" or patience < 5):
        if time.monotonic() - started > 5.8 * 3600:
            raise TimeoutError("Single GPU job budget reached")
        epoch, block = divmod(cursor, per_epoch)
        order = rows["train"].copy()
        random.Random(args.seed + epoch).shuffle(order)
        items = order[block * args.microbatch:(block + 1) * args.microbatch]
        model.train()
        before = time.monotonic()
        image, token, target = encode(items)
        tau = max(1.0 - (epoch / 20) * 0.9, 0.1)
        with torch.autocast("cuda", dtype=torch.bfloat16):
            loss, components, scores, selected = forward_components(model, image, token, target, tau, True, torch)
        if not torch.isfinite(loss):
            raise RuntimeError("Nonfinite three-loss training objective")
        group_size = min(accum, per_epoch - (block // accum) * accum)
        (loss / group_size).backward()
        group_end = (block + 1) % accum == 0 or block + 1 == per_epoch or cursor + 1 == limit
        gradients = delta = norm = None
        if group_end:
            gradients = {}
            for name in ("caption_scorer", "clip_model.text", "image_projection", "text_projection",
                         "cross_attn", "cross_attn_reverse", "pre_output", "classifier"):
                vectors = [p.grad.float().norm() for key, p in trainable.items()
                           if in_group(key, name) and p.grad is not None]
                gradients[name] = torch.stack(vectors).norm().item() if vectors else 0.0
            if any(p.grad is not None for p in model.clip_model.visual.parameters()):
                raise RuntimeError("Frozen image tower received gradients")
            norm = torch.nn.utils.clip_grad_norm_(trainable.values(), 2.0, error_if_nonfinite=True).item()
            before_weight = model.classifier.weight.detach().clone()
            optimizer.step()
            updates += 1
            delta = (model.classifier.weight.detach() - before_weight).abs().max().item()
            if delta <= 0:
                raise RuntimeError("Classifier did not update")
            optimizer.zero_grad(set_to_none=True)
        torch.cuda.synchronize()
        elapsed = time.monotonic() - before
        timings.append(elapsed)
        cursor += 1
        log("batch", cursor=cursor, epoch=epoch + 1, updates=updates, seconds=elapsed,
            loss=float(loss), components={k: float(v) for k, v in components.items()},
            selected_original=int((selected.argmax(1) == 0).sum()),
            selected_internvl=int((selected.argmax(1) == 1).sum()),
            grad_norm=norm, gradients=gradients, classifier_delta=delta, **check_budget(torch))
        epoch_end = cursor % per_epoch == 0
        if args.phase == "formal" and epoch_end:
            result = evaluate("dev")
            log("epoch_dev", epoch=epoch + 1, **result)
            scheduler.step(result["macro_f1"])
            if result["macro_f1"] > best:
                best, best_epoch, patience = result["macro_f1"], epoch + 1, 0
                save_checkpoint(torch, output / "best.pt", {"trainable": trainable, "epoch": best_epoch})
            else:
                patience += 1
        if cursor % 25 == 0 or cursor == limit or epoch_end or cursor == args.stop_after:
            save_checkpoint(torch, checkpoint, {"signature": signature, "cursor": cursor,
                            "updates": updates, "trainable": trainable,
                            "pending_grads": {name: p.grad for name, p in trainable.items() if p.grad is not None},
                            "optimizer": optimizer.state_dict(), "scaler": scaler.state_dict(),
                            "rng": rng_state(torch, device), "progress": {"scheduler": scheduler.state_dict(),
                                                                               "best": best, "best_epoch": best_epoch,
                                                                               "patience": patience}})
            if restore(torch, checkpoint, model, optimizer, scaler, signature) != (cursor, updates):
                raise RuntimeError("Checkpoint readback mismatch")
            log("checkpoint_restored", cursor=cursor, updates=updates, **check_budget(torch))
        if args.stop_after == cursor:
            log("interrupted", cursor=cursor)
            return
    if args.phase == "formal":
        state = torch.load(output / "best.pt", weights_only=True, map_location="cpu")
        with torch.no_grad():
            for name, parameter in trainable.items():
                parameter.copy_(state["trainable"][name])
        for split in ("train", "dev", "test"):
            log("final_metrics", best_epoch=best_epoch, **evaluate(split))
    timings.sort()
    log("completed", batches=cursor, updates=updates, best_epoch=best_epoch or None,
        p50_s=statistics.median(timings), p95_s=timings[math.ceil(len(timings) * 0.95) - 1],
        **check_budget(torch))


if __name__ == "__main__":
    main()
