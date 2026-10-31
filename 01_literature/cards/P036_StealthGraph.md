# P036｜StealthGraph: Exposing Domain-Specific Risks in LLMs through Knowledge-Graph-Guided Harmful Prompt Generation

> **2026-10-31 用户明确授权定稿、上传、合并。** 定稿为正式论文+公开代码+部分公开数据文件静态审计；**未运行作者70B生成流水线、未重新计算主表ASR、未独立人工复核全部标签**。论文结论/源码事实/研究者推断须区分。

## 01. 书目信息与材料
- Huawei Zheng, Xinqi Jiang, Sen Yang, Shouling Ji, Yingcai Wu, Dazhen Deng. **ACL 2026 Main（CCF-A）**，pp. 6519–6539；DOI **10.18653/v1/2026.acl-long.295**。
- 正式页 https://aclanthology.org/2026.acl-long.295/ ，正式PDF https://aclanthology.org/2026.acl-long.295.pdf （21页）；官方仓库 https://github.com/ZJUIDG-AIVA/StealthGraph 。
- 已读论文 §3.1–3.3（含 Algorithm 1）、§4.1–4.5、Appendix I/指标与消融；静态读取 README、real_pipeline/step1–7、src/services/implicit/implicit_generator.py、evaluation/asr_evaluator_service.py、step5_implicit_jailbreak.py、step5_optimized_batch.py、experiment/exp1_dataset.py、exp4_ablation_kg.py、exp3_dataset及exp4_dataset的部分JSON。

## 02. 研究问题和任务边界
- **任务是生成并评价领域相关、语义意图保留但表现形式较隐晦的安全压力测试请求**，非将隐晦文本输入并判定有害/无害的分类器；输出主要为生成请求、改写文本、模型安全失效判断与数据元信息。
- 研究动机：(a)一般安全数据集专业知识覆盖不足；(b)显式有害措辞较易被识别/拒绝；医学、金融、法律和教育中的间接专业表达可揭示安全评测短板。
- 该工作不建立真实人类统一标签的隐晦毒性正负样本；**Attack Success不是文本Harmfulness Ground Truth**。

## 03. 系统流程/算法
1. **KG数据取得**：Wikidata领域根实体和关系 P31 instance of、P279 subclass of、P361 part of、P527 has part；SPARQL检索并以百科页面覆盖近似筛选知名度，Neo4j承载图谱。流行度/实体数不等于风险等级。
2. **KG-conditioned生成**：领域实体及相关信息+风险类别示例作为生成模型输入，得到领域风险候选；Granite Guardian 给unsafe/safe评分，辅以文本质量/PPL等评估和过滤；自动模型评分不是人工标签。
3. **双路径改写**：Direct路径与Context-card路径交替选择；各有独立当前文本状态；改写模型生成新文本，质量门控检验 intent_preserved 和 is_fluent；通过才更新该路径，并测试某个目标模型的安全响应，成功即提前退出；失败进入下一轮/回退，最多N轮。
4. **完成与复核**：Step5输出含成功/失败状态及候选元信息；Step6整理；Step7再次审查潜在危害、意图保留、之前成功样本响应是否真的不安全。生成流程非PPO/GRPO，不存在通过ASR反馈对模型参数做策略梯度；存在输出选择与停止条件。

## 04. 双路径 Algorithm 1 和公开代码审计
- 主实际代码 real_pipeline/step5_implicit_jailbreak.py::_dual_path_stealth_rewrite：初始化 basic_prompt=original_prompt、enhanced_prompt=original_prompt；轮次偶数使用basic、奇数enhanced；保存 best_candidates，质量通过才更换当前路径状态；目标模型回答与ASR Judge决定是否提前成功退出，失败反馈及触发词在路径间共享。
- real_pipeline/step5_optimized_batch.py 的 worker 实际委托给上述 DualPathStealthProcessor，并行/断点恢复并没有替换核心算法；不能从名字推断是另一种训练方法。
- **当前实际质量门控主要是 Gemini类模型两个布尔判断**，不是严格连续的真实相似度和GPT-2 PPL阈值。src/services/implicit/implicit_generator.py 把 intent_preserved=True 映射 similarity_score=1、False为0；is_fluent=True映射所谓 ppl_score=10、False为200，这些是**兼容旧接口的代理值**而非实测连续分数；论文的分析指标可另计算真实PPL/余弦。
- **回退差异**：论文语言称最大迭代失败选最优候选；代码主要调用 _select_best_candidate_gemini()，先保留质量通过的候选再按**最大iteration**取最近一条，完全没有合格候选时退回最新候选，非按全局质量score排序。代码中另有按相似度/PPL排序的旧函数，但与主要流程调用不同。
- 失败保留：Step5与Step6明确区分 successful、failed_with_prompt、failed_no_prompt；Step6优先加载完整结果文件而非只有成功记录，若只找到成功文件会给出告警。后续实验成功子集的筛选须与完整记录分开。

