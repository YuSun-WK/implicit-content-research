# R2-B｜B4a 跨论文综合：情境依赖风险、联合安全判断与多模态安全误判

**状态：DRAFT；2026-11-08；待用户确认后定稿/合并main。** 仅在B4a独立分支新增本文件，不修改B2b/B3a、R1 taxonomy及其他论文卡。资料范围为三篇已在main定稿的阅读卡、R1工作框架和P034/P037/P038/P039/P040/P041核心竞争工作阅读卡；未追加模型运行/大规模逐样本审核。R1是**工作性定义**而非全领域术语共识。

## 0. 核心判断（可用于综述正文）
三篇分别观测“**情境改变动作安全性**（MSSBench）”“**安全输入触发拒答**（MOSSBench）”“**图文输入风险二分类同时顾及正负类**（MMSafeAware）”。尽管都称multimodal safety，其预测对象/GT/指标不同，不能把三篇的accuracy、safe rate、refusal rate合并成一列性能对比。

最值得引入广义隐晦信息综述的统一洞见是：**视觉线索、语言表达与任务意图的关系可使风险产生、消解或随物理环境改变；语境理解错误可传播至风险判断/响应，但最终回答/拒答本身不等于已经正确理解了隐含关系。**

**适用范围限制**：有害性≠隐晦性；风险判断涉及规范和行为后果，而不必出现修辞、狗哨、语用含意；仅当任务确实要求超越字面语义或联合模态推断，并有匹配的标注证据时，才列入综述核心论证。

## 1. Task=(X,Y,G,E)证据矩阵
沿R1的Task=(输入X，目标输出Y，GT协议G，评价E)统一三篇。

| 项目 | MSSBench（R2A-027） | MOSSBench（R2A-028） | MMSafeAware（R2A-029） |
|---|---|---|---|
| 来源 | Multimodal Situational Safety, ICLR 2025 Main, CCF-A | Is Your Multimodal Language Model Oversensitive to Safe Queries?, ICLR 2025 Main, CCF-A | Can't See the Forest for the Trees, ACL 2025 Main, CCF-A |
| X | 活动/指令Q+视觉情境V，Chat/Embodied | 安全图文请求(I,T)→模型自由回答R；有害contrast辅助 | 图像I+文本T，要求判断safe/unsafe |
| Y | IF:情境下回应/行动规划；QC/IC：直接风险分类（子实验） | 自由响应；事后判定拒答/合规 | Safe/Unsafe 输入联合标签 |
| GT输入 | 对“**活动在该环境执行**”安全性，safe/unsafe各980 | 主集**安全、可回答**（设计目标；争议存在）；contrast为有害改变 | unsafe1000 vs safe/over-safety500；设计时审核单图/单文本/联合关系 |
| G人工审核/局限 | Chat有人检，Embodied模拟/生成；公开缺全量逐例三元风险标注；部分Query与intent不匹配 | AMT 5人；约9%候选被多数判“无法无害回答”，逐例票未公开 | 3人审核并剔除4.7%候选；公开无独立三标签/投票细节；当前仓库版本不等于正式1500 |
| E主要指标 | IF四档回应形式经Judge折算的情境行为正确率；QC/IC属另一路分类设置 | Average Refusal Rate；Judge拒答0/配合1，非输入风险Acc | unsafe子集判No率、safe子集判Yes率、总体Accuracy |
| 分类正负都覆盖 | IF safe+unsafe平衡；输出评分有偏差 | 主集全safe；contrast非完整、仅辅助 | 是，论文1000+500；发布版本有偏差 |
| 严格反事实证据 | Chat同query安全/危险不同图；Embodied部分同时换指令 | Contrast244对：198同图异文、43异图同文、3双变；非完整300对 | 按独立单模态风险审核构造，但非样本级配对操作；当前公布主版本缺三向GT |
| 是否测真实自由回答安全+有效性 | 主要按警告/拒答/执行模式的代理准确率，未完整测帮助质量 | 只测拒答/合规，不可靠评价内容质量 | **否，任务是输出安全标签** |
| 综述归类 | 主T6，T5/情境风险邻接 | 主T6，T3否定/意图与T5邻接 | 主T5（扩展语境联合安全判断），次X4；非T6测量 |
| 开源实用性 | HF发布+GitHub，脚本/评判调用存在缺口、API要求 | 主300+对照244公开，评判依赖收费API，数据声明test-only | GitHub缺完整对应1,500样本文件和完整重跑代码；需版本对齐 |

## 2. 构成真正的语义关系是什么
区分下述三种**现象**，避免与一种“隐晦风险”标签合并。

