# ThinkingGuard resume and model acceptance — 2026-11-17

Start: 2026-11-17 01:44:39 UTC. Report: 2026-11-17T03:37:26.686051+00:00. Six-hour ceiling: 07:44:39 UTC. Download deadline: 05:44:39 UTC. Execution stopped after smoke evaluation; no supervised download, isolated proxy or inference process remains. Baseline GitHub commit: 0c855fbc60b5dc067cc6a9660d1679111c9829b6.

## Outcome

**119/119 missing blocks acquired; 929/929 original valid blocks preserved without redownload. Four official weight SHA256 checks pass. Cache ready=true after a documented local index repair. Real NF4 GPU inference completed. Unified smoke parsed 10/10 outputs; the official five-step frozen parser returned INVALID for 4/4. Full 36-pair experiment: NOT_RUN.**

## Acquisition and integrity

Used only ThinkingGuard fixed revision 76892f9768ce828268265171f4bbc5dfb75eafc3, isolated N10 on loopback 17900, two concurrent Range requests. No node audit, system proxy modification, Qwen acquisition, training or paid inference API. Existing blocks were all rehashed before transfer and again checked against the preflight receipts afterward. Successful transfer events match exactly the original 119 missing indexes, with no duplicate successful block events. First bounded pass acquired 108; second acquired the remaining 11. Each block had at most three attempts per pass.

New successful bytes: 1,983,370,784; remaining bytes/blocks: 0. Download error events: 60. Logged transfer observation window: 2642.8 seconds; successful-byte effective throughput over that window: 0.716 MiB/s (includes pauses and assembly). Total on-wire traffic including failed partial requests was not measured. Weights and durable blocks remain exclusively in the original model_snapshots tree and are excluded from Git.

| Shard | Expected bytes | Official SHA256 | SHA256 |
|---|---:|---|---|
| 1 | 4,905,357,176 | PASS | `32eea4896bf5cb65467ea1d20d7441dea603329f9354e5253a8c52211757f947` |
| 2 | 4,915,962,456 | PASS | `b40d5eaf9ca25a5ce6bcf9f1c73cd954d417b4baffcfc6315f7962bc8e7ff26b` |
| 3 | 4,974,674,312 | PASS | `18892b0bc15ebd51ec02248d52b621a1b66fb98d81f14f4318799badda84f777` |
| 4 | 2,738,345,504 | PASS | `bf0f4158d688cfa9498e64ae473794e6c86618328b566fff6f232cd5d3976b77` |

`acceptance.json` contains independent final whole-file hashes and preservation checks. The old sparse .incomplete artifact was not reused. Failed temporary artifacts and every valid block/receipt were retained.

## Official index inconsistency and local repair

The unmodified official snapshot did **not** pass the original cache gate: official index tensor locations disagreed with the SHA256-correct shard headers. `model_audit.json` preserves ready=false before repair. Original index Git blob: 5857ec62530eb589b1876034dd5386f1d98131a6, verified against the pinned revision's stored official metadata. Across the four shards, all **750** tensor names match exactly, with no duplicate/missing/extra tensor, and **17,534,247,392** tensor bytes match index metadata. safetensors.safe_open, dtype/shape byte lengths, contiguous nonoverlapping offsets and exact data lengths passed. The error affects **118 shard-location entries**.

`repair_verified_index.py` verifies the revision, every pinned weight size/SHA256, original index Git hash, complete tensor set, tensor shapes and offsets before constructing a corrected weight_map from actual shard headers. It fails closed on any mismatch. It preserves the official index as model.safetensors.index.official.json and changes no tensor bytes, tensor names, config, prompt or research label. No original audit hash/header requirement was weakened. The existing audit_model_cache.py then returned **ready=true**, with no missing or invalid files (`model_audit_repaired.json`). This is a repaired local snapshot, not a claim that the official index was valid.

