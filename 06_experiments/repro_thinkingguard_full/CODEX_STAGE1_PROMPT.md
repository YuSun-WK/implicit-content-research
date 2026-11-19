# ThinkingGuard｜Codex CLI Stage 1：历史保护、全Test manifest、官方解析器、受控 Pilot

你是 Codex CLI 执行工程师、NLP/MLLM评测复现专家和审计者。请**直接在服务器现有项目中执行**，不要把下面指令写成对用户的建议。仓库 `YuSun-WK/implicit-content-research`；工作分支 `repro/thinkingguard-full-20261119`；目标新目录 `06_experiments/repro_thinkingguard_full/`。本阶段上限：每个 GPU job ≤6h、进程显存安全预算20GiB、仅1块空闲4090/4090D、不用付费API；无法满足就停止在有证据的阶段，不得凭空报结果。

## A. 入场与只读保护（第一优先级）

1. `git fetch` 检查该分支；确认基于 `4eb98bee31a6182bcf8e1ee724679460da008686` 且包含 H1-K1、H1-K2、H1-K3。请先阅读 `06_experiments/repro_thinkingguard_full/R0_Evidence_Audit_and_Repro_Plan_20261119.md` **全部内容**；对照 `03_experiments/h1_k0_triggerbench/H1_K1_FORMAL_EXPERIMENT_REVIEW.md`、K2 Executive/Result Audit、K3 Preparation Report 和原脚本。
2. 为防止当前共享服务器未提交更改受影响，先 `git status --short`、列出 git worktree；如果旧工作树有工作内容，不执行 `git checkout/reset/clean/stash -u`、不覆盖、不rebase、不合并main。安全创建独立 `git worktree`，如已有目标且有改动只在新路径另建并报告。只写本分支新目录和自身日志。
3. 记录旧实验原始预测/指标/已冻结解析器的Git blob SHA和本地SHA256，输出 `artifacts/legacy_immutability.json`，全部结束前复测一致。不要改原数据或原标签。未完成的历史五步36对仍是NOT_RUN。
4. 本分支没有 GPU 前禁止修改系统环境；优先沿用现有Python虚拟环境和完整模型cache。禁止 `pip install -U` 改全局，必要时只在当前项目内建隔离env并冻结requirements（安装前写明变更）。

## B. 校准官方来源（CPU）

1. 作者官方 `https://github.com/FroggyChen/ThinkingGuard`，冻结commit SHA；读取 `inference.py` 中SYSTEM_PROMPT、聊天模板及参数，保留字节级原文/哈希。实际上官方repo当前可查仅README、inference.py、framework.png；如出现新训练脚本必须将相应commit入账，不要假设存在。
2. 通过 Hugging Face API读取 `Sandy124/TriggerBench` 和 `Sandy124/ThinkingGuard-8B` 的HEAD SHA、完整树、model/dataset cards；记录旧dataset revision `3ac26e778db94a282711f463f22ba6db99643bee` 和旧model revision `76892f9768ce828268265171f4bbc5dfb75eafc3`。若HEAD与旧版不同，先输出逐文件 `source_revision_diff.csv` / `source_diff.md`；以**单一固定revision**定义本轮正式实验，不默默混版本。
3. 检查作者正文 arXiv:2609.36562 的Table1/2/3及§4/5，尝试取得正式附件/补充材料并记录取得URL/sha；取不到标 `NOT_VERIFIED` 而非创作细节。不要把 GitHub README 概述误当成训练代码的公开证据。
4. 输出 `docs/source_audit.md` 和 `artifacts/source_snapshot.json`，必须有 URL、repoSHA/HFSHA、verified_at、access_status、文件类型与公开性；不把 token 写入Git。

## C. 生成全部 Test Manifest（CPU）

