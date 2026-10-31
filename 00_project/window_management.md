# 科研窗口与阶段管理规范

> 项目级长期规则。2026-10-26 首次写入；与单篇论文卡片分开保存。

## 1. 窗口划分与容量
- 按**研究主题或研究阶段**划分，而不是随机开窗；优先每个精读窗口处理 3–6 篇高度相关论文。
- 从论文阅读转到横向综合、Gap 审计、迁移审计、Kill Test 或工程复现时，原则上新开对应专题窗口。
- 若上下文过长、讨论重复、单次任务过大或引用混乱，应主动提醒切换，而不是等待用户判断。

## 2. 研究流程主动管理
- 每次进入新任务时，主动检查是否重复检索/重复分析，是否能与已有成果复用，是否有可并行的独立任务。
- 明确哪些任务具有依赖、哪些可推迟；阅读阶段不要提前批量生成缺证据的 Gap 或 Idea。
- 识别过度阅读、反复完善基础设施和任务范围漂移；有足够证据支撑关键假设时，建议转向最小可证伪实验，而非无限阅读。
- 结合资源约束：共享 4090/4090D、单卡计划峰值 16–20 GiB、快速 Kill Test ≤6h、公开数据与代码、Codex/Cursor；无付费 API、从零基础模型训练或大规模自建标注的强制依赖。
- 适时提示检查阅读顺序，优先读直接回答当前问题的原始研究，再读相关机制。
- 遇到原文证据不足、论文版本差异或标签/评测不一致必须标记，不得悄然覆盖。

## 3. 卡片审定与跨窗口依据
- 阶段 A：完整讨论并答疑；阶段 B：用户确认后写 Markdown 卡、更新 papers/sources/progress，并以 PR 待审。
- 用户在当前聊天确认“定稿”即授权准备对应阅读卡及 PR；未经明确要求，不主动合并 PR 到 main。
- 新窗口引用 **GitHub 上已确认且合并的内容** 为优先依据；未合并 PR 应清楚标记“待审”。
- 不覆盖已核验结论；修订注明依据、版本和状态。不得重复 Paper ID。
- Github 不放 PDF、模型权重、Zotero 数据库或本地绝对路径。

## 4. 窗口切换前检查清单
1. 核对该窗口重要结论的原始证据与修订记录。
2. 检查相关卡片/索引是否已写入 PR 或合并 main；未完成时明确写出待办，不假装已保存。
3. 给下一窗口生成交接 Prompt：研究目标、仓库与路径、已完成论文/任务、已经核实的结论、待解决问题、所需原文及当前 PR 状态。
4. 保持同一主题的证据链，避免将模糊聊天记忆当作已核验成果。

## 5. 当前研究进度与阅读序列（2026-10-29 更新）
- 已分析并定稿：P001–P003、P011、P023、P020。P020 的定稿是对此前撤销状态的**重新授权**，不能把正式 PDF 差异审计冒充已完成。
- 第一轮机制整合 R1–R5 已定稿，报告见 `02_synthesis/README.md`；其中对 P020 递归收益、P023 词典覆盖和统一 Pipeline 的结论均保留证据边界。
- 第二阶段论文精读：**P032 (ImpCon) 已于 2026-10-27 定稿并归档**，阅读卡 `01_literature/cards/P032_ImpCon.md`。**P031 (AmpleHate) 经机制专项静态审计发现原文公式/公开实现/训练-测试协议存在重大疑点，用户于 2026-10-27 决定暂缓定稿**；仅保存临时审计记录 `01_literature/audits/P031_AmpleHate_mechanism_pending.md`，不标为已分析，不作为可靠目标关系建模证据，未本地复现。**P024 (CONELA) 已于 2026-10-27 定稿**，阅读卡 01_literature/cards/P024_CONELA.md（人工分歧/代码差异仍开放）。**P030 (SMARTER) 已于 2026-10-27 用户确认定稿**，阅读卡 01_literature/cards/P030_SMARTER.md；前置 HateCOT 与 seed explanations、DPO标签偏好和解释忠实性、未复现/成本均明确留存。**P029（RV-HATE）已于 2026-10-28 获用户授权定稿并合并准备**，详见 `01_literature/cards/P029_RV-HATE.md`。必须携带开放问题：公开 `ppo_eval.py` 用测试集标签优化权重；M0 聚类代表局部/全局索引问题；M1 目标标记训练/测试管线错配；M3 代码执行阻碍；PPO 相对网格/随机搜索的独立必要性尚未证实。上述为静态审计（未复现），不能推断作者论文结果必然无效，不能把 bug 当创新点。**P028（ImpliHateVid）已于 2026-10-28 由用户授权定稿**，阅读卡 `01_literature/cards/P028_ImpliHateVid.md`；开放问题包括两阶段 CL 独立贡献未证实、跨模态隐含意义理解未证实、原始视频需申请且未实物核验、HateMM划分数量不一致、公开 notebook 无完整训练脚本。与 P029 的代码/指标问题分开记录。**P019（V-FLUTE）于2026-10-29获用户授权定稿，正式阅读卡 `01_literature/cards/P019_V-FLUTE.md` 已准备合并**：原文正式 PDF §3–5 与附录 A–K 复核完成。保留来源/标签/图像级划分可能产生捷径、参考解释未必忠实、F1@53 阈值由测试子集人工评价校准、Appendix D epochs 不一致和正文21/附录文字20指令冲突；Appendix H GPT-4o 5-shot F1@0=79.42（高于正文最高微调LLaVA 74.91），Appendix J 解释多任务 F1=80.85→83.26(p<0.1)证据弱，不能当已证明因果收益。此窗精读任务结束，下一窗口转向跨论文方法综合/创新空间反向审计。
- **本批第二阶段精读收束**：P032、P024、P030、P029、P028、P019 均已定稿（各卡内未关闭问题不能抹除）；P031 AmpleHate 暂缓定稿，临时审计保留。P017 表示劫持已于 2026-10-29 完成正式精读并经用户授权定稿；论文与代码的 Patchscopes 实验协议不一致及因果机制未证均保留。**下一阶段应独立开窗做机制/数据/监督/训练/评测横向矩阵、必要性反向审稿、低成本 Kill Test 排序**，先审计现有竞品而不是直接编造 Gap。
- 研究仍处于文献、方法对比与可复现性建设阶段，未形成经竞品反证的最终 Gap 或论文 Idea。读完首批四篇后主动评估是否转入最小可证伪实验。

