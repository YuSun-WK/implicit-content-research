# 第三章 文本修辞与语用含义的计算理解

> R5-A 正文初稿（2026-11-09）。沿用 R4-01 的 3.1–3.5 目录及原 P/T/R2A 编号。文中“作者报告”指论文所述实验，“静态审计”指本项目对公开材料的检查，“综述判断”指跨研究推论；文末引文表同时给出正式论文与既有证据卡。第1、2章术语依 R4-05/06，未在本轮改动。

## 3.1 修辞表达检测

文本修辞研究最先需要回答的是：模型识别了表达形式，还是已经确定了该表达在当前交际中的意义？隐喻通过源域描述目标域，夸张改变程度尺度，反讽可能使表面评价与语境立场相背；习语、委婉语和反问又分别涉及惯用组合、间接命名与疑问句的交际功能。它们可以共现，但标注对象并不相同。形式检测通常给出句子或片段的现象标签（T1）；要回答“究竟指什么”或“对谁表达何种行动”，还需另设意义（T2）与语用意图（T3）的任务真值。把三个层次合并为单一“隐晦理解”得分，会掩盖模型只抓住词面线索的可能性。〔P035；P022；R2A-004〕

在修辞形式的联合识别上，EmoBi〔P035，ACL 2025 Main，CCF-A〕以英文句子为输入，分别预测可共存的隐喻和夸张二元标签。方法先让语言模型生成情绪分析，再描述隐喻的源域和目标域，利用一个任务的预测辅助另一个任务，最后连同先前理由重新判断两种标签；这些环节是结构化提示与多次推理，并非新增的参数训练目标。作者在 HYPO、HYPO-L、LCC 和 TroFi 的联合标注资源上报告分类结果，Table 1 的 F1 与 Table 2 的核验阶段消融支持“这一提示组合在该协议下有用”。但四套资源原有标签和补标标签的血缘不同，且现有消融未以相同调用次数和输出长度隔离情绪、源目标说明与反复判断的独立贡献。项目静态审计还发现当前公开调用顺序以隐喻预测先于夸张预测为主，不能据方法名把实现描述为完全对称的循环。〔P035，§3、Tables 1–2、Fig. 2；P035 阅读卡§3–8〕

反讽检测揭示另一种局限。P015〔ACL 2026 Main，CCF-A〕在现成指令模型上做零样本二分类，作者报告模型在其合成样本与真人语料间出现显著表现差异，并用表示可视化、语言模型熟悉度代理、局部扰动和层消融分析错误。该论文没有先用合成数据训练待评模型，故不能把结果写成“合成训练导致真实测试失败”；真人与合成集合还同时改变平台、话题、长度、标签生成方式和表达难度。其 Table 2 的准确率差异是特定数据与推理协议下的现象，二维表示聚类与删词效应不足以单独证明模型在语用意义上“完全失明”。综述判断是：形式标签的高低分必须结合数据来源和标签操作定义解释；“反讽”这一类内部仍有真实语境依赖、显著语义反差和生成模板差异。〔P015，§2–5、Tables 1–3；P015 阅读卡§2–6〕

习语、委婉和反问也提醒我们注意标签粒度。SemanticQA〔P022，ACL 2026 Main，CCF-A〕把多词表达的片段抽取、分类和语境解释分成原子操作，再要求模型在一次回答中同时给出抽取及判断；不同来源语料的标签与输出格式并不统一。R2A-004〔ACL 2026 Main，CCF-A〕则沿用两个反问/信息寻求问句数据集的二元标签，测量隐藏表示能否被线性探针分开。前者检验可观察的多步骤输出，后者检验表征可分性；两者均不能直接替代对真实说话者意图的独立验证。〔P022，§3–5、Tables 3/5；R2A-004，§3–6、Figs. 1–4〕

## 3.2 非字面意义与语用意图推断

从识别修辞过渡到推断意义，关键变化是输出由“是否出现某种形式”变为“在这组语境中哪个解释更可接受”。(RSA)²〔P020，ACL 2025 Main，CCF-A〕将修辞策略 r 明确加入理性言语行为模型：策略相容函数 f_r(c,m,u) 使话语 u 在特定策略下对非字面意义 m 也可赋非零概率；听者再按说话者选词的条件概率反推候选意义。方法解决了严格字面相容函数将非字面解释概率置零的建模障碍。它依赖候选意义与候选话语集合、意义先验及策略概率；在数值夸张任务中策略函数含人工规则，在天气反讽任务中又利用人类策略判断训练小网络，不能概括成无先验、开放式的意图恢复。作者在 PragMega+ 的有限候选反讽实验中报告策略条件化的收益；Table 2 最优配置为策略条件的 L0 而非更深递归的 L1，Table 3 的先验消融也显示意义先验贡献很大。因此，论文支持“显式策略条件有助于特定候选意义选择”，尚不足以把全部增益归因于递归语用推理。〔P020，§3–5、Tables 1–3；P020 阅读卡§3–7〕

