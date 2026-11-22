# Codex 执行任务｜TRACE MultiOFF：排除5条无效 Caption，多卡并行完成正式训练与测试

## 0. 当前目标与用户最新决定

用户明确决定：
- 不再花时间修复剩余5条不合格 Caption；
- 这5条样本直接从本轮有效数据中排除；
- 只做 MultiOFF；
- 不使用 Gemini，不做 FHM；
- 尽快完成正式训练和测试；
- 检查有多少真正空闲的 RTX 4090/4090D，并尽可能并行使用空闲 GPU。

本任务必须从当前 Git 分支开始，不要重新生成 Caption。

仓库：`YuSun-WK/implicit-content-research`
分支：`repro/trace-aaai2026-20261119`
当前已知 HEAD：`7470be2586ddf70f50342d0e001c32d3cc12777e`
上游 TRACE commit：`83ecb799f897fe275185e082ee9a669f7d04bfaa`

## 1. 先读取证据和本地数据

先检查当前分支、HEAD、工作区状态和 GPU 状态。若 HEAD 已变化，先保留新提交，不得 reset 或覆盖。

必须阅读：
- `Stage2_1_Caption_Repair_Audit.json`
- `Stage2_1_Caption_Repair_Report.md`
- `Stage2_2_Reviewer_Gate.md`
- `Stage2_2_Repaired_Training_Config.yaml`
- `stage2_train.py`
- `stage2_caption.py`
- `Stage2_Complete_TRACE_Training_Report.md`

私有数据路径以本机实际核验为准，历史默认：
- MultiOFF 数据：`$HOME/data/trace-assets/multioff`
- 修复版 Caption Manifest：`$HOME/data/trace-assets/multioff/trace_internvl_only_repaired_v2/records.json`
- 模型资产：`$HOME/data/trace-assets/stage2-models`
- Python：`/tmp/trace-s0-py310/bin/python`
- 上游代码：`/tmp/trace-s0-reference`

检查 Manifest SHA-256，预期值：
`2f6d7c3fb2627f8c81e47794dd16c34763fc8bee5febc4d6536afc6e97bd1007`

如果本地 SHA 不一致，不要猜测或覆盖；先报告实际 SHA 和来源。

## 2. Caption 处理：只排除5条，不再修复

Stage 2.1 审计中已记录5条失败 stable keys：
- `1b757ee63f045fc7a1ed61f683581692580cd6152df82456a870b3368e333bcc`（Train，原 Caption 93 tokens，3次输出均80 tokens）
- `86a2f806f38f018422ace0dc8d7ae021ead001e403c49111dc574dc2b1641923`（Train，关键词规则拒绝）
- `8cab3ea4285074ce8a4c7339caa3b2c59fd87be5eee24d3246bdec740b28a842`（Train，关键词规则拒绝）
- `9dc1a2ed13abb17838a797f7e4cc0131033851ced7aaadba764ba01e69860045`（Train，关键词规则拒绝）
- `a2da3419fcb7b6195e826a2d79708bca855db1a1a892ad824619e94ef190180f`（Dev，关键词规则拒绝）

以上5条仅根据 Caption 质量/生成验收失败排除，不得读取其标签来决定排除。不得再调用 InternVL、RAM++ 或 GroundingDINO。

保留其余735条：
- Train：440
- Dev：147
- Test：148
- Total：735

Test 148条全部保留，不能排除任何 Test 样本。

### 2.1 实现要求

当前 `stage2_train.py` 的 `load_rows()` 和 `validate_caption_lengths()` 仍硬编码740条及444/148/148，必须增加显式 exclusion 支持。建议新增一个只含上述5个 SHA stable keys 的文件：
`Stage2_2_Excluded_Caption_Keys.json`

