# R6-A｜Overall Verdict — R6-A0 总体学术审查（工作稿）

> 2026-11-09｜审查阶段：**R6-A0 完成；R6-A1～A4 未开展正式逐章终审**。  
> 审查者立场：独立学术综述审稿，不代替原论文复现、不直接修改 R5-C，不把内审发现当作原论文违规事实。  
> 源稿固定快照：PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)，HEAD `c04d6a23e864923acd64c192c8b05dc597c2bb90`，Draft/Open；全稿 [Survey_Full_Draft.md](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md)（509行、九章、46小节）；参考 `references.bib` 46条。R6-A 独立分支从 main 建立，**不修改 R5-C 本文**。

## 0. 审稿裁决

**CONDITIONAL PASS FOR ACADEMIC REVISION；NOT YET A HIGH-QUALITY SUBMISSION-LEVEL SURVEY DRAFT。**

稿件已达到**结构完整、边界较清、可用于集中学术修订的综述草稿**水平；但以高水平专业综述投稿为目标，不能只把现有稿件的“谨慎描述”视作已完成批判性综合。核心阻碍在于：(i) 本文独特综述贡献尚未用对照产物充分证明；(ii) 第8章虽有较多评价戒律，跨领域的**正向机制综合与可迁移结论**仍不够具体；(iii) 有重要直接邻近论文未被纳入，以及若干代码静态审计断言缺少适合正式读者的可独立复核出处。

这**不是**“九章框架不成立”或“需要重写91篇精读”；保留第1–9章主体和现有T1–T6五轴框架，采用限点修订更高效。

### 审查维度（非量化打分）

| 维度 | A0判断 | 核心理由 |
|---|---|---|
| 选题与目标读者 | **有价值** | 广义隐晦信息的无害语用→社会规范性危害→多模态联合风险差异确实值得跨界整理；目标适合NLP/安全研究者。 |
| 定义与边界 | **较好，有可消解歧义** | §1.2/§2.1明确“工作性范畴”，不把含义/修辞/编码/有害互作同义；但T5是T4的联合条件特殊情形，T6为邻接行为任务，仍须在正式任务图中更直观地显式标层级。 |
| 研究脉络 | **基本成立** | Ch3→Ch4→Ch5、Ch6→Ch7衔接合理；拒绝“PLM→LLM→VLM单线取代”。 |
| 方法机制解释 | **中等偏好、深度不齐** | (RSA)²、FA-Net、MGMCF、DOSE、CrossGuard、ThinkingGuard均有可识别技术细节；Ch6.6仍偏薄，Ch8方法跨域比较不充分。 |
| 证据审慎性 | **相对突出，但外部复核不足** | 已对AUTALIC、MCIB、MultiMM、VLSU、ThinkingGuard等显式降级因果主张；然而正文“本项目静态审计发现”需要源码永久链接、版本和具体观察证据，否则审稿人难以核验。 |
| 与现有综述的实质区别 | **尚未充分成立** | §1.2相邻综述表只覆盖四篇，第8章原创分析成果主要为评价建议；与已有语用/修辞/有害审核/MLLM安全综述的“新增解释力”待展示。 |
| 跨研究领域综合 | **主要待加强项** | T7过于概括，尚不能单凭它回答“同类方法跨任务何时有效/无效、依赖何种额外监督、已有何种独立控制”。 |
| 投稿成熟度 | **暂不通过** | 上述学术P0及R6-V图表真实渲染/引文出版门槛未关闭。 |

## 1. 已经实现的实质学术价值（应保留）

