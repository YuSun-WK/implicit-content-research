# R6-Fix｜引文一致性、数据版本与评测口径审计

> **R6-Fix-R1 2026-11-10版本提示（保留本文件作为PR#61历史快照）**：本文件以下的48/48/48引文、Silent/MMSafeAware/MOSS公开文件精准数字均仅对应第一轮R6-Fix的历史内部审计，**不代表本轮投稿正文实际引用数量或已经外部固定的发布统计**。新分支已加Mao相邻综述，现正文/Bib/手写书目为**49/49/49**，未钉定的上述发布S计数在新正文/表格中撤去或降为O。逐项新稿证据及未解Gate详见 [R6-Fix-R1八项修订台账](R6FixR1_Eight_Gates_Change_Evidence_Ledger_20261110.md)。原记录不删改以维持历史审计可追溯性。


> **2026-11-09，修订分支内部静态验证；学术事实与技术排版终审仍需独立R6-A复审及R6-V验收。** 依据R5-C固定稿 `c04d6a23e864923acd64c192c8b05dc597c2bb90` 与本分支 `Survey_Full_Draft.md`、`references.bib`、T2–T7、原R2/R3精读卡。标注 F=正式元数据、P=论文作者报告、S=现有公开数据/源码静态审计、H=综述推断、O=未闭合；绝不从文件访问推断实验已运行。

## 一、引用键与书目直接验证结果

对当前修订稿**实际内容**做独立字符串与键集合检查（不是仅看“文件已存在”）：

| 检查项 | 静态结果 | 限制 |
|---|---|---|
| `references.bib` 的BibTeX条目起始行 | **48**，键唯一48，无重复 | 按条目头 `@type{key,` 统计；**尚未用目标期刊编译器完整解析字段/样式**。 |
| 全文 `@citekey` 唯一集合 | **48**，全部能匹配Bib条目 | 文内可能重复引用同键；本次只验证键集合，无外部出版社逐字段证书。 |
| 书目中未被正文任何位置提及的条目 | **0** | 这是全文文本范围（含手写文末参考书目）；正文主体排除文末后是否所有48均被实质讨论，应由R6-V另作真正正文引用审计。 |
| 手写`# 参考文献`编号行 | **48条**、48不同键，与Bib键集合完全相同 | **手写列表仍需排版/字段/顺序复核**，不是自动从BibTeX生成的书目。 |
| 增补文献 | `mei2026expohm`、`searle1975indirect`均在Bib、正文、手写书目及Citation_Key_Mapping | ExPO按ICLR2026正式出版页建书目；Searle1975为经典书章，CCF不适用。 |
| T5/T6/T7关键校验 | **T5 DOSE输入为“新闻图像＋文章文本”**；T6有SIUO独立行；T7有ExPO-HM独立解释式分类行 | 这是科学字段存在性检查，不包含实际PDF/渲染器版面与SVG审查。 |

