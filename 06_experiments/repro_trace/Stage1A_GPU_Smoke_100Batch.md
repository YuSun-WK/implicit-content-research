# TRACE-S1A · 真实 GPU Smoke 与短跑

**G4 `TRAINING_NOT_RUN`。G5 `BLOCKED`。** 两种模式均在 FHM 授权门禁处退出，未向 GPU 载入训练模型。日志中的 NVIDIA 显存空闲值是设备快照。

| 真实 FHM 结果 | `trace_original` | `trace_text_only_diagnostic` |
|---|---:|---:|
| Smoke Microbatch | 0 | 0 |
| 实际 CUDA `optimizer.step()` | 0 | 0 |
| 稳定性 Short Microbatch | 0 | 0 |
| 实际 Loss、有效梯度、参数更新 | 未测 | 未测 |
| GPU allocated / reserved 峰值 | 未测 | 未测 |
| 单步耗时和 p50 / p95 | 未测 | 未测 |
| 真实 Checkpoint 保存、恢复、续训 | 未执行 | 未执行 |

9 项 CPU 测试通过，覆盖原始三候选、诊断单候选分类、零 Scorer 梯度、split JSONL 正规化、图像完整性、独立数据与权重门禁，以及模拟中断后的 CPU checkpoint、RNG 和下一次参数更新一致性。两种真实入口使用未确认授权的配置，退出码均为 3。CPU fixture 的优化器调用和 checkpoint 仅用于代码测试。配置级参数表重建成功。无 FHM Accuracy/F1 或测试阈值。 [CPU 检查日志](s1a_cpu_checks.log) · [入口检查日志](s1a_runtime_checks.log) · [真实运行命令](Stage1A_Mode_Semantics.md)
