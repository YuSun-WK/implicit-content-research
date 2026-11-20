# ThinkingGuard｜Stage 2 FAST TRACK（2026-11-20）

你是执行型 Codex CLI 工程师兼 Multimodal Safety 复现审计员。**目标：停止反复准备、尽快取得可信的100→300→868对新结果。** 前提是实验协议、完整分母和存档不能妥协。直接在服务器执行，不要只回复研究计划；受限时保存已有结果并给出真实阻塞。

## 0. 读入与冻结（必须先做，5分钟级别的最小审计）

仓库：`YuSun-WK/implicit-content-research`，工作分支：`repro/thinkingguard-full-20261119`，起点提交：`b6dc5f70b9ed87892e79d2eaf2ebcef2d1f4af93`（如果已出现更新，记录并比较差异，不覆盖）。禁止动 `03_experiments/h1_k0_triggerbench/` 和 `03_experiments/h1_k2_research_audit/`。先读取：
1. `06_experiments/repro_thinkingguard_full/STAGE1_RECOVERY_EXECUTION_REPORT.md`
2. `runs/recovery_cpu/final_gate_status.json`、`runs/validation_20261119_recovery/summary.json`、`runs/validation_20261119_recovery/transcription_comparison.json`
3. `artifacts/manifests/data_validation.json`、`artifacts/sample_queues.json`、`runs/stage_registry.json`
4. `scripts/run_resumeable_inference.py`、`scripts/recovery_gates.py`、`scripts/official_parser_v3.py`、`scripts/evaluate_pairwise.py`、当前配置与测试。

最新**已核验事实**：A0原始作者Prompt Smoke 6/6生成，标签4/6、结构6/6；A0独立验证36/36生成，标签20/36（55.56%）、结构35/36、`AMBIGUOUS_TEMPLATE`11、`EXTRA_TEXT`5，`FAILED_PARSE_GATE`；验证仅3/18对两侧均可解析，不能用valid-only 85% accuracy作正式结论。原始A0总计42条预测及GPU日志已存。GPU4090D NF4进程峰8330MiB，全卡峰8339MiB；单条验证中位60.10s，受控P95约81.39s。数据Manifest1736条、868对，其中751图verified、缺985；Pilot冻结队列200/200图片READY。36项CPU测试通过，监控宿主PID绑定已跑通。以上数字**不得当成本轮新增结果**。

先计算并保存A0既有原始预测、旧权重、parser与日志SHA256的before/after保护账本，文件路径仅新增到 `06_experiments/repro_thinkingguard_full/`。不要重新跑A0 36条，不要改原来的任何prediction、summary、freeze、queue或哈希。

## 1. 不再耗费GPU反复修补 A0：正式记录失败

A0 `A0_AUTHOR_PROMPT_NF4` 一直保留原始作者Prompt与`reproduction_parser_v3.0.0`；本轮正式记录`A0_ORIGINAL_PROMPT_FAILED_PARSE_GATE`，展示20/36、11个原样复述双选项、5个多余文本。36条独立验证中有4条被匿名人工语义转录为Unsafe但v3拒绝，说明当前严格解析器有额外格式限制；**即使这4条经事前定义的统一规则获救，也只有24/36=66.67%，仍不够95%**。可以离线做v3后验敏感性分析，但不改原始A0指标，不把事后优化的解析视作独立验证，更不要启动昂贵的A0全量来“突破”门槛。

## 2. A1：新增独立的五阶段稳定输出协议（立即优先）

新实验命名`A1_FIVE_STEP_SINGLE_VERDICT_NF4_v1`，保持**相同**ThinkingGuard权重 `76892f9768ce828268265171f4bbc5dfb75eafc3`、固定 TriggerBench `3ac26e778db94a282711f463f22ba6db99643bee`、九类安全定义、同图文wrapper、五段任务、同五个结束标记和`max_new_tokens=1024`、NF4+BF16 compute、greedy。**只定向修改作者第5阶段输出语法**：保留上下文/意图/实体关系推理，在Overall最后一行输出且仅输出一个`Final verdict: SAFE`或`Final verdict: UNSAFE`，两者只能择一，不再展示`[Safe]/[Unsafe]`或`[XX]`这类未填模板；风险类别如需输出必须放在最后一行之前，Overall以`<|/Overall|>`结束。不要在提示词中同时给模型一个待复制的双标签空模板。保持安全标准相同，记录逐字diff、system prompt SHA、chat render SHA。

