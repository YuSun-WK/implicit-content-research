# MSSBench Fast-track Gate Report

Real G1 and G2 outputs exist for **route B only**. This is D protocol transfer with `Sandy124/ThinkingGuard-8B@76892f9768ce828268265171f4bbc5dfb75eafc3`, not an original LLaVA run.

| Route / gate | Status | Evidence |
|---|---|---|
| A original LLaVA / weights | FAIL | Four original files remain incomplete, with no new persistent large object acquired. G1 and G2 did not run on A. [Inventory and offline transfer](fasttrack_model_inventory.md) |
| B verified checkpoint and probes | PASS | Four shard SHA256 values and actual tensor locations verified, plus 2 real probes. The single-image probe described the truck and excavator and expanded the 19 nominal input tokens to 82. [Artifact verification](fasttrack_B/verified_model.json) · [Probes](fasttrack_B/preliminary_probes.jsonl) |
| B G1 / 256 | PASS engineering, PARTIAL output | 2 pairs, 4 inputs, 12 method-inputs, 11 completed/1 model-invalid, 19 of 20 calls. The structurally valid Chat sequence and both Embodied role chains passed. |
| B G2 / 256 | PASS engineering, PARTIAL output | Completed the 20-pair matrix across fixed 40 inputs. The G1 journal records were reused. The remaining 180 calls finished; total 199 generations, 119 completed/1 format-invalid. |
| Pilot | HOLD | Engineering demonstrated within the 20 GiB budget. Embodied paired label accuracy was lower under MA on this small set, the substitute is itself a risk fine-tune, and original LLaVA remains blocked. A 50–100-pair pilot would also need separate approval and slicing to keep each GPU job below 6 h at the conservative bound. |

## Protocol and lineage

- GPU physical index 7, UUID `GPU-79ea6ee8-2e76-d36e-1508-7813c1589ec1`, only `cuda:0` visible. One successful model load for the primary 256-token matrix. CUDA allocated across load and generation peaked at 7.586 GiB, reserved at 7.773 GiB, NVML baseline-relative delta at 8.191 GiB. Primary wall 2479.79 s. [Cost and per-role counts](fasttrack_B/fasttrack_cost.md)
- Offline Python 3.10.19, Torch 2.9.1+cu128, Transformers 4.57.3, Accelerate 1.12.0, bitsandbytes 0.48.2. One batch item, seed 0, greedy, SDPA, NF4 FP16 double-quant with visual tower and LM head excluded, RGB→224×224 then the native Qwen3-VL processor. All 40 primary inputs used the same setup across all three methods. [Runtime versions](fasttrack_B/logs/runtime_versions.log)
- Fixed dataset `12396d24157427b671d97f23a2e370fca98fdf55`, upstream prompt commit `1602193f49cb6925bfa3751be157d0bbf5439779`, adapter `fasttrack-thinkingguard-nf4-v1`, parsing/collection policy `mssbench-stage0-v1+fasttrack-invalid-v1`. Stage 1 strict per-input stopping is preserved. In B, the runner logs model-format invalids and continues the matrix; engineering exceptions stop it. The run manifest records every input SHA, image SHA, config, revision and prompt SHA. [Manifest](fasttrack_B/fasttrack_run_manifest.csv)
- No external Judge. The measured explicit-label scores are distinct from final-behavior keyword buckets. Base has no requested explicit classification field. Raw strings are preserved in JSONL; the CSV response field is JSON-escaped to preserve multiline characters.

[Grouped results and paired labels](fasttrack_B/fasttrack_metrics.md) · [All result rows](fasttrack_B/fasttrack_results.csv) · [All 199 calls](fasttrack_B/fasttrack_agent_traces.jsonl) · [Reviewed failures](fasttrack_B/fasttrack_failures.md)

## Re-run route B

From this experiment directory, the existing read-only checkpoint is rooted at `$HOME/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3`. The committed `verified_model.json` is the produced integrity record. The original source checkout and 40 image files were reused. SQLite and console output are under `.stage0-local/fasttrack/B-thinkingguard/run-nf4-v2-256` and its sibling `run-nf4-v2-256.log`. Invoke on a freshly checked idle UUID only.

```bash
h="$HOME/data/project/h1-cf-killtest"
root=.stage0-local/fasttrack/B-thinkingguard
gpu=GPU-79ea6ee8-2e76-d36e-1508-7813c1589ec1
snap="$h/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3"
CUDA_VISIBLE_DEVICES="$gpu" HF_HUB_OFFLINE=1 TRANSFORMERS_OFFLINE=1 \
  PYTHONPATH="$PWD/$root/addons" TOKENIZERS_PARALLELISM=false \
  timeout -k 15s 21500s "$h/.venv/bin/python" -u stage1_smoke.py \
    --thinkingguard-snapshot "$snap" --model-root "$root" --output "$root/run-nf4-v2-256" \
    --data-root .stage0-local/stage1/data --official-source /tmp/mssbench-stage0-official \
    --gpu-uuid "$gpu" --preliminary-probes --max-new-tokens 256 --through g2
python fasttrack_export.py "$root/run-nf4-v2-256" fasttrack_B
```

The `addons/pynvml.py` link points to the installed NVML module in the Stage 1 venv. Reusing the existing output directory is a resume, while a new directory starts a fresh run.
