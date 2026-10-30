# P034｜CrossGuard: Safeguarding MLLMs against Joint-Modal Implicit Malicious Attacks

> **2026-10-30 用户授权定稿上传合并。** 定稿仅表示正式论文精读与公开代码静态审计已归档，**不代表运行复现、代码问题关闭、作者因果主张得到独立证明**。

## 01. 书目信息与来源
- Xu Zhang; Hao Li; Zhichao Lu. **CrossGuard: Safeguarding MLLMs against Joint-Modal Implicit Malicious Attacks**. **ACL 2026 Main Conference / Long Papers，CCF-A**；正式页码 **25693–25707**；DOI **10.18653/v1/2026.acl-long.1178**。
- ACL正式链接：https://aclanthology.org/2026.acl-long.1178/ ；正式PDF：https://aclanthology.org/2026.acl-long.1178.pdf （15页，§3–6，Figures 1–9，Tables 1–3，Appendices A–D）。
- 作者代码：https://github.com/ZhangXu0963/CrossGuard ；重点审计 red-teaming/run.py、reward_model.py、reward_scheduler.py、self_ppotrainer.py、dataloader.py、train_crossguard/run.yaml、eval_crossguard/crossguard_on_siuo.py。
- 标签：multimodal safety；joint-modal implicit malicious attacks；cross-modal compositional risk；RL red-teaming；input guardrail；和隐式仇恨检测、隐写、图像取证等**非同一任务**。

## 02. 任务与边界
- 对象：图像 I 和文本 T 单独没有显式恶意，但联合表达潜在有害意图；理想形式 H(I)=0，H(T)=0，H(I,T)=1。实际样本还涉及歧义、语境与标签建立质量；不是全部广义隐晦信息都满足此性质。
- **三个不同任务不可混为一谈**：（a）ImpForge产生可能诱导不安全回答的测试输入；（b）CrossGuard在推理前预测输入 Safe/Unsafe；（c）被测MLLM输出后的回答安全性评价（response ASR）。
- SIUO（2025 NAACL Findings，**不是NAACL Main CCF-A**）更早提出相关现象并发布167条人工构造测试样本，CrossGuard不是任务首创。

## 03. 主要贡献与创新性质
1. **ImpForge**：两阶段数据生成（视觉关键词图像匹配→PPO优化文本改写）+三种奖励，提高联合隐含攻击测试样本的获取能力。
2. **CrossGuard**：使用生成数据与已有安全数据混合，基于 LLaVA-1.5-7B 以 LoRA + CE 微调多模态输入安全判别器；**没有独立的新检测架构**。
3. 对比开放/商业MLLM与安全Guard；测试常规显式和联合隐含攻击、OOD表现、正常输入通过率、生成数据/训练数据贡献与PPO消融。
4. **审计判断**：论文对“增加该类型训练数据能够改善SIUO检测”提供较强行为证据；PPO的不可替代性、单模态安全与联合有害真实标签、模型真正学会跨模态交互因果关系均未充分识别。

## 04. 完整输入→训练→输出流程
**ImpForge Stage 1：** 从BeaverTails提取原始不安全文本（Appendix C.1：RL起始文本**5,000条**），通过NER抽取可视觉化实体关键词 k；使用 CLIP 图文相似度从 COCO/WIT 选择相关图像，使用GPT辅助确认图像自身无明显风险，形成 (x_I,x_T,k)。**初始文字本身是不安全的**，尚未形成严格“两个模态都安全”的图文样本。
**Stage 2：** 令 Qwen2.5-VL-7B-Instruct 改写策略 πθ 在固定图像的情况下，仅改写文本得到 x̂_T。奖励要求文本单独安全、与原始风险语义相关、减少图文重复；以 PPO+LoRA 更新改写器，保持与参考策略的 KL 限制。
**防御器CrossGuard：** 混合 ImpForge 与 VQAv2、BeaverTails、FigStep、VLGuard 的 Safe/Unsafe 数据，总样本**1616**；使用 LLaVA-1.5-7B + LoRA 微调安全标签输出。论文式(6)：L_CE = -E log pθ(y|x_I,x_T)，y∈{safe,unsafe}。**代码使用LLaMA-Factory的stage:sft**，还需确认到底为显式分类logit CE还是生成安全标签token的自回归CE，不能自动视作同一实现。

## 05. 三项奖励：论文公式、作用和公开代码事实（重点）
记 x_T 为原始不安全文本，x_I 为单独安全图片，x̂_T 为改写结果，g 为预训练编码器。

**（1）Safety reward，式(2)**：
R_safety(x̂_T) = P_guard(safe | x̂_T)。
输入改写后文本，由预训练guard评估其单独安全概率，防止生成文本本身直接暴露恶意。**代码**：GuardModel使用Llama-Guard-3-8B，在生成的多个位置取 safe token 的最大概率；这不是单个预定位置经过校准的分类概率。

