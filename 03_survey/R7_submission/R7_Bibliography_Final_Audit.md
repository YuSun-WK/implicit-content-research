# R7 参考文献终校记录

基线为 main 的 `references.bib`、正文手工书目、七表与附录 A/B。共 50 个唯一 BibTeX key；正文使用的 50 键与手工表一一对应，没有扩充或删减。正式 PDF 在 CI 中执行 `pandoc --citeproc --bibliography ... --csl source/numeric.csl`，日志显示生成 50 个书目条目；数值引文和末尾列表统一编号，参考文献使用悬挂缩进。Bib 字段中 37 条含 DOI、39 条含 URL；无正式 DOI 的条目保持空缺。

## 出版元数据核对

对 28 个 ACL Anthology 入口逐条对照正式页面：28/28 的题名、年份、DOI、页码一致；27/28 的作者数和顺序一致。余下 AUTALIC 是正式网页与 PDF 首页彼此冲突，不能据其中一方补造完整作者字段。其余 22 条以可访问的出版页、正式索引或既有 R6 证据卡核对可见字段；ACM 与部分 AAAI/CVF 页面访问受限，未宣称 50 条的每个字段均获出版社最终导出认证。

| 条目 | 本轮核对及保守处理 |
|---|---|
| AUTALIC `rizvi-etal-2025-autalic` | [ACL 页面](https://aclanthology.org/2025.acl-long.1022/)列 12 作者，[正式 PDF](https://aclanthology.org/2025.acl-long.1022.pdf)首页列 13 作者（含 Michael Golden），顺序也不同。保留 `Rizvi and others`，需出版方澄清。DOI、年份、页码已核。 |
| ThinkingGuard `zhang2026thinkingguard` | [作者仓库](https://github.com/FroggyChen/ThinkingGuard)声称 ACM MM 2026 与 DOI；未取得 ACM 最终条目及 Track。维持 arXiv 预印本 `@misc`，不算正式会议。 |
| VLSU `palaskar2026vlsu` | [ICLR 2026 页面](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)确认出版身份；正式 PDF、官方摘要、公开 CSV 的样本/模型/类别计数仍有版本差异，维持正文原有分版本说明。 |
| Searle | [1969 专著](https://www.cambridge.org/core/books/speech-acts/D2D7B03E472C8A390ED60B86E08640E7)与 1975 年《Syntax and Semantics》卷 3 pp.59–82 章节分列。 |
| Mao 等 `mao2025pragmatic` | [Information Fusion 正式页](https://www.sciencedirect.com/science/article/pii/S1566253524004901)：114 (2025), 102712, DOI 10.1016/j.inffus.2024.102712；仅用于相邻综述定位。 |
| Ye `ye2025safety` | [arXiv v1](https://arxiv.org/abs/2502.14881v1)可核；未验证正式发表，保留预印本级别。 |

仍需投稿前人工核对：AUTALIC 出版方更正、ThinkingGuard ACM 最终条目及 Track、VLSU 数据版本；ACM/AAAI/CVF 被访问限制的条目请再对出版社导出 BibTeX 与 PDF 首页。详见 `R7_Open_Issues.md`。不能将现有可见字段核对说成全 50 条逐字段终审完成。
