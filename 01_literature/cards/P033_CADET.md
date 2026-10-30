# P033｜CADET — Causality Guided Representation Learning for Cross-Style Hate Speech Detection

> **用户于 2026-10-30 授权“定稿合并”；状态：文献精读与公开代码静态审计定稿，**不是**论文因果有效性认证、实验复现或审计风险关闭。公开数据内容可能涉及冒犯性语言，引用时需遵守数据协议。**

## 1｜书目信息与来源
- **Chengshuai Zhao; Shu Wan; Paras Sheth; Karan Patwa; K. Selçuk Candan; Huan Liu**. *Causality Guided Representation Learning for Cross-Style Hate Speech Detection*. **The Web Conference (WWW 2026，正式主会会议论文，CCF-A)**，pp. 1819–1829；DOI **10.1145/3774904.3792669**。
- 正式出版：https://doi.org/10.1145/3774904.3792669 ；可阅读的正式会议信息 arXiv v2 HTML：https://arxiv.org/html/2510.07707v2 （2026-02-03）。此处 **未核对 ACM 排版 PDF 与 arXiv v2 的逐字/逐表差异**。
- 官方代码：https://github.com/Shu-Wan/cadet ；官方数据：https://huggingface.co/datasets/Shuwan/cadet-datasets ；方法参考：仓库 `docs/CADET.md` 与 `src/cadet/models/cadet.py` / `src/cadet/training/cadet_trainer.py`。

## 2｜任务边界与研究问题
- **Cross-style hate speech detection**，显式训练 → 隐式测试及反方向；训练阶段可获得有害二分类标签、风格标签、部分目标群体标签。**这不是 open-world coded words 或无上下文事实核验**。
- 与通用 implicit content 方向相关，但“隐式”主要取作者二元 style 协议；编码语言/含义语境/修辞并未分别构成可归因任务。
- Authors' causal story（§3）：环境 (U) 影响动机 (M)、目标 (T)、风格 (S)，三者形成文本 (X)，标签 (Y) 与动机/环境有关；以此指导表示模型而非从观测数据真实识别出唯一 DAG。

## 3｜核心贡献（作者主张 vs 独立判断）
1. 提出文本生成的四因素因果图；**建模先验**，不等于 DAG 已被识别。
2. 提出 **CADET** 多损失表示解耦模型（RoBERTa+四潜变量分支+BART重建+GRL+orthogonality+counterfactual）。
3. 公开 IE-HSC 数据组合与显式↔隐式迁移评测，报告显式→隐式平均 F1 0.815、隐式→显式 0.885，摘要称相对强基线提升13%；**报告值未运行复核**。
4. 论文 §5.5 GPT-4 改写形成 375 条人工筛选的配对样本（原始抽样1000条），在其协议下报告 CADET Macro-F1 0.76；需区分这组额外生成/人工验证测试与 IE-HSC 原始标签。

## 4｜方法从输入到变量的逐步实现（§4.2-4.3；代码已静态核验）
- RoBERTa Encoder 输出 `h=last_hidden_state[:,0,:]`，一般为 `[B,768]`，不是把 h 简单切四块，而是四个可训练头由**同一个 h**推断：
  - **U**：`fc_mu_u(h),fc_logvar_u(h)`，VAE 高斯重参数化 (z_u=\mu_u+\sigma_u\odot\epsilon\)，256维；**无真实环境监督标签**。
  - **M**：均值/方差头采样 `zm_raw`（768维），`purify_m(cat(zm_raw,zu))` 产生 `zm`。这只是MLP整合而非算法天然“去除环境”。
  - **T**：目标群体 logits（维度为数据类别数）与 `zu` 拼接净化，再 `GumbelSoftmax` 得 `zt_onehot`。
  - **S**：style logits（2维，implicit=0/explicit=1）与 `zu` 拼接净化，再 `GumbelSoftmax` 得 `z_style_onehot`。
- **分类**：默认 `cls_hate(zm)`；备选 `use_confounder_for_prediction=True` 时读取 `cat(zm,zu)`；目标头 `cls_tgt(zt)`，风格头 `cls_style(zs)`。
- **直接监督**：(L_{hate}=CE(C_h(z_m),y))；目标 (L_{target}=\frac1B\sum_i target\_conf_i CE(C_t(z_t),target\_id_i))；风格 (L_{style}=CE(C_s(z_s),style))。
- **U的来源不是平台类别**：无环境CE；由四因素联合BART重建文本、KL prior regularization、orthogonality、对抗/下游梯度间接塑形；不能自动宣称该向量表示真实混杂因素。

