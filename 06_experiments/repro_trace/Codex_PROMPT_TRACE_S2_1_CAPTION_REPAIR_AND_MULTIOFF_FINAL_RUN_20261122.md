# Codex Task｜TRACE Stage 2.1–2.2：修复 MultiOFF Caption，并重跑 TRACE 训练与测试

## 0. 任务目标与边界

本任务承接当前分支 `repro/trace-aaai2026-20261119` 的 Stage 2。唯一目标：

1. 修复当前 740 条 MultiOFF InternVL Caption 中超过 OpenCLIP 77-token 上限的样本；
2. 对修复后的完整 740 条 Caption 执行严格 Tokenizer 校验；
3. 使用修复后的 Caption，在 MultiOFF 上重新训练并测试当前 TRACE 二候选改编模型；
4. 形成可审计的作者结果对照、修复前后对照和组会报告。

**研究范围固定：**
- 只使用 MultiOFF，不处理 FHM；
- 不使用 Gemini Caption；
- 不调用付费 API；
- 不训练 InternVL；
- 继续使用当前固定的 InternVL2.5-8B 作为 Caption 生成/压缩模型；
- 不更换当前 Stage 2 Backbone、模型结构、损失权重或优化器；
- 当前方法名称必须写为 `TRACE-InternVL-only-MultiOFF-2caption (Adapted Reproduction)`，不得声称完整复现论文三候选设置或论文最佳 Backbone 配置。

## 1. 仓库与固定版本

仓库：`YuSun-WK/implicit-content-research`

分支：`repro/trace-aaai2026-20261119`

任务创建时 HEAD：`447bb2ae8429dacace8006b42e4d12fb2644fe46`

