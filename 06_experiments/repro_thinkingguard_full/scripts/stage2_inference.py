"""Run frozen Stage 2 protocols with a resumable atomic journal."""
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

from a1_parser_v1 import parse as parse_a1
from d0_parser_v1 import parse as parse_d0
from build_test_manifest import verify_image
from recovery_gates import (
    active_processes, bind_pid, prior_summary, queue_hash, queue_ready, registry_key,
    require_idle, run_id_valid,
)

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


def audit_resource(uuid, pid, cap_mib, deadline, log_path, stop, job_id):
    with log_path.open("a", buffering=1) as log:
        while not stop.is_set() and time.monotonic() < deadline:
            row = {"utc": now(), "pid": pid, "job_id": job_id}
            fatal = None
            try:
                row.update(card(uuid))
                processes = active_processes(uuid, gpu_rows)
                row["process_mib"] = processes.get(pid)
                if set(processes) - {pid}:
                    fatal = "OTHER_PROCESS_ON_SELECTED_GPU"
                elif row["process_mib"] is None:
                    fatal = "PROCESS_MEMORY_LOST"
                elif max(row["used_mib"], row["process_mib"]) >= cap_mib:
                    fatal = "MEMORY_LIMIT"
            except (subprocess.SubprocessError, OSError, ValueError) as exc:
                fatal = f"TELEMETRY_UNAVAILABLE: {exc}"
            if fatal:
                row["abort"] = fatal
            log.write(json.dumps(row) + "\n")
            if fatal:
                os.fsync(log.fileno())
                os._exit(71)
            stop.wait(1)
        if not stop.is_set():
            log.write(json.dumps({"utc": now(), "abort": "HARD_WALL_LIMIT", "job_id": job_id}) + "\n")
            os.fsync(log.fileno())
            os._exit(72)


def prerequisite_base(base, registry, stage, input_sha, compatibility):
    if registry_key(base, stage, input_sha) in registry or stage != "smoke":
        return base
    # Preserve one already measured Smoke across the reviewed CLI lookup fix.
    if compatibility.get("new_runner_sha256") != base["runner_sha256"]:
        return base
    previous = dict(base, runner_sha256=compatibility["old_runner_sha256"])
    record = registry.get(registry_key(previous, stage, input_sha), {})
    return previous if record.get("summary_sha256") == compatibility["smoke_summary_sha256"] else base


def verify_local(row):
    path = Path(row["image_local_path"])
    return path.is_file() and sha(path) == row["expected_image_sha256"]


