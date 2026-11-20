# TRACE-S1C · 实验总结与下一步

- **P1 CUDA 自检已完成。** 预训练 CLIP 的单候选 B1、三候选 B1、单候选 B2 均通过。共 9 次真正的 CUDA AdamW 调用，其中每个配置含一次恢复续步的重放，三次重放均逐位一致。合成输入只用于计算路径自检。 [CUDA 自检](Stage1C_CUDA_Architecture_Selftest.md)
- **P2 MultiOFF 已取得并完成一组适配基线。** 官方 CSV 445/149/149，已发布图片 746，三份 CSV 各欠同名图一张，完整样本分母为 444/148/148（共 740 条）。两次真实 smoke、100 Microbatch 验证及正式训练合计 13 次 CUDA AdamW 更新。正式训练 7 epoch，Dev 选 epoch 2，Test Accuracy 0.6149、Macro F1 0.3808、AUROC 0.5361。 [数据审计](Stage1C_MultiOFF_Data_Audit.md) · [训练与评价](Stage1C_MultiOFF_Training_Report.md)
- **P0/P3 FHM 仍为 `FHM_MANUAL_ACTION_REQUIRED`。** 一次路径检查后继续其他路线。真实 FHM Batch/更新均为 0。 [用户人工步骤](Stage1C_FHM_Manual_Data_Action.md)
- **P4 完整 TRACE 为 `BLOCKED`。** 缺少可追溯且对齐的作者 InternVL/Gemini Caption。完整 MultiOFF 的论文配置还需要 CLIP-XLM-R-ViT-H/14 的固定权重及准确的 T(-4)、分类和 relevance 协议。固定代码中的活动 OpenCLIP B/32 分支和论文配置存在差异，且作者该分支在评价标签上选阈值。 [论文与代码核对](Stage1C_MultiOFF_Paper_Code_Alignment.md)

**下一轮首选。** 先向作者核实三个未发布的图像引用，以及 Table 6 ViT-L/14 projection FT 使用的确切数据版本和 WiSE-FT 配置。取得缺图后运行严格的全 split 验收，并用全量签名重新完成 smoke、短跑、同一基线的预定协议。若授权 FHM 先就绪，直接运行单文本诊断的真实 smoke。完整 TRACE 待 Caption 与论文模型配置取得后再启动。

```bash
ROOT="$HOME/data/trace-assets/multioff"
/tmp/trace-s0-py310/bin/python multioff_baseline.py \
  --data-dir "$ROOT" --phase audit --output-dir .local/s1c-multioff-full-admission
```

全量验收通过后，沿训练报告中的命令启动，去掉 `--complete-case` 并使用新输出目录。不得沿用子集的签名、checkpoint 或既有 Test 结果。

本轮起点为 `73660c736fb18ea18175b01832af787c891e2817`。沿用既有 Conda 环境和模型缓存。12 项 CPU 回归通过。 [CPU 日志](stage1c_cpu_checks.log)
