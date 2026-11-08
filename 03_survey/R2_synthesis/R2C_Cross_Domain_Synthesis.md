# R2-C｜广义隐晦信息研究：跨领域机制与证据综合

> 日期：2026-11-08｜状态：**R2-C综述研究骨架（待用户学术审阅）**。依据R0 59篇、R1工作分类、R2-A新候选32篇、R2-B 16篇正式精读及既有P系列核心卡。**未完成91篇逐篇精读或系统综述式全量检索**；原论文结果与本项目静态审计严格区分。保留P001–P041/T001–T018/R2A-001–032原编号。

## 0. 最重要的总论

广义隐晦信息研究不应写成“从简单仇恨识别到高级隐式仇恨”的单线历史，而应以**交际意义如何依赖语境、修辞、社会约定与模态组合而改变**为核心问题；在此基础上区分**表达识别、意义恢复、交际功能推断、风险判断及安全响应**。

至少有五个概念不可互换：
1. **Implicit Meaning（隐含意义）**是意义需要超出直接字面断言推断的属性；不必有有害性，也不必有故意隐瞒。
2. **Figurative（修辞）**是隐喻、反讽、夸张、习语、委婉等现象群；形式被识别不等于具体意义或评价立场已正确解释。
3. **Coded / Dog Whistle（编码/狗哨）**涉及社群知识、词义重映射或对不同受众的意义分层；词项存在不意味着该次出现使用编码义，编码义不必有害。
4. **Subtle / Obfuscated（低显著性/伪装）**分别描述线索显著程度或形式扰动，既不是Implicit的同义词，也不能自动证明说话者有规避意图。
5. **Harmful（有害）**是依照目标、场景、规范与标签政策的评价属性；同一隐含意义可能无害，同一显式字面信息也可能有害。

**研究者分析链（非被论文共同验证的认知流水线）**：
表达形态/片段（T1） → 候选含义和非字面解释（T2） → 话语/交际功能与立场（T3） → 语境下危害标签（T4；T5为某些跨模态联合条件） → 模型输出的安全与有用性（T6）。
任何相邻箭头都需要**独立监督、对照实验与中间变量测量**，不能靠一个最终二分类Acc证明整条链。

## 1. 六条主要研究脉络（“机制轴”与“任务轴”分开）

