# MSSBench Fast-track｜立即解除权重阻断，获得真实 G1/G2 结果（2026-11-19）

你是 AI Security / VLM CCF-A 复现负责人，也是具备实测责任的工程负责人。本任务目标是**尽快获得真实、可追溯的 Base / 1-step CoT / Multi-Agent 对比数据**。速度优先于重复审计，但不得牺牲结果的真实性。不要再把任务仅变成下载诊断。

## 0. 工作现场与既有成果（必须先读）

- Repo `YuSun-WK/implicit-content-research`，分支 `repro/mssbench-multiagent-20261119`，目录 `06_experiments/repro_mssbench_multiagent/`。
- 起始提交 `a23c9713f114ac451439b9486bdb6ef5a5448329`，Draft PR #79。
- 优先读 `stage1_fix_gate_report.md`、`stage1_fix_retrieval.md`、`stage1_fix_weights.csv`、`model_adapter_review.md`、`stage1_native.py`、`stage1_smoke.py`、`pipeline.py`、`journal.py`、`evaluation.py`、`sources.json`。
- 已完成：固定 MSSBench 1960 inputs、20 对 Smoke 图像40/40哈希与解码、16项CPU测试通过、原生LLaVA CPU构建与预处理通过、独立 venv 基础兼容。
- 未完成：原生权重的4个大文件约 15,837,883,537 B；其余8/12已校验。G1/G2真实GPU调用 **0**。当前 downloader 在 HF/ModelScope 下载慢且断流，不能再无限次同策略重试。
- 先执行 git status，保护任何未提交改动；不得覆盖其他实验、提交权重或合并 main。

## 1. 本次采用两条路线并行准备（结果绝对分开）

**路线 A（忠实复现优先）**：原论文已测试的 `liuhaotian/llava-v1.6-vicuna-7b@deae57a8c0ccb0da4c2661cc1891cc9d06503d11` + CLIP 固定版本 + 原生 `haotian-liu/LLaVA@c121f0432da27facab705978f83c4ada465e46fd`。沿用 SHA256、修复版 C 信息流；原生模型4-bit、224像素策略、128输出token均标记为**本地资源/生成协议差异 D**。只有官方权重SHA一致、原生模型运行成功才能声称是「同原模型的本地量化复现」。

**路线 B（并行打通真实多 Agent 研究）**：只在路线 A 无完整模型权重且短期下载仍不可行时，盘点并使用服务器**已有且完整的**开源 VLM checkpoint，优先已缓存的 LLaVA/Qwen2.5-VL-7B/Qwen3-VL-8B 等 7–8B，实在没有可用的则检查已缓存的3B级VLM。必须确认本地权重完整、processor/tokenizer可用和可离线运行。B 严格标记 `D: protocol-transfer / substitute model`，有独立 adapter/model revision、结果目录、表格；绝不能将 B 冒充 LLaVA 或与论文 LLaVA 数值视作完全复现。沿用原任务、固定输入、角色、Prompt、同一模型比较 Base/CoT/MA。不能为了 B 开始又下载同等大小的另一套权重。若没有完整本地替代模型，说明原因并给出最短人工传输方案。

**执行优先级**：先并行完成 A 权重来源盘点 + B 完整现有模型盘点，不再重复旧版全面审计。确定可立即运行的路线后优先获得首条真实 GPU 轨迹。A 仍需继续通过可靠缓存获取文件，但不得因 A 卡住而阻止已缓存 B 的实验。

## 2. A 权重获取的严格策略（不要再重复低效下载）

1. 先只读搜现有 HF_HOME/HF缓存、旧实验目录、共用数据卷、可访问的本地镜像/挂载目录、pip wheel 缓存；根据文件体积+SHA检索可能完整的3个LLaVA shard与CLIP（**不能扫描整盘内容作昂贵逐文件SHA；先按文件名/尺寸粗筛，再哈希候选**）。查已有服务器间共享模型仓库/可访问可信文件位置。不要遍历他人的私有目录或绕过权限。
2. 官方HF和已验证元数据同SHA的 ModelScope都可作传输来源，最终全文件必须等于 `stage1_fix_weights.csv` 的**官方SHA256**。下载工具尽量支持断点续传、单文件分块持久化、指数退避和原子完成；避免五个巨型并发任务被一个失效代理全部拖死。
3. 只做有限的网络健康诊断（例如小范围/小块真实吞吐测试），优先选能持续传输的路径。不得反复进行 64MiB/4MiB 永久重试；如果持续吞吐不足以有效取得剩余约15.84GB，**立即切换到 B，保留 A 部分缓存**，不要以无休止的重试阻断主任务。单独输出可用的人工离线传输命令、目标目录、expected SHA和最小校验步骤（仅在确实缺文件时）。
4. 严禁通过仅文件名相同或远端metadata匹配就跳过全文件校验；`weights_verified.json` 必须在所有资产实际完整且SHA吻合时生成。

## 3. 真正的 GPU 最小闭环（这是本轮第一交付）

