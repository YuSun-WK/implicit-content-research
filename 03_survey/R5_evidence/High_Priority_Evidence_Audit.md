# R5-E｜High-Priority Evidence Audit：五项争议逐条裁决

> 2026-11-09。独立于 Work 正在编写的 R5-A 第3–5章；不修改任何正文或已定稿R2/R3。P=**原论文/出版方直接陈述**（不是本项目复现）；F=**可以直接核对的出版事实**；S=**公开代码/数据静态审计**（注明是本轮还是上游）；H=**推论或研究者解释**；O=**证据仍缺/未解决**。F/P/S/H/O不能互相替代。审计优先顺序 R4-08 P0→P1。
>
> 来源基线：[R4-07](../R4_writing/R4_07_Section_Claim_Evidence_Matrix.md)、[R4-08](../R4_writing/R4_08_Overall_Quality_Gate_20261109.md)、[R2-D](../R2_registry/Metadata_and_Evidence_Conflicts.md)、[AUTALIC R3专项](../R3_targeted_reading/R3B_01_AUTALIC_Three_Issue_Audit.md)、[MCIB R3专项](../R3_targeted_reading/R3B_02_MCIB_CIB_Attribution_Audit.md)、[VLSU P038原卡](../../01_literature/cards/P038_VLSU.md)、[ThinkingGuard P039原卡](../../01_literature/cards/P039_ThinkingGuard.md)。
>
> **方法限制**：本轮核对官方网页和正式PDF关键页、作者GitHub公开源码；公开 VLSU 8159、S-S-U 35 等逐行结果**沿用2026-11-02的P038既有数据实读**，本轮未重新下载整个CSV再运行脚本；AUTALIC压缩CSV未解密，MCIB未训练/运行。不可把此稿写成全量独立复现实验报告。

## 1. 相关综述与本文真实贡献（P0，Ch1 §1.2）

- **F/P：** P011（ACL 2025 Main，CCF-A）已综述LLM语用数据和评测；Farabi et al.（IJCAI 2024 **Survey Track**，按2026年第七版目录会议CCF-B（非普通研究Full/Regular Paper））覆盖2018–2023多模态反讽；P007（EMNLP 2024 **Findings**，会议CCF-B、非Main）已经覆盖多模态仇恨及LLM/LMM检测/解释/去偏/反言语；P002（ACM CSUR，2025在线/2026卷期、CCF未收录）涉及少见修辞；Ge et al.（Artificial Intelligence Review 2023，CCF等级待核）已经有隐喻识别/解释/生成综述。
- **H：** 本综述能稳妥主张的是把跨现象文献统一投影到 T1–T6 / Task=(X,Y,G,E) / 模态与信息预算 / GT / 机制证据约束，这是一种**组织与审计贡献**，不是“首篇”或新验证的理论。
- **O：** 非穷尽检索；除IJCAI明确的2018–2023时间窗，其余尚不能把摘要级对照升格为逐篇全文覆盖率。单独详见 [Related_Surveys_Comparison](Related_Surveys_Comparison.md)。

## 2. AUTALIC（R2A-013；ACL 2025 Main，CCF-A；Ch5 §5.4）

### 2.1 四层裁决

