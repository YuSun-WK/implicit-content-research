# H1-K0 recovery review

Run ID: `h1_k0_recovery_20261107_034443`. Earlier `h1_k0_20261106_065826` remains unchanged.

## Actual work

- Reused the original 36 Test pair IDs and seed/order. Both missing `test/misinformation/45` images were recovered from partial downloads. All 72 images decode, and their 72 SHA256 hashes are distinct. No replacement candidate was used. Causal image review remains `pending_review`.
- Repaired strict paired evaluation. It now rejects duplicate/missing predictions, mixed model revisions/protocols, inconsistent INVALID status, and independent ground truth for Text-only/Image-only. INVALID counts as incorrect and is also reported separately.
- Repaired inference code with pinned model and processor revisions, cached image resolution, single visible GPU, a 20 GiB allocation cap, parsing gate, and a separate ThinkingGuard five-step condition whose parser reads only the final Overall verdict.
- Nine CPU tests passed. No GPU inference code path was exercised.

## Stopped before model load

ThinkingGuard-8B fixed-revision download failed under bounded Hugging Face, aria2c and curl retries. Incomplete weights remain in the local cache. No model was loaded; the Qwen3-VL-8B control was not started. `predictions.jsonl` is empty, `metrics.json` is `not_run`, and all requested classification metrics are unavailable.

## Outstanding audit points

1. GPU loading and inference paths remain untested, including the 20 GiB cap under real generation.
2. The official five-step protocol parser has CPU tests but no real model output validation.
3. The 36 image pairs need human review before causal counterfactual claims.
4. Existing CSV index versus image filename differences remain as documented in the first-run audit.

The GitHub archive contains redacted metadata and failure summaries. It excludes model bytes, dataset images, contact sheets, virtual environments, cache files and raw network logs.
