# H1-K0 model access audit

Date: 2026-11-16 UTC. Scope: model availability and CPU readiness only. No model weights were downloaded, no model was loaded, and no GPU inference was run in this audit. Original run data and results were not changed.

## Direct answers

| Question | Finding |
| --- | --- |
| ThinkingGuard-8B weights complete? | **No.** Fixed revision `76892f9768ce828268265171f4bbc5dfb75eafc3` has readable configuration, tokenizer, Processor and chat template, but **0/4** complete weight shards. |
| Qwen3-VL-8B-Instruct weights complete? | **No.** There is no local cache directory for fixed revision `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`: **0/4** weight shards and no local configuration or Processor files. |
| Missing files? | ThinkingGuard: `model-00001-of-00004.safetensors` through `model-00004-of-00004.safetensors`. Qwen: those four shard names, `model.safetensors.index.json`, `config.json`, `generation_config.json`, `preprocessor_config.json`, `video_preprocessor_config.json`, `chat_template.json`, `tokenizer.json`, `tokenizer_config.json`, `merges.txt`, and `vocab.json`. |
| Most reliable acquisition? | Download both **exact revisions** from official Hugging Face on another authorized device with a stable connection, validate fixed LFS SHA256 there, transfer complete snapshot directories by `rsync` into this user's own project directory, then validate again on this server. |
| Two-pair GPU Smoke Test? | Exact commands are below. Run only after both CPU cache audits report `ready: true`. They create a new run directory and do not modify original runs. |

## Cache inventory and failure diagnosis

The ThinkingGuard snapshot at `~/.cache/huggingface/hub/models--Sandy124--ThinkingGuard-8B/snapshots/76892f9768ce828268265171f4bbc5dfb75eafc3/` contains valid symlinks for `config.json`, `processor_config.json`, `chat_template.jinja`, tokenizer files, `generation_config.json`, and `model.safetensors.index.json`. All four indexed shard links are absent. The index declares 17,534,247,392 tensor bytes. `AutoProcessor` loaded from this local snapshot on CPU as `Qwen3VLProcessor`; the image processor is `Qwen2VLImageProcessorFast`, and the chat template rendered the expected image markers. There is no confirmed corrupt *completed* weight file to discard.

The blob cache retains four `.incomplete` files. Their names match the official LFS SHA256 values below. Shard 1 has 445,798,168 apparent bytes but only 158,047,744 allocated bytes; its beginning is a sparse hole. Shards 2–4 are zero bytes. These are **incomplete artifacts**, not usable model weights. A plain `curl -C -` or file concatenation would treat shard 1 as a continuous prefix and is unsafe. Keep these files untouched; a future official client may reuse verified chunks, but no reliable resume was demonstrated here.

| Model | Shard 1 | Shard 2 | Shard 3 | Shard 4 |
| --- | ---: | ---: | ---: | ---: |
| ThinkingGuard fixed revision | missing; sparse partial | missing; zero-byte partial | missing; zero-byte partial | missing; zero-byte partial |
| Qwen3-VL fixed revision | missing | missing | missing | missing |

Both earlier runs stopped before model loading. The original run's transfer logs record repeated timeout/TLS errors on ThinkingGuard shards 1 and 2. The recovery run's Hugging Face transfer failed on shard 1 with incomplete reads, `aria2c` failed TLS handshakes, and bounded `curl` resume made minimal progress. Qwen was not attempted. On 2026-11-16 a **single HEAD** request for shard 1 returned HTTP 200 after a redirect in 1.56 seconds; this only proves small control requests can succeed, not that a 4–5 GB shard transfer is stable. No large transfer or retry loop was started. The server has ample personal storage space, so the observed blocker is transfer reliability, not disk capacity.

