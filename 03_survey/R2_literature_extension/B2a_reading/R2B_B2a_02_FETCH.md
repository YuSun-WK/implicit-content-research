# R2-B / B2a-02｜Making FETCH! Happen — 定稿阅读卡

> **状态：2026-11-08 用户确认定稿；保留数据与代码未关闭问题、未作独立复现；不改变已有 P001–P041、T001–T018 及阅读卡。**  
> **临时编号：R2A-007**；研究范围：Dog Whistle / 社群编码表达的**词项发现**；R1 主任务 T1，T2/T3 仅机制关联，T4 有害性为下游关联而非本论文直接输出。  
> **核验范围（2026-11-08）**：ACL 2025 Main 正式23页 PDF（含主要图表与附录G）；作者 GitHub 仓库 README、主运行、数据预处理、分词项、索引及指标源码静态审查。未运行全量实验，未逐行下载所有语料。凡无独立实验支持的评论标为“研究者判断”。

## 1. 基础信息和主要贡献
- 完整标题：**Making FETCH! Happen: Finding Emergent Dog Whistles Through Common Habitats**。
- 作者：Kuleen Sasse, Carlos Alejandro Aguirre, Isabel Cachola, Sharon Levy, Mark Dredze。
- ACL 2025 Main Conference（Long Papers），CCF-A，5687–5709；DOI: 10.18653/v1/2025.acl-long.284。
- [正式论文](https://aclanthology.org/2025.acl-long.284/) · [正式PDF](https://aclanthology.org/2025.acl-long.284.pdf) · [作者代码](https://github.com/KuleenS/FETCH-Dog-Whistle)。
- 作者贡献：(i) FETCH! 新任务及三种语料场景；(ii) Word2Vec/Phrase2Vec、MLM、EPD公开基线的同任务比较；(iii) EarShot，向量近邻检索+LLM/有害分类器过滤+词项抽取的可扩展强基线。
- **核心判读**：本文的“emergent / novel”在**主定量评测**里意为 **词项未提供给系统，但已经存在研究者的已知 Dog Whistle 金标词典**。这不是开放世界从未被登记过的真正新词发掘。附录G有研究者从模型输出中事后挑出的候选新词实例，另论，不能与主表 F0.5 混为同一金标。

## 2. 动机与任务 (X,Y,G,E)
**动机（§1-3）**：传统已知词典匹配/给定词义消歧无法应对演变中出现的未登记编码表达；Dog Whistle受特定社群、受众和上下文影响，表达表面义与社群内义不同；作者尝试由已知种子周围的“common habitats”（相似语义/社交语境）寻找其它术语。

**任务定义（§3，论文语义，研究者形式化）**：
- X = 目标语料集合 C，加上其中已知的种子Dog Whistle根词项集合 S（及其表面形式）。
- Y = 预测此前对系统隐藏的 Dog Whistle **类型/词项列表** \hat D，不是逐条帖子是否有害的分类，不强制输出自然语言意义解释。
- G = 按语料里能找到的参考词典条目形成金标 D，划分20% S（种子）/80% H（held-out），按 n-gram 长度分层；保留各根词的表面变体。同根词应整体划分，词表提供语义先验。
- E = 预测类型和参考词项（根词或至少一个表面形式）严格匹配后的 Precision、Data Potential Recall（DPR）、F_0.5。
- **不是**：训练生成新的政治暗语；验证每个帖子中存在双重受众解读；做已知词项的句子级WSD；输出有害程度或推断可观测的说话者真实心理意图。
- 强区分：词典外未知且真实存在的新暗语，在主评测中也可能被算作“预测错误”；因此 F0.5 衡量的是**保留词典条目的发现能力**，不是未知语义发现的实际完整准确率。

## 3. 三种实验场景、数据构建与GT（§3、Table 1）
| 场景 | 原料 | 语料量 | 在语料中找到的金标根词数 | 金标来源及可靠性 |
|---|---|---:|---:|---|
| Synthetic / Reddit | 借用 Silent Signals，原文约16k条，45个争议subreddit；由GPT-4识别编码用例 | 约16k，近乎每条均带所标词 | 298 / 298 | **Silent Signals LLM自动标注的正例**，不是全部人工确认；“Synthetic”不等于生成的假句。原公开版本行数另有差异，见前一篇阅读卡 |
| Balanced / Gab | 被作者称作Dog Whistle高发生率站点的帖子 | 约300,000 | 77 / 340 | Mendelsohn等(2023)人工词典 + regex 语料匹配，不是语境人工金标 |
| Realistic / Twitter | 2017-01至2022-12公开1%流，先约10亿条，抽取6m未匹配词典和1m潜在匹配词典 | 7,000,000 | 177 / 340 | 同上；6m“无”由**词典匹配阴性**判定，不是不存在其它暗语的人类金标；1m人为富集正候选，样本分布不是自然原始流基准率 |
- 金标参考词典约340种根词及相应表面形式，来自社群wiki与学术资料；非每个样本独立解码确认。每种场景按词项长度 stratified split，20%提供给系统做种子，剩80%评估发现。
- **重大GT边界**：Balanced/Realistic的“存在某词”来自对句子正则命中，不能区别正常字面使用、引用批评、反讽或恶意社群编码使用；论文 §9 也承认欠缺专用人工标注语料可出现假阳性。
- **金标覆盖差异**：词典外暗语可能落在分母之外、被判预测假阳；“已知词但新社群含义”并未独立编码成新标签。分层按n-gram而非群体/时间，不能声称时间OOV或跨文化泛化已被验证。
- **数据公开性**：代码有重建管线与数据文件输入协议；截至本次静态审计未确认三场景全部原始Gab/Twitter文字可免申请直接下载，尤其Twitter历史数据不能仅凭GitHub代码存在宣称完全可复现。Silent Signals与词典是可追溯公开资源，但版本/许可需要实际下载复核。

## 4. 方法流水线与技术细节（§4、Fig.2）
### 4.1 Baseline：非EarShot
1. Word2Vec/Phrase2Vec：在目标语料上预处理、训练100维词/短语向量，窗口5、10 epochs、最大词表50万；对种子词取10近邻并向外扩展10轮；uni/bi/tri-gram分别测试。基于分布相似发现词，而非句子分类。
2. MLM：取含种子词的2000条语句，对种子遮蔽后使用 Bernice/BERTweet 预测 top-k 代替单token，k在50～25600内搜索。
3. EPD：AutoPhrase提候选多词组→Word2Vec与种子求相似筛前1000→2000条种子句替换候选→SpanBERT评价句子/短语兼容性→top-k输出；这已是委婉语新词发现技术的迁移，不能当成FETCH独有思路。

### 4.2 EarShot：三阶段 + 两条分支
- **第一阶段 Embed/Index**：对全部帖文用 all-MiniLM-L6-v2 SentenceTransformer生成归一化句向量，建 ChromaDB 向量库。此阶段主要是句子相似度，尚没有训练Dog Whistle识别器。
- **第二阶段 Retrieve**：找出含种子词的句子，检索库中与这些句向量最接近但不属于种子句本身的帖子。**代码的核心检索调用 get_top_k_documents(..., 1)，每个seed帖子只要求1个最近邻**；“共栖语境”由向量近邻近似，未显式建模社群身份、时间传播或真正受众差异。
- **第三阶段 A｜DIRECT**：直接把近邻帖子输入开源LLM（Llama 3.1 8B Instruct、Mistral 7B Instruct、Llama 2 13B Chat）用 prompt抽取dogwhistle短语，要求JSON。可生成较长短语，召回较高但噪声大。
- **第三阶段 B｜PREDICT**：先过滤近邻帖子，再通过 KeyBERT、RAKE、YAKE、TextRank、TF-IDF 等关键词抽取器取 top-k n-gram。过滤器可以是现成hate/toxicity分类器（ToxiGen HateBERT、RoBERTa Dynabench R4、HateXplain BERT）或上述LLM对是否有Dog Whistle做Yes/No判定。该分支“按帖子筛选→关键词提取”不是端到端训练。
- 作者也试过用种子帖子为正、随机其它帖子为负、2 epochs/lr=2e-5/weight_decay=0.01微调现成分类器；论文称得到全零预测，主结果并非依赖该监督训练分支。
- **训练与损失**：EarShot主方法无新建联合可训练网络，无作者自创CE/DPO/RL公式；Embedding和LLM为预训练模型推理，BERT分类器多为off-the-shelf。Word2Vec在目标语料自监督训练，不能写成整个系统“完全无需训练”。

### 4.3 核心评测公式（以下为研究者根据§3.4重写，非本文新优化目标）
令预测词项类型集合 P、被隐藏的词典类型 H，其中语料实际可匹配的为 H_C：
- Precision = 被词典/变体接受的预测项数 / 模型预测项数；
- DPR = 被找到的不同参考根词项数 / |H_C|；
- F_β = (1+β²)PR/(β² P+R)，β=0.5，论文以 DPR 代R。
这里 β<1 意味着 **精确率权重大于召回率**（理由：减少人工复查负担）。注意 precision 在代码中对输出列表计数、recall以根词去重，两者统计对象不完全相同；也未对真实发现词义的语境做语义审核。

## 5. 实验设计与主要结果（§5、Tables 2–5；单位为%）
**主要比较**：同三场景、Word2Vec/Phrase2Vec、MLM、EPD、EarShot-DIRECT、EarShot-PREDICT；PREDICT选最优过滤器+关键词提取器+top-k阈值+n-gram范围，DIRECT比较3个7B–13B开源LLM。Table 4/5给的是不同数据集上各自选出的最优配置，**不是单个固定模型跨场景零调参泛化**。

| 场景 | Word2Vec/Phrase2Vec最优 F0.5 | MLM/EPD最优 F0.5 | EarShot PREDICT最优 F0.5 | EarShot DIRECT最优 F0.5 |
|---|---:|---:|---:|---:|
| Synthetic / Reddit | 5.91 | 2.03 | 14.55（RoBERTa R4+KeyBERT） | **23.29**（Llama2 13B） |
| Balanced / Gab | 1.86 | 0.28 | **5.70**（RoBERTa R4+KeyBERT） | 3.52（Llama2 13B） |
| Realistic / Twitter | 2.47 | 0.61 | **4.63**（HateXplain BERT+YAKE） | 1.17（Llama3.1 8B） |

- Synthetic DIRECT Llama2-13B：P=20.31、DPR=56.30、F0.5=23.29。较广覆盖，precision偏低。
- Balanced PREDICT RoBERTa R4+KeyBERT：P=14.81、DPR=1.65、F0.5=5.70。**发现总量很低**。
- Realistic PREDICT HateXplain+YAKE：P=10.00、DPR=1.47、F0.5=4.63。意味着按词项类型核对仍约90%预测不在金标，且找到的参考词很少，不能宣称实际部署已好用。
- Realistic DIRECT Llama3.1-8B：P=0.94、DPR=60.29、F0.5=1.17；**DPR高不能遮蔽极低precision**。
- Appendix G：作者人工查看top模型输出，举出少量词典外候选，如Wakanda、zogbots等，用语境解释可能的编码义；但**Realistic最优模型没有找到新的词典外Dog Whistle**。这部分是质性案例、非有系统人工标注GT的大规模开放发现准确率。
- 主结果为论文报告，本项目尚未运行对照实验。

## 6. 消融、独立贡献与评测缺口
作者有阈值、提取器、不同BERT与不同LLM、uni/bi/tri-gram等配置对照（附录D–F），但不是完整归因消融：
1. 没有充分的“无近邻检索/随机检索/同主题检索/检索原帖”同预算严格对照，因此**向量近邻的独立贡献**未被完全分离；
2. 没有“去有害过滤器、保留相同候选规模”的严格混杂控制；不同过滤器导致保留帖子规模差异；
3. 按各场景最优F0.5挑阈值，未见独立验证集的稳定跨域决策协议；评测结果可能含调参选择效应；
4. 没有独立的人类受众解释、真实交际动机、词义解码正确性及有害程度标签；
5. 没有专门的历史时间先后训练-测试/社群迁移评测；
6. 词典外真新词主指标反而可能算错，附录G的事后解释并不等同开放发现金标；
7. 编码语言可无害，直接用hate classifier做过滤既可能损失有趣的非仇恨编码，也会偏向显性辱骂/贬损语句：作者§6.1.3自己指出Balanced场景的系统偏向明确侮辱词、错过更细微表达。
因此“EarShot性能好”应具体写成“**在该词典回收型任务和F0.5目标上，相比已测基线更好**”，不得写成“已可靠发现未知人类社群暗语”。

## 7. 官方代码审计（GitHub内容事实 vs 推断）
- [README](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/README.md)确实列出 Word2Vec/MLM/EPD/EarShot 评测入口、split脚本和环境。 [earshot.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/earshot/scripts/earshot.py) 中的检索→直接抽取/二段式过滤→提取流程与论文总体一致；[sentencetransformer.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/earshot/embedding/sentencetransformer.py) 使用 all-MiniLM-L6-v2/normalize_embeddings；[chromadb.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/earshot/db/chromadb.py) 实现 top-1 向量近邻。
- **具体实现疑点 A**：earshot.py 的 DIRECT 分支在评估前读取 args.input_files[0]，但同脚本 argparse 未声明 input_files。这会在该执行路径引起 AttributeError（静态代码推断），应检查作者正式运行版本或修复。
- **具体实现疑点 B**：LLM-PREDICT 过滤实现 any(x in prediction for x in ["yes","y"])，接受包含单字母 y 的输出而非严格的 “yes”；若模型产生其它含 y 的文字，存在假阳过滤风险。代码与论文“明确yes”不是完全同义。
- **具体实现疑点 C**：[recall.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/scripts/recall.py) 用文本模式 w 打开文件却执行 pickle.dump，Python3二进制pickle写入文本文件存在TypeError风险。且该脚本输出列表，而 [utils.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/utils.py) DogwhistleSplitterOther 遍历该对象时按字典键读取 self.seen_dogwhistles[x]，与列表类型不匹配；外部不同版本中间件是否避免该冲突尚未核实。
- **具体实现疑点 D**：[metrics.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/metrics.py) 的Precision按预测列表计数而Recall以对应根词去重，重复词输出与根词映射如何影响P应专项复核。实现侧的预测类型统计方式与通常二分类precision不同，不可误把表中数值当帖子级分类率。
- 以上均为**静态检查发现、尚未执行复现**，不能以代码当前潜在错误直接否定论文报告结果；可能存在未公开运行版本或依赖特定输入格式。
- 可实施性：作者公开源码和环境，但全量7m向量化+ChromaDB+可能13B生成成本高，且Gab/Twitter原始语料可达性未核实；**不满足“拿来即可用单卡16–20GiB、≤6h完整重跑”的已证条件**。低成本先在Silent Signals子集和现成嵌入/开源7B量化环境检查检索+词项指标，有可能，但尚未试验。

## 8. 与 B2a-01 Silent Signals、P023、P020 的关系
| 工作 | 已知/未知词项 | 输入-输出焦点 | 所用知识 | “意义正确”如何验证 |
|---|---|---|---|---|
| Silent Signals，ACL2024 Main A | **已知**Dog Whistle及其已知编码义 | 文本+词项+定义 → 该语境是否使用其编码义 | 专家词典/社群释义 | 小型人类WSD集；大集自动标注抽查 |
| FETCH!，ACL2025 Main A | 系统不知道待找的词项，但**金标词典预先知道** | 语料+已知种子 → 隐藏的其它**词项列表** | 种子词、相似帖向量、已有金标词典评测 | 主要是词项字符串命中，**不是语境义核验** |
| P023 CodedLang，ACL2026 Main A | 人工挖掘现实中文评论中的多机制编码 | 评论/片段 → 编码存在/机制/评价理解 | 汉字音系、字形、社群映射与人类解码 | 片段+解码词项有人工标注；不仅仇恨，涵盖无害编码 |
| P020 RSA²，ACL2025 Main A | 预设修辞策略/候选意义 | 表达+语境+候选意义 → 意义概率 | 策略条件映射、意义先验与递归 | 有限候选意义和人类判断；不是词项发现 |
- **最关键研究启示**：必须分开 **新表面形式发现(T1)**、**语境编码义消歧/解码(T2)**、**群体受众及交际意图(T3)**、**伤害分类(T4)**。检索到新短语 ≠ 知道其编码义；知道存在编码义 ≠ 该句有害。需要对“可审阅的词汇发现”与“可信解释/人类验证”分层讨论。
- 对 R1 综述：将 Dog Whistle / dynamic coded language 的任务进一步拆分为“给定词典的实例级WSD”与“seed-based 词项类型发现”，在证据章重点强调类型级金标 vs 实例级意义/意图金标的巨大差异。不要直接把 FETCH! 当成语用意图推理 T3 或有害内容检测 T4。
- 方法迁移审计：Word2Vec/MLM/EPD 已作为先例；“语义相似检索+LLM抽取新编码词”也已在EarShot实现。直接照搬为新idea缺乏新颖性，需要先证明新失败机制或数据协议能更可靠支持发现。

## 9. 待核验问题（优先级按综述引用风险）
1. [最高] 合法词典外候选输出会被现有gold精度计为false positive的比例有多大？能否系统人工抽检，而非只报告2–3个例子？
2. [最高] 所谓句子级Dog Whistle GT如何区分普通词义/引用/有意编码？regex到底会引入多少假阳？
3. [最高] 当前GitHub的DIRECT、recall和split流程能否无修复完整执行？正式论文报告的模型运行版本、实际命令与commit是什么？
4. [高] 标准化的不同场景seed/test根词是否泄漏同源变体、语义近义词或训练模型记忆？分层随机种子及多seed置信区间在哪里？
5. [高] 无检索、随机检索、检索数量K以及选择性过滤，在相同候选数、token预算和评测集上净增益多少？
6. [高] Twitter 7m“realistic”的人为1m匹配正例富集是否改变真实流行度；真实部署中 Precision-Recall 会怎样？
7. [高] 原始Gab/Twitter数据是否可下载/许可研究使用，已有模型运行权重和中间索引是否公开？
8. [中] 在非有害的编码语言和跨语种/时间动态表达上，基于毒性过滤器的方法是否系统漏检？
9. [中] 对目前公开模型在历史互联网数据上的预训练污染，是否有更可信时间先后holdout？论文已在Limitations承认 contamination风险。

## 10. 精读结论（定稿）
- **任务创新**：明确了“从已有种子出发发现系统未见Dog Whistle类型”的可评测设置，并建立三种难度场景；但指标只覆盖旧词典的 held-out 词项。
- **方法创新**：EarShot是**句向量召回+LLM/分类器过滤+开放/关键词抽取**的系统工程型组合；不是新的Transformer层、损失函数或联合优化框架。
- **证据限制**：最真实的稀疏Twitter设置最佳 F0.5 只有4.63%，主GT缺少语境人工核验，附录G Realistic最优方法没有真正新暗语案例。因而“有效解决未知暗语发现”的强结论不成立；“建立可复现研究基准和初步系统”更恰当。
- **综述价值**：与Silent Signals形成**已知义消歧 vs held-out词项发现**的任务对照，是广义隐晦信息综述里编码表达专节的核心证据；要特别把“检索相似语料”“解释真实隐含义”“确认有害性”拆开叙述。
- **核验状态**：已看官方PDF正文和附录、静态查源码，未全量复现、未完成真实词表误差审计。谨慎引用表格和作者的宣传性术语。

## 11. 索引与证据
- [ACL正式会议论文页](https://aclanthology.org/2025.acl-long.284/) / [官方PDF](https://aclanthology.org/2025.acl-long.284.pdf)：§1–3任务、语料、标签、Table1；§4 EarShot、Fig2；§5 Tables2–5；§6–9结论及局限；Appendix G 真实未知词项的质性例证。
- [GitHub README](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/README.md) / [earshot.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/earshot/scripts/earshot.py) / [chromadb.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/earshot/db/chromadb.py) / [metrics.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/metrics.py) / [recall.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/scripts/recall.py) / [utils.py](https://github.com/KuleenS/FETCH-Dog-Whistle/blob/main/src/utils.py)。
- 本项目相关已定稿：[R2B_B2a_01_Silent_Signals.md](R2B_B2a_01_Silent_Signals.md)、[P023 CodedLang](../../../01_literature/cards/P023_CodedLang.md)、[P020 RSA²](../../../01_literature/cards/P020_RSA2.md)。
