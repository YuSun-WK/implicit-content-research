# R4-07｜广义隐晦信息综述：章节论断—论文—证据矩阵（R4-3 审阅稿）

> 2026-11-09；状态：**R4-3 REVIEW**，未获用户定稿确认。基于最新main的R3-A/B定稿、R2-B跨论文综合、R2-D证据冲突，以及当前R4-01/02。仅将既有文献证据映射到R4全部46个小节；**未独立运行实验、重新阅读全文91篇或穷尽检索外部论文**。

## 0. 使用约定

- 采用任务四元组 **Task=(X,Y,G,E)**：X=输入与额外先验，Y=预测目标，G=Ground Truth，E=评价；不得互换不同任务指标。
- 证据标记：**P**=论文作者直接报告（非本项目复现）；**S**=既有代码/数据静态审计；**H**=综述作者综合解释；**O**=暂缺严格证据。**PA**=仅官方摘要/出版元数据，不支持消融/机制/精确SOTA强引。
- **强引用判据**：可陈述论文已有的任务设计、数据协议或作者报告结果，必要时附限定；不能把整体性能自动归因为信息瓶颈、情绪、多任务迁移、反事实或自验证某模块。
- 代表论文完整英文题名、出版年份、CCF等级、实际Track及入口统一列在§10；同篇跨章引用不改变R4-02的唯一主讲章。
- ‘证据位置’中凡仅写R2/R3已读卡或综合节而未核实正式PDF具体表图的，**R5不能擅自填入Table/Section编号或性能数字**。只有既有卡确定过的Fig/Table才写明。

## 1–9. 每节：问题→论断→代表论文→直接证据→局限

