# R2-B / B3a-03｜Two Streams, One Sarcasm / DOSE（正式精读卡）

> 日期：2026-11-08；**用户明确指示“定稿合并”**。定稿指文献/源码审计结论归档，不表示已跑模型、复现论文主表、或解决全部评测风险。本文为B3a第3篇；与B2b并行，禁止覆盖其文件。数据集文中写作DocMSU-PLUS，官方代码仓库记作DocMSU++。

## 1. 出版与研究定位
- 标题：*Two Streams, One Sarcasm: Orthogonal Expert Tuning for Holistic Multimodal Sarcasm Understanding*。
- **ACL 2026 Main（CCF-A）**，pp.7054–7072。
- 正式论文：https://aclanthology.org/2026.acl-long.319/；PDF：https://aclanthology.org/2026.acl-long.319.pdf
- 官方方法及数据代码：https://github.com/Remwlp/DOSE
- 贡献：DocMSU++（数据及多任务MCQ标注）、DOSE（双流LoRA专家+混合路由+共享/私有子空间正交正则）。
- R1任务：T1反讽存在性、T2反讽机制与解释选择、T3意图判断；对象定位为解释证据定位维度。**没有以T4有害性或T5图文联合有害风险为直接Ground Truth**。讽刺 ≠ 有害。

## 2. 数据集构建、目标标签与任务映射
- DocMSU++从已有DocMSU扩展，**14,128**篇图文，代码官方统计标记“Yes”6,874、“No”7,254；来源为新闻/讽刺文章+图片。
- 论文主表强调五项任务：**Detection（二分类）**、**Mechanism（五类）**、**Description（反讽说明MCQ）**、**Target（目标图文对象MCQ）**、**Intent（五类）**。
- 正式代码 `dose/data_utils.py` 实际定义**六种MCQ变体**：
  `is_sarcastic`, `sarcasm_mechanism`, **`dominant_modality`**（额外任务）, `sarcastic_intent`, `target_qa`, `object_qa`。论文主结果的五项与默认训练/评测6项不应混同。
- 解释与对象定位分别以**选择正确解释和选择文本片段/图像bbox的选项**评价；不是开放式自然语言解释质量和自动框定位IoU的直接测量。
- Gemini-2.5-Pro辅助产生“Premises→Incongruity→Inference”、候选解释/QA/难负例；作者叙述为5位标注人员审核和纠正原标签噪声，报告约12%标签修正与1,000条重叠样本总体Fleiss κ=0.8256。**意图标签是标注者对文本效果/交际目的的判断，非发言者内在动机真值**。
- 公开官方统计 `data/DocMSU++_statistics.json`：`target_qa`覆盖7,128、`object_qa`覆盖5,539、同时两者5,539；与6,874反讽正例不一致。该原始记录覆盖统计≠训练有效题数，因为 `enumerate_mcq_variants()` 遇非反讽会跳过四种后续任务。**不能据此直接定性标签错误，但需要核对原始标注阶段与有效任务阶段的分母。**
- 图像未打包于DOSE仓库，需另从DocMSU获得；正式GitHub提供JSONL及官方train/val/test、data_efficiency、OOD category/task切分；模型基座、训练日志、adapter权重、完整基线实现均未公开。

## 3. 方法与损失
### 3.1 Dual Orthogonal Stream Experts
对第i个专家：
`E_i(x)=B_S^i A_S^i x + B_P^i A_P^i x`。
其中shared/private均为低秩增量；不是两个独立完整MLLM。代码 `dose/dose.py:DualProjectionExpert`确有两组`Linear`和独立低秩秩数；官方脚本默认4专家、shared rank8、private rank8、LoRA r16、alpha32。

### 3.2 Task-Adaptive Hybrid Gate
路由将样本内容路由与任务ID嵌入路由按参数β混合：
`g(x,t)=β·softmax(W_r x)+(1−β)·softmax(E_t)`；
代码 `OSMoELoraLinear.forward` 显式实现这两项和`global_router_weight=0.5`；`family_policy_table`为可学习正权，控制shared/private的任务族权重。

