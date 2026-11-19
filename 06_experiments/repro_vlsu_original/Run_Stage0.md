# Stage 0 CPU reproducibility

The pinned release data audit passed. Stage 1 can begin with downloader implementation and HTTP integration fixtures. Full acquisition depends on validated Stage 1 transport and a bounded live smoke. GPU work remains outside Stage 0.

From this directory, with the pinned proceedings PDF and an Apple checkout available locally

```bash
mkdir -p .local
git -C /path/to/ml-vlsu cat-file blob 09421adeb2e68eac1d5e829dcbd48848f21a0be6 > .local/VLSU.csv
python scripts/extract_paper_prompts.py --pdf /path/to/proceedings.pdf
python scripts/stage0_audit_csv.py --csv .local/VLSU.csv --out reports/stage0
python -m pytest -q
git diff --check
```

The audit and metrics scripts use Python's standard library. Prompt extraction was checked with pypdf 6.16.2 and the synthetic image checks with Pillow 11.1.0. See the execution log for commands and outputs. The audit returns 1 on a version or schema mismatch after writing diagnostics, or 2 on file access errors. The sample-level diagnostics file is private. Prompt TXT files are versioned by hash and generated locally from the conference PDF. Independent human verification is pending.

- [Original experiment matrix](protocol/Original_Experiment_Matrix.md)
- [CPU audit results](reports/stage0/CSV_Audit.md)
- [Evaluation rules](protocol/Output_Parsing_and_Metrics.md)
- [Image acquisition design](protocol/Image_Download_Design.md)
- [Execution transcript](reports/stage0/CPU_Run.txt)
