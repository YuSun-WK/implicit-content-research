# Stage 1 Smoke 指标 · 未运行

G0 的图像和 CPU 契约检查通过，完整原生权重和环境未就绪。G1、G2 都没有生成记录，故无分组准确率、回答类型比例、成对翻转率或真实模型失败案例。

计划分母为 Chat Safe 10、Chat Unsafe 10、Embodied Safe 10、Embodied Unsafe 10，每种方法各跑这些输入一次。G1 取 `query:chat:016:00` 和 `query:embodied:056:00`，每任务每侧一条。采用发布版原类别标签，行为关键词结果为 D 协议。

[图片分母证据](smoke_image_gate.md) · [Stage 1 Gate](stage1_gate_report.md)
