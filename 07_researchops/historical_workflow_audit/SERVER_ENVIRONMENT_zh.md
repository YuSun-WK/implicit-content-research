# 服务器与本地访问核验

- 当前 Work 环境位于 Windows 工作区，`ssh`、`git`、`codex` 命令可见；该 Windows 环境并非用户的 Linux 服务器。
- 通过现有执行环境以非交互、只读 SSH 尝试跳板、直连目标、ProxyJump，均在 TCP 22 连接阶段返回 `Permission denied`；没有到达密码或密钥认证阶段。Windows 应用窗口清单没有已打开的服务器终端。
- 未检查服务器上的 `hostname`、`codex --version`、`tmux`、`screen`、`sbatch`、`ps`、`nvidia-smi`、`~/.codex`、Shell history；安装与历史使用均未知。
- 仅有远端文档提供的历史路径，如 `/home/ubuntu/data/project`、MSSBench 的本地 `.stage0-local/` SQLite journal。不能把归档中的路径等同当前文件存在性。
- 当前无法给出服务器的真实目录树、未跟踪文件清单、运行中任务清单，或未上传文件的完整集合。

**解阻所需最小协助：** 在能访问内网的本机 Work 会话运行同一只读审计，或提供一个已登录的服务器终端；不需要在聊天中再次发送密码、私钥或令牌。