### 3.3 Orthogonality约束
`L_orth= Σ_i || (B_S^i)^T B_P^i ||_F^2`，总损失 `L_total = L_CE + λ L_orth`；代码 `DualProjectionExpert.orthogonality_loss()`执行 `shared_B.weight.T @ private_B.weight` 的Frobenius平方，`OSMoELoraModel.forward()`累加正交损失进训练loss。
- 几何含义：减少两条**输出投影参数子空间**重叠；**不是**约束全部任务梯度余弦相似度非负。
- 即使`B_S^T B_P=0`，两任务`∇_{B_S}L_t`可能相反，任务仍共享B_S等参数。论文未直接报告每对任务`cos(g_i,g_j)`的前后变化，因此不能把几何分离称为“物理阻断任务梯度冲突”的充分证明。
- 论文正交特征余弦相似度约0.014；证实某种表示解耦信号，不等于真实梯度冲突被消除。
- 正交权重：附录Table13提`1e-3`且代码默认`1e-3`；附录B.1的表述另称0.1–1表现较优，未理清实验范围/控制因素，列OPEN，不擅自合并为同一最优超参。

## 4. Baseline、主结果与消融
- 两MLLM骨干包括LLaVA-1.6-7B、Qwen3-VL-8B；baseline：LoRA、MoE-LoRA、CL-MoE。主表强调低数据训练约1%。
- 正式论文Table3，Qwen3-VL-8B Accuracy（%）：
| Task | LoRA | CL-MoE | DOSE |
|---|---:|---:|---:|
| Detection | 94.76 | 94.65 | **95.86** |
| Mechanism | 39.03 | 38.73 | **40.14** |
| Description | 94.98 | 94.81 | **95.69** |
| Target | 85.27 | 81.36 | **88.69** |
| Intent | **74.45** | 71.99 | 74.14 |
| Overall（五任务等权Acc） | 77.70 | 76.31 | **78.90** |
- 正式论文Table4消融：完整Overall78.90；w/o private75.30，w/o shared75.49，w/o orth76.41，w/o adaptive gate75.56；说明模块对总体分数有贡献，但**移除正交项后Target 91.34 > 完整DOSE 88.69**；局部任务仍有trade-off。
- Table5部分任务训练下，模型仍可在其他任务出现负迁移（如仅Description训练时DOSE Mechanism31.76 < 未训练36.25），所以“消除所有负迁移”不成立。
- 必须区分总体分数、不同任务的可用样本分母和平均方式；不能将五任务Accuracy等权平均解释为14,128原始样本上的统一准确率。

## 5. 三项深入审计
### Q1 MCQ捷径（已实际检查公开1%训练子集）
- 文件：`data/data_efficiency/sample_1pct/train.jsonl`，**148条原始样本，其中Yes76/No72**；针对76道`target_qa`选择题统计：正确答案A=1、B=41、C=28、D=6。**固定选B可在该训练子集取得41/76=53.9%**，相比4选1机会水平25%存在强烈选项位置风险。
- 同76题：正确选项平均字符长度140.4，错误选项平均123.9；**总选最长选项在该训练子集得到50.0%**。这只是无需看图的启发式风险信号，非DOSE在完整test上的测量。
- 论文补充Figures对Random Negatives vs Hard Negatives难度有比较；说明难负例更挑战模型，**不能替代位置重排、长短控制、无图无文选项测试**。
- 需严谨关闭：在正式test统计正确答案位置、选项长度、来源与困难负样本偏差；设计question/options-only、shuffled letter位置、多次随机重排、length-controlled难负例。若要定量主张shortcut，必须在独立test而非本训练子集验证。

