# VLSU Stage 2 Work: real GPU smoke completed

2026-11-21, Asia/Shanghai. **GPU_SMOKE_REAL_RESULTS**: five official weight shards verified on Windows, the authorized jump host, and the GPU server; Direct10 + Binary5 + Structured CoT5 completed with BF16.

## Completion state

- Model downloaded: YES, all 16,584,414,560 bytes (15.45 GiB).
- Fixed weight size/SHA-256 verification: **5/5 PASS**, independently on each acquisition/target machine.
- Transfer to GPU server: **COMPLETE**, native-network rsync exit 0.
- Pinned tokenizer, processor, configuration and index files: preserved and verified by the original runner's complete model_manifest gate.
- Model loaded and real GPU inference: **YES, 20 generated outputs**.
- Original paper tables/figures reproduced: **NO**. This is the prescribed small engineering smoke.

Model: Qwen/Qwen2.5-VL-7B-Instruct. HF revision, tokenizer and processor revision: `cc594898137f460bfe9f0759e9844b3ce807cfb5`. Exact expected/observed weight hashes are in Model_SHA_Audit.json; complete target-model file hashes and measured arm statistics are in Execution_Metrics.json.

## Download and private transfer evidence

The eight requested GitHub files were read at branch head `3df77999a2df87ef90a2e022e8eabbb317c7112e`. The actual Windows filesystem and terminal were usable. Official HF at the pinned revision failed to complete a shard; 117,029,901 Xet partial bytes were retained. Official Qwen ModelScope downloaded all five shards on Windows in approximately 23m46s. Independent streaming verification returned exit 0, VERIFIED 5/5. ModelScope master was accepted only because all five bytes/size/SHA values matched the frozen HF manifest; no ModelScope metadata replaced HF metadata.

Windows SFTP upload was approximately 1 MB/s. A request-size adjustment resumed shard 1 from byte 353,501,184; a subsequent connection reset left 673,054,720 bytes in a private .uploading file. That partial was never accepted as a model shard. Windows complete verified files remain intact as a backup.

The already-authorized jump host tiaoban offered a new official-download environment. Its ModelScope client acquired the same five shards, using the client's built-in range-download/resume support. Earlier incomplete files and range parts were retained across adjustments. Tool/runtime interruption terminated local control sessions; the remote nohup download completed and was verified after reconnecting. No new downloader framework was developed.

The observed native interface addresses provided an approximately 0.08 ms path between tiaoban and target sunyu. The transfer used existing rsync with --partial --append-verify and strict SSH host-key checking, reusing the known target host identity. Exact transfer summary: 16,588,463,944 bytes sent, 111 received, 293,601,133.72 bytes/s; total model weight size 16,584,414,560 bytes. RSYNC_EXIT 0 and REMOTE_EXIT 0. The existing revision-named HF snapshot on sunyu received only the five weight files. All model files were then independently rechecked by the unchanged runner before loading.

## Real measured results

| Arm | Generated | Parse valid | Input/output tokens | P50/P95 seconds | Peak allocated/reserved GiB | Physical GPU index |
|---|---:|---:|---:|---:|---:|---:|
| direct | 10/10 | 100% | 9035/20 | 0.463/1.836 | 15.815 / 16.299 | 3 |
| binary | 5/5 | 100% | 4510/10 | 0.591/1.371 | 15.794 / 16.273 | 4 |
| structured_cot | 5/5 | 100% | 6130/906 | 5.477/6.205 | 15.874 / 16.330 | 3 |

All arms used **BF16**, batch 1, do_sample=false and num_beams=1. Original maximum output limits remained Direct/Binary 1024 and CoT 2048. No short-output option, 4-bit, OOM fallback, training or paid inference API was used. Actual outputs were 20, 10 and 906 tokens respectively; configured limits were not reduced.

GPU 3: `GPU-45decdd6-682b-4cd9-2bc3-6769eee7a81f`. GPU 4: `GPU-d72631b6-1716-61ed-d355-8da3e5558910`. Both reported NVIDIA GeForce RTX 4090 D, 49,140 MiB physical memory, driver 580.82.09. **One GPU per arm, sequential arms**: Direct GPU3, Binary GPU4, CoT GPU3. Fresh checks required no existing compute process, utilization 0 and at most 512 MiB used; each selected GPU reported 3 MiB before its run. GPU index was allowed to change between completed processes so that a just-released device did not need to be assumed idle.

