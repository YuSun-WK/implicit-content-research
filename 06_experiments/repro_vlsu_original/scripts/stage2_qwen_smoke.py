"""Local single-GPU Qwen Stage 2 smoke, with a private durable output ledger."""

import argparse
from collections import Counter
from contextlib import closing
from hashlib import sha1, sha256
from importlib.metadata import PackageNotFoundError, version
import json
from math import ceil
import os
from pathlib import Path
import signal
import sqlite3
from statistics import median
import subprocess
from time import monotonic

import yaml

from stage0_metrics import INVALID, gold_label, parse_output
from stage1_download import atomic, digest
from stage1_manifest import canonical, validate_records
from stage2_roster import freeze, task_rows

BASE = Path(__file__).resolve().parents[1]
TITLE = "ENGINEERING SMOKE / PARTIAL REPRODUCTION"
MODES = ("direct", "binary", "structured_cot")


def gpu_environment():
    def query(option, fields):
        try:
            result = subprocess.run(["nvidia-smi", f"--{option}={fields}",
                                     "--format=csv,noheader,nounits"], text=True,
                                    capture_output=True, check=True, timeout=8)
        except (OSError, subprocess.SubprocessError):
            return None
        return [dict(zip(fields.split(","), map(str.strip, line.split(",")), strict=True))
                for line in result.stdout.splitlines() if line.strip()]

    dependencies = {}
    for name in ("torch", "transformers", "Pillow", "qwen-vl-utils", "accelerate", "bitsandbytes", "huggingface-hub"):
        try:
            dependencies[name] = version(name)
        except PackageNotFoundError:
            dependencies[name] = None
    return {"gpus": query("query-gpu", "index,uuid,name,memory.total,memory.free,memory.used,utilization.gpu,driver_version"),
            "compute_apps": query("query-compute-apps", "gpu_uuid,used_gpu_memory"),
            "packages": dependencies}


def available_gpu(environment):
    selected = os.environ.get("CUDA_VISIBLE_DEVICES", "")
    gpus, processes = environment["gpus"], environment["compute_apps"]
    if not gpus or processes is None:
        raise ValueError("GPU availability or process ownership cannot be verified")
    matches = [g for g in gpus if g["uuid"] == selected]
    if len(matches) != 1:
        raise ValueError("Set CUDA_VISIBLE_DEVICES to the one selected physical GPU UUID")
    gpu = matches[0]
    if any(p["gpu_uuid"] == selected for p in processes) or int(gpu["utilization.gpu"]) != 0 or int(gpu["memory.used"]) > 512:
        raise ValueError("Selected GPU is already in use")
    return gpu


def check_prompts():
    entries = yaml.safe_load((BASE / "configs/official_qwen25vl7b.yaml").read_bytes())["prompts"]
    result = {}
    for name in MODES:
        info = entries[name]
        raw = (BASE / info["path"]).read_bytes()
        if sha256(raw).hexdigest() != info["sha256"]:
            raise ValueError(f"Prompt drift: {name}")
        result[name] = raw.decode()
    return result


def model_manifest(path, config):
    if not path.is_dir() or path.name != config["revision"]:
        raise ValueError("Model path must be the exact revision-named HF snapshot")
    expected = json.loads((BASE / "configs/stage2_model_files.json").read_bytes())
    if expected["revision"] != config["revision"] or expected["model_id"] != config["model_id"]:
        raise ValueError("Model file manifest revision mismatch")
    files = expected["files"]
    checked = {}
    for name, metadata in files.items():
        if not metadata.get("sha256") and not metadata.get("git_blob"):
            raise ValueError("Model file provenance unavailable")
        item = path / name
        if not item.is_file() or item.stat().st_size != metadata["size"]:
            raise ValueError(f"Missing or incomplete model file: {name}")
        if metadata.get("sha256"):
            observed = digest(item)
            if observed != metadata["sha256"]:
                raise ValueError(f"Model weight SHA-256 mismatch: {name}")
        else:
            raw = item.read_bytes()
            if sha1(f"blob {len(raw)}\0".encode() + raw).hexdigest() != metadata["git_blob"]:
                raise ValueError(f"Model metadata Git blob mismatch: {name}")
            observed = sha256(raw).hexdigest()
        checked[name] = observed
    return {"model_id": config["model_id"], "revision": config["revision"], "tokenizer_revision": config["revision"],
            "processor_revision": config["revision"], "local_files_verified": True, "sha256_by_file": checked,
            "weight_bytes": sum(v["size"] for k, v in files.items() if k.endswith(".safetensors"))}


def load_processor(path, config):
    from transformers import AutoProcessor

    return AutoProcessor.from_pretrained(
        path, local_files_only=True, trust_remote_code=False, use_fast=True,
        min_pixels=config["image"]["min_pixels"], max_pixels=config["image"]["max_pixels"])


