# Stage 1 Gate Report · STOP

| 门槛 | 状态 | 证据 |
|---|---|---|
| G0 数据版本和图像 | PASS（发布版功能范围） | Table 1 的类别差异 unresolved，保留固定 HF 原标签。20 对及 40 图逐文件大小、SHA256 和 RGB 解码通过。 |
| G0 Adapter、运行器、续跑 | PASS（CPU 契约） | 13 个 CPU 测试通过，验证原生模板 text-only/image 渲染、替换上游输出的下游敏感性、QA 路由、无效停止、实际进程中断和 manifest。 |
| G0 真实模型就绪 | FAIL | HF 大权重传输不完整，PyTorch wheel 与依赖安装失败。真实 Adapter 入口的 CPU preflight 在 SHA 核验门槛拒绝启动。 |
| G1 极小 GPU 探针 | FAIL（未运行） | 计划 4 个图文输入、20 次生成。实际 GPU ID 无、模型加载 0、生成 0，耗时、token 和峰值显存无测量。 |
| G2 20 对功能 Smoke | FAIL（未运行） | G1 未通过，也无六小时外推依据。 |

原生分支仍优先。公开历史没有逐条证据支持重新分类，Table 1 口径保持 unresolved；这项差异按正式任务书允许功能性 Smoke。实际 STOP 是依赖和权重传输，多次网络重置、长读超时和 Xet 未完成。没有生成日志、指标或模型失败案例可报告。Pilot 和 Full 未启动。

唯一下一步是从可稳定传输的缓存或镜像补齐并逐文件核验**同 revision 的原生权重、CLIP 和锁定 wheels**，随后只启动 G1 探针。

[版本对账](table1_reconciliation.md) · [图片门槛](smoke_image_gate.md) · [Adapter 审查](model_adapter_review.md) · [模型环境](model_environment_lock.md) · [资源记录](resource_measurements.md)
