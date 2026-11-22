# MSSBench Stage 2 gate report · 2026-11-22

**Scope:** 100-pair input-safety expansion and fixed 10-pair token-cap diagnostic with `Sandy124/ThinkingGuard-8B@76892f9768ce828268265171f4bbc5dfb75eafc3`. This is **D, substitute-model protocol transfer**. The paper's original LLaVA-1.6 Vicuna-7B has separate Stage 1 native results at commit `f57e9d63894ef6963e35b9c68f891d1a918af129`; no original-model weights were downloaded or inferenced in this Stage 2 run.

## Gates

| Gate | Status | Evidence |
|---|---|---|
| Frozen data and images | **PASS** | 100 distinct original record pairs, 60 Chat / 40 Embodied; original 20 retained; 160 new images downloaded, all 200 pinned-size/SHA256/Pillow-decoded checks PASS. No content-SHA duplicate exclusions were needed. |
| Model and hardware | **PASS** | Existing verified local ThinkingGuard snapshot, fixed revision, NF4 double quantization, 224×224 RGB processing, greedy, batch 1, one `cuda:0` instance per process, no observed CPU offload. Highest model-load allocated 7.586 GiB; canonical-call allocated 6.924 GiB, reserved 7.773 GiB, NVML delta 8.191 GiB. |
| 256-token primary execution | **PASS** | 100 pairs / 200 image-text inputs / 600 method-inputs: 598 complete, two model-format invalid, zero canonical engineering failures; 1,039 real generations. Five new GPU processes totaled 10,855.412 s; longest single process 3,768.653 s (<6 h). The old 120 anchor method-inputs were reused by exact run key. |
| Agent information flow | **PASS** | Independently revalidated all 600 canonical method-input traces. Chat role calls: Intent 120, Visual 120, Safety 120, QA 119 (one Safety format-invalid skips QA). Embodied: Locator 80, Safety 80. Parent IDs, upstream text, image attachment, parser, route, single load, and memory checks pass. |
| Checkpoint resume | **PASS** | Chunk 1 ran as a five-pair pilot and a 20-pair continuation, with 150 distinct terminal run keys and zero recomputed keys. All other chunks also have unique terminal keys. |
| 512-token diagnostic | **PASS** | Ten frozen pairs (five Chat, five Embodied), independent decoding key and journal, 60/60 complete, 100 real calls. Initial two-pair check and remaining eight-pair run each used one GPU model load. 256 vs 512 same-subset cap hits 26/100 → 10/100; output tokens 15,934 → 19,740 (1.24×), generation time 1,299.7 → 1,592.8 s (1.23×). Explicit-label correctness and pair-exact counts did not change on this selected subset. |
| Response-behavior evaluation | **PARTIAL** | Final answer extraction, keyword screen, cap status, and 30 manually inspected traces are available. No paid GPT-4o Judge or equivalent validated response-behavior score was run. |
| Fidelity to original paper model | **PARTIAL** | Same fixed released data and repaired information flow, but this Stage 2 model is ThinkingGuard-8B, with NF4 and 224×224 preprocessing; it cannot be pooled with original LLaVA findings. Published Table 1 Embodied category discrepancy was not resolved by relabeling. |
| QC/IC supplement | **PARTIAL** | Optional QC/IC tasks were not run. The required primary experiment consumed about three hours of new GPU jobs, and the 512 diagnostic was prioritized. No QC/IC results are represented as observed. |

The 512 postprocessing shell stopped after all 60 GPU method-inputs had completed because the running shell file was edited. This was a **postprocessing orchestration error**, not a model or GPU failure. The unchanged SQLite journal was exported and independently revalidated without rerunning any generation; the failed shell line and recovery commands are retained in `logs/`.

## Primary explicit input-label results

The denominators include every planned safe/unsafe input. An invalid or missing label counts as not correct. Base emits no explicit input-safety label.

| Task | CoT safe | CoT unsafe | CoT balanced | Multi-Agent safe | Multi-Agent unsafe | Multi-Agent balanced | Pair exact CoT → MA |
|---|---:|---:|---:|---:|---:|---:|---:|
| Chat, 60 pairs | 60/60 | 13/60 | 73/120 = 60.8% | 55/60 | 34/60 | 89/120 = 74.2% | 13/60 → 31/60 |
| Embodied, 40 pairs | 37/40 | 8/40 | 45/80 = 56.2% | 24/40 | 19/40 | 43/80 = 53.8% | 7/40 → 10/40 |
| All selected, 100 pairs | 97/100 | 21/100 | 118/200 = 59.0% | 79/100 | 53/100 | 132/200 = 66.0% | 20/100 → 41/100 |

The overall Multi-Agent gain is **7.0 percentage points** in explicit input-label accuracy, concentrated in Chat and Unsafe cases. It is **2.5 points lower** than CoT on Embodied input-label accuracy. The paired exact comparison has 28 pairs improved by Multi-Agent, seven harmed, and 65 tied (13 both correct, 52 both incorrect). In Embodied, same-text pairs are CoT 24/44 vs Multi-Agent 22/44 correct sides; different-text pairs are 21/36 for both methods. The selected set contains 20 nonrandom smoke anchors; bootstrap intervals in [the grouped metrics](metrics_256.md) are conditional on these selected records, not a population estimate of MSSBench.

## Measured cost and failure modes

Across the same 200 inputs, Multi-Agent used 639 calls vs CoT's 200 (**3.19×**), 80,713 vs 39,569 output tokens (**2.04×**), and 6,740.9 vs 3,167.6 summed generation seconds (**2.13×**). Chat's respective ratios are 3.99× calls, 2.23× output tokens, and 2.34× generation time; Embodied's are 2.00×, 1.54×, and 1.64×. These are sums of real per-Agent measures; they exclude separate model-load time and do not claim a cost under the paper's original model.

Of 1,039 real calls, 291 reached the 256-token limit. One Chat Safety and one Embodied Safety output omitted the required label field. Both remain terminal model-format-invalid in the 100-pair denominator; the Chat QA call was correctly skipped. [Failure examples](failures_256.md) and [30-case manual inspection](manual_review.md) show overcautious safe-side judgments, ignored image-context hazards, and confusion between task feasibility and safety. The 512 subset reduced cap hits without changing explicit-label accuracy in its small selected denominator. Keyword behavior screens are descriptive only.

## Next-stage decision

**Pilot for a faithful paper-level claim: HOLD.** This Stage 2 table is suitable for an explicitly labeled ThinkingGuard-8B group-meeting comparison of input-safety judgments and cost. It is not evidence that the paper's LLaVA model or GPT-4o-judged response behavior improves under Multi-Agent. A subsequent original-model expansion and a separately specified response-behavior evaluation would be needed for that claim. No Pilot, Expanded Pilot, Full Evaluation, training, paid API, or optional QC/IC GPU job was started here.

Artifacts: [frozen inputs](frozen_100_pairs.csv), [image audit](new_image_audit.csv), [100-pair results](results_256.csv), [1,039 full traces](traces_256.jsonl), [group metrics](metrics_256.md), [paired analysis](paired_comparison_256.md), [cost](cost_256.md), [512 comparison](diagnostic_512.md), [512 results](results_512.csv), [100 diagnostic traces](traces_512.jsonl), [trace validation](trace_verification_all.log), and [real job logs](logs/).
