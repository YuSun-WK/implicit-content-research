# 表6｜多模态风险：输入真值、显式预测、响应行为与指标分母

| 论文 | G_in：输入风险GT、标注/版本 | P_in：显式分类 | R_beh / Q_out：回应评价 | 分母、Judge与不得混同之处 |
|---|---|---|---|---|
| Hateful Memes [@kiela2020hateful] | 图文仇恨二分类；非天然三条件标签 | 研究重点为分类 | 无强制回应任务 | 不能将所有图文难例当S-S-U |
| VLSBench [@hu-etal-2025-vlsbench] | VSIL视觉信息泄漏：比较风险Judge看图文与仅文本；样本偏风险侧 | 非统一三条件GT分类 | Safe Rate=Refusal+Warning，另报Unsafe | Qwen2-VL-7B特定200例：text 29.5%、text+图像描述22.5%、图文16.0%，是**回应比例**而非输入分类准确 |
| MMSafeAware [@wang-etal-2025-cant] | 作者论文Unsafe1000/Over-Safe500，三向人审筛选；发布版文件／图像差异本轮未固定，只记O并撤去精细计数 | 联合Safe/Unsafe二分类 | 非主要生成回应 | 类比2:1，恒判Unsafe总Acc=66.67%；需报Unsafe召回+Safe召回；未固定发布版不用于断言正式样本或图像数量 |
| VLSU [@palaskar2026vlsu] | 人审图/文/联合三条件Safe/Borderline/Unsafe；正式PDF**8187**、公开CSV**8159**；严格S-S-U PDF**37**、CSV**35** | 三级风险；Table1兼容他基准的二分类把Borderline当Safe | Harmless/Helpful行为prompt下拒答与帮助性另测 | 正式PDF第8页Figure5图内标题为**Qwen2.5-VL-32B**，33.8%：分母为该模型**joint三分类已错集合**，其中I/T均正确；非17模型汇总，扩展模型见正式PDF第38页E.3及第39页Figure18；本轮已直接核图内模型名、图注和分母；公开image_grade含141个not_sure；图像单条件作者单人评、文本/联合多评审；论文PDF17模型/摘要11 |
| MSSBench [@zhou2025situational] | 论文1960视觉情境请求；Chat/Embodied控制程度不同 | 有部分显式安全诊断 | IF Judge评情境行动/回答 | Oracle环境事实应与原图输入分开 |
| MOSSBench [@li2025oversensitive] | 300作者目标安全图文请求，约9%人审对能否安全作答有争议；contrast逐ID映射／发布版数量未固定，不保留精确数 | 不提供统一三等级输入分类 | 安全主集上ARR=拒答比例；危险对照可另测拒答 | 安全误拒不是输入分类FPR；不是全300严格单因素配对；发布版证据为S/O |
| **SIUO** [@wang-etal-2025-safe] | 图文表面安全但可能引出危险回复；不提供VLSU式三条件风险人审GT | 非主要的独立输入分类任务 | 输出Safe Rate/攻击成功率；包含参考安全警示与Judge | NAACL2025 **Findings**（举办会议CCF-B，**非主会**）；须注明人工与AI辅助构造子集及judge参考信息 |
| CrossGuard [@zhang-etal-2026-crossguard] | 1616 Guard混合训练，joint类占约12.5%≈202；ImpForge另有**1390红队样本**，尚未核逐例映射 | LoRA/SFT训练输入Safe/Unsafe Guard | 红队攻击ASR↑、Guard漏检ASR↓与生成模型危险回应ASR↓各异 | Fig4 SIUO 60.33→5.39%，FigStep0.12→0.21%；不同在线模板、离线GPT judge、Guard标签输出的定义**不可直接当同一ASR** |
| ThinkingGuard [@zhang2026thinkingguard] | 作者称TriggerBench 2800 Safe +2800 Unsafe成对；图片分别生成，严格只动Trigger未逐对证实 | 风险标签/类别+逐步分析 | 离线SA-MCTS与DPO轨迹训练，非直接安全回复 | 作者接收ACM MM2026（会议CCF-A），最终出版社实际Track仍O；Step-DPO同预算独立性未证 |
| Meerkat-VL [@zhou2026meerkatvl] | 带风险说明等的隐含风险训练材料（非无争议三条件输入金标） | 有风险感知监督，不是独立部署分类器的统一评测 | 安全/帮助性生成，自Actor自评奖励+GRPO | 训练评分读规范risk文本但不重新读原图；不等于独立视觉验证，模型Judge与帮助性需分列 |

**表注。** `G_in`=政策/人审输入真值，`P_in`=显式输入判断，`R_beh`=拒答/警示/执行，`Q_out`=安全与合法帮助质量；**同名ASR可能是攻击得逞、Guard漏检或生成危险回复，必须给主体+Judge+分母**。VLSU 33.8%只指Figure5示例模型的joint分类错误子集，严格S-S-U并非整个联合风险升高类。图片重复、发布数据文件差异、代码脚本观察需保留版本限制。


**版本定位。** VLSU公开CSV固定commit `b7c1780d2d578a82fc5f11a070d93bcd50cb9e45`／blob `09421adeb2e68eac1d5e829dcbd48848f21a0be6`，本轮重读重计8159/35/141，公开链接与计数方法见正文附录A；Figure5与Figure18本轮已直接核[ICLR2026正式PDF](https://proceedings.iclr.cc/paper_files/paper/2026/file/a36e092659c42b2c92b8b0eb2394bf74-Paper-Conference.pdf)，分别位于第8／39页；44页文件SHA-256为`b38dc2e84d20899132125338b3ef8d31f54873660c2562c281c4d992c1f96aa8`。这只补齐正式图表核验，不表示重算原模型预测。
