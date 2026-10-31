# P027｜ExPO-HM: Learning to Explain-then-Detect for Hateful Meme Detection

> **2026-10-31：用户明确授权定稿、上传并合并。** “定稿”指论文与当前公开实现的静态机制审计已经形成正式阅读记录，**不等于作者训练协议已完整复现，不等于解释忠实性已经被证明**。以下所有代码判断仅针对本次可访问的公开 main 分支。

## 01. 书目与证据来源
- Jingbiao Mei; Mingsheng Sun; Jinghong Chen; Pengda Qin; Yuhong Li; Da Chen; Bill Byrne. **ExPO-HM: Learning to Explain-then-Detect for Hateful Meme Detection**. **ICLR 2026 正式会议论文，CCF-A**。
- 正式论文：https://openreview.net/forum?id=bEejbORUI5；会议论文：https://proceedings.iclr.cc/paper_files/paper/2026/hash/812f0e17bf0fa2a31a3d0b24dca49462-Abstract-Conference.html。用户于2026-10-31提供 34 页正式版 PDF；依据 §3.1–3.3、§4.1–4.7、Appendix B–J。
- 作者公开仓库：https://github.com/JingbiaoMei/ExPO-HM；重点源码 docs/reproducibility.md，scripts/grpo/train/run_qwen2_5_vl-7b_cde_paper.sh，scripts/grpo/data_prep/hatefulmemes.py，generate_cde_all.sh，verl/verl/utils/reward_score/{meme_cde.py,meme_fg_cde.py,CDE_full_vocab_for_reward.py,__init__.py}，verl/verl/trainer/ppo/reward.py，verl/verl/workers/reward_manager/naive.py。
- 标签：Hateful Meme Detection / Explain-then-Detect / Multimodal LMM / structured policy manual / curriculum GRPO / conditional decision entropy / explanation quality / calibration。**不是专门定义“图文单独安全、组合有害”的 CrossGuard 任务**。

## 02. 任务定义与关键动机
- 输入：带有叠加文字的图文 Meme（论文记为图像 I）与任务 Prompt p，合称 x=(I,p)；输出：(a) harmful/benign 二分类 c；(b) attack/target/stance 等细粒度标签 z；(c)自然语言解释 e。
- Explain-then-Detect 生成格式：y = <think>e</think><answer>d</answer>。d 为最终二分类或细粒度文本标签，不另训练独立分类头。
- 观察问题：直接检测虽然预测较强但解释缺失；普通 CoT/SFT/DPO/GRPO 解释后检测常低于 Direct-SFT；标准 Yes/No 奖励无法区分“同样预测正确但解释信息质量不同”的路径。
- 人工审核类比：先学习政策分类规范，再练习细粒度判断，最后形成二分类与解释。**类比只是设计动机，不是机制因果证据。**

## 03. 贡献与创新性质
1. **SFT-PM**：将原数据集已有的 annotation guidelines 由专家一次性转换成有定义的结构化政策手册，和 Meme 一同输入，利用已有细粒度真实标签进行普通 autoregressive CE SFT。**不使用人工写的 gold rationale 作为此阶段目标。**
2. **GRPO-CL**：在 SFT-PM 的同一 LMM 上进行 GRPO。论文定义前50%训练步骤仅细粒度、后50%步骤中细粒度/二分类各50%；每个任务生成解释与答案，使用组内相对优势训练。
3. **CDE metric/reward**：用给定输入与模型自己生成解释后，最终决策分布的条件熵衡量不确定性，结合预测正确性奖惩，用于 GRPO。
4. 评测覆盖二分类 macro F1、细粒度 micro F1、LLM-as-judge 解释质量、人工 helpfulness/coherence、ECE/Brier 校准、消融。

## 04. 完整训练与推理 Pipeline
**起点**：Qwen2.5-VL-3B/7B，自回归多模态 LMM，参数 θ，输出概率为 πθ(y|x)=∏t πθ(yt|y<t,x)。

**阶段 A — SFT-PM**：
- 来源：HatefulMemes、MAMI、PrideMM 原始样本、细粒度标签、标注指南；例如 Dehumanizing（将群体非人化）、Mocking、Slurs 等定义。
- 构造训练对：(image + “以下攻击类别及定义...” Prompt, 正确细粒度标签文本)。不同任务如 attack type / protected target 分别形成样本。
- 学习目标：L_SFT=-Σ_t log πθ(y*t|y*<t,x)，只把细粒度标签作为目标。论文 §3.3 明确**没有使用人工 gold explanation e* 做 warmup**；SFT-R 仅作为对照。
- 为什么最终能写解释：基础 LMM 已具备语言生成能力；后续 RL 强制输出解释+标签并对整段序列做策略更新。不能误认为 SFT-PM 已对解释逐步监督。

