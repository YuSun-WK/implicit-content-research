# 原始权重获取与兼容性修复

## 固定资产

官方 LLaVA 三片 safetensors 与 CLIP BIN 的 SHA256 分别为：

| 文件 | 字节 | 官方 SHA256 |
|---|---:|---|
| `native/model-00001-of-00003.safetensors` | 4,938,993,632 | `f61fd54d6e47f55db4452dd5a263cb5323d1b8077cad86bf536ae0e6b46b5df5` |
| `native/model-00002-of-00003.safetensors` | 4,947,390,880 | `a5219e366b4da0d6df6116a2b71c6bceea0b77dfcc5fdec4fa774f0f26c39ec4` |
| `native/model-00003-of-00003.safetensors` | 4,239,524,944 | `52a8836fee344f7582a208e4c01d218aa53fa3a3edbfab4538f50aecd57c1646` |
| `clip/pytorch_model.bin` | 1,711,974,081 | `c6032c2e0caae3dc2d4fba35535fa6307dbb49df59c7e182b1bc4b3329b81801` |

此前已核对服务器 HF/pip 缓存、可见完整文件和本地 Python 环境，未找到这四个官方哈希的整文件。使用服务器已有的 sing-box 节点配置，在本实验忽略目录中临时启动隔离本地代理。HF 固定 revision 的独立 HTTP Range 请求逐一检查 `206`、完整 `Content-Range` 和实际字节数，成功块持久化并支持续传。节点 10/11 都发生过超时和连接重置；节点 11 完成大部分 16 MiB 块。CLIP 最后一个 16 MiB 块改用 16 个 1 MiB 子请求。块级自检后组装，四个整文件均通过官方 SHA256；其余 8 个文件通过官方 SHA256 或 Git blob OID，之后原子生成 [weights_verified.json](weights_verified.json)。未改变模型或视觉塔版本，权重本体没有提交到 Git。

## 隔离环境与真实加载

独立 Python 3.10.19 venv 在 `.stage0-local/stage1/native-venv`。Torch `2.9.1+cu128`、torchvision `0.24.1` 只读复用服务器现有环境，Accelerate `0.27.2` 从另一已有本机环境复制进本 venv；Transformers `4.37.2`、bitsandbytes `0.48.2`、tokenizers `0.15.1` 和其他实用包见 [版本冻结](environment_freeze.txt)。这套 CUDA/Torch/Accelerate 组合是 D 本地兼容修复，偏离原 LLaVA 推荐的 Torch 2.1 系列；原始模型源码 `haotian-liu/LLaVA@c121f0432da27facab705978f83c4ada465e46fd` 与权重均未改写。

首次加载暴露 Accelerate `1.12.0` 对单设备 4-bit 模型调用不允许的 `.to()`，因此在本 venv 使用现成的 `0.27.2`。随后五个 256-token 断点进程各自只加载一次原始权重，所有参数均在 `cuda:0`，`hf_device_map={"": "0"}`，没有观察到 CPU offload 或模型在单次进程中二次加载。单次加载耗时 22.37–26.52 秒。原始 LLaVA `generate(inputs_embeds=...)` 返回的序列带合成 BOS；Adapter 只从 token 计数中去掉该前缀，原始解码回答未被修改。文本探针返回 `Okay.`；单图探针返回 `A truck is dumping dirt.`，实际图像嵌入长度 1227，大于文本 token 长度 52。

单卡使用 GPU 5：`GPU-5a0ba87d-2dc2-fed4-276c-8bb93dcec495`（RTX 4090 D，驱动 580.82.09，49140 MiB）。模型参数和推理均在这张可见 GPU，batch=1，NF4/FP16 双量化、greedy、seed 0、上限 256 token，所有 Agent 在每次进程中共用该实例。最大 PyTorch allocated 5.565 GiB、reserved 6.979 GiB、NVML 相对基线增量 7.398 GiB，均低于 20 GiB。NVML 设备总量可能包含同卡其他进程；PyTorch 值只计本进程。当前数据卷约 3.6 TiB 可用，内存约 491 GiB available。

图像沿用作者发布代码的本地路径 224×224 预缩放，再交原生 LLaVA 处理器；这区别于完全原生 any-resolution。256 token 上限也区别于作者发布包装器的 512，原因是 128-token G1 出现截断。43/200 个规范调用仍达到 256 上限，报告中将其列为可解释性限制。
