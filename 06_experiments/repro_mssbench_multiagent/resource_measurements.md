# Stage 1 资源记录 · PARTIAL

| 项目 | 状态 |
|---|---|
| 数据卷 / RAM | 3.7 TiB 可用 / 501 GiB 可用 |
| 候选单卡 | 物理索引 7，`GPU-79ea6ee8-2e76-d1508-7813c1589ec1`，遥测 48,506 MiB free，0% utilization。未用于生成。 |
| CUDA 分配 / 权重加载 | 未发生 |
| 实际生成调用数 | 0 |
| 角色 token、推理耗时、峰值 GPU allocated/reserved/NVML | 未测量 |
| G1 / G2 计划规模 | 20 / 200 次生成。G2 若获准，复用已完成的 G1 输入键，补齐其余 180 次理论调用。 |
| 六小时限制 | G1 尚无实测调用时长，无法做保守 G2 外推。 |

[主机遥测](logs/stage1/environment.log) · [阻断日志](logs/stage1/g1_preflight.log)
