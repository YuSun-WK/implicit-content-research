# MSSBench｜Stage 2 加速复现：100 对扩展、截断诊断与原论文设置补齐（2026-11-20）

## 任务定位

你是 MSSBench (Multimodal Situational Safety, ICLR 2025) 复现工程负责人，兼可重复性审稿人。本轮强调**快速取得能在组会展示、能被第三方核对的真实测量数据**，不要重复 Stage0/Stage1 CPU 审计，也不要陷入模型下载循环。严格区分 A论文方法、B作者公开代码、C忠实信息流修复、D本地协议迁移。**本轮禁止新方法、训练、付费 API、复杂 Agent 框架，禁止声称替代模型就是论文 LLaVA 原模型。**

Repo: `YuSun-WK/implicit-content-research`；
分支: `repro/mssbench-multiagent-20261119`；
目录: `06_experiments/repro_mssbench_multiagent/`；
起始 Fast-track 结果提交: `9aff13aaec344409205bd9d2e320f95dabf71ccb`；Draft PR #79。
先做 `git status`，不得覆盖未提交文件；保留 Draft，不合并 main。查阅 `fasttrack_gate_report.md`、`fasttrack_B/fasttrack_metrics.md`、`fasttrack_B/fasttrack_cost.md`、`fasttrack_B/fasttrack_failures.md`、`fasttrack_B/fasttrack_run_manifest.csv`、`fasttrack_B/fasttrack_agent_traces.jsonl`、`fasttrack_qwen.py`、`stage1_smoke.py`、`fasttrack_export.py`、`manifest.py`、`journal.py`、`evaluation.py`、`sources.json`。除必要字段外不要重新扫描论文历史。

## 已确定的真实事实（必须从日志重验，严禁覆写）

路线 A 原论文 LLaVA 依然缺4大文件；没有 A 的GPU结果。路线 B 是已验证 `Sandy124/ThinkingGuard-8B@76892f9768ce828268265171f4bbc5dfb75eafc3`，**D 替代模型协议迁移**。B 的 G1+G2 以224预缩放、NF4、greedy、256 max_new_tokens、单 GPU、单模型实例完成20对/40输入×3方法=120 method-input，其中119 complete、1 format-invalid，199个真实调用（理论200），耗时2479.79s，显存增量8.191GiB。Chat CoT unsafe 2/10→MA unsafe 7/10；Embodied CoT safe 10/10 unsafe 2/10→MA safe 5/10 unsafe 5/10；Chat pair exact 2/10→7/10，Embodied 2/10→1/10。Base无显式分类；行为关键词不等于原论文GPT-4o Judge。

**重要新诊断**：49/199 个调用命中256 token上限，包括 Base21, CoT14, QA12, Chat Safety1, Embodied Safety1；其中一个 Chat unsafe Safety 没输出标签、跳过QA。不能把上限触发一律判为完整回答，也不能将任意一次非法输出归类为GPU工程故障。后续需同时报告 final-answer 完整性、显式标签解析率和输入安全正确率。

## 核心执行顺序（成功后连续推进，不要每阶段请示）

### P0：先做 CPU 数据扩展及运行器最小改造，不等待新模型权重

