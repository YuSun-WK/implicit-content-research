# 表6｜多模态风险：输入真值、显式预测、响应行为与指标分母

| 论文 | G_in：输入风险GT、标注/版本 | P_in：显式分类 | R_beh / Q_out：回应评价 | 分母、Judge与不得混同之处 |
|---|---|---|---|---|
| Hateful Memes [@kiela2020hateful] | 图文仇恨二分类；非天然三条件标签 | 研究重点为分类 | 无强制回应任务 | 不能将所有图文难例当S-S-U |
| VLSBench [@hu-etal-2025-vlsbench] | VSIL视觉信息泄漏：比较风险Judge看图文与仅文本；样本偏风险侧 | 非统一三条件GT分类 | Safe Rate=Refusal+Warning，另报Unsafe | Qwen2-VL-7B特定200例：text 29.5%、text+图像描述22.5%、图文16.0%，是**回应比例**而非输入分类准确 |
| MMSafeAware [@wang-etal-2025-cant] | 作者论文Unsafe1000/Over-Safe500，三向人审筛选；公开发布文件版本/重复图像尚待固定 | 联合Safe/Unsafe二分类 | 非主要生成回应 | 类比2:1，恒判Unsafe总Acc=66.67%；需报Unsafe召回+Safe召回；所审仓库编号与配图缺口属于特定静态版本S/O |
| VLSU [@palaskar2026vlsu] | 人审图/文/联合三条件Safe/Borderline/Unsafe；正式PDF**8187**、公开CSV**8159**；严格S-S-U PDF**37**、CSV**35** | 三级风险；Table1兼容他基准的二分类把Borderline当Safe | Harmless/Helpful行为prompt下拒答与帮助性另测 | Figure5约34%是**joint预测已错**的条件子集、非总库或S-S-U；公开image_grade含141个not_sure；图像单条件作者单人评、文本/联合多评审；论文PDF17模型/摘要11 |
| MSSBench [@zhou2025situational] | 论文1960视觉情境请求；Chat/Embodied控制程度不同 | 有部分显式安全诊断 | IF Judge评情境行动/回答 | Oracle环境事实应与原图输入分开 |
| MOSSBench [@li2025oversensitive] | 300作者目标安全图文请求，约9%人审对能否安全作答有争议；所查contrast **244**有映射 | 不提供统一三等级输入分类 | 安全主集上ARR=拒答比例；危险对照可另测拒答 | 安全误拒不是输入分类FPR；不是全300严格单因素配对；发布版证据为S/O |
| **SIUO** [@wang-etal-2025-safe] | 图文表面安全但可能引出危险回复；不提供VLSU式三条件风险人审GT | 非主要的独立输入分类任务 | 输出Safe Rate/攻击成功率；包含参考安全警示与Judge | NAACL2025 **Findings**（举办会议CCF-B，**非主会**）；须注明人工与AI辅助构造子集及judge参考信息 |
| CrossGuard [@zhang-etal-2026-crossguard] | 1616 Guard混合训练，joint类占约12.5%≈202；ImpForge另有**1390红队样本**，尚未核逐例映射 | LoRA/SFT训练输入Safe/Unsafe Guard | 红队攻击ASR↑、Guard漏检ASR↓与生成模型危险回应ASR↓各异 | Fig4 SIUO 60.33→5.39%，FigStep0.12→0.21%；不同在线模板、离线GPT judge、Guard标签输出的定义**不可直接当同一ASR** |
| ThinkingGuard [@zhang2026thinkingguard] | 作者称TriggerBench 2800 Safe +2800 Unsafe成对；图片分别生成，严格只动Trigger未逐对证实 | 风险标签/类别+逐步分析 | 离线SA-MCTS与DPO轨迹训练，非直接安全回复 | 作者接收ACM MM2026（会议CCF-A），最终出版社实际Track仍O；Step-DPO同预算独立性未证 |
| Meerkat-VL [@zhou2026meerkatvl] | 带风险说明等的隐含风险训练材料（非无争议三条件输入金标） | 有风险感知监督，不是独立部署分类器的统一评测 | 安全/帮助性生成，自Actor自评奖励+GRPO | 训练评分读规范risk文本但不重新读原图；不等于独立视觉验证，模型Judge与帮助性需分列 |

**表注。** `G_in`=政策/人审输入真值，`P_in`=显式输入判断，`R_beh`=拒答/警示/执行，`Q_out`=安全与合法帮助质量；**同名ASR可能是攻击得逞、Guard漏检或生成危险回复，必须给主体+Judge+分母**。VLSU 34%只针对joint分类错误子集，严格S-S-U并非整个联合风险升高类。图片重复、发布数据文件差异、代码脚本观察需保留版本限制。
