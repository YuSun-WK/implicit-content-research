# 历史科研工作流审计：阶段性摘要（2026-11-26）

**状态：GitHub 侧调查完成部分样本；本次隔离执行环境无法访问实验室内网；用户本机已验证两跳 SSH 可连，禁止视为完整历史审计。**

1. **仓库如何拉取？** 无法确认历史 Codex 使用 clone、pull、fetch 还是复用本地仓库。GitHub PR 只能证明上传结果，不能证明服务器上的取任务命令。
2. **代码在哪里？** 已确认 GitHub 中存在 `06_experiments/ASIMOV_shortlist_safety/`、`06_experiments/EMBGuard_shortlist_external/`、`06_experiments/repro_mssbench_multiagent/`。EMBGuard 文档记载本地运行路径 `/home/ubuntu/data/project`；MSSBench 脚本引用本地项目和虚拟环境。路径来自归档，当前服务器是否仍存在未核实。
3. **怎么运行？** MSSBench Stage 2 的脚本以单卡环境变量启动 Python、重定向日志，按 SQLite 终态检查分片，并用 `kill -0` 可选等待上游 PID。记录可证实这套脚本与日志被归档，尚不能证明启动该脚本的外层是前台、nohup、tmux、screen、Slurm 或 Codex 持久会话。
4. **各运行方式多少次？** 不能统计。没有 Codex 历史会话或服务器命令记录；把未发现当作零次会误导。
5. **如何判断结束/成功？** MSSBench Stage 2 的分片脚本检查 SQLite `complete + invalid` 个数、排除 `failed/interrupted/running`；日志记载 100 对主实验 598 complete、2 invalid，并有导出和轨迹核验。该证据只覆盖此案例。
6. **关闭 Codex/SSH 后能否继续？** 无法确认；取决于具体外层进程托管方式。
7. **上传了什么？** #80 有报告、复算脚本、820 条评分；#81 有代码、配置、两个模型各 254 条逐例分数、汇总指标，但未见本 PR 内的训练/推理过程日志；#79 有代码、配置、600 方法输入的结果、轨迹和真实日志。三者都不在 main：#80、#81 已关闭未合并，#79 是开放草稿。
8. **Chat 能否审计？** 对上述已上传的评分与轨迹有不同程度的独立复算基础；无法仅凭 GitHub 核实模型确实按所述命令执行、运行时精确代码版本，或服务器未上传产物。
9. **最先做什么？** 先补服务器会话/命令与 Git 记录，查明启动方式和未提交产物，再定统一的运行清单与退出状态记录。

详见 [完整阶段性报告](REPORT_zh.md)、[证据登记](evidence_registry.csv)。