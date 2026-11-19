# Codex｜TRACE-S1C 加速复现：真实 CUDA 自检 + 官方 MultiOFF 路线 + FHM 一次性入场

## 总目标：不再重复无效门禁，尽快获得可信的真实 GPU 训练证据与论文相关数据集指标

**论文**：TRACE: Textual Relevance Augmentation and Contextual Encoding for Multimodal Hate Detection（AAAI 2026 AISI Special Track，CCF-A）。
**任务限制**：只复现 TRACE，禁止改做 VLSU、提出新架构、混用数据标签或消耗付费 API。

- 项目仓库：`YuSun-WK/implicit-content-research`
- 工作分支：`repro/trace-aaai2026-20261119`
- 当前审计 HEAD：`834023dbec856e0567438b4c1c9dd77d73f9f90d`（开始时重新 fetch 并以实时远端为准，禁止强推）。
- 代码目录：`06_experiments/repro_trace/`
- 上游 TRACE 代码固定 Commit：`83ecb799f897fe275185e082ee9a669f7d04bfaa`
- ViT-L/14 模型固定 Hugging Face Revision：`32bd64288804d66eefd0ccbe215aa642df71cc41`，已有 8/8 SHA-256 验证和实际 CPU 加载。
- 参考阅读：`Stage1B_Reviewer_Gate.md`、`Stage1B_Data_Manifest.md`、`Stage1B_Smoke_GPU.md`、`Stage1A_Mode_Semantics.md`、`TRACE_Stage0_Code_Map.md`、`run_stage0.py`、`prepare_clip.py`、`MultiOFF/` 官方代码。
- 已知事实：FHM 指定目录缺失，已连续多个阶段重复报告 G1 BLOCKED；**截至此审计真实 FHM训练 0 Batch / 0次 CUDA optimizer.step()**。本轮禁止再以仅重跑同样 FHM 无数据检查为主成果。

## 严格优先级及执行顺序
P0（立即）：只进行**一次** FHM 指定路径检查。若无授权 FHM，登记一次 `FHM_MANUAL_ACTION_REQUIRED`，随即转 P1 与 P2，不要让全部任务停在 FHM。
P1（首要可独立交付）：在已校验的预训练 ViT-L/14 上，做真正 CUDA forward/backward/AdamW step/checkpoint-resume 的**计算路径自检**，数据为明显标识的合成测试张量和无害虚拟原文，非数据集实验。
P2（首要真实数据路线）：尝试官方原作者发布的 MultiOFF，先查许可及文件完整性，若可合法取得则以作者代码作为基线实现真实训练和评测。
P3（仅当 FHM 已进入授权目录）：FHM `trace_text_only_diagnostic` 真实 Smoke → 最多100 Batch → 根据实测成本安排正式 Baseline。
P4：仅在作者真实原始 Caption 来源确认后规划完整 TRACE；不得凭空生成或拿异源 Caption 冒充复现。

**各 P 分支可独立形成结论**；不得因为 P0 BLOCKED 而跳过 P1/P2。CPU fixture 和CUDA自检不算 FHM/MultiOFF 正式实验。

## 1. P0 — FHM 一次性入场检查
默认候选：`~/data/trace-assets/fhm/`。也可以读取用户明确提供的授权路径，**但只做一次，绝不反复扫描未知共享目录**。
若缺失：记录日期、缺什么，提供给用户完整的手工步骤（登录 DrivenData、核对并接受 Dataset License Agreement、下载官方文件、上传并解压到私有目录）；不绕过登录或使用未获许可第三方镜像。官网 `https://www.drivendata.org/competitions/64/hateful-memes/data/`。
保留 FHM 原始 train/dev_seen/dev_unseen 等 split 和 test 真实标签状态；只能已具许可时设置 `authorization_confirmed: true`。资料不能进入 Git。
不要为了“通过”把本轮的诊断改成无来源数据或随机标签分类。

