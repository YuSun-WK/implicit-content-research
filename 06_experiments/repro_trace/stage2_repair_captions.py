"""Repair only overlength private MultiOFF captions with pinned InternVL."""
import argparse
from collections import Counter
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import statistics
import time

from stage2_caption import grounding_prompt, parse_caption, records, save_state
from stage2_train import REVISION

INTERNVL_REVISION = "e9e4c0dc1db56bfab10458671519b7fa3dd29463"
PROMPT = """<image>
RAM++ visual tags: {tags}
{grounding}
Original meme text (context only): {sentence}
Earlier InternVL image caption to revise: {old_caption}
Rewrite the earlier caption as ONE concise, visually grounded sentence of at most {words} English words. Preserve the main visible entities, actions, relationships, and essential interaction with the meme text. Remove repetition, vague judgments and decorative details. Do not invent identity, attributes, intent or facts unsupported by the image and provided text. Do not output a classification label. Do not simply copy the meme text.
Format exactly: Caption: [one sentence]
"""
PROMPT_TEMPLATE_SHA256 = hashlib.sha256(PROMPT.encode()).hexdigest()
FORBIDDEN_LABEL = re.compile(r"\b(?:non[- ]?offensive|offensive|non[- ]?hateful|hateful)\b", re.I)


def sha(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()


def token_count(tokenizer, caption):
    return len(tokenizer.encode(caption, add_special_tokens=True))


def validate_original(source, old, tokenizer):
    keys = {row["key"] for row in source}
    if set(old) != keys or len(source) != 740:
        raise ValueError("Old manifest must match all 740 official complete-case rows")
    overlong = []
    for row in source:
        item = old[row["key"]]
        for field in ("split", "row_number", "image_name", "image_sha256"):
            if item.get(field) != row[field]:
                raise ValueError("Old caption identity mismatch: " + row["key"])
        caption = item.get("caption")
        if not isinstance(caption, str) or not caption.strip():
            raise ValueError("Empty old caption: " + row["key"])
        if token_count(tokenizer, caption) > 77:
            overlong.append(row["key"])
    if len(overlong) != 334:
        raise ValueError(f"Expected 334 overlength captions; found {len(overlong)}")
    return set(overlong)


def validate_repaired(source, old, new, audit, tokenizer, overlong, complete=True):
    if set(new) != set(old):
        raise ValueError("Repaired manifest keys differ from original")
    counts = Counter()
    before, after = [], []
    by_split = {split: {"before": [], "after": []} for split in ("train", "dev", "test")}
    failed = []
    failed_details = []
    originally_valid_label_keywords = 0
    for row in source:
        key = row["key"]
        previous, current = old[key], new[key]
        for field in ("split", "row_number", "image_name", "image_sha256"):
            if current.get(field) != row[field]:
                raise ValueError("Repaired caption identity mismatch: " + key)
        old_caption, new_caption = previous["caption"], current.get("caption")
        if not isinstance(new_caption, str) or not new_caption.strip():
            raise ValueError("Empty repaired caption: " + key)
        old_length, new_length = token_count(tokenizer, old_caption), token_count(tokenizer, new_caption)
        before.append(old_length)
        after.append(new_length)
        by_split[row["split"]]["before"].append(old_length)
        by_split[row["split"]]["after"].append(new_length)
        counts[row["split"]] += 1
        if key not in overlong and new_caption != old_caption:
            raise ValueError("Originally valid caption changed: " + key)
        if key not in overlong and FORBIDDEN_LABEL.search(old_caption):
            originally_valid_label_keywords += 1
        if new_caption.strip().casefold() == row["sentence"].strip().casefold():
            raise ValueError("Caption copies original meme text: " + key)
        if key in overlong:
            record = audit.get(key)
            if new_length <= 77 and new_caption != old_caption:
                if not record or record.get("old_sha256") != sha(old_caption) or record.get("new_sha256") != sha(new_caption) or record.get("new_tokens") != new_length or record.get("image_sha256") != row["image_sha256"]:
                    raise ValueError("Missing or mismatched repair provenance: " + key)
            else:
                failed.append(key)
                attempts = (record or {}).get("attempt_records", [])
                failed_details.append({"key": key, "split": row["split"], "old_tokens": old_length,
                                       "attempts": len(attempts),
                                       "attempt_token_counts": [item.get("tokens") for item in attempts],
                                       "failure_reasons": [item.get("error") for item in attempts]})
    if counts != {"train": 444, "dev": 148, "test": 148}:
        raise ValueError("Repaired split counts changed")
    if complete and failed:
        raise ValueError(f"Unrepaired captions: {len(failed)}; keys: {','.join(failed)}")
    return {"sample_count": len(source), "split_counts": dict(counts),
            "original_over_77": len(overlong), "unchanged_originally_valid": len(source) - len(overlong),
            "repaired": len(overlong) - len(failed), "remaining_over_77": len(failed),
            "failed_keys": failed, "failed_details": failed_details,
            "originally_valid_label_keyword_count": originally_valid_label_keywords,
            "before_tokens": distribution(before), "after_tokens": distribution(after),
            "by_split": {split: {side: distribution(values) for side, values in sides.items()}
                         for split, sides in by_split.items()},
            "attempts": dict(Counter(audit[key]["attempts"] for key in overlong if key in audit and "new_sha256" in audit[key]))}


def distribution(values):
    ordered = sorted(values)
    return {"n": len(values), "median": statistics.median(values),
            "p95": ordered[(len(values) * 95 + 99) // 100 - 1], "max": ordered[-1],
            "over_77": sum(value > 77 for value in values)}


def run(args):
    from open_clip.tokenizer import HFTokenizer
    tokenizer_dir = args.assets_dir / "openclip_roberta" / REVISION
    tokenizer = HFTokenizer(str(tokenizer_dir), context_length=77, local_files_only=True).tokenizer
    source = records(args.data_dir)
    old_bytes = args.old_manifest.read_bytes()
    old_hash = hashlib.sha256(old_bytes).hexdigest()
    old = json.loads(old_bytes)
    overlong = validate_original(source, old, tokenizer)
    args.output_dir.mkdir(parents=True, exist_ok=True)
    new_path, audit_path, origin_path = (args.output_dir / name for name in ("records.json", "repair_audit.json", "origin.json"))
    if origin_path.exists():
        if json.loads(origin_path.read_text())["old_manifest_sha256"] != old_hash:
            raise ValueError("Old manifest changed since repair began")
    else:
        if new_path.exists() or audit_path.exists():
            raise ValueError("Existing repair directory lacks origin record")
        save_state(origin_path, {"old_manifest_sha256": old_hash, "prompt_template_sha256": PROMPT_TEMPLATE_SHA256,
                                 "internvl_revision": INTERNVL_REVISION, "openclip_revision": REVISION})
    new = json.loads(new_path.read_text()) if new_path.exists() else copy.deepcopy(old)
    audit = json.loads(audit_path.read_text()) if audit_path.exists() else {}
    validate_repaired(source, old, new, audit, tokenizer, overlong, complete=False)
    save_state(new_path, new)
    pending = [row for row in source if row["key"] in overlong and row["key"] not in audit]
    if args.limit:
        pending = pending[:args.limit]
    if pending:
        import torch
        import torchvision.transforms as transforms
        from PIL import Image
        from transformers import AutoModel, AutoTokenizer
        if torch.cuda.device_count() != 1 or not torch.cuda.is_bf16_supported():
            raise RuntimeError("Exactly one BF16-capable GPU required")
        gpu = torch.cuda.get_device_properties(0)
        if "RTX 4090" not in gpu.name:
            raise RuntimeError("RTX 4090/4090D required")
        torch.cuda.set_per_process_memory_fraction(min(1.0, 18 * 1024**3 / gpu.total_memory))
        directory = args.assets_dir / "internvl" / INTERNVL_REVISION
        vl_tokenizer = AutoTokenizer.from_pretrained(directory, trust_remote_code=True, use_fast=False, local_files_only=True)
        model = AutoModel.from_pretrained(directory, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True,
                                          trust_remote_code=True, local_files_only=True).eval().to("cuda:0")
        if not hasattr(model.language_model, "generate"):
            from transformers.generation import GenerationConfig, GenerationMixin
            original = type(model.language_model)
            model.language_model.__class__ = type("InternLM2GenerationCompat", (original, GenerationMixin), {})
            if model.language_model.generation_config is None:
                model.language_model.generation_config = GenerationConfig.from_model_config(model.language_model.config)
        transform = transforms.Compose([transforms.Resize((448, 448)), transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
        start = time.monotonic()
        for index, row in enumerate(pending, 1):
            key = row["key"]
            previous = old[key]
            with Image.open(args.data_dir / "Labelled Images" / row["image_name"]) as opened:
                pixels = transform(opened.convert("RGB")).unsqueeze(0).to("cuda:0", dtype=torch.bfloat16)
            attempts = []
            accepted = None
            for number, words in enumerate((45, 35, 25), 1):
                prompt = PROMPT.format(tags=previous.get("tags", ""),
                                       grounding=grounding_prompt(previous.get("grounding", {})),
                                       sentence=row["sentence"], old_caption=previous["caption"], words=words)
                item = {"attempt": number, "prompt_sha256": sha(prompt), "target_words": words}
                try:
                    with torch.inference_mode():
                        response = model.chat(vl_tokenizer, pixels, prompt,
                                              {"max_new_tokens": 128, "do_sample": False,
                                               "pad_token_id": vl_tokenizer.pad_token_id})
                    candidate = parse_caption(response)
                    item["tokens"] = token_count(tokenizer, candidate)
                    if FORBIDDEN_LABEL.search(candidate):
                        raise ValueError("Output contains classification label")
                    if candidate.strip().casefold() == row["sentence"].strip().casefold():
                        raise ValueError("Output copies original meme text")
                    if item["tokens"] > 77:
                        raise ValueError("OpenCLIP caption exceeds 77 tokens")
                    accepted = candidate
                    attempts.append(item)
                    break
                except Exception as error:
                    item["error"] = type(error).__name__ + ": " + str(error)[:90]
                    attempts.append(item)
            if accepted is not None:
                new[key]["caption"] = accepted
                audit[key] = {"old_sha256": sha(previous["caption"]), "new_sha256": sha(accepted),
                              "old_tokens": token_count(tokenizer, previous["caption"]),
                              "new_tokens": token_count(tokenizer, accepted), "attempts": len(attempts),
                              "attempt_records": attempts, "image_sha256": row["image_sha256"],
                              "model_revision": INTERNVL_REVISION}
            else:
                audit[key] = {"old_sha256": sha(previous["caption"]), "old_tokens": token_count(tokenizer, previous["caption"]),
                              "attempts": len(attempts), "attempt_records": attempts,
                              "image_sha256": row["image_sha256"], "model_revision": INTERNVL_REVISION, "failed": True}
            if index % 25 == 0 or accepted is None:
                save_state(new_path, new)
                save_state(audit_path, audit)
                print(json.dumps({"processed": index, "pending_total": len(pending),
                                  "failed": sum(v.get("failed", False) for v in audit.values()),
                                  "elapsed_s": time.monotonic() - start,
                                  "peak_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3}), flush=True)
        save_state(new_path, new)
        save_state(audit_path, audit)
        print(json.dumps({"processed": len(pending), "elapsed_s": time.monotonic() - start,
                          "peak_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
                          "peak_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3}), flush=True)
    summary = validate_repaired(source, old, new, audit, tokenizer, overlong, complete=False)
    summary.update({"dataset": "MultiOFF", "protocol": "TRACE-InternVL-only-MultiOFF-2caption (Adapted Reproduction)",
                    "old_manifest_sha256": old_hash, "new_manifest_sha256": hashlib.sha256(new_path.read_bytes()).hexdigest(),
                    "openclip_revision": REVISION, "internvl_revision": INTERNVL_REVISION,
                    "prompt_template_sha256": PROMPT_TEMPLATE_SHA256})
    if args.audit_output:
        args.audit_output.write_text(json.dumps(summary, indent=2, allow_nan=False) + "\n")
    print(json.dumps({k: summary[k] for k in ("repaired", "remaining_over_77", "attempts", "new_manifest_sha256")}), flush=True)
    if not args.limit and summary["remaining_over_77"]:
        raise RuntimeError(f"Caption repair gate blocked: {summary['remaining_over_77']} unresolved; keys: {','.join(summary['failed_keys'])}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--old-manifest", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--audit-output", type=Path)
    parser.add_argument("--limit", type=int)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
