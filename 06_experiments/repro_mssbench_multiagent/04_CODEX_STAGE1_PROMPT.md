# MSSBench Stage 1｜数据版本核定、原始 LLaVA 适配与分级 GPU Smoke

日期：2026-11-19。承接 Stage0 @ `a12eef6410fa4561e6fc20fb0803c176dd2aea68`；PR #79。**先 CPU 和数据，再小规模 GPU；不得训练、使用付费 API 或运行 Full。**

## 角色与原则

你是 CCF-A 方法复现审稿人 + 多模态实验工程师。仓库 `YuSun-WK/implicit-content-research`，只在 `repro/mssbench-multiagent-20261119` 分支、`06_experiments/repro_mssbench_multiagent/` 内工作。先 `git status`，保护未提交修改；不要合并 main。审计固定官方源码 `1602193f49cb6925bfa3751be157d0bbf5439779` 和 HF 数据 `12396d24157427b671d97f23a2e370fca98fdf55`。以已有 `sources.json` 和 `manifest.py`、`pipeline.py`、`journal.py`、`evaluation.py` 为起点，**不要推倒重写**。严格区分 A论文、B公开代码、C修复忠实方法、D本地模型/Judge/量化/图像预处理改编。

## 先复核 Stage0 审查发现（优先级 P0）

- Stage0 测到 376 条原始记录、980 对 query 展开、1960 个 Safe/Unsafe 输入，Chat 600 对与 Embodied 380 对；Chat 全部同文字，Embodied 150 对同文字、230 对不同文字。752 个远端图片路径，31 组远端内容重复哈希；未实图解码。
- Embodied 类别统计：论文 Table1 Physical Harm 120 / Property 640；固定 HF 版为 140 / 620，总体 760 不变。**这不是自动判定标签错误，不可为了凑表格修改原标签**。审计论文、补充材料、官方 repo 和 HF revision 历史的证据，列出具体可能不同的 record_index、每条原始类别/任务/文件。若无逐条原始证据，保留 HF 分类并明确「发布版协议」；允许继续**功能性 Smoke**，但不得称严格复现 Table1 类别分组。类别差异不得作为后续无限审计借口。
- Stage0: 官方 Multi-Agent B 有缩进、无 Visual、丢 Intent 和 QA Route 等缺陷；C 的 CPU Mock 7项 PASS，但没有真实生成证据。保持所有步骤的真实流入/流出，并用输入敏感性测试（替换 Intent/Caption/Safety 后下游渲染 Prompt 真的变化）再次验收。

## Step 1｜CPU 数据与图片完整性

1. 读取 `data_audit.md`、`smoke_pairs.csv`、`smoke_images.csv`、`data_audit.json`。只下载 **40 个** smoke 目标文件（远端预估 38,483,771 B），严格锁 HF revision。先查缓存，可复用不可重复大目录。不能下载全仓和全图。
2. 按 `smoke_images.csv` 映射下载，限制相对路径和文件大小，原子写入，失败重试上限固定；核对字节数、HF LFS SHA256、PIL.verify、重新解码 load、尺寸、mime、RGB可处理性。建立 `image_decode_audit.csv`、`smoke_image_gate.md`，生成可追踪异常清单；**不要把远端存在等同于已解码**。
3. 针对 Embodied 20 条分类差异，提供 `table1_reconciliation.md`：事实/推测分开；记录所查数据revision、论文表格、每个可能受影响的原始记录。无法追溯到逐条证据则写 unresolved + 可继续的功能性 Smoke 范围。
4. 核查 20 对是否确为 10 Chat + 10 Embodied，40 个 Safe/Unsafe 输入；不能用 20 输入冒充 20 对。根据实际图像解码结果，确认本轮 smoke manifest 是否须替换损坏图并记录理由。

## Step 2｜原论文 LLaVA-1.6 7B 兼容性

1. 先重新记录 CPU/GPU、磁盘、RAM、占用和 Python/CUDA 版本。单卡共享环境避开正在忙的 GPU；设置 `CUDA_VISIBLE_DEVICES` 指向一张空闲卡，不影响其它任务。
2. 首选论文原生 `liuhaotian/llava-v1.6-vicuna-7b@deae57a8c0ccb0da4c2661cc1891cc9d06503d11` 与 `haotian-liu/LLaVA@c121f0432da27facab705978f83c4ada465e46fd`；检查原生环境兼容矩阵及必要 CLIP 依赖，锁版本并隔离 venv（Python3.10）；**不得升级/破坏其他实验环境**。下载模型和视觉权重必须确认目标路径、缓存策略、空间余量，完成 sha/etag/size 校验。
3. 若原生依赖确实无法在当前环境可靠执行，优先考虑同架构转换版 `llava-hf/llava-v1.6-vicuna-7b-hf@c916e6cdcd760b4cecd1dd4907f84ac649f93b23`，先核查 tokenizer、processor、模型映射、对话模板、图像缩放/anyres、生成解码。**转换版本结果标为 D/compatibility adaptation，不等同原生实现**。本阶段不切 Qwen2.5/Qwen3-VL 等新模型。
4. 创建单份 VLM adapter，提供 `generate(prompt: str, image: Path | None) -> Generation`，模型权重全程仅加载一次。Intent Agent text-only 必须得到真正无图片输入（而不是重复传图）；其余所需 Agent 正确读取同侧图片。batch=1、4-bit NF4优先、greedy、记录 seed、tokenizer、precision、image processor、停止条件。原作者 B 对本地图强制 224x224，要保存 B 设定与原生 any-resolution 的差异，不得静默切换预处理或把不同协议混成一条成绩。
5. 推理阶段使用 `torch.inference_mode()`、单 GPU、最大生成 token 先 128；实测不足时再按统一规则提高到 256，同时记录与原版 max 512 的差异。软件显存峰值以 20GiB 为硬预算；**虽然驱动报告约49GiB，但不能据此放宽用户预算**。如果稳定超限，先缩短上下文/生成和检查图像切片，不能默认卸载重载同一权重。
6. 每次调用记录输入/输出 token、耗时、CUDA allocated/reserved、NVML、模型权重加载次数、实际 image dimensions、error；同步保留原始中间输出。Adapter 必须有最小真实模型 text-only 和 image-conditioned 测试。

