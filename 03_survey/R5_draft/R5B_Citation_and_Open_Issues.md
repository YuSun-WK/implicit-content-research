# R5-B 引文、证据位置与待审事项（2026-11-09）

本文件服务于第6–8章初稿的可追溯审阅及 R5-C 整合。**P**＝正式论文作者报告，**S**＝项目对所查公开代码／数据的静态观察，**H**＝本综述综合判断，**O**＝尚无足够证据；正式出版事实另以出版方页面核对。S 不自动推翻 P，H／O 不得写成原论文的实验结果。以下表号、章节与指标只在已阅读卡或 R5-E 审计明确登记时列出；不以内部阅读卡代替投稿版 BibTeX。

## 1. 第六章核心论文：正式入口与可引用证据

| 编号／论文及出版 | 正式入口 | 已登记的直接证据位置与主张边界 | 待核 |
|---|---|---|---|
| P003 MultiMM；ACL 2025 Main，CCF-A | [ACL](https://aclanthology.org/2025.acl-long.1275/) | §3、Table 1：8,461图文广告及源／目标／情绪标签；§5–6、Tables 2–3：SEMD及情绪消融。所查公开代码测试读入人工情绪〔S〕；主表／消融数值并不完全一致。 | 正式实验的情绪来源、仅原始图文的端到端表现、跨文化来源控制。 |
| P019 V-FLUTE；NAACL 2025 Main，CCF-B | [ACL Anthology](https://aclanthology.org/2025.naacl-long.1/) | §3、Table 1：6,027图文主张—蕴含—解释实例；§4、Table 4：F1@0 与解释阈值分数；§5、Appendix H/J：解释人评、少样本模型与附加训练比较。 | 测试子集校准 F1@53、按图像身份分组和解释干预；不得称参考文本相似度为忠实性。 |
| R2A-017 M3UCD；AAAI 2026 Technical，CCF-A | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/40808) | §3、Tables 1–3、Fig. 4：15,345实例、细粒度分类／概念任务；§4–5、Table 4：共享 LoRA 的正负任务迁移。 | 原始“12标签”与预测形式数量、概念生成的人审一致性；Complementary 不是模型双模态必要性实验。 |
| R2A-018 MGMCF；AAAI 2025 Technical，CCF-A | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/34801) | Methodology、Tables 1–2：图文＋源／目标辅助文本、对象和 Global–Local 模块、四项分类与结构消融。所查源码测试加载域特征且 Dual-Semantic 损失路径与论文描述不一致〔S〕。 | 源／目标特征的 gold／预测来源、发表表格实际代码版本、同模型去模态控制。 |
| R2A-019 DOSE；ACL 2026 Main，CCF-A | [ACL Anthology](https://aclanthology.org/2026.acl-long.319/) | §3–5、Tables 3–5：双流低秩专家、五任务等权 Accuracy 与去正交消融；Target 单项反向变化。公开 1% 训练子集的选项位置／长度是风险线索〔S〕。 | 完整 test 选项重排、论文五任务与代码默认六任务、同预算梯度冲突验证。 |
| R2A-024 MCIB；AAAI 2026 Technical，CCF-A | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/39874) | §3–4、Tables 1–2：MUStARD++R 完整模型 weighted F1 75.64、去细粒度 71.19、MLP 替换 74.32〔P〕。公开 Transformer 路径的 MSE 形状及文本残差旁路见[R3-B 专项](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R3_targeted_reading/R3B_02_MCIB_FINAL.md)与[R5-E 审计](https://github.com/YuSun-WK/implicit-content-research/blob/survey/r5-evidence-audit-20261109/03_survey/R5_evidence/High_Priority_Evidence_Audit.md)〔S〕。 | 等参数／预算去 KL、去条件预测与双去除；正式训练代码版本、主文／扩展版目标函数对齐。公开风险不等于论文表格错误。 |
| R2A-020 MMSD3.0；CVPR 2026 Main，CCF-A | [CVF 官方页](https://openaccess.thecvf.com/content/CVPR2026/html/Zhao_MMSD3.0_A_Multi-Image_Benchmark_for_Real-World_Multimodal_Sarcasm_Detection_CVPR_2026_paper.html) | 本项目目前仅摘要／元数据级候选〔PA〕，用于说明多图反讽研究存在。 | 全文任务、数字、方法及消融均不得从摘要补造。 |

第六章的表 T5 和图 F4 需分别呈现输入字段／任务协议与模态依赖诊断。MGMCF 的源／目标作为输入，M3UCD 的源／目标作为预测目标；MultiMM 的 gold 情绪与 DOSE 的候选选项均应显式登记。

## 2. 第七章核心论文：正式入口与证据对象

| 编号／论文及出版 | 正式入口 | 可引用的实验位置及实际测量对象 | 待核 |
|---|---|---|---|
| T015 Hateful Memes；NeurIPS 2020 正式论文集，CCF-A | [NeurIPS](https://papers.nips.cc/paper/2020/hash/1b84c4cee2b8b3d823b30e2d604b1878-Abstract.html) | 项目目前仅摘要／目录级，作为普通 Meme 有害检测背景。 | 不以其全体样本代表严格 S-S-U。 |
| P034 CrossGuard；ACL 2026 Main，CCF-A | [ACL Anthology](https://aclanthology.org/2026.acl-long.1178/) | §3–6、Table 1：Guard 防护／攻击成功协议；Table 2：ImpForge 改写的红队攻击；Figs. 4–5：有无生成数据与 PPO 对照。SIUO 上报告含 ImpForge 与不含数据的 ASR 5.39／60.33，但基准、模型类型的 ASR 操作定义不完全同质〔P〕。 | 1390 红队样本与约202隐含风险训练样本关系、三条件人工标签、PPO 同预算比较、论文奖励与公开代码版本差异。 |
| P037 VLSBench；ACL 2025 Main，CCF-A | [ACL Anthology](https://aclanthology.org/2025.acl-long.405/) | §3–5、Tables 1/2/4：文本风险泄漏诊断及回应 Safe Rate；回应可分拒答／警告／不安全。 | 评审器与真实输入风险 GT 的关系、正常安全负例、近重复及评测脚本版本。 |
| P038 VLSU；ICLR 2026 正式会议，CCF-A | [正式 PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)；[官方摘要](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html) | §3–4、Table 1：二分类输入理解协议；Tables 2–3：三分类与回应；Fig. 5：联合错误样本中约34%“两单模态预测均正确”；Fig. 9：论文严格 S-S-U 37。PDF 报 8,187 条、17 模型。 | 已审[公开 CSV](https://github.com/apple-aiml-research/ml-vlsu/blob/main/data/VLSU.csv) 8,159 条、严格 S-S-U 35（test-only）；摘要仍写11模型。少28条原因、141 image not_sure 处理、图片可达性及模型数量差异原因均 O。 |
| P039 ThinkingGuard；作者称 ACM MM 2026 接收，会议 CCF-A | [作者公开稿](https://arxiv.org/abs/2609.36562)；[仓库](https://github.com/FroggyChen/ThinkingGuard) | 作者稿 §3–5、Tables 1/3：TriggerBench 配对、SA-MCTS 搜索、Step／Trajectory-DPO 与风险分类消融〔P〕。 | **ACM 出版社最终记录与实际 Track 尚未独立核实**；Oral 不是 Track；配对图像单因素有效性、奖励提示、等预算 Step-DPO 贡献均 O。 |
| P040 Meerkat-VL；ICML 2026 Main，CCF-A | [PMLR](https://proceedings.mlr.press/v306/zhou26ae.html) | 正式论文与公开训练路径：cold-start SFT、Actor 自评、GRPO；输出安全与帮助性〔P/S〕。精读卡未逐项核对完整正式表格数值，正文不报未核百分比。 | 自评时的风险文字信息预算、图像是否被再次读取、奖励系数版本差和独立模块收益。 |
| P041 SIUO；NAACL 2025 Findings，NAACL 会议 CCF-B | [ACL Anthology](https://aclanthology.org/2025.findings-naacl.198/) | 联合输入触发不安全回应的行为基准；不是 VLSU 式单／联合输入三等级人审 GT。 | 与输入 Guard F1 不可直接同比。 |
| R2A-027 Multimodal Situational Safety；ICLR 2025 Main，CCF-A | [ICLR](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html) | MSSBench 1,960图文对；QC／IC 显式判断和 IF 回应行为分开。 | Oracle 状态预算、Chat 与 Embodied 配对条件、IF Judge 对真实帮助性的代表性。 |
| R2A-028 MOSSBench；ICLR 2025 Main，CCF-A | [ICLR](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html) | 300 条安全主集的过度拒答与部分危险对照；是行为指标。 | 部分众包安全判断分歧、并非全量严格配对、拒答 Judge 复核。 |
| R2A-029 MMSafeAware；ACL 2025 Main，CCF-A | [ACL Anthology](https://aclanthology.org/2025.acl-long.832/) | 1,000 Unsafe＋500 Over-Safe 的联合输入二分类；报告危险与安全侧表现。 | 所查公开 prompt／图片文件与论文数目不一致；三条件逐例人审真值未公开。 |

第七章图 F5、表 T6 要固定四层：**G_in 输入真值；P_in 可观察的显式判断；R_beh 响应行为；Q_out 输出安全与帮助性**。CrossGuard 的 Guard 漏判、攻击者的生成 ASR、VLSBench 的回复 Safe Rate、VLSU 的输入 F1 和 MOSSBench 的正常请求误拒，不能当作同一指标。VLSU 的 S-S-U 只是多种组合关系之一，不用 179 条广义风险升级子集替换其 35／37 条严格口径。

## 3. 第八章横向方法引文

- 概率语用：〔P020〕[(RSA)²，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1019/)，候选意义与先验对照见 R3-A2 §1；递归更新的独立贡献未充分隔离。
- 对比和域迁移：〔P032〕[ImpCon，COLING 2022 Main，CCF-B](https://aclanthology.org/2022.coling-1.579/)；〔R2A-008〕[FA-Net，AAAI 2024 Technical，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/29786)；〔P033〕[CADET，WWW 2026 Main，CCF-A](https://doi.org/10.1145/3774904.3792669)。具体 GT 与公开版本限制见第4、5章及 R3-A2 §2。
- 检索与动态义：〔R2A-006〕[Silent Signals，ACL 2024 Main，CCF-A](https://aclanthology.org/2024.acl-long.675/)；〔R2A-007〕[FETCH!，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.284/)；〔R2A-010〕[SeTox，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1602/)。词典留出、固定基础模型未知与真实时间外发现不可混称。
- 解释与偏好：〔P030〕[SMARTER，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1584/)；〔R2A-012〕[Sheep’s Skin，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.814/)；〔R2A-013〕[AUTALIC，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1022/)。解释或多数票不等于真实意图；AUTALIC 总量 2,400 与正文正负合计 2,402 的算术不一致继续保留。
- 多模态意义与安全方法的其余正式链接、章节／表号分别见上两节；R3-A2 的方法史只作为综合入口，不取代原论文出处。

## 4. 已确认争议与开放结论

1. **VLSU〔P/S/O〕**：PDF 8,187／公开 CSV 8,159；PDF Fig. 9 严格 S-S-U 37／所查 CSV 35；PDF 17 模型／官方摘要 11 模型。不同版本不能选择性混用。公开 35 条为 test-only，不能作为有统计把握的完整训练分布；图片可用性与 28 条差异原因仍待查。
2. **MCIB〔P/S/O〕**：完整模型和结构消融可按 Table 2 引用；条件瓶颈自身没有等预算去除实验。公开代码的 MSE 广播风险、原始文本残差及论文／代码目标差异是静态观察，不构成正式训练错误的既定事实。
3. **MultiMM、MGMCF、DOSE〔P/S/O〕**：所查公开代码的测试 gold 情绪、源／目标特征与公开训练子集的选项偏斜须标信息预算及样本范围。完整测试集、正式运行版本和同资源反事实尚待核；不能据静态线索直接判定论文成绩无效。
4. **ThinkingGuard〔作者稿／O〕**：已有作者接收、DOI 和公开稿线索，但 ACM 最终书目及 Track 未独立关闭。出版状态不可改写为正式 Main。配对图像严格单变量及步骤奖励、偏好预算亦未关闭。
5. **CrossGuard、Meerkat-VL〔P/S/O〕**：前者论文奖励公式和公开实现有差异，Guard 漏判与生成攻击 ASR 应分开；后者自评可能见到训练期风险文字且不在评分调用重新读图。不能把模型总体收益直接归为正确联合风险感知的独立作用。

## 5. R5-A 衔接与待审清单

- 第5章 §5.6 已准确把文本危害 T4、第6章意义任务和第7章联合风险／响应分开；第6章 §6.1 接其论证，无须重写前文。
- 第3–5章仍使用“作者报告／静态审计／综述判断”，本轮与之对齐。第6章的意图是标注者对交际目的的判断，与第3章 DRInQ 候选共识及第5章作者立场边界一致。
- 第3章的〔P020〕(RSA)² 正式 ACL PDF 与 arXiv v1 公式编号仍有待逐页对齐；本轮第8章只引方法类别，不重报公式编号。后续 R5-C 统一核对。
- 第5章对 AUTALIC 算术不一致与无删语境定量消融已有保留；第8章只作交叉引用。第5章、R5-E 与本轮对 IJCAI 2024 Survey Track 均不得沿用旧“CCF-A”口径；项目采用 CCF 2026 第七版，IJCAI 为会议 CCF-B，Survey Track 需单列。
- 第3–5章篇幅较紧凑，R5-C 需检查直接竞争方法、参考文献格式与图表引入，不以本轮横向综合替代前文具体机制解释。以上仅为待审，**本轮没有修改 R5-A 的文件**。

## 6. 图表与 R5-C 整合建议

- **F4／T5（第6章）**：分别表示受控模态干预路径和逐篇原始／辅助输入协议，尤其区分 OCR、gold 情绪、源目标域与音视频转写。F4 为概念图，不画虚构性能曲线。
- **F5／T6（第7章）**：F5 固定 G_in、P_in、R_beh、Q_out 四层；T6 列三条件 GT、双侧指标、Judge、数据版本和许可。VLSU 版本争议写进表注。
- **F6／T7（第8章，可压缩或附录）**：方法族×瓶颈的定性映射，标明训练信号与公平对照，避免伪造跨任务名次。
- **R5-C**：先将 PR #54、#55 与本 PR 按审阅意见整合，再核实全稿术语、编号和正式 BibTeX；把第1章相邻综述对照、第2章 Task=(X,Y,G,E)、本章四层安全测量连成前后一致的定义。章节结语不得把证据缺口写为已证实的“首次研究空白”。关键表号、PDF 版本和开源文件观察时间应在统一参考文献／数据版本登记中保留。本文不建议在这些事项完成前宣称稿件可投稿，但**建议进入 R5-C 的全文整合工作**。
