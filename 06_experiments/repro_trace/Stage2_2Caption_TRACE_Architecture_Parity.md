# Stage 2｜二候选 TRACE 架构与作者代码对齐

作者固定 `MultiOFF/clip_roberta_multioff.py` 的活动 backbone 为 **OpenCLIP `roberta-ViT-B-32` / `laion2b_s12b_b32k`**，注释中的 ViT-H/14 不是实际运行配置。[作者固定源码](https://github.com/surrey-nlp/TRACE/blob/83ecb799f897fe275185e082ee9a669f7d04bfaa/MultiOFF/clip_roberta_multioff.py)。本轮以该模型对应的 LAION 官方权重固定 revision `e22e1c12b0a1ba4af9fb6474626585351ea0da25` 加载，OpenCLIP 版本 2.26.1，RoBERTa tokenizer 长度 77。[CPU 实际装配与权重 SHA](stage2_architecture_probe.json)。

两个候选为 `[原始 sentence, InternVL 增强 Caption]`，输入形状 `[B,2,77]`。从作者源码原样抽取 `CLIPClassifier`，冻结视觉塔，仅解冻 RoBERTa 文本塔最后一个 encoder 层。Scorer 对两个文本特征评分，训练用 hard Gumbel-Softmax，推理用 softmax；选择后的文本特征经过图文投影、双向 cross-attention、pre-output 与二分类头。训练目标保留作者 MultiOFF 的 **`L_cls + 0.3 L_cont + 0.7 L_rel`**、focal 形式与 20 Epoch 温度退火。包装层将 B=1 时的 `.squeeze()` 改为稳定的 `reshape(-1)`，并阻止作者评估代码按被评估标签搜索阈值；本轮固定 0.5。作者源码本身未修改。[训练包装层](stage2_train.py)。

| 可训练组 | 参数量 |
|---|---:|
| 文本塔末层 | 7,087,872 |
| Caption Scorer | 1,054,209 |
| 图像投影 / 文本投影 | 527,360 / 527,360 |
| 正向 / 反向交叉注意力 | 4,198,400 / 4,198,400 |
| pre-output / 分类器 | 4,203,520 / 1,025 |
| **总计** | **21,798,146** |

全模型 **227,433,731** 参数，视觉塔可训练参数 **0**。作者的 `train_contrastive` 分支重新编码两个候选后以 hard argmax 取一条，因此对比损失的选择操作本身不给 Scorer 连续梯度；分类和相关性分支可优化 Scorer。作者每 Epoch 计算的 `best_captions` 不参与其 `calculate_loss_gs` 的训练输入选择，本轮不将其解释为直接决定分类候选。二候选改编与论文三候选最佳配置不同，不能称为严格同条件复现。
