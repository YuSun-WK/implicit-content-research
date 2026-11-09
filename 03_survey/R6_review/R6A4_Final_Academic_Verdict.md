# R6-A4｜广义隐晦信息综述最终学术裁决（A0–A3归并终审）

> **裁决时间：2026-11-09；审核范围：学术内容，不含R6-V视觉/正式引文工程验收。**  
> **评审原稿**：R5-C PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)，固定commit `c04d6a23e864923acd64c192c8b05dc597c2bb90`，`03_survey/R5_full_draft/Survey_Full_Draft.md`；本轮未改原稿、表格、Bib或其他研究卡。  
> **先行意见**：R6-A0总体审稿、A1 Ch1–3、A2 Ch4–6、A3 Ch7–9；见本分支各阶段报告和[去重登记](R6A4_Deduplicated_Issue_Register.md)。  
> **证据分层**：F正式来源/出版事实；P作者报告的论文实验/GT/分母；S特定公开发布数据与代码的静态观察；H本综述或本次评审的跨论文推断；O未闭合。R6-A4没有重新执行论文模型、代码复现、全量图片下载或R6-V渲染，不升级此前审计为“已验证正式实验结果”。

## 1. 最终学术意见

**VERDICT = MAJOR REVISION；NOT SUBMISSION-READY。可以进入R6-Fix定向修订，不应直接作为高水平综述定稿/合并R5-C。**

本稿已形成值得保护的学术骨架：广义隐晦信息不是implicit hate的同义词；语用/修辞/编码/社会规范危害/跨模态风险不共享单一GT；T5是T4的联合模态条件性任务、严格S-S-U更窄；T6是相邻回应任务而不是T4内部风险判断必然输出。其主要价值在`Task=(X,Y,G,E)`+可见信息预算+监督来源+评测分母+不能过度归因的统一审计视角，而不是因为收录多个子领域就自动具有独创性。

### 审稿维度裁决

| 维度 | 审稿意见 | 具体基础 |
|---|---|---|
| 文章范围/读者 | **保留** | [R5-C L25–80](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L25-L80)、[R5-C L82–128](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L82-L128) 工作性边界与T1–T6层级已基本成立，适合计算机/AI/NLP读者。 |
| 章节组织/叙事 | **保留九章，定向改** | Ch3语用→Ch4动态编码→Ch5社会危害；Ch6非字面图文→Ch7安全，逻辑可讲，不需从零重写。 |
| 核心文献覆盖 | **有阻断缺口** | 已有ExPO-HM的ICLR 2026（CCF-A）正式研究及项目精读，原稿Ch7–8/46项Bib却缺少；否则“解释后检测/安全”的对照不完整。 |
| 论文机制深度 | **不均衡** | (RSA)²、FA-Net、MGMCF、DOSE、CrossGuard、ThinkingGuard有可识别方法细节；但Ch8/表7未从这些事实抽出具体跨域规律；多图§6.6浅且已自报摘要级。 |
| 正反实证与归因 | **主线审慎、需增强正面证据** | 多数地方没有将分类F1、解释相似/忠实性、输出安全率混算；但若只强调“未证明”，缺少已有论文确实提高了什么及边界反例。 |
| 外部可复核性 | **有阻断缺口** | MultiMM/RV-HATE/CADET/MGMCF/MCIB等所查代码的S级结论若没有固定仓库commit、源码permalink、运行路径与变量形状，不能只用发表论文引文作支撑。 |
| 文献定位与学术增量 | **目前不充分** | [R5-C L25–51](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L25-L51)与[R5-C L384–438](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L384-L438)不能仅靠“跨子域统一整理”区别于既有语用、修辞和多模态安全综述；必须落实正反证据支持的2–3个条件规律。 |
| 可投稿成熟度 | **NO-GO** | 三个P0未在实际正文关闭，R6-V真实图表渲染、书目、跨文件一致性也未独立通过。 |

## 2. 去重总账（冻结）

