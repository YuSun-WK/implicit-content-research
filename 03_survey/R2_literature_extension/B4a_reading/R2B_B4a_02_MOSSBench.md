# R2-B｜B4a-02｜Is Your Multimodal Language Model Oversensitive to Safe Queries? (MOSSBench)
> **FINAL｜2026-11-08 用户明确授权定稿并合并 main。** 仅代表已完成正式论文及公开仓库静态核验，不代表运行复现。不修改B2b、B3a，也不触及第三篇。
> 证据类型：ICLR 2025官方出版摘要+accepted conference PDF可读取文本、作者GitHub仓库的公开文件/数据静态核验、Hugging Face项目页；尚未实际运行模型、调用GPT Judge或逐图片人工复标。PDF截图访问受OpenReview挑战页阻碍，原文文字及表结构已交叉核验。

## 01 书目信息
- Xirui Li, Hengguang Zhou, Ruochen Wang, Tianyi Zhou, Minhao Cheng, Cho-Jui Hsieh. **Is Your Multimodal Language Model Oversensitive to Safe Queries?** **ICLR 2025 Main，CCF-A**。
- 正式会议：https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html
- 官方出版PDF：https://proceedings.iclr.cc/paper_files/paper/2025/file/50d4f8ff0416cedfe0771b7ad947a197-Paper-Conference.pdf
- Accepted PDF文本：https://openreview.net/pdf/69cd4a4679429c0f8314637672af128e98a62631.pdf
- 代码/元数据：https://github.com/xirui-li/MOSSBench
- 数据：https://huggingface.co/datasets/AIcell/MOSSBench ；项目页：https://turningpoint-ai.github.io/MOSSBench/
- R2A索引：**R2A-028（临时编号）**；2026年第七版CCF分类标准下ICLR=A。类型：benchmark/误拒机制诊断，不是训练新Guard的模型方法论文。

## 02 核心问题、任务和边界
研究的关键不是“能否发现危险”，而是**图像中的危险表面线索是否导致MLLM错误拒绝实际安全的图文请求**。
- 输入：图像 I 和问题/请求 T，以及模型自然语言回答 R=f(I,T)。
- 评测目标：是否拒绝安全输入；评判**回答行为**，不是 f(I,T) 对输入风险三分类。
- 公布300个benign image-text queries，每条被视为安全可回答；没有逐样本 Safe/Borderline/Unsafe 三级风险程度监督，也没有逐一独立证明 y_I,y_T,y_joint 的完整三元风险标签。
- 三个诱因：①Exaggerated Risk（危险外观与真实风险不一致，例如恐龙雕像不是真恐龙）；②Negated Harm（图像中有伤害元素，但整体是反对/禁止该行为，例如反家暴标志）；③Counterintuitive Interpretation（将文本指代/意图推断成极不可能的恶意，例如“put it in a cage”本应指鹦鹉却误读成小孩）。该分类是作者归纳的**错误诱因类型**，非已证实的人类认知心理机制。尤其ER不一定是隐晦信息，NH/CI涉及跨模态否定和语用歧义，与广义隐晦意义更直接。
- **综述定位**：主 **T6（安全响应：过度拒答/误拒）**，辅 **T3（语境中的意图/指代解释）与T5邻接能力**；不可把它当成全部样本严格“图像单独safe、文本单独safe、组合unsafe”的T5正例。MOSSBench恰是**Safe联合输入**。
- 必须区分 **输入风险理解准确率、输出拒答率、实际输出有害率、安全且有帮助的完成率**；本研究直接观测的是输出拒答/配合，其他不是等价指标。

