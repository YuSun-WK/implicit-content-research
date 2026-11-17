# 相关工作与创新性矩阵

检索截至2026-11-17。证据等级：P=本轮原文/正式出版页；C=本轮代码静态审计；R=项目既有精读卡；N=尚未逐项核验。不能把R升级成新复现。正文摘要与下面研究判断分开；没有穷尽全部文献的保证。

CCF口径：ACL、NeurIPS、ICML、CVPR、AAAI、CCS、ACM MM为本项目A类目标；Findings不能直接冒称主会A。ICLR按项目2026口径列A*；本轮CCF官网返回405、镜像PDF解析失败，最新目录独立核验未闭合，星号不影响技术竞争判断。NAACL主会按既有B口径记录，等级不决定创新性威胁。

## 统一比较矩阵

| Paper / 作者 | Venue / 状态 | Task、数据、评价 | Failure / Method | 与H1关系与Novelty Threat | 证据/代码状态 |
|---|---|---|---|---|---|
| **ThinkingGuard: Decoding Implicit Hazards via Step-by-Step Risk Attribution in Multimodal Large Language Models**；Ruochen Zhang等 | ACM MM2026 / A；作者出版栏DOI已见 | 隐含风险分类；TriggerBench与外部基准；F1/Recall | 触发因素、五步归因、SA-MCTS、双层DPO | **最高直接竞争**；已发现并方法化关系风险、反事实与过程监督 | [原文§3–5](https://arxiv.org/html/2609.36562v1)，P+C/R；[推理代码](https://github.com/FroggyChen/ThinkingGuard)，完整训练搜索未独立取得 |
| **MMAligner: Safeguarding Multimodal Large Language Models through Representation Calibration**；Shenyi Zhang等 | CCS2026 / A；最终ACM PDF逐项比对未做 | 安全生成；MM-SafetyBench、VLGuard、越狱/效用；拒答/无害性 | 拒答方向与边界校准、良性保持 | **最高表示路线威胁**；不同任务不能免除算法比较 | [原文](https://arxiv.org/html/2608.05909v1)，P+C；[basic实现](https://github.com/shenyizg/MMAligner) |
| **VLSU: Mapping the Limits of Joint Multimodal Understanding for AI Safety**；Shruti Palaskar等 | ICLR2026 / A* | 三层Safe/Borderline/Unsafe；分类与响应分开 | 联合理解失败的组合诊断 | 同一问题族已被系统发现；不能再把unimodal正确/joint错作首创 | [正式页](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)，P+R；[数据/下载工具](https://github.com/apple-aiml-research/ml-vlsu) |
| **VLSBench: Unveiling Visual Leakage in Multimodal Safety**；Xuhao Hu等 | ACL2025 Main / A | 去文本视觉风险泄露评测；安全响应/对齐比较 | 文本即可泄露视觉风险；构造leakless数据 | 单模态捷径观察与“文本不够”不是新问题 | [正式页](https://aclanthology.org/2025.acl-long.405/)，P+R；[公开代码](https://github.com/AI45Lab/VLSBench) |
| **Meerkat-VL: Implicit Risk Safety Alignment in Multimodal LLMs via Perceptual Reasoning and Self-Verification**；Peicheng Zhou等 | ICML2026 / A | 隐含风险安全响应；Meerkat-Safe；安全/帮助 | 规范自评、感知与回答一致性、GRPO | 解释—决定分解或自检并非新方法；仍可问其视觉忠实性 | [正式页](https://proceedings.mlr.press/v306/zhou26ae.html)，P+R；[训练代码](https://github.com/Tunanzzz/Meerkat-VL)，本轮未完整复审全部训练源码 |
| **CrossGuard: Safeguarding MLLMs against Joint-Modal Implicit Malicious Attacks**；Xu Zhang、Hao Li、Zhichao Lu | ACL2026 Main / A | 输入风险guard；ImpForge；显式/隐含与正常输入 | 生成联合攻击数据、微调检测 | 同任务直接基线；“新数据+轻量训练”已经存在 | [正式页](https://aclanthology.org/2026.acl-long.1178/)，P+R；[代码](https://github.com/ZhangXu0963/CrossGuard) |
| **Multimodal Situational Safety**；Kaiwen Zhou、Chengzhi Liu、Xuandong Zhao等 | ICLR2025 / A* | 视觉情境中的安全回答/动作；MSSBench | 同一请求随情境改变风险，分解感知/情境推理 | 场景依赖及分解pipeline早已提出 | [正式原文](https://proceedings.iclr.cc/paper_files/paper/2025/file/1cb57fcf7ff3f6d37eebae5becc9ea6d-Paper-Conference.pdf)，P；[项目](https://mssbench.github.io/) |
| **Unraveling and Mitigating Safety Alignment Degradation of Vision-Language Models**（CMRM）；Qin Liu等 | **Findings ACL2025**，不是ACL Main A | 安全生成；VLSafe等 | 模态表示差、推理时修正 | 表示gap与恢复不是新发现 | [正式页](https://aclanthology.org/2025.findings-acl.186/)，P；MMAligner参考文献仅写预印本，已更新此状态；代码端到端N |
| **Understanding and Rectifying Safety Perception Distortion in VLMs**（ShiftDC）；Xiaohan Zou、Jian Kang、George Kesidis、Lu Lin | **NeurIPS2025 Main / A**；MMAligner引文写2026，采用正式页年份 | 安全响应、效用，**含输入安全分类§6.4**；MM-SafetyBench/LLaVA正常数据 | 只消除安全相关的模态偏移，保留视觉语义 | **直接否定“首次校准风险识别”**；不只拒答工作 | [正式页](https://papers.nips.cc/paper_files/paper/2025/hash/a627b9468c319c13a70b7c2fb8df65a3-Abstract-Conference.html)，[原文§6.4](https://papers.nips.cc/paper_files/paper/2025/file/a627b9468c319c13a70b7c2fb8df65a3-Paper-Conference.pdf)，P；[官方代码](https://github.com/Renovamen/ShiftDC)公开、完整复现N |
| **Steering Away from Harm: An Adaptive Approach to Defending Vision Language Model Against Jailbreaks**（ASTRA）；Han Wang、Gang Wang、Huan Zhang | CVPR2025 / A | 越狱防御、正常任务；ASR/utility | 视觉token随机消融归因，构造方向，自适应steering | 动态门控、视觉风险token和条件steering已覆盖 | [正式页](https://openaccess.thecvf.com/content/CVPR2025/html/Wang_Steering_Away_from_Harm_An_Adaptive_Approach_to_Defending_Vision_CVPR_2025_paper.html)，P；[代码](https://github.com/ASTRAL-Group/ASTRA) |
| **Safety Alignment for Vision Language Models**（SafeVLM）；Zhendong Liu等 | arXiv2024，**正式会议未核实** | 风险图像安全生成；RTVLM等 | safety projector/tokens/head，两阶段训练 | 不是天然的单方向hook方法；新增安全模块已有先例 | [作者原文](https://arxiv.org/abs/2405.13581)，P；原文说将开源，本轮未确认对应完整代码 |
| **DREAM: Disentangling Risks to Enhance Safety Alignment in Multimodal Large Language Models**；Jianyu Liu等 | NAACL2025 Main / B | 分解风险并安全生成；VLGuard/FigStep/SIUO/benign | MRD分解来源/类别/内容，SFT+RLAIF | “图/文/意图/决定解耦”本身已有；需同信息量对照 | [正式原文§3](https://aclanthology.org/2025.naacl-long.604.pdf)，P；[作者仓库](https://github.com/Kizna1ver/DREAM)，本轮未验证训练完整性 |
| **Cross-Modal Safety Mechanism Transfer in Large Vision-Language Models**（TGA）；Shicheng Xu、Liang Pang、Yunchang Zhu、Huawei Shen、Xueqi Cheng | ICLR2025 / A* | 将文本安全机制迁到视觉；安全与视觉任务 | 相关文本检索引导隐藏表示对齐 | 图文安全表征对齐高度重合；不是免费小型post-hoc实验 | [正式页](https://proceedings.iclr.cc/paper_files/paper/2025/hash/92ee07d8a2c8f5ec08eff83f9eff0c1b-Abstract-Conference.html)，P；[代码](https://github.com/xsc1234/VLM_Safety_Transfer) |
| **Internal Activation Revision: Safeguarding Vision Language Models Without Parameter Update**；Qing Li、Jiahui Geng等（MMAligner引文含Derui Zhu、arXiv作者表无此名，最终作者表待核验） | AAAI2025 / A；DOI34954 | 安全生成；SafeBench等 | layer/head级内部激活修正 | “不更新主模型+激活干预”不是创新；方向构造需公平比较 | [AAAI](https://ojs.aaai.org/index.php/AAAI/article/view/34954)访问受限；[作者稿](https://arxiv.org/abs/2501.16378)，P；代码未独立确认 |
| **HiddenDetect: Detecting Jailbreak Attacks against Multimodal Large Language Models via Monitoring Hidden States**（正式页标题；PDF写Large Vision-Language Models）；Yilei Jiang等 | ACL2025 Main / A | **输入攻击检测**，非仅安全回应 | 冻结内部安全信号检测 | 线性probe/读隐藏风险信号不能作为首创 | [正式页](https://aclanthology.org/2025.acl-long.724/)，P；[作者稿及代码入口](https://arxiv.org/abs/2502.14744) |
| **ShieldVLM: Safeguarding the Multimodal Implicit Toxicity via Deliberative Reasoning with LVLMs**；Shiyao Cui等 | 2025预印本；正式会议未证实 | MMIT2100，隐含毒性输入/对话检测 | deliberative cross-modal reasoning | 风险关系/解释式检测直接近邻，必须纳入 | [作者稿](https://arxiv.org/abs/2505.14035)，P（本轮主要核对元数据/摘要，方法全文N） |
| **ReSAM: Representation-Level Safety Margin Alignment for Vision–Language Models**；Jiachen Ma等 | **NeurIPS2026已列官方节目 / A**；早期ICLR稿与最终版需区别 | pseudo-benign安全失败、表示margin | 拒答方向与margin校准 | 又一个强表示路线威胁；旧稿是重叠证据，最终细节待核验 | [官方列表](https://neurips.cc/Downloads/2026)、[作者公告](https://emigmo.github.io/)、[最终PDF入口](https://openreview.net/pdf?id=Q8etLWU90b)被验证页阻断；早期[稿](https://openreview.net/pdf?id=J5pqVzrwNo)可读 |
| **Risk Awareness Injection: Calibrating Vision-Language Models for Safety without Compromising Utility**；Mengxuan Wang等 | 2026预印本，正式会议未核实 | 越狱安全/正常效用 | 文本unsafe原型子空间、高风险视觉token调制 | 风险信号放大/视觉选择性校准高度相近 | [作者稿](https://arxiv.org/abs/2602.03402)，P元数据/摘要，全文实现N |
| **SafeSteer: Adaptive Subspace Steering for Efficient Jailbreak Defense in Vision-Language Models**；Xiyu Zeng等 | 2025预印本，正式会议未核实 | 越狱防御 | SVD子空间与自适应steering | 低秩风险子空间/门控不是空白 | [作者稿](https://arxiv.org/abs/2509.21400)，P元数据/摘要，完整复现N |

## 对MMAligner近邻描述的交叉更正

不能把被审论文的related work作为近邻方法的最终定义。其附录将ASTRA近似为均值方向门控，将SafeVLM近似为推理hook；作者原文分别描述视觉token归因与可训练安全模块，**两套比较对象未必等价**。若复用该论文基线实现，必须注明简化改编，不能据其较低分断言原方法弱。

同理，CMRM已正式发表于Findings，ShiftDC是NeurIPS2025；HiddenDetect已有ACL Main页面。论文参考文献中较旧/不一致元数据不应直接继承。ReSAM的早期ICLR状态不能替代2026-11-17已出现的NeurIPS节目状态。

## 科学内容覆盖裁决

| 拟主张 | 已发现/解释/方法化程度 | 还能问什么 |
|---|---|---|
| 单模态安全、组合有风险 | SIUO、MSSBench、VLSU、ShieldVLM、ThinkingGuard已发现 | 具体分类器在严格任务下的失败形态 |
| 加模态后安全信号减弱 | CMRM、ShiftDC、TGA、MMAligner等已有分析与修复 | 是否存在与拒答偏置不同的关系依赖机制 |
| 中间解释与最后判断不一致 | 多篇过程监督/一致性/自评已有 | 解释的可操纵性与视觉证据的实际依赖 |
| 风险表示可probe | HiddenDetect与ShiftDC直接相关 | 跨场景泛化、绑定特异性及随机方向对照 |
| 反事实更可靠 | ThinkingGuard明确训练构造；一般反事实/对比学习成熟 | 被验证风险干预与无关干预的可识别条件，不能只换loss |
| 保持Safe同时修Unsafe | MMAligner直接做；ASTRA/ShiftDC也强调utility | 同FPR、同监督、同计算下的局部可解释收益 |

当前没有被本审计认证为“已确认未解决”的方法gap。最有希望的窄问题是**经验证的动作—目标关系干预下，风险判别的证据条件依赖**；首先要证明它不能由数据、任务、感知或简单阈值解释，再决定算法。

## 已有项目记录避免重复

已读P034/P037/P038/P039/P040/P041及`02_synthesis/R1–R5`。用户建议的`03_survey/R1_taxonomy/`等路径在指定commit不存在，实际综合位于`02_synthesis/`。项目早已记录文本捷径、反事实多因素、解释不忠实、Step-DPO信息/预算混杂、VLSU test-only与数据版本差异；本轮不把这些当新发现。新增加的是原始结果复算、72张图实审、分级记录、MMAligner源码疑点、ShiftDC分类实验与更新后的近邻覆盖判断。
