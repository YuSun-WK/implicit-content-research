# 表5｜多模态非字面理解：原始输入、辅助监督与可证机制

| 论文 | X_raw、Y与模态 | 训练/测试额外信息（注意区分） | 人审GT、正面结果与尚不可归因之处 |
|---|---|---|---|
| MultiMM [@yang-etal-2025-cultural] | 广告**图文**；隐喻/情绪等 | 作者使用情绪/源目标属性辅助；**所审作者公开代码已固定**[MultiMM@33a01f data_utils.py L67–100](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L67-L100)：train/val/test读取CSV情绪提示（S）；但**情绪字段gold来源/正式论文主表run对应O**，不得直接归责正式实验 | 作者报告隐喻预测提升；同预算“模型预测情绪 vs gold情绪”仍待核 |
| V-FLUTE [@saakyan-etal-2025-understanding] | **图文**；视觉蕴含类别和自然语言解释 | 训练白图模型属输入对照，非等信息的语义单因素干预 | 作者有图F1@0 72.78 vs白图64.77（特定设定）；白图残余表现与来源类别先验说明不能认定视觉因果必要；解释F1阈值不等于忠实性 |
| M3UCD [@zheng2026m3ucd] | **图文**；隐喻、源/目标、意图等 | OCR/多任务属性监督；共享LoRA | 作者报告15,345图文例、Complementary 58.36%**是现象人工贡献类别**，不是同模型去图因果证据；个别任务有负迁移 |
| MGMCF [@zheng2025multigranular] | **图文**；隐喻/情绪/意图/冒犯分类 | 论文定义源/目标概念辅助文本，[MGMCF@02407e loaddata.py L70–109](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L70-L109)已固定预计算source/target字段的公开输入路径（S）；pkl为gold/预测/外部来源及正式run映射仍O | 作者报告对象、全局-局部与双语义模块的结构消融；同信息预算和源码损失对齐仍O |
| **DOSE** [@guo-etal-2026-two] | **新闻图像＋文章文本**；多目标反讽MCQ | 任务提示、共享/私有LoRA专家与投影正交；官方五类主要任务，所审代码有第六种变体 | 作者1%数据预算下五任务均值78.90 vs同底座LoRA77.70（作者协议）；“文本主导61.9%/等贡献22.5%/图像主导15.6%”是标注解释类别，不是因果去模态 |
| MCIB [@wang2026conditional] | **文本＋音频＋视频**；反讽二分类 | MUStARD++R标签协议、三配对条件瓶颈/KL与条件预测辅助训练 | 作者weighted-F1 75.64；去细粒度71.19、Transformer→MLP74.32为结构对照，不是独立“no KL/no conditional”证明；作者公开[MCIB@d1430a MCIB_trans.py L110–126](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L110-L126)与[194–224](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L194-L224)**已固定静态路径（S）**；若真实batch为[B,1]/[B]可广播，**真实shape和正式训练run对应O** |
| MMSD3.0 [@Zhao_2026_CVPR] | **多图＋文本**；反讽 | 正式CVPR2026 Main（CCF-A）论文有CIRM关系推理 | **截至当前只核正式出版页/摘要**，可确认基准和方法存在，未据全文表格宣称模块独立收益或严格多图因果依赖 |

**表注。** `人审模态贡献归属`≠`同模型text-only/image-only/joint的预测变化`≠`人工复标单因素反事实`；这三类证据不可互换。比较前必须给`X_raw/X_train_aux/X_test_gold_or_predicted`，**MultiMM/MGMCF/MCIB的静态源码版本已固定**，未知的是正式run与字段/张量真实来源；已固定S仍不构成作者正式实验错误或学术不端结论。六组可外部访问固定来源另见正文§8.6。
