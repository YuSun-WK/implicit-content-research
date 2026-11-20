# TRACE-S1D｜立即提速：多数类坍缩根因审计、MultiOFF 论文对齐及完整 TRACE 阻塞突破

> **本任务直接执行，不要重新开始 Stage 0–S1C。** AAAI 2026 TRACE 复现，目标是尽快取得可信的论文对齐结果，而不是重复报告数据缺失或制造指标。

## 一、仓库与现有真实证据

仓库 `YuSun-WK/implicit-content-research`，分支 `repro/trace-aaai2026-20261119`，审计起点 HEAD `6d7aa0ea3e32fd679f2f51ee39173c0e7432edeb`。开始先 `git fetch`、确认真实HEAD与工作树，无冲突再继续；不得 force-push/main merge。工作目录 `06_experiments/repro_trace/`，所有真实数据、checkpoint、预测明细保留本地忽略目录或仓库外。

必要阅读：
1. `Stage1C_Accelerated_Executive_Summary.md`
2. `Stage1C_MultiOFF_Training_Report.md`
3. `Stage1C_MultiOFF_Paper_Code_Alignment.md`
4. `Stage1C_MultiOFF_Data_Audit.md`
5. `Stage1C_CUDA_Architecture_Selftest.md`
6. `multioff_baseline.py`, `test_multioff_baseline.py`, `stage1c_multioff_formal.jsonl`
7. `/tmp/trace-s0-reference/MultiOFF/multioff_proj_ft.py`（作者固定提交 `83ecb799f897fe275185e082ee9a669f7d04bfaa`）

已知且不得篡改的事实：
- P1真实CUDA架构自检已过，9次AdamW（含恢复重放），合成输入只能用于计算路径验证，不能算真实性能。
- 作者公开MultiOFF原始CSV Train/Val/Test各445/149/149；原始作者发布图片未找到各1张（均是 offensive），目前完整样本政策为444/148/148，必须保留子集/全量区别。
- MultiOFF `adapted_author_baseline` 已在真数据完成7 Epoch、Dev选Epoch2、仅一次Test评估：Train 0.5811/0.3675/AUROC0.5575；Dev0.6149/0.3808/AUROC0.5517；Test0.6149/0.3808/AUROC0.5361。
- Epoch1 Dev Acc0.3851/F1 0.2780，恰等于全预测 offensive；Epoch2–7 Dev Acc0.6149/F1 0.3808，恰等于全预测 non-offensive。需要**通过预测计数证实**，不要先断言根因。
- 目前严格完整 TRACE 仍缺作者 InternVL/Gemini Caption，FHM 数据仍未取得；不可将原始文本诊断当完整TRACE。
- 预训练HF CLIP ViT-L/14 revision `32bd64288804d66eefd0ccbe215aa642df71cc41` 已经8/8 sha通过，尽量复用，不得重新下载。

## 二、执行策略和硬门禁（加速优先级）

### P0｜20分钟内完成现有Checkpoint的非训练型坍缩审计
**不要一开始就重训**；已有最佳Epoch2模型和正式训练日志，可直接加载。

- 校验本地 `.local/s1c-multioff-formal/best-epoch-2.pt` 与checkpoint manifest的sha，严格复用同一官方图片/CSV hash、固定CLIP、模型结构与处理器。
- 只在 Train 和 Dev 上进行诊断性推理，读取 Test既有聚合历史结果即可。避免在已看过Test的情况下继续调参、反复探查 Test。
- 必须对 Train/Dev 给出 confusion matrix (TN,FP,FN,TP)、预测为 offensive 数和比例、按标签条件分组的 sigmoid(logits) 的 min/p05/p25/median/p75/p95/max、输出方差和置信度分布、PR-AUC、ROC-AUC、Macro F1、offensive-class F1、balanced accuracy、Brier score，并计算始终全负/全正的 reference 指标。报告只提交聚合统计，禁止样本级原文或私人预测。
- 根据 `stage1c_multioff_formal.jsonl` 重建每个Epoch Dev的“全正→全负”迹象。如果历史日志没有预测向量，不要伪称逐Epoch已验证：可用保存的最佳/末次checkpoint验证对应两个阶段，其他阶段标注缺乏模型文件。
- **阈值仅在Dev上探索**：固定0.5与Dev F1最优、Youden、PR曲线候选比较；明确这只是校准诊断，不是新的训练贡献。不能因为阈值调节使指标提高就声称模型学到了强分类能力；AUROC低时要直说。
- 检查 `multioff_baseline.py` 的 image/text token/collate/label、损失目标和小批梯度累积，确认与作者实现的数学关系；分别核查训练模型 Eval和冻结主干，避免类别值映射反向、图像路径错配、全0文本或 Train/Dev交叉污染。
- 检查现有CNN/Zeroshot-CLIP冻结特征对照是否只用Train/Dev判别；不假装有新的论文Benchmark结果。

