# R6-A2｜第4–6章正式逐章学术审稿（编码语言／隐晦有害／多模态语义）

> **状态：R6-A2 REVIEW COMPLETE（仅Ch4–6），2026-11-09；不改R5-C正文，不合并PR**。   
> R5-C源稿PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)；固定HEAD `c04d6a23e864923acd64c192c8b05dc597c2bb90`。阅读原文 [L168–329](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L168-L329)、[tables/T3_Coded_Language.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T3_Coded_Language.md)、[tables/T4_Contextual_Harm.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T4_Contextual_Harm.md)、[tables/T5_Multimodal_Meaning.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T5_Multimodal_Meaning.md)，并对照main中R2-B/B2a/B2b/B3a及R3-B精读、R5-E核证门槛、R6-A0/A1。   
> **证据**：F官方正式出版元数据；P作者报告的正式论文实验、分布和消融；S当前/历史公开源码或数据静态观察（必须固定版本）；H本轮审稿综合；O未闭合。**摘要级可确认存在，但不能从摘要强证因果或逐项性能。**  
> **本轮对外定点核验**：直接打开并检视[CodedLang ACL2026 Main CCF-A PDF](https://aclanthology.org/2026.acl-long.426.pdf)、[SeTox ACL2026 Main CCF-A PDF](https://aclanthology.org/2026.acl-long.1602.pdf)、[AUTALIC ACL2025 Main CCF-A PDF](https://aclanthology.org/2025.acl-long.1022.pdf)首页截图与相关文本；[DOSE ACL2026 Main CCF-A](https://aclanthology.org/2026.acl-long.319.pdf)正式PDF文本及[ACL正式出版页](https://aclanthology.org/2026.acl-long.319/)（PDF截图接口cache miss，不能声称其视觉页审成功）；[MMSD3.0 CVPR2026 CCF-A正式出版页](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_MMSD3.0_A_Multi-Image_Benchmark_for_Real-World_Multimodal_Sarcasm_Detection_CVPR_2026_paper.html)的公开摘要/书目及作者仓库说明，**尚未完成全文表格核对**。其余论文的具体机制/代码据已定稿的项目卡，不谎称本轮重新跑源码或训练。

## 0. 总体裁决

**R6-A2：CONDITIONAL PASS / TARGETED MAJOR REVISION。** 研究材料多已正确避免“检测分数=理解了意义=因果机制成立”的错误，本轮没有发现足以推倒第4–6章的理论性反例，也没有发现可以据此指责论文作者正式实验违规的证据。修订重点在 **可复核S级实现断言（继承A0 P0）**、跨领域公平比较的**正向条件性结论**、以及一项已确认的跨表事实错误。

| 章 | 裁决 | 优点 | 投稿级剩余缺口 |
|---|---|---|---|
| 第4章 编码语言、狗哨、动态义 | **PASS / focused revision** | 把type发现、token消歧、固定候选解码、检索增强风险判断严格分成不同契约；已避免把词典留出冒充时间外全新词发现。 | 数量与人工质量层级尚不够可审；FETCH! 评价口径和FA-Net transductive先验需放在对照表，不只散见正文。 |
| 第5章 语境化隐晦有害 | **PASS WITH MODERATE REVISION** | 明确“隐喻GT≠非人化GT”、AUTALIC质性语境证据≠量化增益、ToxiGen代理标签≠逐句隐义、解释与分类需分开。 | DPO解释与标签偏好混杂、少数类误判/弃权折叠、跨风格类先验漂移与PPO调参的信息访问，需要更明确的读者可执行比较。 |
| 第6章 多模态非字面意义 | **MAJOR TARGETED REVISION** | 方法家族分别落实到对象交互、共享LoRA、正交专家、信息瓶颈；已识别gold情绪、源/目标概念、OCR和外部先验问题。 | **表5 DOSE原始模态事实错误**；多任务样本分母和图文支配类型未入正向比较；代码S级细节缺永久版本；MCIB独立CIB收益不成立；多图部分过薄。 |

**本轮问题清单**：**A2-01～A2-18共18项，含1项“继承A0-02的P0”、15项P1、2项P2**。这不是新造18项全球阻断项：A2-16是A0-02的**具体整改门槛**，其它若与A0重叠应在最终A4按source claim去重。由于原稿已有较多正确审慎表述，部分P1是“应补机制/正面证据及表格”而非对原句进行错误指控。

## 1. 第4章｜编码义、动态词义及跨域的技术真相

### 1.1 已经写对的核心分类与方法

- [L176–180](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L176-L180)中 **CodedLang（ACL2026 Main，CCF-A）**：7,744条中文Google Maps评论、900条span编码正例、七类编码策略；Table2/3/4分别为存在性、策略类别、星级，**星级不是义项GT**。已对照[ACL正式PDF](https://aclanthology.org/2026.acl-long.426.pdf)首页/摘要及[P023_CodedLang](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P023_CodedLang.md)；选样富集不应当成平台自然正率。
- [L182–186](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L182-L186)中 **Silent Signals（ACL2024 Main，CCF-A）**：提供已知词项+编码定义做具体上下文的用义消歧，GPT式一致性筛出语料；论文16,550条模型筛选主集 vs上游所审发布README16,258行的版本差已在原稿说明（非已确立的数据错误）。
- [L190–194](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L190-L194)中 **FETCH!（ACL2025 Main，CCF-A）**：20%词典种子→同一既存参考词典其余约80%词项回收；EarShot为检索+候选提取/过滤，不是完全未知未来词的时间外发现。
- [L198–202](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L198-L202)中 **FA-Net（AAAI2024 Technical，CCF-A）**：源域显性词遮蔽监督+目标域无标签语料参与训练、同类和跨域对比、目标域预测熵；固定类别Acc@k而非开放释义或未见词项发现。
- [L206–210](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L206-L210)中 **SeTox（ACL2026 Main，CCF-A）**：搜索作为推理时可用证据，监督工具轨迹用于SFT，终点为新词毒性标签T4；`model-unknown`按基础模型能否解释词义定义，不是时间新颖性。正式PDF §5.2给624新词测试(490 unsafe/134 safe)、319 known/305 unknown，并定义DR/KDR/UDR/Acc/F1；当前正文正确避免把毒性分类成绩当作意义恢复。

**可保留的正向条件性综合（H）**：`字典定义已知`使Silent Signals实例消歧更可控；`已知类别+目标域无标签语境`使FA-Net跨语域配对学习可操作；`20%已知种子+可检索语料`使FETCH候选词项回收可测；`推理时可搜索`使SeTox在已定义的分类协议中获取动态背景。这是**先验预算与可验证输出相互制约**的规律，不是跨论文直接因果性能排名。现有[L202–214](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L202-L214)已隐含该结构，应将条件和反例显式制成表3第六列。

### 1.2 第4章的四项P1

**A2-01｜P1｜Silent Signals的大主集/小人工集、precision与覆盖率仍需拆清楚。**  
- 原句：§4.2 [L184–186](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L184-L186)“大规模模型筛选的正例主集”“不能把其中一次Precision直接当整个自动标注流程正确率”，总体措辞正确。
- 证据：[B2a-R2B_B2a_01_Silent_Signals](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_01_Silent_Signals.md) §3/5：论文GPT-4筛出**16,550**是模型一致判阳，不是全逐例人审；抽取400正例人审得precision **85.3%**，扩展可接受编码义口径为**89.4%**；论文小人工消歧集和主集生成流程的采样前提不同。当前发布README 16,258静态记录差292（尚未下载全量核行）。
- 修订：表3新增 `大集标签来源/人工质检子集/覆盖率(未确认)` 与版本列；如使用85.3%/89.4%须标“抽样正例人工审查Precision而非整个候选挖掘召回率”；不计算大集未审预测精度或将版本差解释为有意删错。

**A2-02｜P1｜FETCH!词项回收F0.5的统计对象差异和选型预算缺位。**  
- 原句：§4.3 [L190–194](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L190-L194)“指标包括词项Precision、发现比例、F0.5”，已正确承认20/80是词典留出。
- 证据：[B2a-R2B_B2a_02_FETCH](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_02_FETCH.md) §3–5：正例是词典词条正则命中，实际普通义无法由regex识别；precision按输出候选项计数、discovered recall偏词根type去重，**并非完全相同的计数单位**；多个数据集上的最佳模型/过滤器/阈值可能不同，不是无调参跨语料部署。
- 修订：在表3标注 `GT=词典匹配的type回收而非instance人工验证`、`P/DPR分母与类别`、`最优配置按场景挑选`，主文只须补2句，不添加未经证实的召回结论。

**A2-03｜P1｜FA-Net应强调目标域训练时可见以及伪正例质量未测。**  
- 原句：§4.4 [L198–202](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L198-L202)“相似度选择跨域伪正对”“目标域无标签文本参与适应”均准确。
- 证据：[B2a-R2B_B2a_03_Hidden_Chasm_FA_Net](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_03_Hidden_Chasm_FA_Net.md) §2–5：Drug/Weapon/Sexuality 固定**33/9/12**候选目标类，源域有label，目标域未标数据直接参与HC/EM优化；按发布设定**可能含transductive**成分，目标测试词位置已知；未独立人工核每对相似伪正例语义一致。
- 修订：在对比表明记固定类别数/遮蔽目标位置/目标域无标签训练访问，新增“同等目标域无标签预算/无目标文本的inductive对照未证”，伪正例错配只列H/O，不写已发现比例。

**A2-04｜P1｜SeTox应把“新词检测”和“毒性判定”的指标分母真正拆开。**  
- 原句：§4.5 [L206–210](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L206-L210)“检索证据”“model-unknown非训练前未见词”准确，但仅报无搜索对照存在而缺指标定义。
- 证据：[SeTox官方PDF §5.2](https://aclanthology.org/2026.acl-long.1602.pdf)与[B2b-R2B_B2b_01_SeTox](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_01_SeTox.md)：新词测试**624**（490 unsafe/134 safe），model-known 319/unknown 305；DR/KDR/UDR是**unsafe子集的检测率**，与含safe样本的Acc及双类F1不同；选择unknown依据同一指定基础模型解释能力+人工评议，而非严格未来词。
- 修订：用一个脚注或小表列 `unsafe新词DR/KDR/UDR`、`全样本Acc/F1`、`在线搜索快照/训练词项交叉未核`；不要把搜索消融当作词义忠实或开放世界新颖性的证明。

## 2. 第5章｜隐式仇恨、解释监督与规范真值

### 2.1 审稿认可的有效学术区分

1. [L224–228](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L224-L228) **ToxiGen（ACL2022 Main，CCF-A）**：较大规模对抗式自动生成和外测AUC结果支持“给检测器构造压力测试”，但其词表缺失定义的implicit不是独立语用意义标签。**AUTALIC（ACL2025 Main，CCF-A）**则提供真实社群上下文/标注分歧，两者并非“越来越真实、因果更好”的单轴竞争。
2. [L240–246](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L240-L246) **When People are Floods（ACL2025 Main，CCF-A）**只有源域隐喻人审GT，不存在逐句单列非人化/仇恨真值；**Sheep’s Skin（ACL2025 Main，CCF-A）**对显性仇恨进行合成隐喻改写并人工核意图保持，但模型看到的与人工审核的输入条件不同、负侧不足。原稿正确地没有把隐喻识别AUC混为仇恨检测AUC。
3. [L248–254](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L248-L254) AUTALIC九名接受培训的高年级本科研究志愿者、每句三人、Fleiss `κ=0.25`、原三标签`{-1,0,1}`折叠为二分类、2,400总句与242+2160=2402不一致已谨慎描述。已用[ACL正式PDF](https://aclanthology.org/2025.acl-long.1022.pdf)核首页及相关正文，不对尚未打开的原CSV推断真正类别计数；也没有把质性上下文示例写成同模型删语境提升。
4. [L258–262](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L258-L262) 对跨数据集标签政策不一致、CADET“正交=因果去混杂”的歧义、RV-HATE同域分数据集训练及静态PPO调权风险均有合理防线。

### 2.2 第5章五项P1

**A2-05｜P1｜ToxiGen的“对抗性”应与标签忠实度形成正负双侧综合。**  
- 位置：§5.1 [L224–228](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L224-L228)；原稿已有对生成提示代理的限定，但没有用**主实验提供的反例**支撑“压力增大可能损害标签一致性”。
- 证据：[P001_ToxiGen](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P001_ToxiGen.md) §4/6，274,186生成例，13类目标群体；约98.2%缺显性词表只是词面代理；HumanVal 792、人审κ0.46；作者的ALICE配对审查里**更易误导检测器**，但有害提示生成内容与人工有害判断的吻合度下降（论文卡记40.3% vs常规top-k 67.7%，限定为相应小型配对验证）。
- 修订：增加明确的`难度/流畅度/有害标签忠实度`张力，说明不能把对既定分类器造成误判的成功率视为已构建可信隐晦仇恨样本；不把这些小子集百分比外推到全部274k。

**A2-06｜P1｜SMARTER的DPO偏好“正确标签”与“好解释”没有独立消融。**  
- 位置：§5.2 [L234–238](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L234-L238)“生成正误回答与解释；用DPO偏好标签—解释组合”。
- 证据：[P030_SMARTER](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P030_SMARTER.md)（[ACL2026 Main正式论文](https://aclanthology.org/2026.acl-long.1584/)）：在每个已知gold训练标签条件下，按类别生成chosen和rejected（正确/错误**标签token可直接不同**），并不是人类逐对验证解释质量；先做HateCOT解释SFT，低资源只限**目标任务新增标注**；Implicit Hate内部6分类与HateXplain/Latent Hate三分类不同。作者NLI一致性分数不等于faithfulness。
- 修订：正面写DPO相对SFT在具体K设置下的分类增益，同时增`标签本身即可分chosen/rejected、label-only DPO对照缺失`；三任务label space和辅助监督预算在表4附近明确，不改写为“低成本就学会真实隐含语义”。

**A2-07｜P1｜RV-HATE的PPO独立贡献须与四模型整体增益拆开、公开脚本风险须给固定证据。**  
- 位置：§5.2 [L236–238](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L236-L238)、§5.5 [L258–262](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L258-L262)。
- 证据：[P029_RV-HATE](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P029_RV-HATE.md) ([ACL2026 Main CCF-A正式论文](https://aclanthology.org/2026.acl-long.2104/))：Table2四模型**等权83.78** vs PPO权重**84.47**平均macro-F1，**差0.69个百分点**；模型分类器冻结、PPO是在4权重的simplex中优化，并非对每条文本动态选择模块。所查公开`ppo_eval.py`用`test_data`建PPO环境并在同一`test_data`评价（S，代码版本与发表实际路线O）。
- 修订：写清0.69pp对等权而不是把整体RV-HATE相对弱基线的提升全部归PPO；给S级source permanent commit/行、输入split，以及“不能据现态推断正式论文结果无效”；若无法给可引用版本，转为待复核疑点。

**A2-08｜P1｜CADET的跨风格结果不能掩盖政策、类别先验及目标测试作验证的条件。**  
- 位置：§5.5 [L260–262](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L260-L262)。
- 证据：[P033_CADET](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P033_CADET.md)（WWW2026 Main，CCF-A）：部分风格切分不仅改变显/隐风格，也大幅改变正类比例；上游静态代码审计有目标`test`作为`valid`、部分风格标签由自动毒性阈值代理、反事实程序与论文不同等信号。**这些都是所审发布代码层证据，不是对作者正式实验作弊的判决。**
- 修订：除正交无法代表真实因果因素外，应将`源/目标标签定义、原始正类比例、valid是否独立、目标类是否训练前可见`列入迁移条件；若主文继续写具体代码行为必须给commit/permalink和版本限定。

**A2-09｜P1｜AUTALIC二分类协议及使用约束应进入表4而非只留正文。**  
- 位置：§5.4 [L250–254](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L250-L254)、[tables/T4_Contextual_Harm.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T4_Contextual_Harm.md)。
- 证据：[R3B-R3B_01_AUTALIC_FINAL](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_01_AUTALIC_FINAL.md)、[R3B-R3B_01_AUTALIC_Three_Issue_Audit](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_01_AUTALIC_Three_Issue_Audit.md)：原 `-1`表示不相关/上下文不足，先折叠到0再三人众数；单人标注数 595(-1)+5582(0)+1023(1)=7200；κ=0.25；final positive与negative加和矛盾2条；自动审核系统用途需核许可。作者没有同样本有/无上下文判别实验。
- 修订：表4增加`原始类别→评测类别`和`人工票/多数票`口径，以及`许可范围`脚注；分析“把不可判/不相关折叠入非歧视”对少数类召回/误报与决策弃权的含义，**只说潜在指标偏差方向不定**，不可编造实际翻转数。

## 3. 第6章｜输入条件、融合与语义必要性

### 3.1 已有机制内容的准确之处

| 方法与正式刊会 | 模型实际优化/预测对象 | 正面可证的结果 | 不可归因的效应 |
|---|---|---|---|
| **MultiMM/SEMD**，ACL2025 Main（CCF-A） | 中英广告图文，隐喻/源目标/情绪标注；SEMD预测隐喻类别但所查测试代码额外读gold情绪 | 作者Table2 英文/中文隐喻F1 **80.16/77.79** | 不是纯原始图文下情绪自预测或跨文化独立因果影响 |
| **M3UCD/MCLF**，AAAI2026 Technical（CCF-A） | 15,345图文，约12类基础人工属性+多个预测任务；共享LoRA多任务训练 | 同一Qwen2.5-VL-7B源/目标模态macro-F1有提升 | 同一配置Emotion **48.60→46.08**、Metaphor Detection **79.68→78.50**负迁移；任务标签不等于预测解释正确 |
| **MGMCF**，AAAI2025 Technical（CCF-A） | 图文、对象线索、**源/目标概念辅助文本**，四类分类任务，Global–Local与Dual-Semantic | 作者报告去对象、GL、DG性能回落 | 辅助源目标字段来自何处/和基线公平对齐未闭，去分支不等于模态因果必要；对比损失本意与源码路径不完全一致 |
| **DOSE**，ACL2026 Main（CCF-A） | **图文**新闻/文章、五任务MCQ；共享/私有低秩专家+路由+投影正交 | Qwen3-VL-8B 1%训练设定五任务等权Acc **78.90** vs LoRA **77.70**；整体去正交下降 | 仅投影正交非任务梯度消冲突，Intent**74.14<74.45** LoRA；去正交Target反高于完整 |
| **V-FLUTE**，NAACL2025 Main（该会议CCF-B） | 图文视觉蕴含二分类+参考自然语言解释；白图重新训练 | 作者Table4模型联合数据F1@0 **74.91**，白图有降分现象 | F1@0不等于faithfulness；解释阈值校准与图像必要性受来源/统计捷径影响 |
| **MCIB**，AAAI2026 Technical（CCF-A） | 文/音/视反讽二分类，三配对条件瓶颈及辅助预测约束 | 作者MUStARD++R **weighted-F1 75.64**；去fine-grained→71.19、Transformer→MLP→74.32 | 未做等结构独立`no KL/no conditional`控制；模型可以绕过瓶颈读取原文本；公开代码广播风险不等于正式表格失效 |
| **MMSD3.0/CIRM**，CVPR2026 Main（CCF-A） | 多图+文字反讽，跨图桥接与相关性融合 | 官方摘要/正式出版页**确证该任务、基准及所提模型存在** | 本项目只完成摘要级核对，不引未经核的样本具体分布、表格数值、模块独立消融 |

### 3.2 第6章六项P1 + 继承P0

**A2-10｜P1｜M3UCD与DOSE的GT“模态贡献”需对接可观察的去模态证据。**  
- 位置：§6.2 [L284–286](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L284-L286)、§6.3 [L292–296](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L292-L296)。
- 证据：[B3a-R2B_B3a_01_M3UCD](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_01_M3UCD.md)记录M3UCD **Complementary 58.36%** 是人工标注的来源模态分类，非同模型分别去图去文的配对表现；[B3a-R2B_B3a_03_DOSE](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_03_DOSE.md)及[DOSE正式PDF](https://aclanthology.org/2026.acl-long.319.pdf) Appendix/Table6：反讽正例中人工“Text-dominant 61.9%、Equal 22.5%、Image-dominant 15.6%”，且部分机制本来单模态占主导。DOSE与M3UCD的标注概念不同，两个百分比**不得作为同一比例相减**。
- 修订：表5新增`标注的模态贡献类别 vs 同模型(IT/I/T)行为指标`列；至少引一组M3UCD和DOSE类别比例，说明“人工认为Complementary ≠ 模型依赖两个模态”，并指出无反事实重判不得宣布严格组合因果理解。

**A2-11｜P1｜MultiMM/MGMCF的特权辅助字段是第6章最强的公平性比较问题。**  
- 位置：§6.4 [L298–304](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L298-L304)、表5。
- 证据：[P003_MultiMM](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P003_MultiMM.md)已静态检查`code_metaphor/data_utils.py` 测试时将人工情绪列写成自然语言senti输入；论文表2、表3同名SEMD结果口径不同。[B3a-R2B_B3a_02_MGMCF](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_02_MGMCF.md)显示论文直接定义输入`(I,T,T_s,T_a)`、源码`loaddata.py`的训练/测试都读源目标特征；但该预计算pkl到底是gold、模型预测还是外部元数据**O**，不能直接定性“正式测试泄漏gold”；其Dual-Semantic源码传参还存在`text_meta`代替跨图文负对的异议。原稿措辞已谨慎，缺可复查的同条件对比产品。
- 修订：表5将一列拆成`X_raw`、`X_test_aux(oracle/model-predicted/external)`、`Y`、`baseline input parity`，明确从论文可证输入与源代码静态观察分别作P/S；不报告未经核的“纯图文下仍有80.16/77.79”。

**A2-12｜P1（确定事实错误）｜表5把DOSE的模态误写成文本/音频/视频。**  
- 位置：[tables/T5_Multimodal_Meaning.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T5_Multimodal_Meaning.md)：**“DOSE …… 文/音/视；反讽多目标”**，与正文§6.3 [L294–296](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L294-L296)“新闻图文”矛盾。
- 证据：[DOSE ACL2026 Main（CCF-A）正式出版页](https://aclanthology.org/2026.acl-long.319/)和[正式PDF](https://aclanthology.org/2026.acl-long.319.pdf)反复使用**paired image-text article**；[B3a-R2B_B3a_03_DOSE](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_03_DOSE.md)确认来自DocMSU-PLUS图文、五个主任务而代码默认含第六个dominant-modality变体。音视频是另一个**MCIB**论文的真实输入。
- **明确修订**：表5中DOSE行改为“**图像＋文章文本（新闻图文）；反讽检测/机制/描述MCQ/对象/意图**”，保留代码5 vs 6任务的版本说明。不得仅在脚注掩盖模态事实错写。

**A2-13｜P1｜MCIB的独立CIB效果仍缺受控消融，需增强正向机制解释及其限制。**  
- 位置：§6.5 [L310–312](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L310-L312)。
- 证据：[R3B-R3B_02_MCIB_FINAL](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_02_MCIB_FINAL.md)、[R3B-R3B_02_MCIB_CIB_Attribution_Audit](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_02_MCIB_CIB_Attribution_Audit.md)：主文Table2去细粒度75.64→71.19，Transformer→MLP至74.32，仅是结构替代；无同结构`KL=0`、`conditional prediction=0`、双去除的2×2对照；理论主文条件互信息下界、扩展附录和公开MSE+KL的统计目标不同。当前公开Transformer路径MSE[B,1]对label[B]有[B,B]广播风险，分类器残差引入未直接受瓶颈KL约束的原文本。项目先前小张量测试并非模型训练。
- 修订：按`理论目标 → 实际代理损失 → 所报道的正面结构消融 → 未被识别的CIB独立效应 → 公开版本异议`五步说明；如果保留具体源码计算，附固定commit/行/脚本入口；“去捷径”只作为作者动机与待检验机制，不写成本项目证明其无效或论文伪造。

**A2-14｜P1｜V-FLUTE统计来源/解释校准与图像有用性，应增加一项正负对照。**  
- 位置：§6.2 [L282–282](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L282-L282)及§6.5 [L308–308](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L308-L308)。
- 证据：[P019_V-FLUTE](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P019_V-FLUTE.md)（NAACL2025 Main，会议CCF-B）正式论文Table1 NYCartoons **651例全为Entailment**，不同来源不同E/C构造；Table4白图训练`VF-Image F1@0=64.77` vs 实图`VF 72.78`，支持图像对统计分类有帮助、也显示文本/来源有可预测线索；`F1@53`阈值从test抽样人评子集校准，不是独立valid决定；Appendix H GPT-4o few-shot表现可能超过正文最佳微调模型。
- 修订：在现有“白图改变分布”之后补`白图64.77的剩余分类能力`并指出来源/标签构造及阈值选择影响外推；不把白图差值当“真实图片语义必要性已证明”，也不称解释相似度为忠实推理。

**A2-15｜P1｜§6.6对MMSD3.0仅作存在性论据，仍无法代表已出版的多图技术线。**  
- 位置：§6.6 [L318–322](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L318-L322)“目前仅有官方摘要级候选信息”。
- 证据：[CVPR2026 Main（CCF-A）出版页](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_MMSD3.0_A_Multi-Image_Benchmark_for_Real-World_Multimodal_Sarcasm_Detection_CVPR_2026_paper.html)显示正式页码**37885–37895**，摘要明确**MMSD3.0多图基准+CIRM跨图推理模型**、Dual-Stage Bridge与Relevance-Guided Fusion，以及跨MMSD/MMSD2.0/3.0评估；作者[公开仓库](https://github.com/ZHCMOONWIND/MMSD3.0)提供构建与代码信息。本轮**只核验正式页和摘要，不假装已核其表格/模块单独收益或源码运行**。
- 修订选项：A（**优先**）针对该已出版的CVPR CCF-A论文做一次定点全文核查，增加`跨图关系是什么、训练/测试输入分布、去图或关系干预、哪个模块独立起作用、数据是否真实2–4图及有无捷径`的1段；B 如果时间不足，将§6.6明确定位“展望/出版先例”，从主轴表5移到低证据级脚注或缩成2–3句。不要用摘要宣称CIRM在受控关系干预中获证成功。

**A2-16｜P0（继承A0-02，非新增全球P0）｜第5–6章的S级“代码发现”缺对外可复核证据链。**  
- 涉及：§5.2 [L236–236](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L236-L236) RV-HATE的test_data PPO；§5.5 [L260–260](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L260-L260) CADET的目标test用作验证；§6.4 [L300–304](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L300-L304) MultiMM与MGMCF测试辅助及损失；§6.5 [L312–312](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L312-L312) MCIB batch广播与残差。
- 已知归档：P029/P033/P003、B3a MGMCF、R3B MCIB中有各自静态观察；R5-E部分给MCIB文件blob SHA。**但本稿仅引发表论文key，普通读者无法从论文引用定位在所审源码哪个commit/文件/行复核**；对外证明缺失是稿件可审性问题，不等同已证明原作者违反协议。
- **投稿阻断门槛**：对每一条S级源码定论，公开`claim_id / repository+commit / blob+file#L / relevant function+input shape or split / execution checked? / whether paper table uses version? / scope limitation`。如无法取到可靠commit，主文降为“公开实现有待核对的协议风险”并将细节放审计附录/OPEN；绝不保留无源的严重指控。R6-A4按A0-02去重，**不能重复算新P0**。

### 3.3 两个P2精修

**A2-17｜P2｜“T5表”容易与本文T5联合风险任务混读。** §6.4 [L302–302](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L302-L302)末句“首先要在 T5 表中标明”；建议更正为“**表5（多模态非字面意义表）**”，避免读者误以为M3UCD概念预测属于T5联合安全标签。

**A2-18｜P2｜表4选文范围需标为“代表论文而非第5章完整方法清单”。** [tables/T4_Contextual_Harm.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T4_Contextual_Harm.md)只选Latent Hatred、ToxiGen、When People are Floods、Sheep’s Skin、AUTALIC，但正文§5.2/5.5还讨论ImpCon、SMARTER、RV-HATE、CADET。若表题仍叫“主要”GT，应在表注说明**按GT样本类型选代表，不涵盖全部方法**，或补一栏方法与辅助监督；不要让读者误以为另外几篇未被纳入章节证据。

## 4. 将第4–6章升级为高水平综述的三条“可证条件规律”（审稿H建议，非论文作者共同实验）

| 核心比较问题 | 证据两端（已读原论文） | 可写的**条件化正面判断** | 不能写的越界推断 |
|---|---|---|---|
| “未知编码”何时可计算？ | Silent定义条件消歧 vs FETCH已知词典留出 vs FA固定候选与target unlabeled vs SeTox搜索条件毒性 | **开放度由词典先验、测试候选集和外部证据是否可用决定**：强先验适合可评测的局部任务，减少先验需要新的词项/义项人工真值协议。 | 从不同F0.5、Acc@k、DR推断“某架构真的解决开放词义泛化”。 |
| 解释监督何时有用？ | ToxiGen构造代理标签 vs ImpCon已有implied statements vs SMARTER标签条件解释偏好 vs AUTALIC规范分歧 | **额外解释/语境标注提供特定任务监督**，可改善作者报告的分类或揭示歧义，但解释支持、标签正确与真实立场是三种GT；低资源收益必须计入先前监督。 | “向量对齐/生成解释/DPO”已独立因果证明模型理解仇恨隐义。 |
| 多模态融合在什么信息条件下才有说服力？ | MultiMM test-gold情绪线索、MGMCF源目标输入、M3UCD共享LoRA、DOSE正交专家、MCIB压缩目标、V-FLUTE白图 | **较细粒度结构与共享/隔离参数能在各自作者测试协议提高某些预测指标，同时产生负迁移和输入预算差异**；证明真实模态互补还要同模型同样本去模态、反事实重标GT与同预算。 | “网络含Cross-Attention/IB/MoE，所以已保证模型理解图文联合非字面机制并去掉捷径”。 |

这三条中第1、2条可直接回写§4.6与§5.6，第3条可回写§6.7并为A3第7章严格联合风险作桥梁，能为A0要求的“正向跨域机制综合”提供具体材料。但**跨论文比较本身属于H级推论，必须保留各原论文P级条件和反例**。

## 5. 修订优先级与验收Gate

1. **立即修正确定事实**：表5 DOSE“文/音/视”→“新闻图文”；§6.4“ T5 表 ”→“表5”；原稿正文不在本PR修改。
2. **先封住P0可复核性**：逐条绑定RV-HATE、CADET、MultiMM、MGMCF、MCIB公开commit及影响范围，若无源码凭据则降级或移入OPEN，不用`正式实验一定错误`措辞。
3. **补客观证据张力**：FETCH F0.5 type分母、SMARTER标签主导偏好、RV-HATE PPO对等权增量、AUTALIC弃权折叠、M3UCD/DOSE任务负迁移、MCIB瓶颈独立消融、V-FLUTE来源+阈值，精简成表格/脚注而非新长篇。
4. **信息预算与层级**：表3补词典/目标域/检索/人工质检，表4补标注折叠/监督，表5拆X_raw/test-gold/test-model-predicted/指标分母，并明确DOSE MCQ 5主任务 vs代码默认6变体。
5. **MMSD3.0**：只做一次正式全文目标式核查后写机制与消融，或保留摘要级且降低章节权重。**不能**声称本轮已经做完它的全文表格审查。
6. **A2收口**：不将R6-A2标记为全稿录用/已复现；R6-A3应从第7章审输入安全GT vs判断/输出行为，A4统一跨章去重A0遗留P0；R6-V另负责视觉/Bib出版工程。

### 来源与证据索引

- [R5-E 引文与claim gates](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/R5_Citation_and_Claim_Gates.md)
- [R5-E 高优证据专项](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/High_Priority_Evidence_Audit.md)
- [B2a 三篇编码语言精读](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/)
- [B2b SeTox/隐喻与危害精读](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/)
- [B3a 三篇多模态精读](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/)
- [MCIB条件瓶颈专项审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_02_MCIB_CIB_Attribution_Audit.md)
- [AUTALIC三项争议审计](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_01_AUTALIC_Three_Issue_Audit.md)
- [MMSD3.0官方CVPR2026记录](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_MMSD3.0_A_Multi-Image_Benchmark_for_Real-World_Multimodal_Sarcasm_Detection_CVPR_2026_paper.html)
- [DOSE ACL2026官方页](https://aclanthology.org/2026.acl-long.319/)

**终审边界**：A2审的是论文综述是否忠实、完整且推断适度，**不是对作者仓库实施运行复现**；新增一处表内输入模态事实错误可确定，部分机制归因/评测分母为需要补证的P1，公开源码严重风险保留固定版本与未证正式运行的防火墙。