- 在固定数据和已通过解码的40图上操作，不再重复下载数据。对 B 编写**独立、最小** VLM adapter 实现 `generate(prompt,image|None)->Generation`，重用已有 Pipeline/Journal/Evaluation，**不重写已有16个CPU测试**。确保模型只加载一次，Chat 四 Agent(意图text-only→caption→风险判断→QA)，Embodied 两 Agent；A 和 B 的模型包装/对话模板差异完整记录。
- 开始时只用一张实时空闲GPU，单卡软件显存预算严格 **<=20 GiB**、batch1、4-bit优先、greedy、max_new_tokens=128起步，若格式截断可调整至256但必须标记新配置。每次GPU任务<6h，保留 resume。
- **微型单调用探针**：一条 text-only，一条图像条件生成。若加载或视觉输入失败，先修模型适配，不要继续G1。
- **G1 两个配对**：从原 Smoke manifest 选 1对Chat + 1对Embodied（4个输入），同模型 Base/1-step CoT/Multi-Agent，理论20次调用。记录全部 Agent 提示词、原文输出、父调用和中间文本、image hash、原图/processor尺寸、真实token、时延、GPU peak、无效输出、错误类别。
- **G2 20对**：如果 G1 工程链/预算可运行，立即复用 SQLite 继续完整 20对/40输入，三种方法计划200次生成（G1成功完成的条目复用）。不要拿原论文准确率作通过阈值；同方法同样本同模型公平比较。
- **无效输出必须真实保留**：严格评估任务和运行器健壮性分别报告。不要把模型没按照格式给 `Potential intent activity` / `Answer: Yes/No` 等等直接归为权重/图片失败；不要用标准答案或手工补写中间结果。单个样本的无效输出应保留 invalid 和完整轨迹，防止一个无效样本让全部G2永远不能前进；若放宽之前的 `stop_on_invalid`，必须添加明确版本号和独立报告，不得在输出结果中忽略失败分母。上游无效时不得虚构下游。
- 运行之前审计 `stage1_native.py` 中原生配置注入、bnb 4bit属性、vision tower位置、mixed torch 2.9 / Transformers4.37 / Accelerate1.12的实际运行兼容性；发现问题只做最小修复，并记录影响。不得静默把模型改成别的权重。

## 4. 评测与报告：先有真实输出，再追求完善的 Judge

- 明确 Chat `Answer:Yes`=Safe，而 Embodied `Unsafe hint:Yes`=Unsafe。Base 无显式分类不能编造输入分类Accuracy。
- 先产出 safe/unsafe各组：completed/invalid、显式判断正确数（CoT/MA）、Pair两侧都判对数；以及 Base/CoT/MA 逐角色调用次数、总input/output token、总耗时、峰值显存。
- 对最终自然语言响应做保守的规则粗分、保留 Unknown、做至少8–12条人工审阅候选清单；不调用付费Judge、不宣称是论文官方 GPT4-judge评分，不强行将所有响应判成0–3。
- 输出完整 QA 与中间推理示例、典型失败案例；禁止把「多Agent调用更多/回答更长」自动解释成「能力提升」。
- 若目前只具备 B 而 A 仍无权重，组会报告应明确「原模型仍阻断；替代模型协议迁移 G1/G2 已跑通」，绝不混在一张原论文官方表里。

## 5. 并行工作与硬停止

- 可以让无GPU的缓存盘点/下载核验与真实推理B并行，但GPU只使用一张且不挤占他人任务；所有下载/模型加载任务有资源上限、失败时保留日志。对任何来源敏感信息如签名URL、token、代理密码、下载cookie，不要写GitHub。
- 无可用完整模型 / 背景权重未校验 / 需要不受控的大模型下载 / 内核持续OOM / 模态未进入模型 / 输出没进下游 / 数据manifest不一致 → STOP该路线并如实报告，**其他可运行路线继续**。
- 模型推理开始之前只做必要最小验证。不要继续重复论文已有审计、ModelScope仓库历史、HF Table1 20条差异、CPU Mock或长篇环境说明。
- 本轮**不自动开始** Pilot(50-100)、Expanded/Full、消融、额外数据集训练或大规模LLM Judge。

## 6. 交付（必须有真实证据）

在本项目目录提交：
1. `fasttrack_gate_report.md`：每条路线A/B状态，实际模型名称、revision、凭证校验、GPU ID；每个阶段PASS/PARTIAL/FAIL。
2. `fasttrack_model_inventory.md`：已存在完整checkpoint清单及可用性、权重是否复用，没有时明确记录。
3. `fasttrack_run_manifest.csv`、`fasttrack_results.csv`、`fasttrack_agent_traces.jsonl`（可按隐私与体积选提交小量可审阅样本，完整文件保持本地并附可复建路径）。
4. `fasttrack_metrics.md`：按Chat/Embodied + Safe/Unsafe + Base/CoT/MA，区分行为统计与输入分类。
5. `fasttrack_cost.md`：模型加载次数、逐Agent calls/token/elapsed、显存峰值、总耗时和保守Pilot运行量估算（**只在实测后外推**）。
6. `fasttrack_failures.md`：真实错误、无效输出、审阅至少8条；A与B差异；任何修复的代码diff和验证测试。
7. 保留官方、模型、dataset、prompt、adapter各 SHA；提交 GitHub 本分支并更新 Draft PR #79，**不合并main**。

最终回答必须先说明：当前有没有跑出 **真实** Base/CoT/Multi-Agent 指标；如果有，用同一批样本分组报告结果和成本；如果没有，说明**唯一剩余的实质阻断**，不能只回复「环境/代码准备完成」。