**A. 风险涌现（Risk Emergence / Joint Risk）**：在同一标注尺度下，单模态表面安全或信息不足，联合才形成危险请求/危害语义。可作为严格T5核心子集的候选。设人工金标为y_I,y_T,y_IT，典型是 y_I=Safe且y_T=Safe且y_IT=Unsafe；前提是三者标注目标/规范一致，不应仅用“模型单看没识别”替代真实单模态金标。MMSafeAware unsafe按这个准则设计，但当前公开数据未提供全部样本的独立三标签；P038 VLSU与P034 CrossGuard更直接竞争。

**B. 风险消解（Risk Attenuation / Contextual Resolution）**：单模态出现令人警惕的词/物，但联合可由否定、虚构、引用、领域合法性或明确指代还原为安全；典型标签结构至少一模态被标Unsafe，联合Safe。MMSafeAware的Over-Safety是输入端分类误报，MOSSBench的NH/CI等是此类机制潜在实例，但MOSS并无公开完整的独立单模态三元GT，**不能反向证明每个MOSS样本符合此形式**。风险消解并非必然属于狭义隐晦有害正例，可在“联合语义及误报”节做并列论述。

**C. 情境性危险（Situational Safety / Affordance）**：同一请求的安全性取决于视觉环境/物理状态，如运动地点、操作电器的前提条件；要求从I,T共同推断“若按请求执行会发生什么”，而非“话语本身隐藏有害义”。MSSBench Chat比较有力，因为同一Query配安全/危险图；Embodied部分两边也换指令，因此不能所有样本都解释为“仅视觉情境导致的风险翻转”。

**注意**：这三个概念是**本综述的分析维度**，不是三篇作者共同提出的既成领域taxonomy。风险消解、情境性危险不自动计入R1严格T5；原有T5定义不直接改写。

## 3. 指标、混淆矩阵与分类—响应分离
对已有人类输入真值G的二分类任务，设危险为正类：
- `TPR_unsafe = P(predUnsafe | GTUnsafe)`；`FNR=1-TPR_unsafe`。
- `TNR_safe = P(predSafe | GTSafe)`；`FPR=1-TNR_safe`。
- `BalancedAcc=(TPR_unsafe+TNR_safe)/2`；不能把类别不平衡的overallAccuracy作为唯一排名。
- 对MMSafeAware论文分布1000/500，恒定预测Unsafe可得总Accuracy 66.67%、TPR=100%、TNR=0%、BalancedAcc=50%。表3 Claude3 total66.7%且over-safe 1.1%，不能据总分称“近乎准确”。
- MSSBench IF: 发布代码对响应label 0拒绝、1安全警告、2直接执行/回复、3非安全理由不答。对于Safe输入`{2,3}`按正确，对Unsafe输入`{0,1}`按正确。**Label3安全端不提供帮助也算对、Label0危险端无理由拒答也算对**；Judge只看输出的设置可能使得“理解风险”被回答形式替代。需保留审计警告，不能称为输入风险理解Accuracy。
- MOSSBench ARR是 `#Refusals/#SafeInputs`；论文Judge把不准确的直接回答也列compliance。低ARR不能证明Safe判断准确，也不能保证有用。其有害对照RefusalRate不能直接测回答产生具体危害。
- **概念链**： `scene perception→meaning/intent inference→risk classification→policy response→answer quality`，每个环节需要独立观测或可靠干预。把一条预测、解释或拒答作其他环节的测量是构念效度风险。
- 推荐综述对所有多模态安全论文分开报告至少四列：输入风险FNR；输入安全FPR；安全输入拒答ARR；危险输入的不安全帮助率（要有独立响应判读）；如果无法测量，填N/A，绝不以相近指标代替。

## 4. 跨模态依赖究竟由什么实验支持？
采用三层证据，而非二元“看没看图”：
- **E1 任务设计/人工标注**：声称需要联合语义，按单模态条件审核。例如MMSafeAware作者构建协议。证明样本选择意图，但不能单独证明模型预测真的使用图。
- **E2 受控成对测试**：固定文本改图片、或固定图改文本且有**对应两种场景的真实风险金标**，测预测是否朝正确方向翻转。MSS Chat可以作为候选（还需query-intent一致性）；MOSS Contrast244以198/43/3方式分组，且需复核对照GT；MMSafeAware仓库大量复用图片但缺现成逐对翻转标签。
- **E3 机制因果定位**：最小变化、非目标属性控制、因果约束、反事实/图文token干预和人工审核、不同prompt的等信息预算控制；三篇**均不足以独立证明E3层面的内部语义因果机制**。MOSS提供oracle caption/intent后误拒缓解仅为上限诊断；MMSafeAware单例token贡献可视化也不是因果定位；MSS多agent/GT环境状态改善不能证明具体agent职责是唯一因子。
**注意**：将图像随机打乱不会天然保留原安全GT，所以不能把任意image shuffle后沿用原标签打分并称“因果准确率”；必要时只能记录prediction sensitivity，另需有效重标或从已标注的成对数据提取。

