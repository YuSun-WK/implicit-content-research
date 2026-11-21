"""Report aggregate caption coverage and CLIP truncation without exposing samples."""
import argparse
from collections import Counter
import json
import math
from pathlib import Path
import statistics

from stage2_caption import PROMPT_SHA256, records


def quantile(values, fraction):
    return sorted(values)[math.ceil(len(values) * fraction) - 1] if values else None


def aggregate(args):
    from open_clip.tokenizer import HFTokenizer
    source = records(args.data_dir)
    selected = source[:args.limit] if args.limit else source
    state = json.loads(args.manifest.read_text())
    tokenizer = HFTokenizer(str(args.tokenizer_dir), context_length=77, local_files_only=True).tokenizer
    coverage = {split: Counter() for split in ("train", "dev", "test")}
    timings = {stage: [] for stage in ("tags", "grounding", "caption")}
    lengths = []
    duplicates = 0
    for row in selected:
        item = state.get(row["key"], {})
        if item and (item.get("image_sha256") != row["image_sha256"] or
                     item.get("split") != row["split"] or item.get("row_number") != row["row_number"]):
            raise ValueError("Private caption manifest identity mismatch")
        slot = coverage[row["split"]]
        slot["expected"] += 1
        for stage in ("tags", "grounding", "caption"):
            if stage in item:
                slot[stage + "_completed"] += 1
                if stage + "_seconds" in item:
                    timings[stage].append(item[stage + "_seconds"])
            if item.get(stage + "_error") and stage not in item:
                slot[stage + "_failed"] += 1
        caption = item.get("caption")
        if isinstance(caption, str) and caption.strip():
            lengths.append(len(tokenizer.encode(caption, add_special_tokens=True)))
            duplicates += caption.strip().casefold() == row["sentence"].strip().casefold()
    return {"dataset": "MultiOFF", "sample_policy": "complete_case_444_148_148",
            "sample_count": len(selected), "prompt_sha256": PROMPT_SHA256,
            "caption_source": "OpenGVLab/InternVL2_5-8B@e9e4c0dc1db56bfab10458671519b7fa3dd29463",
            "splits": {split: dict(counts) for split, counts in coverage.items()},
            "caption_nonempty": len(lengths), "caption_copies_original_text": duplicates,
            "openclip_tokenizer_limit": 77, "caption_over_77_tokens": sum(value > 77 for value in lengths),
            "caption_token_median": statistics.median(lengths) if lengths else None,
            "caption_token_p95": quantile(lengths, 0.95),
            "caption_token_max": max(lengths) if lengths else None,
            "seconds": {stage: {"n": len(values), "mean": statistics.mean(values) if values else None,
                                 "median": statistics.median(values) if values else None,
                                 "p95": quantile(values, 0.95)} for stage, values in timings.items()}}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--data-dir", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--tokenizer-dir", type=Path, required=True)
    parser.add_argument("--limit", type=int, choices=(10, 50, 740))
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = json.dumps(aggregate(args), indent=2, allow_nan=False) + "\n"
    if args.output:
        args.output.write_text(result)
    else:
        print(result, end="")


if __name__ == "__main__":
    main()
