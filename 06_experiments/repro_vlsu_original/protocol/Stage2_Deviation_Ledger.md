# Stage 2 author protocol and local choices

**ENGINEERING SMOKE / PARTIAL REPRODUCTION.** The exact published model family/size is the target. Stage 2 uses the existing verified images independently of Stage 1 exhaustion. The 10 selected UUIDs are a stratified engineering cohort from the 30 currently decoded release UUIDs. This case mix cannot support Table 1/2/4 metrics, Figure 3/4/5 claims, or author-level reproduction.

| Component | Proceedings and official release | Local smoke |
|---|---|---|
| Model | Table 10 names `Qwen/Qwen2.5-VL-7B-Instruct`. Author weight, processor, tokenizer revision and precision UNKNOWN | Target public revision `cc594898137f460bfe9f0759e9844b3ce807cfb5` for all components, verified metadata and weight pointers. Local BF16 is preferred. An in-memory bitsandbytes NF4 4-bit load from identical base bytes is RESOURCE-CONSTRAINED PARTIAL REPRODUCTION |
| Prompts | D.1 p.33 binary/direct, D.3 p.35 CoT | Re-extracted from pinned proceedings PDF and all SHA-256 matched the Stage 0 lock. PROMPT HUMAN SIGNOFF OPEN |
| Input template | Message roles, order, system message, chat representation UNKNOWN | One user message with image then text containing the exact extracted template, newline, and official query. No explicit system message. The pinned Qwen chat template can supply its own default system text. Record the template digest |
| Preprocess | Table 10 writes min 256/max 1280. Effective units and author preprocessing UNKNOWN | Qwen reference candidate 200,704–1,003,520 pixel area, first frame, EXIF transpose, RGB and fast pinned processor. Record input and visual token counts and the image grid |
| Generation | Max Len 1024 direct/binary and 2048 CoT. Effective default temperature, sampling, beams, stop rules and seed UNKNOWN | Local `max_new_tokens` 1024/1024/2048, greedy, one beam, no temperature/top-p/top-k override used for sampling, model configuration EOS and padding, seed 20261119, SDPA. Explicit shorter trials carry ENGINEERING_SHORT_OUTPUT and a distinct run ID |
| Single modalities | Table 4 compares the corresponding modality label. Exact single-modality prompt bytes UNKNOWN | NOT RUN. Any future single-modality prompt must be labeled LOCAL ADAPTATION with its own gold |
| Output and score | Author F1 averaging and invalid handling UNKNOWN | Independent Stage 0 closed-set parser and separate status ledger. CoT requires one final field on the final nonblank line. No author-comparison F1 emitted |
| Data | Paper reports 8,187 images/queries. Exact image bytes and inference UUIDs UNKNOWN | 8,159 pinned release rows, 30 available Joint inputs at the frozen snapshot. Current roster stays fixed across any further image acquisition. Diagnostic binary and CoT use the same first 5 of the 10 Direct UUIDs |

[ICLR proceedings PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf) · [Pinned Qwen revision](https://huggingface.co/Qwen/Qwen2.5-VL-7B-Instruct/tree/cc594898137f460bfe9f0759e9844b3ce807cfb5)
