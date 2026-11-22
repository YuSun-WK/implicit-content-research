# Work 制作任务｜在 MMAligner 组会 PPT 末尾追加一页 TRACE 复现进展

## 1. 交付目标

以用户提供的原始 PowerPoint 为母版：

`MMAligner 论文分享｜多模态大模型的表示校准(3).pptx`

**只在原 PPT 最后追加 1 页 TRACE 复现进展；原有 9 页内容、顺序、图片、图表和动画全部保持不变。** 新增后共 10 页，新页页码为 10 / 10。

如果当前 Work 会话没有收到该 PPTX 附件，先请用户上传原文件，不得从零重建或根据 PDF 截图重做整套 PPT。

输出：
- 可编辑 PowerPoint：`MMAligner_组会汇报_TRACE复现进展.pptx`
- 如工具支持，再额外导出新增第10页预览 PDF/PNG，方便检查；但 PPTX 是主要交付。

本任务只制作一页，不制作新封面、不重排前9页、不增加额外总结页。

## 2. 风格复刻要求（必须以原PPT为准）

原 PPT 为宽屏 16:9，约 13.333 × 7.5 英寸。请直接复用原文件主题和母版元素。

从原 PPT 提取的视觉规范：
- 白色背景；
- 深蓝绿色标题，标题左侧有短竖线装饰；
- 标题下方一条浅灰色细横线；
- 中文为主，必要英文术语保留；
- 正文使用清晰、克制的无衬线字体，原文件主要为 Noto Sans；
- 主色可参考：深色 `#073C54` / `#005271`，正文深灰蓝 `#122532` / `#577180`；
- 重点结论使用浅蓝色底框，参考 `#DFF1F6`；
- 页脚左侧为论文/章节来源，右侧为页码；
- 标题、正文、图表文字层级清楚，留白充足。

不要使用渐变、花哨图标、卡通插画、深色背景或与原 PPT 不一致的商务模板。不要把一页做成密密麻麻的论文摘要。

## 3. 新增页定位与标题

建议标题：

**个人进展｜TRACE：多模态仇恨 Meme 检测复现**

标题下的元信息小字：

`多模态仇恨 / 冒犯性 Meme 检测  ·  AAAI 2026  ·  AI for Social Impact Special Track（AISI）  ·  CCF-A`

论文完整信息：
- TRACE: Textual Relevance Augmentation and Contextual Encoding for Multimodal Hate Detection
- Girish A. Koushik, Helen Treharne, Aditya Joshi, Diptesh Kanojia
- Proceedings of the AAAI Conference on Artificial Intelligence, 40(45), 38763–38771, 2026
- AAAI-26 Special Track on AI for Social Impact I（AISI）
- CCF 人工智能领域 A 类会议

## 4. 单页布局建议

建议采用“左侧方法机制 + 右侧结果对照 + 底部阶段判断”的结构。

### 左侧：TRACE 方法（约占页面宽度 48%）

用简洁的 4 步流程图表达，不要堆大段文字：

1. **Visual Grounding**
   - RAM / RAM++ 视觉标签识别
   - GroundingDINO 目标检测与区域定位

2. **Visual Context Augmentation**
   - 将视觉标签、目标框与 Meme 原始文字提供给 InternVL-2.5-8B
   - 生成补充图文语境的候选 Caption

3. **Caption Relevance Scoring**
   - Caption Scorer 对候选描述打分
   - Gumbel-Softmax 进行可微相关性选择
   - 目标是突出与仇恨/冒犯判断更相关的描述

4. **Contextual Encoding & Classification**
   - CLIP 编码图像和候选文本
   - 双向 Cross-Attention 融合图文表示
   - 参数高效微调文本编码器末端层，并进行二分类

方法一句话总结（可放流程图下方浅蓝色窄框）：
`视觉 grounding 补充语境，Caption Scorer 选择任务相关描述，再通过 CLIP 图文融合完成分类。`

注意：不要将 InternVL 说成分类器；它在这里负责离线生成候选描述。不要把 RAM / GroundingDINO / InternVL 误写为端到端参与分类器训练。

