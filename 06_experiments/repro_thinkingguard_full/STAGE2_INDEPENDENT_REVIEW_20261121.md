# ThinkingGuard Stage 2 独立审查（2026-11-21）

Reviewed branch: `repro/thinkingguard-full-20261119`  
Reviewed HEAD: `d62757c3151fdae920630972addf12d9b7b6e692`  
Primary evidence: `STAGE2_FAST_EXECUTION_REPORT.md` and the referenced raw prediction, summary, metrics, resource, image-status, and queue artifacts.

## 1. Executive verdict

**D0 Direct Pilot100 = COMPLETE. A1 five-stage v1c = FAILED_PARSE_GATE. Full 300/868 evaluation = NOT RUN.**

The Stage 2 report is broadly consistent with the raw evidence. The completed D0 run is a genuine 100-pair/200-sample result and can be reused as the first 100 pairs of the frozen expansion order. It is a Direct Prompt baseline, not a reproduction of the paper's five-stage method or its DPO ablations.

## 2. D0 Direct Pilot100

- 200/200 rows generated and parsed; 0 INVALID; 100 complete Safe/Unsafe pairs.
- Accuracy 71.50% (143/200); Unsafe precision 71.72%; Unsafe recall 71.00%; Unsafe F1 0.7136.
- Safe FPR 28%; Unsafe FNR 29%; PairAcc 47/100 = 47%; reverse flip 4/100; both Safe 25/100; both Unsafe 24/100.
- Nine-category macro Unsafe F1 0.6959; macro Unsafe recall 0.7113.
- Accuracy Wilson 95% CI 64.88–77.30%; PairAcc Wilson 95% CI 37.51–56.71%; stratified pair-bootstrap 95% interval for Unsafe F1 0.6564–0.7614 and PairAcc 0.38–0.55.
- Privacy is a salient failure category: Unsafe recall 0.1818 and Unsafe F1 0.267. Misinformation is strongest in this pilot: Unsafe recall/F1 0.909.
- D0 uses the same fixed ThinkingGuard checkpoint and TriggerBench revision, but a direct one-verdict prompt and max_new_tokens=256. A1 uses five-stage reasoning and max_new_tokens=1024. They are different protocols; do not attribute differences solely to reasoning depth without controlling token budget and protocol.

Resource evidence: 8,853.80 seconds accumulated per-sample generation time; measured GPU wall lower bound 8,938.57 seconds (2.483 h) over two jobs, with one interruption/resume and no duplicate rows. P50/P95 per-sample latency 44.22/48.45 seconds. RTX 4090 D process/card peaks 8,330/8,339 MiB. Each job stayed under six hours.

## 3. A1 five-stage v1c failure and parser-specific diagnosis

Official A1 v1c Smoke: 6/6 generated, 0/6 parsed. Independent validation: 36/36 generated, structure complete 35/36, 0/36 parsed; 35 `NONTERMINAL_VERDICT`, 1 `MULTIPLE_OVERALL`. A1 Pilot100 and larger A1 evaluation were correctly NOT_RUN.

Additional raw-output audit (performed without using ground-truth labels):

- All 36 validation outputs contain exactly one explicit `Final verdict: SAFE/UNSAFE` phrase.
- All 36 phrases are terminal immediately before an `<|/Overall|>` marker.
- 35 outputs have exactly one Overall marker and a unique terminal verdict.
- One output has multiple Overall markers and should remain INVALID under strict structure validation.
- The v1 parser requires the final verdict to occupy a standalone line (`^Final verdict: (SAFE|UNSAFE)$`). In the 35 otherwise structurally valid outputs, the model placed the final verdict at the end of the same line as the Overall rationale. The parser therefore reports `NONTERMINAL_VERDICT`.

