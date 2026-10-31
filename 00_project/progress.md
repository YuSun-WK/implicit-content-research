# 研究进度（2026-10-31）

本页以 GitHub main 已定稿阅读卡、论文索引与 2026-10-27 的本机 Zotero 整理审计记录为依据。本次没有再次访问用户本机 Zotero，馆藏状态不是实时同步确认。

## 馆藏与精读完成度

- 根 Collection：**36 篇独立论文（P001–P036）**；原始 `01seed_papers` 子集仍为 **32 篇（P001–P032）**。2026-10-27 本机整理记录核验 38 个 PDF 附件，P004、P009 各保留两份；Zotero 云同步未单独核验。
- **已精读并定稿 17 篇**：P001、P002、P003、P011、P015、P017、P019、P020、P023、P024、P027、P028、P029、P030、P032、P033、P034。阅读卡在 `01_literature/cards/`，相应 PR 已合并。
- **暂缓定稿 1 篇**：P031 AmpleHate，方法公式、公开代码与实验协议存在重大疑点；仅将临时静态审计保存到 `01_literature/audits/`。
- **尚未正式精读 18 篇**，其中 Seed 内 16 篇、后恢复的 P035–P036 共 2 篇。
- 定稿率：**根 Collection 17/36=47.2%**；**固定 Seed 15/32=46.9%**。定稿只表示文献与静态证据审计完成，不代表代码/模型已复现。

## 已完成的研究阶段

- 第一阶段：P011/P023/P020 正式精读，且 `02_synthesis/` 中的 R1–R5 机制综合已于 2026-10-27 定稿并合并。P020 曾撤销定稿，后经用户重新确认恢复定稿。
- 第二阶段：P032、P024、P030、P029、P028、P019 六篇正式定稿并合并；P031 仅临时审计。
- 第三阶段：R1“跨论文方法机制综合”在聊天中已初步完成，但**尚未正式存入 GitHub**；R2“竞争工作与反面证据审查”进行中，不得误指为第一阶段的 R2 文档。

## Zotero 清理历史与保存边界

- 2026-10-27 本机核验记录显示：恢复 P033–P036 至根 Collection；原 Seed 保留 32 篇；清理 53 个重复文献记录及 2 个无批注附件；P004 的 47+40 条批注与 P009 两种 PDF 字节版本已保留。详见 `00_project/decision_log.md`、`01_literature/batches/zotero_seed_audit.md` 与 `01_literature/zotero_mapping.csv`。
- PR #9 的馆藏更新与最新阅读状态发生冲突，已选择性移植历史记录和 P033–P036 馆藏状态，**没有用 PR #9 的旧版 P019/P024/P028/P029/P030 等行覆盖 main**。

## 尚未关闭

- **P027 ExPO-HM（ICLR 2026 CCF-A）**：CDE 论文式(9)/(11)权重文字可能重复；实际 binary/FG 熵模式、错误预测中熵区间奖励不同于正文；Figure 2 GRPO G=8 vs公开脚本 n=5；论文后半段细粒度与二分类50/50，脚本后半仅二分类；脚本用FB test_seen的输出做 val，潜在 test-as-val 需核查；解释有用性并非解释忠实性；未本地复现。详见 01_literature/cards/P027_ExPO-HM.md。

- P034 CrossGuard：1390条red-team样本与约202条ImpForge训练样本关系和独立性未证；三奖励公开代码/论文公式不一致；PPO与数据量独立必要性未证；LLaMA-Factory配置max_samples1500 vs论文1616；input-guard与response-ASR异构；未本地运行复现。
- P033 对抗/反事实/循环训练机制与代码差异; 目标测试集兼验证与阈值优化的静态泄漏风险; style毒性代理标签与 true_style 不同; 反向平均F1口径待核验；P015 合成标签条件与真实来源混杂/Min-K%++ 因果不成立及论文/代码分类协议差异；P017 Patchscopes 论文与公开代码的注入层/预测位置差异及 TOCTOU 因果未证；P031 机制/实现矛盾；P029 PPO 使用测试标签调权的静态代码风险；P032/P030/P019 解释监督独立效应与解释忠实性；P028 数据可得性和第二阶段贡献；P024 训练分歧定义与公开代码一致性。
- P020 ACL 正式 PDF 对 arXiv v1 的完整差异核验；P023 新词覆盖和检索实现；P002 正式版差异；P009 出版年份冲突；Zotero 云同步。均不能当作已验证问题解决。
- 尚未执行公开基线的本地 GPU 复现，不宣称已证实任何顶会级创新 Gap。

## 下一步

按已确认的第二批未完成 CCF-A 清单继续核心精读：**P013（ACL 2026 Main）→ P022（ACL 2026 Main）→ P035（ACL 2025 Main）→ P036（ACL 2026 Main）**。P027（ICLR 2026）于2026-10-31定稿；四篇待读完成后优先审查解释忠实性、表征干预、隐晦语义/图文模态依赖的真正竞争工作并设计≤6h Kill Test。独立多模态图文隐晦专题（VLSU/Meerkat-VL/VLSBench）仍保留，不再替代原计划的 CCF-A 读完优先序列。

- 2026-10-29：**P017 Doublespeak** 正式精读、方法答疑及代码静态审计完成，用户明确授权定稿合并；Card `01_literature/cards/P017_In_Context_Representation_Hijacking.md`，非 GPU 复现。P015 进入正式精读中。

- 2026-10-29：P015 正式 PDF 31页完整精读及作者脚本静态审计已获用户明确授权定稿合并，卡片 `01_literature/cards/P015_LLMs_in_Sarcasm_Detection.md`；**原作者“识别生成器/语义盲”的因果主张仍保留未证状态**。下一篇 P033 CADET（WWW 2026，CCF-A）开始正式精读。

- 2026-10-30：用户明确授权 P033 CADET 定稿合并，卡片 `01_literature/cards/P033_CADET.md`。已存原论文/公开代码静态审计：四潜变量分支与监督、GRL与正交、论文式(17–19) style flip/cycle实际实现差异、`train,test,test` 验证泄漏风险、标签及F1聚合疑点；**未本地复现、未将因果有效性认定为已证**。P034 CrossGuard ACL 2026 CCF-A 开始精读。

- **2026-10-30：P034 CrossGuard 正式精读定稿并获用户明确指示上传合并**。卡片 `01_literature/cards/P034_CrossGuard.md`：已归档任务定义、三个奖励公式及代码差异、PPO算法与必要性比较、5000/1390/1616/≈202样本口径、FigStep例外、Table1-3/Fig3-7实验基线和指标、ASR不同评测协议、局限与Kill Test；**未训练或复现，不宣称已实现创新Gap**。

- **2026-10-31：P027 ExPO-HM（ICLR 2026，CCF-A）用户授权定稿上传合并**。正式阅读卡 01_literature/cards/P027_ExPO-HM.md 已记录 SFT-PM→GRPO-CL+CDE 的原文与代码机制、具体公式、数据/实验、奖励误差及测试集验证路径。**未GPU复现，不以静态审计断言作者结果无效**。下一篇正式精读 P013 Exploring Concreteness Through a Figurative Lens（ACL 2026 Main CCF-A）。