要求：
1. 从官方 MultiOFF 原始记录读取740条，确认原始 stable keys 与 Caption Manifest 完全一一对应。
2. exclusion 文件必须与 Stage 2.1 Audit 的 `failed_keys` 完全一致；不能多排、少排或自行追加。
3. 验证5条分布严格为 Train 4、Dev 1、Test 0。
4. 对剩余735条检查 Caption 非空、非原始文本复制、图像 SHA / row_number / image_name / split 对齐。
5. 只对保留的735条执行 OpenCLIP 原始 Tokenizer 的无截断长度检查；必须全部 <=77 tokens。
6. 被排除的5条记录保留在原 Manifest 和审计中，不得删除或覆盖。
7. 输出有效样本清单及 SHA；记录有效数据 split 数量和每类标签计数（只记录汇总，不公开原始数据）。
8. 不因关键词字符串单独拒绝原本合格的406条；本轮以用户决定的5条 exclusion key 清单为准，不再新增关键词过滤。
9. 不修改 Caption 文本，不重新生成任何 Caption。
10. Test 保持原148条，测试指标明确说明这是完整 Test split；Train/Dev 因5条 Caption 质量排除变为440/147。

新增/更新代码需有 CPU 单元测试，验证：
- 5个且仅5个指定 keys 被排除；
- split counts = 440/147/148；
- Test 0 exclusions；
- 保留735条均 <=77；
- 如果 exclusion key 缺失、多出、或 split 不符合预期，硬失败；
- 原 Manifest SHA 不变。

## 3. 训练代码适配

只允许做支持 exclusion 和多卡独立任务调度所必需的最小改动，不改变 TRACE 模型、损失、优化器或超参数。

至少修复以下硬编码：
- `load_rows()` 的740条精确集合检查：先验证原始740 key，再按5 key exclusion 过滤，返回735条。
- split counts 检查改为440/147/148。
- `validate_caption_lengths()` 动态统计保留数据，检查735条。
- `per_epoch = ceil(444 / microbatch)` 改为 `ceil(len(rows["train"]) / microbatch)`。
- 训练与评估的样本数、进度、日志均使用动态 split 数。
- checkpoint signature 必须包含 exclusion manifest SHA、Caption manifest SHA、split counts、seed、microbatch、accumulation 和模型 SHA。
- Test 仍在所有种子训练完成后才评估。
- Test 阈值固定0.5；不允许使用 Test 标签选阈值。
- 保留 Dev Macro-F1 选 checkpoint 和 patience=5。
- 正式训练每个 Epoch 结束保存并回读 Checkpoint。
- 不改变 Focal Loss、三个 Loss 权重、模型结构或学习率。
- 不得继承旧 Caption 版本的 checkpoint。

当前训练配置保持：
- Backbone：OpenCLIP RoBERTa ViT-B/32，固定 revision `e22e1c12b0a1ba4af9fb6474626585351ea0da25`
- 两候选：原始 Meme 文本 + InternVL2.5-8B Caption
- Loss：`L = L_cls + 0.3 L_contrastive + 0.7 L_relevance`
- BF16
- Microbatch 32
- Gradient Accumulation 4
- AdamW，LR 1e-4，weight decay 0.01
- Gradient clipping 2.0
- 最多20 Epoch
- Dev Macro-F1 选模，patience 5
- 固定 threshold 0.5
- 每个单 GPU 任务不得超过5小时59分钟
- 显存软上限18 GiB

协议名称：
`TRACE-InternVL-only-MultiOFF-2caption-Adapted-Excluded5`

## 4. 多 GPU 使用策略（必须执行）

用户要求：检查空闲卡，有多少真正空闲卡就尽可能用多少，尽快完成训练和测试。

### 4.1 发现 GPU

先运行并保存：
```bash
nvidia-smi
nvidia-smi --query-gpu=index,name,memory.total,memory.used,memory.free,utilization.gpu --format=csv,noheader,nounits
nvidia-smi --query-compute-apps=gpu_uuid,pid,process_name,used_memory --format=csv,noheader
```

不要只看 GPU utilization；还要检查显存占用和进程。严禁杀死、暂停或抢占他人的进程。

合格 GPU 条件：
- RTX 4090 或 RTX 4090D；
- 当前显存空闲至少20 GiB（如该卡总显存不足20 GiB，则不得用于本实验，因为单任务预算18 GiB且需留余量）；
- GPU utilization <=10%；
- 没有其他活跃计算任务；仅桌面/Xorg 少量显存占用可以接受；
- 确保每个任务单独使用一张物理 GPU。

将 GPU 发现结果写入 `Stage2_2_GPU_Availability.json`，记录检测时间、每张卡的型号、显存、利用率、进程及是否被选用。

### 4.2 并行运行的实验数量

