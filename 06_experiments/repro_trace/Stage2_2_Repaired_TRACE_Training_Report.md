# Stage 2.2｜修复版 TRACE 训练状态

**NO-GO，训练未启动。** Stage 2.1 新 Manifest 仍有 **5/740** 条超过 OpenCLIP 77-token 限制，未满足任务文档的 740/740 验收门禁。`stage2_train.py` 的前置检查在大模型加载之前拒绝该文件；因此修复版 Seed 42 和 Seed 121 均为 **0 训练 Microbatch、0 次 AdamW 更新、0 个新 Checkpoint、0 次新 Test 评估**。不得把旧版 [Stage 2 正式结果](Stage2_Complete_TRACE_Training_Report.md)当作修复版结果。

已经准备的配置见 [Stage 2.2 固定配置](Stage2_2_Repaired_Training_Config.yaml)：与旧版相同的 Backbone、两候选结构、三项损失、BF16、物理 Batch 32、累积 4、AdamW 1e-4、Dev Macro F1 选模与固定 0.5 阈值。训练包装层新增 Manifest SHA 和 77-token 硬门禁、Macro Precision/Recall 与概率分布记录；双种子完成后才允许分别进行一次 Test 评估。代码准备不等于实验结果。

阻塞证据：[Caption 修复报告](Stage2_1_Caption_Repair_Report.md) · [脱敏审计 JSON](Stage2_1_Caption_Repair_Audit.json)。此前旧 Caption 版本的 Test 已被查看；后续修复版即便完成，也必须披露其为透明的后续复核，不是从未触碰的全新 holdout。
