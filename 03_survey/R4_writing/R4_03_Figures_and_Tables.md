# R4-03｜正式综述的图表体系与制作规范（审阅稿）

> 2026-11-08｜状态：R4 REVIEW DRAFT。**这里只规划图表/给出可执行结构草图，不制作或声称已完成最终图片**。所有图应自行绘制，避免直接复制原论文图和版权问题；正式写作前需补版权、引用和出版核验。
>
> 来源：R1 T1–T6、R2-C、R3-A1/A2/A3/A4、R3-B AUTALIC FINAL与MCIB REVIEW。图表不用于证明尚无数据支持的心理机制或严格因果关系；“概念关系”只表示综述组织框架。

## 0. 整体建议

**建议：6张原创概念图 + 8张核心对比表**。用户可根据投稿目标缩减为四张主图（F1/F2/F4/F5）、五张主表（T1/T2/T3/T5/T6），其余移至附录。优先提供SVG/PDF矢量原图（矢量文件需自行生成）；最终稿中的引用按论文/数据来源列于图注。

**图形规范**：
- 术语中英首次并列；颜色仅作任务层或研究家族编码，**不能**以颜色表示作者论文优劣；
- **实线**表示本文定义的逻辑连接或同一个研究场景的已知关联；**虚线**表示可能的、未经实验证实的跨任务影响；**不使用箭头隐含已验证因果链**；
- 图中的“安全/有害”必须相对明确的GT、风险策略与语境，不应用模糊“普遍正确”语气；
- 模型或数据实验主表数值按原论文任务协议/作者报告分别标明，不跨研究拿F1/Accuracy/安全响应率画统一排行榜；
- 如果图中需要例句，建议用作者许可可再述的**自构造无害例子**，标注“作者示意，非真实标注数据”，不要直接复制受限样本。

## 1. 六张图的正式制作清单

| 图号/位置 | 拟定标题 | 应在图中展示的实体和关系 | 支撑来源与直接主张 | 必须避免的错误 |
|---|---|---|---|---|
| **F1 / Ch1** | **广义隐晦信息研究的并行谱系与交叉问题** | 六条研究线：语用、修辞、社群编码、语境有害性、多模态非字面、多模态风险；用交叉节点标T1/T2/T3/T4/T5/T6与共享语境/模态信息 | R3-A1、R2-C；P020 ACL2025 A、P023 ACL2026 A、P038 ICLR2026 A | 不画成“仇恨分类→LLM→VLM”的统一时间进步箭头；不能声称首次 |
| **F2 / Ch2** | **表达机制、任务、模态条件与证据之间的正交关系** | (A)表达机制：implicature/figurative/coded；(B)任务T1–T6；(C)条件：文本/图文/音视频/对话；(D)信息预算：原始/词典/检索/Oracle；(E)评测：GT/干预/行为 | R1 Task=(X,Y,G,E)；DRInQ ACL2026 A、VAGUE ICCV2025 A、AUTALIC ACL2025 A | 不让每一例都必须依次先检测、再解释、再检测有害；T5不是所有多模态任务上级 |
| **F3 / Ch4** | **社群编码：词项发现、语境消歧、含义解码与危害判定** | 四个并列模块，共享文本/社群/时间上下文：type发现；给定D和定义的instance disambiguation；候选意义mapping；语境化T4判定；每模块下注明GT | Silent Signals ACL2024 A；FETCH! ACL2025 A；FA-Net AAAI2024 A；CodedLang ACL2026 A；SeTox ACL2026 A | 不能把FETCH!已有词典留出写成真实时间OOV；不给四模块画“全部完成后才可做T4”的必经箭头 |
| **F4 / Ch6** | **图文/音视频信息的联合关系与捷径诊断** | 左：独立模态证据及共同信息；中：真实相关关系与虚假相关捷径（OCR、gold情绪、speaker、笑声）；右：text-only/image-only/joint/controlled-pair比较 | MultiMM ACL2025 A；V-FLUTE NAACL2025 B；VLSBench ACL2025 A；MCIB AAAI2026 A | 不把加入图性能提升误画为已证实因果互补；MCIB是文本/音频/视频反讽，不是Meme |
| **F5 / Ch7** | **多模态风险判断与安全响应的四层可测对象** | G_in（人类/政策风险GT）；P_in（模型输入风险预测）；R_beh（拒绝/警告/执行等行为）；Q_out（输出安全、有效性）；分别连各自数据/评价，并画合法安全输入误拒反例 | VLSU ICLR2026 A；MMSafeAware ACL2025 A；MOSSBench/MSSBench ICLR2025 A；CrossGuard ACL2026 A；Meerkat-VL ICML2026 A | 绝不令输入F1、拒答率、输出安全率共享同一数值轴；“拒答”不等于“准确识别风险” |
| **F6 / Ch8** | **技术路线 × 研究瓶颈的机制对照图** | 6×5定性矩阵：词典/RSA、PLM对比域适应、LLM检索工具、多任务融合/LoRA、解释/偏好、Guard/RL；对应语境歧义、时间/OOD、细粒度意义、跨模态捷径、安全/有用性 | R3-A2；FA-Net AAAI2024 A、SeTox ACL2026 A、DOSE ACL2026 A、ExPO-HM ICLR2026 A、MCIB AAAI2026 A | 不用大小/深浅冒充实测性能，也不按年份把旧方法全部划掉 |

