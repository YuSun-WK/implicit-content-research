# VLSU｜Stage 3A 双轨提速：真实预测质量复核 + 30 UUID 全配对 Pilot + 可用图片恢复
**日期：2026-11-21；依赖 HEAD `83b8639883722d1af53209cc7c387b8cddb24766`。目的仅是忠实复现 ICLR 2026 VLSU 原论文实验，不做新模型、SFT、迁移或方法创新。**

## 0. 必须先读取的当前证据
仓库 `YuSun-WK/implicit-content-research`，分支 `repro/vlsu-original-20261119`，实验根目录 `06_experiments/repro_vlsu_original/`。读取
- `reports/stage2work/Execution_Report.md`, `Execution_Metrics.json`, `Model_SHA_Audit.json`
- `Run_Stage2.md`, `configs/stage2_smoke.yaml`, `configs/stage2_model_files.json`
- `scripts/stage2_qwen_smoke.py`, `scripts/stage2_roster.py`, `scripts/stage0_metrics.py`, `scripts/stage1_manifest.py`
- `protocol/Original_Experiment_Matrix.md`, `protocol/Output_Parsing_and_Metrics.md`, `protocol/Stage2_Deviation_Ledger.md`
- `reports/stage1r/Stage1_Image_Coverage.md`, `reports/stage1r/Move_Resume_Instructions.md`, Stage1下载器；PR #78 `06_experiments/VLSU_research_plan_20261118/01_Current_Research_Audit.md` (此前另一个实验环境有132 URL请求/108次成功，**未证明其缓存还存在**)。

已获证据：五个完整官方Qwen权重SHA通过，固定HF revision `cc594898137f460bfe9f0759e9844b3ce807cfb5`，BF16单卡无OOM；Direct10、Binary5、CoT5 均真实成功，parse 20/20；并不等于模型正确或作者原表已复现。模型文件已在GPU服务器，禁止重复下载。报告推理脚本 SHA256 `36b748e941f164e92a6e2cca984da4eda15daffa8a8f26906450bf87c8d393cd`；验证本地实际脚本与报告一致。原始生成和SQLite只存服务器私有`.local/stage2/<run_id>/`，未上传GitHub，云端摘要不能替代原始记录。
数据公开版8159，作者论文8187，Stage1成功解码URL 28、Joint UUID 30（0.37%）；Image-only gold+image 23，S-S-S和U-S-U当前0个成功解码。PR78先前108/132成功来自另一抽样与Windows环境，不能将其算进当前30。

## Track B（立即执行，GPU约束保持不变）：从20条Smoke进入真实可评分30条配对Pilot
### B1 原始20条正确性审计（CPU）
- 用服务器已授权私有目录读三个run_id的原始`raw.jsonl`、`parsed.jsonl`、`run.sqlite`、`run_spec.json`与`summary.json`；核对run_id、UUID、gold、prompt_sha、image_sha、模型revision、脚本hash和真实raw/parsed数量；与GitHub`Execution_Metrics.json`核对。不要提交原文或原始生成。
- 注意Direct10总生成20 tokens、Binary5总生成10 tokens：100% parse valid只说明格式正确；计算各arm真实预测类别分布、混淆矩阵、Acc、Macro-F1、Weighted-F1、各类别P/R/F1，展示invalid count（含真实生成失败与不合语法输出）和sample IDs总数、是否常量预测/过度预测Safe。所有这些只可标`ENGINEERING_SMOKE_DESCRIPTIVE`，小样本不与作者49.4/42.3、52.1/51.4做统计复现结论。
- Direct/CoT的作者表2对照限S/B/U同一Joint gold；Binary要单独把S/B→Safe、U→Unsafe。Direct10 vs CoT5不能作为完整同N配对，必须先用Direct前5同UUID子集比较，并明确分母5。若脚本record关键信息缺失/私人原始输出不可访问，报告阻断，不能推断结果。
### B2 快速完成N<=30的新冻结全配对Pilot
- 维持原10 UUID工作快照和原始GPU Smoke run_id完整不变；建立单独Stage3 config/manifest快照，新的run_id。可用且校验成功的全部30 Joint UUID作为上限；如当前服务器实际可读数不足，N取真实上限，列出原因。用于joint Direct、joint Binary、joint Structured CoT，三arm使用**完全相同的N个UUID**，按固定seed与官方CSV制定可追溯顺序；务必保留7个image_grade=not_sure的Joint有效标签，只有Image-only时排除。
- 禁止因预测是否成功或是否正确再挑选UUID。Stage2旧run可作对照，Stage3必须独立新run_id/快照，不能用旧统计冒充新增运行；可最小复用脚本、调整独立配置，不推倒重写。
- 单卡、BF16、batch1、20GiB PyTorch allocator、每作业<6h、共享GPU空闲检查。作者PromptSHA不变，Direct/Binary max_new_tokens 1024，CoT 2048，拒绝悄悄短输出或改量化、像素预算。模型 revision和完整文件hash不变。若复用现有 runner 配置必须用新的config与原cohort隔离；保留失败/parse_invalid条目，断点续跑。
- 结束后用`stage0_metrics`或最小score适配计算三种arm的分母、解析率、Accuracy/Macro/Weighted F1、混淆和per-class，主报`N decoded eligible`上条件分数，另报对公开8159原分母的coverage。仅列出观察结果，不能宣称原论文表1/2已经复制；作者F1 averaging及invalid规则仍未知。相同UUID配对按Direct vs CoT列出n00/n01/n10/n11（正误翻转）和每条真实联合标签的汇总，无统计过度解读。对关键pattern单列decoded/eligible/generated/valid/correct和N<5警示，S-S-S/U-S-U缺图要显式0样本不报告准确率。
- 记录每arm真实显存、延迟、输出tokens（CoT样本可能出现长尾）、复现版本和脚本commit。原样记录无截断。不能把F1=0或无法定义口径藏起来。