1. **工作性范畴与负边界**：§1.2 [L25–45](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L25-L45) 与§2.1 [L64–80](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L64-L80)明确隐含不等于恶意、语境依赖不等于非字面、风险判断受规范约束。避免了错误地把广义领域缩成implicit hate。
2. **五轴及任务协议意识**：§2.2–2.5 [L82–128](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L82-L128)区分机制、任务、模态、额外信息与GT/E；说明T5仅为更特殊联合风险条件、T6不等于输入危害预测。形式化记号是综述工具而非自然科学定律。
3. **多篇方法有真正机制内容**：§3.2详解(RSA)²策略兼容与先验；§4.4写FA-Net对比/伪正对/熵；§6.3区分MGMCF对象交互、M3UCD共享LoRA与DOSE私有/共享专家；§7.3区分CrossGuard生成Guard与ThinkingGuard轨迹/Step-DPO，而非仅列作者和F1。
4. **学术克制是优点**：AUTALIC的语境质性证据不被伪装为同模型量化上下文消融；MCIB的结构消融不被改写为CIB去捷径的独立因果收益；VLSU论文/发布CSV的分母分版本；风险输入GT/显式预测/拒答/安全帮助性严格区分。
5. **已有跨章桥梁**：§4.6“发现词→实例消歧→意义→危害”、§6.7“非字面意义→联合风险”、§8.5“风险判断→安全回应”的断裂分析有意义，后续应将这些桥梁升级为真正的横向比较产物。

## 2. 三项阻断高水平初稿认定的P0

**P0-A0-01：综述增量尚未被具体比较产物证实。**  
位置：§1.2 [L25–45](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L25-L45)、§1.3 [L46–51](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L46-L51)、§8.1–8.6 [L384–438](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L384-L438)。正文主张“本文采用交叉问题驱动……同一框架……”，但独到结论仍偏编辑性组织；R5-E相邻综述台账已经列出更多重要重叠综述，本稿只呈现四篇，不能仅靠“覆盖多个领域”赢得高水平综述的贡献。**修改门槛**：新增精简且可核的“prior survey × 分析单位 × 本文产物”矩阵；让第8章至少产出2–3条基于不同任务原论文对照的**条件化规律**，明确反例、证据等级与适用边界；不要求做未经完成的PRISMA或夸称首创。

**P0-A0-02：关键静态代码审计主张无法由本稿学术引证直接复核。**  
位置：§3.3 [L150–155](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L150-L155)；§5.2 [L230–239](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L230-L239)；§5.5 [L256–263](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L256-L263)；§6.4–6.5 [L298–317](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L298-L317)。如“测试 gold 情绪”“测试标签用于PPO权重寻找”“MSE跨样本广播”“原文残差旁路”等是**对特定公开代码版本的本项目独立观察**，普通论文书目引用无法支持该代码状态。**修改门槛**：为每条保留在正文的 S 级判断增加可公开核验的固定commit、源码文件/行号、观察范围及“未证正式实验使用此版本”；在公开附录建立可追溯 `claim→code→version→limitation`；无法提供可复核证据的条目降为“本项目待核风险”，或从主文删去具体源码判断。论文作者结果仍按P级呈现。

