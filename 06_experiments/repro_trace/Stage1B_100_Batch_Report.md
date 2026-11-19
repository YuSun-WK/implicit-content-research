# TRACE-S1B · 最多 100 Microbatch

**G5 `BLOCKED`。** G1 缺少授权 FHM，G4 无通过的实际 GPU smoke。短跑 **0/100 Microbatch**，真实 CUDA 优化器更新 **0 次**。Microbatch 2、4、8 的试探未启动。无 Loss、梯度、allocated/reserved 峰值、单步耗时或 p50/p95。无短跑 Checkpoint、中断后续训或 Dev/Test 评分结果。 [Smoke 报告](Stage1B_Smoke_GPU.md)

G4 通过后再依序各试一批 Microbatch 2、4，8 取决于实际显存余量和共享设备占用。选定安全配置后，以同模式和同配置的 smoke Checkpoint 为门禁，运行最多 100 个 Microbatch，每 ≤25 批保存，并实测一次由 Checkpoint 恢复后继续训练。Dev 阈值默认固定 0.5。 [运行与恢复方式](Stage1A_Mode_Semantics.md)
