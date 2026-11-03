# 研究进度（2026-10-31）

本页以 GitHub main 已定稿阅读卡、论文索引与 2026-10-27 的本机 Zotero 整理审计记录为依据。本次没有再次访问用户本机 Zotero，馆藏状态不是实时同步确认。

## 馆藏与精读完成度

- 根 Collection：**36 篇独立论文（P001–P036）**；原始 `01seed_papers` 子集仍为 **32 篇（P001–P032）**。2026-10-27 本机整理记录核验 38 个 PDF 附件，P004、P009 各保留两份；Zotero 云同步未单独核验。
- **已精读并定稿 21 篇**：P001、P002、P003、P011、P013、P015、P017、P019、P020、P022、P023、P024、P027、P028、P029、P030、P032、P033、P034、P035、P036。阅读卡在 `01_literature/cards/`，相应 PR 已合并。
- **暂缓定稿 1 篇**：P031 AmpleHate，方法公式、公开代码与实验协议存在重大疑点；仅将临时静态审计保存到 `01_literature/audits/`。
- **尚未正式精读 14 篇**，均属于原 Seed；另有 **P031 AmpleHate 暂缓定稿 1 篇**（与未读分开统计）。
- 定稿率：**根 Collection 21/36=58.3%**；**固定 Seed 17/32=53.1%**。定稿只表示文献与静态证据审计完成，不代表代码/模型已复现。

## 已完成的研究阶段

- 第一阶段：P011/P023/P020 正式精读，且 `02_synthesis/` 中的 R1–R5 机制综合已于 2026-10-27 定稿并合并。P020 曾撤销定稿，后经用户重新确认恢复定稿。
- 第二阶段：P032、P024、P030、P029、P028、P019 六篇正式定稿并合并；P031 仅临时审计。
- 第三阶段：R1“跨论文方法机制综合”在聊天中已初步完成，但**尚未正式存入 GitHub**；R2“竞争工作与反面证据审查”进行中，不得误指为第一阶段的 R2 文档。

## Zotero 清理历史与保存边界

- 2026-10-27 本机核验记录显示：恢复 P033–P036 至根 Collection；原 Seed 保留 32 篇；清理 53 个重复文献记录及 2 个无批注附件；P004 的 47+40 条批注与 P009 两种 PDF 字节版本已保留。详见 `00_project/decision_log.md`、`01_literature/batches/zotero_seed_audit.md` 与 `01_literature/zotero_mapping.csv`。
- PR #9 的馆藏更新与最新阅读状态发生冲突，已选择性移植历史记录和 P033–P036 馆藏状态，**没有用 PR #9 的旧版 P019/P024/P028/P029/P030 等行覆盖 main**。

## 尚未关闭

- **P036 StealthGraph（ACL 2026 Main CCF-A）**：KG消融200对200条但实体名称96 vs10个、类别频率与来源样本不同，Self-BLEU32.98 vs38.95不足以证明图结构独立必要；公开主算法双路径状态保留真实存在，但失败回退优先选最新质量合格候选而非最高分；Step7在部分评审API失败时fail-open，四领域报告合计输入3541、保留3163、复核前成功1951、复核后1266（减少685）；SG-Implicit✓经目标模型成功筛选，评审Judge部分重合，成功≠文本有害性金标，ASR选择偏差开放；作者Exp1部分CSV路径未找到，未实物复现。详见 01_literature/cards/P036_StealthGraph.md。

- **P035 EmoBi（ACL 2025 Main CCF-A）**：当前开源模型调用主要为情绪→域映射→隐喻→夸张→联合重判，未提供双向对称分支；Verification 是每条样本自动调用一次LLM，没有独立检错器；2023 ACL Findings 补充的双标签存在类别失衡与单人主标注；公开代码缺少导入/占位路径等问题；原文与代码对应版本、评测划分与F1未实际复现。详见 01_literature/cards/P035_EmoBi.md。

- **P022 SemanticQA（ACL 2026 Main/CCF-A）**：数据源按任务处理、样本/标签口径和语境真实意义可信度待进一步实物审计；当前 sequential-task 代码为单次模型生成两个输出字段而非两次调用；论文Table5使用METEOR，公开main/eval对应组合分数为BERTScore；原子抽取和组合抽取匹配规则不同，不能把所有下降直接归为多阶段错误传播；未本地复现。见 01_literature/cards/P022_SemanticQA.md。