| 小节 | 核心研究问题 | 最低可支持的学术论断 | 代表论文原ID | X/Y/G/E（压缩） | 直接证据位置/审计入口 | 证据级别 | 局限与反例 | 正文使用 |
|---|---|---|---|---|---|---|---|---|
| **第1章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 1.1 | 为什么不仅是敏感词过滤？ | 表面词汇与语用含义/规范性危害并非一一对应；广义研究涵盖多条并行现象谱系。 | P011 P023 R2A-013 | X=表达+语境；Y=修辞/编码/歧视；G=各自现象或规范标签；E=任务内指标 | R3-A3 §1 Q3–Q4；AUTALIC §1/§4 | P+H | 工作性范围而非领域共识；案例不能推出总体比例 | 限定可写 |
| 1.2 | 相关综述覆盖什么、本文增量在哪里？ | 已有语用、修辞、仇恨及多模态反讽子域综述；本文创新是跨任务/GT/信息预算的批判性组织视角。 | P002 P011 P007 P010 | X=已有综述；Y=覆盖问题；G=文献纳入协议；E=范围差异对照 | P011正式综述任务范围及R4-02 Ch1书目；P002/P007/P010仅题录/既有分析线索；横向范围对照表尚缺 | P+PA+H+O | P仅支持P011及已确认论文之有限研究范围；其余PA不强引机制。未逐篇核对时间窗/模态/主题；不得称首篇全面综述 | 待补比较表 |
| 1.3 | 需要回答哪些核心问题？ | 采用定义、语境变化、规范危害、模态必要性、可靠性五个RQ组织材料；非单个论文验证的统一模型。 | P011 R2A-001 P038 | X=多研究任务；Y=不同决策；G/E=分别定义 | R4-01 §E；R3-A3 §0/§1 | P+H | RQ1–RQ5是综述作者组织命题，不是因果链 | 框架可写(H) |
| 1.4 | 怎样诚实报告选文？ | R0 59加R2-A 32共91篇去重候选，并区分全文卡、官方摘要和静态审计。 | P002 P011 | X=目录与筛选账本；Y=纳入91项；G=标准化标题；E=去重核计 | R0_Audit_Report §数量与去重；R2-C §1；R4-02 §13 | S+H | 不是PRISMA穷尽检索，也不是领域总体数量 | 直接可写(项目事实) |
| **第2章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 2.1 | 语义、语用和修辞如何分离？ | 会话含意与间接言语行为超越简单字面断言，概率RSA可对部分候选意义建模。 | P011 P020 R2A-001 | X=表达+情境+候选；Y=含意/意义；G=候选共识；E=选择/拟合 | R3-A3 §1 Q2；R3-A2 §1；B1综合 | P+H | Grice/Searle原典须补；候选意义不等于实际发话者心理意图 | 限定可写 |
| 2.2 | 哪些维度应正交？ | 表达机制、任务、模态及依赖、测试信息预算、GT/E分别编码；subtle、coded、harmful非同义。 | P023 R2A-006 R2A-029 | X=多来源；Y=T1–T6；G/E=分任务 | R1五轴；R3-A4 CL01/CL16；R2-C §0 | P+H | 五轴是综述工作分类，非学界共识本体 | 框架可写(H) |
| 2.3 | 语用Ground Truth究竟标什么？ | DRInQ五选一共识、VAGUE视觉四选一行动与RSA候选概率评的是不同操作性目标。 | R2A-001 R2A-002 P020 | X=Q+C或图+话语；Y=含意/行动选项；G=人审共识/构造目标；E=Acc | B1综合 §1–4；R3-A4 CL03 | P+S+H | DRInQ 819/400与公开231不等；VAGUE版本与泄漏边界待核 | 直接可写(任务分层) |
| 2.4 | T1–T6代表什么？ | T1形式、T2含义、T3交际功能、T4规范危害、T5联合模态条件、T6响应；Task=(X,Y,G,E)。 | R2A-001 R2A-011 P038 R2A-027 | X/Y/G/E各有独立目标和分母 | R1框架；R3-A3 §0；R3-A4 CL01 | P+H | T5严格S-S-U更窄；任务不构成模型必经流水线 | 框架可写(H) |
| 2.5 | 相邻任务如何纳入或排除？ | 无害隐喻、社群编码、联合风险、安全响应各有范围；隐写/普通OCR/物体识别不自动核心。 | P023 R2A-011 R2A-027 | X=实例条件；Y=现象/风险/响应；G/E=任务独立 | R4-01 §A；R3-A3 §1 Q3–Q6 | P+H | 纳排实例为综述定义，不是实测频率 | 限定可写 |
| **第3章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 3.1 | 检测修辞与解释具体意义相同吗？ | 反讽、夸张、隐喻等T1识别标签不自动提供T2解释或T3评价立场。 | P015 P035 R2A-004 | X=文本/语境；Y=修辞标签或探针；G=现象标签；E=F1/AUROC | R3-A4 CL05；P035阅读卡；B1综合 | P+H | 线性探针不等于忠实解释；不同指标不可混排 | 直接可写 |
| 3.2 | 怎样研究候选意义与意图？ | DRInQ控制语境做候选含义选择，(RSA)²加修辞策略；语义对比与反问probe诊断不同。 | R2A-001 P020 R2A-003 R2A-004 | X=语境/候选/对比句；Y=解释选项或表征；G=共识/构造；E=Acc/距离/AUROC | B1综合 §1–4；R3-A2 §1/§3 | P+S | 真实开放交际意图与受控选项不同；RSA prior作用待拆 | 限定可写 |
| 3.3 | 情感知识是否独立帮助修辞推断？ | EmoBi在隐喻/夸张检测报告收益；情绪是否促进实际意义映射未被严格因果隔离。 | P035 P003 | X=文本+情绪辅助；Y=修辞识别；G=任务标签；E=分类指标 | P035阅读卡；B3a综合 §3.2；R3-A2 §3 | P+S+O | gold/predicted/random情绪、等预算消融不足 | 限定可写 |
| 3.4 | MCQ与生成解释、探针可同比吗？ | 多选Acc、生成解释相似度与隐藏状态Probe AUROC测量不同层次。 | R2A-001 R2A-004 P022 | X=选项或隐藏态；Y=候选/解释/探针；G=各自标注；E=Acc/BERTScore/AUROC | B1综合 §2；R3-A4 CL05；P022卡 | P+H | P022具体实验分母在R5核原文；不能换算统一理解分数 | 限定可写 |
| 3.5 | 修辞与编码的交叉关系？ | 隐喻和委婉有时用于社群编码，但编码不全是修辞，修辞亦不天然有害。 | P023 R2A-006 R2A-008 | X=修辞/编码实例；Y=形式或意义；G=现象/词典；E=任务指标 | R3-A3 §1 Q3；B2a综合 §2 | P+H | 狗哨多受众功能需社群知识；不能推定规避目的 | 框架可写(H) |
| **第4章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 4.1 | 编码、狗哨和音形变体怎样定义？ | CodedLang提供真实中文评论多种编码方式的任务先例，Dog Whistle强调不同受众条件但编码不必有害。 | P023 R2A-006 | X=中文评论/狗哨上下文；Y=编码识别；G=语料标签/词义定义；E=任务指标 | P023卡；R3-A3 Q3；R2-C §1编码线 | P+H | P023不代表所有狗哨多受众GT；谐音只是部分形式 | 直接可写(范围) |
| 4.2 | 已知狗哨实例能否判义？ | Silent Signals给定词项和编码义定义，完成instance-level消歧；自动筛大集不是全量人审。 | R2A-006 | X=词项+定义+上下文；Y=该处是否编码义；G=小人审/自动伪正例；E=F1/抽检Precision | B2a综合 §一/§三；R3-A4 A4-05 | P+S | 16550论文vs16258公开；不能把主集当全部人工金标 | 直接可写(限定协议) |
| 4.3 | 新狗哨发现是否时间外？ | FETCH!主要由词典20%种子回收已知词典80%留出词项，而非证明真实时间外开放发现。 | R2A-007 | X=语料+种子；Y=type候选；G=已有词典；E=Precision/DPR/F0.5 | B2a综合 §一/§三；R3-A4 CL08 | P+S | 词典外真实词可能被错判；时间/社群外GT不足 | 直接可写(限定) |
| 4.4 | 固定候选委婉义怎样跨域泛化？ | FA-Net在source监督和target适应下进行固定候选义选择，使用相似伪正对。 | R2A-008 | X=源域/目标域语境+候选义；Y=目标词类；G=词典映射；E=Acc@k | B2a综合 §一/§二；R3-A2 §2 | P+S+O | 相似伪正对错配率未实证；不是开放未知释义 | 限定可写 |
| 4.5 | 搜索增强新词毒性解决什么？ | SeTox作者报告搜索增强改善中文新词风险分类，但不证明开放词义或无污染检索。 | R2A-010 | X=新词句+搜索；Y=有害二分类；G=人工安全标签；E=Acc/F1、DR/KDR/UDR | B2b综合 §2/§4/§5；R3-A4 A4-06以外相关卡 | P+S+O | model-unknown相对特定基座；时间、词项重合待核 | 限定可写 |
| 4.6 | 从编码义到危害的逻辑缺口？ | 词项发现、实例消歧、目标解码和风险判定是四个不同标注目标，不能将论文串成已验证流水线。 | R2A-006 R2A-007 R2A-008 R2A-010 | X=不同先验；Y=type/instance/meaning/harm；G=词典/人审；E=独立指标 | B2a综合 §二；B2b综合 §3/§6；R3-A4 CL07 | P+H | 研究间非共享统一样本/预算/GT，不可称端到端验证 | 框架可写(H) |
| **第5章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 5.1 | 隐喻源域、刻板印象与隐性仇恨是否共用GT？ | ToxiGen是隐式/对抗仇恨数据；When People are Floods人工GT是隐喻源域，不是非人化或仇恨逐例标签。 | P001 R2A-011 R2A-013 | X=文本/语境；Y=仇恨/源域/歧视；G=各自标签；E=F1或AUC | B2b综合 §2/§4；AUTALIC §1–3；R3-A4 CL06 | P+H | AUTALIC亦不提供独立显隐标签 | 直接可写(标签差别) |
| 5.2 | 从分类到解释的改进能否归因？ | ImpCon、SMARTER、RV-HATE分别结合隐含陈述/解释/集成分类，但F1提升未证明解释忠实或PPO必要。 | P032 P030 P029 | X=文本+增强/解释；Y=有害分类；G=有害标签；E=Macro-F1 | R3-A2 §2/§5；P029/P030卡；R3-A4 A4-09 | P+S+O | RV-HATE所查公开脚本test标签寻权；不直接否定论文结果 | 限定可写 |
| 5.3 | 隐喻何时是有害，如何证实？ | Flood仅标源域；Sheep's Skin合成人审隐喻式仇恨样本存在漏检和拒答变化，但不能唯一归因T2失败。 | R2A-011 R2A-012 | X=移民推文/受控改写；Y=源域/检测与警告；G=源域人审/保留仇恨意图人审；E=AUC/正类检出/警告率 | B2b综合 §2/§4；R3-A4 CL06 | P+H+O | Sheep给标注者原句而模型未见；正类占主缺负侧FPR | 直接可写(任务限定) |
| 5.4 | 语境和社群立场怎样影响规范判断？ | AUTALIC真实引用/反用/求助案例及每句3人标注、Fleiss κ=0.25展示标签分歧。 | R2A-013 | X=目标句+前后文；Y=歧视二分类；G=9受训本科志愿、每句3票；E=κ/F1 | AUTALIC §2–5、Fig1/3/5、Table2；R3B三争议审计 | P+S+O | 没有同模型加/删语境消融；2400与242+2160冲突；用途许可限制 | 直接可写(质性) |
| 5.5 | 跨域和可解释分类是否真的去偏？ | CADET/RV-HATE等在各自协议报告性能收益，尚不能将增益单独归因于因果风格去偏或PPO。 | P033 P029 P032 | X=跨风格文本；Y=T4分类；G=各数据标签；E=Macro-F1/消融 | R3-A2 §2；R3-A4 A4-09；P033/P029卡 | P+S+O | 版本、test标签、同预算/替代权重搜索尚未对齐 | 限定可写 |
| 5.6 | 文本T4与联合模态T5界在哪里？ | 文本语境规范GT与联合图文风险GT不同；普通Meme图文并置不自动满足严格S-S-U。 | R2A-013 P038 T015 | X=句子或图文；Y=T4/T5；G=不同政策/独立判断；E=分类/安全分组 | R3-A3 Q5–Q6；R3-A4 §2 | P+H | T015仅官方摘要级背景，不作强机制归因 | 框架可写(H) |
| **第6章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 6.1 | 多模态隐晦理解含什么现象？ | 图文隐喻/视觉蕴含/音视频反讽/多图反讽是不同研究谱系。 | P003 P019 R2A-024 R2A-020 | X=图文或音视频、多图；Y=修辞/蕴含；G=特定标签；E=分类/解释指标 | B3a综合 §2/§4；MCIB §1；R3-A4 Ch6 | P+H+PA | MMSD3.0仅摘要元数据；不可强述实现与消融 | 限定可写 |
| 6.2 | 细粒度标签具体标了什么？ | MultiMM/M3UCD/MGMCF/V-FLUTE分别标情绪、隐喻概念、意图、蕴含和冒犯，非统一安全GT。 | P003 P019 R2A-017 R2A-018 | X=图文/辅助；Y=各任务；G=人工/既有标签；E=Acc/F1/BERTScore | B3a综合 §2/§5；R3-A4 CL11 | P+S | M3UCD Complementary是现象标签，不是行为级双模态必要性 | 直接可写(标签目标) |
| 6.3 | 融合与多任务模型改进来自哪里？ | MGMCF对象融合、M3UCD共享LoRA、DOSE正交专家在各自任务报告改进，但不能等于语义迁移因果。 | R2A-017 R2A-018 R2A-019 | X=图文+可能辅助；Y=多任务；G=分类/概念/候选；E=Acc/F1 | B3a综合 §2/§3.1/§3.4；各B3a卡 | P+S+O | 数据量、参数和训练预算不同，个别任务有负迁移 | 限定可写 |
| 6.4 | 情绪/源目标字段是否测试特权？ | MultiMM公开所查代码测试用gold情绪，MGMCF测试引用源目标字段；与纯图文信息预算不同。 | P003 R2A-018 | X=图文+gold或域字段；Y=修辞/情绪/意图；G=多任务标签；E=分类 | B3a综合 §3.2/§3.4；R3-A4 A4-07 | S+P+O | 公开脚本存在信息优势不等于正式全部实验非法泄漏 | 直接可写(审计限定) |
| 6.5 | 信息瓶颈能否独立去捷径？ | MCIB作者在MUStARD++R报告weighted F1 75.64；细粒度/Transformer消融支持整体配置，却没有去CIB独立正交消融。 | R2A-024 P019 | X=文本+音频+视频；Y=反讽二分类；G=既有反讽标注；E=weighted F1及消融 | MCIB正式Table1/2 Eq2–11；R3B_CIB审计 §1–4；R3-A4 CL14/15 | P+S+O | 公开代码MSE广播/原文残差旁路；未独立训练复现；不能称CIB因果消除shortcut | 整体结果可写，因果不可强引 |
| 6.6 | 多图/视频扩展已可靠泛化吗？ | MMSD3.0提供多图反讽候选设定，MCIB提供音视频反讽实证；尚不能跨任务归纳普适泛化。 | R2A-020 R2A-024 | X=多图/音视频；Y=反讽；G=各自标签；E=不同分母 | R2A候选账本；MCIB §1；R3-A4 A4-10 | PA+P+O | MMSD3.0未全文精读，不许写训练细节/数值SOTA | 仅范围/趋势可写 |
| 6.7 | 多模态语义与风险怎样分开？ | 视觉蕴含/隐喻与组合危险属于不同政策、标注和评价，不能从语义表现推出安全GT。 | P019 R2A-017 P038 | X=图文语义或风险；Y=意义或安全；G=不同GT；E=不同指标 | R3-A3 Q5–Q6；R3-A4 CL11/16 | P+H | 意义检测不等于安全标签，反之亦然 | 框架可写(H) |
| **第7章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 7.1 | 联合风险的必要条件是什么？ | 严格S-S-U是单模态各安全、组合危险的特例；联合条件还可能有风险解除/上下文变化。 | P038 R2A-029 T015 | X=图/文/联合；Y=风险；G=三条件安全GT；E=分组指标 | R3-A4 CL11/A4-06；B4a综合 §1–2 | P+S+H | VLSU公开严格S-S-U少且test-only；普通meme不是此类GT | 限定可写 |
| 7.2 | 不同安全基准实际测试什么？ | Hateful Memes危害分类、VLSBench视觉泄漏和行为、VLSU联合风险、MSSBench情境行动具有不同GT。 | T015 P037 P038 R2A-027 R2A-029 | X=图文或环境请求；Y=风险/行为；G=分类或策略；E=Acc/ASR/IF | R3-A4 Ch7–8；B4a综合 §1–2；各精读卡 | P+S+H | VLSU论文8187公开8159；MSSBench IF Judge不是输入风险金标 | 直接可写(分层) |
| 7.3 | 反事实/风险归因是否已有先例？ | CrossGuard与ThinkingGuard已研究联合风险样本、触发归因和反事实/偏好训练，不能称该范式尚无人做。 | P034 P039 | X=图文/配对；Y=风险/归因/对齐；G=合成配对；E=作者风险指标 | R3-A1安全线；P034/P039卡；R3-A4 A4-03 | P+S+O | P039正式出版Track未独立核；合成反事实不一定单变量；Step-DPO贡献需公平消融 | 限定可写 |
| 7.4 | 风险识别与安全响应为何不能混算？ | Meerkat-VL、MSSBench和MOSSBench衡量的风险感知、情境执行、误拒与回应质量并非同一个指标。 | P040 R2A-027 R2A-028 P041 | X=视觉场景请求；Y=判断/拒答/行动；G=政策/行为judge；E=ASR/ARR/IF | B4a综合 §1–3；R3-A4 CL16/17 | P+S+H | Meerkat自检含特权风险文字；MOSSBench安全GT争议；P041 NAACL Findings非Main | 直接可写(指标区别) |
| 7.5 | 安全误拒与危险漏判双侧如何评？ | MMSafeAware输入风险分类与MOSSBench正常请求误拒分别覆盖不同错误侧，单一拒答率不是准确性。 | R2A-029 R2A-028 P038 | X=正负图文；Y=风险/拒答；G=安全/危险人工判断；E=recall/FPR/ARR | B4a综合 §1–4；R3-A4 A4-08；R2-D登记 | P+S+H | 图像重复/提示错配、安全GT分歧与judge分母差异 | 直接可写(协议限定) |
| **第8章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 8.1 | 不同方法族在优化什么？ | 规则/RSA、对比与域适应、LLM检索、跨模态专家、偏好训练、Guard等并行支持不同预测目标。 | P020 P032 R2A-010 R2A-019 P040 | X/Y/G/E随方法不同；不能跨任务同分数 | R3-A2 §0–6；R2-C §2；R3-A4 §6 | P+H | 不能写BERT→GPT→VLM机械替代或单SOTA | 框架可写(H) |
| 8.2 | 辅助先验是否改变信息预算？ | gold情绪/源目标、OCR、给定编码定义与在线检索会改变模型测试可用信息，须单列X字段。 | P003 R2A-006 R2A-018 R2A-010 | X=原输入+oracle/词典/检索；Y=分任务；G=辅助/最终标签；E=同预算对照待补 | B3a综合 §3.2/3.4；B2a §二；R3-A4 A4-07 | S+P+H | 公开实现不等于正式运行版本；不能据此一概断言作者成绩无效 | 直接可写(版本限定) |
| 8.3 | 解释合理性与忠实性如何分辨？ | 自然语言解释/高自信和模型自验证不自动证明其为分类决策的真实因果证据。 | P030 R2A-019 R2A-013 P024 | X=文本/多模态；Y=标签+解释；G=多数票/候选/judge；E=F1/BERTScore/一致性 | R3-A4 CL05/09/15；B3a综合 §3.4；AUTALIC §3–5 | P+S+H+O | 缺解释干预和同任务分层GT，禁止写解释忠实已证 | 限定可写 |
| 8.4 | 如何验证真正模态必要性与域外可靠性？ | 去模态、文本泄漏审计、配对反事实与时间/社群外测试相互补充，单模块消融不充分。 | P037 R2A-017 R2A-024 R2A-008 | X=text-only/image-only/joint；Y=标签；G=配对人工GT；E=受控/分组性能 | R3-A4 CL12/15；B3a综合 §3.3；MCIB专项 §2–3 | P+S+H+O | 模态去除可造成分布漂移，因果必要性仍待实验 | 方法论可写(H) |
| 8.5 | 如何同时汇报两侧风险和回应？ | 输入TPR/FPR、响应拒答率/警告率和有帮助性需在同一案例分开测，不能合成为未经定义的单安全率。 | R2A-029 R2A-028 R2A-027 P040 | X=安全/危险；Y=分类/行为；G=政策/人工标签；E=TPR/FPR/ARR/IF | B4a综合 §1–3；R3-A4 CL16/17 | P+H | 不同数据裁判、样本比例无法横向换算 | 直接可写(目标区别) |
| 8.6 | 哪些开放问题已经有真正证据？ | 真实时间外编码义、T2/T3对T4中介、独立模态语义使用与双侧安全是当前馆藏的未闭合证据问题。 | R2A-007 R2A-011 R2A-024 P034 | X=研究协议；Y=尚待解决主张；G=现有标注不足；E=缺公平干预 | R3-A4 §6/CL18；R3-A2 §6；R2-C §4.3 | S+H+O | 不等于全球首次/无人研究；需另作竞争查重与可达GT审核 | 只写限定展望 |
| **第9章** | **研究主张与证据链** | — | — | — | — | — | — | — |
| 9.1 | 已有研究操作化到什么层次？ | 语用、修辞、编码、有害、联合风险和响应分别拥有不同数据GT与指标；不构成单一任务排行榜。 | R2A-001 R2A-006 R2A-013 R2A-017 P038 R2A-028 | X/Y/G/E按任务；强结论是任务存在和协议定义 | R3-A4 §2/§6；R2-C §1/§3；R4-01 §E | P+H | 不同研究无共享分母，不能讲唯一历史演进因果线 | 综合可写(H) |
| 9.2 | 后续挑战如何避免假创新？ | 展望应侧重可信GT、受控证据必要性、发布许可和双侧响应评价；开放项不是直接新颖性证明。 | R2A-013 R2A-024 R2A-007 R2A-029 | X=待设计对照；Y=未来验证问题；G=待补/需许可；E=同预算因果检验 | R3-A4 §4/§6/CL18；R3B双篇综合 §6；R2-D | H+O | 未关闭任务不能称已解决；未查重不能称无人研究 | 只写限定展望 |