| 脉络 | 代表论文及正式出处/等级 | 已经研究/解决到什么程度 | 主要未证或局限 |
|---|---|---|---|
| **A. 会话含义与间接意图** | P011[语用综述](https://aclanthology.org/2025.acl-long.425/) ACL2025 Main **A**；P020[(RSA)²](https://aclanthology.org/2025.acl-long.1019/) ACL2025 Main **A**；R2A-001 [DRInQ](https://aclanthology.org/2026.acl-long.1597/) ACL2026 Main **A**；R2A-002 [VAGUE](https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html) ICCV2025 Main **A**；R2A-003 [Negation vs Implicature](https://aclanthology.org/2024.acl-long.33/) ACL2024 Main **A**；R2A-004 [Rhetorical Questions](https://aclanthology.org/2026.acl-long.5/) ACL2026 Main **A** | 从理论RSA与语境假设，发展为固定问句换语境的含义选择、视觉情境下间接动作选择、否定/含意表示与隐藏状态探针 | 多选/探针结果不等于开放意义恢复；GT为人工或合成语境下**可接受解释**，非真实发言者心理可观测意图 |
| **B. 修辞表达与意义映射** | P003 [MultiMM](https://aclanthology.org/2025.acl-long.1275/) ACL2025 Main **A**；P019 [V-FLUTE](https://aclanthology.org/2025.naacl-long.1/) NAACL2025 Main **B**；P035 EmoBi ACL2025 Main **A**；R2A-017 M3UCD AAAI2026 Main **A**、R2A-018 MGMCF AAAI2025 Main **A**、R2A-019 DOSE ACL2026 Main **A** | 从修辞识别向源/目标概念、蕴含、情绪、意图、对象定位、解释MCQ和多任务模型扩展 | 情绪辅助信息可能是测试时gold；OCR/域概念输入不对齐；多任务增益未控制数据预算；解释指标与语义忠实性有距离 |
| **C. 编码语言、狗哨、新兴词义** | P023 [CodedLang](https://aclanthology.org/2026.acl-long.426/) ACL2026 Main **A**；R2A-006 [Silent Signals](https://aclanthology.org/2024.acl-long.675/) ACL2024 Main **A**；R2A-007 [FETCH!](https://aclanthology.org/2025.acl-long.284/) ACL2025 Main **A**；R2A-008 [Hidden Chasm/FA-Net](https://ojs.aaai.org/index.php/AAAI/article/view/29786) AAAI2024 Main **A**；R2A-010 [SeTox](https://aclanthology.org/2026.acl-long.1602/) ACL2026 Main **A** | 已区分编码存在、已知编码义消歧、词项级发现、固定目标类别解码、新词语境检索辅助毒性分类 | “未知”多是词典留出或基座模型未知，非严格时间新义；词典/自动标签不是逐例人审金标；解码与危害监督通常未同时独立提供 |
| **D. 修辞—立场—有害性边界** | P001 [ToxiGen](https://aclanthology.org/2022.acl-long.234/) ACL2022 Main **A**；R2A-011 [When People are Floods](https://aclanthology.org/2025.acl-long.398/) ACL2025 Main **A**；R2A-012 [Sheep’s Skin, Wolf’s Deeds](https://aclanthology.org/2025.acl-long.814/) ACL2025 Main **A**；P029 RV-HATE、P030 SMARTER、P032 ImpCon（正式刊会与评测边界另见P卡）；R2A-013 [AUTALIC](https://aclanthology.org/2025.acl-long.1022/) ACL2025 Main **A**（候选，未精读） | 从隐含/合成有害基准与分类监督，进入隐喻型非人化测量、隐喻改写后的风险漏检、搜索辅助的新词毒性与语境歧视标签 | **源域隐喻金标≠非人化/仇恨金标**；合成攻击成功≠真实话语普遍失效；缺独立意义/立场/有害多层真值和安全负例；模型漏检归因仍有多解 |
| **E. 多模态关系、视觉语境与联合风险** | P034 [CrossGuard](https://aclanthology.org/2026.acl-long.1178/) ACL2026 Main **A**；P037 [VLSBench](https://aclanthology.org/2025.acl-long.405/) ACL2025 Main **A**；P038 [VLSU](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html) ICLR2026 Main **A**；R2A-027 MSSBench ICLR2025 Main **A**；R2A-029 MMSafeAware ACL2025 Main **A**；P039 ThinkingGuard ACM MM2026 **A刊会，出版待核** | 从普通多模态Meme/语义判别发展到文本视觉信息泄漏、三条件风险标签、情境风险、反事实Trigger定位与Guard优化 | 图文并列输入≠双模态必需；是否为joint-only harm取决于严格样本级GT；合成反事实不一定只改变一个语义因素，因果归因难 |
| **F. 安全行为及误拒权衡（相邻延伸）** | P041 [SIUO](https://aclanthology.org/2025.findings-naacl.198/) NAACL2025 **Findings（非主会A）**；R2A-028 [MOSSBench](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html) ICLR2025 Main **A**；P040 [Meerkat-VL](https://proceedings.mlr.press/v306/zhou26ae.html) ICML2026 Main **A** | 从危险响应行为、正常误拒与安全帮助冲突，走向风险感知/自验证/偏好与RL后训练 | Safe response/拒答率与输入风险GT不等价；解释自验证未必重新读图；奖励和评价judge可能引入特权信息；不应扩成泛安全对齐综述 |

注：表中 R2A-017/018/019、027/028/029 的正式出处与任务细节见对应B3a/B4a综合；P系列出处以各自卡片为准。**同列不构成可比benchmark。** CCF按2026年第七版“刊会等级”口径，Findings及正式出版状态额外注明。

## 2. 技术演变：不是“PLM被LLM完全替代”的单线

| 时段/技术层 | 典型做法及代表 | 贡献与未完全解决的边界 |
|---|---|---|
| **早期规则、语义与概率语用** | 词典/规则、候选释义、RSA 的 L0→S1→L1；P020在此基础上引入修辞策略相容函数 | 用透明结构表述“说话者怎样选择表达、听者怎样推断”；依赖候选意义、规则、策略/先验，人为设定可能很强 |
| **监督NLP/PLM阶段** | 词向量、BERT/MBERT/ViT编码、跨模态注意力、对比学习/域适应，典型FA-Net、MGMCF、MultiMM | 可针对特定基准训练表征与分类器；已遇到域/平台/词义变化、额外输入特权、融合与捷径风险 |
| **LLM作为语境推断与开放解释器** | P020 RSA与LLM结合、DRInQ/VAGUE候选解释、Silent Signals提示、FETCH!检索、SeTox搜索增强调用、P030解释学习 | 变强的是生成/检索与柔性推断；答案选择依赖prompt/定义/工具证据，解释文本未必真实支撑结论 |
| **VLM/MLLM多任务和机制优化** | M3UCD统一LoRA、DOSE专家路由、图文/多图隐喻反讽、P034判别器、P039分步归因 | 有更细粒度任务和多模态基准；不可把模型准确率直接解释为“感知了必要的图像证据” |
| **安全对齐/响应后训练** | P037多模态SFT/DPO基线、P039 Step-DPO、P040 GRPO、自验证与代理推理 | 开始优化安全/有帮助回答，但评价中风险感知、响应模板、奖励优化与过度拒答纠缠；不能直接和输入分类共用指标 |

**核心变化是评价粒度扩张**：现象标签 → 语义与意图 → 语境/模态必要性 → 风险归因 → 安全输出；而不是“新模型在旧数据F1更高所以真正理解了隐晦含义”。

## 3. R2-B 16篇核心论文的证据状态索引（原始编号不改）

| 批次 | 原编号与论文 | 主问题/分类 | 主要可用证据与最关键未关闭项 |
|---|---|---|---|
| B1 | R2A-001 DRInQ (ACL2026 A) | T3会话含义选择 | 固定Q换C的人类共识选择；公开231≠论文819，困难子集不完整 |
| B1 | R2A-002 VAGUE (ICCV2025 A) | T3视觉语境意图 | 视觉语境四选一；构造目标/额外字段与原图分组待审 |
| B1 | R2A-003 Negation vs Implicature (ACL2024 A) | X2语义/意图表征 | 对比句编码/训练诊断；式与代码入口、构造标签核验未闭合 |
| B1 | R2A-004 Rhetorical Questions (ACL2026 A) | T1/X2反问探针 | 探针AUROC与方向诊断；非开放意图解释，PCA协议待审 |
| B2a | R2A-006 Silent Signals (ACL2024 A) | T1a实例编码义消歧 | 定义已给定；自动主集及小人审评测，16,550/16,258版本差 |
| B2a | R2A-007 FETCH! (ACL2025 A) | T1b词项发现 | 20/80已知词典词项留出；GT不是词典外真实发现，原始语料不足 |
| B2a | R2A-008 Hidden Chasm/FA-Net (AAAI2024 A) | T2a固定候选解码 | source有监督/target适应；相似度伪正对可能错配，暂无错配实测 |
| B2b | R2A-010 SeTox (ACL2026 A) | T4新词毒性 | 搜索增强已有人工安全标签；词项重叠与检索证据可靠性待审 |
| B2b | R2A-011 When People are Floods (ACL2025 A) | T1隐喻源域测量 | 人评隐喻源域；**无独立非人化/仇恨GT** |
| B2b | R2A-012 Sheep’s Skin, Wolf’s Deeds (ACL2025 A) | X3/T4/T6隐喻风险评测 | 人审合成仇恨改写及漏检；检测/响应、提示与多轮长度混杂 |
| B3a | R2A-017 M3UCD (AAAI2026 A) | T1/T2多任务隐喻 | 15,345人工属性；公开数据未见，辅助标签/互补标签真实性待审 |
| B3a | R2A-018 MGMCF (AAAI2025 A) | T1/T3/T4多任务Meme | 分类消融；源/目标域测试输入及损失源码与论文不一致 |
| B3a | R2A-019 DOSE (ACL2026 A) | T1/T2/T3反讽MCQ | 正交LoRA/整体改善；1%训练MCQ选项偏差、5/6任务分歧 |
| B4a | R2A-027 MSSBench (ICLR2025 A) | T5关联/T6情境风险回应 | 同Q Chat配对；IF Judge把无理由拒答/能力不足不答计为正确 |
| B4a | R2A-028 MOSSBench (ICLR2025 A) | T6误拒 | 300安全请求+244危险对照；9%安全判断争议及对照不全 |
| B4a | R2A-029 MMSafeAware (ACL2025 A) | T5联合风险分类 | 1,000/500双侧分类；公开prompt与图不匹配、445图重复 |

**出版等级**均为2026年第七版CCF对应刊会等级，且以上16篇均在R2-A中登记为正式 Main/Technical。阅读卡“定稿”表示方法与证据可供综述引用，但**不表示代码可复现或开放问题解决**。此表仅列最重要未闭合项，详细来源追溯到相应精读卡。

## 4. 已有方法“解决”与“没有证明”的边界

### 4.1 强支持（针对作者的任务）
- 语境变化、视觉线索和编码先验会改变固定选择/分类表现；DRInQ、VAGUE、Silent Signals、FETCH!等提供可操作任务，但金标层次不一。
- 任务扩展不局限存在性：P019 修辞视觉蕴含+解释、M3UCD多属性、DOSE多任务MCQ提供评价结构。
- 安全判断不止有害正例：MOSSBench和MMSafeAware显示**安全侧误拒/误报同样重要**；P038以三条件标签更系统展示组合风险模式。
- 通过静态源码/发布数据可发现影响复现的具体版本及协议不一致（见B3a/B4a/资源审计）。

### 4.2 仅为提示或间接证据
- “模型会因隐晦意义未恢复而漏检”：终端T4错误不能单独定位T2。
- “情绪知识促进概念映射”：多任务/情感输入消融尚欠等预算、非gold输入。
- “消掉图像后预测变差所以理解了跨模态关系”：去模态是必要诊断但不构成完整机制证明。
- “解释越详细越忠实”：解释是监督或生成物，尚非内部因果忠实性指标。
- “PPO/DPO/GRPO特定模块独立导致提升”：须结合相同基座与训练数据/预算、公平消融、代码版本和下游正负两侧指标。

### 4.3 真正尚未解决的问题（限定为**本综述证据尚未闭合**，不是声称全球学术空白）
1. **中间语义与最终标签的可辨识归因**：缺跨T2/T3/T4独立金标、模型中间输出与对照干预共享的可比协议。
2. **开放世界编码词项与语境义**：词典外/时间外/社区外的真实新义和多受众使用机制，公开可下载、逐例可靠标签稀缺。
3. **跨模态语义因果依赖**：静态捷径与真互补的区分需要人工证据、固定同模态干预、来源/图片分组和风险翻转。
4. **双侧风险与安全有用输出的联合评估**：危险侧漏检、正常误报、模型拒答/警告/危险回答之间缺统一且不投机的Judge和独立参考。
5. **复现与数据漂移**：论文规模/发布文件/GT不一致、外链素材及闭源服务限制、训练/测试特权字段使用。

这些是**可检验的审计议程**。要宣称CCF-A novel research gap，仍须定向查重+可执行Kill Test，不能凭综述文字直接成立。

## 5. R1 Taxonomy 建议修订（只提出，不覆写原稿）

**保留 T1–T6 为任务轴、X1–X4 为研究活动轴**，但增加如下非互斥维度：

1. **表达机制 A（非任务类别）**：会话含意/言语行为、修辞、狗哨与编码、词形伪装/谐音、文化与社区知识、跨模态语义组合。由哪种机制触发需单独证据，不能给每篇普通有害Meme随意贴“隐晦”。
2. **任务细分 B**：T1a已知编码义的语境使用判定 / T1b新词项发现；T2a固定候选解码 / T2b开放释义与源—目标域；T3a含义/间接行动 / T3b立场、修辞目标与交际功能；T4a风险类别/目标 / T4b情境有害性与规范性判断；T6a回应安全 / T6b拒答与有用性。
3. **条件轴 C**：文本/图文/多图/音频/视频/会话时序，以及依赖类型：单模态足够、单模态互补、语境解除危害、组合新增风险。**T5是T4的特例**而非所有图文研究的自动上级类别。
4. **监督与信息预算 D**：原始输入、OCR、给定词典定义、gold情绪/域/意图、模型预测中间量、Oracle caption、检索证据；标明测试时哪些字段可用。
5. **评价轴 E**：单标签分类、候选选择、开放意义解释、人类合理性、解释忠实性、跨模态反事实、危害规范判断、输出安全/有用性。记录标注单元和指标分母。

**不建议**将“情绪”升为与T1–T6并列的一级隐晦信息类别；其可为内容属性/辅助变量，也可构成单独情感任务，但不是隐晦性必要条件。**不建议**新增独立“多模态语境安全=第七任务”，因为输入风险和输出安全已可在T4/T5/T6加条件轴表达。

## 6. 用于R3的“发展脉络”写作结构（初步）

- **前置定义**：隐晦信息工作定义，implicit / figurative / coded / subtle / harmful / context-dependent 多轴交叉及研究纳入标准；
- **理论与语用意义**：RSA与会话含义→可操作的意图/情境评测；
- **文本非字面与编码**：修辞检测→释义与意义指派；编码发现→语境消歧→新词检索；
- **从意义到有害性**：隐式仇恨、非人化/委婉、语用立场/目标/规范性判断、人工分歧；
- **多模态理解**：隐喻/反讽/视觉蕴含→多任务/多图→模态依赖与捷径；
- **多模态风险与安全回应（限定篇幅）**：输入Guard、联合风险、视觉泄漏、情境安全、误报/误拒、回应策略；
- **方法谱系横向综合**：规则/RSA、PLM对比/迁移、LLM prompt/RAG、LoRA/MoE、偏好/RL；不把不同任务下模型分数进行SOTA总排名；
- **统一评测与开放问题**：GT可信度、语义/风险双层标签、训练测试信息预算、因果干预、双侧错误、数据可达性。

下一步可以启动**R3综述框架与技术发展脉络设计**；正式撰写各节前需用[覆盖审计](R2C_Coverage_and_Evidence_Audit.md)标注必须定向核验/补读项，而非重新精读全部候选。

## 7. 来源索引

- [R0 59篇核对报告](../R0_inventory/R0_Audit_Report.md)、[R0分类](../R0_inventory/Research_Taxonomy.md)
- [R1工作框架](../R1_taxonomy/R1_Working_Framework_DRAFT.md)、[R1 59篇映射](../R1_taxonomy/R1C_Task_Mapping_DRAFT.md)
- [R2-A 32篇候选](../R2_literature_extension/R2A_Candidate_Ledger.md)、[R2-A覆盖](../R2_literature_extension/R2A_Coverage_Audit.md)
- [B1综合](../R2_literature_extension/B1_reading/R2B_B1_Synthesis_DRAFT.md)、[B2a综合](../R2_literature_extension/B2a_reading/R2B_B2a_Synthesis.md)、[B2b综合](../R2_literature_extension/B2b_reading/R2B_B2b_Synthesis.md)
- [B3a综合](B3a_Cross_Paper_Synthesis.md)、[B4a综合](B4a_Cross_Paper_Synthesis.md)
- [R2数据可达性](../R2_dataset_audit/Resource_Gaps.md)、[R2代码审计](../R2_dataset_audit/Code_Reproducibility_Audit.md)
