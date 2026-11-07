# H1-K0 recovery run final report

Run ID: `h1_k0_recovery_20261107_034443`. Source run: `h1_k0_20261106_065826` (unchanged).

## Completed

The original fixed 36 Test pairs are preserved. Both missing `test/misinformation/45` images were recovered from partial files and passed Pillow decode. All 72 images have distinct SHA256 values; visual causal validity remains pending human review. Nine CPU unit tests passed for strict evaluation and output parsing.

## Model and results

No model was loaded. ThinkingGuard-8B revision `76892f9768ce828268265171f4bbc5dfb75eafc3` could not be fully downloaded after bounded Hugging Face, aria2c and curl attempts. Qwen3-VL-8B comparison was not started. GPU inference count and prediction count: **0**. Joint/Text-only/Image-only and official five-step outputs: **0**.

Accuracy, Unsafe F1, PairAcc, FNR, FPR, correct risk flip rate, parse failure rate and pair quadrants are **unavailable**, not zero. No confidence intervals can be computed.

## Engineering changes

`evaluate.py` now rejects duplicate, missing, mixed-revision and mislabelled INVALID records, and computes statistics per pair with INVALID explicitly counted as an error. `run_inference.py` pins model/processor revisions, resolves cached image paths, enforces a 20 GiB process allocation cap and post-generation check, checks unified output parse success, and isolates the ThinkingGuard five-step protocol with a final-Overall-only parser. These GPU paths remain untested because weights were unavailable.

## Anomalies and stop reason

The initial image recovery attempts failed, then succeeded through bounded partial-file resume. Weight transfer repeatedly failed with `ChunkedEncodingError`, TLS handshake and connection errors. The cache retains incomplete weights. At the observed download rate, completing the model and inference would exceed the run budget.

Raw local logs are retained in this run; GitHub copies must be sanitized. No original experiment predictions were modified.