## 6. 2026-10-29 进度口径及第三阶段交接
- 2026-10-27 的 Zotero 整理历史已选择性整合到最新阅读索引：根 Collection 为 36 篇（P001–P036），固定 Seed 仍为 32 篇（P001–P032）。原先“32 篇当前全部馆藏”的陈述只适用于整理前的历史快照。
- 当前研究状态以 `00_project/progress.md` 为准（2026-10-30 更新：16 篇定稿、P031 暂缓、根 Collection 的19篇未正式精读）。上述已定稿包括第二阶段 P019、P024、P028、P029、P030、P032；不能被 2026-10-27 的旧版索引回滚。
- 第三阶段 R1 跨论文机制综合仅在聊天中初步完成，**尚未归档 GitHub**；接续 R2 竞争工作/反面证据审计。**勿将第一阶段的 `02_synthesis/R2_P011_P023_P020_Method_Comparison.md` 误认作第三阶段 R2**。

## 7. P017 定稿与 P015 开始（2026-10-29）
- P017: `01_literature/cards/P017_In_Context_Representation_Hijacking.md`；ACL 2026 Main / CCF-A。静态审计发现 Patchscopes 论文 vs 公开代码注入层、解释提示与 logits 位置不一致；TOCTOU、superposition 非因果证明；未经本地复现。
- P015: `LLMs in Sarcasm Detection? It’s elementary! (Or is it?)`；ACL 2026 Main / CCF-A；DOI 10.18653/v1/2026.acl-long.1346；下一篇精读，需先核实真实/合成数据构建、split、捷径分析及因果干预，不由摘要预判结论；尚未定稿。
- **教学/精读解释偏好（用户明确确认）**：说明原理时依次给 **抽象概念（是什么/为什么）→ 实际实现（输入/张量/逐步操作/公式/代码）→ 完整简单例子**；不得用“把向量注入Prompt”这样省略工程细节的表述取代解释。明确区分论文声称、公开代码实际做法与推测。

## 8. P015 定稿与 P033 进入精读（2026-10-29）
- P015 ACL 2026 CCF-A 的正式 PDF 31页、Tables/Figures/Appendix与公开代码静态审计已定稿：`01_literature/cards/P015_LLMs_in_Sarcasm_Detection.md`。关键限制：零样本真人/合成差距≠训练泛化失败；先指定标签再生成文本导致标签条件风格混杂；识别生成器身份不足以区分同一生成器两类样本；Min-K%++/UMAP/LIME/Attention/ablation/occlusion无法单独证明因果捷径或语义盲。代码预测、抽样、token occlusion、Table1与Table3口径差异保留。未经 GPU复现。
- 下一篇 P033 CADET：`Causality Guided Representation Learning for Cross-Style Hate Speech Detection`，WWW 2026（CCF-A），DOI 10.1145/3774904.3792669；正式全文精读关注四类因素 DAG/identifiability、潜变量解耦、对抗 confounder、风格干预及反事实一致性、真实 GT/划分、复现成本；官方 github Shu-Wan/cadet。未定稿。

