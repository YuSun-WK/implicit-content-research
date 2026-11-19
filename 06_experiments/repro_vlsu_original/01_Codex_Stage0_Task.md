# 给 Codex CLI 的 Stage 0 任务｜VLSU ICLR 2026 原论文忠实复现

你负责在仓库 YuSun-WK/implicit-content-research 中完成 VLSU **Stage 0：证据锁定、复现协议和CPU数据审计工具**。严禁训练、GPU推理、4-bit方案先行、跨数据集迁移或任何新方法。严禁改动综述、H1及PR #78规划。

## 首先定位现有资料
1. `git fetch origin`，切换现有远程分支 `repro/vlsu-original-20261119`（如本地分支已存在则更新/核对，不强制reset或覆盖别人的工作）。
2. 先读 `06_experiments/repro_vlsu_original/00_Stage0_Source_Protocol_Audit.md`，再读主分支 `01_literature/cards/P038_VLSU.md`。
3. 阅读正式版 https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf 的§2-5、Figure 3/4/5、Table1/2/3/4、附录A（Fig9, Table7）、附录D.1/D.2/D.3/D.4（Table10）、附录E、附录F.2。读PR#78头分支的 `06_experiments/VLSU_research_plan_20261118/01_Current_Research_Audit.md`，不得假设它在main。
4. 官方代码数据源 https://github.com/apple-aiml-research/ml-vlsu ，固定初始HEAD `cbe363a26d2129ff1b526c283af0a2b7aa3d9b28`；数据Blob `09421adeb2e68eac1d5e829dcbd48848f21a0be6`。若上游已变化，先记差异，不静默升级。
5. 逐字核对D.1（二分类/三分类）和D.3（Structured CoT）提示词。Prompt必须从正式PDF原文提取/校验后以TXT文件保存，并注明会议正式版页码、PDF SHA256、人工核对状态；不要使用arXiv旧版替代。D.2是GPT-4o Judge的提示，不是Table3被测助手的Helpful行为指令。

## 编写审计报告（不给无依据的确定性）
在本目录新增 `protocol/Original_Experiment_Matrix.md`：逐行列Table1、2、3、4、Figure3、4、5、Appendix E，任务、输入模态、gold字段、二/三类映射、prompt文件/位置、被测试模型、生成参数、样本数、F1定义、指标、作者报告值、官方是否提供脚本、本地复现状态、缺失信息。标注 AUTHOR-REPORTED / VERIFIED-OFFICIAL-CODE / LOCALLY REPRODUCIBLE / PARTIAL / UNKNOWN / NOT RUN。所有作者数值指向论文页/表，不要捏造。
纠正：Figure3 才是17类组合准确率；Figure4是joint与单模态预测的关联/混淆；Figure5是joint错例四分法。Qwen7B Table1 binary 50.0/55.3，Table2 direct 49.4/42.3、CoT 52.1/51.4，Table4 image65.2/48.0、text60.3/44.2、joint49.4/42.3（依次Acc/F1，单位百分比）；如果复读PDF发现冲突，以证据写冲突，不覆盖原文件。

## 关键不可假定的细节
- Table1 只针对binary：S/B→Safe，U→Unsafe，必须使用binary Prompt；三类预测事后折叠不是作者原流程。
- 三类E1分别用 `image_grade`、`consensus_text_grade`、`consensus_combined_grade`；不能用joint label测unimodal。
- image `not_sure` 不映射Borderline；保留其joint评测资格；涉及三侧正确性的条件统计仅能在三标签均有效的UUID交集上做。
- Table2和Table4作者F1平均方式、输出parse-fail处理若论文未明确，请写 UNKNOWN 并并列建议本地输出macro/weighted/per-class，作者原F1不得直接标为Macro-F1。
- Table10 Qwen是 `Qwen/Qwen2.5-VL-7B-Instruct`，direct最大输出长度文中1024，CoT2048，图像参数“min=256,max=1280”必须核查源码中的单位换算；温度作者对Qwen写“default”，**不准把0.0冒充原设置**。原实验HF revision/processor/随机种子/chat-template等缺失则写 UNKNOWN，并为本地独立选项留配置但不可填造作者原值。
- D.1的三类模板明确出现image and query；论文没列unimodal专用逐字模板时，不得发明并称原文，应记录E1单模态包装协议缺口。

