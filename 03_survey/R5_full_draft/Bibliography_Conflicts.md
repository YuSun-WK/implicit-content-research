# R5-C 书目与版本冲突台账

审计日期：2026-11-09。F=正式出版事实；P=作者报告；S=公开文件静态观察；O=未关闭。仅在能核的字段上建立 `references.bib`；以下冲突不能凭简称、旧 README 或记忆补写。

| 条目 | 已核事实与冲突 | 本稿处理 | 未关闭动作 |
|---|---|---|---|
| AUTALIC [@rizvi-etal-2025-autalic] | ACL Anthology网页/.bib列12作者；其正式PDF首页列13作者，含 Michael Golden，顺序亦有差异；DOI与页码一致 [F] | Bib作者暂记 `Rizvi, Naba and others`，正文以 Rizvi 等短引；不声称完整作者字段已核 | 投稿前以PDF逐人核校并请求出版元数据更正；原CSV 2400与分项2402亦未闭 |
| ThinkingGuard [@zhang2026thinkingguard] | 作者仓库称ACM MM 2026接收及 DOI，出版社最终条目和实际 Track 未独立取得 [P/O] | 仅作arXiv公开研究先例，Bib标 `@misc`；不计已核ACM Main | 核ACM正式页、作者顺序、页码/Article ID及Track，再决定替换预印本条目 |
| VLSU [@palaskar2026vlsu] | 正式PDF报告8187、17模型、S-S-U 37；官方摘要仍写11模型；此前公开CSV实读8159、S-S-U 35 [F/P/S] | Bib采用ICLR 2026正式会议信息；正文/表6分版本标数字 | 对齐正式PDF、摘要与发布CSV快照；图片可达性、28条差异与test-only限制仍待核 |
| SeTox [@cui-etal-2026-new] | 作者仓库旧BibTeX与ACL Anthology正式条目有字段冲突 [F] | 取ACL 2026 Main正式页面导出的BibTeX | 不再用README覆盖正式作者与页码；投稿时再核PDF首页 |
| IJCAI 2024 Survey [@farabi2024survey] | 旧记录把IJCAI标CCF-A；项目采用2026第七版为CCF-B，且本文为Survey Track [F] | 引文映射按B、Survey Track，Bib正常书目不嵌入等级 | 若目标刊要求不同年份目录，另列评级口径 |
| MCIB [@wang2026conditional] | AAAI 2026 Technical 已核；正式主文、扩展版与公开实现的目标函数/训练路径未完全对齐 [F/P/S/O] | Bib以AAAI卷期页码/DOI为准；正文只引作者整体结果与已审结构消融 | 正交去CIB消融、公开代码版本与正式训练关系仍待核 |
| MultiMM / MGMCF [@yang-etal-2025-cultural; @zheng2025multigranular] | 所查代码含gold情绪或源/目标辅助特征 [S]；正式结果是否等同该运行路径未核 [O] | 表5单列测试信息预算；不将静态风险写成已证实论文结果错误 | 获取模型运行配置及同预算基线 |
| ExPO-HM [@mei2026expohm] | ICLR 2026 Conference（CCF-A）官方出版页与作者Bib均可核，已于R6-Fix补入正文与书目 [F/P] | 依据官方论文记录与作者字段建唯一新条目；分类目的为Explain-then-Detect并非严格S-S-U输入三标签 | 完整正式PDF/公开脚本的课程配置与CDE实现差异仍为P/S/O，不能把静态发布当正式训练配置 |
| Searle 1975 [@searle1975indirect] | 间接言语行为原典为Cole/Morgan主编《Syntax and Semantics》卷3 pp.59–82，独立于Searle 1969专著 [F] | 补入理论原典并保留1969书目 | 出版社目录的具体纸本版次由R6-V按目标期刊体例核对 |
| CVF / ICLR / NeurIPS 非ACL条目 | 某些出版站点即时访问受限；CVF摘要索引、ICLR正式页、NeurIPS出版页及已审卡片可核主要字段 [F/P] | 采用可核字段，缺 DOI/页码时留空，不推造；参见引文映射 | R6排版前逐条重取官方BibTeX与PDF首页比对 |

**书目准入。** `references.bib` 是R6-Fix在R5-C的46条基础上新增ExPO-HM与Searle 1975后的48条学术引用工作稿，非“所有48条逐字段均已由出版社最终BibTeX核验”的声明。正文实际引用、Bib条目与映射一一对应；出版社未能取得的字段保守留空。