1. 使用冻结数据分割逐CSV读取（历史36 CSV资料可复用），严格构造Test全部868对 / 1736条。category mapping 包含 train `region_belief` vs test `religion_belief`，原字段不要丢。
2. Test manifest 一条一侧，保留 `pair_id,sample_uid,source_row,source_csv,split,category,side,ground_truth,text,image_source_path,image_local_path,image_sha256,image_decode_status,download_status,run_status`。`pair_id`应来自split/category/CSV标识而非图片文件数字（442对旧记录的CSV index和图片编号不同）。
3. 检查每对两个侧别齐全，text精确一致；重复文本/图像路径/原文件哈希/Train-Test交叠；如果当前HEAD与历史不一致，真实比对CSV、样本键、图路径及标签。按九类输出原始sample数、有效pairs数和缺失清单。
4. 使用本机已有HF缓存图片，下载仅缺失的当前Test资源且逐文件核验；不得批量下载全部Train图像，不得重新下载已存在且哈希通过的文件。没有已发布checksum的图像要记录本次哈希，不冒充官方checksum。若网络不可用，生成状态表并停止后续GPU，不能跳过。
5. 导出 `artifacts/manifests/test_manifest.csv`、`test_manifest.sha256`、`data_validation.json`、`leakage_audit.json`；不上传原始图像/模型。

## D. 把官方五步协议从旧 parser 中单独复现（CPU）

1. 首先**完整阅读**旧 `official_parser_v2_frozen.py`、`parser_freeze.json`、`development_audit.json`、`validation_official/predictions.jsonl` 和4条人工转录结果。直接复用思想，但新代码命名 `official_parser_v3.py`，不能替换旧文件、不能复制旧指标并声称新实验。
2. 严格采用作者 `inference.py` SYSTEM_PROMPT，与五个结束符 `<|/Intent|>` `<|/Entity|>` `<|/Attribute|>` `<|/Risk|>` `<|/Overall|>` 和 `max_new_tokens=1024`。按作者文字每步输出，保存每段原始字符串、起止位置、是否缺失/重复/空/错序，整体结构与最终判定单独统计。
3. 最终分类只允许在唯一 `Overall` 段存在**唯一明确的最终结论**时提取。 `[Safe]/[Unsafe]` 是二选一占位模板，必须 `INVALID(AMBIGUOUS_TEMPLATE)`。不能看真实标签、pair侧别、前4段中的Safe/Unsafe去猜。即使最终段可读、前四段残缺也需保留明确 `structure_complete=false`，不要混同解析成功与五步正确。
4. 加pytest测试至少覆盖：五段全有、无Overall标题但固定intro、裸Safe、[Unsafe]、重复结束符、乱序、空段、完整双标签模板、多个不同结论、截断末尾、尾随噪声、含词“safety”的假阳性；还要保证 `parse(raw)` 只有 raw 参数，导出 `parser_version/parser_sha256/tests_sha256`。
5. 官方代码未公开解析器，不要命名 `official_author_parser`，应命名 `reproduction_parser_v3` 并区别于作者prompt。
6. **不得**在看新的独立验证结果后修改原A0 parser规则。若需要放宽或引入额外末尾指令，创建独立 `A1_REPAIRED` prompt和新parser版本/验证集，A0原结果保留。

## E. 模型cache与GPU安全门槛

1. 重用旧 `audit_model_cache.py` 核验 `Sandy124/ThinkingGuard-8B` 四 shard哈希、每个tensor index/大小/header；旧修复问题涉及官方权重Map里118个tensor分片位置，若本机缓存已修复，则必须记录官方和本地索引SHA、provenance；**无权重字节变化**才可引用旧权重对应关系。如失败，不下载全模型替代缺文件前先报状态。
2. 读取 `nvidia-smi` 并检查允许使用GPU，**绝不终止其他人的进程**。按现有H1记录修复PID监控：PID无法映射=不可用/保守fail，不是假0；记录整卡和进程区别、PyTorch峰、显存采样峰；进程20GiB安全上限，CUDA alloc cap可设18GiB留余量。
3. smoke 采用6条以内、包含不同类别与safe/unsafe；先固定prompt hash、model SHA、processor SHA、quant、torch/transformers/CUDA、seed、decoding、1024 tokens、图像预处理配置。保持 `BF16原作者设置` vs `NF4预算适配` 两个命名；本轮默认NF4以符合20GiB预算，不声称数值等同原论文。
4. 对Smoke保存完整原始输出、token统计、elapsed、GPU日志；任何一条生成失败也记FAILED不删除。先检查有无输出超过1024token导致截断，以及粘贴双标签模板的发生率。
5. 固定解析器后，在未用于旧parser开发的Test中冻结一批新解析验证样本（建议18对，九类各2对），只看raw文本、不看GT进行结论转录。独立匿名复核最好由两人，若无人可用明确写 `independent_human_review=NOT_RUN`。A0准确率不能拿来调解析器。
6. 解析成功率门槛是最终**唯一结论提取率≥95%**，五段结束标记覆盖率另计。未过则本轮不跑100/300/868对的A0；出具 FAIL 报告、固定歧义例子和A1实验提案（不要偷偷按改后prompt续跑A0）。
7. 资源门槛：预计单任务Wall≤6h（尽量将 `max_wall_seconds=19000` 预留收尾）；显存≤20GiB；网络/磁盘充足、无抢占其他人进程；失败自动保存已完成JSONL、可恢复队列。