## 9. P033 定稿与 P034 进入精读（2026-10-30）
- P033 CADET（WWW 2026 CCF-A）获用户明确授权“定稿合并”；正式卡 `01_literature/cards/P033_CADET.md`。切勿因定稿忽略关键未证项：潜变量因果身份、style预测标签与true_style不一致、`train,test,test`用目标风格测试集做验证/阈值/选模型、式(17–19)反事实与cycle数学/实现错配、随机采样一致性替代真实style干预、式(12) `lambda_u`实现不一致、表2均值汇总不一致；均为静态审计，**尚无本地实验**。
- 下一篇 **P034 CrossGuard**（ACL 2026 Main CCF-A）：DOI 10.18653/v1/2026.acl-long.1178；ACL正式页面 https://aclanthology.org/2026.acl-long.1178/；官方 https://github.com/ZhangXu0963/CrossGuard；先审计 text/image单独无害联合表达恶意的定义、ImpForge RL奖励及生成标签、LoRA模型训练和 guardrail安全/正常样本评估； **P034 未定稿**。下一篇跨NLP与VLM，必要时新开专窗。

## 10. P034 定稿与多模态隐晦检测专题交接（2026-10-30）
- **P034 CrossGuard（ACL 2026 Main，CCF-A）用户授权定稿合并**：`01_literature/cards/P034_CrossGuard.md`。必须继承：三奖励正式论文 vs 公开代码的差异；5000 RL初始文本、1390 ImpForge红队评估样本、1616混合训练样本（其中12.5%≈202联合隐含类型）**不能混写**；论文没有证据确定≈202是否取自1390或两组是否独立；PPO不具同预算独立必要性证明；FigStep数据消融略退化；在线MLLM/离线MLLM/guardrail用不同ASR判据；SFT训练配置max_samples=1500 vs论文本体1616；全部仅静态审计。
- 研究计划已从继续单篇P034阅读切换为**单独的新窗口：多模态图文隐晦信息检测领域审计**。先核验 VLSU（ICLR 2026 CCF-A）、Meerkat-VL（ICML 2026 CCF-A）、VLSBench（ACL 2025 Main CCF-A）及SIUO（NAACL 2025 Findings，不按CCF-A主会统计）；优先数据标签可信/模态依赖评测/竞品查重，再定是否需要Kill Test。不要重做 CrossGuard 的多GPU PPO，也不要自动认定“PPO改GRPO、新数据+LoRA”有足够创新。

## 11. P027 定稿及第二批 CCF-A 继续阅读（2026-10-31）
- 用户已明确授权 P027 **ExPO-HM**（ICLR 2026，CCF-A）定稿、上传、合并，正式卡片在 01_literature/cards/P027_ExPO-HM.md。模型 Qwen2.5-VL；SFT-PM 仅细粒度标签 CE，GRPO-CL 课程，CDE 以预测正确性与决策熵组合成奖励。相关公开实现与论文存在课程第二阶段配比、G数、熵模式/奖励公式、测试集作验证路径的静态差异；解释一致性与忠实性不能混为一谈；未运行GPU。
- 读后正式完成计数 **17/36（47.2%）**，Seed **15/32（46.9%）**；P031 暂缓，18篇未正式精读。
- **约定的第二批 CCF-A 阅读顺序必须保留**：P027 [已定稿] → **P013** Exploring Concreteness Through a Figurative Lens（ACL 2026 Main，DOI 10.18653/v1/2026.acl-long.705） → **P022** SemanticQA → **P035** Hyperbole/Metaphor → **P036** StealthGraph。P013 在进入精读前须核对正式 PDF 和作者代码，已讨论过局部概念但**未形成正式精读卡**；不要误判为已读。
- 多模态隐晦专题 VLSU/Meerkat-VL/VLSBench 与上述第二批阅读并行存在，不覆盖此次明确的顺序。

## 12. P013定稿及P022进入精读（2026-10-31）
- P013 Exploring Concreteness Through a Figurative Lens（ACL 2026 Main CCF-A）已经用户授权定稿合并；正式卡 01_literature/cards/P013_Concreteness_Figurative_Lens.md。关注 Concreteness评分token提取的是**生成后重喂的token表示**，不是预测该token前的隐藏向量；论文跨层global SVD vs开源逐层重复抽样+中心化SVD不一致，可能消去平均差异；正负方向不校准、steering参数/文件接口不匹配、缺随机方向控制；仅静态审计没有GPU复现。
- 正式定稿 **18/36**，Seed **16/32**；P031继续暂缓，17篇尚未精读。第二批 CCF-A 余下**P022 → P035 → P036**。P022 ACL 2026 Main正式PDF https://aclanthology.org/2026.acl-long.210.pdf 已实际读取，可直接进行全文精读；若后续PDF不可访问则须询问用户上传，不得依靠摘要冒充全文。精读教学先总体后细节，解释每个任务标签/数据构造/算法公式/实验和局限。

