# R6-Fix-Review｜24个唯一整改单元的独立学术复审矩阵

> **冻结PR#61稿**：`c125c6358c655951d07286763f3b7a3eed6e9275`；**审稿单独分支，只记录判决**。R6-A4的24项由原A0=11、A1=14、A2=18、A3=17合计60历史编号唯一映射，本表**复用相同主归属，不新生P0编号**。  
> **结果**：3 P0→1 CLOSED/2 PARTIAL；17 P1→11 CLOSED/6 PARTIAL；4 P2→4 CLOSED。合计**16 CLOSED/8 PARTIAL**。闭环标准必须就原A4目标审核，原始论文/公开代码不可证部分可以保留O，不强迫伪证。  
> **参考**：[PR#61修订](https://github.com/YuSun-WK/implicit-content-research/pull/61)、[R6-A4全稿24项根因](https://github.com/YuSun-WK/implicit-content-research/blob/survey/r6a-academic-review-20261109/03_survey/R6_review/R6A4_Deduplicated_Issue_Register.md)、[本轮独立Verdict](R6FixReview_Independent_Verdict_20261109.md)；“CLOSED”为学术问题目标满足，**并非**给PR/论文提交通过的同义词。

| 整改单元 | 对应所有历史编号 | 学术判定 | PR#61真实修订定位 | 判定理由（证据P/S/H/O保持原分层） | 若未关闭，必须怎样改 |
|---|---|---|---|---|---|
| **P0-01** | `A0-01`、`A1-01`、`A3-13` | **PARTIAL** | Ch1 §1.2 L25–46；Ch8 §8.1.1 L418–426；T7 | 已有四行相关综述及三条H规律，但至少两条主要在单子域内部，只给审计原则而少能区分先行综述的跨域条件对照。 | 加一张prior survey×分析单位×本稿独有证据产物矩阵；三规律至少两条交叉不同子域，明确条件→预测→正例→反例及不可迁移点。 |
| **P0-02** | `A0-02`、`A1-13`、`A2-16` | **PARTIAL** | Ch5 L248/274、Ch6 L314/316/326、Ch7 L386、Ch8 L430；R6_fix代码索引 | 六组作者公开源码可直接定位固定行，正式实验映射保持O；但索引存私有仓库，论文相对链接不可保证出版/外审访问；T5仍称MultiMM尚未固定。 | 将固定作者公共permalink入正文/公开附录；T5/T7同步口径；MMSafeAware/README/contrast精确S计数钉数据blob或删降。 |
| **P0-03** | `A0-03`、`A3-12` | **CLOSED** | Ch7 L374；Ch8 L414–425；T7；Bib@mei2026expohm | ExPO ICLR2026正式出版社、方法位置、SFT/GRPO/CDE与SMARTER/ThinkingGuard/Meerkat对照、RA-HMD及非S-S-U范围均已补。 | 学术范围无额外改动，R6-V继续BibTeX实际解析与正式出版字段校验；发现新反证才重开。 |
| **P1-01** | `A0-06`、`A0-07`、`A1-02` | **PARTIAL** | Ch1 L25–58；相关综述表四行 | 已明确91候选/48引用和叙述性审阅，未捏造PRISMA；相关综述的纳入/排除与证据层次仍不够让读者复查论文选择。 | 补按任务/证据深度的48条引文分组和排除边界；清晰交代R5-E更多相邻综述如何选，不能凭空补系统检索日志。 |
| **P1-02** | `A0-04`、`A0-05`、`A1-03`、`A1-05` | **CLOSED** | Ch2 L84–135；T2；F2静态语义 | T5作为T4条件子任务，严格S-S-U更窄；T6行为相邻层；纳入排除四组反例与SVG静态标题对应。 | 不需重新定义Task，R6-V仍须真实查看SVG版面。 |
| **P1-03** | `A1-06`、`A1-08`、`A1-12` | **PARTIAL** | Ch2 L106–122；T2，另T5/T6 | X_train_aux/X_test_aux/G/E框架已列，DRInQ/VAGUE给了例子；但关键论文的金标和推理预算仍未完整落到逐协议小表。 | 选3个跨不同子域的具体实验，分别填raw/test-aux/train-teacher、G构造和E分母，与最强baseline同预算对照。 |
| **P1-04** | `A1-07`、`A1-09`、`A1-10`、`A1-11` | **CLOSED** | Ch2 L66–72；Ch3 L140–158；Bib@searle1975indirect | Searle1975原典补齐；(RSA)²概率而非Acc及字面负收益、EmoBi消融预算和DRInQ困难抽样均写明。 | 保持已核的P级数值条件，不改作因果独立收益。 |
| **P1-05** | `A2-01`、`A2-02`、`A2-03`、`A2-04` | **PARTIAL** | Ch4 L192–222；T3 | Silent/FETCH!/FA-Net/SeTox已按instance/type/固定候选/有搜索风险区分；T3仍对FETCH! F0.5/P的真实分母只写需核查。 | 对FETCH!等具体指标给作者表中真实单位及分母，若未核则只列定性作者结论且明确表注不声称已核度量。 |
| **P1-06** | `A2-05`、`A2-09` | **CLOSED** | Ch5 L232–268；T4 | ToxiGen生成提示代理与AUTALIC人审、-1并入0、少量样本冲突、用途许可均有明确边界；原CSV仍O且不伪造。 | 不强求未获授权原CSV；正式审稿时保留2,400与2,402冲突脚注和许可限制。 |
| **P1-07** | `A2-06`、`A2-07`、`A2-08` | **CLOSED** | Ch5 L242–278；固定RV/CADET代码索引 | SMARTER标签条件DPO、RV-HATE相对等权+0.69pp、CADET目标验证访问路径均已区分作者P与公开实现S。 | 不能升级S为正式论文泄漏；所有S引用仍受P0-02公开可访问整改。 |
| **P1-08** | `A2-11`、`A3-11` | **PARTIAL** | Ch6 L314–318；Ch7 L386；T5 | 训练/测试辅助预算已经阐明并固定MultiMM/MGMCF/Meerkat源码；但T5的MultiMM版本措辞与正文矛盾。 | T5改“当前作者仓库公开检测入口已固定commit；正式论文run/情绪来源对应O”，MGMCF词义概念pkl来源仍O。 |
| **P1-09** | `A2-10`、`A2-13`、`A2-14` | **CLOSED** | Ch6 L292–331；T5 | M3UCD/DOSE人工模态贡献标签与去模态行为区别、MCIB结构消融不足以验证CIB独立贡献、V-FLUTE白图非单因素均写明。 | 方法归因仅限作者P级论文，同参数no-KL/no-conditional仍为研究缺口。 |
| **P1-10** | `A2-12` | **CLOSED** | Ch6 L308–310；T5 DOSE | DOSE已经改“新闻图像＋文章文本”；MCIB为文/音/视，不再互换。 | 保持ACL2026 Main（CCF-A）官方任务对象，R6-V检查最终排版的表格也同步。 |
| **P1-11** | `A0-09`、`A2-15` | **CLOSED** | Ch6 §6.6 L332–335；T5 MMSD3.0 | MMSD3.0作为CVPR2026 Main（CCF-A）多图反讽正式先例已明说只有出版摘要级，未伪造独立消融。 | 如投稿需要定量多图机制收益才追加定点核原文，否则维持这种限缩。 |
| **P1-12** | `A3-01`、`A3-02`、`A3-03`、`A3-10` | **PARTIAL** | Ch7 L354–364；T6；数据版本审计 | VLSU版本/标注人数和MMSafeAware/MOSS风险标签分母已给，但VLSU Fig5约34%未明确示例模型；MMSafeAware发布版数量没有可公开复核的固定数据来源。 | 给Fig5具体模型或限定“作者示例图”，并钉数据发布版本/脚本；不能将静态文件数量归为正式评测。 |
| **P1-13** | `A3-04`、`A3-06`、`A3-09`、`A3-15` | **CLOSED** | Ch7 L356、370–390、396–401；T6新增SIUO | 输入风险/P_in/回应R_beh/输出Q_out区分、SIUO Findings（会议CCF-B）补入、VLSU Harmless/Helpful双向、CrossGuard ASR指标不可互换均明确。 | R6-V仍检查T6排版；正文中不同ASR需保留Judge/分母标签。 |
| **P1-14** | `A3-05` | **CLOSED** | Ch7 L370–372；T6；数据版本表 | CrossGuard 1390红队、1616平衡Guard训练、12.5%≈202比例近似非官方ID、FigStep反方向准确。 | 不可把二者样本集合推定包含/相斥；作者代码训练样本ID仍O。 |
| **P1-15** | `A3-07`、`A3-08` | **CLOSED** | Ch7 L376–380；T6、T7 | ThinkingGuard 5600配对图片分别生成、离线SA-MCTS、Step-DPO额外Unsafe监督和消融边界已完整指出；ACM Track保持O。 | 仅保持已报告作者结果，严格单因素/真实训练budget无法独立核定则保留OPEN科研问题。 |
| **P1-16** | `A0-08`、`A3-14` | **PARTIAL** | Ch8 L406–426；T7 | T7已按攻击PPO、输入Guard、解释GRPO和回复GRPO重新分组，但FETCH/FA-Net及ImpCon/SMARTER仍合并不同Y的论文行；跨域具体P级数字不足。 | 拆分用于三规律的代表性混合行，给比较单位/实际优势与负例；与P0-01综合矩阵一并完成。 |
| **P1-17** | `A0-10`、`A3-16` | **CLOSED** | Ch9 L480–490 | 三条低成本Kill Test分别给X/Y/G/E、可用现成数据、停止规则和不可以证明的因果结论，避免直接宣称新任务。 | 未来若实际实验数据不可得可在后续研究调整，不影响本综述展望操作性。 |
| **P2-01** | `A0-11`、`A1-14`、`A3-17` | **CLOSED** | Ch2 L132；Ch8 L456 | 去掉“归入2.5”“图6候选暂不收入”的内部编辑口吻，相关段落成为规范综述文字。 | R6-V补一般文案校对即可。 |
| **P2-02** | `A1-04` | **CLOSED** | Ch1 L48–52 | “预期贡献”已改成已做分析产物及证据上限，语态正确。 | 最终是否达到所称贡献受P0-01复审，但时态问题已关闭。 |
| **P2-03** | `A2-18` | **CLOSED** | T4末尾表注 | 表4注明只展示按GT挑选的代表研究，避免遗漏第5章其他方法导致误解。 | 无需改变Ch5方法文献数以填表。 |
| **P2-04** | `A2-17` | **CLOSED** | Ch6 L316 | “T5表”明确改成“表5（多模态非字面意义表）”，不再误指任务T5。 | 无需额外科学修订。 |

## 复核前置要件与稿件级状态

**不能先合并后复查**。优先执行两项P0的精确增量，联动P1-01/P1-03/P1-05/P1-08/P1-12/P1-16，其余已CLOSED的科学内容不再被机械重写。所有实改须更新[24项源追踪Ledger](https://github.com/YuSun-WK/implicit-content-research/blob/survey/r6fix-full-draft-major-revision-20261109/03_survey/R6_fix/R6Fix_Source_and_Change_Ledger.md)的新commit/行，避免只在审稿表标CLOSED而稿件仍旧。

**外部数据/正式实验仍O**：VLSU公开CSV与正式论文版本差、AUTALIC受限CSV的真实类别统计、ThinkingGuard配对单因素严格度与出版社最终Track、MMSafeAware公开发布图像、Meerkat来源Parquet及训练run配置、MCIB条件loss真实batch shape。它们不会因24项审稿进度而转为作者违规或已复现的结论。

**目前不得升级全稿Verdict为SUBMISSION-READY。** R6-V负责实际渲染/出版引用工程；学术审稿复查两P0后再决定是否可作为提交候选。
