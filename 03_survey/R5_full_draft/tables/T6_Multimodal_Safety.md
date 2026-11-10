# 表6｜多模态风险与安全回应：输入识别和输出行为分开评价

### A. 输入风险真值与显式风险判断

| 研究与任务 | 输入真值与标注协议 | 模型预测或训练目标 | 证据边界 |
|---|---|---|---|
| Hateful Memes [@kiela2020hateful] | 图文仇恨二分类标签；不是图像Safe、文本Safe、联合Unsafe的三条件GT。 | 研究重点为图文联合分类。 | 普通图文仇恨分类基准不能被整体称为严格S-S-U数据。 |
| MMSafeAware [@wang-etal-2025-cant] | 作者报告Unsafe 1,000、Over-Safe 500及三向人工筛选；发布版文件和图像差异尚未固定。 | 联合Safe/Unsafe分类。 | 2:1比例下恒判Unsafe的总Accuracy已达66.67%；应同时报告Unsafe召回与Safe召回，不能只报总准确率。发布版精细数量仍为待核。 |
| VLSU输入分类 [@palaskar2026vlsu] | 正式PDF报告8,187条、17个模型；官方摘要写11个模型；所查公开CSV为8,159条；严格S-S-U分别为37/35条。三类标签为Safe、Borderline、Unsafe。 | 显式三级输入风险分类；Table 1为兼容旧基准另设二分类，并将Borderline并入Safe。 | 正式PDF、摘要和公开CSV版本口径不同；不能把二分类结果与正式三级结果直接换算。公开CSV另有141条image_grade=not_sure。 |
| CrossGuard输入Guard [@zhang-etal-2026-crossguard] | 1,616条Guard混合训练数据，联合类约占12.5%（约202条为估算）；ImpForge另有1,390条红队样本，尚未逐例映射。 | 使用LoRA/SFT训练图文Safe/Unsafe Guard。 | SIUO中Guard ASR报告60.33→5.39%，但训练数据量与类别构成也发生变化；不能把全部收益归因于新分类架构。FigStep为0.12→0.21，并非所有基准都单调改善。 |
| ThinkingGuard输入风险归因 [@zhang2026thinkingguard] | 作者报告TriggerBench共5,600条，Safe/Unsafe各2,800；图片分别生成，配对不等于只改变Trigger。 | 风险标签和五步分析；SA-MCTS离线搜索轨迹，Trajectory-DPO与Step-DPO更新模型。 | 作者Table 3的Unsafe F1由0.779升至0.810，Recall由0.699升至0.749；额外Unsafe监督、训练token和配对图像的单因素有效性尚未独立控制。作者称ACM MM 2026录用，会议CCF-A，正式Track仍待核。 |

### B. 生成式回应、攻击行为与回应质量

| 研究与任务 | 输入或触发条件 | 实际观察的回应与指标 | 不能混同的内容 |
|---|---|---|---|
| VLSBench回应评测 [@hu-etal-2025-vlsbench] | 比较模型面对图文风险、仅文本或附加图像描述时的回应。 | Safe Rate按Refusal+Warning统计；Qwen2-VL-7B特定200例中，text为29.5%、text+image description为22.5%、image+text为16.0%。 | 这些是回应比例，不是输入风险分类准确率；必须说明提示、模型和样本分母。 |
| VLSU安全回应提示 [@palaskar2026vlsu] | 同一模型和请求，将推理提示从Harmless改为Helpful。 | Gemini-1.5的Borderline拒答62.4%→10.4%，Unsafe拒答90.8%→53.9%；QwenVL-32B的Borderline拒答23.4%→30.7%，Unsafe拒答71.2%→57.5%。 | 这是回应策略变化，不是显式输入分类P_in的变化；模型间趋势并不一致。 |
| MSSBench情境回应 [@zhou2025situational] | 1,960个图文情境请求；Chat与Embodied设置的行动能力不同。 | IF Judge评价情境行动或回答；部分设置可额外提供Oracle环境状态。 | Oracle环境事实改变了信息预算；Judge评分不是模型内部风险分类标签。 |
| MOSSBench过度拒答 [@li2025oversensitive] | 作者目标安全图文请求300条；约9%的人工判断对能否安全作答存在争议。 | 安全主集上的ARR为拒答比例；危险对照可另行测量。 | 安全侧误拒不是输入分类FPR；发布版contrast配对和ID映射未完全固定，不能把全部样本称为严格单因素配对。 |
| SIUO攻击回应 [@wang-etal-2025-safe] | 表面安全的跨模态输入可能诱导模型给出危险回复；不提供VLSU式三条件人审输入GT。 | 输出Safe Rate或攻击成功率，包含人工与AI辅助构造子集及Judge参考信息；NAACL 2025 Findings，会议CCF-B，非Main。 | 行为攻击评测不能并入输入风险三分类准确率；Judge、参考安全警示及样本构造方式必须单独说明。 |
| ImpForge红队生成 [@zhang-etal-2026-crossguard] | 生成隐晦联合攻击图文，PPO优化文本改写器并结合图像生成。 | 观察被测模型是否产生不安全回应，即攻击成功率。 | 攻击成功率不是Guard漏检率；PPO必要性仍需与同预算检索、Best-of-N等控制比较。 |
| Meerkat-VL安全有用回应 [@zhou2026meerkatvl] | 训练材料包含user_intent、harmful_intent和safety_warning等规范风险说明。 | Cold-start SFT、同Actor NPSV评分、一致性惩罚DPCA及GRPO优化安全且有帮助的回答。 | 训练评分使用风险文本，但不重新读取原图；不等于独立视觉验证。模型Judge与帮助性评价应分别报告。 |

**表注。** 输入风险真值、显式风险分类、实际回应行为和输出安全/帮助性质量是不同评价对象。危险输入上的漏判、安全输入上的误报、不安全帮助和正常请求误拒应分别报告。不同论文中的ASR可能分别指攻击得逞、Guard漏检或生成危险回复，必须同时给出主体、Judge和分母。S-S-U只是严格联合风险的一个子类。
