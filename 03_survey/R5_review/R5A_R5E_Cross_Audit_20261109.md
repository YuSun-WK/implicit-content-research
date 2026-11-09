# R5-A × R5-E｜跨分支质量审核与R5-B移交（2026-11-09）

**总体裁决**：R5-A正文初稿 **PASS FOR DRAFT / NOT JOURNAL-READY**；R5-E证据审计 **PASS AFTER METADATA CORRECTION**。本轮仅审核、纠正R5-E IJCAI等级并记录门槛；**未合并PR #54/#55，也未更改R5-A正文**。

## GitHub真实状态
- [PR #54](https://github.com/YuSun-WK/implicit-content-research/pull/54)：`survey/r5a-ch03-ch05-draft-20261109`，4份新增文件，`03_survey/R5_draft/`；3章共17小节。
- [PR #55](https://github.com/YuSun-WK/implicit-content-research/pull/55)：`survey/r5-evidence-audit-20261109`，3份新增文件，`03_survey/R5_evidence/`。
- 两分支只在各自新目录中新增内容，未修改R0–R4；本次未合并。
- R5-A静态范围核计：Ch3 3.1–3.5，约7041字符；Ch4 4.1–4.6，约6000字符；Ch5 5.1–5.6，约7532字符（含章节内部引用，非最终印刷字数）。

## 审核意见

| 检查项 | 结果 | 要求 |
|---|---|---|
| R4九章/46节对齐 | PASS | 第3–5章的17节均有正文，未重复覆盖第1/2章 |
| 方法/GT/评价边界 | PASS for draft | T1/T2/T3/T4区分；模型受控实验与推断区分；不跨任务将F1/Acc当同一指标 |
| 关键论断 | PASS with caveat | P035 EmoBi情绪辅助不称独立因果；DRInQ只是多选共识；FETCH!词典留出非真实时间外；Flood仅源域隐喻GT；AUTALIC不声称删语境增益 |
| 实现与论文版本 | PASS with caveat | P029/P033公开代码问题不等于正式表分数被证伪；P020 arXiv v1 vs ACL PDF式号待逐页核 |
| 相关综述对照 | R5-E已形成、Ch1尚未整合 | R5-C全文整合时补第1章§1.2，并保留组织性贡献而非首创性宣称 |
| 期刊级正式BibTeX | 尚未完成 | 当前用项目ID+出版链接过渡，R5-C制作统一.bib并核文献原稿版本 |
| 图表 | 尚未制作 | R5-B/C按R4 F1/F2/F3/F5优先级制作；T2/T3/T5/T6主表 |

## 实际发现并修复的错误：IJCAI分级
PR #55原在三份审计报告将 **IJCAI 2024 Survey Track** 写成会议 **CCF-A**。按照项目采用的**2026年CCF第七版目录**，IJCAI已从A降为**CCF-B**；Survey Track也须单独标记，与普通Main/Technical Research paper区分。

**已直接改正PR #55的三个文件**：
- `Related_Surveys_Comparison.md`
- `High_Priority_Evidence_Audit.md`
- `R5_Citation_and_Claim_Gates.md`

依据：CCF 2026年3月31日[第七版正式公布](https://www.ccf.org.cn/Academic_Evaluation/By_category/)和第七版[检索性转录](https://github.com/haozhou-wong/ccf-recommended-list-2026-markdown/blob/main/ccf-2026-quick.md)（人工智能B类包含IJCAI）。

## 仍需保留的未关闭问题（不阻止初稿合并）
1. AUTALIC作者网页/BibTeX与PDF作者人数及排序存在差异，数据2400 vs类别合计2402，使用许可受限；写Rizvi et al.并不编造完整作者列表。
2. MCIB AAAI 2026 CCF-A整体模型结果能报，条件IB独立效应缺等预算消融、公开MSE广播和文本残差旁路不可直接断定影响正式论文训练。
3. VLSU论文与公开CSV的样本数量和S-S-U数量有版本差，17模型PDF vs11模型摘要有版本差；联合风险分类不等于回应行为。
4. ThinkingGuard ACM MM 2026（会议级A）出版社正式元数据/Track待核；不可算作已完全核验正式Main。
5. R5-A P020方法公式依旧存在arXiv v1/ACL正式版本编号对齐问题；R5-B/C引用数字或公式需核PDF原页。
6. 现有R5-A章稿较紧凑，正式投稿前需再扩展逐节的直接竞争工作比较、方法机制图表、标准BibTeX，而非只是增添抽象评价。

## 下一步（执行顺序）
1. **合并PR #55**（审计边界先进入main），再**合并PR #54**（正文）；审核者本轮没有执行merge。两PR分别修改独立新目录，原则上冲突可能性低。
2. 启动**R5-B**：Work基于最新main与R5-E门槛撰写Ch6–Ch8，按`03_survey/R5_draft/`独立分支提交PR；将MCIB/VLSU/ThinkingGuard列为写作高风险。
3. 并行或随后开展**R5-C预处理**：以Work整理官方BibTeX/相关综述表、绘F1/F2/F3/F5矢量草图，但不在尚未完成正文时宣称全稿完毕。图形实际渲染需要检查字体和版权。
4. 等Ch6–8审核通过再写Ch9结语，全文统一审核Ch1–9及图表、任务定义与引文；R6由Chat主导。

**结论**：可以进入R5-B，不必重新写R5-A，也不必等每一项源论文开放数据/复现争议关闭。
