# VLSU Stage 1R｜环境 DNS 诊断、恢复下载和完整覆盖率验收
**2026-11-19；上游提交 3aa05b9668e753eed68b1d09ab3779bdc2a50d71；只使用 CPU/网络**

## 复核事实（不可修改）
- Stage0 PASS；Stage1 Python suite 68 passed、Smoke 51 UUID/49 URL，其中30 UUID可解码；恢复成功记录无重复下载。
- 当前状态PARTIAL；论文8187、官方 CSV8159、唯一URL8157。当前仅65个URL尝试、28个URL解码，按UUID映射为30/8159 (0.37%)。30 UUID terminal failed、7 pending、8092未尝试。joint decoded 30，image gold decoded 23，text gold eligible 8159，三模态Gold共同交集上限23。
- 网络记录319次attempt事件中 dns_timeout=217，full_last_stop=environment_dns_unavailable；这些次数不是唯一图片数量。当前解析器是 `stage1_transport.py:resolve` 经 `subprocess.run(... timeout=5)` 启动子进程进行 `socket.getaddrinfo`；真实网络不稳定与子进程耗时/并发互相影响**尚未区分**，不能只加重试。
- P0关键组：S-S-S=0/2166，S-S-B=1/58，S-S-U=2/35，U-S-B=4/924，U-S-U=0/142，B-B-U=1/32。没有可支持模型分组准确率的样本覆盖。
- 详细来源：`Run_Stage1.md`、`reports/stage1/Stage1_Execution_Log.txt`、`Stage1_Image_Coverage.md`、`coverage_summary.json`、`scripts/stage1_transport.py`、`scripts/stage1_download.py`、`scripts/stage1_manifest.py`。
- 固定数据SHA256 `9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f`；保留全部原始URL、UUID、标签及失败证据。不可替换/补图。

## 1. 先 CPU/网络诊断，未通过不允许直接全量运行
1. 保持同分支 `repro/vlsu-original-20261119`；不修改综述、H1或PR#78。读取现有 Stage1 代码、测试与真实日志。
2. 生成 `reports/stage1r/DNS_Diagnosis.md`、`Network_Probe_Log.txt`。有网络时对两个可信公共控制域及小样本已知域执行序列化解析对照：系统解析（如 getent）、Python本进程 getaddrinfo、当前隔离子进程 getaddrinfo；记录每个的成功率/耗时/errno，时间和机器环境。并对控制域做合法、短超时、低频率 HTTPS HEAD/GET，以区分 DNS、TCP、TLS、HTTP。禁止关闭TLS验证、使用不可信代理、修改实验室全局DNS、调高并发、绕过站点授权或下载失败图片镜像。
3. 检查 subprocess 的启动开销/并发排队、子进程5s timeout是否引发额外假性DNS超时（需要与控制实验区分）。必要时只对网络解析层做最小范围的受测修复，确保每次DNS和每个redirect仍按原SSRF安全政策验证，并固定真实连接IP与Host/SNI一致，不能因修复而退回普通不受控requests.get。
4. 明确判定：如果两个控制域的串行DNS也持续失败，则 `ENVIRONMENT BLOCK`：停止外部批量访问，给出用户在网络稳定且有访问权限的机器上执行脚本的命令、缓存迁移/状态完整性核验步骤，不宣称已经恢复。严禁连续空转重试。

## 2. 修复、离线回归与小批量真实恢复
1. 修复要添加离线/本地模拟测试：解析超时 vs 正常解析（包括慢子进程）、DNS失效停止门、恢复失败不重复记账、恢复状态保留历史；原有68测试全部通过。记录真实`python -m pytest -q`、`git diff --check`输出。
2. 确认域名/HTTPS控制稳定后再继续原 `.local/stage1/` 状态库，不能`rm -rf`；先`--dry-run`，核验SQLite和对象hash，再在`--resume`上做**至多 20–50 个新请求**的限制性测试，生成小批报告并复核请求限速/成功图片不重下/失败原因。仅环境DNS瞬态失败可在诊断通过后使用`--retry-environment-dns`重新开放；403/404/406/unsafe_target仍须保留原终态；不要重置完整历史或无限重试。
3. 如果测试可用且结果可复现，再分批跑 full，workers<=4初始、每host<=1、保持温和频率。使用`--max-requests`在稳定性良好后逐批提升；失败后优先诊断，不要耗光剩余8000 URL的重试预算。受服务器磁盘/网络/权限所限时停在PARTIAL，准确汇报已完成量；不保证8k URL都可用。
4. 不可搬运版权受限图片、原始CSV或私有日志到GitHub。若换机器下载，写`Move_Resume_Instructions.md`说明如何在合法工作环境安全迁移`.local`中的SQLite/哈希对象/partial/manifest，保留旧记录；若路径/权限不匹配，用明确可审计的迁移，不可删失败日志覆盖。

## 3. 复查任务覆盖和报告状态
1. 重新运行`stage1_report.py`并输出按UUID/URL、HTTP、完整字节、解码、not_attempted、pending、failed_terminal、按标签及25个已观察组合的覆盖率（保留两额外单例和?分组），生成固定SHA256的private roster；提交聚合统计及manifest hash，不提交图片、完整URL、危险文本。
2. 保证`status=FULL`如果只代表“所有URL已到终态”，**绝不能解释为图片全部可访问**。报告明确四个独立状态：processing_exhaustive、decoded_joint_coverage、error_reason_breakdown、model_eligibility。即使全URL终态也要注明DNS terminal与本机网络阻碍，对后续可用性保留重试权。
3. 注明完整的本地状态与报告不能在GitHub云端直接证明真实缓存物存在；给`--root`、文件数与hash校验命令和真实本机执行结果。
4. 检查`stage1_manifest.validate_predictions`任务集合，至少保证joint/image/text固定UUID强一致性及Figure4/5三模态共同交集，缺失和unknown不能在评测时静默排除。
5. Prompt的独立人工核对、Qwen权重revision、量化等属于后续Stage2，仍OPEN，不得宣称MODEL REPRODUCED。

## 4. 决策门与交付
- 如果环境控制测试失败，清晰输出 **STAGE1R=BLOCKED_BY_ENVIRONMENT**，不跑full，提出在授权网络环境的复现命令和迁移步骤。
- 如果网络恢复但full未完成，输出 **STAGE1R=PARTIAL**，原因、下一批与按模式覆盖率。此时最多可提议固定小样本模型Smoke，不能称全量Table2/4复现。
- 如果全部URL完成尝试或按审计规则到终态，输出 **STAGE1R=ACQUISITION_EXHAUSTED**（不等于full image coverage），提供所有任务的实际可评测UUID数及固定清单；再由Chat审查是否足够开展E1/E3/E4/E5/E6。
- 只在以上gate后再建议Stage2 GPU任务，本轮严格禁用GPU，不下载模型或推理。
- 提交到同一分支`repro/vlsu-original-20261119`，不合并main。产出新增审计/测试/命令/状态检查、日志及汇总；回报Commit SHA、真实测试命令和数值、DNS诊断证据、已尝试/未尝试/解码/失败和所有关键组覆盖、状态库保留/迁移、下阶段阻断原因。
