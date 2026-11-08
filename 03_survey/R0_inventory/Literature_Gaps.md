# Literature Gaps｜现有文献覆盖缺口

更新：2026-11-08。这里的“缺口”指**现有资料的覆盖或证据缺口**，不能直接推断整个领域没有相关论文。本轮未开展大规模扩展检索。

## 2024–2026 CCF-A 优先核对

按 [CCF 第七版（2026）目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)的**刊会等级**、论文的**实际 Track**及**出版核验状态**分列。现有 59 篇中，2024–2026 年 A 类刊会且有正式主会常规/Research 出版证据的论文 **21 篇**：原有 19 篇沿用仓库正式版来源记录（本轮未逐篇外部复核），新增 [T001（KDD 2026 Research）](https://kdd2026.kdd.org/papers/)与 [T003（WWW 2026）](https://doi.org/10.1145/3774904.3792627)经定点核验。此数并不代表广义隐晦信息领域的总量。

| 编号 | 刊会等级 | 实际 Track 与出版状态 | 严格计数 |
| --- | --- | --- | --- |
| T001 | KDD：A | 2026 Research 正式论文；官方名单及 DOI 已核 | 计入 |
| T003 | WWW：A | 2026 正式会议录；DOI 已核 | 计入 |
| T014 | NeurIPS：A | 2024 Datasets & Benchmarks 正式论文；[官方论文页](https://proceedings.neurips.cc/paper_files/paper/2024/hash/17fc467c11997914127c001fdc801bea-Abstract-Datasets_and_Benchmarks_Track.html)已核 | 另列；该 Track 是否符合 CCF Full/Regular 口径待学术审核 |
| P039 | ACM MM：A | 作者录用声明及 DOI 已见，正式 ACM 论文页/会议录与实际 Track 未核 | 暂不计入 |

P027、P038 所属 ICLR 在第七版为 A 类；P001 为 2022 年 ACL Main，因此不进入 2024–2026 统计。Findings、Industry、Workshop 与预印本不能因刊会为 A 就计作 A 类主会常规论文。

### 覆盖和核验优先级

1. **剩余出版与 Track 核验**：T001、T003 的正式出处已补证；T014 官方 Datasets & Benchmarks 论文页已找到，但是否纳入 CCF Full/Regular 计数仍待学术审核。P039（ThinkingGuard）有作者录用与 DOI 记录，仍需 ACM 正式论文页/会议录及实际 Track。ICLR 2026 的 P027、P038 按 CCF 第七版记 A。
2. **跨语言与中文真实编码表达**：P023 提供中文评论编码语言，T008–T009、T011–T013 补谐音/伪装/委婉语线索；临时条目无正式出处和精读证据。跨平台、跨语种、随时间变动的新编码策略覆盖不足。
3. **从标签到含义的可核验链条**：现有检测/基准常直接预测类别。隐含意义恢复、说话者意图、受众知识与伤害判断的分层金标、合理分歧及解释忠实性仍缺可比协议；这是基于现有材料的研究假设，见 R1–R4。
4. **图文联合风险与多模态捷径**：P034、P037–P041 已覆盖多个 2025–2026 高水平候选，但视觉泄漏、图文反事实配对、单模态基线、同预算对比和拒答/有用性权衡仍有开放审计项。不能把普通 Meme 检测直接当作“联合后才有害”的证据。
5. **视频与动态语境**：仅 P025、P028 明确以视频为对象；P025 尚未分析、正式出处未核。音频、时间上下文与跨帧隐含风险在本批材料中明显稀疏。
6. **复现与数据版本**：P029 的评测泄漏风险、P031 的机制疑点、P033 的测试集参与选择、P038 的数据行数不一致、P039 的正式版、P040 的消融与数据实物均未关闭。已“定稿”的阅读卡不表示复现通过。

## 下一阶段最小核验清单

- 继续核对尚无官方出版证据的临时编号；T001、T003、T014、T015 已完成本轮定点出版核验，T014 的严格计数口径仍待审核。
- 对 P002 正式版与阅读版全文差异、P006/P009 年份、P039 正式出版及其余来源冲突条目继续核验。
- 按方向补读，而非按“隐式仇恨”单一路线扩展。当前记录支持优先补中文编码/委婉、跨语言语用、视频及联合模态安全。

出处：[仓库来源清单](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/sources.csv)、[P031 待审记录](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/audits/P031_AmpleHate_mechanism_pending.md)、[R1–R5 综合目录](https://github.com/YuSun-WK/implicit-content-research/blob/main/02_synthesis/README.md)；新增候选见总索引中的上传表行号。