1. 固定并保留当前20对 Smoke 和原始256-token journal，不重新运行已完成的相同配置。配置、模型 revision、Prompt SHA、数据 SHA 都不可变。
2. 从固定 `combined.json` / `manifest.csv` 生成 **100个不同原始record的配对样本（Chat 60、Embodied 40）**，每对都含一条 Safe 和一条 Unsafe；必须包括原先 10+10 对（清楚标记 anchor smoke），再新增 Chat50对、Embodied30对。新的80对通过 deterministic seed `20261120` 选择，按 Chat 4类别、Embodied 5 subtask、`same_text`/ `different_text` 进行可行的分层；报告实际分配及无法严格均衡的层。为每个record固定一个query/text_index，不能先看模型输出再挑样本；优先避免跨记录 image content SHA 相同，所有排除理由可追溯。
3. 真实数据只下载新增80对涉及的图片（通常最多160个独立路径），按现有下载器固定 revision 和 SHA256+PIL完整解码；不要下载752图全集，除非额外材料确实需要。下载失败只修该图，不能偷偷换样本而不更新冻结清单。
4. **最小改造 runner**：允许传 `--pair-manifest`（冻结的 CSV），不再把 `smoke_inputs`/固定 `len(work)==120` 当成唯一运行入口。复用现有 Pipeline/Journal/evaluation/export，不重写 Adapter 或16个旧CPU测试。新增断点续跑、分chunk作业（建议每25对一片），并在每个作业结束可靠导出报告；保持 identical run identity，已 complete 或 terminal-invalid 不重复生成。新组允许从旧256 journal读取完成项：如需 merge，先做幂等行级校验、数据库备份和确切键一致性验证；更稳妥做统一索引聚合旧/新两个journal，禁止直接覆盖旧数据。
5. 纯CPU测试：冻结manifest配对数=100、分别60/40，same_text统计、Sha一致、每个方法×输入只有一个有效归属、恢复后不重算已有条目、GPU异常/Invalid分类正确。仅提交改动相关的新增测试，不再新建复杂审计体系。

### P1：优先完成 100 对的 **256-token 连贯扩展**（本次第一目标）

1. 使用**同一完整缓存** ThinkingGuard revision，已有基础环境，默认无网络、greedy/NF4/224预缩放/seed0。严格只用一张实际空闲 GPU，软件峰值<=20GiB，单次进程GPU<6h，按25对切片或动态余时终止。不要与其他用户抢卡。模型每片只加载一次，已有完成项尽可能复用不重复生成。
2. 原始20对仍沿用旧256-token结果；新增80对理论调用数：Chat50×2×(1+1+4)=600，Embodied30×2×(1+1+2)=240，合计**840次（若Agent无效可能减少）**。100对满规格理论1040次生成；最终必须按真实轨迹记账，不能按理论计。
3. 对每个输入保留 label、method、完整角色轨迹、prompt与上游传递字段、输入img SHA与text SHA、status（complete/invalid/engineering_error）、模型/处理器/量化/decode、真实token、时延、显存、token-cap hit。上游Safety invalid不执行QA，但下一个input必须继续；工程异常或哈希不匹配按可恢复异常策略停止该片，不丢已完成数据。
4. 汇报 Chat/Embodied separately：Safe正确/错误/invalid、Unsafe正确/错误/invalid、balanced accuracy（完整分母，invalid按未正确计）、pair两侧都正确、总完成率、invalid率、token-cap率。**Base不产生显式判断准确率**；只能报告行为描述。再分 Chat类别、Embodied类别/子任务和 Embodied same_text vs different_text。新扩展集里按记录聚类计算 bootstrap CI，并明确 100对含非随机 Smoke anchor，不得宣称全库代表性。
5. 对 CoT 和 MA 同一pair比较，分别报告 improved / harmed / tie（使用paired exact及同侧纠错矩阵）。避免把 MA 为更多 token 和更多调用带来的成本隐藏。

### P2：截断敏感性诊断（可与新增图片下载/CPU工作交错，但不应拖慢 P1）

