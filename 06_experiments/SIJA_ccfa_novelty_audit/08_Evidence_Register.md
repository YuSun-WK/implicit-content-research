# 证据总表与主张边界

审查截止：2026-11-17（北京时间）。本文件集中管理外部事实；研究方案与阈值是本项目判断，不是已测结果。论文元数据、方法描述、作者性能报告、项目旧实验和本轮静态阅读不能互相替代。

## 一、如何理解“独立核验”与支持强度

- **已核原文/代码**：本轮独立读取一手页面、PDF或固定提交，确认作者确实这样写/实现；没有独立复现实验性能。
- **公开日志核验**：交叉读取逐例计数/配置/事件及报告；原图/完整输出私有时，不能提升到语义金标复验。
- **强**：直接支持限定的文件/公式/状态事实。**中**：作者实验或条件性机制解释，范围受数据和协议约束。**有限**：摘要/元数据或访问不完整。**待证/判断**：本研究假设或策略评价。

SHA256用于记录所读PDF字节，Git blob SHA记录源码字节，不是内容正确性的证明。机器清单见 [09](09_Source_Manifest.json)；新版与新增实验详见 [10](10_SIJA_v2_and_FA2_Delta_Audit.md)。

## 二、仓库与项目已有证据

| Claim ID | 限定主张 | 来源及定位 | 官方/固定链接 | 独立核验 | 支持强度 | 尚缺证据 |
|---|---|---|---|---|---|---|
| R01 | main固定提交；目录规范允许独立实验审计，旧成果不可覆盖 | README、00_project工作流/目标/数据schema/进度/决策；main tree | [main快照](https://github.com/YuSun-WK/implicit-content-research/tree/985901a5c4830ac1f46dcad4884fbeee7bb82102) | 已读固定文件与tree，交付前刷新未变 | 强，仓库事实 | 不代表未提交服务器工作；API显示public而非用户所述private |
| R02 | PR #73尚未合并，P042及索引是前置读书材料 | head e37ea2…；P042、papers.csv、sources.csv | [PR #73](https://github.com/YuSun-WK/implicit-content-research/pull/73) | 已读实际文件，不只PR摘要 | 强，文件事实 | 不能用v1卡片覆盖v2新证据 |
| R03 | PR #74完成结构与CPU接口审计，没有模型推理；766条metadata并非完整金意图 | SI2ESBench_Data_Audit、data_structure日志；ZIP1535项/1532PNG；source766，声明spec路径0，combined cue766 | [PR #74固定目录](https://github.com/YuSun-WK/implicit-content-research/tree/508cca52ec7b7a87c0028c4a8756e62ebd690152/06_experiments/SIJA_feasibility_audit) | 已读六报告、指定接口及数据/接口日志 | 强，公开结构日志；语义有限 | 本轮未重下ZIP/逐图核验；不能声称所有图不存在或损坏 |
| R04 | 历史提示/解析器双尖括号与PDF单尖括号不同，不能称仅空白规范化 | PR74 scripts/original_prompt.txt、baseline_prompts.json、guard_interface.py；v1 p.26及v2 p.29 | [固定提示](https://github.com/YuSun-WK/implicit-content-research/blob/508cca52ec7b7a87c0028c4a8756e62ebd690152/06_experiments/SIJA_feasibility_audit/scripts/original_prompt.txt) | 读取源码、PDF文本并查看v1页面图像 | 强，格式事实 | 尚无性能偏差测量；不能认定历史模型结果因此错误 |
| R05 | H1已有ThinkingGuard权重加载与小样本推理；非FA2 | 分支experiments/h1-k0-triggerbench-20261106；H1_THINKINGGUARD_RESUME_ACCEPTANCE.md、acceptance.json、smoke metrics；官方格式4/4 INVALID，完整36对NOT_RUN | [H1固定分支](https://github.com/YuSun-WK/implicit-content-research/tree/e48548adf2429343f5810c1d8305fa93ce44915b/03_experiments/h1_k0_triggerbench) | 已读报告/结构结果，未审私有原始预测 | 强，有限运行事实 | 两对3/4准确、1/2 PairAcc不能说明总体性能；NF4约7.738GiB不能外推其它配置 |
| R06 | FA2已出现但可靠分析分母0；无Gold/Strong机制结论 | PR75 head6020ec…；00–06报告、configs、全部logs、technical_pilot/error_case_index及全部scripts | [PR #75](https://github.com/YuSun-WK/implicit-content-research/pull/75) / [固定实验目录](https://github.com/YuSun-WK/implicit-content-research/tree/6020ecd9b54f257b349add958495022eaa1ea693/06_experiments/SIJA_post_reconstruction_gap) | 全部公开文件已读；技术计数/哈希/事件交叉核对 | 强，公开技术事实；机制未建立 | 私有原图/完整输出未读；HUMAN_VERIFIED=0；4B未完整下载；正常模型输入0，Gold0；NO→NO不能当错误持续 |

审查早期返回81分支与两个开放PR；后刷新82分支、三个开放PR。初始“未发现FA2”仅为早期快照，**本交付已全部按R06修正**。PR75基于PR74，故不能从main缺目录推断FA2不存在。机器清单保留两次快照以解释差异。

## 三、论文方法、实验与发表状态

完整标题、年份、发表状态和CCF列统一在 [01](01_Literature_and_Novelty_Matrix.md)；下面定位支持实际比较的内容。正式主会A、Findings、workshop和预印本严格区分。

| Claim ID | 核心主张 | 页码/章节/表图 | 官方一手链接 | 独立核验 | 支持强度 | 尚缺证据/不可外推 |
|---|---|---|---|---|---|---|
| E01 | SIJA已包含r/a/s、后果预测与安全判断；v2已有正常效用、generic/relaxed与成本比较 | v2 §3.2、§5.3–5.5、C.3–C.5 pp.27–31 Tables12–14；v1提示p.26作历史对照 | [版本](https://arxiv.org/abs/2610.23909) / [v2 PDF](https://arxiv.org/pdf/2610.23909v2) / [代码](https://github.com/yexianmin/SIJA) | v1/v2 PDF、HTML与代码tree已核；核心方法/主实验和附录对照已读 | 强，方法/版本；作者性能为中 | 未独立重跑；未见Guard r/a/s/后果独立金标与条件错误分解；README不提供完整防御；ICLR2027在审不是录用 |
| E02 | VJA已有编辑器VLM自省安全门及KV cache复用，不能把前置意图安全判断当新原则 | §2.2/Fig.3；Appendix A.4/Table5；src/models/qwen_image_edit_safe.py | [ICML/PMLR](https://proceedings.mlr.press/v306/hou26h.html) / [代码](https://github.com/CSU-JPG/VJA) | 正式PDF方法/实验与核心门控源码已读 | 强，机制/正式状态 | 代码极大token上限/解析fallback不等于论文测量配置；独立VLM适配延迟不可借原系统数据 |
| E03 | IGSR直接限制一般性“感知到风险仍不安全”的首创性；LoRA双路意图+仲裁有具体训练机制 | ACL PDF §3–5，Eqs1–2、Fig.3、Table4及Figs4–5 | [ACL 2026 Main](https://aclanthology.org/2026.acl-long.1821/) / [PDF](https://aclanthology.org/2026.acl-long.1821.pdf) | 正式PDF方法、实验/消融及框架图已核 | 强，方法重叠；作者性能中 | 论文代码链接本轮404；不是全流程training-free；未直接测完整编辑r/a/s条件错误，不能说与FA2测量完全相同 |
| E04 | Meerkat把风险/意图感知和答案安全/有用性分开评分，以NPSV/DPCA及GRPO训练 | §3，Eqs3–11、Fig.5、Tables2–4；公开train_script/train.sh | [ICML/PMLR](https://proceedings.mlr.press/v306/zhou26ae.html) / [代码](https://github.com/Tunanzzz/Meerkat-VL) | 正式PDF方法/消融与训练入口已读 | 强，目标定义/正式状态 | 自验证不是独立形式真值；八卡配置不能承诺单卡重训；本轮未加载checkpoint |
| E05 | SafeGuard已有视觉语义增强、策略条件化学习及局部安全编辑评测 | CVPR PDF §2–4、Figs1–5、Tables3/5/6；plugin.py与safeeditbench.py | [CVPR正式PDF](https://openaccess.thecvf.com/content/CVPR2026/papers/Piao_Towards_Policy-Adaptive_Image_Guardrail_Benchmark_and_Method_CVPR_2026_paper.pdf) / [代码](https://github.com/adorableChowhound/SafeGuard-VL) | PDF、核心奖励/评测代码及数据卡已核 | 强，机制/状态；数据访问有限 | 128图/62对计数表述不完全一致，601是策略实例；RL checkpoint不等于Full；unknown映射safe须在统一协议中单列INVALID |
| E06 | ThinkingGuard已有逐步风险归因与关键步骤偏好；训练成本明显高于小头 | 作者PDF §§3–4、框架图与训练细节；首页ACM DOI；官方MM节目 | [DOI](https://doi.org/10.1145/3767308.3835707) / [作者PDF](https://arxiv.org/pdf/2609.36562) / [官方节目](https://2026.acmmm.org/site/ACMMM2026_Full_Programme.pdf) / [代码](https://github.com/FroggyChen/ThinkingGuard) | 作者PDF/DOI/节目交叉核对，推理代码与tree已读 | 强，状态与报告机制 | ACM出版页受访问限制，未下载出版方PDF；repo不等于完整训练发布；4×A100/约90min及搜索成本是作者设置 |
| E07 | VLSU已研究联合安全理解及结构CoT局限，非所有错误可归为单一重建问题 | 正式PDF §4–5 pp.6–7及结构推理实验/附录 | [ICLR 2026记录](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html) | 正式PDF主要实验与相关方法已读 | 强，已研究问题边界 | 不是图像编辑效果学习方法；本轮未复现其测量 |
| E08 | ShiftDC以视觉/文本激活偏移分解和安全方向投影干预表示 | 正式PDF §3方法、pp.4–6及后续校准公式 | [NeurIPS 2025 PDF](https://papers.nips.cc/paper_files/paper/2025/file/a627b9468c319c13a70b7c2fb8df65a3-Paper-Conference.pdf) / [代码](https://github.com/Renovamen/ShiftDC) | 正式PDF方法已读，代码入口核实 | 强，机制原则 | 不是已实现的编辑状态算子；本轮未审所有代码/训练 |
| E09 | AGLA已有局部增强与global/local logits融合；它处理幻觉，不保证政策执行 | CVPR PDF方法中的IPM/GradCAM及全局/局部解码 | [CVPR PDF](https://openaccess.thecvf.com/content/CVPR2025/papers/An_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_with_Assembly_of_CVPR_2025_paper.pdf) / [代码](https://github.com/Lackel/AGLA) | 正式PDF方法与官方代码入口核 | 强，计算原则 | 不将attention当因果解释；没有安全性能迁移证据 |
| E10 | VCD是原图/扰动图logits对照，语义对照本身不是新机制 | CVPR PDF §3解码公式 `(1+α)original−αdistorted`与候选约束 | [CVPR正式页](https://openaccess.thecvf.com/content/CVPR2024/html/Leng_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_through_Visual_Contrastive_CVPR_2024_paper.html) / [代码](https://github.com/DAMO-NLP-SG/VCD) | 正式PDF核心公式已核 | 强，原方法 | 视觉噪声不等于有效安全反事实；本轮未运行 |
| E11 | ITI已有少量数据学习attention-head方向并在推理期干预 | NeurIPS §3方法与干预定义 | [正式记录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/81b8390039b7302c909cb769f8b6cd93-Abstract-Conference.html) / [代码](https://github.com/likenneth/honest_llama) | 正式PDF方法/代码入口已核 | 强，原原则 | 原任务是真实性，不是编辑安全；未证明安全标签可线性分离 |
| E12 | Task Shield检查工具/指令是否服务用户任务；恶意用户目标仍需独立安全政策 | ACL PDF方法ContributesTo关系与任务对齐验证 | [ACL 2025 Main](https://aclanthology.org/2025.acl-long.1435/) | 正式PDF方法已读 | 强，机制/威胁范围 | 未核实完整作者代码；不能将任务对齐等同合法/安全 |
| E13 | UVR在生成中定位不安全输出patch并调节信息流，属直接系统竞品 | ICML PDF方法pp.3–5及unsafe anchor/attention机制 | [ICML/PMLR](https://proceedings.mlr.press/v306/yang26an.html) / [代码](https://github.com/deng12yx/UVR) | 正式PDF方法与代码入口已核 | 强，机制与状态 | 需编辑器内部状态；不能与独立Guard延迟/F1同协议排名；本轮未运行 |
| E14 | SafetyPairs已有安全关键局部反事实及静态/变化原子事实VQA筛选 | PDF §3–4 pp.4–6、Figs3–5/Table1；loader/config/pipeline | [作者发表状态](https://machinelearning.apple.com/research/safetypairs) / [PDF](https://arxiv.org/pdf/2510.21120v1) / [代码](https://github.com/apple-aiml-research/ml-safetypairs) | 方法/实验、作者状态及关键代码已读 | 强，配对与约束先例 | 2026 ICLR workshop非主会A；1510对/3020图是作者报告；本轮未取得完整成品数据包，不能声称其不存在 |
| E15 | PolicyShiftGuard已解耦属性与策略，并以同图不同政策的margin学习边界 | PDF §2–3 pp.3–5；§5 pp.8–9 Tables4–6；分类入口 | [arXiv](https://arxiv.org/abs/2607.05910) / [代码](https://github.com/ssmisya/PolicyShiftGuard) | PDF方法/消融、repo tree及分类入口已读 | 强，已提出机制；正式状态未核录用 | 不能把可执行规则或成对margin当新贡献；未完整运行训练发布 |
| E16 | SSU已有局部证据到判决的activation patching/读出；条件可区分对不代表全体正确 | PDF/HTML §3–4 pp.3–6与数据构造；57文本对/60图像对；14对仅局部改变，46对还有其它变动 | [arXiv](https://arxiv.org/abs/2610.07514) / [代码入口](https://github.com/faezehdehghant/SSU-Bench) | 主要方法/控制/限制已读 | 强，诊断先例；效果外推有限 | 网页与API访问不一致；线性读出模型自身判决不等于正确政策标签；非完整编辑Guard算法 |
| E17 | Grounding Safety研究VQA与坐标输出的安全差异 | 作者摘要及官方全文入口 | [arXiv](https://arxiv.org/abs/2610.05637) | 仅核摘要/元数据，未精读全文 | 有限 | 不能据此评判所有grounding方法；未核正式录用或完整代码 |
| E18 | DiffusionGuard保护图像持有者免受恶意编辑，与前置请求Guard威胁不同 | ICLR正式记录与PDF方法摘要；标题版本差异 | [ICLR 2025记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/43b77cef2a83a25aa27d3271d209e4fd-Abstract-Conference.html) / [代码](https://github.com/choi403/DiffusionGuard) | 正式记录/方法范围核验，未做全文级代码审计 | 中 | 不强作同任务分类baseline；PDF题名含Inpainting，记录题名为Image Editing |
| E19 | Conformal Risk Control在假设下控制预期风险，不自动保证适应性攻击安全 | ICLR论文风险控制定义/定理与交换性前提 | [ICLR 2024记录](https://proceedings.iclr.cc/paper_files/paper/2024/hash/f3549ef9b5ff520a7e41ff3cc306ab2b-Abstract-Conference.html) | 正式元数据与核心保证范围核 | 中 | 未设计本项目可证明损失；不能承诺条件/分布外/攻击保证 |
| E20 | Learn then Test用假设检验进行风险受控参数选择；正式发表并非ICLR | AOAS 19(2) pp.1641–1662，DOI10.1214/24-AOAS1998 | [出版方卷册PDF](https://www.imstat.org/publications/aoas/aoas_19_2/aoas_19_2.pdf) / [DOI](https://doi.org/10.1214/24-AOAS1998) | 正式出版元数据/核心方法范围核 | 中 | CCF不适用；没有证明本实验满足条件 |
| E21 | MagicBrush是人工指令编辑资料，不是自动安全金标 | NeurIPS 2023 Datasets&Benchmarks正式记录/官方项目数据说明 | [正式记录](https://proceedings.neurips.cc/paper_files/paper/2023/hash/64008fa30cba9b4d1ab1bd3bd3d57d61-Abstract.html) / [官方项目](https://osu-nlp-group.github.io/MagicBrush/) | 正式轨道/数据角色核；FA2图像访问见R06 | 强，资料性质 | 未下载图像包/审核正常标签；普通编辑不保证政策ALLOW |
| E22 | MSSBench已研究图文情境安全，但不同版本实例数量不同 | ICLR2025正式记录/数据摘要：1960对；早期1820不混用 | [正式记录](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html) / [代码](https://github.com/UCSB-AI/MSSBench) | 正式状态及版本元数据核 | 中 | 未精读/复现实验；来源混杂不能未经审计转写为SIJA事实 |
| E23 | SIUO为Findings NAACL2025，不能标主会A录用 | Anthology卷/书目信息 | [正式记录](https://aclanthology.org/2025.findings-naacl.198/) / [项目](https://sinwang20.github.io/SIUO/) | 正式元数据核 | 强，发表状态 | 本轮不声称全文级方法审计 |
| E24 | 新近Label Audit区分标签对象与数据来源混杂，支持本项目做捷径控制 | 作者HTML §4/Table3/Appendix D | [arXiv全文](https://arxiv.org/html/2611.01125v1) | 相关方法/结果/限制已读，未重跑 | 中，作者报告 | 其MSSBench报告不能转作SIJA数据缺陷；正式录用未核 |
| E25 | AnyEdit是另一公开编辑资料候选，现成安全三元组可用性未落实 | CVPR2025正式题名/记录 | [CVPR正式记录](https://openaccess.thecvf.com/content/CVPR2025/html/Yu_AnyEdit_Mastering_Unified_High-Quality_Image_Editing_for_Any_Idea_CVPR_2025_paper.html) | 仅核发表/资料角色；PDF直接访问403，正式HTML/索引可见 | 有限 | 未取得数据/许可证逐项审核，不纳入ready资源 |
| E26 | 模型与数据卡可用于选型，但当前访问和显存不能由名称推断 | HF API固定revision、gated/license/文件元数据；见09 | [Qwen3-VL-4B](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct) / [Gemma3-4B](https://huggingface.co/google/gemma-3-4b-it) / [InternVL3.5-4B](https://huggingface.co/OpenGVLab/InternVL3_5-4B) / [SafeEditBench](https://huggingface.co/datasets/tyodd/SafeEditBench) | 公开卡与API已核，未下载权重或受限图像 | 强，元数据；运行待证 | Gemma gated=manual；InternVL语言骨干Qwen3，不能夸称独立语言家族；FA2 Qwen下载失败不是模型不可用的永久结论 |
| E27 | 等级用CCF2026第七版；ICLR在该版为A；仅正式full/regular主会适用 | 官方发布/分类页；72页目录镜像pp.47、57 | [CCF官方目录页](https://www.ccf.org.cn/Academic_Evaluation/By_category/) / [2026 PDF镜像](https://scdm-shu.github.io/ccf/2026-CCF-Ranking.pdf) | 官方发布信息可检索；直接访问有405/JS限制，目录正文用镜像逐项核 | 中到强；镜像来源明确 | 未获得官方PDF同字节比对，不伪称官方原件哈希；不将2026等级倒推历史或授予workshop/Findings |
| E28 | 会议评价原创性/质量/意义有差异，没有统一“必需模型数/样本量/理论”门槛 | 各会议2026 reviewer guidelines | [CVPR](https://cvpr.thecvf.com/Conferences/2026/ReviewerGuidelines) / [ICML](https://icml.cc/Conferences/2026/ReviewerInstructions) / [NeurIPS](https://nips.cc/Conferences/2026/ReviewerGuidelines) | 官方页面相关评价标准核 | 中，规则概述 | 本项目会议建议是专家判断，不是会议承诺或录用概率 |

## 四、决定、假设与证据要求的区别

| Claim ID | 本研究判断/假设 | 推理依据 | 当前支持 | 哪种结果会推翻/限制它 |
|---|---|---|---|---|
| S01 | TGSV当前不值得按CCF-A方法项目完整开发 | E01–E05、E09–E16；M2未有可计算对象、M3未有独立约束 | 专家NO-GO判断，非实验失败 | 出现明确区别于已有工作的算法，且同监督/计算/机制证据成立时重审 |
| S02 | 一般性后重建错误宜作诊断，不能单独承担新问题 | IGSR/Meerkat/VLSU与SIJA原则重叠 | 强边界依据；新诊断具体测量仍可能有价值 | 窄问题有此前未覆盖机制、重要性与可验证算法时收窄重建 |
| H01 | 源图风险可能压过操作方向 | 任务逻辑，v2过拒只说明张力，不说明该机制 | **未建立** | K-DIR强基线已解决、金标/策略/格式可解释残余时停止 |
| H02 | 实际目标侧监督可支持超出普通CE/MLP的风险效果学习 | 04中的候选残差算子；不是现有结果 | **未实现/未评估** | 同监督简单模型相当、随机配对不降、只提高全拒绝时停止 |
| S03 | 优先C1限额否证，其余暂不开发；C>D>B>E>A | 直接竞品、资源与数据门综合 | 策略排序，不是录用概率 | 数据门/机制门失败即E；不把D误当现成新算法 |
| S04 | Gold-Intent处理不能自动识别内部因果机制 | 03因果图、额外文本可直接影响后果/判决、条件选样 | 逻辑/识别分析 | 只能用更强识别设计缩小替代解释，不能以错误持续次数替代 |
| S05 | 单卡小试可做，完整论文远超一个六小时块 | 固定调用预算、模型规模与公开训练配置、R05/R06技术日志 | 条件估算，非本轮实测 | 实际显存/吞吐、可用资料及审核人力不足时缩主张或停止 |

K-DIR的32组、24测试组、6/4个错误门槛与+5pp方法投入门是本项目预注册决策规则。功效计算、Wilson/配对统计用于表达不确定性；没有任何来源将这些数字规定为CCF-A最低录用标准。

## 五、本轮没有完成的验证

本轮没有SSH/GPU运行、权重下载、训练、FA2重跑、图像编辑生成、适应性攻击或全包图像审核。原论文表格数字均为作者报告；PR75是其它任务提交的公开日志。本研究的替代算法、效果、泛化与新颖性均待后续门验证。所有论文结果占位符必须在真实证据取得后才替换。
