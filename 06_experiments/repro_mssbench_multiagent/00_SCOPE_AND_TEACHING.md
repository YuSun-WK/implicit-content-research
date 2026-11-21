# MSSBench｜Multi-Agent 忠实复现：范围与教学

2026-11-19，Stage 0（仅 CPU/代码与数据检查；未运行 GPU）。
正式论文：[ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html)。
论文PDF：[OpenReview](https://openreview.net/pdf?id=I9bEi6LNgt)。
官方仓库：[UCSB-AI/MSSBench](https://github.com/UCSB-AI/MSSBench)，本轮审计 HEAD 1602193f49cb6925bfa3751be157d0bbf5439779。
已有证据：[B4a MSSBench](../../03_survey/R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md)；[B4a 综合](../../03_survey/R2_synthesis/B4a_Cross_Paper_Synthesis.md)。

## 首先理解

Agent = 持有角色 Prompt 和输入/输出契约的一次模型工作单元；Pipeline = 按顺序调用这些工作单元；Prompt Routing = 根据某步输出选下一步 Prompt；Orchestration = 管理调用、状态、失败恢复、日志。四个 Agent 可以共享一份加载的 VLM 权重；不需要训练，也不需要 LangChain/AutoGen。

本科生教学例子（人为构造，非数据实测）：问题「如何提高棒球挥棒准确性？」；安全图片=宽敞训练场，不安全图片=狭窄办公室且附近有电脑。Intent 输出「练习挥棒」；Visual 输出「办公室中有显示器、桌椅，空间狭小」；Safety 基于意图+图片+caption 判「Answer: No」（Chat 中 No=不安全）；QA 采用提醒风险的 Prompt，而不是提供立即在办公室挥棒的步骤。安全图应触发普通回答。两张图使用同一问题才是关键实验。

## 论文原始方法（不要和当前公开代码混淆）

Chat 开放 VLM：四代理
- Intent Reasoning：输入 query；输出 Potential intent activity。
- Visual Understanding：输入 image；按附录提示「Describe the image in one long sentence.」输出 caption。
- Safety Judgment：输入 inferred intent + image + caption；输出 Reasoning / Answer: Yes 或 No（Yes=活动安全）。
- QA：输入 query、image、安全判断（及适当评判信息）；Yes 走普通问答 Prompt，No 走风险提醒 Prompt，解析失败要记录。
原论文对闭源较强模型用三代理（去 Visual），本实验不调用闭源API。

Embodied：**两代理，不是上述四代理**。Key Object Locator 输入指令和图片，识别需重点关注的物体/环境状态；Safety Reasoning 输入指令、图片及该环境状态，同时做风险判断和动作计划/风险警示。Embodied 的 Unsafe hint: Yes 表示有危险，与 Chat 的 Answer: Yes 方向不同。

论文 1-step CoT 是一次调用完成意图、安全和答复；不是四次调用的平均。所有 Agent 使用同一模型实例、同一解码配置（兼容性需要例外时报告）。

## 四档复现声明

A 论文设计；B 作者公开代码原样行为；C 修复必然程序错误后遵循 A 的信息流；D 因本地模型、量化、Judge、样本范围等产生的改编。不得将 C 或 D 写成「官方仓库原样运行」；不得将 D 的本地 Judge 数字称作论文官方成绩。

## 论文实验矩阵

- Benchmark：Chat vs Embodied、Safe vs Unsafe。正式版 1960 个 image-query inputs = Chat 1200 + Embodied 760，Safe 980 + Unsafe 980。注意 input 数不等于 JSON 记录数、独立图片数或 pair 数。
- 诊断：IF 直接回答；QC 判断 query 对当前环境是否安全；IC 输入意图/活动而非原问句；IC+Self Caption 先让 VLM 自描图再判断；IC+GT Caption 输入额外的人工环境描述，属 oracle 优势。
- 主实验：Base、1-step CoT、Multi-Agent，均应分 Chat Safe/Unsafe 与 Embodied Safe/Unsafe。
- 补充诊断（非论文原消融）：-Intent、-Visual、-explicit Safety step、等调用数 Self-Refine；需要独立附表。
- 论文 Fig 7 中 LLaVA 1.6 Chat Base / 1-step CoT / Multi-Agent = 53.2 / 64.8 / 71.0（图中Base与论文 Table 2 存在模型行对应疑点；重跑时先核对原图）；Embodied 51.1 / 57.0 / 57.9 同样需先核对基线。不得以这些数字作为本地替代 Judge 的直接复现目标。

## 必须保留的错误分析

Intent -> Caption -> Safety -> QA 的每条原始 prompt、原始输出、解析标签、父调用ID、图像hash、耗时、token、GPU peak、失败码。通过同 query safe/unsafe 成对评估与人工核验检查漏检/误报/过拒，切勿把拒答当成视觉理解成功。