A0登记**11**条、A1登记**14**条、A2登记**18**条、A3登记**17**条，合计**60个历史编号**。逐编号唯一归属的终审根问题为：

- **3个P0（全局阻断）：**`P0-01`原创跨域综合与先行综述差异、`P0-02`作者公开源码S级判断的可复核性、`P0-03`ExPO-HM正式研究遗漏。
- **17个P1（实质修订）：** 从选文方法、任务范围与GT，到各方法/数据/反馈的真实结果与负例，至横向表7与结语研究议程。
- **4个P2（纯编辑/定位）：** 内部编辑备忘、“预期贡献”、表4代表性声明、表5与T5缩写歧义。

计数为**24个去重后的整改单元，而非24条新发现**。按等级单元分组后每个历史编号恰属一个主责任组，另允许跨组“依赖”关系。A1-01/A3-13属于A0-01；A1-13/A2-16属于A0-02；A3-12属于A0-03。不得将它们额外累计为全稿新P0。

## 3. 三个真正阻断投稿的P0（必须在新稿原文中实际关门）

### P0-01｜独特学术贡献尚未由有形的跨论文比较结果证明

- **原文锚点**：[R5-C L25–51](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L25-L51)引言相邻综述与贡献，[R5-C L384–438](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L384-L438)方法族/评价综合，[表7](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T7_Method_Families.md)。
- **直接证据**：项目[R5-E Related Surveys](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/Related_Surveys_Comparison.md)登记多个已有相关综述；R6-A1核Ma ACL2025 Main（CCF-A）语用综述，原稿四行相关综述对照较窄；R2-C/R3-A已准备更细的机制演化。**“综述价值不足”属Reviewer H级裁决，不是某篇论文的作者实验事实。**
- **必须改成什么**：第1章给`已有综述 × 重点分析单位 × 当前稿无法简单由其得出的交叉证据产物`的简明公平比较；第8章将表7从方法名录升级为`任务Y、X_train/X_test先验、gold/生成监督、作者本协议正向收益及反例、独立控制缺口`矩阵。至少实写以下**三条有P证据支撑的H级条件规律**：
  1. **编码开放度由先验预算决定**：Silent已知定义的instance消歧、FA-Net固定类别+目标域未标数据、FETCH词典留出type回收、SeTox测试时搜索——可计算的输出与先验预算一同变化；不能跨协议宣称实现未来完全未知词的“真实开放世界泛化”。
  2. **解释监督与目标漂移**：ImpCon已有implied statement、SMARTER gold类别条件偏好、ExPO-HM政策SFT+CDE、ThinkingGuard触发与步骤偏好、Meerkat规范风险知识自评——在作者各自协议产生预测收益，但模型可用标注知识与奖惩对象不同，解释可读/正确/忠实必须分开；必须附反例/边际收益不大的例子。
  3. **联合安全的双侧代价**：VLSU行为prompt的Borderline与Unsafe拒答同时下移；CrossGuard SIUO防护ASR大降但FigStep轻微升高；MOSSBench安全主集有争议与部分有害对照。风险分类、回应拒答和攻击ASR不能直接合成一个Pareto点，条件性论断须明写各自Y/G/E。
- **P0关门标准**：引言有可引用的先行综述公平差异；§8有至少3个完整的`正向结果+反例+条件+证据级`案例，不是泛泛“应同预算”；表7与正文数据相符；第9章只保留最重要的可证伪未来问题。修完后必须由独立复审确认确实比旧稿增加解释力，不能用“添加一张表”自动视作过关。

### P0-02｜本项目对公开代码的高风险静态观察缺可被外部读者复核的固定证据链