**新增论文定位（F/P）**：ExPO-HM, *Learning to Explain-then-Detect for Hateful Meme Detection*，ICLR 2026 Main（**CCF-A**），[正式出版页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)、[OpenReview原稿](https://openreview.net/forum?id=bEejbORUI5)、[项目P027精读](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)。在综述中属于**仇恨Meme的解释后检测**，不是VLSU式严格`y_I=Safe/y_T=Safe/y_IT=Unsafe`输入三条件标签。原作者报告HatefulMemes宏F1 naive GRPO 74.5→组合方案81.1，RA-HMD 80.2；CDE是决策熵代理，不是已验证解释因果faithfulness。

**经典理论补充**：Searle (1975), *Indirect Speech Acts*, Cole & Morgan (eds.), *Syntax and Semantics Vol.3*, pp.59–82；与1969专著都保留；书章无CCF等级。ThinkingGuard依作者预印本/接收声明处理，**ACM MM会议CCF-A不等于已核正式Main Track**；手写参考列表已删除其多余Markdown强调，但最终元数据仍待出版社核。

## 二、核心数据/论文版本与分母：事实与OPEN严格隔离

| 论文/会场等级 | 正式论文作者报告（P） | 已存公开材料观察（S，依以前归档卡；非本轮全量重做） | **综述允许结论/不能推断内容** | 未闭合（O） |
|---|---|---|---|---|
| **VLSU**｜ICLR 2026，CCF-A | 正式PDF **8187**样本、15安全类、17组合、17评测模型；严格S-S-U **37**；Figure5约33.8%为**joint预测已错误**样本中I/T各自预测正确的条件比例；Table1另采用二分类`Borderline→Safe` | 已审作者CSV **8159**完整行，S-S-U **35**；image_grade `not_sure` **141**；官方摘要早期**11模型** | 同报告PDF和CSV各自统计；严格S-S-U极小；33.8%**不**是全数据或S-S-U漏检率，也非三分类F1 | 少28行缘由、图像实际下载/授权可达率、作者官网11 vs PDF17差异 |
| **AUTALIC**｜ACL 2025 Main，CCF-A | 总2400条；论文正242+负2160 **合计2402**；9位受训高年级本科志愿者/每例3票，`-1`并入非歧视0再多数票；κ=0.25；上下文质性案例，不是同模型去上下文增益 | 原始受限CSV未独立打开 | 论文存在2条算术不符**确定**，真实CSV标签分布**未知**；质性语境例≠因果模型表现 | 原CSV真实分布、ACL论文PDF/网页作者差异及许可下样本用途 |
| **Silent Signals**｜ACL 2024 Main，CCF-A | 主模型筛阳数据 **16550**；400正例抽查人审precision约85.3%，广义可接受编码义约89.4% | 历史README检查主集**16258**记录 | 人审precision不能当模型筛选全程总体recall或“16550人工逐条金标” | 292差异的版本原因/可下载全量一致性 |
| **MMSafeAware**｜ACL 2025 Main，CCF-A | 联合二分类Unsafe1000/Over-Safety500，共**1500**；三条件人审筛选原则 | 此前项目卡所审发布状态：1523编号prompt、1453有编号图片、445种不同Git Blob、70无匹配图片 | 作者1500正式论文样本和可见发布文件是两种版本；类别2:1令恒判Unsafe总Acc **66.67%**，还需安全侧召回 | 官方发布commit与全部图片实物解码、论文实际评测文件版本及图像级近重复 |
| **MOSSBench**｜ICLR 2025 Main，CCF-A | 作者安全意图图文主集300条；约**9%**有人工安全作答争议 | 所审有害contrast **244** ID可与主数据匹配，非全部300 | ARR是响应拒答而非输入二分类FPR；300主例并非全部严格的单因素有害对照 | 争议样本逐人标签和有害对照GT完整复核 |
| **CrossGuard**｜ACL 2026 Main，CCF-A | Figure6 **1390** ImpForge攻击评测例；Figure7 Guard总**1616**混合训练例、联合隐含类**12.5%≈202**（换算，不是逐例真实整数）；Figure4 SIUO ASR **60.33→5.39**，FigStep **0.12→0.21** | 部分红队/Guard训练公开脚本已静态阅读，确切训练样本ID映射未锁定 | 红队攻击生成与Guard学习是不同阶段；Guard漏判ASR与在线/离线生成不安全回复ASR的Judge不同；**不能**断言1616含1390全部或精确哪202条 | 训练/评测逐例去重、PPO奖励论文实现对齐、模型/Guard同条件Judge |
| **ThinkingGuard**｜作者称ACM MM 2026接收，会议CCF-A，最终Track未核 | 作者报告TriggerBench **5600**图文实例(2800/2800)、离线SA-MCTS，Step-DPO Full Unsafe F1 **.810** vs without Step **.779** | 配对文本/ID能对应，但安全/不安全图片分别生成，非一张图的受控局部编辑；可公开的完整奖励/逐例人审材料不足 | 作者配置提升成立于其论文协议；**不**能独立归因真实Trigger因果忠实或排除更多Unsafe监督 | ACM正式最终书目与Track、严格pair控制、step奖励完整参数/预算 |
| **Meerkat-VL**｜ICML 2026 Main，CCF-A | 作者论文/README RL数据 **8436**，训练NPSV/DPCA+GRPO对齐安全与帮助 | 早期HF页面显示**8466**记录（实际Parquet未全量读取）；本轮已[固定自评代码](R6Fix_Public_Code_Evidence_Index.md)仅重新使用已生回答与规范风险说明，不重新传原图 | 有训练时规范risk/answer级教师条件的自评分，不等于推理时独立图像重审或输出风险分类F1 | 30条版本差、正式ICML全基线表、数据字段实际训练传递及同预算模块消融 |
| **DOSE**｜ACL 2026 Main，CCF-A | **新闻图像＋文章文本**、五种主反讽MCQ任务；人工模态贡献Text-dominant 61.9%/Equal22.5%/Image-dominant15.6%（所审定稿卡与论文） | 所审公开代码有可能第六task变体 | **模态已修正**；人工“主导”归属≠模型去模态行为或真正因果互补 | 完整不同数据版本与选项泄漏广泛性未独立证实 |
| **DRInQ**｜ACL 2026 Main，CCF-A | 初始至少4/5人共识819，筛400难例用于主困难评价（作者协议） | 早期公开CSV所审版本231条等，需区分任务子集 | 定向抽样的400不能概括自然交际总体；不同公开数据版本需明确 | 官网/发布文件差异缘由 |
| **MMSD3.0**｜CVPR 2026 Main，CCF-A | 正式出版页可确认多图反讽数据集与CIRM模型 | 本项目仅官方摘要/出版级核对 | 只用于多图技术先例；不引未经本项目精读的数值消融、图像因果结论 | 定点全文Table/Figure、样本许可与严格跨图依赖 |

## 三、不同“安全能力”评测协议绝不能偷换

- **输入风险`G_in/P_in`**：MMSafeAware与VLSU显式风险/严重度分类，危险Recall、Safe侧FPR（政策与标注来源必须给明）。
- **输出行为`R_beh`**：SIUO（NAACL 2025 **Findings**，举办会议CCF-B但**非Main**）与VLSBench拒答/警示/危险帮助比例。SafeRate高可能只是拒答率高；并非显式风险分类Accuracy。
- **响应质量`Q_out`**：Meerkat-VL、MOSSBench主要分析安全与合法帮助；拒答率低不自动等于帮助质量高。
- **CrossGuard ASR不同Judge**：红队改写使生成模型危险回应更频繁（攻击越成功ASR越高），Guard输出Safe/Unsafe的错误放行率（越低越好），在线生成的关键词拒答模板判定与离线生成GPT Judge不完全等同；论文五基准平均ASR是**五列等权算术均值**，不是整合样本分母统一加权。

## 四、真实检查已完成 vs 仍需Work/R6-V

**本轮完成**：GitHub文件一致性静态集合核对（48/48/48、无缺失重名）、新增ExPO正式论文且在正文/表7出现、DOSE模态表内纠错、风险数据版本按层列举，以及作者公开源码六组固定可公开commit/行号索引。R5-C老数据冲突台账仍保留而非篡改。

**R6-V另行必须做**：真实BibTeX parser解析及所需样式编译、引用键只取真正**正文区域**的审计、出版社作者/题名/页码/Track逐项核、F1–F5 SVG真实渲染与灰度/单双栏可读性、T1–T7真正版面和交叉链接检查、DOCX/PDF渲染内容对照。**本文件不能替代真实渲染或声称48条Bib字段已全部获出版社最终核准。**

**状态：R6-Fix已修改正文和科学表，科研修订待独立复审；本审计不自动关闭A4的3个P0。**