def prepare_inputs(processor, path, prompt, query):
    from PIL import Image, ImageOps

    with Image.open(path) as raw:
        image = ImageOps.exif_transpose(raw).convert("RGB")
    messages = [{"role": "user", "content": [{"type": "image", "image": image},
                 {"type": "text", "text": f"{prompt}\n{query}"}]}]
    formatted = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
    return processor(text=[formatted], images=[image], return_tensors="pt")


class Qwen:
    def __init__(self, path, config, precision, seed):
        import torch
        from transformers import BitsAndBytesConfig, Qwen2_5_VLForConditionalGeneration

        self.torch = torch
        if not torch.cuda.is_available() or torch.cuda.device_count() != 1 or not torch.cuda.is_bf16_supported():
            raise ValueError("One BF16-capable CUDA device is required")
        torch.manual_seed(seed)
        total = torch.cuda.get_device_properties(0).total_memory
        budget = config["gpu_budget_gib"] * 1024**3
        torch.cuda.set_per_process_memory_fraction(min(1, budget / total), 0)
        self.processor = load_processor(path, config)
        quantization = None
        if precision == "4bit":
            quantization = BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_quant_type="nf4",
                                              bnb_4bit_compute_dtype=torch.bfloat16,
                                              bnb_4bit_use_double_quant=True)
        self.model = Qwen2_5_VLForConditionalGeneration.from_pretrained(
            path, local_files_only=True, use_safetensors=True, dtype=torch.bfloat16,
            attn_implementation="sdpa",
            **({"quantization_config": quantization, "device_map": {"": "cuda:0"}} if quantization else {}))
        if not quantization:
            self.model.to("cuda:0")
        self.model.eval()
        self.runtime = {
            "torch_cuda": torch.version.cuda, "gpu_name": torch.cuda.get_device_name(0),
            "chat_template_sha256": sha256(self.processor.chat_template.encode()).hexdigest(),
            "eos_token_id": self.model.generation_config.eos_token_id,
            "pad_token_id": self.model.generation_config.pad_token_id,
            "precision": precision, "quantization": {"backend": "bitsandbytes", "type": "nf4",
            "compute_dtype": "bfloat16", "double_quant": True} if quantization else None,
            "load_peak_allocated_bytes": torch.cuda.max_memory_allocated(),
            "load_peak_reserved_bytes": torch.cuda.max_memory_reserved(),
        }

    def peaks(self):
        return {"peak_allocated_bytes": self.torch.cuda.max_memory_allocated(),
                "peak_reserved_bytes": self.torch.cuda.max_memory_reserved()}

    def generate(self, path, prompt, query, settings):
        torch = self.torch
        start = monotonic()
        torch.cuda.reset_peak_memory_stats()
        data = prepare_inputs(self.processor, path, prompt, query).to("cuda:0")
        grid = data["image_grid_thw"][0].tolist()
        merge = self.processor.image_processor.merge_size
        preprocessed_s = monotonic() - start
        with torch.inference_mode():
            output = self.model.generate(**data, **settings, temperature=None, top_p=None, top_k=None)
        torch.cuda.synchronize()
        tokens = output[0, data["input_ids"].shape[-1]:]
        return {"raw_output": self.processor.decode(tokens, skip_special_tokens=True,
                                                    clean_up_tokenization_spaces=False),
                "generated_tokens": len(tokens), "input_tokens": data["input_ids"].shape[-1],
                "image_grid_thw": grid, "image_tokens": grid[0] * grid[1] * grid[2] // merge**2,
                "runtime_s": monotonic() - start, "preprocess_s": preprocessed_s, **self.peaks()}