**阶段 B — GRPO-CL + CDE（同一强化学习过程的两个设计维度，并非两个串行模型）**：
- 论文的课程：first 50% steps FG only；remaining 50% steps 50% FG + 50% binary。FG 类别可能多标签，binary 为 Yes/No。
- 对每个 Prompt 采样一组 y1...yG，每条含 think explanation + answer。Figure 2 画 G=8；**当前公开训练脚本 rollout.n=5**。
- 以格式、标签正确性、CDE 分配逐条奖励 rg；组内 advantage Ag=(rg−mean(r))/std(r)；GRPO 使用 clipped policy objective 和 KL 正则更新模型生成策略。论文 Eq.(5–6)；GRPO 不另训练 value/critic model。
- RL 训练时改变的是整个回答 token 序列的概率，解释部分受到间接奖励梯度影响，但奖励本身**没有直接计算解释语义真值或忠实性**。

**测试推理**：给图像及任务 Prompt，单模型生成 <think>理由</think><answer>标签</answer>；不提供真实标签、无需在线 RL，二分类/细粒度依实际任务 Prompt 输出。

## 05. CDE 公式、计算与奖励（重点）
- 论文 Eq.(7)：H(d|e,x) = −Σ_d πθ(d|e,x) log πθ(d|e,x)。要区分**答案位置 next-token 概率**与“解释文字本身的熵”。小熵代表决策确定，不证明解释忠实。
- 论文 Eq.(8) 评估指标：对每个验证样本采样 K=16 个解释，分别算决策熵后求均值；**K=16 属于 CDE 评测，不是 GRPO 训练组采样 G**。
- §3.2 和 Appendix G：可把 binary 词表归并成 Yes/No；为了通用细粒度标签论文采用 full-vocabulary entropy 的表述；实际为计算效率使用 top-10–50 token 近似，细粒度多 token 类别需平均 token 熵。
- 代码链路：rollout 请求 top-k logprobs→ token IDs/logprobs 随 response 存储→ reward_manager/naive.py 将 extra_info 与 tokenizer 交给 default_compute_score→ 根据 data_source=meme_cde 或 meme_fg_cde 选择对应奖励→定位 <answer> 位置→决策概率/熵→correctness-conditioned piecewise reward→合成 scalar score→GRPO。
- 公开脚本设置 reward_logprobs=50；binary 默认 entropy_mode="binary"（Yes/No token 近似），FG 用 top-k full-vocab 熵并按 log(num_tokens) 归一化。不能把两种熵等同，也不能把 top-k 近似声称为真正“完整词表”精确熵。
- 论文 Eq.(11)：δ=1 时 h≤a 奖 w，a<h<b 奖 w(b−h)/(b−a)，h≥b 奖0；δ=0 时 h≤a 奖−ρw，a<h<b 奖 w(h−a)/(b−a)，h≥b 奖 w。默认 a=.1,b=.5,w=.2,ρ=.25。
- **论文公式潜在重复权重**：Eq.(9) 写 r=r_format+r_acc+w*r_CDE，但 Eq.(11) 的 r_CDE 已含 w；实现不按字面双乘。当前代码合成 total = (1−format_score)*accuracy + format_score*format + cde_reward；脚本 format_score=.1, cde_weight=.2。示例满分 0.9+0.1+0.2=1.2。
- **代码 Eq.(11) 中间区间差异**：incorrect 且 a<h<b 时，代码先算 q=(h−a)/(b−a)，base=wq，penalty=−ρw，再取 penalty+(base−penalty)*q；不同于论文线性 wq。以 h=.2,a=.1,b=.5,w=.2,ρ=.25 得代码 −.025，论文 +.05，奖励符号可能相反。
- **FG partial match 差异**：FG 准确奖励允许部分命中；当前源码使用 accuracy_reward>0 判断用于 CDE 的 is_correct，未必等同完全正确。
- **位置/概率回退**：binary 奖励中通过重构 top-k tokens 定位 <answer>，可能做跨位置候选匹配、缺一侧时合成另侧 token score；这时熵不是严格来自同一答案位置的原始二分类分布。尚未运行验证各分支命中比例。
- **代码配置传递**：verl/trainer/ppo/reward.py 静态核验 reward_kwargs 被绑定到默认评分函数，未发现“奖励参数全部丢失”的证据；实际值仍需记录训练日志确认。
- 警惕：confidence/calibration、plausible explanation 与 faithful reasoning 是不同性质；低 CDE 不自动证明真正隐含语义恢复。

