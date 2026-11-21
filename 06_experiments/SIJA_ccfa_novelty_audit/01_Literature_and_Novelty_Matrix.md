# 文献检索、直接竞争与创新性矩阵

检索截止：2026-11-17（北京时间）。项目资料以 GitHub 固定提交为准；论文事实另查出版方、作者预印本、官方项目和代码，未用旧聊天替代一手来源。证据 ID 与核查深度见 [08](08_Evidence_Register.md)。

## 检索方法与边界

采用四组检索：①图像编辑攻击/前置 Guard/生成期干预；②感知、意图、后果与安全决定分离；③grounding、反事实、策略、内部干预和风险校准；④编辑方向、风险归因、目标验证和语境依赖。逐项搜索用户列出的题目和简称，再追踪直接竞争文献的参考文献、官方代码和最新相关工作。

代表性查询包括完整论文标题，以及 `image editing safety guard outcome verification counterfactual safety 2026`、`image editing risk attribution`、`image editing state transition safety`、`multimodal safety preconditions postconditions`、`visual grounding safety`、`From Local Evidence to Safety Verdicts`、`selective prediction risk controlling prediction sets`。这是一轮有明确竞争对象的系统检索，**不是 PRISMA 式穷尽综述，也不能证明世界上不存在同类方法**。

直接竞品读取正式/作者PDF的方法、关键公式、主表和消融；SIJA、IGSR、Meerkat、SafeGuard的部分框架/格式还检查了页面图像。共下载提取16篇不同研究的17份PDF（SIJA含v1/v2），另核对CCF目录；来源、SHA256和阅读范围存于 `09_Source_Manifest.json`。其它论文的核查深度单列，不假称均精读全文。全文缓存不提交。

等级统一采用 **CCF 2026 第七版的会议等级口径**。ICLR 在这一版为 A；这不表示其早年发表时已经列 A，也不表示 workshop/Findings 自动继承主会等级。正式状态和具体版本分别标注。[E27]

## 文献总矩阵

“未覆盖”仅表示本轮核对范围内的方法边界，不能被解读为该方法已经在该场景失败。表内方法均为作者提出；本轮没有复现其性能。

