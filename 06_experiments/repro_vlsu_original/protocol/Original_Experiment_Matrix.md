# VLSU ICLR 2026 original experiment matrix

**AUTHOR-REPORTED** identifies evidence from the hash-pinned proceedings PDF. **VERIFIED-OFFICIAL-CODE** identifies behavior inspected at the fixed Apple revision. **LOCALLY REPRODUCIBLE / LOCAL REPRODUCTION** applies to the CPU audit and evaluation rules. **PARTIAL REPRODUCTION** is the intended scope of later experiments on the public release. **NOT RUN** means no local experiment result. **UNKNOWN** marks an unresolved source detail. Pages refer to the conference PDF; hashes and extraction are in the [prompt manifest](../prompts/README.md).

CSV gold abbreviations are I = `image_grade`, T = `consensus_text_grade`, J = `consensus_combined_grade`. S/B/U are Safe/Borderline/Unsafe. Counts in the local column are theoretical eligibility ceilings derived from the published CSV. The paper dataset totals 8,187 according to §3, Table 7 and §F.2. Exact evaluated UUIDs and effective denominators are UNKNOWN unless evidence is specified. Author F1 averaging and any positive class are UNKNOWN throughout. All metric pairs below are Accuracy/F1 in percent. Q7/Q32/Q72 stand for the three Qwen2.5-VL Instruct sizes whose checkpoint IDs are reported below.

| Source | Task, modalities, gold, mapping | Prompt and model settings | Author metrics and sample evidence | Apple eval implementation | Local scope and missing information |
|---|---|---|---|---|---|
| Table 1 p.5, §4.1 | Joint binary safety on VLSU (J, S/B→Safe, U→Unsafe) | D.1 p.33 [binary](../prompts/README.md), 17 VLMs and human oracle, D.4 open-model settings | Q7 50.0±1.1/55.3; oracle 94.3±0.3/91.0; bootstrap 10,000 iterations. Exact evaluated UUIDs and F1 implementation UNKNOWN | UNKNOWN, no release script | PARTIAL / NOT RUN, 8,159 max, direct binary generation. Other benchmarks outside scope |
| Table 2 p.7, §4.3 | Joint three-class standard vs structured CoT, J S/B/U | D.1 p.33 [direct](../prompts/README.md) and D.3 p.35 [structured CoT](../prompts/README.md); Gemini-1.5, Gemini-2.5, GPT-4o, Q7, Q32; Qwen Max Len 1024/2048 | Standard → CoT: Q7 49.4/42.3→52.1/51.4, Q32 63.3/63.5→61.9/62.7, Gemini-1.5 62.0/62.2→63.1/63.2, Gemini-2.5 65.4/65.3→64.1/64.3, GPT-4o 51.3/45.8→56.5/54.4 | UNKNOWN, no release script | PARTIAL / NOT RUN, up to 8,159 same-UUID pairs. Exact paired author roster and invalid policy UNKNOWN |
| Table 3 p.7, §4.4 | Joint response behavior under two instructions. J S/B/U strata, refusal as binary judge outcome | Harmless and Helpful generation instructions referenced in §4.4. D.2 pp.33–34 gives GPT-4o evaluation prompts. Gemini-1.5 and Q32 | Refusal % (S/B/U): Gemini Harmless 34.7/62.4/90.8, Helpful 4.6/10.4/53.9; Q32 Harmless 12.9/23.4/71.2, Helpful 22.7/30.7/57.5. No F1 | UNKNOWN, no release script | NOT RUN. 8,159 joint pairs max per framing. Full behavior instructions, exact model/judge revisions and evaluated strata sizes UNKNOWN |
| Table 4 p.8, §5 | Three-class safety on image-only I, text-only T, joint J. S/B/U retained | D.1 p.33 joint [direct](../prompts/README.md), separate image/text prompts UNKNOWN. GPT-4o, Gemini-1.5, Gemini-2.5(R), Q7/Q32/Q72. Qwen direct Max Len 1024 | In I/T/J order: GPT-4o 71.8/66.3, 79.0/66.7, 51.3/45.8; Gemini-1.5 70.7/65.7, 69.0/62.4, 62.0/62.2; Gemini-2.5(R) 72.2/67.4, 80.6/72.3, 65.4/65.3; Q7 65.2/48.0, 60.3/44.2, 49.4/42.3; Q32 67.6/60.6, 80.8/71.3, 63.3/63.5; Q72 69.8/64.6, 75.2/64.9, 60.8/60.8 | UNKNOWN, no release script | PARTIAL / NOT RUN, 8,018/8,159/8,159 eligible. Author handling of uncertain image labels and invalid predictions UNKNOWN |
| Figure 3 p.6, §4.2 | Joint three-class accuracy by 17 true I–T–J patterns, J as gold | Joint D.1 task; GPT-4o, Gemini-1.5, Q7/Q32/Q72 and human oracle | §4.2 describes ∼90% for U-U-U and ∼20–55% for S-S-U across models. Plotted precision only. See Figure 9 p.17 for pattern statistics; actual prediction denominators UNKNOWN. No F1 | UNKNOWN, no release script | PARTIAL / NOT RUN. 8,016 in paper patterns, 2 extra standard, 141 uncertain shown separately. Wilson CI is local |
| Figure 4 p.8, §5 | Three-class prediction agreement. Image vs joint and text vs joint, with J splitting all/joint correct/joint wrong | §5/Table 4 modes. Figure model identity and image/text wrapping UNKNOWN | κ in all/correct/wrong order: image 0.379/0.372/0.391, text 0.421/0.576/0.154. Printed cells sum to 8,335/5,279/3,056 in both comparisons. No F1 | UNKNOWN, no release script | PARTIAL / NOT RUN; ≤8,018 valid-gold aligned UUIDs, before missing images and invalid predictions. Author cohort accounting UNKNOWN |
| Figure 5 p.8, §5 | Joint error attribution using same-UUID I/T/J predictions against own three-class gold | §5/Table 4 modes; chart explicitly Q32 | Image wrong only 32.3%, text wrong only 25.9%, both wrong 7.9%, both correct 33.8%. Joint errors as denominator. Figure 18 p.39 gives 2,991 Q32 errors. No F1 | UNKNOWN, no release script | PARTIAL / NOT RUN on Q7, ≤8,018 before availability and parsing. Author intersection and invalid policy UNKNOWN |
| Appendix E.1, Table 11 p.37 | Binary benchmark extension for VLSU, J S/B→Safe | D.1 binary; 17 VLMs and oracle as in Table 1 | VLSU Q7 F1 55.3, oracle F1 91.0. F1 only, same unresolved averaging | UNKNOWN, no release script | PARTIAL / NOT RUN, VLSU only up to 8,159 |
| Appendix E.2, Figures 16–17 pp.37–38 | I/T/J three-class accuracy by true pattern, score each against own gold | Table 4 modes, GPT-4o and Q32; Qwen direct Max Len 1024 | Q32 text B about 18–40%, S/U >75%, §E.2; curves are plotted. Exact evaluated UUIDs UNKNOWN. No F1 | UNKNOWN, no release script | NOT RUN. Local mode ceilings as in Table 4, or up to 8,016 for a paired analysis across the Figure 9 patterns |
| Appendix E.3, Figure 18 pp.38–39 | Four joint-error groups using I/T/J, as Figure 5 | GPT-4o, Gemini-1.5-Flash, Q7/Q32/Q72; Table 4 modes | Q7 4,121 joint errors, 49.7% accuracy, shares 19.7/39.7/23.7/17.0 (image only/text only/both wrong/both correct). Q32 2,991/63.5%; Q72 3,193/61.0%; Gemini 3,111/62.0%; GPT-4o 3,963/51.6%. No F1 | UNKNOWN, no release script | PARTIAL / NOT RUN for Q7, ≤8,018. Author cohort and invalid policy UNKNOWN |
| Appendix E.4, Table 12 p.39 | Joint behavior per J S/B/U stratum, refusal and helpfulness | As Table 3. D.2 helpfulness rubric 1–10 with a separate refusal score | Refusals as Table 3. Helpfulness % S/B/U, Gemini 54.4/51.5/24.6→70.9/76.0/42.9; Q32 62.5/64.2/29.6→55.6/55.8/31.4. Exact aggregation details UNKNOWN. No F1 | UNKNOWN, no release script | NOT RUN; exact behavior prompts and judge release UNKNOWN; up to 8,159 per framing |