## F. 100对 Pilot：仅在上述门槛通过后

1. 在冻结Test manifest上，根据预先公开的 `seed=20261119` 生成Pilot样本名单，九类近均衡，**优先选择尚未用于官方A0解析开发的独立pair**。如总体分层抽样，保留类别和全局顺序。100对是200图文输入，并非100行。
2. 先测量真实8–12条最坏/典型图像延迟的P50/P90/P95；用P95加安全边界来决定单作业最大条数；如200条本次放不下就拆成可恢复小批，不能为赶100对突破6h。
3. 运行 `A0_AUTHOR_PROMPT_NF4`，存 `runs/<runid>/predictions.jsonl`，每行 `run_id,sample_uid,pair_id,side,gt,model_sha,prompt_sha,parser_sha,status,raw_output,steps,parsed_verdict,elapsed,generated_tokens,image_sha`；原始输出原样保留；同键重启跳过，写盘原子且校验总记录/重复。不要用生成失败样本的跳过机制篡改最终分母。
4. Pilot必须产出九类 micro/macro F1、Accuracy、Unsafe Recall、FPR/FNR、PairAcc/反向翻转/两侧Safe或Unsafe、INVALID和wilson95、cluster pair-bootstrap；还需 `valid-only` 和 `strict-full-denominator`并列。若Pilot出现差性能，**不要为提高Accuracy调prompt或选子集**，如数据/解析/GPU完整就仍可推进更大规模。
5. 如上层门槛未过，Stage1应停止在已完成的最小阶段，不虚构100对指标或GPU数据；`NOT_RUN`不得输出零准确率。

## G. 交付和复核

- 最低输出：`docs/source_audit.md`，`docs/dataset_model_manifest.md`，`docs/parser_design.md`，`docs/protocol_comparison.md`，`configs/author_five_step_nf4.yaml`，`scripts/build_test_manifest.py`，`scripts/official_parser_v3.py`，`tests/test_official_parser_v3.py`，`scripts/run_resumeable_inference.py`，`scripts/evaluate_pairwise.py`，`artifacts/manifests/*`，`runs/<id>/*`及`STAGE1_EXECUTION_REPORT.md`。
- Git先提交CPU与无GPU测试结果，然后将本阶段GPU日志真实结果另commit；原始图片、模型权重、缓存、HF token、用户私有映射等大件不得提交。gitignore要精准避免把预测、可重算统计报告一并误忽略。
- 代码必须能在 `--dry-run` / `--preflight-only` 模式不占GPU，`--resume`安全，参数哈希冲突时拒绝合并；重复key fail，`INVALID`显式保留。
- 汇总严格按照 `DONE / PARTIAL / BLOCKED / NOT_RUN` 四状态，附真实运行命令、完整版本、commit、SHA、测得P50/P95/GPU峰、实际预测数、九类有效性、解析失败示例、受保护旧文件哈希对照；列明下一步从100→300→868的预算门槛，**本阶段禁止擅自启动300/868以及训练**。
- 若GPU/网络暂时不可用，不要一直阻塞；尽量完成CPU审计、manifest、解析器及测试，报告无法运行的具体缺口。不要让缺失资源变成虚构的结果。

**核心任务：保护旧实验，建立真实full Test Manifest，解决官方五步输出解析可验证性，只有通过数据/解析/资源门槛才跑100对Pilot。**
