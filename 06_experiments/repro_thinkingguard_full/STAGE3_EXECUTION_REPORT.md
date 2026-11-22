# ThinkingGuard Stage 3 execution report — D0 300-pair milestone

Protocol D0 is the frozen **Direct Prompt baseline**, not the author’s five-stage ThinkingGuard inference. Its 256-token budget differs from A1v2’s 1024-token budget; any comparison cannot isolate reasoning alone. All 300 pairs follow the fixed expansion queue, including old H1/A1 sample IDs newly inferred with the D0 prompt. No prior H1/A0/A1 prediction enters D0 metrics.

## Status

| Stage | Status | Evidence |
|---|---|---|
| D0 Pilot100 | DONE | 100 pairs / 200 predictions, unchanged from Stage 2 |
| D0 cumulative300 | DONE | 300 pairs / 600 predictions; 600 parsed; zero INVALID or MISSING |
| D0 cumulative868 | PARTIAL | 300/868 pairs predicted; fixed denominator retains 1,136 MISSING rows |
| D0 next 300–399 slice | IN_PROGRESS | frozen ready queue has 86 pairs; independent run in progress |
| A1v2 Smoke / independent validation / Pilot | NOT_RUN | separate prompt/parser/queue/config/freeze prepared; validation images downloaded, GPU priority remains D0 |
| SA-MCTS / DPO training | NOT_RUN | CPU evidence audit only; public search/reward/training implementation unavailable |

## D0 300 pairs: fixed full denominator

| Measure | Strict full denominator | Valid only |
|---|---:|---:|
| Accuracy | 0.7217 | 0.7217 |
| Unsafe F1 | 0.7106 | 0.7106 |
| Unsafe recall | 0.6833 | 0.6833 |
| Safe FPR | 0.2400 | 0.2400 |
| Unsafe FNR | 0.3167 | 0.3167 |
| PairAcc | 0.4733 | 0.4733 |
| Label coverage | 1.0000 | 1.0000 |
| Rows scored / valid | 600 / 600 | 600 / 600 |

Accuracy 433/600; PairAcc 142/300. Quadrants: correct safe→unsafe 142, reversed 9, both Safe 86, both Unsafe 63, invalid pair 0. Confusion: {'tp': 205, 'tn': 228, 'fp': 72, 'fn': 95}. Strict and valid-only coincide because all 600 labels parsed. Wilson95 accuracy [0.684481853273717, 0.7560311259435425]; PairAcc [0.4175289979894728, 0.5298119604758365]. Pair-cluster bootstrap95 is preserved in the cumulative JSON.

Nine-category macro Unsafe F1 0.7085; macro Unsafe Recall 0.6844.

| Risk category | Pairs | Accuracy | Unsafe F1 | Unsafe recall | PairAcc |
|---|---:|---:|---:|---:|---:|
| ethical_violations | 35 | 0.6857 | 0.6207 | 0.5143 | 0.4000 |
| illegal_activities | 34 | 0.7647 | 0.7500 | 0.7059 | 0.5882 |
| misinformation | 33 | 0.8636 | 0.8525 | 0.7879 | 0.7273 |
| offensiveness | 33 | 0.6970 | 0.6667 | 0.6061 | 0.4242 |
| physical_harm | 33 | 0.6667 | 0.6857 | 0.7273 | 0.3939 |
| privacy | 33 | 0.5909 | 0.5263 | 0.4545 | 0.2424 |
| property_damage | 33 | 0.6364 | 0.7000 | 0.8485 | 0.3030 |
| religion_belief | 33 | 0.8182 | 0.7857 | 0.6667 | 0.6364 |
| violence | 33 | 0.7727 | 0.7887 | 0.8485 | 0.5455 |

The JSON cumulative result contains every failing sample UID, predicted label and reason, strict/valid-only per-category counts, Wilson intervals, pair-cluster intervals, and immutable input lineage. The 868-pair interim report is marked COVERAGE_IN_PROGRESS; its strict score is dominated by missing predictions and is not a full-test performance estimate.

## GPU resource accounting

