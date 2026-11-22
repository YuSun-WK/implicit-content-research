# Stage 2.1｜MultiOFF Caption 修复协议

研究对象为 **TRACE-InternVL-only-MultiOFF-2caption (Adapted Reproduction)**。旧版 740 条 InternVL Caption 保存在 Git 外的 `~/data/trace-assets/multioff/trace_internvl_only/records.json`；本轮新清单单独保存在 `~/data/trace-assets/multioff/trace_internvl_only_repaired_v2/records.json`。脚本只读旧版，按旧清单 SHA、官方 CSV 的 Split、原行号、图片名和图片 SHA 对齐。

用训练时相同的 `open_clip.tokenizer.HFTokenizer`（`roberta-ViT-B-32`，固定 revision `e22e1c12b0a1ba4af9fb6474626585351ea0da25`，`context_length=77`）底层 `encode(caption, add_special_tokens=True)` **不截断**计数。旧版实测 334 条超出 77，406 条合格。合格项必须逐字保留。

只对超长项调用固定 `OpenGVLab/InternVL2_5-8B@e9e4c0dc1db56bfab10458671519b7fa3dd29463`，BF16、单卡、仅推理。提示输入原图、现存 RAM++ tags、GroundingDINO 定位摘要、原始 Meme 文字与原有 Caption；不读取分类标签。要求将视觉实体、动作、关系和必要的图文交互改写成一句简洁 Caption。最多三次，逐次收紧目标词数为 45、35、25；每次均以 OpenCLIP 原始 Tokenizer 重新验收。拒绝直接复制原始文字、包含分类标签词的输出与任何超过 77 tokens 的输出；**不截断，不将失败输出标记合格**。

每条成功修复在私有 `repair_audit.json` 中记录旧/新 Caption SHA-256、旧/新 token 数、尝试数、每次提示 SHA、InternVL revision 与原图 SHA。每 25 条以内原子保存新 Manifest 和审计文件，支持恢复。仓库仅发布按 Split 聚合的统计和失败稳定 key，不发布图片、Caption 文本、原始标签或模型权重。

**训练门禁：** 740/740 对齐且非空、406 条合格原文完全不变、334 条均有成功修复记录、全部 Caption ≤77 tokens、无原文直接复制。`stage2_train.py` 在加载 OpenCLIP 模型前再次以相同 Tokenizer 对全量新 Manifest 执行长度检查。任一门禁失败，禁止 Stage 2.2 正式训练。