## CPU数据验证工具（严谨、无损）
实现 `scripts/stage0_audit_csv.py`，支持 `--csv /path/VLSU.csv --out reports/stage0`，只做CPU审计，不联网抓图、不修改CSV。输出 `dataset_audit.json`、`patterns.csv`、`schema_errors.jsonl`、`version_manifest.json`，另附Markdown简报。正确处理CSV引号、Unicode、逗号及空值。原文件按字节SHA256，行数、九列、UUID唯一、URL唯一、prompt唯一、字段级空值、三标签分布、not_sure、27标准组合+额外问号模式，逐表输出；记录各实验的**理论上限分母**，不可写成图片实际可用分母。完整样本级失败清单本地保存但不要提交带用户内容/第三方版权数据。官方初始CSV应验8159行、8159UUID、8157URL、7638 prompt、141 not_sure、19常规组合+6含问号、25总组合；任何偏差中止并报告，不要自动修补。
标注17论文标准模式与两个发布额外单例B-S-S/S-U-B；加模式S-S-U35、S-S-B58、U-S-B924、U-S-U142、B-B-U32检查断言。可以选用 `pandas` / 标准库，避免重依赖；将网络下载另留 Stage1 设计，不执行全量图片下载。

## Stage1 下载器**设计文档**（本阶段不开始下载）
写 `protocol/Image_Download_Design.md`：按UUID+URL追溯、断点续传与重试原因、有限并发和每host限速、Retry-After、超时、字节上限、最大解码像素、MIME/PIL验证、hash与去重、下载和解码失败分别计数、final URL/redirect、内容改变记录、私有网络地址/localhost/非http(s)拦截（防SSRF）、不要绕过403或版权限制。图像只放.gitignore路径，绝不提交或用失效URL的替代图片静默补齐。

## 运行配置与评估设计（Stage0只写配置，不加载大模型）
- 新增 `configs/official_qwen25vl7b.yaml`：model id，HF revision **待下载时固定**，tokenizer/processor revision，precision原始BF16、量化4bit为可选resource_constrained，pixel budget原文/解析状态，原文default temperature未解析，binary/direct/CoT三套prompt SHA256与max_new_tokens，seed/采样/beam停止条件显式留空待证。不得填伪造的original参数。
- 新增 `protocol/Output_Parsing_and_Metrics.md`：binary严格Safe/Unsafe；direct严格Safe/Borderline/Unsafe；CoT只能解析最终[Final Classification]字段；raw_output单独保存，parse_fail为INVALID（不能被模型回答中的关键词误报）；整体指标主分母含invalid并额外报告valid-only；all三类P/R/F1、macro/weighted、混淆和解析失败。设计在同UUID intersection上比较两种prompt，不通过丢弃难样本提升指标。E4 小组Wilson CI；E6两个不同条件概率；Figure4 逐模态×joint的混淆和Cohen κ。报告无图样本覆盖，作者指标另列。
- 将模型加载和量化方案拆为 ORIGINAL PAPER、LOCAL UNQUANTIZED、LOCAL 4BIT，说明本地16–20GiB只是预算、未实测；不要运行GPU。列出E1/E2/E5全量理论40654次生成及共享GPU分块≤6h的停止/恢复设计。

## 测试、验收与提交
- 单元测试：CSV带引号/空值、重复UUID、意外标签、not_sure掩码、二类B→Safe、CoT最终行解析、unsupported标签、空输出、Figure5分母/zero-denominator、缺图时denominator保持。没有完整parser实现也至少将测试规范和预期写明，不允许虚报PASS。
- 运行CPU审计、pytest（如有）和git diff --check；记录运行命令、真实stdout、Python依赖/版本、任何错误和缺失文件。未拿到CSV时用fixture测试但明确标 NOT VERIFIED，不能以PR#78数据代替本机实测。
- 提交只包含此独立目录下审计文档、prompt、configs、代码/测试和可公开聚合报告、.gitignore变更；不得提交图片/模型权重/原始CSV/敏感完整模型输出，不动旧目录；提交分支 `repro/vlsu-original-20261119`，**不合并main**。
- 最终在终端简报：commit SHA、改动文件、每项实测/未实测、完整协议缺口清单、可复现的命令、Stage0是否PASS、Stage1能否开始的gate。没有源证据的参数一律UNKNOWN；若审计不通过，应BLOCK而非跳至GPU实验。
