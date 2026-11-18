# VLSU 图文联合安全分类研究决策

**2026-11-18｜CONDITIONAL GO，仅批准进入数据与低成本验证阶段。原 CRTL 三模块直接立项 NO-GO。**

1. **优先问题**。在固定安全规范下，能否从图像和文本**独立复用、组合均有可信标签**的对照中，学到让联合等级随图文关系正确变化的评分，并迁移到未见组合？
2. **选择理由**。相比辅助任务、动态路由和风险残差，配对图上的闭环对照有一个明确可证伪的性质：任意图像单独效应和文本单独效应都在同一个对照中抵消。能直接测量数据是否提供这种监督，也能在同骨干、同样本、同预算下检验它是否产生独立收益。
3. **候选技术贡献**。用稀疏二部配对图的加权环空间投影，从多类标签构造训练信号。三重标签用来界定同单模态等级的支持域并训练单模态头。对森林、孤立边和不可信组合，交互目标自动失去监督或显式关闭。图投影与双重差分都有先例，贡献需要体现为可信对照上的分类收益和跨组合泛化。
4. **最接近的工作**。**Can the Parts Fool the Test?（NeurIPS 2026 官方录用名单）已提出二部配对闭环、严格抵消、CycleAcc 和 Cycle OE 训练**。CMIE 已把双差用于安全遗忘，MemePIVOT 已用于反事实线索监督，FBHM 已做析因构造和低样本调节，EMAP 与 Wörtwein 等已分别测量和学习非加性。HoliSafe 已使用五种二元图文安全组合训练。 [Cycle OE 论文](https://arxiv.org/html/2610.23248) · [NeurIPS 名单](https://neurips.cc/Downloads/2026) · [CMIE](https://aclanthology.org/2026.emnlp-main.2220/) · [MemePIVOT](https://aclanthology.org/2026.findings-emnlp.1329/) · [FBHM](https://aclanthology.org/2026.emnlp-main.1596/) · [EMAP](https://aclanthology.org/2020.emnlp-main.62/) · [Beyond Additive Fusion](https://aclanthology.org/2022.findings-emnlp.344/) · [HoliSafe](https://youngwanlee.github.io/holisafe/)
5. **可检验的区别**。Cycle OE 针对图文匹配/不匹配的两正两负完整矩形。候选只保留**多类安全等级、真实稀疏观测图与重叠环加权**的差异，并复用二部图的已有不变性。CMIE 则针对生成模型激活的定位和擦除。若同数据的 Cycle OE 多类适配、逐边 CE 或等价投影解释全部收益，停止该方法路线。
6. **最大风险已出现**。VLSU 正式论文给出 8,187 条、17 模式；公开 CSV 实得 **8,159 条、25 个原始标签三元组**，去掉 141 个图像不确定样本剩 **19 个标准三元组**。S-S-U 实得 **35** 条。以原 URL 和规范化全文为节点，精确身份二部图 **环秩为 0**。当前 VLSU 无法单独训练或评价该闭环机制。复算项目 TriggerBench 全量清单，Train 与 Test 的精确路径图也都无环；单边反事实配对可以服务备选。来自其他数据的二元配对也无法验证多类 Borderline 主张。 [正式论文](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf) · [固定 CSV](https://github.com/apple-aiml-research/ml-vlsu/blob/cbe363a26d2129ff1b526c283af0a2b7aa3d9b28/data/VLSU.csv)
7. **现在只优先做一个实验**。CPU 配对支持审计。用合法可取得的 Hateful Memes、MemeCF、FBHM 或 HoliSafe 的逐例标签清单，按原图内容身份和规范化文字建图，计算环秩、独立组数和非零标签对比，检查同一安全政策及划分。二分类材料先检验机制，多类材料决定能否继续以 S/B/U 为主论文。数据门通过后，才运行冻结编码器的等预算对照。以 Cycle OE、逐边 CE、常规 MTL 为主要否证对象。见[执行协议](07_Experimental_Roadmap_and_Kill_Tests.md)。
8. **投入决定**。投入一次有界查验。主方案为可信稀疏闭环上的安全分类，备选为单边配对的敏感性与稳定性学习。通用闭环训练和简单迁移到安全数据的原创性均为 NO-GO。当前证据支持**研究问题和数据门**，尚不足以认定已找到 CCF-A 方法突破。

本轮完成了版本与证据核验、CSV 全量统计、分层小样本图片解码和理论设计。模型训练、完整图片清点、外部数据逐例闭环清点、人审及迁移结果均待开展。资料以项目已公开的 H1 结果及作者原始来源为依据。方案中的阈值是本项目的投入规则。

## 交付目录

| 文档 | 决策用途 |
|---|---|
| [01 当前研究审计](01_Current_Research_Audit.md) | 官方协议、实际字段、图结构、已有 H1 与复现边界 |
| [02 文献与技术迁移矩阵](02_Literature_and_Transfer_Matrix.md) | 发表状态、竞争方法、十五类迁移技术 |
| [03 研究缺口与创新判断](03_Research_Gap_and_Novelty.md) | 原方案反例、近期查重、三位模拟审稿结论 |
| [04 候选方向与选择](04_Candidate_Ideas_and_Selection.md) | 三条路线的公式、资源、失败模式 |
| [05 推荐方法](05_Recommended_Method_Design.md) | 数据支持、环空间目标、证明、训练与推理 |
| [06 论文蓝图](06_CCF_A_Paper_Blueprint.md) | 英文标题、引言、贡献、四图五表与投稿叙事 |
| [07 实验执行规划](07_Experimental_Roadmap_and_Kill_Tests.md) | 分阶段数据门、低成本对照、完整实验和迁移 |
