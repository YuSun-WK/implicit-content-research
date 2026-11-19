# TRACE-S1B｜FHM 原始数据入场与真实单卡训练门禁

> 本任务仅在用户已从 DrivenData 官方许可入口取得 FHM 并放入服务器授权目录后执行；如缺失，停在 G1，不得绕过。仅 TRACE，非 VLSU。

## 0. 固定输入与限制
- Repo: `YuSun-WK/implicit-content-research`
- Branch: `repro/trace-aaai2026-20261119` (起点记录 HEAD；S1A审查时 HEAD=`6c60d9d0fba08b4fdcfd6f7eb1df95caf2a04c3e`，如已更新以新的远端实际状态为准)
- Work dir: `06_experiments/repro_trace/`
- 阅读：`Stage1A_Reviewer_Handoff.md`、`Stage1A_Data_Access_Gate.md`、`Stage1A_Mode_Semantics.md`、`Stage1A_Model_Weights_Report.md`、`run_stage0.py`、`data_manifest.py`、`test_stage0.py`。
- 作者 TRACE 源码固定 SHA: `83ecb799f897fe275185e082ee9a669f7d04bfaa`。
- CLIP 固定 revision: `32bd64288804d66eefd0ccbe215aa642df71cc41`; 已经在 S1A 报告通过 8/8 SHA 和 CPU 加载，**不要重新下载**，除非本地核验失败。
- 单卡 RTX 4090/4090D、实用显存预算 ≤18 GiB、单次作业≤6h；不使用付费API、不修改作者核心模型、不训练 VLM。
- 学术门禁：`trace_original` 只有在官方原图+标签及作者原始两列Caption均可验证时才允许；当前首先运行 `trace_text_only_diagnostic`，这不是论文 Table 4 的 Projection-only CLIP Baseline。

## 1. Gate G1 — 人工下载的 FHM 正规验收
1. 先问本地指定目录是否存在（默认候选 `~/data/trace-assets/fhm/`）；只检查授权目录。不存在则立即输出 `MANUAL_DATA_ACTION_REQUIRED`，不要重扫无关硬盘、合成数据或下载未经授权第三方镜像。
2. 记录授权来源、下载日期/包名、校验摘要（不在 git 中上传文件或原文）；仅在用户实际确认已接受官方许可时，把本地私有 YAML 的 `authorization_confirmed` 设为 true。自己不能代表用户接受许可。
3. 验证 train、dev_seen、其他实际可得 split 的 JSONL、id、img、text、label（只有真实含标签的 split 才能评分）；图片是否存在/可解码；训练/验证 ID与图片路径是否交叉；标签分布；重复；missing值；路径安全。识别 JSONL 无 `split` 字段时用命名 split 合法补齐。不要误把 test_seen/test_unseen 的标签当作已公开。
4. 生成项目目录下可提交的**仅聚合统计**报告和本地忽略的详细诊断日志；如任何 train/dev 严格验收项失败，先处理输入格式错误/报告，禁止GPU训练。

## 2. Gate G2 — 已下载 CLIP 核验
运行仓库 `prepare_clip.py` 检查本机固定 revision 下的8个文件和完整sha256；真实模型CPU加载应正确。保持本地模型目录在 Git仓库外。
若无法通过，`WEIGHTS_BLOCKED`；报告具体文件，**不可换模型或使用随机权重**。

## 3. Gate G3 — 两种实验模式边界
- 第一条可运行通路：`experiment_mode=trace_text_only_diagnostic`，仅FHM原始文字作为唯一候选、classification-only，使用原作者 ViT-L/14 Encoder/Projection/Fusion/Classifier；报告必须标注 `diagnostic`，不可拿来与论文 Table 4 的 Projection-only Baseline 直接比较。
- `trace_original` 继续严格要求原作者 `ivl_8b_new_caption` 与 `gemini_caption` 全量、对齐、有来源；在缺少原始Caption时仍 `AUTHOR_CAPTIONS_BLOCKED`。不要用空串、“No caption”、其他模型Caption冒充原件。
- 上游模型只解冻文本层索引4/7/10，非论文 T(-4)。保留原上游哈希及证据差异。
- 若在 smoke 遇到工程兼容问题，优先最小化 wrapper 修复并添加CPU测试，记录修复前后的具体张量形状及是否属于忠实代码路径差异；禁无声换主干或重写损失。

## 4. Gate G4 — 真正的一次GPU optimizer step
- 提前检测GPU空闲，选一张当前可用且符合限制的4090/4090D，设置 `CUDA_VISIBLE_DEVICES` 只暴露一张。优先 BF16，microbatch=1，accumulation_steps=1，seed=121。
- 用 `.local/` 中独立 YAML 设置 `mode: smoke` 与诊断模式，启用真实FHM train样本和实际 CLIP checkpoint，运行原wrapper；必须真正执行forward、backward、gradient clipping、AdamW optimizer.step()和checkpoint回读。
- 记录梯度范数（分类器、训练文本块、投影、融合）、分类器参数改变、冻结视觉塔梯度为none、finite loss、CPU/GPU使用及time。注意单候选Caption scorer的选择梯度为0不构成诊断失败。
- 校验 resume 及 optimizer/scaler/RNG一致性。若显存超出约18GiB、OOM、参数未更新、发生非有限梯度，退出且不得继续。

## 5. Gate G5 — 最多100 Microbatch稳定性
- 只在G4通过后测试 microbatch 2、4（8仅在充分留有显存且无不良共享占用时测试），各自先执行**一批**，全部记录实际峰值；不要直接并行。
- 固定可用配置开启最多100个Microbatch的 `mode: short`，有效batch、梯度累积等均实际记录；每≤25批落地 checkpoint。每次任务≤6h。
- 测试 checkpoint 中断恢复后能继续训练；记录单Step实际耗时和 p50/p95、alloc/reserved峰值、optimizer更新次数、loss components和有限性。
- 只允许 Dev fixed_0.5（可选独立Dev校准作为附加分析）；不要基于测试集标签调阈值或生成测试分数。
- 不得扩展成完整30 Epoch、四组Loss消融、Benign Confounders或者MultiOFF。

## 6. 交付物与验收
仅修改 `06_experiments/repro_trace/**`（必要时局部.gitignore），提交：
- `Stage1B_Data_Manifest.md`（聚合统计与授权状态）
- `Stage1B_Smoke_GPU.md`（真实运行命令、0或1+次更新、梯度/显存/耗时/恢复）
- `Stage1B_100_Batch_Report.md`（完整实际短跑或BLOCKED，禁止想象数值）
- `Stage1B_Reviewer_Gate.md`（G1–G5和Stage2是否GO）
- 环境与配置快照（脱敏）、局部测试结果。
验收：必须有真实FHM输入、完全固定模型、真实optimizer.step与checkpoint恢复、显存与时间实测、loss组件日志，才能称 G4/G5 PASS。
不要提交原图、完整标签明细、Meme原文字、作者Caption、模型权重、个人账号凭据或受限样本预测。
提交前检查diff与大文件；小步提交后push到本分支，**不得merge main或force-push**。若失败只使用git revert撤销自己本轮新提交，不动前一轮成果。

## 7. 输出中文总结
报告每个Gate、真实Batch数、是否发生optimizer.step、峰值GPU内存、Step耗时、Checkpoint恢复证据、仍需用户人工动作、确切提交SHA；明确 `true FHM experiment` vs `CPU fixture`。
如果G1未过，停止训练并交付清楚的“用户还需做什么”说明。只有通过G4和G5后再提Stage2正式训练方案，不自行执行。
