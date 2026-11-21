# Stage 2｜TRACE-InternVL-only-MultiOFF-2caption 正式训练

**Adapted Reproduction。** 训练使用真实 MultiOFF Train 444 条；Dev 148 条只用于模型选择，最终 Test 148 条在选定 Checkpoint 后评价一次。两条候选是官方原始 `sentence` 与本轮固定 InternVL2.5-8B Caption。没有 FHM、Gemini、付费 API 或 InternVL 参数训练。[完整配置](Stage2_Training_Config.yaml) · [聚合训练日志](Stage2_Training_Summary.json) · [逐批数值日志](stage2_formal_seed42_events.jsonl)。

## seed 42 主运行

从固定预训练 OpenCLIP 与新初始化 TRACE 头开始，BF16、物理 Batch 32、累积 4、AdamW 1e-4、weight decay 0.01。最多 20 Epoch，Dev Macro F1 最优选择，patience 5，固定分类阈值 0.5。真实运行 **6 Epoch、84 Microbatch、24 次优化器更新**，第 6 Epoch 触发 Dev 早停，最佳为 **Epoch 1**。单次作业 **897.7 秒**，训练步时 p50/p95 **6.72/7.28 秒**；PyTorch 进程峰值 allocated/reserved **2.094/2.262 GiB**，低于 18 GiB 软门限。Checkpoint 在每个 Epoch 结束及相邻间隔不超过 25 批时保存并回读；best/last 文件仅存本地。[Checkpoint SHA 与大小](stage2_seed42_checkpoint_manifest.json)。

| Epoch | Train 总 Loss 均值 | Classification | Contrastive | Relevance | Dev Macro F1 | Dev 预测正类 |
|---:|---:|---:|---:|---:|---:|---:|
| 1 | 0.6882 | 0.1463 | 1.4640 | 0.1467 | **0.4776** | 8 |
| 2 | 0.5745 | 0.1414 | 1.1254 | 0.1363 | 0.3808 | 0 |
| 3 | 0.5156 | 0.1421 | 0.9415 | 0.1302 | 0.3808 | 0 |
| 4 | 0.4735 | 0.1324 | 0.8262 | 0.1332 | 0.3808 | 0 |
| 5 | 0.4580 | 0.1339 | 0.7819 | 0.1278 | 0.3808 | 0 |
| 6 | 0.4549 | 0.1314 | 0.7877 | 0.1247 | 0.3808 | 0 |

Train Loss 列为本轮逐 Microbatch 记录的 Epoch 均值，三个分量列为**加权前**均值。正式目标是 `cls + 0.3 cont + 0.7 rel`。Dev Macro F1 的 Epoch 1 优势来自固定 0.5 阈值；后续 Epoch 尽管总 Loss 降低，Dev 预测退化成全负类。按预先固定的 Dev 规则保留 Epoch 1，没有使用 Test 决定模型或阈值。[一次有界 Train/Dev 概率和末 10 次更新梯度排查](Stage2_Dev_Collapse_Diagnostic.json)显示末 Checkpoint 的 Dev 预测概率最大仅 0.4163，Scorer 与文本/融合/分类器仍有非零梯度。这表明阈值下的正类预测消失；不能单凭日志确定因果机制。

| 选定 Epoch 1 的评估 Split | N | Accuracy | Precision | Recall | Macro F1 | Offensive F1 | AUROC | 预测正类 | TN/FP/FN/TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Train | 444 | 0.5991 | 0.6053 | 0.1237 | 0.4686 | 0.2054 | 0.5943 | 38 | 243/15/163/23 |
| Dev | 148 | 0.6419 | 0.7500 | 0.1053 | 0.4776 | 0.1846 | 0.5307 | 8 | 89/2/51/6 |
| Test | 148 | **0.6014** | **0.4167** | **0.0877** | **0.4425** | **0.1449** | **0.5257** | **12** | **84/7/52/5** |

推理采用作者的 softmax 加权文本特征；下面“选择”按两条 Scorer 分数的 argmax 统计，表示倾向，不代表推理使用硬单条 Caption。Train 为原文 **217/444**、InternVL **227/444**；Dev **66/148、82/148**；Test **69/148、79/148**。训练阶段则确实用 hard Gumbel-Softmax，逐批选择计数保留在事件日志。Test 最终仅预测 12 个正类，尚未消除明显的正类低召回问题。

## seed 121 预设重复运行

配置与 seed 42 相同，仅随机种子改为 **121**；从同一固定预训练 backbone 和新初始化的头开始。真实运行 **6 Epoch、84 Microbatch、24 次更新**，作业耗时 **763.6 秒**，PyTorch 峰值 reserved **2.611 GiB**。Dev 在所有 Epoch 的 Macro F1 都为 **0.3808**，均预测 0 个正类；平分时保留先到的 Epoch 1。其 Train/Dev/Test 指标如下。[逐 Epoch、逐项 Loss 与指标](Stage2_Training_Summary_Seed121.json) · [逐批脱敏日志](stage2_formal_seed121_events.jsonl) · [Checkpoint SHA](stage2_seed121_checkpoint_manifest.json)。

| Split | N | Accuracy | Precision | Recall | Macro F1 | Offensive F1 | AUROC | 预测正类 | TN/FP/FN/TP |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| Train | 444 | 0.5811 | 0 | 0 | 0.3675 | 0 | 0.5787 | 0 | 258/0/186/0 |
| Dev | 148 | 0.6149 | 0 | 0 | 0.3808 | 0 | 0.5147 | 0 | 91/0/57/0 |
| Test | 148 | **0.6149** | **0** | **0** | **0.3808** | **0** | **0.4516** | **0** | **91/0/57/0** |

seed 121 最佳 Checkpoint 的 Caption Scorer 倾向原文 / InternVL 为 Train **127/317**、Dev **32/116**、Test **29/119**。两种子都未达到稳定的正类识别：seed 42 低召回，seed 121 全负类。形式上 B32 累积 4 的目标有效批为 128；每个 444 样本的 Epoch 尾部实际只剩 32+28=60 条，包装层按该尾部两个 Microbatch 求均值，属于单卡适配细节。
