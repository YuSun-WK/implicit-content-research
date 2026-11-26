# 执行方式和结束判定

## 统计边界

读取 81 个 JSONL，在事件时间早于 2026-11-26 的记录中，发现 7,274 个 exec 调用，其中 4,766 个输入含 exec_command，1,788 个含 write_stdin，解析出 4,480 个 cmd 参数。筛选得到 9 条 Shell & 后台启动命令（跨 4 会话）、1 条 nohup；Codex 工具命令中没有实际 tmux new/send-keys/attach、screen 启动或 sbatch/srun 提交。命令匹配次数不是独立实验数，也不包括终端外用户操作。[E012,E018]

| 历史任务组 | 时间 | 启动方式 | 结束证据 | 日志/产物 | 证据 |
| --- | --- | --- | --- | --- | --- |
| TRACE formal seed42 | 11-21 | 前台统一命令会话 92493；timeout 21540s | 2 次轮询，exit 0 | 私有 events/checkpoint；公开 events | E015,E020 |
| TRACE formal seed121 | 11-21 | 前台统一命令会话 23469 | 4 次轮询，exit 0 | 同上 | E015,E020 |
| MSSBench 256 | 11-22 | 前台脚本；exec cell g5:305 | 日志与 SQLite 计数；未见 cell 最终退出 | 私有 SQLite、公开结果/日志 | E017,E023 |
| ASIMOV manual workers | 11-20 | Shell 3 workers & + wait；外层会话 51443 | 39 次轮询，exit 0 | 历史日志路径；PR 评分 | E016,E022 |
| ASIMOV Qwen workers | 11-20/21 | Shell worker & + wait | 命令记录；未逐个核查退出 | PR 评分 | E018,E022 |
| EMBGuard workers | 11-20/21 | Shell worker & | 命令记录；逐 worker 状态未复核 | PR 逐例评分 | E018,E026 |
| HumanShift Round014b | 09-20 | 三个 GPU seed Shell & + wait | 命令记录；未逐 seed 复核 | 仓库外记录 | E018 |
| PA Gate1 killtest | 10-10 | 四条件 Shell & + wait | 命令记录；未逐条件复核 | 仓库外记录 | E018 |
| HumanShift E3 CPU | 09-16 | nohup + &，CPU | 后台最终退出状态未定位 | /tmp/humanshift_e3_seed2025.log 历史路径 | E018 |

上述 9 个代表任务组按外层 Shell 语义分类：前台脚本/命令 3，Shell 后台 worker + wait 5，nohup 脱离 1。Codex 统一会话属于另一维度：TRACE 两次和 ASIMOV manual 可核对 session ID 与最终退出；MSSBench 是 exec cell，未见最终 wait。tmux 承载的是 CLI 自身，不能额外给 9 组都加“tmux 实验”标签。[E013,E015,E016,E017,E018]

## 是否成功

TRACE 有进程退出 0、事件日志、Checkpoint、摘要精确重算；没有公开逐例预测，故最终模型推理不能仅凭 GitHub 独立核验。[E015,E020] ASIMOV 有外层退出 0 与 PR 评分，但 worker 独立退出及过程日志未在 PR 找到。[E016,E022] MSSBench 脚本用 SQLite SQL 确认 complete+invalid 总数且无 failed/interrupted/running，过程日志包含一次诊断脚本故障和恢复；外层 exec cell 的最终退出码未找到。[E017,E023] VLSU Stage2 文件明确 NOT RUN，不计为成功。[E024]

Codex 曾使用 ps/日志/nvidia-smi/结果文件等读数监控；历史记录不足以证明所有实验均检查完整预测数、OOM 与人工终止的归因。命令会话退出状态可判断外层命令结果，后台子进程还需独立 PID/退出状态。仅在会话结束后保存路径/状态/manifest 才能可靠恢复监控；所审案例没有统一跨会话机制。[E012,E015,E016,E017]
