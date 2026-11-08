# Literature Gaps｜现有文献覆盖缺口

更新：2026-11-08。这里的“缺口”指**现有资料的覆盖或证据缺口**，不能直接推断整个领域没有相关论文。本轮未开展大规模扩展检索。

## 2024–2026 CCF-A 优先核对

仓库现有记录中，2024–2026 年、标为 A 且已记载正式主会出处的条目有 **19 篇**（按本轮来源和类型判定；CCF 版本仍应在学术审核时复核）。它们集中于 ACL、ICML、WWW 与部分多模态安全方向。另有 **4 篇** A 类声称不满足“已核正式主会”条件，包含上传表新增候选、Findings/非主会或正式出版待核条目；不得并入前述数量。

| 编号 | 年 | 需区别对待的候选 | 现阶段类型 |
| --- | --- | --- | --- |
| P039 | 2026 | ThinkingGuard: Decoding Implicit Hazards via Step-by-Step  | 录用/正式出版待核验 |
| T001 | 2026 | From Shallow Humor to Metaphor: Towards Label-Free Harmful | 会议主会（上传表声称/待核验） |
| T003 | 2026 | Bias Mitigation for Harmful Meme Detection using Front-doo | 会议主会（上传表声称/待核验） |
| T014 | 2024 | Towards Comprehensive Detection of Chinese Harmful Memes | 会议D&B Track（非主会） |


### 覆盖和核验优先级

1. **新增 2024–2026 A 类候选先做出版核验**：T001（ALARM/KDD 2026）、T003（CausalHM/WWW 2026）、T014（ToxiCN-MM/NeurIPS D&B 2024）只来自上传表；需官方论文页、track、DOI/永久链接。P039（ThinkingGuard）仅有作者录用记录及 arXiv，正式 ACM MM 版本待核。ICLR 2026 的 P027、P038 虽有正式会议来源，CCF 等级应按所采用目录版本复核。
2. **跨语言与中文真实编码表达**：P023 提供中文评论编码语言，T008–T009、T011–T013 补谐音/伪装/委婉语线索；临时条目无正式出处和精读证据。跨平台、跨语种、随时间变动的新编码策略覆盖不足。
3. **从标签到含义的可核验链条**：现有检测/基准常直接预测类别。隐含意义恢复、说话者意图、受众知识与伤害判断的分层金标、合理分歧及解释忠实性仍缺可比协议；这是基于现有材料的研究假设，见 R1–R4。
4. **图文联合风险与多模态捷径**：P034、P037–P041 已覆盖多个 2025–2026 高水平候选，但视觉泄漏、图文反事实配对、单模态基线、同预算对比和拒答/有用性权衡仍有开放审计项。不能把普通 Meme 检测直接当作“联合后才有害”的证据。
5. **视频与动态语境**：仅 P025、P028 明确以视频为对象；P025 尚未分析、正式出处未核。音频、时间上下文与跨帧隐含风险在本批材料中明显稀疏。
6. **复现与数据版本**：P029 的评测泄漏风险、P031 的机制疑点、P033 的测试集参与选择、P038 的数据行数不一致、P039 的正式版、P040 的消融与数据实物均未关闭。已“定稿”的阅读卡不表示复现通过。

## 下一阶段最小核验清单

- 先核对 T001–T018 的正式论文页、DOI、年/track 和 CCF 目录版本，再把上传表声称转为可计数事实。
- 对 P002、P006、P009、P010、P039 等来源冲突条目做版本/年份/等级核验。
- 按方向补读，而非按“隐式仇恨”单一路线扩展。当前记录支持优先补中文编码/委婉、跨语言语用、视频及联合模态安全。

出处：[仓库来源清单](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/sources.csv)、[P031 待审记录](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/audits/P031_AmpleHate_mechanism_pending.md)、[R1–R5 综合目录](https://github.com/YuSun-WK/implicit-content-research/blob/main/02_synthesis/README.md)；新增候选见总索引中的上传表行号。