| 争议 | 事实/作者报告/代码/怀疑 | R5可写边界 | 状态 |
|---|---|---|---|
| 规模与类别 | **F/P：** 正式PDF §3.2.3 断言总句数2400，正242、负2160；**242+2160=2402**。Table2单人票数595(-1)+5582(0)+1023(1)=7200=2400×3。这是**正式原文内部算术不一致**。 | “作者报告收集2400条；其最终正负计数在正文中存在2条差异，尚未用CSV确认。”不要编造“实际2158负例”。 | 论文矛盾**已证实**；真实CSV分布**OPEN** |
| 标注者 | **P：** 摘要笼统称trained experts，PDF §3.2.1详述9名经培训的高年级本科研究志愿者，每句3人标；不是全员持证专家/临床人士。作者报告Fleiss κ=0.25。 | “经专题培训的本科研究志愿标注者；保留个体意见与分歧，最终以多数票构成二分类。”不能称完美客观意图金标。 | **CLOSED（身份表述）** |
| 语境依赖 | **P：** 论文展示引用、反讽、社群求助和医学化措辞受语境影响的定性样例；提供相邻上下文。**O：**缺同模型target-only vs target+context的等条件定量对照。 | “为语境化社会规范标注提供案例与分歧证据”，不能说“定量证明加入语境提升X点F1”或“模型一定未恢复说话人意图”。 | 质性证据**CLOSED**；因果定量**OPEN** |
| 许可与获取 | **P/S：** 作者公开加密ZIP及项目页获取口令。附录允许符合使用指南的非商业学术研究，禁止擅自再分发；商业用途及开发/部署自动化审核工具需先获明确批准。未打开原始CSV。 | 可以引用论文和统计争议；要做训练或复现须核定用途、授权与版本，不把“学术”自动理解为开发审核器免责。 | 公开许可条款**CLOSED**；具体模型训练许可边界、CSV**OPEN** |

### 2.2 本轮新增书目冲突：PDF 与 ACL Anthology 自动BibTeX