## 5. 三篇研究提供的实证观察、可解释边界
- **MSS**（ICLR2025）：1960图文；IF GPT-4o Chat safe98.8/unsafe19.8、Embodied safe99.7/unsafe3.9；Claude总平均64.0；多agent有改善但有oracle信息/成本问题。这些是**情境回应形式正确率**，不证明输入标签任务的准确率。
- **MOSS**（ICLR2025）：300安全主集，三类型各100；Claude3 Opus(web)人评ARR76.33%、GPT4o(API)8.00%；过敏程度强烈依赖模型/版本/平台；不能把自动Judge和人工或web/API混为一谈。约9%候选有人标争议（具体逐例票缺失），若按绝对safe解释会影响误拒的构念效度。Contrast仅244；单侧安全样本不代表全域安全能力。
- **MMSafeAware**（ACL2025 Main）：论文1500（unsafe1000/safe500）、29类；Claude3 unsafe几乎全判危险但safe仅1.1%；LLaVA经VCD unsafe96.8→88.2、safe6.0→15.3（表6），对立指标有此消彼长；不能从少量数值证明增加视觉理解必然导致安全漏检。
**不应**把MSS的IF accuracy、MOSS ARR、MMSafeAware Safe Acc取平均作安全排名，也不能从不同模型版本推断跨论文单模型性能升降。

## 6. 发布数据/协议审计的可证内容
**MSSBench**：正式1960（安全980、危险980，Chat1200/Embodied760），早版摘要1820有冲突；Chat以同文本换图，Embodied不总如此。HF抽查有intent-query不匹配。发布脚本Judge/agent部分存在静态潜在实现问题及付费依赖；当前无端到端复现证据。
**MOSSBench**：主集300公开实物吻合，Contrast244，比较固定图片内容和问句得到198同图异文、43异图同文、3双变；其中一部分样本安全真值受人标争议，原始票未公开；评判器需付费API且有静态边缘错误路径。
**MMSafeAware**：作者论文1500，但已审核GitHub `data/prompt.txt`有1523个编号、1453个编号图片（后70个prompt缺图），1453张图片仅445个Git Blob SHA；readme按ID隐式提供safe/unsafe且与论文1000/500总量不一致；结果提取代码用简单字符串包含yes/no且端点与README不一致；当前无可直接运行的完整官方1500标签-图片一一映射。**不能把发布版本缺口误称为原研究必然只有1453样本**。
**总体评价**：目前最强已支持结论是“图文语境与输出安全决策存在双向误判，现有评测协议并不统一”；较弱甚至未证的是“某种内部推理模块普遍失败”、“普适的因果模态捷径”和“针对该空白的某个新模型必然有效”。

## 7. 与已入库2025–2026竞争工作：新意禁区
| 候选主张 | 已读竞争工作 | 对新方法的约束 |
|---|---|---|
| 我们首创图文联合有害输入检测 | CrossGuard（ACL2026 Main, A）；VLSU（ICLR2026, A） | 不成立；需新失败机制/严格监督/跨任务泛化 |
| 首次同时考虑漏检与过度保护 | MMSafeAware（ACL2025 Main, A）、MOSSBench（ICLR2025, A） | 不成立 |
| 发现文本捷径/图片未被真正利用 | VLSBench（ACL2025 Main, A）和MMSafeAware相关诊断 | 单独观察不足构成新颖性 |
| 创新是安全/危险反事实配对和步骤推理 | ThinkingGuard（ACM MM2026, A） | 已有反事实+风险归因+训练 |
| 先识别场景/意图再判断风险并回应 | MSSBench（ICLR2025, A）、Meerkat-VL（ICML2026, A） | 普通多Agent/CoT链条不够新 |
| 首次兼顾安全与有用性输出 | SIUO（NAACL2025 Findings；**非主会A**），Meerkat-VL（ICML2026, A） | 必须明确能力/指标增量，控制拒答捷径 |

以上仅审计本项目已读竞争论文，不表示已经覆盖全部2026研究，**没有直接确认A会创新空白成立**。

## 8. 对R1 taxonomy与综述写作的建议（**提案，不改原文件**）
1. **不改T5/T6一级定义**。继续保持 T5=联合模态隐含风险检测（严格证据门槛，T4特殊场景），T6=安全响应。三篇R2-A候选不抢占P034等已有编号。
2. 在T5/关联章节用“依赖模式”二级维度区分：①联合语义涌现（严格T5核心）②联合语境风险消解（T5关联，显式标Safe）③情境活动风险（T5邻接，可能偏T6）。
3. 单列一小节**误判与决策可靠性**：输入漏检/误报 → 过度拒答/过度配合 → 安全与帮助的权衡。该节可承载MSS/MOSS和VLSU，不把它们与隐喻/狗哨等表达机制并列为同级taxonomy。
4. 明确风险承载对象：`text/image content harm`、`instruction intent / action consequence`、`generated response harm`，以及视觉与语境信息是否实际决定GT。
5. 给每篇论文统一记录`{input, GT object, GT provenance, label space, metric, modal dependence evidence(E1–E3), response quality assessed?, published data integrity, evidence status}`；该表是综述证据工具，不是新算法。
6. 综述可用简短叙述：`模态信息获取→上下文指代/意图恢复→风险语义判定→输出策略与实际帮助`，说明上下游错误可传播，**不能宣称三篇直接证明这些阶段有独立可观测模块**。

