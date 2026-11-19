# Stage 2 决策

**BLOCKED。** Stage 0 准备与 CPU 检查完成，FHM 严格复现的运行门禁为 `DATA_BLOCKED`。

| 条件 | 状态 |
|---|---|
| 固定作者代码、算法审计与离线包装 | 已完成 |
| FHM 原图与相关 split 标签授权可用 | 未确认 |
| 作者两列原始 Caption 的覆盖和生成来源 | 未确认 |
| 固定 CLIP 本地模型权重 | 未发现 |
| 真实单 Batch、优化器更新、显存与恢复 | 未运行 |
| 最多 100 Batch 的稳定性与周期恢复 | 未运行 |

下一轮 Codex 任务为 **TRACE-S0 授权输入验收与单 Batch 实跑**。取得官方授权的图像、训练及开发标签和作者两列原始 Caption 后，先在本地核验来源、覆盖、占位值和重复记录，并验证官方 CLIP 快照哈希。准备好后对单卡 BF16 Microbatch 1 执行完整前向、反向、一次真实 AdamW 更新和 Checkpoint 恢复。有效梯度、权重变化和低于 18 GiB 的峰值证据齐备后，再跑最多 100 Batch 并重审 Stage 2。原始 Caption 继续缺失时，维持 `DATA_BLOCKED`。
