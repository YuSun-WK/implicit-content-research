# 目标服务器与目录

2026-11-26 实测：hostname=sunyu，用户 ubuntu，工作目录 /home/ubuntu/data/project，网卡含 192.168.191.243；本轮没有 SSH 跳转。[E011] Codex 路径 /home/ubuntu/bin/codex，版本 codex-cli 0.169.0。tmux 与 screen 可执行；sbatch/squeue/sacct/gh 不在 PATH。这仅是安装状态，不代表历史使用。[E011,E013]

~/.codex/sessions 有 81 个 JSONL；首建日期 2026-09-11 至 11-19，部分会话恢复后持续写入到 11-25。文件包含 custom_tool_call、工具结果、会话 ID、退出码；只提取脱敏科研操作。~/.codex/config.toml 存在，仅查看键名；auth.json 未打开。当前科研 tmux pane 名称：killtest、killtest_SIJA、mssbench_fuxian、thinkingguard_fuxian、trace_fuxian、vlsu、vlsu_fuxian；pane 当前程序均为 codex。多个 Codex 实例当前并存，但未证明同时写同一目录。[E012,E013]

~/.bash_history 有 684 行，包含 tmux 194 个匹配行、screen 2、codex 43、sbatch 0；Shell history 不是 Codex 工具调用的完整记录。项目目录最大深度 5 与 HumanShift 最大深度 3 未发现 AGENTS.md；本结论不覆盖更深或其他目录。[E013,E019]

本机可见主要目录树见 [总报告](REPORT_zh.md)。TRACE 当前两份 Git 副本分别位于 trace-stage0 与 implicit-content-research-trace；前者本地 commit 7470be2，远端 TRACE 分支曾观察到 0f50a5f，不能把当前本地 HEAD 当作所有历史运行 SHA。mssbench-stage0-repo 本地 0de6e89；H1 目录不是根 Git 仓库。[E019] 当前进程/目录状态不能反推历史执行状态。