### F1 草图（概念路线，而不是因果时间轴）

下面是仅供作者绘图的Mermaid结构草稿，**不是正式论文的图像**：

\`\`\`mermaid
flowchart LR
  A["语用含意 / 间接言语行为"] --- S["情境化意义与任务目标"]
  B["修辞 / 非字面映射"] --- S
  C["社群编码 / 狗哨 / 新词"] --- S
  D["语境有害性 / 规范"] --- H["危害性判断 T4"]
  E["多模态非字面关系"] --- M["跨模态语义"]
  F["联合风险与安全响应"] --- R["输入风险T5 / 输出行为T6"]
  S -. "可能关联；非必然因果" .-> H
  M -. "情境与组合关系" .-> H
  H -. "相关但评价不同" .-> R
\`\`\`

Mermaid图在GitHub正文里应检查预览；正式导出矢量时把所有“可能关联”改为可辨识虚线，保持五轴与T5/T6边界。

### F5 草图（变量之间有关联、指标必须独立）

\`\`\`mermaid
flowchart TD
  X["输入：图像I、文本T、情境C"] --> G["G_in: 输入人审风险GT"]
  X --> P["P_in: 模型预测风险标签"]
  P --> R["R_beh: 拒答 / 警告 / 正常帮助 / 违规执行"]
  R --> Q["Q_out: 实际输出安全与帮助性"]
  G -. "有标签时可比较" .-> P
  G -. "政策条件下的合理行为" .-> R
  G -. "不等于" .-> Q
\`\`\`

该图是**测量分层**。P_in并非所有研究都显式输出：若仅观察最终回复，内部风险预测可能不可直接观测，所以P_in到R_beh的箭头也不表示已由论文证明内部因果。

## 2. 八张正式综述核心表

| 表号/位置 | 推荐表名 | 列字段（必须含证据状态） | 优先比较的论文（会场、CCF） |
|---|---|---|---|
| **T1 / Ch2** | **广义隐晦信息六类概念的必要条件与交叉** | 术语；性质；是否必须非字面；是否必须意图隐藏；是否必然有害；任务例；典型反例 | P011 ACL2025 A、P023 ACL2026 A、R1；理论经典不设CCF |
| **T2 / Ch2–3** | **T1–T6任务定义与GT可观测性** | Task；输入X及额外先验；输出Y；GT G及标注主体；评价E；限制；例证 | DRInQ ACL2026 A、VAGUE ICCV2025 A、V-FLUTE NAACL2025 B、VLSU ICLR2026 A |
| **T3 / Ch4** | **编码语言基准与开放词义协议对比** | 论文ID；已知词/未知词；type/instance；可用词典义；真实时间划分否；标签者；指标；许可；全文证据状态 | Silent Signals ACL2024 A、FETCH! ACL2025 A、FA-Net AAAI2024 A、CodedLang/SeTox ACL2026 A |
| **T4 / Ch5** | **隐晦有害数据的标签来源与歧义** | 论文；GT是否含implicit定义；是否有人审隐含解释；样本来源；有无引用/社群语境；标注分歧；安全负例；主要限制 | T017 Latent Hatred EMNLP2021 B、ToxiGen ACL2022 A、When People are Floods ACL2025 A、AUTALIC ACL2025 A |
| **T5 / Ch6** | **多模态修辞理解任务—方法—额外输入** | 论文；模态；目标任务；解释/源目标GT；是否用gold情绪/域；主干与loss；模态消融；训练/测试捷径风险；证据等级 | MultiMM ACL2025 A、V-FLUTE NAACL2025 B、MGMCF AAAI2025 A、M3UCD AAAI2026 A、DOSE ACL2026 A、MCIB AAAI2026 A |
| **T6 / Ch7** | **多模态风险与安全响应：输入/输出标签协议** | 论文；输入是否明确safe/unsafe/borderline；单模态标签；联合风险配对；模型输出分类/回答；Safe及Unsafe两侧指标；Judge；test-only/许可 | Hateful Memes NeurIPS2020 A、VLSBench ACL2025 A、MSSBench/MOSSBench ICLR2025 A、VLSU ICLR2026 A、CrossGuard ACL2026 A、Meerkat-VL ICML2026 A |
| **T7 / Ch8** | **方法族、训练信号与已提出的竞争性机制** | 方法；监督来自何种标签/外部知识；训练or推理；是否需要检索/付费模型；作者指标；关键公平基线；未证；直接竞争 | P020 ACL2025 A、ImpCon COLING2022 B、FA-Net AAAI2024 A、SeTox ACL2026 A、DOSE ACL2026 A、ExPO-HM ICLR2026 A、RV-HATE ACL2026 A |
| **T8 / Ch8或附录** | **证据透明与可复现性风险清单** | 论文ID；问题类别；已证实P/S/T/H/O；具体数值/代码版本；受影响结论；已关闭/未关闭；使用许可 | AUTALIC ACL2025 A、VLSU ICLR2026 A、DRInQ ACL2026 A、MultiMM ACL2025 A、MCIB AAAI2026 A、RV-HATE ACL2026 A |

**主文 vs 附录建议**：T1/T2/T3/T5/T6放正文；T4/T7可根据篇幅正文压缩；T8完整表建议在线附录/补充资料，正文仅展示最有代表性的反例及方法论规则。

## 3. 必须保持严格的数字证据

| 数据/方法 | 可以列的数字性质 | 当前不能画的数字或注记 |
|---|---|---|
| R0/R2：59+32=91 | **本项目文献入账候选数**，不是全球年度发表数 | 禁止用这91条做“全领域近年研究数量增长曲线”或PRISMA流程图（检索召回不存在） |
| AUTALIC（ACL 2025 Main A） | 论文称2,400目标句、3位标注者/句、κ约0.25；需标论文报告[P] | 242正+2160负=2402，**不一致**；未打开真实CSV，禁按二者绘制精确占比柱状图；并遵守限制用途 |
| VLSU（ICLR 2026 Main A） | 论文设计3层风险、17种目标组合；公开CSV含8,159记录和not_sure，由P卡静态审计 | 不把论文8,187与公开8159混为同版本；严格S-S-U的公开35条不能写37且不报区间；官方test-only不可无声明作训练集 |
| MCIB（AAAI 2026 Technical A） | 作者报告R数据weighted F1=75.64、文本/音频/视频三模态；R3-B稿含方法/源码差异[S/O] | 不画“无捷径 vs 有捷径”因果前后提升证明图；SpeechPrompt v2表内P/R/F1有数学疑点，未核实前不用该行作精确可视化 |
| MultiMM（ACL 2025 Main A） | 论文报告跨文化/源目标/情绪标签与相应对照 | gold情绪测试输入不是部署预测情绪；不得在图上当同输入预算纯图文baseline |
| MOSSBench（ICLR 2025 Main A） | 安全请求中模型输出是否拒绝/响应等行为指标 | 禁把安全请求误拒率和输入Unsafe二分类混画 |
| ThinkingGuard（ACM MM 2026刊会A） | 方法可按作者录用稿描述；正式元数据待核 | 不能直接列入“经官方验证已正式出版的CCF-A Main论文总数” |

## 4. 图表制作优先级和工单

| 优先级 | 图表 | 可直接使用的资料 | 需要追加的人工/静态核验 | 完成标准 |
|---|---|---|---|---|
| **P0** | F1、F2、T1、T2 | R1任务框架、R2-C、R3-A1/A2 | 核词汇边界，避免多任务层级混淆 | 每个节点有定义/反例、所有箭头不表示未经证实的因果 |
| **P0** | F3、T3 | Silent Signals/FETCH!/FA-Net/CodedLang/SeTox精读 | 核词典留出、是否给定词义与可用许可 | type/instance/meaning/harm四栏可与各篇论文一一匹配 |
| **P0** | F4、T5 | MultiMM、MGMCF、M3UCD、DOSE、V-FLUTE、MCIB | MCIB最终审计；MultiMM和MGMCF额外输入协议 | 所有模型方法标签有可追溯原文；无假“因果视觉理解” |
| **P0** | F5、T6 | VLSU、MSSBench、MOSSBench、CrossGuard、Meerkat-VL | 区分数据标签 vs Judge行为；VLSU版本 | 文字解释变量不同，误拒与漏检均可表示 |
| **P1** | F6、T7 | R3-A2方法史和竞争矩阵 | 只从已验证训练协议归类 | 无SOTA排行榜/虚假跨任务排名 |
| **P1** | T4、T8 | AUTALIC R3-B、R2-C/P卡静态审计 | AUTALIC许可及类别数，MCIB指标口径，P039出版 | 数值都带证据/数据版本，无歧义指标脚注 |

**时间顺序（不表示异步承诺）**：先确定F1/F2逻辑，冻结T1/T2的GT定义，再画F3/F4/F5；最后通过T7/T8审计前面每张图/表。对尚缺实物的dataset图像和原文不制作任何“真实统计曲线”。

## 5. 参考来源和论文主分配

- [R4正式目录](R4_01_Formal_Outline.md)
- [R4全91篇论文唯一主归属](R4_02_Paper_Allocation.md)
- [R3-A2六大方法谱系](../R3_evolution/R3A_Method_Evolution.md)
- [R3-A4证据门槛（审阅稿）](https://github.com/YuSun-WK/implicit-content-research/blob/survey/r3-a4-evidence-audit-review-20261108/03_survey/R3_evolution/R3A_Coverage_and_Evidence_Audit.md)
- [R3-B AUTALIC定稿](../R3_targeted_reading/R3B_01_AUTALIC_FINAL.md)
- [R3-B MCIB审阅稿](https://github.com/YuSun-WK/implicit-content-research/blob/r3b-mcib-targeted-review-20261108/03_survey/R3_targeted_reading/R3B_02_MCIB_REVIEW_DRAFT.md)

> 本文为图表设计工作单，尚未获用户定稿授权，未绘制或导出图像文件；任何论文数值图、授权受限语料图与原论文图片复用都需在后续单独核验。
