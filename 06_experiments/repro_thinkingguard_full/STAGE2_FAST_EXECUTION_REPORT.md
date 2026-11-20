# ThinkingGuard Stage 2 fast execution report

Updated 2026-11-20T17:04:44.794729+00:00. This checkpoint records actual completed work through the frozen A1 independent validation. D0 Smoke is complete and Direct Pilot is running.

| Milestone | State | Evidence |
|---|---|---|
| A0 original prompt | FAILED_PARSE_GATE, preserved | Stage 1 42 outputs; independent validation 20/36 parsed, 11 ambiguous templates and 5 extra text. |
| A1 repaired protocol | FAILED_PARSE_GATE | Development Smoke v1, v1b and v1c each generated 6/6, all 0/6 strict labels. Final v1c independent validation generated 36/36 with 0/36 labels and 35/36 complete structures. |
| A1 validation and Pilot | FAILED / NOT_RUN | Validation 36/36 raw predictions preserved, 0/36 parsed: 35 NONTERMINAL_VERDICT and 1 MULTIPLE_OVERALL. A1 Pilot remains 0/200 because 35/36 extraction gate failed. |
| D0 Direct | SMOKE_DONE / PILOT_RUNNING | Direct Smoke generated and parsed 6/6 in 316.18 s, process peak 8,330 MiB. Frozen Pilot 200/200 inputs are ready; inference has begun. |
| 300 pairs and full 868 | NOT_RUN | Full Test image coverage is 855/1736, with 881 missing or not yet verified at this checkpoint. |
| Training | NOT_FEASIBLE | SA-MCTS and DPO are outside this stage. |

A1 validation was sampled with seed 20261120 before checking image availability, excluding historical H1 36 pairs, A0 Smoke/Validation, and the Pilot 100 pairs. It contains 18 pairs, two per category; 13/36 images were ready at freeze and the remaining 23/36 were downloaded with the fixed dataset revision and official LFS SHA256 plus PIL verification. This validation is separate from A0 and Pilot. Human blind GT review is NOT_RUN.

The full Test download log currently records 81 successful fixed-revision fetches and 60 failed fetches across bounded windows. The per-file subprocess timeout is 30–45 seconds in the latest window; no download runs indefinitely. The manifest was not overwritten; inference refreshes only an in-memory view of verified image bytes. A0 and historical protection ledger contains 249 files, including model shards and 219 historical H1 files, with zero SHA256 changes at this checkpoint.

All 41 CPU tests pass. Initial A1 Smoke launches were safely refused when the chosen GPU became occupied. Subsequent A1 jobs completed on GPU 4. A1 v1b was interrupted after 3/6 samples by `OTHER_PROCESS_ON_SELECTED_GPU`; the same Run ID resumed the remaining 3 without regenerating saved rows. The final independent A1 validation took 2,344.64 s, with process peak 8,330 MiB and whole-card peak 8,339 MiB. Frozen-source raw-only replay matched all 36 saved parse decisions with zero mismatches and used no GT. A1 strict full-denominator Accuracy, Unsafe F1, nine-category macro Unsafe F1 and PairAcc are all 0 because all 36 predictions are INVALID; valid-only scores are undefined. This is a format failure, not a claim about underlying classification quality. D0 Smoke parsed 6/6; Direct Pilot metrics are pending its complete 200-row denominator.

The A1 protocol retains the fixed model and dataset, wrapper, safety categories, NF4/BF16, greedy decoding and 1,024-token cap. It repairs the terminal Overall verdict and is not the original author prompt. D0 is a prompt baseline with a 256-token cap, not a training ablation. The author result is not strictly comparable to this quantized hardware path.

## Resume commands

```bash
cd /home/ubuntu/data/project/thinkingguard-stage1/06_experiments/repro_thinkingguard_full
MODEL=/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3
PY=/home/ubuntu/data/project/h1-cf-killtest/.venv/bin/python
GPU_UUID=GPU-d72631b6-1716-61ed-d355-8da3e5558910  # recheck permission and idleness
PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=10s 19100s "$PY" -u scripts/stage2_inference.py --protocol a1 --stage smoke --model "$MODEL" --gpu-uuid "$GPU_UUID" --run-id a1_smoke_v1c_20261120 --resume
PYTHONDONTWRITEBYTECODE=1 timeout --kill-after=10s 19100s "$PY" -u scripts/stage2_inference.py --protocol a1 --stage validation --model "$MODEL" --gpu-uuid "$GPU_UUID" --run-id a1_validation_v1c_20261120 --resume
# After 35/36 validation extraction, run A1 Pilot with --stage pilot and a new run ID.
# D0 can run its own Smoke and Pilot even if A1 validation fails.
HF_HUB_DISABLE_XET=1 HF_HUB_DOWNLOAD_TIMEOUT=15 timeout --kill-after=5s 1800s "$PY" -u scripts/stage2_download.py --scope full --max-files 120
```

Every GPU job has the internal 19,000-second hard wall, external 19,100-second timeout, 20 GiB observed cap, 18 GiB CUDA allocator cap, host-PID binding challenge, and per-sample fsync journal. Rerun a partial run with the same ID and `--resume`; the runner rejects mixed identities.
