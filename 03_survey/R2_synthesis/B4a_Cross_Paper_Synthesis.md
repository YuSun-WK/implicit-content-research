# R2-C｜B4a 多模态情境安全、输入风险感知与过度拒答：跨论文综合

> 2026-11-08｜R2-C 综合审阅稿。依据 B4a 三篇已定稿卡片及 P034/P037–P041 既有精读；没有在此轮重新运行模型、下载全图、使用商业Judge或复核每条人工标注。保留 **R2A-027/028/029** 临时号；不改变原始R1和阅读卡。

## 1. 三篇研究不是同一个问题

| 原始编号与正式出处 / CCF | 风险和响应被如何定义 | 真正测量什么 | 主要证据风险 |
|---|---|---|---|
| **R2A-027** [*Multimodal Situational Safety*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html)，**ICLR 2025 Main，A** | 活动/用户请求 Q 在视觉环境 V 中是否适宜执行；论文1,960 image-query pairs，980 safe/980 unsafe | Instruction Following（IF）回答行为；另有QC、IC显式安全判断诊断及多agent prompting | IF judge对回应模式评分，并非读图判断风险；Chat有同query换图，Embodied部分连指令一起变 |
| **R2A-028** [*Is Your Multimodal Language Model Oversensitive to Safe Queries?*](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html)，**ICLR 2025 Main，A** | 300个作者视作benign的图文问题，观察回答是否发生拒绝；另有244个危险修改对照 | 安全输入过度拒答（ARR），不是独立的风险二分类 | AMT多数意见中约9%认为不能无害回答；300与正文残留544、244配对的范围要分开 |
| **R2A-029** [*Can’t See the Forest for the Trees: Benchmarking Multimodal Safety Awareness for Multimodal LLMs*](https://aclanthology.org/2025.acl-long.832/)，**ACL 2025 Main，A** | image/text/joint语义相互影响，1000不安全+500过安全，目标是输入 Safe/Unsafe | 直接回答“图文输入是否安全”；两侧召回 | 公共仓库prompt 1,523、对应编号图片1,453、仅445不同图像Blob，与论文1,500条不一致 |

**核心裁决**：MSSBench研究环境约束下是否应行动；MOSSBench研究对安全请求是否无谓拒绝；MMSafeAware评估输入安全分类。这三类指标不能合并为“安全识别准确率”。

## 2. 从输入风险到输出策略的分层

应至少分开以下五个变量：
- **G_in**：输入在规定政策和环境下的Safe/Borderline/Unsafe真值；需要独立GT与规范说明。
- **P_in**：模型预测的输入风险标签；可计算危险召回/FNR、安全召回/FPR、Balanced Accuracy。
- **R_beh**：输出行为属于拒答、解释危险并警示、直接协助、能力不足等；属于行为评测。
- **Q_out**：真实回答是否造成不安全帮助、是否充分解决合法请求（Safety+Helpfulness），与单纯拒答不同。
- **D_modal**：预测是否依赖关键视觉/文字事实；需同模型跨模态干预，单看成功率不足。

在正类定义为Unsafe时：
- 风险漏检=GT Unsafe且模型判Safe（FN）；风险误报=GT Safe且模型判Unsafe（FP）。
- 过度拒答=Safe输入却拒绝（输出行为层）；即便模型输入分类正确也可能因策略拒绝。
- 漏拒绝或危险回答=输出层安全失败；不能仅凭输入分类测得。
- 过度保守策略可能增大Unsafe召回/拒答率、同时显著损害Safe通过率；应看**双侧指标、阈值与平衡准确率**。

## 3. 最重要的 Ground Truth / 协议核验

### 3.1 MSSBench：风险识别与 IF judge 不能偷换
- **P**：正式ICLR论文为1,960条（Chat 1,200；Embodied 760），既有旧项目资料1,820为版本差异；Chat公开脚本可见固定query+安全/危险两图，Embodied部分使用不同safe_instruction与unsafe_instruction。并非全部“只换图片就翻转标签”。
- **S**：既有卡核查的 GPT-4o response-judge 仅看回答，rubric将“安全场景下因能力不足不答”label3归为correct，将“危险场景下无安全理由拒绝”label0也归为correct；评审prompt还预设询问属于危险情境。故**IF correctness可高估有用性和真实风险理解**，这一解释来自公开评分定义；不表示作者论文数值一定错误。
- **P**：多agent和Oracle关键环境状态提升部分模型表现，能作为视觉状态感知可能是瓶颈的**行为证据**；GT caption/关键状态增加了额外信息，非公平同输入方法。
- **O**：批量运行脚本当前静态存在导入/作用域/分类解析潜在问题；尚未実跑确认。需分开QC/IC分类和IF回答而非复用同一judge。

### 3.2 MOSSBench：误拒不等于正确理解
- **P/S**：作者正式摘要/公开JSON为300 safe案例，三类诱因各100：Exaggerated Risk、Negated Harm、Counterintuitive Interpretation。AMT报告平均harmfulness 1.84/5，但约9%多数认为不能安全回答；此类判定分歧不能简单忽略。
- **S**：244条harmful contrast可与300主集PID匹配：**198**同图异文、**43**同文异图、**3**双变化，**56**个主样本无对应contrast；仅部分对照构成严格单因子干预。
- **P**：某些历史模型在text-only时拒答更少，暗示视觉刺激与拒答相关；但“视觉删去”也减少必要语义信息，既不能证明原先误拒都是视觉理解错误，也不能证明改善拒绝率即改善安全判断。
- **O**：主数据安全GT的人评逐例票未公开，拒答的自动Judge和真实有害回答质量需要独立验证；测试集作者明确禁止用作训练。

### 3.3 MMSafeAware：平衡指标优于原始总Accuracy
- **P**：正式论文设计Unsafe 1,000、Over-Safe 500，声称分别满足某种单模态/联合风险关系；三路人工审核用于**构造筛选**，主评估只输出联合Safe/Unsafe，不等于对外发布完整三路逐例GT。
- **S**：现有卡核验公开主仓库的prompt编号1,523、对应图片1,453（缺70个编号图）、图像Git Blob唯一445；公开版本难以与论文1,500完全一一对应。重复图片可用于语义组合，但**不是IID图像样本**；需要按图像分组统计置信区间。
- 论文目标2:1不均衡：**总判Unsafe**就有66.67%总Accuracy但Safe Accuracy=0；必须同时报告Unsafe Recall、Safe Recall、Balanced Accuracy（恒判Unsafe基线为50%）。输入误报不等于模型生成拒答率。
- **P**：安全系统提示、视觉对比解码及视觉中心微调能改变两组表现，有的降低误报同时扩大漏检；方法系既有技术迁移，不是本文新提出的跨模态因果训练方法。
- **O**：公开标签与图像文件版本、论文Tables不同条件基线、实际Judge解析、版权和类别一致性需核。

## 4. 模态联合依赖到底如何证明

**三篇的输入与辅助监督强弱不相同**：
1. MSS Chat：同query+两场景图可作自然干预，但仍要检查意图与实际query是否一致；Embodied混合变化，需筛选同指令配对。
2. MOSS：部分安全图文需要否定、指代、物体真伪语境才能避免误拒；**Safe joint输入不是joint harmful**；没有逐项 y_I/y_T/y_joint正式安全三标签。
3. MMSafeAware：更直接关心joint输入标签，同时有设计层三向标注规则；实际发布逐例三向标签缺失，重复图和文件缺口妨碍公平对照。

建议报告的实验矩阵：同一冻结VLM上 joint(I,T) / text-only / image-only、同query对图、同图换问句、成对反事实（若GT已由人工核验），再分层观察**标签翻转正确率、漏检、误报、警告/拒答/安全且有用输出**。没有新人工GT时，图像shuffle只测**预测敏感性**，不能延用原配对的真值。

## 5. 与已有高水平工作避免重复（按原始编号）

| 现有证据 | 正式出处与等级 | 与B4a的区别 |
|---|---|---|
| **P034 CrossGuard** | [ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1178/) | 联合隐含风险输入Guard和PPO样本改写；生成奖励的论文/代码机制差异待审计 |
| **P037 VLSBench** | [ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.405/) | Visual Safety Information Leakage；主要测回应安全性而非输入分类 |
| **P038 VLSU** | [ICLR 2026 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html) | 分别提供image/text/joint三级严重度设计；发布CSV8,159对，正式论文8,187对，严格S-S-U仅35/37例，不能拿全量当严格联合有害 |
| **P039 ThinkingGuard** | **ACM MM 2026，CCF-A刊会，录用/DOI已见，正式出版及Track未独立核实** | 已有反事实TriggerBench + 逐步风险归因 + Step/Trajectory-DPO方法，不能把“反事实+分步推理”作为未有先例 |
| **P040 Meerkat-VL** | [ICML 2026 Main，CCF-A](https://proceedings.mlr.press/v306/zhou26ae.html) | 自验证感知+GRPO对齐，目标是安全且有用的回答；训练奖励使用有特权风险说明的文本自评 |
| **P041 SIUO** | [NAACL 2025 Findings](https://aclanthology.org/2025.findings-naacl.198/)，**非NAACL主会；NAACL刊会等级CCF-B** | 正常单模态组合引发不安全输出；不是输入三标签风险GT |

上述工作覆盖危险侧、误拒侧与安全回应。**不能再把“模型有多模态安全漏检”“文本捷径存在”“先推理再回答/用反事实”直接当无竞争的创新点。**

## 6. 综述写作裁决

- R1仍用 **T5联合模态条件风险识别** 和 **T6安全响应** 两个一级任务，但T5内部明确分为：①严格组合风险变化（单模态安全→联合危险）、②视觉情境改变活动安全性、③语境解除表面危险（joint safe，误报侧）。第三类可以作为相邻“语境化安全辨识”，不是T5正例。
- T6细分：拒答/警告/安全且有帮助、以及过度拒答；输出侧指标不能代替输入分类。
- 论文的Main贡献分别是新情境基准、误拒评测、双侧安全意识基准，不能把三篇写成同一种Guard提升曲线。
- **结论等级**：模型在作者任务下存在安全-帮助权衡与不同错误分布（P）；数据/实现存在可检查的发布差异（S）；“失败来自内部视觉语义推理缺陷而非标签/Judge/拒答策略”仍属研究者假说（H）。

来源：
- [MSSBench精读](../R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md)
- [MOSSBench精读](../R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md)
- [MMSafeAware精读](../R2_literature_extension/B4a_reading/R2B_B4a_03_MMSafeAware.md)
- [R2数据资源审计](../R2_dataset_audit/Resource_Gaps.md)
- [R1任务框架](../R1_taxonomy/R1_Working_Framework_DRAFT.md)
