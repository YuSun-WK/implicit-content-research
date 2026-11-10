# R7 正式综述交付

本目录将 `../R5_full_draft/Survey_Full_Draft.md` 及其图、表、`references.bib` 排成通用中文 A4 学术审阅稿。R5/R6 科学正文仍是唯一内容来源；R7 没有另建一份可能漂移的科学稿。当前未指定目标期刊，故本稿不声称符合某一刊会模板。

## 文件

- `Survey_Final_Review.pdf`：正式引用编排的完整审阅 PDF，43 页，九章、五图、七表、附录 A/B、50 条参考文献。T7 占两页横向 A4。
- `source/build.cjs`、`source/numeric.csl`、`source/package.json`、`source/package-lock.json`：可编辑排版源与锁定依赖。R5 Markdown/Bib/SVG/表格均为可编辑源。
- `R7_Typesetting_QA.md`、`R7_Figure_Table_QA.md`、`R7_Bibliography_Final_Audit.md`、`R7_Open_Issues.md`、`R7_Final_Handoff.md`：验收记录。
- `Figure_Table_Check_Pages.pdf`：图表重点页检查册；本地 41 页预览所抽取的 17 页，不代替最终 43 页 PDF 的逐页复核。

## 重建

在仓库根目录运行：

```bash
sudo apt-get install pandoc fonts-noto-cjk poppler-utils
cd 03_survey/R7_submission/source
npm ci
npx playwright install --with-deps chromium
REQUIRE_PANDOC=1 npm run build
```

Windows 可安装 Pandoc、Node.js 24 和 Playwright Chromium 后执行相同的 `npm ci` / `npm run build`。不设置 `REQUIRE_PANDOC=1` 且缺少 Pandoc 时，仅会生成采用 R6 手工书目表的本地版面预览；正式交付必须使用 Pandoc citeproc 和 `numeric.csl`。构建脚本只使用相对路径，不依赖本机 Edge 路径。Linux 字体优先 Noto Serif/Sans CJK SC；Windows 回退 SimSun/Microsoft YaHei，数学字体优先 Cambria Math/STIX Two Math。字体不同会改变分页，须重新做视觉检查。

构建失败时，先检查 `pandoc --version`、`node --version`、Playwright Chromium 安装、R5 正文的 50 个引用键和 SVG 路径。脚本会对缺失表格、未知引文、未映射公式、书目数量及最终 PDF 报错。CI 工作流只在本 R7 分支的排版源或 R5 源变化时构建，并提交 PDF 与依赖锁文件；不会推送到 main。

未提供 DOCX：现有排版包含横向 T7 和 SVG/MathML，尚未验证忠实的 Word 转换。可编辑的 Markdown、BibTeX、SVG、表格与排版配置均已保留。
