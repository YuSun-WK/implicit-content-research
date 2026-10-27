# P024｜CONELA（2026-10-27 定稿）

**论文** Do-Kyung Kim, Hyeseon Ahn, Youngwook Kim, Yo-Sub Han. Analyzing Offensive Language Dataset Insights from Training Dynamics and Human Agreement Level. COLING 2025 Main, pp. 9780–9792.
正式版 https://aclanthology.org/2025.coling-main.653/ ；正式PDF https://aclanthology.org/2025.coling-main.653.pdf ；代码 https://github.com/kdkcode/CONELA 。
**阅读卡状态** 用户 2026-10-27 授权定稿；已审正式论文与公开代码，非本地复现，部分数据来源细节/代码差异保留待核验。

## 方法动机、输入输出
问题：有害/隐式仇恨数据具有主观性，模型学习难度与标注员分歧不完全相同；作者拟用两者筛出相对可靠且有泛化价值的训练子集。
输入：原训练文本及类别标签、来自原数据的人类分歧/聚合信息。输出：筛后训练集、重新训练的二分类器；测试和验证使用固定原测试/验证集。
1. BERT 多 epoch 训练，记样本 i 在 epoch t 对其标注类别的概率 p_{it}；C_i=mean_t(p_{it}), V_i=std_t(p_{it})；这衡量的是模型对**给定标签**的学习过程，而非人工判定的语义真值。
2. Data Cartography 划分 EtL（高 C）、AtL（高 V）、HtL（余项）。公开 split_categories.py 实现：高 C 取约 1/3，再从余下按高 V 取约 1/3，余项为 HtL；没有固定的语义阈值。
3. 论文§3.2按人工“完全一致/非完全一致”将三类各拆成 Consensual/NonConsensual，六类中删除 EtL-NonConsensual 和 HtL-NonConsensual，保留 AtL 两类和 EtL/HtL 的一致样本，重新训练普通分类器。这是**筛选数据**，不是新网络结构或推理损失。
4. 论文§4额外有小数据集 weighted disagreement/ensemble 扩展，不应与核心筛选混为一谈；公开代码中的完整实现待核对。

## 人工分歧来源与概念边界
论文使用既有公开数据集的信息，未找到作者另行全量招募标注员新标记样本的证据。Table 2：SBIC/OLID/ETHOS为训练来源及ID/OOD测试，DynaHate/ToxiGen仅用于测试；SBIC的 offensiveYN 是原有人工作答的聚合字段。对OLID、ETHOS具体哪一版本包含怎样的逐人标注/投票数据及代码如何转化还须单独核验，不能把论文声称提供一致性信息自动当作核验完成。
论文将 Consensual 定义为所有标注员一致，Non-Consensual则为不一致。代码中的 abs_offensiveYN=abs(offensiveYN-0.5) 以及组内中位数阈值，只衡量和0.5的距离，不等价于核实每位标注员原始选择；例如SBIC允许0/0.5/1回答时，全员0.5也有可能被判为“低一致”。
数据集任务非完全同构：SBIC offensiveness/social bias、OLID offensive、ETHOS hate、DynaHate/ToxiGen hate等不能统一当作严格隐式仇恨真值。

## 作者实验（§5–7）
Table2数据规模：SBIC训练35,424→筛后28,322/测试4,691；OLID 19,826→18,401/测试2,479；ETHOS 798→568/测试100；DynaHate测试4,120；ToxiGen测试8,960。
Table3 BERT F1%：SBIC→SBIC 85.52→87.56，SBIC→OLID 83.64→90.35，ETHOS→OLID 59.51→72.39（同一测试集上对比）；Table6 SBIC训练跨五个测试集平均 75.10（完整）→78.41（CONELA），只删 EtL-NonConsensual 75.13，只删 HtL-NonConsensual 77.63，删除全部 NonConsensual 77.41。
这**支持所报告设置下的分类性能增益**，不能证明被删除者大多数标签错误、性能来自隐含意义恢复或联合机制具有充分因果归因。对照尚需等量随机删除、等量按训练错误/低C删除、等量按人类分歧删除、类别比例控制和明确种子、原始同义/重叠审计。人工分歧可能表示真实多解性，而不一定是标注噪声。固定测试集排除了“删测试难样本”这一解释，却不排除改变训练分布带来的收益。

## 公开代码静态审计（未运行）
- cartography_sbic.py：产生epoch日志、计算C/V；split_categories.py：分3×2训练集；conela_sbic.py：训练及评测。
- split_categories.py实际上对每个学习类别的 abs(offensiveYN-0.5) 取 **组内中位数** 分Consensual和NonConsensual，不是论文的“全员一致”。README中的示意代码则采用“距离=0.5”，又与实际脚本不同。需保存版本及参数核验。
- cartography_sbic.py 与 conela_sbic.py Dataset 返回(input_ids,token_type_ids,attention_mask,label,index)，而模型调用把 batch[1] 映射到 attention_mask、batch[2] 映射到 token_type_ids：张量参数疑似互换，可能严重干扰 BERT。不能声称当前公开代码已经完整复现论文数值；需要实测和作者版本对照。
- cartography脚本输出训练动态JSONL，split_categories.py示例直接pd.read_csv读取，需要文件转换/核对。cartography代码 np.std 默认ddof=0，而论文Eq(2)写样本标准差N-1；分组排序可能不变但数字不同。
- 旧版依赖和多阶段训练可能增加调试成本；16–20GiB/≤6h实测未进行。

## 研究关系
与P032 ImpCon区别：ImpCon利用既有隐含解释为表征学习提供额外监督；CONELA根据学习动态和人类标注分歧更改训练数据，而不是显式输出或推理隐含含义。与R1–R5保持语言机制、任务标签、模型学习行为分层。此卡不代表任何新Gap/Idea已获证实。