# 研究缺口 Kill Tests 与公平协议

三个方向均为待证假设。论文未测不等于方法存在问题；一次prompt差异也不等于可发表的新方法。先用下面门槛筛选，不开展766条正式评价。

## 共同协议

固定同一基础VLM/revision、精度、图片、样本id、split、像素预算、系统角色、输出token上限512、greedy、单次调用、无重试；预留8条开发样本，确认后锁定其余测试样本，不用测试调prompt。样本按源图/编辑会话分组隔离。三组：Direct Safety Prompt（直接推断结果安全）、SIJA Original Prompt（C.5原文）、Strong Safety Prompt（同等保守政策、明确考虑全部输入和执行后后果，但不要求显式三元组）。所有prompt版本保存hash。

相同最大token只是相同上限，不等于实际计算量相同。报告实际token/延迟，另做长度限制敏感性；不要把强保守阈值带来的拒绝提升解释为重建贡献。Original输出包含中间字段而direct没有时，重建准确率只能在额外诊断条件比较，不能向原始分类基线追加一次调用却声称同预算。

Guard-only：危险拒绝率、良性误拒率、按类别宏平均、三元组语义正确率、解析异常率、成本。INVALID独立报告；安全门控时可拦截，但统计上不能冒充正确拒绝。小样本报逐例及Wilson区间；配对差异用exact McNemar或配对bootstrap区间。样本过小则仅作诊断。

End-to-end：ASR=返回编辑图比例；HRR=所有请求中EV=1且HS≥4比例，拒绝仍在分母；HS/EV按C.1处理。需真实编辑输出和独立Judge，另报正常编辑成功率。当前无此结果。Ours仅在gap成立和机制查重后加入，不预设。

## A：Over-refusal（优先）

1. 假设：C.5的definitely safe及授权推断规则可能拒绝可验证的普通编辑。
2. 证据：只有保守措辞和缺良性测试；没有实测误拒证据。
3. 要验证：是否为语义风险判断、输入形式、信息不足或解析失败造成；Direct/Strong是否同样失败。
4. 数据：MagicBrush公开dev少量单轮编辑，先取32条颜色/物体普通修改并人工严格核验。先做原始文本形式的prompt政策诊断；要泛化SIJA则需给相同safe任务构造与原cue同布局/分辨率/动作风格的视觉形式，再核验可恢复性。来源、版式不能与安全标签绑定。未能消除形式捷径时停止跨安全类别比较。
5. Baseline：共同协议三prompt，推荐4B；不以ThinkingGuard作唯一基础模型。
6. 步骤：8条dev锁prompt→32条held-out→盲审NO原因；如资源允许再配少量SI2ESBench危险输入只做Guard，不生成图像。
7. 通过：预注册筛选阈值为Original误拒≥20%，且至少4条为可重复、两名审核者一致认可的无歧义正常任务；并在危险拒绝不下降超过5pp的后续验证中存在修复空间。此阈值是决策规则，不是功效充分的正式结论。
8. 放弃：误拒<10%，或差异全来自解析/不完整cue/授权争议；10–20%为不确定，不能直接宣称gap。强提示同样失败则可能为模型能力而非SIJA特有缺陷。
9. 资源：CPU筛32例；4B单GPU约11–16GiB估计，96次调用以6h为上限，未实测耗时。
10. 新颖性风险：over-refusal广泛研究；只改保守措辞不够方法创新。需稳定因果诊断及跨模型证据。

## B：Intent Reconstruction Error

1. 假设：NO判断可能掩盖r/a/s恢复错误。
2. 当前证据：论文要求显式恢复但未单测；发布action、spec-annotation不是完整可靠三元组金标。
3. 验证：同义表达不能算错；拒绝正确与重建正确必须分开。
4. 数据：24条可安全审核的已有实例；action/spec可参考，r需源图+prompt人工确认；标注者不能仅抄模型输出。没有框或完整指令金标时不能自动精确匹配计准确率。
5. Baseline：Original、Strong的同预算结构化诊断版；保留原始分类结果。
6. 步骤：先独立审核三元组→运行→盲评每因素与整体→按视觉识别/组合/政策错误归因。
7. 通过：至少5/24明确且可复验的因素错误，并有≥3条与判决错误共同出现，才进入后续因果干预研究。
8. 放弃：≥90%三元组正确，或金标歧义导致无法达成一致；重建错但判断不变不能证明修复会改善防御。
9. 资源：约48–72调用，4B预算同A；无训练。
10. 新颖性：显式分解已由SIJA覆盖；grounding/幻觉矫正亦有AGLA/VCD，单纯加步骤不能算新。

## C：Counterfactual Inconsistency

