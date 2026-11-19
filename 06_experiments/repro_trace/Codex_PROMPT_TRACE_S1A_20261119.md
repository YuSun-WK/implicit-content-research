# Codex Task TRACE-S1A — 受限数据入场、CLIP 固定权重、原始文本诊断训练（最多100 Batch）

角色：AAAI 2026 TRACE 单卡复现工程师 / PyTorch CLIP 训练工程师 / 证据审计员。
只研究 TRACE，禁止 VLSU、新模型或大规模 VLM 训练。

## 0. 基线与输入
仓库：YuSun-WK/implicit-content-research
分支：repro/trace-aaai2026-20261119
开始前：git fetch、git status、git rev-parse HEAD，并确认该分支。当前已审查的 HEAD 是 5e852acfb747839b958f145ef6c8e94e5f3ccd05；若远端更新，先理解新变更，绝不覆盖或强制推送。
阅读：
- 06_experiments/repro_trace/Gate_Decision.md
- 06_experiments/repro_trace/100_batch_report.md
- 06_experiments/repro_trace/Caption_Availability_and_Provenance.md
- 06_experiments/repro_trace/TRACE_Stage0_Code_Map.md
- 06_experiments/repro_trace/run_stage0.py
- 06_experiments/repro_trace/data_manifest.py
固定作者代码 commit: 83ecb799f897fe275185e082ee9a669f7d04bfaa。
CLIP Hugging Face: openai/clip-vit-large-patch14
预设固定模型 revision: 32bd64288804d66eefd0ccbe215aa642df71cc41
固定资产 SHA 见 upstream_manifest.json。

上轮真实结果：CPU 5/5 测试通过，445,480,710 总参数，其中39,127,813可训练；0个FHM训练 Batch、0次真实optimizer.step()，GPU显存峰值、Loss、F1均未测量，状态DATA_BLOCKED。不得把CPU fixture当作GPU训练成果。

## 1. 本轮目标（先解锁训练基础设施，不开展正式epoch）
顺序执行：
A. 数据授权核验及原始 Caption 可用性核验。
B. 获得并验证固定CLIP权重。
C. 解耦完整 TRACE 与无Caption训练诊断的门禁。
D. 有合法 FHM + 权重时，执行1 Batch真实GPU smoke，合格后最多100 Microbatch训练验证。
E. 若FHM数据不可获得，完成A–C与CPU单元测试，明确标记BLOCKED并交付人工所需动作；不得自己合成FHM或用其他未授权镜像顶替。

## 2. 数据授权与清单
- 仅检查当前项目授权工作区、用户显式指定路径及既有报告记录的项目目录。优先检查官方 DrivenData/FHM原件及train/dev_seen/dev_unseen/test_seen/test_unseen文件，明确每个split的图片、ID、标签是否可用。
- 数据下载/许可入口：https://www.drivendata.org/competitions/64/hateful-memes/
- 不绕过许可、登录、验证码或访问限制。需要用户登录或同意许可时立即输出MANUAL_DATA_ACTION_REQUIRED，给出准确UI步骤与建议本地目录；不私自从第三方网盘/HF镜像下载。
- 所有正式本地数据放在git忽略目录或仓库外；绝不提交图片、标签明细、原始文本、Caption原文。仅提交计数、哈希、授权状态和来源说明（不得公开令牌或敏感路径）。
- 检查split、label 0/1、重复、丢图、错误image path、caption列真实性；若test labels缺失，不得编造或估计。
- 专门区分 author InternVL captions、author Gemini captions、用户重新生成 captions、占位字符串；没有作者原始两列时完整TRACE仍标记BLOCKED。

## 3. 下载并固定CLIP权重（不需要FHM即可做）
- 检查已有合法本地cache；如不存在且网络允许，使用官方Hugging Face快照下载，revision固定为32bd64288804d66eefd0ccbe215aa642df71cc41，目标在git之外。
- 优先下载model.safetensors、config、tokenizer和processor所需文件；支持 hf CLI或 huggingface_hub.snapshot_download，必须保留精确revision与哈希校验。
- 与 upstream_manifest.json逐文件sha256比对，失败时保留错误日志，不关闭校验，不自动退回main/latest/第三方复制。
- 记录文件大小、实际缓存路径、下载是否成功、SHA状态。不要提交模型文件。
- 若服务器外网失败，记录具体网络/HTTP/哈希失败；给出用户可在授权联网机器执行的固定版本下载及离线传输命令，但不可伪称成功。

