# R5-E｜Citation and Claim Gates（正式综述引文及论断准入门槛）

> 2026-11-09。独立学术证据审查，供并行的 R5-A 撰稿 Work 引用。**本文件不是综述正文，也不自动修订第3–5章。** 对照 [R4小节证据矩阵](../R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)、[R4质量门槛](../R4_writing/R4_08_Overall_Quality_Gate_20261109.md)、[R2-D冲突台账](../R2_registry/Metadata_and_Evidence_Conflicts.md)；细节证据见 [专项核验](High_Priority_Evidence_Audit.md)、[相邻综述](Related_Surveys_Comparison.md)。

## 1. 证据分类（正文/表注强制执行）

| 符号 | 证据层级 | 准许措辞 | 不准擅自升级 |
|---|---|---|---|
| F | 可在官方正式出版页、正式PDF或出版元数据核实的事实 | “ACL Anthology 正式条目记载……”“该正式PDF报告……” | 官方摘要 ≠ 正式全文所有细节；DOI字符串 ≠ 已核Track |
| P | **论文作者报告**的实验、数据、标注、结论 | “作者报告……”“论文Table X中……” | 不写“我们复现证明……”；作者归因 ≠ 受控因果证据 |
| S | 仓库/CSV/代码**静态观察**，须注明版本和观察范围 | “在所查公开代码路径中……”“既有审计读到的CSV含……” | 公开代码 ≠ 作者正式训练所用的完整内部版本 |
| H | 本综述作者的比较、任务归纳与合理机制解释 | “本文提出工作性分类”“这一现象提示……” | 不当成该领域一致接受的定理或已有样本级验证 |
| O | 尚无充分公开证据或验证尚未完成 | “仍待核实”“现有实验不能隔离……” | 不能反说作者作弊/论文无效/技术必然无效 |

**最小引用单位**：一条主张应同时明确 paper ID、正式题名、venue 年度及 **CCF等级、实际Track**，如有性能数字还必须明确数据版本、输入X、标签G、评测E、表格/图号和证据等级。保留 R0/R2原编号，不制造“第91篇之外新增已全文精读”的假象。

### 准入规则与强制降级

- **PASS**：正式出版事实经核，或作者明确报告的任务/结果与PDF定位一致，且措辞限定。
- **PASS-WITH-QUALIFIER**：数据和公开文件分版本、作者只给定性案例、仅静态代码可证、缺等预算消融；必须写“作者报告”“当前所查版本”“不能据此证明……”。
- **BLOCK-STRONG-CLAIM**：断言因果机制独立有效、标签普遍无争议、严格反事实、真实OOD/开放世界或风险响应等同识别，而没有相应GT/对照；可以保留弱事实，**不必删除整篇文献**。
- **BIB-BLOCK**：出版社信息、正式Track或PDF作者与网页BibTeX矛盾；先采用可独立核对的正式字段或仅作者—年份短引，不编造完整书目。

## 2. 分章精确论断门槛

