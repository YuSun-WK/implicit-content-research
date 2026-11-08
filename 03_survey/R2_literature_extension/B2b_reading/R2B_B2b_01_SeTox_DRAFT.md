# R2-B / B2b-01｜SeTox — 中文新词隐含毒性精读工作稿

> 状态：**WORKING DRAFT，尚未用户定稿，不合并main**。2026-11-08。候选临时编号 R2A-010；不改动原有P/T编号。主任务T4安全风险检测，T1新词定位与T2新义理解是中间能力。
> 证据：A=ACL2026 Main官方论文正文与附录；B=论文所指向作者公开GitHub仓库、训练配置/数据schema的静态核查；C=本项目研究者推断。当前**没有全量模型复现，也没有完成train/test重合审计**。

## 1. 基本信息
- Shiyao Cui, QingLin Zhang, Di Wang, Yida Lu, Zhexin Zhang, Jinhua Gao, Jinglin Yang, Min He, Han Qiu, Minlie Huang. **New Terms, New Toxicity: Consensus-based Chinese Neologism Toxicity Detection via Search-Augmented LLMs**. ACL 2026 Main (Long Papers)，**CCF-A**，pp.34683–34701。DOI 10.18653/v1/2026.acl-long.1602。
- 正式论文：[ACL Anthology](https://aclanthology.org/2026.acl-long.1602/)；[PDF](https://aclanthology.org/2026.acl-long.1602.pdf)；[作者官方代码](https://github.com/thu-coai/Setox)；[HF数据](https://huggingface.co/datasets/thu-coai/SeTox)；[7B权重](https://huggingface.co/thu-coai/SeTox-Qwen2.5-7B)；[3B权重](https://huggingface.co/thu-coai/SeTox-Qwen2.5-3B)。
- **核心创新定位**：为中文网络新词的语义变化与毒性风险建立词表、共识筛查流程，并用工具调用SFT教小型LLM在必要时先搜索新词义、再进行句级safe/unsafe判断并输出理由。
- 不是新对比学习损失、RL算法，不是仅凭搜索无需训练，也不是一般隐晦信息识别的全部任务。

## 2. 概念与任务 (X,Y,G,E)
- Neologism包含**旧词产生新义**与**新词形出现**。隐含毒性可来自本来中性的表面用语在社群中衍生的贬损意义；但新词、编码词、意图隐藏与有害性相互不等价。
- 输入 X：含普通或潜在网络新词的中文句子s，以及可选外部搜索工具E。输出 Y：句子safe/unsafe标签与自然语言解释；模型可能首先定位新词t并搜索R(t)。
- G：基于974条中文网络新词人审词表和人工/自动构造的句级安全标签；不是完整自然语言社区“心理意图”金标。E：新词测试集DR/KDR/UDR、Accuracy和安全/不安全F1，普通测试集Accuracy/F1。
- **论文的“公共共识”是操作性标准**：词在Google结果**第一页前9条**中能检索到有风险的社会性解释，再由Qwen3-Max及人工检查。搜索排序/可见度不等于多数群体共识，且风险五类未必等同普适危害标签。
- 风险分五种：贬损攻击、敏感话题、违背道德、成人内容、违法犯罪。尤其“敏感话题”不是严格的hate/unsafe普适定义，综述应单独标注该审核政策假设。

## 3. 词典与Ground Truth（§3，Table1）
- 原料来源：梗百科等词库、State ToxiCN/ToxiCN既有数据、微博争议话题评论；Qwen3-8B辅助提候选。Google top9搜索片段由Qwen3-Max判风险及元数据；4名中文标注员两轮复核，产出974条包含原义/现义/来源/风险类别/解释/例句的词表。
- **标注粒度警告**：词条拥有有害用法≠每条包含这个词的句子都不安全。多义、否定、引用、科普、反讽对实例级标签都有影响。
- 公开词表964? **不是**。正式报告与README均称974条；GitHub数据说明显示词文本974条互不重复，但源ID中7个数字重复，应按词而非ID核对。

## 4. 训练与测试数据（§5.1–5.2）
| 数据 | 总计 | 具体构成 |
|---|---:|---|
| 训练safe | 811 | 511良性新词实例 + 300普通安全ToxiCN |
| 训练unsafe | 784 | 484有害新词实例 + 300普通有害CHSD |
| **训练合计** | **1595** | 995带搜索工具轨迹 + 600普通直接输出 |
| 新词test | 624 | 490 unsafe + 134 safe |
| 普通test | 368 | CHSD一般safe/unsafe实例 |
- **Known/Unknown划分**：按Qwen2.5-7B-Instruct（基础模型）先输出词义、再由人核验是否理解新义划分，测试包含319 model-known与305 model-unknown。
- **关键禁止偷换**：Base-model-unknown并不代表fine-tuned SeTox没有在SFT训练集中见过这个词，更不代表此词在论文发表后才被发明；目前正文没有明确展示train/test词项级严格不重叠。
- [公开数据校验脚本](https://github.com/thu-coai/Setox/blob/main/scripts/validate_release.py)检查test词位于974词库、数据总行数与哈希，但**不显式检查train/test的word或者sentence交集**。尚未完成逐行交叉核对，不能断言实际泄漏；必须保留该未证风险。
- 作者[数据README](https://github.com/thu-coai/Setox/blob/main/data/README.md)明确列出7个重复源ID（79,132,569,591,373,427,730）；真正词文本唯一。作者[训练观察审计](https://github.com/thu-coai/Setox/blob/main/docs/data_audit.md)使用规则标记235/995（23.62%）存在搜索失败/广告/爬取质量等疑似噪声，其中101条广告/联系方式，134条页面质量；这是**启发式**噪声线索而不是235条人工证实的错误标签。

## 5. 方法：搜索工具调用+解释监督SFT（§4, Fig2, Eq1/2）
**推理路径**：输入句子→模型判断是否涉及不明新词→必要时定位term→调用外部搜索→获得公众语境搜索结果→模型综合证据输出safe/unsafe及解释。普通文本可以不搜索。
- 论文Eq(1)任务定义：Y=M(s,E)，其中E为搜索工具。
- 训练语料分两路：
  1) 新词样本 (s,t,R,Y)：t是待查词，R是预先检索的搜索信息，Y是给定安全标签与Qwen3-Max**在已知标签条件下**生成的解释；模型学习何时调用工具、调用哪个词及依据返回的证据回答。
  2) 普通样本 (s,Y)：模型学习不调用工具直接输出安全判断和解释。
- 原文Eq(2)可形式化为 L=E_Dneo[L_neo(s,Y | t,R)] + E_Dgen[L_gen(s,Y)]。此处竖线表示条件输入而非对比学习。模型训练时仅对模型生成的**工具调用token、安全label token、解释token**优化自回归CE/负对数似然；工具返回的检索文本不是需要预测的token。**无PPO、DPO、奖励模型、RL。**
- 基础 Qwen2.5-7B-Instruct：4 epochs，lr 1e-5，max length 4096，batch 32，AdamW；作者正式论文报告**4张A100**，公开[7B YAML](https://github.com/thu-coai/Setox/blob/main/train_code/qwen2.5-7b.yaml)是LLaMA-Factory **full-SFT + DeepSpeed ZeRO3**，不是LoRA。
- [inference.py](https://github.com/thu-coai/Setox/blob/main/setox/inference.py)：工具参数term传入搜索引擎时组成“网络用语 {term} 是什么意思”；结果回填模型上下文，再生成安全标签和解释。[search.py](https://github.com/thu-coai/Setox/blob/main/setox/search.py)默认Serper外部在线搜索，提供static固定fixture及none模式。
- **协议疑点**：论文Limitations强调每句单轮查询；当前公开runner的max_rounds默认5，属于潜在“代码版本/运行配置”差异，未据此断言论文真做了多轮搜索。
- 解释质量≠忠实：上游Qwen3-Max已知真实label才生成解释，可能带label-conditioned合理化；若把错误搜索摘要替换输入，是否影响最终标签尚未经严格验证。

## 6. Baselines、结果与消融（§5，Table2/3，%）
| 方法 | 新词不安全检出DR | 新词Accuracy | 基座不认识词的UDR | 普通文本Acc |
|---|---:|---:|---:|---:|
| Qwen2.5-7B-Instruct | 62.10 | 70.43 | 52.44 | 93.17 |
| Qwen3-8B | 76.96 | 80.53 | 71.72 | 92.93 |
| Qwen3-Max（只提示无搜索） | 85.84 | 88.96 | 81.30 | 92.83 |
| Gemini-3-Flash Preview（只提示无搜索） | 91.83 | 92.94 | 91.52 | 91.82 |
| **SeTox-7B** | **92.86** | **94.07** | **94.07** | **93.21** |
- 两个94.07是不同指标：新词全体test Accuracy、基座模型原先不认识的新词unsafe recall (UDR)，不应合并口径。新词test的unsafe比例为490/624，超过78%，故应同时读Acc和F1，不只读DR。
- **不对称比较**：相同量级Qwen是“无SFT、无搜索”提示基线；SeTox是额外SFT且可检索；更大模型亦只提示无搜索。因此表格不能单独归因于搜索，更不能跨领域宣称全面胜过所有大模型。
- 7B消融(Table3)：有搜索 DR/KDR/UDR 92.86/91.73/94.07；无搜索87.63/90.71/85.19。**UDR下降8.88百分点**，有利于支持在该实验设置下工具调用带来增益。
- 但是“无搜索”变体的训练文本仍可能包含用搜索结果生成的解释，所以这不是完全剥离外部web知识的因果对照。
- 附录A词项定位 Table4：7B Soft Match **90.87%**、Hard Match **74.68%**；存在不少未准确定位的情形。附录C人类对100句解释的主观一致性评价7B约**92.0%**，不能证明每个决策真正因果依赖检索。
- 论文错误分析：知道新词贬损义仍误判句子整体语用（contextual misinterpretation）；模型安全政策与实际规范不一致（criteria misalignment）；检索span错误。

## 7. 可复现性、实现对照与研究约束
- 作者[GitHub README](https://github.com/thu-coai/Setox/blob/main/README.md)提供源码、数据包及3B/7B权重，整体比FA-Net更容易开展低成本验证。但**README的BibTeX条目目前与官方ACL题名、作者、页码不一致**；所有参考文献应以ACL Anthology正式出版信息为准。
- 作者自述的训练工具观察噪声可能影响复现与搜索可靠性；公开检索后端依赖Serper API，未经确认不可假设免费/无限调用。
- 用户共享4090且目标16–20GB/≤6h：**推荐只做开源3B权重+static fixtures小子集的推理审计**，不要默认重训full-SFT Qwen7B或重复4×A100条件。模型权重本身能否在可用窗口准确跑通需另测。
- 待核：①train/test term-overlap, sentence-overlap, template-overlap；②新词未知是基座已知还是SFT未见；③搜索时间/来源/结果漂移；④搜索错误与相反证据对标签的影响；⑤纯SFT vs检索 vs训练解释的同预算拆分；⑥token成本与实际调用频次；⑦政策敏感项的跨场景可移植性。

## 8. 与B2a/P023/P020的关系（不能混评）
| 论文 | 主要输出 | GT性质 | 映射 |
|---|---|---|---|
| Silent Signals, ACL2024 Main, CCF-A | 已知Dog Whistle用例是否编码义 | 词项/定义+局部人工WSD/自动标注 | T1/T2 |
| FETCH!, ACL2025 Main, CCF-A | 从种子找**其它词项类型** | 词典held-out type match | T1 |
| FA-Net, AAAI2024 Main, CCF-A | 遮蔽委婉语的预设目标义类别 | 词典映射+无标签target域适应 | T2 |
| **SeTox, ACL2026 Main, CCF-A** | 新词含义辅助的**句子风险标签**+解释 | 人工核对词表+安全标签+搜索证据 | **T4**，T1/T2中间能力 |
| P023 CodedLang, ACL2026 Main, CCF-A | 编码检测、变换机制、部分解码 | 中文真实评论与标注 | T1/T2 |
| P020 RSA², ACL2025 Main, CCF-A | 策略条件下意义推断 | 候选意义与人类判断 | T2/T3关联 |
- **综述的核心句**：检索到词语某种编码含义，不足以判定其在具体语境中就是攻击/有害；新词义恢复与句级风险判定需要不同GT。

## 9. 创新性及结论
- 本文的核心价值是**动态新词隐含毒性这个特定任务定义、974词项审查及教模型在决策时主动查词的工具使用监督**。不是首次引入RAG，也没有独特的新的数学损失。
- 在作者的数据和基线条件下性能很强，但“未知新词”是相对于基座模型知识的操作划分，**不等于经严格类型留出和时间切分验证的未来新词泛化**。
- 最大审计阻断项：按词项级train/test去重；公开工具噪声；证明解释有证据忠实性；评判“共识”是否真正成立及不同安全政策下的ground truth兼容。
- 未证创新空间（非新idea成立）：已查对词义但错判整句风险、搜索结果污染与误导、不可靠词义与政策规则的耦合。

## 10. 证据
- [ACL2026官方PDF](https://aclanthology.org/2026.acl-long.1602.pdf)：§2–5，Table1–3、Fig2、Appendix A/C/D/E/I；
- [源码](https://github.com/thu-coai/Setox)：README、data/schema.md、data/README.md、docs/data_audit.md、train_code/qwen2.5-7b.yaml、setox/inference.py、setox/search.py、scripts/validate_release.py。
- 所有结果数字为作者报告，**尚未复现实验**。训练-测试词项重叠目前是“未核验”，不是已确认数据泄漏。
