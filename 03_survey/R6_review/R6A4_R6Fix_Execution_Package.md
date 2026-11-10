# R6-A4 → R6-Fix｜可直接交给ChatGPT Work/Codex的中文综述定向修订执行包

> **文档版本R6A4-FIX-1.0；2026-11-09；状态READY-FOR-EXECUTION，NOT YET STARTED。**  
> **用途**：把R6-A0–A4的真实学术审稿意见交给执行者，**仅修订现有R5-C稿，不重写九章、不重做R0–R5、不大规模新增精读或数据集、不复现多GPU论文**。由Work/执行者从GitHub直接读取，所有成果走GitHub PR。  
> **注意**：本执行包本身不会修改原稿。任何学术争议必须标OPEN并回报，不能擅造论文数字、源码检查结果或书目Track。

## 0. 唯一权威输入（必须按顺序读取）

仓库：`YuSun-WK/implicit-content-research`。

1. **冻结原稿**：PR [#57](https://github.com/YuSun-WK/implicit-content-research/pull/57)，分支`survey/r5c-full-draft-figures-bib-20261109`，固定源HEAD `c04d6a23e864923acd64c192c8b05dc597c2bb90`；正文`03_survey/R5_full_draft/Survey_Full_Draft.md`，该目录的`tables/T1–T7`、`references.bib`、`Citation_Key_Mapping.md`、`Bibliography_Conflicts.md`和`R5C_Open_Issues.md`。
2. **审稿PR**：[PR #58](https://github.com/YuSun-WK/implicit-content-research/pull/58)，分支`survey/r6a-academic-review-20261109`，重点先读[R6A4_Final_Academic_Verdict.md](R6A4_Final_Academic_Verdict.md)、[R6A4_Deduplicated_Issue_Register.md](R6A4_Deduplicated_Issue_Register.md)，再按需要查A1/A2/A3原句、[R6A_Claim_Evidence_Corrections.md](R6A_Claim_Evidence_Corrections.md)与[R6A_Chapter_Issue_Log.md](R6A_Chapter_Issue_Log.md)。
3. **本项目已有证据**：main中`03_survey/R5_evidence/`，`03_survey/R4_writing/R4_07_Section_Claim_Evidence_Matrix.md`、`03_survey/R2_synthesis/`、`03_survey/R3_evolution/`与各已定稿阅读卡；重点`01_literature/cards/P027_ExPO-HM.md`、`P034_CrossGuard.md`、`P038_VLSU.md`、`P039_ThinkingGuard.md`、`P040_MeerkatVL.md`和B3a/B4a卡。
4. **外部正式出处优先**：ExPO-HM ICLR 2026（CCF-A）[官方论文记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)，DOSE ACL 2026 Main（CCF-A）[出版页](https://aclanthology.org/2026.acl-long.319/)，CrossGuard ACL 2026 Main（CCF-A）[出版页](https://aclanthology.org/2026.acl-long.1178/)，VLSU ICLR 2026（CCF-A）[正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)。无法访问原文所需关键参数时标O，不用泛化知识填空。

## 1. 分支和PR严格规则

- **不直接改main/原PR#57分支，不合并PR #57或#58**。为修订创建新的分支，建议从**固定的R5-C commit** `c04d6a23...`起新分支 `survey/r6fix-full-draft-major-revision-20261109`。
- 因PR #57尚为Draft，优先以其分支为**stacked PR的base**展示仅R6-Fix增量；若执行时PR #57已被人工合并/改变，请先读取最新PR及base，再选择可清楚审阅的主线，不能盲目覆盖。
- 本修订分支可以编辑`03_survey/R5_full_draft/Survey_Full_Draft.md`、`tables/T1–T7`、`references.bib`、`Citation_Key_Mapping.md`、相关冲突账本，以及新增`03_survey/R6_fix/`审计产物。**不要覆盖`03_survey/R6_review/`既有审稿历史**、`01_literature/cards/`原定稿或R2/R3旧记录。
- 与R6-V分工：本任务负责**科学结论、表内学术字段、来源证据及正文引用**；R6-V负责图形真实渲染、黑白可读性、表格排版、书目/链接工程检查。若需要改变SVG的学术节点/箭头，先提科学内容变更建议，不在未审阅下用视觉PR悄改。
- 不用自动“关闭问题”的措辞。每项必须给`新稿commit/行号、修订前后、原论文/代码permalink、P/S/H/O证据、状态`；审稿复审决定CLOSED。

## 2. 执行排序（以真实依赖而非章号机械推进）

### F0｜版本及事实冻结（不写新结论）
- [ ] 记录R5-C commit、46条Bib key、九章标题、原图F1–F5、表T1–T7文件hash/数量；与审稿PR版本建立patch基线。
- [ ] 生成`03_survey/R6_fix/R6Fix_Source_and_Change_Ledger.md`，列旧稿/新稿、各review issue ID、owner、证据等级、是否需要外部核实。
- [ ] 设“旧审稿ID→24唯一问题”追踪表，不把继承P0重复当新P0。

### F1｜强制事实纠错与明确指标分母（可先做）
- [ ] **P1-10**：表5 DOSE 原始模态“文/音/视”**改为“图像＋新闻文章文本”**，MCIB仍为文/音/视，核所有相关正文。
- [ ] **P1-14**：CrossGuard 1390 ImpForge红队样本、1616 Guard训练样本、约12.5%≈202联合类**三个不同统计单位**；不宣称原始ID精确子集。
- [ ] **P1-13/P1-12**：CrossGuard Fig4 SIUO 60.33→5.39 vs FigStep 0.12→0.21，ASR攻击者/Guard/回应类型、裁判与分母；VLSU 8187正式/8159公开、S-S-U37/35、联合错误子集的约34%、Borderline二分类映射、image not_sure的处理条件。表6插SIUO（NAACL2025 Findings，会议CCF-B，非Main）。
- [ ] **P1-04/P1-07**：RSA(²)字面代价、DRInQ挑战集选择、EmoBi去情绪/去核验结果、SMARTER的gold标签条件偏好、RV-HATE PPO较等权83.78→84.47、CADET目标域前提，按原论文实际metric复核。**不能跨表或模型抄数**。
- [ ] **P2-01/P2-02/P2-04**：删“归入2.5/图6候选”等内部备忘，修“预期贡献”时态和“T5表”歧义；修表4“仅代表GT”范围。

### F2｜P0-03 正式论文覆盖与方法定位
- [ ] 核P027 ExPO-HM的**官方ICLR 2026（CCF-A）**Bib字段并加唯一citation key；正文§7.3或§8.1/8.3至少一个明确对照段，表7增加独立解释后检测行。
- [ ] 对照SMARTER（gold标签与解释偏好）、ExPO（policy manual SFT+课程GRPO+CDE）、ThinkingGuard（SA-MCTS离线搜索+Step-DPO风险归因）、Meerkat（Normative Actor Self-Verify+GRPO安全有用回复）及CrossGuard（red-team PPO样本生成 vs Guard LoRA/SFT分类）。
- [ ] 比较项必须列`Y预测对象、训练可用额外risk/trigger/label知识、更新哪个模型、损失/奖励、原论文正向结果与反面/归因不足`。ExPO解释judge/CDE不等于解释faithfulness；**不能放到严格S-S-U的GT研究行**。
- [ ] 检查新增Bib与全部正文引用key一致，正式出版Track写准，不借用未核ACM MM final条目。

### F3｜P0-01 让综述提供真正跨领域机制综合
- [ ] 扩第一章相关综述对照，显式说明本文相对既有语用/修辞/多模态安全综述**新增分析单位**，不是“没有人写过”。
- [ ] 按表7重写Ch8核心**三条条件规律**：①编码新义开放度与词典/类别/检索先验；②解释或规范知识如何经CE/对比/DPO/GRPO影响不同Y，且解释忠实性与标签正确不同；③联合危害漏判与正常误拒在各自协议的真实正反实证。
- [ ] 每条规律至少**两篇不同子领域论文**，附`paper+venue(CCF)+Y/GT/extra_info+真实正收益+限制/反例`。务必保留数据集/任务异质性，**不要跨论文数值直接作因果横向SOTA排名**。
- [ ] 将§1.3贡献和§9.2简化研究议程指向确实完成的比较产物，取消“只是提出更多研究”式重复。

### F4｜P0-02 固定代码与发布数据的外部证据
- [ ] 新建`03_survey/R6_fix/R6Fix_Public_Code_Evidence_Index.md`，每行提供claimID/作者论文/官方代码repo/immutable git commit/file精确行/函数&输入示例或shape/审计方式/观察日期/正式实验版本是否已证。
- [ ] 扫描全部正文`本项目静态`、`源码`、`公开实现`、`test_data`、`gold emotion`、`MSE`、`广播`、`oracle`、`数据缺失`：所有严重代码结论若无法用固定版本复核则**保守改写/删去具体指控**。
- [ ] 排查P029 RV-HATE、P033 CADET、P003 MultiMM、MGMCF、R3B MCIB、P027 ExPO和P040 Meerkat源码版本；如版权/访问阻碍，不把缺证说成事实。
- [ ] 不能声称运行复现、完整数据验证或正式实验作弊。若只做当前main静态阅读，写清“所查代码版本”。

### F5｜其他P1学术修订（按24项主根因逐项验收）
- [ ] **P1-01/02/03**：引言选文91→46的叙述性纳排、T4/T5/T6层级/工作定义、Task(X,Y,G,E)的raw/train/test-aux、GT源/人工一致与评测judge。
- [ ] **P1-05**：Silent/FETCH!/FA-Net/SeTox的词典类型、目标域访问、Precision/DPR/DR/Acc分母，不能概称完全未知新词。
- [ ] **P1-06**：ToxiGen生成提示代理的对抗难度 vs人审核标签矛盾；AUTALIC原-1折叠、trained undergrad/投票、2400与2402算术冲突、合法用途限制，**未读CSV保持O**。
- [ ] **P1-08/09**：MultiMM测试gold情绪/MGMCF目标源字段/Meerkat自评规范知识；M3UCD与DOSE模态人工归属不等于模型去模态依赖；MCIB缺独立KL/conditional损失消融；V-FLUTE白图残余F1与来源偏差，分清事实与待控制。
- [ ] **P1-11**：MMSD3.0（CVPR2026 Main，CCF-A）定点核原文后补有限信息，否则缩为已出版的多图先例；不得自行编造消融。
- [ ] **P1-15**：ThinkingGuard配对图分别生成/步骤偏好额外Unsafe监督的受控边界；未证ACM正式Track，保留O。
- [ ] **P1-17**：第9章只留可执行三路Kill Test（现有公开GT和低成本冻结诊断），不要宣称本文已经用新实验验证研究规律。

## 3. 输出产物（必须可复核）

提交PR前至少应有：

1. 修改后的完整 `Survey_Full_Draft.md`（九章仍完整）；相关T1–T7科学字段、`references.bib`及引文映射同步。
2. `03_survey/R6_fix/R6Fix_Source_and_Change_Ledger.md`：**24个去重单元逐行**`原ID / 原句锚点 / 新文件新行 / 前后差异 / 来源/P-S-H-O / 状态`。
3. `03_survey/R6_fix/R6Fix_Public_Code_Evidence_Index.md`：固定源码索引或清楚列降级的claim。
4. `03_survey/R6_fix/R6Fix_Citation_and_Data_Version_Audit.md`：ExPO正式Bib、引用key核查、各数据版本数字的分母和judge来源、仍OPEN事项。
5. `03_survey/R6_fix/R6Fix_Revision_Summary_and_Reviewer_Checklist.md`：本次改稿的三项P0逐条关门证据，P1/P2状态，非本人能核/未运行部分，待审稿人复核动作。
6. **新Draft/Open PR**，标题`R6-Fix｜广义隐晦信息综述：P0修复与分层证据修订`，base优先指向R5-C PR #57的分支，列明依赖关系；不要自动合并或关闭原PR。

## 4. 质量闸门与禁止行为

- **P0-01**：必须有至少三条来自真实论文正反实验及先验条件的跨领域综合规律，并在引言公平定位；只多写一章或扩到91篇不算通过。
- **P0-02**：无任何无法固定源码版本的严重S级结论；未实测不能写“代码复现证实正式论文存在泄漏”。
- **P0-03**：ExPO正式citation key、至少一处机制对比、T7正确定位及非S-S-U边界都具备。
- **Facts P1**：DOSE表5模态正确；CrossGuard 1390/1616/≈202及ASR三对象；VLSU Fig5约34%条件分母、PDF/CSV版本；AUTALIC总数冲突不伪造最终CSV结论。
- **No silent evidence upgrade**：每篇正式会议/期刊标CCF等级，并区分会议Main/Findings/预印本/作者接收声明；论文级P、源码S、跨域综述H、缺口O不互换。
- **No manufactured work**：不造不存在的下载链接、作者实验表格数字、GPU复现、逐例人标、人类评委一致、全部图像可用率或官方Track。
- **Version gates**：原R5-C、审稿PR#58、修订分支、R6-V分支关系公开；旧审稿历史不改写为“CLOSED”。
- **Wait for human review before merge**：最终是否关闭P0由Chat审稿核对新稿决定；是否通过R6-V实际图表/Bib验收单独决定，互不代替。

## 5. 给Work的最短调用指令（以本文件为权威任务书）

**打开GitHub仓库 `YuSun-WK/implicit-content-research`，先读PR #57固定源稿和PR #58中的`R6A4_Final_Academic_Verdict.md`、`R6A4_Deduplicated_Issue_Register.md`及此执行包；按F0→F5在新独立R6-Fix分支修订现有九章全文、相关学术表和Bib，留下24项逐条更改证据与可公开复核的S级源码索引，提交Draft PR供我审阅，不直接合并、不开大规模精读或训练，不做未经证实的学术推断。**

**完成条件不是“PR已创建”，而是实际九章改稿和四类审计文件均已提交；不能完成的项目逐条列OPEN及原因，不要伪装DONE。**
