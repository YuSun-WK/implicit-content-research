# R2-B / B1-04｜Rhetorical Questions in LLM Representations（正式精读卡）

> 更新时间：2026-11-08；状态：**定稿（保留未关闭核验问题）**。临时索引 **R2A-004**，**不占用 P001–P041 / T001–T018 正式编号**。

## 0. 正式信息、开放资源与证据
- **题目：** Rhetorical Questions in LLM Representations: A Linear Probing Study
- **作者：** Louie Hong Yao, Vishesh Anand, Yuan Zhuang, Tianyu Jiang
- **发表：** ACL 2026 Main（Long Papers），**CCF-A**；页码 155–172；DOI：10.18653/v1/2026.acl-long.5。
- 官方全文：https://aclanthology.org/2026.acl-long.5.pdf
- 官方论文页：https://aclanthology.org/2026.acl-long.5/
- 作者代码与数据：https://github.com/ruyi101/rq-representation-probing
- **研究类型：** 冻结大模型的内部表示诊断与跨域线性探针分析；不是新语言模型训练方法。

## 1. 研究问题、动机及任务归属
- **核心问题：** 反问句（rhetorical question）与普通信息寻求疑问句（information-seeking question）的差异，能否在 LLM 内部隐藏状态中被线性读取？不同探针及数据域学到的“反问方向”是否一致？
- 反问句的言语功能可能是表达立场、批评、说服，而非寻求事实答案；句法疑问形式并不确定语用功能。
- **R1主归类：X2（表示与机制分析）**；关联 **T1（修辞识别）** 和 **T3（交际功能判断）**。本研究未直接输出开放式的隐含意义释义，也未恢复真实人物的心理意图，更不是 T4/T5 有害内容检测。
- **输入：** 疑问句与社交媒体上下文；**读出：** LLM 各层隐藏向量；**探针输出：** 反问评分/二分类标签；**主评价：** AUROC、方向对齐与排序稳定性。
- **证据：** 正文 §1–3，Figure 1。

## 2. 数据、标签与Ground Truth
| 数据集 | 场景 | 总量 | 反问数 | 训练/验证/测试 | 上下文 |
|---|---|---:|---:|---|---|
| RQ（Zhuang & Riloff 2020） | Twitter | 4,997 | 2,332 | 3,200 / 797 / 1,000 | 上一条推文 + 当前问句 |
| SRAQ（Ikumariegbe et al. 2025） | Reddit | 971 | 609 | 384 / 103 / 484 | 当前问题段落（主实验）或完整评论（附录） |

- **GT**：原始数据集已有的反问句/信息寻求问句二元标签（0=information-seeking，1=rhetorical），作者沿用其原始划分，没有重新标注或证明两套标注协议完全等价。
- **原始来源：** https://aclanthology.org/2020.acl-srw.41/ （ACL 2020 Student Research Workshop，非ACL Main）；https://aclanthology.org/2025.emnlp-main.1553/ （EMNLP 2025 Main，CCF-B）。
- **证据：** §3.1，PDF第3页（出版页157）。

## 3. 完整计算流程和关键公式
### 3.1 隐藏状态
1. 用冻结的 Qwen3-32B 与 Llama-3.3-70B-Instruct 提取各层激活；比较末 Token 表示 \(h_T\) 与平均表示 \(\bar h=\frac1T\sum_{t=1}^T h_t\)。
2. 主要实验把每个数据集、模型、输入设置下的隐藏状态映射到 **64维 PCA** 空间；多个探针使用该设置中的同一投影。还检查未经PCA的部分结果。
3. 不是端到端微调原语言模型；标签训练仅用于探针。注意PCA拟合范围有单独未决复现疑问，见第7节。
- **证据：** §3.2，式(1)，§4，Figure 1，Appendix A/B。

### 3.2 三种线性探针
- **diffMean**：\(w_{\rm DM}=\mu_+-\mu_-\)，其中正负类分别为反问与信息寻求问句；评分 \(s(x)=w_{\rm DM}^{\top}h(x)\)。训练自由是指**无需优化分类器参数**，但计算均值仍需要类别标签，不是无监督。§3.3，式(2)。
- **Logistic 回归**：对隐藏向量训练 \(s=w^\top h+b\)，用二元交叉熵优化；属于线性有监督探针。
- **Linear SVM / hinge probe**：同样学习线性方向，使用合页损失的间隔优化。
- diffMean使用训练集，两个可学习探针在训练集训练、验证集选择，主结果报告测试集；§3.3，出版页158。

### 3.3 方向和排序一致性
- **AUROC**：能否区分反问和信息寻求问句；
- **Cosine similarity**：探针权重向量的几何对齐；
- **Spearman**：相同目标语料的探针评分排序是否一致；§3.4，式(3)；
- **Top/bottom 20% 的 Jaccard**：对最典型两端样本的选择是否重合；§3.4，式(4)。
- 跨数据集比较时，PCA子空间不同，作者将向量映回原始隐藏空间再比较（§6、Appendix B）。