### Q2 正交与梯度冲突
- 源码和数学明确支持`(B_S)^T B_P`几何正交及一部分整体性能增益，但**没有直接`cos(∇L_a, ∇L_b)`测量**，无法证明“阻断任务梯度干扰”的因果链。
- 正交消融总体+2.49pp，但Target任务存在反向变化；任务子集实验仍有负迁移。需要same-budget, parameter-matched & seed-controlled消融，计算任务梯度余弦、冲突率、每任务增益及其关联，再谈机制证实。
- 本结论不否认DOSE有效，否认的是“正交=任务梯度零冲突”的过强推导。

### Q3 Ground Truth与训练协议不一致
- 代码六种任务变体，论文五项主结果；默认训练`DocMSUPlusPlusDataset`对每原始样本枚举所有有标签的MCQ实例；部分任务仅在is_sarcastic=Yes下有效，因此每条样本可贡献不同数目实例。
- 同1%公开训练子集：Detection148、Mechanism76、Dominant-Modality76、Intent76、Target-QA76、Object-QA66，**共518条有效任务实例**。该计数不等于148个独立图文输入，也不等于五任务等样本预算。
- `scripts/train_qwen_dose.py`默认`data/splits/train.jsonl`全量训练、2epochs、batch2、gradient accumulation4、lr1e-4、max_length960；而Table3使用1%数据，需要手动设置`data/data_efficiency/sample_1pct/train.jsonl`。代码默认选6任务，训练/测试任务协议须显式与论文5项比较相匹配。
- `scripts/evaluate_dose_mcq.py`默认六任务，分别按任务可用样本的选项准确率计算；必须单独说明各分母和最后加权方式，否则无法称论文表被无歧义复现。

## 6. 开放问题、复现资源与风险
- 官方README承认：标注/切分/训练入口和DOSE adapter代码公开；原始图片、checkpoint、adapter权重、基线代码/实验日志、完整超参搜索**不提供**。
- 论文附录描述单A100 80GiB的实验；不能据此假定可在共享GPU16–20GiB、≤6h完整重训8B骨干。repo自带1%划分适合未来先做样本格式与低成本静态审计，而非立即开启GPU大训练。
- 优先OPEN：完整测试集选项风格与位置捷径、模板式选项导致的模型偏差；训练任务6 vs 报告5的真正运行配置；附录正交系数不一致；参数匹配的负迁移机制验证、偏差随机种子；数据人工审校的逐任务一致性及漏标原因。
- 不得将现有MCQ成绩称为自由文本解释的忠实性或因果反事实验证。

## 7. 跨论文比较定位
- M3UCD（AAAI 2026 Main，CCF-A）：多标签细粒度基准和共享LoRA多任务统一训练；未充分证明辅助任务知识迁移。
- MGMCF（AAAI 2025 Main，CCF-A）：对象级线索、Global-Local融合与多预测分支；源/目标域输入、对比损失实现与去模态证据待审计。
- DOSE（ACL 2026 Main，CCF-A）：MCQ式多任务反讽理解与双流正交专家缓解总体负迁移；未证明参数几何正交等价于消除任务梯度冲突。
- 三篇均不能直接证明T5“图文联合构成的隐含有害”能力；MGMCF的Offensiveness只是标签属性，M3UCD类似；DOSE焦点是反讽语义和语用。

## 8. 可追溯来源
- ACL主文与附录：https://aclanthology.org/2026.acl-long.319.pdf （重点Fig4、Tables3–5、AppendixB/D）
- 官方GitHub `README.md`, `PACKAGING_NOTES.md`, `dose/dose.py`, `dose/data_utils.py`, `scripts/train_qwen_dose.py`, `scripts/evaluate_dose_mcq.py`, `data/DocMSU++_statistics.json`, `data/data_efficiency/sample_1pct/train.jsonl`。
- R1工作定义：`03_survey/R1_taxonomy/R1_Working_Framework_DRAFT.md`。
