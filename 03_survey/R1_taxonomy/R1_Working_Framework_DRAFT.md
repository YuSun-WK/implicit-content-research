# R1-A/B/C｜广义隐晦信息研究概念与任务工作框架
更新：2026-11-08。状态：**WORKING DRAFT；用于组内中文综述，不声称本体分类已获全领域共识**。

## R1-A：定义与边界
本文工作性界定：广义隐晦信息指语言或多模态交际中，目标意义、立场或意图无法仅由直接字面表达充分确定，需借助语境、语用推理、修辞映射、共享约定、编码形式或跨模态关系进行理解的信息。这是组织综述的研究者定义，非统一现成学科术语。

- Implicit：意义属性（未直接断言/需推断）
- Subtle：表达线索或判断显著性，非隐含同义词
- Figurative：隐喻、反讽、夸张等非字面现象集合
- Coded：存在约定或转换映射的编码表达；Dog Whistle强调受众解释差异，不与所有编码语言等同
- Obfuscated：形式变换/降低可识别性；异常词形不等于已证明规避动机
- Context-dependent：语境参与解释；指称消歧本身不一定构成隐晦意义
- 隐晦性、故意隐藏、有害性三者相互独立，允许叠加。

## R1-B：任务框架
| 任务 | 输入及输出焦点 | 必须分开的能力 |
|---|---|---|
| T1 表达识别 | 判断某种隐晦现象、片段或策略是否出现 | 识别≠解释 |
| T2 意义理解 | 候选意义、释义、跨模态蕴含/解释 | 解释质量≠内部忠实性 |
| T3 语用意图推断 | 言语行为、立场、会话含义和交际目的 | 标注者推断≠可观测内心意图 |
| T4 有害内容检测 | 危害类别、目标、严重程度 | 有害≠隐晦；情绪≠仇恨 |
| T5 联合模态隐含风险识别 | 特别要求图文等联合依赖的风险与归因 | 图文输入≠联合依赖；实质上T4特殊场景 |
| T6 安全响应 | 面对风险的拒绝/帮助/安全行为 | 拒答率≠风险理解准确率 |

论文统一记录 Task=(X,Y,G,E)：输入X、目标输出Y、Ground Truth与标注协议G、评价E。它只是综述分析记号，不是新模型。

## R1-C：59篇映射与分类
详见 [R1C_Task_Mapping_DRAFT.md](R1C_Task_Mapping_DRAFT.md)。
单标签盘点：T1 8 / T2 4 / T3 0 / T4 27 / T5 3 / T6 2；其余X1综述10 / X2表示1 / X3攻击与生成2 / X4数据评测2。共59篇。该分布只反映现有馆藏，不代表全领域。

## 为正式综述推荐的多轴组织
- A 表达机制：语用含意、修辞映射、编码/谐音/狗哨、文化语境、跨模态组合。
- B 预测任务：T1/T2/T3 → T4（其中T5专门讨论）→ T6关联拓展。
- C 模态及依赖条件：文本、图文、视频/音频、对话/时序语境；单模态充分还是确需联合。
- D 研究技术：统计/规则、传统监督与PLM、LLM/VLM提示与微调、检索、对比/因果表征、推理与对齐。
- E 证据与评价：标签定义、解释忠实性、数据捷径、跨域、反事实与安全/帮助权衡。

综述章节**不能直接将以上五维混作同级标题**。核心主体优先T1–T5的语义与检测任务，T6安全响应限定为相邻研究及任务衔接。

## 已知开放事项及下一步
1. P016/P018/P025/T012已用官方论文页补充任务核验，R0对应旧范围标注应在日后统一版本审计时修正。
2. T3独立代表论文不足，R2按语用数据与任务补充2024–2026正式文献。
3. Coded、Dog Whistle、中文动态编码、多模态组合依赖及视频隐含风险需要补充。
4. 普通有害Meme和一般毒性文献不能自动标为“隐晦研究”核心证据。
5. 未关闭的出版、数据、实现与复现疑点保留；勿把已阅读卡片当作复现通过。

## 核心来源
- [P011 Pragmatics Survey](https://aclanthology.org/2025.acl-long.425/)；ACL 2025 Main，CCF-A
- [P020 (RSA)²](https://aclanthology.org/2025.acl-long.1019/)；ACL 2025 Main，CCF-A
- [P023 CodedLang](https://aclanthology.org/2026.acl-long.426/)；ACL 2026 Main，CCF-A
- [P019 V-FLUTE](https://aclanthology.org/2025.naacl-long.1/)；NAACL 2025 Main，CCF-B
- [P016 Easy as PIE?](https://aclanthology.org/2025.emnlp-main.1213/)；EMNLP 2025 Main，CCF-B
- [P018 Comparative Study of Multilingual Idioms and Similes](https://aclanthology.org/2025.coling-main.580/)；COLING 2025 Main，CCF-B
- [P025 HVGuard](https://aclanthology.org/2025.emnlp-main.456/)；EMNLP 2025 Main，CCF-B
- [T012 JointEDI](https://aclanthology.org/2024.findings-acl.403/)；ACL 2024 Findings（非ACL主会）
