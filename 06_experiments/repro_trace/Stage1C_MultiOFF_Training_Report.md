# TRACE-S1C · MultiOFF 实测训练

**`adapted_author_baseline` · PASS。** 固定 TRACE 的 projection 类、collate 和 focal loss 在作者公开数据的完整样本子集上完成真实训练与评价。Train/Dev/Test 实际分母为 444/148/148。正式训练从新初始化的投影与分类头开始，主干始终使用固定的预训练 CLIP，未把 smoke 或 short 的权重带入正式训练。 [数据与排除规则](Stage1C_MultiOFF_Data_Audit.md) · [与论文协议差异](Stage1C_MultiOFF_Paper_Code_Alignment.md)

| 阶段 | Microbatch | 批数 | CUDA AdamW 更新 | 步时 p50 / p95 (s) | 峰值 allocated / reserved (GiB) |
|---|---:|---:|---:|---:|---:|
| Smoke | 1 | 1 | 1 | 0.770 / 0.770 | 1.869 / 1.920 |
| Smoke | 16 | 1 | 1 | 1.016 / 1.016 | 1.906 / 2.066 |
| Short | 16 | 100 | 4 | 0.513 / 1.009 | 2.193 / 2.334 |
| 正式 | 16 | 196 | 7 | 0.535 / 1.010 | 2.534 / 2.652 |

B1 smoke 总 Loss 0.088677，融合/图像/文本 focal 分量为 0.044751 / 0.043240 / 0.044221（加权前）。裁剪前总梯度范数 0.121248，融合分类器最大参数变化 0.0001000，冻结主干无梯度。每个阶段的日志保留实际 loss 分量、梯度与更新证据。两次 smoke 均保存并回读。Short 在 25、50、75、100 批保存并回读，在第 50 批退出后由新进程恢复游标、已有的 1 次更新及待累积梯度，继续至第 100 批。实际更新的有效批为 444、444、444、256。 [B1 日志](stage1c_multioff_smoke_b1.jsonl) · [B16 日志](stage1c_multioff_smoke_b16.jsonl) · [短跑日志](stage1c_multioff_short.jsonl)

正式配置预先固定 seed 42、BF16、单卡 RTX 4090、逻辑批上限 512（实际每 epoch 444）、AdamW 学习率与 weight decay 均为 1e-4，梯度裁剪 1.0，最多 20 epoch，Dev Macro-F1 的 patience 5。按短跑实测 p95 做保守估算约 1930 秒。正式运行计时 182.77 秒，于第 7 个 epoch 早停。Dev 指标平手时保留先达到的 checkpoint，最终选择第 2 个 epoch。阈值固定 0.5，Test 在选定 checkpoint 后评估一次。正式运行输出为恢复状态和最佳 Dev checkpoint，实测跨进程恢复来自 short。 [预算](stage1c_multioff_budget.json) · [正式日志](stage1c_multioff_formal.jsonl) · [Checkpoint 哈希](stage1c_multioff_checkpoint_manifest.json)

| Split | N | Offensive | Accuracy | Macro F1 | AUROC |
|---|---:|---:|---:|---:|---:|
| Train | 444 | 186 | 0.5811 | 0.3675 | 0.5575 |
| Dev | 148 | 57 | 0.6149 | 0.3808 | 0.5517 |
| Test | 148 | 57 | 0.6149 | 0.3808 | 0.5361 |

Test Accuracy 和 Macro F1 与在这 148 条上始终预测多数类别所产生的两个指标相同。AUROC 是连续分数上的排序指标，实测 0.5361。该运行提供可审计的适配基线结果，论文原始 Table 6 条件仍待对齐。

## 实际启动命令

在 `06_experiments/repro_trace/` 下执行。输出均写入忽略的 `.local/`。重跑需另用新输出目录。

```bash
ROOT="$HOME/data/trace-assets/multioff"
CLIP_DIR="$HOME/data/trace-assets/clip/32bd64288804d66eefd0ccbe215aa642df71cc41"
PY=/tmp/trace-s0-py310/bin/python
export CUDA_VISIBLE_DEVICES=0
run_multioff() {
  timeout -k 10s 21540s "$PY" multioff_baseline.py \
    --data-dir "$ROOT" --model-dir "$CLIP_DIR" --complete-case "$@"
}
B16=.local/s1c-multioff-smoke-b16
SHORT=.local/s1c-multioff-short
run_multioff --phase smoke --microbatch 1 --output-dir .local/s1c-multioff-smoke-b1
run_multioff --phase smoke --microbatch 16 --output-dir "$B16"
run_multioff --phase short --microbatch 16 --output-dir "$SHORT" \
  --smoke-checkpoint "$B16/last.pt" --stop-after 50
run_multioff --phase short --microbatch 16 --output-dir "$SHORT" \
  --smoke-checkpoint "$B16/last.pt" --resume
run_multioff --phase formal --microbatch 16 --output-dir .local/s1c-multioff-formal \
  --smoke-checkpoint "$B16/last.pt" --short-log "$SHORT/events.jsonl"
```
