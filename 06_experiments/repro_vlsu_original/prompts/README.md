# ICLR 2026 prompt manifest

Source SHA-256 `b38dc2e84d20899132125338b3ef8d31f54873660c2562c281c4d992c1f96aa8`.
Use the 44-page PDF released by the conference. [Proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)

| TXT | PDF and printed page | Review |
|---|---|---|
| `binary.v1.txt` | p.33 D.1 binary box | Assistant line-by-line cross-check using plain and layout extraction |
| `direct.v1.txt` | p.33 D.1 three-class box | Assistant line-by-line cross-check using plain and layout extraction |
| `structured_cot.v1.txt` | p.35 D.3 box | Assistant line-by-line cross-check using plain and layout extraction |

Independent human sign-off is pending. The extraction preserves wording, case, punctuation, and line wraps from the box text as exposed by pypdf 6.16.2. The v1 files use UTF-8 and one terminal LF. PDF typesetting whitespace can differ from author runtime prompt bytes, which are UNKNOWN. The extractor emits the three TXT files under ignored `.local/prompts/` from the hash-pinned source. The committed config pins each output hash. Redistribution permission for verbatim prompt files was unconfirmed.

```bash
python scripts/extract_paper_prompts.py --pdf /path/to/iclr-vlsu.pdf
```
