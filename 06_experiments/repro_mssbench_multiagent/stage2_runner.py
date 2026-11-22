"""Run one bounded ThinkingGuard Stage 2 slice with the Stage 1 pipeline."""
import argparse
import csv
import json
import os
from pathlib import Path
import signal
from time import monotonic
from uuid import uuid4

from fasttrack_qwen import ADAPTER, IMAGE_MARKER, MODEL_ID, REVISION, ThinkingGuard
from journal import Journal, run_key
from manifest import SOURCES, expand_record, read_dataset, sha256
from pipeline import InvalidAgentOutput, PROMPT_VERSION, Pipeline, load_prompts
from stage1_native import QUANTIZATION
from stage1_smoke import ValidatedPipeline, build_work, read_journal, write_outputs


def frozen_rows(manifest, data_root):
    dataset = read_dataset(data_root / "combined.json")
    with manifest.open(newline="") as stream:
        frozen = list(csv.DictReader(stream))
    if len(frozen) != 200 or len({r["pair_id"] for r in frozen}) != 100:
        raise ValueError("expected frozen 100-pair manifest")
    rows = []
    for fixed in frozen:
        task, index = fixed["task"], int(fixed["record_index"])
        row = next(r for r in expand_record(task, dataset[task][index], index)
                   if r["pair_id"] == fixed["pair_id"] and r["gold_label"] == fixed["gold_label"])
        for field in ("dataset_revision", "pair_id", "task", "record_index", "text_index",
                      "variant", "gold_label", "category", "subtask", "same_text", "image_path"):
            if str(row[field]) != fixed[field]:
                raise ValueError(f"frozen row mismatch: {fixed['pair_id']} {field}")
        if sha256(row["text"].encode()) != fixed["text_sha256"]:
            raise ValueError("frozen text hash mismatch")
        rows.append({**row, "text_sha256": fixed["text_sha256"], "expected_bytes": fixed["expected_bytes"],
                     "hf_lfs_sha256": fixed["hf_lfs_sha256"],
                     "anchor": fixed["anchor"] == "True", "chunk_id": int(fixed["chunk_id"]),
                     "pair_index": int(fixed["pair_index"])})
    return rows


def configure(work):
    for unit in work:
        config = unit.config
        config.pop("native_source_commit")
        config.pop("vision_revision")
        config.update(model_id=MODEL_ID, model_revision=REVISION, adapter_revision=ADAPTER,
                      prompt_version=PROMPT_VERSION + "+fasttrack-invalid-v1",
                      processor="qwen3-vl-224-native-template-v1", image_marker=IMAGE_MARKER,
                      collect_invalid=True,
                      quantization={**QUANTIZATION, "skip": ["visual", "lm_head"]})
        config["decoding"]["repetition_penalty"] = 1.0


def checked_model(root, snapshot):
    payload = (root / "verified.json").read_bytes()
    verified = json.loads(payload)
    if (verified["model_id"], verified["revision"]) != (MODEL_ID, REVISION):
        raise ValueError("wrong cached substitute model lock")
    for item in verified["files"]:
        target = snapshot / item["name"]
        if not target.is_file() or target.stat().st_size != item["bytes"]:
            raise ValueError(f"cached substitute file changed: {item['name']}")
    return sha256(payload)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for name in ("pair-manifest", "data-root", "model-root", "snapshot", "official-source", "output"):
        parser.add_argument(f"--{name}", type=Path, required=True)
    parser.add_argument("--gpu-uuid", required=True)
    parser.add_argument("--max-new-tokens", type=int, choices=(256, 512), required=True)
    parser.add_argument("--chunk", type=int, choices=range(4))
    parser.add_argument("--pair-ids-file", type=Path)
    parser.add_argument("--pilot-pairs", type=int, default=0)
    parser.add_argument("--limit-pairs", type=int, default=0)
    args = parser.parse_args()
    if (args.max_new_tokens == 256) != (args.chunk is not None):
        parser.error("256 requires --chunk; 512 requires --pair-ids-file")
    if args.max_new_tokens == 512 and args.pair_ids_file is None:
        parser.error("512 requires --pair-ids-file")
    if args.pilot_pairs and args.max_new_tokens != 512:
        parser.error("--pilot-pairs only applies to 512")
    if args.limit_pairs and (args.max_new_tokens != 256 or args.limit_pairs < 1):
        parser.error("--limit-pairs applies only to 256")
    if os.environ.get("CUDA_VISIBLE_DEVICES") != args.gpu_uuid or os.environ.get("HF_HUB_OFFLINE") != "1":
        raise ValueError("one selected GPU and offline model loading required")
    args.processor = "mssbench_224"
    args.seed = 0
    lock = checked_model(args.model_root, args.snapshot)
    rows = frozen_rows(args.pair_manifest, args.data_root)
    if args.max_new_tokens == 256:
        selected = [r for r in rows if r["chunk_id"] == args.chunk and not r["anchor"]]
        pilot_ids = None
    else:
        ids = args.pair_ids_file.read_text().splitlines()
        if len(ids) != 10 or len(set(ids)) != 10:
            raise ValueError("expected ten fixed diagnostic pair IDs")
        pilot_ids = set(ids[:args.pilot_pairs]) if args.pilot_pairs else set(ids[2:])
        selected = [r for r in rows if r["pair_id"] in ids]
    if len(selected) != 2 * len({r["pair_id"] for r in selected}):
        raise ValueError("slice lost a pair side")
    work = build_work(args, selected, lock)
    configure(work)
    args.output.mkdir(parents=True, exist_ok=True)
    journal = Journal(args.output / "smoke.sqlite")
    prior = {a["key"] for a in read_journal(journal) if a["status"] in ("complete", "invalid")}
    pending = [unit for unit in work if run_key(unit.config) not in prior]
    if pilot_ids is not None:
        pending = [unit for unit in pending if unit.config["pair_id"] in pilot_ids]
    if args.limit_pairs:
        limit_ids = list(dict.fromkeys(unit.config["pair_id"] for unit in work))[:args.limit_pairs]
        pending = [unit for unit in pending if unit.config["pair_id"] in limit_ids]
    print("slice pairs", len(selected) // 2, "pending method-inputs", len(pending), flush=True)
    if not pending:
        write_outputs(args.output, journal, work, set(), [])
        return
    prompts = load_prompts(args.official_source)
    started = monotonic()
    session = str(uuid4())

    def deadline(_signum, _frame):
        raise TimeoutError("Stage 2 GPU job reached six-hour limit")

    signal.signal(signal.SIGALRM, deadline)
    signal.alarm(6 * 3600)
    loads = []
    try:
        model = ThinkingGuard(args.snapshot, args.gpu_uuid,
                              max_new_tokens=args.max_new_tokens, seed=0)
        loads.append(model.model_load)
        with (args.output / "model_loads.jsonl").open("a") as stream:
            stream.write(json.dumps({"session": session, **model.model_load}) + "\n")
        pipeline = Pipeline(model, prompts, stop_on_invalid=True)
        for unit in pending:
            config = {**unit.config, "session": session, "gpu_uuid": args.gpu_uuid}
            print(config["pair_id"], config["gold_label"], config["method"], flush=True)
            try:
                journal.run(config, ValidatedPipeline(pipeline, config), unit.text, unit.image)
            except InvalidAgentOutput as exc:
                print("model-format invalid", config["pair_id"], config["gold_label"],
                      config["method"], str(exc), flush=True)
        print("slice seconds", round(monotonic() - started, 3), flush=True)
    finally:
        signal.alarm(0)
        write_outputs(args.output, journal, work, set(), loads)


if __name__ == "__main__":
    main()
