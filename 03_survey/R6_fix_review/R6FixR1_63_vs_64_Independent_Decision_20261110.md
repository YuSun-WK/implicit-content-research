# R6-Fix-R1｜双分支独立比较终裁（2026-11-10）

**裁决：选择PR #63（`survey/r6fix-r1-targeted-revision-20261110`，HEAD `80bad7e668a5510f7897b8ee117d7851ebaa8114`）为唯一科学修订主版本；PR #64（`survey/r6fix-r1-targeted-gates-20261110`，HEAD `0df7e4f694e40325b2f3d566efada79704e543ec`）不再作为并行主版本。**

**R6-Fix-R1八项：阶段性学术判定8项CONDITIONAL CLOSED/GO FOR FINAL INTEGRATION，前提是合并前处理下述确定性引文定位及论文最终格式问题。这不是投稿终稿通过，也不是对作者运行的独立复现。** 本判定仅针对PR#62留存的8个PARTIAL及受影响的一致性，先前已关闭16项原则上不重复开审。

## 一、为什么选#63（比较的是学术证据，不是提交次数）

| 维度 | #63（选用） | #64（不选用） | 判定 |
|---|---|---|---|
| P0-01 / 跨子领域实质增量 | C1：(RSA)²修辞意义先验×FETCH编码词根发现；C2：DRInQ文本含意、VAGUE视觉行动意图、ExPO-HM解释监督；C3：(RSA)²字面/反讽子群与VLSU安全/帮助拒答子群。每个条件附P级具体数、同论文反例、异质协议限制及可否证预测 | C1：FETCH×DOSE候选、性能改善对照，但DOSE结构+1.2pp并不直接检验候选空间的因果贡献；C2：文本SMARTER缺同预算量化，而主要实数出自两个多模态研究；C3：VLSU与CrossGuard主要在同一多模态安全大类且评价主体不同 | #63更接近先行综述×分析单位×跨领域条件证据这一P0门槛；**仅能作为H级学术综合，不是共同机制或meta-analysis** |
| P0-02 / 公开证据 | 附录A六组作者公开仓库的40位commit/file#line、逐条O限制、固定VLSU公开CSV及计数方案；本次独立从GitHub直接读取6/6固定作者源码路径均成功 | §8.7也有六组公开源码，基本满足外部可访问门槛，但没有#63同样完整的发布版CSV检查小附录 | 两者均满足关键公开入口，#63审计闭环更完整 |
| P1-03/01 | 七行X_raw/train_aux/test_aux/Y/G/E具体协议；49条引用按用途/证据层级逐键附录B，公开审稿人可看清来源边界 | 有协议小表与49条Bib，但纳入用途分组及正文P/S平行示例简略 | #63可审性较好 |
| P1-05 FETCH | #63使用Balanced：EarShot PREDICT 14.81/1.65/5.70；DIRECT LLaMa13B 2.97/13.58/3.52 | #64使用Realistic：EarShot PREDICT 10.00/1.47/4.63；DIRECT LLaMa8B F0.5 1.17 | **两组都与ACL2025正式PDF Table4/5相符；属不同场景不是科学冲突**，#63现有量化已经充分 |
| 相邻综述 | #63引入Ye等2025 arXiv预印本（仅摘要/目录定位）及Ma/Farabi/Hee/Kühn | #64引入Mao等2025 `Information Fusion`正式短综述，DOI `10.1016/j.inffus.2024.102712` | **#64这一点有值得保留的增量**，最终整合时可向#63补充Mao（不复制#64 C1–C3） |
| 原九章结构 | #63按正文附录A/B放证据与49键用途清单 | #64于第8章新增§8.7，可能偏离R4固定8.1–8.6主框架 | #63适合最终排版的正文/附录分层 |

## 二、8项逐条审核终裁（以#63为主）

| 原Gate/问题 | R1内容在实际正文或表中的定位 | 独立审核结果与限制 |
|---|---|---|
| **A / P0-01** | 第1章§1.2先行综述对照；§8.1.1 C1–C3；表7 | **CONDITIONAL CLOSED**：跨修辞/编码、语用/视觉/仇恨分类、修辞/安全响应三组可证伪H假设有跨子域作者P数据和反向组别，且承认无相同预算因果试验。保留“支持条件性审计视角”而非“已证明通用机制”的限定；不得说前人没有这些分析。 |
| **B / P0-02** | 随稿附录A，A1–A6；VLSU固定CSV重计；T3/T5/T6/T7 | **CONDITIONAL CLOSED**：本轮直接访问六组40位commit源码文件6/6；RV-HATE公开脚本含test_data传递，CADET loader含train/test/test，MultiMM读取CSV row[5]构造senti，MGMCF加载source/target pkl，MCIB loss含squeeze与残差，Meerkat-VL提示含规范风险文本。稿件各项保留S≠论文正式训练run的O，不依赖本私有仓库。固定发布数字或已降级。 |
| **C / P1-08** | 表5、表7、附录A A3–A5 | **CLOSED**：所审公开代码路径固定，但正式run、辅助属性来源、实际batch等仍O，没有代码未固定vs已固定的新矛盾。 |
| **D / P1-12** | 第7章§7.2、表6，GateD正式PDF核验报告 | **CLOSED（限正式材料分析）**：将VLSU Figure5的33.8%限定为Qwen2.5-VL-32B示例joint三分类已错集合中的both-correct条件份额；不把它当17模型/全库汇总；附录E.3/Fig18与发布CSV分开。固定正式图PDF第8/39页可查；本独立环节通过PDF文本+前次直接读图记录，未重跑模型。 |
| **E / P1-01** | §1.4、附录B | **CLOSED**：59+32=91仅候选登记；49引用逐键用途与F/P/S/H/O级别；无PRISMA伪流水，叶氏预印本的全文证据限缩。 |
| **F / P1-03** | 第2章协议实例表（DRInQ/VAGUE/MultiMM P与S/DOSE/VLSU分类与回应） | **CLOSED**：七行把X_raw、训练与推理额外信息、Y、G、E/分母和未核同预算对照分开；没有把G默认当推理输入。 |
| **G / P1-05** | 第4章§4.3、表3、表7 | **CLOSED**：FETCH正式Table4/5 Balanced P,DPR,F0.5与root/type分母正确；没有将词典20%留出改写成严格未来未知词。 |
| **H / P1-16** | 表7、§8.1.1 | **CLOSED**：拆FETCH/FA-Net、ImpCon/SMARTER；区分ImpForge攻击PPO与Guard LoRA/SFT，正反对照数字保持同论文条件，不跨任务排列SOTA。 |

