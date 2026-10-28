# P028｜ImpliHateVid：视频隐式仇恨数据与两阶段多模态对比学习（定稿；关键疑点保留）

> **状态**：2026-10-28 用户明确“定稿、上传、合并”。此“定稿”指阅读与证据审计已归档，**不表示两阶段机制已被独立证明、标注/划分已取得实物核验，或仓库已可复现**。仍开放数据下载、划分审计与代码运行。**不要将其作为无条件可靠的可复现基线。**

## 1. 书目信息、任务与贡献

- Mohammad Zia Ur Rehman, Anukriti Bhatnagar, Omkar Kabde, Shubhi Bansal, Nagendra Kumar. *ImpliHateVid: A Benchmark Dataset and Two-stage Contrastive Learning Framework for Implicit Hate Speech Detection in Videos*. **ACL 2025 Main Long Papers**, pp. 17209–17221, DOI: **10.18653/v1/2025.acl-long.842**。
- 正式页面 https://aclanthology.org/2025.acl-long.842/ ；正式 PDF https://aclanthology.org/2025.acl-long.842.pdf ；仓库 https://github.com/videohatespeech/Implicit_Video_Hate
- 两项贡献应分开：① 建立 **ImpliHateVid** 具隐式/显式/非仇恨三类标签的视频基准；② 提出两阶段监督对比学习和多模态/辅助特征分类器。此前已有视频仇恨检测（HateMM、MultiHateClip）与多模态融合架构（MulT 等）；**新数据集上基线由本文作者重新适配/训练测试，不是原模型在尚不存在数据集上的历史成绩**。
- 任务：ImpliHateVid 的 Hate/Non-hate 二分类（隐式与显式合并为 hate）及 Non-hate/Implicit/Explicit 三分类；HateMM 仅二分类。检测标签不是隐含命题恢复/细粒度语用机制解释。

## 2. 数据构建及 Ground Truth

- ImpliHateVid：**2,009** 个英语视频、约 86.5 小时，来源 BitChute/Odysee；1,000 Non-hate、509 Implicit Hate、500 Explicit Hate；论文 Table 1：平均转录词数约 175.404 / 85.166 / 80.326（Non/Implicit/Explicit），存在**文本长度潜在标签捷径**，尚未审计因果。
- 论文 §3/Appendix A：4 名标注员（1 硕士生、3 本科生），由教授与博士生监督；50 个专家标注示例作为训练和纠错基础；分批标注、争议讨论。标注指南区分隐含讽刺、幽默、代码语言与直接歧视；文本、视觉与语境的定位是定义的一部分。报告 Fleiss’ κ：二分类 **0.8387**、三分类 **0.8027**，是人员一致性证据，不等于标签完全正确。论文称还指出有害片段和目标群体，但**文件级别的可下载字段与标注粒度未实物核验**；无已核验的 sarcasm/metaphor/coded hate 等机制级 GT。
- **数据访问限制 [HIGH]**：官方 README 明确仅限学术非商用、不可再分发、机构邮箱+签署协议+申请审核后获取下载指引；公开仓库 **不直接提供 2,009 原始视频或完整固定分割数据**。未实际获得授权/下载包，不能声称可复现。对原始内容泄漏、近重复、同事件/频道重合、分割固定性和隐私合规需后续验证。
- 正式论文 §5.2：ImpliHateVid Train/Val/Test = 1,283/325/401，合计2,009；HateMM = 662/166/210，合计**1,038**，但 §5.1 称使用1,035/总1,083，存在**三样本报告差异 [HIGH]**，不能凭此直接断言测试集泄漏。
- 后续衍生 Ex-ImpliHateVid（https://github.com/DUT-lujunyu/IARE）公开说明提供 2,005 条衍生解释/偏好样本，不包含原始视频，且与作者原始 GT 不等价；不得认为这解决了访问问题。

## 3. 方法的实际输入、学习目标及推理

1. **原始视频→预处理**：WAV 音频、ASR 转录、均匀抽帧（文中 100 帧，不足填充），再由预训练 **ImageBind** 分别提取图像、文本、音频 1024D 特征；辅助数据包括 NRC emotion、VADER sentiment、图像 captions 与 BERT caption 表示。 ImageBind 基础编码器不应误称本文从零训练的大规模 VLM。
2. **Stage 1**：三类模态专用 MLP 将 1024D 输入映射至 256D，拼接 [图像,文本,音频] →投影头；以同类别/异类别视频作为监督对比正负集合，使融合表示更便于分类。未直接监督隐含命题。
3. **Stage 2**：按 `IT/TI, IA/AI, TA/AT` 六个**有向分支**分别从相应单一模态的 Stage1 输出经 MLP (256→128) 映射，再使用带标签的跨模态监督对比损失。如 IT 只接收图像表示、TI 只接收文本表示；**这里不是图像生成文本、不是 cross-attention、没有直接比较词与帧的语义对应**。同类别的不同视频仍可作跨模态正样本，不能将监督信号理解成独立的图文语义对齐真值。
4. **分类**：六分支嵌入 + Emotion/Sentiment + Caption 表示拼接，经 Dense/Dropout/Softmax 输出二或三分类；监督对比损失与分类训练流程需要源代码完整闭环核实。
5. **公开 notebook 特征**：主 `Codes/Multistage Contrastive Learning.ipynb`（24 个代码 cells）只有编码器、损失、分类器等定义，**没有 fit/evaluate/predict、训练循环、数据读取与加载 split 的完整入口**。映射网络是 Dense MLP；`SupervisedContrastiveLoss_self/cross` 正样本依据 `labels_i==labels_j`，将 **negative-only** 作为归一化分母，与标准 NT-Xent/SupCon 不同，可能对 batch 类别组成敏感。静态读码不等于运行错误已证实。辅助 notebook 存在本地绝对路径/缺未定义变量/固定 reshape，需要重构；未运行或确认 checkpoint。
6. 论文公式 §4.3 图2、Eq(1)–(10) 为主要方法依据；只支持模型架构与作者意图，具体训练需以可执行版本交叉核实。