## 13. P022定稿与P035正式精读（2026-10-31）
- P022 Revisiting a Pain in the Neck / SemanticQA（ACL 2026 Main CCF-A）已获用户明确授权定稿合并；正式卡 01_literature/cards/P022_SemanticQA.md。任务数据适配而非统一真值；六种 Sequential 是一个 Prompt 一次 query_llm 同时生成两个字段，非独立两轮 Pipeline；组合评价正文Table5使用METEOR，当前开源eval.py用BERTScore；原子/组合抽取的exact-match规则差异、标签疑点、数据数量口径保留。**尚未训练/运行复现。**
- 已精读**19/36（52.8%）**、Seed **17/32（53.1%）**，P031仍暂缓，剩余16篇。原定第二批CCF-A只余 **P035 → P036**。
- P035 Enhancing Hyperbole and Metaphor Detection with Their Bidirectional Dynamic Interaction and Emotion Knowledge（ACL 2025 Main CCF-A），官方PDF https://aclanthology.org/2025.acl-long.23.pdf **11页已实际阅读**；正式码 https://github.com/ZhengL00/EmoBi；从框架、emotion analysis、emotion-guided domain mapping、bidirectional dynamic interaction、verification、四数据集协议和消融开始读，讲解按“全局→具体、概念→公式→Prompt/代码→例子→结果”进行；若任何原始材料不可读取需明确告知用户。

## 14. P035定稿并进入P036（2026-10-31）
- P035 EmoBi（ACL 2025 Main CCF-A）用户明确授权定稿上传合并。卡 01_literature/cards/P035_EmoBi.md：四阶段情绪→域映射→双修辞关联→最终联合LLM自检；公开代码实际上隐喻先行→夸张→联合重判，没有完全对称hyperbole-first分支；2023 ACL Findings 既有HYPO/HYPO-L/TroFi/LCC双标签及标注质量证据；当前仓库运行导入/数据路径错误，未本地训练/推理复现。Verification加分不等于可靠纠错，保留同预算消融问题。
- 当前**20/36（55.6%）**，Seed**17/32（53.1%）**；P031继续暂缓，15篇尚未正式精读。第二批CCF-A最后一篇 **P036 StealthGraph**（ACL 2026 Main，DOI 10.18653/v1/2026.acl-long.295；PDF https://aclanthology.org/2026.acl-long.295.pdf；code https://github.com/ZJUIDG-AIVA/StealthGraph）。正式精读须核对任务为**隐晦有害提示的生成、测试模型安全性**，不能混同一般隐晦信息分类检测；始终先概览后讲公式、数据生成/验证、实验与代码，读不到原始PDF要让用户提供。

## 15. P036定稿与第三阶段计划（2026-10-31）
- 用户明确授权 P036 StealthGraph（ACL 2026 Main/CCF-A）定稿并合并。正式卡 01_literature/cards/P036_StealthGraph.md。现象：Wikidata知识图谱帮助生成不同实体的专业风险请求，双路径隐晦改写+Gemini质量审查+LLM响应ASR；**KG200条vs无KG200条的实体名称数96 vs10，故Self-BLEU改善有实体覆盖混杂，不能宣称图边独立因果**；代码质量失败后选择最近合格候选而非全局最高质量；Step7存在部分fail-open并下调模型成功标签。成功改写子集SG-Implicit✓的模型ASR是选择后的行为评测，不是隐晦有害文本人工金标。
- **最新定稿21/36（58.3%）、Seed17/32（53.1%）**；P031 AmpleHate 独立暂缓、其他14篇未正式精读。第二批CCF-A阅读 P027/P013/P022/P035/P036 全部完成；**停止自动展开下一批阅读**，优先单独开窗做第三阶段：R1已读论文的机制—数据—真值—训练—评测对比矩阵→R2直接竞品和反证→R3筛选至多2个数据可达/单卡≤6h的假设及最低成本Kill Test。新窗口需把正式论文PDF与公开代码查实，不得把聊天初稿冒充已入GitHub；并行数据可达性核验与竞品查重。多模态图文隐晦主题（CrossGuard/P019/VLSU/Meerkat-VL）优先但先验证数据和真实双模态依赖。