## 5｜对抗学习、正交与训练机制
- **三个对抗MLP**：`D_m(zm),D_t(zt),D_s(zs)` 预测256维 `zu.detach()`；代码 (L_{adv}=\frac13\sum_{i\in\{m,t,s\}}MSE(D_i(GRL(z_i)),z_u.detach()))。GRL 前向恒等、反向将潜变量分支梯度乘 `-alpha`，因此判别器减少MSE、特征提取端倾向增加MSE；**损失下降只意味着更好拟合当前学习的 zu，不代表真实平台可还原**。
- **正交**：四潜变量分别经可训练MLP投射到128维，单位归一化后两两平方余弦相似度，代码平均六对的 `o_ij`。**论文式(12) 的 \(\lambda_u>1\) 强调U关联项；公开当前代码六项直接平均，不见对应 \(\lambda_u>1\) 特别加权**，为公式与实现差异。
- **重建**：四潜变量各投影BART hidden维后相加，expand到序列长度，BART teacher-forcing 重建输入（CE）。与 KL、任务损失共同训练。
- **正交不等于统计独立**；无法根据GRL训练或在投影空间中的正交推出潜变量已恢复真实因果因素。可用 held-out probes 测量平台/风格/目标泄漏。

## 6｜风格反事实及 Cycle 的论文与代码差异（**高优先级风险**）
- 论文式(17)：只翻转 `z_s` 的 onehot（0↔1）；严格定义 `z_m^{cf}=z_m,z_t^{cf}=z_t,z_u^{cf}=z_u`。式(18)：(L_{cf}=\|C_h(z_m)-C_h(z_m^{cf})\|^2)，**若保持同一个 z_m 张量且分类器只依赖 z_m，数学上恒为0；无非平凡风格不变监督信号**。
- 公开 `cadet.py`：`flip_style=True` 时把 `z_style_onehot=1-F.one_hot(style_labels,num_classes=2)`；与此**没有直接连到 hate_logits**（默认只依赖 `zm`）。
- 公开 `cadet_trainer.py`：反事实loss是对原始与 `flip_style=True` 的**两次独立完整前向**后 softmax hate logits 做MSE；`zm` 经独立高斯噪声和训练态dropout，故loss可能非0；但非零不自动是“风格翻转造成”，可能只是 stochastic consistency。需对照 same-randomness flip 与 no-flip repeats。
- **Cycle**：论文式(19)声称 `Decode→Encode→Style flip back→Reconstruct original` 的闭环；代码 **并未真正文本解码再编码**，而是对同文本再次 `flip_style=True` 直接 `MSE(outputs['zm'], outputs_cycle['zm'])`；代码甚至并非执行两次风格翻转，机制不能按原文“cycle textual consistency”宣称。
- 论文 Table3 `Full F1=0.99`, `-L_cf F1=0.75`（下降0.24），与代码表面机制的独立性存在张力；该ablation究竟哪个数据子集、是否使用泄漏验证和对照随机性，**尚不能从文本断言**。
- **最小核验**：冻结参数 eval 固定随机数/采样噪声，用 100 条数据比较 (a)同向两次前向；(b)仅 flip style；(c)同一个zm只flip zs 的 logits difference；(d)当前代码Lcf；分别记录梯度范数和loss，至少1个seed再扩展。

## 7｜数据集/标签/协议（**高优先级风险**）
- **IE-HSC = 既有公开来源整合**：AbuseEval、DynaHate、Implicit-Hate-Corpus、IsHate；数据卡公开 `hate_label`、`avg`、`style`、`true_style`、`target`、`target_conf`。
- `avg` 为 Perspective API 六项属性平均；`style = 1(avg>=0.4)`，小于阈值为0（缺失默认0）；`true_style` 来自分割文件名（部分数据集不是同一取值）。**实际训练batch使用 `style` 而不是 `true_style`**，所以相当一部分style supervision是基于自动毒性评分阈值，而非严格显式/隐式语言行为的GT；必须对照混淆矩阵才能解释。
- 数据集标签条件强烈不同：如 AbuseEval `explicit_train` hate占98.8%，`implicit_train` hate占14.7%；跨风格变化也伴随类先验变化，可能形成 trivial baseline 偏差。需平衡类别/标签条件的风格划分并分别报告 F1 per class 与 Macro-F1。
- `target,target_conf` 的生成/标注协议在当前README数据卡中未明确至可逐样本核查；`target_conf>=0.9` 过滤后样本分布需查。构建目标词表时 `all_targets=set(train['target'])|set(test['target'])`，使用目标测试集的类别集合（无逐样本标签训练但改变输出维度/类别字典），需固定训练可知 label space 和未知类协议。
- **[CRITICAL: 公开代码验证与测试同集]** `src/cadet/datasets/dataloader.py::load_data/get_dataloaders` 返回 `(train,test,test)`，`cadet_trainer.py` 对val使用标签算F1、阈值选择、best checkpoint/early stopping。因此**按当前实现，目标风格 test 参与模型选择**；与论文声称跨风格泛化/独立测试的严谨性不一致。暂不得断言论文报表即由同一commit生成、或所有结果无效，必须追溯发表版本与重跑无泄漏验证。

