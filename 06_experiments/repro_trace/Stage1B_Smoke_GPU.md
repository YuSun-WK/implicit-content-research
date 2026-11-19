# TRACE-S1B · 单 Batch GPU smoke

**G4 `TRAINING_NOT_RUN`。** G1 阻塞，所以没有启动 `trace_text_only_diagnostic` 训练进程。当前未绑定 GPU。真实 FHM smoke 为 **0 Batch**，CUDA AdamW 更新为 **0 次**。Loss、梯度范数、分类器参数差、冻结视觉塔梯度、训练显存峰值和单步耗时均未测量。真实训练 Checkpoint 保存及恢复均未执行。 [本轮预检日志](stage1b_preflight.log)

现有 CLIP 快照经离线复核，8/8 文件 SHA-256 一致，真实预训练模型在 CPU 加载了 427,616,513 个参数。9 项 CPU fixture 为代码回归检查，涵盖单候选分类和恢复程序。 [权重验证日志](stage1b_clip_validation.json) · [CPU 检查](stage1b_preflight.log)

G1 通过后，从 `06_experiments/repro_trace/` 执行下列计划命令。私有 YAML 需在确认官方许可后填入实际图像、split 和现有模型路径。GPU 序号由届时的空闲检查决定。 [配置与环境快照](stage1b_preflight_config.json) · [现有配置说明](Stage1A_Mode_Semantics.md)

```bash
CUDA_VISIBLE_DEVICES="<空闲的 4090 或 4090D 序号>" \
  timeout -k 10s 5h59m /tmp/trace-s0-py310/bin/python \
  run_stage0.py --config .local/s1b-smoke.yaml
```

计划用 BF16、Microbatch 1、累积 1、seed 121。通过条件包括有限分类 Loss、文本块 4/7/10 和各融合及分类模块的有效梯度、冻结视觉塔无梯度、分类器权重实际更新、低于 18 GiB 的显存峰值及 Checkpoint 回读。单候选 Scorer 排序梯度为零不影响诊断验收。
