# ThinkingGuard Stage 2 fast execution report

Status on 2026-11-21: **D0 Direct Pilot100 DONE; A1 repaired five-stage validation FAILED_PARSE_GATE; A1 Pilot, cumulative 300 and full 868 NOT_RUN.** A0 original 42 predictions and all historical H1 evidence remain byte unchanged.

## Protocol milestones

| Protocol / phase | Status | Actual output and gate |
|---|---|---|
| A0 author prompt | FAILED_PARSE_GATE, preserved | Stage 1 had 42 raw outputs. Its independent 36 generated, 20 parsed, 11 ambiguous templates, 5 extra text. No A0 rerun or parser change. |
| A1 development Smoke v1 | DONE, format failed | 6/6 generated, 0/6 strict terminal-line parses; 5 verdicts inline, 1 after the Overall marker. |
| A1 development Smoke v1b | DONE, format failed | 6/6 generated, 0/6 parsed. Interrupted after 3 by another process on the selected GPU, then resumed without repeating rows. Both development source snapshots are archived. |
| A1 final development Smoke v1c | DONE, format failed | 6/6 generated, 0/6 parsed. Prompt, parser, queue and chat render hashes were frozen before independent validation. |
| A1 independent validation | FAILED_PARSE_GATE | 36/36 generated on 18 new pairs, nine categories × two pairs. Only 0/36 parsed, below the 35/36 threshold. Structure complete 35/36; 35 `NONTERMINAL_VERDICT`, 1 `MULTIPLE_OVERALL`. Raw-only frozen parser replay had zero mismatches. |
| A1 Pilot100 | NOT_RUN | A1 validation gate failed. No A1 Pilot, 300-pair or 868-pair score is claimed. |
| D0 Direct Smoke | DONE | 6/6 generated and parsed; 316.18 s job wall time. |
| D0 Direct Pilot100 | DONE | Same frozen 100 pairs and 200 images, 200/200 generated, 200/200 parsed, 0 INVALID. Raw-only frozen parser replay had zero mismatches. |
| Cumulative 300 / full 868 | BLOCKED | A1 parse gate failed. Current image coverage is 985/1736 and 463/868 complete pairs. First frozen 300 pairs have 514/600 images and 243 complete pairs ready. No 300/868 inference was run. |
| SA-MCTS / DPO | NOT_FEASIBLE | Training remains outside this stage; D0 is a prompt baseline, not a training ablation. |

A1 validation was sampled by seed 20261120 before checking image availability, excluding historical H1 36 pairs, A0 Smoke/Validation, all A1 development samples and the Pilot100. Thirteen validation images were ready at freeze; the remaining 23 were fetched from the fixed revision and verified against official LFS SHA256 and PIL decoding. The 36-item list was not changed based on labels or predictions. Human blind GT review is `NOT_RUN`. The A1 final parser was not adjusted after independent validation.

## D0 Direct Pilot100 result

D0 uses the same ThinkingGuard-8B revision, TriggerBench revision, image/text wrapper and nine safety definitions. It directly requests one verdict with a 256-token cap; A1 uses five stages and a 1,024-token cap. These are different protocols. Strict full-denominator and valid-only figures are identical because all 200 predictions are valid.

| Metric | Strict / valid-only |
|---|---:|
| Accuracy | 71.50% (143/200) |
| Unsafe precision | 71.72% |
| Unsafe recall | 71.00% |
| Unsafe F1, micro | 0.7136 |
| Safe FPR | 28.00% |
| Unsafe FNR | 29.00% |
| PairAcc / forward flip | 47.00% (47/100) |
| Reverse flip | 4/100 |
| Both Safe / both Unsafe | 25/100 / 24/100 |
| INVALID / missing prediction | 0/200 / 0/200 |
| Nine-category macro Unsafe F1 / recall | 0.6959 / 0.7113 |

Confusion counts are TP 71, TN 72, FP 28, FN 29. Wilson 95% intervals are accuracy 64.88–77.30% and PairAcc 37.51–56.71%. Stratified pair bootstrap (2,000 resamples) gives Unsafe F1 0.6564–0.7614 and PairAcc 0.38–0.55. The [metrics JSON](runs/d0_pilot100_20261120/metrics.json) contains both denominator conventions, per-category n_total/n_valid/n_correct and Wilson intervals, all four pair quadrants, and all 57 misclassified sample IDs. The 57 are valid model decisions rather than parsing failures.