## Track A（与B并行，用CPU/网络）：扩大官方VLSU图像覆盖
- **优先恢复已有成果**：在用户允许访问的Windows历史实验目录、授权跳板机`tiaoban`及GPU服务器`sunyu`中寻找PR #78此前132条下载的真实缓存/日志，核验UUID、原始官方CSV URL以及实际bytes SHA/Pillow解码，且图像依然对应原链接与数据许可；若没有真实文件不得宣称108张已经可用。不要扫描无授权私有目录。
- 当前官方Image URL总8157，Stage1已有28解码成功、30 UUID。通过`reports/stage1r/Move_Resume_Instructions.md`合法冷迁移整个Stage1状态库、verified objects、partials、events到稳定授权机器；先测控域+目标域网络/HTTPS。**下载模型成功的跳板机不保证所有图像来源稳定**，应做小批真实网页检查再逐步恢复。
- 严格保留官方原URL，不另寻替代图片、不得绕过403/版权/限制，保持TLS、SSRF保护、每host低频、workers<=4。先30个请求、再100/300等有界分批，失败按HTTP、DNS、超时、类型、解码分开；保护已有缓存hash和attempt历史，不清空状态。
- 每次freeze新画像时公开只提交aggregates/hash：全8159的decoded、failed、pending、not_attempted，按原Joint标签S/B/U、17个作者pattern、额外2个、image not_sure6个的分布，按source host/失败类别聚合。新增private快照UUID必须冻结；不要合并进旧的Stage2/Stage3 cohort。
- 依据新图片量预先确定下一小批分层Pilot (例如100–200真实已解码图), stratification事先固定，覆盖关键组S-S-S、S-S-U、U-S-B、U-S-U、B-B-U，不能用刻意超采稀有组推算未经加权的全分布Accuracy。较大规模优先近真实公开分布或按pattern加权报总体结果，明确selection bias与缺失图片分母。
- 图像版权与语义身份：禁止自动以别的图替代原链接；只保存授权研究缓存。能否恢复PR78的历史缓存必须作为`CONFIRMED / NOT FOUND / UNVERIFIED`三分状态。

## 第三个问题：正式原论文协议优先次序
- 第一主线：Table1 joint binary；Table2 Qwen7 Joint Direct vs CoT配对（作者Q7报告Direct49.4/42.3、CoT52.1/51.4，binary50.0/55.3，均是作者报告的整库结果）。先为扩大数据做实验管线验收，再有代表性数据进行可比评测。
- Figure3 17个pattern准确率是P1，但稀有组以及成功获取率必须分别显示；样本少时空项不推断。
- Table4 image/text/joint是P1：image-only gold不同且排除141 not_sure，text-only8195? **注意正确官方数是8159**。作者没有明确给出single-modality原始prompt字节，因此若本地版本则`LOCAL ADAPTATION`，不得报与作者Table4严格同协议。若能确认官方提示再正式运行。Figure4/5需要同UUID三模态有效输出；Figure5原图报告Qwen32B，不应把Qwen7输出当作原模型原数值复现。
- 未证实细节：作者F1平均方式、数据8187 vs 8159、原图片身份、模型权重revision与预处理/采样实际参数不明；保持差异台账。本人Prompt逐字签核仍OPEN，禁止自动宣称已经人工审核。

## GitHub交付与停止条件
- 首选由已有Windows ChatGPT Work任务接手：使用明确授权的主机和连接，不在GitHub提交raw image/query/model-output/weight/SSH密钥/下载URL令牌。
- 新文件置于`reports/stage3a/`、`configs/stage3a_pilot.yaml`等**独立目录**。交付 `Stage3A_Result_Audit.md`, `stage3a_metrics.json`, `image_acquisition_status.json`, `Execution_Log.txt`，必要的最小脚本/测试与一份`Run_Stage3A.md`。所有实际GPU生成需要私有日志路径、hash、run_id，report标`RUN`/ `NOT RUN`；没有私人输出不得写虚构数值。
- pytest当前server报告81 passed（GitHub最新单元测试与server可能不完全同步）：核对Git工作树和实际runner SHA、pytest来源；运行真实测试和`git diff --check`，不误将私有/未提交的server代码结果当成repo code版本。保存原运行输出。
- 未触发训练、标签重标、数据改版、付费API、大模型换代。无需再下载官方Qwen模型；权重已到GPU服务器。
- 分支 `repro/vlsu-original-20261119` 提交，不合并main。最终以简洁结论报告：真实smoke预测正确性，30人群paired pilot是否完成，样本覆盖新增量及关键pattern，是否可以进入有代表性Table1/2复现，剩余仅需用户参与的步骤。
- **成功判据**：B1给出真实预测正确性，B2对当前实际可用上限实现三种Prompt同UUID配对，Track A从既有cache或合法真实下载推动图像可用性增长（若网络不可用真实报告原因）。不能以另一份网络诊断或空泛设计替代结果。
