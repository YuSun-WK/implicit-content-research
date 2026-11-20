# ThinkingGuard Stage 2 fast execution report

Updated 2026-11-20T06:31:47.645136+00:00. This checkpoint records actual completed work; no Stage 2 GPU prediction has been generated yet.

| Milestone | State | Evidence |
|---|---|---|
| A0 original prompt | FAILED_PARSE_GATE, preserved | Stage 1 42 outputs; independent validation 20/36 parsed, 11 ambiguous templates and 5 extra text. |
| A1 repaired protocol | CPU_READY, GPU_BLOCKED | Independent parser and prompt frozen. Smoke 6, new validation 36 (nine categories, two pairs each), Pilot 200 are preflight ready. A1 Smoke GPU launch refused an occupied card before loading. |
| A1 validation and Pilot | NOT_RUN | 0/36 and 0/200 Stage 2 predictions. A1 Pilot requires 35/36 validation extraction. |
| D0 Direct | CPU_READY, GPU_BLOCKED | Independent prompt/parser frozen; 200/200 Pilot image inputs preflight ready. Direct Smoke and Pilot not run. |
| 300 pairs and full 868 | NOT_RUN | Full Test image coverage is 830/1736, with 906 missing or not yet verified. |
| Training | NOT_FEASIBLE | SA-MCTS and DPO are outside this stage. |

A1 validation was sampled with seed 20261120 before checking image availability, excluding historical H1 36 pairs, A0 Smoke/Validation, and the Pilot 100 pairs. It contains 18 pairs, two per category; 13/36 images were ready at freeze and the remaining 23/36 were downloaded with the fixed dataset revision and official LFS SHA256 plus PIL verification. This validation is separate from A0 and Pilot. Human blind GT review is NOT_RUN.

The full Test download log currently records 56 successful fixed-revision fetches and 3 failed fetches in the current window. The manifest was not overwritten; inference refreshes only an in-memory view of verified image bytes. A0 and historical protection ledger contains 249 files, including model shards and 219 historical H1 files, with zero SHA256 changes at this checkpoint.

All 40 CPU tests pass. The A1 Smoke launch preflight reported manifest/data/tree/queues/parser/prompt/model all true. The selected GPU acquired another user's process before allocation; `require_idle` stopped the job. `runs/stage2_gpu_blocked.json` records the GPU snapshot. Actual Stage 2 GPU hours, peak VRAM, A1/D0 parse rates, category F1, PairAcc, and Pilot scores are NOT_RUN; no result values are inferred from Stage 1.

The A1 protocol retains the fixed model and dataset, wrapper, safety categories, NF4/BF16, greedy decoding and 1,024-token cap. It repairs the terminal Overall verdict and is not the original author prompt. D0 is a prompt baseline with a 256-token cap, not a training ablation. The author result is not strictly comparable to this quantized hardware path.

## Resume commands

```bash
cd /home/ubuntu/data/project/thinkingguard-stage1/06_experiments/repro_thinkingguard_full
MODEL=/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3
PY=/home/ubuntu/data/project/h1-cf-killtest/.venv/bin/python
GPU_UUID=GPU-d72631b6-1716-61ed-d355-8da3e5558910  # recheck permission and idleness
PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=10s 19100s "$PY" -u scripts/stage2_inference.py --protocol a1 --stage smoke --model "$MODEL" --gpu-uuid "$GPU_UUID" --run-id a1_smoke_20261120 --resume
PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=10s 19100s "$PY" -u scripts/stage2_inference.py --protocol a1 --stage validation --model "$MODEL" --gpu-uuid "$GPU_UUID" --run-id a1_validation_20261120
# After 35/36 validation extraction, run A1 Pilot with --stage pilot and a new run ID.
# D0 can run its own Smoke and Pilot even if A1 validation fails.
HF_HUB_DISABLE_XET=1 HF_HUB_DOWNLOAD_TIMEOUT=15 timeout --kill-after=5s 1800s "$PY" -u scripts/stage2_download.py --scope full --max-files 120
```

Every GPU job has the internal 19,000-second hard wall, external 19,100-second timeout, 20 GiB observed cap, 18 GiB CUDA allocator cap, host-PID binding challenge, and per-sample fsync journal. Rerun a partial run with the same ID and `--resume`; the runner rejects mixed identities.
