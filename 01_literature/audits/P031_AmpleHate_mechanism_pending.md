# P031｜AmpleHate：机制正确性暂存审计（暂缓定稿）

> **状态（2026-10-27）**：用户明确决定“暂缓定稿”；本文件仅记录已完成的**初步全文/代码机制审计**，不是正式阅读卡，不代表本地复现或完整复核已完成。该状态允许进度记录合并至 main，但不允许将 P031 标为“已分析/已定稿”。

## 证据与研究任务

- 论文：Yejin Lee et al., *AmpleHate: Amplifying the Attention for Versatile Implicit Hate Detection*, EMNLP 2025 Main，DOI：10.18653/v1/2025.emnlp-main.1469。
- 正式 PDF：https://aclanthology.org/2025.emnlp-main.1469.pdf（§3.1–3.4、Figure 2、§4 与 Table 1–3）。
- 官方公开代码（当前 main，静态审计）：https://github.com/leeyejin1231/AmpleHate；
  关键文件：model/model.py、utils/preprocess.py、utils/dataloader.py、train.py、test.py、config/train_config.py、config/test_config.py。
- 作者目的：显式实体目标经 NER 提取，隐式线索由 [CLS] 表示，计算目标与句子上下文关系向量 r，并通过 z=h0+λr 注入分类表示。其报告的任务为若干有害语言数据集上的二分类；NER 实体不等于真正受攻击群体。

## A. 论文中的机制问题（原文 §3.2 / Figure 2）

原文明确写 Q=h0、K=H_tgt、V=h0，并定义 r_tgt 为目标权重乘 V 后求和；同时表述 r=r_exp+r_imp。**条件化数学判断**：如果将其 Softmax 理解为在同一样本的所有候选目标上标准归一化，则各目标共享同一 V=h0，故 r_exp=(Σ_t α_t)h0=h0（显式目标非空时）；隐式目标只含 [CLS] 时 r_imp=h0。这样注意力权重分布即使改变，也不能选择性改变关系向量，故论文对“目标敏感关系表示”的解释未由其公式支持。

**不能无条件声称 r=2h0**：正文同时计算 explicit/implicit 的叙述与 Figure 2 中的“有显式目标时用显式，否则 [CLS]”分支并不一致；是否在所有实际条件下加两项，需作者代码/运行证据明确。上述推导也以 Softmax 跨目标归一化为条件，不排除作者另有未明确写出的归一化方式。

## B. 当前公开代码的独立可证问题

1. **batch 维注意力，而非句内目标注意力**（model/model.py：HeadAttention.forward）。当前 Q_h、K_h、V_h 形状均为 [B,d]，attention_scores = Q_h @ K_h.T 为 [B,B]，output=(row softmax)@V_h：样本 i 的向量受同 batch 样本 j 的 Key/Value 影响，而 j 并非 i 的句内目标。该性质可由张量形状证明；未对完整预训练模型做逐 batch 不变性测试。B=1 时 softmax 只有一个元素，输出恒为 W_v h0，不含目标 Key 信息。
2. **多目标求和与 padding 无掩码**（model/model.py、utils/dataloader.py）。逐个目标位置重复调用上面的 batch-attention，输出求和；不同样本目标数不足时填充索引 0（[CLS]）而没有有效目标 mask。即使 B=1，输出也随目标位置总数而改变；同批样本的最大目标数可影响输出。
3. **训练与推理目标管线不一致**（train.py、test.py）。训练 loader 开启 use_ner=True；验证及测试 loader 关闭 use_ner=False。关闭 NER 时目标索引总是 [0]，即 [CLS]。因此当前公开的验证/测试入口没有真实运行显式目标抽取，不能直接检验预测收益来自显式目标建模。
4. **NER 类别/位置对齐疑点**（utils/preprocess.py）。允许实体类别 ORG/NORP/GPE/LOC/EVENT，但默认使用 CoNLL-03 NER tagger，标签空间是否能覆盖所要求的类别要逐项比对；字符串 tokens.index(ht) 无法可靠对齐多 token/子词实体，失败后回退 [CLS]。需要运行统计真实有效目标的比例。
5. **论文与默认复现配置不一致**：论文 §4.3 报 6 epochs、Macro-F1；公开 config/train_config.py 默认 4 epochs，test.py 采用 weighted-F1，而训练校验采用 macro-F1；test_config.py 的 e=1 不一定与训练搜索所得一致。以上仅说明默认公开复现协议不同，不证明作者报告值错误。

## C. 关于结果与可支持结论

论文 Table 1 报 AmpleHate（bert-large-ner）七个数据集平均 Macro-F1 82.14%，BERT 75.27%，LAHN 76.56%；对应作者报告的平均百分点增益为相对 BERT +6.87、相对 LAHN +5.58。**这些是论文声称/报告的结果**，并非本项目复现实验。由于当前公式/实现/训练-测试管线的问题，现有分数与注意力可视化**不足以可靠归因于句内 Target–Context 关系建模**。不能据此判定数据或结果造假，也不能否认一个改变后的分类器可能提高 F1。是否存在作者私有实验版本、公开代码后续改动仍待查证。

## D. 后续处理（本轮不执行）

- **P031 暂缓定稿，不再继续常规精读、不作为已确证的目标关系建模基线。**
- 仅当之后确实需要复现时：先固定单个输入、改变同 batch 其他文本；再固定样本和 batch 替换目标索引并统计变化；核查真实 NER 覆盖率；最后才考虑修正后重训和公平消融。需要确认作者使用的具体提交/权重/运行配置。当前未实际跑完整模型，无显存与时间保证。
- 下一阅读优先级转向 P024（CONELA）、P030（SMARTER），不把 P031 的代码缺陷直接升级为 Research Gap 或 Idea。
