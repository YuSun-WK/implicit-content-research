# P037｜VLSBench: Unveiling Visual Leakage in Multimodal Safety

> **2026-11-02 用户明确授权定稿、上传、合并。** 正式ACL论文与公开数据/评测代码静态审计；**未在GPU跑完整实验、未重新调用GPT-4o评审，也未实物逐张检查全部图片**。以下论文报告与审计结论分开。

## 01 书目信息与材料
- Xuhao Hu, Dongrui Liu, Hao Li, Xuanjing Huang, Jing Shao, **ACL 2025 Main（CCF-A）**，DOI 10.18653/v1/2025.acl-long.405，pp.8285–8316。
- 官方PDF https://aclanthology.org/2025.acl-long.405.pdf；官方GitHub https://github.com/AI45Lab/VLSBench ；数据 https://huggingface.co/datasets/Foreshhh/vlsbench 。
- 已静态读取 README.md、data/data.json、eval.py、eval_utils.py，以及models目录；未训练作者模型/调API。

## 02 研究问题、任务边界
- **VSIL（Visual Safety Information Leakage）** 指多模态安全测试中，图片承载的关键风险信息已经被文本问题表达，导致模型无需真正理解图像也可能正确拒绝。
- 论文研究安全**响应**（Refusal/Warning/Unsafe），并非输入风险二分类准确率。Safe Rate高可能来自过度拒绝，不能等同风险识别准确、因果视觉理解或真值。
- 研究动机：旧多模态安全基准中纯文本安全对齐表现可与图文对齐相近；作者质疑是数据文本信息泄漏导致捷径。

## 03 VSIL形式与评审模型
- 对同一危险场景，用LlamaGuard3-11B-Vision（**预训练安全Judge直接推断；没有为每个基准分别微调**）分别评审J(I,T)、J(T)；若两者都为unsafe，则存在操作性VSIL证据。
- R1 = mean 1[J(I,T)=unsafe]；R2 = mean 1[J(I,T)=J(T)=unsafe]。当R1约等于R2，说明经Judge判危险的图文样本有较多只靠文本即可判危险。
- 论文Table1四基准：SafeBench (54.80%,54.40%)，JailbreakV-raw (65.36%,65.00%)，Harmbench-mm (30.91%,30.00%)，VLSafe (91.35%,91.08%)。差值约0.27–0.91百分点；依赖Judge，不证明所有被测MLLM实际没用图片。
- 作者实验中另外使用LlamaGuard3-8B评估部分响应，区分11B-Vision初步输入风险审查与8B输出安全评判。

## 04 数据构建/GT
- 官方data/data.json**2241条**，六大类：Violent590、Illegal Activity539、Self-Harm370、Erotic343、Hate269、Privacy130；19子类。
- 数据字段 instruction_id/instruction/image_path/category/sub_category/source/image_description/safety_reason；**没有天然平衡的安全与危险双类金标**。
- 来源计数（静态JSON）：generation1234、MultiTrust296、coco2017 130、Ch3Ef179、MLLMGuard260、Unsafebench142。来源混合生成、现有图像，注意近重复/图片语义不足问题。
- 生成方法：从风险元素或既有图片出发，生成初始问题/图像描述→重写文本去除直接风险信息→生成/收集匹配图片→模型与人工审核，使用GPT-4o/Qwen2-VL-72B/SD3.5等现成模型；非训练新生图网络。
- 有些safety_reason语义为“可能未经授权”“可能造成伤害”，应理解为**潜在风险警告**而非“确定正在执行违法有害行为”的客观事实。相同I,T可能合法授权或未经授权；适合安全响应和风险感知，直接全标unsafe训练二分类会单类退化。
- 静态数据审计：图片路径unique=1957、instruction unique=2226、至少1条空instruction（id1685），存在问题文字与图像路径重复及少数sub_category和category交叉；不等于已证实图像字节相同，也不是已跑数据清洗。

## 05 主要实验、算法、训练成本
- 作者评测LLaVA、Qwen2-VL、Llama3.2-Vision、GPT-4o等多模型，比较Textual SFT、Multimodal SFT、Textual DPO、Multimodal DPO、PPO与unlearning类已有方法；**无新PPO/DPO公式或训练策略贡献**。
- SFT：最大化安全参考回答token概率（CE）；DPO：给定偏好对(x,y+,y-)，提高好回答相对差回答与参考模型的log-odds；PPO：已有SPA-VL协议。切勿把文本SFT与图文SFT差距全归因视觉，二者训练来源/分布不匹配。
- 文本SFT筛选SafeRLHF约2000风险+1000正常=3000条；图文SFT参考VLGuard；DPO参考SPA-VL约3万偏好数据（详表以正式论文为准）。完整训练含4×A100 80GB，超出单卡16–20GiB ≤6h目标。

