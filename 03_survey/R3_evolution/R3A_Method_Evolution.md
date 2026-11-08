# R3-A2｜广义隐晦信息研究的方法技术演进（审阅稿）

日期：2026-11-08。状态：**REVIEW DRAFT，仅完成 R3-A2，等待学术审阅，不合并main**。本文件承接[R3-A1研究史](R3A_Research_Evolution.md)及R1、R2-C。采用R0去重59篇、R2-A新增32篇候选、R2-B新增16篇精读与原有P系列卡片；**不是对91篇全部完成全文精读或独立GPU复现**。保留原始P/T/R2A编号。

评级按2026版CCF刊会口径：ACL、AAAI、ICCV、CVPR、ICLR、ICML、WWW等为CCF-A；COLING、EMNLP、NAACL为CCF-B；Findings、Workshop、Datasets & Benchmarks、录用尚未正式出版论文另标注。证据：[P]作者论文与主表报告；[S]本项目此前公开代码/数据静态核验；[H]综述研究者综合推断；[O]未验证。P/S不代表在本项目复现成功。

## 0. 总论与路线图

**不能写成“规则→PLM→LLM→VLM，依次淘汰”**。研究的技术演进是不同任务上对以下五类不足做交叉响应：[H]
1. **表面形式与真实含义不对齐**：已知表达的歧义、修辞策略和社群编码；
2. **语域、社群、时间与风格漂移**：监督训练分布不等于实际应用；
3. **单一标签缺少解释粒度**：检测到隐喻/仇恨，不等于解释源域、目标与立场；
4. **多模态输入存在特权信息和捷径**：加图、加情绪、加Oracle信息并不自动证明联合理解；
5. **输入风险与回答行为不同**：风险漏检、误报、误拒、危险生成需要分别监督和评价。

任务对应R1的T1表达识别、T2候选意义解释、T3语用功能推断、T4有害性分类、T5联合模态特殊风险、T6安全响应。**技术路线和任务是多对多关系，不存在所有模型共同的“性能SOTA曲线”。**

| 方法族 | 初始瓶颈 | 新增的核心机制 | 作者支持的结果类型 | 尚未证实的主张 |
|---|---|---|---|---|
| M1 词典、规则、统计原型与概率语用 | 已知词的歧义，非字面含义难恢复 | 字面/编码词表、语境原型、RSA说话者—听者条件概率 | 有限候选义项的推断及隐喻源域测量[P] | 开放新义、真实发言者内心意图[O] |
| M2 PLM监督、对比与域适应 | 基准拟合过强、域外泛化不足 | CE/BCE、语义正负对、伪配对、表示解耦、集成优化 | 对各自数据集的分类或迁移指标改善[P] | 对齐表示=正确恢复隐含意义[O] |
| M3 LLM提示、检索与工具 | 语用知识广、动态新义难内化 | 定义条件推断、近邻搜索、在线证据、工具调用SFT | 编码义消歧、词项回收、新词毒性分类[P] | 词典留出等于真实时间新词、解释忠实[O] |
| M4 跨模态细粒度融合与多任务 | 标签过粗、图文对象与关系复杂 | 对象局部特征、global-local融合、辅助情绪、共享LoRA/私有专家 | 多任务分类、概念预测或视觉蕴含分数[P] | 情绪有独立因果贡献、视觉绝对必要[O] |
| M5 解释监督与偏好/不确定性优化 | 输出标签但依据可能不可信 | 解释SFT、DPO、GRPO、答案熵奖励、课程训练 | 特定分类与解释指标改善[P] | 合理/确定的理由就是忠实证据[O] |
| M6 联合风险判别与安全后训练 | 联合风险漏判、过度拒答 | Guard、反事实触发归因、Step-DPO、自验证与GRPO | 危险检测或输出安全/有用性提升[P] | 安全回复率可替代输入危害理解[O] |

## 1. M1｜规则、词典、原型与概率语用

**试图解决什么**：在词项和部分语义约定已知的情况下，透明地定位表达、定义候选意义或刻画说话者如何在语境中选择表达。

**方法机制**：词典/正则和n-gram匹配已知项；专家定义、编码词表与语境线索支持条件消歧；语义原型相似度用于衡量特定隐喻源域。RSA使用字面听者、策略性说话者和语用听者构建概率递归。

