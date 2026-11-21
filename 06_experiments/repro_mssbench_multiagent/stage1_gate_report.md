# Stage 1 Gate Report · 原始 LLaVA G1 PASS，G2 PARTIAL

2026-11-21 在固定官方 LLaVA-1.6 Vicuna-7B 与 CLIP 权重整文件校验通过后完成真实 GPU Stage 1。详细证据、真实轨迹、分组结果及资源数值见 [原始模型门槛报告](native_stage1/native_gate_report.md) 和 [实验档案](native_stage1/README.md)。此前 G0 FAIL 是当时权重未完整下载的历史状态，现已修复；此前 ThinkingGuard 结果仍独立标记为 D 替代模型协议迁移。

| 门槛 | 结果 |
|---|---|
| 数据和 40 张图片 | PASS；固定 HF 发布版，论文 Table 1 类别差异保持 unresolved |
| 原始模型权重与独立环境 | PASS；12/12 文件核验，单卡 NF4 加载成功 |
| 纯文本和单图探针 | PASS；原始输出与图像嵌入长度已保存 |
| G1 | PASS；2 对、4 图文输入、20 次模型生成，信息流和 QA 路由实测通过 |
| G2 | PARTIAL；20 对、40 图文输入、200 次规范生成完成，118/120 方法×输入 complete、2/120 安全标签 invalid |
| 资源预算 | PASS；峰值 PyTorch reserved 6.979 GiB，NVML 增量 7.398 GiB，低于 20 GiB |
| 官方回答 Judge | 未执行；本地关键词粗筛不能代替 GPT-4o 评分 |
| Pilot | HOLD；本轮未启动 |

具体配置为单卡 GPU 5、batch 1、greedy、seed 0、224×224 本地图预缩放、256 max new tokens。模型使用原始权重/源码，CUDA/Torch、量化和文本解析为有记录的本地适配。43 次规范输出触及 token 上限、7 条 Embodied Multi-Agent 最终回答字段 Unknown，均不能写作成功的完整回答。输入安全标签评测与回答行为粗筛严格分开。