- **F：** 同一个 [ACL Anthology条目](https://aclanthology.org/2025.acl-long.1022/)（DOI **10.18653/v1/2025.acl-long.1022**）网页/BibTeX列出12名作者。
- **F：** 该条目所链[正式PDF首页 p.20999](https://aclanthology.org/2025.acl-long.1022.pdf#page=1)实际列**13名作者**：包括 **Michael Golden**；且PDF中 Tristan Cooper 排在 Alexis Morales-Flores 前，网站列表顺序和写法不同。
- **F：** ACL Anthology条目自身“Correct Metadata”区提示PDF为权威校对基准。
- **裁决：出版网页的作者元数据与其正式PDF有真实可见冲突。** 目前不能自作主张改写馆藏BibTeX，也不能说“已通知/已修正”。建议投稿书目核查时依据PDF核作者并向Anthology提交元数据更正；在未更正前保留双版本记录，正文用**Rizvi et al. (2025)**可避免误列所有作者。
- **状态：新发现F，冲突OPEN；比起已关闭的年份/DOI，此项需要单独追踪。**

**原始证据：** [ACL正式页](https://aclanthology.org/2025.acl-long.1022/)；[PDF](https://aclanthology.org/2025.acl-long.1022.pdf) §3.2和Appendix A.1；[作者GitHub](https://github.com/nrizvi/AUTALIC)；[作者项目页](https://nrizvi.github.io/AUTALIC.html)。本轮对PDF首页与p.21003作了可视核查。

**推荐措辞：**“Rizvi等（ACL 2025 Main，CCF-A）提出含相邻话语语境的反自闭症歧视数据集AUTALIC，由经培训的本科研究志愿者多重标注，并报告标注分歧和社会语境中的定性误判案例。数据总数在文中报告为2400，但二分类正负计数相加不符；本综述不对原始类别分布作独立重估，也不将案例解释为语境作用的定量因果效应。”

## 3. MCIB（R2A-024；AAAI 2026 Technical Track: Machine Learning VIII，CCF-A；Ch6 §6.5）

| 主张或实现点 | 证据 | 裁决与允许引用 | 状态 |
|---|---|---|---|
| 出版 | **F：** AAAI Vol.40 No.31，26652–26660，2026-03-14，DOI **10.1609/aaai.v40i31.39874**；AAAI官方页面列Technical Track Machine Learning VIII | **正式发表且Track确定**；不能称“AAAI最佳论文” | CLOSED |
| 整体分类效果 | **P：** 作者报告MUStARD++R weighted F1=75.64；Table2去细粒度71.19（差4.45个百分点）、用MLP替代Transformer74.32（差1.32pp） | “作者报告完整配置性能与两种结构消融”。不是本项目训练复现。 | CLOSED（可限量引用作者报告） |
| 条件IB目标的独立贡献 | **P/O：** 没有完整网络只去KL、只去条件预测、两者都去的同参数/同预算正交消融；SIB/DIB/ITHP是不同完整系统 | **不能量化CIB单独带来多少提升**，更不能将性能提升归因于“真实互补语义恢复” | OPEN |
| 理论/代码统计目标 | **P/S：** 论文主文 Eq(9–10)为条件对数似然代理；arXiv扩展附录 Eq(34)形式不同；公开Transformer代码使用抽样预测的MSE+KL而非字面相同NLL | 存在理论/发布实现待对齐，不能反推正式训练错误；**代码配置并不直接证明最大化所声称的条件互信息** | OPEN |
| Tensor形状 | **S：本轮再次直接核公开 [MCIB_trans.py](https://github.com/sljgkjhwe/MCIB/blob/main/MCIB_trans.py#L110-L125)**：y_pred来自num_labels=1通道，通常[B,1]，而 y.squeeze(-1)通常[B]，MSE广播[B,B]；R3曾用小张量验证该行为。备用MLP版处理不同。 | “当前公开Transformer路径存在非逐样本监督的高可信广播风险”；**不得说正式论文必然受到这一bug影响** | S风险已证；正式运行路径OPEN |
| 瓶颈旁路 | **S：** [MCIB_trans.py #L194–224](https://github.com/sljgkjhwe/MCIB/blob/main/MCIB_trans.py#L194-L224)为expand(output)+x，x是原始DeBERTa文本表征 | “最终分类器不是严格仅依赖CIB压缩后表征”；这不构成残差设计自身错误 | CLOSED（源码结构）/机制OPEN |
| 脚本/复现 | **S：** [MCIB_trans_Train.py](https://github.com/sljgkjhwe/MCIB/blob/main/MCIB_trans_Train.py)采用KFold(5)但fold_idx>0时break；读取本地features_Process/*.pkl；不同于充分公开的五次完整fold复现实验 | 公开脚本不足以独立对齐全部正式实验；不等于作者没做实验 | OPEN |
| 细节指标 | **R3既有审计：** Table1 SpeechPrompt-v2的weighted P/R/F1数值与通常加权均值关系存在疑点，正文还把某列Precision称accuracy | 在论文指标脚本明确前，**不要强引该行作为严格29.88pp捷径因果证据** | OPEN |

**最小可引用结论**：“Wang等（AAAI 2026 Technical，CCF-A）提出面向音/视/文本反讽的条件信息瓶颈融合，并报告MUStARD++R上的整体加权F1及结构消融；目前缺少同结构控制实验来量化条件IB的独立收益。公开Transformer路径的条件MSE与残差使用方式进一步限制了‘通过IB已去除标签捷径’的强机制解释。”

**代码审计范围说明：**本轮通过GitHub连接器读取当前 [MCIB_trans.py](https://github.com/sljgkjhwe/MCIB/blob/main/MCIB_trans.py) blob SHA **2570266d66e6fca4f3e4c03e0b860db4003a4416**、[MCIB_trans_Train.py](https://github.com/sljgkjhwe/MCIB/blob/main/MCIB_trans_Train.py) blob SHA **8a9dc35f3722c86fd0b58a664d9796e4c5d4fb13**。**本轮未重跑小张量测试或训练**，其测试记录出自R3专项；源码行号基于此次实际内容。

## 4. VLSU及跨模态安全（P038；ICLR 2026 Conference，CCF-A；Ch7 §7.1–7.2）

### 4.1 三层真值、S-S-U 与版本

- **F/P：** [ICLR 2026正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)明确报 **8,187**条、**15**风险类、**17**安全组合模式，示例任务分别有人审的image-only、text-only、joint三种严重度：Safe/Borderline/Unsafe。**Borderline是安全等级，不是标注者不确定概率。**
- **S（R3/P038已做逐行审计、非本轮重读）：** [作者公开CSV](https://github.com/apple-aiml-research/ml-vlsu/blob/main/data/VLSU.csv)为**8,159**行（比论文少28），公开 CSV 联合三类计数2189/3310/2660，存在image_grade=not_sure **141**条，实际三元组可能超过文中所取17模式；要指出观察时间及作者repo版本，不能假定差额都是错误或删去了哪28条。
- **P vs S（上游已核）：** 正式论文Figure9严格 **S-S-U=37**；当时公开CSV严格 **S-S-U=35**。S-S-U意思是**图单独Safe、文单独Safe、合起来Unsafe**，只是joint风险类别之一；不能把公开179个联合风险升级子集都叫S-S-U。35条属于此前读取的**官方test-only**切片，样本很少。
- **P：** 正式论文 Figure5的“约34% Both Correct”分母是**联合预测失败的样本**，且两种单模态预测正确；不是全体样本比例、也不是S-S-U子集上的错误率。
- **F：本轮新增出版摘要冲突：** [ICLR官方摘要网页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)及[Apple研究官网文章](https://machinelearning.apple.com/research/vlsu)仍写评估**11个**模型，但会议**正式PDF首页明确写17个**。这是网页摘要和正式PDF版本不一致，不能把“官方页11”与“正式PDF 17”无声明地混同。**正式主结果用PDF 17口径，同时在引用登记中说明网页仍为11。**
- **S：** 当前作者README继续用8,187作为**论文声称**；该文本不证明公开CSV行数也为8,187。数据许可证标为CC-BY-NC-ND，代码ASCL；图片来自网页链接，图片权利/可用性需单独看。
- **O：** 为何少28、image not_sure如何映射、逐条图像下载可用率、17模型统一评估代码和行为提示词逐字复现尚未关闭。

### 4.2 理解风险 vs 安全响应，不得混算

| 任务/对象 | 输入X、GT及输出Y | 指标的意义 | 不可外推 |
|---|---|---|---|
| **VLSU Safety Understanding** | X=图/文/图+文；GT=image/text/joint安全等级（含Borderline）；Y=模型对安全等级分类 | 三分类Acc/F1或Table1为兼容比较时**Borderline合并到Safe**的二分类协议 | **不能**把其结果当行为拒答率；不得把论文的二分类表与三分类F1直接排名 |
| **VLSU Safety Alignment** | X=图文请求；Y=生成的回应；评审GPT-4o判断拒答与有用性 | 拒答率/帮助性，非输入风险“是否判断正确” | **不能**将拒答视作识别GT；helpful提示不等于安全 |
| **SIUO（P041）** | 图文独立看似安全而联合使模型生成危险响应的安全对齐挑战 | ASR、模型行为、攻击/回答判别 | NAACL 2025 **Findings**（会议CCF-B），不是NAACL Main；不等于VLSU的三等级人审输入GT |
| **MSSBench（R2A-027）** | 情境安全与行为执行/拒绝评测 | 情境下的指令遵循/安全行为指标 | 不能拿输出执行率直接当输入hazard分类召回 |
| **ThinkingGuard/TriggerBench（P039）** | 图文配对，Safe/Unsafe及风险解释 | 作者报告F1/recall，偏输入识别和结构化归因 | 其Safe/Unsafe是合成协议，不能自动等于VLSU人审联合标签 |

**审慎表述：**“VLSU（ICLR 2026，CCF-A）把单图、单文和联合图文的安全程度分别标注，并区分安全等级判别与后续回应的拒答和帮助性。论文提出17种安全组合模式；但正式论文与当前公开CSV的总数及严格S-S-U计数存在版本差异，其少量S-S-U样本不应被当作整个多模态风险分布的代表。”

## 5. ThinkingGuard出版、Track与竞争证据（P039；Ch7 §7.3）

| 主张 | 实际可核来源 | 裁决 |
|---|---|---|
| 获ACM MM 2026录用 | [作者GitHub README](https://github.com/FroggyChen/ThinkingGuard)明确2026-07录用；[研究组出版页](https://rose-vision.github.io/publications/)将ThinkingGuard列ACMMM2026 **Oral**；[arXiv v1](https://arxiv.org/abs/2609.36562)写accepted ACMMM 2026 | **录用及作者/课题组口径证实**，但仍是作者侧信息，不等于已取得ACM官方最终记录 |
| DOI和书目 | 作者README给**10.1145/3767308.3835707**，提供booktitle “Proceedings of the 34th ACM International Conference on Multimedia (MM '26)”；arXiv关联DOI | **DOI存在作者声明和关联线索**，本轮尝试独立打开ACM/DOI主页未成功；**未独立获取ACM出版社正式条目和页码** |
| 实际Track | 作者实验室称“Oral”，表示报告形式；官方技术日程当前可检索页面未提供可核对的本篇Track字段 | **Oral不等于Research/Main/Technical Track已证实**。目前不能把作者录用、口头报告和正式Technical Track当作同一件事 |
| 时间 | ACM MM 2026会议日程为**2026-11-10至14日**；本审计日期**2026-11-09**，会议尚未开始 | 本次最严格写“作者报告已获ACM MM 2026接收，已给出DOI；正式ACM目录和具体Track待独立核对” |
| 作者BibTeX质量 | 作者README BibTeX含Markdown链接塞入url字段，如 url={[https://github.com/...](https://github.com/...)}，**不是可直接可信编译的正式出版社BibTeX** | 作者条目是**待校对引用草案**，不可作为“已核ACM官方BibTeX” |
| 方法先例 | [P039精读卡](../../01_literature/cards/P039_ThinkingGuard.md)作者报告5600条，SA-MCTS/Trajectory+Step DPO、基于Qwen3-VL-8B；当前公开仓库主要README+inference.py，完整搜索/奖励/训练代码未见 | **已存在强竞争方法先例**；其奖励有效性、反事实单因素编辑、等预算Step DPO独立增益仍是O；不得宣称已经严格因果归因 |

**正式综述推荐表达：**“Zhang等提出ThinkingGuard，作者称已被ACM Multimedia 2026（该会议CCF-A）接收，并以合成图文触发样本、逐步风险归因和偏好对齐研究联合风险检测；截至2026年11月9日，本文尚未独立核实ACM正式出版条目和具体Track。因此在正式发表状态和机制因果归因上保留限定。”

**必要提醒：** 实验室“Oral”是**支持存在报告安排的作者侧记录**，不是委员会颁发的Track元数据；发表状态不能仅由DOI字符串逻辑推出。

## 6. 其他高优先级书目/版本与BibTeX准入

以下内容是**正式入口和引文状态登记**，不是手工编造的完整BibTeX文件。正文参考文献应从出版方实际BibTeX导出并校PDF；有冲突者不得直接复制。

| 项目 | 正式信息/等级 | 首选出处 / BibTeX key 或处理 | 本次结论 |
|---|---|---|---|
| **P011语用综述** | ACL 2025 Main，**CCF-A**，DOI 10.18653/v1/2025.acl-long.425 | [ACL Anthology](https://aclanthology.org/2025.acl-long.425/)；正式BibTeX可从网页复制 | **CLOSED**出版/Track |
| **P002修辞综述** | ACM CSUR，2025在线/2026卷58(2) Article42，**CCF未收录（上游R4）** | [DOI](https://doi.org/10.1145/3744554)；2024 arXiv不可作为最终年份 | **CLOSED**版本区分；全文差异O |
| **P007仇恨综述** | EMNLP 2024 **Findings**，会议**CCF-B**，DOI 10.18653/v1/2024.findings-emnlp.254 | [ACL正式页](https://aclanthology.org/2024.findings-emnlp.254/)，key **hee-etal-2024-recent** | **CLOSED**出版/Track |
| **R2A-013 AUTALIC** | ACL 2025 Main，**CCF-A**，DOI 10.18653/v1/2025.acl-long.1022 | [ACL正式页](https://aclanthology.org/2025.acl-long.1022/)，key **rizvi-etal-2025-autalic**；**PDF/网页作者差异，暂不使用未经核对的完整作者字段** | **OPEN**新作者冲突 |
| **R2A-024 MCIB** | AAAI 2026 Technical Machine Learning VIII，**CCF-A**；vol40(31):26652–26660；DOI 10.1609/aaai.v40i31.39874 | [AAAI正式页](https://ojs.aaai.org/index.php/AAAI/article/view/39874)；作者王义华等（Yihua Wang et al.） | **CLOSED**出版，机制OPEN |
| **P038 VLSU** | ICLR 2026 Conference，**CCF-A**，无须杜撰DOI/页码 | [ICLR正式条目](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)和[正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)；作者README里的**palaskar2025vlsu是arXiv 2025**，不是正式ICLR 2026条目 | **CLOSED**正式venue；**OPEN**官网摘要11 vs PDF17、CSV差异 |
| **P039 ThinkingGuard** | ACM MM 2026（会议**CCF-A**；**实际Track及ACM正式出版权威记录未核**） | [作者README](https://github.com/FroggyChen/ThinkingGuard)，作者给DOI 10.1145/3767308.3835707；不可当出版社BibTeX | **OPEN** |
| **R2A-010 SeTox** | ACL 2026 Main，**CCF-A**，DOI 10.18653/v1/2026.acl-long.1602 | [ACL正式页](https://aclanthology.org/2026.acl-long.1602/)；key **cui-etal-2026-new**。R2-D已发现作者repo README与ACL正式书目冲突，**必须以ACL记录为准** | **CLOSED**正式书目；作者README冲突未改 |
| **P034 CrossGuard** | ACL 2026 Main，**CCF-A**，DOI 10.18653/v1/2026.acl-long.1178 | [ACL正式页](https://aclanthology.org/2026.acl-long.1178/)，key **zhang-etal-2026-crossguard** | **CLOSED**出版/Track |
| **P041 SIUO** | NAACL 2025 **Findings**，会议**CCF-B**，DOI 10.18653/v1/2025.findings-naacl.198 | [ACL正式页](https://aclanthology.org/2025.findings-naacl.198/)，key **wang-etal-2025-safe** | **CLOSED**发表类型；与T5 GT不同 |
| **P040 Meerkat-VL** | ICML 2026，**CCF-A** | [PMLR论文入口](https://proceedings.mlr.press/v306/zhou26ae.html)；此次没有成功重取页面正文，沿用已归档书目，**本轮不声称再次独立核BibTeX** | 先前归档；本轮**未追加关闭** |

### 需要给撰稿Work的精确修正通知（无需改正文）

1. Ch1 §1.2：至少对照P011/P007/P002与IJCAI 2024 Survey Track，不写“首篇”。
2. Ch5 §5.4：AUTALIC保留2400 vs 2402的矛盾、9受训本科志愿者、无上下文因果消融、许可；新增PDF/ACL Anthology作者不符。
3. Ch6 §6.5：MCIB最多表述整体F1和模块配置，不能把条件IB当作已独立验证的去捷径手段；公开代码问题须加“当前公开实现，未证明正式训练受影响”。
4. Ch7 §§7.1–7.3：VLSU正式PDF17模型而官方摘要网页11；8187论文 vs 8159上游CSV、S-S-U=37 vs 35；风险等级分类和响应拒答必须不同表列。ThinkingGuard写“作者称接收、Track待核”。
5. 其他：SeTox正式ACL BibTeX覆盖README；Findings与Main / D&B/Survey/Technical不等价。

## 7. 最终状态：关闭的是**证据定位和可写边界**，不是全部研究疑问

| 事项 | 可关闭 | 必须保持OPEN |
|---|---|---|
| 已有综述差异 | 子域重叠及本综述组织贡献的谨慎边界 | 完全穷尽的先行综述对照、逐篇全文纳入时间窗 |
| AUTALIC | 身份、许可公开原则、算术不一致的存在、质性案例可引 | CSV类别计数、语境定量因果、具体审核工具许可、PDF/官方网页作者冲突 |
| MCIB | AAAI出版/Track、整体结构消融为作者报告、当前代码广播风险/旁路 | IB独立收益、正式实验版本和数据复现、代码与推导一致性 |
| VLSU | 三层GT与风险理解/响应分离、官网与PDF模型数冲突存在 | 28行差、35/37模式原因、图像有效率、评审prompt |
| ThinkingGuard | 作者侧录用及DOI声明存在、方法先例 | ACM官方正式书目及Track、出版社BibTeX、配对有效性和公平Step-DPO归因 |