- **原文锚点**：[R5-C L150–160](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L150-L160) EmoBi/SemanticQA；[R5-C L230–263](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L230-L263) RV-HATE/CADET；[R5-C L298–316](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L298-L316) MultiMM/MGMCF/MCIB；另Ch7部分MMSafeAware/Meerkat所查发布版本。
- **已登记来源**：P029 RV-HATE的`ppo_eval.py`可能用test split建奖励环境；P033 CADET的目标test用于valid；P003 MultiMM测试读取人工情绪；B3a MGMCF源/目标辅助字段；R3B MCIB的MSE[B,1]对[B]广播/原文本残差路径；P027 ExPO-HM公开训练脚本与论文配置不一致。**这些是S级审计卡指出的具体版本风险，并不是论文作者当年的真实训练流程已被本稿验证违规**。
- **必须改成什么**：对于全部保留在投稿正文的`我们发现作者代码……`断言，建立独立索引：
  `claim_id | citation for published paper | public repository | immutable commit | file#Lx-Ly | invocation config/split/data shape | observation(S/static or unit-test) | cannot infer published experiment used version | audit date`。
- **允许的两种关门方式**：
  1. 固定源代码及精确行为可被第三方访问、重现静态判定，则保留在正文并以索引支持，范围严格限于所审版本；或者
  2. 不能固定/证明时**降级为“公开实施细节需进一步核对”并移入OPEN或删除具体违规措辞**，不将这类断言当发表论文实证。不得为了显示创新而保留无法证实的指责。
- **P0关门标准**：逐句审稿检索没有任何未给固定版本与作用范围的高风险S级事实断言；公开附件可定位，或已作保守删降；禁用“实验已违规/作者泄漏已证明”等未证用语。

### P0-03｜ExPO-HM（ICLR2026 Main，CCF-A）的直接相关方法覆盖缺口

- **原文锚点**：[R5-C L354–370](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L354-L370)、[R5-C L386–413](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L386-L413)；原R5-C的`references.bib`46条已核不包含ExPO-HM。
- **证据**：[ICLR 2026正式页面](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)，https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md。作者论文以Hateful Memes解释后分类为目标，政策手册SFT、细粒度→二分类课程GRPO、CDE奖励与评估；作者报告binary macro-F1 naive GRPO74.5→ExPO-HM81.1，而对强直接RA-HMD80.2为+0.9百分点。CDE小≠解释忠实；所查公开脚本和论文课程设置有未闭合版本差异。
- **必须改成什么**：Ch7/Ch8、T7增加“解释后检测”和风险归因监督的对照：SMARTER（标签条件的解释DPO）、ExPO-HM（政策+课程+CDE）、ThinkingGuard（SA-MCTS搜索后Step-DPO）、Meerkat-VL（风险说明自评+GRPO回应），每项写`Y、X/teacher、优化loss/reward、作者P级收益、未证机制`；新增规范官方Bib与真实正文引用key。
- **P0关门标准**：`references.bib`存在经官方记录核的唯一正式条目；正文至少一处机制和一处证据限度比较；T7与引用键一致；**明确ExPO-HM不是VLSU式三条件S-S-U输入GT**，不得为了增加覆盖而误分任务。

## 4. P1与P2后续处理原则

所有17个P1与4个P2的**唯一编号归属、原文锚点、原作者证据与可验收修订**已冻结在[去重问题表](R6A4_Deduplicated_Issue_Register.md)。以下为必须警惕的几条事实性检查：

1. **DOSE输入模态确认写错**：[原表5](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T5_Multimodal_Meaning.md)把DOSE列作“文/音/视”；DOSE是新闻**图+文**的反讽理解（ACL2026 Main，CCF-A），音视频对应MCIB。此项虽归P1-10，但**必须实际改表**。
2. **跨模态与安全的重要分母**：CrossGuard Figure6生成1390红队攻击样本，不是其Figure7的1616混合Guard训练例；后者约12.5%即≈202条联合类型，尚未独立确定哪202条来自1390。SIUO Fig4 ASR 60.33→5.39，FigStep同协议0.12→0.21，须一并呈现；VLSU PDF8187/公开8159、严格S-S-U37/35，34%是joint预测**已错**组的条件比例，而非全体或严格S-S-U。
3. **不同评价不得互换**：VLSBench SafeRate拒答+警告≠输入准确率；MMSafeAware unsafe1000/over-safe500导致恒判Unsafe总Acc可达66.67%；MOSSBench 300安全意图样本的部分人审安全性有异议；ThinkingGuard配对图片各自生成、Step-DPO多了Unsafe监督；Meerkat自评不重新读取图像。这些需要“已验证”与“尚需控制”的正反两面。
4. **图与表的科学含义独立于外观**：R6-V只可调整可读性/出版形式，若发现图2层级或表5事实错误、表7方法机制错误，应在R6-Fix内容修订里解决，不让视觉工程私自重写研究断言。

