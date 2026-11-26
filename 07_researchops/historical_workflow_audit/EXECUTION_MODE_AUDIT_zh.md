# 历史执行方式：证据边界

| 案例 | 可证实的内层执行 | 外层托管（前台/nohup/tmux/screen/Slurm/Codex 会话） | 完成检查 |
| --- | --- | --- | --- |
| MSSBench Stage 2 主实验 | `stage2_run_remaining.sh` 的 Python 分片命令、单卡 UUID、日志重定向；五个新增 GPU 进程的结果见门槛报告 | 无法确认；脚本及日志不记载其如何启动 | SQLite terminal count、失败状态排除、导出、轨迹核验 |
| MSSBench Stage 2 512-token | `stage2_run_diagnostic.sh` 的两批调用；日志显示 GPU 执行后 shell 第 41 行报错，CPU 后处理单独恢复 | 无法确认 | 日志、60 条完整记录和 100 个 Agent 调用的对账 |
| EMBGuard 外部验证 | README 记载 pilot/worker/finish/replay 命令和 2×254 条评分 | 无法确认 | 评分状态与 `metrics.json`；服务器进程退出码未知 |
| ASIMOV | 归档的 `recompute.py` 可 CPU 复算 820 行评分 | 无法确认 | 上传的评分/报告；原始模型执行日志未知 |

**统计口径：** 样本为 3 个 PR、其中 MSSBench 两个运行阶段；没有服务器历史会话。Foreground、Background、tmux、screen、Slurm、Codex 持久化会话的“确认次数”均记作 **无法统计**，绝非 0。Python 在脚本内同步执行与脚本本身由后台托管可以同时成立。

观察到的具体失效：512-token GPU 调用结束后，运行中的 shell 脚本被编辑，导致后处理命令不存在；日志和恢复记录支持“后处理失败后恢复”，不能据此判断是 Codex、用户还是其他进程编辑。