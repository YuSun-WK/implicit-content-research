"""Private, resumable RAM++ -> GroundingDINO -> InternVL2.5-8B caption pipeline."""
import argparse
from collections import Counter
import csv
import hashlib
import json
import os
from pathlib import Path
import statistics
import sys
import time
import traceback

from PIL import Image

from multioff_baseline import SPLITS, digest

SOURCE = "83ecb799f897fe275185e082ee9a669f7d04bfaa"
PROMPT_TEMPLATE = """<image>
{grounding}
Meme text (provided): {sentence}
Task: Analyze this meme image and generate a **single caption** (under 77 tokens) suitable for CLIP fine-tuning.
The caption should:
- **Describe the main visual elements** (people, objects, and setting)
- **Mention key identifying features** (race, gender, nationality, disability, etc.) if relevant
- **Summarize the text overlay** (if short) or **explain its meaning** concisely
- **Describe any implied humor, stereotypes, sarcasm, or exaggerated statements**
- **Identify if the meme references a specific group or topic that may be controversial**
- **Avoid subjective labels like 'offensive' or 'non-offensive'**
Additionally, **if the meme conveys strong emotions (mockery, sarcasm, contempt, etc.), describe how the text and image interact to create this impression.**
Format the response as:
Caption: [Generated caption here]
"""
PROMPT_SHA256 = hashlib.sha256(PROMPT_TEMPLATE.encode()).hexdigest()


def records(root):
    images = (root / "Labelled Images").resolve()
    output = []
    for split, prefix in SPLITS.items():
        with (root / "Split Dataset" / f"{prefix}_meme_dataset.csv").open(encoding="utf-8-sig", newline="") as stream:
            reader = csv.DictReader(stream)
            if reader.fieldnames != ["image_name", "sentence", "label"]:
                raise ValueError("Unexpected MultiOFF columns")
            for row_number, row in enumerate(reader):
                name = row["image_name"]
                if not name or Path(name).name != name:
                    raise ValueError("Invalid image name")
                path = (images / name).resolve()
                if not path.is_relative_to(images) or not path.is_file():
                    continue  # Predeclared complete-case policy: one missing image per split.
                with Image.open(path) as image:
                    image.verify()
                image_sha = digest(path)
                key = hashlib.sha256(f"{split}\0{row_number}\0{name}\0{image_sha}".encode()).hexdigest()
                output.append({"key": key, "split": split, "row_number": row_number,
                               "image_name": name, "image_sha256": image_sha,
                               "sentence": row["sentence"], "label": row["label"]})
    counts = Counter(item["split"] for item in output)
    if counts != {"train": 444, "dev": 148, "test": 148} or len({item["key"] for item in output}) != 740:
        raise ValueError(f"Unexpected complete-case MultiOFF counts: {dict(counts)}")
    return output


def load_state(path):
    return json.loads(path.read_text()) if path.exists() else {}


def save_state(path, state):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(".tmp")
    temporary.write_text(json.dumps(state, ensure_ascii=False, separators=(",", ":")) + "\n")
    os.replace(temporary, path)


def grounding_prompt(grounding):
    prefix = "Key elements in the image:"
    if not grounding:
        return prefix + " No specific object information available."
    for obj, boxes in grounding.items():
        confidence = max(box[4] for box in boxes)
        certainty = "high certainty" if confidence > 0.7 else "moderate certainty" if confidence > 0.5 else "low certainty"
        prefix += f" {obj} (detected with {certainty}, count: {len(boxes)}),"
    return prefix.rstrip(",") + "."


def parse_caption(response):
    if "Caption:" not in response:
        raise ValueError("InternVL response lacks Caption marker")
    caption = response.split("Caption:", 1)[1].strip()
    if not caption or caption.casefold() in {"no caption", "[generated caption here]"}:
        raise ValueError("Empty or placeholder InternVL caption")
    return caption