**P0-A0-03：遗漏与本文主轴直接相关、已在R4规划中的ExPO-HM。**  
位置：§7.3–7.4 [L354–375](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L354-L375)、§8.1/8.3 [L386–413](https://github.com/YuSun-WK/implicit-content-research/blob/c04d6a23e864923acd64c192c8b05dc597c2bb90/03_survey/R5_full_draft/Survey_Full_Draft.md#L386-L413)。R4-02把 **P027 ExPO-HM** 明确设为Ch7 Core；R3-A2对其解释后检测、政策手册SFT、课程GRPO、条件决策熵与忠实性不足已有正式精读支撑；R5-C正文与Bib却没有该项。它是ICLR 2026 **CCF-A** 正式研究，不是严格S-S-U联合风险GT，故**不能**把它误加为joint-only例子。**修改门槛**：在§7.3/§8.3或§8.1加一个与SMARTER/ThinkingGuard/Meerkat-VL的**目标—监督—奖励—解释证据**对照段，限定“低决策熵≠解释忠实”，补正式书目和正文引用；不必新增长篇精读。

## 3. 需要修但不推翻整体定位的P1

- **P1-A0-04：T5/T4/T6的分类关系呈现不够直观。** 任务表并列六行，正文却正确承认T5属于T4中特定联合模态条件、T6是行为层；表2及图2宜显式添加“层级/交叉”列，不要求重做T1–T6。
- **P1-A0-05：选文从91条候选到46条主文引用缺可审的选择说明。** §1.4已说明非系统综述，但未逐项交代代表文献选择逻辑及未采纳候选的分布；建议增加叙述性综述的“检索范围、截止时间、主讲/辅助、摘要级禁强证”的简表，不伪造严格系统检索。
- **P1-A0-06：现有综述表未充分利用R5-E已经核验的相邻材料。** 至少补与广义框架直接重叠的隐喻处理综述和LVLM安全综述；注明比较只基于官方摘要或出版页者，不擅称读过全文。
- **P1-A0-07：方法“解决了什么”偏弱于“没有证明什么”。** Ch8/表7大量结论正确但抽象；应为每类方法给出可验证的正向作用、改进的具体失效对象、有效所需先验和不能推导的结论；避免只用泛化的“需同预算”代替跨论文分析。
- **P1-A0-08：第6.6多图路线证据过薄。** 目前仅摘要级MMSD3.0，且先前R5-C已主动记录这一点；不应写未经全文核验的机制。可缩短该节或针对一篇正式原文做小规模定点核验。
- **P1-A0-09：第9章仍在复述第8章的一般审计原则。** 建议改为3–4条优先级明确的、具有X/Y/G/E和最低实验条件的研究议程，保持非“无人研究”措辞。

## 4. 投稿定位与优先改法

**建议定位**：`Critical Narrative Survey of Implicit / Non-literal / Coded Meaning and Contextual Multimodal Risk: Task–Evidence and Evaluation Protocols`。中文原题可以保留，但引言必须用**可显示的综合产物**解释该跨域范围为什么形成新的研究认识，而非只因主题宽。

不建议改为PRISMA系统综述；不建议把T6安全对齐扩为独立通用对齐综述；不建议为填满91篇而逐篇增加摘要；不建议把未做的代码/数据复现写成自己证明原论文的事实。

推荐顺序：**先P0-A0-01（贡献与Ch8产物）→P0-A0-03（直接论文覆盖）→P0-A0-02（S级证据可复核）→P1定义/选文/章节结构→逐章A1–A3核数字→A4正式裁决**。R6-V另线处理图表实际渲染、BibTeX和DOCX/PDF，不以视觉审计替代学术审计。

## 5. 审查边界及来源

本轮确已直接阅读R5-C第1–9章、T1/T2/T7三张结构性表、R5-C移交/冲突/开放问题、R4-07/08、R5-E相关综述比较及引文门槛、R2-C/R3-A技术综合与P027卡。**A0只是总体门槛审查**；T3–T6其余表的逐条内容、全部46个BibTeX字段、正式PDF每一数字、原论文及代码逐路径重跑、SVG真实渲染**不在本次已完成范围**，必须由R6-A1～A4或R6-V继续。A0所列论文级异议均只作“补证/降级/核验”指令，未声称有论文作弊或错误结论已证。

- [R6任务书](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R6_review/R6_Kickoff_and_R5C_Gate_20261109.md)
- [R5-E相关综述对比](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/Related_Surveys_Comparison.md)
- [R5-E引文门槛](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/R5_Citation_and_Claim_Gates.md)
- [R4-02论文分配](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_02_Paper_Allocation.md)
- [R4-07章节证据矩阵](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)
- [R2-C综合](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_synthesis/R2C_Cross_Domain_Synthesis.md)
- [R3-A2技术演化](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_evolution/R3A_Method_Evolution.md)
- [P027 ExPO-HM正式精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)
