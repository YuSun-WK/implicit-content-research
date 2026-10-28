# P029｜RV-HATE：Reinforced Multi-Module Voting for Implicit Hate Speech Detection（定稿；问题未关闭）

> **记录状态**：2026-10-28 用户明确授权“定稿、上传、合并”。这是**已定稿的阅读/静态审计记录**，**不是论文机制全部获证实**，也**不是复现通过**。下列严重问题不得因“定稿”而删除。未下载数据、训练四个分类器或运行 PPO；代码审计基于公开仓库 main，并核对部分历史分支。无作者实验原始权重/日志。

## 1. 文献信息及研究定位

- **论文** Yejin Lee, Hyeseon An, Yo-Sub Han. *RV-HATE: Reinforced Multi-Module Voting for Implicit Hate Speech Detection*. **ACL 2026 Main Conference Long Paper**，pp. 45364–45383；DOI：10.18653/v1/2026.acl-long.2104。
- **正式页面** https://aclanthology.org/2026.acl-long.2104/ ；**正式 PDF** https://aclanthology.org/2026.acl-long.2104.pdf ；**公开代码** https://github.com/leeyejin1231/RV-HATE ；2025 arXiv 预印本 https://arxiv.org/abs/2510.10971。
- **研究任务**：IHC、SBIC、DYNA、Hateval、ToxiGen 上的各数据集二分类；标签语义不完全统一。研究“隐式仇恨”相关分类基准，并非显式恢复隐藏命题、语用含义或潜在攻击目标；**非跨数据集未见机制泛化证明**。
- **核心设想**：各数据集语言/标注特点不同；先按 M0–M3 四种训练策略训练独立 BERT，再做数据集级加权 logits 集成。创新集中于模块组合和 PPO 权重优化，而不是端到端语义推理。M0 基于 SharedCon，M3 参考 LAHN；需要将基线贡献与新设计分开。

## 2. 输入、训练、推理 Pipeline

输入：(x,y) 文本及二分类标签，外加无监督 SimCSE 向量、簇标签/簇代表；M1 使用 NER、GPT-4o 辅助目标标记；M2 使用 IQR 删除离群训练样本；M3 使用动量编码器/队列采困难负例。

1. **M0 聚类对比学习**：分别按类别用预训练 SimCSE 得句向量；sklearn KMeans 分簇（不是 spherical KMeans），按簇中心与样本的**余弦相似度**选一个真实代表文本（centroid sample）。原文 x 与簇代表 a(x) 共享 BERT 编码，训练 CE（仅原文）+ 簇标签约束的对比损失：L=λ L_CE+(1−λ)L_CL。默认 λ=0.5、τ=0.3。对比损失使用归一化 [CLS] 隐状态。
2. **M0 对比的精确定义（已检查代码）**：batch 原文视图和代表文本视图拼为 2B；`SupConLoss` 先通过 `labels_i==labels_j` 构造 mask，随后只保留**跨视图同簇正样本**；分母仍包括除自身之外的其他样本（包括同视图同簇），并非把簇内所有样本作为等价正例直接彼此拉近。由此**间接鼓励**原文与本簇代表接近，不保证所有簇内样本同一位置。聚类相似≠隐含意义等价；无证明这种约束改善语用推理。
3. **M1 目标标记**：spaCy NER 与 GPT-4o 补充，给识别的群体/实体插入 [TARGET]，在扩展输入上训练 BERT。NER 提及实体不等于语义被攻击对象，遗漏隐含目标也可能存在。论文披露的额外 API 监督不满足完全无付费 API 重现的前提。
4. **M2 离群点处理**：簇内距离 d 到中心，IQR 阈值 Q3+1.5IQR，删除较远训练样本；不等于证明这些样本标签错误。Table 11 各训练集删除约 0.31–0.69%；稀有真实隐晦表达可能被错误删除。
5. **M3 困难负样本**：LAHN 式动量编码器/跨 batch 队列，基于标签相反、余弦相似度较高、模型分数等选择负样本，优化 CE 与对比目标。困难负例可能包含标签模糊/错误，需独立审计。
6. **PPO 加权投票**：分别在四模型上得 z_k(x)∈R²，输出 argmax_c Σ_k w_k z_k,c。w≥0、Σw=1。代码中四维状态/动作，权重裁剪正数后归一化；单步 episode；奖励 R=2(F1−F1_baseline)，使用 SB3 PPO MlpPolicy；训练期间四个分类器冻结。学习的是**每数据集的四个静态权重**，并非每条文本动态模块路由，也非训练 BERT 进行解释。
7. 推理仅需文本和四个训练好的模型/权重，不需要真实类别与解释；M1 文本预处理是否一致须另核。