Interpretation: the model violated the prompt's two-line formatting instruction, while the strict parser rejected an otherwise unique, explicitly marked terminal verdict. This supports testing a **new A1v2 output contract/parser** that explicitly permits the terminal verdict clause to follow the Overall rationale on the same line. The old A1v1 validation set can be used only for parser development/regression analysis; it cannot serve as A1v2's independent validation. Freeze A1v2 and validate on a new unseen 36-row/18-pair set before any Pilot.

## 4. TriggerBench image coverage

Latest verified inventory at the reviewed HEAD:

- 1,736 Test images in the frozen manifest (868 Safe/Unsafe pairs).
- 985/1,736 images READY; 751 MISSING.
- 463/868 complete pairs READY; 405 pairs have at least one missing image.
- Frozen first-300 expansion queue: 243/300 complete pairs READY; 57 pairs incomplete; 514/600 images READY, so 86 images remain missing inside the first-300 queue.

The 57 incomplete first-300 pairs are distributed as follows:

| Category | Incomplete pairs | Missing images |
|---|---:|---:|
| Physical harm | 10 | 15 |
| Regional & belief | 13 | 23 |
| Misinformation | 1 | 1 |
| Offensiveness | 10 | 13 |
| Violence | 10 | 13 |
| Privacy | 7 | 12 |
| Property damage | 6 | 9 |
| **Total** | **57** | **86** |

All 86 missing images in the first-300 queue already appear in the Hub/curl attempt logs as failed attempts. The current downloader skips previously attempted UIDs by default; simply rerunning the broad download command will not retry them. Add an explicit UID-list/retry-failed path that appends new attempt records and still validates official LFS SHA256 plus PIL decoding.

## 5. Stage 3 engineering blockers

1. `scripts/stage2_inference.py` currently rejects `--protocol d0 --stage batch`; its batch branch explicitly requires protocol A1. This blocks extending the completed D0 Pilot100 to 300/868.
2. `scripts/stage2_cumulative.py` is hard-coded to A1 and rejects D0 predictions. It needs protocol-aware lineage checks and D0 cumulative scoring.
3. D0 Pilot100 was produced with the current runner SHA. Extending the runner changes its SHA. A cumulative report must not silently mix runner versions; add a small explicit compatibility manifest that permits only the reviewed batch-slicing/dispatch code change while requiring the D0 prompt, parser, config, model, dataset, image processor and source-tree hashes to match exactly.
4. `stage2_download.py` and `stage2_curl_fallback.py` skip UIDs already present in their attempt logs. Retry of the 86 first-300 missing images requires explicit opt-in.
5. The expansion queue includes all 868 official Test pairs; D0 Pilot100 exactly matches its first 100. The remaining batches must cover every subsequent pair, including old H1 pairs and A1 Smoke/Validation pairs, under D0's own frozen prompt. Do not reuse H1/A0/A1 predictions for D0. The D0 Smoke run is a separate format check; rerun its pair IDs in the full D0 batch and do not merge the Smoke file into cumulative metrics.

## 6. Recommended next milestones

1. Extend D0 batch inference and cumulative evaluation without altering the completed D0 Pilot100.
2. Retry the 86 missing first-300 images using a frozen UID list and bounded retries.
3. Complete D0 pairs 101–300 in two 100-pair jobs; if some images remain unavailable, run the currently READY first-300 pairs as `COVERAGE_IN_PROGRESS` and fill missing pairs later without shrinking the denominator.
4. Continue D0 pairs 301–868 in batches of at most 100 pairs, while recovering the remaining 665 missing images. Full completion requires 1,736/1,736 predictions and all 868 complete pairs.
5. In parallel on CPU, prepare A1v2 with an explicit terminal-verdict contract and a new unseen 36-row validation set. Run it only after freezing prompt/parser/queue hashes. If it passes at >=35/36, run A1v2 Pilot100 on the same 100 pairs for a paired D0-vs-A1 comparison.
6. SA-MCTS/DPO training remains NOT_FEASIBLE for this stage; D0 is not a training ablation.

All prior H1, Stage 1 A0, and Stage 2 protected artifacts remain unchanged according to the 249-file before/after ledger.
