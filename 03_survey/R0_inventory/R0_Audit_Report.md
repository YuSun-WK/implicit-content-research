# R0 Audit Report｜文献资产盘点

日期：2026-11-08。仅盘点现有资料；未改动 GitHub 原始文件，未撰写综述正文。

## 数量与去重

| 项目 | 数量 | 口径 |
| --- | --- | --- |
| 仓库 papers.csv | 41 | 保留 P001–P041 |
| 上传 CSV 可识别论文行 | 61 | 不含 4 个分区标题 |
| 跨源匹配 | 41 | 标准化完整题名；仓库 DOI 保留作核验锚点 |
| 上传表内部重复行 | 2 | P009 两行、P023 两行各多一条 |
| 新增独立论文 | 18 | 临时编号 T001–T018 |
| 合并后独立论文 | 59 | 41+18；未合并未证实的相似论文 |


上传表内部重复：P009（上传行 6、13）, P023（上传行 32、70）。仓库 sources.csv 共 43 行，对应 41 篇；P002、P026 各有两个版本来源，**来源行不是新增论文**。zotero_mapping.csv 共 89 行，含已清理的历史重复馆藏键，**馆藏映射行不是论文数**。

## 阅读与核验状态

| 精读状态 | 篇数 |
| --- | --- |
| 已分析，精读程度待核验 | 6 |
| 待分析 | 31 |
| 已精读 | 21 |
| 暂缓定稿 | 1 |


有阅读卡 **27 篇**；P031 无正式阅读卡，但有单独待审记录。仓库待分析 13 篇；新增 18 篇均未见阅读卡。
“已精读”仅在仓库阅读状态、卡片或来源清单提供全文精读证据时使用；“已分析，精读程度待核验”不自动提升。开放问题与阅读完成并存。

## 年份、等级与类型