## 06. 数据集与 Ground Truth
- HatefulMemes（Meta）：binary 训练 8,500 / 测试 1,000；FG 扩展标注攻击七类、protected categories 五类，多标签。原始数据包含 image/text confounders，有助于检验跨模态需求，但不能保证当前模型真实依赖图像。
- MAMI：binary 训练 9,000 / 测试 1,000；细粒度 objectification/shaming/stereotype/violence，多标签。
- PrideMM：binary 训练 5,063 / 测试 507；细粒度 stance 和 target 类别。
- Hatred：有人工 gold rationale 的 2,982 train / 246 test，**仅含 hateful 类解释**，且来源关联 HatefulMemes；不能当作与 HatefulMemes 完全独立的第四数据源。
- §B.3 声称 HatefulMemes binary dev seen 用于验证、test seen 用于测试；fine-grained dev unseen 用于最终评价。需要结合公开脚本独立对照。
- 政策规范转为结构化手册为专家一次性操作，细粒度 GT 沿用公开基准；无证据表明本文新标注了大规模解释训练集。
- 标签与样本质量仍有多标签不平衡、上下文误读与图文捷径风险。

## 07. 主实验与基线（表1；Qwen2.5-VL-7B）
- 数据/系统：Direct-SFT，zero-shot，Explain-then-Detect SFT/DPO/GRPO，RA-HMD（直接检测），LOREHM / U-CoT+（解释式系统）；不同模型与工具并非都同预算同能力。
- HatefulMemes B F1：Direct-SFT 75.0，RA-HMD 80.2，Explain DPO 73.6，Explain GRPO 74.5，**ExPO-HM 81.1**。相对最强 direct RA-HMD 仅 +0.9 个百分点；相对 plain GRPO +6.6。
- HatefulMemes attack micro F1：GRPO 61.2 → ExPO-HM 75.6（+14.4）；target micro F1：64.5 → 77.2（+12.7）。
- MAMI B F1：GRPO 76.8 → ExPO-HM 82.3（+5.5）。
- HatefulMemes LLM-as-judge：GRPO 5.2 → ExPO-HM 6.2（0–10）。
- Table 1 指标 B 属于宏 F1，而细粒度为微 F1，不混为一个评测口径。

## 08. 消融、解释与校准证据
- Table 2（Qwen2.5-VL-7B / HatefulMemes）：
  - naive GRPO：B/Attack/Target = 74.5/61.2/64.5；LLM=5.2；CDE=.263。
  - +SFT-PM：75.8/70.8/70.2；LLM=5.6；CDE=.092。
  - +GRPO-CL：78.4/74.3/76.1；LLM=5.8；CDE=.056。
  - +CDE：**81.1/75.6/77.2；LLM=6.2；CDE=.026**。
- Table 3：SFT-PM 完整训练后 B F1 81.1/解释6.2；仅 SFT-R（gold explanation warmup）79.2/5.7；SFT-FG 78.9/5.6；SFT-B 73.5/5.1。只支持本协议比较，**不能泛化为解释监督无用**。
- §4.3：60 个模型配置×种子点的 CDE 与 LLM judge 相关 Pearson r=−.78、Spearman ρ=−.81；是聚合相关，不是解释变化的因果证据。
- 人评 §4.7 Appendix F：3名标注员；coherence 96%→100%；helpfulness 1.6→2.2（0–4）；Krippendorff alpha=.71。说明相对有用性，但不验证内部机制忠实。
- Appendix D/E：GPT-4o-mini 主 judge；其他 judge、BERTScore补充。解释评分会参考最终模型预测，错误标签可能触发最高分限制，因而**解释评分并非与分类正确性完全独立**。
- Appendix H：ECE / Brier 改善，支持概率校准改善；仍**不证明解释 faithful**。
- Appendix J：共享失败案例包括需要多步隐含语义、外部背景知识及模态关联的 Meme，不能说已解决隐式内容推理。

