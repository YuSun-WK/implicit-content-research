# TRACE-S1B · 门禁与交接

| 门禁 | 判定 | 本轮证据 |
|---|---|---|
| G1 官方 FHM 入场 | `MANUAL_DATA_ACTION_REQUIRED` | 指定候选目录不存在，未收到许可确认，读取 0 条 FHM 记录 |
| G2 固定 CLIP | `VERIFIED_AND_LOADED` | 复用现有固定 revision，8/8 SHA-256 通过，预训练 CLIP 实际 CPU 加载通过 |
| G3 实验模式 | `AUTHOR_CAPTIONS_BLOCKED`（`trace_original`） | 作者两列原件仍未验证。单文本诊断只依赖 G1/G2 输入，保留作者网络与分类损失 |
| G4 单批 GPU smoke | `TRAINING_NOT_RUN` | 0 个真实 FHM Batch，0 次 CUDA AdamW 更新 |
| G5 短跑与中断恢复 | `BLOCKED` | 0/100 Microbatch，无真实 GPU Checkpoint 恢复证据 |

**Stage 2 `BLOCKED`。** 下一轮继续 S1B。先验收用户确认许可的官方数据，再执行单文本诊断的 GPU 单批更新及 Checkpoint 回读。G4 和 G5 均通过后复核 Stage 2。本轮未制定正式训练方案。

作者 TRACE 固定提交仍为 `83ecb799f897fe275185e082ee9a669f7d04bfaa`，训练路径解冻文本块 4、7、10。诊断只用原文字和分类损失。论文 Table 4 的 projection-only CLIP 对照是独立协议。

[正规数据入场](Stage1B_Data_Manifest.md) · [CLIP 离线校验](stage1b_clip_validation.json) · [Smoke](Stage1B_Smoke_GPU.md) · [100 Microbatch](Stage1B_100_Batch_Report.md)

2026-11-20 再验收：G1 仍为 `MANUAL_DATA_ACTION_REQUIRED`，G2 离线复核通过，G4/G5 未执行。详见 [本轮门禁、日志与下一步](Stage1B_Retry_20261120.md)。