- **P020 (RSA)²**，[ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1019/)：把修辞策略r及其与意义m的相容性纳入RSA，使非字面意义不再被严格字面真值排除。[P] 作者报告特定天气反讽、数字表达的候选意义预测改进。[S] 卡片消融表明意义先验贡献突出，未充分证明递归更新本身贡献最大；替代表达及候选集合也可能带来信息优势。
- **R2A-011 When People are Floods**，[ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.398/)：局部词级LLM线索与SBERT文档源域原型相似度互补。[P] 支持某些隐喻源域的测量；人审GT是**隐喻源域**，不是非人化或仇恨GT。
- **R2A-006 Silent Signals**，[ACL 2024 Main，CCF-A](https://aclanthology.org/2024.acl-long.675/)：虽然利用LLM提示，仍要求预给Dog Whistle词项和编码义定义；与开放新词发现不同。

**方法边界**：规则、词典及概率语用并未随LLM出现而失效；它们常用作候选召回、可控先验、解释对象或对照实验。[H] 但词表存在≠该句采用编码义；策略条件概率≠真实说话者内心状态；未指定候选义时无法凭此保证开放世界语义恢复。

证据：[P020精读](../../01_literature/cards/P020_RSA2.md)、[B2a综合](../R2_literature_extension/B2a_reading/R2B_B2a_Synthesis.md)、[B2b综合](../R2_literature_extension/B2b_reading/R2B_B2b_Synthesis.md)。

## 2. M2｜PLM监督学习、对比学习、领域适应和表示去偏

**原始做法**：BERT/RoBERTa等编码器 + 分类头 + CE/BCE，依靠已有标签拟合“是否隐喻、反讽、隐式仇恨/冒犯”等T1/T4任务。[P] 可得到特定IID数据上的高分类性能；[H] 但主题词、目标群体、平台或语体等可能与标签相关，从而影响跨域可靠性。

| 工作（正式出处、等级） | 引入的新机制 | 论文直接支持[P]与限制[S/H/O] |
|---|---|---|
| **P032 ImpCon**，[COLING 2022 Main，CCF-B](https://aclanthology.org/2022.coling-1.579/) | 将原隐含仇恨句与人工implied statement或增强文本构正对，CE+对比损失 | 作者跨IHC/SBIC/DynaHate报告分类改进；不是所有样本都含人审解释，不足以证明模型完成语用解释。 |
| **R2A-008 FA-Net / Hidden Chasm**，[AAAI 2024 Technical，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/29786) | 显性词遮蔽代理监督、域内对比(IC)、跨域相似度伪正对(HC)、目标域预测熵最小化(EM) | 作者在固定目标词类别的委婉语解码协议上报告改善；目标域文本参加适应，伪正对类别错配率未证。不是“未见词时间泛化”。 |
| **P029 RV-HATE**，[ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.2104/) | 四个BERT模块采用不同处理/对比策略，集成预测以PPO搜索权重 | 作者表中等权平均Macro-F1 83.78→PPO 84.47，差0.69个百分点；[S] 当前公开脚本在测试数据labels上寻权并在同集测试，存在严重协议问题，但不直接证明正式发表运行使用同版本。低维权重搜索对比不足。 |
| **P033 CADET**，[WWW 2026 Main，CCF-A](https://doi.org/10.1145/3774904.3792669) | 对显/隐风格的表示解耦、对抗/正交约束、风格反事实 | [P] 作者报告跨风格改善；[S/O] 所查代码的部分反事实/循环实现与论文叙述待闭合，不能直接宣称识别了社会因果变量。 |

**创新性红线**：对比学习/伪正样本/无监督域适应不是新范式；从另一领域迁移时须比较ImpCon/FA-Net/CADET。单一t-SNE可视化或跨数据集F1提高**不能证明**模型已学到真实隐含命题。RV-HATE的PPO还需要与同等预算的验证集网格、随机、Bayesian权重搜索比较，且应完全隔离test标签。

证据：[P032精读](../../01_literature/cards/P032_ImpCon.md)、[FA-Net精读](../R2_literature_extension/B2a_reading/R2B_B2a_03_Hidden_Chasm_FA_Net.md)、[P029精读](../../01_literature/cards/P029_RV-HATE.md)、[P033精读](../../01_literature/cards/P033_CADET.md)。

## 3. M3｜LLM提示、语义推理、检索增强与工具调用

| 工作（正式出处、等级） | 研究问题和具体机制 | 实验支持与必要限制 |
|---|---|---|
| **R2A-006 Silent Signals**，[ACL 2024 Main，A](https://aclanthology.org/2024.acl-long.675/) | 已知词项及**已知编码义定义**输入LLM，以多次一致判定筛选真实上下文中的狗哨使用 | [P] 有人工小集和400例人工抽查；大规模16,550模型筛选正例抽查precision 85.3%，不等于全量人工金标。[S] HF主集公开记录16,258，存在版本差异。 |
| **R2A-007 FETCH!**，[ACL 2025 Main，A](https://aclanthology.org/2025.acl-long.284/) | 根据已知种子词共同语境建句向量索引，近邻检索→LLM/分类器过滤→关键词抽取；另有直接LLM抽取 | [P] 词项级回收；[S] 20/80 split为**已有词典**的词项留出，不是现实时间上新词的严格open-world标注；真实Twitter设定表现弱。 |
| **P020 (RSA)²**，[ACL 2025 Main，A](https://aclanthology.org/2025.acl-long.1019/) | LLM生成/概率结合候选意义、修辞策略与RSA | [P/S] 策略信息和先验在特定候选任务受益，不意味着自由恢复全部交际含义。 |
| **P035 EmoBi**，[ACL 2025 Main，A](../../01_literature/cards/P035_EmoBi.md) | 情绪/隐喻/夸张互相提供提示；最终LLM重判 | [P] 作者在对应双任务数据上报告收益；[S] 公开实现更接近隐喻先行→夸张后行→联合重判，不是双向无限迭代；验证没有独立ground truth。 |
| **R2A-010 SeTox**，[ACL 2026 Main，A](https://aclanthology.org/2026.acl-long.1602/) | 针对中文动态新兴词，搜索外部语境证据，并用工具调用轨迹SFT改善毒性分类 | [P] 作者报告小模型在新词毒性测试上改善；[S/O] model-unknown相对固定基础模型，未证严格时间未知；词项重合、搜索时点和外部信息污染仍待审核。 |

### 把“评测”和“技术改进”分开
- **R2A-001 DRInQ**，[ACL 2026 Main，A](https://aclanthology.org/2026.acl-long.1597/)：同一问句变化上下文下五选一含义判断，主要是任务/基准。
- **R2A-002 VAGUE**，[ICCV 2025 Main，A](https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html)：图像情境下间接行动四选一，主要是基准及评测。
- **R2A-004 Rhetorical Questions**，[ACL 2026 Main，A](https://aclanthology.org/2026.acl-long.5/)：冻结模型线性探针检查反问线索可读性，主要是内部表示诊断，不等于新反问生成训练体系。

**不能直接宣称创新的做法**：“语义近邻检索+LLM找编码词”（FETCH!已有），“新词搜索+模型判断毒性”（SeTox已有），“给定编码定义提示LLM消歧”（Silent Signals已有），“加入情绪/修辞提示并自我验证”（EmoBi已有）。要构成方法贡献，需证明不同的、可衡量的失败机制且排除简单等预算Prompt/检索对照。[H]

证据：[B1综合](../R2_literature_extension/B1_reading/R2B_B1_Synthesis_DRAFT.md)、[B2a综合](../R2_literature_extension/B2a_reading/R2B_B2a_Synthesis.md)、[B2b综合](../R2_literature_extension/B2b_reading/R2B_B2b_Synthesis.md)。

## 4. M4｜多模态融合、多任务细粒度语义与条件瓶颈

### 4.1 从分类向概念、对象、解释和意图
- **R2A-025 RGCL**，[ACL 2024 Main，CCF-A](https://aclanthology.org/2024.acl-long.291/)：多模态Hateful Meme中的检索引导对比学习；后续检索式检测不能称检索首次用于该任务。
- **P026 RA-HMD**，[EMNLP 2025 Main，CCF-B](https://aclanthology.org/2025.emnlp-main.1215/)：LLM hidden state接语言模型分类辅助路径和MLP分类头，检索/KNN改善作者的跨域Hateful Meme协议。LMH监督来自**相同类别标签的词元生成**，不是额外金标解释，也不是保证通用语言能力保留的充分因果证据。
- **P003 MultiMM**，[ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1275/)：多文化图文隐喻、源/目标与情感标注；SEMD图文编码+情感表示。[P] 消融支持加入情感输入的分数改善；[S] 所查测试代码将**人工gold sentiment**作为输入，缺少只输入原始图文→预测情感→隐喻的完整公平流水线。
- **P019 V-FLUTE**，[NAACL 2025 Main，CCF-B](https://aclanthology.org/2025.naacl-long.1/)：将图文修辞理解变为visual entailment标签及解释生成任务。作者白图重训64.77、真实图片72.78，支持视觉带来预测信息，不独立证明正确非字面关系；参考解释分数≠忠实性。
- **R2A-018 MGMCF**，[AAAI 2025 Technical，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/34801)：对象级线索+global/local融合+多任务分类+作者所谓Dual-Semantic损失。[P] 删模块影响任务得分；[S/O] 当前代码在test接收源/目标域辅助特征，损失实现与论文叙述存在实质差异，字段真实来源待核。不能断言论文实验已gold泄漏。
- **R2A-017 M3UCD**，[AAAI 2026 Technical，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/40808)：细粒度图文隐喻多属性数据与共享LoRA训练。[P] 作者报告多任务部分收益，也存在负迁移；没有same-token/step+辅助标签随机化，不能归因真正任务知识迁移。
- **R2A-019 DOSE**，[ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.319/)：共享/私有低秩专家+参数正交，在反讽的检测、机制、对象、意图等MCQ任务训练。[P] 整体表现提升；[S] 当前公开1%训练子集存在MCQ选项位置/长度捷径信号，仅是小训练子集审计，不代表全测试已有相同问题；参数正交不等于梯度冲突已直接测量为零。

### 4.2 新的直接竞争：多模态捷径已经被方法化
**R2A-024 MCIB**，[AAAI 2026 Technical Track，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/39874/)：官方正式摘要说明从MUStARD++清理角色、笑声等shortcut构建MUStARD++R，并提出条件信息瓶颈融合模型以改进反讽检测与泛化。[P：本阶段仅官方摘要层确认；R3-B并行全文精读中]。

这足以推翻“首次研究多模态反讽捷径”的新颖性主张，但**不等于已审计MCIB消融的独立有效性**。[O] 样本选择、条件信息瓶颈损失、真实预算与泛化机制仍由R3-B复核。

### 4.3 技术演变的主要学术判断
从“image+text→分类”逐步扩展为“概念/对象/情绪/交际功能多任务预测”，并反过来追问**模型是否真正依赖那些使标签改变的视觉关系**。[H] 表达为“多任务/融合在特定实验条件下取得经验收益”是成立的；表达为“已经证明情绪因果帮助隐喻映射、LoRA专家完全消除了梯度冲突或视觉不可替代”则证据不足。

证据：[B3a跨论文综合](../R2_synthesis/B3a_Cross_Paper_Synthesis.md)、[P003](../../01_literature/cards/P003_MultiMM.md)、[P019](../../01_literature/cards/P019_V-FLUTE.md)、[P026](../../01_literature/cards/P026_RA-HMD.md)。

## 5. M5｜解释监督、DPO/GRPO与预测确定性的可靠性边界

| 方法及等级 | 机制差异 | 已支持证据与不足 |
|---|---|---|
| **P030 SMARTER**，[ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1584/) | 先利用已有HateCOT及少样本SFT生成解释，再将正确/错误标签+解释组成偏好对，用DPO提高目标任务输出 | [P] 作者报告少样本分类/解释收益；[S] chosen/rejected往往连最终类别token也不同，DPO可能主要强化标签而非忠实解释；HateCOT前置数据/计算不能计作零成本。 |
| **P027 ExPO-HM**，[ICLR 2026 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html) | 细粒度标签手册SFT-PM→GRPO课程学习；把给定模型解释之后的答案条件熵(CDE)纳入奖励 | [P] 报告Hateful Meme分类、解释与校准效果；[S] 当前公开奖励代码在熵中间区间与论文公式存在差异；低答案熵不等于解释语义真实，更不等于忠实因果作用。 |
| **P019 V-FLUTE**，NAACL 2025 Main，CCF-B | 训练标签+解释生成的自回归token CE，不是独立DPO或忠实性损失 | [P] 作者特定benchmark的解释相似度与人评；[O] 不保证内部推理真用到解释。 |
| **P035 EmoBi**，ACL 2025 Main，CCF-A | 多轮提示中的LLM重判/所谓Verification | [S] 自我重判无独立标注/事实检查器，不能把它当作可信“验证”算法。 |

**不可等同**：标签正确、解释流畅、解释参考文本相似、对模型答案一致、回答分布低熵、真正作为判决依据的忠实解释。这些是不同的评价命题。严谨的机制审计至少需要label-only vs explanation+label的等token训练，chosen/rejected只改理由不改类别的偏好对、随机解释对照、解释删除/置换，以及对独立人审意义标注的评价。[H]

证据：[P030](../../01_literature/cards/P030_SMARTER.md)、[P027](../../01_literature/cards/P027_ExPO-HM.md)、[P019](../../01_literature/cards/P019_V-FLUTE.md)、[P035](../../01_literature/cards/P035_EmoBi.md)。

## 6. M6｜多模态隐含风险：输入感知、归因与安全响应分开优化

### 6.1 基准与诊断并不天然提出新训练器
- **P037 VLSBench**，[ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.405/)：定位Visual Safety Information Leakage，基于文字重写构造视觉必要性更强的风险评测，并测试现有SFT/DPO/PPO路线；**不是本文发明PPO/DPO**。基准正例侧为主，不能直接当平衡检测集。
- **R2A-027 MSSBench**，[ICLR 2025 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html)：视觉环境决定活动是否合适，多agent推理属于prompt-level拆分而非新SFT/RL训练。行为Judge与风险GT必须分开。
- **R2A-028 MOSSBench**，[ICLR 2025 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html)：安全请求过度拒答；ARR是输出行为，不等于危险分类的FPR，也不等于回答正确性。
- **R2A-029 MMSafeAware**，[ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.832/)：输入安全二分类，提供双侧错误诊断；VCD/VRTuning为既有技术应用；总accuracy可能被全判Unsafe的多数类策略误导。
- **P038 VLSU**，[ICLR 2026 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)：image/text/joint三级风险标签及17种设计组合；[S] 公开CSV8159 vs论文8187，含image not_sure，严格S-S-U公开记录35条；是**test-only**，不能训练后称在原官方测试协议上独立评测成功。

### 6.2 真正的方法训练路线
| 代表及出版情况 | 方法更新在哪里 | 有什么支持、什么没有证明 |
|---|---|---|
| **P034 CrossGuard**，[ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1178/) | ImpForge用强化学习生成隐含联合恶意输入，然后训练识别输入恶意意图的Guard | [P] 作者报告跨显隐攻击及正常输入的防护收益。[S/O] 作者生成奖励源码、ASR评价协议、训练比例及标签规范存在既有静态审计疑点；输入Guard F1/ASR不能替代安全回答的帮助性。 |
| **P039 ThinkingGuard**，ACM MM 2026为CCF-A刊会，**作者录用/DOI线索已见，但正式出版页/Track未独立核** | TriggerBench安全/危险配对→SA-MCTS搜索逐步风险归因→Trajectory及关键Step-DPO | [P：作者稿] 移除Step-DPO后报告风险指标下降；[S/O] 视觉配对并非已确认只改变触发元素；搜索Judge看到特权触发答案，训练/奖励源码不完整。不能写“正式已出版的CCF-A主会研究”。 |
| **P040 Meerkat-VL**，[ICML 2026 Main，CCF-A](https://proceedings.mlr.press/v306/zhou26ae.html) | Cold-start SFT训练分析/回答格式，自验证NPSV/DPCA构建感知-回答一致性奖励，实际用GRPO更新模型 | [P] 作者报告安全和帮助性提升；[S] 当前公开训练评分可使用金标风险解释文字，并非无外部信息地独立再看图；代码/README奖励系数有差异。 |

**学术分界**：CrossGuard主要针对**输入识别**，ThinkingGuard偏**触发元素归因及检测训练**，Meerkat-VL主要是**安全且有帮助的模型输出**。对它们不能将输入危险F1、危险回答率、拒答率、审判器给的safe rate、helpfulness合为一个数字。[P/H]

证据：[B4a跨论文综合](../R2_synthesis/B4a_Cross_Paper_Synthesis.md)、[P034](../../01_literature/cards/P034_CrossGuard.md)、[P037](../../01_literature/cards/P037_VLSBench.md)、[P038](../../01_literature/cards/P038_VLSU.md)、[P039](../../01_literature/cards/P039_ThinkingGuard.md)、[P040](../../01_literature/cards/P040_MeerkatVL.md)。

## 7. 2025–2026技术趋势：可说什么，不能说什么

| 趋势 | 已有直接先例与CCF等级 | 研究事实[P] | 不能延伸的机制断言[H/O] |
|---|---|---|---|
| 语用条件推断变为可测任务 | P020 ACL2025 A；DRInQ ACL2026 A；VAGUE ICCV2025 A | 条件先验/换语境候选判别已具体化 | 真实心理意图被完全还原 |
| 静态参数外知识 | FETCH! ACL2025 A；SeTox ACL2026 A | 近邻/外部检索对对应任务有用 | 时间外未见编码义已被可靠解决 |
| 细粒度修辞、多任务训练 | MultiMM ACL2025 A；M3UCD AAAI2026 A；DOSE ACL2026 A | 不再只给一个修辞二元类别 | 情绪辅助有因果贡献、专家消除了所有梯度冲突 |
| 模态捷径控制 | VLSBench ACL2025 A；MCIB AAAI2026 A | 有视觉安全泄漏和反讽捷径研究 | “首次发现多模态shortcut” |
| 解释偏好和不确定性 | SMARTER ACL2026 A；ExPO-HM ICLR2026 A | 分类/解释/校准在作者数据协议有收益 | 低熵与自洽解释必然忠实 |
| 反事实安全归因与自验证 | CrossGuard ACL2026 A；ThinkingGuard作者稿；Meerkat-VL ICML2026 A | 从输入Guard延伸到关键风险与输出优化 | 配对图必然单因素、SelfVerification必然独立事实核查 |
| 风险检测双侧指标 | MSSBench/MOSSBench ICLR2025 A；VLSU ICLR2026 A | 危险遗漏和正常输入误判都需评价 | 只提高拒答率就表示更安全 |

## 8. 直接竞争/查重新颖性清单（不是新Gap证明）

| **不应单独声称新颖的创意** | 至少要比较的先例 | 若再研究，最低限度应证明什么[H] |
|---|---|---|
| 用对比学习改善隐含仇恨/委婉语 | ImpCon（COLING2022 B）、FA-Net（AAAI2024 A） | 新的正负对语义正确性、已知类别域迁移严格划分 |
| RL调模块集成权重 | RV-HATE（ACL2026 A） | 独立valid/test+同预算非RL权重搜索 |
| “因果”去显隐风格 | CADET（WWW2026 A） | 与真实不变性干预及标签测量相对应 |
| LLM发现/解码Dog Whistle | Silent Signals（ACL2024 A）、FETCH!（ACL2025 A） | 明确type发现、instance消歧、严格真实时间外新义 |
| 检索增强新兴词毒性 | SeTox（ACL2026 A） | 证据可信度/时间污染控制和新失败机制 |
| 情绪促进隐喻/夸张 | MultiMM、EmoBi（ACL2025 A） | 去掉gold情绪、同训练预算、辅助变量打乱 |
| 图文多任务修辞理解 | MGMCF（AAAI2025 A）、M3UCD（AAAI2026 A）、DOSE（ACL2026 A） | 真正的概念解释、图文依赖和任务迁移 |
| 抑制多模态反讽捷径 | MCIB（AAAI2026 A，尚待R3-B精读） | 对真实跨域/反事实有不同的可证伪机制 |
| 解释→检测、偏好优化 | SMARTER（ACL2026 A）、ExPO-HM（ICLR2026 A） | 标签与解释贡献分开，验证解释忠实性 |
| 图文联合隐含风险Guard | CrossGuard（ACL2026 A）、VLSU（ICLR2026 A） | 额外且可信的联合语义/风险监督和双侧测量 |
| 反事实触发+步骤DPO | ThinkingGuard（ACM MM作者录用稿，正式Track待核） | 超出既有TriggerBench与Step-DPO的独立机制 |
| 自验证+GRPO安全回答 | Meerkat-VL（ICML2026 A） | 无特权真值的信息约束和感知-行为独立控制 |

这些只是**重复宣称预警**，不能从“某控制缺失”自动推导“已找到CCF-A创新空白”。

## 9. 评价、Ground Truth与可靠性审计要求

**任务必须写作 Task=(X,Y,G,E)**：X是原始输入及全部可用辅助先验，Y是输出对象，G是人审/机器生成/词典/偏好等金标和标注协议，E是指标和分母。不同论文Accuracy/F1不能在共同表中无条件横向排名。

- **语义和危害**：隐喻识别GT不等于“非人化仇恨”GT；编码词词典条目不等于这句话用了编码义；模型能给出自然语言解释，不等于解释被独立人审核实。AUTALIC（ACL2025 Main A）目前由R3-B定向补读，不能在此假装其全文已经审完。
- **输入信息预算**：原文配文、OCR、测试gold sentiment/源目标域、给定词典定义、Oracle caption、外部搜索结果、前置风险说明必须分别登记；信息不同，性能并非公平可比。
- **多模态因果**：同一模型joint/text-only/image-only、合理单因素反事实配对和经人审翻转标签是不同证据；只做shuffled images不能沿用原标签宣称因果检测正确。M3UCD人工“Complementary”不等于模型确实联合推理。
- **指标切分**：T1检测F1、T2开放解释质量、T3多选准确率、T4风险分类Balanced Accuracy、T5组合条件翻转、T6拒答/安全/有用性均有独立分母。MMSafeAware的全判Unsafe已有66.67%原始accuracy但Balanced Accuracy仅50%，是不能只报总分的直观例子。
- **代码证据**：[S] 见RV-HATE公开test寻权、MultiMM测试gold情感、MGMCF论文/代码损失差异、DOSE小子集选项捷径、VLSU数据版本、Meerkat-VL特权评分等；**只可归于审计的仓库版本，不可据此自动断言正式实验无效**。
- **可复现性和资源**：公开论文、代码页面、数据包可达、正确split、已复现训练是不同状态；本项目还未跑端到端复现。后续方法型实验坚持现成公开数据、单卡16–20GiB优先、≤6小时kill test、不依赖付费API；这不限制综述引用计算量大的学术研究。

## 10. 与R3-A1衔接及R3-A3移交

**写作建议**：主体章节按“问题和预测对象”而非技术代际组织；方法史用横向机制矩阵穿插：
1. 表达识别与解释：词典/规则/RSA→PLM/对比→定义条件LLM/检索；
2. 隐晦有害评价：分类/对比与跨域→解释、动态词义、偏好训练；
3. 多模态非字面理解：融合作为基线→对象/概念/多任务→捷径抑制；
4. 联合风险与安全回应：输入风险标签→风险触发归因→回答策略/帮助性，显式区分漏检、误报和误拒；
5. 贯穿全文的方法证据：GT目标、特权信息、同预算、反事实、解释忠实性、发布版本。

**阶段决策**：R3-A2审阅稿可以提交用户学术审阅；R3-A3叙事和R3-A4证据终审尚未完成。R2-C认为还需在R3-B分别定向精读AUTALIC与MCIB以补语境有害标注分歧、多模态捷径的直接证据；**不需要重启全量检索**。

### 关键可追溯来源
- [R1分类框架](../R1_taxonomy/R1_Working_Framework_DRAFT.md)
- [R2-C跨领域综合](../R2_synthesis/R2C_Cross_Domain_Synthesis.md)
- [R2-C覆盖/证据审计](../R2_synthesis/R2C_Coverage_and_Evidence_Audit.md)
- [R2-A候选账本](../R2_literature_extension/R2A_Candidate_Ledger.md)
- [R2-B1语用综合](../R2_literature_extension/B1_reading/R2B_B1_Synthesis_DRAFT.md)
- [R2-B2a编码综合](../R2_literature_extension/B2a_reading/R2B_B2a_Synthesis.md)
- [R2-B2b语义—危害综合](../R2_literature_extension/B2b_reading/R2B_B2b_Synthesis.md)
- [R2-B3a多模态多任务](../R2_synthesis/B3a_Cross_Paper_Synthesis.md)
- [R2-B4a多模态安全](../R2_synthesis/B4a_Cross_Paper_Synthesis.md)
- [R2元数据及证据冲突](../R2_registry/Metadata_and_Evidence_Conflicts.md)

> 当前文件为审阅分支上的新增草稿，未覆盖R0/R1/R2原稿，也未提前生成R3-A3/A4成果。