## 09. 公开实现与论文不一致（仅静态核验）
- **GRPO 课程**：论文后半 50/50 混合 FG+binary；当前 scripts/grpo/train/run_qwen2_5_vl-7b_cde_paper.sh 先 FG EPOCHS=3，再 binary EPOCHS=3，第二阶段指定 BINARY_TRAIN_PATH 只有二分类。**任务配比不符**；按 epochs 未必等于论文 “各占一半 steps”，训练样本数不同更不能直接换算。
- **组采样**：Figure 2 G=8，当前脚本 rollout.n=5，可能影响相对优势与预算。
- **reward/entropy**：论文更一般的 full vocabulary CDE、Eq.(9)/(11)权重；当前 binary 默认 binary entropy、FG top-k entropy、错判中间区间二次插值及缺失 logit 回退。需保存且不可一概宣称已对齐。
- **验证集**：当前脚本 TEST_PATH=./data/verl/FB/test.parquet，设置 data.val_files=TEST_PATH，每5步运行验证；generate_hatefulmemes.sh 的 FB test.parquet 对应原始 test_seen.jsonl。论文称 dev seen 用于验证、test seen 用于测试，因此**存在潜在 test-as-val 风险**，是否构成实际评测泄漏取决于选择 checkpoint、验证日志、最终测试使用划分，未核实；不能直接称“作者泄漏”。
- **模型初始化**：GRPO 脚本期望先合并 SFT LoRA 到 HF checkpoint；不能直接拿其默认 7B 全参数或独立新模型来代表作者模型链路。
- **再现声明**：docs/reproducibility.md 明确本公开版本使用比最初开发时更新的 verl 与 LLaMA-Factory，结果可能不等于论文；目前只有静态审计，**没有启动 GPU 训练、没有核验数据实物/日志/具体 checkpoint**。
- **资源**：正式论文 Appendix C 报 GRPO/ExPO-HM 8×H100 80GiB，约4h；LoRA r=64、alpha=128、冻结视觉模块；不能推断共享单卡16–20GiB可按原法完整复现。

## 10. 严格 novelty / 反面证据
- 方法贡献是 **structured policy SFT + coarse/fine curriculum GRPO + correctness-conditioned decision entropy reward 的训练协议组合**，不是新分类骨干，也不是新隐晦数据集。
- CDE 最有辨识度，但作为解释代理存在 proxy gap：决策置信度不等于内容理解；人工与 LLM 评分偏向 plausibility/helpfulness，未给出针对解释内容的固定输入/参数反事实干预来证明 faithfulness。
- 递进消融支持每个模块在当前设置下有增益；仍不能证明 CDE 优于同预算温度校准/label smoothing/简单熵奖或等长解释控制；课程序列是否使模型学习语用而非类别先验也未充分识别。
- 对比“P027比全部最强直接检测有巨大提升”必须注意：相较 RA-HMD 在 HatefulMemes binary 仅 +0.9 F1 point。
- 论文 Appendix J 明示对真正复杂隐含 Meme、外部知识语境失效；这是研究问题证据但不是独占创新空间。

## 11. 与项目既有研究的连接
- P030 SMARTER：以解释/标签数据构造 DPO 偏好；P027 以结构化政策知识和 CDE 等程序奖励做 GRPO；区别是直接解释偏好监督 vs 间接不确定性反馈。
- P019 V-FLUTE：图文修辞蕴含和解释监督，任务标签不能与 hateful meme detection 直接统一。
- P034 CrossGuard：侧重 text/image 分开无恶意、组合显露意图的多模态 guard，P027 是 meme hateful 分类/细粒度/解释；两者训练方式和标签假设不同。
- 可能迁移的机制：利用现有细粒度标签形成策略/政策辅助监督，研究解释忠实性与多模态必要性。但只能是审计线索，不得先宣称空白或顶会 idea。

## 12. 最小 Kill Test / 未解决事项 / 复现边界
1. **协议审计优先（无GPU）**：训练 parquet 的 data_source、split、checkpoint 与 Script 实际 CDE 模式；确认论文 50/50 vs 公开两阶段、G=8 vs n=5、论文开发代码和最新开源代码的对应版本。
2. **奖励单测（CPU）**：固定 logits/概率，校验 binary/FG 阈值、incorrect 中间区间正负、partial match、奖励 kwargs、缺失候选回退；确认实际 CDE 是否非零及异常样本率。
3. **评测隔离（无GPU）**：追踪 dev_seen/test_seen/dev_unseen/hatred 相关样本 ID，确认早停/选模型时使用 split，避免测试集选 checkpoint。
4. **低成本机制诊断（若能拿到现有模型/预测）**：固定 x、模型，变更解释中目标/攻击/模态关系与无关措辞，观察决策与校准变化；控制正确/错误标签组别。结果仅支持一定程度的解释依赖，仍需对比模型是否依赖图像。
5. **研究资源约束**：不把 8×H100 GRPO 当作 ≤6h 单卡直接 Kill Test。先验证公开数据可得、预训练 3B 冻结或 inference-only，必要时再评估 LoRA 可行性。
6. **未证**：严格复现论文数值、训练最优 checkpoint、CDE 与 faithful explanation 的因果机制、标签/图像依赖、完整代码协议及具体可运行峰显存。

**归档结论**：P027 为 ICLR 2026/CCF-A 有实证支持的方法型工作；关键贡献是利用细粒度政策与课程奖励改善解释式检测，CDE 并非直接解释正确性评判。已完成正式论文和核心源码静态分析，保留全部开放风险并由用户授权定稿。**下一篇按既定 CCF-A 队列精读 P013（Exploring Concreteness Through a Figurative Lens，ACL 2026 Main），其后 P022/P035/P036。**
