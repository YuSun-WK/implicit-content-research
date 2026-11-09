# R6-V｜46条BibTeX、引用与链接工程审计（2026-11-09）

## 一、范围与方法

读取PR #57的以下真实文件：`Survey_Full_Draft.md`、`references.bib`、`Citation_Key_Mapping.md`、`Bibliography_Conflicts.md`，及T1–T7七份Markdown表；并抽核AUTALIC的[ACL Anthology正式页](https://aclanthology.org/2025.acl-long.1022/)以及ThinkingGuard[作者公开稿](https://arxiv.org/abs/2609.36562)和[作者仓库](https://github.com/FroggyChen/ThinkingGuard)。

扫描方式为GitHub源文件文本逐项比对、BibTeX条目/字段/大括号静态解析、正文`[@key]`语法提取、表格引用提取、Markdown本地链接与标题/公式标记检查；**未编译BibTeX/LaTeX，也未对46条参考文献全部逐篇核对出版平台PDF首页**。

## 二、检查结果

| 项目 | 结果 | 结论 |
|---|---|---|
| `references.bib`条目 | 46 | PASS：无重复key |
| 全文+七表实际引文key集合 | 46 | PASS：都在BibTeX中存在 |
| 仅Bib有、全文及表均无引用的key | 0 | PASS |
| 正文及七表引用但Bib缺失 | 0 | PASS |
| 基础字段author/title/year及inproceedings容器 | 46条按类型静态检查 | PASS（未出现空缺） |
| DOI字段存在 | 36条 | 不强制全员有DOI；缺失项需按出版类型判断 |
| URL字段存在 | 36条 | 同上；部分DOI可作为书目入口 |
| 正文九章 | 9个一级章节 | PASS |
| 正文章节二级小节 | 46个 | PASS |
| 正文图像链接 | F1–F5五个 | PASS：在PR #57分支均存在 |
| 正文七张表链接 | T1–T7 | PASS：结构与路径一致 |
| 相对本地链接 | 共17次引用（包含重复目标） | PASS：目标文件均在PR #57的21份交付中 |
| 内联数学标记`\\(`/`\\)` | 各11次 | PASS：未见数量不匹配；未作正式TeX排版 |
| 参考文献显示 | 第41和45项出现空斜体标记 | **FIXED**：在R6-V分支正文尾部修正 |

## 三、已提交的确定性修复（不更改科学主张）

- 参考文献第41条ThinkingGuard原文字尾部 `**.` 空强调/文献容器残留 → 写作 `*arXiv 预印本*`。作者接收/ACM正式Track问题仍保留原冲突台账，**未升格为ACM正式论文**。
- 参考文献第45条Searle专著 `**.` → 使用BibTeX本有的出版机构 `*Cambridge University Press*`。不添加未经核准的页码或版本。
- 上述修改只涉及`03_survey/R5_full_draft/Survey_Full_Draft.md`的两处书目显示行；章节正文、论文引文键及实验数字未动。

## 四、需留待R6-A/最终编排的开放事项

1. **AUTALIC**：Anthology正式网页显示12作者与2,400条；本项目记录正式PDF首页13作者（含Michael Golden）与正文242+2160=2402算术矛盾。本分支**保留首作者+others的Bib简化写法**，不无依据补齐作者；不得据公开网页直接否定PDF版差异。实际许可也需遵守。
2. **ThinkingGuard**：作者仓库给出ACM MM 2026录用及DOI `10.1145/3767308.3835707`，但目前未取得ACM出版社最终条目/Track。本稿`@misc`与arXiv链接保留。**会议CCF-A等级不能替代论文Track出版核验**。
3. **VLSU**：论文PDF与公开CSV的8,187/8,159，S-S-U 37/35，官方摘要11模型/PDF17模型仍为版本问题，不应“修正”为单一数字。
4. **SeTox**：正式ACL BibTeX优先于作者旧README；本轮只做静态一致性比对，未重访所有出版源。
5. **46条逐项出版源核验不足**：静态字段完整、引用键完整 ≠ 所有标题/作者/DOI/出版社元数据经独立核对；建议R6最终版逐条以正式平台导出对照。
6. **T5 DOSE输入模态内容冲突**：表5写“文/音/视”，而正文§6.3写“新闻图文”；此为科学事实核对对象，R6-V不改表，需R6-A确认论文ACL 2026 Main（CCF-A）真实协议。
7. **图/表位置和长表版式**：有五图七表真实链接，但目标期刊尚未确定；T2/T6尤其需要通栏/横向版面检查。Markdown源码通过并不意味着DOCX/LaTeX印刷布局通过。
8. **Markdown渲染器差异**：Pandoc风格的`[@key]`有环境依赖，普通GitHub Markdown不自动转作者年份；投稿时应选定Pandoc/CSL/LaTeX工具链完成正式引文转换。

## 五、交付关系

- R5-C原分支PR #57保持Draft且未被本轮直接修改。
- 本R6-V分支基于#57的HEAD，PR针对R5-C分支，只包含本轮差分，便于在R6-A学术审查期间独立验收。
- R6-V报告与图形改动仅解决**工程层**问题；学术证据准入决定权仍归R6-A/R6合并审查。