- **P013（ACL 2026 CCF-A）**：评分token的生成后隐藏状态可能混入模型自产评分；静态词典分数不是上下文具体性独立真值；原文跨层 global SVD 与源码逐层10次抽样再中心化 SVD不同；默认basis文件名/形状和steering配置不对齐；SVD符号未显式校正；尚无随机方向/语义保真因果控制与本地复现。详见 01_literature/cards/P013_Concreteness_Figurative_Lens.md。

- **P027 ExPO-HM（ICLR 2026 CCF-A）**：CDE 论文式(9)/(11)权重文字可能重复；实际 binary/FG 熵模式、错误预测中熵区间奖励不同于正文；Figure 2 GRPO G=8 vs公开脚本 n=5；论文后半段细粒度与二分类50/50，脚本后半仅二分类；脚本用FB test_seen的输出做 val，潜在 test-as-val 需核查；解释有用性并非解释忠实性；未本地复现。详见 01_literature/cards/P027_ExPO-HM.md。

- P034 CrossGuard：1390条red-team样本与约202条ImpForge训练样本关系和独立性未证；三奖励公开代码/论文公式不一致；PPO与数据量独立必要性未证；LLaMA-Factory配置max_samples1500 vs论文1616；input-guard与response-ASR异构；未本地运行复现。
- P033 对抗/反事实/循环训练机制与代码差异; 目标测试集兼验证与阈值优化的静态泄漏风险; style毒性代理标签与 true_style 不同; 反向平均F1口径待核验；P015 合成标签条件与真实来源混杂/Min-K%++ 因果不成立及论文/代码分类协议差异；P017 Patchscopes 论文与公开代码的注入层/预测位置差异及 TOCTOU 因果未证；P031 机制/实现矛盾；P029 PPO 使用测试标签调权的静态代码风险；P032/P030/P019 解释监督独立效应与解释忠实性；P028 数据可得性和第二阶段贡献；P024 训练分歧定义与公开代码一致性。
- P020 ACL 正式 PDF 对 arXiv v1 的完整差异核验；P023 新词覆盖和检索实现；P002 正式版差异；P009 出版年份冲突；Zotero 云同步。均不能当作已验证问题解决。
- 尚未执行公开基线的本地 GPU 复现，不宣称已证实任何顶会级创新 Gap。

## 下一步（2026-10-31 第三阶段：方法综合→对抗审计→Kill Test）

**第二批 CCF-A P027→P013→P022→P035→P036 已全部定稿**。停止以完成其余文献数量为目标（14篇仍未正式精读，P031独立暂缓）。不应把第三阶段在聊天中的 R1 草稿说成已上传；第一阶段 02_synthesis/R1–R5 的含义与第三阶段 R1–R3 必须区分。

1. **第三阶段 R1**：从已精读21篇抽取统一方法—任务—标签—数据—证据矩阵，按（词义/语用→目标/有害性、文本→图文、解释/自检→信任）机制分组；只列直接有原文和代码证据的结果。
2. **R2 直接竞品与反面证据**：围绕最可疑的2–3个现象检查 2025–2026 CCF-A及必要安全论文是否已有方法，特别看模态捷径/语境依赖/解释忠实/困难样本选择偏差、已有显性vs隐晦评测；先查重后构思创新。
3. **并行数据与复现审计**：现成可下载带可信GT的公开数据、训练测试划分/近重复、可运行基线，优先现成稳定的检测任务。明确区分 StealthGraph ASR、SemanticQA修辞标签、CrossGuard联合隐含行为与真正有害性标签，不能互相代替。
4. **R3仅保留至多两个可证伪假设**：每个写出对照/负对照/失败门槛、单卡16–20GiB内峰值估计、≤6h kill test、代码改动最小和可发方法型论文空间；若数据/标签不达标先 NO-GO，不追加大规模生成或付费API。
5. **进入实验门槛**：至少一个公开数据集+可运行强基线+冻结或轻量训练流程+可客观评价的现象；先CPU与小样本单卡验证，避免第一步就重跑70B生成/PPO训练。优先考虑图文联合隐含安全检测或语境/修辞引发的安全判断失效，尚无已证实独占创新Gap。