The official fixed-revision [ThinkingGuard file metadata](https://huggingface.co/api/models/Sandy124/ThinkingGuard-8B/revision/76892f9768ce828268265171f4bbc5dfb75eafc3?blobs=true) and [Qwen file metadata](https://huggingface.co/api/models/Qwen/Qwen3-VL-8B-Instruct/revision/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b?blobs=true) supply the eight pinned LFS sizes and SHA256 hashes embedded in `scripts/audit_model_cache.py`. Each repository has four shards, totaling roughly 17.5 GB of weight files, so plan for over 35 GB of source and destination storage together. The official [snapshot download guide](https://huggingface.co/docs/huggingface_hub/guides/download) documents `snapshot_download` with a pinned revision and local directory.

## CPU readiness and code changes

The experiment branch previously lacked the local pre-inference repairs. They are now included: image paths resolve through explicit `--image-root` and frozen `hf_path`; all selected images are SHA256-checked and decoded before model loading; INVALID comparisons are excluded from valid agreement; GPU telemetry counts this PID, while the PyTorch process cap remains 20 GiB; model metadata is retained by model, protocol, and session. The inference script now accepts `--model-path` for a transferred local snapshot, forces Hub offline mode, and runs a CPU integrity gate **before CUDA initialization**. The gate checks fixed revision, required files, index membership, full official LFS size/SHA256, and safetensors headers. It never loads tensors or uses GPU.

ThinkingGuard's local `config.json` and the official Qwen config for the pinned revision both declare `Qwen3VLForConditionalGeneration` / `qwen3_vl`. Installed Transformers 4.57.3 maps `AutoModelForVision2Seq` to that exact class. ThinkingGuard retains the [official five-step prompt and Processor/chat-template usage](https://github.com/FroggyChen/ThinkingGuard/blob/main/inference.py). Real model loading and output parsing are still unverified. The 36 frozen pairs, all 72 image SHA256 values and decoding, contact sheets, cache gate, parser, duplicate/missing/mixed-revision evaluation, and PID-only memory accounting were checked by **23 passing CPU tests**. No raw experiment result was edited.

## Recommended transfer workflow (future, on an authorized device)

Use only the official model repositories and a device/account you are authorized to use. Run the following on that device with a stable connection. The download is pinned to full commit IDs, writes into that device's personal directory, and uses two workers rather than an unbounded parallel retry strategy:

```bash
python3 -m venv "$HOME/h1-hf-venv"
"$HOME/h1-hf-venv/bin/python" -m pip install huggingface_hub
"$HOME/h1-hf-venv/bin/python" - <<'PY'
from pathlib import Path
from huggingface_hub import snapshot_download
root = Path.home() / 'h1_model_snapshots'
for repo, revision in (
    ('Sandy124/ThinkingGuard-8B', '76892f9768ce828268265171f4bbc5dfb75eafc3'),
    ('Qwen/Qwen3-VL-8B-Instruct', '0c351dd01ed87e9c1b53cbc748cba10e6187ff3b'),
):
    destination = root / repo.replace('/', '__') / revision
    snapshot_download(repo_id=repo, revision=revision, local_dir=str(destination), max_workers=2)
    print(destination)
PY
```

After this audit branch is available on GitHub, clone it on that device and run the **CPU-only** verifier on both downloaded directories. It exits with code 2 if any required file, shard size, SHA256, header, or revision is wrong:

```bash
git clone --branch experiments/h1-k0-triggerbench-20261106 --single-branch https://github.com/YuSun-WK/implicit-content-research.git "$HOME/h1-audit-code"
AUDIT="$HOME/h1-audit-code/03_experiments/h1_k0_triggerbench/scripts/audit_model_cache.py"
python3 "$AUDIT" Sandy124/ThinkingGuard-8B "$HOME/h1_model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3"
python3 "$AUDIT" Qwen/Qwen3-VL-8B-Instruct "$HOME/h1_model_snapshots/Qwen__Qwen3-VL-8B-Instruct/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
```

Set `SERVER_HOST` to the SSH endpoint already authorized for this server. Transfer only into this user's personal project directory. `rsync` retains interrupted transfers in a separate partial directory; rerun the same command after interruption. Never copy into another user's cache, and do not merge these files with the sparse old `.incomplete` blob:

```bash
SERVER_HOST='<your-authorized-ssh-host>'
ssh "ubuntu@$SERVER_HOST" 'mkdir -p /home/ubuntu/data/project/h1-cf-killtest/model_snapshots'
rsync -aP --partial-dir=.rsync-partial "$HOME/h1_model_snapshots/" "ubuntu@$SERVER_HOST:/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/"
```

On this server, rerun both `audit_model_cache.py` commands against `/home/ubuntu/data/project/h1-cf-killtest/model_snapshots/...`. Require `ready: true` from both before any GPU use. The SHA256 check verifies the transferred bytes against Hugging Face's fixed-revision LFS metadata, not only against the source device.

## Future two-pair GPU Smoke Test commands (do not run now)

These commands run all three planned model/protocol combinations on the **first two original pairs** in a new smoke directory. They leave the original recovery run untouched. Use GPU index 2 only if it is available at that time; the inference script enforces a 20 GiB single-process budget.

```bash
cd /home/ubuntu/data/project/h1-cf-killtest
EXPERIMENT="$PWD/archive_model_access/03_experiments/h1_k0_triggerbench"
MODEL_ROOT="$PWD/model_snapshots"
IMAGE_ROOT="$PWD/image_cache_h1_k0_recovery"
SMOKE_RUN="$PWD/runs/h1_k0_smoke_2pairs_$(date -u +%Y%m%d_%H%M%S)"
mkdir -p "$SMOKE_RUN"
cp runs/h1_k0_recovery_20261107_034443/sample_manifest.csv "$SMOKE_RUN/sample_manifest.csv"
.venv/bin/python "$EXPERIMENT/scripts/audit_model_cache.py" Sandy124/ThinkingGuard-8B "$MODEL_ROOT/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3"
.venv/bin/python "$EXPERIMENT/scripts/audit_model_cache.py" Qwen/Qwen3-VL-8B-Instruct "$MODEL_ROOT/Qwen__Qwen3-VL-8B-Instruct/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
.venv/bin/python "$EXPERIMENT/scripts/run_inference.py" "$SMOKE_RUN" Sandy124/ThinkingGuard-8B --protocol unified --limit-pairs 2 --gpu 2 --image-root "$IMAGE_ROOT" --model-path "$MODEL_ROOT/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3"
.venv/bin/python "$EXPERIMENT/scripts/run_inference.py" "$SMOKE_RUN" Sandy124/ThinkingGuard-8B --protocol official_five_step --limit-pairs 2 --gpu 2 --image-root "$IMAGE_ROOT" --model-path "$MODEL_ROOT/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3"
.venv/bin/python "$EXPERIMENT/scripts/run_inference.py" "$SMOKE_RUN" Qwen/Qwen3-VL-8B-Instruct --protocol unified --limit-pairs 2 --gpu 2 --image-root "$IMAGE_ROOT" --model-path "$MODEL_ROOT/Qwen__Qwen3-VL-8B-Instruct/0c351dd01ed87e9c1b53cbc748cba10e6187ff3b"
```

**Stop condition now:** Neither model is ready. Do not run the GPU Smoke Test or full experiment until both fixed-revision snapshots pass the CPU integrity gate.