**正文放置建议**：T5节首讲“联合依赖/场景条件的风险理解”（以MMSafeAware+P038 VLSU为例）；随后“视觉情境改变行为安全性”（MSS）；最后将“风险误报与过度拒绝”（MOSS）及“响应—理解脱钩”（MSS Judge、P041、P040）列为评测与部署可靠性边界。经典修辞/语用参照T1–T3章节，不在本节重复长篇解释。

## 9. 方法型创新线索：只形成待证假设，不宣布Gap
- **H1 证据可靠性假设**：在含显式图文反事实、可靠标签的子集里，固定模型的“联合输入被识别为危险/安全”可能与“正确解释风险触发线索”不一致。已有P039风险归因和P038三标签工作，若想发展方法必须证明超越其数据/对照与性能。
- **H2 误报—漏检耦合**：通过视觉增强减少safe误报可能增加unsafe漏检；要验证这是否仅由分类阈值/系统提示安全保守程度引起，还是存在可分离的图文消歧机制。MMSafeAware VCD/VRTuning结果只提供可能性，不能用单项改进断言新机制。
- **H3 识别—响应错配**：输入分类正确仍可能不提供安全且有帮助的响应，反之泛拒绝可让响应安全率虚高。Meerkat-VL与SIUO已有较强竞争，必须独立测且查重。

**最优先K0（CPU，0新标注）**：汇总三篇已核对的样本id、label字段、image SHA、固定模态对比例、缺失文件、Judge规则、版权/训练限制，生成三个dataset card和一张protocol compatibility matrix；不将MOSS test-only样本用作训练。
**K1（单卡，冻结模型，先200–300例）**：优先用P038 VLSU或严格审核的MSS Chat固定query对做输入分类；分开算unsafe recall、safe recall、Balanced Accuracy、pairwise directional flip；必要时只对原样本预测，不伪造新的图像置换GT。
**K2（输出侧少量采样）**：另行评“拒绝/警告/安全帮助/有害回答”，以人工复核样本或可核验开放模型辅助，避免只用拒答词regex；在无付费Judge下不声称与原论文官方结果可比。
**Kill条件**：①数据核对不清/无可靠金标；②对照实验表明现象仅由保守阈值可解释；③P038/P039/P040或2026更新工作已覆盖且无明确独立贡献；④成本超过单卡16–20GiB/6h，均停止将该假设包装为方法论文。

## 10. 结论／证据等级
- **高置信**：三篇任务输出不等价；二分类与自由回答必须区分；MSS一部分同query不同图；MOSS主300/contrast244；MMS GitHub主数据版本与论文数值有冲突；“全预测Unsafe”66.67%是MMS论文类比例下的算术基线。
- **中等置信**：图文风险涌现、消解和情境条件是有用的综述分析维度；各论文实验提示过度谨慎和危险漏检存在权衡；是否跨模型普遍成立需同基线重测。
- **低/待验证**：特定内部模块因果失败、模型真正利用了视觉而非文字捷径、跨论文对等数值排名、任一新方法显著且可复现超越2026工作。

## 11. 可追溯来源
- R1工作框架：`03_survey/R1_taxonomy/R1_Working_Framework_DRAFT.md`；R1任务映射：`03_survey/R1_taxonomy/R1C_Task_Mapping_DRAFT.md`；R2A：`03_survey/R2_literature_extension/R2A_Candidate_Ledger.md`。
- MSSBench精读卡：`03_survey/R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md`。出版：https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html
- MOSSBench精读卡：`03_survey/R2_literature_extension/B4a_reading/R2B_B4a_02_MOSSBench.md`。出版：https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html
- MMSafeAware精读卡：`03_survey/R2_literature_extension/B4a_reading/R2B_B4a_03_MMSafeAware.md`。出版：https://aclanthology.org/2025.acl-long.832/
- 竞争工作：`01_literature/cards/P034_CrossGuard.md`, `P037_VLSBench.md`, `P038_VLSU.md`, `P039_ThinkingGuard.md`, `P040_MeerkatVL.md`, `P041_SIUO.md`。
- 本文是对已定稿卡的证据整合，若基础卡的未关闭疑点之后被证实/推翻，**本综合结论须同步更新**。
