# R6-A3｜第7–9章正式逐章学术审稿：联合风险、安全行为与跨域综合

> **状态**：R6-A3 REVIEW COMPLETE，2026-11-09。**仅审稿，不更改R5-C、不合并PR。**  
> **固定版本**：R5-C PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)，commit `c04d6a23e864923acd64c192c8b05dc597c2bb90`；审查主文 [R5-C L330–457](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L330-L457)、[R5-C T6_Multimodal_Safety](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T6_Multimodal_Safety.md)、[R5-C T7_Method_Families](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T7_Method_Families.md)，对照 R6-A0/A1/A2、R4-07、R5-E、R3-A/R2-B/B4a及 P027/P034/P037/P038/P039/P040/P041正式精读卡。  
> **学术证据级别**：F=官方出版/固定版本元数据；P=正式论文作者报告/截图或正文（非独立复现）；S=公开源码、README、数据静态观察（必须固定commit）；H=审稿综合性推断；O=未闭合。外部检索截至2026-11-09。  
> **核查诚实说明**：本轮打开 ICLR2026 VLSU、ACL2026 CrossGuard 官方PDF并读相应表图提取文本；VLSU正式PDF首页截图成功，Figure5/Figure9以及CrossGuard Figure4的网页截图因cache miss未成功，后者数值依据PDF可读文本+此前定稿卡交叉；官方ICLR ExPO-HM出版页面已直接核验。ThinkingGuard作者仓库与arXiv作者录用声明可确认，但**尚未取得ACM出版社正式最终条目/确切Track**，不能擅称已核“Main正式出版”。Meerkat-VL的正式ICML全文基线/消融表仍沿用项目已定稿卡（其已明言未逐表核验）；本轮不假称重跑原始训练、看过全部图片或全部PDF逐页截图。

## 一、裁决与数目

**R6-A3：CONDITIONAL PASS / CH7 TARGETED REVISION, CH8 MAJOR REVISION, CH9 MODERATE REWRITE。**

| 章节 | 真实优点 | 必修问题 |
|---|---|---|
| Ch7 **多模态联合风险与安全回应** | §7.1 `G_in/P_in/R_beh/Q_out`四层实质正确；VLSU三条件GT、Hateful Memes非全S-S-U、CrossGuard Guard vs红队、ThinkingGuard推理 vs回应生成区分准确。 | 数据版本和标注可靠性还缺一张清晰对照；CrossGuard的样本分母及Fig4例外需补；ThinkingGuard反事实/Step-DPO独立效果未完备；Meerkat self-score与训练gold风险知识的边界需凸显；表6缺SIUO。 |
| Ch8 **方法族与评价可靠性** | “输入信息预算”“GT分歧”“解释忠实”“单模态/反事实”“安全双侧错误”分析正确，并多次避免错误因果推断。 | **两项继承P0**：高相关ICLR2026 ExPO-HM遗漏；仅把边界与必要控制排列为章节，独特的正向、条件化机制综合不足。T7未能承载训练目标、信息优势、有效作用及负例的真正比较。 |
| Ch9 **总结与展望** | 结语不声称发现统一SOTA或无人研究空白，边界严谨。 | §9.2在重复Ch8列举的“应记录信息/应做去模态/应分两侧”而缺具备X/Y/G/E、现成GT与最低诊断的**优先研究议程**。 |

**问题总数：17项，2项P0（A3-12继承A0-03、A3-13继承A0-01；不是新全局P0）+14项P1+1项P2**。与A0/A1/A2重叠的claim须A4去重；本轮所有issue仅为OPEN，不是已改稿的关闭状态。

## 二、Ch7逐节审稿与优先改法

### 7.1 四层测量：保持原文框架

[R5-C L334–338](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L334-L338)正确将`G_in`定义为人审/政策输入风险真值、`P_in`定义为模型**显式报告**风险类别、`R_beh`定义为拒答/警示/执行等行为、`Q_out`定义为安全性与合法帮助质量。没有显式分类接口时，不可从“拒绝”反推内部P_in；同一政策下三条件图/文/联合安全才能称S-S-U；T5是T4特殊的组合约束，T6是回应层。这是本稿的学术骨架，**不建议重写**。