- 2026-10-29：**P017 Doublespeak** 正式精读、方法答疑及代码静态审计完成，用户明确授权定稿合并；Card `01_literature/cards/P017_In_Context_Representation_Hijacking.md`，非 GPU 复现。P015 进入正式精读中。

- 2026-10-29：P015 正式 PDF 31页完整精读及作者脚本静态审计已获用户明确授权定稿合并，卡片 `01_literature/cards/P015_LLMs_in_Sarcasm_Detection.md`；**原作者“识别生成器/语义盲”的因果主张仍保留未证状态**。下一篇 P033 CADET（WWW 2026，CCF-A）开始正式精读。

- 2026-10-30：用户明确授权 P033 CADET 定稿合并，卡片 `01_literature/cards/P033_CADET.md`。已存原论文/公开代码静态审计：四潜变量分支与监督、GRL与正交、论文式(17–19) style flip/cycle实际实现差异、`train,test,test` 验证泄漏风险、标签及F1聚合疑点；**未本地复现、未将因果有效性认定为已证**。P034 CrossGuard ACL 2026 CCF-A 开始精读。

- **2026-10-30：P034 CrossGuard 正式精读定稿并获用户明确指示上传合并**。卡片 `01_literature/cards/P034_CrossGuard.md`：已归档任务定义、三个奖励公式及代码差异、PPO算法与必要性比较、5000/1390/1616/≈202样本口径、FigStep例外、Table1-3/Fig3-7实验基线和指标、ASR不同评测协议、局限与Kill Test；**未训练或复现，不宣称已实现创新Gap**。

- **2026-10-31：P027 ExPO-HM（ICLR 2026，CCF-A）用户授权定稿上传合并**。正式阅读卡 01_literature/cards/P027_ExPO-HM.md 已记录 SFT-PM→GRPO-CL+CDE 的原文与代码机制、具体公式、数据/实验、奖励误差及测试集验证路径。**未GPU复现，不以静态审计断言作者结果无效**。下一篇正式精读 P013 Exploring Concreteness Through a Figurative Lens（ACL 2026 Main CCF-A）。

- **2026-10-31：P013 Exploring Concreteness Through a Figurative Lens（ACL 2026 Main，CCF-A）用户授权正式定稿并合并**。作者正式PDF 20页已读取；层级Probe、DiffMean/跨层SVD、steering及公开代码静态审计已归档；SVD实现差异与未证因果保留。已完成**18/36（50.0%）**，原Seed **16/32（50.0%）**。下一篇 **P022 SemanticQA**（ACL 2026 Main，CCF-A；官方24页PDF已可访问）。

- **2026-10-31：P022 SemanticQA（ACL 2026 Main，CCF-A）用户授权定稿并归档**。正式24页PDF和GitHub静态分析完成；数据任务化处理、Sequential单次双字段生成、Conditional/Overall及METEOR-vs-BERTScore差异均已存卡；不宣称已运行复现。当前 **19/36（52.8%）**，Seed **17/32（53.1%）**。下一篇 **P035 EmoBi**（ACL 2025 Main，CCF-A，官方PDF 11页已实际读取）。

- **2026-10-31：P035 EmoBi（ACL 2025 Main/CCF-A）用户授权定稿**。已完成正式11页PDF和代码静态精读、2023 Findings标注来源追溯、方法/Verification/实验/复现质疑；阅读卡 01_literature/cards/P035_EmoBi.md。进度**20/36（55.6%）**，Seed**17/32（53.1%）**；下篇P036 StealthGraph（ACL 2026 Main/CCF-A），已找到官方PDF。

- **2026-10-31：P036 StealthGraph（ACL 2026 Main/CCF-A）获用户授权定稿合并**。已归档21页原文、两路径算法与开源主要代码、KG去除消融实体96 vs10与Self-BLEU的混杂、Step7质量统计（3541→3163记录，成功1951→1266）、成功子集的筛选偏差及Judge部分重合。只做静态审计，不宣称Gold truth或完整70B复现。正式定稿 **21/36（58.3%）**，固定Seed **17/32（53.1%）**；进入第三阶段方法横向综合/数据可达性/竞品反证，再设计最多2个 ≤6h kill tests。


