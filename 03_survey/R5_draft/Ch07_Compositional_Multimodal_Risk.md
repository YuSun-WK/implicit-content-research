# 第七章 多模态联合风险理解与安全响应

> R5-B 正文初稿（2026-11-09）。遵循 R4-01 的 7.1–7.5。输入风险真值、模型显式判断、实际响应行为及输出安全性／帮助性是四个不同测量对象。论文报告〔P〕、公开文件静态审计〔S〕、综述推断〔H〕与待核事项〔O〕在文中保持区分。

## 7.1 联合风险的任务定义

第六章的非字面意义判断以修辞或蕴含关系为目标；安全研究还需回答某一图文请求在给定政策、受众和环境下是否构成风险。设图像为 I、文字为 T、可见情境为 C，可以分别要求人或评审者判断图像、文字与联合输入的风险等级；也可以要求模型直接生成回应。前者属于 T4 输入危害判定，其中强调模态组合依赖的协议构成 T5；后者是相邻的 T6 安全响应。图文同时出现并不自动满足 T5：危险可能已由文字单独给出，也可能由视觉情境解除文字表面风险。严格的 Safe–Safe–Unsafe（S-S-U）仅指图与文分别安全、联合危险的一个更窄子类。〔P038；R2A-027；R4-01；综述判断〕

为了防止指标偷换，本章分开记录四层。第一层 G_in 是依据明确政策或人工标注得到的输入风险真值；第二层 P_in 是模型**实际显式输出**的风险类别，只有接口要求模型分类时才可观察；第三层 R_beh 是拒答、警示、执行或转向安全建议等响应行为；第四层 Q_out 评价输出是否安全且是否帮助合法用户。危险输入上拒答率升高不必然等于风险分类召回升高，安全输入上的误拒也不等于输入分类误报。对没有显式分类步骤的生成模型，不应从最终一句拒答反推其内部一定判断了 Unsafe。〔P038；R2A-028；R2A-029；综述判断〕

典型联合关系不只“两个安全部分组成危险整体”。同一请求在图中出现特定实体或环境时可能升级，图像也可表明危险词语处于否定、教学或非现实语境，从而降低风险；另有图片单独已经含明显危险信号，文字只是指令化。要判断组合**改变**了标签，必须为同一政策下的单模态与联合条件建立可比较的真值，并区分人类“无法单独判断”和政策上的 Borderline；VLSU 中 Borderline 是安全等级，而非标注概率。〔P038；R2A-027；R2A-029；综述判断〕

## 7.2 图文安全数据、视觉泄漏与版本边界

Hateful Memes〔T015，NeurIPS 2020 正式论文集，CCF-A〕使图文组合成为有害内容检测的重要基准，但普通 Meme 的联合分类标签不能自动证明每个样本均属严格 S-S-U。本项目目前只将该篇作为官方出版与任务背景，不从摘要级材料杜撰其细节或复现成绩。VLSBench〔P037，ACL 2025 Main，CCF-A〕转向视觉安全信息泄漏：若文本或其他捷径已足以触发拒答／危险回答，加入图像后的安全表现可能误导对视觉依据的判断。其主要评测对象是生成回应的拒答、警示和不安全行为；不能直接当作独立的三条件输入风险金标。〔T015；P037；R4-07〕

MMSafeAware〔R2A-029，ACL 2025 Main，CCF-A〕则直接让 MLLM 对联合图文给出 Safe／Unsafe。论文构造了 1,000 条不安全及 500 条“过度敏感”测试情形，三向判断用于样本筛选，主评估却是联合输入的二元分类；公开仓库未提供足以逐例复核全部图像／文字／联合金标的完整三列投票记录。项目既有静态审计还发现所查仓库的 prompt、图片编号和唯一图像文件数量与论文 1,500 的协议口径不能简单一一对应，这要求正式比较记录版本、缺图和按图像分组的不确定性。2:1 的标签比例下，恒判 Unsafe 已能取得 66.67% 总 Accuracy，却无法识别安全侧；因此需同时报告危险召回、安全召回和按组别的错误。〔R2A-029，§3–5；R2-C B4a 静态审计〕