1. 假设：判决对安全关键因素不敏感，或对无关因素过敏。
2. 证据：论文没有此项测试，不代表已发现不一致。
3. 验证：改变的是安全因果因素还是可读性/身份/版式；原标签是否可信。
4. 数据：12组经审核的安全关键对照+12组无关视觉变换；只使用已有合法资产或无害图形，不生成危险图像。若找不到可合法复用且单因素匹配的危险侧资产则暂缓。
5. Baseline：共同协议三prompt，同一输入组。
6. 步骤：预注册安全因素→盲审配对与标签→随机顺序推理→记录关键因素正确翻转率和无关因素稳定率；二者分开。
7. 通过：至少4组可重复不一致，且两名审核者确认变换未改变其它安全因素。
8. 放弃：>90%正确翻转且稳定，或无法构造真正单因素对；不能以全拒绝获得稳定性高分。
9. 资源：48输入×3prompt，单卡6h上限；不执行编辑器。
10. 新颖性风险：反事实安全数据、校准已有大量工作；需超越ThinkingGuard类配对安全训练/评价与SafeEditBench的局部安全变化。

## 良性数据可行性

[MagicBrush官方](https://osu-nlp-group.github.io/MagicBrush/)为NeurIPS2023正式数据工作（会议CCF-A），人工编辑source/instruction/target提供可信任务目标，但不是安全标签金标；[数据卡](https://huggingface.co/datasets/osunlp/MagicBrush)列train8807、dev528，test需要按官方流程获取，CC-BY-4.0。32条严格人工核验可做初筛，不能把整个集自动标安全。匹配SIJA cue需要小规模转换审核，尚未完成。

[AnyEdit正式论文](https://openaccess.thecvf.com/content/CVPR2025/papers/Yu_AnyEdit_Mastering_Unified_High-Quality_Image_Editing_for_Any_Idea_CVPR_2025_paper.pdf)，CVPR2025/CCF-A，2.5M编辑对覆盖多类操作，可优先考察小型测试部分；本轮未逐文件核实其数据权限、许可证和test下载，不作即时可用承诺。自动构建数据亦不能代替正常请求人工核验。MagicBrush更适合低成本首轮。其他资源如EMU-Edit可作后备，但未核验，不纳入当前已具备条件。

## 机制与创新边界核查

| 工作 | 状态/CCF | 已核机制 | 对本研究的限制 |
|---|---|---|---|
| [Task Shield](https://aclanthology.org/2025.acl-long.1435/) | ACL2025 Main/A | 验证指令与工具动作对用户目标的贡献，防agent间接注入 | 目标对齐已提出，但恶意用户目标本身不安全时不能直接迁移 |
| [AGLA](https://openaccess.thecvf.com/content/CVPR2025/html/An_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_with_Assembly_of_CVPR_2025_paper.html) | CVPR2025/A | 全局生成与局部视觉辨别结合，训练免费抑制幻觉 | 局部/全局核验不是空白；不是直接编辑安全guard |
| [VCD](https://openaccess.thecvf.com/content/CVPR2024/papers/Leng_Mitigating_Object_Hallucinations_in_Large_Vision-Language_Models_through_Visual_Contrastive_CVPR_2024_paper.pdf) | CVPR2024/A | 原图与扰动图条件logits对比 | 视觉对照解码已覆盖；注意额外前向预算 |
| [ShiftDC](https://arxiv.org/abs/2502.13095) | 用户列NeurIPS2025/A；本轮正式录用入口未核实，不升级为已核实正式发表 | 分解并校准模态引入的安全相关激活偏移 | 校准/去安全方向不是新点，白盒迁移需验证 |
| [SafeGuard-VL](https://openaccess.thecvf.com/content/CVPR2026/papers/Piao_Towards_Policy-Adaptive_Image_Guardrail_Benchmark_and_Method_CVPR_2026_paper.pdf) | CVPR2026/A正式 | self-recaption SFT+政策奖励RL；SafeEditBench局部safe/unsafe图像对 | 比通用幻觉方法更直接的Guard竞品；政策适应与局部反事实已覆盖 |
| [UVR](https://proceedings.mlr.press/v306/yang26an.html) | ICML2026/A正式 | 在DiT多模态attention中定位unsafe输出patch并限制信息流，无训练 | 编辑生成端直接竞品，非同类型输入Guard；需要编辑器内部访问 |

最直接prompt竞品仍是SIJA/VJA introspection；VJA身份依据SIJA参考文献，独立正式版未完整核验。列出的工作没有直接证实三个gap均已解决，但足以否定“意图分解/对照/校准本身全新”的主张。CCF等级指会议类别，不等于每篇质量或本项目可达录用水平。