## 06 输出评测定义和代码口径
- GPT-4o评审响应三类：label1 Safe with refusal（拒答），label2 Safe with warning（风险警告并适当回应），label3 Unsafe（忽视风险直接回答）。
- Safe Rate = #1 + #2；Warning rate与Refusal rate分开。拒答比例高可抬高SafeRate，即使模型根本没识别视觉风险。
- **对用户的重点答疑**：图文输入安全率、仅文本安全率、文本+图片描述安全率变化，是响应策略变化，不直接等于风险理解能力变化。Qwen2-VL-7B在200样本试验：图文16.0（拒1.0，警15.0）；文本29.5（拒19.5，警10.0）；文本+图片描述22.5（拒3.5，警19.0）。移除图像可能引发保守拒答；插入文字描述可能把拒答转成带警告回答；不可称文本更懂图文。
- 表2旧基准Textual SFT已有高SafeRate；表4 VLSBench多模态SFT常明显优于文本SFT：LLaVA1.5-7B 21.26 vs13.99、LLaVA1.5-13B 28.03 vs14.71、Qwen2-VL-7B 78.39 vs67.42；实验支持有图训练在新基准更优，但数据混杂使单因归因不足。

## 07 公开代码静态核验
- eval.py对应不同模型loaders；其main里**data = data[:2]**，按README示例运行仅测2条，完整评测需删除/调整截断。
- eval_utils.py依赖OpenAI API GPT-4o结构化Judge，输出1/2/3；无法免付费完整复现实验；当前模型/API可用性与论文运行时版本不同。
- eval.py没有公开所有训练设置的端到端训练工程，已发布部分模型checkpoint入口；静态读取不等于权重已实物下载/本地复现。

## 08 论文贡献与局限
- 主要贡献：针对多模态安全数据中的文本捷径提出VSIL检查、构造更少风险文字泄漏的VLSBench并评测文本/图文安全对齐相对优势。
- 局限：去掉文字直接风险线索≠模型必须使用关键图片；风险说明主观性与欠缺干净的safe负例；过度拒答可能提高SafeRate；Judge不完美；Textual/Multi SFT训练数据分布差异；原脚本默认只测前2条。
- 不推断模型已内化正确跨模态因果路径；不把任何未经验证的小问题宣布作者主结论无效。

## 09 反事实/最低成本实验启示
- 使用公开样本+文本/图文消融与同图语义变化对照检查关键视觉依赖，指标必须分输入风险识别Accuracy/F1（前提GT可靠）、输出Refusal/Warning/SafeRate、解释忠实性。
- 当前2241条以潜在风险正例为主，不具备平衡二分类金标；可直接用于小规模无训练安全响应评测、无需复杂GPU，但官方GPT Judge收费且图片实物需确认。
- P041：发现单模态看安全、联合后不安全的任务；P037：安全基准不应把视觉线索泄漏到文字中。P038进一步系统测联合安全理解；P039涉及反事实归因；P040自验证，须先查重再做创新假设。

## 10 留存疑点/复现待办
1. 核验图片下载、图像内容对应及真实的身份/授权上下文，不以safety_reason一律当客观金标。
2. 审计重复instruction和images路径/近重复分组；剔除空instruction后重算主结果。
3. 匹配训练数据来源与规模，分别控制图文输入、训练与Judge，排除分布混杂。
4. 检验SafeRate增加来自拒答还是真正的风险识别；增加不安全/安全反事实对需新标签来源与成本审计。
5. 如需运行官方eval.py须处理[:2]及付费GPT Judge限制；不能声称已复现整表。

## 11 定稿
- **2026-11-02经用户授权定稿并合并main**。文章重要性：ACL 2025 Main/CCF-A，多模态隐晦风险评测的直接竞品/捷径审计基础。
- 下一篇P038 VLSU（ICLR 2026/CCF-A），从任务和标签合法性、17组合模式、三层风险判定、8,187数据、论文实验协议与代码实物开始。
