# R3-A4｜广义隐晦信息综述：覆盖与证据终审（审阅稿）

> 2026-11-08｜**REVIEW DRAFT / 尚未用户定稿 / 未合并main**。
>
> 本轮完成**现有馆藏与R3叙事的证据映射、出版类型与数据协议审计**，而不是重新进行全领域搜索或模型训练。本文基于main的R0/R1/R2-C及R3-B AUTALIC定稿、R3-A1/A2及独立R3-A3分支，并**有条件参考**另一个R3-B分支的MCIB审阅稿。R3-A3和本文件均未获正式定稿，R3-A1也仍为审阅稿。
>
> 等级：2026 CCF第七版按**刊会**核查；正式发表、Main/Technical、Findings、Workshop、D&B、作者录用和代码可复现是不同概念。本文不使用“91篇都精读/复现/CCF-A”说法。
>
> 审计证据等级：**PF**=已完成正式论文全文/附录精读；**PA**=官方正式元数据/摘要、尚无全文机制审计；**S**=本项目既有公开数据或代码静态核验；**H**=研究者跨论文解释性推断；**O**=未核实，禁止表述为已证事实。PF/PA并非实际GPU复现。

## 1. 文献覆盖实际口径（先核计数，避免以文献库代替领域）

- **现有去重目录91篇**=R0的P001–P041共41篇 + T001–T018共18篇（合计59） + R2-A临时编号R2A-001–032共32篇。R2-B中16篇已形成正式单篇精读卡、另外16篇是目录元数据/候选深度，不等于“未发表”；R0阅读卡本就包含不同完成状态，不能把91统一写作“精读”。[S：R2-C资源盘点]
- R0单标签馆藏曾T3=0，只表示**原59篇按R1映射尚无T3主任务**；DRInQ、VAGUE、(RSA)²、意图表征论文已经补强语用线，不应宣称全领域缺少T3。[PF/PA/H]
- 本项目目前对人工标注、领域/文化、图文、视频/音频的覆盖并不平衡：T4有害分类与图文安全研究较丰富；严谨实际时间外编码义、开放语用解释、社群立场、长时对话、多图/视频语义监督较薄。这里只是**项目馆藏覆盖判断**，不是“该领域从未有研究”。[H/O]
- R3-B新状态：**AUTALIC R2A-013**已经全文精读定稿并merge main；**MCIB R2A-024**在分支 r3b-mcib-targeted-review-20261108 有7,324字的完整机制审阅稿，但**尚未定稿、尚未并入main**。不能让R3-A1/A3早先“均未精读”的旧句继续当作最新版事实。[S]
- 本轮再次确认AAAI出版页：MCIB AAAI 2026, Vol 40(31), Technical Track Machine Learning VIII、2026-03-14已正式出版。[PA; https://ojs.aaai.org/index.php/AAAI/article/view/39874]
- 2026-11-08时ACM MM 2026会议计划11月10–14举行；P039 ThinkingGuard已具作者仓库、arXiv、DOI 10.1145/3767308.3835707和录用线索，但**未独立获得ACM官方具体会议论文页/track核验**。不得仅凭DOI和作者引用在统计中计作“已核实正式出版的ACM MM主会论文”。此为出版审计待关闭项，而非否定其已录用。[S/PA/O]
- **没有独立端到端训练复现**。已有S证据可指向脚本、JSON/CSV、模型流程或版本冲突，但不能自动推导作者正式结果错误。

核对依据：
[R2-C覆盖审计](../R2_synthesis/R2C_Coverage_and_Evidence_Audit.md)；
[R2元数据与证据冲突](../R2_registry/Metadata_and_Evidence_Conflicts.md)；
[AUTALIC R3-B定稿](../R3_targeted_reading/R3B_01_AUTALIC_FINAL.md)；
[AUTALIC三争议审计](../R3_targeted_reading/R3B_01_AUTALIC_Three_Issue_Audit.md)；
[MCIB R3-B审阅稿（独立分支）](https://github.com/YuSun-WK/implicit-content-research/blob/r3b-mcib-targeted-review-20261108/03_survey/R3_targeted_reading/R3B_02_MCIB_REVIEW_DRAFT.md)。

## 2. R3-A3九个临时章节的主张与证据匹配

| 章节/任务 | 需要在综述中成立的核心结论 | 可优先引用的直接论文及出版/CCF | 当前证据级别 | 不可越界表述；终审动作 |
|---|---|---|---|---|
| **Ch1 概念和范围** | Implicit、Figurative、Coded、Obfuscated、Subtle、Harmful不是同义词；T1–T6是项目工作性分类 | P011语用综述 ACL 2025 Main **A**；P023 CodedLang ACL 2026 Main **A**；R1框架 | PF+H | **不是**统一学界公认“广义隐晦信息本体论”；定义须标为本文操作性工作定义；语境依赖≠全部非字面。 |
| **Ch2 理论和语用** | 字面语义与语用含意/间接言语行为的评价对象不同；上下文可改变候选解释 | Grice/Searle 1975理论（不按CCF-A/B）；P020 (RSA)² ACL 2025 Main **A**；DRInQ ACL 2026 Main **A**；VAGUE ICCV 2025 Main **A** | 理论+PF | DRInQ为受控五选一、人类共识而非心理意图；VAGUE为视觉情境四选一，非实际行动/风险GT；(RSA)²主要增益与意义先验高度关联。 |
| **Ch3 修辞表达/意义** | 识别有无修辞与源目标映射、对象、意图、解释是不同监督目标 | P003 MultiMM ACL 2025 Main **A**；R2A-017 M3UCD AAAI 2026 Technical **A**；R2A-019 DOSE ACL 2026 Main **A**；P035 EmoBi ACL 2025 Main **A** | PF+S | MultiMM所查测试输入gold情绪；M3UCD任务同预算迁移未证；DOSE小训练子集有选项捷径风险；这些不证明解释忠实。 |
| **Ch4 编码、狗哨和词义变化** | 词项type发现、给定释义的instance消歧、固定候选解码、危害判断是四种不同任务 | Silent Signals ACL 2024 Main **A**；FETCH! ACL 2025 Main **A**；FA-Net AAAI 2024 Technical **A**；CodedLang ACL 2026 Main **A**；SeTox ACL 2026 Main **A** | PF+S | FETCH! 80%为**已有参考词典留出**，非真实历史新义；Silent Signals大规模主集LLM筛选非全部人审；SeTox model-unknown相对基础模型、在线搜索带证据漂移。 |
| **Ch5 隐晦有害与语境** | 识别隐喻/社群词汇不足以直接推出有害性；引用、立场、社群与规范的GT应独立定义 | P001 ToxiGen ACL 2022 Main **A**；When People are Floods ACL 2025 Main **A**；Sheep's Skin ACL 2025 Main **A**；**AUTALIC ACL 2025 Main A，R3-B已定稿** | PF+S+H | Flood论文人工GT仅隐喻源域、非非人化GT；Sheep合成漏检不能唯一归因T2失败；AUTALIC含显/隐而无逐例显隐标签且无同模型删语境消融。 |
| **Ch6 多模态非字面理解** | 跨模态关系、对象/源目标、多任务与视觉蕴含拓展单标签识别 | P019 V-FLUTE NAACL 2025 Main **B**；MGMCF AAAI 2025 Technical **A**；M3UCD AAAI 2026 Technical **A**；DOSE ACL 2026 Main **A**；MMSD3.0 CVPR 2026 Main **A（PA候选）** | PF + PA + S | image+text不等于所有例子的两模态必要性；V-FLUTE白图对照只说明统计增益；MGMCF测试辅助域及公式/代码待核；多图MMSD3.0尚不能用全文方法归因。 |
| **Ch7 联合风险检测** | 讨论文本/图片/联合风险GT及其有时不一致，区分特殊S-S-U与一般meme风险 | Hateful Memes NeurIPS 2020 **A**；P037 VLSBench ACL 2025 Main **A**；P038 VLSU ICLR 2026 Main **A**；P034 CrossGuard ACL 2026 Main **A** | PF+S | VLSBench主要风险/输出行为评测不能作平衡二分类金标；VLSU公开8159 vs论文8187、含not_sure，严格S-S-U公开35条且test-only；CrossGuard生成风险与真实环境GT仍有区别。 |
| **Ch8 安全响应边界** | 输入危害预测、模型拒答/警告、实际安全与有帮助的回答分开评测 | MSSBench、MOSSBench ICLR 2025 Main 均**A**；MMSafeAware ACL 2025 Main **A**；Meerkat-VL ICML 2026 Main **A**；ThinkingGuard作者录用稿 ACM MM **A刊会，正式发表/Track待核** | PF+S；P039状态O | MOSSBench安全GT部分存在人工争议，对照非全量300；MSSBench IF Judge是回应而非独立分类；Meerkat自验证使用风险文字特权监督；拒答率≠准确风险理解。 |
| **Ch9 方法与开放挑战** | 方法进步不仅是骨干代际，也包括词义先验、领域迁移、训练/测试信息预算、解释可靠性与捷径诊断 | P032 ImpCon COLING 2022 Main **B**；FA-Net AAAI 2024 **A**；RV-HATE ACL 2026 **A**；ExPO-HM ICLR 2026 **A**；**MCIB AAAI 2026 Technical A** | PF+S+PA(摘要)+R3B-DRAFT | 不把训练预算/数据差异、模型自信或可视化等同机制证明；MCIB审阅卡暂只能“有条件支持”，核心指标与源码疑点未归档定稿。 |

**本表区分“发表论文有此任务/作者报告结果”与“由模型实验已严格证明某中间机制”。** Ch2–Ch8论文有相交归属，正式R4可在交叉章节短引而不是重复逐篇长述。R3-A3的9章仍是**逻辑候选**，不是R4不可更改目录。

## 3. 需要R4明确标注等级的18个核心论断

**等级建议**：A=可以作为直接的任务/数据/相对结论写入（保留限定）；B=可以作为有依据的跨论文解释性观点，不得称“证明”；C=必须降级/条件化或待核；D=明确禁止/被已有论文反驳。

| ID | 论断 | 评级 | 依据、限定与处理 |
|---|---|---|---|
| CL01 | 广义隐晦信息可用T1–T6描述多类任务 | **B** | R1/R2自定义综述框架，不是全球共识本体；T5为T4特殊联合条件，T6邻接应用。 |
| CL02 | 语言学有早于隐式仇恨的语用/修辞理论传统 | **A** | Grice/Searle/MIP等早于Latent Hatred；历史上是并行谱系，不声称单线起源。 |
| CL03 | 改变语境会改变某些候选会话含义 | **A** | DRInQ受控问句/候选意义，VAGUE视觉情境选择；仅对应构造任务协议。 |
| CL04 | 语用无法由分类模型实现 | **D** | “分类模型”是方法形态；语用含义可被操作为选择/分类标签，真正区别在GT和语境条件。 |
| CL05 | 修辞检测与具体意义/对象解释是不同任务 | **A** | MultiMM/M3UCD/DOSE/V-FLUTE不同标签及输出；不自动证明忠实解释。 |
| CL06 | 检测到隐喻就意味着该语句有害/非人化 | **D** | When People are Floods仅标注隐喻源域，T4无独立GT。 |
| CL07 | 狗哨词项发现、实例消歧、毒性判断不同 | **A** | FETCH!/Silent Signals/SeTox任务输入/输出不同；不得合并成绩。 |
| CL08 | FETCH!已解决开放世界时间外新暗语 | **D** | 主实验是已有词典20/80词项留出，非时间新义。 |
| CL09 | AUTALIC直接证明规范性标签存在人工分歧及语境案例 | **A** | ACL2025正式全文+R3-B定稿：每句3位受训本科志愿标注、κ=0.25；例子有引用/反用和社群自述。 |
| CL10 | AUTALIC定量证明加上下文提高检测性能 | **D** | 无同模型target-only vs +context消融；不能用BERT同域finetune和LLM zero-shot差来证明。 |
| CL11 | 多模态数据提供新的跨模态语义关系评测对象 | **A** | V-FLUTE/M3UCD/VAGUE/VLSU各有不同任务和GT；并非单一“隐含风险”标签。 |
| CL12 | 融合/去图实验充分证明模型正确联合推理 | **D** | 模态替换会变分布，额外gold字段/文本泄漏可供捷径；需配对单因素反事实与人审GT。 |
| CL13 | 2026前无人研究多模态反讽捷径/IB | **D** | MCIB AAAI2026已正式发表，VLSBench等更早诊断文本泄漏（任务不同）。 |
| CL14 | MCIB在修订MUStARD++R上作者报告weighted F1=75.64 | **A（限论文结果）** | 正式AAAI Table1及R3-B审阅稿；不能扩展为“完整消除shortcut”。 |
| CL15 | MCIB已因果证明conditional IB自身是唯一增益来源 | **C** | 标准IB/去各子损失/同预算对照不足、代码损失与主文公式对照未闭合；R3-B仍待审。 |
| CL16 | 输入风险标签和输出拒答/安全有用性是不同指标 | **A** | VLSU/MMSafeAware vs MSSBench/MOSSBench/Meerkat-VL，任务协议本身可证。 |
| CL17 | 模型安全率提高意味着感知正确且回答有用 | **D** | 可能是保守拒答/提示策略；需要双侧误判与输出质量。 |
| CL18 | 发现任一控制实验缺口就等于发明CCF-A新Gap | **D** | 缺口仅为当前证据/复现审计，须先证明尚未有直接竞争工作、可观测机制与真实可达GT。 |

## 4. 重要数据、代码与发表状态：未关闭问题优先级

| 风险ID | 来源 | 当前能证实什么 | 仍需核查与建议处理 | 优先级 |
|---|---|---|---|---|
| **A4-01** | AUTALIC，ACL2025 Main A（R2A-013） | 论文共2400句、242正+2160负=2402算术不符；标注者为9位受训高年级本科志愿者而非全部临床专家；含访问约束 | 原CSV尚未开封重计；R4可引用方法与现象，但**不能给精确最终类别分布**，注明模型用途的许可证边界 | **P0（具体数字）/P2（结构）** |
| **A4-02** | MCIB，AAAI2026 Technical A（R2A-024） | 论文已正式出版；R3-B草稿静态发现loss与论文公式/训练脚本不完全对应、实际公开脚本只跑首折 | 等R3-B定稿；不宣称conditional IB完全清除了shortcut；表1SpeechPrompt分数数理不一致须查代码/勘误 | **P0（精确表格/机制）** |
| **A4-03** | P039 ThinkingGuard，ACM MM 2026 A刊会 | 作者代码、arXiv与DOI以及已录用声明存在；目前可作相近方法竞争，不可忽略 | 查ACM权威正式出版条目与Track；会议计划2026-11-10至14，不应因未来会议日期混淆“DOI存在”和“会议已举行” | **P1** |
| **A4-04** | DRInQ，ACL2026 Main A | 论文819人类共识/400困难集，公开CSV当前231行、148问句 | 版本/样本对应、选项和场景泄漏；R4不在同一分母混报76/89与困难子集67/88 | **P1** |
| **A4-05** | Silent Signals，ACL2024 Main A | 论文主集16550，HF主集README 16258，小检测集100 vs101 | 版本差、LLM自动标签与人工测试区别 | **P1** |
| **A4-06** | VLSU，ICLR2026 Main A | 论文8187，公开CSV 8159，图像not_sure与17设计模式不完全对应 | 不能以论文规模充当可实物下载规模；S-S-U公开35条统计不稳定，test-only不作官方训练 | **P0（训练使用）/P1（引用）** |
| **A4-07** | MultiMM/MGMCF/DOSE | gold情绪、源目标辅助与MCQ选项差异在公开代码/小样本有可识别风险 | 不因训练消融直接宣称多任务知识迁移、联合语义归因或高质量自由解释 | **P1** |
| **A4-08** | MOSSBench/MSSBench/MMSafeAware | 输入GT、拒答Judge和行为指标是三种不同层次；MOSSBench约9%安全GT有分歧 | 不交叉换算accuracy、refusal、unsafe recall；图片复用和样本配对需留痕 | **P1** |
| **A4-09** | RV-HATE，ACL2026 Main A | 当前公开ppo_eval.py使用test labels学权重 | 不称作者发表成绩已无效；如正式写“PPO必要性”必须加同预算验证集搜索与版本限定 | **P1** |
| **A4-10** | 摘要候选如MMSD3.0、MCIB先前状态、A类论文Track | R2A官方metadata通常可核题名/出版渠道/研究问题 | 严禁仅据摘要推断训练细节、SOTA、消融；项目文献账本的“未读”状态按最新R3-B版本更新，不改原卡 | **P1** |

### MCIB新增的表格一致性警报（以审计日志方式呈现）

AAAI 2026正式PDF Table1 报SpeechPrompt v2原MUStARD++ **Precision=78.33、Recall=58.06、weighted F1=73.47**。若三列确为同一类加权P/R/F1且使用相同类别权重，由各类 F1_i ≤ (P_i+R_i)/2，可得 weighted-F1 ≤ (weighted-P+weighted-R)/2 = **68.195**，故这组三数与标准同权加权定义不兼容。[P+H] 正文又将78.33→63.03称为“accuracy”变化，和表头Precision不符。**只能得出需核栏目/脚本/表格或更正的内部口径疑点**，不可断言其他模型结果不可信。正式PDF截图接口本轮未成功加载，文本和R3-B卡保持复核状态。AAAI正式页：[MCIB](https://ojs.aaai.org/index.php/AAAI/article/view/39874)；[R3-B审阅卡](https://github.com/YuSun-WK/implicit-content-research/blob/r3b-mcib-targeted-review-20261108/03_survey/R3_targeted_reading/R3B_02_MCIB_REVIEW_DRAFT.md)。

## 5. R3-A3叙事的必要修改（提出修改，不覆盖A3文件）

1. **更新AUTALIC状态**：A3各处“R3-B将补读/仅摘要”更新为“已全文定稿（在main），带样本数字冲突/许可/缺删语境消融限制”。
2. **更新MCIB状态**：A3各处“只看摘要/R3-B将补读”改为“正式AAAI正文已审计于独立R3-B审阅分支，待定稿；有conditional IB方法但独立消融证据有限”。
3. **明确模态范围**：MCIB为文本+音频+视频反讽，不是静态图文Hateful Meme；MSSBench主要是情境安全响应，V-FLUTE是视觉蕴含，不共用GT。
4. **P039出版状态**：按作者录用/DOI、ACM MM CCF-A刊会与正式出版社页/track三个状态记录；未取得官方确认前单列，不按正式主会A已出版计数。
5. **细化R3“任务链”**：T5是T4一种受控联合模态风险条件，T6是输出行为邻接研究；不将T1→T2→T3→T4→T6描写成所有算法必须经过的心理/因果链。
6. **章节结构压重复**：A3临时Ch6多模态隐含意义和Ch7联合风险需要按**意义/危害GT**明确拆开；Ch8安全响应控制篇幅，不扩为通用RLHF综述；Ch9只横向机制对照，不重复给每篇论文完整Pipeline。
7. **不用单一性能排名证明历史转折**：同任务不同split、K、Oracle信息和训练预算分开；给每章定义准确GT、指标分母、模型输出形式。
8. **讲清语境依赖与隐晦差异**：普通实体消歧、法律授权和视觉物理情境可能涉及上下文，却不一定属于“非字面意义”或“隐晦有害”；使用纳入/排除阈值解释相邻文献。
9. **更新过时的前向状态语句**：R3-A1末尾仍说“后续做R3-A2”；R3-A2与A3个别R3-B将来时语句应在R4引用前改为阶段事实；不自动将A1/A3改为FINAL。
10. **增加图文严谨性警报**：需有可观察的同输入模态消融、受控视觉/文本反事实、人工独立标签，才能说“模型依赖了关键视觉事实”；不以“有图性能升高”作为充分证据。

## 6. 当前可支持的综合研究结论（供R4前言或综述收尾采用）

**可较强论证**：[PF/PA]
- 多条研究路线分别已建立语用含义/间接行动、修辞检测与解释、编码发现与语境消歧、隐含有害性/情境判断、多模态关系和安全回复等不同的**任务/标注/评价对象**。
- 2024–2026已有CCF-A论文将词典先验、对比与域适应、LLM搜索、图文/音视频多任务、结构化风险解释及安全对齐用于具体数据协议；不能称某一方法族首次被移入“广义隐晦信息”。
- 模态可靠性和输入特权已有直接研究（VLSBench、MCIB、MultiMM审计等）；文本/图片组合的风险GT与模型回复安全行为不可互换。
- AUTALIC提供真实社群对话中的**标注分歧、引用/反用和误报案例**，但不证明所有隐式有害内容的语境因果机制。

**需要限定为当前文献的未闭合证据，不可冒充公认研究空白**：[H/O]
- T2/T3中间解释是否是T4危害预测的必要或忠实因果中介；
- 可下载、有可靠人工Gold的真正时间外/群体外新编码意义发现；
- 跨模态补充信息是否实现正确语义因果关系，而非OCR/标签相关/辅助字段捷径；
- 精确区分“风险没有感知到”与“识别后仍作错误回答”的评测与公平优化；
- 数据发布差异、许可/不可得、token/训练预算不等价对综合结论的影响。

**进入R4条件**：见本目录 [R3A_R4_Readiness_Gate.md](R3A_R4_Readiness_Gate.md)；只有在A1/A3/A4审阅、AUTALIC与MCIB状态同步、论文正式渠道清理后才将“逻辑框架”转为正式论文提纲。本次可作有条件推进，不宜直接大规模写正文。

## 7. 可追溯原始入口

- [R3-A1历史发展稿](R3A_Research_Evolution.md)（main中仍为审阅稿）
- [R3-A2方法演进定稿](R3A_Method_Evolution.md)
- [R3-A3综述叙事稿](R3A_Survey_Narrative.md)（同分支上游）
- [R3-A3关键转折](R3A_Key_Research_Turning_Points.md)（同分支上游）
- [R2-C证据审计](../R2_synthesis/R2C_Coverage_and_Evidence_Audit.md)
- [R2元数据证据冲突](../R2_registry/Metadata_and_Evidence_Conflicts.md)
- [R2-A32篇候选与官方页](../R2_literature_extension/R2A_Candidate_Ledger.md)
- [R3-B AUTALIC定稿](../R3_targeted_reading/R3B_01_AUTALIC_FINAL.md)
- [R3-B AUTALIC三争议定稿](../R3_targeted_reading/R3B_01_AUTALIC_Three_Issue_Audit.md)
- [R3-B MCIB独立审阅稿](https://github.com/YuSun-WK/implicit-content-research/blob/r3b-mcib-targeted-review-20261108/03_survey/R3_targeted_reading/R3B_02_MCIB_REVIEW_DRAFT.md)
- [CCF 2026第七版目录入口](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)

> 以上所有评审结论是综述参考证据与写作边界，不构成“研究领域已被穷尽”的系统综述结论，也不代替发表论文的独立复现。审阅分支仅新增A4文件，不覆写A1/A2/A3、R1/R2、R3-B。