为兼顾用户的“尽快完成”和统计可靠性，预先固定4个随机种子：
`[42, 121, 2026, 3407]`

其中42和121可与旧 Caption 版本同种子结果进行配对对照；2026和3407作为新增独立重复。

每个种子是一个独立单卡进程，不使用 DDP，不在同一张卡上同时运行两个训练进程：
- 有4张或更多合格空闲卡：4个种子同时运行；
- 有3张合格空闲卡：先并行3个，空出卡后运行第4个；
- 有2张合格空闲卡：两批运行，每批2个；
- 只有1张合格空闲卡：4个种子串行运行；
- 没有合格空闲卡：不启动，报告 GPU 阻塞。

**最多使用4张 GPU**，因为本轮预先固定4个独立种子；不要为了“占满卡”重复启动同一个种子，也不要运行 DDP 改变优化设置。若空闲卡超过4张，多余卡不需要占用。

每个进程使用：
`CUDA_VISIBLE_DEVICES=<physical_gpu_index>`
使进程内部只看到一张 `cuda:0`，满足当前训练脚本的单可见设备约束。

每个 seed 使用独立输出目录：
- `.local/s2-excluded5-seed42`
- `.local/s2-excluded5-seed121`
- `.local/s2-excluded5-seed2026`
- `.local/s2-excluded5-seed3407`

禁止两个进程写入同一目录。日志、checkpoint、stdout/stderr 均分开保存。运行期间定期采集 `nvidia-smi`，确保每个进程没有超过18 GiB预算。任何卡出现其他用户任务、显存不足或温度/硬件错误时，停止向该卡调度新任务，不得终止其他用户任务。

## 5. 执行顺序：尽快完成但保留最低验证

### Step A：CPU 验收

- 实现 exclusion manifest 和动态 split 适配；
- 运行所有现有 CPU 单元测试；
- 新增测试全部通过；
- 运行 lint/compile；
- 审查 Git diff，确保没有改变模型和 Loss 公式。

### Step B：单卡 Smoke

使用第一张合格 GPU，使用735条有效清单和固定 Manifest SHA：
- 单 batch forward/backward；
- 验证各模块梯度有限；
- 冻结视觉编码器没有梯度；
- 参数确实更新；
- checkpoint 保存、回读成功；
- 77-token gate 通过；
- 峰值显存 <=18 GiB。

Smoke 通过后释放该 GPU，再启动正式训练。不要为了省几分钟跳过 smoke。

### Step C：四个种子正式训练

固定种子：
`42, 121, 2026, 3407`

所有种子从同一固定预训练 Backbone 和新初始化任务头开始，禁止从旧 checkpoint 续训。

训练仅使用：
- Train 440；
- Dev 147 用于选模；
- 不读取 Test 标签参与训练/选模。

每个种子：
- 最多20 Epoch；
- patience 5；
- 保存完整事件日志；
- 每25 microbatch、每 Epoch 结束保存并回读 checkpoint；
- 记录 epoch train loss 分量、Dev Accuracy、Macro Precision/Recall/F1、Offensive F1/Recall、AUROC、混淆矩阵、正类预测率、概率分布、Caption 选择统计、梯度范数、step time、GPU allocated/reserved peak；
- 每个任务小于5h59m；
- 出错后保留日志和可恢复 checkpoint，不要静默重跑或覆盖。

### Step D：所有种子训练完成后再评估 Test

四个训练都必须有 `completed` 事件和 `best.pt`，否则不得进入最终 Test 评估。

修改 `--peer-run-dir`/评估逻辑，使每个种子的 Test 评估前，验证全部4个种子：
- 每个 seed 恰好一个 run；
- seed 集合恰好为42、121、2026、3407；
- 所有 run 的 Caption SHA、exclusion SHA、Backbone SHA、训练配置、数据 split counts 一致；
- 所有 run 已完成训练；
- 各自 best checkpoint 存在且签名匹配。

然后用各自 Dev 选出的 best checkpoint，在 Test 148 上分别评估一次，固定阈值0.5。四个 Test 评估可并行使用空闲 GPU；若 GPU 已被其他任务占用，等待或串行，不抢占。

Test 指标不得用于选择种子、Checkpoint、阈值或超参数。

## 6. 必须输出的指标与对照

