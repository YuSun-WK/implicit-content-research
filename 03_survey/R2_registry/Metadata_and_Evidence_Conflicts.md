# R2-D｜元数据与证据冲突登记

日期：2026-11-08（Asia/Shanghai）。用途：记录统一目录的未关闭核验项；本文件不作创新点判断，不构成综述正文。

## 口径与覆盖

- 统一目录为 **91 篇独立论文**：R0 的 P001–P041（41 篇）、T001–T018（18 篇），以及 R2-A 的 R2A-001–032（32 篇）。规范化题名检查未发现跨组同名；R2-A 原有“32 篇不在 R0”的判定保留。P002、P026 的多版本来源，以及 P009、P023 的原上传表重复，均不另计论文。见 [R0 审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R0_inventory/R0_Audit_Report.md)、[R2-A 账本](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/R2A_Candidate_Ledger.md)。
- 16 篇 R2-A 候选已有 R2-B 单篇精读卡；其余 16 篇保留临时编号，列为“尚未核实候选”。“尚未核实”指全文、数据或代码层级仍不足；R2-A 已记录官方出版页元数据，不能误写成未发表。
- CCF 等级采用项目此前按 [2026 第七版目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml) 核验的刊会等级；实际 Track 另列。**论文已发表、官方页面可见、数据可得、代码可运行、实验指标复现**是五个不同状态。12 项审计资源均未完成训练或端到端指标复现。[资源与代码审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md)。
- 工作簿中“PDF 核验状态”为“按官方页路径推定”的链接只是待打开核验的定位线索，不能当作已实读正式 PDF。部分评价指标为阅读卡线索，引用具体数值前须核对实验切片。

## 出版、版本与分类冲突