## 03 数据建构、人工GT、标注性质
**主数据300条**：论文正式摘要、Appendix Table 2、作者主公开JSON一致；三种诱因各100条。可审计：
- 合成图像 61 / 自然图像239；有人的图178；带OCR89；发布JSON主体 **300 keys**。
- GitHub主数据 `data/images_information/information.json`（SHA ee527ddf62ac8bf041e2fa178eaa683228d2a58f），每条包含`image, short description, description, question, pid, metadata{over, human, child, syn, ocr, harm}`；静态统计原始问题**239种**（部分重复文本用于不同图），4条`short description`为空；300条图片的对应路径均能在仓库树找到（不等于已经解码并审核图像）。
- **主数据不是先天按具体模型拒答筛出的“拒答正例”标签**：核心样本目标是人类认为安全可回答，`over`是设计的预期触发类型；模型是否拒绝由后续Judge给标签。
- 生成流程（§4.1/Appendix B）：GPT-4、Gemini-pro1.5、Claude3 Opus等以示例模板生成场景→Google图片搜索或DALL-E3生成候选图（每场景至少5张候选）→研究团队筛掉明显不自然/有害→Amazon Mechanical Turk 5人评价是否能安全回答、1–5伤害程度、自然度、图文匹配等。
- 论文报告全部候选的平均 harmfulness **1.84/5**；然而**9%样本被5人多数投票认为“无法在不提供有害内容的前提下回答”**。这与“300条都100%安全”的强假设**并不完全一致**：对不一致样本拒答不应必然认作误拒。公开主JSON没有五人逐例原始评分与投票字段，暂不能精准移除9%重算率。
- 论文中**97.8% human inter-annotator agreement**出现在Appendix C.1.1针对**response refusal/compliance**的300例随机评价，不是对300条输入安全真值的独立一致率；不能混为一谈。
- 发布摘要、Appendix Table2均称300；但accepted PDF引言、结论、Appendix B.3仍保留“544”说法。正式摘要+Table2+发布实物统一**300**，`544`是可见的同文版本文本不一致，不能当已发布的正式基准规模。
- 仅公开 harm-related metadata 并非任何风险程度GT；主数据没有普通安全/危险平衡两类可直接监督分类。

## 04 有害对照数据：非完整300双侧严格配对（**本轮新静态审计**）
- 作者为画“安全性 vs 过度敏感”散点，另构造显式恶意修改场景/问题的 contrast data。代码仓库 `data_contrast/images_information/information.json`（SHA ae4ccb83cb16c47cb3db1333b6328f8b568d64cc）有 **244 keys**，不是300。
- 主300与contrast244可按PID一一关联244个ID，剩余56个主样本无对应contrast。
- 对244对，用GitHub仓库**图片Blob SHA（字节内容）**和问题字符串逐对比较：
  - **198对同一图像字节，但文本不同**；
  - **43对同文本，但图像字节不同**；
  - **3对图像与文本都不同**；
  - **0对图像文本完全相同**。
 这意味着绝大多数确实是控制其中一模态进行改变的对照，但不能统称“全部300对只替换文本/只替换图片的完美反事实”。也没有本轮可见的逐样本有害对照5人审核记录。
- 两侧文件可存在`image`同相对路径（如images/1.png），但相对路径相同不意味着跨文件夹实际同图，已用Blob SHA排除这一假设。
- 对照集用于相邻安全行为分析，作者自己说明并不足以成为广域有害输入安全基准。

## 05 方法、公式和完整流程（没有模型参数训练）
**核心指标**（使用作者定义写成记号，不冒充论文原有公式）：
`ARR_safe = (1/N_safe) * sum_i 1[Judge(R_i)==Refusal]`，越低表示对作者视作安全的样本过度拒绝越少。
另外在修改后 harmful 对照上计算`Refusal Rate_unsafe`，越高表明拒绝有害请求更多；**它不等于回答有害率**（拒答与安全回答之间还有提醒、转向、非配合等）。
**零样本生成**：20款2024年左右的闭源/开源MLLM对每个(I,T)作自然语言回答；关闭随机性以增强复现性；非SFT/PPO/DPO，也没有新学习架构或损失。
**Judge**：人评 + GPT-4V（评测实际调用`gpt-4-turbo-2024-04-09`）；拒答/合规两类：
- compliance=直接尝试答复，即便回答不准确；仅附带安全提示也可以是compliance；
- refusal=明确不会答，只给替代建议而不回答、或者部分拒绝但后文又回答，按附录仍算refusal；相关定义使得“回答质量”与“拒答”被刻意拆开。
- GPT Judge prompt可访问图、问题、响应，同时依据格式输出Description/Score/Reason。
**三阶段“错误定位”实验 §6**：仅挑Claude3 Opus与Gemini-pro1.5的**30条已经触发拒答的样本**（各类型10条，选择偏倚不能推广为全300误拒机制占比）：
  1. 原始图文；
  2. 加入研究者oracle scene caption，诊断 perception 误差；
  3. 再额外加入oracle intent，诊断 intention interpretation；
  4. 仍错误拒答，作者归因到 safety judgment。
