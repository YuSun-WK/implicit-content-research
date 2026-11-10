# 表2｜T1–T6 的输入、输出与 Ground Truth

| 任务 | X 与先验 | Y | G：标注对象/主体 | E：指标与限制 | 代表 |
|---|---|---|---|---|---|
| T1 表达识别 | 文本/图文及现象定义 | 是否出现、类别或片段 | 人审现象标签 | 分类 F1；不能证明意义恢复 | [@wan-etal-2026-newspaper; @zheng-etal-2025-enhancing] |
| T2 意义理解 | 语境、候选义/源目标 | 候选解释、蕴含或释义 | 人审/构造的可接受意义 | 选择准确率/解释质量；不等于心理意图 | [@spinoso-di-piano-etal-2025-rsa; @saakyan-etal-2025-understanding] |
| T3 语用功能 | 会话/视觉场景及候选行动 | 间接行动、立场、受众 | 人类共识或构造行动 | MCQ/人审；候选空间有上限 | [@arai-ren-2026-drinq; @Nam_2025_ICCV] |
| T4 有害判断 | 内容、目标、社会语境、政策 | 风险类别/程度 | 规范性人审/政策标签 | 双侧错误；多数票保留分歧 | [@hartvigsen-etal-2022-toxigen; @rizvi-etal-2025-autalic] |
| T5 联合模态风险 | 图/文/情境；须说明单模态条件 | 联合输入风险 | 联合 GT；必要性另需配对人审 | 分类 F1/三条件对照；S-S-U仅窄子集 | [@palaskar2026vlsu; @zhang-etal-2026-crossguard] |
| T6 安全回应 | 输入与行为政策 | 拒答、警告、正常帮助等 | 行为评审与安全/帮助性判定 | 误拒/危险回应；不能替代 T4/T5 | [@li2025oversensitive; @zhou2026meerkatvl] |

**表注。** Task=(X,Y,G,E) 是本文记录单项实验协议的记号；不同任务的 Accuracy、F1、ASR 或拒答率不可横向排名。
