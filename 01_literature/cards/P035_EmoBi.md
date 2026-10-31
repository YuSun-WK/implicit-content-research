# P035 — Enhancing Hyperbole and Metaphor Detection with Their Bidirectional Dynamic Interaction and Emotion Knowledge

**状态：2026-10-31 用户授权正式定稿。** 完成正式论文与公开源码静态精读；未在本地进行训练、推理或数值复现。关键不一致与未证事项不因定稿而关闭。

## 1. 基本信息与材料
- 作者：Li Zheng, Sihang Wang, Hao Fei, Zuquan Peng, Fei Li, Jianming Fu, Chong Teng, Donghong Ji。会议 **ACL 2025 Main（CCF-A）**，489–499，DOI 10.18653/v1/2025.acl-long.23。
- 正式 PDF：https://aclanthology.org/2025.acl-long.23.pdf（11页）；论文：https://aclanthology.org/2025.acl-long.23/；官方代码：https://github.com/ZhengL00/EmoBi。
- 对照联合标注原论文：A Match Made in Heaven: A Multi-task Framework for Hyperbole and Metaphor Detection（**ACL 2023 Findings，并非CCF-A主会**）https://aclanthology.org/2023.findings-acl.26/；数据：https://github.com/abisekrk/multitask_hyperbole_metaphor_detection/tree/main/data 。

## 2. 任务/贡献
- 输入英文句子 x，预测两个非互斥二元标签：Hyperbole 0/1，Metaphor 0/1；同句两者可共存。识别修辞并不等于隐晦有害检测。
- 作者方法 **EmoBi** 把情绪分析、隐喻源域-目标域映射、双向任务交互、自我核验整合到 LLM Prompt Pipeline。**没有新建Transformer、没有训练奖励模型、没有使用PPO/DPO/GRPO**。
- 动机：修辞表达隐含情绪与跨域映射；隐喻线索有望帮助识别夸张，反之亦然，需区分机制假设与论文已证明事实。

## 3. 整体框架与真实输入输出
1. Emotion Analysis：LLM 接收原句输出自然语言情绪分析 e，代码 model.py 函数 analyze_emo，使用 Ollama。
2. Domain Mapping：LLM 接收原句和 e，输出 source domain / target domain 和选择理由，函数 target_source_domains；概念源域是用来类比的对象，目标域是真正欲描述的对象。
3. Interaction：论文 §3.5 与 Figure 2 说明 metaphor→hyperbole 和 hyperbole→metaphor 相互促进，通过 LLM 生成标签/解释作为后续 Prompt 条件，并非跨模型隐藏状态 Attention。
4. Verification：把前述情绪、源域/目标域、两个标签及其解释，再请求 LLM 一次，同时重新判断两个标签，无外部 gold 或独立真值判别器。

## 4. 论文“Bidirectional”与源码调用顺序的差异
- 源码 main.py 的固定顺序为 analyze_emo → target_source_domains → metaphor_learning → hyperbole_learning → hyperbole_metaphor。
- 第四步 hyperbole_learning **明确接收已生成 metaphor_judgment**，但未收到 metaphor_reason 全文；没有对应的独立 Hyperbole-first → Metaphor-second 分支。两种标签及解释在最后 hyperbole_metaphor 被整体传入用于重判。
- 因此当前公开实现更贴切地说是“隐喻先行→夸张后行→末尾联合重判”，并非两个完全对称、反复迭代的双向循环。不能据此直接断言论文实际实验使用的源码版本等同当前main。

## 5. Verification 细节与因果证据边界
- 当前代码对每条样本都运行一次联合核验，没有先行错误检测门控，没有ground truth输入；只是让同一个LLM利用更多上下文重新预测两个二元标签。
- 论文Table2：去掉核验后多个数据集两任务F1下降约1.2–1.9个百分点，支持“添加核验阶段提高最终分数”，**不证明**它专门识别并纠正错误，也不能排除更多token/额外LLM调用带来的收益。
- 真正审计应报告 C→C、C→E、E→C、E→E 预测转移及 CorrectionRate、CorruptionRate；与同调用预算的直接重复分类、自一致性、打乱理由/标签做比较。

## 6. 数据与标签血缘
- 本文沿用 **2023 ACL Findings** 联合双标签资源，不是 2025 文中重新大规模标注四个数据集。
- HYPO、HYPO-L 原有 Hyperbole 标签，2023工作新增 Metaphor 标签；TroFi、LCC 原有 Metaphor 标签，2023工作新增 Hyperbole 标签。
- 2023报告规模分别 HYPO 1418、HYPO-L 3326、TroFi 3838、LCC 7542。**这些是联合标注资源数量，不等于 P035 各最终评测 split。**
- 2023新增标签由四名英语流利标注员承担（三名硕士研究生及一名语言学硕士）；正式样本通常单人主标注，预标注 Fleiss κ=0.674，并做抽样质量检查。不能认为每条标签经多人数一致投票。
- 标签四组合统计（both/only hyperbole/only metaphor/neither）：HYPO 515/194/107/602；HYPO-L 237/770/19/2200；TroFi 209/235/1710/1684；LCC 615/144/3187/3596。双任务共现/标签分布不均可能形成捷径。
- 已静态检查源仓库数据文件 hypo.csv、hypo-l.csv、trofi.csv、lcc.csv 及 Trofi_Label_Balanced.csv、LCC_Label_Balanced.csv（部分实际记录包含 Sentence,Hyperbole,Metaphor）。**P035 实际是否使用平衡子集、如何划分和选择checkpoint 尚未闭合**。
- 原始 TroFi/LCC 可能采用词项/句子层混合标注口径，转换为句级双标签需另审计；不能直接迁移为 implicit hate 数据。

