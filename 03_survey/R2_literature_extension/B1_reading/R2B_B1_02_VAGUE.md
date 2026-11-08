# R2-B｜B1-02 VAGUE 正式精读卡（定稿）

更新时间：2026-11-08｜状态：**定稿（核验问题保留）**｜临时编号：**R2A-002**；不占用原始P/T编号。

## 0. 发表与开放资源
- **VAGUE: Visual Contexts Clarify Ambiguous Expressions**
- Heejeong Nam, Jinwoo Ahn, Keummin Ka, Jiwan Chung, Youngjae Yu
- **ICCV 2025 Main，CCF-A**，pp.1537–1547。
- 正式论文：https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html
- 正式PDF：https://openaccess.thecvf.com/content/ICCV2025/papers/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.pdf
- 作者仓库：https://github.com/Hazel-Heejeong-Nam/VAGUE
- 数据：https://huggingface.co/datasets/HazelNam/vague-bench
- **VAGUE 1.0（3993条）已弃用；正式审计以 VAGUE 2.0（1677条）为准**。作者 README 明确记载版本差异。

## 1. 问题与任务边界
研究多模态意图消歧（Multimodal Intention Disambiguation, MID）：图像场景提供说话者间接表达所依赖的实体、事件与行为，模型需据此推断说话者希望听者完成的行动。与普通VQA、图文匹配、图文有害检测不同。
- R1：主任务**T3语用意图推断**；次任务**T2隐含意义理解**。不是T5联合隐含风险识别。
- 输入：图像 $I$、间接话语 $p_i$、四个候选行动/解释 $C$；输出：当前图文语境支持的正确行动解释。作者任务表述 $T(I,p_i)=\arg\max_{c\in C}P(c\mid I,p_i)$ 是推理目标，不是新训练损失。
- 例：残疾人专用停车位中的轿车，隐晦话语暗示对方将车辆移走。与直接命令“move the sedan”不同（作者仓库README给出完整公开JSON样例）。
- 来源：正文§1、§3.1及Fig.1–2。

## 2. 数据与标签协议
- 样本来自VCR（1144）与Ego4D（533），共**1677**。每条包括image、direct（直接表达）、indirect（间接表达）、solution（行动三元组）、mcq（4选1候选）、meta（caption、对象/图像信息、质量rating等）。
- 先取视觉场景、物体/人物线索，再以GPT-4o构建可执行的**直接请求**及行动三元组$(subject,action,object)$；人工对直接性、合理性评分，筛选可行实例。
- 根据同一目标行动生成间接话语，设计讽刺/幽默/习语等表达形态；人工复核间接表达的自然度与可推断性。保持**目标意图一致**但降低字面直接性。
- 选项包含一个预设正确解释与三类有针对性的干扰项：**SU（surface understanding，停留在字面）；NE（nonexistent entity，视觉实体错配）；FS（fake scene，在假场景中可成立的解释）**。此设计允许对错误行为做粗诊断，而非读取内部推理。
- 本文GT为**生成式目标行动+人工合理性审核**；不能直接视为图像中真实说话者已确认的心理意图。论文的人工94%分数来自400条子集、特定评价者协议；不等同多人对全体数据的共识。
- 证据：正文§4.1–4.2、Fig.3，补充材料§B、§E；公开仓库README和HF数据字段。

## 3. 方法和计算流程
- **没有提出新VLM训练网络或新优化目标**。评测三种设置：LM（只给间接文本）、SM（语言模型+图像caption）、VLM（直接图像+文本），比较图文信息对四选一Accuracy的帮助；另外考察CoT提示。
- 不能将SM和VLM差距视作严格的因果视觉依赖证明，因caption和原图的表示、信息与处理过程不同。
- 证据：正文§5.1–5.4，Table 1–3，Fig.4，补充材料§G。

## 4. 实验与证据
- Table 1：Qwen2.5-VL-72B在VCR上LM/SM/VLM分别**29.6/55.6/74.2%**，在Ego4D上**26.8/59.3/69.8%**；GPT-4o在VCR上**46.4/69.5/65.1%**，说明原图不总优于caption文本化通道。
- Table 2：400条评测子集上，Qwen2.5-VL-72B **72.3%**、InternVL-2.5-MPO-26B **63.0%**、GPT-4o **62.3%**、Gemini-1.5-Pro **60.3%**、人类评价者**94.0%**；这一子集与完整1677条结果**不可混用**。
- Fig.4错误类型分布：不少错误落在SU，但这只是干扰项导出的行为诊断，不构成模型内部只按字面推断的因果证据。
- Table 3/补充Table G4：CoT提升并不稳定，例如Qwen2.5-VL-72B原图设置报告从72.8%下降至69.9%，不能宣传“加推理一定提高语用理解”。

## 5. 创新、局限与审稿意见
- 主要贡献是**明确MID任务、提供人工筛选数据、设计有语义针对性的负例和失误归因分析**；不是全新架构。
- 需要限缩的论断：基于真实图像构建的行动意图不等于真实人类交流中的意图；LM/VLM分数差不能为每条样本提供严格的图像必要性；FS/SU/NE只能诊断模型选择，不证明其内部推理路径。
- 数据多为英语场景与构造的单轮话语，文化迁移、开放式解释、多意图、图像反事实控制仍有不足。
- **公开仓库可访问**，含benchmark、models、src等目录，并有VAGUE 2.0 HF/Google Drive下载入口；未实跑，不能据此声称完整可重复复现。

## 6. 与P011/P020和DRInQ的位置
- P011是语用研究综述；P020是(RSA)²概率语用解释机制；DRInQ固定句子改变**文本语境**；VAGUE使图像语境参与**间接行动意图消歧**。
- 建议作为综述T3多模态语用推断的核心案例，支撑“视觉感知≠隐含意图理解”“语境的重要性与GT可观察性”“有针对性的干扰负例”三条讨论。不得仅因图文输入就归入T5有害风险检测。

## 7. 未关闭核验事项
- [ ] 核对HF发布快照、图像权限与原始样本间的重复/数据泄漏。
- [ ] 对照正式PDF与公开代码逐行检验选项生成和评价脚本；**未进行运行级复现**。
- [ ] 审核数据中包含direct、solution、caption的字段在模型prompt构造时是否可能泄露GT。
- [ ] 若将视觉依赖写成严格因果结论，须加入同间接句的图像置换反事实。
- [ ] 人评仅特定400条评测子集；不可概括成全体样本上的多人共识。

参考：官方正式论文与Supplementary；作者README https://github.com/Hazel-Heejeong-Nam/VAGUE/blob/main/README.md 。
