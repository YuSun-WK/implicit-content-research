# R2-C｜文献覆盖、Ground Truth与学术证据审计

> 日期：2026-11-08；状态：**R2-C阶段审阅稿**。R2-C是已收集文献的机制和证据综合，**不是**对2024–2026全部CCF-A论文的PRISMA穷尽检索；也没有对各论文进行独立GPU复现。本文件只补充决策与审计，不覆写R0/R1/R2精读卡、CSV、XLSX。

## 1. 范围与盘点结果（严格区分“收录”与“精读”）

| 资产 | 数量 | 实际口径 |
|---|---:|---|
| R0去重文献 | **59** | P001–P041共41 + T001–T018共18；R0已核对CSV与用户导出清单 |
| R2-A额外候选 | **32** | R2A-001–032，标题未在R0的59篇中出现；官方会议页/摘要层核验，**并未全部全文精读** |
| 已知候选联合清单 | **91** | 59+32，仅表示当前两处账本的题名去重候选，不等于91篇A会、91篇精读或领域总量 |
| R2-B新精读卡 | **16** | B1=4，B2a=3，B2b=3，B3a=3，B4a=3；均对应R2A编号 |
| R2-A尚未完成R2-B精读 | **16** | 余下候选中部分为方法支撑、关联、次优先级，不意味着16篇必须全部读完 |
| R0原始阅读卡 | **27** | R0当时有21“已精读”+6“已分析精度待核”；另P031待审记录；这些状态不同于R2-B |

刊会等级按 [CCF第七版（2026）](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)统一：ACL/AAAI/ICCV/CVPR/ICLR/ICML/ACM MM为**CCF-A刊会**；EMNLP/NAACL/COLING为**CCF-B刊会**。**会议/期刊被列A≠论文实际Track或发表状态自动属于A类主会常规论文**：Findings、Industry、Workshop、Companion、Datasets & Benchmarks和作者录用应单列。

R0原有29 A / 23 B / 6未收录 / 1不适用的盘点不因新候选而被追溯改写；正式综述需在**统一91篇主索引**中按任务多标签而不是机械延续R1的59篇单标签计数。

## 2. 各学术脉络的覆盖裁决

| 脉络 | 当前证据密度与代表（正式刊会/CCF） | 覆盖裁决 | R3建议 |
|---|---|---|---|
| 语用含义/间接意图 | P011/P020 ACL2025 A；DRInQ ACL2026 A、VAGUE ICCV2025 A、Negation-v-Implicature ACL2024 A、Rhetorical Questions ACL2026 A | **基本具备**：T3不再是R0中“0篇”的叙述；候选选择、表示与内在意图区分 | 作为理论-行为-表征三层，不再大量补读 |
| 编码、狗哨与动态词义 | P023 ACL2026 A；Silent Signals ACL2024 A、FETCH! ACL2025 A、FA-Net AAAI2024 A、SeTox ACL2026 A | **基本具备**：发现/消歧/解码/危害环节不同 | 需要写明真实时间外新义与词典内留出不同；中文/跨语种前沿点到即可 |
| 隐含伤害的语境与标注分歧 | P001 ACL2022 A、B2b ACL2025/26 A；R2A-013 AUTALIC ACL2025 A（未精读），R2A-014 Graphically Speaking ACL2025 A（未精读） | **结构性薄弱**：B2b多为隐喻测量、合成攻击和新词分类；真实对话语境下“引用/反用/受害者语境”证据仍不足 | **优先补读AUTALIC（1篇）**，必要时读Graphically Speaking；为T3→T4衔接和标注分歧提供直接证据 |
| 多模态修辞/多任务 | P003 ACL2025 A、P019 NAACL2025 B、P035 ACL2025 A、M3UCD AAAI2026 A、MGMCF AAAI2025 A、DOSE ACL2026 A | **核心足够**，但有输入特权/多任务等预算/源域漏检疑点 | 基于现有卡写主线；不要因为分类高分就断言源目标正确 |
| 跨模态修辞捷径/音视频关系 | R2A-024 MCIB AAAI2026 A（未精读）；R2A-020 MMSD3.0 CVPR2026 A（未精读）；P025 EMNLP2025 B、P028视频工作 | **证据深度不足**：已列候选，未充分综合音频、视频、时间与捷径抑制方法 | **优先补读MCIB（1篇）**，有篇幅再对MMSD3.0/P025作摘要级核对；不必全面精读音视频系列 |
| 联合模态风险与安全响应 | P034/P037 ACL A、P038 ICLR A、P040 ICML A，R2A-027/028 ICLR A、029 ACL A；P039 ACM MM A刊会待正式出版核 | **高度覆盖**：有输入风险、视觉泄漏、误拒、输出安全和风险归因 | 主要是证据质量、评测协议和模型版本辨析，不再加大量普通Guard论文 |
| 经典Hateful Meme技术谱系 | P026/P027、T001–T004/T014–T016；R2A-025 RGCL、026 UMR均ACL2024 A | **已有足够关联材料** | 作为表征/检索/融合方法背景，禁止挤占语用/隐含意义主章节 |