## 05. Step7质量检查/真实公开报告
- real_pipeline/step7_quality_check.py 有Check1（改写是否仍存在潜在风险，失败删除）、Check2（意图是否一致，失败删除）、Check3（仅对先前判断成功的记录重新检查对应目标模型响应，失败则**保留记录但下调成功标志**）。当前最后校验通过OpenRouter访问Gemini 2.5 Flash。
- **fail-open疑点**：某些Judge调用失败时函数返回 True + 'Evaluation failed, keeping record by default'，并非所有失败调用一律严拒；这仅证明代码有风险路径，未实际统计发生次数。
- 从仓库 exp3_dataset 四领域的 step7_quality_check_report 实际读取统计：医学输入1023/保留924/成功前451后297；金融836/731/576→358；法律947/849/514→338；教育735/659/410→273。**合计输入3541、保留3163、前成功1951、后成功1266，减少685（已纠正此前回答误写1366的算术错误）**。复核成功数减少包括过滤与重判两类因素，不能一概当成纯错误纠正。

## 06. KG去除消融及其真正证据
- Appendix I/Table15报告 No-Guided Self-BLEU=38.95，KG-Guided=32.98，差值−5.97；Self-BLEU衡量同批文本表面重复程度，**不是实体覆盖、知识真实性、图关系因果作用和安全金标**。
- 公开 experiment/exp4_dataset/kg_ablation/ 两个JSON各200条；亲自读取字段并对distinct做静态统计：KG组不同node_name=96、不同wikidata_uri=97；No-KG组仅各10；共有的名称10、URI10；两组prompt_id交集4。KG组10个风险类别量不完全相同，No-KG组每类20。
- exp4_result JSON公布 embedding-based diversity KG=.7613374591、No-KG=.6291790009；Self-BLEU KG=32.9837812317、No-KG=38.9455699539；公开 exp4_ablation_kg.py 只读备好的输入并算embedding/self-BLEU，**没有实现同实体/同预算生成的严格对照**。
- **关键混杂**：两组实体覆盖与类分布不同，可能天然影响文本多样性；最终各200条不证明实际生成次数、token预算、过滤成本一致。现有证据支持“两个发布方案下KG组更有词汇/embedding多样性”，不充分证明图谱边关系相对相同实体描述必不可少。建议 A领域名、B同实体列表、C同实体+文本描述、D同实体+KG关系，固定种子/预算/类别等消融。

## 07. 数据版本、ASR和筛选偏差
- 论文表1 SG-Origin=候选原始文本；SG-Implicit=改写文本；SG-Implicit✓=按前期攻击效果筛选的成功改写子集。六个评测模型平均ASR依次15.17% / 61.58% / 84.92%。**84.92%是条件化选择后的分布，不能全归因隐晦性增加**。
- 改写时目标模型Llama-3.1-8B-Instruct；最终Table1六个不同待测模型不包含它，减弱同一目标模型过拟合问题，但迁移评测并未取消按成功样本筛选造成的难度偏置。
- experiment/exp1_dataset.py：SG-Origin与SG-Implicit分别从同一个StealthGraph_random_data.csv的original_prompt和stealth_prompt字段读取，SG-Implicit✓使用单独的StealthGraph_stealth_random_data.csv；随机至多抽200条；公开仓库当前未见对应路径里的这两份CSV，**无法独立核对表1最终200个ID和逐对重合**。
- 当前评测脚本三裁判：Gemini 3 Flash、Claude Sonnet 4、GPT-5 Mini，多数票≥2为成功；前期改写评审含Gemini3 Flash，**评审器并非全部独立**。论文Appendix E StrongREJECT替代评测下平均ASR三组18.8% /69.4% /85.5%，加强排名稳健性但无法消除筛选偏差。
- 当前版本Step5、Step7不同阶段使用Gemini 3 Flash/Gemini 2.5 Flash等，必须记录commit和调用配置，不能将所有LLM-Judge视作同一固定评测器。