## 8｜论文主要实验、证据强度
- Table1: IsHate 29,116，IHC 22,584，AbuseEval 14,100，DynaHate 41,134；这些是论文全量统计口径，**不是当前下载切片经过 target_conf≥0.9 后的必然实际样本数**。
- Table2（作者报告的每数据集 F1）：Explicit→Implicit: IsHate .96、IHC .79、AbuseEval .67、DynaHate .84，平均 .815；Implicit→Explicit: .92、.81、.99、.91，平均 .9075（**注意：作者正文称平均 .885，与 Table2 这4项简单平均 .9075 不一致；需要确认指标、取整和汇总口径，不能混写为已解决**）。
- Table3（另一个消融场景） Full F1=.99；移除Lcf F1=.75；移除Ladv=.86；移除Lorth=.92；未明确与Table2哪一数据切分/评估完全同构，保留差异并不跨表机械比较。
- §5.5 用GPT-4自动把1000条显式文本改写，人工审核保留375条反事实候选；属于额外数据构建工作，并不适合“不构建大标注/不用付费API”的直接复制。
- 论文宣称5次独立run、A100 80GB GPU、最大长度256、至多50epochs、early stopping val macroF1；**尚未GPU复现，不能保证本人的16–20GiB单卡可完成全模型**。

## 9｜创新、假设与已证/未证
- 方法贡献：将 causal prior、disentangled representations、GRL、orthogonality、VAE+BART reconstruct、style flip consistency合为一个 cross-style detection 框架；具体技术大部分为已存在模块，论文主张来自组合、任务定义与实验。
- 未证：潜变量语义可识别性/因果充分性、U真实环境含义、风格独立反事实因果训练、gated data label correctness、无测试泄漏的跨风格泛化、消融机制独立性。
- **不要把当前代码差异直接当研究Gap/idea；先做版本与实验查证。**

## 10｜可迁移机制及 Kill Test
- 候选：在公开implicit-hate真实标签上比较普通RoBERTa、仅M监督、GRL、正交、随机一致性（no-flip）、真正style干预；独立源域验证与封存目标测试。测 targeted false positive、cross-style F1、按标签条件来源/风格分层。
- 尤其做 **flip vs no-flip、same-noise** 和 **target test完全不做val** 两个审计实验，可先 small subset CPU/单卡抽样证明机制，再决定是否完整训练。
- 控制 peak VRAM 16–20GiB、短测≤6h；不假设A100 80GB原设定可直接复现；可使用 100条/500条验证解析过程，无需新人工标签/付费API。

## 11｜关键待解问题
1. 按主会camera-ready PDF核对 arXiv v2是否存在实质方法/表差异。
2. 论文原始评测是否使用当前代码`train,test,test`？提供无泄漏split对照。
3. `style`毒性代理标签与`true_style`的逐集一致性，目标conf provenance / 留存样本数。
4. 公式(12)`lambda_u>1`代码未专门加权、公式(19) Cycle 与代码不一致，是否影响报告消融。
5. flip在固定随机性下是否真正改变`hate_logits`，以及梯度方向/强度。
6. Table2 implicit→explicit平均与正文.885汇总差异需要解释。

## 12｜归档与下一篇
- P033 定稿仅表示「已解释、审计、明确边界并记录反面证据」，不是批准此方法机制/结果。主仓库该卡供后续竞品查重和 Kill Test 规划。
- **下一篇 P034**：*CrossGuard: Safeguarding MLLMs against Joint-Modal Implicit Malicious Attacks*，Xu Zhang、Hao Li、Zhichao Lu，**ACL 2026 Main（CCF-A）**；DOI 10.18653/v1/2026.acl-long.1178，官方 https://aclanthology.org/2026.acl-long.1178/ ，代码 https://github.com/ZhangXu0963/CrossGuard；需审计“text+image各自安全但联合危险”的数据构建、ImpForge RL奖励与跨模态推理、训练任务/对抗评测和代码可达性；当前**尚未正式精读、不得定稿**。