## 3. 实验证据及归因边界

- **论文 Table 1，五数据集 IHC/SBIC/DYNA/Hateval/ToxiGen Macro-F1**：BERT/CE [77.70,83.80,78.80,81.11,90.06]，平均82.29；SharedCon [78.50,84.30,79.10,80.24,91.21]，平均82.67；LAHN平均82.57；RV-HATE [79.07,84.62,81.82,83.44,93.41]，平均**84.47**；数据为论文报告、非独立复现。
- **论文 Table 2**：单模型融合四策略平均81.64，四独立模型等权投票83.78，PPO投票84.47。PPO对等权的**平均增益0.69 F1百分点**，不能把 RV-HATE vs SharedCon +1.80 全归因于 PPO；未见相同数据划分/预算下 grid/random/Dirichlet、Bayesian 等简单权重搜索对照。
- **论文 Table 3/图**：作者的移除模块/单模块消融与 t-SNE 支持报告设置下模块互补性及表示变化，但不足以证明每个模块正确建模相应语言机制、或“隐含意义理解”改善。
- **标签/数据**：IHC implicit hate vs SBIC offensiveness vs Hateval/ToxiGen/DYNA hate 不是同一 Ground Truth 定义；跨基准数字并不直接等于独立跨领域迁移。未排除簇主题捷径、代表文本错误、训练集删除导致的分布变化。论文 GPT 自动标记/检查不等于完整人工真值。

## 4. 公开代码静态审计：必须保留的未解问题（重点）

**[CRITICAL | 可由当前代码直接证明] 测试集标签泄漏到 PPO 奖励**：`ppo_eval.py` 创建 `EnsembleEnv(test_data, models, f1_baseline=f1_baseline,...)`；环境预缓存该 split logits 和 **labels**，`step(action)` 在其上计算 Macro-F1 并作为 reward。之后仍调用 `test(test_data, models, optimal_weights,...)`。这是**测试集上调权再在该测试集评价**，不符合论文所述验证集寻权→独立测试评价。更换为 `EnsembleEnv(valid_data,...)` 是最小协议修正。该静态证明只针对当前公开脚本；**不得据此断言作者发表时的实验实际使用相同版本或成绩虚假**。

**[HIGH | 当前实现索引不一致] M0 聚类代表索引**：`utils/clustering.py:get_center_post_idx_with_cosine` 对单簇局部 `cluster_post` 取 argmax，返回的是局部位置；`utils/shared_semantics.py` 随后使用 `dataset[input_col][idx:idx+1]` 当成全局位置取句子。结果可能是**非对应簇**文本。需修正索引映射，统计簇归属和重训敏感性。

**[HIGH | 管线错配/运行待核] M1**：`config/train_config.py` 中 `use_ner=True if type=="ner" else False`，而 README/预处理用 `m1`；`ppo_eval.py` 用 `type="m0"` 加载一个 shared evaluation dataset 给四模型。M1 标记后的 tokenizer、加词表 BERT 与实际评测是否保持一致未被当前入口保障。 `utils/shared_semantics.py` 的 M1 `use_ner=True` 分支使用 AutoTokenizer 代替 SimCSE 句向量对象，`utils/clustering.py` 又以 `if use_ner == "True"` 判断布尔值；存在类型/输入不匹配风险。需实测有效目标覆盖与输入 ID。

