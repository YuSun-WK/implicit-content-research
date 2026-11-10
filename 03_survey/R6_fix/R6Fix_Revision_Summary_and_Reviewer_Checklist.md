# R6-Fix｜实改摘要与独立Reviewer验收清单（交Chat复审）

> **版本：2026-11-09；状态 IMPLEMENTED / REVIEW PENDING；不是R6终稿已通过。**  
> 原始R5-C PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)固定commit `c04d6a23e864923acd64c192c8b05dc597c2bb90`；R6-A最终审稿[PR #58](https://github.com/YuSun-WK/implicit-content-research/pull/58)（三P0/17P1/4P2）；本R6-Fix在**独立新分支**修改原稿副本，旧PR不修改不合并。  
> 证据类型F正式出版、P原作者实验、S当前固定公开代码、H本稿综述推论、O尚未证实。全部24个去重问题的具体旧/新行及改动见[R6Fix_Source_and_Change_Ledger.md](R6Fix_Source_and_Change_Ledger.md)，本次六组固定源码见[R6Fix_Public_Code_Evidence_Index.md](R6Fix_Public_Code_Evidence_Index.md)。

## 1. 可直接阅读的新稿成果

- **九章正文未推倒重写**：`03_survey/R5_full_draft/Survey_Full_Draft.md`。新增或实质修改引言贡献、T4/T5/T6边界、语用和修辞实证反例、编码语言开放度、隐晦有害标签与训练预算、多模态辅助信息、联合风险数据版本、安全回应权衡、第8章三条条件规律及第9章三条可证伪研究议程。对未核的实现结论已改为**带固定证据的S级静态观察**或明确待核线索，不指责作者正式实验已违规。
- **六张科学表**：`tables/T2–T7`均已改；T1原科学内容未动。T5确认DOSE（ACL 2026 Main，**CCF-A**）是新闻**图像＋文章文本**，而文本＋音频＋视频属于MCIB（AAAI 2026 Technical，**CCF-A**）。T6新增SIUO（NAACL2025 **Findings**，举办会议CCF-B但非Main）。T7含ExPO-HM（ICLR 2026 Main，**CCF-A**）并按任务Y拆PPO/Guard/DPO/GRPO。
- **参考文献**：Bib由46→**48**，新增正式ExPO-HM与Searle1975理论原典；手写编号书目与Bib键均为48。最新文本集合检查：**主体九章的48个唯一citekey全部存在于Bib，48项Bib均在正文章节实际被引，无重复、无缺失**；此项是机械键检查，正式出版字段/目标刊编译仍需R6-V。
- **三份审计资产**：24项逐项改动台账、六组固定commit源码索引、数据版本与引用一致性审计；这些文件是可复审证据，并非原创训练实验。

## 2. 三个P0：实际修订内容与必须经Chat复审确认的关闭门槛

| P0 | 已实施修改（有形产物） | Reviewer应做的独立核查 | 当前状态 |
|---|---|---|---|
| **P0-01：有辨识度的跨领域学术结论** | 第1章公平比较Ma语用、Farabi反讽、Hee多模态仇恨既有综述，声明新增分析单位为`Y/G/E与训练-测试先验的正反对照`；第8章新增**三条完整有作者正向数值/反例及条件**的规律：编码词义先验预算、解释监督目标漂移、联合风险与正常误拒；表7真正按任务Y/教师信息/收益/边界拆分；第9章三条可证伪议程 | 逐条回读涉及论文表图，判断是否确实增加可传达的比较认识，而不仅是并列案例；审查引言贡献是否兑现、是否超出已有综述；有任何跨论文未同条件数值排名即退回 | **REVISED / REVIEW OPEN** |
| **P0-02：S级实现主张外部可追溯** | 从GitHub HEAD固定RV-HATE、CADET、MultiMM、MGMCF、MCIB、Meerkat-VL的完整commit并直接读源码，形成六组`file#L`公开证据索引；正文已加入索引相对链接，未完成EmoBi/SemanticQA/ExPO细节均降为OPEN；所有关于正式论文运行的结论以O限制 | 在固定SHA文件逐行复核脚本入口、shape、split和其他变量；检查**正文每一句涉及源码**是否具有固定证据或明示仅历史线索；查明代码版本与正式论文运行映射仍无凭据，绝不得写“已证明作者作弊/实验错误” | **REVISED / REVIEW OPEN** |
| **P0-03：ExPO-HM遗漏** | `mei2026expohm`加入Bib/引文映射/手写书目及第7/8章，表7与SMARTER、ThinkingGuard、Meerkat-VL比较解释后分类/风险归因/回应GRPO等不同Y与额外知识；明确ExPO非严格S-S-U数据 | 复核ICLR2026（CCF-A）正式元数据、Policy Manual→课程GRPO+CDE、naive GRPO 74.5/完整81.1/RA-HMD 80.2的**论文实验协议**；确认没有把CDE低解释成忠实推理 | **REVISED / REVIEW OPEN** |

**P0未由执行者自行标记CLOSED**；闭环只能是后续Reviewer按新稿与上述固定证据复审，且R6-V图表/Bib通过后才能考虑投稿准备状态。

## 3. P1/P2实施状态与注意事项

- P1-01到P1-17都有实际正文或科学表格修改、限缩或保留O，见24行台账；其中**P1-01只有真实的叙述性检索协议**，因为历史上并未执行统一检索式/PRISMA，不虚构检索流程。**P1-11的MMSD3.0采取官方摘要级限缩**，未重新声称已核全文独立机制消融。**P1-06的AUTALIC原受限CSV仍未独立读取**，不能修正2400与242+2160不符的原始数据。**P1-12的MMSafeAware发布文件版本和图片可达**没有实物跑通，需继续作为O而不是改写作者论文GT。
- 四个P2均已编辑或标注：§1.3不再称“预期贡献”，第2章与第8章移除内部编辑备忘，表4注明“代表GT并非第5章方法全量”，§6.4避免“T5表”误指T5任务。正式PDF里的中文标点、表宽和字号由R6-V负责。
- 继续保留**ThinkingGuard ACM MM 2026已接收**为作者表述；ACM MM会议属CCF-A，但正式出版社条目/具体Track O，Bib仍为arXiv，不得擅自标为已核Main。SIUO是NAACL2025 Findings，而非Main。
- 公共代码的六组固定S级观察**不自动等于正式论文训练配置**；本次没有运行任何原论文完整模型或执行多卡训练，也没有对所有真实/合成图片逐张人审。

## 4. 下一次独立审稿须实际勾验的Gate

- [ ] **G1 结构与贡献**：九章完整；第1章“相对已发表相关综述的新分析单位”与第8章三条H级规律具有学术增量，并且每条至少含一组论文的正向结果和一条负例/边界。
- [ ] **G2 科学与数值**：重点核CrossGuard 1390/1616/≈202、Fig4 SIUO 60.33→5.39 vs FigStep 0.12→0.21、VLSU 8187/8159与S-S-U37/35及34% conditional、AUTALIC -1折叠和2400/2402、DOSE输入修正和标注主导比例、ExPO真实优化目标及各类F1定义。
- [ ] **G3 方法公平性**：T7没有将攻击生成PPO、输入Guard分类、Step-DPO风险归因、CDE解释后检测、GRPO回应对齐并排成SOTA；gold情绪/源目标/搜索/教师规范风险说明按训练/测试预算区分。
- [ ] **G4 可复核性**：每条高风险静态源码观察均有immutable source commit/path/line或已明确降级；不得将公开路径代码错误与正式作者实验结果无证挂钩。
- [ ] **G5 引文/格式（由R6-V承担）**：48条Bib使用真实解析器检查并逐条核关键作者、出版年份、Track、page/DOI；Markdown手写参考列表与Bib一致；F1–F5用渲染器真实查看中文字体、黑白、单双栏缩放；T1–T7按版面检查溢出/交叉引用。
- [ ] **G6 证据开放性**：有差异的发布版数据仍标O，没有编造CSV、图片可达、实验复现、Judge人工一致性、正式Track或未证因果结论。
- [ ] **G7 PR依赖与提交**：R6-Fix分支从PR#57原commit派生，Draft PR base设PR#57原分支以显示仅修订delta；PR#57/#58仍Draft/Open，不在本次自动合并；所有审稿历史不被覆盖。

## 5. 清晰的停止条件和后续关系

R6-Fix实施任务的完成标准是**实际新稿、表/引用、证据索引与Draft PR都在GitHub中**；本文件提供的是**“请开始独立复审”的交付信号**，并非学术质量已经PASS。若正式稿有科学内容修正与R6-V图形/Bib工程修正发生冲突，应在审核者确认后再整合，不能让视觉执行偷偷改变GT或因果结论。

**建议Reviewer的返审格式**：`unique_issue_id | revision_commit_and_lines | source_fidelity(P/S/H/O) | decision(CLOSED/PARTIAL/OPEN) | required_next_change`。在R6-A4所有P0确认CLOSED及R6-V真正通过之前，状态始终是**NOT SUBMISSION-READY**。
