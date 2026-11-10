# R6-A1｜第1–3章正式逐章学术审稿

> **状态：R6-A1 REVIEW COMPLETE（仅第1–3章），2026-11-09**。从R6-A0独立审核继续，非改写原稿。  
> **审查源稿**：R5-C Draft PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)，固定commit `c04d6a23e864923acd64c192c8b05dc597c2bb90`；正文 `03_survey/R5_full_draft/Survey_Full_Draft.md` 第1–3章 [L1–167](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L1-L167)；表1 `tables/T1_Concepts.md`、表2 `tables/T2_Tasks_and_GT.md`。  
> **证据基线**：main中R1分类、R2-B/B1综合、R3-A、R4-07/08、R5-E相关综述与citation gates，以及P011/P015/P020/P022/P035等定稿精读卡。额外定点核验[Ma ACL正式主页](https://aclanthology.org/2025.acl-long.425/)、[(RSA)² ACL正式论文](https://aclanthology.org/2025.acl-long.1019/)、[DRInQ ACL正式论文](https://aclanthology.org/2026.acl-long.1597/)、[EmoBi ACL正式论文](https://aclanthology.org/2025.acl-long.23/)及PDF关键表/图；DRInQ PDF p.34598–34599、EmoBi PDF p.495已实际查看页面图像。(RSA)² PDF文本可检索但本轮截图缓存未成功；其Table2/3数值与已定稿P020卡交叉吻合，**不声称完成其正式PDF逐页视觉验收**。   
> **结论等级**：F=出版官方信息；P=论文作者数据/结果；S=所查公开代码/CSV静态观察；H=本次审稿综合；O=未闭合。作者报告不等于本人复现，代码现态不等于正式论文训练状态。

## 0. 审稿总裁决

**第1–3章：CONDITIONAL PASS / TARGETED MAJOR REVISION（局部重要修订，保留总体结构）。**

- **第1章：MAJOR REVISION。** 研究范围和任务问题具有学术价值，且明确不是PRISMA；但与最近语用/修辞/仇恨及LVLM安全先行综述相比，`新贡献=更宽的编排`仍未充分完成可证的比较；91候选→46引用的选择透明度亦不足。
- **第2章：PASS WITH MODERATE REVISION。** 语义/语用/规范危害分离、五轴与T1–T6非流水线的理论立场总体正确。核心欠缺是**工作性分类的边界和继承关系尚未完全操作化**（T5是T4的关系依赖特化，T6是相邻输出层）；X、G、E的具体可观测性需要更精确说明。
- **第3章：PASS WITH TARGETED REVISION。** 相比常见逐篇罗列，已有(RSA)²、DRInQ、EmoBi、SemanticQA的可识别机制与证据不足分析，方向正确。但有两项**被作者原文直接展示的负侧/选择偏差**未充分呈现：RSA字面场景损失；DRInQ 400难例偏向人机/原生成标签不一致。EmoBi核验消融有量化结果，但情绪、互动、源/目标和核验的边界需要同预算与GT分层。

**新增或细化本轮问题**：共 **1 P0 + 11 P1 + 2 P2 = 14项**。其中A1-01、A1-02/03/05、A1-12与A0早期清单**有交叉，属于细化而非重复新增全局P0数量**；全局issue log应按编号引用不重复加总。

### 建议保留的论证链

1. §1.1 把字面不足与非恶意表达联系起来；§1.2/2.1工作性定义主动承认`隐含≠细微≠有害`。
2. §2.2 将机制、预测Y、模态/社群/时间、训练测试信息和GT/E分成五轴，不将VLM/DPO/危害作为同一性质的一级类别。
3. §2.3/3.2明确受控候选的**可接受解释标签**不是可观测的真实心理意图。
4. §3.1 EmoBi是提示调用结构而非新训练损失；SemanticQA的组合任务不是多次独立模型调用；反问probe只观察可线性读出的信息，这些限定准确。
5. §3.2不把(RSA)² Table2的最佳 L0 解释为L1递归独立成功；§3.3不把Self-Verification等于外部事实核查；§3.4拒绝跨Acc/F1/候选正确概率/解释相似度/AUROC硬排名。
6. §3.5对CodedLang与Silent Signals的桥梁不是`修辞即编码`或`编码即恶意`，有助于第4章的任务拆分。

## 1. 第1章：定位、相关综述与选文审核

**学术优点**：[L11–24](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L11-L24)围绕交际意义与规范判断切入；[L38–44](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L38-L44)定义工作性广义范畴，同时排除普通显式毒性/无关OCR；[L54–56](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L54-L56)不把91篇写成全领域论文数。

**A1-01｜P0｜已有综述对照不足以证明“贡献增量”（继承A0-01）**  
- **原文定位**：§1.2 [L27–40](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L27-L40)，§1.3 [L48–50](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L48-L50)；表仅列Kühn、Ma、Farabi、Hee四项，贡献写“在同一框架中分别定位表达机制、预测任务、模态条件和证据可靠性”。
- **证据/反例**：Ma et al., *Pragmatics in the Era of Large Language Models*，ACL 2025 Main **CCF-A**，正式摘要已涵盖语用现象、数据构建、任务形式及评价局限；[正式论文](https://aclanthology.org/2025.acl-long.425/)；Mao et al., *A survey on pragmatic processing techniques*，Information Fusion (2025，**本项目CCF等级待核**)已在官方出版摘要梳理五类语用处理任务、技术与应用，[出版社页](https://www.sciencedirect.com/science/article/pii/S1566253524004901)；另有R5-E登记的Ge 2023隐喻处理综述与LVLM安全综述（后者出版状态待核）。现有表格只以一句“不同分析单位”自我定位，缺`先行工作具体覆盖什么，本稿额外解决什么不可比较性`的证据产品。这是审稿人H级判断，**不是声称所有相关综述均已全文核对**。
- **修订动作**：用`prior survey / 核验状态 / task&GT关注范围 / 本稿附加的直接可检验比较 / 限制`矩阵替换笼统差异；至少对Ma与Mao做实质重叠说明、对Kühn/Farabi/Hee补任务GT差异。第8章必须给出具体“任务—监督—证据门槛”的跨论文结论，回写到§1.3，不能把“更宽”单独当贡献。**验收**：每条自称的“本文贡献”能定位到表或分析段，且有两个以上不同子域原论文及反例支持。

**A1-02｜P1｜91候选→46条主文引用的选择依据不足**  
- **原文**：§1.4 [L52–56](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L52-L56)“从R0的59条和R2-A的32条去重候选……91条；优先使用已完成精读”。
- **证据**：R4-02 91项唯一主讲分配与R5-C 46条BibTeX；R5-E已承认先行综述全文时间窗/PRISMA未核。论文本已诚实声明“非系统综述”，因此不能要求PRISMA漏斗或假装全量召回；但读者仍需知道主文为什么重点讲这些论文。
- **修订动作**：表明截止日期、检索渠道与覆盖范围、代表作选择准则（直接回答RQ/任务GT可追溯/原文可核优先）、仅元数据文献如何使用、46条与91候选的关系；如给主题分布先从真正Bib和映射统计，不能凭R4分配篇数估计。

**A1-03｜P1｜广义定义的核心/邻接边界仍有循环归属风险**  
- **原文**：§1.2 [L38–42](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L38-L42)“需要……模态间关系来推断的信息”与§2.1 [L70–80](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L70-L80)“目标意义、评价立场或交际功能不能仅由直接字面表达充分确定”；§2.5 [L124–124](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L124-L124)排除普通上下文任务。
- **问题**：对一般安全判断，“有政策/上下文”不等于隐晦语用；对普通图文meme，只要图像提供语义仍未必形成非字面或组合风险；对指示词消歧，虽然有字面以外的指称语境但应留在邻接。正文已认识此问题，尚缺一套明确可执行的纳入最小条件。
- **修订动作**：给`Core（有隐含机制/已审关系GT）→Adjacent（仅风险响应或纯上下文）→Exclude（普通毒性/OCR/任意指称）`三档，加至少四个例子与“可证明的实验对象”。不要把T6的一切安全对齐自动归为核心广义隐晦信息。

**A1-04｜P2｜第1章“预期贡献”的表述尚属任务书口吻**  
- **原文**：§1.3 [L50–50](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L50-L50)“本文预期的贡献是三个方面的综述性整理”。
- **修订动作**：等第8章最终有对应产物后改为`本文贡献`并给具体表/节；无产物者删除或降为`分析目标`。不是要求无证据夸大论文已完成的实验。

## 2. 第2章：理论基础、五轴、T1–T6与可观测GT

**理论判断**：§2.1指出语义并非全无上下文、Grice/Searle/Frank–Goodman分别是言语行为/会话含意/概率语用的理论锚点，概念准确；不应把语用GT说成真实心理状态。表1逐项区分隐含、subtle、coded、形式伪装及harmful，整体可保留。

**A1-05｜P1｜T1–T6不能同时被当“六个同层互斥任务”使用（细化A0-04）**  
- **原文**：§2.2 [L86–100](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L86-L100)，§2.4 [L108–114](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L108-L114)，“T5的特殊地位”；[表2](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T2_Tasks_and_GT.md)将T4风险与T5联合风险、T6安全回应各写一行。
- **证据**：R2-C与R4-07给T5属特定多模态关系依赖的T4、T6单列行为评价；VLSU、MSSBench、Meerkat-VL的预测输出并不共用分母。本稿**已在正文正确说明**，问题在于表格及概念图易诱导误读。
- **修订动作**：表2新增`任务层/继承关系/是否可并存`；T1–T3是不同预测目标但实际可重叠；T4属于规范性输入风险；T5为有明确组合性评估的T4子设定，S-S-U更窄；T6是回应行为/质量而非同类输入标签。不要人为要求模型执行T1→T6流水线。

**A1-06｜P1｜Task=(X,Y,G,E)缺可部署X与原始训练监督/评价Judge的边界标注**  
- **原文**：§2.2 [L94–100](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L94-L100)“D 训练/测试可用信息预算”与“E Ground Truth与证据协议”；§2.5 [L120–124](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L120-L124)引入`G_in/P_in/R_beh/Q_out`。
- **问题**：`Task`四元组是好的编辑记录式，但把原始输入、测试gold辅助字段和外部检索统称X，会影响第3章EmoBi自生成情绪与MultiMM测试gold情绪的区分。G是生成规则/标注主体/数据标签的合成记录，不一定单一人审“真值”；E需要区分自动分数、人工判断和模型Judge，及对缺省/争议样本如何计分。
- **修订动作**：保留四元组，只在其下加一张最小`X_raw / X_aux^train / X_aux^test / Y / G_source+policy / E_metric+denominator+judge`示例（DRInQ、VAGUE、EmoBi各一）；`X_aux^test`不得默认为真实部署可用；G中`human consensus`与`generated target checked by humans`区别标出。不要无必要发明复杂数学新理论。

**A1-07｜P1｜间接言语行为的原典可更精准**  
- **原文**：§2.1 [L64–68](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L64-L68)仅引Grice 1975、Searle *Speech Acts* (1969)、Frank & Goodman (2012)来支撑“间接言语行为”理论和间接请求例子。
- **证据**：1969著作为言语行为基础，未必错误；但Searle *Indirect Speech Acts* (1975)，载Cole/Morgan的`Syntax and Semantics Vol.3` pp.59–82，是这类间接请求最直接原典（[书目对照](https://onlinelibrary.wiley.com/doi/10.1002/9780470757031.biblio)）。Grice 1975与Frank/Goodman 2012现有Bib至少基本元数据已核（[Frank/Goodman正式索引](https://pubmed.ncbi.nlm.nih.gov/22628647/)）。
- **修订动作**：补Searle 1975原典的书目与引用位置；不能用1969书的确实存在推断1975文章已被引。是精度补强，非原文严肃错误或须重新建理论。

**A1-08｜P1｜表1/表2需标清标签“标注对象”与“标注来源/审核程度”，不可默认都是人审金标**  
- **原文**：表2的“T1 G=人审现象标签”“T2 G=人审/构造的可接受意义”；§2.3 [L102–106](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L102-L106)同一语用范畴的候选设置。
- **证据**：EmoBi四资源由2023联合标注工作在不同原始标签基础上补标；DRInQ为模型生成场景、62位被招募者、5人/条且至少4人一致的筛选；VAGUE为生成预设行动并人工评估合理性，不是现实发话者自标的真实意图（[VAGUE卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_02_VAGUE.md)）。
- **修订动作**：给G分`原始人工/追加标注/生成+筛选/代理与伪标签/多数票+异议`类别，避免表2“人审”给出所有正例均多人数投票的印象；表1仍保持工作性而非因果本体。

## 3. 第3章：文本修辞与语用方法、机制及实验支持

**机制审核结果**：

| 工作 | 已有机制解释是否基本对 | 精准可主张的实证 | 仍欠缺/不能写 |
|---|---|---|---|
| **(RSA)²**，ACL 2025 Main，**CCF-A** | **对**：策略相容函数替代严格字面相容，候选/先验限制得到讨论。 | 作者Table2共50情境：hard策略L0正确意义平均概率0.85，普通LLM RSA L0为0.73，soft策略L1为0.80；Table3去意义先验大降。 | 作者Fig4字面情境普通LLM RSA L0≈0.95，策略hard L0≈0.77；不能只讲非字面侧改进，也不能归因递归L1独立成功。 |
| **DRInQ**，ACL 2026 Main，**CCF-A** | **对**：固定问句、变语境、5选1共识判断。 | 819条通过至少4/5人一致，400条定向筛选困难集；Table2 human 0.88±0.10、OpenAI-o3 vanilla 0.67±0.02。 | 400条难集不是随机普遍场景；模型间差距依赖测试集选取和构造候选。 |
| **VAGUE**，ICCV 2025 Main，**CCF-A** | 目前提得太简：视觉场景+间接表达→候选行动。 | VAGUE2.0 1677样本，4选1；SU/NE/FS三种负例；LM/SM caption/VLM原图不同信息预算，400子集人评94%。 | 不能将模型VLM>LM简单说成视觉因果依赖，或把人评94%套在全部1677条。 |
| **EmoBi**，ACL 2025 Main，**CCF-A** | **对**：情绪→源/目标→隐喻/夸张条件提示→自重判，非新网络训练。 | Table2去情绪F1降4.4–5.7点（各任务配置范围）；去核验降1.2–1.9点。 | 两类标签来自既有联合标注；公开主路径不是完全对称双向训练；不同提示调用/token/标签血缘不控制，不证明情绪为因果中介或Verification真正检错。 |
| **SemanticQA**，ACL 2026 Main，**CCF-A** | **对**：一次Prompt同时输出抽取及解释，而非程序两次独立推理。 | 作者Table5报告抽取条件下的METEOR及综合分。 | 所查代码某路径计算BERTScore-F1，与正式Table5 METEOR口径不同；不要强引公开代码输出等于正式论文指标。 |
| **反问探针**，ACL 2026 Main，**CCF-A** | **对**：冻结模型表示上的线性可读性，非开放意图恢复。 | diffMean、Logistic、hinge probe测AUROC/方向/排序一致性。 | diffMean仍使用类标签算正负均值，不是无监督；不同数据集标签协议和PCA映射影响方向解释。 |

**A1-09｜P1｜(RSA)²漏掉同一实验的字面情境代价（本轮新增实质性发现）**  
- **原文**：§3.2 [L144–144](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L144-L144)“策略条件有助于特定候选意义选择”，仅强调Table2最佳L0和Table3先验。
- **直接证据**：[(RSA)² 正式论文](https://aclanthology.org/2025.acl-long.1019.pdf) §5.3 Table2、Figure4、§5.4 Table3；[P020定稿卡§5–7](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P020_RSA2.md)。Table2 hard策略L0=0.85而传统L0=0.73（50情境平均正确意义概率）；Fig4分组时字面情境传统L0≈0.95 vs策略L0≈0.77。平均提升不等于所有子群都提升。PDF该页截图本轮缓存未成功，数值据PDF文本和卡片交叉核，标P且非独立复现。
- **修订动作**：在Table2之后加入一句“增益有方向性，字面情境可能过度解释为反讽”，用0.95/0.77并注明分组和指标；解释策略后验在literal场景不可靠（P020审计0.55），避免用`理解隐含意义改进`覆盖负例代价。**验收**：正侧/负侧与机制归因两句同段呈现。

**A1-10｜P1｜DRInQ 400难例的选择协议应置于结论之前**  
- **原文**：§3.2 [L146–146](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L146-L146)“困难子集Table2报告400道五选一题”，未写该400如何形成。
- **直接证据**：[DRInQ ACL 2026 PDF](https://aclanthology.org/2026.acl-long.1597.pdf) §3.7（出版页34598）、Table2（34599），已检查页面图像；819共识通过后，400件倾向选择`低人机一致性`或`人工一致答案与生成目标不一致`的困难设置，非随机的现实语用样本。Table2 400条三次few-shot采样，OpenAI-o3 0.67±0.02、human 0.88±0.10。
- **修订动作**：明确“经过难度筛选的400条，不能外推成自然日常会话总体语用准确率”；指出`generation A_g`与`human consensus A_c`区分，以及标签来源与候选构造。保留已正确陈述的“解释提示非普遍改善”。

**A1-11｜P1｜EmoBi的正向结果、主导消融和预算混杂未平衡叙述**  
- **原文**：§3.1 [L136–136](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L136-L136)“Table1 F1与Table2核验阶段消融”；§3.3 [L152–154](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L152-L154)主要谈重判和部署。
- **直接证据**：[EmoBi ACL 2025](https://aclanthology.org/2025.acl-long.23.pdf) §3、Table1/2（p.495已实际查看）；[P035定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md)。Table2情绪移除通常下降大于核验移除（如HYPO metaphor 84.5→79.4，-5.1；verification 84.5→83.1，-1.4；HYPO-L metaphor 80.3→74.6，-5.7），但模块移除**不是**等prompt/tokens控制，不能把差值归为单一独立因果机制。数据双标签来自2023 *A Match Made in Heaven*（ACL 2023 **Findings**，不能当Main）补标。
- **修订动作**：补“解决什么：联合形式检测”“采用什么：多次LLM prompt与源/目标情绪解释”“直接提升：情绪/互动/核验条件下的各自F1消融”“未隔离：调用预算/标签先验/真实意义GT”。在表注指明2023 Findings标签血缘，禁止称2025重新标出四个大数据集。

**A1-12｜P1｜DRInQ与VAGUE同属于T3，但可观察GT、负例及视觉信息预算需要明确对照**  
- **原文**：§2.3 [L104–106](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L104-L106)一段连提、§3.2 [L146–146](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L146-L146)仅介绍DRInQ，VAGUE几乎未进入第3章的方法比较。
- **证据**：[B1-DRInQ](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_01_DRInQ.md)与[B1-VAGUE](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_02_VAGUE.md)定稿：前者`固定问句Q→文本C变换→5候选人类共识`，后者`图像+间接话语→4候选行动（三类精心构造干扰项）`，比较LM/SM(caption)/VLM原图。本稿的五轴恰适合展示二者差异。
- **修订动作**：增1个紧凑对照段或表：`固定/变化因素—候选制作—GT来源—评估分母—潜在捷径`。不要求另开多模态长篇；用于连接§3语用与第6章模态必要性。

**A1-13｜P1｜第3章S级实现判断和评价指标需公开可追溯版本（细化A0-02）**  
- **原文**：§3.1 [L136–140](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L136-L140)“静态审计发现当前公开调用顺序”；§3.3 [L152–154](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L152-L154)“源码还保留固定先后顺序及运行依赖问题”；§3.4 [L158–160](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L158-L160)“SemanticQA公开程序……一次提示”。
- **证据**：[P035卡§4、§8](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md)记载所审主路径`analyze_emo → target_source_domains → metaphor_learning → hyperbole_learning → hyperbole_metaphor`及运行风险；[P022 SemanticQA卡§5](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P022_SemanticQA.md)记载`main.py`一次调用与`eval.py`在特定路径的METEOR/BERTScore差异。原论文书目不能代替**版本化源码证明**。
- **修订动作**：如保留具体公开实现断言，附永久commit、文件/行、输入输出字段、所审路径是否实际运行的范围，统一写S/O。若无固定公开版本，降为“所查实现线索、待运行确认”并不把官方作者实际Table结果标为违规。

**A1-14｜P2｜第2章编辑性标题与段落接续清理**  
- **原文**：§2.5 [L126–126](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L126-L126)：“本章小结（归入2.5，不单列2.6）”；[L74–76](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L74-L76)两行“必须区分的概念如下：详见表1”。
- **修订动作**：前者改成正式“本章小结”（同级或自然段）并去任务书括号；后者合并成通顺一句“表1概括……”。不改变学术概念。

## 4. 必须保留的证据防线及不应新增的假强断言

- **不要**把Grice/Searle/RSA的认知模型解释为“已观察到每位实际作者真实心理意图”；DRInQ和VAGUE是人工共识/生成任务目标。
- **不要**把五轴写成统计正交空间；T1–T6是综述审计标签而非模型必经决策链。
- **不要**将DRInQ的0.67写作整个日常语用准确率，或VAGUE 400人评94%写作1677条全量人类结果。
- **不要**把(RSA)² Table2的“0.85概率”说成85%分类准确率，或只写非字面情境成功不写字面情境下降。
- **不要**把EmoBi Table2模块消融说成情绪的因果中介已证实；不能把2023补标写成2025新人工标注，更不能把普通LLM多次自重判说成独立外部Judge。
- **不要**把SemanticQA同一prompt的多输出说成独立顺序API调用，或把线性probe得到的可分向量说成解释忠实、无监督发现了单一语用方向。
- **不要**为了凑2024–2026 CCF-A而删除Grice/Searle等理论原典、或者把ACL Findings/VAGUE/相邻期刊CCF等级编造为Main或A。

## 5. R6-Fix精准工作指令（A1范围）

**先做**：a. 补第1章先行综述差异矩阵并让§1.3每项增量映射到既有证据产物；b. 补第2章表2层级、示例X/G/E与纳排标准；c. 在第3章加入(RSA)² literal负侧与DRInQ困难选集、EmoBi多组件对照，同时简要比较VAGUE。  
**再做**：d. 交接给A2处理MultiMM的test-gold和其它S级代码证据，不要把第3章对test-gold的陈述跨章消失；e. 最后统一本章S级公开代码固定commit与附录来源，投给R6-V检查正式出版书目和引用样式。  
**不做**：全文重写；新模型训练；大规模新增文献；凭猜想修改作者数值；改写原仓库R1–R5审计历史。

### A1审稿证据入口

- [R5-C全文固定快照](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md)
- [R5-E相邻综述](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/Related_Surveys_Comparison.md)
- [R4-07章节主张证据表](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)
- [P020 (RSA)²定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P020_RSA2.md)
- [B1 DRInQ定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_01_DRInQ.md)
- [B1 VAGUE定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_02_VAGUE.md)
- [P035 EmoBi定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md)
- [P022 SemanticQA定稿卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P022_SemanticQA.md)

**R6-A1终结语**：第1–3章已有足够可靠的研究主线，**不需要重写，但以第1章贡献对照为P0，其他以定向补证与降低推断为主**。只完成这三章的学术审稿；Ch4–6、Ch7–9和A4全局verdict仍OPEN。
