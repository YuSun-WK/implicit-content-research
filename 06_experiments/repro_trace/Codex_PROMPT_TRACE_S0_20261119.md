# Codex Task TRACE-S0: exact-code intake, data/caption gate, and 100-batch readiness
You are the PyTorch/CLIP reproduction engineer and evidence auditor for AAAI 2026 paper TRACE (AISI Special Track, CCF-A). Only work on TRACE in the repository YuSun-WK/implicit-content-research.

## INPUTS
- Repo branch: repro/trace-aaai2026-20261119
- Pre-audit: 06_experiments/repro_trace/TRACE_Stage0_Paper_Code_Audit_20261119.md
- Paper: https://ojs.aaai.org/index.php/AAAI/article/view/41220
- Official upstream: https://github.com/surrey-nlp/TRACE.git
- FIXED upstream commit: 83ecb799f897fe275185e082ee9a669f7d04bfaa
- Focus: clip_vitL_14_ft.py, utils/caption_selection.py, utils/loss_functions.py, vg_caption_gen.py; inspect benco_eval.py as secondary context.
- Hardware constraint: one RTX 4090/4090D, 16–20 GiB nominal available VRAM; no job >6h; NO paid APIs, no large-VLM finetuning.
- Existing local dataset/cache location is UNKNOWN; inspect responsibly, never assume it exists. User-provided credentials/tokens must NEVER be printed or committed.

## MANDATORY TASK ORDER (this invocation only)
1. Verify clean git state, confirm branch. Do not change main. Clone/download official TRACE at pinned commit into a local external source directory (or git submodule only if truly necessary; avoid bundling unneeded files); record upstream SHA and LICENSE.
2. Produce an evidence-based code map with relevant line numbers, showing training data schema, imports, model module graph, precise requires_grad trainable names/count, caption count/selection masks, loss gradient flow, tensor shapes, checkpoint behavior, evaluation threshold policy, and references to API services, RAM++, GroundingDINO, InternVL, Gemini. Explicitly inspect whether 'last four layers' matches upstream: it likely does NOT. Identify when forward duplicates visual/text encoders and when loss_config changes selection policy.
3. Scan LOCAL storage only in authorized project directories for FHM or TRACE JSON/JSONL, images, pre-generated captions and any authorized FHM download archive. Do not crawl sensitive unrelated directories. Do not attempt to bypass dataset license. If absent, mark DATA_BLOCKED. Do not fabricate data. Never upload copyrighted images or captions to Github.
4. Create a CSV/JSON-safe data manifest script that reads user-provided local paths (CLI args/env, not hardcoded /backup/girish_datasets) and reports ONLY metadata: split counts, label counts, image existence, duplicate IDs, candidate nonempty caption counts, 'No caption'/'nan' placeholders, exact source/provenance fields, max token lengths. It should NOT export raw meme text/images/captions. Validate FHM vs MultiOFF separately. If FHM official split label absent, explicitly mark and prevent test scoring.
5. Create minimal isolated env specification actually compatible with current Python/CUDA/torch, and capture dependency versions, NVIDIA GPU inventory/free memory. Keep original author's requirements intact, document every deviation. No installation touching global environment.
6. Prepare a NONINVASIVE configuration layer around the pinned author code: dry-run trainable-param report, adjustable data_path/image_root, train/dev split, local model cache, microbatch 1/2/4/8, gradient accumulation, <=100 train-batch cap, BF16/FP16 based on GPU, determinism seed, disabled wandb or offline, and output_dir. Preserve existing author model and scoring algorithms. Do not silently fix scientific differences in this task. Add short isolated minimal tests for shapes and missing caption handling. Add a non-test-leaking validation-only metric path as explicit 'evaluation fix', and retain a separate author-legacy metric for audit if needed.
7. If legal data AND model weights are already locally present and environment passes: run a 1-batch forward/backward and at least ONE actual optimizer.step() using smoke-only accumulation_steps=1, followed by checkpoint save+reload (no long run). Mark smoke-only effective batch as different from the formal paper protocol. Capture gradients of scorer, unfreezed text blocks, crossattn, projection, classifier and log_vars; confirm frozen visual tower grads remain none.
8. Only if 1-batch smoke passed, GPU <18 GiB peak, and dataset permission confirmed, execute <=100 batches on FHM training split with periodic checkpoints (<=25 batches between saves), record per-step wall time, cuda max_memory_allocated/reserved, loss components, CUDA OOM if any, and roundtrip save/resume. STOP at 100 batches; DO NOT start epochs or ablations. If preconditions absent, STOP before GPU and return clear blocker report, not synthetic performance figures.
9. Summarize whether strict reproduction is blocked by unavailable original Gemini/InternVL captions; do not replace those fields with BLIP/Qwen/etc. Discuss options only. Do not call Gemini or use paid API.

## ALLOWED MODIFICATION SCOPE
Only 06_experiments/repro_trace/** and .gitignore when needed to protect secrets and large data.
Do not edit 01_literature, 03_survey, VLSU, main, other experiments, or upstream originals outside a clearly recorded local wrapper.
No model weight, raw dataset, image, full caption dump, access tokens, WANDB credential, or substantial generated predictions containing sensitive content in commits.

## EXPECTED OUTPUTS (commit textual + small code artifacts)
- README.md with reproduction status/commands
- upstream_manifest.json (repository, exact commit, LICENSE, key file SHAs)
- TRACE_Stage0_Code_Map.md (file:line, real graph and gradient flow, discrepancy register)
- data_manifest.py and data_manifest_summary.json (metadata only, if data available)
- Caption_Availability_and_Provenance.md
- environment_probe.py and environment_report.md
- repro_config.yaml (safe defaults: dry-run, 1GPU, microbatch=2, no external APIs)
- checkpoint validation/gradient smoke tests, local-run logs if possible
- 100_batch_report.md (completed vs blocked, wall-time/memory/loss/checkpoint evidence)
- Gate_Decision.md with explicit GO / BLOCKED / NO-GO for Stage 2

## ACCEPTANCE CRITERIA
- Upstream commit hash and all key library/model revisions actually pinned or marked unknown.
- No 'official TRACE reproduced' claim without genuine original caption provenance.
- No CUDA memory over ~18 GiB without prior stop; no >6h training jobs.
- No validation/test threshold chosen using evaluation ground truth; include fixed 0.5 and dev-calibrated threshold.
- Diagnostic per-parameter requires_grad table, finite gradients, one checkpoint roundtrip for any executed training.
- No fabricated images, metrics, caption fields or test labels; empty manifest honestly recorded.
- Original code remain recoverable; protocol deviations tracked.
- Exit after Stage 0 + max 100-batch readiness, not full training.

## GIT / ROLLBACK
Before edits: git status, git rev-parse HEAD and record. Work only on repro/trace-aaai2026-20261119; create logically grouped commits (audit first, code second, optional smoke logs third). Push branch. Summarize hashes, filenames, any failures and exact commands executed. If tests fail, revert ONLY your new wrapper changes to last passing commit using git revert (never reset --hard or force-push; don't alter user's other work). Prepare a draft PR against main if authorized, but DO NOT MERGE. If branch has new remote changes, fetch/rebase safely and avoid overwriting.
Finally return a concise report in Chinese with gates, verified facts, unknowns, measured GPU data (if any), no-results state, and the EXACT next Codex task recommendation. Do not start Stage 2.
