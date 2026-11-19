# TRACE Stage 0 隔离环境

实测版本与 GPU 快照见 [environment_probe.json](environment_probe.json)。驱动 580.82.09，`nvidia-smi` 报支持 CUDA 13.0，PyTorch 构建和实际导入使用 CUDA 12.8。独立 Conda 环境中的 Python 3.10.19、torch 2.9.1+cu128、torchvision 0.24.1+cu128、Transformers 4.57.3、tokenizers 0.22.1。GPU inventory 显示 2 张 RTX 4090、6 张 RTX 4090 D，单卡探测限定设备 0，CUDA 可用，compute capability 8.9。该设备 NVIDIA 驱动当时报告总量 49,140 MiB、空闲 48,506 MiB，Stage 0 仍将训练预算设为 18 GiB。inventory 是瞬时状态。

训练入口使用 Hugging Face `CLIPModel`。公开配置资产实测可构造 `CLIPTokenizerFast`，词表 49,408、最大长度 77，`CLIPImageProcessor` 裁剪尺寸 224×224。上游 requirements 中另列 OpenAI CLIP Git revision `dcba3cb2e2827b402d2701e7e1c7d9fed8a20ef1`，本路径没有导入或安装 `clip`。当前 wrapper 复用 HF 模型返回的 projected Tensor，显式选择 eager attention。

## 官方依赖与本轮运行差异

固定 `requirements.txt` 原样保留于上游检出；该文件是跨任务环境。训练脚本导入 torch、torchvision、PIL、Transformers、tqdm、numpy、pandas、scikit-learn 和 wandb。包装仅执行训练模型类与 collate 声明，按需调用固定的 loss 与选 Caption helper。CSV/JSON 处理移到包装，pandas 和 W&B 不进入本轮运行依赖。Caption 生成另依赖 RAM 仓库修订 `88c2b0ca13e38cca6655f83ad0185271167dbcbf`、GroundingDINO API、`google.generativeai` SDK、未随库提供的 RAM++ checkpoint，均属于独立阶段。Caption 生成时各模型精确 checkpoint revision 未知。 [官方依赖](https://github.com/surrey-nlp/TRACE/blob/83ecb799f897fe275185e082ee9a669f7d04bfaa/requirements.txt)

优先尝试官方 torch 2.3.1、torchvision 0.18.1 与 Transformers 4.26.1。PyTorch wheel 镜像首轮读取超时，重试及 PyPI 路径出现哈希不匹配，应用层依赖下载也遇到哈希不匹配。未关闭校验。改用项目主机已有可工作的 Conda 环境离线克隆到独立前缀，`pip check` 通过。采用该环境实测版本完成 CPU 检查；真实训练的数值等价性仍未验证。环境报告 JSON 列出包版本，`requirements-stage0.txt` 按实际运行版本给出最小常用包。未改动全局环境。

当前主机复用命令如下。

```bash
/home/ubuntu/anaconda3/bin/conda create --offline -y -p /tmp/trace-s0-py310 --clone /home/ubuntu/anaconda3/envs/ESTMM
CUDA_VISIBLE_DEVICES=0 /tmp/trace-s0-py310/bin/python environment_probe.py
```

在可连接官方 wheel 索引的机器可按相同版本另建环境。以下是环境规格，当前主机的验证使用上述克隆环境。

```bash
python3.10 -m venv .local/venv
.local/venv/bin/python -m pip install --index-url https://download.pytorch.org/whl/cu128 torch==2.9.1 torchvision==0.24.1
.local/venv/bin/python -m pip install -r requirements-stage0.txt
.local/venv/bin/python -m pip check
```
