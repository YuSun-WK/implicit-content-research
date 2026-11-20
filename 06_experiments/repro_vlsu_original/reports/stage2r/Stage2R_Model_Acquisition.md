# Stage 2R acquisition and inference status

Status: **MODEL_WEIGHTS_PARTIAL / MODEL_FETCH_BLOCKED_BY_ENVIRONMENT**. The fixed Qwen revision is `cc594898137f460bfe9f0759e9844b3ce807cfb5`. Five complete shards are required. At this checkpoint, 0/5 have passed full SHA-256 verification; 418,416,954 of 16,584,414,560 expected weight bytes are present as private partials. The initial 284,199,226 bytes were preserved. See `model_acquisition_manifest.json` for each shard's exact expected hash, size and current bytes.

The official HF LFS batch endpoint served signed URLs for the five pinned objects. 16 MiB and 64 MiB Range probes succeeded with exact HTTP 206 and Content-Range. A bounded two-worker download then accepted two 64 MiB chunks. Every subsequent chunk failed after three attempts with network timeout or TLS error. Failed responses were not appended. The standard `hf download` attempt did not add bytes. The cache, signed URLs and raw transfer evidence remain private under `.local/stage2`.

**GPU model load and Direct/Binary/CoT generation: NOT RUN (0/10, 0/5, 0/5).** Full shard hashes are a mandatory gate. BF16 memory, latency, generated tokens, parsing and Accuracy remain UNKNOWN. Stage 1 coverage remains 30/8,159 Joint UUID; Track A is blocked independently. Stage 3 Pilot cannot start from this checkpoint. Prompt human signoff is also OPEN.

## Resume on a stable authorized machine

Use only the official repository and fixed revision. In a private directory with enough disk space:

```bash
REV=cc594898137f460bfe9f0759e9844b3ce807cfb5
hf download Qwen/Qwen2.5-VL-7B-Instruct --revision "$REV" \
  --include '*.safetensors' '*.json' merges.txt --cache-dir /private/vlsu-hf --max-workers 1
```

Verify each of the five files against `configs/stage2_model_files.json` before transfer. Transfer the revision snapshot with linked blobs, or materialize its complete files, to the experiment server's private `.local/stage2/hf/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$REV/`. For a materialized snapshot:

```bash
rsync -avP /private/verified-snapshot/ \
  user@authorized-server:/private/repro/06_experiments/repro_vlsu_original/.local/stage2/hf/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$REV/
```

Then run `scripts/stage2_qwen_smoke.py` against the frozen CSV, Stage 1 snapshot and exact revision directory. Its `model_manifest` gate checks all weights and metadata before GPU loading. Check GPU occupancy at execution time. Do not put weights, images, raw predictions, signed URLs or credentials in GitHub.

CPU regression run with the pinned CSV: **80 passed in 7.15s**. The separate run without `VLSU_PINNED_CSV` had 79 passed and one expected environment skip. No inference metrics can be extrapolated without actual generation.