但要注意：VLSU `image-only`的单人标注可靠性与`text/joint`两/三人标注并不完全等价；“单模态被标为安全”是操作性GT，不是所有人均一致、永远不依赖语境的定理。需要标注评估**政策**的准确可复核范围。

### 7.2 数据/分母审计

**A3-01｜P1｜VLSU版本信息已对但需给可操作的“模式统计口径”。**
- **定位**：[R5-C L346–348](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L346-L348)和[R5-C T6_Multimodal_Safety](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T6_Multimodal_Safety.md)。
- **证据**：[VLSU ICLR 2026正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf) §3、Fig5、Fig9、附录；[P038_VLSU](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md)。正式论文 **8187**、15 harm类、17安全组合、17模型；本项目已审作者CSV **8159**、严格S-S-U **35** vs PDF **37**，公开image_grade另有**141 not_sure**；PDF官方文字的~34%为联合分类已失败样本中两个单模态预测都正确的条件比例，不是全库比例更不是S-S-U子集比例。正式Table1二分类将Borderline并入Safe，而三分类表不同。
- **现有缺口**：主文虽已陈述这些事实，表6的“正式/CSV”只在一个单元中，读者无法重建`not_sure`处理、binary vs ternary以及条件分母。
- **修订验收**：表6或附脚注列 `PDF/CSV总数`、`严格S-S-U数`、`not_sure排除条件`、`Figure5比例的准确分母`、`二/三分类边界`；不将未知28条来源臆断为删错记录，也不据35/37得到低方差强泛化结论。

**A3-02｜P1｜联合风险三条件GT的人工判断强度并不完全等价。**
- **定位**：[R5-C L334–338](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L334-L338)、[R5-C L346–348](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L346-L348)。
- **证据**：[P038_VLSU](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md) §4：image-only由一名经验作者判断，text/joint多为三名、少量两名专业评审；多模式人工一致性有差别（P038记录S-S-U 82.5%、B-B-U 54.1%的模式级原始agreement），并非每条三条件同一严格多评审投票。**不同标注者/政策判断标准也可能影响所谓“组合升降”**。
- **修订**：在表6或§7.2一两句区分各模态的标签来源/复核次数，并将“人审三条件标签存在”与“严密反事实单变量标注保证”区分开。不是否认VLSU价值，不要求新一轮大规模标注。

**A3-03｜P1｜MMSafeAware的发布版本和重复图像比类比例更严重地影响样本独立性。**
- **定位**：[R5-C L344–344](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L344-L344)和表6一行。
- **证据**：[R2B_B4a_03_MMSafeAware](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_03_MMSafeAware.md)；**MMSafeAware ACL 2025 Main（CCF-A）**原文报告unsafe1000/oversafe500，两类本质为同一joint二分类的正负侧；本项目所查公开prompt显示1523条编号记录、1453个可匹配编号图片文件、其中仅445个不同Git blob SHA、70条prompt无对应编号图片；这些是特定发布状态S级观察，**不是正式论文数据必然为1453条的事实**。
- **修订**：表6加入`论文版/发布可配对文件数`与`重复图片分组/未可达`证据边界；坚持总Acc恒判Unsafe=66.67%，再给双侧recall或balanced accuracy；**任何文件数/图像SHA属于S级，必须固定官方commit/日期**，不得凭当前仓库断言作者评价造假或所有复现不可能。