| R5章节/位置 | 允许写入的最低主张（需相应来源） | 一律禁止的强断言 / 风险 | 状态及操作 |
|---|---|---|---|
| **Ch1 §1.2 相关综述** | ACL 2025 Main（CCF-A）P011聚焦LLM语用；IJCAI 2024 **Survey Track**（会议按2026年第七版目录为CCF-B；非普通研究Full/Regular Paper）已有多模态反讽综述；EMNLP 2024 **Findings**（会议CCF-B）P007已有多模态仇恨审核综述；P002的CSUR正式版2025在线/2026卷期 | “本文首篇系统/唯一全面”“过去无人统一语用与安全”“已有综述仅仇恨” | **PASS-WITH-QUALIFIER**；引用相关综述对比表，贡献限定为跨任务X/Y/G/E的批判性组织；全文检索时间窗OPEN |
| **Ch2 §2.1–2.5** | 会话含意、间接言语行为、RSA是不同理论锚点；T1–T6与Task=(X,Y,G,E)是本综述工作分类 | “五轴统计独立”“T1→T6是模型真实的因果推理流水线”“标注的候选含义等于真实心理意图” | 工作分类**PASS(H)**；Grice/Searle原典书目需单独核实 |
| **Ch3 §3.1–3.2 修辞/含意** | 把修辞存在性T1、候选意义T2、交际功能T3区分；DRInQ受控多选的GT不同于真实自由表达 | “检测F1高证明理解含意”“候选答案正确等于意图忠实”；DRInQ论文819/400不能直接写公开CSV231行是同一完整集 | **PASS-WITH-QUALIFIER**；DRInQ行数映射OPEN |
| **Ch3 §3.3–3.5 情绪/Probe** | EmoBi等作者报告辅助情绪与修辞分类结果；探针AUROC、MCQ accuracy、解释相似度不同 | “情绪独立导致语义恢复”“probe等于faithful explanation”“所有比率可转成统一理解准确率” | **BLOCK-STRONG-CLAIM**（独立因果）；只引作者完整系统报告P |
| **Ch4 §4.1–4.2 编码义判别** | CodedLang讨论中文在线评论编码；Silent Signals是已给狗哨词项及编码义的instance消歧；其论文主集16550 vs所查README16258存在版本差 | “自动发现未知词”“主集全由人类逐例金标”“两个版本样本规模一致” | **PASS-WITH-QUALIFIER**；规模差 OPEN |
| **Ch4 §4.3 FETCH!** | 词典20%种子对剩余80%已知词的候选回收任务是作者协议的一部分 | “已验证未来时间外、未出现过词典外的真实开放发现” | **BLOCK-STRONG-CLAIM**；只能据协议写词典留出 |
| **Ch4 §4.4–4.5 FA-Net/SeTox** | FA-Net研究固定候选委婉义的跨域适应；SeTox用外部搜索辅助新词毒性判定（ACL 2026 Main，CCF-A） | “无监督生成全新编码词真实意义”“相似伪正例一定语义同类”“搜索结果不含标签污染”“未知新词无训练测试重合” | **PASS-WITH-QUALIFIER**；未验证的伪对质量/时序/跨词重合留O；SeTox书目以ACL正式页为准 |
| **Ch4 §4.6 任务串联** | 发现(type)、上下文实例消歧、语义解码、危害判定是不同GT/评估 | “已有论文共同验证一条端到端编码→危害流水线” | **PASS(H)**；主张为分析分类，不是模型流程 |
| **Ch5 §5.1/§5.3 隐喻与危害** | When People are Floods标的是隐喻源域；Sheep’s Skin报告合成隐喻式仇恨样本与特定提示下的风险误判 | “有源域标签即有非人化/仇恨逐例GT”“漏检说明模型必定不理解隐喻意义” | **PASS-WITH-QUALIFIER**；不能用无害隐喻样本充当有害标注 |
| **Ch5 §5.2/§5.5 解释分类** | RV-HATE、SMARTER、CADET等作者在各自协议报告检测性能；所查公开RV-HATE部分脚本有test标签调参风险线索 | “PPO/解释/因果风格模块独立提升已严格证明”“发布脚本疑点=正式结果无效” | **PASS-WITH-QUALIFIER**；等预算消融和正式运行路径 OPEN |
| **Ch5 §5.4 AUTALIC** | ACL 2025 Main（CCF-A）作者报总2400、每句3人、9名受训本科研究志愿者、κ=0.25、语境质性案例；242+2160=2402正文算术矛盾。数据加密公开，但许可限制开发/部署自动审核器 | “准确正242负2160总2400已CSV验证”“9名临床认证专家”“同模型去/加语境证明增益”“非限制开放数据” | **PASS-WITH-QUALIFIER**；统计分布、语境定量因果、某些训练用途需审批、官方作者元数据冲突均OPEN |
| **Ch5 §5.6 过渡** | 文本歧视GT与联合图文风险GT不是同一个标签；普通meme图文输入不自动证明严格S-S-U | “所有图文仇恨论文都是组合安全研究” | **PASS(H/P)**；T4/T5分轴 |
| **Ch6 §6.1–6.4 多模态修辞** | 反讽/隐喻/视觉蕴含的标签范围各异；所查MultiMM实现测试用gold情绪、MGMCF用源目标字段 | “这些作者成绩严格证明模态不可替代”“所有正式模型存在标签泄漏” | **PASS-WITH-QUALIFIER**；X预算不等可据静态代码说明，正式运行版本O |
| **Ch6 §6.5 MCIB** | AAAI 2026 **Technical Track**（CCF-A）；作者在MUStARD++R报weighted F1=75.64，结构/特征消融有结果 | “CIB单独带来X点”“已因果去除捷径”“代码MSE广播证明正式实验错了”“残差仍然只走瓶颈” | **BLOCK-STRONG-CLAIM**；论文结构结果可限定引，机制独立性/公开训练复现OPEN |
| **Ch7 §§7.1–7.2 VLSU** | ICLR 2026（CCF-A）正式PDF写8187、17模式、17模型；此前公开CSV实读8159和S-S-U 35（论文Figure9 37）；图/文/联合安全三级别分别标 | “公开文件就是8187”“全部联合风险都是S-S-U”“34%是S-S-U漏检率”“Borderline等于模型不确定”；官方摘要网页仍写11模型需分版本 | **PASS-WITH-QUALIFIER**；不能从test-only 35样本作广泛定量泛化 |
| **Ch7 §7.3 ThinkingGuard** | 作者README报ACM Multimedia 2026（会议CCF-A）录用、DOI 10.1145/3767308.3835707，提出TriggerBench+SA-MCTS+Trajectory/Step-DPO | “已独立核实ACM官方Main论文正式入库/实际Track”“反事实只改trigger已人审保证”“Step-DPO提升排除样本预算” | **BIB-BLOCK**（正式ACM/Track待核）；作者录用/方法先例可限定引用 |
| **Ch7 §§7.4–7.5 联合风险/响应** | VLSU joint风险classification 与VLSU refusal/helpfulness、SIUO ASR、MSSBench情境行为、MOSSBench误拒的GT和分母不同 | “拒答率等于安全判断准确率”“ASR等于有害标签F1”“helpful模型因此更安全” | **BLOCK-STRONG-CLAIM**；结果必须分输入风险/输出行为两表 |
| **Ch8–9 方法和未来** | 提出同预算、保持标签不变的受控反事实、跨分布、双侧误判及标注分歧审计等研究问题 | “本文实验证明共同失效机制”“首个提出独立语义中间真值的研究” | **PASS(H)** 仅作为建议；不能写成新实验成果 |

