# Codex CLI 历史科研实验工作流审计

日期：2026-11-26。范围：目标服务器 sunyu 上本人可读的 Codex 会话、Shell 历史、实验目录，以及 YuSun-WK/implicit-content-research 的代表性实验分支和 PR。本次调查只读，没有重新训练、推理或更改历史实验。证据编号见 [证据登记](evidence_registry.csv)。

## 方法与统计口径

当前主机即目标服务器，网卡含 192.168.191.243，无需重新 SSH。[E011] 识别 ~/.codex/sessions 内 81 个 JSONL，按事件时间截取 2026-11-26 之前的工具调用，避免把本次审计命令算入历史。只提取科研相关命令、会话 ID 和退出码，不复制完整会话或读取凭据。[E012] 同时检查 Shell history、当前 tmux pane、项目 Git 状态、私有产物与远端 PR 文件。历史会话所见是下限；未找到的机制只能说在已读取记录中未发现。命令调用次数可能包含同一实验的重试，不能当作实验次数。[E012,E013]

## 实际工作流

Chat/GitHub 提供任务文档；Codex 在 /home/ubuntu/data/project 下的多个长期工作目录读取或更新仓库，通过 exec_command 执行 Python、Shell 和 Git 命令。长命令常获得 Codex 统一命令会话 ID，再经 write_stdin 轮询；部分 Shell 用 & 并行启动 worker 并 wait。当前七个科研 tmux pane 的前台程序是 codex，说明用户的 CLI 本身运行在 tmux 中，不能推出每个 Python 实验由独立 tmux 托管。[E012,E013,E015,E016,E017]

历史工具调用中匹配 git fetch 108、pull 28、clone 15、worktree add 14、status 529、diff 355、明确 git add 152、commit 148、push 71 个命令字符串；git add . 与 force push 均为 0。次数不是成功执行数。实践既有长期复用，也有重复副本：TRACE 至少有 trace-stage0 和 implicit-content-research-trace 两个 Git 工作目录，VLSU/H1 还有仓库外工作目录。[E014,E019] 未逐次对齐运行代码 SHA 和提交，故不能认定每次实验启动前都固定了代码版本。提交作者也不能证明具体命令是谁输入。已读命令中没有 gh pr create，当前 gh 也不在 PATH；PR 的存在不能证明由 Codex CLI 输入了创建命令。没有查到 force push 或直接向 main 提交的匹配命令，但这不是对全历史的排除。

## 三条可核查的启动到上传证据链

1. TRACE MultiOFF：2026-11-21，stage2_train.py --phase formal 前台命令含 timeout 21540s。Seed 42 获统一命令会话 92493，两次 write_stdin 后 10:22:07 exit_code 0；Seed 121 会话 23469，四次轮询后 11:32:41 exit_code 0。[E015] 私有目录有事件日志和 best/last Checkpoint。两份本地事件日志 SHA256 与 GitHub 公开事件日志相同，汇总器从事件重算的摘要与上传摘要完全一致；各 84 microbatch、24 参数更新，Test 各 148 条。GitHub 可核查事件与汇总，但缺私有 Caption、权重和样本级预测，无法仅凭 GitHub 重跑模型或独立重算 AUROC。[E020,E021]
2. ASIMOV：2026-11-20 三个 worker 经 Shell & 和日志重定向并行启动，外层 wait；统一命令会话 51443 经 39 次 write_stdin 轮询，07:50:42 exit_code 0。[E016] PR #80 只有 README、recompute.py、820 行 scores.csv（另有表头），支持对分数做 CPU 复算，却没有 worker 过程日志。历史命令给出日志路径，但该项目目录目前未在目标工作区找到；不能声称日志仍在服务器，也不能由 PR 单独核验原始模型运行。[E022,E025]
3. MSSBench：stage2_run_remaining.sh 经 Codex exec 启动并返回 cell ID g5:305。脚本做单卡检查、按块同步 Python、SQLite 终态计数与导出；后续记录通过日志、进程、GPU 和数据库检查。未找到该 cell 的最终 wait 返回，外层工具退出码不能标为已确认。[E017] PR #79 上传结果 CSV、traces JSONL、多份过程日志；私有 SQLite 和中间日志未上传。600 个方法输入中 598 complete、2 invalid；诊断脚本 GPU 阶段后第 41 行报错，随后 CPU 恢复。[E023]

进程消失、程序退出 0、产物数量完整、结果复算是四种不同证据。不能推广某一案例的检查标准到所有历史实验，也未发现代表性案例仅凭 GPU 空闲宣布成功。[E015,E016,E017,E020,E022,E023]

## 目录结构与限制

    /home/ubuntu/data/project/
    ├── trace-stage0/                    Git；TRACE 代码、报告、.local 私有训练产物
    ├── implicit-content-research-trace/ Git；TRACE 第二本地副本
    ├── mssbench-stage0-repo/            Git；MSSBench 代码、私有 SQLite
    ├── vlsu-original-repro/            工作目录；Stage 2 推理标记 NOT RUN
    ├── h1-cf-killtest/                  非 Git；脚本、日志、metrics、模型快照
    └── 06_experiments/VLSU_pairing_inventory/ 非 Git；配对清单
    /home/ubuntu/data/trace-assets/multioff/ 私有数据与 Caption

当前目录仅证明调查时状态。[E019,E024] PR #80/#81 已关闭未合并，#79 仍为 Draft，不能只看 main。[E022,E023,E026] 旧 PR #82 的“服务器不可访问”只描述此前隔离执行环境，本次已在目标服务器核实，不再作为当前限制。[E010,E011]

调查无法穷尽所有历史实验；Shell history 不覆盖全部非交互命令；远端没有某文件不证明其从未生成。ASIMOV/EMBGuard 历史工作目录当前未找到，无法做逐文件本地对账。[E012,E025] VLSU Stage 2 摘要明确 NOT RUN，不能算完成实验。[E024] 详见 [执行方式](EXECUTION_MODE_AUDIT_zh.md)、[上传审计](ARTIFACT_UPLOAD_AUDIT_zh.md)、[风险审计](WORKFLOW_RISK_AUDIT_zh.md)。