**A3-04｜P1｜VLSBench的主要风险是响应指标可被拒答策略“假改善”，不只文本视觉泄漏。**
- **定位**：[R5-C L342–342](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L342-L342)与表6。
- **证据**：[P037_VLSBench](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P037_VLSBench.md)：**VLSBench ACL 2025 Main（CCF-A）** VSIL Judge比较`J(image,text)`和`J(text)`是否都判危险；该输入端诊断与最终输出`SafeRate=Refusal+Warning`是两个不同对象。原文报告Qwen2-VL-7B的200条对照：text-only SafeRate29.5%（拒19.5/警10.0）、text+image-description22.5%（拒3.5/警19.0）、真实图文16.0%（拒1/警15）。这些是特定200条试验的**行为分布**，不能说文字更懂风险。其新基准2241样本主要为风险正例，不能拿来直接测稳健的平衡输入二分类F1。
- **修订**：§7.2或表6加“`VSIL输入端文本代理诊断` vs `Refusal/Warning/Unsafe回应`”双层，1句解释退图后SafeRate上升未必体现风险理解；图文配对是否视觉必要仍需干预。既有原文正确区分，补代表性数值使审查更具体。

### 7.3 检测器、对抗生成与触发归因

**A3-05｜P1｜CrossGuard的1,390／1,616／≈202统计单位应显式写出。**
- **定位**：[R5-C L356–356](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L356-L356)，现只报“混合数据”及Fig4 60.33→5.39。
- **证据**：[P034_CrossGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P034_CrossGuard.md) §6：**CrossGuard ACL 2026 Main（CCF-A）** Figure6 ImpForge约**1390条生成的联合攻击样本**是red-team评测库；Figure7显示Guard总训练样本约**1616条**，其中joint-modal implicit类占**约12.5%≈202条**（按百分比近似换算，**不是独立官方公布精确202**）。**现在并无经原始训练/红队索引核实的证据，能确认202恰来自1390中哪202条**。
- **修订**：主文增加上述三量及任务用途，避免使读者把1390全部当作1616个训练实例的一部分，也不要宣称二者完全互斥或确定包含关系。于表6备注训练集类别混合和未知映射状态。