VLSU〔P038，ICLR 2026 正式会议，CCF-A〕提供更明确的三条件风险标注：图像单独、文字单独和联合输入分别可为 Safe、Borderline 或 Unsafe。论文正式 PDF 报告 8,187 条、15 个风险类和 17 种组合模式；本项目此前逐行审计的作者公开 CSV 为 8,159 条，差 28 条，原因未明。正式论文 Figure 9 的严格 S-S-U 为 37 条，所查公开版本为 35 条且属于 test-only 切片；公开文件中的其他风险升级组合不能全部叫 S-S-U。论文 PDF 写评测 17 个模型，而 ICLR 官方摘要网页仍写 11 个，这也是须并列保留的版本差异，不能任选其一并抹去另一版本。〔P038，正式 PDF §3–4、Fig. 9、Appendix F；R5-E 高优先级审计〕

VLSU 的安全理解实验和安全对齐实验还使用不同输出。前者要求模型预测输入等级；其 Table 1 为兼容既有基准采用二分类提示，并把 Borderline 并入 Safe，而三分类实验有自己的分母与 F1。后者让模型生成回答，再由评审器判断拒答与帮助性。论文 Figure 5 所述约 34% 的“两单模态都预测正确、联合预测错误”，分母是**联合预测失败**的样本，不是全库、也不是严格 S-S-U 的错误率。公开 CSV 还含 image_grade 为 not_sure 的记录，模式统计需要说明剔除或映射规则；这些细节均影响对“联合理解失败”的解释。〔P038，Tables 1–3、Fig. 5；R5-E 审计〕

Multimodal Situational Safety〔R2A-027，ICLR 2025 Main，CCF-A〕把活动请求放入视觉环境，MSSBench 论文报告 1,960 个图文对，区分显式安全判断诊断和是否遵循／拒绝的行为评估。同一句请求配不同场景图的 Chat 部分适合讨论视觉条件；Embodied 部分不一定严格只改图像。其 IF Judge 对回答模式评分，并非直接读取模型内部风险分类；给模型 Oracle 环境状态也提高了可用信息预算。SIUO〔P041，NAACL 2025 Findings，NAACL 会议 CCF-B，非 Main〕观察表面安全的跨模态输入引发不安全输出，主要是行为对齐挑战，不能并入 VLSU 的人工输入三等级真值。〔R2A-027，§3–5；P041；R2-C B4a〕

【表 T6 占位：按论文列出输入风险真值及标注主体、是否分别有图／文／联合标签、模型显式分类、响应行为、输出安全和帮助性指标、裁判器、数据版本及许可。表中单列 VLSU 的 PDF／公开 CSV 差异与 S-S-U 特例。】

## 7.3 检测器、触发归因与反事实训练

在有清楚风险标签的前提下，方法研究才可问模型是否识别了“哪一种组合关系”触发风险。CrossGuard〔P034，ACL 2026 Main，CCF-A〕面向图文联合隐含恶意攻击。其 ImpForge 先从不安全请求抽取可视觉化实体并匹配图片，再固定图片、以 PPO 改写文字，奖励文字单独安全、保留原请求相关语义并减少显性图文重复；随后将生成样本与其他安全数据混合，以 LoRA 微调 LLaVA 基座的 Safe／Unsafe 输入防护器。推理时防护器先判输入标签，攻击生成器并非回应模型。论文 Fig. 4 报告，加入生成数据后 SIUO 上的防护 ASR 由 60.33 降至 5.39；但训练集大小和类别构成也随之变化，不能把差值全归因于“学会联合语义”。作者以生成攻击的成功率、防护器漏判率和被测 MLLM 的危险回应评价不同系统，这些 ASR 的操作定义及裁判器并不完全同质。该工作说明联合风险 Guard 与强化红队样本生成已有直接先例；训练样本的触发规则、合成分布和奖励实现仍须与正式表格、公开版本对应，不能从一个总体分数推出对任意自然图文风险的泛化。与 VLSU 的人审三等级不同，CrossGuard 所优化的二元标签和生成式攻击协议必须单列。〔P034，§3–6、Table 1、Fig. 4；P034 精读卡静态审计〕

