# ThinkingGuard Full TriggerBench Reproduction (2026-11-19)

**状态：R0 证据审计与 Stage1 Codex 交接已提交；新GPU实验 NOT_RUN。** 原始 H1-K0/K1/H1-K2/H1-K3 路径全部保留。本独立分支以既有 H1-K3 快照为底座，而不是尚未包含历史实验的 main。

- [R0_Evidence_Audit_and_Repro_Plan_20261119.md](R0_Evidence_Audit_and_Repro_Plan_20261119.md)：论文实验矩阵、旧实验差异、旧解析失败和冻结记录、全Test Manifest要求、九类指标和两种分母、训练开源边界及GPU成本。
- [CODEX_STAGE1_PROMPT.md](CODEX_STAGE1_PROMPT.md)：直接交给Codex CLI的第一阶段执行规范（只做来源/CPU核验、解析器、Smoke、门槛通过后最多100对Pilot；不运行300/868或训练）。

**验收状态标记**：`PLAN_READY` 仅表示任务文档和分支已存在；`DATA_NOT_RECHECKED` 表示尚未通过服务器检查当前HF HEAD与图片；`PILOT_NOT_RUN` 表示尚未有新的GPU预测。不得把旧 36 对统一协议结果写成新 868 对五阶段结果。