def execute(backend, root, subjects, queries, rows, image_root, prompts, run_spec, mode):
    run_id = sha256(canonical(run_spec)).hexdigest()
    run_dir = root / run_id
    run_dir.mkdir(parents=True, mode=0o700, exist_ok=True)
    atomic(run_dir / "run_spec.json", canonical(run_spec))
    settings = run_spec["generation"]
    parse_mode = "cot" if mode == "structured_cot" else mode
    start = monotonic()
    with closing(sqlite3.connect(run_dir / "run.sqlite", timeout=1)) as db:
        db.execute("CREATE TABLE IF NOT EXISTS outputs (uuid TEXT PRIMARY KEY, payload TEXT NOT NULL)")
        # Hold an exclusive filesystem lock across GPU work to prevent a concurrent
        # resume from regenerating an already scheduled sample.
        import fcntl
        with (run_dir / "run.lock").open("a") as lock:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            done = {uid: json.loads(data) for uid, data in db.execute("SELECT * FROM outputs")}
            stop = None
            try:
                for subject in subjects:
                    uid = subject["uuid"]
                    if uid in done:
                        continue
                    path = image_root / subject["image_sha256"]
                    record = {**subject, "run_id": run_id, "prompt_sha256": run_spec["prompt_sha256"],
                              "input_sha256": sha256(canonical([subject["query_sha256"], subject["image_sha256"],
                                                                 run_spec["prompt_sha256"]])).hexdigest(),
                              "state": "generated", "model_revision": run_spec["model_revision"],
                              "processor_revision": run_spec["model_revision"], "seed": run_spec["seed"],
                              "precision": run_spec["precision"], "quantization": run_spec["runtime"]["quantization"],
                              "decoding": settings, "eos_token_id": run_spec["runtime"].get("eos_token_id"),
                              "pad_token_id": run_spec["runtime"].get("pad_token_id")}
                    try:
                        if digest(path) != subject["image_sha256"]:
                            raise ValueError("Image hash changed")
                        record.update(backend.generate(path, prompts[mode], queries[uid], settings))
                    except Exception as exc:
                        record.update(state="generation_error", error=type(exc).__name__)
                        if isinstance(backend, Qwen):
                            record.update(backend.peaks())
                        stop = type(exc).__name__
                    with db:
                        db.execute("INSERT INTO outputs VALUES (?,?)", (uid, canonical(record).decode()))
                    done[uid] = record
                    if stop:
                        break
            except KeyboardInterrupt:
                stop = "interrupted"
            finally:
                ledger = [done.get(r["uuid"], {**r, "run_id": run_id, "state": "not_run"}) for r in subjects]
                validate_records(ledger, {r["uuid"] for r in subjects}, rows, 4)
                parsed = []
                for record in ledger:
                    generated = record["state"] == "generated"
                    label = parse_output(record["raw_output"], parse_mode) if generated else INVALID
                    parsed.append({k: v for k, v in record.items() if k != "raw_output"} | {
                        "prediction": label, "mapped_gold": gold_label(record["gold"], binary=mode == "binary"),
                        "parse_status": ("valid" if label != INVALID else "invalid") if generated else "not_generated",
                        "raw_output_reference": f"raw.jsonl#{record['uuid']}" if generated else None})
                atomic(run_dir / "raw.jsonl", b"".join(canonical(r) for r in ledger))
                atomic(run_dir / "parsed.jsonl", b"".join(canonical(r) for r in parsed))
                successes = [r for r in parsed if r["state"] == "generated"]
                durations = sorted(r["runtime_s"] for r in successes)
                distribution = Counter(r["parse_status"] for r in parsed)
                summary = {"run_id": run_id, "mode": mode, "selected": len(subjects), "generated": len(successes),
                           "status": "COMPLETE" if len(successes) == len(subjects) else "PARTIAL",
                           "states": dict(Counter(r["state"] for r in parsed)), "parse_status": dict(distribution),
                           "valid_rate": distribution["valid"] / len(successes) if successes else None,
                           "p50_latency_s": median(durations) if durations else None,
                           "p95_latency_s": durations[ceil(len(durations) * .95) - 1] if durations else None,
                           "samples_per_s": len(durations) / sum(durations) if durations else None,
                           "generated_tokens": sum(r["generated_tokens"] for r in successes),
                           "generated_tokens_per_sample": [r["generated_tokens"] for r in successes],
                           "peak_allocated_bytes": max((r["peak_allocated_bytes"] for r in parsed if "peak_allocated_bytes" in r), default=None),
                           "peak_reserved_bytes": max((r["peak_reserved_bytes"] for r in parsed if "peak_reserved_bytes" in r), default=None),
                           "call_wall_s": monotonic() - start, "stop": stop}
                atomic(run_dir / "summary.json", canonical(summary))
    return summary


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--csv", type=Path, required=True)
    parser.add_argument("--stage1-root", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--model-path", type=Path)
    parser.add_argument("--out", type=Path, default=BASE / ".local/stage2")
    parser.add_argument("--mode", choices=MODES, default="direct")
    parser.add_argument("--precision", choices=("auto", "bf16", "4bit"), default="auto")
    parser.add_argument("--short-output", type=int)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    os.umask(0o077)
    config = yaml.safe_load((BASE / "configs/stage2_smoke.yaml").read_bytes())
    args.out.mkdir(mode=0o700, parents=True, exist_ok=True)
    config_sha256 = digest(BASE / "configs/stage2_smoke.yaml")
    environment = gpu_environment()
    atomic(args.out / "gpu_environment.json", canonical(environment))
    roster, queries, rows = freeze(args.csv, args.stage1_root, args.manifest, config["stage1_manifest_sha256"],
                                   config["seed"], config["joint_count"])
    roster_data = canonical(roster)
    roster_sha256 = sha256(roster_data).hexdigest()
    atomic(args.out / f"roster-{roster_sha256}.json", roster_data)
    prompts = check_prompts()
    subjects = task_rows(roster, args.mode, config["diagnostic_count"])
    details = {"scope": TITLE, "roster_sha256": roster_sha256, "selected": len(subjects),
               "stage1_manifest_sha256": config["stage1_manifest_sha256"], "mode": args.mode,
               "total_frozen": len(roster["subjects"]), "patterns": dict(Counter(r["pattern"] for r in subjects)),
               "gold_counts": dict(Counter(r["gold"] for r in subjects)), "status": "NOT RUN"}
    print(json.dumps(details, sort_keys=True), flush=True)
    if not args.execute:
        return 0
    if not args.model_path:
        parser.error("--execute requires --model-path")
    os.environ.update(HF_HUB_OFFLINE="1", TRANSFORMERS_OFFLINE="1")
    try:
        model = model_manifest(args.model_path, config)
    except (ValueError, OSError) as error:
        blocked = {**details, "generated": 0, "stop": "MODEL SNAPSHOT NOT AVAILABLE", "reason": str(error),
                   "model_revision": config["revision"]}
        atomic(args.out / f"{args.mode}-latest-summary.json", canonical(blocked))
        print(json.dumps(blocked, sort_keys=True), flush=True)
        return 2
    atomic(args.out / "model_manifest.json", canonical(model))
    environment = gpu_environment()
    gpu = available_gpu(environment)
    settings = {k: v for k, v in config["generation"].items() if k != "max_new_tokens"}
    length = config["generation"]["max_new_tokens"][args.mode]
    if args.short_output is not None and not 1 <= args.short_output < length:
        parser.error("--short-output must be positive and below the configured max length")
    settings["max_new_tokens"] = args.short_output or length
    budget = min(config["gpu_budget_gib"], int(gpu["memory.free"]) / 1024)
    precision = args.precision
    if precision == "auto":
        precision = "bf16" if model["weight_bytes"] / 1024**3 + 2 <= budget else "4bit"
    if precision == "bf16" and model["weight_bytes"] / 1024**3 + 2 > budget:
        raise ValueError("BF16 exceeds the budget estimate; select auto or 4bit")
    if precision == "4bit" and any(not environment["packages"][dep] for dep in ("bitsandbytes", "accelerate")):
        raise ValueError("bitsandbytes and accelerate are required for the resource-constrained run")
    signal.signal(signal.SIGTERM, lambda *_: signal.raise_signal(signal.SIGINT))
    signal.signal(signal.SIGALRM, lambda *_: signal.raise_signal(signal.SIGINT))
    signal.alarm(6 * 60 * 60 - 30)
    def build_spec(backend):
        return {"roster_sha256": roster_sha256, "config_sha256": config_sha256, "mode": args.mode,
                "prompt_sha256": sha256(prompts[args.mode].encode()).hexdigest(),
                "model_revision": config["revision"], "generation": settings, "precision": precision,
                "runtime": {k: v for k, v in backend.runtime.items() if not k.startswith("load_peak")},
                "packages": environment["packages"], "image": config["image"], "seed": config["seed"],
                "runner_sha256": digest(Path(__file__)),
                "scope": (TITLE if precision == "bf16" else "RESOURCE-CONSTRAINED PARTIAL REPRODUCTION"),
                "output_protocol": "ENGINEERING_SHORT_OUTPUT" if args.short_output else "PAPER_MAX_LEN_LOCAL_API"}
    load_start = monotonic()
    try:
        backend = Qwen(args.model_path, config, precision, config["seed"])
    except (Exception, KeyboardInterrupt) as exc:
        failure = {**details, "stop": type(exc).__name__, "precision_attempted": precision,
                   "load_wall_s": monotonic() - load_start, "model_revision": config["revision"]}
        atomic(args.out / f"{args.mode}-latest-summary.json", canonical(failure))
        print(json.dumps(failure), flush=True)
        raise
    load_wall = monotonic() - load_start
    summary = execute(backend, args.out, subjects, queries, rows, args.stage1_root / "objects", prompts,
                      build_spec(backend), args.mode)
    summary.update(load_wall_s=load_wall, runtime=backend.runtime, nvidia_smi_before=gpu,
                   nvidia_smi_after=gpu_environment()["gpus"], precision=precision, model_revision=config["revision"],
                   label=TITLE if precision == "bf16" else "RESOURCE-CONSTRAINED PARTIAL REPRODUCTION")
    atomic(args.out / f"{args.mode}-latest-summary.json", canonical(summary))
    print(json.dumps(summary, sort_keys=True), flush=True)
    return 0 if summary["status"] == "COMPLETE" else 2


if __name__ == "__main__":
    raise SystemExit(main())
