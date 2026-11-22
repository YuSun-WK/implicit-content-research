# Stage 0 Gate Report · FAIL（进入 Smoke 的门槛）

Stage 0 审计与交付已完成。Smoke 判定为 **STOP**。正式论文 Table 1 与固定发布 JSON 的 Embodied 分类相差 20 条输入。原生 LLaVA 启动条件、Smoke 图像完整性及适配器真实行为仍待验证。

| 交付 / 门槛 | 状态 | 证据 |
|---|---|---|
| Source Code Audit | PASS | [原代码审计](source_code_audit.md) |
| Repair Log | PASS | [逐项证据及实现落点](repair_log.md) |
| Data Audit | PARTIAL | [JSON 实测与论文对账](data_audit.md)，图像为路径和远端哈希级审计 |
| Model Compatibility Report | PARTIAL | [原生与转换路线](model_compatibility.md)，原生依赖和权重未就绪 |
| Resource Budget | PASS | [资源与规划预算](resource_budget.md) |
| Experimental Matrix | PASS | [实验矩阵](execution_matrix.csv)，包含待实现的诊断 |
| Evaluation Protocol | PASS | [输入与行为评分](eval_protocol.md)，本地模型 Judge 策略待执行 |
| Mock Test Results | PASS | [七项 CPU 契约测试](mock_test_results.md) |
| Run schema / resume | PASS | [SQLite 格式与断点测试](run_log_schema.md) |
| Stage 0 → Smoke | FAIL | 分类对账未闭合、40 张候选图片尚未解码、原生模型尚未具备本地运行条件 |

未闭合的 P0 有发布版 vs Table 1 的 Embodied 分类差异，以及真实适配器、权重/视觉依赖和已解码图像三项启动依赖。官方 B 代码仍保留原缺陷，C 代码已在 CPU 验证关键信息流。Caption 诊断与本地 Judge 仍为 D 的后续工作。本阶段仅运行 CPU 检查，`nvidia-smi` 为只读遥测，GPU 推理、训练、付费 API、模型和图像下载均未发生。

下一步先核定论文 Table 1 所用 Embodied 类别版本。若无法取得逐条对应证据，应明确确定以固定 HF 版为复现口径，然后才重审 Smoke 准入。
