# TRACE-S2 | MultiOFF + InternVL2.5-8B 单生成器 + TRACE完整机制：从Caption生成直接推进至真实训练结果

日期：2026-11-20。角色：PyTorch / OpenCLIP / InternVL 复现工程师与证据审计负责人。
唯一目标：仅在 MultiOFF 数据集上，用本地 InternVL2.5-8B 生成增强Caption，然后真正训练和评测含 TRACE 主要机制的二候选完整模型。不要停留在准备文档。

## A. 范围与明确复现等级
- GitHub：YuSun-WK/implicit-content-research
- Branch：repro/trace-aaai2026-20261119；当前审计HEAD为06e6d5373257f860697decde4d14e7f3e199fe61。开工先fetch/status/记录实时SHA；若有更新先核对，禁止force push与merge main。
- 仅修改 06_experiments/repro_trace/**，必要时局部.gitignore。上游 TRACE 固定commit：83ecb799f897fe275185e082ee9a669f7d04bfaa，保存为只读参照。
- **只用MultiOFF，不检查或下载FHM；只使用InternVL2.5-8B一个生成式VLM，不调用Gemini、OpenAI或任何付费API。** RAM++和GroundingDINO属于原方法的离线视觉标签/目标检测模块，允许继续使用。
- Caption候选严格是 [原始sentence, InternVL增强caption] 两条；实际执行Caption Scorer、训练Gumbel-Softmax、文本编码器部分微调、双向融合、分类+对比+相关性三项损失。
- 准确命名：TRACE-InternVL-only-MultiOFF-2caption (adapted reproduction)。这是完整核心方法结构的二候选改编复现，不等于论文三候选/最佳XLM-R ViT-H/14的严格同条件复现。
- 单卡 RTX4090/4090D，GPU峰值目标<18GiB，单次运行<=6h，GPU作业串行，必要时分段checkpoint继续。绝不上传原图、原始CSV记录、原文/Caption、模型权重、Checkpoint、token或样本级预测。

## B. 优先读取原始代码和已完成证据（不要重复Stage0-S1C）
本地：
06_experiments/repro_trace/Stage1C_MultiOFF_Data_Audit.md
06_experiments/repro_trace/Stage1C_MultiOFF_Paper_Code_Alignment.md
06_experiments/repro_trace/Stage1C_MultiOFF_Training_Report.md
06_experiments/repro_trace/Stage1C_CUDA_Architecture_Selftest.md
06_experiments/repro_trace/multioff_baseline.py
上游官方同commit：
MultiOFF/multioff_cap_gen.py
MultiOFF/clip_roberta_multioff.py
MultiOFF/multioff_proj_ft.py
utils/caption_selection.py
utils/loss_functions.py
README.md

已验证原始MultiOFF 445/149/149，但每份CSV各1条缺少可匹配原图，完整样本子集444/148/148，共740条真实图文。原始图片已经在服务器~/data/trace-assets/multioff/，复用、不要重新下载。
旧Stage1C的ViT-L/14 adapted projection baseline Test Acc .6149 / MacroF1 .3808 / AUROC .5361，与恒负类预测一致；旧结果不能视为有效对照或复现成功。
上游实际MultiOFF/clip_roberta_multioff.py当前启用OpenCLIP roberta-ViT-B-32 / laion2b_s12b_b32k，而不是注释的xlm-roberta-large-ViT-H-14。此前缓存的HF ViT-L/14与之不同，不能直接混用并声称同模型。

## C. Step1：固定并生成InternVL增强Caption（立即开始）
官方模型：OpenGVLab/InternVL2_5-8B。必须固定当前可下载官方revision、文件sha、Tokenizer与生成参数；检查模型所需trust_remote_code文件的来源版本；仅做推理、不训练InternVL。
遵循MultiOFF/multioff_cap_gen.py真正的Visual Grounding流程：
1. RAM++ 识别标签。
2. GroundingDINO 从标签定位对象与置信度。
3. 使用作者提供的带grounding信息prompt，让InternVL2.5-8B产生单条适用于CLIP的图像+Meme文字语义增强caption。原prompt包含避免直接写offensive/non-offensive标签，不能把真实标签送入Caption生成提示词。
4. 保留生成来源、prompt hash、量化模式、模型revision、时延、bbox摘要；不得替换为普通图像描述模型，不得使用Gemini。
5. 原作者脚本批处理默认走Gemini、InternVL加载与调用被注释，device硬编码cuda:1、文件路径为作者机器、pd.concat未重建索引并用df.loc[i]写入，容易造成Train/Val/Test的caption错配。使用wrapper修正所有这些工程问题；不改作者上游代码。用concat(ignore_index=True)与唯一稳定键（split+原CSV行号+image_name+image_sha256）对应每张图片；输入输出一致性必须由测试证明。
6. 首先测试10条真实样本，验证模型正确加载、图像预处理、图片文字可理解、caption成功解析、无误关联。
7. 然后运行50条真实样本pilot，记录平均/中位/p95生成时延、allocated/reserved显存峰值、空Caption数、失败类型、真实OpenCLIP tokenizer的77-token上限及截断率。原作者要求under77 tokens，但不能默认遵守；若工程上限制max_new_tokens，记录与原版max_new_tokens=4096的差异，避免悄悄改模型或prompt。
8. 10+50通过后继续生成全部740条完整样本的caption，绝不因每完成一个阶段而停下征求批准；每<=25条原子写入本地生成清单，支持重新启动跳过已成功条目、原图SHA一致性校验、失败重试、禁止重复拼接Caption。
9. RAM++/GroundingDINO与InternVL串行使用GPU，不同时驻留显存。InternVL先试BF16，如>18GiB或OOM先尝试官方8-bit，仍失败则审计4-bit可行性与质量风险；尽量保持相同8B模型，不得无声明换用1B/4B模型。任何量化改变都要显式标注 adapted generation。禁止无止境重试，失败必须留下可操作日志。
10. 数据文件与Caption保存在仓库外，例如~/data/trace-assets/multioff/trace_internvl_only/；存储原文字仅本地，Git里只能提交聚合计数/来源哈希。正式完整训练前必须检查train444/dev148/test148均有2条有效候选（总体740/740）；失败样本重试，不能以空串、No caption或复制原始文字/他人Caption伪造。
11. 生成Dev/Test captions允许离线处理图片，但绝不把Dev/Test标签输入Caption提示词、模型训练或监督选择。后续只在Train上拟合模型。

## D. Step2：构建真正含全部主要模块的TRACE MultiOFF训练入口
尽量复用官方 MultiOFF/clip_roberta_multioff.py，建立独立wrapper，冻结原作者源码。必须核对与复用当前官方OpenCLIP roberta-ViT-B-32 + laion2b_s12b_b32k及其对应tokenizer/processor，校验真实预训练权重非随机初始化，记录OpenCLIP版本与checkpoint哈希，不得静默换用HF ViT-L/14。

模型必须确实执行：
- image tower冻结，text tower末层按作者当前脚本解冻；保存每组参数名、可训练数量及梯度。
- 两候选shape [B,2,T]；caption_scorer给分；训练hard Gumbel-Softmax、推理softmax；文本特征选择后进入image/text projection、双向cross-attention、pre_output与binary classifier。
- 使用官方MultiOFF文件中的三项损失：Classification、Contrastive、Relevance，原代码总损失 cls + 0.3*cont + 0.7*rel，保持原权重及temp schedule（除非数值bug阻断，需写明修复）。
- 不要将FHM的utils/loss_functions.py可学习权重方案当成MultiOFF官方损失；当前MultiOFF脚本是另一实现。
- 注意作者train_contrastive存在硬argmaxcaption选择与额外编码器前向，审查分类与相关性梯度实际作用范围，不能声称所有损失都优化Caption Scorer。
- 审计官方预选best_captions是否实际参与训练前向；如果仍然给所有候选token，就不能在报告中宣称预选直接决定最终分类Caption。
- B=1 / B=2路径中 .squeeze() 导致形状不稳定，以及caption数据字段类型、唯一键、训练/验证拆分、冻结视觉塔、不同microbatch loss-scale等，写自动化单测。
- 禁止作者evaluate_model按当前eval或Test标签搜阈值；主指标固定0.5。Dev可额外寻找阈值并冻结，但不能把Test带入配置选择，也不能反复对Test调优。

## E. Step3：单卡GPU门禁后连续完成完整训练
G1：模型/数据/三类视觉模块真实就绪，caption源正确。
G2：10->50 pilot通过，再740条均已覆盖；没有任何paid API或Gemini。
G3：作者OpenCLIP backbone与完整方法模块真实加载，2候选shape通过单测。
G4：1个真实MultiOFF microbatch forward + backward + AdamW optimizer.step + checkpoint save/reload；检查cls/cont/rel三项loss均finite、caption scorer/text last block/fusion/classifier梯度可达、vision冻结无梯度、参数实际改变，记录GPU峰值与step耗时。
G5：测试microbatch 2/4/8/16/32（逐一先只运行1batch，仅在显存允许时增大），然后选择安全microbatch完成最多100个实际训练microbatch或1个完整Epoch的短跑；Contrastive在batch=1无法形成有效批内负例，梯度累积不等价于增加同批负例，因此优先物理batch>=2，若可行接近原始物理32、目标有效128。Checkpoint间隔<=25batch。
G6：G4/G5通过后**本轮直接运行完整seed42训练**（原作者max20epochs、Dev early stop按源代码核实；AdamW原默认lr1e-4，weight_decay0.01；数据、seed、精度、微批和实际更新次数记录）。每Epoch写Train loss components/Dev confusion TN FP FN TP、Dev accuracy/macroF1/offensiveF1/ROC-AUC、预测正类比例、Caption选择original vs InternVL的占比，best/last可恢复checkpoint。最多6h每次，可分段续训而不改变协议。
G7：在全部Dev选模/阈值固定之后，只进行一次Test评估，报告N、Accuracy、Precision、Recall、macroF1、offensive F1、AUROC、confusion matrix、模型预测正类数及caption选择分布。说明旧baseline Test历史已被看过，避免把多轮Test调参称作盲测。
G8：若seed42成功且预算允许，可做seed121的重复训练；不是必须，不在本轮开启全面四组消融、超参搜索或跨数据集研究。若预测坍缩，做一次有界Train/Dev概率/梯度排查，不能通过反复刷Test挑分。

## F. 结果对比与解释边界
- 主模型名称只能是TRACE-InternVL-only-MultiOFF-2caption (adapted reproduction)。
- 作者TRACE Table6最佳MultiOFF结果 Acc.678/F1.673来自更大XLM-R ViT-H/14与另一完整数据候选配置，仅能作为异配置参考，不是同等条件的硬门槛。
- Stage1C的ViT-L/14 baseline不同backbone、没有Caption且结果疑似多数类坍缩，不得把差值解释成Caption Scorer/Relevance机制的独立贡献。同backbone、同Caption覆盖的控制消融应在下一轮规划，先把完整两候选方法真实训练完。
- 报告是否只是得到了不同caption、caption scorer梯度非零、分类器性能是否提高、增益能否归因相关性机制这四个不同层面的证据，不混为一谈。
- 原始图像/Caption和错误样本可以在服务器本地查看，不可把受限原始内容或可识别受限样本行提交Git。

## G. 交付、验收、回滚
仅在06_experiments/repro_trace/**新增生成器/训练wrapper、配置、回归单测、只含聚合数值与hash的可提交日志。至少生成：
Stage2_InternVL_Caption_Pipeline_Audit.md
Stage2_Caption_Coverage_Manifest.json（聚合）
Stage2_2Caption_TRACE_Architecture_Parity.md
Stage2_Training_Config.yaml
Stage2_GPU_Smoke_100Batch.md
Stage2_Complete_TRACE_Training_Report.md
Stage2_Author_vs_Local.md
Stage2_Reviewer_Gate.md
可重跑CLI入口，并保存独立运行日志/模型Checkpoint在本地gitignore目录。

验收：740条真实caption正确归属，单卡真实optimizer更新，完整主干/Caption Scorer/Gumbel/三项Loss/文本层微调都实际运行；正式训练及Dev/Test真实指标存在、可追溯；如果因资源失败写清目前实际完成步骤而非编造。
全部采用小步commit并push当前分支，禁止force-push/merge main；失败用git revert仅撤销本轮自身新提交，保护前轮证据。
最终中文报告依次给出：生成caption覆盖/延时/显存与revision、所用backbone和可训练参数、实际更新数/epoch/checkpoint、Dev/Test指标和多数类坍缩检查、对照限制、当前Git SHA与日志路径、下一轮唯一优先事项。不要把生成任务文档当成完成训练。
