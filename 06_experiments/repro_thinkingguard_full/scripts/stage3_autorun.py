"""Boundedly wait for one previously permitted idle GPU and resume a frozen batch."""
import argparse
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

from recovery_gates import active_processes, require_idle
from stage2_inference import ROOT, card, gpu_rows

KNOWN_PERMITTED = (
    "GPU-45decdd6-682b-4cd9-2bc3-6769eee7a81f",
    "GPU-d72631b6-1716-61ed-d355-8da3e5558910",
    "GPU-5a0ba87d-2dc2-fed4-276c-8bb93dcec495",
)


def now():
    return datetime.now(timezone.utc).isoformat()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--protocol", choices=("d0",), required=True)
    ap.add_argument("--start-pair", type=int, required=True)
    ap.add_argument("--slice-pairs", type=int, required=True)
    ap.add_argument("--batch-queue", type=Path, required=True)
    ap.add_argument("--run-id", required=True)
    ap.add_argument("--model", type=Path, required=True)
    ap.add_argument("--max-wait-seconds", type=int, default=7200)
    ap.add_argument("--max-attempts", type=int, default=5)
    args = ap.parse_args()
    deadline = time.monotonic() + args.max_wait_seconds
    event_path = ROOT / "runs" / f"{args.run_id}_launcher.jsonl"
    attempt = 0
    while time.monotonic() < deadline and attempt < args.max_attempts:
        selected = None
        for uuid in KNOWN_PERMITTED:
            try:
                require_idle(uuid, card, lambda: active_processes(uuid, gpu_rows))
                selected = uuid
                break
            except (ValueError, OSError, subprocess.SubprocessError):
                continue
        if selected is None:
            time.sleep(30)
            continue
        attempt += 1
        command = [sys.executable, "-u", str(ROOT / "scripts/stage2_inference.py"),
            "--protocol", args.protocol, "--stage", "batch", "--batch-start-pair",
            str(args.start_pair), "--batch-pairs", str(args.slice_pairs),
            "--batch-queue", str(args.batch_queue), "--model", str(args.model),
            "--gpu-uuid", selected, "--run-id", args.run_id, "--resume"]
        log_path = ROOT / ".local" / f"{args.run_id}_attempt{attempt}.log"
        event = {"attempt": attempt, "start_utc": now(), "gpu_uuid": selected,
                 "run_id": args.run_id, "command": command}
        with log_path.open("w") as log:
            try:
                completed = subprocess.run(command, cwd=ROOT, stdout=log,
                    stderr=subprocess.STDOUT, env={**os.environ, "PYTHONDONTWRITEBYTECODE": "1"},
                    timeout=19100)
                event["exit_code"] = completed.returncode
            except subprocess.TimeoutExpired:
                event["exit_code"] = 124
        event["end_utc"] = now()
        event["log_path"] = str(log_path)
        with event_path.open("a") as f:
            f.write(json.dumps(event) + "\n")
            f.flush()
            os.fsync(f.fileno())
        print(json.dumps(event), flush=True)
        if event["exit_code"] == 0:
            return 0
        time.sleep(30)
    return 3


if __name__ == "__main__":
    raise SystemExit(main())
