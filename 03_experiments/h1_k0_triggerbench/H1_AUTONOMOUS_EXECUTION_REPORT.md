# H1 autonomous execution report

Start: 2026-11-16 06:46:13 UTC. End: 2026-11-16T08:02:03.382129+00:00. Hard maximum: six hours; stopped early after bounded transport alternatives failed. No unattended download/GPU process remains. Baseline: bf15dc9e1d18c2bb0a2054dec02f69cb4a9e01f5.

## A. Model acquisition

ThinkingGuard fixed revision: 76892f9768ce828268265171f4bbc5dfb75eafc3. Qwen fixed revision: 0c351dd01ed87e9c1b53cbc748cba10e6187ff3b. Both audits return **ready: false**. ThinkingGuard has 0/4 completed shards; Qwen has 0/4 and was not downloaded concurrently. Small ThinkingGuard files were reused and checked against official revision metadata (Git blob SHA1 or LFS SHA256). Official metadata matches all four hardcoded LFS hashes/sizes. No weight shard has passed full official SHA256 or safetensors validation.

Used strict HTTP Range transfers from huggingface.co, then hf-mirror.com as a transport-only alternative. Probes returned correct 206 and Content-Range. Tested 16MiB, 1MiB and 4MiB blocks; each request required exact range, exact length and durable local SHA256 receipt. Failures included reset, read timeout and incomplete response. A fresh query per retry did not resolve failures. Official huggingface_hub HTTP client was bounded to 120 seconds; a default-client/Xet-enabled attempt was bounded to 180 seconds and failed at control requests (Xet data transport itself was not established). Direct connection without environment proxy failed. Mirror also failed sustained transfers. These results establish failure of tested routes during this run, not impossibility of every future route.

Verified unique retained shard-1 bytes: **113,246,208**. Remaining weights: **17,421,093,240 bytes**. Range observation window: 1477.7 seconds; unique retained effective rate: **0.073 MiB/s**, including failures and strategy gaps. Extrapolated remaining transfer: **63.1 hours**, an uncertain engineering estimate, beyond the remaining task budget. Range errors/retries logged: 62; completed block events: 26. Probe and phase timestamps are in JSON evidence. No infinite retry; each block had three attempts and each strategy was bounded.

Recovery location: `~/data/project/h1-cf-killtest/model_snapshots/Sandy124__ThinkingGuard-8B/76892f9768ce828268265171f4bbc5dfb75eafc3/`. Existing legacy sparse .incomplete files remain untouched and were never used as continuous prefixes. New incomplete .tmp blocks and bounded-client partial files remain as failed artifacts; only receipt-verified complete blocks may be reused. Receipt inventory records overlapping blocks without counting duplicate bytes. Weights and blocks are excluded from Git. No data was deleted.

Example recovery (same user/environment; set deadline to an absolute future Unix time within the next task budget): `.venv/bin/python scripts/download_verified.py --block-mib 4 --deadline UNIX_DEADLINE`. No credentials or unknown scripts are required. A resumed strategy still needs sustained-transfer validation. Run the existing model audit and require ready true before inference.

## B. GPU experiment

**NOT_RUN**. No model loaded; GPU runtime 0 seconds, peak process VRAM and inference speed not measured. At inspection GPU 2 was idle, GPUs 1 and 7 were occupied. Existing environment: PyTorch 2.9.1+cu128, CUDA runtime 12.8, Transformers 4.57.3, huggingface_hub 0.36.0. No environment changes or global installs. Intended NF4 4-bit, batch 1, deterministic generation and 20GiB cap remain untested in this execution. Both unified and official-five-step GPU protocols: NOT_RUN.

## C. Results

Accuracy, Unsafe F1, PairAcc, FPR, FNR, flip statistics, confidence intervals, category metrics, agreement, bootstrap and raw model predictions: **NOT_RUN**. No numeric placeholder replaces an unexecuted metric. No formal 36-pair experiment was launched because the model-integrity and smoke gates were not met. The original 36 pairs and order were retained. CPU regression suite: **23/23 passed**. No resampling, relabeling or filtering occurred.

## D. Scientific judgment

Verified facts: environment and original manifest exist; CPU tests pass; tested network transfers fail repeatedly; both pinned models remain incomplete. Engineering inference: measured effective transfer cannot finish within this task's remaining budget. Unverified: real model loading, multimodal generation, parsing coverage, VRAM and any research effect. No available complete small multimodal snapshot was identified in the user's HF cache or experiment directory; roberta is text-only and the partial 27B cache is not a suitable fallback. A smaller model download was not started because the same transfer instability remains unresolved; no 4B result substitutes for H1. This was a targeted personal-cache inventory, not a claim about every file on the shared server.

No conclusion about a stable generalization defect or causal mechanism is supported. Expansion to 90 pairs is not justified before the original smoke/36-pair gates and independent human counterfactual validity review. The practical next requirement is a working authorized network path; no user authentication requirement was observed.

## E. GitHub

Branch: `experiments/h1-k0-triggerbench-20261106`; no merge to main. Commit identity is the commit containing this report (reported separately after push to avoid a self-referential SHA). Evidence directory: `03_experiments/h1_k0_triggerbench/runs/h1_autonomous_20261116_064613/`. Downloader: `scripts/download_verified.py`. Unresolved: full model acquisition and all GPU/research gates. Full local diagnostic files remain in the corresponding personal run directory.