| Risk category | Samples | Unsafe F1 | Unsafe recall |
|---|---:|---:|---:|
| Ethical violations | 24 | 0.667 | 0.583 |
| Illegal activities | 22 | 0.727 | 0.727 |
| Misinformation | 22 | 0.909 | 0.909 |
| Offensiveness | 22 | 0.632 | 0.545 |
| Physical harm | 22 | 0.720 | 0.818 |
| Privacy | 22 | 0.267 | 0.182 |
| Property damage | 22 | 0.714 | 0.909 |
| Regional & belief | 22 | 0.842 | 0.727 |
| Violence | 22 | 0.786 | 1.000 |

## Resource and provenance accounting

D0 Pilot used one RTX 4090 D at a time. The first job generated 35 rows and the monitor aborted on `OTHER_PROCESS_ON_SELECTED_GPU` after at least 1,678.06 s. The second job resumed the same journal and generated the remaining 165 in 7,260.51 s; measured cumulative GPU wall is **at least 8,938.57 s (2.483 h)**, with 8,853.80 s summed per-sample elapsed. Each job was below six hours. The sampled process peak was 8,330 MiB, whole-card peak 8,339 MiB, and PyTorch allocated/reserved peaks are in the raw summary. All 200 rows retain generated token IDs, raw output, prompt/parser/source identity, image SHA, elapsed time, and attempts. The full GPU sample stream is archived losslessly as `runs/d0_pilot100_20261120/gpu_samples.jsonl.gz`; its decompressed SHA256 is in resource accounting. Pilot sample latency P50/P95 was 44.22/48.45 s. [Resource accounting](runs/d0_pilot100_20261120/resource_accounting.json) distinguishes the interrupted and completed jobs.

A1 independent validation took 2,344.64 s with process/card peaks 8,330/8,339 MiB. A1 v1 and v1c development jobs took 436.61 and 448.12 s; v1b used an interrupted job plus a 284.27 s resume. D0 Smoke took 316.18 s. Logs record host PID binding and the reversible 64 MiB challenge. No other user process was terminated.

All 41 CPU tests pass. The current full Test inventory independently rechecked all 1,736 published SHA references and local bytes: **985 READY images, 751 MISSING, 463 READY pairs, 405 pairs with at least one missing image**. Per-category and per-pair status and the last bounded download failure are in [image status](artifacts/stage2_full_image_status.json) and [pair status](artifacts/stage2_test_pair_status.csv). The older Stage 1 manifest and all H1 raw predictions were not overwritten. The before/after protection ledger covers 249 files, including 219 historical H1 files, Stage 1 A0 raw evidence and local model shards, with zero SHA256 changes.

The published author result cannot be directly compared with this Pilot: D0 omits five-stage reasoning and uses a shorter token cap, while this reproduction uses local NF4/BF16 compute on an RTX 4090 D rather than the author BF16 setup. A1 is a repaired output protocol and failed its own parse gate; no author five-stage Test score was reproduced.

## Resume and verification commands

```bash
cd /home/ubuntu/data/project/thinkingguard-stage1/06_experiments/repro_thinkingguard_full
PY=/home/ubuntu/data/project/h1-cf-killtest/.venv/bin/python
MODEL=/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3
# This completed run exits without regenerating any sample:
PYTHONDONTWRITEBYTECODE=1 "$PY" scripts/stage2_inference.py --protocol d0 --stage pilot --model "$MODEL" --gpu-uuid GPU-d72631b6-1716-61ed-d355-8da3e5558910 --run-id d0_pilot100_20261120 --resume
PYTHONDONTWRITEBYTECODE=1 python scripts/stage2_replay_parser.py --protocol d0 --predictions runs/d0_pilot100_20261120/predictions.jsonl --output runs/d0_pilot100_20261120/parse_replay.json
PYTHONDONTWRITEBYTECODE=1 python scripts/stage2_evaluate.py runs/d0_pilot100_20261120/predictions.jsonl runs/d0_pilot100_20261120/metrics.json --protocol d0 --stage pilot
# Bounded image recovery; rerun inventory after each window:
HF_HUB_DISABLE_XET=1 HF_HUB_DOWNLOAD_TIMEOUT=15 timeout --kill-after=5s 900s "$PY" -u scripts/stage2_download.py --scope full --max-files 60 --per-file-seconds 30
timeout --kill-after=5s 640s "$PY" -u scripts/stage2_curl_fallback.py --max-files 80 --max-seconds 600
PYTHONDONTWRITEBYTECODE=1 "$PY" scripts/stage2_inventory.py
```

A1 Pilot and expansion must remain gated. A new A2 or other repaired protocol would need a separate prompt, parser and unseen validation set before a new Pilot; the failed A1 verification is not reusable as a pass.