[ICLR 2026 proceedings PDF, §§2–5, A.3, D, E and F.2](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)

## Model, implementation and source gaps

- **AUTHOR-REPORTED.** D.4/Table 10 gives `Qwen/Qwen2.5-VL-7B-Instruct`, `Qwen/Qwen2.5-VL-32B-Instruct` and `Qwen/Qwen2.5-VL-72B-Instruct`. Max Len 1024/2048 for Q7/Q32 and 1024 for Q72. The API argument and stop behavior are UNKNOWN. D.4 reports default temperature for Qwen and InternVL-3, 0.0 for the other models, A100-SXM4-80GB, one GPU for models under 12B, four for Q32 and eight for Q72. GPT-4o has a documented refusal-phrase filter (pp.35–36). Its resulting labels/denominators and the general parser are UNKNOWN. Author Qwen checkpoint, tokenizer and processor revisions, precision, dependency versions, seed, effective decoding values (temperature, sampling, beams, stopping), system message and image/text chat wrapping are UNKNOWN.
- **AUTHOR-REPORTED.** Table 10 writes `pixels: min=256, max=1280` for Qwen. **VERIFIED QWEN REFERENCE CODE.** Qwen documents 256–1280 as an example visual-token range, converted with a factor of 28 per side to 200,704–1,003,520 pixel area. The reference image utility uses `IMAGE_FACTOR=28` and constrains resized area. This is a candidate local conversion. The authors' actual unit, image RGB/orientation and resizing path, processor overrides and cached image bytes are UNKNOWN. [Qwen README](https://github.com/QwenLM-corp/Qwen2.5-VL/blob/a8fdb64927bad8fe499afe5f4f40562fb0b659b2/README.md) · [Qwen image utility](https://github.com/QwenLM-corp/Qwen2.5-VL/blob/a8fdb64927bad8fe499afe5f4f40562fb0b659b2/qwen-vl-utils/src/qwen_vl_utils/vision_process.py)
- **VERIFIED-OFFICIAL-CODE.** Apple HEAD `cbe363a26d2129ff1b526c283af0a2b7aa3d9b28` matches the source lock. README, two license files, one CSV, one results image and the image download utility are the full tracked tree. The download helper has a Pillow verify path, WebP conversion, file-signature fallback and a generic retry marker. Apple publishes neither inference/evaluation code nor the per-run prediction rosters in this tree. [Apple pinned tree](https://github.com/apple-aiml-research/ml-vlsu/tree/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28)
- **INTERNAL PAPER DIFFERENCES.** Figure 9 legend sums to 8,185 vs the Table 7 total 8,187. Several pie annotations differ from the legend, e.g. S-S-S 2,174 vs 2,175. The local pattern table identifies its reference count column as the legend. Figure 4 printed cells sum to 8,335, which exceeds the stated dataset size by 148. Figure 18 reports a different Q7 joint accuracy from Tables 2/4 (49.7% vs 49.4%). In §E.3, the prose describes ∼41% both-wrong for GPT-4o; Figure 18 labels 41.1% both-correct and 7.7% both-wrong. Causes and cohort relationships are UNKNOWN. Preserve each value at its source. [ICLR proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)

## Publication vs release

| Gold | Paper Table 7 (S/B/U) | Locked CSV (S/B/U/uncertain) |
|---|---|---|
| Image | 4,222 / 1,873 / 2,092 | 4,182 / 1,810 / 2,026 / 141 |
| Text | 4,335 / 1,451 / 2,401 | 4,328 / 1,452 / 2,379 / 0 |
| Joint | 2,186 / 3,312 / 2,689 | 2,189 / 3,310 / 2,660 / 0 |

Appendix F.2 describes a test-only split. The public CSV has 8,159 rows, a difference of −28, and 19 observed S/B/U patterns versus the paper's 17. Extra B-S-S and S-U-B appear once each. Six patterns contain image `not_sure`; all 141 rows have valid text and combined labels. S-S-U is 35 in the CSV vs 37 in the Figure 9 legend. The cause of the version gap and the UUIDs of the paper cohort are UNKNOWN. The README repeats the paper counts. Retain all release rows and show paper-pattern, extra, and uncertain group coverage independently. [CSV audit](../reports/stage0/CSV_Audit.md) · [Per-pattern audit](../reports/stage0/patterns.csv) · [Official release](https://github.com/apple-aiml-research/ml-vlsu/tree/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28)

P038 was checked at main `985901a5c4830ac1f46dcad4884fbeee7bb82102`. PR #78 was checked at its independent head `39ca54e8238b7a0f3ba01fd65e5c23708aa0f806`. Its 108/132 decodes describe that earlier stratified sample. Release-wide availability is NOT RUN. [P038](https://github.com/YuSun-WK/implicit-content-research/blob/985901a5c4830ac1f46dcad4884fbeee7bb82102/01_literature/cards/P038_VLSU.md) · [PR #78](https://github.com/YuSun-WK/implicit-content-research/pull/78)

## Table 1 VLSU values for the remaining models

The entries are author-reported Accuracy/F1 (%) for the VLSU column. The preceding matrix gives Q7 and the oracle.

| Model | Accuracy | F1 |
|---|---:|---:|
| GPT-4o | 48.8±1.1 | 54.1 |
| Gemini-1.5 | 67.3±1.0 | 64.1 |
| Gemini-2.5(R) | 78.4±0.9 | 70.9 |
| o1(R) | 83.0±0.8 | 70.7 |
| o3(R) | 80.8±0.9 | 70.5 |
| GPT-5(R) | 81.6±0.8 | 74.6 |
| Haiku-4.5(R) | 81.6±0.8 | 74.6 |
| Sonnet-4.5(R) | 75.4±0.9 | 68.3 |
| Phi-3.5V | 56.0±1.1 | 59.0 |
| LLaVA1.5 | 70.0±1.0 | 62.7 |
| InternVL3 | 65.5±1.0 | 63.3 |
| GLM4.1V(R) | 40.8±1.1 | 51.9 |
| LLaVA-CoT(R) | 67.0±1.0 | 53.3 |
| Gemma3 | 67.4±1.0 | 65.7 |
| Q32 | 66.6±1.0 | 64.7 |
| Q72 | 66.7±1.0 | 65.0 |

[ICLR proceedings PDF, Table 1 p.5](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)
