# 原生 LLaVA Adapter 审查 · CPU 契约 PASS，真实运行未验证

| 口径 | 设计与实现 |
|---|---|
| A 论文 | A.7 的 Chat Intent 接文字、Visual 接图片，Safety 组合意图/图片/描述，QA 按判断走 A、B 或 C。Embodied 先提示定位相关环境状态，再把状态、同侧图片和指令交给 Safety Reasoning。 |
| B 发布代码 | 原生 Vicuna-7B、`llava_v1` 对话模板、本地图先 RGB/224×224、greedy、上限 512。发布调用链缺失和误接点保留在原快照。 |
| C 方法修复 | 保留 Stage 0 的模板与拓扑。Safety 新拼接的 `Image caption:` 是实现字段名。QA A 使用 safe 提示；B/C 依 A.7 追加 raw safety 提示。Stage 1 严格门槛会在无效判断时保存证据后停止，Stage 0 的默认 fallback 不变。两 Agent 用同侧图且第二步收到状态。 |
| D 本机运行 | 原权重、原生 class 与 builder。为离线绑定将内存中 `mm_vision_tower` 指向核验后的固定 CLIP 本地目录，源文件和模型文件保留发布字节。计划单卡 4-bit NF4/FP16 compute/双量化、batch=1、greedy、seed 0、默认上限 128。默认 `mssbench_224` 对应 B 像素策略，`native_anyres` 是独立配置并进入幂等键。本轮均未实际生成。 |

[ICLR A.7](https://proceedings.iclr.cc/paper_files/paper/2025/file/1cb57fcf7ff3f6d37eebae5becc9ea6d-Paper-Conference.pdf) · [发布 LLaVA 包装器](https://github.com/UCSB-AI/MSSBench/blob/1602193f49cb6925bfa3751be157d0bbf5439779/models/load_LLaVA.py)

CPU 测试用固定原生 `llava_v1` 模板渲染 text-only 与 image turns，并分别替换 Intent、Caption、Safety 输出验证后继渲染变化。真实 Adapter 才建立 vision tensor，Intent 不构造像素输入。Runner 对真实 trace 要求 0/1 个 image token、完整原始 Prompt/答案、按角色使用同一个模型实例、有效输出、角色依赖和 GPU 预算。保存 tokenized input 及第一轮实际嵌入序列长度、生成 token 数、图像原始和适配尺寸、模型加载次数及耗时。单次调用抽样 NVML 总设备占用并减空闲基线，另记录 PyTorch allocated/reserved 峰值；设备增量可能包含同卡其它进程，作为额外停止条件。

复用 SQLite，记录严格格式失败或进程中断前已提交的轨迹。CPU 测试模拟独立进程退出，重启跳过已完成键、保留中断尝试并重跑未完成输入。自然语言只按警示/拒答关键词粗筛，缺结构化输出保留 Unknown。输入分类方向和行为评分各自独立。 [实现](stage1_native.py) · [门控 Runner](stage1_smoke.py) · [测试](logs/stage1/tests.log)