**[HIGH | 运行阻碍] M3**：`train_hard_negative.py` 多处用 `log.parma.gpu_num`（笔误），以及扩展词表/权重加载等配置差异；不能宣称代码一键复现 M3。注意静态检查未尝试运行作者所有历史配置。

**[MEDIUM | 论文与默认代码]**：论文 §4 报 PPO **10,000** steps，`config/eval_config.py` 默认 **100,000** steps；Table 12 IHC 权重0.191+0.258+0.167+0.357=0.973，超过正常舍入误差，且表头把 M3 写成 M4；原文另有 PPO 参数数量描述不一致处，均需核对脚本版本/作者权重与报告。

**[HIGH | PPO 必要性尚未证实，非代码错误]**：权重问题是 4 维 simplex（仅3个自由度），一步 episode、固定 logits，是低维静态调参；无同预算非RL 搜索对照。是否“PPO优于简单搜索”目前**未知**，不能写“PPO不如随机/网格”或“已证实无创新”。作者公开库没有直接提供训练好的四模型 logits/checkpoints（根据仓库树/Release 的既有检查）；后续应先确认可导出 logits。

## 5. 最小可证伪实验与资源审计

**零训练协议审计优先**：冻结相同四模型，对固定 train/validation/test 划分导出形状 [N,4,2] 的 logits 和标签；只在 validation 上寻找权重；比较 equal / best-single / grid(步长0.05共1771种) / Dirichlet random(固定预算) / corrected PPO(相同目标与随机种子)；独立 test 仅报告结果，按不同随机种子给均值和方差。避免在 test 上二次调权。预处理与 checkpoints 不可靠时先检查输入一致性，不要解释异常 F1。
**低成本簇机制审计**：每簇全局索引映射正确性、簇内/簇间正样本比例、同簇语义一致性、同簇跨视图与仅标签对比的对照。修复程序不等于发现科学创新。
**实际开销**：四个 BERT-base 独立训练和四次推理；作者 Table5 报 IHC 各模块约1h、PPO5–10min，但依赖输入/权重/版本、共享 GPU 不保证 16–20GiB/≤6h 完整复现。M1 依赖商业 API，不满足无收费 API 的全流程复现；可研究不依赖外部 API 的子实验，不声称复现作者完整设置。

## 6. 与 P032/P024/P030 的定位及审计结论

P032 ImpCon 使用已有 implied statements 作为**语义对齐监督**；P024 CONELA 用训练动态+人工分歧作**数据选择**；P030 SMARTER 用 HateCOT/seed explanations/自动偏好对做**LLM post-training**；P029 使用簇代表/目标标记/离群删除/困难负样本及 PPO 进行**表示学习+模型集成**。相同点均可能改善分类 F1，但没有任何一篇的分类增益自动证明语言学意义的隐含意义恢复。

**定稿结论**：原文叙述、公式、模块和静态代码已形成正式记录；**复现未完成**。对“PPO相对非RL最优权重的必要性”“M0/1/3代码-论文一致性”“当前公开 PPO Test-set leakage”的标记保持开放，不能作为可靠语义机制或严格独立测试提升的既定证据。**后续优先小型机制/协议审计，而不是直接从 bug 推演新 Idea**。

## 7. 证据锚点

- 正式 PDF：Figure 1；§3.1–3.5；§4；Table 1–5；附录 Table 10–12。
- GitHub（公开 `main` 已静态核对）：`ppo_eval.py`、`model/loss_sharedcon.py`、`utils/clustering.py`、`utils/shared_semantics.py`、`utils/preprocess_dataset.py`、`utils/dataset_loader.py`、`train.py`、`train_hard_negative.py`、`config/train_config.py`、`config/eval_config.py`。
- `dev`、`feat02-reinforcement` 分支 `ppo_eval.py` 曾比对相同的 `EnsembleEnv(test_data,...)` 行，未检查所有提交历史。
