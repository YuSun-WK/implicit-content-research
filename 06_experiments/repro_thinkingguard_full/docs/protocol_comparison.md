# 协议与报告口径

| 条件 | 输入与范围 | 推理配置 | 指标 |
|---|---|---|---|
| 作者 Table 1 | TriggerBench-Test 1,736 图文侧别，九类 | 论文说明训练与 benchmark 设计。作者示例使用 BF16、固定五步提示词和 1,024 token 上限 | 九类 Unsafe F1/Recall 及等权平均 |
| 历史 H1-K1 unified | 36 对，正式 180 条含 72 条图文、36 条仅文本、72 条仅图像 | NF4、定制短标签提示词、greedy、32 token | 图文 Accuracy 51/72、Unsafe F1 0.644、PairAcc 15/36 |
| Stage 1 A0 | Smoke 6 条、独立验证 36 条、过门槛后 Pilot 100 对 | 作者代码的 verbatim SYSTEM_PROMPT 与 user wrapper、模型固定 chat template 和默认图像处理、NF4 + BF16 compute、greedy、1,024 token | 结构完整率、唯一结论提取率、耗时与显存。Pilot 同时报告 strict 和 valid-only、类别宏平均、整体微平均、配对指标。 |

历史五步正式 36 对维持 NOT_RUN。Stage 1 NF4 是显存预算适配，作者 BF16 示例和论文评测的数值可比性尚未验证。CPU 配置核查确认固定 tokenizer 的五个结束标记都能经作者的 `skip_special_tokens=True` 解码保留。

Pilot strict 将 INVALID 和未生成记录纳入全分母。Safe INVALID 保留在 FPR 分母并单列，Unsafe INVALID 进入 FNR。Wilson 用于二项比例。按类别分层的 pair bootstrap 一次重采同对两侧，计算 Accuracy、Unsafe F1 和 PairAcc 的区间。有效对的四种预测组合按 Safe 侧、Unsafe 侧顺序记录。