## 2026-11-02｜第四批多模态联合安全阅读（新增）
- 论文索引已扩展为P001–P041；旧版2026-10-31“馆藏36篇”仅是当时快照，**不能据此认定P037–P041尚未录入**。新增五篇与本机Zotero同步状态不重新推断。
- **P041 SIUO（NAACL 2025 Findings，非CCF-A主会）用户授权正式定稿并合并**：论文任务、269（167人工+102 AI辅助）数据口径、167条公开gen/mcqa不同格式、Safety/Effectiveness与MCQA协议、公开自动评测脚本字段风险均记录于01_literature/cards/P041_SIUO.md。只做静态审计，**未实物完整复现269条、未重新评价15模型**。
- 此前已定稿21篇，加入P041为**22篇**；P037–P040仍待正式精读，当前进行P037 VLSBench（ACL2025 Main/CCF-A）。
- 研究决策：P041是响应安全基准，不能等同隐晦输入二分类金标；后续重点审查P037单模态信息泄漏、P038联合能力、P039风险归因、P040自检对齐。严格先查竞争工作再判断创新空间。

- **2026-11-02 P037 VLSBench（ACL 2025 Main/CCF-A）用户正式授权定稿并合并**：已归档VSIL形式、预训练LlamaGuard3-11B-Vision直接判别未按集微调、2241图文数据分布与一条空instruction、Qwen2-VL仅文本29.5% vs文本加图片描述22.5%的拒答/警告解释、SFT/DPO结果、官方eval.py默认data[:2]和GPT-4o Judge成本问题。见01_literature/cards/P037_VLSBench.md。**未本地复现、未逐图审查**。此前22篇+P037，当前**23篇已正式定稿**。下一篇P038 VLSU（ICLR2026 CCF-A），P039/P040未精读。

- **2026-11-02 P038 VLSU正式定稿**：新增阅读卡01_literature/cards/P038_VLSU.md；正式论文8187行/17组合 vs GitHub CSV实测8159行/25三元组（141条not_sure），S-S-U论文37 vs发布35；官方只有test split，图片是外部URL、尚未实测可达性；未实物复现17个模型或GPT Judge；Harmless/Helpful行为控制提示词原文未完整核实。已定稿累计**24篇**（原23+P038），后续P039 ThinkingGuard、P040 Meerkat-VL。

- **2026-11-03 P039 ThinkingGuard（ACM MM2026/CCF-A）正式定稿**：论文方法、2,800 Unsafe+2,800 Safe反事实设计、训练/测试口径、五步推理、SA-MCTS过程奖励与Max-Q、Trajectory/Step-DPO及消融已归档于01_literature/cards/P039_ThinkingGuard.md；三项未证事项：奖励尺度阈值/Judge代码不公开，Step-DPO未充分同token/数据/类别权重控制，安全/危险配对图片未证仅改变Trigger。SA-MCTS负责搜索而DPO负责训练参数。未GPU复现、未逐图评审。累计**25篇正式定稿**；下一篇P040 Meerkat-VL（ICML2026/CCF-A）。

- **2026-11-03 P040 Meerkat-VL（ICML 2026/CCF-A）经用户授权正式定稿并合并**：阅读卡01_literature/cards/P040_MeerkatVL.md；方法SFT冷启动→NPSV同Actor四维文本自评→DPCA(推理/回答评分一致性惩罚)→GRPO训练已通过公开源码静态审计。评分阶段输入预设用户意图/风险说明，不重传原始图像；README与train.sh的lambda_con=0.3 vs0.2不一致，脚本有路径/引号/数据类配置/接口疑点。论文报告8436条RL数据而HF页面显示8466，实际Parquet未逐条读取；约1000条自验证SFT监督分数的具体来源未查明；**正式论文完整消融表未逐项核验、未GPU复现**。此前25篇+P040，当前**26篇正式定稿**；P041/P037/P038/P039/P040跨论文专题核心五篇均已定稿。建议下一步进入联合风险检测/风险感知/安全响应的机制横向审计、数据可达性和最小Kill Test。