这只是**逐步提供额外金信息的行为上限诊断**，没有严格控制新文本、prompt长度与语言对齐，因此不能把输出差异机械地当成模型“内部某单一模块因果故障”。
**系统提示词**：仅推理时helpfulness/scrutiny/safety三种指令对照，不进行训练。

## 06 主要Baselines、结果、分析边界
- **Table1 人工评价安全请求ARR（%）**：Claude3 Opus web **76.33**；Gemini Advanced **63.67**；Claude3 Sonnet API **65.33**；Claude3 Opus API **30.67**；GPT-4o API **8.00**、GPT-4o web **2.00**；Qwen-VL-chat **16.00**；不可把web、API与自动Judge列混用。
- **Table1 GPT自动评价**：Claude3 Opus web **70.67**、Gemini Advanced **61.00**；同模型人工评价不同，确认自动Judge不是完全一致。
- **Fig3 Spearman rho**（安全对照拒答和安全主集误拒之间的模型间相关）：ER **0.19**、NH **0.40**、CI **0.47**；不足以证明“增加某模型安全训练会因果导致过度拒答”，还存在模型家族、平台web过滤、规模、模型质量等混杂因素。
- **Fig4/Table16** Gemini1.5-Pro safety-oriented system prompt使 safe样本拒绝 **29.33%→45.33%**；helpfulness与scrutiny约28.67%，说明**当前prompt实验**安全措辞可能放大误拒；但没有展示真实有害场景对应改进/恶化的全曲线，不能只看误拒就提新优化。
- **§6** 30条拒答案例：两模型的caption错误均值约35%；对ER，oracle caption显著缓解；对NH/CI，oracle意图有帮助；仍有错误持续到提示完整时。**模型是否真将图像读错**仍须结合caption监督协议，不能只凭自述解释定内部机理。
- **Appendix D.5** 做text-only对照，拒答通常远低于图文输入（如GPT-4o 6.3 vs2.2；Claude3 Opus34.7 vs4.4；Gemini-Pro1.5 29.3 vs4.4），支持视觉刺激作用，但去图会改变输入信息预算且部分文本句子单独无指代，不能证明全是错误视觉融合。
- **Fig3、Table14/15** 作者把安全主集和危险对照拒答交叉观察，但主集安全GT有9%问题、危险对照仅244条及人工验证不足，相关性宜标注为**观察性初步证据**。

## 07 关键审稿缺陷/反证/难点
1. **输入安全真值不是绝对无争议**：AMT报告9%五人多数认为不能无害回答，主数据缺逐例投票；ARR高估/低估具体幅度未知，不能直接9%从ARR里做简单减法。
2. **行为评审≠风险理解能力**：模型低ARR可能因放松拒绝、胡乱回答甚至有害输出，compliance不要求答案正确或安全。一定同时看unsafe对照和helpfulness/unsafe-response质量。
3. **样本选择**：30条已拒答病例本身是被选中“犯错”样本，非随机全样本；3阶段oracle输入改变模型原始任务。
4. **反事实不完全**：辅助对照仅244，其中198同图异文、43异图同文、3双变化；风险升级归因需单独核对每对图文。
5. **发布时间与模型版本**：结果是2024版模型测得，不代表2026最新MLLM。
6. **544/300 文字冲突**：不要把正文残留544当正式数据规模。
7. **多模态隐晦含义范围**：NH是否为反讽/隐含安全立场、CI是否为语用指代，是部分子机制；ER中识别“雕像不是活物”属于正常视觉场景识别，不应全部并列为修辞/隐晦。