## 4. 完整实验清单与读数：分清可支持什么

**论文 Table 2：二分类主要结果（F1）**
- ImpliHateVid：BERT 68.84%、Wav2Vec2 77.24%、DeepCNN 78.00%、CSID 81.54%、MCMF 82.20%、MulT **83.52%**；完整系统 **87.73%**，相对最强所列基线 +**4.21百分点**。
- HateMM：BERT 66.40%、CSID **71.40%**、MulT 52.12%、完整系统 **97.58%**（+26.18百分点）；幅度异常大值得核验原始划分/数据与模型适配，但不能仅据此认定作弊。
- 由于在 ImpliHateVid 二分类中把隐式与显式合并，这组结果**不证明单独对隐式仇恨有相同幅度优势**；GPT-4o/Llama 为零样本调用，与训练基线不是等条件。

**论文 Table 3：ImpliHateVid 三分类**
- 整体 Macro-F1：MulT **66.27%**、完整系统 **69.18%**，+**2.91百分点**；
- Implicit Hate 类别 F1：MulT **64.08%**、完整系统 **66.05%**，只高 **1.97百分点**。评价隐式任务时必须优先引用细分类指标，而不能以二分类+4.21代替。
- Table 3 另外报告每类 Accuracy/Precision/Recall/F1；三分类宏平均高并非隐含意义推理直接证据。

**论文 Table 4/Figure 3：模态消融**
- 三分类 Implicit F1：仅文本30.38、仅图像30.77、仅音频**45.83**；文本+音频37.50、音频+图像33.94、文本+图像27.16；完整系统**66.05**。同表 Macro-F1 59.51、55.87、59.77、61.31、61.68、44.48、69.18。说明**完整系统**优于所测消融，但**增加模态并不单调改善**，且完整模型还含 caption/emotion/sentiment，不能把全部增益归给“跨模态互补/理解”。
- 缺少固定单模态能力并打乱跨模态配对的配对反事实检验。

**论文 Table 5/Figure 4：辅助特征消融**
- 三分类 Macro-F1：删除 Emotion **68.09%**、删除 Caption **67.36%**、删除 Sentiment **67.70%**、完整系统 **69.18%**。说明所报告设置下有辅助特征收益，Caption 删除影响较大；不能归因给 Stage2。正文 §5.5.2 又称完整系统 Macro-F1 **66.29%** 与 Table5 **69.18%** 不一致；应保留作者笔误/表格或设置错配可能，不当作已证造假。

**论文 Appendix：数据标注一致性**（4 标注者，Fleiss κ 如上），以及 Figure5 Token Attribution 个例（词语重要性可视化，只是个例，不证明隐含语义忠实性）。

**最重要的缺失实验 [HIGH | 理论增益未经消融]**：没有在**相同模型容量与固定输入**下系统比较 `No-CL`、`Only Stage1`、`Only Stage2`、`Stage1+Stage2`。既有表格不能独立证明“第二阶段必要”，也不能排除额外参数/训练步骤/辅助特征贡献；与外部架构比较非因果消融。

## 5. 方法批评与最低成本复现前提

- 作者使用 supervised category-level cross-modal contrastive learning；**有分类性能提升证据，缺乏模型是否真的理解隐晦语义/跨模态冲突的直接证据**。需控制仅文字/画面/声音线索捷径、同频道/同事件重合、标签敏感性；3类标注不代表5类语用机制标准答案。
- 与 P003 MultiMM 的图区隐喻/文化语义标签、P032 ImpCon 的明示 implied statement 辅助监督对照，P028 的主要贡献更接近 **dataset+视频融合分类**，不是结构化隐含意义推理。
- **可行性 [HIGH]**：受限下载需要机构申请，不能假设即时可用；完整视频预处理、ImageBind Huge、多个模块和 notebook 重构对共享 GPU 有风险，不能保证单卡16–20GiB及<6h完整复现，尤其无预提取特征的情况下。
- **严格的最小验证路线**：先取得数据协议许可，确认是否含原始视频/Video_ID/类别/片段/目标/划分；检查重复与文本长度捷径；有冻结三模态特征后，使用相同划分与固定架构比较 NoCL / Stage1 / Stage2 / Both（优先于端到端重跑 ImageBind）。无法拿到许可时先暂停本篇 GPU 复现，而不是反复调网络。
- **定稿结论**：认可其视频隐式仇恨 Benchmark 建设意义和完整系统分类增益；**两阶段对比学习的独立必要性未证实**，**跨模态隐含意义推理未证实**，**原始数据实际可获得性与复现性未核实**。这三项开放问题必须保留。

## 6. 证据与下一步

- ACL PDF §3（收集/标注）；§4（网络/监督目标，Fig2）；§5（Table2–5，Fig3–5）；Appendix A（来源/类别/一致性）。
- GitHub README（数据申请许可）；`Codes/Multistage Contrastive Learning.ipynb`、`Codes/Extracting ImageBind Features.ipynb`、`Codes/Text Extraction from Audio.ipynb`、`Codes/Caption Generation.ipynb`（已静态检查，未运行）。
- 建议下一篇 **P019 Understanding Figurative Meaning through Explainable Visual Entailment（V-FLUTE）**，转到具有解释/蕴含标签的多模态修辞理解，以对照 P028 的仅类别监督；不要提前在新论文尚未精读时标记定稿。
