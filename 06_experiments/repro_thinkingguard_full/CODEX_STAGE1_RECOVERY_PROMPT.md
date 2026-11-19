# ThinkingGuard Stage 1｜Recovery & First GPU Evidence

你是 Codex CLI 实验工程师。**本轮是补救 Stage 1 数据门槛和 GPU 监控，而不是重跑旧36对或直接全量训练。** 仓库 `YuSun-WK/implicit-content-research`，分支 `repro/thinkingguard-full-20261119`。首先读取：
- `06_experiments/repro_thinkingguard_full/STAGE1_INDEPENDENT_REVIEW_AND_RECOVERY_20261119.md`（本轮审查与明确缺陷）
- `06_experiments/repro_thinkingguard_full/STAGE1_EXECUTION_REPORT.md`（原报告）
- `06_experiments/repro_thinkingguard_full/R0_Evidence_Audit_and_Repro_Plan_20261119.md`（冻结要求）
- `03_experiments/h1_k0_triggerbench/H1_K1_FORMAL_EXPERIMENT_REVIEW.md` 及旧 `scripts/gpu_monitor.py`（PID命名空间的历史真实证据）

**必须先在新目录修复三个工程问题**：① 全局1736张图片齐全的 `gpu_data_gate` 不能阻止只需要所选6/36/200张图的Stage1作业；引入基于冻结队列和SHA的stage_ready，对正式Full另用global gate。② `nvidia-smi` 报host PID、容器 `os.getpid()` 不匹配；参照H1-K1已验证的unique host PID绑定方案和64MiB可逆CUDA显存挑战，监控错配不可当0，不能关闭监控掩盖；绑定失败或GPU被他人占用就不启动。③ `runs/smoke`、`runs/validation` 与任意 `--run-id` 的前序门槛查找冲突；统一使用明确固定run id或stage registry，必须支持时间戳/断点恢复且防止混配置。对三项写CPU mock/regression测试、记录冻结前后源码和配置SHA；不得修改旧H1代码及历史结果。

**随后采取双轨执行**：
A. 下载：本轮已有297/1736张官方LFS SHA+PIL确认（来自旧缓存72、新下载225），缺1439张（207有失败记录、1232没有实际下载成功，不能统称均请求失败）；已有102个完整pair，其中大多聚集在ethical_violations和illegal_activities。优先下载固定 `sample_queues.json` 的 smoke6→validation36→pilot200，若需先诊断网络，降低并发到2–4，按官方HF固定 revision `3ac26e778db94a282711f463f22ba6db99643bee` 有界重试/断点续传，尝试已安装的huggingface_hub客户端（不更新全局环境），严格用官方LFS SHA校验。保留现有297文件不重下；失败/未尝试/已验证分开记录。整套Test其他缺图在后续下载窗口补齐。
B. GPU：只有符合数据、安全门槛才执行正式冻结A0 Smoke6和独立验证36，模型revision `76892f9768ce828268265171f4bbc5dfb75eafc3`，NF4、BF16 compute、max_new_tokens1024、greedy、作者原样Prompt，冻结parser。若冻结Smoke仍缺图片但现有完整pair可用，可以另建 `diagnostic_smoke_ready_v1` 作工程诊断，记录旧36对重叠情况；**不能冒充正式样本或解锁正式validation/pilot**。GPU显存上限20GiB，单作业<6h，不杀其他用户进程，保留raw输出/身份/时间/显存/版本。若独立36条解析<35条成功，保留A0 FAIL，不回写parser；另提A1修复Prompt的独立预注册方案，不自动把A1标为作者复现。
C. 仅在A0正式验证PASS且GPU预算符合预期后跑100对Pilot（200张图，可按时段恢复，不超过6小时/作业）；计算全分母和valid-only微/宏Unsafe F1，Accuracy/Recall/FPR/FNR、9类分组、PairAcc/四象限/INVALID、paired bootstrap。不能按正确率挑样本或跳过失败。不得提前跑300/868及DPO/SA-MCTS训练。

**交付**：新的 `STAGE1_RECOVERY_EXECUTION_REPORT.md`、修复后的 scripts/tests、固定队列/下载优先级及hash清单、所有实际GPU原始输出（若执行）、每个阶段的DONE/PARTIAL/BLOCKED/NOT_RUN状态与确切数量、测得P50/P95/峰值、实际命令、完整commit SHA、旧受保护blob前后验证。允许网络失败时先完成CPU和准确状态报告，不无限重试。完毕提交本分支、不合并main。

请独立执行至当前安全门槛允许的最远阶段，不要把尚未运行的GPU实验标记为完成。
