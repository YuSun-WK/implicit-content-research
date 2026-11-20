"""Exercise the pinned TRACE compute path with private generated inputs on one CUDA device."""
import argparse
from contextlib import redirect_stdout
import io
import json
import math
import os
from pathlib import Path
import random
import time

from prepare_clip import backbone_spec, inspect_files, load_clip, require_verified
from run_stage0 import (
    BUDGET, DIAGNOSTIC, GROUPS, MODES, ORIGINAL, author_loss, check_budget,
    grad_report, local_path, restore, rng_state, save_checkpoint, upstream,
)

MARKER = "SYNTHETIC_COMPUTE_ONLY_NOT_DATASET_RESULT"


def snapshot(value, torch):
    if isinstance(value, torch.Tensor):
        return value.detach().to("cpu", copy=True)
    if isinstance(value, dict):
        return {key: snapshot(item, torch) for key, item in value.items()}
    if isinstance(value, (tuple, list)):
        return type(value)(snapshot(item, torch) for item in value)
    return value


def verify_equal(actual, expected, torch):
    if isinstance(expected, torch.Tensor):
        torch.testing.assert_close(actual.detach().cpu(), expected, rtol=0, atol=0)
    elif isinstance(expected, dict):
        assert actual.keys() == expected.keys()
        for key in expected:
            verify_equal(actual[key], expected[key], torch)
    elif isinstance(expected, (tuple, list)):
        assert len(actual) == len(expected)
        for left, right in zip(actual, expected):
            verify_equal(left, right, torch)
    else:
        assert actual == expected


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model-dir", required=True, type=Path)
    parser.add_argument("--upstream-dir", default="/tmp/trace-s0-reference")
    parser.add_argument("--output-dir", required=True, type=Path)
    parser.add_argument("--mode", choices=tuple(MODES), default=DIAGNOSTIC)
    parser.add_argument("--microbatch", choices=(1, 2), type=int, default=1)
    args = parser.parse_args()
    output = local_path(args.output_dir)
    output.mkdir(parents=True, exist_ok=False)

    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1", CUBLAS_WORKSPACE_CONFIG=":4096:8")
    import torch
    from transformers import CLIPTokenizerFast, __version__

    def log(event, **details):
        with (output / "events.jsonl").open("a") as stream:
            stream.write(json.dumps({"scope": MARKER, "mode": args.mode,
                                     "microbatch": args.microbatch, "event": event, **details},
                                    allow_nan=False) + "\n")

    updates = 0
    try:
        if torch.cuda.device_count() != 1 or not torch.cuda.is_bf16_supported():
            raise RuntimeError("Expose exactly one BF16 CUDA device")
        props = torch.cuda.get_device_properties(0)
        if "RTX 4090" not in props.name:
            raise RuntimeError("Use an RTX 4090 or 4090D")
        device = torch.device("cuda:0")
        torch.cuda.set_per_process_memory_fraction(min(1.0, BUDGET / props.total_memory))
        torch.cuda.reset_peak_memory_stats()
        torch.use_deterministic_algorithms(True)
        torch.backends.cudnn.benchmark = False
        random.seed(121)
        torch.manual_seed(121)
        backbone = backbone_spec()
        hashes = require_verified(inspect_files(args.model_dir, backbone))
        classify, collate, losses, commit = upstream({"upstream_dir": args.upstream_dir}, torch,
                                                      lambda _: load_clip(args.model_dir)[0])
        with redirect_stdout(io.StringIO()):
            model = classify().to(device).train()
        optimizer = torch.optim.AdamW((p for p in model.parameters() if p.requires_grad), lr=1e-4)
        scaler = torch.amp.GradScaler("cuda", enabled=False)
        trainable = {name: p for name, p in model.named_parameters() if p.requires_grad}
        tokenizer = CLIPTokenizerFast.from_pretrained(args.model_dir, local_files_only=True)
        phrases = ("A blue square.", "A small geometric shape.", "A colored figure on a canvas.")
        count = len(MODES[args.mode][0])
        tokens = tokenizer(list(phrases[:count]), padding="max_length", truncation=True,
                           max_length=77, return_tensors="pt")
        generator = torch.Generator().manual_seed(413)
        batches = []
        for index in range(2):
            pixels = torch.rand(args.microbatch, 3, 224, 224, generator=generator)
            torch.save(pixels, output / f"synthetic-{index}.pt")
            batches.append(collate([
                {"pixel_values": pixels[row], "input_ids": list(tokens.input_ids),
                 "attention_mask": list(tokens.attention_mask), "labels": torch.tensor(float((row + index) % 2)),
                 "image_ids": "synthetic", "num_captions": count}
                for row in range(args.microbatch)
            ]))
        signature = {"scope": MARKER, "mode": args.mode, "microbatch": args.microbatch,
                     "revision": backbone["reference_revision"], "upstream": commit}
        log("start", revision=signature["revision"], upstream=commit, seed=121, gpu=props.name, torch=str(torch.__version__),
            transformers=__version__, precision="bf16", deterministic=True,
            backbone_files_verified=len(hashes), total_parameters=sum(p.numel() for p in model.parameters()),
            trainable_parameters=sum(p.numel() for p in trainable.values()), **check_budget(torch))

        def step(batch, phase):
            nonlocal updates
            torch.cuda.synchronize()
            started = time.perf_counter()
            with torch.autocast("cuda", dtype=torch.bfloat16):
                loss, components = author_loss(losses, model, batch, device, True, args.mode)
            if not all(torch.isfinite(value).item() for value in [loss, *components]):
                raise RuntimeError("Nonfinite loss")
            scaler.scale(loss).backward()
            scaler.unscale_(optimizer)
            gradients = grad_report(model, torch)
            if (not all(math.isfinite(value) for value in gradients.values())
                    or gradients["frozen_grad_count"]):
                raise RuntimeError("Nonfinite or frozen gradients")
            required = GROUPS if args.mode == ORIGINAL else set(GROUPS) - {"caption_scorer"}
            if any(gradients[name] <= 0 for name in required):
                log("gradient_gate_failed", phase=phase, gradients=gradients)
                raise RuntimeError("Required gradient was zero")
            torch.nn.utils.clip_grad_norm_(trainable.values(), 1.0, error_if_nonfinite=True)
            before = model.classifier.weight.detach().clone()
            scaler.step(optimizer)
            updates += 1
            scaler.update()
            change = (model.classifier.weight.detach() - before).abs().max().item()
            optimizer.zero_grad(set_to_none=True)
            peak = check_budget(torch)
            log("step", phase=phase, update=updates, seconds=time.perf_counter() - started,
                loss=loss.item(), components=[value.item() for value in components],
                classifier_max_abs_change=change, gradients=gradients, **peak)
            if change <= 0:
                raise RuntimeError("Classifier weight did not change")
            return loss.item()

        def state():
            return {"trainable": trainable, "optimizer": optimizer.state_dict(),
                    "scaler": scaler.state_dict(), "rng": rng_state(torch, device)}

        step(batches[0], "initial")
        checkpoint = output / "last.pt"
        save_checkpoint(torch, checkpoint, {**state(), "signature": signature,
                         "pending_grads": {}, "cursor": 1, "updates": updates})
        loss_reference = step(batches[1], "continuation_reference")
        reference = snapshot(state(), torch)
        if restore(torch, checkpoint, model, optimizer, scaler, signature) != (1, 1):
            raise RuntimeError("Incorrect checkpoint cursor")
        saved = torch.load(checkpoint, map_location="cpu", weights_only=True)
        verify_equal(state(), {key: saved[key] for key in state()}, torch)
        del saved
        log("checkpoint_restored", exact_weights_optimizer_scaler_cpu_cuda_rng=True, **check_budget(torch))
        replay_loss = step(batches[1], "continuation_replay")
        verify_equal(state(), reference, torch)
        if loss_reference != replay_loss:
            raise RuntimeError("Replay loss differed")
        log("completed", optimizer_steps=updates, bitwise_replay=True, **check_budget(torch))
    except Exception as exc:
        log("failed", optimizer_steps=updates, error_type=type(exc).__name__, error=str(exc))
        raise


if __name__ == "__main__":
    main()
