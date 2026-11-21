# Stage 2｜审稿门禁与下一步

本轮目标 **TRACE-InternVL-only-MultiOFF-2caption (adapted reproduction)** 已真实运行完成。判定为 **`DELIVERED_WITH_PERFORMANCE_LIMITATIONS`**；不得称作论文三候选、最佳 XLM-R ViT-H/14 条件的严格数值复现。

| Gate | 判定 | 证据 |
|---|---|---|
| G1 数据与官方模型 | PASS | MultiOFF 官方完整样本 444/148/148；RAM++、GroundingDINO、InternVL 和 OpenCLIP 固定版本文件 SHA-256 校验。[数据审核](Stage1C_MultiOFF_Data_Audit.md) · [资产清单](Stage2_Model_Asset_Manifest.json) |
| G2 Caption 生成 | PASS | 10→50→740 条真实样本依序运行，740/740 正确键对齐且非空；334/740 超过 77 token。[覆盖](Stage2_Caption_Coverage_Manifest.json) · [流程](Stage2_InternVL_Caption_Pipeline_Audit.md) |
| G3 全部核心模块 | PASS | 作者 OpenCLIP 与 Classifier 实际装配；二候选、Scorer、训练 hard Gumbel、末层文本、两向融合、三项 Loss 均执行。[架构](Stage2_2Caption_TRACE_Architecture_Parity.md) |
| G4 真实 GPU Smoke | PASS | B2 真实前反向、AdamW 更新、各训练组非零梯度、视觉塔冻结、Checkpoint 保存回读；三项 Loss 有限。[日志](stage2_smoke_b2_events.jsonl) |
| G5 稳定性 | PASS | B2/4/8/16/32 单批探测；B32 100 Microbatch、29 更新，第 50 批跨进程恢复，Checkpoint 间隔 ≤25。[报告](Stage2_GPU_Smoke_100Batch.md) |
| G6 正式训练 | PASS | seed 42 与预设重复 seed 121 各 6 Epoch、84 Microbatch、24 更新；Dev 选 Epoch 1，均低于 6 小时及 18 GiB。[正式训练](Stage2_Complete_TRACE_Training_Report.md) |
| G7 最终 Test | PASS | 每个种子只在 Dev 选模完成后评估一次 Test，阈值固定 0.5，精度与混淆矩阵来自数值日志。[seed 42](Stage2_Training_Summary.json) · [seed 121](Stage2_Training_Summary_Seed121.json) |
| G8 有界坍缩排查 | PASS | 仅检查 Train/Dev 最佳与末状态概率及末 10 次更新梯度；未用 Test 调参。[诊断](Stage2_Dev_Collapse_Diagnostic.json) |

两次正式结果暴露性能风险：seed 42 Test 只预测 **12/148** 正类，Offensive F1 **0.1449**；seed 121 预测 **0/148** 正类。后续分析不得把 seed 42 的 Macro F1 高于旧 ViT-L/14 baseline 直接归因于 Caption 或 Relevance，因为 backbone、候选和训练协议不同。

**下一轮唯一优先实验：**在相同 OpenCLIP backbone、相同 740 样本、相同划分与固定 0.5 阈值下，预先锁定一个“仅原始文字”的同条件控制运行，保持其余训练与 Dev 选模规则一致，并以 seed 42/121 比较正类召回和概率分布。此项控制可检验二候选机制与当前全负类退化的关系；不要在 Test 上反复筛选配置。原论文严格同条件复现仍需作者原始增强 Caption、实际训练配置和对应 checkpoint。