**P0 交付**：`Stage1D_Collapse_Root_Cause_Audit.md`、只含聚合数值 `stage1d_dev_score_distribution.json`。结论标注 CONFIRMED/LIKELY/UNRESOLVED，不能在证据不足时把“少数类低召回”硬写成根因。

### P1｜立即进行“作者协议对齐”而非盲目增加Epoch
参考固定作者源码 `MultiOFF/multioff_proj_ft.py` 的 `CLIPClassifier`、`FocalLoss`、`train_model`、`wise_ft`、`evaluate_model`。重点：
- ViT-L/14原始sentence +图像，冻结backbone，作者 projection结构/3个focal loss；seed42、batch512、AdamW lr1e-4 weight_decay1e-4、ReduceLROnPlateau、patience5、最大20epochs。
- 本地BF16及microbatch16的grad accumulation近似作者物理512的整体batch，不能偷换成“逐microbatch更新”，必须明确数值差异；已有训练只7个optimizer更新，每Epoch更新1次。
- 作者原实现有WiSE-FT在Dev搜索alpha ∈ [0,0.1,...,1]。现有脚本**省略了WiSE-FT**。实现可独立复用的作者 `wise_ft` 结构及Dev评估，不修改作者源码；冻结权重可共用，只需插值可训练参数。**仔细核查作者代码的所谓zeroshot_model是否与原训练模型是同一对象并被in-place修改**，如果是，作者实际WiSE-FT混合可能并非“初始随机头 ↔ 最优头”，必须区分`literal_author_execution`与语义上正确的`init_vs_best`。不能无声明“修正”作者机制。
- 先基于已有Epoch2 best与Epoch7 final，在Dev比较**按作者源码实际对象状态**的WiSE插值是否可重现；如缺初始权重快照，不能伪造真正zeroshot权重，用新的seed重跑并保存初始化、每Epoch和best快照。
- 补充**真正的 author-aligned baseline** 训练入口，要求允许 `--seed`、`--mode author_literal|adapted`（语义严格定义），所有checkpoint签名包含模式/seed/数据hash/CLIP revision/split/超参/阈值。每次实验输出独立目录。
- 给出对齐表：官方源码/论文设置 vs Stage1C vs Stage1D，包括样本数差3、同一split标签差异、精度BF16、batch累积、采样次序、WiSE、Dev模型选择、DataLoader丢图行为、Test评估、指标定义、epoch/optimizer更新数。
- 严禁为了提升分数直接改变焦点损失、数据划分、backbone或冻结层数；那些只能另设非论文对齐的诊断实验，不能混到 author_literal。

### P2｜3个种子的快速正式复现（只用Train+Dev选择，不反复碰Test）
单卡GPU共享，单次≤6h，显存目标≤18GiB。已有一次完整训练实测182.77秒，复用权重、数据和环境，不要重建或重下载。
- 优先种子 42（已存在Stage1C，可用作adapted参照但不能冒充新协议完成），以及121、3407；先明确实验模式和作者参数。至少**两个全新种子**完整运行20epochs上限+patience5，并记录有多少实际optimizer updates。
- CPU一致性/输入检查通过后直接开始，以实际step时延/显存和用户实验预算为门禁，不要因为微小文件缺口无限等待。
- 每Epoch记录 Train loss、Dev confusion、macro F1、positive-class F1、AUROC、positive prediction count、概率分布；保存前3次score drift有必要检查；记录best model和last model以及init模型的哈希。
- Dev选最佳Epoch，若有author literal WiSE，则只用Dev选择alpha。阈值政策预先明确为固定0.5，单独的Dev calibration只作为敏感性分析，不用Test寻优。
- 对每个新种子只计算Train/Dev。**原Test已在上一轮看过**；本轮不可做网格搜索然后反复报Test。若要最终论文对齐Test结果，必须先锁定唯一的预注册配置/seed/alpha/threshold，再执行一次Test评估，且明确报告此前已经看过Test聚合结果、严格意义上非首次盲测。
- 如果连续多个seed Dev预测全部同一类，指标等于多数类、AUC约0.5，则记录为`BASELINE_COLLAPSE_CONFIRMED`；禁止无穷试随机seed/阈值直到看见漂亮数字。可保留明确的`diagnostic_nonpaper`单次loss/batch-size机制自检，但不混入复现结果。
- 仅剩三张原作者发布缺图，允许运行明确的complete-case补充复现，不得为找图拖延整轮。用最多一次有界的官方来源查找，无法核实就报告缺图及数据差异，不要填充、换图或重下载未知镜像。
- 对比论文 TRACE Table6 的“ViT-L/14 projection FT” Acc0.604 F10.377 仅作弱数值参照：如果结果来自全负类常量预测且非全量数据、无同样WiSE-FT，不可称正式再现Table6。