DRInQ〔R2A-001，ACL 2026 Main，CCF-A〕从评价设计切入：保持表面问句 Q 不变，改变情境 C，使五个候选含义中被人类共识支持的选项变化。候选不是任意干扰项，而是同一问句在其他情境下可能成立的解释，因此模型不能仅靠问句形式作答。论文把生成的情境和含义交给五人判断，仅保留至少四人一致的实例；其困难子集 Table 2 报告 400 道五选一题的结果。解释提示并非对所有模型都有提升，这与“只要生成理由就能增强语用理解”的假设不符。其共识真值仍是对构造场景的可接受解释，不是对现实说话者心理状态的观测；本项目审计发现论文总体/困难集数量与当前公开 CSV 数量不同，故正文只使用论文中条件明确的困难集口径。〔R2A-001，§3–5、Table 2、Fig. 6；R2A-001 阅读卡§3–7〕

另一条技术线研究表征应如何分开否定与隐含意图。R2A-003〔ACL 2024 Main，CCF-A〕从现有意图数据出发，用模型生成否定和含意变体，再以三元组距离及分类/聚类检验意图编码器。训练用语义对比拉近保留意图的表达、推远改变意图的表达；论文 Table 2–3 显示常规意图分类能力不能保证困难三元组排序正确，针对困难负例训练也可能使不同指标出现取舍。不过原始意图类继承既有数据，变体主要由模型生成且人工核验仅覆盖抽样，不能将排序正确率直接解释为开放对话中的间接言语行为恢复。反问探针研究〔R2A-004〕进一步显示，跨数据集分类仍可达到可用 AUROC 时，探针方向和高排名实例集合可能不稳定。综述判断是：表示可分、候选解释选对、真实交际功能恢复三者需要各自的检验。〔R2A-003，§3–6、Tables 1–3；R2A-004，§4–7、Figs. 1–4〕

## 3.3 情绪与交互辅助：从相关线索到可部署证据

情绪是修辞的重要线索，却既可能是表达后果，也可能只是与语料主题共同出现。EmoBi〔P035〕把模型自生成的情绪描述送入源目标映射与隐喻/夸张相互提示，使情绪成为推理时的辅助文本。其关键优点在于把“何种情绪、何种映射”显式放进可检查的中间输出；其直接评测目标仍是两个形式标签，而非人工标注的情绪因果作用或最终语用意义。作者 Table 2 的去核验消融显示完整流程在所测资源上得分较高，但核验本身是同一模型基于更多提示再判断，没有外部真值纠错器。静态审计所见源码还保留固定先后顺序及运行依赖问题；这些观察提示复现与归因风险，不等于否定论文已报告的表内结果。〔P035，§3–4、Tables 1–2；P035 阅读卡§4–8〕

情绪信息的“可用”还取决于测试时如何获得。多模态隐喻论文 P003〔ACL 2025 Main，CCF-A；第6章主讲〕所审公开检测代码把数据表中的人工情绪标签拼入测试输入，这属于额外金信息预算，不能与只见原始文本或图文的系统并排解释为纯语义能力。对文本修辞而言，同样应区分模型自行预测的情绪、训练时辅助情绪标签、测试时人工情绪标签以及随机或打乱的情绪提示。综述判断是：只有在相同模型、相同推理预算下比较这些条件，并检查情绪错误时标签是否随之翻转，才能更具体地论证情绪线索的部署价值。现有结果说明其作为设计线索有前景，却尚未证明所有修辞理解必须经由情绪中介。〔P003 阅读卡；P035 阅读卡§5–9〕

## 3.4 测试形式的边界

