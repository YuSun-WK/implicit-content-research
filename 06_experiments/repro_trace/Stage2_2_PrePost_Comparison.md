# Stage 2.2｜修复前后对照状态

Caption 层面的直接对照已完成：[修复审计](Stage2_1_Caption_Repair_Audit.json)显示旧版 **334/740** 超过 77 tokens，新版仍有 **5/740** 超限；旧版合格的 **406 条逐字不变**，原超长项中 **329/334** 成功修复。新 Caption 中位数 / P95 / 最大长度为 **52 / 75 / 110 tokens**。五条失败项保留原 Caption，没有截断或通过门禁。

| 固定种子 | 旧 Caption 最佳 Epoch | 旧版 Dev Macro F1 | 旧版 Test Accuracy / Macro F1 / AUROC | 修复版 Dev/Test |
|---:|---:|---:|---|---|
| 42 | 1 | 0.4776 | 0.6014 / 0.4425 / 0.5257 | **未运行；Caption 门禁失败** |
| 121 | 1 | 0.3808 | 0.6149 / 0.3808 / 0.4516 | **未运行；Caption 门禁失败** |

旧版值来自 [Stage 2 数值日志汇总](Stage2_Complete_TRACE_Training_Report.md)；不能计算修复前后性能差或声称性能改善。即使后续完成新训练，重写也改变了 Caption 内容，差值不能单独归因于长度。旧版 Test 已被查看，后续修复版评估应作为透明后续复核。
