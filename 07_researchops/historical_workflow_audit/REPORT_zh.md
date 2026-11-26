# Codex CLI 历史科研实验工作流审计（阶段性）

日期：2026-11-26。范围：GitHub PR #79、#80、#81 的文件清单与若干原始文件；当前 Work 环境的只读 SSH 连接测试。**服务器侧受连接策略阻断，因此本报告不是完整历史调查。**

## 方法与可确认结论

GitHub 连接器读取仓库、PR 元数据、变更路径、README、脚本、日志、指标和逐例文件。远端文件路径与 SHA 定位于 [证据登记](evidence_registry.csv)。Windows 当前没有已打开的服务器终端。非交互 SSH 到跳板、直连服务器以及 ProxyJump 都在端口连接阶段被拒绝，故没有读取 Codex 历史会话或任何服务器私有文件。

#80 是三文件的 ASIMOV 归档，报告和 `scores.csv` 提供可复算的脱敏分数，但没有原始推理过程日志。#81 有 24 个变更文件，包括两个模型各 254 行评分、配置、报告与汇总指标。#79 的 MSSBench Stage 2 则保留了多份运行日志、600 个方法输入的可移植结果与 1,039 次 Agent 生成轨迹。三者均未合并 main；#80/#81 关闭未合并，#79 开放 Draft。此差异说明必须检索所有 PR 状态和分支。

MSSBench 主实验脚本可证实使用单卡 UUID、离线模型、Python 分片、日志重定向、SQLite terminal count 与失败状态排除；可选 `WAIT_FOR_PID` 使用 `kill -0` 等待。日志记录四个新 chunk 中五个 GPU 进程及 598 complete、2 invalid 的导出。512-token 诊断日志记载运行脚本在 GPU 完成后因编辑而在第 41 行失败，随后 CPU 导出和校验恢复。**脚本内前台运行 Python 不说明外层如何托管脚本**；不能由这些文件推断 Codex 持久会话、nohup、tmux、screen、Slurm 使用次数或断开 SSH 后存活性。

EMBGuard README 记录 `/home/ubuntu/data/project` 下的 CPU replay 命令，两个模型的 pilot/worker/finish 脚本及版本配置。该路径是历史归档陈述，不是当前服务器实测。ASIMOV README 说明 820 行评分与 CPU 复算。所有项目的服务器本地未跟踪文件、运行时精确 commit、Git add/commit/push 命令及 Codex CLI 行为仍未知。GitHub PR 作者与 commit 不能证明由 Codex 输入了具体命令。

## 当前可回答与不能回答

具体简答见 [摘要](EXECUTIVE_SUMMARY_zh.md)，逐案例执行和上传证据见 [执行审计](EXECUTION_MODE_AUDIT_zh.md)及[产物审计](ARTIFACT_UPLOAD_AUDIT_zh.md)。本轮没有调查到服务器 Codex 版本、历史会话、进程、tmux/Slurm、shell history、Git reflog 或本地未上传产物；不能将“无法确认”归为“从未使用”。风险评级只针对已观察事项。

## 后续只读调查门槛

在可访问内网的环境中：定位本人项目目录与 `~/.codex` 的会话结构；仅提取相关执行命令和退出状态；按 task/run ID 对齐本地 `git status/log/reflog`、脚本和运行日志；检查本人进程、tmux/screen/Slurm；将本地 artifacts 与 PR 文件清单逐项对账。生成脱敏的模式统计，分清 Linux 进程托管与 Codex 工具会话。核查完成后更新本 PR 及 CSV，才可形成完整结论。无需重新发送凭据。

[服务器限制](SERVER_ENVIRONMENT_zh.md) · [风险](WORKFLOW_RISK_AUDIT_zh.md) · [路线](IMPROVEMENT_ROADMAP_zh.md)。