# R6-Final-Integration｜最终验收报告（2026-11-10）

## 1. 版本裁决与整合范围

- **唯一科学主版本**：PR #63，固定HEAD `80bad7e668a5510f7897b8ee117d7851ebaa8114`；PR #64已关闭，只参考其中Mao正式书目元数据，不迁入其C1–C3或另立并行主稿。
- **整合基线**：main `49214314d544f865e046aae0a0fe165f08e542f5`。独立分支 `survey/r6-final-integration-20261110` 从该SHA创建；不自动合并。
- **唯一完整正文**：[`../R5_full_draft/Survey_Full_Draft.md`](../R5_full_draft/Survey_Full_Draft.md)。承接PR #61→#63科学稿的九章、附录A/B和T1–T7；未重新写作九章。正文与PR #63逐行比对，仅改标题状态、Mao相邻综述、两处来源定位、附录B及第50条书目；C1–C3的数字与条件性结论未改。
- **PR #60保护**：F1–F5均沿用main原始Git blob；五个哈希依次为 `e13da166`、`98b8a906`、`2540e055`、`7053da69`、`7b74ff92`。T1–T6与PR #63 blob一致；没有修改已合并的R6-V审稿/格式结论或既有审稿档案。
- **证据附件**：PR #61的`R6_fix`四份文件与PR #63的`R6_fix_r1`四份文件随主稿迁入；仅在两份R1台账中补充正式G4/ACL定位与最终整合勘误说明，保留其原轮次结果及独立审稿状态。

## 2. 两处确定性引文修复

1. **VAGUE**：ICCV 2025[正式补充材料附录G Table G4](https://openaccess.thecvf.com/content/ICCV2025/supplemental/Nam_VAGUE_Visual_Contexts_ICCV_2025_supplemental.pdf)的Qwen2.5-VL-Instruct 72B VLM/CoT数据仍为72.8→69.9%。正文§8.1.1、表7及书目冲突台账以正式G4为主锚。作者[arXiv v3 HTML](https://arxiv.org/html/2411.14137v3)把同一组数据标为G6，故保留版本号差异说明；未改实数或解释为新的实验。
2. **(RSA)²**：C1与C3的Table 2／3、Figure 4证据入口及表7已改为[ACL 2025正式论文](https://aclanthology.org/2025.acl-long.1019.pdf)。不再将异常的arXiv HTML v1当作独立核对入口。正确候选意义的平均概率仍分别按论文条件呈现，未称Accuracy。

## 3. Mao等相邻综述的纳入决定

**纳入**Mao等 *A survey on pragmatic processing techniques*，*Information Fusion* 114 (2025), 102712，DOI `10.1016/j.inffus.2024.102712`，键 `mao2025pragmatic`。第1章以其承认已有语用任务与方法综合，附录B列相邻综述用途；不引入#64的科学综合、不将其作为新的作者实验。保留Ye预印本的摘要级定位，因此49→50条。CCF级别按本次目录检索标“未收录”，不猜等级。

## 4. 实际执行的工程验收

| 验收对象 | 实际方法 | 结果 |
|---|---|---|
| BibTeX | [`verify_final.py`](verify_final.py)逐字符解析条目、嵌套大括号／引号、字段、重复键与必需元数据 | **PASS**：50条，50个唯一键；非仅正则数 `@entry` |
| 文内／表内引用 | 正文九章、附录B、手写书目、七表与Bib集合核对 | **PASS**：正文50、附录B50、手写参考50；T1–T7均无游离键 |
| 结构与链接 | 九章章号、七表列宽与行、相对文件链接、五图SVG XML及主线哈希 | **PASS**：9章、7表、5图；无断开的相对链接 |
| 实际排版 | [`render_preview.js`](render_preview.js)用Markdown渲染生成[HTML](R6_Final_Preview.html)和[45页A4 PDF](R6_Final_Preview.pdf)；将T1–T7附入预览 | **PASS**：五SVG全部加载；12个实际表格（正文5表＋附表7）；屏幕/打印横向溢出0；PDF无空白页，逐页A4、关键证据文本可提取 |
| 科学主张保护 | 与PR #63原文按行比对及表/图Git对象核对 | **PASS**：只作上述定点修复与Mao补充；P/S/H/O层级、C1–C3的跨协议限制及原独立审核8项CONDITIONAL CLOSED判定保持 |

机器记录见[`validation.json`](validation.json)与[`render_validation.json`](render_validation.json)。PDF是审阅排版预览，投稿版仍须按目标期刊模板完成最终样式。

## 5. 结论与人工确认

**结论：达到“SUBMISSION-READY CANDIDATE（投稿准备候选稿）”的整合与工程验收门槛；尚未达到可不经人工终校直接投稿的无条件终稿标准。** PR #63独立审核的八项学术判定是当前科学范围内CONDITIONAL CLOSED；此报告不重判先前16项，也不宣称独立复现作者模型实验。公开代码固定版本的S级静态观察没有升级为作者正式实验P级事实。

投稿前仍需人工确认：

1. 目标期刊或会议的具体模板、图表字号、参考文献体例和中英文标点；本预览为A4审阅版，表7密度高，最终模板应再人工通读缩版。
2. [书目冲突台账](../R5_full_draft/Bibliography_Conflicts.md)中的AUTALIC正式PDF/网页作者差异、ThinkingGuard最终出版条目与Track、Searle原典版次，以及非ACL条目逐字段出版校样；本次完成真实语法解析与键核对，不等于50条逐字段出版社认证。
3. VLSU正式论文与公开CSV的8187/8159、37/35差异，及图像可达性；目前文中保留P/S/O边界。MultiMM、MGMCF、MCIB、Meerkat-VL等公开源码与正式训练run的对应关系仍须作者或正式运行记录确认。
4. Ye预印本是否已有正式发表版本；若变更，应核实新元数据并同步正文、Bib及映射。

本报告只复核最终整合变更集，不修改原审稿结论；最终PR保持未合并。