**说明：CLOSED是原24根因问题中R1对应“当前范围内已按要求修补”的科研内容评审；残存O不会因本裁决消失。不能据此声称49条出版社字段、最终绘图缩版及正式排版已通过。**

## 三、已实核的原文锚点与两个必须修正的稿件瑕疵

- FETCH!，ACL 2025 Main（CCF-A），[正式论文Table4/5](https://aclanthology.org/2025.acl-long.284.pdf#page=8)：
  - Balanced PREDICT/BERT 14.81/1.65/5.70，与DIRECT LLaMa13B 2.97/13.58/3.52；
  - Realistic PREDICT/BERT 10.00/1.47/4.63，与DIRECT LLaMa8B F0.5=1.17。**不是同一场景或可直接等预算竞争模型。**
- DRInQ，ACL 2026 Main（CCF-A），[正式Table2](https://aclanthology.org/2026.acl-long.1597.pdf)：GPT-5-Mini 0.56→0.62，Claude Sonnet 4.5 0.65→0.62；数据是400困难项、三次in-context例采样。
- (RSA)²，ACL 2025 Main（CCF-A），[正式PDF](https://aclanthology.org/2025.acl-long.1019.pdf)：Table2总集L0 0.73→0.85；Figure4字面0.95→0.77；Table3在L1/指示变量配置下正确义后验均值约0.84、取消意义先验后0.51。**该概率并非Accuracy。**
- VAGUE，ICCV 2025 Main（CCF-A），[作者v3实验表](https://arxiv.org/html/2411.14137v3)：Table3 GPT-4o 64.6→66.4；**Appendix G中Qwen2.5-VL 72B 72.8→69.9的表号在作者v3 HTML实际是Table G4，不是#63稿中的“Table G6”。** 必须修复正文、表7及台账中同类“G6”引用，不改实数。官方[ICCV出版页](https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html)可作出版锚点。
- (RSA)²作者[arXiv HTML v1](https://arxiv.org/html/2506.09301v1)目前打开却显示“Instructions for *ACL Proceedings”而非论文本体，**不要继续把这个异常HTML页面当成Table2/3/图4的可独立核对入口**；使用上面已核正式ACL PDF及页/表锚点替代。此处是**引用链接故障，不代表RSA数值错误**。
- Mao等 *A survey on pragmatic processing techniques*，`Information Fusion` 114 (2025), 102712，DOI `10.1016/j.inffus.2024.102712` 已由[出版社入口](https://www.sciencedirect.com/science/article/pii/S1566253524004901)核对作者、篇名、期刊与文章编号。2026 CCF第七版目录未找到`Information Fusion`，正式引用可标“CCF目录未收录（按本次检索）”而非猜等级。**建议最终整合向#63补这条相邻综述正式文献，并解释其此前已有的任务/方法综合；如保留Ye预印本则书目由49→50，必须重新核键和正文。**

## 四、版本/合并与工程收口决策

1. **学术主线固定#63**：以后从该固定HEAD及现有main（已含#57全文、#58审稿、#60 R6-V图形、#65审核档案）开展最终整合。#64关闭为“被选版替代”，仍可回看Mao元数据和备选比较，但不得作为另一条科学主线再合并。
2. **先不把未整理的#61→#63叠加栈强行直接合并main**：主线main已包含R6-V对SVG和正文文末两行的修改；#61/#63源自旧R5-C分支。直接重基/自动合并可能使最新排版更改被覆盖，并且#63还有上面的确定性引用链接和表号缺陷。**Work最终整合应在main上创建唯一主稿分支，选择性移入#61 + #63最终学术内容，保留main图形，修复两处引用；做差异核对。**
3. **R6-Final Integration由Work完成，不交给Chat重复渲染**：保留F1–F5的R6-V已通过修订，全文49（或加Mao后50）个引用真实Bib解析/出版社元数据、T1–T7目标模板实际渲染、Markdown→PDF/Word真实排版、科研改稿及多文件链接同步。不能把“SVG曾渲染通过”当成最终尺寸PASS。
4. **最终审稿只复核变更集**：确认#63科学主张没有被重构/覆盖，两个已知引文瑕疵关闭，真实Bib和图表验收后，才允许标“SUBMISSION-READY CANDIDATE”。旧R6-Fix 16个已关项继续保护，不重启九章或大规模阅读。

**决定**：#63主线，#64非主线。八项整改在当前科学审稿范围内全部满足目标（两个确定引文问题由最终工程整合补丁收口）；R6-Final Integration GO；全文目前仍NOT SUBMISSION-READY。
