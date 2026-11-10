# R6-Fix-Review｜PR #61正式独立学术复审与修订关闭裁决

> **独立审核记录：2026-11-09；REVISION-REVIEW COMPLETE，SOURCE PATCH NOT MODIFIED**  
> **审核对象固定**：PR [#61](https://github.com/YuSun-WK/implicit-content-research/pull/61)，R6-Fix稿固定commit `c125c6358c655951d07286763f3b7a3eed6e9275`（九章正文、T2–T7、Bib 48条、R6_fix四份审计文件）；源稿PR #57固定`c04d6a23e864923acd64c192c8b05dc597c2bb90`。原R6-A4整改要求见[24项根因表](https://github.com/YuSun-WK/implicit-content-research/blob/survey/r6a-academic-review-20261109/03_survey/R6_review/R6A4_Deduplicated_Issue_Register.md)。  
> **职责**：只审学术质量、声明与证据；不直接修改R6-Fix、R5-C、R6-A的科学正文或合并PR；不替代R6-V的PDF/SVG实渲染、BibTeX编译和目标会议格式验收。若后续源稿变更，本裁决必须重新对新commit核验。  
> **学术证据类型**：F正式出处；P作者论文报告结果/GT（未独立复现）；S固定公开代码/发布数据静态观察；H跨论文综合；O尚未闭合。各题材为评价指南，不把R6-Fix内部自述当成果成立的证据。

## 一、最终Verdict（对固定版本）

**MAJOR REVISION REMAINS / 不批准标记SUBMISSION-READY。R6-Fix是实质性修订，但未关闭全部投稿阻断项。**

审稿对A4的**24个唯一整改单元**逐项复核，结果为：

| 等级 | 学术范围CLOSED | PARTIAL / 待进一步定向修改 | 仍阻断最终认可 |
|---|---:|---:|---|
| **P0（3）** | **1**（P0-03） | **2**（P0-01、P0-02） | **是** |
| **P1（17）** | **11** | **6** | 其中若干影响投稿可信度 |
| **P2（4）** | **4** | **0** | 否 |
| **总计24** | **16** | **8** | **须再修订后复审** |

**CLOSED只表示该整改单元在学术内容审核下满足原A4目标**，不代表外部CSV/代码O项全部获证，也不代表论文整体或R6-V工程通过。历史A0–A3审稿60条映射仍保持唯一归属，不额外创造新的P0计数。完整逐项判决见[24项Reviewer Matrix](R6FixReview_24_Issue_Matrix_20261109.md)。

## 二、三项P0逐项裁决

### P0-01｜PARTIAL：三条规律已经写出，但学术“增量”的证明仍弱

**正面**：[R6-Fix L25–46](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L25-L46)真实承认已有语用/反讽/多模态有害综述，[R6-Fix L418–425](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L418-L425)确实新增三条正面与反面证据，[R6-Fix L480–490](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L480-L490)把它们连接到可证伪、现有GT低成本诊断，而非简单重复旧稿“有待研究”。这比R5-C实质进步。

**尚未过关的原因**：
1. **已有综述差异仍主要是宽度，不是分析结果**：§1.2的四行相关综述各写“本文联结更多研究”，与此前Ma（ACL2025 Main，CCF-A）的数据/评测框架和Farabi（IJCAI2024 Survey Track；按2026第七版会议CCF-B）的多模态反讽比较尚未展示**相同研究单位下它们的结论不能回答而本文能回答什么**；缺可在正文引用的先行综述×本稿所得结论matrix。项目既有[R5-E先行综述证据](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/Related_Surveys_Comparison.md)尚列Mao等2025语用处理综述、Ye等LVLM安全综述、Kühn少见修辞格等竞争背景，本稿只引用其中有限行，无法据现状称差异已充分证明。
2. **“跨领域规律”中有两条其实多为单子域的协议提醒**：规律一比较四种编码研究的输入预算，真正跨到T2非字面语义/泛化协议的相同结构尚未被论证；规律三主要来自多模态安全数据与回应，各数字的Y/G/E不共享，结论更接近“分开评价”而不是可解释的条件转移规律。规律二跨度较好，但只说解释标注有信息优势、不能证明faithfulness，尚未通过`同监督预算的竞争替代解释`展示更一般的预测关系。
3. **数据引用多，辨识度强的“条件→适用结果→反例→能否迁移”表仍缺**：三条每个有纸面正反证据，但几个“正面”仅给先验存在和模糊“在原协议上有效”，不是跨论文经同维度重编码后的比较。因此这是一套值得发表的**审计视角雏形**，目前却不够强以证明原创综述贡献已实现。

**必须修**：第1章将R5-E的竞争对象归并为`prior survey范围 / 已提出的任务或评价单位 / 本稿新的跨域条件比较产物 / 正文页表证据`（至少包含Ma、Farabi、Hee、Mao/Ye之一）；第8章将三条写为简明但真正可被反驳的`条件C → 可观察预测Y/E → 多篇作者P级支持 → 反例与替代机制 → 不适用域`比较矩阵，其中至少两条跨**不同子学科**产生明确经验对照；不能用增加引用数量代替条件科学综合。保留H级表述，不假称本人已做meta-analysis或因果实验。

### P0-02｜PARTIAL：固定作者源代码可复核，但“外部审稿人可直接访问完整证据”尚不成立

**正面**：本轮对[固定索引](https://github.com/YuSun-WK/implicit-content-research/blob/survey/r6fix-full-draft-major-revision-20261109/03_survey/R6_fix/R6Fix_Public_Code_Evidence_Index.md)的几处高风险静态证据重新独立访问**作者公开仓库固定commit**：
- [RV-HATE ppo_eval.py@acfe053 L155–180](https://github.com/leeyejin1231/RV-HATE/blob/acfe053172a7266c8dde3759551882701478cdac/ppo_eval.py#L155-L180)与[L33–67](https://github.com/leeyejin1231/RV-HATE/blob/acfe053172a7266c8dde3759551882701478cdac/ppo_eval.py#L33-L67)确有`EnsembleEnv(test_data,...)`及标签宏F1 reward；这是**公开脚本入口**事实，不能无对应正式训练记录断言作者发表的模型权重真实这样训练。
- [CADET dataloader@1f1a25 L119–142](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/datasets/dataloader.py#L119-L142)和[L257–313](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/datasets/dataloader.py#L257-L313)返回`train,test,test`，结合[trainer L219–252](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/training/cadet_trainer.py#L219-L252)会对所传val调F1用于模型选择；正式训练run mapping仍O。
- [MultiMM data_utils@33a01f L67–100](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L67-L100)明确对train/val/test取CSV第六列构造`senti`；这证明公开检测路径的测试辅助输入，**不等于独立判定所有正式论文表格使用同一运行入口**。
- [Meerkat-VL ray_trainer@9ecb L489–616](https://github.com/Tunanzzz/Meerkat-VL/blob/9ecb79281492bd491ef65f72647bcef893cba4fa/verl/trainer/ppo/ray_trainer.py#L489-L616)确将模型生成的回答与`user_intent/safety_warning/harmful_intent`组合为文字自评提示，没有重新提供图像张量；只就当前函数判断。

**剩余高优先问题**：
1. **作者代码公开≠项目索引公开**：完整S证据索引位于**私有研究GitHub仓库**。正文只写相对链接`../R6_fix/R6Fix_Public_Code_Evidence_Index.md`（如[R6-Fix L248–248](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L248-L248)、[R6-Fix L314–326](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L314-L326)），外部同行审稿/出版成PDF时**未必能访问**该文件；“外部可复核”这个A4 P0门槛仍不满足。应把足够的固定作者源代码permalink直接放到稿件脚注/附录，或创建可授权的公开证据附录（不公开用户私有精读/其他项目文件）。
2. **稿件与表格口径没有同步**：正文[R6-Fix L314–314](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L314-L314)与[R6-Fix L430–430](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L430-L430)已明确MultiMM公开检测路径有固定commit，当前[表5](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/tables/T5_Multimodal_Meaning.md)仍称“该实现断言仍需公开固定版本”。对于MCIB，正文[R6-Fix L326–326](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L326-L326)固定公开源码后，表5/表7还泛称“公开实现风险待固定版本”；应区分**已固定静态路径**与**实际训练batch或正式作者版本未证**。
3. **高风险发布数据数字缺同级固定来源**：[R6-Fix L358–358](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L358-L358)给出MMSafeAware 1523 prompt、1453图、445种blob、70缺图的**精确S级**结论，原证据卡是某发布状态，但本轮公开索引未列该**发布仓库commit/路径/计数脚本**；Silent Signals 16550/16258 README差和MOSSBench 244 contrasts也是S/O，需逐项加不可变来源，或删去过细计数、改写成版本不一致待核。
4. **稿件性质**：若投稿于普通学术综述，而非“软件考据论文”，应评估把争议性实现审计移到公开、可复核、短小附录，正文突出P级已发表实证与信息预算定义。不得仅因GitHub可读就宣告作者学术失范。

**关闭标准**：所有保留的高风险S级正文数字要么附公开可进入的固定来源，要么保守删降；正文/T5/T7同口径；索引外部访问路径须不依赖当前私有研究仓库；绝不声称作者正式训练代码就是该版本。

### P0-03｜CLOSED（学术内容范围）；独立书目工程仍待R6-V

**确已修好**：ExPO-HM是[ICLR 2026 Conference（CCF-A）正式论文](https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html)，Mei等七位作者已核；`references.bib`增加`mei2026expohm`，[R6-Fix L374–374](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L374-L374)明确其为Hateful Meme“解释后检测”，与SMARTER、ThinkingGuard和Meerkat区分目标/奖励及输入GT；[R6-Fix L414–424](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L414-L424)在第8章和[表7](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/tables/T7_Method_Families.md)把政策SFT、课程GRPO、CDE、作者原协议宏F1与RA-HMD直接基线的边界一起呈现。数据目的不是严格S-S-U被明确说明。这达到了A4 P0-03的**学术覆盖与归因**门槛。

**限制**：这不认证48条Bib已由BibTeX解析器及出版社逐项校对；不把CDE低熵宣称faithfulness，也不将`74.5→81.1`称独立CDE消融收益。原P027精读卡显示完整配置中SFT、课程、CDE一起变化，正式论文评估有多数据集；该研究尚存在公开脚本与作者训练配置的版本O。R6-V将正式书目工程单独验收，不重新打开本P0的学术遗漏问题。

## 三、新发现/未闭合的非重复问题（并入原24项，不新增虚假P0）

| Review ID（依附A4单元） | 严重性 | 原稿锚点与实证基础 | 必要动作 |
|---|---|---|---|
| RR-01 → **P1-12** | P1 | [R6-Fix L362–362](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/Survey_Full_Draft.md#L362-L362)和表6称Figure5约33.8%条件占比正确，但原[P038 VLSU精读卡](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md)§6将**Figure5具体饼图归于Qwen2.5-VL-32B**，正式PDF§5和E.3将示例与其他模型的扩展结果分开。 | 在正文及T6显式标“原论文Figure5示例/该模型（以原图标题核）”，注明不同模型图18另有占比；不要读成全部17模型统一的33.8%。 |
| RR-02 → **P1-08 / P0-02** | P1 | [表5](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/tables/T5_Multimodal_Meaning.md) vs 已固定[MultiMM commit](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L67-L100) | 表5写“公开路径已固定、正式论文run对应仍O”，而不是“commit尚未固定”；MCIB同理。 |
| RR-03 → **P0-01 / P1-01** | P1 | §1.2仅四行相邻综述，虽项目[R5-E](https://github.com/YuSun-WK/implicit-content-research/blob/main/03_survey/R5_evidence/Related_Surveys_Comparison.md)已发现Mao语用处理、Ye LVLM safety与多种隐喻综述；新三规律在§8.1.1更多是可靠评价提醒。 | 扩成“相邻综述—已有分析单位—本稿新增可复核比较结论”的实质矩阵，结合P级实验展示超出单子域综述的解释性对照。 |
| RR-04 → **P1-05/P1-12/P0-02** | P1 | Silent README与MMSafeAware发布文件精确数、MOSSBench特定公开contrast未在六份固定代码索引建立数据blob/版本链；现只有历史阅读卡。 | 资料属可核项目私有归档但发表性“我们发现”仍需公开数据commit/原始文件路径、计数命令或改成“此前所查版本提示差异，待核”。 |
| RR-05 → **P1-01/P1-16** | P2 | [表7](https://github.com/YuSun-WK/implicit-content-research/blob/c125c6358c655951d07286763f3b7a3eed6e9275/03_survey/R5_full_draft/tables/T7_Method_Families.md)合并FETCH!/FA-Net和ImpCon/SMARTER等本来不同的Y，正面“各自有收益”有时没有具体量化同论文对照；§1.4声明叙述性选择合理，但48条如何支撑每个条件规律没有映射。 | 每条规律最少2个**分开列行**的代表实验，给可审原论文结果、单位和干预缺口；非真实跨域数据不做对抗性比较。 |

## 四、明确经本次独立核证且**不是错误**的点

- **2026年CCF第七版等级**：IJCAI已由A降到**B**，ICLR成为**A**。因此Farabi（IJCAI 2024 Survey Track）的`会议CCF-B（按2026现行目录）`是有效的**当前评级**，不能仅依据旧版2017/2022 A类目录误判。该轨仍是Survey Track，不应说成与Main Regular的CCF-B论文资格完全等价。出处：[CCF2026正式目录声明](https://www.ccf.org.cn/Academic_Evaluation/By_category/)、[第七版整理](https://github.com/haozhou-wong/ccf-recommended-list-2026-markdown/blob/main/ccf-2026-quick.md)。
- CrossGuard（ACL 2026 Main，CCF-A）正式附录Figure6/7写1,390红队样本和1,616平衡Guard训练样本，Figure7占12.5%，稿中`≈202`正确作为**四舍五入换算、非作者逐例真数**；Figure4 SIUO 60.33→5.39，FigStep 0.12→0.21，已给正反反例。出处：[正式论文PDF](https://aclanthology.org/2026.acl-long.1178.pdf)Appendix A、§5.5。
- VLSU（ICLR 2026，CCF-A）正式PDF首页写8187/17模型/34%与62.4→10.4/90.8→53.9；公开CSV之前项目卡报告8159与严格S-S-U35、图片标签not_sure141，当前稿不偷换测试输入分类F1与安全回复拒答率。出处：[ICLR正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)及[项目P038](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P038_VLSU.md)。
- DOSE（ACL 2026 Main，CCF-A）在表5已纠正为**新闻图像＋文章文本**而非文/音/视（后者MCIB）；[ACL正式出处](https://aclanthology.org/2026.acl-long.319/)。
- 引用机械核对：**九章主体48个唯一citekey、Bib48项、手写参考48项**均一一对应；全部5张SVG和7张表的本地Markdown链接在GitHub当前分支可解析。**未执行真实BibTeX解析器、SVG可视化或PDF构建**，这不自动构成R6-V PASS。

## 五、正式复审处理决定

1. **允许进入一次定向R6-Fix-R1（不重新启动R0–R5），禁止直接合并或投稿。** 优先修两项未闭合P0及其依赖P1，不需要为了小问题追加数十篇全新精读。
2. **学术P0-03视作CLOSED**，仅在新的稿件出现ExPO事实/GT退化、或R6-V发现正式引文问题时重新打开；严禁为了“审稿全部P0相同”而把已补论文再算未完成。
3. **P0-01、P0-02维持PARTIAL且为投稿阻断。** 修订时给`unique ID → 新稿immutable commit+line → 原论文/公开实现证据 → 关闭/剩余O`，才允许重审后关闭。新增缺陷并入既有主根因，不要把24项变成无止境的虚增问题。
4. **保留PR #61为Draft/Open，学术评审文件独立保存在`03_survey/R6_fix_review/`分支，不触碰`03_survey/R5_full_draft/`中的原稿、表格、SVG与Bib**。R6-V的PR #59/#60属于另一支线，不能把它们的视觉产物直接作为本次学术P0的验收证据。

**Reviewer签署结论：R6-Fix可进入定向再修订；以P0-01和P0-02为阻断项；P0-03学术范围CLOSED；16/24本轮学术整改通过，8/24部分通过；全文仍NOT SUBMISSION-READY。**