## 7. 论文结果与基线
- Table1 EmoBi F1（Hyperbole/Metaphor）：HYPO 90.8/84.5；HYPO-L 79.3/80.3；LCC 84.9/91.3；TroFi 84.2/76.6。
- MTL-F-RoBERTa：HYPO 88.1/78.7、HYPO-L 68.7/57.2、LCC 65.9/80.5、TroFi 56.1/57.3。摘要对比所谓 TroFi Hyperbole +28.1%、HYPO-L Metaphor +23.1% 对应表格**百分点差**而不是相对提升率。
- 普通 CoT 与 EmoBi 的增量更小，如 TroFi Hyperbole 78.5 → 84.2（+5.7个百分点），强基线选择会影响方法叙述。
- Ablation 去情绪、域映射、互动、核验都会造成下降，但没有同预算额外Prompt/额外推理次数因果对照，不可声称都已证明正确理解。

## 8. 当前公开代码复现风险
- config.py 指定 MODEL_NAME=llama3:8b；model.py 用 Ollama 本地推理，temperature=0。可能无需付费API，但**不是已验证单卡可运行/可在6小时内复现**。
- main.py 中 data_dir/input_name 仍为占位值，且使用 pd 但未显式导入 pandas；config.py 使用 datasets 但未导入；README 要求 requirements.txt，实际仓库文件为 requirement.txt。
- model.py 的 metaphor_learning()/hyperbole_learning() 调用 safe_parse_int 但未在全局定义/导入；最后 hyperbole_metaphor() 内存在同名局部函数，不能供前面函数调用；该局部函数使用 re 但当前文件未导入 re。属于源码静态级可识别的运行故障。
- 仓库另有传统多任务分类/encoder类，不可把未进入LLM主调用链的类误认为本文核心 EmoBi 的训练模块。
- 未核查当前main对应发表实验的具体commit、数据预处理、真实验证集划分与最终checkpoint。

## 9. 审稿判断
- 创新是结构化语义信息与双修辞交互的 prompt orchestration，而不是新联合数据集/新训练结构；已有2023 Findings论文证明隐喻与夸张联合检测的主题并非本文首创。
- Verification改善F1 ≠可靠检错；情绪/源域文本生成 ≠人工验证语用真值；双向命名 ≠当前代码完全对称。
- 执行性能、词汇类别统计先验、同句双标签关联、更多推理预算可能造成混杂。保持作者结果与审计推断分开。

## 10. 项目关联与低成本Kill Test
- 可能借鉴：隐晦检测中“发现修辞→恢复目标含义→判断有害意图”的操作分解，但不能把修辞标签直接作为有害标签，也不能仅把“增加CoT/情绪分析”视为CCF-A方法创新。
- 低成本优先：修复独立调用/导入/数据路径和解析；小规模公开 CSV 四标签分组；对比 1-pass、metaphor-first、hyperbole-first、joint recheck 与等token等调用次数对照；记录 C→E/E→C；不生成新的大标注数据。
- 用户硬约束：公开数据/可信真值、复用代码，单卡共享显存16–20GiB、6h以内先做Kill Test、避免付费API。不能把作者完整复现难度当作已解决。

## 11. 未关闭问题
- 公开单向序列与论文“双向”版本差异是否存在别的实现；
- 四套数据实物、平衡子集与划分；
- 解释/域映射的真实性及人工样本质量；
- Verification 的额外计算对照与真实纠错能力；
- 原论文统计值的独立运行复现。
**这些作为定稿后的开放问题长期保留。**

## 12. 下一篇交接
- **P035 于2026-10-31用户授权定稿**，索引和进度需同步。
- 下一篇 **P036 StealthGraph: Exposing Domain-Specific Risks in LLMs through Knowledge-Graph-Guided Harmful Prompt Generation**，ACL 2026 Main（CCF-A），正式PDF https://aclanthology.org/2026.acl-long.295.pdf ，作者代码 https://github.com/ZJUIDG-AIVA/StealthGraph 。
- P036是**领域隐含有害提示的生成与红队评测**，不是隐晦文本检测器；优先核验 graph-grounded constraints→explicit harmful prompt→direct/context obfuscation→质量/安全评估、原始标签可靠性、数据发布、安全伦理和低成本复现；严格先总体后细节，读不到原文则问用户。
