# R6-Fix｜公开代码/数据静态审计证据索引（固定版本）

> **状态：2026-11-09 已定点重新读取公开GitHub固定commit及下列源码；没有运行作者论文完整实验或确认相应源码就是正式论文报告所用版本。**  
> 本索引专门响应R6-A4 **P0-02**：发表论文的正式引文（F/P）与本项目对**公开代码版本**的静态观察（S）必须分开。公开源码中的可复核片段**不是作者涉嫌不当行为的正式判决**。所有链接使用固定40位commit SHA，避免浮动main；作者论文代码版本映射仍O。

## 1. 已固定且重新核到的S级关键记录

| Claim ID | 论文 / 公开仓库固定commit | 精确源码位置与本轮直接静态读取内容（S） | 可写范围；尚缺的证据（O） |
|---|---|---|---|
| S-RV-01 | RV-HATE（ACL 2026 Main，CCF-A）；[leeyejin1231/RV-HATE@acfe053172a7266c8dde3759551882701478cdac](https://github.com/leeyejin1231/RV-HATE/tree/acfe053172a7266c8dde3759551882701478cdac) | [ppo_eval.py L19–L67](https://github.com/leeyejin1231/RV-HATE/blob/acfe053172a7266c8dde3759551882701478cdac/ppo_eval.py#L19-L67)：环境对所传dataset计算/缓存模型logits和真实label，并以macro-F1差反馈reward；[L155–L180](https://github.com/leeyejin1231/RV-HATE/blob/acfe053172a7266c8dde3759551882701478cdac/ppo_eval.py#L155-L180)：这条入口以**test_data**构造PPO环境，学习权重后在同一test_data评估 | 可肯定：**该公开入口**的test标签参与权重优化目标；未核作者论文Table实际是否从该入口/commit产生，不能用它否定作者正式所有数值；也未运行全管线。 |
| S-CAD-01 | CADET（WWW 2026 Main，CCF-A）；[Shu-Wan/cadet@1f1a25d56907c9aa83f9285ce32753a6945097f6](https://github.com/Shu-Wan/cadet/tree/1f1a25d56907c9aa83f9285ce32753a6945097f6) | [src/cadet/datasets/dataloader.py L119–L142](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/datasets/dataloader.py#L119-L142)及[L257–L313](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/datasets/dataloader.py#L257-L313)两处分支返回`(train,test,test)`；[src/cadet/training/cadet_trainer.py L219–L252](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/training/cadet_trainer.py#L219-L252)训练时对val_loader算F1并按其选最好模型/阈值 | 这使**所审公开训练路径**存在验证与最终测试不独立的高优先级风险；尚未重跑启动参数、核正式表是否取同代码/数据以及目标风格split；不写“论文作者已证明泄漏”。 |
| S-MM-01 | MultiMM（ACL 2025 Main，CCF-A）；[DUTIR-YSQ/MultiMM@33a01f111208b2ddbacdb06a667828c1246cc42b](https://github.com/DUTIR-YSQ/MultiMM/tree/33a01f111208b2ddbacdb06a667828c1246cc42b) | [code_metaphor/data_utils.py L67–L100](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L67-L100)：同一循环包含train/val/test，row[5]写成`data_dict['senti']`自然语言提示；[L150–L159](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L150-L159)从senti列进行tokenize并返回模型输入 | 可说公开隐喻检测路径直接读取CSV的情绪字段，并应用于测试样本；该列的人审/标签来源以已有P003精读卡为准；不能在未对齐运行脚本情况下把正式所有SEMD结果等同这一源代码版本，亦非隐喻真值标签直接泄漏。 |
| S-MG-01 | MGMCF（AAAI 2025 Technical，CCF-A）；[ZhengL00/MGMCF@02407e81099db63674ff27d97ee332011fcf4be0](https://github.com/ZhengL00/MGMCF/tree/02407e81099db63674ff27d97ee332011fcf4be0) | [loaddata.py L12–L25](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L12-L25)从独立pkl加载source/target特征；[L55–L64](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L55-L64)按ID生成相应特征；[L70–L78](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L70-L78)train/val/test均从同load_dataset路径生成；[L103–L109](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L103-L109)将source与target作为model inputs | 可说存在额外源/目标概念的**预计算输入优势**；这些pkl是人工gold、模型预测或外部数据何种来源**未实物溯源**，不能判定正式实验违反信息预算或全基线不公平。 |
| S-MC-01 | MCIB（AAAI 2026 Technical，CCF-A）；[sljgkjhwe/MCIB@d1430aa7bf827731b99cf4baed73525f0fd590c3](https://github.com/sljgkjhwe/MCIB/tree/d1430aa7bf827731b99cf4baed73525f0fd590c3)（旧R3B审计已登记同commit，本轮重新GET源码） | [MCIB_trans.py L110–L126](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L110-L126)在loss中先`y=y.squeeze(dim=-1)`后计算`criterion(y_pred,y)`，`y.expand_as(y_pred)`处被注释；若`y_pred[B,1]`与`y[B]`，PyTorch可广播为B×B；[L194–L224](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L194-L224)的分类路径确含`expand(output)+x`文本残差 | **有条件的张量形状风险+未经瓶颈约束的文本旁路**，不是正式训练错误已复现。必须打印真实训练batch两张量形状及激活路径，并核确认论文表格是否出自同commit；理论条件IB效果未有同结构noKL/noConditional消融。 |
| S-MK-01 | Meerkat-VL（ICML 2026 Main，CCF-A）；[Tunanzzz/Meerkat-VL@9ecb79281492bd491ef65f72647bcef893cba4fa](https://github.com/Tunanzzz/Meerkat-VL/tree/9ecb79281492bd491ef65f72647bcef893cba4fa) | [verl/trainer/ppo/ray_trainer.py L489–L553](https://github.com/Tunanzzz/Meerkat-VL/blob/9ecb79281492bd491ef65f72647bcef893cba4fa/verl/trainer/ppo/ray_trainer.py#L489-L553)：`ActorSelfVerifyManager`持有actor worker，prompt插`user_intent/safety_warning/harmful_intent`及answer；[L554–L616](https://github.com/Tunanzzz/Meerkat-VL/blob/9ecb79281492bd491ef65f72647bcef893cba4fa/verl/trainer/ppo/ray_trainer.py#L554-L616)：准备verify输入仅取先前responses文本+reward_model的ground_truth，再tokenize纯文字，未重新加入图片张量 | 可说**该自评构造函数**不是独立视觉重看；是否训练脚本成功进入分支和最终表格采用该版本仍O。此输入预算与真正“从原图重新审证据”的多模态自验证需要严格区分。 |

## 2. 暂无完整immutable file#line复核的既有S级线索（已在正文降级）

| Claim ID | 历史卡/作者仓库 | 当前状态与正文处理 |
|---|---|---|
| S-EMO-OPEN | [EmoBi P035](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P035_EmoBi.md)；作者库[ZhengL00/EmoBi](https://github.com/ZhengL00/EmoBi)；已识别仓库HEAD `e6a689d10af45a55bd8ba075490e880b7322473d`，未完成确定执行入口的逐行比对 | 调用先后顺序/双向性只写“既有阅读卡提出待核”，**不声称已经对外完全复核**。 |
| S-SQA-OPEN | [SemanticQA P022](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P022_SemanticQA.md)；[jacklanda/SemanticQA](https://github.com/jacklanda/SemanticQA)，当前HEAD `56c82a587f4a6cef609255cd10af372d8c76600a`，未核确切main evaluation调用 | 公开一次prompt“同时抽取解释”的实现仅以既有卡标待核，主文不描述为作者正式全部评测唯一执行方式。 |
| S-EXPO-OPEN | [ExPO-HM P027](https://github.com/YuSun-WK/implicit-content-research/blob/main/01_literature/cards/P027_ExPO-HM.md)；[官方代码](https://github.com/JingbiaoMei/ExPO-HM)，当前HEAD `388728efe24790171e38d9932226eeedcd22edfe`，本轮未重核课程train shell与reward数值路径 | 仅引用正式论文P级完整配置/消融；公开训练脚本课程/rollout不一致的历史卡记录保留O，**不将其写为论文正式训练事实**。 |

## 3. 复现等级/证据责任和发表门槛

1. 上述固定commit均经本轮GitHub只读接口定位；所列行可外部复查原始文件。除阅读卡历史记录外，**本轮没有运行模型、执行训练、重算PPO奖励、下载全数据或复现论文F1/ASR**。
2. “公开代码含该条件分支”≠“论文表格使用该分支”，特别是RV-HATE的PPO训练入口、CADET的val/test分离、MCIB的loss形状和Meerkat自评的reward数据字段必须附实际入口/版本日志才能升级正式实验协议结论。
3. **当前正文仅引用受限S级观察或提出验证要求**；任何编辑若要写“作者正式实验存在测试泄漏/模型真正不看图”等强论断，必须先获得作者实验使用commit、有效数据路径、可复核模型行为和合法的数据使用授权，否则阻断。
4. 该索引作为R6-Fix版本的学术证据附录，与原作者论文引用分开；源码链接不是论文成绩的直接证据。对无法公开定点证实的内容可保留OPEN，审稿复核时判是否移出正文。

**审稿状态**：P0-02已取得多条可信固定源码证据并将其与论文实验分层，仍待R6-A复审确认正文每处S级结论都正确引用且没有不当扩展；不能在此文件自行宣布P0-02 CLOSED。
