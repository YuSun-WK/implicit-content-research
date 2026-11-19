# TRACE-S1A · 门禁与交接

| 门禁 | 判定 | 证据 |
|---|---|---|
| G1 授权 FHM 和 Train/Dev 图文标签 | `MANUAL_DATA_ACTION_REQUIRED` | 项目路径和归档索引无确认原件，官方 Data Download 要求登录 |
| G2 固定 CLIP 权重 | `VERIFIED_AND_LOADED` | 8/8 文件 SHA-256 一致，实际 CPU `CLIPModel` 加载通过 |
| G3 作者原始两列 Caption | `BLOCKED` | 未找到可追溯原件，诊断模式独立于本门禁 |
| G4 真实 GPU 优化器、计时及 Checkpoint | `TRAINING_NOT_RUN` | 实际 FHM 批数和 CUDA 更新次数均为 0 |
| G5 最多 100 批稳定性与无泄漏审查 | `BLOCKED` | 尚无通过的真实 Smoke 或短跑日志 |

**正式 Baseline 训练 `BLOCKED`。** 下一轮优先取得授权 FHM 并核查官方 split、图片和原始文字。固定权重已就绪。取得合法数据后，用 `trace_text_only_diagnostic` 做单卡 BF16、Microbatch 1 的真实更新与恢复，随后按门禁做短跑。作者两列 Caption 另行走来源核验，齐备后才可开始 `trace_original`。论文对齐的投影分类 baseline 需要另有实验协议。

[数据入场与人工动作](Stage1A_Data_Access_Gate.md) · [权重报告](Stage1A_Model_Weights_Report.md) · [训练证据](Stage1A_GPU_Smoke_100Batch.md) · [运行方式](Stage1A_Mode_Semantics.md)
