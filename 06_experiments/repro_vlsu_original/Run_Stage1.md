# Stage 1 CPU-only image availability

The downloader verifies the original Apple CSV by SHA-256, Git blob and Stage 0 release assertions before creating a queue. Each exact URL is requested as a single source and linked back to all release UUIDs. The code is independent of Apple's download helper, which is licensed under the Apple Sample Code License and was inspected for comparison. Dataset license CC BY-NC-ND 4.0. Rights for third-party images remain with their respective sources. [Apple release](https://github.com/apple-aiml-research/ml-vlsu/tree/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28)

## Execution and local artifacts

From this directory, provide the official CSV path. Python uses Pillow, PyYAML and pytest for the test suite. `--dry-run` is the default. The example makes a bounded initial smoke acquisition, resumes it and checks a second completed resume. The full phase requires the smoke gate in the same state database.

```bash
export VLSU_PINNED_CSV=/path/to/VLSU.csv
python -m pytest -q
git diff --check
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --phase smoke --dry-run
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --phase smoke --execute --max-requests 12
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --phase smoke --execute --resume --max-requests 210
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --phase smoke --execute --resume --max-requests 0
python scripts/stage1_download.py --csv "$VLSU_PINNED_CSV" --phase full --execute --resume
python scripts/stage1_report.py --csv "$VLSU_PINNED_CSV"
```

A request-budget pause returns 2 and preserves completed work. SIGINT lets active workers finish or checkpoint within their time limits. Reuse the same `--root` for resume and report. The default is `.local/stage1/`. A configured external root must be private and outside tracked files. The durable SQLite event log records requests, replies, download outcomes and decode verdicts. Content-addressed objects and bounded partials stay private. The report emits an immutable snapshot under `.local/stage1/snapshots/` and a local failed-UUID JSONL. Only aggregate files and manifest hashes are published. To copy the results, verify the referenced snapshot SHA-256 and each required cache object's digest. `validate_predictions` checks exact UUID membership and gold from this snapshot and the pinned CSV before future scoring.

Replies, redirect chains, intermediate errors and terminal outcomes are recorded separately. A source is terminal on an access denial, confirmed missing URL, permanent validation failure or exhaustion of the retry budget. Existing verified objects are rehashed before resume. Failed terminal records and hashes remain evidence. A separate run root would be required for a deliberate freshness check, with separately identified signatures and preserved prior manifests. No alternate sources are queried. Pillow verify and first-frame decode run in a time- and memory-bounded subprocess. Stage 1 tests record offline HTTP behavior and separately exercise the production TLS hostname and pinned-peer checks with socket doubles.

## Recovering a resolver outage

Use the [Stage 1R network gate and migration procedure](reports/stage1r/Move_Resume_Instructions.md) before attempting a live recovery.

When recent attempts show a sustained resolver fault, the runner checks two public DNS controls through the same resolver without making HTTP requests. If both fail it pauses. After connectivity returns, add `--retry-environment-dns` to the smoke resume command once to reopen only terminal transient DNS failures. Previous attempts and successful objects are retained. Origin access restrictions stay terminal. Pending DNS attempts can resume under their existing budgets.

## Gates

The smoke scope is deterministic (seed 20261119) and includes both released duplicate-URL groups. A full run can start only after the offline suite has passed, all smoke sources have terminal evidence, at least one image has verified decode and a separate completed smoke resume admits zero requests. A network budget, cooldown, interrupt or disk reservation can pause full acquisition without closing the coverage denominator. The report records observed availability and pending rows. Model results are NOT RUN. Figure 4/5 statistics still require three valid model predictions per UUID on the reported input intersection.

The Stage 0 independent human prompt review remains OPEN. The author image-area interpretation, Qwen precision and revisions remain UNKNOWN. Image identity and semantic consistency with author-cached originals remain UNKNOWN.