ThinkingGuard〔P039〕把输入风险检测与逐步归因放在同一模型：TriggerBench 以关键实体和触发因素构造 Safe／Unsafe 图文配对；离线 SA-MCTS 搜索五阶段风险分析轨迹，随后以完整轨迹及关键步骤的偏好对进行 DPO 训练；推理时模型直接输出结构化分析、风险类别和安全标签。作者报告 Table 3 中完整模型相对去 Step-DPO 的 Unsafe F1 与召回收益，支持该**训练配置**的经验价值。但额外关键步骤偏好对可能同时增加样本、token 与危险样本权重；没有同预算的额外轨迹对照，不能将差异独立归因于“逐步归因机制”。独立生成的配对图片也可能在触发因素之外发生视觉变化，需逐对人工验证和按 pair 分组切分。〔P039，作者公开稿 §3–5、Tables 1/3；P039 精读卡〕

ThinkingGuard 的出版状态须单独说明：作者仓库与研究组称其获 ACM MM 2026 接收并给出 DOI，ACM MM 会议在项目采用目录中属 CCF-A；截至本稿日期，尚未独立取得 ACM 出版社最终条目和论文实际 Track。因此本文仅用作已公开的直接竞争研究先例，不将其列为“已核 ACM MM Main 正式论文”，也不凭作者标注 Oral 推断 Track。对其 SA-MCTS 奖励提示、配对反事实的单因素程度和 Step-DPO 等预算效应，保持开放状态。〔P039；R5-E 高优先级审计〕

CrossGuard 与 ThinkingGuard 已分别推进防护训练和触发因素归因，故“构建联合风险配对”“让模型解释危险所在”本身不能写作无人研究。尚需的实验证据是：在同一对人工复标的图文上，固定模型和训练预算，置换**一个**关键因素后输入风险真值与显式预测是否同步变化，并排除图像生成纹理、文本模板及对象类别泄漏。分类 F1、风险分析文本和反事实敏感性应分别报告。〔P034；P039；综述判断〕

## 7.4 安全响应与过度拒答

风险判断即使正确，也不唯一规定回复方式。针对危险请求，安全输出可拒绝具体有害步骤并提供可用的替代信息；针对正常请求，机械拒答则损害帮助性。MOSSBench〔R2A-028，ICLR 2025 Main，CCF-A〕以 300 条作者视作安全的图文请求研究过度拒答，另有部分危险对照。其指标是安全输入上的拒答行为，不是模型输入风险分类的准确率。项目既有审计显示对照并非全部一一配对，且部分众包意见认为主集中的少量请求不能安全回答，故需保留标注分歧。去图后拒答减少也不能单独证明原拒答全因视觉理解错误：删图同时改变了可见事实。〔R2A-028，§3–5；R2-C B4a 静态审计〕

Meerkat-VL〔P040，ICML 2026 Main，CCF-A〕把目标从输入类别转向安全而有帮助的生成。其 cold-start 监督微调使 VLM 输出感知分析与回答；随后同一 Actor 对自身分析和回答给出若干质量分，经感知一致性奖励和 GRPO 更新。训练监督包括用户目标、风险说明和安全警示等文本字段，公开评分路径的自评调用并未重新接收原图，故不能把“自验证”理解为独立视觉事实核查。作者报告安全及帮助性改进，然而项目精读卡尚未逐项核对正式 PDF 的完整基线与消融表；本章不报未经对齐的百分比。风险知识字段、冷启动与奖励优化的独立贡献仍需同信息、同预算对照。〔P040，ICML 正式版及公开训练代码；P040 精读卡〕

VLSU 的拒答／帮助性实验、MSSBench 的情境行动、MOSSBench 的正常请求误拒和 Meerkat-VL 的安全回应，分别对响应链的不同层施压。SIUO 的攻击成功率关注危险输出，MMSafeAware 的危险召回关注输入判别。即使数字看似都以百分比报告，拒答率、ASR、分类 F1 和安全回复率也不能换算为同一个“安全性能”。尤其不能把高拒答率视作模型已经识别图文组合的风险来源。〔P038；R2A-027；R2A-028；R2A-029；P040；P041；综述判断〕