## 4. 拆成严格复现与诊断模式，严格命名
模式一 trace_original：保留现有3候选 text / ivl_8b_new_caption / gemini_caption、作者cls+rel、Gumbel选择、已审计的上游算法；只有全部真实来源成立才能训练。
模式二 trace_text_only_diagnostic：需要授权FHM的图像、原始text与合法Train/Dev标签及固定CLIP权重；只有1条候选text，损失为classification ONLY；不要求也不补填增强Caption。复用作者CLIPClassifier的视觉/文本层、投影、双向融合与分类器，不训练生成式VLM；清楚声明这是“单Caption TRACE结构诊断”，不是论文的projection-only CLIP baseline，不可和作者Table 4直接做performance差值。
- 以明确的实验模式参数解耦 run_stage0.py 中 assert_inputs、FIELDS、LOSS_CONFIG、author_loss()要求2个focal项、梯度组验证、签名和checkpoint，保持trace_original功能与默认安全门禁不回归。
- 单候选情况下Scorer/Gumbel不产生有意义的caption排序学习。不要把Scorer梯度非零作为diagnostic smoke的通过条件，优先仅检查分类器、投影、文本可训练块、融合中理论可达梯度、冻结视觉塔无梯度；不要谎称Scorer机制已验证。
- 不能添加假Caption或混用训练/开发标签；诊断报告每张图唯一的caption来源为original_text。
- 严格禁止修改作者 pinned upstream文件；实现改动仅在wrapper及独立脚本中，按差异记录科学改变。
- 提醒：如果以后需要复现论文的“基础CLIP投影分类器”应另建真正的paper-aligned baseline；本轮不做。

## 5. 首轮真实GPU测试（仅当数据与权重都通过）
- 单卡CUDA_VISIBLE_DEVICES，优先bf16，Microbatch=1、accumulation=1；先执行包含真实optimizer.step()的一批，确认loss为有限值、classifier权重变化、文本层/融合层/投影梯度非零、视觉塔冻结参数无梯度。按模式区分评分器是否应有梯度。
- 保存并回读checkpoint，包含可训练参数、optimizer/scaler、random/torch/CUDA RNG和批游标；使用真正的恢复程序继续同一种子相同数据顺序。
- 通过后分别测试 Microbatch=2 和4（8仅在显存明确足够时）；每个候选先只运行1 Batch，不能把不同Batch结果直接比性能。
- 再固定一个可行Microbatch，最多100个Microbatch，至少每25个Batch保存一次可恢复checkpoint。
- 同一GPU任务不超过6h、PyTorch峰值显存尽量<18GiB，监测共享GPU实时占用；OOM、损失NaN或未更新立即终止并记录。
- 输出实际step time、p50/p95、peak allocated/reserved、actual optimizer steps、classification loss序列、grad norm、checkpoint roundtrip、每种配置实际有效Batch大小、完整运行命令。
- 如果模型权重下载成功但没有合法FHM，只做CLIP加载/参数清单，不做伪造的GPU FHM smoke；可以执行合成张量的独立代码单元测试，但不得当成实验结果。
- 不启动完整训练、多种损失消融、MultiOFF、Benign Confounders、测试集评估或Caption生成。

## 6. 必须特别检查的工程风险
- 不要把FHM test真实label作为阈值搜索输入；本轮最多在dev报告fixed_0.5或用dev校准。
- 上游ViT-L/14只解冻第4/7/10层，非paper T(-4)；不得误写成原论文T(-4)复现。
- 上游loss_functions.py cls-only使用Scorer选择，但C=1下选项固定；不要不必要地改写成别的分类器。
- 上游重复调用视觉/文本塔，真实显存可能高；不得为了通过smoke悄悄换backbone、冻结更多层、缓存训练特征或者删模块。若提出优化，单独记录为适配并做数值一致性测试。
- 单候选样本的shape、labels维度、focal loss与checkpoint可读性加回归测试；原始3候选测试不能破坏。
- 查看数据清单在FHM原始split JSONL没有split字段时能否正确正规化；保留原始ID/路径，但不要泄露记录内容。
- model.safetensors校验和实际CLIPModel加载必须成功才可声称权重已就绪。

## 7. 代码/文档修改范围
仅修改或新增 06_experiments/repro_trace/**；必要时更新局部.gitignore，不修改main/其他项目/作者源码，不提交大文件。
建议交付：
- Stage1A_Data_Access_Gate.md
- Stage1A_Model_Weights_Report.md
- Stage1A_Mode_Semantics.md
- Stage1A_GPU_Smoke_100Batch.md 或明确BLOCKED
- Stage1A_Reviewer_Handoff.md（下一步GO/BLOCKED决策）
- 可配置的wrapper、fixture单元测试、运行配置、无敏感内容日志
- 如已有manifest/report，更新并保留Stage0原始事实，不重写历史结论

## 8. 验收与回滚
Gate G1：FHM有合法来源、相关train/dev图文标签完整；缺则MANUAL_DATA_ACTION_REQUIRED。
Gate G2：固定CLIP模型全部所需文件及SHA通过；缺则WEIGHTS_BLOCKED。
Gate G3：原始两列Caption真实可追溯；缺则trace_original=BLOCKED，但不得阻塞trace_text_only_diagnostic。
Gate G4：至少一次真实CUDA optimizer.step、完整checkpoint回读、显存与时延实测；缺则TRAINING_NOT_RUN。
Gate G5：诊断最多100个Microbatch、无数据泄漏、日志与模型一致；合格可建议下一阶段正式Baseline训练。
在分支上分小提交并push；禁止force push或merge；提交前git diff、单测、检查大文件/敏感数据。如失败，只使用git revert撤销自己新增提交，保留上轮成果。
最终用中文返回：真实完成情况、每个Gate状态、模型权重下载状态、需要用户本人做什么、真实GPU训练结果（无则写0）、commit URL、下一轮Codex任务建议。
