# R2-B / B2a-01｜Silent Signals, Loud Impact — 定稿阅读卡

> **状态：2026-11-08 用户确认定稿；开放问题保留，未作独立复现；不修改 P/T 编号或已有精读卡。**  
> **临时编号：R2A-006。研究范围：广义隐晦信息下的 Dog Whistle、已知编码词义消歧（T1 主、T2 次；T3 为边界关联）。**  
> **核验时间：2026-11-08。证据层级：①ACL正式PDF；②作者公开 Hugging Face 数据页面/README；③本项目研究者审计推断。未运行代码或模型复现。**

## 1. 基本信息与核心结论
- Julia Kruk, Michela Marchini, Rijul Magu, Caleb Ziems, David Muchlinski, Diyi Yang. **Silent Signals, Loud Impact: LLMs for Word-Sense Disambiguation of Coded Dog Whistles**. ACL 2024 Main Conference (Long Papers)，CCF-A；页码12493–12509，DOI 10.18653/v1/2024.acl-long.675。
- [正式论文页](https://aclanthology.org/2024.acl-long.675/) · [官方PDF](https://aclanthology.org/2024.acl-long.675.pdf) · [主数据集](https://huggingface.co/datasets/SALT-NLP/silent_signals) · [检测评测集](https://huggingface.co/datasets/SALT-NLP/silent_signals_detection) · [消歧评测集](https://huggingface.co/datasets/SALT-NLP/silent_signals_disambiguation)。
- **一句话**：针对已知 Dog Whistle 词项和已知编码义，判断特定文本使用的是编码义还是普通义；用提示式 LLM + 重复一致性筛选，从词典命中的海量候选中抽取高置信正例。该文不是未知暗语自动发现，也不是训练了新的深度学习架构。
- 文中以 *soy* 为例：普通“豆制品”义与特定群体的贬损编码义可在不同语境中共存（Fig.1）。Dog Whistle 核心在不同受众对同一表达的差异性解释，不可把 Coded、Dog Whistle、有害性及说话者真实意图互相等同。

## 2. 研究问题、任务输入输出与理论边界（§1–§4）
**任务A：Automatic Dog Whistle Resolution/Detection** (§4.1)：
- 输入：句子 x，Dog Whistle 定义；Zero-/Few-shot 提示。
- 输出分级：(i) Presence 是否存在；(ii) Identification 指出表达片段；(iii) Definition 解释对应编码义。三项准确不等同。
- 任务A在未知命中词项时更困难；测的是提示下的检测、片段识别和定义，不能当作作者主要海量数据标注流程。

**任务B：Dog Whistle Disambiguation** (§4.3)：
- 输入：一个已知词项 D、**词典预给定的编码意义 definition(D)**、10句包含D的上下文。
- 输出：每句属于“使用该定义下的编码义”还是“普通/非对应编码义”，并可附解释。
- 研究者形式化（**非论文提出的训练损失**）：`y_i = 1[ meaning(D, x_i) = definition(D) ]`，`\hat y_i = LLM(x_1,...,x_{10},D,definition(D),prompt)`。这是有强先验的 **给定释义的词义消歧**，不是无条件自由解码，也不证明意图可被心理层面复原。
- 需特别注意“非对应编码义”的语句：也可能在另一社群/政治语境下具有另一种编码意义（§6.1、§7.1）。

## 3. 数据来源、构建流程与 Ground Truth（§3、§6，Table 1）
1. **词项来源**：Allen AI Dog Whistle Glossary 的340个条目、1000+表面变体；词典给出词项、编码定义与相关群体，是 **先验知识**，不是模型自己发现的新义。
2. **候选挖掘**：从美国国会记录（1900–2023）和 Reddit 选定社群评论采集，关键词检索得到 Potential Instance Dataset：Reddit **6,026,910** 条，国会 **1,088,130** 条，合计 **7,115,040** 条。命中仅表示“可能存在暗语”，**不是正例金标**；每段只记录找到的第一个关键词，可能漏掉第二个。
3. **小规模人工评测集**：
   - Synthetic-Detection：论文 **100 条**，50 coded / 50 non-coded（50非正例中一半含普通义词项、另一半无命中词项）；来源仍是现实评论/国会文本，并非全部生成句。
   - Synthetic-Disambiguation：论文 **124 条**，13个 Dog Whistles，通常每词9–10条，含coded/non-coded；两个作者/领域人员独立标注，仅保留双方一致项，分歧排除少于5条。
4. **大规模生成**：从 Potential Instance 中抽取 **100,000** 个候选，针对已知 D 与释义提示 GPT-4 重复独立推理 **3次**，仅保留一致判成编码义的实例；论文得到 **16,550** 个模型筛出的编码正例（Reddit **13,220**，国会 **3,330**），涵盖 **298种根词项**、**706种表面形式**；含日期、source、ingroup、释义以及 speaker/chamber/party 或 subreddit 信息。
5. **人工校核** (§6.1)：另抽取400条模型预测正例人工检查，按原词典定义判断的 precision **85.3%**。把“使用了不同但可能真实的编码意义”的部分例子纳入后，作者给出 **89.4%**。**两者不能与小型消歧集上的95.7% /96.2%混为一谈，也不等于所有16,550逐条人工验证。**
6. **当前公开数据差异（2026-11-08静态页面审计）**：[主数据README](https://huggingface.co/datasets/SALT-NLP/silent_signals/blob/main/README.md) 的 split 元数据为 **16,258** 行（viewer显示16.3k），与正文16,550差**292**；[Detection页面](https://huggingface.co/datasets/SALT-NLP/silent_signals_detection)显示**101**行，与论文100不同；[Disambiguation页面](https://huggingface.co/datasets/SALT-NLP/silent_signals_disambiguation)显示**124**行，但viewer呈现21种表面词、17种根词和3种 label 值，论文却称13个 Dog Whistles 且正文任务为二元消歧。**未下载并逐行核查，不推断具体原因，不将当前公开版与论文版本视为完全一致。**
7. **标签信任级别**：词典级编码义标签（已有知识）→人工小规模正负标注（双人一致）→LLM自动生成的高置信正例（带噪）→400条人工抽审的precision估计。大规模主集本身并非含全量负例、平衡标签的标准二分类测试集。
8. **任务标签≠有害标签**：相关群体及词典定义给出语义背景，不表示每个样本获得独立人工毒性等级、真实说话者歧视意图或伤害后果标签。

## 4. 方法、公式、训练与推理（Fig.2，§4）
- **没有新模型结构、CE监督训练、DPO/PPO或端到端优化目标**。论文采用既有 GPT-3.5、GPT-4、Mixtral、Gemini 的prompt方式；全部报告应视为作者运行的结果。
- 自动检测提示：解释Dog Whistle概念+句子 → 是否含有 → 定位 → 定义；提示要求 JSON 结构输出。
- 词义消歧提示：给定 D 及其**编码定义**，把同一词的10个用例放入集合，逐句判断是否符合定义，解释预测；“同一组10句”是对照上下文，不是让模型无词典发现新暗语。
- **推理一致性过滤**：独立完成 N∈{1,3,5} 次预测。研究者记号（非作者新损失）：若 `\hat y_i^{(1)}=...=\hat y_i^{(N)}=1` 则保留为高置信编码正例；不同预测的样本被弃选。该方法是 **selection/abstention**，不是典型投票、多模型集成或参数训练。对总召回有牺牲，应报告覆盖率和recall。
- Appendix C Table 4/5 对 GPT-3.5 考察**3种问题问法和5种狗哨定义**；这是提示敏感度研究，不能当作因果证明的机制消融。
- Appendix F 另有 GPT-4 给定3–7个真实编码用例生成词义定义的扩展实验，和主线**已知定义消歧**不同；没有解决未知暗语开放发现。

## 5. 实验 Baselines、指标、结果（Table 2、Fig.3、Appendix）
**自动检测**：100条 Synthetic-Detection；比较 4 LLM 的 zero/few-shot，人工众包作为参考（62名MTurk、720次标注；候选词义给定选项，与LLM自由回答条件不完全同构）。Table 2以百分数表示：
| 任务 | Human F1 | 最优 Zero-shot F1 | 最优 Few-shot F1 |
|---|---:|---:|---:|
| Presence | 64.8 | GPT-4 85.7 | Gemini 88.3 |
| Identification | 33.6 | Gemini 61.5 | Gemini 76.0 |
| Definition | 29.7 | Gemini 56.0 | Gemini 73.5 |
注：Table 2不同任务使用的定义/对齐评分应结合原文解释核查；不能将众包较低成绩直接推出LLM真正“比人类更了解社群隐义”，因为受试者先验和答题格式不完全相同。

**消歧**：124条人工标注 Synthetic-Disambiguation，指标为编码正类 Precision/Recall/F1（Fig.3）：
| 模型 / 重复次数 | P | R | F1 |
|---|---:|---:|---:|
| GPT-4，N=1 | 86.4 | 56.7 | 68.5 |
| GPT-4，N=3 | **95.7** | **50.0** | 65.7 |
| GPT-4，N=5 | **96.2** | 71.2 | **82.0** |
- 数据构建采用**N=3**，不是实验中F1最高的N=5；保留N=3仅表示作者按自己的筛选方案操作，不可将96.2%写为所用自动标注流程的实际precision。
- GPT-4优于其它三个在消歧实验中的表现，但不同模型对含有害语义的输出有安全阻断/拒答，可能混淆“语义能力”“平台安全策略”“格式执行能力”；部分模型consistency过滤后recall接近0。
- **关键内部矛盾/未解**：N从3升至5时GPT-4 recall由50.0增至71.2，尽管概念上更严格一致性应该减少被保留预测；可能涉及随机独立运行、评估或不同预测集合，但原文未交代同一批嵌套预测关系，不能视为严格单调门槛验证。

## 6. 作者贡献、局限及证据强度
**可支持的贡献**：
- 将**狗哨词义区分**从简单关键词识别拆出，提出具有实际标注协议的独立消歧子任务；
- 给定词典定义、同词多语境和LLM一致性筛选，形成可扩展的语料抽取工作流；
- 公开具有时代/社群元数据的真实文本语料，可做社群性编码义研究。
**不能支持的主张**：
- **不是**自动发现未知词项、独立推断真实意图、有害度金标、实现端到端因果解释或训练新网络；
- 词典确定的 `ingroup` 不等于对每篇文本作者/受众真实身份或意图的独立观察；
- 时间趋势源于**非均匀词典覆盖、Reddit社区选择、年份原始采样差异**，不能直接推断总体社会语料Dog Whistle流行率；
- 400条抽检85.3%说明自动集存在不可忽视的正例噪声。
**作者自述局限**（§7.2、§9）：定义和使用群体随时间变化，词典不完备；实际表达可能只是引用或批判性转述（referential speech），与蓄意歧视性狗哨不同；是否要求说话者具有显式意图存在语言哲学分歧。
**研究者补充疑点**：人工抽样的分层协议、负例覆盖、词项级未见泛化、时间/跨社群验证、提示与评测定义共享导致的先验捷径、未观察真实听众的解释差异、历史统计的选择偏差、HF公开行数差异，均未关闭。

## 7. 与 P023、P020 及 R1 的联系
- **P023 CodedLang（ACL 2026 Main，CCF-A）**：中文评论中多种编码操作和人工片段/解码标注，检测是否编码、策略分类、下游评分理解；不必具有双重受众效应或歧视义。Silent Signals 是英语政治/社群狗哨，对**词项已知、义项预给定**的上下文消歧，并无七类中文音形转换的开放解码。**编码语言是宽范畴，Dog Whistle是依赖受众分层的特殊交际实践。**
- **P020 (RSA)²（ACL 2025 Main，CCF-A）**：它把修辞策略 r 作为概率语用意义推断条件，评价有限候选意义分布；Silent Signals 是词典定义条件下 LLM 二分类，**不包含RSA L0/S1/L1递归，也未估计人群解释的概率分布**。能否移植RSA要有说话者/听者共同词典、候选语义、社群先验，不可直接宣称已验证。
- **R1映射**：主T1（语境中编码义使用识别）、次T2（已知定义的消歧/定义生成扩展）；T3交际意图仅属理论关联，因无直接真实意图GT；不能归入T4独立有害判断。显式分离 **编码义是否出现 / 所指对象与意义 / 说话者意图 / 有害性标签**。
- **写作位置**：表达机制章节“社群性编码与Dog Whistles”；方法任务章节“已知词义消歧”；可信度章节“词典先验和动态义项、主集伪标签质量”；桥接下一篇 FETCH! 的**未知表达发现**。

## 8. 代码/可复现状态与开放核验项
- 作者公开可访问的主数据、两个评测集及两个海量潜在候选集，HF页可读取其Schema；主数据页显示 **CC BY-SA 4.0**。
- **截至本次定向检查，官方论文与数据卡未列完整评测脚本仓库；没有找到经作者确认的独立官方代码仓库**。不能把第三方项目写成作者代码，也不能宣称完整复现。
- 仅核对正式PDF和公开页面/README，**尚未下载Parquet逐行统计、验证代码/复跑LLM或核对复现API成本**。大规模管线使用商业API GPT-4，不满足本项目“无付费API”的完整原始复现条件；但读取公开结果、用本地模型测试小评测集可另行设计。
- 待核验：16,550 vs 16,258、100 vs 101、13 vs 17根词及3 labels、N3/N5精度与召回变化、人工验证的独立性及采样细节、是否存在官方运行脚本。

**结论（定稿版）**：本文最有价值的是用社群已知编码词义+上下文对照定义“狗哨语义消歧”的可操作任务，而非新训练算法。其大规模高置信数据是LLM自动筛出的**带噪正例语料**，仍需对普通义负例、引用/意图、动态跨群体意义和出版版本差异进行严格限制。这些边界对广义隐晦信息综述至关重要。

## 9. 主要证据索引
- [ACL正式版 §1–§9、Table1–2、Fig2–3、Appendix C/F](https://aclanthology.org/2024.acl-long.675.pdf)
- [官方论文元数据](https://aclanthology.org/2024.acl-long.675/)
- [HF主数据Schema及split metadata](https://huggingface.co/datasets/SALT-NLP/silent_signals/blob/main/README.md)
- [HF人工检测集](https://huggingface.co/datasets/SALT-NLP/silent_signals_detection)
- [HF人工消歧集](https://huggingface.co/datasets/SALT-NLP/silent_signals_disambiguation)
- [HF Reddit潜在候选集](https://huggingface.co/datasets/SALT-NLP/informal_potential_dogwhistles)
- [HF国会潜在候选集](https://huggingface.co/datasets/SALT-NLP/formal_potential_dogwhistles)