每个 split 至少输出：
- Accuracy；
- Macro Precision；
- Macro Recall；
- Macro F1；
- Offensive Precision / Recall / F1；
- AUROC；
- Confusion Matrix；
- predicted positive count/ratio；
- probability min/p10/median/mean/p90/max；
- Caption candidate selected counts；
- loss components（训练）；
- best epoch。

### 对照 A：修复版新实验四种子
报告每个种子结果，以及 mean ± std。Test 指标同样汇总 mean ± std。

### 对照 B：旧 Caption 版本
只对 seed42、seed121 做同种子对照。明确这是修复 Caption 后的后续复核；旧版 Test 已经被查看，新版 Test 不是全新盲测。新旧版本差异同时包含 Caption 重写与5条样本排除，不能把性能变化单因果归结为 token 截断修复。

### 对照 C：TRACE 原论文
论文最佳配置和本地 B32、InternVL-only、排除5样本版本存在 Backbone、候选数和数据样本差异。必须标记 Adapted Reproduction，不得声称严格复现 Table 6。

## 7. 必须交付的文件

提交到 `06_experiments/repro_trace/`：
1. `Stage2_2_Excluded_Caption_Keys.json`
2. `Stage2_2_GPU_Availability.json`
3. `Stage2_2_MultiGPU_Execution_Plan.md`
4. `Stage2_2_Excluded5_Training_Config.yaml`
5. `Stage2_2_Excluded5_Training_Summary_Seed42.json`
6. `Stage2_2_Excluded5_Training_Summary_Seed121.json`
7. `Stage2_2_Excluded5_Training_Summary_Seed2026.json`
8. `Stage2_2_Excluded5_Training_Summary_Seed3407.json`
9. `Stage2_2_Excluded5_Test_Results.json`
10. `Stage2_2_Excluded5_PrePost_Comparison.md`
11. `Stage2_2_Excluded5_Author_vs_Local.md`
12. `Stage2_2_Excluded5_Training_Report.md`
13. `Stage2_2_Excluded5_Reviewer_Gate.md`
14. 更新后的代码和 CPU 测试；
15. 更新 `README.md`。

不要将原图、Caption 文本、完整私有 Manifest、模型权重或 Checkpoint 提交 Git。运行时事件日志和 checkpoint 留在 Git 忽略的 `.local/`；仓库只提交脱敏聚合指标、哈希、配置和审计报告。

## 8. 最终验收

只有以下全部满足才可报告完成：
- 5个且仅5个指定样本被排除，排除依据与标签无关；
- 保留735条，split=440/147/148；
- Test 148条完全不变；
- 所有735条 Caption <=77 OpenCLIP tokens；
- CPU 测试、单卡 smoke 通过；
- 四个预注册种子均真实训练完成；
- 所有种子都用 Dev 选模；
- 所有种子在训练结束后才评估 Test；
- Test 阈值固定0.5；
- 日志、checkpoint、指标可追溯；
- GPU 使用符合不抢占规则和18 GiB软上限；
- 不把 Adapted Reproduction 说成严格复现。

如果只有部分 GPU 可用，按实际空闲卡数调度，不得谎报“使用了全部 GPU”。如果训练失败，准确报告失败种子及是否可恢复。

## 9. Git 修改和提交

- 当前分支：`repro/trace-aaai2026-20261119`
- 不 reset、不 force push、不覆盖旧结果。
- 只提交代码、CPU 测试、排除 keys（哈希）、脱敏汇总、配置和报告。
- 检查 `.gitignore`，确认私有文件没有进入 Git。
- Commit message：
  `repro(trace): run excluded-caption MultiOFF seeds across idle GPUs`

最终回复必须包括：
1. 检测到多少张 GPU，哪些被判定为空闲，实际用了多少张；
2. 5条样本排除后的数据规模；
3. 四个种子各自的训练完成状态、最佳 Epoch、Dev 指标、Test 指标；
4. 四种子 mean±std；
5. 每个 GPU 的峰值显存与总耗时；
6. 失败或恢复情况；
7. 最新 Commit SHA；
8. 与原论文、旧 Caption 版本的差距；
9. 下一步研究建议。

**现在开始执行，不要再等待用户批准这份已明确的执行方案。不要只写计划；目标是实际完成四种子 MultiOFF 训练和测试。**