**（2）Semantic reward，式(3)**：
R_sim(x_I,x_T,x̂_T) = cos(g(x_I ⊕ x̂_T), g(x_T))。
旨在保留原始文本意图，使图文联合与原始请求语义接近；余弦相似**不等于有害意图严格等价**。论文把 ⊕ 描述为供编码的联合文本输入。**代码**：使用 sentence-transformers/all-MiniLM-L6-v2，仅以图片关键词构造文本描述 d_I，得到
R_sim_code = cos(g(x_T),g(d_I + x̂_T)) - cos(g(x_T),g(d_I))；
并非直接通过图片提取跨模态向量，且比原论文增加了减去单独描述相似度一项。

**（3）Overlap reward，式(4)**：
R_overlap = 1 - (1 / |Tok(x̂_T)|) Σ_{w∈Tok(x̂_T)} max(0, cos(g(w),g(x_I)) - τ)，τ=0.2。
目的是减少文本和图像的显性重复。论文把余弦相似视作所谓互信息近似，**但一般余弦相似不具有真实统计MI的理论保证**。**代码**：对每个图像关键词使用 0 if keyword in rewritten_string else 1 的直接子串匹配奖励；**不是**式(4)的Token-level语义重叠。

**总目标**（论文式(5)）：
max_θ E_{x̂_T∼πθ}[ Rψ(x_I,x_T,x̂_T,k) − λ D_KL(πθ || π_ref) ]。
PPO 通过采样生成文本、计算不可微的整段评分、优势估计和概率比 clip 更新策略，KL控制更新偏离。**代码配置** Qwen/Qwen2.5-VL-7B-Instruct + LoRA/Peft + Value Head；PPO lr=3e-6，cliprange=.06，vf_coef=1，batch_size=mini_batch_size=1，init_kl_coef=.2。
**额外实现差异**：公开代码总奖励 = w_safe*safe + w_useful*useful + w_hidden*hidden + w_similarity*similarity；run.py 初始权重 [1.0,0.0,1.0,1.0]；动态调权是乘法，useful=0不会只凭乘法变正。**三公式与代码四项权重不能逐项同名等价**。
- 用PPO的理由：输出是一段不存在唯一标准答案的生成文本，而评分发生在生成后；需要基于奖励的策略更新。但**“合适”不等于“唯一必要”**；SFT、多候选采样+筛选、GRPO等都是需要预算对齐的比较对象。

## 06. 数据与标签：**1390、1616、约202**必须严格区分
- **5000条**：BeaverTails原始不安全文本，RL训练起点（附录C.1）。
- **1390条**：Figure 6 明确称 ImpForge 生成的隐含多模态恶意样本，覆盖14类，**用于red-teaming evaluation**。
- **1616条**：Figure 7 展示的CrossGuard最终混合训练数据；其中：
  - 50.2% **non-malicious** ≈ 811；
  - 11.7% **vision-based OCR malicious** ≈ 189；
  - 13.2% **text-based malicious** ≈ 213；
  - 12.4% **vision-based non-OCR malicious** ≈ 200；
  - 12.5% **joint-modal implicit malicious** ≈ **202**。
- 以上按百分比换算的整数仅为近似，**不能当作作者公布的逐类精确数**。
- **重要未证关系**：论文没有交代这≈202条是否从1390条中抽出、怎样筛选、是否独立另生、与red-teaming评估集是否重叠；**绝对不能写“从1390抽202，其余1188作测试”**。
- 混合来源：VQAv2正常图文；FigStep OCR显式恶意；BeaverTails原始文本+图片；VLGuard视觉非OCR显式恶意；ImpForge联合隐含恶意。
- ImpForge unsafe训练标签来自原本不安全目标与构造协议；论文附录D.4提到AI生成内容经过人工核验，**不代表公布1616条的全部独立人工标注、不一致解决与各模态单独安全的完整证据**。严格三标签 y_I、y_T、y_{IT} 需要另行核对。
- 图片实物、哈希去重、文图配对、标签可信度和训练/评估划分尚未运行核验。