## 2. P1 — 真正的 GPU 数值/成本自检（即使没有任何 FHM 数据也运行）
创建一个**独立的** `cuda_architecture_selftest.py` 及严格测试报告，读取官方 fixed SHA 模型，用现有 wrapper 的作者 `CLIPClassifier`、`calculate_loss_gs`、优化器逻辑。只使用缓存中真实 pretrained weights。
- 仅在 `.local/` 创建少量合成 RGB 图片张量与无害固定虚拟 Text、伪标签，显著记录 `SYNTHETIC_COMPUTE_ONLY_NOT_DATASET_RESULT`；原始文件不可提交。
- 必测 `trace_text_only_diagnostic` 单 Caption / Classification-only；可行时再测 `trace_original` 的三候选 + Classification/Relevance 的**算法自检**，三段虚拟 Text不是作者 Caption，绝不将其称为论文训练或 Caption 复现。
- 用真实设备完成 1 microbatch、一次真实 loss.backward、有效梯度、一次 AdamW optimizer.step，记录每个模块的grad norm、冻结视觉塔是否无梯度、classifier参数差、真实 allocated/reserved 峰值和 step 时间。
- 同时验证单卡 checkpoint 保存/恢复的 trainable weights、optimizer/scaler 和 CPU/CUDA RNG；做一组确定性下一步一致性 sanity test（必要时关闭非确定性路径，明确声明）。
- 在微批1通过且<18 GiB后，可再测微批2；不需要先跑 100个虚拟Batch。一次计算路径自检的成果是 GPU可训练性/资源瓶颈，**不是任何分类效果**。
- 共享GPU有负载时选择当前安全的空闲4090/4090D（只暴露1张卡）；单次≤6h，实用显存预算≤18GiB，发生OOM/NaN立即停止并记录。禁止静默缩小主干或冻结更多参数以逃避OOM。
- 若作者源码有B=1形状bug，使用已记录的wrapper适配，保留上游源码SHA；在正式评估前写明所有数值兼容适配。不要为让梯度检查通过捏造数据集结果。
- 若网络/cache/显存失败如实报告，不允许空白报告或把CPU小模型fixture当成CUDA完成。

## 3. P2 — 官方 MultiOFF：争取本轮获得第一组真实数据集性能指标
MultiOFF是TRACE官方论文的第二个评估数据集（Offensive / Non-offensive，而非FHM Hateful / Non-hateful），不混用任务语义、标签和划分。
**原始作者的数据入口**：
- 原始论文与来源：https://aclanthology.org/2020.trac-1.6/
- 作者原始GitHub：https://github.com/bharathichezhiyan/Multimodal-Meme-Classification-Identifying-Offensive-Content-in-Image-and-Text
- 其 README 给出的作者Google Drive资料夹：https://drive.google.com/drive/folders/1hKLOtpVmF45IoBmJPwojgq6XraLtHmV6?usp=sharing
- TRACE上游对应脚本：`MultiOFF/clip_roberta_multioff.py`、`MultiOFF/multioff_proj_ft.py`、`MultiOFF/multioff_cap_gen.py`。

顺序：
(a) 检查作者公开数据入口与使用条款，能合法直接下载才下载至 Git 仓库外 `~/data/trace-assets/multioff/`；若需要Google登录/权限，输出 `MULTIOFF_MANUAL_ACTION_REQUIRED` 和最短人工动作，切勿绕过权限或改用第三方未经核验版本。
(b) 读取并核验实际 csv/图片的 schema：`image_name`、`sentence`、label编码及 Training/Validation/Testing 官方划分（论文报告445/149/149，但只能以实际文件计数为准）、图片解码、重复、类别分布、许可证及路径安全。
(c) 在 `MultiOFF/clip_roberta_multioff.py` 中，作者实际是OpenCLIP `roberta-ViT-B-32`，需 `multioff_updated_captions_final.csv`，而非此处已下载的HF ViT-L/14；不要冒称二者可直接复用。先审计作者脚本中的固定/未固定 checkpoint、caption、损失、训练与评估的路径和潜在test阈值泄漏。
(d) **首先追求一个可以忠实归属的原作者无 Caption 基线**：审计 `MultiOFF/multioff_proj_ft.py` 是否能在原始 `sentence` + 图片条件下用已验证ViT-L/14和原脚本模型结构跑通。此脚本与“完整 TRACE”的架构不同，结果必须清楚命名 `author_multioff_projection_baseline` 或 `adapted_author_baseline` 并列出所有差异。若根本无法忠实对齐论文的baseline条件，就标记 `NON_PAPER_ALIGNED_DIAGNOSTIC`，不造表。
(e) 如果真实MultiOFF输入已验收：先1个真实GPU Smoke，再最多100 Microbatch短跑；这两门禁通过且以实测耗时推断可在≤6h内完成时，**本轮即可推进一次完整的作者代码基线训练**，优先3个epoch探通，选最佳Dev epoch，允许在时间预算允许下继续至作者原定义的epoch/early stop（如果达到预算应保存resume后停）。测试集只能在超参/阈值固定后评一次，Accuracy/Macro-F1/AUROC（只有合法两类时）；记录每个指标的实际N和标签。
(f) 如果原始InternVL/Gemini Caption不可获得，不允许运行或声称完整MultiOFF TRACE已复现。可以做一次公开来源/官方repo releases审计、记录作者联系渠道/拟请求的原始数据字段，**不得使用收费 Gemini API 或未经许可的伪 Caption**。
(g) 别为了“加速”直接跑全部组合；优先一条真正可比且能产生可信指标的低成本实验，再考虑完整TRACE。
(h) 每项正式实验必须固定seed、真实source hash、模型revision、config、optimizer、精度、采样和数据划分，严格分开Train/Dev/Test，不能在测试集上搜索阈值。