开始前必须：
- 检查当前分支和工作区；
- 确认当前 HEAD 是否仍为上述提交或其后继；
- 不覆盖他人新提交；若 HEAD 已变化，先 fetch/rebase 并说明；
- 上游 TRACE 固定提交：`83ecb799f897fe275185e082ee9a669f7d04bfaa)。

先阅读：
- `Stage2_InternVL_Caption_Pipeline_Audit.md`
- `Stage2_Caption_Coverage_Manifest.json`
- `Stage2_Model_Asset_Manifest.json`
- `Stage2_Training_Config.yaml`
- `Stage2_Runbook.md`
- `stage2_caption.py`
- `stage2_coverage.py`
- `stage2_train.py`
- `Stage2_Complete_TRACE_Training_Report.md`
- `Stage2_Training_Summary.json`
- `Stage2_Training_Summary_Seed121.json`

## 2. 已知本地数据与模型路径

以服务器真实路径为准，先检查存在性，不得重新下载已验证资产：

```bash
DATA="$HOME/data/trace-assets/multioff"
ASSETS="$HOME/data/trace-assets/stage2-models"
OLD_CAPTIONS="$DATA/trace_internvl_only"
NEW_CAPTIONS="$DATA/trace_internvl_only_repaired_v2"
PY="/tmp/trace-s0-py310/bin/python"
RAM_SOURCE="/tmp/trace-s2-ram-source-v2"
```

旧私有 Caption Manifest：
`$OLD_CAPTIONS/records.json`

新版本必须单独保存：
`$NEW_CAPTIONS/records.json`

**绝对禁止覆盖旧 Manifest。** 旧版本用于修复前后审计和回滚。

现有数据完整案例划分为：
- Train：444
- Dev：148
- Test：148
- Total：740

原始完整 Caption 中，334/740 超过 77 tokens，406/740 不超过 77。此前实际生成中位数约 2.86 秒/条、P95 约 4.66 秒/条。RAM++、GroundingDINO 和 InternVL 模型资产已下载并通过哈希审计。

## 3. Stage 2.1：Caption 修复

### 3.1 修复原则

只处理 OpenCLIP Tokenizer 计数 **大于77** 的 Caption。其余406条必须逐字保留，不得无故重新生成。

对334条超长 Caption，优先采用基于原图的语义压缩/重写：
- 输入原始图片；
- 输入对应 RAM++ tags 和 GroundingDINO grounding 信息；
- 输入原始 Meme 文本；
- 输入当前超长 InternVL Caption；
- 让同一固定版本 InternVL2.5-8B 将 Caption 改写为简洁、视觉扎实的单句；
- 保留最重要的视觉实体、动作、关系，以及必要的图文交互信息；
- 删除重复描述、空泛评价和不必要修饰；
- 不得输出 offensive/non-offensive 或 hateful/non-hateful 标签；
- 不得读取或使用数据集真实 label；
- 不得添加图像和文本没有支持的身份、属性、意图或事实；
- 不得直接复制原始 Meme 文本作为 Caption。

目标长度建议为 **60–65 个 OpenCLIP tokens**，硬性上限为77（计入 special tokens）。InternVL 自身 Tokenizer 长度不能替代 OpenCLIP Tokenizer 验收。

### 3.2 必须使用训练时完全相同的 Tokenizer

使用当前固定 OpenCLIP RoBERTa ViT-B/32 对应目录：

`$ASSETS/openclip_roberta/e22e1c12b0a1ba4af9fb6474626585351ea0da25`

使用 `open_clip.tokenizer.HFTokenizer`，与 `stage2_coverage.py` 一致：
- `context_length=77`
- 对 Caption 调用底层 HF tokenizer 的 `encode(caption, add_special_tokens=True)`
- 按实际返回 token 数计数；
- 不能只数空格分词、字符数或 InternVL tokens；
- 不能先截断再检查；
- 不能通过 `truncation=True` 隐藏超长问题。

### 3.3 修复脚本要求

新增独立脚本，例如：
`stage2_repair_captions.py`

不要破坏现有 `stage2_caption.py` 的历史复现逻辑。新脚本应：

1. 读取旧 Manifest 和官方 MultiOFF CSV，按现有稳定 key、split、row_number、image_name、image_sha256 精确对齐；
2. 复制旧 Manifest 到新版本目录；
3. 通过 OpenCLIP Tokenizer 找出全部且仅有超长项；
4. 对406条合格项保留完全相同的 Caption 字符串；
5. 只对334条超长项进行 InternVL 压缩/重写；
6. 每条 Caption 最多自动重试3次，逐次收紧长度要求；
7. 每条生成后立即用 OpenCLIP Tokenizer 验证；
8. 仍然超长时不得静默截断、不得写入“合格”状态；记录失败并停止正式训练；
9. 支持断点续跑，每25条或更频繁原子保存；
10. 对每条修改记录保存旧 Caption hash、新 Caption hash、旧/新 token 数、尝试次数、prompt hash、模型 revision、原图 hash；
11. 新旧 Manifest 分离，旧文件只读；
12. 输出脱敏汇总，不将 Caption 文本、图片、标签或模型权重提交 Git。

允许修改：
- 新增 `stage2_repair_captions.py`
- 新增必要的 CPU 单元测试
- 新增或修改 `stage2_coverage.py` 以输出修复前后差异
- 必要时对 `stage2_train.py` 增加 Caption 长度硬门禁和指标统计

不要改动官方上游源码；不要重写模型架构。

### 3.4 Caption 修复验收门禁

只有全部满足才进入训练：

- 740/740 样本 key、split、原图 SHA 对齐；
- Train/Dev/Test 仍为444/148/148；
- 740/740 Caption 非空；
- 740/740 OpenCLIP token 数不超过77；
- 406条原本合格 Caption 与旧版逐字相同；
- 334条原超长 Caption 全部有修复记录；
- 没有 Caption 直接复制原始 Meme 文本；
- 没有标签泄漏；
- 没有静默截断；
- 所有模型、Tokenizer、Prompt 版本和 SHA 可追溯。

如果最终有任何一条无法修复，停止训练并报告确切数量和失败样本稳定 key（不得公开图片或 Caption 文本）。

## 4. Stage 2.2：修复版 MultiOFF TRACE 训练与测试

### 4.1 模型与训练配置保持不变

继续使用当前 Stage 2 模型：
- OpenCLIP `roberta-ViT-B-32`；
- 固定 revision：`e22e1c12b0a1ba4af9fb6474626585351ea0da25`；
- 原始 Meme 文本 + 修复后的 InternVL Caption 两候选；
- 视觉编码器冻结；
- 当前作者分类器/融合结构；
- Loss：`L = L_cls + 0.3 L_contrastive + 0.7 L_relevance`；
- BF16；
- RTX 4090/4090D 单卡；
- 显存软上限18 GiB；
- Microbatch 32；
- Gradient Accumulation 4；
- AdamW，LR 1e-4，weight decay 0.01；
- gradient clipping 2.0；
- 最多20 Epoch；
- Dev Macro-F1 选模型，patience 5；
- 固定分类阈值0.5；
- 不得在 Test 上搜索阈值或选择 Epoch。

**本任务不允许为追求更高 Test 指标而修改学习率、Loss 权重、阈值、Prompt 或数据划分。** 如发现实现 bug，先停下来记录、修复并重新通过测试，不可边跑边调参。

### 4.2 训练前门禁

修改 `stage2_train.py`，在正式训练开始前直接验证全部 Caption：
- Manifest 完整性和 SHA；
- split 数量；
- Caption 非空；
- OpenCLIP token 数全部 <=77。

任何失败必须在加载大模型/启动训练前报错。

先执行：
1. CPU 测试：覆盖长度统计、334条筛选、旧 Caption 保留、修复 Manifest 原子写入；
2. GPU 单 Batch smoke：检查 forward、backward、梯度有限、参数更新、Checkpoint 保存/恢复；
3. 只有以上通过才开始正式训练。

不必重复 RAM++/GroundingDINO，也不必重新跑全量100-batch压力测试；本轮模型架构未变，重点验证新 Manifest 和长度硬门禁。

### 4.3 正式训练

为与旧实验形成直接对照，固定重跑两个既有随机种子：
- Seed 42
- Seed 121

每个种子从相同固定预训练 Backbone 和新初始化任务头开始，不能从旧 Stage 2 Checkpoint 续训。

建议输出目录：
- `.local/s2-repaired-v2-formal-seed42`
- `.local/s2-repaired-v2-formal-seed121`

使用新的修复版 Manifest。两次训练串行执行，不能同时占用 GPU。

每个种子：
- 只用 Train 444 训练；
- 每 Epoch 用 Dev 148 计算指标、选择最佳 Checkpoint；
- 选定最佳 Checkpoint 后才运行 Test 148；
- 每25个 Microbatch、每个 Epoch 结束及关键阶段保存并回读 Checkpoint；
- 记录完整 Loss 分量、梯度范数、预测概率分布、Caption Scorer 选择分布、耗时和显存；
- 单次 GPU 作业不超过5小时59分钟；
- 任何异常必须保留日志和可恢复 Checkpoint。

### 4.4 指标

Train/Dev/Test 均至少统计：
- Accuracy；
- Macro Precision；
- Macro Recall；
- Macro F1；
- Offensive Precision / Recall / F1；
- AUROC；
- Confusion Matrix；
- 预测正类数量/比例；
- 预测概率分布（min、max、mean、median、分位数）；
- 固定阈值0.5。

当前 `stage2_train.py` 已有 accuracy、positive-class precision/recall、macro F1、offensive F1、AUROC 和混淆矩阵；请补充 Macro Precision、Macro Recall 及概率分布统计，保持旧指标定义不变。

### 4.5 测试集使用与披露

此前旧 Caption 版本的 Test 指标已经被查看。本轮：
- 不得使用 Test 结果调参、改 Prompt、选模型或决定修复策略；
- 不得根据 Seed 42/121 的 Test 表现选择性报告某个种子；
- 仍按预先固定的 Dev Macro-F1 规则选 Checkpoint；
- 修复版 Test 只在两种子训练完成、Checkpoint 固定后评估；
- 报告必须披露 Test split 曾在旧 Caption 版本上被查看，因此修复版结果是透明的后续复核，不应声称这是从未触碰的全新 holdout。

## 5. 结果对照与结论边界

必须制作三层对照：

### A. 修复前 vs 修复后（相同 Backbone、模型、种子、训练配置）
- Seed 42：旧 vs 新；
- Seed 121：旧 vs 新；
- 比较 Dev/Test 的所有指标、正类预测比例、AUROC、最佳 Epoch；
- 不把结果变化单因果归结为 Caption 长度，因为重新生成也改变了超长 Caption 的具体文本。

### B. 本地结果 vs TRACE 论文 MultiOFF Table 6
清楚注明：
- 本地模型是 RoBERTa ViT-B/32、InternVL-only 两候选；
- 论文完整候选与 Backbone 设置不完全相同；
- 这是 Adapted Reproduction，不是论文 Table 6 的严格复现；
- 指标统一比较 Macro F1 和 Accuracy，Precision/Recall 仅在定义一致时比较；
- 不复制或推断论文未报告的 AUROC。

### C. Caption 修复质量
报告：
- 原始超长数334；
- 成功修复数；
- 最终超长数（必须为0）；
- 406条原有合格 Caption 是否完全未改变；
- 新 Caption token 数 median/P95/max；
- 按 Train/Dev/Test 分组统计；
- 旧/新 token 数分布；
- 重试次数和失败数；
- 选择 InternVL Caption vs Original Caption 的数量及比例。

## 6. 必须交付的文件

全部放入 `06_experiments/repro_trace/`，不要把私有数据写入仓库：

1. `Stage2_1_Caption_Repair_Protocol.md`
2. `Stage2_1_Caption_Repair_Audit.json`
3. `Stage2_1_Caption_Repair_Report.md`
4. `Stage2_2_Repaired_Training_Config.yaml`
5. `Stage2_2_Training_Summary_Seed42.json`
6. `Stage2_2_Training_Summary_Seed121.json`
7. `Stage2_2_Repaired_TRACE_Training_Report.md`
8. `Stage2_2_PrePost_Comparison.md`
9. `Stage2_2_Author_vs_Local_Comparison.md`
10. `Stage2_2_Reviewer_Gate.md`
11. 修复脚本和 CPU 测试文件；
12. 更新 `README.md`，链接新增报告。

事件日志和 Checkpoint 可保存在 Git 忽略的 `.local/`；仓库只提交脱敏聚合指标、哈希、配置和审计记录。

## 7. GPU、资源与时间约束

- 只允许一张 RTX 4090/4090D；
- `CUDA_VISIBLE_DEVICES` 必须显式固定为一个可用 GPU；
- 18 GiB 显存软上限；
- 单次 GPU 命令最多5小时59分钟；
- GPU 作业串行；
- 不重新下载已验证模型；
- Caption 修复只使用现有 InternVL、RAM++ tags、GroundingDINO grounding 和原始图像；
- 不重新运行 RAM++ 或 GroundingDINO；
- 不并行加载 InternVL 与 CLIP 训练模型；
- 每25条 Caption 原子保存，支持断点续跑；
- 每25个训练 Microbatch 和每 Epoch 保存/回读 Checkpoint。

## 8. 验收标准

本任务完成必须同时满足：

**Caption**
- 740/740 对齐、非空；
- 740/740 <=77 OpenCLIP tokens；
- 原406条合格 Caption 不变；
- 原334条超长 Caption 均有可追溯修复记录；
- 无标签泄漏、无静默截断；
- 旧 Manifest 完整保留。

**Training**
- Seed 42 和121 均从头训练完成；
- 训练、Dev 选择、最终 Test 评测流程完整；
- 每个种子都有可恢复 Checkpoint 和完整事件日志；
- 梯度、Loss、参数更新均通过数值检查；
- 显存、时长符合约束；
- 所有指标可由日志重新计算。

**Research audit**
- 明确写 Adapted Reproduction；
- 不将本地 B32 结果冒充论文最佳配置；
- 不使用 Test 指标调参；
- 如性能仍然较差，照实报告，不得改阈值或筛选种子制造提升；
- 给出 GO / CONDITIONAL GO / NO-GO 结论及证据。

## 9. 修改范围、提交与回滚

允许修改：
- `06_experiments/repro_trace/stage2_repair_captions.py`（新增）
- `stage2_coverage.py`
- `stage2_train.py`（只增加长度门禁与指标记录，不改变模型/损失/优化器）
- 对应测试、配置和报告
- `README.md`

禁止：
- 修改上游 TRACE 代码；
- 修改旧 Caption Manifest；
- 覆盖旧 Checkpoint、旧日志或旧报告；
- 将图片、Caption、数据标签、模型权重或私有 Manifest 提交 Git；
- 为提升 Test 指标而修改训练协议。

提交前：
1. 运行全部 CPU 测试；
2. 检查 Git diff 和 `.gitignore`；
3. 检查仓库中没有私有 Caption、图片、权重、完整原始数据；
4. 只提交代码、配置、脱敏聚合结果、审计报告；
5. 提交到当前分支，Commit message 建议：
   `repro(trace): repair MultiOFF captions and rerun two-seed TRACE`
6. 在最终回复提供 Commit SHA、两种子结果、Caption 修复统计、耗时、显存、遗留问题及下一步建议。

**不要只完成脚本或只跑 smoke 就宣布任务完成。最终目标是修复 Caption 后，真实完成 MultiOFF 两种子 TRACE 训练与测试。**