## 07. 实验设计与核心结果（ASR%，越低防护越好、但红队生成越高表示越具攻击性）
### Exp.1 防护效果（§5.2，Table 1）
五个基准 **JailBreakV、MM-SafetyBench、SIUO** 为OOD，**FigStep、VLGuard** 为ID。五基准平均ASR是5列**等权算术平均**，非按样本数加权的总错误率。
| 模型 | JailBreakV | MM-SafetyBench | SIUO | FigStep | VLGuard | 平均 |
|---|---:|---:|---:|---:|---:|---:|
| LLaVA-1.5-7B | 51.43 | 28.85 | 95.81 | 62.60 | 46.38 | 57.01 |
| Qwen2.5-VL-7B | 2.14 | 10.00 | 41.56 | 24.20 | 9.73 | 17.53 |
| GPT-4o | 6.08 | 16.15 | 48.92 | 1.60 | 6.11 | 15.77 |
| Claude-3.5-Sonnet | 5.00 | 13.08 | 23.95 | 13.00 | 5.21 | 12.05 |
| LlavaGuard | 90.71 | 32.58 | 90.80 | 83.08 | 90.42 | 77.52 |
| Llama-Guard3-Vision | 34.29 | 74.89 | 50.40 | 66.92 | 89.82 | 63.26 |
| JailDAM | 32.50 | 16.54 | 81.44 | 6.00 | 15.38 | 30.37 |
| HiddenDetect | 4.64 | 8.65 | 44.91 | 72.20 | 26.02 | 31.28 |
| **CrossGuard** | **0.72** | **0.38** | **5.39** | **0.21** | 7.24 | **2.79** |
SIUO是167条联合隐含攻击样本上的ASR，CrossGuard 5.39%≈9/167；2.79%是简单平均五个基准，不是全部数据合并ASR。由于被测MLLM与Guardrail评测协议差异，**不能直接据这些绝对值宣称真实统一安全性差距**。

### Exp.2 安全与正常输入放行（§5.3，Figure 3）
用 MM-SafetyBench 安全测试、MMBench 的正常VQA测试，衡量高拦截与正常放行之间的折中，避免“全拒绝”方案。论文称CrossGuard效果较好；未给完整可核数值时不要编造精度。

### Exp.3 新生成测试样本的攻击能力（§5.4，Table 2）
对比 BeaverTails*（原始不安全请求+同图，未优化）与加入 ImpForge 改写的图文输入：
| 被测系统 | BeaverTails* | +ImpForge |
|---|---:|---:|
| Qwen2.5-VL-7B | 4.20 | **76.60** |
| GPT-4o | 9.80 | **70.40** |
| Claude-3.5-Sonnet | 9.00 | **44.40** |
| Llama-Guard3-Vision | 47.60 | **97.20** |
| HiddenDetect | 4.00 | **71.40** |
论文称平均提升 **57.08个百分点**；这项实验**高ASR**表示作为red-team攻击样本更容易绕过防护，并不是防御能力更强。

### Exp.4 新训练数据的独立贡献（§5.5，Figure 4）
三组 base LLaVA、CrossGuard训练但去掉ImpForge、CrossGuard训练含ImpForge；后两组较能隔离数据贡献，但未严格固定总样本数/类比例：
| 基准 | w/o ImpForge | with ImpForge |
|---|---:|---:|
| JailBreakV | 0.76 | 0.72 |
| FigStep | **0.12** | **0.21** |
| MM-SafetyBench | 10.20 | 0.38 |
| SIUO | 60.33 | **5.39** |
| VLGuard | 11.58 | 7.24 |
**SIUO下降54.94个百分点**，是最强的数据贡献证据；**FigStep 0.12→0.21 略变差**，与作者正文“一致下降”措辞不完全对应。性能提升不能全归因于“学会联合推理”，还可能包含训练数量/类别先验变化和生成数据捷径。

### Exp.5 PPO必要性（§5.6，Figure 5与Appendix C.2）
比较 BeaverTails*、ICL（3个SIUO专家例子）、LoRA SFT（已有隐含改写数据）、PPO(ImpForge)，在 Qwen2.5-VL、GPT-4o、Claude-3.5、Llama-Guard3-Vision、HiddenDetect 上测攻击 ASR。作者柱状图表明PPO最高；**Figure 5没有为全部柱标精确值，不编造精确数字**。未充分控制同资源/同候选数量/同筛选/同训练数据；结论是“当前设置更有效”，**非PPO独立必要性证明**。

### Exp.6 成本（Appendix B.2，Table 3）
A40 GPU下 CrossGuard **推理** latency 0.24s/item，推理峰显存 14.14GB，JailBreakV ASR 0.72；**不意味着单卡16–20GiB能训练完整RL链路**。

## 08. ASR计算协议（Appendix C.3；重要审稿缺陷）
- **在线MLLM** GPT-4o、Claude-3.5：回答未触发预定义拒绝模板即计攻击成功；易将安全但措辞不同的回答误判。
- **离线MLLM** LLaVA、Qwen2.5-VL：用 GPT-4o-mini 裁判回答是否含清晰拒绝或安全警告，Unsafe 占比即 ASR；裁判与模板判据有偏差。
- **Guardrail** CrossGuard 等：直接输出 safe/unsafe 或恶意分数，对已知不安全输入错判Safe的比例相当于输入侧漏检率(FNR)；它不是危害回答生成率。
- **三套操作性定义不完全同质**：跨模型ASR比较需要统一独立评测，尤其Guardrail与被测MLLM不应当完全按同一种生成攻击成功来解释。