Original index SHA256: `520b2e05079402e9468a8701d03d1154d14b2599593afb6effa7fb60c1bff070`. Local corrected index SHA256: `4e072f2b3e4199e17d96874148d16e241db2e0d2c0a1f64c4403afaade9c4961`. Both index files and detailed repair evidence are archived. Predictions and model metadata record the corrected index hash/provenance in addition to the fixed model revision. Future official snapshot downloads may restore the bad original index; rerun the explicit verified repair before the unchanged audit if that occurs.

## GPU smoke

GPU 2 became occupied before launch; idle check blocked that attempt before model loading. GPU 3 (RTX 4090 D) was checked idle and used instead. Single model per process, batch 1, NF4 4-bit, BF16 compute, double quantization, do_sample=false, unified max_new_tokens=32 and official max_new_tokens=1024. No multi-GPU placement or CPU/disk offload. Seed 20261105. The first two original frozen pairs, their order, image SHA256 checks and labels were retained. CPU regressions: 23/23 pass before and after the metadata-only inference change.

| Protocol | Raw records | Parse success | PyTorch peak GiB | Generation seconds |
|---|---:|---:|---:|---:|
| unified | 10 | 10/10 | 7.738 | 318.23 |
| official_five_step | 4 | 0/4 | 7.723 | 238.41 |

No OOM or generation exception. Raw image/text generations and evaluation files exist; 14 records have no duplicate model/protocol/pair/condition/side keys. Unified includes four Joint, two text-only and four image-only predictions. Official protocol includes four image-text predictions. No single-modality accuracy was reported against Joint labels.

Memory caveat: PyTorch maximum allocated/reserved peak is 7.738GiB with the existing 20GiB allocator cap. Device usage was observed at 8335MiB during the isolated smoke. PID-based nvidia-smi telemetry returned 0 in all 533 samples despite known GPU use; these are **unavailable telemetry**, not true zero usage. The exact process-wide peak including non-PyTorch allocations is not independently established by that telemetry. This limitation is retained in acceptance_gate.json; the report does not claim a measured 0MiB process or conflate shared device memory with process attribution.

Official outputs contain analysis and the Overall end delimiter, but omit the frozen parser's required numbered `5. Overall:` heading; two also use unbracketed verdicts. Frozen parse status remains **INVALID/missing_overall** for all four. No raw output, parser, prompt or threshold was altered after observing results. This is a format/parser acceptance failure, not evidence that all four semantic risk judgments were incorrect.

## Evaluation and decision

Unified two-pair smoke only: Joint accuracy 3/4=75% (Wilson95 30.1–95.4%), Unsafe F1 0.667, PairAcc 1/2=50% (Wilson95 9.45–90.55%), FPR 0/2, FNR 1/2. Correct flip 1/2; reverse flip 0/2; both Safe 1/2; both Unsafe 0/2. These are four Joint observations from two exploratory smoke pairs, not results for the planned 36 pairs or evidence of stable generalization/causal defects. Full metrics and confidence intervals are in the protocol-specific JSON files. The official metrics retain the original INVALID-as-incorrect policy and cannot be interpreted as valid-label accuracy. Protocol metrics are never mixed.

Unified observed parsing is 10/10; the 95% formal gate remains unchanged and is not statistically established by ten observations. Because the official parsing smoke fails and exact PID memory telemetry remains unavailable, the **overall smoke acceptance gate is not fully passed** and the full experiment was not started. 36-pair metrics, nine-category formal results, Qwen comparison and bootstrap: **NOT_RUN**. Human causal validity review remains separate.

Raw predictions: `runs/h1_resume_20261117_014439/smoke/predictions.jsonl`. Model/quantization/index metadata: smoke/model_revisions.json. Logs, phase timestamps, original manifest, GPU samples, acceptance checks and both original/repaired cache audits are retained. No weights, proxy configuration or credentials are committed.

## Next step

Model download is complete; no user download/upload or authentication is required. The next work is a prospective review of official output parsing and process-memory observability before authorizing a formal-run gate. Preserve these original INVALID outputs; do not silently reinterpret them or claim a completed 36-pair kill test. No main merge is performed. The report's containing GitHub commit is supplied separately after publication.
