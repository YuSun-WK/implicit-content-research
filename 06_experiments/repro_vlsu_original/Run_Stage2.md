# Stage 2 single-GPU engineering smoke

Run from the experiment directory. A Stage 1 auditable snapshot and its objects are sufficient for this first engineering run. Verify that they are present via [Stage 1R state migration](reports/stage1r/Move_Resume_Instructions.md). Update the smoke config only when starting an explicitly new cohort or revision.

## Restore the missing Qwen weight shards

Use an environment with a CUDA-compatible PyTorch and Transformers supporting Qwen2.5-VL, such as the tested PyTorch 2.9.1+cu128/Transformers 4.57.3 combination. BF16 uses CPU initialization followed by a single-GPU transfer. 4-bit requires compatible bitsandbytes and accelerate. Use a permitted network for the official Hugging Face download, or privately transfer a verified cache. Keep the snapshot directory named after the revision. If transferring a Hugging Face cache, include its linked blobs or materialize the files in the named directory.

```bash
export REV=cc594898137f460bfe9f0759e9844b3ce807cfb5
export VLSU_PINNED_CSV=/absolute/private/path/VLSU.csv
export VLSU_STATE_ROOT=.local/stage1
umask 077
hf download Qwen/Qwen2.5-VL-7B-Instruct --revision "$REV" \
  --include '*.safetensors' '*.json' merges.txt --cache-dir .local/stage2/hf --max-workers 3
export VLSU_MODEL_PATH=".local/stage2/hf/models--Qwen--Qwen2.5-VL-7B-Instruct/snapshots/$REV"
python scripts/extract_paper_prompts.py --pdf /absolute/private/path/vlsu-iclr-proceedings.pdf
export VLSU_ROSTER="$VLSU_STATE_ROOT/snapshots/78863294fca58b40d15581913e7f7d2c97ba0bc293ae75eb1c674e5b76d38512.json"
python scripts/stage2_qwen_smoke.py --csv "$VLSU_PINNED_CSV" --stage1-root "$VLSU_STATE_ROOT" \
  --manifest "$VLSU_ROSTER"
```

## Direct first, then paired diagnostics

Select one idle GPU by physical UUID using `nvidia-smi` after checking local scheduling rules. The runner checks the idle state after hashing verified inputs and model bytes. Use a five-hour, 59-minute, 30-second external time limit with a 30-second kill grace. No training or API calls occur. The 20 GiB allocator budget is enforced for PyTorch allocations, including BF16.

```bash
export CUDA_VISIBLE_DEVICES=GPU-replace-with-idle-device-uuid
timeout --signal=INT --kill-after=30s 21570s python scripts/stage2_qwen_smoke.py \
  --csv "$VLSU_PINNED_CSV" --stage1-root "$VLSU_STATE_ROOT" --manifest "$VLSU_ROSTER" \
  --model-path "$VLSU_MODEL_PATH" --mode direct --precision auto --execute
```

Rerun the identical command to resume the same run ID. The durable database skips completed records, leaves failure records in the ledger and emits explicit rows for any queued UUIDs. A hard termination can leave the last uncommitted record queued. Raw and parsed JSONL and SQLite are private under `.local/stage2/<run_id>/`. Report only aggregate metrics and hashes. If BF16 is above the estimated budget, auto selects 4-bit. If BF16 actually hits OOM, stop that process and preserve its ledgers, then restart once with `--precision 4bit` in a compatible environment using the same base snapshot. 4-bit has a different run ID. After Direct, substitute `--mode binary` and `--mode structured_cot` in separate bounded jobs. Keep the same frozen prefix for paired diagnostics.

## Pilot decision

After real Direct and CoT generation, use per-arm p95 end-to-end time per UUID, model load time and observed GPU memory peaks. A conservative starting batch limit is `floor((21570 - load_seconds - checkpoint_margin_seconds) / p95_seconds)`, capped by the actual fixed eligible UUID count and adjusted downward using measured pilot behavior. For N eligible samples, use measured per-arm throughput separately and include loading and checkpoint overhead. Report image availability uncertainty independently. Expand across paper patterns only after coverage and author protocol review. No numeric time or peak-memory extrapolation is currently available because generation has not started.