### 右侧：论文与本地结果对照（约占页面宽度 48%）

用小表格展示 Accuracy 和 Macro-F1，统一保留三位小数：

| 设置 | Accuracy | Macro-F1 |
|---|---:|---:|
| TRACE 原论文 MultiOFF | **0.678** | **0.673** |
| 本地旧 Caption 版 Seed 42 | 0.601 | 0.443 |
| 本地旧 Caption 版 Seed 121 | 0.615 | 0.381 |
| 本地两种子均值 | **0.608** | **0.412** |

表格标题建议：
`MultiOFF Test：论文结果 vs. 本地阶段性结果`

表格旁边或下方放一行差距：
`本地两种子均值较论文：Accuracy −7.0 pp；Macro-F1 −26.1 pp`

数据来源与口径：
- TRACE 论文 Table 6：Accuracy=0.678、F1=0.673、Precision=0.673、Recall=0.681。
- 论文 Experimental Setup 明确说明 Precision / Recall / F1 使用 macro average；因此本地比较列使用本地报告中的 Macro-F1。
- 本地 Seed 42：Test Accuracy=0.601351，Macro-F1=0.442508。
- 本地 Seed 121：Test Accuracy=0.614865，Macro-F1=0.380753。
- 两种子简单均值：Accuracy=0.608108，Macro-F1=0.411630。
- 不要把本地 Macro-F1 写成 Offensive F1，也不要把 AUROC 当成论文主指标。

**关键标注：以上本地结果是 Caption 修复前的旧版本阶段性结果，不是修复版最终结果。** 可在表格标题旁标注“旧 Caption 版 / 初步结果”，不要写成完整复现成功。

### 数据集信息（可放在左侧流程下方或页底）

用一行区分论文数据和本地复现：

- 论文：Facebook Hateful Memes（FHM）+ MultiOFF
- 本地本轮：仅 MultiOFF；旧版实际样本为 740（Train/Dev/Test = 444/148/148）

原论文 Table 2 报告：
- FHM：8.5k / 500 / 1k
- MultiOFF：445 / 149 / 149

请明确论文与本地 MultiOFF split 数量不同，不要混写。

## 5. 必须放入的简短分析与当前状态

在底部使用一个浅蓝色结论框，最多 2–3 行，表达：

**初步分析**
- 本地采用 RoBERTa ViT-B/32，论文 MultiOFF 最佳配置为 CLIP-XLM-R-ViT-H/14，微调文本编码器最后 4 层；本地是更小的 Backbone / 两候选设置，不能视为严格同配置复现。
- 旧版 740 条 Caption 中有 334 条超过 OpenCLIP 77-token 上限，旧版结果存在输入截断风险，可能影响语义信息与性能。
- Caption 修复已完成 329/334 条，剩余 5 条按用户决定排除；修复版 4-seed 多 GPU 训练已形成执行任务，但截至当前最新仓库提交，**尚无新训练日志、Checkpoint 或修复版 Test 结果**。

可以压缩成底部状态条：
`已完成：旧版 MultiOFF 双种子训练与测试；Caption 修复：329/334；下一步：排除 5 条后开展多 GPU 四种子重跑。`

不要把“已提交多 GPU 执行计划”写成“多 GPU 训练已完成”。不要编造修复版指标、空闲 GPU 数量或新训练结果。

## 6. 复现边界（必须准确）

本地方法必须标注为：

`TRACE-InternVL-only-MultiOFF-2caption（Adapted Reproduction）`

与原论文的关键差异：
- 论文 MultiOFF 最佳配置：CLIP-XLM-R-ViT-H/14，微调文本编码器最后 4 层；
- 本地旧版：RoBERTa ViT-B/32，两候选（原始 Meme 文本 + InternVL Caption）；
- 论文 Table 2 的 MultiOFF split 为 445/149/149；本地旧版数据为 444/148/148；
- 本地没有完成 FHM 实验；
- 本地旧版 Caption 有超长问题，修复版训练尚未完成。