## 3. 书目与BibTeX“入正文前”的逐项检查

**四步顺序**：a. 正式出版平台与 DOI（或正式 proceedings 标识）→ b. 正式PDF首页题名/作者/顺序与出版平台元数据→ c. 实际 Track：Main / Findings / Survey / Technical / Datasets & Benchmarks / 预印本→ d. 年份/卷期/页码或article-number及可解析BibTeX。CCF评级对应刊会，不等于具体Track同质。

| 条目 | 固定的可引用元数据与来源 | 立即阻断的元数据问题 |
|---|---|---|
| **P011** | ACL 2025 Main，CCF-A，DOI 10.18653/v1/2025.acl-long.425，[官方](https://aclanthology.org/2025.acl-long.425/) | 不能标Findings或未发表 |
| **P007** | EMNLP 2024 **Findings**，会议CCF-B，DOI 10.18653/v1/2024.findings-emnlp.254，[官方](https://aclanthology.org/2024.findings-emnlp.254/) | 不能标Main |
| **P002** | ACM Computing Surveys DOI 10.1145/3744554，2025在线/2026卷期，项目CCF未收录，[官方](https://doi.org/10.1145/3744554) | 不能把2024预印本年份当正式发表年 |
| **R2A-013 AUTALIC** | ACL 2025 Main，CCF-A，DOI 10.18653/v1/2025.acl-long.1022，[官网](https://aclanthology.org/2025.acl-long.1022/)及[PDF](https://aclanthology.org/2025.acl-long.1022.pdf) | **PDF列13作者（含Michael Golden），网页/BibTeX列12作者**：完整作者字段暂不能称已核 |
| **R2A-024 MCIB** | AAAI 2026 Technical: Machine Learning VIII，CCF-A，DOI 10.1609/aaai.v40i31.39874，[官方](https://ojs.aaai.org/index.php/AAAI/article/view/39874) | 主文与扩展附录需区分；不把代码结果当正式成绩 |
| **P038 VLSU** | ICLR 2026正式会议，CCF-A，[PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf) | 正式PDF17模型 vs 官方摘要网页11；作者repo BibTeX是2025 arXiv版本，不是正式2026 Proceedings |
| **P039 ThinkingGuard** | 作者所报ACM MM 2026、DOI 10.1145/3767308.3835707，[作者仓库](https://github.com/FroggyChen/ThinkingGuard) | **ACM官方正式版本/实际Track未独立核验**；README的BibTeX url字段含Markdown链接，不可直接复制 |
| **P041 SIUO** | NAACL 2025 **Findings**，会议CCF-B，DOI 10.18653/v1/2025.findings-naacl.198，[官方](https://aclanthology.org/2025.findings-naacl.198/) | 不能称NAACL Main |
| **R2A-010 SeTox** | ACL 2026 Main，CCF-A，DOI 10.18653/v1/2026.acl-long.1602，[官方](https://aclanthology.org/2026.acl-long.1602/) | 作者README旧BibTeX与ACL正式记录不符，以官方为准 |
| **T014** | NeurIPS 2024 **Datasets & Benchmarks Track**，会议CCF-A，见[R2-D](../R2_registry/Metadata_and_Evidence_Conflicts.md) | 不能标为普通Main/Regular |

**引文执行约束**：
1. 没有核对的精确页码、表号、损失系数、样本数不得从回忆补填。若来源仅官方摘要，标 **PA** 并只引摘要范围；PA不能用来支持消融和SOTA。
2. 数据论文数量冲突必须明确说“论文版本”“所查发布文件版本”，不能选看上去正确的一方悄悄修正历史审计。
3. 包含自动审查数据许可限制的附录是实质学术复现信息，不能只在方法附注中略去。
4. 对于已有不同来源年份/作者冲突，BibTeX最终版应单独审核并保留核验时间；任何本稿写出的 DOI 不是凭空保证BibTeX已经完全正确。
5. Work并行写作时，本稿以“修改建议/阻断清单”的形式交付；**不向工作分支直接写入任何正文修订**。

## 4. 最小交接清单、闭环状态与未解决阻断项

### 可以在限定范围内关闭
- **CLOSED-FACT**：P011/P007/P002的正式场合与版本区分；AUTALIC算术不一致的存在、9名本科研究志愿者身份、公开使用条款；MCIB的正式 AAAI Technical 发表和所查代码具体形态；VLSU输入三标注与响应评价两种不同任务；SeTox正式ACL条目优先；SIUO为Findings。
- **CLOSED-WRITING-GATE**：已提供无需新实验即可使用的弱表述与强结论禁区；这不是对原作者研究开放问题的实证“关闭”。

### 仍须OPEN，不准强行闭合
- **OPEN-DATA**：AUTALIC原CSV和最终正负分布、VLSU少28条的原因与图片可达性及141 not_sure处理、Silent Signals 292条差异。
- **OPEN-CAUSAL**：AUTALIC严格语境对照、MCIB有/无CIB独立正交消融及正式代码版本、ThinkingGuard真反事实配对有效性及Step-DPO等预算贡献。
- **OPEN-BIB**：AUTALIC PDF与ACL Anthology作者字段冲突；ThinkingGuard ACM官方出版社页面/正式BibTeX/具体Track；VLSU官网摘要11与正式PDF17的版本缘由。
- **OPEN-COVERAGE**：相邻综述中摘要级作品的完整纳入时间窗及正式期刊等级；若投稿要求系统综述，应另做可复核检索协议，不能称本轮已完成PRISMA。

## 5. PR验收条件

- 提交内容仅属于 **03_survey/R5_evidence/** 中本文件与 [Related_Surveys_Comparison.md](Related_Surveys_Comparison.md)、[High_Priority_Evidence_Audit.md](High_Priority_Evidence_Audit.md) 三文件。
- 不修改 R0–R4 历史材料，不碰 Work 正在进行的 R5 第3–5章正文。
- PR可以完成**本轮证据审查交付**，不构成“所有研究事实已解决/可直接投稿”的声明。