建立`configs/a1_five_step_single_verdict_v1.json`、`scripts/a1_parser_v1.py`、`tests/test_a1_parser_v1.py`、`artifacts/a1_protocol_freeze.json`；所有版本化文件**独立于A0冻结文件**。A1 parser只从末段唯一最终行取值，不接受双候选、多个相互矛盾判断或从中间Risk段补标签；结构完整率独立统计。生成/解析不使用GT、side推断或另一侧预测。解析器/Prompt在真正独立验证前冻结。对历史A0 raw可进行开发性误差分析，但不能把用于Prompt设计的样本再当独立验证。

A1开发Smoke用6条（可重用已经被观察过的A0 Smoke，仅工程开发并明确重复），只确认加载/格式/显存。再固定一个**新的**36条独立验证集（18对、九类各2对），排除旧H1 36对、A0 Smoke/Validation和所有A1开发样本，尽可能与Pilot100对不重合，遵循预先固定 seed、类别、完整图像状态，记录先抽样后发现缺图的恢复过程。**不要根据预测、标签或已有模型分数挑可用图片**；冻结样本列表与数据SHA，按该列表下载必要缺图。如果剩余可用对的覆盖不足，则冻结后仅补图、不任意换样本。若采用按文件可用性取样的工程验证，必须明确选择偏差，且不能当正式随机Test表现。

对A1独立验证要求：36条全生成，最终标签可解析≥35/36、结构完整率单独报告、全部原始输出和解析失败案例保留。人类双盲GT审核如无可用人员明确NOT_RUN，绝对不能假称完成。不要根据验证GT调Prompt或解析器；失败时冻结A1失败，并仅追加一个可审计的备选方案（见第5节），不要无限调试。

## 3. 立即推进 Pilot100对；条件满足后扩展300与868

**A1独立验证PASS后**，直接在现有已验证且固定的`artifacts/sample_queues.json`的Pilot200条（100对）运行A1，保持同样的样本清单、完整Safe/Unsafe配对和真实标记。原有A0验证失败**不应该成为A1的上游门槛**：修复runner的protocol-specific stage registry，A1自己的Smoke/Validation gate仅对A1生效；每次加载要严格检查固定model、dataset、source tree、prompt/parser/manifest/queue哈希和前序完整输出。不要把A0的Smoke/Validation结果冒充A1先验门槛。

Pilot达成200/200个明确终态、原始数据与预测记录完整、资源限制和可恢复性检查PASS后，自动计算：Micro Unsafe F1, 9类 Macro Unsafe F1/Recall, Accuracy/Precision/Recall/FPR/FNR, PairAcc, 4 quadrants, 正向/反向翻转、INVALID、结构完整率，及逐类n_total/n_valid/n_correct/Wilson95和按pair重采样的CI；strict full denominator和valid-only并列。缺图/生成失败/INVALID不能从Primary分母静默删去。完整冻结Pilot数据内**不按准确率筛选样本**；模型低准确率≠停机条件。

将全Test划分为固定、可恢复、类别可检查的优先队列。先把与Pilot重合的结果在**同一协议/同一权重/同一输入处理且source SHA完全一致**时复用（不能将A0结果混进A1），然后继续至累计300对（600条），最终Test868对（1736条）。若尚未获得足够图片，CPU下载进程以官方固定revision优先补齐剩余Test985张，区分失败91/未就绪894，使用现有成功的HF Hub0.36.0和curl低并发/有界重试、官方LFS SHA256+PIL校验，避免反复下载已验证751张。**下载与已就绪的GPU推理可在安全I/O/CPU资源下并行开展**，下载进程绝不能改变GPU推理时打开的图像字节。允许现有已就绪子集先跑，并标记`coverage-in-progress`，但不得称完整Test完成，也不得以已就绪子集做最终无偏总体指标；未运行者保留状态。按冻结顺序、缺图状态和可恢复事务调度，不跳过未下载项后默默缩小最终分母。

GPU：仅单张经许可空闲4090/4090D、20GiB进程上限、CUDA allocator≤18GiB、每个job墙钟≤6h，建议将每个job实际运行限制设≤19000秒且预留安全退出；使用历史已验证的容器/宿主PID可逆64MiB挑战，不杀其他用户任务，不改全局Python/CUDA，不用付费API。根据新A1 Pilot P95和实际长尾动态决定batch容量，优先使用一个job内最大安全可做条数，但不能因估计不足撞6h；所有已完成预测及时fsync+atomic保存，配置变更拒绝resume混合。若总Test仍欠图，先完成能跑的冻结样本并同步下载，不反复生成同样样本。

**禁止在无控制条件下启用更激进的量化、降图像分辨率、改变`max_new_tokens`或改采样以加快速度**；任何性能优化必须建立新的实验ID，并以小样本证明不改变目标语义/可比性。任何多GPU并行必须遵守用户单卡任务预算和共享服务器使用政策；默认单GPU。

## 4. Direct Prompt 对照保底（可与A1下载/CPU准备并行）