## Step 3｜分级真实 GPU 运行与门槛

**G0（仅 CPU/下载，必须先通过）**：40 个图片逐个 decode + SHA 匹配，manifest 可重建，模型环境/adapter实现和参数清楚，单元测试通过。若任何必要文件不可获取，报告原因和替代选择，不捏造成功。

**G1（极小端到端探针，先做）**：仅选择 1 对 Chat + 1 对 Embodied，即 4 个图文输入，分别运行 Base、1-step CoT、Multi-Agent；计划调用 2*(1+1+4) + 2*(1+1+2) = **20 次模型生成**。必须保留全部角色轨迹，证明 Prompt/图像/角色链和 QA Route 在**真实 LLaVA**上正确；测 GPU 峰值<20GiB，记录每角色耗时/真实 token/Invalid。任何 OOM、无意义输出、视觉未送达、模型二次加载、错误安全判断方向 -> STOP 调试，不进入 G2。

**G2（20 对 Smoke）**：只有 G1 PASS 且测得保守用时外推可在单次 <6h完成后才运行 `smoke_pairs.csv` 全部 20 对、40 个输入：10对Chat×2×(1+1+4)=120 + 10对Embodied×2×(1+1+2)=80，共 **200 次模型调用**。三种方法对同批样本使用同一模型 revision、解码和图像协议。输出 `smoke_results.csv`、`agent_traces.jsonl`、`smoke_metrics.md`、`resource_measurements.md`、`stage1_gate_report.md`。如计算预算不够、模型故障或数据问题，则停止并保留 G1 结果。

**本次不要自动继续**到 Pilot、Expanded Pilot、Full、正式消融、IC+self/GT或大型本地 Judge。后续单独审批。IF/CoT/QA 最终回应可由规则作行为粗筛，并用小量人工例子审阅；不要把规则/本地 Judge 叫成作者 GPT-4o 评分。QC/IC 路线仍保留在实验矩阵，先不混入 200 次主 Smoke。

## Step 4｜修正协议与工程缺口

- 对 Stage0 `Pipeline` 的 Chat Safety Prompt 拼接（`\nImage caption:`）、QA Yes/No/Else 的多层条件、Intent text-only 与 Captions，逐一核对论文 Appendix A.7 和原始 Prompt。属于 C 的额外字段命名或中间文本拼接需要单列为可追溯「实现解释」；遇到论文模糊处，禁止声称逐字忠实。
- 验证 `response_for_judge` 在 real output、CoT `Query answer`、Embodied `Response to instruction` 的鲁棒性；字段不合法保留 Unknown，不当作 Safe/Unsafe 分类。
- 复用 `journal.py` SQLite 幂等 key，测试程序中断、重新启动时跳过已完成输入而保留故障尝试。必要时修复 exception/trace schema，写修复日志。
- 分类别结果明确用 HF 数据标签口径；结论同时报告 per-pair 两侧都对的指标、Chat/Embodied 拆分、不可解析率、总 token /调用数 /耗时；样本很少，不能拿单个 Smoke 结论做显著性宣称。

## 必须交付与 STOP 条件

文档：`stage1_README.md`、`table1_reconciliation.md`、`image_decode_audit.csv`、`smoke_image_gate.md`、`model_adapter_review.md`、`model_environment_lock.md`、`stage1_gate_report.md`。
代码：版本锁定的 VLM adapter、G1/G2 runner、端到端测试、续跑单元测试；不要覆盖原作者 B 快照和其它实验。运行日志：G1 全 Agent 调用，若 G2 通过则 20 对完整 trace/成本/初步结果。
STOP：无法确认数据/图像真值、LLaVA 实例不稳定、峰值>20GiB、输出/路由无法解释、单次GPU预算外推≥6h、任一 Agent 丢失上游输入、结果无法从固定版本重建、需要付费API。出现 STOP 时提交已有真实结果及 blocker，不要自行替换模型或假报完整性。

最后更新 PR #79（保持 Draft），提交本阶段代码与报告，记录 commit SHA、确切运行命令、G0/G1/G2 PASS/PARTIAL/FAIL、实际 GPU ID、峰值显存、调用次数、token、耗时、未解决风险和**下一步唯一建议**。不得自动合并 main。
