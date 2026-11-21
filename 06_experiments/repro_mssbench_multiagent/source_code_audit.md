# Source Code Audit · PASS

审计固定在 UCSB-AI/MSSBench 的 `1602193f49cb6925bfa3751be157d0bbf5439779`。开始时实验分支干净，基线提交为 `58bf2497c07c071ed2ac6d8bd9f1af89894a97cd`。官方快照独立检出，保留原文件。使用 `inspect_source.py` 校验提交和工作树并调用 Python `compile`。所有模型适配器仅编译、静态阅读。 [官方快照](https://github.com/UCSB-AI/MSSBench/tree/1602193f49cb6925bfa3751be157d0bbf5439779)

| 文件 | 分类及结果 | 证据 |
|---|---|---|
| `inference.py` | 编译通过。L7 导入基线，目标默认环境先报 `openai` 模块缺失，隔离 Judge 后暴露多 Agent 缩进错误。L26、L31–37 缺 CoT、多 Agent 和独立 caption 入口。先导入模型再读 `combine.json`，而发布文件名是 `combined.json`。 | 实际导入、隔离导入、源码与 HF 文件清单 |
| `utils/infer_on_data.py` | 编译通过。L6、L11 串联 Judge、多 Agent。L34–46 的 IC+caption 仅给 Chat unsafe 侧发布文本。L69–84 给两侧各自的单条指令，但只保存 unsafe 侧 prompt。L86 的 zip 遇到不等长会截断。L62、L99 依赖已有输出父目录，L101 对所有模式调用回答 Judge 且切片可选的 `output_path`。 | 实际导入、隔离执行、静态 |
| `utils/infer_on_multiagent.py` | L14 `IndentationError`。仅修缩进后 L8 `ModuleNotFoundError`。隔离执行复现缺少 `model`、`safe_image`、`safe_imge` 绑定和目录当 JSON 文件写入。L40–47 丢弃 intent、缺 caption；L18 丢弃 QA 模板；L26 从 safe 图提取 unsafe 状态。 | 实际编译、隔离执行及回调探针 |
| `utils/prompts.py` | 编译通过。定义 IF/QC/IC、CoT 和角色模板。L45–62 CoT 无入口，L64–78 缺独立 Visual 模板。论文 A.7 提供 Caption 文本及 QA B/C 的安全评估字段。 | AST、程序入口、论文 A.7 |
| `utils/gpt4_eval.py` | 编译通过。L1–15 需要 `openai`，空配置下在导入时构造 Azure 客户端。L18–20 把 API 版本字段传给 `model`。L34–57、L96–158 评分仅见回答且预设情境有风险。异常跳过整对。两类任务分开计分。 | 实际导入缺包、静态，无 Azure 调用 |
| `models/load_LLaVA.py` | L4–20 依赖 LLaVA 项目包。L34–40 本地图缩为 224×224，远程图与本地图路径处理不同。L50–56 导入即加载，L68–71 greedy 上限 512，L118–123 图像与文本设备放置方式不同。 | 编译、静态、环境元数据 |
| `models/load_MiniGPT4.py` | L76–92 依赖后端 globals，L115–117 顶层执行绝对路径样例，L125 覆写 `sys.argv`，L151–165 再初始化并重定义接口。 | 编译、静态 |
| `models/load_mPLUG_Owl2.py` | L68–74 加载后立即运行 `image.jpg` 示例，L88–94 再加载模型并重定义 `call_model`。 | 编译、静态 |
| `models/load_Qwen_VL.py` | L15–17 导入即加载权重，使用未固定版本的 `trust_remote_code` 和 CUDA。 | 编译、静态 |
| `models/load_deepseek.py` | L3–4 依赖独立项目，L10–15 导入即加载并转 BF16/CUDA，启用未固定版本的远程代码。 | 编译、静态 |
| `models/load_GPT4o.py` | L11–23 依赖 Azure SDK、认证和部署配置；L39 起走服务调用。 | 编译、静态 |
| `models/load_gemini.py` | L2–9 顶层配置 SDK 和模型；L12 起走服务调用。 | 编译、静态 |
| `models/load_claude.py` | L1–15 依赖 Anthropic SDK 和密钥；调用构造图像输入。 | 编译、静态 |

13 个 Python 文件中 12 个通过编译。实际导入、隔离探针与静态发现分别标在表中。既有审计的两处细节已校正。IC 分支保存的是 **unsafe** 模板，缺失的是 safe 侧实参；Embodied 的原版辅助函数确实把抽取的状态拼进第二步，只是 unsafe 侧用错了图。

[编译与隔离运行](logs/source_checks.log) · [目标环境实际导入](logs/original_import.log) · [修复对应表](repair_log.md)