另设 `D0_DIRECT_TG_NF4_v1`。同一ThinkingGuard模型、同一九类安全定义、同图文和评测集，区别仅为**不要求五步推理，输出唯一Safe或Unsafe**；也应固定输出语法、parser、max tokens和版本（Direct短输出可合理较短但必须如实报告预算差异）。先在少量数据做独立格式Smoke、核验输出格式；随后尽快做**同样Pilot100对**，形成有效的100对正式基线，不需假装这是作者Table3的DPO消融。D0与A1同pair配对比较，报告不同生成token预算和协议差异。若A1验证再次失败，可优先完成D0的100对，以避免本轮仍然0正式Pilot，同时把A1状态保留为FAILED而不是为追进度删掉失败。

Direct Pilot不是新方法贡献，也不是训练消融。禁止用Direct Pilot结果去调A1之后再把Pilot当独立测试；发生调参就必须明确探索性质并另外留出冻结评测数据。

## 5. 停止规则与备选

A1验证未达到≥35/36：保留全部raw、无效类型、类别、预算；**不得**强行解锁A1正式Pilot作为成功复现，也不得后验改label。如果主要失败是唯一尾行格式仍缺失，可提出单独的`A2_TWO_PASS_VERDICT`协议：第1次只做五步推理，第2次用固定、无GT的分类决策指令对同图文和上一次推理做唯一判定；要计入两次调用成本/不同输入量，必须新未见验证集，独立标注，不声称原作者协议。没有必要时不要自动开启昂贵A2。D0保底应继续执行。

如果下载不稳定，使用有界重试和分批续作，不能无限等网络，不能把缺图伪装成完整评测。若GPU不可用仅做可以执行的CPU任务并报告准确阻塞，而不是无限重试抢占。完整训练SA-MCTS/DPO本阶段仍为NOT_FEASIBLE；不可用Prompt对照冒充SFT或DPO消融。Qwen基座模型等A1/D0主要结果完成且缓存允许后才考虑，不因追求大矩阵延误主要交付。

## 6. 代码和工程整改（只做必要更改）

当前runner仍有`if args.stage=="full": cli.error("Full Test is available only for preflight in Stage 1")`限制。Stage2需要解除该禁止，但必须基于每批可恢复队列实现**阶段性完整性门槛**，不要求1736图全部先就绪才能对可用批次推理；只有`FINAL_FULL_TEST_COMPLETE`要求1736/1736独立终态。现有`queue_ready`固定full=1736，对增量batch需新增`batch_ready`及完整pair、来源校验，不靠截断单侧图改变样本。现有`prior_summary`按stage+runner SHA查找，A1/D0应使用protocol-specific独立registry。可选通过单模型常驻处理多个短batch减少重复加载，但每个作业必须完整记录GPU归属和≤6h，总budget不跨job隐藏。

注意`runs/validation_20261119_recovery/metrics_descriptive.json`的valid-only 85%只基于20/36条且仅3/18对完整两侧；任何报告不能拿它与作者Table1 0.764直接比较。旧A0 validation精确哈希均已归档。新实验的 A1 只可与“作者结果（不同Prompt/量化）”作非严格对照，不能宣称复现作者BF16设置。

## 7. 提交与交付

全部保存在`06_experiments/repro_thinkingguard_full/`独立新版本路径，不改动Stage1原始raw或其freeze。新增：
- `STAGE2_FAST_EXECUTION_REPORT.md`（完整真实里程碑、每阶段DONE/PARTIAL/BLOCKED/NOT_RUN）
- `docs/a0_failure_evidence.md`；`docs/a1_protocol_diff.md`；`docs/author_vs_repro_scope.md`
- A1/D0 configs、parser、regression tests、冻结json、独立队列、prompt hashes、预测raw与所有指标
- 下载成功/失败清单、Test pair全量状态、每GPU作业完整耗时与峰值、每次resume日志、统计区间、典型失败配对
- 旧H1/K1/K2/K3和Stage1 42条GPU原始预测的保护哈希账本，提交前后相同

只有真实结果才能写结果数字。每完成关键checkpoint（A1 validation、Pilot100、累计300、全868）即commit，不要只在最后一次大提交；失败或被预算阻断时先保存并提交已有可复核部分。输出最终Commit SHA、实际推理条数、剩余图像数、A1/D0解析率、A1/D0九类macro F1、PairAcc、作业GPU小时、每批剩余以及下一次恢复命令。模型/图片/环境不得上传Git。

**执行优先顺序（不要再用长时间重复审计代替GPU实验）：A0失败归档→A1开发/新验证→A1 Pilot100→D0 Pilot100（或视A1失败提前D0）→300→868；剩余图片下载从第一刻同步进行。**
