# P038｜VLSU: Mapping the Limits of Joint Multimodal Understanding for AI Safety

> **2026-11-02 用户授权正式定稿并合并**。研究依据：ICLR 2026正式论文、Apple官方GitHub仓库与发布CSV直接字段/逐行静态审计。**未本地运行模型、未逐一下载网页图片、未复现作者全部17模型与GPT-4o Judge**。必须区分正式论文统计与发布文件的统计，不得覆盖彼此。

## 01. 书目信息与材料
- Shruti Palaskar, Leon Gatys, Mona Abdelrahman 等；**ICLR 2026 正式会议（CCF-A）**；正式PDF https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf ；预印本 https://arxiv.org/abs/2510.18214 。
- 官方仓库 https://github.com/apple-aiml-research/ml-vlsu ，发布CSV https://github.com/apple-aiml-research/ml-vlsu/blob/main/data/VLSU.csv ，下载脚本 utils/save_dataset_images.py。
- 公开CSV的原始Git Blob SHA **09421adeb2e68eac1d5e829dcbd48848f21a0be6**；首次发布提交2025-11-18 b7c1780d2d578a82fc5f11a070d93bcd50cb9e45。下述CSV统计来自直接读取该Blob全文逐行解析；并非直接使用README报告数字。

## 02. 核心研究问题与任务
- 比较 image-only、text-only、image-text joint 的安全等级判断，解释为什么单模态单独正确时联合判断仍错误。
- 每条(I,T)有三个级别标签 y_I, y_T, y_J，取自 **Safe / Borderline / Unsafe**。Borderline是规范意义上的敏感边界，不是“模型不确定”的同义词。
- **任务A Safety Understanding**：模型输出标签；核心是联合风险分类，可用Accuracy、F1。
- **任务B Safety Alignment**：模型自由生成响应，以是否拒绝、有用性评估响应策略；**拒绝率≠联合风险分类准确率**。用于区分安全与帮助之间的行为权衡。
- 相比P041 SIUO与P037 VLSBench（偏安全响应）：VLSU提供较系统的人工监督输入风险标签，更适合做冻结分类评测；并不意味着每个风险判断是独立无争议的法律事实。

## 03. 三层标签与17种组合
- 理论3³=27种；论文最终报告17种实际模式，包含S-S-S、S-U-U、U-S-B、S-S-B、S-S-U等，不是所有模式同样普遍。
- 在论文Figure9：S-S-U仅**37条**，关键“分别安全，联合变得不安全”的子集太小，不能独立支撑强统计泛化。
- 公开CSV的图像标签有额外 **not_sure**（141条），实际三元组**25种**，包括论文未列的B-S-S 1条、S-U-B 1条；论文17模式与当前公开版本并非逐项一致。
- 从公开CSV中定义严格的“联合风险升级”（以S=0,B=1,U=2，且无not_sure）为 y_J > max(y_I,y_T)：S-S-B58、S-S-U35、B-S-U45、S-B-U9、B-B-U32，合计**179**。它们是不同机制，不能把179都当作S-S-U。
- 可报告联合错误时 Both Correct 子集：在模型image-only和text-only都预测正确条件下，joint仍预测错误；是模型输出层条件错误，不是对内部推理的因果保证。

## 04. 数据构建与人工标注
- 论文规模 **8,187**图文配对、15个安全类别、17模式；联合风险原文统计Safe2186/Borderline3312/Unsafe2689；正式版评估**17个模型**（旧arXiv写11个，不能混用）。
- 构造：以安全分类为依据生成检索概念→搜集真实图片→Gemini/DSPy约束生成配套文字→专业人工标注image-only/text-only/joint的严重程度（生成时目标等级不直接当最终人工金标）。
- 论文报告225名有相关经验标注人员参与；image-only由一名经验作者负责；text-only/joint多数由三名专业标注员、部分两名；170金标用于校准；92.4%样本有3人标注，约7.6%两人。
- 论文整体Krippendorff α=0.806、raw agreement=86.9%；但组合级原始一致率从S-S-S93.7%到B-B-U54.1%，关键S-S-U82.5%（126次配对比较不是126条样本）。人际一致性不等于客观唯一真值；image-only单人标注的独立一致性缺失。

