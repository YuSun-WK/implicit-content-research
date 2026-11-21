# Stage 2 Work execution checkpoint

2026-11-21 (Asia/Shanghai). **Local official weights: 5/5 SHA-256 PASS. Server transfer incomplete. GPU inference NOT RUN.**

The eight requested files were read from the connected GitHub branch and the branch was cloned at `3df77999a2df87ef90a2e022e8eabbb317c7112e`. The runner, smoke YAML and model manifest on the GPU server match that commit after Git newline normalization. Existing uncommitted server-side Stage 2T files were preserved.

## Completed download and verification

The actual Windows terminal and filesystem were usable. No complete matching model was found in the inspected current workspace and standard user caches. An isolated Python environment used huggingface_hub 2.4.0 and modelscope 1.40.3.

Official Hugging Face was attempted at the pinned revision. Xet left 117,029,901 incomplete bytes; the HTTP alternative did not complete a shard. Those partials were preserved. The Qwen official ModelScope repository downloaded all five files on Windows in approximately 23m46s. Independent streaming size/SHA-256 verification returned **VERIFIED 5/5**, exit code 0. A second complete verification before transfer also passed. See Model_SHA_Audit.json for exact observed hashes and sizes. ModelScope master is accepted only for these five hash-matching weight files; HF metadata remains pinned and unchanged on the GPU server.

The complete local cache is private, outside the Git checkout. No model file, image, dataset, signed download URL, password, key, token or raw model generation is committed.

## Server access and ongoing transfer

Authenticated access to the authorized jump host tiaoban and target sunyu succeeded. The target model directory is the existing HF snapshot named `cc594898137f460bfe9f0759e9844b3ce807cfb5`. The target project filesystem had approximately 3.6 TiB free. GPU inventory included idle RTX 4090 D devices at inspection time; a fresh availability check is required before inference.

SFTP used temporary .uploading files and retained byte offsets for recovery. The initial transfer was interrupted once for SFTP request-size tuning, resumed from byte 353,501,184, and later lost its SSH connection. The server retained 673,054,720 bytes of shard 1. This partial is not accepted as a verified shard. Local upload throughput was approximately 1 MB/s, so an alternative official ModelScope download was started on the already-authorized jump host, which has sufficient disk space and working official-source access. All jump-host files must pass the same five hashes before server transfer. No new downloader framework was developed.

## GPU status and next gate

The existing environment is /tmp/trace-s0-py310/bin/python, PyTorch 2.9.1+cu128 / Transformers 4.57.3. The existing runner's Direct10 execution-preparation pass returned exit 0, roster SHA-256 `63e4519eb511a677e2e7e9b5aa91158d963ea3fee424b4e680c961415647c7a6`. This is preparation, not GPU generation.

Model loaded: **NO**. Direct **0/10**; Binary **0/5**; Structured CoT **0/5**. GPU precision, token counts, parse validity, latency and peak memory are unmeasured. No paper result is claimed.

Continue the current authorized transfer route, verify all weights and pinned metadata on the target, recheck one idle physical GPU UUID, and execute the unchanged runner with BF16, 20 GiB allocator budget and per-job external timeout 21,570 seconds. Run Direct10, then paired Binary5 and Structured CoT5. Preserve raw outputs and durable ledgers only in private .local storage. Expand samples only after these actual measurements are available; no throughput estimate has been invented.


