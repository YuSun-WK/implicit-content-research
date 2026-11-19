# TRACE Stage 0 · 100 Batch 验证

**DATA_BLOCKED。** 本地输入检查没有确认 FHM 原图、标签和作者两列原始 Caption；也未找到 CLIP 训练权重。真实 FHM 训练 Batch 为 0，真实 `optimizer.step()` 为 0。训练峰值显存、损失、真实梯度、训练耗时、可恢复 GPU checkpoint、Accuracy/F1 均无测量值。未运行测试集评分。

实际执行记录见 [stage0_checks.log](stage0_checks.log)、[cpu_checks.log](cpu_checks.log) 和 [environment_probe.json](environment_probe.json)。

- Dry-run 使用固定 CLIP 配置在 meta device 构造模型并输出逐参数清单。真实训练权重未载入。
- CPU fixture 验证候选形状、单样本上游错误及包装形状适配、有限 loss、Scorer/文本梯度可达、冻结视觉塔无梯度、Dev 阈值和简单 Checkpoint 原子序列化。fixture 使用小型随机初始化模型与合成单元测试张量，没有调用优化器，也没有验证真实 CUDA checkpoint 的 optimizer/scaler/RNG 回读。
- 一次早期 CPU fixture 发现包装将上游 FocalLoss 替换到模块全局后触发作者显式 `super(FocalLoss, self)` 的递归。最终包装仅给函数调用提供局部的 Focal 构造绑定，重跑通过。上游文件哈希保持一致。
- 真实 smoke 请求触发本地输入门禁，退出码 3，发生于 PyTorch 导入和模型加载之前。接下来的 100 Batch 条件未达到。GPU 记录只反映设备枚举和显存空闲快照。
