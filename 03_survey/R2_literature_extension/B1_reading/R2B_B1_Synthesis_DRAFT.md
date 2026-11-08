# R2-B / B1｜语用与视觉意图四篇论文综合（工作版）
更新：2026-11-08。状态：**综合审核WORKING DRAFT**；四篇独立阅读卡均已定稿，但开放数据/实现问题保留。

## 1. 四篇研究的本质差别

| 论文 | 主要目标 | R1映射 | 输入与输出 | GT与主要指标 |
|---|---|---|---|---|
| [DRInQ](R2B_B1_01_DRInQ.md) (ACL 2026 Main, CCF-A) | 固定问句Q、变化文本语境C时选择当前会话含义 | T3主、T2次 | Q+C+五种候选含义→选择 | 人类4/5共识；五选一Accuracy |
| [VAGUE](R2B_B1_02_VAGUE.md) (ICCV 2025 Main, CCF-A) | 图像语境下消解间接行动意图 | T3主、T2次 | 图像+间接表达+4行动选项→选择 | 生成目标行动+人工合理性审核；Accuracy |
| [Negation vs Implicature](R2B_B1_03_Negation_vs_Implicature.md) (ACL 2024 Main, CCF-A) | 区分词面相似与意图一致的语义编码，兼研究对比训练 | X2主，T2/T3关联 | 原句、否定、隐含正例→embedding距离/聚类或分类 | 原数据intent标签+LLM构造；Triplet/分类/聚类指标 |
| [Rhetorical Questions](R2B_B1_04_Rhetorical_Questions_Linear_Probing.md) (ACL 2026 Main, CCF-A) | 冻结LLM隐藏状态中的反问区分线索及跨域稳定性 | X2主，T1/T3关联 | 疑问句及语境→隐藏向量→线性反问评分 | 来源语料反问标签；AUROC、方向余弦、Spearman、Jaccard |

## 2. 横向得到的结论与不能推断的结论

1. **语境作用**：DRInQ在文本C上控制问句Q；VAGUE以图像构成场景上下文，说明T3可为文本/多模态任务。但“改图后模型是否仅因风险/意图变化而改答案”仍需要单模态/反事实严格控制。
2. **不同层的能力证据**：DRInQ与VAGUE的多选准确率是行为层证据；Negation-vs-Implicature的距离排序是表征性质；Rhetorical Questions的probe AUROC是隐藏状态可读性。不可写成同一种“语用理解准确率”。
3. **GT不能偷换为心理意图**：DRInQ是生成语境再由人工投票；VAGUE是构造行动目标再人工审核；意图编码器样本部分依赖原始类别与模型生成；反问数据沿用原语料标签。均不直接观察真实说话者的全部意图。
4. **类别定义与候选捷径**：五选一/四选一的高分仅支持特定候选集内的选择能力，不能直接断言开放语义恢复；probe方向一致性低也不否定标签本身可线性分类。
5. **模型≠统一新训练体系**：DRInQ/VAGUE重点为评测及数据任务；Negation-vs-Implicature含hard positive/negative对比编码学习；Rhetorical Questions为冻结模型的线性探针。技术代际不宜直接排序优劣。
6. **与旧馆藏的连接**：P011是语用现象/评测综述，P020 RSA是策略条件概率推理，B1提供可操作的文本语境、视觉语境、语义表征、内部探针四类互补证据。

## 3. R1分类修订及综述建议

- T3仍然有效，但应区分**会话含义与语境解释**、**间接言语行为/行动意图**、**语义意图表征**三种任务对象；不宜把所有意图编码器任务当作开放式语用推断。
- 语境是任务输入条件而非和T1–T6并列的单一标签：文本篇章、社会知识、视觉场景，以及实际对话者背景可各自提供语境证据。
- 综述建议先以P011/P020建立语用意义机制，再以DRInQ/VAGUE作为“语境下的解释选择”，之后用Negation-vs-Implicature与Rhetorical Questions说明分类性能之外的表示可靠性诊断。
- 图文多模态**语用理解**与图文**安全风险判断**仍须分别写，不能把VAGUE直接当T5安全数据集。

## 4. 最影响证据可靠性的未关闭问题

- DRInQ：正式论文819条人工验证、400条困难子集，作者README的公开CSV只有231条/148不同问句；引言76%/89%与困难集Table2 67%/88%不能混用。
- VAGUE：README弃用v1.0 3,993条，使用v2.0 1,677条；400条人工测试与全体不同；direct/solution/caption字段的潜在label泄漏、图像置换控制待审。
- Negation-vs-Implicature：论文损失公式、公开train_st.py及实际Table3运行入口是否吻合未完全核实；生成正负例的GT只能视作任务化操作标签。
- Rhetorical Questions：附录声称PCA训练划分均值，公开脚本对加载的embedding集拟合；尚不能认定已发生测试泄漏，需追踪正式运行输入；跨域探针方向不一致受域与标注协议影响。
- 四篇均未完成全量独立代码运行复现。后续综述应明确区分原论文报告与本项目静态审计。

## 5. 阶段决策

**B1精读完成，跨论文工作综合完成，可进入B2。** B1开放问题不要求在开始下一组前全部关闭；它们属于正式写作的引用核验和必要时的定向补审。

## 6. B2建议阅读顺序
1. R2A-006 Silent Signals（ACL 2024 Main, A）：狗哨编码义消歧；
2. R2A-007 Making FETCH! Happen（ACL 2025 Main, A）：新狗哨发现；
3. R2A-008 Uncovering and Mitigating the Hidden Chasm（AAAI 2024 Main, A）：委婉语解码与域差；
4. R2A-010 New Terms, New Toxicity / SeTox（ACL 2026 Main, A）：新词毒性与动态语境；
5. R2A-011 When People are Floods（ACL 2025 Main, A）：非人化隐喻；
6. R2A-012 Sheep's Skin, Wolf's Deeds（ACL 2025 Main, A）：隐喻隐式仇恨的生成/检测与安全诊断。

依据：[R2-A候选清单](../R2A_Candidate_Ledger.md)、[R1工作框架](../../R1_taxonomy/R1_Working_Framework_DRAFT.md)，以及本文件四篇已定稿精读卡。