**A3-06｜P1｜CrossGuard Fig4出现未同时呈现的负向例外，ASR同名不同判据。**
- **定位**：[R5-C L356–356](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L356-L356)、表6和[R5-C L376–382](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L376-L382)。
- **直接来源**：[CrossGuard ACL2026正式PDF Figure4](https://aclanthology.org/2026.acl-long.1178.pdf) §5.5（P）及[P034_CrossGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P034_CrossGuard.md) §7–8：**w/o ImpForge→with**，SIUO ASR **60.33→5.39**大幅下降；FigStep **0.12→0.21**小幅上升；MM-SafetyBench 10.20→0.38。文中“consistently reduces”不适用于FigStep的数值级小反例，综述要如实正负双侧。在线MLLM用拒答模板、离线生成模型由GPT-4o-mini judge、Guardrail输入Safe/Unsafe错判作ASR；**不能把guard FNR与响应ASR当作相同的一个分母或标注过程**。
- **修订**：补FigStep的反例，写“绝大多数基准尤其SIUO改善，并非全部单调”；把`red-team攻击强度ASR↑`、`Guard漏判ASR↓`、`生成回答危险ASR↓`分三行，列judge和正类分母；评价数据增加/类别比例改变仍是H/O。

**A3-07｜P1｜ThinkingGuard的反事实“配对”还不是受控单因素实验。**
- **定位**：[R5-C L358–362](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L358-L362)、表6。
- **证据**：[P039_ThinkingGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P039_ThinkingGuard.md)：作者报告**5600个图文实例（2800 Unsafe +2800 Safe）**，训练3864、测试1736，按同index/text和Safe/Unsafe图片成对；图像分别由生成器创建，未取得逐对人工重判记录，未证除了`E_T`以外视觉因素保持相同。表6只写“作者配对、待独立复核”是正确但不够可执行。
- **修订**：增加`pair_id`为评测单位的建议及`Key保持/Trigger变更/其它变化/图像去重/人工安全复标`门槛；将“反事实研究先例”与“已证明单变量风险因果机制”分开。训练测试是否已按pair隔离列O，不能据未核实断言泄漏。

**A3-08｜P1｜ThinkingGuard的Step-DPO消融需要与额外Unsafe监督和token预算对照。**
- **定位**：[R5-C L358–362](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L358-L362)。
- **证据**：[P039_ThinkingGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P039_ThinkingGuard.md) Table3作者报告w/o Step-DPO `Accuracy .756 / F1-Unsafe .779 / Recall .699`，Full `.784/.810/.749`；相应差为 **+2.8/+3.1/+5.0个百分点**。离线SA-MCTS产生轨迹但不直接更新部署模型；偏好DPO蒸馏后才训练权重。关键步骤仅Unsafe数据提供额外偏好，并可能提高该类训练频次和token数。SA-MCTS Judge会读取构造时的`Key/Trigger`提示，部分奖励参数/脚本未公开。
- **修订**：给Fig/Table受控范围内的正收益数值，随后写“不足以证明逐步归因本身的独立因果作用”；建议与`等额外trajectory偏好、Unsafe重采样、同token/step`对照。不要误写MCTS本身是部署时实时推理或五个独立网络。**ACM MM2026 会议CCF-A，实际Main Track/出版状态仍O**。

### 7.4–7.5 安全响应与误拒

**A3-09｜P1｜VLSU“有帮助”与“低过度拒绝”的提升存在已经量化的危险侧代价。**
- **定位**：[R5-C L364–370](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L364-L370)及[R5-C L376–382](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L376-L382)只笼统写安全/帮助权衡。
- **证据**：[VLSU ICLR2026正式PDF摘要及§4.4](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)（P）：Gemini1.5改变**推理时行为prompt**从Harmless到Helpful时，Borderline拒答率 **62.4%→10.4%**，Unsafe拒答率 **90.8%→53.9%**；不是重训/SFT、不是二分类F1，也不能泛化所有模型。
- **修订**：把这组正反数值作为本综述**真正支持的条件性权衡案例**，与MOSSBench安全请求误拒及Meerkat输出对齐方法进行任务区分；不能只写“帮助性升高”或把低Borderline拒答率当普遍改善。

**A3-10｜P1｜MOSSBench的安全主集不是全员无异议安全金标，正负对照不是300严格一一配对。**
- **定位**：[R5-C L366–366](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L366-L366)和表6；目前正文已说“少量意见认为不安全”及“不全部配对”，需量化。
- **证据**：[R2B_B4a_02_MOSSBench](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md)：**ICLR2025 Main（CCF-A）**作者主基准300安全意图样本，但人评约**9%**认为无法在无害前提下安全回答；所查公开对照数据244 ID与300中244对有映射，其余56未配对。Safe ARR=回应行为Judge判Refusal比例；并非直接证输入GT三条件安全。
- **修订**：表6加`300安全主集/244已映射有害对照/9%争议`，涉及“过度拒绝率”时写**相对于论文按人工与政策构建的安全主集**，不外推为全体客观合法请求；对照单位按pair匹配，而不是称所有300为严格单因素。

**A3-11｜P1｜Meerkat-VL的自验证是带规范性风险说明的同Actor训练期评分，不等于独立重新看图。**
- **定位**：[R5-C L368–370](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L368-L370)与表6；原稿已提“评分不重新接收图片”，正确，但没有说明**评分器额外掌握的答案级监督**的性质和比较证据。
- **证据**：[P040_MeerkatVL](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P040_MeerkatVL.md)（**ICML2026 Main，CCF-A**）。Meerkat-Safe训练材料作者报告8436，而所查公开浏览器8466的版本差O；训练期评分由同一Actor读取已经生成的risk analysis/answer以及 `user_intent / harmful_intent / safety_warning` 等规范性GT文本，不重新读视觉原图；NPSV四分数结合一致性惩罚DPCA经GRPO更新，惩罚为`|p_h-a_h|+|p_s-a_s|`，同低分时也可得到零不一致罚；不构成事实真值独立检验。**正式ICML论文主表和各阶段等预算消融原卡明确未逐项核对**，不能本轮编结果百分比或声称确认NPSV独立增益。
- **修订**：在§7.4建立`训练冷启动risk GT → 训练自评额外规范说明 → GRPO优化 → 推理仅原始图文与问题 → 输出回应Judge`的字段图；表达“作者报告综合安全/帮助收益，独立归因尚O”，别以规范自评分准确率替代视觉风险感知独立GT。

### Ch7正面综合和审稿定位

本章可以写成“哪些失败属于哪一层”：VLSBench主要审**文本可代图信息/输出拒答模式**；VLSU提供**分开人审的输入风险GT**；MMSafeAware在联合标签上同时有unsafe与oversafe设计；CrossGuard/ThinkingGuard优化**输入Guard/触发归因**；MOSSBench/VLSU/Meerkat检验**安全侧误拒与合法帮助**。**这些已是真实存在的任务先例，不是新发明的问题**。相反，用一个ASR或分类F1统称“多模态安全能力”才是错误比较。

## 三、Ch8｜跨论文机制综合与高优先级遗漏

**A3-12｜P0（继承A0-03）｜已核正式ICLR2026 CCF-A ExPO-HM遗漏，使“解释—检测—安全”方法比较缺一个直接竞争方法。**
- **位置**：[R5-C L388–396](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L388-L396)、[R5-C L406–412](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L406-L412)、[R5-C L432–436](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L432-L436)；应关联Ch7 [R5-C L354–370](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L354-L370)；`references.bib`现有46条不含`ExPO-HM`，本轮再次按字符串检查已确认。
- **证据**：[ICLR2026 ExPO-HM正式出版页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)（F）及[P027_ExPO-HM](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)（用户已有正式PDF精读；P+S/O）。作者提出policy manual warmup SFT、细粒度↔二分类课程GRPO、**Conditional Decision Entropy (CDE)**奖励/评价；是“解释后检测”而非Safe–Safe–Unsafe标注，不可简单并入T5严格组合风险数据。
- **已归档具体正面证据**：HatefulMemes binary macro-F1 `naive GRPO 74.5→ExPO-HM 81.1`（+6.6pp），相对强直接方法RA-HMD 80.2仅**+0.9pp**；课程/PolicySFT/CDE递进消融有分数，但各阶段同时改变协议；CDE与解释judge评分负相关不证明解释内容因果忠实。当前公开训练脚本与论文课程比例/rollout组数尚有版本差，不能擅自说论文复现通过。
- **精准修订**：新增BibTeX正式条目；Ch7 §7.3或Ch8 §8.1/8.3增一小节或一段，按`Y预测目标、额外知识、SFT→RL/DPO优化变量、指标及独立对照、解释忠实性证据`与SMARTER/ThinkingGuard/Meerkat-VL同表对照。**这是覆盖修复，不是补一段“已有人研究”就算关闭P0**；不得把CDE小理解为推理因果已证。

**A3-13｜P0（继承A0-01）｜第8章现在主要是正确的“禁强推论/应做对照”集合，尚未兑现第1章的原创跨域综合。**
- **定位**：§8.1 [R5-C L388–396](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L388-L396)及表7、§8.2–8.6 [R5-C L398–438](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L398-L438)。
- **问题**：把五类方法从词典、对比、检索、融合写到偏好优化可以帮助检索，但没有回答`给定GT和信息预算时，哪种额外监督改变哪个可证失败机制；何时正收益与反例并存；已有实验证实到哪一步`。例如“没有同预算所以不能归因”多次重复，但既有定稿卡其实提供了不少同论文**正向或负侧直接对照**，可写出原稿以外的高水平机制论断。属H级学术审稿判断，**不是声称其他综述从未做这些研究**。
- **建议必须交付的三条跨域“**条件性规律**”（每条至少2篇不同任务）**：
  1. **可观测意义的先验预算规律**：Silent Signals给定社群定义做instance WSD、FA-Net固定目标类+目标未标数据、FETCH留出已知词条做type discovery、SeTox依检索判安全。**正面**：先验越可结构化，便越能定义封闭GT与可复核指标；**边界**：不能外推“真实未来开放词义已解决”；**证据**：作者方法协议P + 本稿H，并非跨论文因果数值。
  2. **解释监督的目标漂移规律**：ImpCon配implied statement促进特定分类，SMARTER以gold标签构造DPO preference，**ExPO**的policy+CDE改善作者报告的检测，ThinkingGuard借teacher trigger/轨迹蒸馏，Meerkat将规范risk description进入自评。**正面**：解释/规范辅助通常以额外监督、奖励或候选空间塑形不同输出；**边界**：F1与解释judge分不等于忠实视觉/心理解释、同预算独立增益各异。可给每项可查表/条件、至少1个反向或仅小增量证据（ExPO对RA-HMD +0.9pp、ThinkingGuard Unsafe重采样混杂）。
  3. **联合安全的双侧决策边界规律**：MMSafeAware的2:1 unsafe/oversafe、VLSU Harmless→Helpful呈两侧拒答互换、CrossGuard SIUO FNR大降但FigStep小退、MOSSBench安全请求误拒。**正面**：同一政策下危险漏判与正常误拒可以分别优化和报告，提示词/训练数据会改变权衡；**边界**：横跨P_in/R_beh的数值不可直接拼成同一Pareto点，需共享样本/policy/judge才能比较。
- **验收**：T7和§8每条规律分别有`具体论文×可测目标×必要信息×作者真实提升×反例/无效处×尚无的因果控制`；重写引言§1.3指向该有形分析产物。补三条就可避免空泛“首次综述广义隐晦”的不实主张。

**A3-14｜P1｜表7把输入Guard、解释DPO与回应GRPO合并为一类，无法表达可比机制与信息权限。**
- **定位**：§8.1 [R5-C L394–396](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L394-L396)、[R5-C T7_Method_Families](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T7_Method_Families.md)最后一行“偏好/Guard [CrossGuard;ThinkingGuard;Meerkat]”；遗漏SMARTER/ExPO与独立的红队数据生成器的作用。
- **证据**：[P034_CrossGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P034_CrossGuard.md)、[P039_ThinkingGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P039_ThinkingGuard.md)、[P040_MeerkatVL](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P040_MeerkatVL.md)、[P027_ExPO-HM](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)及[P030_SMARTER](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P030_SMARTER.md)。CrossGuard红队生成`PPO`目标是攻击文本候选、Guard本身`LoRA+CE/SFT`判输入；ThinkingGuard轨迹+Step-DPO蒸馏`P_in`; ExPO-HM生成解释后标签、SFT/GRPO/CDE；Meerkat-VL输出安全帮助文本、cold-start/Actor self-score/GRPO；SMARTER DPO label+explanation。**优化器名称一样、被优化的输出和教师字段未必相同**。
- **修订**：T7按`产生训练样本`/`输入标签Guard`/`解释式标签检测`/`回应质量对齐`四个**任务×优化目标行**分别写；附实际训练Y、是否有gold risk/trigger/policy知识、Judge来源、同预算证据、失败副作用。避免把所有“RL+解释”类比为单一技术族。

**A3-15｜P1｜表6遗漏被正文反复引用的SIUO，风险输入/回应ASR混淆风险较大。**
- **定位**：§7.2 [R5-C L350–352](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L350-L352)、§7.4 [R5-C L368–370](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L368-L370)、§8.5 [R5-C L424–426](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L424-L426)；[R5-C T6_Multimodal_Safety](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/tables/T6_Multimodal_Safety.md)无SIUO行。
- **证据**：[P041_SIUO](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P041_SIUO.md)：**SIUO 为NAACL2025 Findings（会议本身CCF-B，Findings并非主会）**；主要衡量“表面安全图文可引起不安全输出”的生成行为，其中作者参考警示、答案与judge作为判断协议，非输入三标签`y_I/y_T/y_J`共享金标；原作者报告167人工样本+102 AI辅助等结构，公开版本可达O。
- **修订**：表6新增`SIUO：输入表面安全/潜在组合风险样本；显式输入分类非主要评测；响应Safe Rate/ASR与judge；版本及参考答案/安全警示`行；与CrossGuard Table1所使用的SIUO分母区分。**不把旧NAACL Findings误标CCF-A**。

## 四、Ch9｜结语/展望：将重复原则换成可研究的优先议程

**A3-16｜P1｜§9.2与8.2–8.6过度同义重述，缺X/Y/G/E、数据可用性与最小判断的优先路线。**
- **位置**：[R5-C L450–456](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L450-L456)。
- **证据**：前一章已阐释“记录GT、去模态、评价双侧安全”，结语几乎逐项重复。R5-E/R4研究目标并不要求承诺新模型/新大规模数据，也不应宣称这些问题学界完全无人研究。
- **建议替换为3条明确、带先例和成本边界的研究路线**：
  1. **R1输入组合可靠性**：X=(I,T)或控制替换；Y=`P_in safe/borderline/unsafe`；G=VLSU三条件人工GT（仅公开可用子集严格S-S-U≈35），E=条件错误+两侧召回+分层误差；Kill Test=冻结同一VLM分别I/T/IT，先做可达/版本审计，不凭35小样本宣称普适机制。
  2. **R2解释真实性与训练特权**：X=图文+可用/不可用规范risk字段；Y=解释+输入类别或回应；G=已有标签与独立人工核验样本（缺则明确不能测解释faithfulness）；E=类F1、judge解释支持、同预算干预后判别变化；Kill Test=ExPO/ThinkingGuard/Meerkat固定推理或文本奖励脚本消融，同输入预算对照，不承诺能原样重训8GPU方案。
  3. **R3双侧风险—帮助边界**：X=同政策下安全、危险与边界图文；Y=显式风险P_in及R_beh/Q_out；G=VLSU/MOSS/MMSafeAware各自不同，必须先修订可共用子集与分歧标签；E=unsafe recall、safe false positive、safe refusal及helpfulness分列；Kill Test=相同模型对Harmless/Helpful提示、相同judge+人工审核抽样；禁止跨不同数据集拼“统一安全Pareto”。
- **验收**：每条给研究问题、已有竞争工作和“何时只能得相关性结论”，避免空泛“应做更多工作”，也不要为填结语而承诺新增大规模样本。

**A3-17｜P2｜删除图表编辑任务语句，保证第8章为论文而非项目交接稿。**
- **位置**：§8.5 [R5-C L428–428](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L428-L428)“图6作为候选图暂未收入本稿；方法族与瓶颈的定性关系已由表7承担”。
- **问题**：属于工作流编排语言，不是给领域读者的学术结论。
- **修订**：删整句；如需说明图表布局，用正式论文附录编辑说明，不进入正式稿正文。相同级别的“本项目静态审计发现”可保留有严格源码附录时，但不可当成果口号。

## 五、R6-A3可以新增的可证学术结论（建议写到正文的“正面证据”）

| 主张 | 真实实证支持 | 失败边界/机制推断级别 |
|---|---|---|
| **联合标签与独立模态的分组评测能揭露传统总体准确率不易呈现的错误。** | VLSU Fig5约34%来自joint预测**错误**且两个单模态正确的情况（P）；MMSafeAware unsafe/oversafe分组可检验不同错误侧（P）。 | 不能说模型内部视觉处理因果失败已被证明；label来源和policy/数据版本仍需核。 |
| **少量特定联合风险训练样本可能显著降低Guard在同类数据的漏检。** | CrossGuard论文混合训练集约202 joint类别，SIUO w/o data ASR60.33→with5.39（P）；FigStep 0.12→0.21为限定反例。 | 数据总量/类别比例变化、攻击或Guard ASR的judge区别需固定；不能将改进归新检测器或PPO必要性。 |
| **模型优化解释/决策后可以改善该协议下分类，但解释的独立因果忠实性仍未获保证。** | ExPO-HM naive GRPO→组合方案二分类macro-F1 74.5→81.1（P），ThinkingGuard w/o Step-DPO→Full Unsafe F1.779→.810（P），均存在训练预算/教师信息差异。 | 未证解释真的参与风险决策；两种论文不共享任务GT/训练数据，不可横排绝对F1。 |
| **降低不必要拒绝可能同时降低危险输入拒绝。** | VLSU Gemini1.5 prompt对照 Borderline拒答62.4→10.4%、Unsafe拒答90.8→53.9%（P），MOSSBench提供安全误拒压力基准。 | 拒答率不是安全且帮助性评分、也不是模型显式输入风险Accuracy；必须在共同政策/数据下评价双侧。 |

这些结果都已在现有馆藏得到支持；本稿的学术贡献应是**把成功条件、需要的额外监督及不可迁移的失败机制组织成可检验比较**，而非声称自己做了新模型训练或给出单一SOTA。

## 六、R6-Fix优先工作与边界

1. **先P0**：把ExPO-HM补入Ch7/Ch8/T7及46条Bib以外的新条目，不能仅加标题；为第8章落地三条跨域正向条件规律，并反向修订引言贡献。
2. **修第7章核心证据**：CrossGuard 1390/1616/≈202 + FigStep反例/ASR单位；VLSU 34%条件分母+三级标注质量+响应prompt反向权衡；ThinkingGuard配对/Step-DPO等预算边界；Meerkat自验的风险GT文本条件。
3. **扩表6、表7但不堆数字**：表6加入SIUO、各自输入GT分层/风险回应指标/Judge/发布状态；表7拆清Guard+解释DPO+GRPO训练阶段、先验知识、正面效果/负面例。
4. **证据版本与来源链接**：R6-A0-02的公开源码immutable commit门槛仍适用；MMSafeAware图像文件数、Meerkat同Actor评分、CrossGuard奖励实现、ThinkingGuard反事实信息都不可用作者正式论文Bib单独证明本项目S级观察。未获ACM MM正式出版详情，不擅将作者声明升级为已核Track。
5. **缩/改§9.2**：不重复第8章方法规则，改为3条有数据、有X/Y/G/E、有最低成本诊断且有明确不能强推断之处的未来议程。
6. **开放项保留**：VLSU论文/CSV差28、S-S-U37/35、Meerkat 8436/8466、ThinkingGuard真实配对属性、ExPO/Meerkat正式训练版本、拒答Judge提示，不能因R6-A3审稿完成就写为CLOSED。

## 证据导航

- [R5-C源稿固定commit](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md)
- [R4-07章节主张矩阵](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)
- [R5-E引文与主张门槛](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/R5_Citation_and_Claim_Gates.md)
- [P027 ExPO-HM](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)
- [P034 CrossGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P034_CrossGuard.md)
- [P038 VLSU](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md)
- [P039 ThinkingGuard](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P039_ThinkingGuard.md)
- [P040 Meerkat-VL](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P040_MeerkatVL.md)
- [P041 SIUO](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P041_SIUO.md)
- [B4a MSS/MOSS/MMSafeAware](https://github.com/YuSun-WK/implicit-content-research/tree/main/03_survey/R2_literature_extension/B4a_reading)
- [VLSU ICLR2026正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)
- [CrossGuard ACL2026正式PDF](https://aclanthology.org/2026.acl-long.1178.pdf)
- [ExPO-HM ICLR2026正式论文页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)

**R6-A3审稿结语**：第7章不是失败章；真正阻断高水平综述投稿的是第8章论证的原创比较产物不足和ExPO-HM覆盖缺口（继承A0 P0），第9章须完成面向研究者可操作的论证收束。所有17项问题保留OPEN供R6-Fix与A4统一裁决；不宣称原作者训练协议有问题已被运行证实。
