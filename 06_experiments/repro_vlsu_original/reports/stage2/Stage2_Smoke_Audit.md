# VLSU accelerated Stage 2 smoke

**Track B SMOKE BLOCKED / NOT RUN.** No real Qwen outputs were generated. Direct, Binary and Structured CoT all remain NOT RUN. The runner reached its preflight and stopped before loading any weights. Missing model bytes are the blocker. Track A is independently BLOCKED_BY_ENVIRONMENT.

## Model and data preflight

| Check | Evidence |
|---|---|
| CUDA | An idle NVIDIA GeForce RTX 4090 exposed 48,506 MiB free in nvidia-smi. The selected UUID was the sole visible CUDA device. CUDA 12.8 with PyTorch 2.9.1 supported BF16. Inference peak memory is unmeasured. [GPU probe](GPU_Environment.json) |
| Exact model | Public model revision `cc594898137f460bfe9f0759e9844b3ce807cfb5`. The official Git objects corroborated every upstream file entry and all five LFS SHA-256 pointers. The 9 metadata, tokenizer and processor files were cached and locally verified. [Model manifest](model_manifest.json) |
| Weight acquisition | The Hub client failed with TLS EOF. The official Git LFS batch endpoint returned five download actions. Bulk transfers made partial progress and repeatedly ended with low throughput, short responses, empty replies or timeouts. One-megabyte range probing succeeded. The latest resume still yielded 0/5 complete verified shards. The private cache retains the partial bytes. No GPU job reserved the card while waiting for weights. [Execution log](Stage2_Execution_Log.txt) |
| Cohort and templates | 10 deterministic Joint UUIDs from the verified existing snapshot, with gold S/B/U = 3/3/4 and nine patterns. All selected image hashes verified. Three prompts re-extracted from the pinned proceedings PDF matched their hashes. PROMPT HUMAN SIGNOFF OPEN. [Deviations](../../protocol/Stage2_Deviation_Ledger.md) |
| Real CPU processor | The pinned Qwen processor successfully built multimodal image grids and tokens for Direct 10, Binary 5 and CoT 5. No Qwen weights were involved. Offline test fixtures verified interruption, resume and strict parsing. No generated raw or parsed prediction artifacts exist for real runs. [Inference summary](Inference_Run_Summary.json) |

The upstream weights total 16,584,414,560 bytes (about 15.45 GiB). BF16 is the first choice within the 20 GiB allocator budget, with peak memory still awaiting measurement. No quantization was executed. GPU inference latency, throughput, generated-token counts, output validity and numerical full-run extrapolation are unavailable. Follow the bounded Direct command after transferring the complete hash-verified revision. Run paired Binary and CoT afterwards and use measured per-arm p95 to size a formal pilot. [Run commands](../../Run_Stage2.md) · [Official revision](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct/tree/cc594898137f460bfe9f0759e9844b3ce807cfb5)

## Track A image acquisition

The first probe passed the serial controls, but the capped 30-request resume then failed its runtime DNS gate before any image request. The 2026-11-20 serialized recheck did not pass. No alternate authorized stable worker was available in this session. No images were requested or added by these attempts. The acquisition history remains at 893 events. Preserve the original SQLite, objects and manifest for a capped resume on an authorized stable worker. [Latest probe](Track_A_Probe_Log.txt) · [Migration](../stage1r/Move_Resume_Instructions.md)

| Measure | Latest verified |
|---|---:|
| HTTP 200/206 sources | 31 |
| Complete bodies | 29 |
| Decoded URL images / official UUIDs | 28 / 30 |
| Joint UUID coverage | 30/8,159 (0.37%) |
| Image-only / Text-only / three valid gold and image inputs | 23 / 8,159 / 23 |
| Terminal failures / attempted pending / unattempted | 30 / 7 / 8,092 |
| S-S-S / S-S-U / U-S-U / B-B-U decoded coverage | 0/2,166 · 2/35 · 0/142 · 1/32 |

The official CSV has 8,159 rows and the paper reports 8,187. Coverage remains PARTIAL. Formal Stage 3 pilot and paper comparability remain open pending successful engineering generation and cohort/protocol review. [Track A counts](Track_A_Status.json) · [All patterns](../stage1r/coverage_by_pattern.csv)
