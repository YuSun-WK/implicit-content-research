# Codex CLI 首个任务｜MSSBench Stage0：CPU数据/代码审计，不启动GPU

你是 ICLR 2025 CCF-A Reproducibility Engineer。任务是为 Multimodal Situational Safety / MSSBench 建立可复现的 Level 0 核验基座，不允许启动大规模GPU任务。
工作仓库：YuSun-WK/implicit-content-research，工作分支 repro/mssbench-multiagent-20261119，工作目录 06_experiments/repro_mssbench_multiagent/。绝不覆盖、清理或影响其它实验，不合并 main；遇到未提交改动先检查并保护。

## 阅读顺序
先阅读本目录 00_SCOPE_AND_TEACHING.md、01_SOURCE_CODE_AUDIT.md、02_DATA_MODEL_RESOURCE_PROTOCOL.md。
然后阅读已有的 03_survey/R2_literature_extension/B4a_reading/R2B_B4a_01_Multimodal_Situational_Safety.md 和 03_survey/R2_synthesis/B4a_Cross_Paper_Synthesis.md。
官方论文：https://openreview.net/pdf?id=I9bEi6LNgt
官方源码：https://github.com/UCSB-AI/MSSBench
源端审计 HEAD: 1602193f49cb6925bfa3751be157d0bbf5439779
HF 数据：https://huggingface.co/datasets/kzhou35/mssbench

## Stage0 任务清单
1. 检查 git status、所在 branch、提交 SHA；建立官方源码只读快照/或 vendor 目录的固定 commit 记录；只写本项目目录。
2. 逐文件建立审计矩阵：inference.py、utils/infer_on_data.py、utils/infer_on_multiagent.py、utils/prompts.py、utils/gpt4_eval.py、models/*.py。通过 python -m py_compile 或 ast.parse 验证原始代码问题，区别 SyntaxError、ImportError、RuntimeError、语义不一致；不得把已有文件当成可运行证据。
3. 新建 repair_log.md，将每项修复列出原行号、B行为、C修复、语义变化、证据。提供纯 Python、无框架、单模型复用的接口设计；先不加载大型权重。可写假的 MockVLM 模型，用字符串探针验证 Intent/Caption/Safety 输出确实被下游使用；测试 Chat 开源4-agent/Embodied 2-agent。C 与 D 不混。
4. 先从 HF 只下载 combined.json（记录完整 revision 和 SHA256）；读取完整字段，给出 JSON 记录数、Chat查询展开数、Embodied多指令展开数、safe/unsafe输入数、pair数、类别分布、文字同一性、重复 path 和实际同一图片依赖情况；输出 manifest.csv / data_audit.json / data_audit.md。由于尚未下载所有图片，不要谎称图片已经有效解码；本阶段可只按20对清单定向获取需要的图并核验 PIL。
5. 检查目录内是否已有模型缓存及原始数据，不重复下载；hf_hub_download 或 hf download 应按具体文件和 revision 取回，禁止 clone 全部图片；记录 df -h、free -h、nvidia-smi、CUDA_VISIBLE_DEVICES、可用显存及潜在冲突，不实际分配 GPU。
6. 对论文 LLaVA-1.6 Vicuna-7B 先核查官方可下载路径、模型权重版本、源仓库 LLaVA adapter 旧依赖/224 resize的差异、4bit可行性。给出原版本隔离依赖建议、Transformers转换版能否兼容的可验证计划；**不要下载14GB模型**。若需要后续使用 trust_remote_code，记录安全/版本检查。
7. 建立输出 schema（每个 run 保留模型revision、图像sha、调用阶段、raw prompt、raw answer、parsed、耗时、token估算、峰值显存、error），定义幂等 resume key；提供最小 mock test、缺失文件测试、反向 Yes/No 解析测试、非法输入测试。
8. 将 IF 输出行为 Judge 和 QC/IC 输入二分类评分代码分开；本阶段只完成评测程序规格和单元测试，不调用任何 GPT/Claude/Gemini API。
9. 建立 resource_budget.md（物理/可用显存、磁盘、cache、依赖）和 execution_matrix.csv，必须把估算与实际数据分栏。
10. 运行 CPU tests 及数据脚本，汇总正确执行命令、失败详情、证据；提交到当前分支并记录commit，提出 Draft PR供审阅但不要合并。

## 严格限制
- 本阶段禁止 pip 大规模重装、HF 全仓下载、GPU模型加载、任何训练、商业API、启动Full。
- 对原本有 SyntaxError 的文件，可复制进入隔离的 original snapshot 并记录原始错误；不要无记录直接“修好原版”。
- 不写伪造数据指标。所有「论文目标数」「HF网页规模」「本地实测数」严格分开。
- 所有文件路径禁止绝对 root 写死；环境变量设置缓存路径，解析路径必须限制在数据根目录内。
- 若发现数据版本与论文不一致，先列证据/影响和可复现实验范围，标记 STOP，不静默删样本。
- 所有功能应支持单GPU、batch=1、写入后断点续跑，但 Stage0 不运行GPU。

## 必须交付
README/SourceCode_Audit/Repair_Log/Data_Audit/Resource_Budget/Model_Compatibility/Eval_Protocol/Execution_Matrix/Mock_Tests/Test_Logs/Stage0_Gate_Report，明确每一项 PASS/PARTIAL/FAIL，记录来源 SHA 和机器环境。报告要能够让我直接决定能否进入 Smoke Test。

完成后给出：改动文件清单、运行命令、实际统计、尚未解决P0、估算存储/显存以及唯一建议下一步。不要只说“任务完成”，不要启动 GPU。