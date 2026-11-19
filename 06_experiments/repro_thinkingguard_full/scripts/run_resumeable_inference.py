"""Run the frozen ThinkingGuard Stage 1 queues with an atomic prediction journal."""
import argparse
import csv
import fcntl
import hashlib
import importlib.metadata
import json
import math
import os
import subprocess
import sys
import threading
import time
from datetime import datetime, timezone
from pathlib import Path

from official_parser_v3 import parse

ROOT = Path(__file__).resolve().parents[1]


def now():
    return datetime.now(timezone.utc).isoformat()


def sha(path):
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def read(path):
    return json.loads(path.read_text())


def atomic_write(path, payload):
    temporary = path.with_name("." + path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    temporary.replace(path)
    directory = os.open(str(path.parent), os.O_DIRECTORY)
    try:
        os.fsync(directory)
    finally:
        os.close(directory)


def write(path, payload):
    atomic_write(path, json.dumps(payload, ensure_ascii=False, indent=2) + "\n")


def journal(path, rows):
    atomic_write(path, "".join(json.dumps(row, ensure_ascii=False) + "\n" for row in rows.values()))


def read_journal(path, expected, identity):
    result = {}
    if path.exists():
        for line in path.read_text().splitlines():
            row = json.loads(line)
            uid = row["sample_uid"]
            if uid not in expected or uid in result or row["identity"] != identity:
                raise ValueError(f"Unknown/duplicate key or configuration conflict: {uid}")
            result[uid] = row
    return result


def smi(*options):
    return subprocess.check_output(["nvidia-smi", *options], text=True, timeout=6).strip()


def gpu_rows():
    raw = smi("--query-compute-apps=gpu_uuid,pid,used_gpu_memory", "--format=csv,noheader,nounits")
    return [tuple(field.strip() for field in line.split(",")) for line in raw.splitlines()]


def card(uuid):
    row = smi("-i", uuid, "--query-gpu=uuid,name,memory.total,memory.used,utilization.gpu,driver_version",
              "--format=csv,noheader,nounits")
    uid, name, total, used, busy, driver = (x.strip() for x in row.split(","))
    return dict(uuid=uid, name=name, total_mib=int(total), used_mib=int(used),
                utilization_pct=int(busy), driver=driver)


def audit_resource(uuid, cap_mib, deadline, log_path, peaks, started):
    pid = str(os.getpid())
    seen = False
    with log_path.open("a", buffering=1) as log:
        while time.monotonic() < deadline:
            row = {"utc": now(), "pid": pid}
            fatal = None
            try:
                row.update(card(uuid))
                processes = [(p, m) for device, p, m in gpu_rows() if device == uuid]
                memory = next((value for proc, value in processes if proc == pid), None)
                row["process_mib"] = int(memory) if memory is not None else None
                seen |= memory is not None
                if any(proc != pid for proc, _ in processes):
                    fatal = "OTHER_PROCESS_ON_SELECTED_GPU"
                if row["process_mib"] is None and seen:
                    fatal = "PROCESS_MEMORY_LOST"
                if row["process_mib"] is None and time.monotonic() - started > 45:
                    fatal = "PROCESS_MEMORY_UNAVAILABLE"
                if row["used_mib"] >= cap_mib or (row["process_mib"] or 0) >= cap_mib:
                    fatal = "MEMORY_LIMIT"
                for field in ("used_mib", "process_mib"):
                    if row[field] is not None:
                        peaks[field] = max(peaks.get(field, 0), row[field])
            except (subprocess.SubprocessError, OSError, ValueError) as exc:
                fatal = f"TELEMETRY_UNAVAILABLE: {exc}"
            if fatal:
                row["abort"] = fatal
            log.write(json.dumps(row) + "\n")
            if fatal:
                os.fsync(log.fileno())
                os._exit(71)
            time.sleep(0.5)
        log.write(json.dumps({"utc": now(), "abort": "HARD_WALL_LIMIT"}) + "\n")
        os.fsync(log.fileno())
        os._exit(72)


def percentile(values, quantile):
    values = sorted(values)
    return values[max(0, math.ceil(len(values) * quantile) - 1)] if values else None


def summarize(rows, stage, peaks):
    generated = [r for r in rows.values() if r["status"] == "GENERATED"]
    valid = sum(r["parsed_verdict"] in ("Safe", "Unsafe") for r in generated)
    latency_rows = generated
    if stage == "validation" and len(generated) >= 10:
        rank = sorted(generated, key=lambda r: (r["image_pixels"], r["visual_tokens"], r["sample_uid"]))
        middle = len(rank) // 2
        latency_rows = rank[middle-2:middle+3] + rank[-5:]
    values = [r["elapsed"] for r in latency_rows]
    return dict(prediction_count=len(rows), generated_count=len(generated), extracted=valid,
                coverage=valid/len(rows) if rows else None,
                structure_complete=sum(r["structure_complete"] for r in generated),
                ambiguous_templates=sum(r["parse_status"] == "AMBIGUOUS_TEMPLATE" for r in generated),
                hit_token_cap=sum(r["generated_tokens"] == 1024 for r in generated),
                stage_end_marker_coverage={
                    step: sum(not r["steps"][step]["missing"] for r in generated)
                    for step in ("Intent", "Entity", "Attribute", "Risk", "Overall")
                },
                latency_sample_uids=[r["sample_uid"] for r in latency_rows],
                latency_seconds={f"p{q}": percentile(values, q/100) for q in (50, 90, 95)},
                independent_human_review="NOT_RUN", gpu_sample_peaks_mib=peaks)


def main():
    cli = argparse.ArgumentParser(description=__doc__)
    cli.add_argument("--stage", choices=("smoke", "validation", "pilot"), required=True)
    cli.add_argument("--model", type=Path, required=True)
    cli.add_argument("--gpu-uuid")
    cli.add_argument("--run-id")
    cli.add_argument("--resume", action="store_true")
    cli.add_argument("--dry-run", action="store_true")
    cli.add_argument("--preflight-only", action="store_true")
    args = cli.parse_args()

    settings_path = ROOT / "configs/author_five_step_nf4.yaml"
    prompt_path = ROOT / "configs/author_prompt.json"
    queue_path = ROOT / "artifacts/sample_queues.json"
    manifest = ROOT / "artifacts/manifests/test_manifest.csv"
    validation = read(ROOT / "artifacts/manifests/data_validation.json")
    freeze = read(ROOT / "artifacts/parser_freeze.json")
    config, prompt, queues = map(read, (settings_path, prompt_path, queue_path))
    model_audit = read(ROOT / "artifacts/model_cache_audit.json")
    with manifest.open() as handle:
        rows = list(csv.DictReader(handle))
    entries = {r["sample_uid"]: r for r in rows}
    ordered = queues[args.stage]
    requirements = {
        "manifest": len(rows) == len(entries) == 1736 and sha(manifest) == validation["manifest_sha256"],
        "data": validation["gpu_data_gate"] and all(entries[uid]["run_status"] == "READY" for uid in ordered),
        "queues": sha(queue_path) == freeze["queue_sha256"] and len(ordered) == len(set(ordered))
                  and len(ordered) == {"smoke": 6, "validation": 36, "pilot": 200}[args.stage],
        "parser": sha(Path(__file__).with_name("official_parser_v3.py"))
                  == freeze["parser_sha256"] == config["parser_sha256"]
                  and sha(ROOT / "tests/test_official_parser_v3.py") == freeze["tests_sha256"],
        "prompt": sha(prompt_path) == freeze["prompt_config_sha256"] == config["prompt_config_sha256"]
                  and hashlib.sha256(prompt["system_prompt"].encode()).hexdigest()
                  == config["system_prompt_sha256"],
        "model": model_audit["status"] == "DONE" and args.model.name
                 == config["model_revision"] == model_audit["revision"]
                 and (args.model / "model.safetensors.index.json").is_file()
                 and sha(args.model / "model.safetensors.index.json") == model_audit["local_index_sha256"]
                 and all((args.model / filename).is_file() and sha(args.model / filename) == evidence["sha256"]
                         for filename, evidence in model_audit["processor_and_configs"].items()),
    }
    print(json.dumps(dict(stage=args.stage, queued=len(ordered), preflight=requirements), indent=2), flush=True)
    if args.dry_run:
        return 0
    if not all(requirements.values()):
        return 2
    if args.preflight_only:
        return 0
    if not args.gpu_uuid or not args.run_id or not args.run_id.replace("-", "").replace("_", "").isalnum():
        cli.error("A permitted GPU UUID and an alphanumeric run ID are required")

    identity_base = dict(config_sha256=sha(settings_path), manifest_sha256=sha(manifest),
                         queues_sha256=sha(queue_path), model_audit_sha256=sha(ROOT / "artifacts/model_cache_audit.json"),
                         runner_sha256=sha(Path(__file__)))
    identity = dict(**identity_base, stage=args.stage, run_id=args.run_id)
    out = ROOT / "runs" / args.run_id
    out.mkdir(exist_ok=True)
    lock = (out / ".lock").open("a")
    fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    identity_path, journal_path = out / "identity.json", out / "predictions.jsonl"
    if identity_path.exists() and (not args.resume or read(identity_path) != identity):
        raise ValueError("Existing run requires --resume with the same configuration")
    if journal_path.exists() and not identity_path.exists():
        raise ValueError("Journal exists without a run identity")
    prior = read_journal(journal_path, set(ordered), identity)
    if len(prior) == len(ordered):
        prior_summary = out / "summary.json"
        if prior_summary.exists():
            return 0 if read(prior_summary)["resource_gate"] else 3
        raise ValueError("Complete prediction journal is missing its terminal resource summary")
    benchmark_p95 = None
    required_stages = {"smoke": [], "validation": ["smoke"], "pilot": ["smoke", "validation"]}
    for stage in required_stages[args.stage]:
        previous = ROOT / "runs" / stage / "summary.json"
        summary = read(previous) if previous.is_file() else {}
        if not summary.get("resource_gate") or summary.get("identity") != dict(**identity_base, stage=stage, run_id=stage):
            raise ValueError(f"Missing passing {stage} resource gate for this configuration")
        if stage == "validation":
            if summary["prediction_count"] != 36 or summary["coverage"] < freeze["minimum_parse_coverage"]:
                raise ValueError("Independent A0 parse coverage did not reach 95%")
            benchmark_p95 = summary["latency_seconds"]["p95"]
            review_path = previous.with_name("raw_only_transcription.json")
            review = read(review_path) if review_path.exists() else {}
            if review.get("raw_review_sha256") != sha(previous.with_name("raw_only_review.json")):
                raise ValueError("Missing raw-only verdict transcription for the validation run")
            expected_review = {row["review_id"] for row in read(previous.with_name("raw_only_review.json"))}
            decisions = review.get("decisions", {})
            if set(decisions) != expected_review or set(decisions.values()) - {"Safe", "Unsafe", "INVALID"}:
                raise ValueError("Validation transcription is incomplete")
            verdict_records = read_journal(previous.with_name("predictions.jsonl"), set(queues["validation"]),
                                          summary["identity"])
            replay = {hashlib.sha256((str(config["seed"]) + key).encode()).hexdigest()[:16]:
                      row["parsed_verdict"] for key, row in verdict_records.items()}
            if replay != decisions:
                raise ValueError("Validation parser and raw-only verdict transcription disagree")
    initial = card(args.gpu_uuid)
    if (initial["uuid"] != args.gpu_uuid or "4090" not in initial["name"] or initial["used_mib"] > 64
            or initial["utilization_pct"] or any(device == args.gpu_uuid for device, _, _ in gpu_rows())):
        raise ValueError("Requested GPU is occupied or differs from the allowed GPU class")
    for uid in ordered:
        row = entries[uid]
        if uid not in prior and sha(Path(row["image_local_path"])) != row["image_sha256"]:
            raise ValueError(f"Image content changed: {uid}")
    for shard in model_audit["shards"]:
        if sha(args.model / shard["name"]) != shard["sha256"]:
            raise ValueError(f"Model weight changed: {shard['name']}")
    for package, version in config["versions"].items():
        if package not in ("python", "cuda") and importlib.metadata.version(package) != version:
            raise ValueError(f"Environment version mismatch: {package}")
    if ".".join(map(str, sys.version_info[:3])) != config["versions"]["python"]:
        raise ValueError("Python version mismatch")
    if not identity_path.exists():
        write(identity_path, identity)
    write(out / f"job-{time.time_ns()}.json", dict(
        start_utc=now(), argv=sys.argv, gid=initial, git=subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(), identity=identity))
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_uuid
    os.environ["HF_HUB_OFFLINE"] = "1"

    start = time.monotonic()
    deadline = start + config["max_wall_seconds"]
    peaks = {}
    thread = threading.Thread(target=audit_resource,
                              args=(args.gpu_uuid, config["memory_cap_gib"]*1024, deadline,
                                    out / "gpu_samples.jsonl", peaks, start), daemon=True)
    thread.start()
    import torch
    from PIL import Image
    from transformers import AutoProcessor, BitsAndBytesConfig, Qwen3VLForConditionalGeneration

    if torch.version.cuda != config["versions"]["cuda"] or torch.cuda.device_count() != 1:
        raise ValueError("CUDA version or visible-device count differs")
    torch.manual_seed(config["seed"])
    fraction = min(1.0, config["torch_allocator_cap_gib"] * 1024**3 / torch.cuda.get_device_properties(0).total_memory)
    torch.cuda.set_per_process_memory_fraction(fraction, 0)
    quant = dict(config["quantization"])
    quant["bnb_4bit_compute_dtype"] = torch.bfloat16
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model, local_files_only=True, torch_dtype=torch.bfloat16, device_map={"": 0},
        quantization_config=BitsAndBytesConfig(**quant)).eval()
    processor = AutoProcessor.from_pretrained(args.model, local_files_only=True)
    for uid in ordered:
        reserve = max(180, benchmark_p95 * 1.5 + 30) if benchmark_p95 else 240
        if time.monotonic() + reserve >= deadline:
            break
        if uid in prior:
            continue
        row = entries[uid]
        started = time.monotonic()
        raw, author_decoded, generated_tokens, visual_tokens = "", "", 0, 0
        token_ids = []
        attempts = []
        status, parsed = "FAILED", parse("")
        parsed["parse_status"] = "GENERATION_FAILED"
        for attempt in range(2):
            try:
                with Image.open(row["image_local_path"]) as image:
                    rgb = image.convert("RGB")
                messages = [
                    {"role": "system", "content": prompt["system_prompt"]},
                    {"role": "user", "content": [{"type": "image"}, {"type": "text",
                     "text": prompt["user_wrapper"].format(text=row["text"])}]},
                ]
                text = processor.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
                inputs = processor(text=[text], images=[rgb], return_tensors="pt").to("cuda:0")
                visual_tokens = int((inputs.input_ids == model.config.image_token_id).sum().item())
                with torch.inference_mode():
                    ids = model.generate(**inputs, max_new_tokens=1024, do_sample=False)
                new_ids = ids[0][inputs.input_ids.shape[1]:]
                token_ids = new_ids.tolist()
                generated_tokens = len(token_ids)
                raw = processor.decode(new_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
                author_decoded = processor.decode(new_ids, skip_special_tokens=True)
                parsed = parse(raw)
                eos = model.generation_config.eos_token_id
                eos = eos if isinstance(eos, list) else [eos]
                if generated_tokens == 1024 and token_ids[-1] not in eos:
                    parsed.update(parse_status="TRUNCATED", parsed_verdict="INVALID")
                status = "GENERATED"
                break
            except torch.cuda.OutOfMemoryError as exc:
                attempts.append({"attempt": attempt+1, "error": str(exc)})
                if "inputs" in locals():
                    del inputs
                torch.cuda.empty_cache()
            except Exception as exc:
                attempts.append({"attempt": attempt+1, "error": repr(exc)})
                break
        prior[uid] = dict(run_id=args.run_id, identity=identity, sample_uid=uid, pair_id=row["pair_id"],
                          side=row["side"], gt=row["ground_truth"], status=status, raw_output=raw,
                          author_decoded=author_decoded, model_sha=config["model_revision"],
                          prompt_sha=config["system_prompt_sha256"], parser_sha=config["parser_sha256"],
                          elapsed=time.monotonic()-started, generated_tokens=generated_tokens,
                          generated_token_ids=token_ids,
                          image_sha=row["image_sha256"], visual_tokens=visual_tokens,
                          image_pixels=int(row["image_width"])*int(row["image_height"]),
                          attempts=attempts, torch_peak_allocated_mib=torch.cuda.max_memory_allocated()/1024**2,
                          torch_peak_reserved_mib=torch.cuda.max_memory_reserved()/1024**2, **parsed)
        journal(journal_path, prior)
        print(f"{args.stage} {len(prior)}/{len(ordered)} {uid} {status} "
              f"{prior[uid]['elapsed']:.2f}s", flush=True)
    telemetry = [json.loads(line) for line in (out / "gpu_samples.jsonl").read_text().splitlines()]
    observed_peaks = {
        field: max((r[field] for r in telemetry if r.get(field) is not None), default=None)
        for field in ("used_mib", "process_mib")
    }
    summary = summarize(prior, args.stage, observed_peaks)
    summary.update(end_utc=now(), job_wall_seconds=time.monotonic()-start, identity=identity,
                   resource_gate=len(prior) == len(ordered) and summary["generated_count"] == len(ordered)
                   and observed_peaks["process_mib"] is not None and max(observed_peaks.values()) < 20*1024)
    write(out / "summary.json", summary)
    if args.stage == "validation" and len(prior) == len(ordered):
        blind = [{"review_id": hashlib.sha256((str(config["seed"]) + uid).encode()).hexdigest()[:16],
                  "raw_output": prior[uid]["raw_output"]} for uid in sorted(
                      prior, key=lambda key: hashlib.sha256(key.encode()).digest())]
        write(out / "raw_only_review.json", blind)
    return 0 if summary["resource_gate"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
