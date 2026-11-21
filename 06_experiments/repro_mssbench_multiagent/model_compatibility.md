# Model Compatibility Report · PARTIAL

优先模型为 LLaVA-1.6 Vicuna-7B。可见缓存未发现原权重、HF 转换权重、CLIP 336 权重或已安装的原生 `llava`。已核验权重发布元数据和 CPU 导入，GPU 加载与生成仍是待验证项。

| 路线 | 已核验 | 需验证 |
|---|---|---|
| 原生 `liuhaotian/llava-v1.6-vicuna-7b` | revision `deae57a8c0ccb0da4c2661cc1891cc9d06503d11`，3 shards 共 14,125,909,456 B，架构 `LlavaLlamaForCausalLM`、`spatial_unpad`、CLIP ViT-L/14-336。官方项目 builder 有 NF4 路线。 | 选择独立 Python 3.10 环境，锁原生项目及 wheel/CLIP 版本。核对 CLIP 的实际加载路径和冷缓存占用。验证单卡前向与文本-only Intent。 |
| 转换版 `llava-hf/llava-v1.6-vicuna-7b-hf` | revision `c916e6cdcd760b4cecd1dd4907f84ac649f93b23`，3 shards 共 14,126,954,312 B，用 `LlavaNextForConditionalGeneration`。现有 Python 3.10 环境中 4.57.3 类、Accelerate、bitsandbytes 可在 CPU 条件导入，NF4 配置可构造。 | 校验转换前后张量名映射、形状和抽样数值，分别检查 processor、conversation 模板、图像 token、缩放/填充及裁剪、文本解码边界。对相同样本、配置检查输出，记录差异。 |

[原权重](https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/tree/deae57a8c0ccb0da4c2661cc1891cc9d06503d11) · [转换权重](https://huggingface.co/llava-hf/llava-v1.6-vicuna-7b-hf/tree/c916e6cdcd760b4cecd1dd4907f84ac649f93b23) · [CLIP 版本](https://huggingface.co/openai/clip-vit-large-patch14-336/tree/ce19dc912ca5cd21c8a653c79e251e808ccabcd1)

原生候选源码锁为 `haotian-liu/LLaVA@c121f0432da27facab705978f83c4ada465e46fd`。其依赖声明含 torch 2.1.2、torchvision 0.16.2、Transformers 4.37.2、tokenizers 0.15.1、sentencepiece 0.1.99、Accelerate 0.21.0。PEFT 与 bitsandbytes 仍需解出兼容且固定的组合。独立环境使用现成 wheel，先做离线 CPU 导入及 tokenizer/processor 夹具检查。CLIP 外部权重文件 `pytorch_model.bin` 约 1.71 GB，原生视觉加载器存在从该仓库加载的路径。后续核实权重格式和 loader 兼容性并锁定本地快照。 [依赖声明](https://github.com/haotian-liu/LLaVA/blob/c121f0432da27facab705978f83c4ada465e46fd/pyproject.toml) · [原生加载器](https://github.com/haotian-liu/LLaVA/blob/c121f0432da27facab705978f83c4ada465e46fd/llava/model/builder.py)

原 MSSBench 包装器对本地图像使用 224×224，再送入带 any-resolution 相关配置的模型。忠实对照需保存 224 分支、`llava_v1` 对话模板、greedy 和 512 的原上限。后续预检采用 greedy/batch=1/128 tokens 上限，4-bit NF4、FP16 计算、双量化、单个可见设备与单份权重；这是 D 配置。保留原始分辨率、使用 HF processor 或改生成上限均需独立版本与记录。后续核对单卡加载的实际 device map、语言模型与视觉模块量化范围、停止条件、生成是否含输入回显，以及实测 allocated/reserved/NVML。先在锁 revision 的内置实现或审核过的原生源码路线运行。若任何备选模型依赖远程代码，先审阅固定 SHA 文件及其导入路径，默认禁用远程执行。 [4-bit 文档](https://huggingface.co/docs/transformers/en/quantization/bitsandbytes)

[CPU 导入日志](logs/transformers_import.log) · [原始环境日志](logs/environment.log)