**没有证据显示当前综述“缺少一个完全未入账、非加入不可的新CCF-A研究脉络”。** 少量补读重点是**已入账但机制核验不足**，不新启动检索池。AUTALIC和MCIB的官方元数据及摘要已有外部定向核对：
- [AUTALIC](https://aclanthology.org/2025.acl-long.1022/)：ACL 2025 Main（CCF-A），2,400条来自Reddit的句子及上下文，训练有相关背景的专家标注且公开individual annotations；**本次仅官方摘要核验，未全文审读**。
- [Conditional Information Bottleneck for Multimodal Fusion](https://ojs.aaai.org/index.php/AAAI/article/view/39874)：AAAI 2026 Technical Track（CCF-A），针对反讽的角色、笑声等捷径设计MUStARD++R与MCIB；**本次仅官方摘要核验，未审核源码与实验主表**。这意味着不能将“研究多模态捷径”描述为无人做过的新点。
- P039 ThinkingGuard：目前所见作者仓库给出ACM MM 2026录用/DOI，[作者代码](https://github.com/FroggyChen/ThinkingGuard)，**尚未获得独立的正式ACM出版页/具体Track核验**；截至2026-11-08亦不宜把11月10–14日会议视为已举办完毕。综述写“已录用/DOI已见，正式发表待核”，勿计入严格正式主会数。

## 3. Ground Truth、捷径、信息泄漏与指标可比性清单

> 证据级别：**P**=正式论文作者报告；**S**=前序读卡的代码/数据静态核验；**H**=研究者合理风险假设；**O**=尚无直接确认。P/S不自动等于GPU复现或公开数据完整。

| 编号与实验对象 | P或S支持的事实 | H/O：限制和最低关闭动作 | 优先级 |
|---|---|---|---|
| R2A-001 DRInQ | P: 819验证/400困难集；S: 公开CSV 231、148不同Q | O: 找全公开文件和题型/问句分组；MCQ排序捷径 | 高（若引用完整数据） |
| R2A-002 VAGUE | P: V2.0 1677图文意图候选；S: 数据页有direct/solution等字段 | O: 保证评测不把答案字段送入Prompt；原图来源ID分组 | 中 |
| R2A-006 Silent Signals | P: 主集16,550；S: HF元数据16,258、小检测集101 vs原100 | H: 自动筛选伪标签不能充当所有样本逐条人审真值；需确定版本 | 高 |
| R2A-007 FETCH! | P: 已知词典词项20/80留出；S: 原始平台语料难整包取得 | H: 词典之外真新词缺金标；不能把type回收率当新义使用F1 | 高 |
| R2A-008 FA-Net | P: 固定候选目标词与无标签目标域适应 | H: HC相似度伪正对可能错配；无实际错配率 | 中 |
| R2A-010 SeTox | P: 新词毒性/检索增强及安全标签；S: 有作者JSON/检查脚本/权重入口 | O: 训练/测试词项交集与搜索循环标签污染；引用以ACL正式书目为准 | 高 |
| R2A-011 When People are Floods | P: 人审隐喻源域，**不是人审非人化/仇恨真值** | 不得用隐喻源域检出率作为隐含仇恨检测能力证据 | **硬约束** |
| R2A-012 Sheep’s Skin | P: 合成隐喻、作者人审与检测/警告下降 | O: 仅正例导致无法估普通误报；多轮改变文本位置与历史 | 高 |
| R2A-017 M3UCD | P: 数据15,345及多任务；S: 作者链接未见可读训练数据文件 | O: 同模型单模态测试、相同预算任务迁移、OCR/元数据、发布split | 高 |
| R2A-018 MGMCF / MET-MEME | S: 公开train/test加载源/目标域特征；Dual-Semantic公式与代码显著不一致 | O: pkl是否gold、论文主表代码版本、同预算去域概念；不可直接宣称已证明泄漏 | **最高** |
| R2A-019 DOSE | P: 参数正交与总体多任务收益；S: 1%训练target MCQ B位置偏多，默认6任务≠主文5项 | O: 完整测试位置/长度捷径、真实梯度冲突、独立解释质量；训练样本与题目实例分母 | 高 |
| R2A-027 MSSBench | P: 1,960正式版、Chat/Embodied；S: IF judge某类无理由不答也算正确 | O: strict same-Q配对、意图与询问一致、judge对图/问句盲点、QC/IC评分脚本闭合 | **最高** |
| R2A-028 MOSSBench | S: 300 JSON，contrast244；P: AMT约9%安全性争议 | O: 逐例投票/图审核，针对两侧数据报漏拒与有用性，ARR不是理解准确率 | **最高** |
| R2A-029 MMSafeAware | P: 1500；S: prompt1523/编号图1453/uniqueBlob445 | O: 原始版可下载性、70缺图、去重/分组bootstrap、首答案解析，且不能将误报当拒答 | **最高** |
| P038 VLSU | P: 8,187三路风险标签、17模式；S: CSV8,159且image_grade另有not_sure | O: 图像外链成功率、组合标签口径、test-only数据不得当训练+验证 | **最高** |
| P039 ThinkingGuard | P: 反事实TriggerBench、步骤奖励和Step-DPO；S: 标签配对目录与权重链接 | O: 完整生成/训练源码、全图逐对审计；正式出版核验 | 高 |
| P040 Meerkat-VL | P: NPSV/DPCA+GRPO、Meerkat-Safe；S: 自评步骤使用含GT风险解释的文字输入而非再次独立看图 | O: 数据版本8466/8436、奖励源码/消融、数据字段可验证性 | 高 |
| P041 SIUO | P: 269论文规模；S: 官仓两个任务JSON各167并复用样本 | O: 102 AI辅助条目发布状态；评测脚本变量/字段静态疑点 | 中 |

### Ground Truth分层规则（应在综述方法学节明示）
1. **人审对象到底是隐喻/编码存在、意义、目标、立场、危害，还是回答行为**；若只有修辞存在GT，不能支撑“非人化/仇恨识别”直接结论。
2. **标注者心理推断≠发言者真实动机**；社会规范安全标签需要政策、场景与合理分歧。对特定同词/语用歧义必须允许多解或标出争议度。
3. **合成器/安全Judge/训练器同源**及提示附带gold意义、图像OCR、源目标域、候选定义、检索与oracle信息均可能造成额外信息优势；**潜在泄漏要标H，实见输入差异标S，只有实物和同协议对照后才能定量归因**。
4. **文本/图像文件复用**：训练/测试交叉需要按同问句、词根/编码义、图片hash、meme模板、对象、来源平台和日期分组；重复不自动是错误，但将同源数据当独立IID有误。
5. **指标永远跟随Ground Truth和分母**：MCQ Accuracy≠自由解释准确率；BERTScore≠隐喻映射忠实性；ROC-AUC源域≠有害判断F1；输入Safe/Unsafe Acc≠输出Safe Rate；MOSS ARR≠MMSafeAware OverSafe Accuracy；不同子集/基线不能跨论文直接排名。

## 4. 高质量综述目前“足够吗”？

分三个层次回答：
- **概念分类与章节设计：足够**。59篇R0+32篇经定向核验的新增候选覆盖语用、修辞、编码、隐晦有害、多模态与响应；16篇新增已详细精读，已有P系列重要方法卡支撑核心技术脉络。
- **正式写作各章引用：基本足够，但存在两个必须守住的薄弱环节**：①真实社会语境有害性与标注分歧（R2A-013 AUTALIC）；②多模态修辞模型捷径抑制已有方法（R2A-024 MCIB）。这两篇**已登记、已确认CCF-A正式出处**，建议在对应章节动笔前做定向精读；不是进入R3画框架的阻断条件。
- **发表级、可称系统综述的文献完备性：尚不能宣称达到**。未做PRISMA/全数据库穷尽搜索、R0多篇只有摘要或未确认出版、R2新增还有16篇未精读、原始PDF/代码/数据版本未全部独立复现。若面向可投稿综述需在R3/R4补检索日志、纳入排除规则、引用Meta-data和版本审计。

现有证据**不能直接推出一个未被研究的CCF-A方法创新Gap**，但已经足以支撑**高质量中文研究型综述的提纲、核心脉络与批判性评述**。

## 5. 阶段关闭条件与R3移交

### R2是否可以正式关闭？
**建议：进入“R2-C已写入审阅分支 / 待PR审阅合并”的阶段性完成状态。** 完成四份文件归档+review/merge后，**R2的文献扩展与机制综合主任务可流程性关闭**。这不是关闭论文级证据债务；B1综合目前文件名仍为DRAFT、R1 taxonomy也是工作版，R3需继续追踪而不可将其默认为已正式冻结。

### 需要修正R1什么？
不覆盖既有文档，而在R3形成新taxonomy：
- 保留T1–T6任务轴，单标签仅用于馆藏盘点；大多数论文实际多任务。
- T3增加会话含意、间接行为与立场/目标子任务；T1区分instance词义判定/type词项发现；T2区分固定集合解码和自由解释。
- T5以“严格组合新增危险”“视觉情境风险变化”“语境解除表面危险”作依赖条件区分；第三者通常属于T4安全负例/误报分析。
- 将T6细分“输入风险识别之后的安全输出行为/有用性”，并严格区分拒答率、危险回答率、真实风险判断准确率。
- 模态、机制、测试时可用的gold/Oracle/检索字段、证据等级为独立轴；情绪/意图不能被当作隐晦有害GT的替身。

### 必须补读哪些文献？
- **R3启动前无新的阻断性必补CCF-A论文**；不建议继续开大规模新论文阅读窗口。
- **建议两篇R3并行定点精读（每篇限定任务、GT、主方法、最关键消融即可）**：
  1. **R2A-013 AUTALIC**（[ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1022/)）：专家多标注的上下文反歧视内容，重点查看上下文是否改变标签、分歧如何处理、如何避免仅敏感话题检测；直接服务“语用→危害”章节。
  2. **R2A-024 Conditional Information Bottleneck for Multimodal Fusion**（[AAAI 2026 Technical，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/39874)）：已有多模态反讽捷径控制、条件瓶颈及MUStARD++R，查方法与消融是否匹配，防止把shortcut审计当成新贡献。
- 仅当正式章节扩展到多图/音视频、对话辱骂时，追加R2A-020 MMSD3.0（CVPR 2026 Main A）、R2A-014 Graphically Speaking（ACL 2025 Main A）、P025 HVGuard（EMNLP 2025 Main B）。这不是立即启动的新批次。
- P039正式ACM出版需在会议/出版社发布时再核，**不能提前写“正式已出版”**。

### 能否进入R3？
**可以。** R3首先做“总综述框架+技术代际+逐章节证据矩阵”，同时只开展两项定向核验。无需为关闭每一个dataset/API/GPU问题而延迟框架设计。

### 移交时必须保留的证据状态
- **直接依据论文（P）**、**源码/数据静态可核（S）**、**研究者解释性推断（H）**、**仍待核（O）**四类标记；
- “未公开/不一致”必须写明检查的仓库版本与范围，避免将**当前公开仓库**的缺失错误地扩展为**论文正式实验**缺失；
- 用户实验约束：单GPU目标16–20GiB、≤6小时、不依赖付费API、不新建大标注；正式综述的学术覆盖可超越资源，但推荐后续实验时必须分别审计数据、代码、成本。

## 6. 可追溯来源

- [R0 Audit](../R0_inventory/R0_Audit_Report.md)、[R0 Literature Gaps](../R0_inventory/Literature_Gaps.md)
- [R1 Taxonomy](../R1_taxonomy/R1_Working_Framework_DRAFT.md)、[R1 Task Mapping](../R1_taxonomy/R1C_Task_Mapping_DRAFT.md)
- [R2-A候选Ledger](../R2_literature_extension/R2A_Candidate_Ledger.md)、[R2-A搜索协议](../R2_literature_extension/R2A_Search_Protocol.md)、[R2-A覆盖](../R2_literature_extension/R2A_Coverage_Audit.md)
- [B1](../R2_literature_extension/B1_reading/R2B_B1_Synthesis_DRAFT.md)、[B2a](../R2_literature_extension/B2a_reading/R2B_B2a_Synthesis.md)、[B2b](../R2_literature_extension/B2b_reading/R2B_B2b_Synthesis.md)
- [B3a](B3a_Cross_Paper_Synthesis.md)、[B4a](B4a_Cross_Paper_Synthesis.md)、[跨领域综合](R2C_Cross_Domain_Synthesis.md)
- [R2资源缺口](../R2_dataset_audit/Resource_Gaps.md)、[代码复现审计](../R2_dataset_audit/Code_Reproducibility_Audit.md)
- 本轮仅对[ACL AUTALIC官方页](https://aclanthology.org/2025.acl-long.1022/)及[AAAI MCIB官方页](https://ojs.aaai.org/index.php/AAAI/article/view/39874)进行额外摘要级核验；不声称完成其全文审稿。
