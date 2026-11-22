# 官方源码独立审计｜静态证据与修复语义（2026-11-19）

审计源：UCSB-AI/MSSBench@1602193f49cb6925bfa3751be157d0bbf5439779。当前只核对远端原文及其调用链；未在目标 GPU 服务器执行原仓库。语法错误可直接由源码确定；实际导入/推理结果仍由 Codex Stage0 的 compile、mock 验证。以下所有位置按官方 main 文件行号。

## 阻断项

| 源位置 | 可直接检查的行为 | 分级 | 推荐处置与语义影响 |
|---|---|---|---|
| utils/infer_on_multiagent.py:14 | elif 比 if 多一格缩进，Python Syntax/IndentationError | P0 | 修缩进；语义不变 |
| utils/infer_on_data.py:10, inference.py:5 | 基础 inference 顶层导入坏的 multiagent 文件，因此连 IF 也可能被阻断 | P0 | 修语法并使模块可导入；语义不变 |
| utils/infer_on_multiagent.py:8 | from prompts import *，真实路径 utils/prompts.py | P0 | 改绝对包导入；语义不变 |
| utils/infer_on_multiagent.py:18,22,26 | chat_response/embodied_response 用未传参的 model；embodied 内含未定义 safe_image | P0 | 显式传 model/image；语义不变 |
| utils/infer_on_multiagent.py:65,69-71 | 主循环引用尚未定义 safe_imge, unsafe_imge, safe_image, unsafe_image | P0 | 每个 embodied 记录显式拼路径；语义不变 |
| utils/infer_on_multiagent.py:57-59,75-77 | os.makedirs(output_path) 把应为 JSON 文件的路径建成目录，随后 open 写文件失败 | P0 | 创建 dirname(output_path)，原子写文件；语义不变 |
| inference.py:18-33 | 仅设置 if/qc/ic/ic_cap，无 cot/multiagent/gt-cap 分支；main 根本不调用 test_multiagent | P0 | 新建显式任务调度器；新增有效运行入口，不冒充作者原样实现 |
| utils/gpt4_eval.py:1-15 | 需 AzureOpenAI，空 api_base/api_key/deployment；模块在导入时初始化 client | P0 | 推理与评分解耦，关闭网络，单独实现 local judge；评价协议改变，属 D |
| inference.py:20 | 固定读取 combine.json，但 HF 有 combined.json | P0 | 别名探测并记录实际文件名；语义不变 |

## 方法语义差异（比程序崩溃更严重）

| 源位置 | 公布代码行为 | 修复后的要求 |
|---|---|---|
| infer_on_multiagent.py:40-44 | 计算 safe_intent/unsafe_intent，但 Safety Agent 用原 query，不用意图结果 | Safety 输入解析后的 Potential intent activity，记录原文和解析 |
| infer_on_multiagent.py:40-47 | 完全没调用 Visual Understanding，也没将 Caption 喂给 Safety | Chat 开放模型必须真正产生 caption 并传给 Safety（论文四代理） |
| infer_on_multiagent.py:11-18 | 根据判断设置 QA prompt，但 return model(img, query) 直接丢弃 prompt，且未用 safety_output | QA 必须接受选中的模板+query，记录路由及判断证据 |
| infer_on_multiagent.py:26 | unsafe_vf 错误地用 safe_imge，导致 unsafe 环境状态从 safe 图提取 | unsafe 侧应使用 unsafe image；否则改变了视觉证据 |
| infer_on_multiagent.py:21-30 | 两 Agent 辅助函数未显式绑定调用实例/图片；输出轨迹未保存 | 传参和日志化；保持两代理结构 |
| utils/prompts.py:45-62 | 定义 Chat/Embodied CoT Prompt，却无运行入口 | 提供一调用 CoT 实验入口 |
| utils/prompts.py:64-78 | 定义 Intent、Safety、QA、Embodied prompts；没有独立 Visual prompt 常量 | 按论文 Appendix A.7 原样加入 Visual prompt，并校对终端标点/拼接 |
| infer_on_data.py:19-77 | IC_CAP 使用作者现成 caption 只给 Chat unsafe，不给 safe；没有 self-caption 推理步骤；IF/QC/IC 全走相同 Judge | 拆分 IC+GT（oracle）与 IC+Self（额外模型调用）；QC/IC 直接解析 Yes/No |
| infer_on_data.py:57-67 | Embodied IC 的 safe/unsafe 两侧可能用不同 instruction；同时保存的 prompt 与实际 unsafe prompt 不一致 | 忠实记录左右输入，标记是否同 instruction；不能盲认「只换图」 |
| utils/gpt4_eval.py:50-69,96-196 | Judge 只见回答，看不到原图和原 query，提示还预设活动是危险的；Safe 2/3 正确，Unsafe 0/1 正确 | 完整保留官方 0–3 rubric 作为被审计协议，另建本地代理评分与人工核验，不宣称分数相同 |
| models/load_MiniGPT4.py:114-125 | import 阶段跑绝对路径 sample；覆盖 sys.argv，初始化配置混乱 | 原模型兼容修复应隔离为独立 adapter，避免 import 副作用 |
| models/load_mPLUG_Owl2.py:68-74,88-94 | 导入时重复加载模型、直接推理缺失 image.jpg；call_model 被二次定义 | 去掉副作用、单次加载；行为变化记录 |
| models/load_LLaVA.py:40,50-56 | 本地图片被强制 resize 为 224x224；原始 LLaVA-1.6 高分辨率视觉处理可能因此受影响 | 先保持 B 原行为作为对照；高分辨率 C 修复的忠实性需单独定性，不能静默改变 |
| models/load_Qwen_VL.py:15-16 | Qwen/Qwen-VL-Chat 信任远程代码，依赖旧版 Transformers | pin 依赖、记录 trust_remote_code，不静默升级模型 |
| models/load_deepseek.py:10-15 | bf16 CUDA 直接加载 7B，16–20GiB预算存在风险 | 优先兼容性检测，不直接下载多份模型 |
| models/load_GPT4o.py / load_gemini.py / load_claude.py | 依赖商业 API key | 本地无付费 API 协议不运行 |

## 审计裁决

B（原公开 multi-agent 脚本）不是已验证可运行实现；更不能用它证明 A（论文四代理链）已实现。C 需要建立逐 Agent 输入输出的真实依赖，且加单元测试断言：若替换 Intent/Caption/Safety 的输出，后继输入会相应改变。D 只允许在清楚标记量化、模型包装器、图片处理、解码、Judge 等差异后报告。

修复日志必须至少含：问题ID、原路径/行号、原始行为、修复diff、新调用轨迹、是否改变论文方法语义、验证测试结果、Git SHA。