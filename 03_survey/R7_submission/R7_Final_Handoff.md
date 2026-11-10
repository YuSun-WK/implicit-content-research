# R7 交接

## 本次交付

基于最新 main `ecd1973774a50f74b994f2e6435343fad0024882` 创建独立 R7 分支。正式通用 A4 PDF 43 页，保留九章、第 8 章 C1–C3、五张矢量图、七张表、附录 A/B 和 50 条参考文献；T7 独立横向两页。原 R5 科学源未更改。排版工程、CSL 和依赖锁文件随稿提交。未合并 PR。

正式构建命令：在 `03_survey/R7_submission/source/` 运行 `npm ci && npx playwright install --with-deps chromium && REQUIRE_PANDOC=1 npm run build`；需预装 Pandoc 和 Noto CJK 字体。CI 已用 Pandoc citeproc 编排 50 条文献。构建路径跨平台相对定位，不使用本机 Edge 路径。

## 验收结论

本地 41 页预览已逐页渲染并看过总览，重点图表页作原分辨率复核；修复两处公式转义显示。正式 43 页 CI PDF 尚需独立逐页视觉和实体打印核验。书目冲突仍有 AUTALIC、ThinkingGuard、VLSU 等未关闭项，详见专门台账。当前达到 **Level 1：Readable Review Draft**；完成正式 PDF 的逐页视觉检查、剩余书目字段与图表打印复核后再判 Level 2。目标刊未指定，不判 Level 3。

导师审阅建议先读 `Survey_Final_Review.pdf`；图表可对照 `Figure_Table_Check_Pages.pdf`、`R7_Figure_Table_QA.md`，书目请见 `R7_Bibliography_Final_Audit.md` 与 `R7_Open_Issues.md`。图表检查册来自本地预览，页号与正式 PDF 不完全相同。