## 10. 代表论文正式书目及证据入口

> 仅列上述论证链中出现的论文。出版资料取R4-02所附主索引，保留原编号和实际Track；R2A文献的官方元数据核验**不等于全部全文精读**。

| 编号 | 正式英文题名 | 年份、Venue、CCF、Track | 阅读状态 | 出版及阅读卡入口 |
|---|---|---|---|---|
| P001 | ToxiGen: A Large-Scale Machine-Generated Dataset for Adversarial and Implicit Hate Speech Detection | 2022；ACL 2022，主会 Volume 1: Long Papers；CCF-A；ACL 2022 Main／Long Paper，正式会议论文 | AN（已分析，全文程度未核） | [官方/登记页](https://aclanthology.org/2022.acl-long.234/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P001_ToxiGen.md) |
| P002 | Computational Approaches to the Detection of Lesser-Known Rhetorical Figures: A Systematic Survey and Research Challenges | 2025 在线／2026 卷期；ACM Computing Surveys，58(2)，Article 42；阅读版 arXiv 2024；CCF-未收录；正式期刊论文（2025 在线／2026 卷期） | AN（已分析，全文程度未核） | [官方/登记页](https://dl.acm.org/doi/10.1145/3744554)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P002_Rhetorical_Figures_Survey.md) |
| P003 | Cultural Bias Matters: A Cross-Cultural Benchmark Dataset and Sentiment-Enriched Model for Understanding Multimodal Metaphors | 2025；ACL 2025 Long Papers；CCF-A；会议主会正式论文 | AN（已分析，全文程度未核） | [官方/登记页](https://aclanthology.org/2025.acl-long.1275/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P003_MultiMM.md) |
| P007 | Recent Advances in Online Hate Speech Moderation: Multimodality and the Role of Large Models | 2024；Findings of the Association for Computational Linguistics: EMNLP 2024；CCF-B；Findings正式论文（非主会） | PA（仅元数据/待分析） | [官方/登记页](https://aclanthology.org/2024.findings-emnlp.254) |
| P010 | Spoken in Jest, Detected in Earnest: A Systematic Review of Sarcasm Recognition—Multimodal Fusion, Challenges, and Future Prospects | 2025；IEEE Transactions on Affective Computing；CCF-B；期刊论文 | PA（仅元数据/待分析） | [官方/登记页](https://ieeexplore.ieee.org/document/11173951/) |
| P011 | Pragmatics in the Era of Large Language Models: A Survey on Datasets, Evaluation, Opportunities and Challenges | 2025；ACL 2025 Main Conference (Long Papers)；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2025.acl-long.425/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P011_Pragmatics_LLM_Survey.md) |
| P015 | LLMs in Sarcasm Detection? It’s elementary! (Or is it?) | 2026；ACL 2026 Main Conference (Long Papers; CCF-A)；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2026.acl-long.1346/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P015_LLMs_in_Sarcasm_Detection.md) |
| P019 | Understanding Figurative Meaning through Explainable Visual Entailment | 2025；NAACL 2025 Main Long Papers；CCF-B；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2025.naacl-long.1/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P019_V-FLUTE.md) |
| P020 | (RSA)²: A Rhetorical-Strategy-Aware Rational Speech Act Framework for Figurative Language Understanding | 2025；ACL 2025 Main Conference (Long Papers)；CCF-A；会议主会正式论文 | AN（已分析，全文程度未核） | [R4-02来源](R4_02_Paper_Allocation.md) |
| P022 | Revisiting a Pain in the Neck: A Semantic Reasoning Benchmark for Language Models | 2026；ACL 2026 Main（CCF-A）；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2026.acl-long.210/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P022_SemanticQA.md) |
| P023 | “Newspaper Eat” Means “Not Tasty”: A Taxonomy and Benchmark for Coded Language in Real-World Chinese Online Reviews | 2026；ACL 2026 Main Conference (Long Papers)；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2026.acl-long.426/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P023_CodedLang.md) |
| P024 | Analyzing Offensive Language Dataset Insights from Training Dynamics and Human Agreement Level | 2025；COLING 2025 Main；CCF-B；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2025.coling-main.653/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P024_CONELA.md) |
| P029 | RV-HATE: Reinforced Multi-Module Voting for Implicit Hate Speech Detection | 2026；ACL 2026 Main (Long Papers)；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2026.acl-long.2104/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P029_RV-HATE.md) |
| P030 | SMARTER: A Data-efficient Framework to Improve Toxicity Detection with Explanation via Self-augmenting Large Language Models | 2026；ACL 2026 Main；CCF-A；会议主会正式论文 | AN（已分析，全文程度未核） | [官方/登记页](https://aclanthology.org/2026.acl-long.1584/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P030_SMARTER.md) |
| P032 | Generalizable Implicit Hate Speech Detection Using Contrastive Learning | 2022；COLING 2022；CCF-B；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2022.coling-1.579/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P032_ImpCon.md) |
| P033 | Causality Guided Representation Learning for Cross-Style Hate Speech Detection | 2026；The Web Conference (WWW 2026; CCF-A)；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://doi.org/10.1145/3774904.3792669)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P033_CADET.md) |
| P034 | CrossGuard: Safeguarding MLLMs against Joint-Modal Implicit Malicious Attacks | 2026；ACL 2026 Main Conference (Long Papers; CCF-A)；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2026.acl-long.1178/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P034_CrossGuard.md) |
| P035 | Enhancing Hyperbole and Metaphor Detection with Their Bidirectional Dynamic Interaction and Emotion Knowledge | 2025；ACL 2025 Main（CCF-A）；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2025.acl-long.23/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md) |
| P037 | VLSBench: Unveiling Visual Leakage in Multimodal Safety | 2025；ACL 2025 Main（CCF-A）；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2025.acl-long.405/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P037_VLSBench.md) |
| P038 | VLSU: Mapping the Limits of Joint Multimodal Understanding for AI Safety | 2026；ICLR 2026（CCF-A）；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md) |
| P039 | ThinkingGuard: Decoding Implicit Hazards via Step-by-Step Risk Attribution in Multimodal Large Language Models | 2026；ACM MM 2026（作者称已录用；DOI 已登记；正式出版待核）；CCF-A；作者录用声明 | PF-R0（目录记载） | [R4-02来源](R4_02_Paper_Allocation.md) |
| P040 | Meerkat-VL: Implicit Risk Safety Alignment in Multimodal LLMs via Perceptual Reasoning and Self-Verification | 2026；ICML 2026（CCF-A）；CCF-A；会议主会正式论文 | PF-R0（目录记载） | [官方/登记页](https://proceedings.mlr.press/v306/zhou26ae.html)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P040_MeerkatVL.md) |
| P041 | Safe Inputs but Unsafe Output: Benchmarking Cross-modality Safety Alignment of Large Vision-Language Models | 2025；NAACL 2025 Findings；CCF-B；Findings正式论文（非主会） | PF-R0（目录记载） | [官方/登记页](https://aclanthology.org/2025.findings-naacl.198/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P041_SIUO.md) |
| T015 | The Hateful Memes Challenge: Detecting Hate Speech in Multimodal Memes | 2020；NeurIPS 2020，Advances in Neural Information Processing Systems 33；CCF-A；NeurIPS 2020 正式论文集论文 | PA（仅元数据/待分析） | [官方/登记页](https://papers.nips.cc/paper/2020/hash/1b84c4cee2b8b3d823b30e2d604b1878-Abstract.html) |
| R2A-001 | DRInQ: Evaluating Conversational Implicature with Controlled Context Variation | 2026；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2026.acl-long.1597/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_01_DRInQ.md) |
| R2A-002 | VAGUE: Visual Contexts Clarify Ambiguous Expressions | 2025；ICCV Main；CCF-A；ICCV Main | PF-R2B（全文卡） | [官方/登记页](https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_02_VAGUE.md) |
| R2A-003 | Can Your Model Tell a Negation from an Implicature? Unravelling Challenges With Intent Encoders | 2024；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2024.acl-long.33/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_03_Negation_vs_Implicature.md) |
| R2A-004 | Rhetorical Questions in LLM Representations: A Linear Probing Study | 2026；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2026.acl-long.5/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_04_Rhetorical_Questions_Linear_Probing.md) |
| R2A-006 | Silent Signals, Loud Impact: LLMs for Word-Sense Disambiguation of Coded Dog Whistles | 2024；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2024.acl-long.675/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_01_Silent_Signals.md) |
| R2A-007 | Making FETCH! Happen: Finding Emergent Dog Whistles Through Common Habitats | 2025；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2025.acl-long.284/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_02_FETCH.md) |
| R2A-008 | Uncovering and Mitigating the Hidden Chasm: A Study on the Text-Text Domain Gap in Euphemism Identification | 2024；AAAI 2024 Technical Track；CCF-A；AAAI Technical Track | PF-R2B（全文卡） | [官方/登记页](https://ojs.aaai.org/index.php/AAAI/article/view/29786)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_03_Hidden_Chasm_FA_Net.md) |
| R2A-010 | New Terms, New Toxicity: Consensus-based Chinese Neologism Toxicity Detection via Search-Augmented LLMs | 2026；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2026.acl-long.1602/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_01_SeTox.md) |
| R2A-011 | When People are Floods: Analyzing Dehumanizing Metaphors in Immigration Discourse with Large Language Models | 2025；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2025.acl-long.398/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_02_When_People_are_Floods.md) |
| R2A-012 | Sheep’s Skin, Wolf’s Deeds: Are LLMs Ready for Metaphorical Implicit Hate Speech? | 2025；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2025.acl-long.814/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2b_reading/R2B_B2b_03_Sheeps_Skin_Wolfs_Deeds.md) |
| R2A-013 | AUTALIC: A Dataset for Anti-AUTistic Ableist Language In Context | 2025；ACL Main；CCF-A；ACL Main | PF-R3B（全文+专项） | [官方/登记页](https://aclanthology.org/2025.acl-long.1022/)；[R3-B专项](../R3_targeted_reading/R3B_01_AUTALIC_FINAL.md) |
| R2A-017 | M3UCD: A Multi-task Multimodal Metaphor Understanding Challenge Dataset for LLMs | 2026；AAAI 2026 Technical Track；CCF-A；AAAI Technical Track | PF-R2B（全文卡） | [官方/登记页](https://ojs.aaai.org/index.php/AAAI/article/view/40808)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_01_M3UCD.md) |
| R2A-018 | Multi-Granular Multimodal Clue Fusion for Meme Understanding | 2025；AAAI 2025 Technical Track；CCF-A；AAAI Technical Track | PF-R2B（全文卡） | [官方/登记页](https://ojs.aaai.org/index.php/AAAI/article/view/34801)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_02_MGMCF.md) |
| R2A-019 | Two Streams, One Sarcasm: Orthogonal Expert Tuning for Holistic Multimodal Sarcasm Understanding | 2026；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2026.acl-long.319/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B3a_reading/R2B_B3a_03_DOSE.md) |
| R2A-020 | MMSD3.0: A Multi-Image Benchmark for Real-World Multimodal Sarcasm Detection | 2026；CVPR Main；CCF-A；CVPR Main | PA（仅元数据/待分析） | [官方/登记页](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_MMSD3.0_A_Multi-Image_Benchmark_for_Real-World_Multimodal_Sarcasm_Detection_CVPR_2026_paper.html) |
| R2A-024 | Conditional Information Bottleneck for Multimodal Fusion: Overcoming Shortcut Learning in Sarcasm Detection | 2026；AAAI 2026 Technical Track；CCF-A；AAAI Technical Track | PF-R3B（全文+专项） | [官方/登记页](https://ojs.aaai.org/index.php/AAAI/article/view/39874)；[MCIB专项](../R3_targeted_reading/R3B_02_MCIB_CIB_Attribution_Audit.md) |
| R2A-027 | Multimodal Situational Safety | 2025；ICLR Main；CCF-A；ICLR Main | PF-R2B（全文卡） | [官方/登记页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md) |
| R2A-028 | Is Your Multimodal Language Model Oversensitive to Safe Queries? | 2025；ICLR Main；CCF-A；ICLR Main | PF-R2B（全文卡） | [官方/登记页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md) |
| R2A-029 | Can’t See the Forest for the Trees: Benchmarking Multimodal Safety Awareness for Multimodal LLMs | 2025；ACL Main；CCF-A；ACL Main | PF-R2B（全文卡） | [官方/登记页](https://aclanthology.org/2025.acl-long.832/)；[原阅读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_03_MMSafeAware.md) |

## 11. R5正文前必须保留的证据缺口与写作动作

| 优先级 | 涉及小节 | 可以引用 | 禁止越界与定向补证 |
|---|---|---|---|
| P0 | 5.4 | AUTALIC引用/反用质性案例、三人标注、κ=0.25 [P] | 不能称加语境带来已量化因果增益；2400 vs 242+2160统计未核；遵守数据许可 |
| P0 | 6.5 | MCIB AAAI 2026 Technical作者报告MUStARD++R weighted F1=75.64，结构消融 [P] | 条件IB本身缺等预算正交消融；公开代码MSE广播与残差旁路 [S] 不等于正式运行必受影响；Table1指标口径待核 |
| P0 | 7.1–7.2 | VLSU分文本/视觉/联合判断的任务构型 [P] | 论文8187与公开8159不同；strict S-S-U公开35条且test-only，不能扩大全库成立 [S/O] |
| P1 | 6.3–6.4/8.2 | MultiMM gold情绪、MGMCF源目标字段、DOSE选项捷径的静态线索 [S] | 不能称训练结论已严格证明正确联合语义或独立情绪增益，须核同预算与正式运行版本 |
| P1 | 4.2–4.5 | Silent Signals已知定义消歧、FETCH词典留出、SeTox搜索辅助毒性 [P/S] | 不能归为严格时间外、开放世界编码词自动发现 |
| P1 | 5.3/7.5 | Flood隐喻源域GT、Sheep合成仇恨正例协议、MOSSBench误拒评测 [P] | 缺独立逐例非人化GT/负侧错误或对照充分性 |
| P1 | 7.3 | ThinkingGuard存在录用/DOI及作者研究先例 | ACM MM正式出版与实际Track待独立核实，不计入已核主会正式发表 |
| P1 | 1.2 | 已入库相关综述足以开展子域范围比较 | 尚缺逐篇时间窗、任务、模态、评价、本文增量核验；禁止‘首篇全面综述’ |
| P2 | 2.1 | Grice、Searle、RSA可为理论锚点 | R5补经典原典与可靠书目；不强制为语言学原典标CCF类别 |

## 12. 覆盖核计与阶段裁决

- 46条论证链：Ch1=4、Ch2=5、Ch3=5、Ch4=6、Ch5=6、Ch6=7、Ch7=5、Ch8=6、Ch9=2；各小节至少一条“可写主张→已登记论文/内部审计→限定条件”。**不等于46条都拥有可用于因果机制的强实证证据**。
- 第1章相关综述比较、第8章开放挑战、第9章展望含明显H/O成分，正式写作应按编辑/研究者综合观点署明；未读摘要候选不能成为训练机制、数字强证据。
- R4-3结论为 **CONDITIONAL PASS FOR EVIDENCE MAPPING，NOT FINAL FOR R5 CITATION**。R4-4图表和R4-5前两章已经形成审阅稿并与本矩阵对照；仍不重写R3、不修改91篇旧索引。R4整体及各项稿件是否**定稿/合并main**，须另经用户确认。

### 核心审计上游

- [R4-01正式目录](R4_01_Formal_Outline.md)；[R4-02论文映射](R4_02_Paper_Allocation.md)
- [R3-A4证据审计](../R3_evolution/R3A_Coverage_and_Evidence_Audit.md)；[R3-A3叙事](../R3_evolution/R3A_Survey_Narrative.md)；[R3-A2方法](../R3_evolution/R3A_Method_Evolution.md)
- [AUTALIC×MCIB双篇终审](../R3_targeted_reading/R3B_03_AUTALIC_MCIB_Cross_Paper_Synthesis_FINAL.md)
- [B1语用](../R2_literature_extension/B1_reading/R2B_B1_Synthesis_DRAFT.md)；[B2a编码](../R2_literature_extension/B2a_reading/R2B_B2a_Synthesis.md)；[B2b隐晦有害](../R2_literature_extension/B2b_reading/R2B_B2b_Synthesis.md)
- [B3a多模态修辞](../R2_synthesis/B3a_Cross_Paper_Synthesis.md)；[B4a情境安全](../R2_synthesis/B4a_Cross_Paper_Synthesis.md)；[R2-D证据冲突](../R2_registry/Metadata_and_Evidence_Conflicts.md)