## 4. 主要结果与证据位置
1. **层与表示形式（§4，Figure 1）**：last-token在中深层通常比mean pooling更稳定；diffMean深层AUROC约0.8；hinge/logistic在RQ约0.85–0.9、SRAQ约0.8–0.85。是**不同层/数据集的近似范围**，不可当作单一最优模型定值。
2. **同数据集探针不等价（§5，Figure 2）**：hinge和logistic权重方向、排序几乎重合；diffMean与两者存在明显差异。特别是SRAQ，diffMean与训练探针的方向余弦相似度常约0.5，部分排序较不一致。可分类不意味着所有探针找到同一方向。
3. **跨域可迁移但方向不统一（§6，Figure 3–4）**：跨RQ和SRAQ AUROC仍约0.7–0.8，然而跨域方向余弦相似度常约0.2–0.4，最高排名20%的集合Jaccard经常低于0.2。相似AUROC与相似实例排序是两回事。
4. **语言学解释（§7，Table 1–2）**：作者借定性实例提出不同域的方向可能分别偏向篇章层立场/论证与局部句法提问形式；这些解释不是对所有候选语言学因素逐一完成的干预因果检验。
5. **激活干预（Appendix F，式(11)，Figure 10–11）**：沿diffMean方向扰动激活，研究生成问题反问程度变化；提供初步行为干预佐证，但输出依赖LLM评价、有限模型/语境，不能推导出已发现唯一因果“反问神经元”。
- **主结论：** “可线性区分”和“可跨域分类”不等于“共享稳定且唯一的反问表示方向”。

## 5. 创新性、贡献与合理外推
- **贡献1：** 由下游反问分类转向多层、不同聚合方式的隐藏状态诊断。
- **贡献2：** 将分类可迁移性与方向/排序一致性分开评价，揭示不同训练域/探针可以给出相近AUROC、却重视不同样本。
- **贡献3：** 提供定性与有限干预证据，支持反问线索有多种表达形式（篇章立场与局部句式）。
- 主要贡献是**表示研究/测量方法及经验发现**，不是新型反问检测架构或泛用语用推理模型。
- **必须限缩：** 不等价于证明多种独立的“内在语用特征”已经被精确定位；跨数据集差异受域、文本长度、语境粒度和标注协议共同影响。

## 6. 与馆藏与前三篇的关系、综述建议
- **P011**：语用研究与评价综述；**P020 (RSA)²**：概率语用意义推断框架；
- **DRInQ**：固定文本问句，控制语境变化来测会话含义（T3）；
- **VAGUE**：视觉语境中的间接行动意图（T3）；
- **Negation vs Implicature**：意图语义相似性与表征学习（X2/T2/T3）；
- **本文**：反问句隐藏状态的可线性读取、跨域稳定性与多方向线索（**X2/T1/T3**）。
- 中文综述建议放在“修辞与语用的表征、诊断及泛化可靠性”小节，作为**分类准确≠表征结构一致**的典型案例。不可据此宣称广义隐晦信息所有机制均存在同样多向量结构。

## 7. 公开代码与未关闭复现问题
- 官方仓库：https://github.com/ruyi101/rq-representation-probing
- 已公开：RQ的\`data/RQ.csv\`、逐层embedding提取、PCA、Logistic/SVM探针训练及一致性分析脚本。README明示 **SRAQ未直接附带**，需要从原论文另行取得；embedding、PCA和探针产物需本地重新生成。**代码公开不等于完整数据及运行验证。**
- **核心待核验：** 正式PDF Appendix B的PCA均值明确描述为**训练split计算**（出版页166）；但公开 \`scripts/pca_transform.py\` 片段对所加载embedding层矩阵使用 \`PCA(...).fit_transform(X_np)\`。若输入为全体train/val/test，则与文中描述不完全一致，潜在存在无监督预处理利用测试数据的问题。**尚未追溯正式实验的输入和执行脚本，不应断言已经发生测试泄漏**。
- 进一步核验标签跨域可比性、长/短上下文与域差异控制、不同PCA拟合范围对最终AUROC影响、干预实验中独立人工评价。
- 32B/70B逐层隐藏状态提取对共享16–20GiB单卡环境并非低成本复现；不建议直接作为下一阶段Kill Test的首选基线。

## 8. 主要证据索引
- 主文 §3.1–3.4、式(1)–(4)、Figure 1–4、Table 1–2；
- Appendix A：PCA与原空间对比；Appendix B：PCA映回原空间、训练集均值表述；Appendix F：steering分析；Appendix G：语境粒度。
- 正式PDF： https://aclanthology.org/2026.acl-long.5.pdf
- 开放仓库README/代码： https://github.com/ruyi101/rq-representation-probing/blob/main/README.md
- PCA脚本： https://github.com/ruyi101/rq-representation-probing/blob/main/scripts/pca_transform.py

> 注意：正式精读卡完成，不等于完成外部数据来源逐行审计或运行级复现。保留上述未关闭核验事项。
