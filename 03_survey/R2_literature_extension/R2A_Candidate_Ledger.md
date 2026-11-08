# R2-A｜2024–2026 CCF-A候选文献补充索引
日期：2026-11-08。状态：**系统定向检索工作版，非PRISMA穷尽系统综述，待R2-B精读筛选**。

**基准**：R0去重59篇及[R1任务映射](../R1_taxonomy/R1C_Task_Mapping_DRAFT.md)。以下 32 篇的题名不在R0 59篇中，故为新增候选；已在先前聊天口头讨论过不等于入库。编号R2A-xxx是临时编号，**不写入P001–P041/T001–T018正式序列**。

**证据等级**：仅核验官方出版页面元数据、摘要与会议/Track；尚未完成全文精读、数据实物审计和代码复现。CCF统一第七版（2026），将2026版目录评级应用于2024–2026论文；CCF A指刊会分级，不自动代表论文审稿类别。

| 临时编号 | 完整标题 | 年份 | 会场（CCF 2026） | 相关任务 | 关联性质 | 阅读优先级 | 研究要点与边界 | 官方论文页 |
|---|---|---:|---|---|---|---|---|---|
| R2A-001 | DRInQ: Evaluating Conversational Implicature with Controlled Context Variation | 2026 | ACL Main，A | T3/T2 | 核心 | 优先 | 保持问题表面形式，变化上下文评测会话含义与意图理解 | [官方来源](https://aclanthology.org/2026.acl-long.1597/) |
| R2A-002 | VAGUE: Visual Contexts Clarify Ambiguous Expressions | 2025 | ICCV Main，A | T3/T2 | 核心 | 优先 | 1.6K图像-间接表达及候选意图；视觉语境消歧 | [官方来源](https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html) |
| R2A-003 | Can Your Model Tell a Negation from an Implicature? Unravelling Challenges With Intent Encoders | 2024 | ACL Main，A | T3/机制 | 核心 | 优先 | 意图编码器对否定和会话含义的对比式诊断与训练 | [官方来源](https://aclanthology.org/2024.acl-long.33/) |
| R2A-004 | Rhetorical Questions in LLM Representations: A Linear Probing Study | 2026 | ACL Main，A | T1/T3/机制 | 机制 | 补充 | 反问句表示与跨数据集探针差异，不等于实际意图已被完整复原 | [官方来源](https://aclanthology.org/2026.acl-long.5/) |
| R2A-005 | Beyond Detection: Evaluating Fallacy Awareness of LLMs in Interactive Scenarios | 2026 | ACL Main，A | T3/T6-边界 | 关联 | 补充 | 交互语用语境下谬误觉察，不属于一般隐晦检测 | [官方来源](https://aclanthology.org/2026.acl-long.59/) |
| R2A-006 | Silent Signals, Loud Impact: LLMs for Word-Sense Disambiguation of Coded Dog Whistles | 2024 | ACL Main，A | T1/T2-编码 | 核心 | 优先 | 狗哨普通义与编码义消歧；16,550高置信用例 | [官方来源](https://aclanthology.org/2024.acl-long.675/) |
| R2A-007 | Making FETCH! Happen: Finding Emergent Dog Whistles Through Common Habitats | 2025 | ACL Main，A | T1-新编码发现 | 核心 | 优先 | 新兴Dog Whistle发现，EarShot检索与LLM基线 | [官方来源](https://aclanthology.org/2025.acl-long.284/) |
| R2A-008 | Uncovering and Mitigating the Hidden Chasm: A Study on the Text-Text Domain Gap in Euphemism Identification | 2024 | AAAI Main，A | T2-委婉语解码 | 核心 | 优先 | 委婉语到目标词映射及训练/测试语域差距 | [官方来源](https://ojs.aaai.org/index.php/AAAI/article/view/29786) |
| R2A-009 | SenseRel: A Sense-Level Benchmark for Denotational and Connotational Meaning Relations | 2026 | ACL Main，A | T2-语义变化 | 机制 | 补充 | 词义层面概念变化、隐喻映射、情感效价与唤醒 | [官方来源](https://aclanthology.org/2026.acl-long.20/) |
| R2A-010 | New Terms, New Toxicity: Consensus-based Chinese Neologism Toxicity Detection via Search-Augmented LLMs | 2026 | ACL Main，A | T4-动态编码 | 核心 | 优先 | 语义演变下新词隐含毒性；SeTox检索增强 | [官方来源](https://aclanthology.org/2026.acl-long.1602/) |
| R2A-011 | When People are Floods: Analyzing Dehumanizing Metaphors in Immigration Discourse with Large Language Models | 2025 | ACL Main，A | T1/T4-隐喻贬损 | 核心 | 优先 | 移民话语的非人化隐喻分析；非普通安全分类器 | [官方来源](https://aclanthology.org/2025.acl-long.398/) |
| R2A-012 | Sheep’s Skin, Wolf’s Deeds: Are LLMs Ready for Metaphorical Implicit Hate Speech? | 2025 | ACL Main，A | X3/T4诊断 | 核心 | 优先 | 隐喻隐式仇恨生成与检测/防护失败诊断；主要是攻击与评测 | [官方来源](https://aclanthology.org/2025.acl-long.814/) |
| R2A-013 | AUTALIC: A Dataset for Anti-AUTistic Ableist Language In Context | 2025 | ACL Main，A | T4-语境偏见 | 核心 | 优先 | 专家标注的语境依赖反自闭症歧视；含标注分歧 | [官方来源](https://aclanthology.org/2025.acl-long.1022/) |
| R2A-014 | Graphically Speaking: Unmasking Abuse in Social Media with Conversation Insights | 2025 | ACL Main，A | T4-对话语境 | 核心 | 补充 | 对话回复图结构与上下文中辱骂检测；并非全为隐含内容 | [官方来源](https://aclanthology.org/2025.acl-long.894/) |
| R2A-015 | Confident, Calibrated, or Complicit: Safety Alignment and Ideological Bias in LLM Hate Speech Detection | 2026 | ACL Main，A | T4-可靠性 | 核心 | 补充 | 显式/隐式仇恨检测、校准、角色/意识形态干扰与公平 | [官方来源](https://aclanthology.org/2026.acl-long.1594/) |
| R2A-016 | Class Distillation with Mahalanobis Contrast: An Efficient Training Paradigm for Pragmatic Language Understanding Tasks | 2025 | ACL Main，A | T1/T4-迁移方法 | 方法 | 优先 | 性别歧视/隐喻/反讽的跨任务类别蒸馏；并非统一语义解码 | [官方来源](https://aclanthology.org/2025.acl-long.1424/) |
| R2A-017 | M3UCD: A Multi-task Multimodal Metaphor Understanding Challenge Dataset for LLMs | 2026 | AAAI Main，A | T1/T2-多模态修辞 | 核心 | 优先 | 15,345样本，12类人工标注属性的多任务多模态隐喻基准 | [官方来源](https://ojs.aaai.org/index.php/AAAI/article/view/40808) |
| R2A-018 | Multi-Granular Multimodal Clue Fusion for Meme Understanding | 2025 | AAAI Main，A | T1/T3/T4-多任务 | 核心 | 优先 | MET-MEME：隐喻、情绪、意图、冒犯四任务联合；MGMCF | [官方来源](https://ojs.aaai.org/index.php/AAAI/article/view/34801) |
| R2A-019 | Two Streams, One Sarcasm: Orthogonal Expert Tuning for Holistic Multimodal Sarcasm Understanding | 2026 | ACL Main，A | T1/T2/T3-多模态修辞 | 核心 | 优先 | DocMSU-PLUS多任务与DOSE双流专家，需核实真实分项指标 | [官方来源](https://aclanthology.org/2026.acl-long.319/) |
| R2A-020 | MMSD3.0: A Multi-Image Benchmark for Real-World Multimodal Sarcasm Detection | 2026 | CVPR Main，A | T1-多图反讽 | 核心 | 补充 | 多张图片及图文关系引发讽刺；CIRM跨图推理 | [官方来源](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_MMSD3.0_A_Multi-Image_Benchmark_for_Real-World_Multimodal_Sarcasm_Detection_CVPR_2026_paper.html) |
| R2A-021 | CofiPara: A Coarse-to-fine Paradigm for Multimodal Sarcasm Target Identification with Large Multimodal Models | 2024 | ACL Main，A | T1/T3-反讽目标 | 核心 | 补充 | 检测后的反讽目标定位，理解与识别分开 | [官方来源](https://aclanthology.org/2024.acl-long.522/) |
| R2A-022 | Incongruity-aware Tension Field Network for Multi-modal Sarcasm Detection | 2025 | ACL Main，A | T1-反讽 | 核心 | 补充 | 图文事实/情感不一致建模，ITFNet | [官方来源](https://aclanthology.org/2025.acl-long.705/) |
| R2A-023 | RAM-SD: Retrieval-Augmented Multi-agent framework for Sarcasm Detection | 2026 | ACL Main，A | T1-反讽 | 核心 | 补充 | 检索、类型规划、多agent分类与解释，未证明解释忠实 | [官方来源](https://aclanthology.org/2026.acl-long.64/) |
| R2A-024 | Conditional Information Bottleneck for Multimodal Fusion: Overcoming Shortcut Learning in Sarcasm Detection | 2026 | AAAI Main，A | T1-捷径/可靠性 | 核心 | 补充 | 多模态反讽的捷径消除与条件信息瓶颈；AAAI Technical Track | [官方来源](https://ojs.aaai.org/index.php/AAAI/article/view/39874) |
| R2A-025 | Improving Hateful Meme Detection through Retrieval-Guided Contrastive Learning | 2024 | ACL Main，A | T4-多模态方法 | 方法 | 补充 | RGCL，RA-HMD及ExPO-HM前置研究；普通Meme不自动等于联合隐含风险 | [官方来源](https://aclanthology.org/2024.acl-long.291/) |
| R2A-026 | Uncertainty-Guided Modal Rebalance for Hateful Memes Detection | 2024 | ACL Main，A | T4-多模态方法 | 方法 | 补充 | UMR，模态不确定性与单/跨模态权重平衡 | [官方来源](https://aclanthology.org/2024.acl-long.239/) |
| R2A-027 | Multimodal Situational Safety | 2025 | ICLR Main，A | T5/T6-情境风险 | 核心 | 优先 | MSSBench 1,960图文对，同查询不同视觉情境风险差异 | [官方来源](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html) |
| R2A-028 | Is Your Multimodal Language Model Oversensitive to Safe Queries? | 2025 | ICLR Main，A | T5/T6-过度拒绝 | 核心 | 优先 | MOSSBench 300安全输入，视觉线索触发无谓拒答；负例很重要 | [官方来源](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html) |
| R2A-029 | Can’t See the Forest for the Trees: Benchmarking Multimodal Safety Awareness for Multimodal LLMs | 2025 | ACL Main，A | T5-风险意识 | 核心 | 补充 | MMSafeAware 1,500图文对，危险与过度敏感并评 | [官方来源](https://aclanthology.org/2025.acl-long.832/) |
| R2A-030 | Teach to Reason Safely: Policy-Guided Safety Tuning for MLRMs | 2026 | ICLR Main，A | T6-安全对齐 | 关联 | 补充 | 视觉注意力漂移与安全推理退化；PST对齐，不是独立分类器 | [官方来源](https://proceedings.iclr.cc/paper_files/paper/2026/hash/8ece25974724edad00c8d0bcc8a235e8-Abstract-Conference.html) |
| R2A-031 | Visual Intention Grounding for Egocentric Assistants | 2025 | ICCV Main，A | T3-视觉意图拓展 | 关联 | 补充 | 隐含意图到视觉对象定位；任务范围不同于有害检测 | [官方来源](https://openaccess.thecvf.com/content/ICCV2025/html/Sun_Visual_Intention_Grounding_for_Egocentric_Assistants_ICCV_2025_paper.html) |
| R2A-032 | HumorDB: Can AI understand graphical humor? | 2025 | ICCV Main，A | T1/T2-纯视觉幽默 | 关联 | 补充 | 纯视觉幽默及最小反事实对，非图文隐含有害判断 | [官方来源](https://openaccess.thecvf.com/content/ICCV2025/html/Jain_HumorDB_Can_AI_understand_graphical_humor_ICCV_2025_paper.html) |

> 字段解释：**优先**=先读；**补充**=次批；**核心**、**方法**、**机制**、**关联**代表内容与综述的直接程度，不是论文质量评级。

## 排除/单列的高相关非主会A论文
- [PUB: A Pragmatics Understanding Benchmark](https://aclanthology.org/2024.findings-acl.719/)，ACL 2024 **Findings**；语用14任务和28k样本，强关联但不能称ACL Main A。
- [MTMCS-Bench](https://aclanthology.org/2026.findings-acl.96/)，ACL 2026 **Findings**；图文多轮安全含义很相关，不能称ACL Main A。
- [Small Cues, Big Consequences (MemeCF)](https://aclanthology.org/2026.findings-emnlp.1329/)，EMNLP 2026 **Findings**；证据归因相关但不是ACL A。
- [I Came, I Saw, I Explained](https://aclanthology.org/2026.lrec-1.743/)，LREC 2026；多模态修辞解释忠实性，非CCF-A。
- [Can Thinking Models Think to Detect Hateful Memes?](https://doi.org/10.1145/3774905.3795465)，WWW 2026 **Companion**，不能写成WWW Main A。
- [Improving multimodal hateful meme detection exploiting LMM-generated knowledge](https://openaccess.thecvf.com/content/CVPR2025W/MULA2025/html/Tzelepi_Improving_multimodal_hateful_meme_detection_exploiting_LMM-generated_knowledge_CVPRW_2025_paper.html)，CVPR 2025 **Workshop**。
- [SafeLens](https://ojs.aaai.org/index.php/AAAI/article/view/42390)，AAAI 2026 **Demonstration**；不属于Technical Track。

## 审计边界
- 这32篇是**本轮已查到且有官方主会出版页的候选**，不是整个领域仅有32篇，也不代表每篇都应放入正文核心。
- 首轮以题名及摘要判断“主任务”，不能证明方法优劣、数据完全可下载、评价协议可靠或代码可复现。
- 原R0 59篇保留不改。后续经R2-B筛选后再合并进统一总索引，正式分配编号。
