# R8｜正式PDF整合交付与校验报告（2026-11-10）

## 交付物
- 新版正式审阅稿：`03_survey/R8_submission/Survey_R8_Review.pdf`
- 图表抽查页：`03_survey/R8_submission/Figure_Table_Check_Pages.pdf`
- 构建记录：`03_survey/R8_submission/Build_QA.md`
- 引文编号：`03_survey/R8_submission/R8_Reference_Numbering_QA.md`
- 唯一 Draft PR：[PR #70](https://github.com/YuSun-WK/implicit-content-research/pull/70)，**未合并**。

## 修订覆盖
1. 以作者编辑过的最终摘要为基准，优化术语、关键词及与拒答评测实际指标对应的表述。
2. 引言：§1.1图1下移，§1.2先引入范围后列既有综述，删除1.4冗长内部审计节，在1.3末保留一段必要的综述类型说明；删除冗余章节顺序提示。
3. §2.1：依据Grice、Searle、Frank/Goodman既有引用重写理论基础首段，改善例子衔接；subtle改为“不易察觉”，表1和第2章小结同步。
4. 五张SVG图全部重绘，按已确认紧凑样式压缩卡片留白，并更新图1–5图注。
5. 另一窗口七张表T1–T7完整候选均已应用；T6拆为输入识别与回应/攻击两面板，T7按方法族合并，正文引导句消除重复表题。
6. PDF构建源为各表独立设置列宽、字号和分页，T5整表另起页、T6两面板分隔、T7横向。
7. 原`R7_submission/Survey_Final_Review.pdf`固定阅读底稿保持原状。

## 自动校验和人工视觉抽查
- GitHub Actions `R8 revised survey PDF`：最终运行 [42821906228](https://github.com/YuSun-WK/implicit-content-research/actions/runs/42821906228)，成功。
- PDF共**43页**（A4纵向+1页横向表7）；含九章、附录A/B、图1–5、表1–7、50条书目，按[1]–[50]各一次且顺序连续。
- 检查关键修改词与旧句删除：通过。首次输出存在表7表注单独占页、末页仅剩一条书目的问题，后经版面修改均已解决。
- 本轮下载最终构建产物并使用PyMuPDF抽取全文及渲染首页、图表所在页和参考文献首尾页进行视觉检查，未发现明显裁切、乱码、孤立表注或孤立末条参考文献。
- **视觉验收限度**：仅对重点页抽查和构建器自动规则核对，尚未进行目标期刊模板的最终校样与实体打印。

## 未关闭学术证据问题
- AUTALIC作者字段与数据计数冲突；VLSU正式PDF/公开CSV版本差异；ThinkingGuard正式ACM条目及Track待核；MCIB和若干多模态方法的代码静态观察不能替代正式实验配置。这些仍在`R7_Open_Issues.md`与`Bibliography_Conflicts.md`中保留。
- 综述方法属于批判性叙述性综合，不声称系统检索PRISMA覆盖率，也不声称本轮新增训练复现。
- 编辑者对论文内容的逐段阅读仍可继续；这次是**用户明确要求的阶段性正式PDF交付**，不是“R8全文审完”最终收口。
