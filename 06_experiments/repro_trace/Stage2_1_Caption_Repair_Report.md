# Stage 2.1｜真实 Caption 修复结果与阻塞

结论：**`CAPTION_GATE_BLOCKED`**。本轮仅使用 MultiOFF 和固定 InternVL2.5-8B，未使用 FHM、Gemini 或付费 API；旧 Manifest 保持只读，SHA-256 仍为 `9c2b130be4579876604a7586ffc85a194106b01c67341bede39d600eed5530bf`。新私有 Manifest SHA-256 为 `2f6d7c3fb2627f8c81e47794dd16c34763fc8bee5febc4d6536afc6e97bd1007`。[逐项脱敏审计](Stage2_1_Caption_Repair_Audit.json)；完整 Caption 和图片均未发布。

| 检查 | 修复前 | 本轮修复后 |
|---|---:|---:|
| 完整样本、Train/Dev/Test | 740；444/148/148 | 740；444/148/148 |
| 超过 77 OpenCLIP tokens | 334 | **5** |
| token 数中位数 / P95 / 最大 | 75 / 128 / 246 | 52 / 75 / 110 |
| 原本合格的 Caption 逐字保留 | — | **406/406** |
| 原超长项成功修复 | — | **329/334** |

按 Split，剩余超限为 Train **4**、Dev **1**、Test **0**。成功修复的 329 条中，325 条首试通过、3 条第 2 次通过、1 条第 3 次通过；其余 5 条各尝试 3 次，均未标记合格。失败稳定 key、旧 token 数、每次输出的 token 数和拒绝原因记录在审计 JSON，未包含 Caption 文本。失败原因：1 条三次均输出 80 tokens；4 条输出虽短，但含协议禁止的分类标签词。新清单的失败项仍保留旧 Caption，绝无静默截断。

InternVL 修复循环两段实测耗时 **28.764 + 515.765 = 544.529 秒**，不含模型加载与独立审计；两段 PyTorch reserved 显存峰值分别为 **17.588** 与 **17.816 GiB**，未超过 18 GiB。脚本按最多 25 条原子保存，并能从私有 Manifest 与修复审计恢复。旧版与新版都只保存在 Git 外。

脚本从未将真实标签提供给 InternVL。不过按禁止标签词的字符串筛查，原有 406 条合格且必须逐字保留的 Caption 中有 **6 条**包含这些词；这并非读取标签造成的泄漏证据，但意味着不能声称最终文本完全没有分类词。该冲突和 5 条未通过项都需要在后续协议中明确处理。训练包装层用实际 OpenCLIP Tokenizer 再验新 Manifest，真实返回 `OpenCLIP 77-token gate failed for 5 captions`，未加载大模型。

依据任务文档，**任一 Caption 未修复就必须停止正式训练**。本轮没有修复版 GPU Smoke、优化器更新、Seed 42/121 训练、Checkpoint 或 Test 指标；[Stage 2.2 门禁](Stage2_2_Reviewer_Gate.md)判定 NO-GO。下一轮应先制定并固定针对这 5 条的新增处理协议及 6 条旧 Caption 分类词的解释，再生成新版本 Manifest；不得在本轮第 3 次失败后继续自动尝试或直接截断。
