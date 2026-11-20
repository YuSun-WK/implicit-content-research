# Stage 2S source switch

**EXTERNAL_DOWNLOAD_REQUIRED.** Official ModelScope `Qwen/Qwen2.5-VL-7B-Instruct` served `config.json`, then transferred 135,659,680 bytes of the smallest weight shard before five connection retries ended in `ConnectionError`. The first 7,876,447 bytes matched the existing official HF partial byte for byte; this does not establish full equivalence. ModelScope `master` is not the fixed HF revision. No complete ModelScope shard has been accepted. The existing HF partials (418,416,954 bytes) remain untouched. `Model_SHA_Audit.json` records every expected hash and partial count.

Weight gate: **0/5 full SHA-256 verified**. GPU load and Direct/Binary/CoT are **NOT RUN** (0/10, 0/5, 0/5). Actual memory, throughput, token counts and parse validity remain unmeasured. Stage 1 image availability is still 30/8,159 Joint UUID. Stage 3 Pilot cannot start. The one manual dependency is a stable authorized machine that can acquire and privately transfer the five hash-matching weight files. Once they arrive, Codex can verify them and run the fixed GPU smoke.

The pinned CSV regression suite returned **80 passed in 7.59s**. No model weights, images, signed URLs or raw outputs are in this commit.