## 4. P3 — 用户已放入FHM时的快速路径
若官方许可及Train/Dev图片标签齐备，立即利用现有 `trace_text_only_diagnostic` 做真实GPU smoke(1 batch)→microbatch=2试探→最多100 Batch的short；G4/G5通过后，在本轮剩余允许作业预算内给出下一阶段正式CLIP Projection baseline训练的运行计划（若已写成可靠作者对齐脚本且单次<=6h，也可直接跑**一组**先验固定配置的正式baseline，不能未经审阅无限扩展）。
完整TRACE `trace_original` 必须等作者原始 `ivl_8b_new_caption`、`gemini_caption` 有可追溯来源且对齐后才能运行；保持论文ViT-L/14 T(-4)与作者脚本块4/7/10 的差异记录。
任何FHM Test label不可确认时不得在上面打指标。

## 5. 加速的工程约束
- P0的数据检查以分钟级快速退出为目标；**不得把新的一轮再次花在大量不存在路径的查找与重复报告**。
- P1和P2可同时准备CPU代码/下载，但是实际GPU作业串行；不与其他用户的GPU进程抢卡。
- 各候选依赖明确，不需要每次暂停等待用户确认，除非登录、数据许可、付费API、受限下载等必须由用户本人决定。
- 能复用既有Conda环境、CLIP snapshot、作者git检出就复用；不要重建环境、反复下载已校验权重。
- 如原训练代码性能低：先量化实际Step耗时和GPU占用；可以使用BF16、合理microbatch、数据IO缓存等工程适配，但绝不在“严格复现”路径静默更换关键模型、主干或损失。每项适配要说明是否可能影响数值。
- 单次GPU工作≤6h，实用显存占用<18GiB；每项任务可以在后续运行中使用checkpoint分段续跑，但禁止声称已经完成未执行的阶段。
- **禁止基于数据集未知的时延/准确率做承诺**。

## 6. Reviewer审计报告与GitHub交付
仅允许修改/新增 `06_experiments/repro_trace/**`（及其局部.gitignore），不要触碰 main 或其它方向。
必须交付：
1. `Stage1C_Accelerated_Executive_Summary.md`：每项事实是已完成/仅计划/被阻塞，列出真实CUDA优化器步数和真实MultiOFF训练样本数。
2. `Stage1C_CUDA_Architecture_Selftest.md`：逐模块梯度、显存、步时、Checkpoint、是否使用真实CLIP权重，并醒目标记SYNTHETIC_COMPUTE_ONLY。
3. `Stage1C_MultiOFF_Data_Audit.md`：作者数据链接、许可、真实文件清单和split count、下载阻塞。
4. `Stage1C_MultiOFF_Paper_Code_Alignment.md`：论文/上游Table与baseline架构精确对应关系；OpenCLIP vs HF CLIP差异；有无原始Caption；是否存在test泄漏。
5. `Stage1C_MultiOFF_Training_Report.md`：若已正式运行则有Train/Dev/Test真实指标、运行命令、seed、checkpoint、日志和审计；未运行则明确0和原因。
6. `Stage1C_FHM_Manual_Data_Action.md`：一次性向用户交代官网许可、目录结构、数据校验命令；不要重复同一个空路径搜索。
7. 可执行代码、CPU回归测试、只含聚合数字与环境信息的真实日志，以及下一步GO/BLOCKED verdict。

**绝不可将**模型权重、图片、CSV/JSONL整行、Meme原文、Caption原文、密钥、带权限URL/token或个人身份信息提交到GitHub；不要公开任何用户私人路径里的样本。
在当前分支分步commit、push，最终报告确切commit SHA与GitHub链接；不可merge main或force push。任何错误用git revert只撤销自己本轮新增提交。

## 7. 最终中文输出，按此顺序
- 为什么这轮比S1B产生了新进展（至少应有真实CUDA selftest，或给出可核验失败原因）。
- 官方MultiOFF是否拿到了，确切split的N是多少，哪条作者代码路径跑通。
- 真实CUDA selftest更新次数、Peak GiB、Step秒数、checkpoint是否恢复。
- 在真实MultiOFF或FHM上完成了多少次optimizer.step、多少个Epoch、什么指标（没有就明确0，不允许假数字）。
- 仍需用户本人完成的最短动作（若需要）。
- 下一步最短可获得**论文相关真实性能指标**的实验计划和启动命令。
- 当前分支最新Commit / 文件链接。