def run(args):
    import torch
    import torchvision.transforms as transforms

    source = records(args.data_dir)
    selected = source[:args.limit] if args.limit else source
    private = args.output_dir / "records.json"
    state = load_state(private)
    for row in source:
        saved = state.get(row["key"])
        if saved and (saved["image_sha256"] != row["image_sha256"] or saved["split"] != row["split"] or saved["row_number"] != row["row_number"]):
            raise ValueError("Existing caption manifest identity mismatch")
    device = torch.device("cuda:0")
    if torch.cuda.device_count() != 1 or not torch.cuda.is_bf16_supported():
        raise RuntimeError("Expose exactly one BF16-capable GPU for Stage 2 inference")
    properties = torch.cuda.get_device_properties(0)
    if "RTX 4090" not in properties.name:
        raise RuntimeError("Use a single RTX 4090 or 4090D")
    torch.cuda.set_per_process_memory_fraction(min(1.0, 18 * 1024**3 / properties.total_memory))
    torch.cuda.reset_peak_memory_stats()
    model_dir = args.assets_dir
    if args.stage == "tags":
        sys.path.insert(0, str(args.ram_source))
        # RAM's pinned bert.py imports helpers from a pre-4.57 Transformers path.
        import transformers.modeling_utils as modeling_utils
        import transformers.pytorch_utils as pytorch_utils
        for name in ("apply_chunking_to_forward", "find_pruneable_heads_and_indices", "prune_linear_layer"):
            if not hasattr(modeling_utils, name):
                setattr(modeling_utils, name, getattr(pytorch_utils, name))
        from ram.models import ram_plus
        from ram import inference_ram, get_transform
        weights = model_dir / "ram_plus" / "84d4aee3a0265c4e0df1f714f0572011d1bf2ec3" / "ram_plus_swin_large_14m.pth"
        bert = model_dir / "bert_tokenizer" / "86b5e0934494bd15c9632b12f734a8a67f723594"
        model = ram_plus(pretrained=str(weights), image_size=384, vit="swin_l",
                         text_encoder_type=str(bert)).eval().to(device)
        transform = get_transform(image_size=384)
    elif args.stage == "grounding":
        from transformers import AutoProcessor, AutoModelForZeroShotObjectDetection
        directory = model_dir / "grounding_dino" / "12bdfa3120f3e7ec7b434d90674b3396eccf88eb"
        processor = AutoProcessor.from_pretrained(directory, local_files_only=True)
        model = AutoModelForZeroShotObjectDetection.from_pretrained(directory, local_files_only=True).eval().to(device)
    else:
        from transformers import AutoModel, AutoTokenizer
        directory = model_dir / "internvl" / "e9e4c0dc1db56bfab10458671519b7fa3dd29463"
        tokenizer = AutoTokenizer.from_pretrained(directory, trust_remote_code=True, use_fast=False, local_files_only=True)
        model = AutoModel.from_pretrained(directory, torch_dtype=torch.bfloat16, low_cpu_mem_usage=True,
                                          trust_remote_code=True, local_files_only=True).eval().to(device)
        if not hasattr(model.language_model, "generate"):
            from transformers.generation import GenerationConfig, GenerationMixin
            original_class = type(model.language_model)
            model.language_model.__class__ = type(
                "InternLM2GenerationCompat", (original_class, GenerationMixin), {})
            if model.language_model.generation_config is None:
                model.language_model.generation_config = GenerationConfig.from_model_config(
                    model.language_model.config)
        transform = transforms.Compose([transforms.Resize((448, 448)), transforms.ToTensor(),
                                        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
    durations = []
    completed = failed = 0
    for row in selected:
        key = row["key"]
        entry = state.get(key, {"split": row["split"], "row_number": row["row_number"],
                                "image_name": row["image_name"], "image_sha256": row["image_sha256"]})
        field = {"tags": "tags", "grounding": "grounding", "caption": "caption"}[args.stage]
        if field in entry and (field != "caption" or entry[field]):
            continue
        if args.stage == "grounding" and "tags" not in entry:
            raise RuntimeError("RAM++ tags missing for selected sample")
        if args.stage == "caption" and "grounding" not in entry:
            raise RuntimeError("GroundingDINO result missing for selected sample")
        image_path = args.data_dir / "Labelled Images" / row["image_name"]
        before = time.perf_counter()
        try:
            with Image.open(image_path) as opened:
                image = opened.convert("RGB")
            with torch.inference_mode():
                if args.stage == "tags":
                    value = inference_ram(transform(image).unsqueeze(0).to(device), model)[0]
                elif args.stage == "grounding":
                    query = (str(entry["tags"]).lower().replace(" | ", ". ") + ".") if entry["tags"] else "no tags."
                    inputs = processor(images=image, text=query, return_tensors="pt", padding=True, truncation=True)
                    inputs = {k: v.to(device) for k, v in inputs.items()}
                    found = processor.post_process_grounded_object_detection(
                        model(**inputs), inputs["input_ids"], threshold=0.4, text_threshold=0.3,
                        target_sizes=[image.size[::-1]])[0]
                    value = {}
                    for score, label, box in zip(found["scores"], found.get("text_labels", found["labels"]), found["boxes"]):
                        value.setdefault(str(label), []).append([*[round(float(v), 2) for v in box], round(float(score), 2)])
                else:
                    prompt = PROMPT_TEMPLATE.format(grounding=grounding_prompt(entry["grounding"]),
                                                    sentence=row["sentence"])
                    pixels = transform(image).unsqueeze(0).to(device=device, dtype=torch.bfloat16)
                    response = model.chat(tokenizer, pixels, prompt,
                                          {"max_new_tokens": args.max_new_tokens, "do_sample": False,
                                           "pad_token_id": tokenizer.pad_token_id})
                    value = parse_caption(response)
            torch.cuda.synchronize()
            elapsed = time.perf_counter() - before
            entry[field] = value
            entry[f"{field}_seconds"] = elapsed
            entry.pop(f"{field}_error", None)
            durations.append(elapsed)
            completed += 1
        except Exception as exc:
            entry[f"{field}_error"] = f"{type(exc).__name__}: {str(exc)[:120]}"
            with (args.output_dir / "errors.log").open("a") as error_stream:
                error_stream.write(f"stage={args.stage} key={key}\n{traceback.format_exc()}\n")
            failed += 1
        state[key] = entry
        if torch.cuda.max_memory_allocated() > 18 * 1024**3:
            raise RuntimeError("Stage 2 GPU allocation exceeded 18 GiB")
        if (completed + failed) % 25 == 0 or failed:
            save_state(private, state)
            print(json.dumps({"stage": args.stage, "processed": completed + failed, "completed": completed,
                              "failed": failed, "peak_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3}), flush=True)
    save_state(private, state)
    present = Counter(row["split"] for row in source if state.get(row["key"], {}).get(field))
    result = {"stage": args.stage, "requested": len(selected), "new_completed": completed, "new_failed": failed,
              "coverage": dict(present), "wall_seconds_sum": sum(durations),
              "latency_median_s": statistics.median(durations) if durations else None,
              "peak_allocated_gib": torch.cuda.max_memory_allocated() / 1024**3,
              "peak_reserved_gib": torch.cuda.max_memory_reserved() / 1024**3,
              "prompt_sha256": PROMPT_SHA256 if args.stage == "caption" else None,
              "max_new_tokens": args.max_new_tokens if args.stage == "caption" else None}
    print(json.dumps(result, sort_keys=True), flush=True)
    if failed:
        raise RuntimeError(f"{failed} samples failed; private manifest has per-sample errors")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", required=True, choices=("tags", "grounding", "caption"))
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--assets-dir", type=Path, required=True)
    parser.add_argument("--ram-source", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, choices=(10, 50, 740))
    parser.add_argument("--max-new-tokens", type=int, default=256)
    run(parser.parse_args())


if __name__ == "__main__":
    main()
