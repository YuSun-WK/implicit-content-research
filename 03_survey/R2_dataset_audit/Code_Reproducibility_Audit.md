# Code Reproducibility Audit｜代码与权重可达性

审计日期：2026-11-08。CCF等级按[第七版目录](https://www.ccf.org.cn/Academic_Evaluation/By_category/2026-03-31/870181.shtml)；刊会等级与论文Track分别记录。只审计指定资源的公开可达性和标签协议，不判断方法创新性。

## 验证层级

- **A 实读**：本轮通过官方GitHub连接器取得文本文件内容并解析。
- **B 页面/树**：核对官方仓库文件树、README或Hugging Face数据卡/viewer；不等于取得全部字节。
- **D 既有卡**：引用既有精读卡的直接文件审计，本轮未重复下载。
- **未运行**：12项均未进行训练或端到端基准复现；权重“未见”仅指所查官方入口。

## 逐项审计

### DRInQ（R2A-001）

- 正式论文：[ACL 2026 Main，CCF A](https://aclanthology.org/2026.acl-long.1597/)。
- 数据：[官方入口](https://github.com/hjarai/drinq/blob/main/drinq_validated.csv)。论文口径：819人工共识；400困难集；当前公开观察：CSV实读231行、148个不同问句；104,149字节仓库文件。
- 文件与标签：drinq_validated.csv；5列。5选1隐含解释 A–E；23意图动词用于构建。GT：每条5人判断，至少4/5一致；consensus为评测GT，implied_comment是生成目标。
- 划分与泄漏：公开CSV未见官方train/valid/test；论文困难集未完整发布。同一问句跨语境；必须按问句分组且防选项顺序/生成模板捷径。
- 代码：[入口](https://github.com/hjarai/drinq)；仅CSV、演示和海报，未见完整评测脚本。权重：未见。
- 额外资源：构造用GPT-4o；完整生成需商业API/人工标注。验证：A：GitHub CSV内容实读并解析231条；代码树静态核查；未运行。
- 待核：论文819/400与公开231无映射或完整困难集。

### VAGUE（R2A-002）

- 正式论文：[ICCV 2025 Main，CCF A](https://openaccess.thecvf.com/content/ICCV2025/html/Nam_VAGUE_Visual_Contexts_Clarify_Ambiguous_Expressions_ICCV_2025_paper.html)。
- 数据：[官方入口](https://huggingface.co/datasets/HazelNam/vague-bench)。论文口径：1,677（VAGUE 2.0）；当前公开观察：HF viewer约1.68k行，作者README称1,677；未逐行下载。
- 文件与标签：HF parquet图像+字段；另有Google Drive入口。direct/indirect/solution；四选一意图及干扰项；rating。GT：生成目标行动经人工合理性筛选；不是现实说话者可观测意图。
- 划分与泄漏：HF当前仅train单split；未见官方train/valid/test三分。solution、direct、caption、fake_caption保留在样本内；需保证评测prompt隔离；VCR/Ego4D源图近重复。
- 代码：[入口](https://github.com/Hazel-Heejeong-Nam/VAGUE)；benchmark与inference脚本。权重：未见专用权重。
- 额外资源：VCR/Ego4D原始素材权限与来源许可；GPT/Gemini基线需API。验证：B：HF数据页及GitHub树/README；未下载parquet或图片。
- 待核：核对图像可用率、字段泄漏与按原图分组划分。

### CodedLang（P023）

- 正式论文：[ACL 2026 Main，CCF A](https://aclanthology.org/2026.acl-long.426/)。
- 数据：[官方入口](https://github.com/Crowd-AI-Lab/CodedLang/tree/main/Data)。论文口径：7,744评论；900编码正例；当前公开观察：Data/CodedLang.csv存在，仓库标称8,453,026字节；本轮接口未返回大文件内容，实数未重新计。
- 文件与标签：CodedLang.csv、Code_Dictionary.csv、种子样例；HF镜像RuyuanWan/CodedLang。编码二元；7类策略多标签；片段、解码、星级。GT：两位标注员协商；词典辅助采样；原评论星级为平台原始字段。
- 划分与泄漏：未见官方train/valid/test独立文件。词典/同编码片段、同商家或评论模板跨随机划分；decode_review和翻译字段可泄露答案。
- 代码：[入口](https://github.com/Crowd-AI-Lab/CodedLang)；Code/Prompts.txt；Code/README.md近空，未见完整运行程序。权重：未见。
- 额外资源：闭源GPT/Gemini/DeepSeek基线需相应API；原Google评论源依赖。验证：B：仓库文件树与README；引用既有P023精读卡；大CSV未实读。
- 待核：明确可执行评测脚本、split及词项级交叉；核对发布CSV行数。

### Silent Signals（R2A-006）

- 正式论文：[ACL 2024 Main，CCF A](https://aclanthology.org/2024.acl-long.675/)。
- 数据：[官方入口](https://huggingface.co/datasets/SALT-NLP/silent_signals)。论文口径：主集16,550；检测100；消歧124；当前公开观察：主集README split元数据16,258；检测viewer 101；消歧viewer 124（既有卡页面核验）。
- 文件与标签：HF三个独立数据集；主集parquet。已知狗哨词在语境中的编码义/普通义；检测与释义。GT：词典定义+GPT-4筛出主集高置信正例；小评测集双人一致；主集非全量人工二分类。
- 划分与泄漏：各数据集页面主要为train单split；无统一官方train/valid/test。同根词/词形及社区与时期重叠；词典定义直接进入任务；主集标签非平衡负例。
- 代码：入口；。权重：未见。
- 额外资源：原始大集构建调用GPT-4；Reddit/API和历史语料许可。验证：B：HF卡/README及既有精读卡；未下载parquet。
- 待核：16,550→16,258差292；检测100→101；消歧标签值与论文二元口径需核。

### FETCH!（R2A-007）

- 正式论文：[ACL 2025 Main，CCF A](https://aclanthology.org/2025.acl-long.284/)。
- 数据：[官方入口](https://github.com/KuleenS/FETCH-Dog-Whistle)。论文口径：三场景：约16k、Gab和700万Twitter帖（论文设置）；当前公开观察：仓库有重建脚本；未见三场景完整原始帖/索引打包；无可核实际总行数。
- 文件与标签：源码/环境文件；输入需外置CSV/parquet/Gab-Twitter文件和词典。词典根词发现；20% seed/80% held-out词项。GT：词典/正则匹配而非逐帖人类编码义判定；Silent Signals正例为LLM筛选。
- 划分与泄漏：split_train_test.py生成词项分割；未发布固定完整三场景split。同根词变体、词典外新义、时间/社群重叠；词典匹配假阴性。
- 代码：[入口](https://github.com/KuleenS/FETCH-Dog-Whistle)；源码和环境公开。权重：未见官方训练权重或向量索引。
- 额外资源：Gab/Twitter历史文本、约700万帖索引计算；商业API分支可选，离线分支需大模型。验证：B：GitHub代码树；既有卡逐文件静态审计；未跑全量。
- 待核：原始语料不可确认一键获取；静态审计记录DIRECT/recall等潜在运行问题。

### SeTox（R2A-010）

- 正式论文：[ACL 2026 Main，CCF A](https://aclanthology.org/2026.acl-long.1602/)。
- 数据：[官方入口](https://github.com/thu-coai/Setox/tree/main/data)。论文口径：词典974；训练995+600；测试624+368；当前公开观察：实读JSON：词典974、普通训练600、新词测试624、普通测试368；train_tool大文件未返回，995据作者data/README。
- 文件与标签：5个JSON、schema、checksums；HF thu-coai/SeTox。safe/unsafe；细类spec_label；词典5风险类别；human_revised。GT：词典共识与人工修订评测标签；解释/检索结果不是独立真值。
- 划分与泄漏：官方训练与测试文件；未见validation文件。训练/测试同词、词典曝光、搜索结果包含答案、在线搜索时间漂移均待核。
- 代码：[入口](https://github.com/thu-coai/Setox)；训练/推理/评测及校验脚本。权重：https://huggingface.co/thu-coai/SeTox-Qwen2.5-3B；7B同组织已列。
- 额外资源：实时检索需Serper API key；static/mock/none替代；基础Qwen许可分别核查。验证：A：4个JSON内容实读计数；B：train_tool树/作者README；未跑模型。
- 待核：核对词项交集；作者README BibTeX与ACL正式标题、作者、页码冲突；训练搜索噪声。

### M3UCD（R2A-017）

- 正式论文：[AAAI 2026 Technical Track，CCF A](https://ojs.aaai.org/index.php/AAAI/article/view/40808)。
- 数据：[官方入口](https://github.com/DragonReed/M3UCD)。论文口径：15,345；每条12属性标签；当前公开观察：所引GitHub树仅海报/补充材料/幻觉索引PDF；未见数据文件；公开行数不可核。
- 文件与标签：未找到可下载数据表/图像包。隐喻有无/类别、源目标域与模态、情绪、冒犯、意图等12属性。GT：论文称多人协作人工标注；本轮无样本级文件复核。
- 划分与泄漏：未见公开官方split文件。若复用MET-MEME等源，需按源图/文本模板/域分组；当前无法实测。
- 代码：入口；。权重：未见。
- 额外资源：申请/开放计划未明确；需联系作者取得真实发布链接。验证：B：论文官方页+作者GitHub整树清单；没有数据可下载。
- 待核：论文规模不得写为“公开15,345”；发布链接与标签字典缺失。

### MET-MEME（R2A-018所用数据）

- 正式论文：[SIGIR 2022原数据；AAAI 2025 Technical Track复用，CCF A / A（刊会级）](https://ojs.aaai.org/index.php/AAAI/article/view/34801)。
- 数据：[官方入口](https://www.kaggle.com/datasets/liaolianfoka/met-meme)。论文口径：原作者README 10,039图文对（中文6,045、英文3,994）；AAAI论文复用；当前公开观察：原GitHub只有README与小型code.rar，图像指向Kaggle；未下载Kaggle包；第三方HF 10,030不可当官方数。
- 文件与标签：原README称Cimages.rar、Eimages.rar在Kaggle；仓库无图像压缩包。隐喻有无/类型/源目标域与模态；7情绪、5意图、4冒犯程度。GT：原数据人工标注；AAAI 2025不新建该GT。
- 划分与泄漏：本轮未核官方固定train/valid/test；第三方拆分不可冒充官方。同meme模板/图像和双语变体跨split；原样本与M3UCD复用造成跨基准重叠。
- 代码：入口；未找到MGMCF作者官方实现。权重：未见MGMCF官方权重。
- 额外资源：Kaggle账号/下载条款及预训练BERT/VGG/ResNet自行准备。验证：B：原作者GitHub树/README、Kaggle入口、AAAI官方页；未下载压缩包。
- 待核：原始10,039与第三方HF 10,030相差9；确认Kaggle实物及官方split。

### VLSU（P038）

- 正式论文：[ICLR 2026 Main，CCF A](https://proceedings.iclr.cc/paper_files/paper/2026/hash/a36e092659c42b2c92b8b0eb2394bf74-Abstract-Conference.html)。
- 数据：[官方入口](https://github.com/apple-aiml-research/ml-vlsu/blob/main/data/VLSU.csv)。论文口径：8,187；17组合；当前公开观察：既有P038卡直接CSV审计8,159条完整9列；本轮确认文件存在（2,215,163字节），未重新取回大CSV。
- 文件与标签：data/VLSU.csv，图像为web_path外链；下载脚本。image/text/joint各Safe、Borderline、Unsafe；公开image_grade另有not_sure 141条。GT：专业人员标注；图像层单人、文本/联合多数3人；共识标签。
- 划分与泄漏：作者仅Test Split；无官方训练/验证。同图URL重复、提示重复、网页图像失效；按图/URL/域分组前不可随机训练。
- 代码：[入口](https://github.com/apple-aiml-research/ml-vlsu)；有图片下载工具，未见17模型统一评测全脚本。权重：未见专用权重。
- 额外资源：图像外链/版权及CC-BY-NC-ND；部分评测GPT-4o Judge需API。验证：D：既有卡实读8159行；本轮B级确认树和README；未下载图片。
- 待核：论文多28条；图片实际成功率未知；not_sure及类别分布不一致。

### MSSBench（R2A-027）

- 正式论文：[ICLR 2025 Main，CCF A](https://proceedings.iclr.cc/paper_files/paper/2025/hash/1cb57fcf7ff3f6d37eebae5becc9ea6d-Abstract-Conference.html)。
- 数据：[官方入口](https://huggingface.co/datasets/kzhou35/mssbench/tree/main)。论文口径：R2-A称1,960；项目页摘要称1,820（版本矛盾）；当前公开观察：HF viewer仅724张图；另有combined.json 309kB及chat/embodied文件夹；未逐条数完整问答对。
- 文件与标签：combined.json、chat/、embodied/；GitHub评测代码。安全/不安全视觉情境；Chat与Embodied任务及类别。GT：构造意图/检索图像经人工核验；安全语境判断并非图像单独危害标签。
- 划分与泄漏：HF图像viewer为train单split；未证官方train/valid/test。同一意图的安全/不安全图像配对须按意图分组；文件名/类别提示捷径。
- 代码：[入口](https://github.com/UCSB-AI/MSSBench)；推理与评测脚本。权重：未见专用权重。
- 额外资源：闭源模型评测需API；图像与combined.json的配对完整性需核。验证：B：HF文件页/viewer、作者GitHub README与树；未下载255MB图像。
- 待核：1,960/1,820/724图像口径待统一；实际可运行样本数需逐条配对核验。

### MOSSBench（R2A-028）

- 正式论文：[ICLR 2025 Main，CCF A](https://proceedings.iclr.cc/paper_files/paper/2025/hash/50d4f8ff0416cedfe0771b7ad947a197-Abstract-Conference.html)。
- 数据：[官方入口](https://github.com/turningpoint-ai/MOSSBench/tree/main/data)。论文口径：300安全图文查询；另有对照图；当前公开观察：实读information.json恰300键；树列data/images 304张编号PNG、contrast_images 244张；HF contrast viewer报metadata缺失错误。
- 文件与标签：information.json、images/、data_contrast/；HF AIcell/MOSSBench。三类触发因素：Exaggerated Risk、Negated Harm、Counterintuitive Interpretation；安全查询/拒答行为。GT：作者收集安全样本、AMT第三方复核；拒答率为模型行为，不是输入有害标签。
- 划分与泄漏：发布数据无正式train/valid/test；HF自动显示train不等于作者训练划分。同查询对照图和原图跨划分；图中文字/视觉风险提示；评估模型拒答判断需固定准则。
- 代码：[入口](https://github.com/turningpoint-ai/MOSSBench)；模型包装、评估脚本。权重：未见专用权重。
- 额外资源：GPT/Claude/Gemini等商业API可选；部分本地模型需另下载。验证：A：GitHub JSON实读300键及文件树304/244张；B：HF页面错误；未下载图片。
- 待核：304 PNG与300标注键未一一匹配；HF contrast预览坏；需确认官方对照配对。

### V-FLUTE（P019）

- 正式论文：[NAACL 2025 Main，CCF B](https://aclanthology.org/2025.naacl-long.1/)。
- 数据：[官方入口](https://huggingface.co/datasets/ColumbiaNLP/V-FLUTE)。论文口径：6,027；train 4,578 / valid 726 / test 723；当前公开观察：HF README元数据三split合计6,027；本轮仅数据卡，未下载约4.8GB实物。
- 文件与标签：HF parquet含image/claim/label/explanation/phenomenon/source_dataset；Zenodo图像另见仓库说明。Entailment/Contradiction；五种修辞；自然语言解释。GT：来源任务规则/LLM生成候选解释后专家审修；并非每条3人独立投票。
- 划分与泄漏：官方train/validation/test明确。NYCartoons全Entailment；同图多claim跨随机split、数据来源标签规则差异；F1@53阈值借测试子集校准。
- 代码：[入口](https://github.com/asaakyan/V-FLUTE)；训练转换和评测脚本。权重：https://huggingface.co/asaakyan/LLaVA-1.5-7b-eViL-VFLUTE-lora。
- 额外资源：训练报告4×A100 40GB；原图版权/Zenodo；部分基线GPT-4 Vision API。验证：B：HF README三split和GitHub树；D：既有P019卡PDF/代码静态审计；未下载图像。
- 待核：按图片ID/近重复和来源重分组审计；测试集阈值校准独立性。

## 关键复现界限

1. **公开代码≠完整复现**：FETCH! 原始社媒语料、VLSU外链图像、M3UCD缺失数据、MET-MEME的Kaggle包都需单独验收。
2. **HF自动train≠官方训练集**：VAGUE、Silent Signals、MSSBench、MOSSBench的viewer split不作为论文监督学习划分。
3. **闭源服务与算力**：DRInQ生成用GPT-4o，SeTox live search用Serper；V-FLUTE原训练使用4×A100 40GB。公开小集上的本地推理可行性不等于原实验可重跑。
4. **出版元数据冲突**：SeTox作者README BibTeX写成不同标题/作者/页码，应以[ACL正式记录](https://aclanthology.org/2026.acl-long.1602/)为准。
