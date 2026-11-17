# H1-K2 独立科研审计

**裁决：PIVOT。** 保留图文风险检测，暂停将11例输出变化解释为表示衰减；下一步先做人类质量审核和任务控制。审计基准固定为[0a043abbf575d6b21f8d4095dbdfba7bad880465](https://github.com/YuSun-WK/implicit-content-research/commit/0a043abbf575d6b21f8d4095dbdfba7bad880465)，日期2026-11-17（北京时间）。无GPU训练/推理、无付费API、无原实验修改。

## 建议阅读顺序与必交十文档

1. [Executive Decision](H1_K2_Executive_Decision.md)：总裁决与唯一优先路线。
2. [Result Independent Audit](H1_K2_Result_Independent_Audit.md)：180条预测复算、协议/统计/训练隔离。
3. [Counterfactual Quality Audit](H1_K2_Counterfactual_Quality_Audit.md)：标准、原36对/探索子集、人工审核。
4. [MMAligner Deep Reading](H1_K2_MMAligner_Deep_Reading.md)：公式、实现、复现与创新冲突。
5. [Related Work Novelty Matrix](H1_K2_Related_Work_Novelty_Matrix.md)：直接方法近邻、元数据更正、未验证项。
6. [Competing Hypotheses](H1_K2_Competing_Hypotheses.md)：H-A至H-H及可区分实验。
7. [Method Candidates](H1_K2_Method_Candidates.md)：三条草图、成本、反例与否决条件。
8. [CCF-A Reviewer Verdict](H1_K2_CCF_A_Reviewer_Verdict.md)：两种模拟审稿视角。
9. [Kill Test Roadmap](H1_K2_Kill_Test_Roadmap.md)：分阶段预注册、门槛和下一轮工程任务。
10. [Paper Blueprint](H1_K2_Paper_Blueprint.md)：两条不同假设的论文故事与必要实验体系。

另附[36对逐对明细及21个错误侧别](H1_K2_Counterfactual_36_Detail.md)、[全字段CSV](H1_K2_Counterfactual_36.csv)。CSV等级为助手非盲研究筛查，不是独立人类裁决；未修改原Safe/Unsafe标签。A6/B12/C18不能用于替换原正式36对分数。

## 本轮实做与未做

| 项目 | 状态 |
|---|---|
| 指定K1报告、原预测、metrics、manifest、metadata、审核JSON与8脚本 | 已读取并交叉核验 |
| 72张图 | 固定revision重新取得、SHA25672/72、解码与全对视觉筛查 |
| 原始36份Train/Test CSV | 重新下载并逐行解析，共5600行；选中72条源侧记录匹配 |
| 180条预测/关键指标/Wilson/pair bootstrap | 独立复算通过 |
| 历史K0/recovery/model-access/network/resume | 已区分工程与模型运行，未将旧NOT_RUN覆盖 |
| 项目已有文献/综合 | 重点P034/P037–P041及02_synthesis/R1–R5；指定03_survey路径不存在 |
| MMAligner正文/附录/9代码文件与4个split JSON | 本轮已读，静态核查及split独立核算；未运行模型 |
| 最新相关文献 | 原始发表页/重点章节横向核验；未全部完整复现或全文精读，矩阵逐项标明 |
| 独立人类盲审、QB、同任务Prompt实验 | 未执行 |
| 训练近重复/实际训练样本清单、当前服务器权重重hash | 未执行 |
| GPU、LoRA、隐藏状态干预、MMAligner全套 | 未执行 |
| CCF2026官网目录与部分最终出版全文 | 获取受限，未闭合；不把作者稿状态冒充最终逐页核验 |

## 复算与来源

运行`python 03_experiments/h1_k2_research_audit/scripts/recompute_audit.py --repo .`。只读原始K1文件、CPU计算并在终端打印，不覆盖原始指标；`--write`仅允许写入K2证据目录。原图和原始CSV的来源/字节摘要分别见[evidence/image_verification.json](evidence/image_verification.json)、[evidence/csv_source_verification.json](evidence/csv_source_verification.json)，本分支不重新分发图像或论文全文。

其余证据：[复算](evidence/independent_recalculation.json)、[源文件hash](evidence/source_sha256.json)、[额外完整性检查](evidence/additional_integrity_checks.json)、[质量汇总](evidence/quality_summary.json)、[MMAligner源码blob](evidence/mmaligner_sources.json)。源文件hash以原始Git blob为准，避免Windows换行转换产生假变化。

人类需要决定风险政策和争议标签，Codex负责匿名材料/计算/执行，Work可继续文献审计与机制设计。不能由助手模拟“第二名人类审核者”来通过门槛。
