# R6-Fix｜引文一致性、数据版本与评测口径审计

> **2026-11-10 R6-Fix-R1增量更新（基线PR #61）；学术事实与技术排版终审仍需独立R6-A复审及R6-V验收。** 依据R5-C固定稿 `c04d6a23e864923acd64c192c8b05dc597c2bb90` 与本分支 `Survey_Full_Draft.md`、`references.bib`、T2–T7、原R2/R3精读卡。标注 F=正式元数据、P=论文作者报告、S=现有公开数据/源码静态审计、H=综述推断、O=未闭合；绝不从文件访问推断实验已运行。

## 一、引用键与书目直接验证结果

R6-Fix-R1检查脚本为[verify_r1.py](../R6_fix_r1/verify_r1.py)，只验证机械一致性，非独立学术终裁。

| 检查项 | 本轮实际结果 | 限制 |
|---|---|---|
| Bib条目头／唯一键 | **49／49**，原48条保留，仅追加Ye摘要级综述对照 | 括号平衡与唯一键不是完整BibTeX解析／样式编译 |
| 九章主体（排除附录和文末书目）引用 | **49**，与Bib集合相等，无缺引／冗余 | 并不证明全部出版字段准确 |
| 手写书目 | **49条／49唯一键**，与Bib相等 | 人工字段一致性仍需R6-V |
| 附录B用途目录 | **49键，逐键恰好一次** | 原48＋新Ye；用途分组不冒充PRISMA筛选记录 |
| 表1–7引用和列数 | 全部键在Bib中；Markdown列数一致 | 不替代真实排版渲染 |
| 固定公开代码／发布数据 | 六组40位commit＋file#line在**正文附录A**；VLSU CSV按固定blob重计8159／35／141 | S≠论文正式run；不需外审进入私人索引 |

Ye（arXiv:2502.14881v1，预印本，CCF不适用／正式状态未核）只按作者摘要／目录作相关综述定位，未伪称全文审计。原91候选是59＋32登记，32仅相对R0题名不重，不等于全面去重后91篇，更不是49条的PRISMA分母。

**新增论文定位（F/P）**：ExPO-HM, *Learning to Explain-then-Detect for Hateful Meme Detection*，ICLR 2026 Main（**CCF-A**），[正式出版页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)、[OpenReview原稿](https://openreview.net/forum?id=bEejbORUI5)、[项目P027精读](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)。在综述中属于**仇恨Meme的解释后检测**，不是VLSU式严格`y_I=Safe/y_T=Safe/y_IT=Unsafe`输入三条件标签。原作者报告HatefulMemes宏F1 naive GRPO 74.5→组合方案81.1，RA-HMD 80.2；CDE是决策熵代理，不是已验证解释因果faithfulness。

**经典理论补充**：Searle (1975), *Indirect Speech Acts*, Cole & Morgan (eds.), *Syntax and Semantics Vol.3*, pp.59–82；与1969专著都保留；书章无CCF等级。ThinkingGuard依作者预印本/接收声明处理，**ACM MM会议CCF-A不等于已核正式Main Track**；手写参考列表已删除其多余Markdown强调，但最终元数据仍待出版社核。

## 二、核心数据/论文版本与分母：事实与OPEN严格隔离

| 论文/会场等级 | 正式论文作者报告（P） | 公开材料S或待核O（VLSU本轮按固定blob重计；其他明确标历史／未固定） | **综述允许结论/不能推断内容** | 未闭合（O） |
|---|---|---|---|---|
| **VLSU**｜ICLR 2026，CCF-A | 正式PDF **8187**样本、15安全类、17组合、17评测模型；严格S-S-U **37**；Figure5作者示例Qwen2.5-VL-32B约33.8%为该模型**joint三分类已错误**集合中I/T均正确的比例，非17模型汇总；Table1另采用二分类`Borderline→Safe` | 本轮重读固定blob `09421adeb2e68eac1d5e829dcbd48848f21a0be6`：**8159**记录、S-S-U **35**、`not_sure` **141**；脚本见正文附录A；Figure5本轮可读作者v2图，正式PDF超时 | 同报告PDF和CSV各自统计；严格S-S-U极小；33.8%**不**是全数据或S-S-U漏检率，也非三分类F1 | 少28行缘由、图像实际可达率、摘要11 vs PDF17；**正式版Figure5图题／模型对应仍待独立复核** |
| **AUTALIC**｜ACL 2025 Main，CCF-A | 总2400条；论文正242+负2160 **合计2402**；9位受训高年级本科志愿者/每例3票，`-1`并入非歧视0再多数票；κ=0.25；上下文质性案例，不是同模型去上下文增益 | 原始受限CSV未独立打开 | 论文存在2条算术不符**确定**，真实CSV标签分布**未知**；质性语境例≠因果模型表现 | 原CSV真实分布、ACL论文PDF/网页作者差异及许可下样本用途 |
| **Silent Signals**｜ACL 2024 Main，CCF-A | 主模型筛阳数据 **16550**；400正例抽查人审precision约85.3%，广义可接受编码义约89.4% | 历史发布说明提示版本差；本轮未固定README，撤去精细发布整数，记O | 人审precision不能当模型筛选全程总体recall或“16550人工逐条金标” | 历史README不可变版本及全量数据一致性 |
| **MMSafeAware**｜ACL 2025 Main，CCF-A | 联合二分类Unsafe1000/Over-Safety500，共**1500**；三条件人审筛选原则 | 历史发布文件／配图／重复情况未固定版本和计数链；本轮撤去精细整数，记O | 作者1500是论文P；未固定发布文件不能替换该评测分母；类别2:1令恒判Unsafe总Acc **66.67%**，还需安全侧召回 | 官方发布commit与全部图片实物解码、论文实际评测文件版本及图像级近重复 |
| **MOSSBench**｜ICLR 2025 Main，CCF-A | 作者安全意图图文主集300条；约**9%**有人工安全作答争议 | contrast逐ID映射／发布数量本轮未固定，撤去精细整数，记O | ARR是响应拒答而非输入二分类FPR；300主例并非全部严格的单因素有害对照 | 争议样本逐人标签和有害对照GT完整复核 |
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

**本轮完成**：主体／Bib／手写书目49键一致，附录B逐键目录49项；表3/5/6/7同步；六组固定公开源码直接纳入正文附录A；VLSU固定CSV重计；8项增量与限制见[R1任务台账](../R6_fix_r1/R6FixR1_Eight_Issue_Change_Ledger_20261110.md)。

**未完成或仍需独立核验**：正式VLSU PDF本轮超时，Figure5模型／图题仅通过作者版本、作者镜像检索和既有精读交叉核，不能自判Gate D全文版本复核通过；RSA/VAGUE所加定点数字的作者版本与会议版逐页一致性亦O。跨域C1–C3的学术增量需独立评审；任何公开源码与正式run对应均未认证。

**R6-V另行验收**：真实BibTeX parser及样式编译、出版社字段／Track校对、图形与表格的实际渲染、DOCX/PDF内容同步。本轮不覆盖R6-A／R6-V文件、不合并PR、不宣布SUBMISSION-READY。