| 编号 | 冲突或边界 | 当前处理与下一步 | 证据 |
|---|---|---|---|
| P002 | 2024 arXiv 阅读版与 ACM Computing Surveys 正式版不同；正式版 2025 在线、2026 卷期，正式 DOI 10.1145/3744554。 | 只计同篇一条；正式出版信息与阅读版年份分开；全文差异待对照。 | [R0 审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R0_inventory/R0_Audit_Report.md)、[正式 DOI](https://dl.acm.org/doi/10.1145/3744554) |
| P006、P009 | 上传表与仓库/在线年、卷期年口径不同。 | 保留 R0 原年份及开放问题，核对期刊官网正式卷期。 | [R0 总索引](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R0_inventory/Literature_Inventory.xlsx) |
| P039 | ACM MM A 级刊会、作者录用/DOI 线索已见；正式出版页与实际 Track 未核。 | 不把录用/DOI 直接升格为已正式出版；待核 ACM 会录。 | [R0 审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R0_inventory/R0_Audit_Report.md) |
| T014 | NeurIPS 2024 为 Datasets & Benchmarks Track。 | 记录刊会 A 与实际 Track；不按普通 Main/Regular 论文混计。 | [R0 审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R0_inventory/R0_Audit_Report.md) |
| R2A-010 | SeTox 作者仓库 README BibTeX 的标题、作者、页码与 ACL 正式记录不一致。 | 目录以 ACL 正式记录为准；保留仓库冲突待作者修订。 | [ACL 正式页](https://aclanthology.org/2026.acl-long.1602/)、[代码审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md) |
| P016、P018、P022、P025 | R0 关联层级与 R1 任务映射有边界调整，尤其 P025 是跨模态隐式仇恨研究，P022 同时涉及抽取/分类/解释。 | 统一目录保留 R0 原标注，同时把 R1 主任务单列；分类采用 R1 修正并留证据链接。 | [R1 任务映射](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R1_taxonomy/R1C_Task_Mapping_DRAFT.md) |
| P026/P027/T001–T004/T014–T016 | 普通 Hateful Meme 图文输入不自动证明“单模态安全、组合后有害”的 T5。 | 保留 T4 或方法相关；只有任务/标签证据支持时才列 T5。 | [R1 任务映射](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R1_taxonomy/R1C_Task_Mapping_DRAFT.md) |
| R2A-003、R2A-027、R2A-028 | R2-A 任务栏是候选阶段的关联任务；精读卡分别将三元组意图表征诊断归 X2，将 MSSBench、MOSSBench 的主要安全响应/误拒评测归 T6。 | 统一目录保留 R2-A 原关联任务字符串，同时用精读卡修正主任务；不把输出行为指标改写成输入风险分类指标。 | [R2A-003 卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_03_Negation_vs_Implicature.md)、[MSSBench 卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md)、[MOSSBench 卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md) |

## 12 项数据资源的规模与复现缺口

“公开观察”列只陈述已审计文件、页面或既有卡所见。论文声称规模不等于可下载、可运行规模。证据级别 A=文本实读，B=官方页面/树/数据卡，D=沿用既有卡实读；均不表示实验已复现。全部逐项字段、代码入口、Ground Truth 与潜在捷径见 [原资源审计表](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Dataset_Access_Audit.xlsx) 和本目录的 `Dataset_Evidence_Matrix.xlsx`。

| 资源（编号） | 论文/作者口径与当前公开观察 | 未关闭问题及风险性质 | 主要证据 |
|---|---|---|---|
| DRInQ（R2A-001） | 论文 819 人类共识样本、400 困难集；公开 CSV 实读 231 行、148 个问句（A）。 | 231 与 819/400 的版本/映射未释；缺完整困难集和完整评测脚本。同问句跨语境、选项顺序和生成模板是**潜在**捷径。引言 76%/89% 与 Table 2 困难集 67%/88% 口径不同，不得合并。 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_01_DRInQ.md)、[公开 CSV](https://github.com/hjarai/drinq/blob/main/drinq_validated.csv) |
| VAGUE（R2A-002） | 论文 1,677；HF viewer 约 1.68k、README 称 1,677，未逐行下载（B）。 | 原图和字段需逐项核验；solution/direct/caption 等字段在样本内，评测提示隔离和源图分组需实测。GT 为人工筛选的构造目标，不是现实说话者的可观测意图。 | [数据页](https://huggingface.co/datasets/HazelNam/vague-bench)、[资源审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md) |
| CodedLang（P023） | 论文 7,744 评论、900 编码正例；大 CSV 存在，审计接口未返回内容，实数未重计（B）。 | 官方 split/可执行评测脚本未见；词项、商家、模板交叉与答案字段暴露是**待测**风险。 | [官方数据树](https://github.com/Crowd-AI-Lab/CodedLang/tree/main/Data)、[P023 卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P023_CodedLang.md) |
| Silent Signals（R2A-006） | 论文主集 16,550、检测 100、消歧 124；README 主集 16,258、检测 viewer 101、消歧 124（B）。 | 主集差 292、检测差 1；须核文件版本和标签值。主集词典/GPT-4 筛选不等于全量人工二分类金标。 | [数据卡](https://huggingface.co/datasets/SALT-NLP/silent_signals)、[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_01_Silent_Signals.md) |
| FETCH!（R2A-007） | 论文使用约 16k、Gab 与 700 万 Twitter 帖等场景；公开仓库有重建脚本，未见完整原始帖/索引包（B）。 | 无可核全量行数；社媒语料、词典及环境依赖待验，代码静态审计发现可能的运行问题，但未端到端执行。词典匹配不是逐帖人工编码义金标。 | [作者仓库](https://github.com/KuleenS/FETCH-Dog-Whistle)、[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_02_FETCH.md) |
| SeTox（R2A-010） | 论文词典 974、训练 995+600、测试 624+368；实读四个 JSON 为 974/600/624/368，995 仅据 README（A+B）。 | 995 的 train_tool 大文件待实读；词项交集、搜索结果答案暴露和在线时间漂移为潜在风险；live search 需 Serper。 | [数据树](https://github.com/thu-coai/Setox/tree/main/data)、[资源审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md) |
| M3UCD（R2A-017） | 论文 15,345、每条 12 属性；所引仓库未见可下载数据，公开行数未知（B）。 | 不写“公开 15,345”；需取得数据、标签字典与官方 split；当前无法测试跨来源重复。 | [作者仓库](https://github.com/DragonReed/M3UCD)、[资源审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md) |
| MET-MEME（R2A-018 所用数据） | 原作者 README 为 10,039；第三方 HF 为 10,030，Kaggle 包未下载（B）。 | 差 9 的版本来源未知；Kaggle 实物、官方 split、与 M3UCD 复用重叠待验；未找到 MGMCF 作者官方实现。 | [Kaggle 入口](https://www.kaggle.com/datasets/liaolianfoka/met-meme)、[资源审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md) |
| VLSU（P038） | 论文 8,187；既有卡 CSV 实读 8,159，差 28；本轮只确认文件仍在（D+B）。 | 外链图片成功率未知；not_sure 141 条与三类标签口径、类别分布待核；统一评测脚本未见。 | [P038 卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md)、[公开 CSV](https://github.com/apple-aiml-research/ml-vlsu/blob/main/data/VLSU.csv) |
| MSSBench（R2A-027） | R2-A 称 1,960，项目页摘要 1,820；HF viewer 724 张图，完整问答对未逐条计数（B）。 | 三种口径不可直接互换；需核 combined.json、图像及 Chat/Embodied 配对。此资源评估视觉情境安全，不能一律写作 T5 的单模态安全/组合危险。 | [数据树](https://huggingface.co/datasets/kzhou35/mssbench/tree/main)、[资源审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_dataset_audit/Code_Reproducibility_Audit.md) |
| MOSSBench（R2A-028） | 论文正式摘要/表与主 JSON 为 300 安全查询；仓库树列 304 主图/244 对照图（A+B）。精读卡另按 PID 与 Blob SHA 静态核对 244 对：198 同图异文、43 异图同文、3 双变化。 | accepted PDF 仍残留 544 口径；AMT 中约 9% 被多数评为不能无害回答，逐例原始票未公开；故 300 条的“绝对安全”GT 有争议。对照仅 244 对，不是完整 300 严格反事实；HF 对照 viewer 报错。拒答率是模型行为，不是输入有害金标。 | [精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md)、[官方数据树](https://github.com/turningpoint-ai/MOSSBench/tree/main/data) |
| V-FLUTE（P019） | 论文与 HF README split 元数据均合计 6,027；约 4.8GB 实物未下载（B+D）。 | 图像近重复与来源分组、F1@53 测试子集阈值校准独立性待审；代码/权重可见不等于训练指标复现。 | [数据卡](https://huggingface.co/datasets/ColumbiaNLP/V-FLUTE)、[P019 卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P019_V-FLUTE.md) |

## 共同待核事项

1. 将“人类共识”“构造任务目标”“词典/伪标签”“专家审修解释”“模型拒答行为”分别作为 Ground Truth/观测类型，不能统称真实意图或人工金标。
2. 对同问句、词根、图像、meme 模板、原始数据集、时间和社群进行分组重测后，才可判断是否发生数据泄漏。本登记只记录**潜在**泄漏与捷径。
3. 取得缺失数据和官方划分，核查代码、权重、依赖和许可，再单独记录训练/推理执行结果。现有记录没有任何一项实验复现完成。
4. 对 16 篇尚无 R2-B 精读卡的 R2-A 候选，补足正式 PDF 全文、Ground Truth、评价协议、数据和代码核验；不要由题名或刊会等级推出实验结论。
