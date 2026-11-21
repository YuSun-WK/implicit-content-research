# Stage 2｜真实 MultiOFF GPU Smoke 与 100 Microbatch

本页数值均来自本轮真实单卡运行日志，数据为原作者发布的 MultiOFF 完整样本子集及本轮 InternVL 增强 Caption。权重、Caption 和 Checkpoint 保存在 Git 忽略的私有目录。GPU 为 NVIDIA GeForce RTX 4090，精度 BF16，作者 OpenCLIP 权重 SHA-256 已核验。

| 探测物理 Batch | 真实 AdamW 更新 | 单步秒 | 总 Loss | 对比 Loss | 峰值 PyTorch reserved GiB | 分类器最大参数差 |
|---:|---:|---:|---:|---:|---:|---:|
| 2 | 1 | 1.565 | 0.249219 | 0.138672 | 1.311 | 0.00010003 |
| 4 | 1 | 1.660 | 0.458544 | 0.488037 | 1.318 | 0.00010003 |
| 8 | 1 | 2.230 | 0.433003 | 0.611664 | 1.303 | 0.00010003 |
| 16 | 1 | 2.494 | 0.669043 | 1.401794 | 1.309 | 0.00010003 |
| 32 | 1 | 7.123 | 0.732836 | 1.533401 | 1.566 | 0.00010003 |

B=2 首批三项未加权 Loss 分别为 Classification **0.105664**、Contrastive **0.138672**、Relevance **0.145647**，加权总损失 **0.249219**。裁剪前总梯度范数 **7.377794**；Scorer **4.000646**、训练文本末层 **1.068180**、图像投影 **1.283424**、文本投影 **1.200668**、正反向融合 **0.965276 / 1.036782**、pre-output **4.864090**、分类器 **2.920761**。视觉塔梯度为零。每种 Batch 均实际执行 `optimizer.step()`、原子 Checkpoint 保存与同进程回读。[私有原始运行日志](.local/s2-smoke-b2/events.jsonl) 在服务器保留，发布的脱敏副本见 `stage2_smoke_b2_events.jsonl`。

短跑选物理 Batch **32**、梯度累积 **4**、目标有效 Batch **128**，严格限制 **100 Microbatch**。第 50 批后结束进程，随后在新进程加载 `last.pt` 恢复到第 100 批。实际 **100 批、29 次 AdamW 更新**；每次相邻 Checkpoint 间隔不超过 25 批，恢复日志含第 50 批和续跑事件。全部三项 Loss 有限。全 100 批单步耗时 p50 **6.333 秒**、p95 **7.431 秒**；进程峰值 allocated **2.015 GiB**、reserved **2.197 GiB**。这两个内存值为 PyTorch 进程实测峰值，设备上其他进程占用另见事件中的 `device_free_bytes`。没有从短跑权重继续正式训练。

主要证据：`stage2_smoke_b2_events.jsonl`、`stage2_smoke_b4_events.jsonl`、`stage2_smoke_b8_events.jsonl`、`stage2_smoke_b16_events.jsonl`、`stage2_smoke_b32_events.jsonl`、`stage2_short_events.jsonl`。日志仅含数值、配置与 SHA，无原始文本或样本级预测。
