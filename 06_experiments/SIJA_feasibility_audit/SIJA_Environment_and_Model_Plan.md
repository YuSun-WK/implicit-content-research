# 环境与模型方案

2026-11-16 13:31 UTC实测nvidia-smi：8卡，0–1为RTX4090，2–7为RTX4090 D；工具报告每卡49140MiB（以服务器实报为准，不套用零售卡规格）。驱动580.82.09，显示CUDA兼容版本13.0，不代表已安装CUDA Toolkit。0/3/4/5/6约3MiB占用；1为13731、2为12145、7为9507MiB。后续compute-apps读到两个PID，但ps未能解析属主，容器进程可见性有限；不能断言无人使用。无kill、无GPU推理。本轮只读查询。

系统Python3.13.5；已有项目venv只读探测PyTorch2.9.1+cu128、Transformers4.57.3。未改环境。磁盘约3.7TiB空闲。可见ThinkingGuard-8B缓存目录15G、revision 76892f9768ce828268265171f4bbc5dfb75eafc3、config声明Qwen3VL；没有发现标准*.safetensors文件，尚不能证明是可直接加载的完整checkpoint。它还经过安全训练，不能代替未适配基础VLM作无混杂基线。未扫描其他用户私有缓存。

| 模型 | 规模 | 多图 | 预计峰值显存（未实测） | 依赖成本 | 适合性 | 依据 |
|---|---|---|---|---|---|---|
| Qwen3-VL-4B-Instruct | 4B | 官方支持 | bf16约11–16GiB，随视觉token/输出增长 | 专属venv、torch/transformers/Pillow/accelerate | 首选 | 官方模型卡/技术报告 |
| Qwen3-VL-8B-Instruct | 8B | 官方支持 | bf16约19–26GiB；4bit约10–17GiB | 量化需额外bitsandbytes兼容核验 | 原精度超预算风险；量化备选 | 同上 |
| 本地ThinkingGuard-8B | 8B | 架构支持，实测未知 | bf16约19–26GiB | 缓存完整性、加载方式未验 | 仅备选诊断 | 本地config |

固定官方revision：4B `ebb281ec70b05090aa6165b016eac8ec08e71b17`；8B `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b`。均Apache-2.0。[4B](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)、[8B](https://huggingface.co/Qwen/Qwen3-VL-8B-Instruct)、[官方技术报告](https://arxiv.org/abs/2511.21631)。4B文件约8.89GB；8B下载前需按固定树重新求和，预留20–25GB。两者不能用权重大小冒充峰值显存。官方支持量化生态，但本轮没有验证具体量化checkpoint或速度。

不需要特殊推理服务框架，优先Transformers直接调用。官方支持交错多图；未核得一个固定的最大图片张数，实际受上下文及视觉token限制。试验人为限制2图、每图≤512×512、batch1、输出512tokens，保持比例且不裁剪；这属于适配设定。输入分辨率下降可能损伤小图标/文字识别，必须记录。

| 方案 | 软件/模型 | 显存 | 磁盘 | 瓶颈/阻碍 |
|---|---|---|---|---|
| A 零GPU | Python标准库、HTTP、Git | 0 | 元数据与目录远小于10MB；论文缓存仅临时 | ZIP可范围读取；已完成 |
| B Guard验证 | 新建专属venv，4B或完整本地checkpoint | 目标≤16GiB，硬上限20GiB | 新4B预留12–15GB；当前不下载 | 先做两张无害图加载，再少量人工核验输入；峰值未知 |
| C 端到端 | Guard+Qwen编辑器+独立Judge | 分阶段串行，编辑器预算待实测 | 数十至上百GB，需单独核算 | 官方设置缺失，编辑与Judge成本高；仅计划 |

B尚未执行：没有已确认完整且符合基础模型比较条件的本地checkpoint；默认禁止大模型下载。下一轮若获准下载4B，先核验可用卡与共享调度，显式单卡device，避免device_map=auto跨卡；记录allocated/reserved峰值、耗时和token。任一峰值>20GiB、影响他人或6h预算将停止，不强行运行。无付费API依赖。