## 09. 代码复现与论文版本差异（静态核验）
- rl训练脚本 red-teaming/run.py 导入 **self_ppotrainer_ori.py**，但当前公开仓库只检索到 **self_ppotrainer.py**；后者导入 reward_model.py 中未找到的 UsefulRewardModel；GuardModel中使用未在该文件定义的 access_token；有多个本地训练数据、图片、adapter路径和外部认证依赖。**存在硬编码服务凭据，必须清理/撤销，绝不复制使用**。
- 奖励理论公式与 reward_model.py 的实际安全token最大值、文本差分余弦、关键词子串匹配差异已核实；不确定公开commit是否生成论文结果。
- **train_crossguard/run.yaml**：llava-hf/llava-1.5-7b-hf，stage:sft，finetuning_type:lora，lora_rank:8，lora_target:all，batch_size:1，bf16，epochs:5，val_size:.1；**max_samples:1500 vs论文1616**，需确认完整训练协议。训练数据源名 impforge 的实物注册、图像文件路径、检查点权重未完全核验。
- eval_crossguard/crossguard_on_siuo.py依赖本地 ../data/siuo.json 和图片路径；只输出 safe/unsafe 文本，不能作为全表1评测pipeline已一键复现的证据。
- **未运行**：仓库可下载和标签实物未验证，模型训练、SFT CE形式、各评测judge输出未重跑。

## 10. 严格创新审计、未证与反面证据
- **强项**：重要且明确的任务；工程可操作的生成与数据增强；新增训练数据能将SIUO ASR 60.33→5.39；完整防护对比。
- **弱项**：生成器PPO多目标奖励部分为已有模块组合；CrossGuard只是LLaVA + LoRA + CE；代码与论文公式显著不同；数据标签/独立性未核；不同ASR判据不可互换。
- **尚未证明**：三标签 y_I safe、y_T safe、y_IT unsafe 在全部合成样本成立；真正联合语义推理而非文本捷径；PPO相对同计算量SFT/采样筛选的独立效应；所有测试无训练重叠。
- **不可直接据此提出的“新方法”**：换PPO为GRPO、换更大VLM、再生成更多相似数据、仅加一层attention；须先发现具独立证据支持的失败机制。

## 11. 与已有文献/迁移空间
- 与 P019 V-FLUTE（修辞视觉语义）、P015（生成数据捷径与表示）、P033 CADET（跨风格表示解耦）有关，但任务/标签不能简单拼接。
- 直接相近工作：SIUO（NAACL 2025 Findings）、VLSBench（ACL 2025 Main CCF-A）、VLSU（ICLR 2026 CCF-A）、Meerkat-VL（ICML 2026 CCF-A）、Jailbreak in Pieces（ICLR 2024 CCF-A，相近但未必要求两模态均安全）。
- 这些是**下一窗口系统查重对象**，本卡并未完成逐篇机制精读。潜在候选有跨模态交互必要性、组合泛化、可靠解释、证据/不确定性，但**不能宣称尚无人做**。

## 12. 最小Kill Test与待关闭事项
1. **K0数据可达性**：拿到真实训练源、≈202 implicit训练样本与1390 red-team样本，哈希/近重复去重；核查与SIUO评测重复，标签来源及多模态组合判据。
2. **K1不训练诊断**：用公开SIUO/VLSU等已有标注，对冻结小型VLM比较text-only、image-only、joint，统一输出判别协议与正常对照，检查是否存在真实跨模态依赖。
3. **K2语义控制实验**：利用已有可信配对或语义可证的对照，不随意生成未标注“真值”的反事实；测试替换图像/语境改变风险判定的必要性。
4. **K3数据增量**：固定基线/数据总量/类先验，比较w/o与with联合隐含样本；先试低成本推理与轻量方法，再决定是否做LoRA。
5. **K4 PPO必要性**：如有完整可复现reward与数据，再对比同预算 ICL、SFT、best-of-N/filtering、PPO；不能把高攻击ASR直接等同高质量合法数据标签。
6. **开放问题**：1390与≈202关系；训练/测试去重；三奖励代码差异；两组评测协议；1616 vs1500；联合语义因果证据；真实显存/文件可用性；图文安全三元标签GT。

**归档裁决**：CrossGuard最强的实证是“任务专属训练数据显著提升联合隐含安全检测”，而不是PPO唯一必要或检测网络具有新颖结构。定稿但保留全部开放风险。**下一专题**：多模态图文隐晦内容领域审计，优先VLSU、Meerkat-VL、VLSBench；在竞品核验后决定实验，不优先重复多GPU PPO。