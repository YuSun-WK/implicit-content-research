# A0 original prompt failure evidence

The frozen author prompt, model and `reproduction_parser_v3.0.0` generated 42 original predictions in Stage 1. The A0 Smoke generated 6/6 with 4/6 unique labels. The independent A0 validation generated 36/36 with 20/36 unique labels (55.56%), 35/36 complete five-stage structures, 11 `AMBIGUOUS_TEMPLATE`, and 5 `EXTRA_TEXT`. It therefore failed the frozen 35/36 parse threshold. The 11 ambiguous outputs repeat both label options from the original prompt. Four of the five extra-text outputs have an anonymized raw-only semantic transcription of Unsafe, but even accepting all four would yield only 24/36 (66.67%). That sensitivity calculation does not change A0 predictions or metrics.

The A0 validation strict full-denominator accuracy is 47.22%, Unsafe F1 is 0.7647, and PairAcc is 11.11%. Its valid-only accuracy of 85% uses only 20/36 labels and 3/18 complete pairs. It cannot be presented as the formal Test result or directly compared to the author's Table 1 figure.

Source evidence: `runs/smoke_20261119_recovery/`, `runs/validation_20261119_recovery/`, `runs/recovery_cpu/final_gate_status.json`, and `artifacts/parser_freeze.json`. The Stage 2 protection ledger records their SHA256 before new work.