同一“理解”标题下，测量对象可能相距很远。DRInQ 的五选一准确率要求在给定候选中选出共识含义；(RSA)² 的 PragMega+ 报告正确候选获得的平均概率；SemanticQA 的解释任务比较生成文本与参考解释的 METEOR/BERTScore，联合任务还把片段抽取是否正确计入综合分；反问线性探针的 AUROC 则只显示隐藏状态携带可供线性分类的信息。这些量的分母、随机基线、参考答案空间及信息预算不同，不能把数值放进统一排行榜。〔R2A-001，Table 2；P020，Table 2；P022，Tables 3/5；R2A-004，Figs. 1–4〕

尤需警惕“解释流畅”替代“解释忠实”。SemanticQA 公开程序的顺序组合是一次提示中同时请求抽取与解释，并非程序先完成一次抽取调用、再把结果交给第二次调用；因此联合分数下降可以由抽取边界、输出格式或参考解释覆盖不足造成，不能直接推断独立步骤的错误传播。R2A-004 的探针即便跨域保持分类能力，也未发现稳定唯一的反问表示方向；P015 的二维可视化和局部词扰动同样不能直接呈现模型内部语用推理。更可信的比较需要同一表达在不同语境下的配对判断，分别给出字面与非字面负例，并报告候选意义、对象和立场的独立标注。这里的后两项属于综述提出的评价要求，而非上述论文已完成的统一实验。〔P022，§4–5及代码审计；R2A-004，§5–7；P015，§4–5〕

## 3.5 从修辞到社群编码的桥梁

委婉表达可以经由替代词、谐音或跨语言变形固定为社群约定，隐喻也可能成为群体内部识别信号；但两者没有必然包含关系。CodedLang〔P023，ACL 2026 Main，CCF-A〕在真实中文评论中标注编码片段和主要编码方式，其“Newspaper Eat”一例需要音系与翻译链的逆推，不能仅以传统隐喻源目标映射说明。Silent Signals〔R2A-006，ACL 2024 Main，CCF-A〕则预给狗哨词项与编码定义，再判断具体上下文是否用了该义；一个表达在其他语境仍可按普通义使用。这些材料共同把研究问题从修辞类型扩展到受众共享知识、实例多义与词义变化。〔P023，§2–4、Table 1；R2A-006，§3–4、Fig. 2〕

由此进入第4章时，需要先问研究者究竟是在发现一种表达、消歧其一次使用、恢复所指意义，还是评价其危害。反讽、隐喻、委婉和编码都可能承载无害交流；无论形式多隐晦，仅凭形式标签都不能推出交际者有规避审核的目的。编码表达与有害性之间还隔着目标、立场及规范判断，这一层将在第5章讨论。〔P023；R2A-006；R2A-008；综述判断〕

### 本章引文与证据入口

- 〔P015〕[LLMs in Sarcasm Detection?，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1346/)；[定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P015_LLMs_in_Sarcasm_Detection.md)。
- 〔P020〕[(RSA)²，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1019/)；[定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P020_RSA2.md)。精读所据 arXiv v1 与正式 PDF 式号/表号尚未逐页对齐。
- 〔P022〕[SemanticQA，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.210/)；[定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P022_SemanticQA.md)。
- 〔P035〕[EmoBi，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.23/)；[定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md)。
- 〔P023〕[CodedLang，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.426/)；[定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P023_CodedLang.md)。
- 〔R2A-001〕[DRInQ，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.1597/)；[R2-B 定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_01_DRInQ.md)。
- 〔R2A-003〕[Negation vs Implicature，ACL 2024 Main，CCF-A](https://aclanthology.org/2024.acl-long.33/)；[R2-B 定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_03_Negation_vs_Implicature.md)。
- 〔R2A-004〕[Rhetorical Questions，ACL 2026 Main，CCF-A](https://aclanthology.org/2026.acl-long.5/)；[R2-B 定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B1_reading/R2B_B1_04_Rhetorical_Questions_Linear_Probing.md)。
- 〔R2A-006〕[Silent Signals，ACL 2024 Main，CCF-A](https://aclanthology.org/2024.acl-long.675/)；[R2-B 定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_01_Silent_Signals.md)。
- 〔R2A-008〕[FA-Net，AAAI 2024 Technical Track，CCF-A](https://ojs.aaai.org/index.php/AAAI/article/view/29786)；[R2-B 定稿精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R2_literature_extension/B2a_reading/R2B_B2a_03_Hidden_Chasm_FA_Net.md)。
- 〔P003〕[MultiMM，ACL 2025 Main，CCF-A](https://aclanthology.org/2025.acl-long.1275/)；[精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P003_MultiMM.md)；仅作信息预算的交叉引用。