**P2 交付**：`Stage1D_Protocol_Parity_Matrix.md`、`Stage1D_Seed_Replication_Report.md`、实际本地运行日志与只含聚合表格的Git存档、可恢复签名checkpoint（本地不提交）。

### P3｜打开完整TRACE的方法路径：与其他步骤并行，限时做来源核查
- 检查官方 TRACE 仓库的 README、提交与公开 Releases，原作者的公开补充材料，以及可公开合法下载的原始Caption索引；只查一轮不重复穷举。
- 针对 **FHM** 与 **MultiOFF**，分别列出需要作者提供的样本对齐键（ID/image/split）、`ivl_8b_new_caption`、`gemini_caption`、Caption模型/生成参数、论文训练的checkpoint revision、Table6 ViT-L projection FT的WiSE和score协议。为用户准备**可直接发送给作者的英文短邮件草稿**，不主动发邮件。
- 不得用随机、Gemini付费API、其他模型生成的Caption冒充原始增强Caption。缺原始数据时只输出`STRICT_TRACE_BLOCKED_CAPTION`，但**不得以它为理由阻断P0/P1/P2**。
- FHM仅检查一次 `~/data/trace-assets/fhm/` 或用户明确告知的位置；缺授权数据就指出由本人完成DrivenData许可与下载，不反复扫描目录，绝不通过不明镜像取代。
- 如果官方Caption和FHM授权数据已实际到位，立即按已有门禁执行其真实GPU Smoke+至多100 Batch，并在剩余单次预算内安排符合论文的下一次正式运行。否则不要空跑。

## 三、交付规则及速度要求
- 本轮最小成功标准：**P0模型预测坍缩审计 + P1协议差异表 + P2至少2个新seed的真实Train/Dev正式实验**。P3有明确可执行作者材料请求。
- 阻塞不得整轮停止：某条数据不可用，独立推进其它条。
- 能复用 `/tmp/trace-s0-py310`、已验证的 CLIP cache、`~/data/trace-assets/multioff/`、`.local/s1c-multioff-formal/` 等已有文件则直接复用。
- 实验以数据、代码、日志为准：不能根据概率或预测补写未经运行的 Test 分数。不得上传原始图像、行级样本、Meme原文、Caption、token、完整预测、pretrained模型或checkpoint到GitHub。
- 只改 `06_experiments/repro_trace/**` 和局部.gitignore；CI/单测、diff、数据脱敏检查后提交当前分支，禁止force push、merge main。
- 报告包括时间、GPU、命令、实测峰值显存、Epoch、update计数、Dev正负类预测数、Macro F1/AUROC/混淆矩阵、协议偏差和受限因素。
- 如发生异常，保留有用错误日志与原证据，继续其他可独立任务，不得编造成功。

## 四、最终中文输出（必须据实）
1. **是否确定坍缩？** Train/Dev 预测正类数、混淆矩阵、各类分数分布，AUROC是否真的弱；主要原因是否可证据支持。
2. **正式对齐程度**：相对作者源码的表格；WiSE-FT究竟实际如何执行、是否只是混合两个已训练checkpoint。
3. **新seed实测结果**：各自最佳Dev Macro F1、AUROC、positive recall、预测正类数量和epochs；是否达到nontrivial双类别识别。
4. **任何Test结果**：有没有重新使用Test？若使用，是否预先锁定协议且诚实披露已接触Test。
5. 完整TRACE Caption、FHM授权数据和作者材料的具体阻塞；给用户可发送的作者英文邮件草稿。
6. 每个真实实验的命令、日志、Checkpoint hash（仅摘要）、总耗时/峰值显存、实际optimizer更新数。
7. 当前commit SHA、GitHub交付文件链接、下一阶段GO/NO-GO建议；绝不简单写“完成实验”而不说明预测坍缩。