文献总数、去重及阅读状态未变。P002 现分记 2025 在线发表、2026 卷期（58(2)，Article 42）；其原始 2024 年份保留于“年份原值”，对应 arXiv 阅读版。P001 为 [ACL 2022 Main Long Paper](https://aclanthology.org/2022.acl-long.234/)，会刊 A 类。

按总索引当前“年份”字段，2020/2021/2022/2023/2024/2025/2026 年分别为 1/3/4/1/4/19/20 篇；P002 的双年份另列 1 篇，年份仍待核的 6 篇另列。刊会等级汇总：A 29、B 23、第七版未收录 6、不适用 1。出版核验状态：本轮定点核验 6 篇、沿用仓库正式版来源记录且本轮未逐篇外部复核 32 篇、仍待核验 21 篇；这些状态与精读状态无关。

**统一口径**：[CCF 第七版（2026）](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)只决定刊会等级；论文的实际 Track 和是否经官方正式出版核验为独立字段。ACL、KDD、WWW、NeurIPS、ACM MM、ICLR 属 A；EMNLP、COLING、NAACL、TKDD、IPM、IEEE TAC 属 B。ACM Computing Surveys 在此版目录中未收录，并非“待猜测的 A/B”。Findings、Industry、Datasets & Benchmarks 等论文仍显示所属刊会等级，但不得直接据此断定为 A/B 类主会常规论文。Research Square/arXiv 预印本无刊会等级。

### 定点出版核验

| 编号 | 已确认事实 | 待核边界与证据 |
| --- | --- | --- |
| P001 | ACL 2022 主会 Volume 1: Long Papers；DOI 10.18653/v1/2022.acl-long.234；ACL 第七版 A | [ACL Anthology](https://aclanthology.org/2022.acl-long.234/) |
| P002 | 正式 ACM Computing Surveys DOI **10.1145/3744554**；2025 在线、2026 卷期 58(2) Article 42；第七版未收录该刊 | [ACM 正式版](https://dl.acm.org/doi/10.1145/3744554)；[arXiv 2024 阅读版](https://arxiv.org/abs/2406.16674)的 DOI 10.48550/arXiv.2406.16674 不可充当正式版 DOI；全文差异待核 |
| T001 | ALARM 列于 KDD 2026 官方 Research 论文名单；DOI 10.1145/3770854.3780213；KDD A | [KDD 官方名单](https://kdd2026.kdd.org/papers/)；[DOI](https://doi.org/10.1145/3770854.3780213) |
| T003 | CausalHM 列于 WWW 2026 会议录 pp. 7517–7528；DOI 10.1145/3774904.3792627；WWW A | [DOI](https://doi.org/10.1145/3774904.3792627)；[作者公开书目](https://github.com/critivitycheng/CausalHM) |
| T014 | NeurIPS 2024 Datasets & Benchmarks Track 正式论文；NeurIPS A | [官方论文页](https://proceedings.neurips.cc/paper_files/paper/2024/hash/17fc467c11997914127c001fdc801bea-Abstract-Datasets_and_Benchmarks_Track.html)；该 Track 的 CCF Full/Regular 计数适用性待审核 |
| T015 | Hateful Memes 收录于 NeurIPS 2020 官方论文集；NeurIPS A | [官方论文页](https://papers.nips.cc/paper/2020/hash/1b84c4cee2b8b3d823b30e2d604b1878-Abstract.html)；DOI 未见可靠记录 |
| P039 | ACM MM 第七版 A；作者录用声明及 DOI 10.1145/3767308.3835707 已见 | [arXiv 记录](https://arxiv.org/abs/2609.36562)；ACM 正式论文页、会议录、实际 Track 待核。DOI 登记不等于正式出版 |

### 2024–2026 A 类论文计数

**21 篇**有正式主会常规/Research 出版证据且刊会列为 A：其中 19 篇沿用仓库来源清单的正式版记录（本轮未逐篇外部复核），T001、T003 为本轮定点外部核验。另有 T014 为 A 类刊会的正式 Datasets & Benchmarks Track 论文，因 CCF Full/Regular 口径适用性未定而单列；P039 为 A 类刊会录用/DOI 已见但正式出版未核，暂不计入。此为现有索引的严格统计，不是领域完整检索结果。

## 主要未解决问题

- **出版与元数据**：P002 正式版/阅读版全文差异；P006 上传 2025 与仓库 2026；P009 在线年/馆藏年；P039 ACM MM 正式版；P004、P014、P016、P018、P021、P025 的正式出处。T001、T003、T014、T015 已完成定点官方/会议录核验；其他临时条目仍有出版信息待核。
- **机制/评测**：P031 暂缓定稿；P029、P033 评测协议风险；P034 奖励实现差异；P038 论文/公开数据规模不同；P040 消融数据未实物核验。其他逐篇开放项见总索引及相应阅读卡。
- **来源级别**：P007 是 Findings；P041 是 NAACL Findings；P004 为 Research Square 预印本；P039 的仓库来源为 arXiv/作者录用记录；ACM MM 的 A 类刊会等级已核，但正式出版与 Track 未核，不计入严格 A 类主会论文数。

## 可追溯性与方法

- 仓库快照：main tree SHA `9487d27bd918310719710ee85376afd87e3dc1b1`；主要来源：[papers.csv](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/papers.csv)、[sources.csv](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/sources.csv)、[zotero_mapping.csv](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/zotero_mapping.csv)、[cards/](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards)、[audits/](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/audits)、[02_synthesis/](https://github.com/YuSun-WK/implicit-content-research/blob/main/02_synthesis)。
- 上传文件：`D:/download/论文总结 - 隐晦信息检测.csv`（用户所述 xlsx 在本轮提供的是该 CSV 导出；只见这一工作表）。总索引逐行列明上传表行号与原始刊会字段。
- 对齐规则：先用标准化题名精确匹配（Unicode 归一、标点/空白折叠、末尾简称移除），再审阅相似题名；仓库编号优先。无 DOI 的新增条目按题名区分，正式身份仍待下一阶段核验。
- 本轮按 [CCF 第七版发布页](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)及[目录 PDF](https://dengpingfan.github.io/papers/CCF-Recommend-2026.pdf)核对刊会等级，并对上述指定条目做定点出版核验；未对全库作大规模新文献检索。原始文献记录、阅读卡及 02_synthesis/ 未改动。
