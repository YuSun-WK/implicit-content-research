# CCF-A 方法论文蓝图

## 标题候选

1. **Cycle-Supervised Learning for Context-Dependent Multimodal Safety Classification**
2. **Learning Joint Safety Decisions from Recombined Image–Text Pairs**
3. **When Safety Depends on the Pair: Identifiable Interaction Contrasts for Vision–Language Classification**

标题 1 为当前候选。标题 3 的 identifiable 只适用于观测图支持上的对比。多类数据门未过时，标题避免承诺分级安全贡献。

## Introduction / Motivation（立项稿）

Vision–language safety decisions often depend on the relationship between an image and a text request. Under the VLSU annotation policy, the same image-only and text-only severity levels can lead to different joint labels. Current benchmarks capture this variation and report errors even when models assign both unimodal labels correctly. Recent detectors address the problem using explanation-guided training, counterfactual examples, and representation interventions. These results motivate evaluating joint predictions under controlled changes to the image–text pair. [VLSU](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf) · [VLSBench](https://aclanthology.org/2025.acl-long.405/) · [ExPO-HM](https://openreview.net/pdf?id=bEejbORUI5) · [ThinkingGuard](https://doi.org/10.1145/3767308.3835707)

A joint label may vary within a unimodal severity stratum because of the relationship between the modalities, differences in their content, or artifacts introduced during data construction. The three labels constrain the severity assigned to each view, while lexical style, visual source, and unobserved context can still predict the joint label. A contrast that reuses only one modality controls that modality's main effect. To control both main effects, the same images and texts must occur in several independently labelled pairings. Prior work on relational OOD detection already uses such cycles to evaluate and train image–text matching models. Safety data introduce a further question about sparse support and multiple policy labels. Our audit of the released VLSU metadata finds that its exact URL–text pairing graph is a forest, which leaves these contrasts unsupported at that identity resolution. The result highlights the relevance of pairing design when interpreting joint classification errors.

We ask whether a lightweight classifier can learn to change its decision with the image–text relationship when valid pair labels supply this information. Building on Cycle OE, we propose to supervise multiclass severity contrasts in the cycle space of the observed pairing graph, including graphs without complete rectangles. On this support, the training signal is invariant to arbitrary additive image-only and text-only logit shifts. The classifier also learns absolute safety levels from standard case labels. We will test whether cycle supervision improves held-out recombinations beyond the same data and compute used for standard classification, multi-task learning, and matched-pair ranking. We will also test whether any advantage transfers to datasets with independently defined safety or hate labels. [Cycle OE](https://arxiv.org/html/2610.23248) · [CMIE](https://aclanthology.org/2026.emnlp-main.2220/) · [EMAP](https://aclanthology.org/2020.emnlp-main.62/) · [MemePIVOT](https://aclanthology.org/2026.findings-emnlp.1329/) · [FBHM](https://aclanthology.org/2026.emnlp-main.1596/)

### 正式投稿需要补上的证据

第一段可以引用作者结果；加入本研究“数据是否提供对照”的新审计时须明确 URL 身份与近重复界限。第二段的替代解释是可行假设，除非一手实验证明，避免将模型失败归因于单一机制。第三段的结果句在至少两个独立测试来源及公平对照均完成后写入具体指标、置信区间与适用范围。外部二元机制阳性、VLSU 三类迁移阴性时，明确拆分两个性质的结论，取消三类机制收益表述。

## Method 论文组织

1. **Problem formulation**。给定 I,T 输出规范定义的 S/B/U，三重标签是部分可用训练监督。定义单侧等级条件、图节点身份、标签与 policy、固定分割和对照支持。
2. **Support-aware contrasts**。陈述观测二部图、关联矩阵、权重、投影公式、环秩定理及对任意相加项不变的命题。展示标准 2×2、缺一角和有六环无矩形三例。给出单环因子和多环协方差形式。
3. **Classifier and optimization**。冻结骨干+投影+低秩联合头，联合 CE 和掩码单模态损失，标签投影作目标。写清楚各梯度、标签来源和划分。解释对同状态和稀有样本的处理。完整公式在[方法设计](05_Recommended_Method_Design.md)。
4. **Training, inference and complexity**。构图与求解只在训练。推理读每条独立 I,T。给训练图求解时间、缓存、可训练参数、显存、单条/吞吐量与校准。
5. **Comparison to prior objectives**。完整小矩形时与差分等价，稀疏有环支持才可检验推广。与 Cycle OE、CMIE、EMAP、Wörtwein、MemePIVOT 区分比较对象和学习目标，引用原工作。给同数据、同参数、同辅助标签和等步数差分。

## 预计英文 Contributions

以下三项是有对应检验的目标，待完成实证后以真实结果改写。

- **We characterize which interaction contrasts are identifiable from observed multimodal safety pairings under arbitrary additive logit shifts, and audit their support for policy-labelled, incomplete graphs of image–text pairings.** 对应图秩、真实语义的端点核验、标签口径和合成正负对照。
- **We introduce a multiclass training objective that matches labelled and predicted contrasts over sparse pairing graphs and accounts for dependence between overlapping cycles, with a single-pair classifier at inference.** 对应公式、四格等价边界、长环与缺边、同数据 MTL/CE/配对排序、参数与预算消融。
- **We evaluate relationship-sensitive classification on held-out recombinations and test whether the learned scoring transfers across independently labelled vision–language safety tasks.** 对应公平迁移 A–D、负例扰动、混淆矩阵、效率与外部规划。只有观察到增益时才在贡献句写入具体数值。

## 四幅图

| 图 | 内容 | 要回答的问题 |
|---|---|---|
| Figure 1 Motivation | 同单侧安全等级的两组真实配对，标签和来源可核验。标出文本提示、视觉证据、固定规范与单侧置信。加 VLSU 两个转移组的计数与组众数参照 | 为何总体分类分数可以掩盖同状态困难子集。原图发布权未确认时用合法的中性示意 |
| Figure 2 Framework | 双冻结编码、三头、图分支训练专用、推理路径及数据分割。沿用[方法结构图](05_Recommended_Method_Design.md) | 训练依赖和部署输入是什么，数据和标签有无泄漏 |
| Figure 3 Mechanism | 2×2 的 +−−+，删一边后 P=0，6 环无四格例；对标准化 class logits 和标签都投影 | 为什么简单相加在该对照下失效，以及稀疏图有什么可测差异 |
| Figure 4 Validation | 纯加性/错线空检，真实闭环方向、保持组 KL、关键/非关键扰动及按组置信区间 | 效果来自对照关系、额外数据还是来源捷径；给分母与失败样本 |

## 五张表

| 表 | 比较、数据与指标 | 欲检验主张与可能负结果 |
|---|---|---|
| Table 1 Main Results | VLSU 协议分别报告 held-out GroupSplit 与固定外部评测。Text/Image-only、CLIP+MLP、Hate-CLIPper、Cross-Attn、UMR、MTL、CSSC，另列开放 VLM。Accuracy、Macro-F1、S/B/U F1、Unsafe 漏判、安全误报与区间 | 分类整体增益与 B 表现。罕见增益而整体负时如实给受益范围，与类权重相同对照 |
| Table 2 Ablation | 相同配对数据与优化预算，移除单侧监督、换加性头、关闭环损失、换 Cycle OE/普通四格/排序、冻结或换骨干、重加权、同参数宽度、训练步数等 | 仅闭环项独立作用，若相同数据 CE 达标，否决机制主张 |
| Table 3 Combination-wise | 原论文 17 组对齐、额外两组及 uncertain 列，给 n、每组正确率/按目标类召回、混淆方向和区间。重点 SSU/SSB/USB/USU/BBU | 两侧标签同、联合标签异时是否改善。小 n 与一致性限制逐组主张 |
| Table 4 Cross-dataset | HM official、Harm-C/Harm-P 或 MAMI；A–D×linear probe/1/5/10/100% 微调，源目标去重，目标官方指标与 Macro-F1/AUROC | 机制的增量迁移和标签效率。若 B/C 和 D 等效，只能归因为通用额外监督或样本 |
| Table 5 Efficiency | 相同硬件、预处理、batch 1/批量，trainable/total 参数、存储、精度、GPU 及 wall clock、显存峰值、p50/p95、吞吐和缓存分开 | 单卡实际成本。附强 VLM 质量/预算参考，较弱但便宜只能主张权衡 |

### 投稿定位

ICLR/NeurIPS/ICML 论文需表现为带可识别条件的通用学习机制，并有跨来源或跨模态任务复验。只有轻微 VLSU 提升时不足。ACL 侧重语言语境、隐晦表达、文本泄漏及规范边界和配对诊断。CVPR 候选需要视觉关系与定位、通用组合强对照。AAAI 或 ACM MM 可着重数据受限和可靠多模态系统，但技术新颖性和强竞品要求仍成立。
