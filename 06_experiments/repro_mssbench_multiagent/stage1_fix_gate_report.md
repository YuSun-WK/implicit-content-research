# Stage 1-Fix · G1 Gate STOP

| 检查 | 裁决 | 实际结果 |
|---|---|---|
| 已有缓存和资源 | PASS | HF cache 59 GiB，pip cache 141 MiB，扫描了缓存和可见工作卷。未找到尺寸匹配的完整原生三片权重或 CLIP。发现可复用本机 PyTorch 等依赖。 |
| 独立 venv 和原生 CPU 路径 | PASS（CPU） | Python 3.10.19。原生 builder、NF4 配置、固定 tokenizer 和固定 CLIP processor 通过。真实 Smoke 图片从 224×224 生成原生预处理 Tensor `(1, 3, 3, 336, 336)`。 |
| 模型资产最终校验 | FAIL | 8/12 文件通过官方 SHA256 或 blob OID。四个缺失大文件共 15,837,883,537 B；可续传部分合计 22,256,175 B。没有理由生成 `weights_verified.json`。 |
| 加载、纯文本探针、单图探针 | 未执行 | 真实运行器在权重门槛停止；GPU 未分配，CPU offload 与加载峰值未测。 |
| G1（2 对、4 输入、20 次生成） | 未执行 | 权重校验未通过。模型加载及真实调用均为 0。无真实 Token、耗时、显存、输出格式或路由结果。 |
| G2 / Pilot / Full | 未启动 | 本轮范围止于 G1。 |

唯一下一步是通过可稳定传输的文件缓存预置**同 SHA256 的四个大权重**到该实验独立目录，完成原源校验，再使用同一个模型实例运行两个独立探针和 G1。

[逐权重状态](stage1_fix_weights.csv) · [CPU 运行证据](logs/stage1fix/cpu_native_import.log) · [实际 G1 preflight](logs/stage1fix/g1_preflight.log)
