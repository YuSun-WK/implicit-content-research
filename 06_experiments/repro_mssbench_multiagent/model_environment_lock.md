# 原生模型环境 · 已通过真实加载

固定 `liuhaotian/llava-v1.6-vicuna-7b@deae57a8c0ccb0da4c2661cc1891cc9d06503d11`、`openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1` 和 `haotian-liu/LLaVA@c121f0432da27facab705978f83c4ada465e46fd`。12/12 必需文件经过官方大小、SHA256 或 Git blob OID 校验，锁定清单见 [weights_verified.json](native_stage1/weights_verified.json)。

隔离 Python 3.10.19 venv 使用 Transformers 4.37.2、Accelerate 0.27.2、bitsandbytes 0.48.2 和现成 Torch 2.9.1+cu128。原先 Accelerate 1.12.0 的单卡 4-bit `.to()` 错误已在本 venv 内解决；环境来源和全量冻结见 [兼容记录](native_stage1/retrieval_and_compatibility.md) 与 [environment_freeze.txt](native_stage1/environment_freeze.txt)。没有修改其他实验环境。

原始模型在 GPU 5 成功加载。五个 256-token 断点进程各加载一次，单次进程内全部 Agent 共用一个实例；参数均在 `cuda:0`，没有观察到 CPU offload。文本/单图探针、真实 Agent 轨迹、峰值显存及 G1/G2 结果见 [Stage 1 Gate](stage1_gate_report.md)。权重、图像和 venv 留在忽略的本地缓存，不提交大型二进制。