## 5. 建议R6-Fix依赖链和工作量边界

建议**不重启大规模精读，不扩大至91篇全部逐篇摘要，不新建人标大数据集，不进行多GPU复现**。

- **Gate 0 / 版本冻结**：以原R5-C固定commit为底稿保留独立修订副本，在R6-Fix分支以清晰的父分支PR关系开展，不直接覆盖旧PR#57或main；确保改稿中每条claim仍可回指历史编号。
- **Gate 1 / 纯确定性修复**：DOSE表5模态、内部编辑语句、Bib ExPO条目、ThinkingGuard/NAACL Findings的正式Track标法与Bib校对、T5/表5歧义、关键数字分母、SIUO表6行。做到无需训练也能检查。
- **Gate 2 / P0科学论证**：形成先行综述对照+Ch8三条条件规律+ExPO与其他解释/风险方法对比；扩表7为有实证结论/反例/信息预算的对照，不以文字扩充冒充新增贡献。
- **Gate 3 / P0证据追溯**：S级源码+版本目录；能证的限定写，不能证的保守降级。对应P1实际样本/标注/检索/解释多侧修复。
- **Gate 4 / 学术再次审稿**：逐P0带新的原文行、证据永久链接、修订前后差异`OPEN→CLOSED/OPEN`；全稿检查无虚构“本项目复现”。P1根据必须/可选分类明确剩余风险。
- **Gate 5 / R6-V独立技术核验**：F1–F5真实渲染与单/双栏黑白可读、T1–T7布局、`references.bib`合法可解析、所有citekeys唯一对应正式元数据、Markdown/DOCX/PDF一致；未经核实的ACM Track等仍标OPEN，不编造。

**投稿前门槛**：三个P0均在实际新稿关闭、至少所有P1中的事实性错误及关键分母得到改正、R6-V图表/Bib/引用通过、一次综合复审证明最终稿仍符合原稿证据限制，才可更新为“SUBMISSION-READY CANDIDATE”。本文未选具体投稿期刊/会议，因此本轮**不宣称已满足某特定期刊的格式或篇幅规则**。

## 6. 边界与残留风险

- A4是**A轨学术内容的终裁**，不是对R6-V结果的认证；不自动把PR #57／#58标合并就绪。
- VLSU CSV差28、AUTALIC 2400 vs 242+2160及原CSV未核、MMSafeAware公开图片缺口、Meerkat数据8436/8466、ThinkingGuard ACM正式Track/反事实质量、MCIB源代码是否对应论文正式训练等仍有O项。可以保留带版本限定的开放项，不强求把所有外部不可获得数据伪装为CLOSED。
- 不因存在O项就否定所有作者论文结果；也不因作者已发表CCF-A就把训练协议机制独立性当成自动成立。
- 完整可执行工单见[R6-Fix交接包](R6A4_R6Fix_Execution_Package.md)。本文件的“最终裁决”是当前R5-C学术成熟度裁决；不是对之后尚未生成的R6-Fix稿的验收结论。

**最终签署：R6-A0、A1、A2、A3、A4全部学术审稿完成；Verdict MAJOR REVISION；三个P0均OPEN；R6-Fix尚未执行；PR保留Draft/Open、不合并。**
