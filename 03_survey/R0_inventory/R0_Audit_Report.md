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

| 年份 | 篇数 |
| --- | --- |
| 2020 | 1 |
| 2021 | 3 |
| 2022 | 4 |
| 2023 | 1 |
| 2024 | 4 |
| 2025 | 20 |
| 2026 | 20 |
| 待核验（2025在线/2026馆藏日期（待核验）） | 1 |
| 待核验（上传表：2025） | 5 |


| CCF字段 | 篇数 |
| --- | --- |
| A | 23 |
| B | 14 |
| 不适用/待核验 | 9 |
| 待核验 | 12 |
| 未列入（上传表声称） | 1 |


CCF 字段是**刊会等级**，不等于某篇论文已正式发表。Findings、Industry Track、D&B Track、Workshop 与 arXiv 不套用主会 A/B 等级；上传表声称未经过正式出版核验的新增条目在总索引中单列“CCF说明”。ACM Computing Surveys 的上传行互相矛盾（P009、P002 等），统一保留“待核验”。CCF 目录入口：[CCF 推荐目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/)。

## 主要未解决问题

- **出版与元数据**：P002 预印本/期刊版本；P006 上传 2025 与仓库 2026；P009 在线年/馆藏年；P039 ACM MM 正式版；P004、P014、P016、P018、P021、P025 的正式出处。T001–T018 的 DOI 与官方链接均待核。
- **机制/评测**：P031 暂缓定稿；P029、P033 评测协议风险；P034 奖励实现差异；P038 论文/公开数据规模不同；P040 消融数据未实物核验。其他逐篇开放项见总索引及相应阅读卡。
- **来源级别**：P007 是 Findings；P041 是 NAACL Findings；P004 为 Research Square 预印本；P039 的仓库来源为 arXiv/作者录用记录。不得计作已经核定的 A 类正式主会论文。

## 可追溯性与方法

- 仓库快照：main tree SHA `9487d27bd918310719710ee85376afd87e3dc1b1`；主要来源：[papers.csv](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/papers.csv)、[sources.csv](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/sources.csv)、[zotero_mapping.csv](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/zotero_mapping.csv)、[cards/](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards)、[audits/](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/audits)、[02_synthesis/](https://github.com/YuSun-WK/implicit-content-research/blob/main/02_synthesis)。
- 上传文件：`D:/download/论文总结 - 隐晦信息检测.csv`（用户所述 xlsx 在本轮提供的是该 CSV 导出；只见这一工作表）。总索引逐行列明上传表行号与原始刊会字段。
- 对齐规则：先用标准化题名精确匹配（Unicode 归一、标点/空白折叠、末尾简称移除），再审阅相似题名；仓库编号优先。无 DOI 的新增条目按题名区分，正式身份仍待下一阶段核验。
- 本轮针对 CCF 仅查阅 [CCF 官方目录入口](https://www.ccf.org.cn/Academic_Evaluation/By_category/)及其中 [人工智能目录](https://www.ccf.org.cn/Academic_Evaluation/AI/)、[数据/内容检索目录](https://www.ccf.org.cn/Academic_Evaluation/DM_CS/)；未替每篇新增论文做外部扩展检索。刊会版本差异与 track 仍需学术复核。