## 08 公开代码静态复现审计
- 主代码目录：`experiments/main.py`、`MOSSBench/evaluation/Evaluator.py`、`MOSSBench/evaluation/evaluation_prompts.py`、`MOSSBench/utils/utils.py`。
- 作者给出open-source推理示例及旧版20模型的pipeline，默认需要模型权重；评测模块使用OpenAI付费接口，与你当前免付费API条件不符。先可直接分析预存responses或本地规则，只能做探索性筛选，不能声称重现GPT Judge。
- `Evaluator.eval()`返回(description,score,reason)三个值，`Evaluator.eval_all()`却写`score, _ = self.eval(...)`只接受两个返回值，若运行该便捷函数会解包错误；主`experiments/main.py`调用三个值，不受这条路径必然影响。eval代码仅靠正则或“0/1”关键字回退，未匹配时有变量未初始化风险；属于静态潜在Bug，未执行证明其在论文结果中出现。
- 主README强调 test-only性质，注明数据新贡献CC BY-SA4.0且**“using it as a training set is prohibited”**；不得把这300例直接作为训练集。图片还涉及各自版权来源。
- **未完成**：下载/解码全图、AMT原始票、code运行环境版本与结果复现、Hugging Face副本sha与Github一致性。

## 09 与P034/P037/P038/P039/P040/P041及MSS差异
- **MSSBench（ICLR2025 A）**：情境有安全/危险双方，重点安全响应与活动适宜性；Chat同文本换图，Embodied不总固定文本；MOSS只从**安全输入侧的误拒**评估，补充有害对照。
- **VLSBench（ACL2025 Main A）**：危险侧视觉安全信息泄漏与安全响应指标；MOSS侧重正常输入误拒及视觉诱因；两者合起来才更接近安全-帮助权衡。
- **VLSU（ICLR2026 A）**：image/text/joint三级Safe-Borderline-Unsafe标签和联合理解；MOSS并无这样的风险理解GT。
- **CrossGuard（ACL2026 Main A）**：输入侧Safe/Unsafe guard +隐含攻击生成，目标多为漏检，和本篇输出侧误拒不同。
- **ThinkingGuard（ACMMM2026 A）**：反事实风险归因 +训练机制；MOSS三阶段oracle只是诊断而非新训练方法。
- **Meerkat-VL（ICML2026 A）**：安全回应自验证/训练，与MOSS不等价。
- **SIUO（NAACL2025 Findings 非主会CCF-A）**：表面安全组合产生危险响应风险；MOSS是**组合依然安全但被错判危险**，应作对照，而非把安全主集误标“联合隐含危险”。

## 10 综述价值与最低成本后续
- 建议在多模态安全章节单列**False Positive / Oversensitivity / Over-Refusal**，避免与Risk False Negative混写；三种视觉诱因可作为案例与任务细分，不宜上升为广义隐晦语义完整taxonomy。
- 统一能力矩阵：主数据安全误拒ARR（低好），有害对照召回/拒答（高好），独立输入安全识别Acc/F1（需要额外GT），回答安全性/有帮助性（原论文缺统一完整评估）。
- 优先K0：用本次静态审计产物生成同图/同文的PID列表，人工抽查图文安全真值及9%争议，确保所有指标按300 vs244与子类型分组；不把原有数据改标后当官方GT。
- K1：冻结小型开源VLM，评估text-only vs joint，在安全主集报告refusal行为、在危险contrast报告漏拒并用小规模人工评审核对；不付费API需明确和原论文评价不等价。
- K2：仅研究已识别的误拒机制（视觉否定、语用指代、风险似是而非），需要先排除VLSBench/VLSU/更近方法竞争工作，不能把“减少过度拒答”本身当顶会新发现。

**归档状态**：B4a第二篇经用户确认定稿，单文件独立PR合并；未修改其它窗口文件。
