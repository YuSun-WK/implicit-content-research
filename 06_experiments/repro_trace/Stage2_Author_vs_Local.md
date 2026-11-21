# Stage 2｜作者结果与本地运行的解释边界

| 运行或论文行 | 数据与模型 | Accuracy | F1 | AUROC |
|---|---|---:|---:|---:|
| TRACE 论文 Table 6 最佳 MultiOFF | 作者报告的更大 XLM-R ViT-H/14 与原配置 | 0.678 | 0.673 | 本轮未核实 |
| 本项目 Stage 1C 适配 projection baseline | 740 完整样本、HF ViT-L/14、原文单候选 | 0.6149 | Macro 0.3808 | 0.5361 |
| 本轮二候选完整机制，seed 42 | 同 740 完整样本、OpenCLIP RoBERTa ViT-B/32、原文 + 本轮 InternVL | **0.6014** | **Macro 0.4425** | **0.5257** |
| 本轮二候选完整机制，seed 121 | 同上，预设重复种子 | **0.6149** | **Macro 0.3808** | **0.4516** |

作者论文数值和本轮所用骨干、候选来源与数量、完整样本筛选、评价实现不相同。作者原 MultiOFF `evaluate_model` 在被评价标签上选择阈值，本轮固定 **0.5**。作者论文 F1 定义与本轮显式 Macro F1 的一致性未核实，所以论文行仅作异配置参照。Stage 1C baseline 使用另一个 ViT-L/14 主干；其 Test 已在历史阶段看过，本轮不能把两者的差值归因于 Caption Scorer、相关性损失或 InternVL 的独立贡献。seed 42 的 Test 正类 F1 为 **0.1449**，预测正类 **12/148**；seed 121 预测正类 **0/148**。两种子的方差说明当前方法尚未稳定识别正类。固定门限下 seed 42 Test Accuracy 比 Stage 1C baseline 低，Macro F1 较高，AUROC 略低。[seed 42 汇总](Stage2_Training_Summary.json) · [seed 121 汇总](Stage2_Training_Summary_Seed121.json)。

本轮确定的证据层次：

1. **Caption 来源与覆盖：** 固定 InternVL 8B 实际生成 740/740 条，来源和对齐键可核验；其中 334 条超出 OpenCLIP 77-token 限制。
2. **机制是否执行：** 真实 GPU 的 Scorer、Gumbel、两向融合、末层文本编码及三项 Loss 均运行，梯度和参数变化见 Smoke 与短跑日志。
3. **模型表现：** 两个预设种子的最终 Test 指标分别来自其 Dev 选定的 Epoch 1，未在 Test 上调阈值；seed 42 后续 Epoch 的 Dev 预测出现全负类退化，seed 121 从首个 Epoch 就全负类。
4. **增益归因：** 尚无同 backbone、同 Caption 覆盖的控制实验，因此无法把分数差归因于某一模块；后续应只做一个预先固定的同条件对照。
