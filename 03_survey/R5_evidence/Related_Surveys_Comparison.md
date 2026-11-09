# R5-E｜Related Surveys Comparison：相邻综述证据与定位对照

> 审计日期：2026-11-09；独立证据工作稿。对齐 main 的 R4-07 §1.2、R4-08 P0。仅根据**已访问的出版主页/摘要/既有R3证据**评价覆盖，未声称全文逐篇PRISMA复查。CCF等级按本项目采用的2026第七版口径；“待核”绝不擅定。会议等级与具体 Track 分列，Findings、Survey Track 与 Main 不混称。

## 1. 引言必须承认的先行综述

| 文献（项目编号） | 正式发表/CCF与Track | 审计能确认的核心范围；时间窗 | 对本综述造成的实质重叠 | 本综述可主张的**差异**，非“独家首创” | 证据与状态 |
|---|---|---|---|---|---|
| **Ge, Mao & Cambria, A survey on computational metaphor processing techniques: from identification, interpretation, generation to application**（本轮对比补入，不赋旧编号） | Artificial Intelligence Review 2023；**CCF等级待核**；期刊综述 | 隐喻的识别、解释、生成、应用；历史覆盖待全文核 | 已有跨隐喻“检测→理解→生成”体系，**不能把从检测转解释视为首次提出** | 本文把隐喻置于语用、编码、危害和多模态安全的不同GT下比较 | [DOI](https://doi.org/10.1007/s10462-023-10564-7)；出版/摘要已核，时间窗待核 |
| **Kühn et al., Computational Approaches to the Detection of Lesser-Known Rhetorical Figures**（P002） | ACM Computing Surveys，2025在线/2026卷58(2) Article 42；**项目R4标CCF未收录** | 较少研究的修辞格的定义、数据和检测；2024 arXiv为早期版本，正式卷期不等于预印本年 | 不能说尚无综合修辞综述 | 本文跨越修辞标签、狗哨、社区规范危害及风险响应，使用统一X/Y/G/E审计而非扩大修辞分类 | [正式DOI](https://doi.org/10.1145/3744554)、[DBLP正式卷期](https://dblp.dagstuhl.de/rec/journals/csur/KuhnMG26.html)、[arXiv早期版](https://arxiv.org/abs/2406.16674)；全文版本差异未核 |
| **A systematic review of figurative language detection: Methods, challenges, and multilingual perspectives**（新对照） | Natural Language Processing Journal 13 (2025), 100192；**CCF等级待核** | 隐喻/反讽/讽刺等修辞检测；从词汇至语用层、跨语言数据和方法；具体纳入起止年待核 | 不能把“修辞的多层分类和标注异质性”说成未被综述 | 本文考察语用意义、编码义、规范有害标签与T5/T6行为的不可互换性 | [出版主页/摘要](https://www.sciencedirect.com/science/article/pii/S2949719125000688)；摘要级 |
| **Farabi et al., A Survey of Multimodal Sarcasm Detection**（新对照） | IJCAI 2024 **Survey Track**；**按2026年第七版目录IJCAI为CCF-B（曾为A）**；Survey Track，非普通研究Full/Regular Paper | **2018–2023**多模态反讽文献；文/图/音/视频的模型、数据、评测 | 已有系统的多模态反讽研究述评；不能称本文首先跨文本和视觉研究反讽 | 本文继续关联编码、多模态图文安全的单模态/联合GT与安全回应，而非重新宣称首篇MSD综述 | [IJCAI正式页](https://ijcai.org/proceedings/2024/887)，DOI:10.24963/ijcai.2024/887；正式页可读、时间窗明确 |
| **Chen et al., A survey of automatic sarcasm detection**（新对照） | Neurocomputing 578 (2024), 127428；**CCF等级待核** | 反讽定义、任务、数据与不一致性/情绪/常识方法视角；纳入年份未从摘要核定 | 不能声称此前无人系统比较反讽的情绪和常识特征 | 本文从测试信息预算及标签、机制归因而非单个修辞任务方法谱系切入 | [出版主页](https://www.sciencedirect.com/science/article/pii/S0925231224001991)；摘要级 |
| **Mao et al., A survey on pragmatic processing techniques**（新对照） | Information Fusion (2025), 102712；**CCF等级待核** | 五项重要语用任务及理论、技术、应用；每项定义和起止年需全文核 | 无法声称“语用处理尚缺综述” | 本文跨语用到社会规范/隐晦危害及联合视觉安全，不把语用单独封闭 | [出版主页](https://www.sciencedirect.com/science/article/pii/S1566253524004901)；摘要级 |
| **Ma et al., Pragmatics in the Era of Large Language Models**（P011） | **ACL 2025 Main Long Papers，CCF-A** | 大模型语用能力的任务、数据集、标注设计与评价，包括含意/指称 | 与本文第2–3章实质重叠；不能说首次建立语用评估坐标 | 本文跨T1–T6，将不同GT、输入先验与语用到规范安全的断裂列作统一比较 | [ACL正式页](https://aclanthology.org/2025.acl-long.425/)，DOI:10.18653/v1/2025.acl-long.425；正式版 |
| **Hee et al., Recent Advances in Online Hate Speech Moderation: Multimodality and the Role of Large Models**（P007） | **EMNLP 2024 Findings**；EMNLP会议**CCF-B**，**非主会** | 文/图/音频仇恨，LLM/LMM 检测、解释、去偏和反言语 | **重要近邻竞争综述**：不能声称首次跨模态研究隐晦仇恨或首次统一检测与响应 | 本文从一般隐含意义、修辞、编码到危害/安全GT逐层区分，重点是可引用的X/Y/G/E证据门槛，而非仅moderation任务 | [ACL Anthology正式页](https://aclanthology.org/2024.findings-emnlp.254/)，DOI:10.18653/v1/2024.findings-emnlp.254 |
| **Spoken in Jest, Detected in Earnest**（P010） | IEEE Transactions on Affective Computing 16(4), 2025；项目登记**CCF-B** | 语音反讽到多模态融合的系统综述；具体覆盖起止年待核 | 已覆盖音频与视频反讽模型及评估挑战 | 本文不复述声学特征演进，改在任务标签与安全语义差别下对照 | [IEEE正式摘要](https://ieeexplore.ieee.org/abstract/document/11173951)，DOI:10.1109/TAFFC.2025.3612205 |
| **Ye et al., A Survey of Safety on Large Vision-Language Models**（新对照） | arXiv:2502.14881（2025，**预印本，CCF不适用/正式状态待核**） | LVLM攻击、防御、评估及生命周期分类 | 不能说此前缺少多模态安全综述 | 本文将**组合风险标签T5**与**响应行为T6**分开，且从语用/编码前驱谈跨模态隐晦表达 | [arXiv](https://arxiv.org/abs/2502.14881)；摘要级，尚未确认为正式论文 |

## 2. 与已有工作的实际区别：可主张 vs 不可主张

本综述的贡献应描述为**编辑性综合/批判性证据组织**（H），除非自行进行可重复的系统编码，不能假装已产生新因果定律或量化元分析。

| 对比维度 | 相邻综述已有覆盖 | 本文计划的可核查增量 | 稿件必须满足 |
|---|---|---|---|
| 跨现象 | 隐喻、反讽、语用、仇恨分别有较强综述 | 将隐含意义/修辞/编码/社群语境/多模态风险置于一篇工作性框架，**不是首篇** | Ch1限定领域与排除关系；列出至少P002/P007/P011/Farabi |
| Ground Truth | 现有综述已谈任务和数据 | 逐项区分现象T1、解释T2、交际T3、危害T4、组合风险T5、响应T6，以及人工/合成/政策/judge GT | 主表标注标注对象与标注者 |
| 信息预算 | 不同子域已经注意到语境、辅助信息、模态融合 | 对同篇实验登记 X 中是否含gold emotion、定义词典、检索结果、图像、特权提示与oracle | 不能把不同输入预算直接排名 |
| 可证性 | 普遍讨论模型偏差、因果/解释问题 | 将作者报告P、代码静态S、综合H、待核O分开；把反事实有效性、同预算模块消融、两侧安全误判列为claim gates | 不把怀疑写作事实；无实验不宣称解决 |
| 多模态安全 | 现有仇恨及LVLM安全综述已覆盖多模态 | 严格区分输入joint安全等级、单模态对照、响应拒答/有用性，不用ASR替代分类准确率 | Ch7的VLSU、SIUO、MSSBench须分组 |

## 3. 第1章 §1.2 可用的谨慎贡献表述

> 既有研究已分别对计算隐喻处理、修辞格、反讽、语用评测、仇恨内容审核以及多模态模型安全开展综述，包括ACL 2025的语用数据与评价综述、IJCAI 2024 Survey Track的多模态反讽综述和EMNLP 2024 Findings的多模态仇恨审核综述。本综述不主张首次涵盖某一种现象，而从“表达与隐含意义—交际功能—规范风险—多模态联合条件—安全响应”的不同操作性任务出发，以输入信息预算、标注目标、评价指标和机制证据等级为统一分析维度，讨论不同子域结论何时能够比较、何时不能迁移。此跨域对照是本文的组织贡献，并非已被新实验验证的机制理论。

## 4. 状态及引用检查

- **已关闭（书目级）**：P011 ACL 2025 Main、P007 EMNLP Findings、Farabi IJCAI 2024 Survey Track、P002 正式卷期与2024阅读版的区别。
- **部分关闭**：子域覆盖与本文重叠已基于正式摘要/官网确认；“五轴/T1–T6全局最完整”未做穷尽对比，不写。
- **未关闭**：各综述全文纳入条件与具体文献时间窗（除Farabi），若投稿前需要量化覆盖率须逐篇全文读并保留检索式；CCF待核期刊不能猜等级。
- **绝对禁用**：“首篇系统覆盖广义隐晦信息”“首次统一多模态安全与语用”“此前研究只关注隐式仇恨”“首次提出检测与响应的区别”。

上游基线：[R4-07](../R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)、[R4-08](../R4_writing/R4_08_Overall_Quality_Gate_20261109.md)、[R2-D](../R2_registry/Metadata_and_Evidence_Conflicts.md)。本次新增仅为相邻综述**对照来源**，不自动加入原91篇主分配，也不覆盖R0/R2历史目录。