## 05. **重要：直接核验公开CSV与论文不同**
- GitHub发布CSV全文可读共**8159条完整9字段记录**（不是8187）；独立按行与9字段校验：不是简单CSV解析错误。
- 全部公开记录联合标签分布：Safe **2189**、Borderline **3310**、Unsafe **2660**；对比正式论文2186/3312/2689。
- image_grade分布safe4182/borderline1810/unsafe2026/**not_sure141**；text-grade safe4328/borderline1452/unsafe2379；joint-grade三类均无not_sure。
- 公开CSV S-S-U **35**而论文Figure9为37；image_grade明确的样本共**8018**，处理三层标签/模式时宜明确剔除not_sure规则，不必在只预测joint时必然丢掉141条。
- 公开CSV唯一UUID 8159、唯一图片URL **8157**、唯一prompt **7638**；HTTP875/HTTPS7284；URL跨约2944域名，若大量来源失效或版权限制，需要按图片下载成功子集重算分布/任务表现；**本轮未实际逐一HTTP下载图片，不宣称可达率**。
- 公开CSV非空combined_category**5948**，空**2211**（其中joint Safe2149/Borderline36/Unsafe26），论文附录Table6的6113属类别统计而非全体样本，但与当前5948仍不一致，不可当作全面清零。
- 论文数据有且仅有**Test Split**（附录F.2）；不能在同一公开测试集微调然后当官方测试结果发表。若训练应另用公开训练基准，VLSU做外部验证；调整split要标明新协议。
- 许可证：公开数据CC-BY-NC-ND；另有图片自身版权/可用性。仅内部研究使用与修改发布受不同限制，须遵守。

## 06. 分类实验与关键结果
- Table1为了横向比较既有基准，**专门使用二分类提示词**，将Gold Borderline→Safe，模型也直接预测Safe/Unsafe；非把三分类结果随意合并。与Table2/4/5等三分类F1不能直接同比。
- 附录D.1二分类提示核心意译：“若用户内容unsafe/harmful/malicious输出Unsafe，否则Safe；只能输出一个标签”。图文结合共同输入。
- 正式论文Figure5 Qwen2.5-VL-32B“Both Correct”**33.8%（简称34%）的分母是全部joint预测错误样本**，而非全体8187/8159，更非S-S-U 35/37条；包括U-S-B等降低/改变风险的类型。四类占比：Image Wrong32.3%、Text Wrong25.9%、Both Wrong7.9%、Both Correct33.8%（加总有四舍五入误差）。
- Table2 Structured CoT为推理时提示词（非训练）：例GPT-4o F1 45.8→54.4、Qwen2.5-VL-7B42.3→51.4；部分模型变差，如Qwen2.5-VL-32B63.5→62.7，不能声称CoT普遍有效或解释忠实。
- 模态分别正确不等于已证明模型内部所有视觉/文本语义表示都充分，不能在CJF指标上跨分母误比论文33.8%。

## 07. Harmless vs Helpful提示词及评审
- 论文§4.4采用**两种推理时行为指令**控制同一模型生成响应（Gemini-1.5、Qwen2.5-VL-32B），并非SFT/PPO/DPO或更改模型参数。
- Harmless指令参考MM-SafetyBench、Helpful指令参考Greenblatt et al.；**正式论文和公开仓库未充分给出这两种“被测模型行为指令”的逐字原文**。附录D.2中名为Helpfulness Prompt的是给GPT-4o Judge评价有用性的，不是Table3的Helpful行为指令。缺少原样提示词是可复现性疑点，禁止把示意prompt冒充原文。
- Refusal Judge把响应判为refusal 0/1；Helpfulness Judge评定有用性，使用GPT-4o评审，不能当输入安全金标。
- 论文Table3 Gemini-1.5 Harmless→Helpful时：Safe拒答34.7%→4.6%；Borderline62.4%→10.4%；Unsafe90.8%→53.9%。帮助性增加可能降低过度拒答，却也增加有害内容漏拒；Qwen2.5-VL-32B行为方向不完全一致，不应过度普遍化。

## 08. 公开代码可达性
- GitHub README、data/VLSU.csv、utils/save_dataset_images.py和utils/README均已检查；图片在web_path远程URL而不是本地完整图片压缩包。
- 提供下载工具，支持从URL下载、Pillow验证、WebP转PNG、部分失败标记“manually retry download”。脚本底部path_to_data、local_image_save_path、updated_data_path为空，需要人工设置；下载失败有retry但没有保证成功。
- 目前未发现17模型全部统一评测与原全部生成流水线的完整代码；相关复现实验需自行实现统一prompt/输出解析并记录版本。无付费API最小方案：CPU统计+本地小规模冻结Qwen2.5-VL-3B/量化7B分类测试，先测显存速度和图片可达率。

## 09. 方法型论文可行性与Kill Test
- VLSU作为**独立多模态风险三分类评测**有条件GO；作为主训练集NO-GO（官方只有test split）。
- 作为仅S-S-U核心方法论文主评测NO-GO（公开35/论文37条，统计置信区间宽）；179条联合升级子集可探索性试验，但必须逐组报告并保留原始UUID。
- 具体最低成本：先下载/解码并记录每组合实际可用率及失败集中度、处理not_sure；再冻结3B/7B单卡模型分别输入image-only、text-only、joint，计算分类Acc/Macro-F1/组别结果、BothCorrect条件错误率，**不得混同论文33.8%的分母**；保留失败案例并抽查标签冲突；只做小规模200–300条试测，实际性能/显存/6h可行性须测量。
- 此时不承诺已证实顶会创新Gap；需P039 ThinkingGuard、P040 Meerkat-VL方法竞争审计后再设最多2个可证伪假设。

## 10. 本轮尚未闭合事项
1. CSV为何比正式论文少28条且联合三类统计变化；目前commit历史只确认初次发布2025-11-18，未找到删样本原因；需作者或官方协议说明。
2. 公开8159条实际图片下载/可解码比例、按模式缺失分布、图片内容与原任务匹配/版权均未实物核验。
3. 论文的17组合/附录Table6统计与公开CSV少量差异、image_grade not_sure映射规则未从官方找到完整说明；不能把发布文件当论文官方精确复现列表。
4. Harmless/Helpful行为指令逐字原文未公开；未核对所有旧版vs新版prompt/实验运行环境。

## 11. 定稿
- 2026-11-02 用户明确授权正式定稿合并main；**仅原文/公开CSV/脚本静态审计，不代表运行复现**。
- 当前多模态阅读顺序：已完成P041 SIUO→P037 VLSBench→P038 VLSU；下一篇 **P039 ThinkingGuard（ACM MM 2026 CCF-A）**，重点审核TriggerBench反事实构建、结构化推理监督、偏好对齐和代码/指标/训练成本。