因此：
- 不得称为“完整严格复现”；
- 不得把本地差距全部归因于 Backbone 或 Caption 某一个因素；
- 可说“当前结果低于论文报告，可能与 Backbone 规模、候选描述配置、数据划分及 Caption 长度截断等差异有关”。

## 7. 信息密度与视觉要求

- 新增页只放一页，正文中文为主；
- 关键英文保留：Visual Grounding、Context Augmentation、Caption Scorer、Gumbel-Softmax、Cross-Attention、Macro-F1；
- 不超过 4 个主要视觉区块；
- 方法流程图不超过 4 个节点；
- 结果表不超过 4 行；
- 分析最多 3 条；
- 不要写完整公式、训练参数长列表或实验日志细节；
- 结果数字应比正文更醒目，但不能夸张；
- 避免把“本地结果低于论文”隐藏在很小的脚注中；
- 页脚注明：`TRACE §3 · Table 2 · Table 6；本地记录：Stage2_Complete_TRACE_Training_Report.md`；
- 页码使用 `10 / 10`。

## 8. 事实来源

### 原论文
- 官方 AAAI 页面：https://ojs.aaai.org/index.php/AAAI/article/view/41220
- 官方 PDF：https://ojs.aaai.org/index.php/AAAI/article/download/41220/45181
- 代码：https://github.com/surrey-nlp/TRACE
- DOI：https://doi.org/10.1609/aaai.v40i45.41220

原论文中本页主要依据：
- §3.1 Visual Grounded Context Augmentation
- §3.2 Caption-aware Text Encoder Fine-tuning
- Table 2 数据集划分
- Table 6 MultiOFF 结果

### 本地 GitHub 证据
仓库：`YuSun-WK/implicit-content-research`
分支：`repro/trace-aaai2026-20261119`

- 旧版真实训练报告：
  `06_experiments/repro_trace/Stage2_Complete_TRACE_Training_Report.md`
  https://github.com/YuSun-WK/implicit-content-research/blob/repro/trace-aaai2026-20261119/06_experiments/repro_trace/Stage2_Complete_TRACE_Training_Report.md

- Caption 修复报告：
  `06_experiments/repro_trace/Stage2_1_Caption_Repair_Report.md`
  https://github.com/YuSun-WK/implicit-content-research/blob/repro/trace-aaai2026-20261119/06_experiments/repro_trace/Stage2_1_Caption_Repair_Report.md

- 当前门禁：
  `06_experiments/repro_trace/Stage2_2_Reviewer_Gate.md`
  https://github.com/YuSun-WK/implicit-content-research/blob/repro/trace-aaai2026-20261119/06_experiments/repro_trace/Stage2_2_Reviewer_Gate.md

- 最新多 GPU 执行任务（仅计划，不代表已经运行）：
  `06_experiments/repro_trace/Codex_PROMPT_TRACE_S2_2_MULTI_GPU_EXCLUDED5_FORMAL_RUN_20261122.md`
  https://github.com/YuSun-WK/implicit-content-research/blob/repro/trace-aaai2026-20261119/06_experiments/repro_trace/Codex_PROMPT_TRACE_S2_2_MULTI_GPU_EXCLUDED5_FORMAL_RUN_20261122.md

## 9. 最终验收清单

完成后请自查：
1. 原始 9 页完全未改动；
2. 只新增 1 页，总计 10 页；
3. 新页的颜色、字体、标题、页脚与原 PPT 一致；
4. TRACE 领域、年份、AAAI 特别轨道、CCF-A 正确；
5. 方法描述准确区分视觉 grounding、Caption 生成、Caption 评分和 CLIP 分类；
6. 论文 MultiOFF 指标和本地两个种子指标准确；
7. Macro-F1 口径一致；
8. 旧 Caption 版 / 初步结果 / 截断风险明确标注；
9. 329/334 Caption 修复与 5 条排除后的新训练状态没有被写成已经完成；
10. 没有任何编造的实验数字、GPU 数量或训练完成状态；
11. 字体无缺失、无文字溢出、无元素重叠；
12. 新增页可编辑，不要把整页扁平化成一张图片。

请交付最终 PPTX，并简要说明新增页布局和事实核对结果。