The original runner enforced a **20 GiB PyTorch allocator budget**. Maximum observed PyTorch allocated/reserved memory across arms: 15.874 / 16.330 GiB. Independent 1-second NVML sampling observed peaks of 17,121 / 17,095 / 17,153 MiB for Direct/Binary/CoT; these include CUDA overhead and are sampled observations, distinct from allocator peaks.

PyTorch 2.9.1+cu128, Transformers 4.57.3; existing Python environment /tmp/trace-s0-py310/bin/python. Model load times were 33.26 / 16.76 / 10.61 seconds. P50/P95 above measure per-sample runtime and exclude model loading and preflight model hashing. These small-cohort p95 values are not population latency estimates.

All 20 records have state generated; **no failed samples, no generation errors**. GPU jobs each completed on their first execution; durable SQLite/JSONL records were preserved. No GPU-resume replay was needed. The workflow and each Python job had an external 21,570-second limit with 30-second kill grace, so the entire GPU workflow was bounded below six hours.

## Frozen protocol and evidence

- Runner SHA-256: `36b748e941f164e92a6e2cca984da4eda15daffa8a8f26906450bf87c8d393cd`.
- Smoke config SHA-256: `5b9891cfbdeb40ebfdd161aa2198d0e8ee7c1ea5fd6f3c89a279d81a39414c79`.
- Roster SHA-256: `63e4519eb511a677e2e7e9b5aa91158d963ea3fee424b4e680c961415647c7a6`.
- Stage 1 snapshot SHA-256: `78863294fca58b40d15581913e7f7d2c97ba0bc293ae75eb1c674e5b76d38512`.
- Exact UUID order check passed: Binary5 == CoT5 == Direct10[:5]. Prompt hashes, generation settings and run IDs are in Execution_Metrics.json.
- Existing regression suite: **81 passed in 6.89s** under the server's base Python. The GPU venv did not contain pytest; it was not modified.
- Only a private shell wrapper was added to sequence the unchanged runner, enforce a whole-workflow timeout, and sample NVML. bash -n passed. Existing uncommitted Stage 2T server files were preserved.

Private evidence remains under the experiment's .local/stage2/<run_id>/ (raw.jsonl, parsed.jsonl, run.sqlite, run_spec.json, summary.json) and .local/stage2work/ (workflow/arm logs, NVML CSVs, complete model verification). Raw model text, UUID/query/image records, datasets, weights and credentials are not committed.

## Actual workflow log (UTC)

```text
SERVER_ALL_MODEL_FILES_VERIFIED cc594898137f460bfe9f0759e9844b3ce807cfb5
START direct GPU-45decdd6-682b-4cd9-2bc3-6769eee7a81f 2026-11-21T05:42:14Z
COMPLETE direct 2026-11-21T05:43:20Z
START binary GPU-d72631b6-1716-61ed-d355-8da3e5558910 2026-11-21T05:43:20Z
COMPLETE binary 2026-11-21T05:44:06Z
START structured_cot GPU-45decdd6-682b-4cd9-2bc3-6769eee7a81f 2026-11-21T05:44:07Z
COMPLETE structured_cot 2026-11-21T05:45:09Z
```

This corresponds to 13:42:14–13:45:09 Asia/Shanghai for the three sequential arms.

## Next executable pilot arrangement and remaining limits

The weight/network deployment gate is resolved. Remaining formal-reproduction limits are data/image coverage and expansion of the frozen cohort, not model acquisition. Earlier project evidence still documents only a small available image pool; no new full-dataset image availability claim is made here.

1. Preserve this Stage 2 config, all three run IDs and the private ledgers. In a new isolated worktree/config commit, freeze a new paired cohort from actually available image objects with valid Joint gold. Start with **at most 30 eligible UUIDs**, and lower N if the audited eligible count is smaller.
2. In that isolated config snapshot set joint_count=N and diagnostic_count=N; retain the pinned model, seed, preprocessing, prompts and generation limits. Reuse the same runner for Direct, Binary and CoT with new config-derived run IDs. Do not overwrite this smoke's configuration or outputs.
3. Preflight frozen CSV/image hashes and select one actually idle GPU again. Keep BF16, 20 GiB allocator budget, batch 1 and the existing whole-workflow external time bound. Use per-arm measured p95 plus loading/hashing/checkpoint overhead to set conservative scheduling limits; maximum output lengths and unseen images can produce longer tails, so do not extrapolate a paper-scale throughput claim from these short outputs.
4. Compare paired parse outcomes and inspect any failures privately before expanding further. Release formal Table/Figure comparisons only after the required image coverage and original protocol conditions are satisfied. These 20 generations are not the original paper's experimental results.