1. 用**独立journal/不同decoding键**，在原100对中的固定10对（Chat 5、Embodied 5，按之前256命中上限和对立性分层预选）上以统一 **512 max_new_tokens** 完整重跑三方法；不要把512的一行和256的一行混在同一个Accuracy/成本表。先跑2对确认显存与耗时，再做剩余8对。
2. 对照同一10对的256-token结果，报告 label解析率、token-cap比例、最终行为字段是否完整、safe/unsafe准确率、pair exact、实际推理时延。注意：若 512 仍截断，不得无限增加至1024/2048；写明模型的多步思考造成的限制。
3. 若整体分母/协议不一致，禁止给出优劣结论。512只是预定义敏感性对照，不替换P1的100对256主表。
4. 人工审阅（无需用户手工标注）至少30个自动精选案例：Chat/Embodied、safe/unsafe、各方法、结构失效、错误修正、截断、同文本/异文本均覆盖。每例保留原图路径、query、模型原文、上游轨迹、自动标签和审阅理由；不凭空生成GT标注。
5. 原论文 GPT4 Judge 的0-3回答行为评估无法由关键词取代。当前仅自动粗筛; 可以在有限选例上给出**人工审阅草案**和审阅未确定性，但不能称得到了原论文的回答行为准确率。若考虑使用同一ThinkingGuard作本地judge，应先单列D探索性且不能作为主判定。

### P3：如果 P1 快速结束，优先补论文QC/IC设置（可选连续执行，不牺牲核心P1/P2）

可重用同100个原始record，按原文变体区别：QC 使用 query、IC 使用intent/单instruction，必须使用原始代码/论文对应字段和与输入一致的两侧图。按100对每侧一次，可分别再产生各200次分类调用。**QC/IC的输入分母及配对不同于IF**，不能因为同图就强制当做同样本ID；严格按原任务正确解释 Yes/No。单独的新journal/方法/配置、数据清单和独立表。若当前GPU预算不允许，先留同一个冻结manifest和待办记录，禁止拖延P1/P2。

### P4：原始LLaVA路线只允许离线进度维护，不能影响B扩展

如果共享可访问缓存已经出现四份完整A权重，按SHA验证、最小单图测试后再继续A的G1。否则将已固定的预置命令/哈希保留，说明必须在稳定网络机器或离线数据传输后才能完成A。**不再多轮低成功率HF/ModelScope传输诊断，不自动下载新的不相关VLM。**保持明确：B不是原论文LLaVA同模型复现。

## 核心可检验交付

在原目录追加 `stage2/...`，至少：
- `stage2/README.md`（真实命令、固定输入、环境、输入输出SHA和工作状态）
- `stage2/frozen_100_pairs.csv`、`stage2/strata_counts.csv`、`stage2/new_image_audit.csv`
- `stage2/results_256.csv`、`stage2/traces_256.jsonl`（可能体积较大，可提交完整摘要索引+按需片段；保留本地真实sqlite并附可复建位置）
- `stage2/metrics_256.md`、`stage2/paired_comparison_256.md`、`stage2/cost_256.md`
- `stage2/diagnostic_512.md`、`stage2/manual_review.md`、`stage2/gate_report.md`
- 代码：`stage2_select.py`、最小数据下载/通用 runner/export、相应单元测试；尽量复用现有文件，避免重复工程。
- 所有指标必须从真实SQLite/trace**编程重算**，并与提交的CSV、Markdown对账，不能由人手填表或把尚未运行的值写成真实测量。

## STOP/继续准则

- 新增的100对256数据若能正常完成、有效显式判定，按计划执行；格式invalid要真实留存，不能自动重试直到变正确。
- 如新增前10对中 Safety/Locator等关键字段invalid占比明显升高（例如>10%）或图文输入链断裂，先限量检查Prompt与源数据，记录诊断；**不要悄悄改模型Prompt并把前后结果混表**。
- 一张卡、<=20GiB软件显存、每次GPU job <=6小时，必要时缩成25对或更少的片段；不可因追求100对而挤占其它GPU任务。
- 不开始新模型开发、不做无验证的“Multi-Agent优于CoT”叙事；不从小样本得出充分结论。
- 本轮最终输出优先给用户一张**100对样本真实结果与配对成本**的表，再给512诊断；如果哪一步没有完成，明确精确实际运行数与唯一阻断，不要用准备完成代替实验完成。
- 提交分支并更新 Draft PR #79，不合并 main、不改变其它研究文件。
