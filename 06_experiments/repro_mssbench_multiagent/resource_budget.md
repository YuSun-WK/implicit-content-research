# Resource Budget · PASS（容量审计）

| 资源 | 服务器实测 | 后续计划或上限 |
|---|---|---|
| 工作区数据卷 | 3.7 TiB 可用 | 新环境建议预留 45–60 GB；低于 20 GB 停止权重获取 |
| 根卷、临时目录和默认 HF 缓存所在卷 | 6.3 TiB 可用；全局 HF cache 已占 59 GiB | 用实验专用 `HF_HOME`，避免额外复制完整快照 |
| RAM / swap | 501 GiB available / 8 GiB swap | 建议至少 32 GiB available |
| GPU | 8 张 4090/4090 D。每张驱动报告 49,140 MiB，六张在采样时约 48,506 MiB free、0% utilization | 按实际 free 选择单卡；实验软件上限 16–20 GiB。4-bit 7B 估 8–16 GiB，取决于视觉张量和 KV cache |
| 已在用 GPU | 1/2 在采样时 100% 利用率，free 分别 34,772 / 35,742 MiB | 跳过 1/2；后续占用需重新核查 |
| 驱动 / CUDA | 580.82.09，驱动报告 CUDA 13.0；探测的两个 torch 2.9.1 wheel 报 CUDA 12.8，`nvcc` 未在 PATH | 原生和转换依赖分开固定；以 wheel 编译 CUDA 和实测加载为准 |
| 默认 Python | 3.13.5，有 Pillow 11.1.0 和 tqdm 4.67.1，缺 torch、Transformers、原生 llava | Stage 0 使用默认 Python；真实模型用独立 Python 3.10，现有其他实验环境只读探测 |
| 图片 | JSON 308,884 B；发布元数据 254,494,078 B 图像，Smoke 清单 38,483,771 B | 单张直接存放，不维护解压副本 |
| 原模型 | 本机未找到；远端元数据约 14.126 GB 模型权重，视觉依赖可能再占约 1.71 GB | 只保留一个主权重路线。4-bit 运行仍需原始下载体积 |
| 其余磁盘 | 本轮未安装或下载模型 | 环境 3–8 GB；输出 0.1–1 GB；临时 2–8 GB；均为估算 |

`CUDA_VISIBLE_DEVICES` 起始未设置。CPU 模型库探测显式隐藏 CUDA，`torch.cuda.is_initialized()` 为 False。显存容量取驱动计数，单卡硬件的物理构成未独立核验。采样值会随作业变化。

主矩阵 Smoke 理论调用 200 次，Full 10,240 次，均未计重试、诊断和 Judge。Pilot 按任务、方法、每角色真实耗时和失败回退外推。若预计超过 6 小时，按输入片段切块并用 SQLite 键恢复。Smoke 从 128 tokens 开始记录生成长度、峰值、延迟和 I/O；Pilot 另核对解析率 ≥95%，Expanded Pilot 的超时/硬失败 ≤2%。

[资源和环境日志](logs/environment.log) · [CPU 导入日志](logs/transformers_import.log)
