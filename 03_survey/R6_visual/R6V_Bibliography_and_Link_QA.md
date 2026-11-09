# R6-V｜BibTeX、正文引用、表格与技术链接审计（2026-11-09）

## 输入与审计界限
- 来源：[PR #57](https://github.com/YuSun-WK/implicit-content-research/pull/57)，`03_survey/R5_full_draft/`中的九章主稿、`references.bib`、引文键映射、冲突台账与T1–T7。
- **不修改任何学术论断或原始PR #57正文**；只输出可确定的格式修补patch与独立QA结果。
- 通过GitHub连接器读取原文件；本次字面/结构审计检查UTF-8内容、BibTeX外层平衡及必要字段；**尚未调用完整BibLaTeX/biber编译，也未逐项重新下载46篇PDF核出版社条目**。

## 一、引文与 BibTeX 验收

| 规则 | 结果 | 解释 |
|---|---|---|
| BibTeX条目总数与键唯一性 | **46 / 46唯一，PASS** | 无重复键 |
| 结构性必要字段 | **PASS（静态）** | 46条都有title/author/year；inproceedings有booktitle、article有journal、book有publisher；外层大括号平衡 |
| 正文`[@key]`及并列引文→BibTeX | **PASS** | 全部46个被引用的key均存在BibTeX中 |
| BibTeX→正文被引 | **PASS** | 没有未被正文实际引用的46条以外文献 |
| 正文/书目显示层 | **需修复两处** | 参考文献第41行ThinkingGuard和第45行Searle自动排版为无意义`**.`；见`R6V_Reference_Display.patch` |
| 46条官方出版字段逐项独立核实 | **NOT COMPLETE** | 原R5-C混合已核官方记录和项目阅读卡；不能宣称全部逐字出版方BibTeX |

**注意**：以上只能确认键映射和静态结构完整，不代表BibTeX已经通过目标期刊模板的完整排版编译。建议R6-Fix执行`biber`或目标模板bibtex/pandoc的真实构建以检查姓名解析、大小写保护和中文/英文标点。

## 二、重点书目核验/保留

1. **AUTALIC** `rizvi-etal-2025-autalic`：ACL Anthology正式网页及其导出BibTeX列**12位作者**，而正式PDF首页列**13位**（包含 Michael Golden，顺序也不同）；已比较官方两种载体。R5-C `Rizvi, Naba and others`是**保守暂行写法**，不是完整最终作者表。总量2400与242+2160=2402的标注统计矛盾继续保留。官方网页： https://aclanthology.org/2025.acl-long.1022/ ，PDF： https://aclanthology.org/2025.acl-long.1022.pdf 。**未经作者/出版方说明不得自动判定哪个名单最终胜出。**
2. **ThinkingGuard** `zhang2026thinkingguard`：作者公开稿与作者仓库提供ACM MM 2026接收和DOI`10.1145/3767308.3835707`，但本轮仍未可靠取得**ACM出版社最终书目和实际Track**。原`@misc`保留为预印本而不强行升级为已核正式Main。可确定的是第41条显示`**.`应替换为“*arXiv预印本*.”。
3. **Searle** `searle1969speech`：BibTeX有`publisher = {Cambridge University Press}`；正文第45条`**.`属于明显格式生成错误，应替换为`*Cambridge University Press*.`（不改变论文研究论证）。
4. **VLSU**：BibTeX取正式ICLR 2026出版记录；PDF/公开CSV 8,187/8,159、S-S-U 37/35、模型17/11的差异不是BibTeX能解决的问题。表6仍需按各协议保留分母，不得自动统一数字。
5. **SeTox**：采用ACL Anthology正式出版条目，不能用作者README旧引用字段覆盖。
6. **IJCAI 2024 Survey**：会议在项目采用CCF 2026第七版口径为B，Survey Track不等同Research/Main Track；保留主稿映射的正式出版类型。

## 三、表T1–T7 QA（静态格式，非最终论文版面）

| 表 | 数据行 | 列 | Markdown列数匹配 | 排版关注 |
|---|---:|---:|---|---|
| T1 概念 | 7 | 6 | PASS | 通栏/必要时缩写表头 |
| T2 任务/GT | 6 | 6 | PASS | 文字密集，宜横向跨栏或附录 |
| T3 编码 | 5 | 5 | PASS | 定义/评价列可保留较宽 |
| T4 语境有害 | 5 | 4 | PASS | 语义长度适中 |
| T5 多模态意义 | 7 | 4 | PASS | 辅助输入字段需允许换行 |
| T6 多模态安全 | 9 | 5 | PASS | 数据版本脚注和指标分母不能缩掉 |
| T7 方法族 | 7 | 4 | PASS | 控制实验长句最密，建议跨栏/拆分 |

- 7张表均含引文标记；通过分隔符列数静态检查，未发现缺列或多列。
- 表格**尚未在目标期刊版心和指定字号中真实排版渲染**；不能把“Markdown格式PASS”当作排版PASS。建议T2/T6/T7优先通栏，宽度不足时拆成主表和补充表。R6-A负责学术真实性；本轮不改表格中的任何数值。

## 四、文内链接、公式与标题检查

- 在`Survey_Full_Draft.md`找到17次非HTTP本地相对链接；各目标均在PR #57的文件集中且路径存在，**PASS（目录级）**。外部https链接未逐站复测404/重定向。
- 原稿包含9章、46节，章节标题与小节号连续；没有大面积TODO图表占位，F1–F5由相对链接引入。
- 行内LaTeX使用`\\( ... \\)`等模式，须到正式MD→PDF/Word转换器再作数学排版测试；本次**没有可声称完整公式排版通过的PDF**。
- 第41、45条是本次发现的确定显示错误；见补丁。现有稿仍为结构化批判性叙述综述，不能当作已满足目标期刊排版的终稿。

## 五、开放问题及移交

**本轮已解决（在独立副本/补丁中）**：中文SVG跨平台可渲染性；提供5图独立SVG可视预览；两处文末标点/斜体格式的精确修复补丁；46键双向引用一致性；T1–T7静态列结构与内部相对链接检查。

**依然OPEN**：审稿人对图文内容的学术判断；目标期刊正式通栏可读字号与真实打印样张；BibTeX逐字段官方核验；AUTALIC作者争议、ThinkingGuard最终ACM出版Track、VLSU版本差异；公式真实PDF构建、各表最终版面和外部URL可达性。

**R6-V结论**：技术审查**Conditional PASS**，不是“投稿排版通过”。请将本分支经人工审阅的修订SVG与引用显示patch在最终R6-Fix阶段整合入R5-C主稿，保留科学证据状态；不要直接合并正在审阅的R5-C PR。