| Run | Prediction rows | Measured wall lower bound (s) | Process peak (MiB) | Card peak (MiB) |
|---|---:|---:|---:|---:|
| d0_pilot100_20261120 | 200 | 8938.57 | 8330 | 8339 |
| d0_batch_100_100_ready_v1_20261121 | 196 | 10363.09 | 8330 | 8339 |
| d0_batch_200_100_ready_v1_20261122 | 186 | 7096.35 | 8330 | 8339 |
| d0_batch_100_100_supplement_v1_20261122 | 4 | 183.85 | 8330 | 8339 |
| d0_batch_200_100_supplement_complete_v1_20261122 | 14 | 561.32 | 8330 | 8339 |

Total through 300 pairs: 27143.18 s (7.540 GPU h), including 8,938.57 s Stage 2 Pilot100. Stage 3 added 18204.61 s. Every job finished below six hours and 20 GiB. Telemetry is archived losslessly as `gpu_samples.jsonl.gz` beside each run, with raw and archive SHA256 in `resource_accounting.json`. The first D0 batch used a resumable launch; no completed UID was regenerated.

## Data, protocol and source integrity

Test manifest remains 868 fixed pairs / 1,736 images at dataset revision `3ac26e778db94a282711f463f22ba6db99643bee`. Latest inventory at report generation: 1201 READY / 535 MISSING images; 581 READY / 287 incomplete pairs. The first 300 pairs are all image-complete. The exact original 86 missing UID list is `artifacts/stage3_first300_missing86.json` (SHA256 `ae85943b187c7ddaca6bc7d09a7b7fde5051f89cba27882f8103b973123ed15c`). Hub and curl attempt journals are append-only; each accepted image passed fixed-revision official LFS SHA256 and PIL decode.

Protected ledger: 249 pre-existing files rehashed, 0 changed. The D0 Pilot100 raw/metrics/freeze and old H1/A0/A1 evidence were not modified. The old/new D0 runner compatibility is frozen in `artifacts/d0_batch_runner_compatibility.json` and exact diff in `docs/d0_batch_runner_diff.patch`; only runner SHA is allowed to differ.

`artifacts/a1v2_protocol_freeze_v2.json` identifies A1v2 as a repaired final-verdict format, not the author’s original prompt. The new 36-row validation set was sampled before image availability and cannot be replaced after outcomes. A1v1’s old 36 outputs were used solely for parser development regression; they do not count as independent A1v2 validation. Human blind review: NOT_RUN. Training-method evidence and missing implementation details: `docs/stage3_training_method_evidence_audit.md`.

## Author comparison and remaining work

The author Table 1 reports nine-category average Unsafe F1 0.764 and Recall 0.866 for the full trained five-stage method. D0 300 is a direct prompt baseline on only the first fixed 300 pairs, so its macro 0.7085/0.6844 cannot be treated as a comparable reproduction or model-training ablation. A1v2 independent validation and Pilot100 remain necessary for a same-model five-stage comparison.

Pending: complete the 300–399 D0 ready subset, download its missing images and all remaining Test images, then continue frozen <=100-pair recoverable batches through 868. Run A1v2 Smoke and independent 36-row validation on a later single-GPU window; run Pilot100 only if >=35/36 parse uniquely and 36/36 generate. Do not launch SA-MCTS or DPO training in Stage 3.

## Reproduction and recovery commands

Run from `06_experiments/repro_thinkingguard_full`. Python inference environment: `/home/ubuntu/data/project/h1-cf-killtest/.venv/bin/python`; use the local fixed model snapshot `.../Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3`. Set an actually idle permitted GPU UUID after checking `nvidia-smi`.

```bash
python scripts/stage2_cumulative.py --protocol d0 --pairs 300 --output runs/d0_cumulative300_recheck.json runs/d0_pilot100_20261120/predictions.jsonl runs/d0_batch_100_100_ready_v1_20261121/predictions.jsonl runs/d0_batch_200_100_ready_v1_20261122/predictions.jsonl runs/d0_batch_100_100_supplement_v1_20261122/predictions.jsonl runs/d0_batch_200_100_supplement_complete_v1_20261122/predictions.jsonl
python scripts/stage2_inference.py --protocol d0 --stage batch --batch-start-pair 300 --batch-pairs 100 --batch-queue artifacts/stage3_batches/d0_300_100_ready_v1.json --model /home/ubuntu/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3 --gpu-uuid <IDLE_PERMITTED_UUID> --run-id d0_batch_300_100_ready_v1_20261122 --resume
```

CPU tests: `python -m pytest -q tests` → 47 passed. The first attempt with the inference virtualenv could not run pytest because that environment does not install it; the repository tests were run successfully with system Python 3 and pytest 8.3.4.