【图 F5 占位：从人工／政策输入真值 G_in 到可观察的显式预测 P_in、实际响应 R_beh 和输出安全／帮助性 Q_out 画四层测量对象；另画危险漏判、正常请求误拒两侧错误，箭头只表示评测记录关系，不代表从输出可读出内部判断。】

## 7.5 正负两侧评价与失败归因

安全系统的失败有两面。在输入分类协议中，危险样本被判 Safe 是漏检，安全样本被判 Unsafe 是误报；在回应协议中，危险请求收到可执行有害帮助与正常请求被拒绝是不同错误。前两者依赖 G_in 与显式 P_in，后两者依赖 R_beh、Q_out 和相应人工或评审器标准。一个方法可降低危险侧漏检，却扩大安全侧误拒；若只报总 Accuracy 或总拒答率，这种代价会被类别比例遮盖。MMSafeAware 的 2:1 设计、MOSSBench 的安全主集和 VLSU 对 Safe／Borderline／Unsafe 的分组，正好说明需要同时呈现条件分母、两侧召回与策略质量。〔R2A-029；R2A-028；P038；综述判断〕

失败归因也须受控。文本单独模型的错误不必然意味着图像“不可替代”，因为图片可能含 OCR 或模型未被训练处理白图；图像置换后的标签如果未经人工复标，沿用原联合金标会把无效反事实当成模型错误。VLSBench 的视觉泄漏诊断、VLSU 的单模态与联合标注、ThinkingGuard 的配对触发、MSSBench 的同请求换场景图，分别提供了可借鉴的控制环节，却各有数据构造和指标限制。测试图像缺失、近重复、生成模板、评审器提示词和不确定标注也应随分数一并公开。〔P037；P038；P039；R2A-027；综述判断〕

因此，第七章可得的稳妥结论是：联合模态风险及安全回应已拥有多个直接研究方案，但现有证据尚不能用一个拒答或分类指标证明模型同时具有正确的风险感知、忠实归因与安全有用的行为。第八章将把这类证据链与前面语用、编码、修辞和文本危害研究并列，讨论信息预算、Ground Truth 与干预设计如何决定跨任务比较的可信范围。〔P034；P038；P040；R4-07；综述判断〕

### 本章引文与证据入口

- 〔T015〕[Hateful Memes，NeurIPS 2020 正式论文集，CCF-A](https://papers.nips.cc/paper/2020/hash/1b84c4cee2b8b3d823b30e2d604b1878-Abstract.html)；本项目仅摘要／目录级使用。
- 〔P034〕[CrossGuard，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1178/)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P034_CrossGuard.md)。
- 〔P037〕[VLSBench，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.405/)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P037_VLSBench.md)。
- 〔P038〕[VLSU，ICLR 2026 正式会议，CCF-A，PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)；[官方摘要页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md)。
- 〔P039〕[ThinkingGuard，作者公开稿](https://arxiv.org/abs/2609.36562)；[作者仓库](https://github.com/FroggyChen/ThinkingGuard)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P039_ThinkingGuard.md)。ACM MM 2026 会议 CCF-A；本篇正式出版及 Track 待核。
- 〔P040〕[Meerkat-VL，ICML 2026 Main，CCF-A](https://proceedings.mlr.press/v306/zhou26ae.html)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P040_MeerkatVL.md)。
- 〔P041〕[SIUO，NAACL 2025 Findings，会议 CCF-B](https://aclanthology.org/2025.findings-naacl.198/)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P041_SIUO.md)。
- 〔R2A-027〕[Multimodal Situational Safety，ICLR 2025 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md)。
- 〔R2A-028〕[MOSSBench，ICLR 2025 Main，CCF-A](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md)。
- 〔R2A-029〕[MMSafeAware，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.832/)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B4a_reading/R2B_B4a_03_MMSafeAware.md)。