## 08. 安全微调及主实验
- 论文Table3：Llama3.1-8B使用不同来源的200对风险请求/安全回应做SFT/QLoRA，SG-Implicit✓测试ASR AdvBench55.5、Do-Not-Answer66.0、SG-Origin25.0、SG-Implicit12.0，说明领域/隐晦训练数据可能改善针对性防御，但需审查同源实体与文本近重复。
- MMLU Table4未微调49.75，AdvBench43.59、Do-Not-Answer43.01、SG-Origin43.41、SG-Implicit42.68、SG-Implicit✓42.71；安全SFT均比未微调明显下降，不能声称能力没有损失。
- 双路径OSR Table7最大迭代10/18/30：Direct28.25/36.56/42.23%，Context25.81/33.14/37.93%，Dual29.03/36.75/45.06%。迭代10和18的双路径相对Direct仅+0.78/+0.19百分点；还需匹配调用数量验证独立价值。

## 09. 标签可信/任务边界裁决
- Granite Guardian unsafe分数、Gemini意图保留/流畅度布尔、目标模型ASR、最终模型Judge票数都是不同代理监督；任何一者都不是独立专家判定的隐晦有害文本ground truth。
- 该公开数据可用于安全压力测试（待测模型响应是否越界），**不能直接当成自然发生的隐晦有害信息二分类标准数据集**，尤其缺高质量无害同实体/同语境对照，存在筛选后分布及相似文本重叠。
- SG-Implicit✓的成功标签随目标模型与评审规则而改变；同一请求在模型A成功拒绝、模型B不安全回答，不表示文本本身风险标签发生变化。应保持harmfulness-vs-ASR的严格分离。
- 合适定位：领域风险数据生成/安全评测研究工作，和广义隐晦检测高度相关，但并非直接可用的检测方法或可信正负金标。

## 10. 复现成本与可达性
- 官方README要求Neo4j/Wikidata、vLLM、多阶段生成、70B微调生成/改写模型、8B Granite Guardian、第三方商用评审模型与A100级实验预算；用户约束共享4090/4090D、单卡16–20GiB、≤6小时Kill Test、免费公开数据不支持直接完整复现。
- 已在GitHub定位 exp3_dataset四领域下的step3、step7 JSON/CSV与质量报告；静态数据审计（无训练）可行，须预先检查字段/标签命名/来源ID并避免把步骤成功当真值。先不要运行70B流水线。

## 11. 反向审稿及最小Kill Test
1. KG归因：比较相同200实体/相同类别/相同预算下的entity-list、entity-description、full-KG关系，对Self-BLEU、Embedding Diversity、实体关系覆盖、过滤率和Judge评分同时报告。
2. 代码协议：对少量非敏感占位文本用mock方式测试基本/增强路径状态保留、质量失败时不更新、最近候选fallback和Step7 fail-open；避免直接运行可能生成危险请求的实战测试。
3. 数据统计：现有公开JSON/CSV按original_prompt_id/group/domain/entity/parent/quality/stealth_success审计，筛查近重复与测试集选择偏差，必要时抽查专家语义与风险。
4. 低成本推断：冻结公开安全模型，在可信既有标签/合理对照上比较显式—隐晦任务差距；区分拒绝率、危害识别准确率、被评审判为攻击成功的ASR。
5. 原文不证：图结构独立贡献；完整表1具体样本ID、配对协议；所有质量评审成功执行；自动标签金标性；跨实体跨域泛化与安全SFT训练测试独立性。

## 12. 定稿与下一阶段
- **2026-10-31 用户明确授权P036定稿上传合并**；该卡保留静态核验与未复现边界，归档为 ACL 2026 Main / CCF-A 的领域安全数据生成与评测方法。
- 结束既定第二批 P027→P013→P022→P035→P036 的核心CCF-A正式精读；**不机械追求完成其余全部36篇**。下一阶段应新开研究窗口做第三阶段R1（横向机制-数据-评测矩阵，非第一阶段R1–R5重复）、R2（直接竞争工作与否证审计）、R3（至多2个可证伪研究假设与公开数据/代码单卡≤6h Kill Test）。
- 并行数据可达性核验+竞品机制审核，重点比较 P013/P022/P035/P036 与 P027/P034、P017/P033、P019；优先考虑广义隐晦安全判断是否因词义语境/跨模态关系失效，而不是只提升语言生成ASR或多写解释。