def register_summary(runs, base, stage, summary_path, identity):
    path = runs / "stage_registry.json"
    with (runs / ".stage_registry.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        registry = read(path) if path.exists() else {}
        key = registry_key(base, stage, identity["inputs_sha256"])
        registry[key] = {"run_id": identity["run_id"], "summary_sha256": sha(summary_path)}
        write(path, registry)



def register_stage2_summary(runs, base, stage, summary_path, identity):
    path = runs / "stage2_registry.json"
    with (runs / ".stage2_registry.lock").open("a") as lock:
        fcntl.flock(lock, fcntl.LOCK_EX)
        registry = read(path) if path.exists() else {}
        registry[registry_key(base, stage, identity["inputs_sha256"])] = {
            "run_id": identity["run_id"], "summary_sha256": sha(summary_path)}
        write(path, registry)


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
    cli.add_argument("--protocol", choices=("a1", "d0"), required=True)
    cli.add_argument("--stage", choices=("smoke", "validation", "pilot"), required=True)
    cli.add_argument("--model", type=Path, required=True)
    cli.add_argument("--gpu-uuid")
    cli.add_argument("--run-id")
    cli.add_argument("--resume", action="store_true")
    cli.add_argument("--dry-run", action="store_true")
    cli.add_argument("--preflight-only", action="store_true")
    args = cli.parse_args()

    settings_path = ROOT / f"configs/{args.protocol}_stage2_nf4_v1.json"
    prompt_path = ROOT / ("configs/a1_five_step_single_verdict_v1.json" if args.protocol == "a1" else "configs/d0_direct_v1.json")
    parser_path = Path(__file__).with_name("a1_parser_v1.py" if args.protocol == "a1" else "d0_parser_v1.py")
    queue_path = ROOT / "artifacts/stage2_queues_v1.json"
    freeze_path = ROOT / f"artifacts/{args.protocol}_protocol_freeze.json"
    manifest = ROOT / "artifacts/manifests/test_manifest.csv"
    freeze, config, prompt, queues = map(read, (freeze_path, settings_path, prompt_path, queue_path))
    model_audit = read(ROOT / "artifacts/model_cache_audit.json")
    with manifest.open() as handle:
        rows = list(csv.DictReader(handle))
    entries = {r["sample_uid"]: r for r in rows}
    with (ROOT / "artifacts/dataset_source_tree.csv").open() as handle:
        tree = {r["path"]: r["lfs_sha256"] for r in csv.DictReader(handle)}
    # Refresh only the in-memory row view from immutable, hash-verified image bytes.
    # The original Stage 1 manifest remains frozen.
    for row in rows:
        if row["run_status"] == "READY":
            continue
        path = ROOT / "images" / row["hf_image_path"]
        if path.is_file():
            image_sha, width, height = verify_image(path, row["expected_image_sha256"])
            row.update(image_local_path=str(path.resolve()), image_sha256=image_sha,
                       image_width=str(width), image_height=str(height),
                       image_decode_status="OK", run_status="READY",
                       image_hash_reference="HF_LFS_SHA256")
    ordered = queues["a1_smoke" if args.stage == "smoke" else "a1_validation" if args.stage == "validation" else "pilot"]
    stage_data = queue_ready(args.stage, entries, ordered, tree, config["dataset_revision"], verify_local)
    requirements = {
        "manifest": len(rows) == len(entries) == 1736 and sha(manifest) == freeze["manifest_sha256"],
        "data": stage_data["ready"],
        "official_tree": sha(ROOT / "artifacts/dataset_source_tree.csv") == freeze["source_tree_sha256"],
        "queues": sha(queue_path) == freeze["queue_sha256"] and not stage_data["invalid_queue"],
        "parser": sha(parser_path) == freeze["parser_sha256"] == config["parser_sha256"]
                  and sha(ROOT / f"tests/test_{args.protocol}_parser_v1.py") == freeze["tests_sha256"],
        "prompt": sha(prompt_path) == freeze["prompt_config_sha256"] == config["prompt_config_sha256"]
                  and hashlib.sha256(prompt["system_prompt"].encode()).hexdigest() == config["system_prompt_sha256"],
        "model": model_audit["status"] == "DONE" and args.model.name == config["model_revision"] == model_audit["revision"]
                 and sha(args.model / "model.safetensors.index.json") == model_audit["local_index_sha256"]
                 and all((args.model / filename).is_file() and sha(args.model / filename) == evidence["sha256"]
                         for filename, evidence in model_audit["processor_and_configs"].items()),
    }
    print(json.dumps(dict(stage=args.stage, queued=len(ordered), protocol=args.protocol,
                          preflight=requirements, stage_data=stage_data), indent=2), flush=True)
    if args.dry_run:
        return 0
    if not all(requirements.values()):
        return 2
    if args.preflight_only:
        return 0
    if not args.gpu_uuid or not run_id_valid(args.run_id):
        cli.error("A permitted GPU UUID and an alphanumeric run ID are required")

    identity_base = dict(protocol=args.protocol, prompt_sha256=sha(prompt_path), parser_sha256=sha(parser_path), config_sha256=sha(settings_path), source_tree_sha256=sha(ROOT / "artifacts/dataset_source_tree.csv"),
                         queues_sha256=sha(queue_path), model_audit_sha256=sha(ROOT / "artifacts/model_cache_audit.json"),
                         runner_sha256=sha(Path(__file__)), gates_sha256=sha(Path(__file__).with_name("recovery_gates.py")))
    identity = dict(**identity_base, inputs_sha256=queue_hash(entries, ordered), stage=args.stage, run_id=args.run_id)
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
        completed_summary = out / "summary.json"
        if completed_summary.exists():
            return 0 if read(completed_summary)["resource_gate"] else 3
        raise ValueError("Complete prediction journal is missing its terminal resource summary")
    benchmark_p95 = None
    required_stages = [] if args.stage == "smoke" else ["smoke"] if args.stage == "validation" or args.protocol == "d0" else ["smoke", "validation"]
    registry_path = ROOT / "runs/stage2_registry.json"
    registry = read(registry_path) if registry_path.exists() else {}
    for stage in required_stages:
        stage_order = queues["a1_smoke" if stage == "smoke" else "a1_validation"]
        input_sha = queue_hash(entries, stage_order)
        previous, summary = prior_summary(ROOT / "runs", registry, identity_base, stage, input_sha, read, sha)
        if stage == "validation":
            if summary["prediction_count"] != 36 or summary["extracted"] < 35:
                raise ValueError("Independent A1 parse coverage did not reach 35/36")
            benchmark_p95 = summary["latency_seconds"]["p95"]
    processes = lambda: active_processes(args.gpu_uuid, gpu_rows)
    require_idle(args.gpu_uuid, card, processes)
    for shard in model_audit["shards"]:
        if sha(args.model / shard["name"]) != shard["sha256"]:
            raise ValueError(f"Model weight changed: {shard['name']}")
    for package, version in config["versions"].items():
        if package not in ("python", "cuda") and importlib.metadata.version(package) != version:
            raise ValueError(f"Environment version mismatch: {package}")
    if ".".join(map(str, sys.version_info[:3])) != config["versions"]["python"]:
        raise ValueError("Python version mismatch")
    initial = require_idle(args.gpu_uuid, card, processes)
    if not identity_path.exists():
        write(identity_path, identity)
    job_id = str(time.time_ns())
    write(out / f"job-{job_id}.json", dict(
        start_utc=now(), argv=sys.argv, gid=initial, manifest_sha256=sha(manifest), git=subprocess.check_output(
            ["git", "-C", str(ROOT), "rev-parse", "HEAD"], text=True).strip(), identity=identity))
    os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu_uuid
    os.environ["HF_HUB_OFFLINE"] = "1"

    start = time.monotonic()
    deadline = start + config["max_wall_seconds"]
    import torch
    from PIL import Image
    from transformers import AutoProcessor, BitsAndBytesConfig, Qwen3VLForConditionalGeneration

    if torch.version.cuda != config["versions"]["cuda"] or torch.cuda.device_count() != 1:
        raise ValueError("CUDA version or visible-device count differs")
    require_idle(args.gpu_uuid, card, processes)
    torch.cuda.init()
    torch.manual_seed(config["seed"])
    fraction = min(1.0, config["torch_allocator_cap_gib"] * 1024**3 / torch.cuda.get_device_properties(0).total_memory)
    torch.cuda.set_per_process_memory_fraction(fraction, 0)
    cap_mib = config["memory_cap_gib"] * 1024

    def verify_card(used):
        if max(used, card(args.gpu_uuid)["used_mib"]) >= cap_mib:
            raise ValueError("GPU ownership challenge exceeded budget")

    def allocate():
        probe = torch.empty(64 * 1024 * 1024, dtype=torch.uint8, device="cuda:0")
        torch.cuda.synchronize()
        return probe

    def release():
        torch.cuda.empty_cache()
        torch.cuda.synchronize()

    ns = next((line.split()[1:] for line in Path("/proc/self/status").read_text().splitlines()
               if line.startswith("NSpid:")), [])
    try:
        binding = bind_pid(processes, allocate, release, {os.getpid(), *map(int, ns)}, verify_card)
    except (ValueError, OSError, subprocess.SubprocessError) as exc:
        write(out / f"gpu-binding-{job_id}.json", {"status": "BLOCKED", "reason": str(exc)})
        raise
    write(out / f"gpu-binding-{job_id}.json", dict(**binding, status="DONE", gpu_uuid=args.gpu_uuid))
    monitor_stop = threading.Event()
    thread = threading.Thread(target=audit_resource,
                              args=(args.gpu_uuid, binding["host_pid"], cap_mib, deadline,
                                    out / "gpu_samples.jsonl", monitor_stop, job_id), daemon=True)
    thread.start()
    quant = dict(config["quantization"])
    quant["bnb_4bit_compute_dtype"] = torch.bfloat16
    model = Qwen3VLForConditionalGeneration.from_pretrained(
        args.model, local_files_only=True, torch_dtype=torch.bfloat16, device_map={"": 0},
        quantization_config=BitsAndBytesConfig(**quant)).eval()
    processor = AutoProcessor.from_pretrained(args.model, local_files_only=True)
    parser = parse_a1 if args.protocol == "a1" else parse_d0
    for uid in ordered:
        reserve = max(180, benchmark_p95 * 1.5 + 30) if benchmark_p95 else 240
        if time.monotonic() + reserve >= deadline:
            break
        if uid in prior:
            continue
        row = entries[uid]
        started = time.monotonic()
        raw, author_decoded, generated_tokens, visual_tokens = "", "", 0, 0
        chat_render_sha = None
        token_ids = []
        attempts = []
        status, parsed = "FAILED", parser("")
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
                chat_render_sha = hashlib.sha256(text.encode()).hexdigest()
                inputs = processor(text=[text], images=[rgb], return_tensors="pt").to("cuda:0")
                visual_tokens = int((inputs.input_ids == model.config.image_token_id).sum().item())
                with torch.inference_mode():
                    ids = model.generate(**inputs, max_new_tokens=config["max_new_tokens"], do_sample=False)
                new_ids = ids[0][inputs.input_ids.shape[1]:]
                token_ids = new_ids.tolist()
                generated_tokens = len(token_ids)
                raw = processor.decode(new_ids, skip_special_tokens=False, clean_up_tokenization_spaces=False)
                author_decoded = processor.decode(new_ids, skip_special_tokens=True)
                parsed = parser(raw)
                eos = model.generation_config.eos_token_id
                eos = eos if isinstance(eos, list) else [eos]
                if generated_tokens == config["max_new_tokens"] and token_ids[-1] not in eos:
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
                          chat_render_sha256=chat_render_sha,
                          elapsed=time.monotonic()-started, generated_tokens=generated_tokens,
                          generated_token_ids=token_ids,
                          image_sha=row["image_sha256"], visual_tokens=visual_tokens,
                          image_pixels=int(row["image_width"])*int(row["image_height"]),
                          attempts=attempts, torch_peak_allocated_mib=torch.cuda.max_memory_allocated()/1024**2,
                          torch_peak_reserved_mib=torch.cuda.max_memory_reserved()/1024**2, **parsed)
        journal(journal_path, prior)
        print(f"{args.stage} {len(prior)}/{len(ordered)} {uid} {status} "
              f"{prior[uid]['elapsed']:.2f}s", flush=True)
    monitor_stop.set()
    thread.join()
    telemetry = [json.loads(line) for line in (out / "gpu_samples.jsonl").read_text().splitlines()]
    observed_peaks = {
        field: max((r[field] for r in telemetry if r.get(field) is not None), default=None)
        for field in ("used_mib", "process_mib")
    }
    summary = summarize(prior, args.stage, observed_peaks) if args.protocol == "a1" else dict(
        prediction_count=len(prior), generated_count=sum(r["status"] == "GENERATED" for r in prior.values()),
        extracted=sum(r["parsed_verdict"] in ("Safe", "Unsafe") for r in prior.values()),
        coverage=sum(r["parsed_verdict"] in ("Safe", "Unsafe") for r in prior.values())/len(prior) if prior else None,
        structure_complete=sum(r["structure_complete"] for r in prior.values()),
        latency_seconds={f"p{q}": percentile([r["elapsed"] for r in prior.values()], q/100) for q in (50,90,95)},
        independent_human_review="NOT_RUN", gpu_sample_peaks_mib=observed_peaks)
    summary.update(end_utc=now(), job_wall_seconds=time.monotonic()-start, identity=identity,
                   parse_gate=("PASS" if summary["extracted"] >= 35 else "FAILED_PARSE_GATE")
                              if args.stage == "validation" and len(prior) == len(ordered) else "NOT_EVALUATED",
                   torch_peak_allocated_mib=max(r["torch_peak_allocated_mib"] for r in prior.values()) if prior else None,
                   torch_peak_reserved_mib=max(r["torch_peak_reserved_mib"] for r in prior.values()) if prior else None,
                   resource_gate=len(prior) == len(ordered) and summary["generated_count"] == len(ordered)
                   and observed_peaks["process_mib"] is not None and max(observed_peaks.values()) < 20*1024)
    write(out / "summary.json", summary)
    if args.protocol == "a1" and args.stage == "validation" and len(prior) == len(ordered):
        blind = [{"review_id": hashlib.sha256((str(config["seed"]) + uid).encode()).hexdigest()[:16],
                  "raw_output": prior[uid]["raw_output"]} for uid in sorted(
                      prior, key=lambda key: hashlib.sha256(key.encode()).digest())]
        write(out / "raw_only_review.json", blind)
    if summary["resource_gate"] and args.stage in ("smoke", "validation"):
        register_stage2_summary(ROOT / "runs", identity_base, args.stage, out / "summary.json", identity)
    return 0 if summary["resource_gate"] else 3


if __name__ == "__main__":
    raise SystemExit(main())
