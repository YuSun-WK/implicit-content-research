# 表7｜跨子域方法族：优化对象、直接证据与未闭合问题

| 方法族 | 代表研究（正式出处与CCF等级） | 方法实际改变什么 | 现有证据与关键边界 |
|---|---|---|---|
| 概率语用推断 | (RSA)²（ACL 2025 Main，CCF-A） | 在给定候选意义、语境和修辞策略下，建模说话者/听者的概率推断；不依赖新增类别微调。 | 正式实验显示修辞策略和意义先验会改变候选意义概率；这支持候选空间内的概率推断，不等于开放式释义或真实心理意图读取。 |
| 提示式含意与行动选择 | DRInQ（ACL 2026 Main，CCF-A）；VAGUE（ICCV 2025 Main，CCF-A） | 冻结LLM/MLLM，通过上下文示例、解释提示或CoT完成候选含意/行动选择。 | 部分模型因解释提示而提升，另一些模型下降或不变；提示收益不具有跨模型单调性，也不证明解释忠实。 |
| 编码词项与检索辅助 | Silent Signals（ACL 2024 Main，CCF-A）；FETCH!（ACL 2025 Main，CCF-A）；FA-Net（AAAI 2024 Technical，CCF-A）；SeTox（ACL 2026 Main，CCF-A） | 分别使用已知编码义、种子词典、固定目标类别或在线检索；其预测单位包括实例义、词项类型、候选目标义和毒性标签。 | 证明不同先验可支持各自定义任务；不能把它们合称为统一开放词义发现，也不能横排Precision、Acc@k和毒性F1。 |
| 监督表示学习与多模态融合 | ImpCon（COLING 2022 Main，会议CCF-B）；MGMCF（AAAI 2025 Technical，CCF-A）；M3UCD（AAAI 2026 Technical，CCF-A）；MultiMM（ACL 2025 Main，CCF-A）；DOSE（ACL 2026 Main，CCF-A） | 使用对比学习、多任务标签、源/目标概念、情绪辅助、共享/私有LoRA或任务专家，改变表示和融合方式。 | 作者报告了各自协议下的性能收益，也有负迁移和额外监督；结构消融或人工模态归属不能单独证明因果机制或模态必要性。 |
| 信息瓶颈与条件压缩 | MCIB（AAAI 2026 Technical，CCF-A） | 将条件预测、KL压缩与多模态表示结合，用于音视频文本反讽分类。 | 完整配置报告weighted-F1=75.64；现有消融未单独隔离CIB损失。公开Transformer实现还存在潜在维度广播风险及原始文本残差路径，正式run对应关系仍未核实。 |
| 解释与轨迹偏好优化 | SMARTER（ACL 2026 Main，CCF-A）；ExPO-HM（ICLR 2026，CCF-A）；ThinkingGuard（ACM MM 2026，会议CCF-A，正式Track待核） | 分别使用标签—解释DPO、政策SFT+课程GRPO+CDE，以及离线SA-MCTS轨迹与Step-DPO；优化目标分别是毒性分类、仇恨Meme解释后检测和输入风险归因。 | 作者报告的性能收益来自不同监督对象与训练协议；额外教师信息、gold标签、Unsafe偏好和token预算尚未完全匹配，不能把收益统一归因于解释或逐步推理。 |
| 红队攻击生成与输入Guard | ImpForge/CrossGuard（ACL 2026 Main，CCF-A） | ImpForge用PPO优化隐晦攻击改写；CrossGuard用LoRA/SFT训练图文Safe/Unsafe Guard。 | 攻击成功率、Guard漏检率和生成模型危险回应率是不同指标；训练数据量与类别组成也会影响结果，不能把全部提升归因于分类架构。 |
| 安全回应对齐与行为评价 | Meerkat-VL（ICML 2026 Main，CCF-A）；VLSU（ICLR 2026，CCF-A） | Meerkat-VL通过SFT和GRPO优化安全且有帮助的回答；VLSU的Harmless/Helpful提示实验则在冻结模型上比较回应策略，不更新参数。 | 回应安全性、帮助性和拒答行为可发生不同方向变化；它们不等同于显式输入风险分类，也不能据拒答率反推模型内部风险判断。 |

**表注。** 本表按方法实际优化对象归纳，不构成跨任务排行榜。各论文的具体数据、指标和GT见表3–表6；第8.1.1节C1–C3负责跨子域条件性综合，本表不重复其全部数字。CCF等级按项目采用的2026年第七版目录口径；Findings、Technical、Main和作者录用但正式Track未核的状态分别标明，不以会议整体等级替代论文Track信息。
