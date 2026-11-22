# Stage 2.2｜作者与本地结果对照边界

| 条件 | MultiOFF Accuracy | F1 | 证据状态 |
|---|---:|---:|---|
| TRACE 论文 Table 6 最佳行 | 0.678 | 0.673 | 作者论文；更大 Backbone、不同候选设置，F1 定义未确认相同 |
| 本地旧 Caption、RoBERTa ViT-B/32、seed 42 | 0.6014 | Macro 0.4425 | 真实旧版 Test；[历史训练报告](Stage2_Complete_TRACE_Training_Report.md) |
| 本地旧 Caption、RoBERTa ViT-B/32、seed 121 | 0.6149 | Macro 0.3808 | 真实旧版 Test；同上 |
| 本地修复版 Caption、seed 42/121 | — | — | **NO-GO；无修复版模型和 Test 指标** |

本地方法名称为 **TRACE-InternVL-only-MultiOFF-2caption (Adapted Reproduction)**。论文行不能作为同条件数值复现目标；作者未报告的 AUROC 不予推断。本轮 5 条 Caption 门禁失败，故不提供作者与修复版模型的虚构性能对照。