| 类别 | 简称/ID | 完整标题 | 年份 | 发表状态/会议 | CCF | 正式来源/PDF | 核心问题与机制 | 与 TGSV 重合 | 尚未覆盖的本研究需求 | 公开代码/本轮状态 |
|---|---|---|---:|---|---|---|---|---|---|---|
| 编辑直接竞品 | SIJA E01 | When the Editing Intent Is Split: A Cross-Modal Jailbreak Attack for Large Image Editing Models | 2026 | arXiv v2（11-16）；ICLR 2027 under review | 不适用，未录用 | [论文](https://arxiv.org/abs/2610.23909) / [PDF](https://arxiv.org/pdf/2610.23909v2) | 跨组件分散编辑意图；r/a/s 重建、后果推断后门控 | M2 原则与 M3 基础安全判断已在其中 | 未见独立后果监督、r/a/s正确条件错误分解及源状态×操作四格；正常效用v2已报告 | [SIJA](https://github.com/yexianmin/SIJA)，固定树仅 README |
| 编辑直接竞品 | VJA E02 | When the Prompt Becomes Visual: Vision-Centric Jailbreak Attacks for Large Image Editing Models | 2026 | ICML 正式主会 | A | [PMLR](https://proceedings.mlr.press/v306/hou26h.html) / [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/hou26h/hou26h.pdf) | 视觉承载编辑指令；编辑器 VLM 自省，可复用 KV cache | 意图恢复、结果安全预判早已存在 | 本轮不能由其结果推出 split-intent 条件机制 | [VJA](https://github.com/CSU-JPG/VJA)，读了前置门控核心文件 |
| 感知—决策直接竞品 | IGSR E03 | Mitigating Safety Context Amnesia in Multimodal Reasoning Models via Intent-Guided Safety Reasoning | 2026 | ACL Main Long 正式 | A | [Anthology](https://aclanthology.org/2026.acl-long.1821/) / [PDF](https://aclanthology.org/2026.acl-long.1821.pdf) | 风险线索已被感知却被语境合理化；LoRA 双路意图提取+仲裁 | M1/M3 和一般性后感知动机高度重合 | 非面向编辑目标图监督的操作效果学习 | [论文所列链接](https://github.com/kulasuoit/IGSR) 本轮 404；不声称完整开源 |
| 感知—回答直接竞品 | Meerkat-VL E04 | Meerkat-VL: Implicit Risk Safety Alignment in Multimodal LLMs via Perceptual Reasoning and Self-Verification | 2026 | ICML 正式主会 | A | [PMLR](https://proceedings.mlr.press/v306/zhou26ae.html) / [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/zhou26ae/zhou26ae.pdf) | 四轴感知/答案评分；NPSV 自验证与 DPCA 一致性奖励，GRPO | 感知与安全结果分离、自验证、效用约束 | 未直接学习源图到编辑目标的有向风险变化 | [代码](https://github.com/Tunanzzz/Meerkat-VL)，训练/评测框架公开，未运行 |
| 图像 Guard 直接竞品 | SafeGuard-VL E05 | Towards Policy-Adaptive Image Guardrail: Benchmark and Method | 2026 | CVPR 正式主会 | A | [正式 PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Piao_Towards_Policy-Adaptive_Image_Guardrail_Benchmark_and_Method_CVPR_2026_paper.pdf) | self-recaption 语义 SFT+策略条件 GRPO；SafeEditBench 局部安全图像对 | 策略 grounding、局部反事实、感知—规则分离 | 分类对象为已有图像；不是任意待执行编辑后果预测 | [代码](https://github.com/adorableChowhound/SafeGuard-VL)，读奖励和评测脚本 |
| 隐含风险直接竞品 | ThinkingGuard E06 | ThinkingGuard: Decoding Implicit Hazards via Step-by-Step Risk Attribution in Multimodal Large Language Models | 2026 | ACM MM 正式论文；核 PDF DOI/会期与官方节目 | A | [DOI](https://doi.org/10.1145/3767308.3835707) / [作者 PDF](https://arxiv.org/pdf/2609.36562) | 关键实体/触发实体；SA-MCTS 过程奖励搜索、全轨迹与关键步偏好 | 实体、关系、后果、风险归因均非新原则 | 特定图像编辑源目标效果算子不在已核机制中 | [代码](https://github.com/FroggyChen/ThinkingGuard)，树仅推理代码与材料，不等于完整训练发布 |
| 联合理解评测 | VLSU E07 | VLSU: Mapping the Limits of Joint Multimodal Understanding for AI Safety | 2026 | ICLR 正式主会 | A（2026口径） | [正式记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html) / [PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf) | 图/文/联合安全与 borderline；检查结构 CoT 和安全—效用 | 联合理解与判断的落差已明确 | 非新的编辑 Guard 训练算法 | [代码/数据](https://github.com/apple/ml-vlsu)，本轮主要核正式 PDF |
| 表示校准 | ShiftDC E08 | Understanding and Rectifying Safety Perception Distortion in VLMs | 2025 | NeurIPS 正式主会 | A | [正式 PDF](https://papers.nips.cc/paper_files/paper/2025/file/a627b9468c319c13a70b7c2fb8df65a3-Paper-Conference.pdf) | caption 文本对应与视觉激活偏移分解，移除安全相关分量 | 风险表征校准、理解与判决的桥接 | 不提供编辑操作后的真实目标监督 | [代码](https://github.com/Renovamen/ShiftDC)，本轮以正式方法 PDF 为依据 |
| 视觉机制 | AGLA E09 | Mitigating Object Hallucinations in Large Vision-Language Models with Assembly of Global and Local Attention | 2025 | CVPR 正式主会 | A | [正式 PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/An_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_with_Assembly_of_CVPR_2025_paper.pdf) | IPM/GradCAM 形成局部增强图，全局+局部 logits 融合 | M1 的局部证据 grounding 原则 | 幻觉缓解不等于安全政策执行；不提供三元组安全金标 | [作者代码](https://github.com/Lackel/AGLA)，未本地运行 |
| 视觉机制 | VCD E10 | Mitigating Object Hallucinations in Large Vision-Language Models through Visual Contrastive Decoding | 2024 | CVPR 正式主会 | A | [正式页面](https://openaccess.thecvf.com/content/CVPR2024/html/Leng_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_through_Visual_Contrastive_CVPR_2024_paper.html) / [PDF](https://openaccess.thecvf.com/content/CVPR2024/papers/Leng_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_through_Visual_Contrastive_CVPR_2024_paper.pdf) | 原图与扰动图 logits 对照，限制候选 token | 视觉对照并非新机制 | 扰动并非语义保持的安全反事实 | [VCD](https://github.com/DAMO-NLP-SG/VCD)，未运行 |
| 基础内部干预 | ITI E11 | Inference-Time Intervention: Eliciting Truthful Answers from a Language Model | 2023 | NeurIPS 正式主会 | A | [正式记录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/81b8390039b7302c909cb769f8b6cd93-Abstract-Conference.html) / [PDF](https://proceedings.neurips.cc/paper_files/paper/2023/file/81b8390039b7302c909cb769f8b6cd93-Paper-Conference.pdf) | 少量数据找 attention-head 方向并干预 | 低成本 activation steering 已存在 | 原任务是真实性，非编辑安全 | [作者代码](https://github.com/likenneth/honest_llama)，未运行 |
| 验证机制 | Task Shield E12 | The Task Shield: Enforcing Task Alignment to Defend Against Indirect Prompt Injection in LLM Agents | 2025 | ACL Main Long 正式 | A | [Anthology](https://aclanthology.org/2025.acl-long.1435/) / [PDF](https://aclanthology.org/2025.acl-long.1435.pdf) | 抽取指令，以 ContributesTo 验证指令/工具动作服务用户任务 | 行动前仲裁与验证思路 | 用户本身恶意时，任务对齐不足以判安全 | 本轮未找到可独立确认的完整作者代码入口，不推测链接 |
| 生成期直接竞品 | UVR E13 | Unified Safe In-context Image Generation in Multimodal Diffusion Transformers via Restricting Unsafe Information Flows | 2026 | ICML 正式主会 | A | [PMLR](https://proceedings.mlr.press/v306/yang26an.html) / [PDF](https://raw.githubusercontent.com/mlresearch/v306/main/assets/yang26an/yang26an.pdf) | DiT 输出 patch 安全锚定位、attention 信息流调节 | 安全关键区域与生成后果不是空白 | 不同于生成前自然语言 Guard；需要编辑器内部状态 | [UVR](https://github.com/deng12yx/UVR)，未运行 |
| 局部反事实竞品 | SafetyPairs E14 | SafetyPairs: Isolating Safety Critical Image Features with Counterfactual Image Generation | 2025/2026 | 2025 arXiv；2026 ICLR Trustworthy AI Workshop | **非主会，不计A** | [作者发表说明](https://machinelearning.apple.com/research/safetypairs) / [PDF](https://arxiv.org/pdf/2510.21120v1) | 局部安全编辑；静态/变化原子 VQA 约束+人工审核；对比训练 | 反事实、局部编辑验证已提出 | 没有等同于待执行编辑 Guard 的有向算子 | [迁移后代码](https://github.com/apple-aiml-research/ml-safetypairs)，读 loader/配置/流水线；完整成品包未取得 |
| 策略边界直接竞品 | PolicyShiftGuard E15 | PolicyShiftGuard: Benchmarking and Improving Policy-Adaptive Image Guardrails | 2026 | arXiv，未核实正式录用 | 不适用 | [论文](https://arxiv.org/abs/2607.05910) / [PDF](https://arxiv.org/pdf/2607.05910) | 随机化策略 SFT；同图不同策略的 pass/block margin | 属性—策略分离、成对决策训练不能当空白 | 变化轴是策略，非编辑操作与源目标状态 | [代码](https://github.com/ssmisya/PolicyShiftGuard)，树与训练入口已核 |
| 因果机制直接竞争 | SSU E16 | From Local Evidence to Safety Verdicts: Causal Tracing in Vision-Language Models | 2026 | arXiv v1，未核正式录用 | 不适用 | [论文](https://arxiv.org/abs/2610.07514) / [PDF](https://arxiv.org/pdf/2610.07514v1) | 文本/图像最小对照、局部与末 token activation patching、读出 | 证据到判决的干预链路已有 | 主要是诊断，不是前置编辑效果预测算法 | [作者链接](https://github.com/faezehdehghant/SSU-Bench)，网页可见而 API 404，访问状态不一致 |
| 输出通道安全 | Grounding Safety E17 | Visual Grounding Safety in Vision-Language Models | 2026 | arXiv，未核正式录用 | 不适用 | [论文/全文入口](https://arxiv.org/abs/2610.05637) / [PDF](https://arxiv.org/pdf/2610.05637) | 同请求 VQA/坐标输出对比；grounding 拒绝与能力数据微调 | 正确区域定位不保证安全；输出通道断裂已研究 | 不是图像编辑请求的效果预测 | 本轮核官方摘要；未审全部训练代码，不能声称已复现 |
| 图像持有者防护 | DiffusionGuard E18 | DiffusionGuard: A Robust Defense Against Malicious Diffusion-based Image Editing | 2025 | ICLR 正式主会；PDF 内题名含 Inpainting | A（2026口径） | [正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/43b77cef2a83a25aa27d3271d209e4fd-Abstract-Conference.html) / [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/43b77cef2a83a25aa27d3271d209e4fd-Paper-Conference.pdf) | 源图保护扰动，early diffusion 目标与 mask 增强 | 同属编辑安全，但威胁模型不同 | 不应强作 Guard 分类 baseline | [代码](https://github.com/choi403/DiffusionGuard)，官方入口核实，未重跑 |
| 不确定性基础 | CRC E19 | Conformal Risk Control | 2024 | ICLR 正式主会 | A（2026口径） | [正式记录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html) / [PDF](https://proceedings.iclr.cc/paper_files/paper/2024/file/f3549ef9b5ff520a7e41ff3cc306ab2b-Paper-Conference.pdf) | 单调有界损失的期望风险校准 | “加风险校准”不是新的安全算法 | 交换性/损失条件不能在自适应攻击中直接假设 | 论文方法入口；本轮未验证代码 |
| 不确定性基础 | LTT E20 | Learn then Test: Calibrating Predictive Algorithms to Achieve Risk Control | 2025 | Annals of Applied Statistics 19(2) 正式期刊 | CCF目录不适用 | [DOI](https://doi.org/10.1214/24-AOAS1998) / [出版方卷册PDF](https://www.imstat.org/publications/aoas/aoas_19_2/aoas_19_2.pdf) | 用多重假设检验选风险受控参数 | 阈值/选择风险控制是已有技术 | 不自动保证条件安全或 OOD/攻击安全 | 理论来源，不作为直接 Guard 模型 |
| 普通编辑资料 | MagicBrush E21 | MagicBrush: A Manually Annotated Dataset for Instruction-Guided Image Editing | 2023 | NeurIPS Datasets & Benchmarks Track 正式；非方法主轨 | 会议A，轨道单列 | [正式记录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/64008fa30cba9b4d1ab1bd3bd3d57d61-Abstract.html) | 人工源图/指令/目标图；正常编辑效用资料 | 非安全方法查重 | 普通编辑标签不等于安全金标 | [官方项目](https://osu-nlp-group.github.io/MagicBrush/)，本轮未取图像包 |
| 情境安全 | MSSBench E22 | Multimodal Situational Safety | 2025 | ICLR 正式主会；较早 arXiv 为2024 | A（2026口径） | [正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html) / [PDF](https://proceedings.iclr.cc/paper_files/paper/2025/file/1cb57fcf7ff3f6d37eebae5becc9ea6d-Paper-Conference.pdf) | 同请求不同安全情境；视觉、显式安全、情境推理诊断 | 语境—行动—安全分离非编辑独有 | 无编辑目标图；正式/旧网页样本数不同 | [代码](https://github.com/UCSB-AI/MSSBench)，本轮核正式元数据 |
| 联合安全评测 | SIUO E23 | Safe Inputs but Unsafe Output: Benchmarking Cross-modality Safety Alignment of Large Vision-Language Models | 2025 | **Findings of NAACL** 正式 | 不继承NAACL/ACL等级 | [Anthology](https://aclanthology.org/2025.findings-naacl.198/) / [PDF](https://aclanthology.org/2025.findings-naacl.198.pdf) | 单独安全、组合有风险；联合理解与风险判断 | 联合输入风险不是新问题 | 不是待编辑源目标学习资料 | [官方项目](https://sinwang20.github.io/SIUO/)，本轮核元数据，非重新全文精读 |
| 最新有效性审计 | Label Audit E24 | What Does a Safety Label Measure? Auditing Situational-Safety Benchmarks for Multimodal LLMs | 2026 | arXiv v1；未核正式录用 | 不适用 | [论文](https://arxiv.org/abs/2611.01125) / [全文](https://arxiv.org/html/2611.01125v1) | 场景/请求/文件来源混杂，风险排序与阈值分类分开 | 一个条件错误率不能直接指认推理失败 | 本轮未复现其基准审计；不能把其报告当SIJA缺陷证据 | 只核相关方法/表3/附录D，代码运行状态未验证 |
| 普通编辑补充 | AnyEdit E25 | AnyEdit: Mastering Unified High-Quality Image Editing for Any Idea | 2025 | CVPR 正式主会 | A | [正式 PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/Yu_AnyEdit_Mastering_Unified_High-Quality_Image_Editing_for_Any_Idea_CVPR_2025_paper.pdf) | 大规模统一编辑资料/模型 | 非安全机制新颖性证据 | 下载和安全标签仍需审核，不视为现成危险编辑金标 | 作为后备来源，不作为本轮已可用数据 |

## 直接竞争论文逐项分析

### 1. SIJA：最直接的原则重叠

核对 §3.1–3.2、§5.4、C.4–C.5、Fig.3–4、Table1；PDF pp.4–5/9/26–27。其可执行防御实例是提示驱动的 r/a/s 输出、推断结果再判断，另有 OCR 文本空间基线。没有在这些章节找到独立后果学习器、后果金标监督或独立正确性证书。**“未找到”只限定其实现边界，不表示这些环节已失败。**

作者Fig.4及v2 Table12的93.1%是危险请求拒绝率；Table1的Safe编辑配置是另一系统设置，不能用差值推出后重建错误率。**v2已新增正常效用：** Table14在100条同来源/指代/cue格式的正常替代操作上，原分解防御正常放行11%、危险拒绝93.1%；relaxed版正常放行60%、危险拒绝66.8%。这是作者报告的生成前指标，不能当实际正常编辑成功率。

v2 Table13还提供generic重建：危险拒绝86.3%（分解93.1%），输出117.47/123.77tokens、延迟4.02/4.37秒。Table12具名GLM-OCR、Qwen3-VL-2B-Instruct与Qwen3Guard-4B；introspection列additional models为None。因此“作者完全未测效用/成本/重建格式”及“所有Guard身份都未知”均已过时。外部Guard可识别，不代表完整introspection实现、生成设置和逐例日志已经公开；Gemma-4-31B-it仍是输出Judge，不能代填Guard。[详见版本差异](10_SIJA_v2_and_FA2_Delta_Audit.md)

未见被新增实验解决的部分是：独立审核重建正确率、独立后果命题准确率、条件/联合错误分解，以及控制源状态×操作的方向机制。v2的100条正常控制已经缩小剩余空间；若后续只重复其over-refusal或放宽授权提示，应终止方法新颖性主张。

对我们的实质限制：M2 若只是生成一段编辑后描述，没有新增原则；M3 的门控亦非新。可比较的新对象只能是明确可学、可观察、可独立核验的编辑效果，而非“再想一步”。

### 2. VJA：不仅是攻击和数据

核对 §2.2/Fig.3 与 Appendix A.4/Table5。它利用编辑器已有 VLM 的文本安全能力审查视觉编辑意图，复用 KV cache；不应一概描述成另加外部 Guard。公开 `qwen_image_edit_safe.py` 中有实际生成前门控与解析；代码提示、返回处理和极大 token 上限不能直接视为论文测量配置。

公平比较有两层：独立 VLM 上的 VJA-style 提示，与实际编辑器 cache 复用系统。前者不能拿后者的延迟报告背书。它已把编辑请求的真实意图与安全预测联系起来，故“图像编辑需要理解后果”不构成我们的新贡献。

### 3. IGSR：对原 Motivation 最具破坏性的先例

核对 §3 的行为/attention 分析、§4/Eq.1–2、Fig.3、Table1–4/Fig.5、A.8。Perception Decoupler 经教师生成的双路意图数据做 LoRA 训练；Cognitive Arbiter 在冻结目标模型上先枚举证据，再检查完成请求是否必须实现风险意图。**目标模型推理期不改参数，不等于整个方法完全无需训练。**

其消融区分 perception prompting、训练的 decoupler 与仲裁；我们必须比较这些机制，而不能只比一个短 Direct Prompt。attention 变化属于作者机制证据，不能单靠它推出“认知抑制”的唯一原因；这项限制也不能抹去它已经提出的研究问题。

本轮论文代码链接 404，故完整 IGSR 未跑通。可实现清楚标注的 prompt-only 迁移和用公开原监督的受限替代；不能将它们命名为作者 checkpoint 复现。

### 4. Meerkat-VL：自验证已有实际目标

核对 §3/Eq.3–11、Fig.5、Table2–4、§4.4–4.6。训练期用风险感知、意图感知、回答安全、回答帮助四个分数，NPSV 结合规则和标注评分，DPCA 惩罚答案分数高于相应感知分数。Table2 对感知项和一致性惩罚做消融。它不是简单推理时追加一次 Judge。

其一致性项具有真实计算含义；但分数仍由学习模型给出，不是任意语义命题的形式验证。迁移时必须隔离只在训练奖励中使用的标注。公开脚本有多 rollout 与八卡配置；当前资源下使用 checkpoint/同骨干轻量对照合理，忠实单卡重训不可先验承诺。

我们的候选若仍是“理解与安全两头监督+一致性”，没有清楚差异。潜在区别仅在源图与实际目标图之间的操作效果监督，且还要排除普通蒸馏即可解释。

### 5. SafeGuard-VL：策略与视觉边界已被覆盖

核对 §2–4、Fig.1–5、Table3/5/6。先通过 self-recaption 学习未被弱化的危险语义，再做策略条件 RL；SafeEditBench 使用局部编辑后的近似图像对，并在五类政策下判断。它评的是已有图像内容，不等于给任意未来编辑预测结果。

代码审查发现：奖励插件根据答案与格式计分，不能称为独立验证解释真实性；评测脚本将非识别标签最终映射为 0，包含 `unknown`。新实验应保留原协议复现轨道，另用统一 INVALID 计分轨道，而不能静默继承或改写后混报。论文对数据数量有 128 images 与 62 pairs 等表述，数据卡也有不同计数口径；必须以固定下载 manifest 解析，不把图数、配对数与政策实例数混用。

SafeEditBench 的 gated 状态是当前真实资源门；公共页面可见不等于已经获准读取文件。

### 6. SafetyPairs：连原子后果检查也不是空白

核对 §3–4/Fig.3–5/Table1。该工作不止生成安全—危险图像对，还用静态事实与应变化事实的 yes/no VQA 约束筛掉不忠实编辑，再人工核查，并研究轻量 Guard 的数据效率。这直接限制“用原子事实验证变化”这一创新包装。

其流程限制为危险到安全的生成方向，不能无依据把现成对反向命名为可信执行轨迹。代码 loader 有 `edit_instruction` 字段，但本轮没有取得并验证实际成品 metadata+图片包。**公开生成代码不等于当前已经具备可下载、标注可靠的全部训练三元组。**

候选算子方法必须超出使用配对数据与 VQA 约束；“推理期不看目标图、训练期从目标效果学操作”是需要另查重和消融的区别，不能靠本表证明首创。

### 7. PolicyShiftGuard：规则与成对间隔不再是独占路线

核对 §2–3、Fig.2 和方法消融章节。先标原子图像属性、再执行政策规则产生标签；训练随机化政策表述，随后对同图 pass/block 政策对加 margin。核心约束形如 `max(0,m-[s(block-policy)-s(pass-policy)])`，不是只做多次提示。

这会直接压缩“证据属性→确定性政策→成对训练”的新颖性。它改变的是政策轴，我们若改变操作轴仍需解释为什么这不是自然迁移。若只把 pair loss 中的政策文本换成编辑指令，方法创新不充分。

### 8. SSU：从局部证据到判决已有干预研究

核对 §III–IV、Eq.1–18、TablesI–II 和后续结果。使用单词替换或带意图区 mask 的图像对，分别 patch 改变位置与最后输入 token；还比较跨例安全方向和线性读出。作者明确区分“读出模型自己的决定”与“预测正确安全金标”。

机制干预主要选择原模型已区分正确的配对，故不能直接解释错误样本的全部机制。图像对中有外 mask 变化，论文对此作出限定；不能把它们描述成完全像素隔离的因果试验。我们的新方法也须面对同样条件。

因此，单独复现“早层局部、晚层决策”或增加线性探针，不足以作为新方法。若训练小算子，必须证明学到操作变化，不能只是复刻模型已有且可能错误的 verdict。

## 可迁移机制的精确区别

| 方法 | 实际计算 | 可迁移用途 | 不能迁移的推论 |
|---|---|---|---|
| AGLA | 用匹配模型梯度/attention 形成相关区域，`logits_global + α logits_local` | 强视觉证据基线 | 区域关注不等于安全判决有因果依据；相关 cue 可能遮掉风险背景 |
| VCD | 典型对照为 `(1+α)logits_original − α logits_distorted`，带候选约束 | 幻觉与额外前向预算控制 | 模糊/噪声图不是标签可信的安全反事实 |
| ShiftDC | 对模态引入的 activation shift，校准其安全方向分量 | 白盒风险表征对照 | caption 与图像不真正同信息；有读出信号不等于正确推理 |
| ITI | 在选定 attention heads 上沿学得方向偏移激活 | 小数据干预对照 | 更真实的回答不自动成为更安全的编辑判断 |
| Task Shield | 抽取指令，计算其对高优先任务的贡献，拒绝不贡献项 | 处理 cue/外部内容中的指令注入 | 目标本身危险时，忠实完成目标仍不安全 |
| UVR | 对早期输出 patch 与危险锚比较，定位后调节注意力流 | 编辑器内部安全干预竞争系统 | 与独立 Guard 的 F1/延迟不是同协议；其局部定位也不是视觉证据解释的万能证书 |
| CRC/LTT | 按独立校准损失/检验选阈值 | 所有方法共用的风险—覆盖校准 | 在自适应攻击或新政策上无条件得到分布无关安全保证 |

## 新颖性结论

**直接覆盖一般 Motivation 的前三篇：SIJA、IGSR、Meerkat-VL。**

**重新设计后必须加入的竞争者：SafeGuard-VL、SafetyPairs、PolicyShiftGuard、SSU。** 预印本与 workshop 不按 CCF-A 计，但依然影响技术首创性。

本轮没有发现一篇已核论文完全等同于本文 04 中的有向效果算子；这只是检索边界内的负结果。当前算子方案仍与表征蒸馏、条件算子学习、对比学习有明显关系，其“新颖”必须以更精确算法和同监督对照来证明。**不能用“没有同名论文”代替机制查重，不能把此结论写为 first/novel without qualification。**
