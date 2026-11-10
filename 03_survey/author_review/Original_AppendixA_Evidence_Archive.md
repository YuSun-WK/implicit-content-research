# R8 附录A历史源码证据备份（非正式综述内容）

> 此文件按R8现存稿原样保存附录A的代码位置与发布CSV证据，以便未来直接重构正文内的源码链接和来源限定。此为内部研究证据材料，不属于拟提交的综述学术附录；不代表代码运行结果或正式论文训练配置。正式替换附录前，必须完成正文旧指向的迁移。

# 附录A 可随稿公开的最小源码／发布数据证据

本附录是稿件本体的一部分，直接列出公开作者仓库的不可变链接；评阅者无需访问本研究的私人记录。2026-11-10定点重读下列文件。**S只证明所列commit中的公开路径，不证明作者正式论文的表格或模型权重由该版本／入口产生；未运行训练或推理。** 源码的静态风险不构成对作者正式实验错误或不当行为的判决。

| 编号／对应研究（刊会等级见正文引文映射） | 固定公开源码（40位commit＋文件行） | 可复核S观察；必须保留的O |
|---|---|---|
| **A1 RV-HATE**（ACL 2026 Main，CCF-A） | `acfe053172a7266c8dde3759551882701478cdac`：[ppo_eval.py L19–67](https://github.com/leeyejin1231/RV-HATE/blob/acfe053172a7266c8dde3759551882701478cdac/ppo_eval.py#L19-L67)、[L155–180](https://github.com/leeyejin1231/RV-HATE/blob/acfe053172a7266c8dde3759551882701478cdac/ppo_eval.py#L155-L180) | 环境缓存所传dataset标签并用macro-F1变化作reward；所列入口传test_data、训练PPO后再评同数据。**O**：论文实际入口／commit／split与表格对应，无运行复现。 |
| **A2 CADET**（WWW 2026 Main，CCF-A） | `1f1a25d56907c9aa83f9285ce32753a6945097f6`：[dataloader.py L119–142](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/datasets/dataloader.py#L119-L142)、[L257–313](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/datasets/dataloader.py#L257-L313)；[trainer L219–252](https://github.com/Shu-Wan/cadet/blob/1f1a25d56907c9aa83f9285ce32753a6945097f6/src/cadet/training/cadet_trainer.py#L219-L252) | 所列loader返回train/test/test；trainer按传入val的F1选模型／阈值。**O**：正式run是否使用这些分支、参数和目标split。 |
| **A3 MultiMM**（ACL 2025 Main，CCF-A） | `33a01f111208b2ddbacdb06a667828c1246cc42b`：[data_utils.py L67–100](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L67-L100)、[L150–159](https://github.com/DUTIR-YSQ/MultiMM/blob/33a01f111208b2ddbacdb06a667828c1246cc42b/code_metaphor/data_utils.py#L150-L159) | train/val/test从CSV row[5]构造senti，tokenize后返回；row[2]为隐喻目标。**O**：情绪列有效来源、OCR与正式表的run对应；不等于隐喻真值直接泄漏。 |
| **A4 MGMCF**（AAAI 2025 Technical，CCF-A） | `02407e81099db63674ff27d97ee332011fcf4be0`：[loaddata.py L12–25](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L12-L25)、[L55–78](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L55-L78)、[L103–109](https://github.com/ZhengL00/MGMCF/blob/02407e81099db63674ff27d97ee332011fcf4be0/loaddata.py#L103-L109) | 加载source/target pkl并随模型输入返回。**O**：pkl为gold、预测或外部构造的哪一种来源，及正式run和baseline的信息对应。 |
| **A5 MCIB**（AAAI 2026 Technical，CCF-A） | `d1430aa7bf827731b99cf4baed73525f0fd590c3`：[MCIB_trans.py L110–126](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L110-L126)、[L194–224](https://github.com/sljgkjhwe/MCIB/blob/d1430aa7bf827731b99cf4baed73525f0fd590c3/MCIB_trans.py#L194-L224) | loss中squeeze标签；分类路径有expand(output)+x残差。**仅当**实际y_pred为[B,1]且y为[B]时才有广播风险；真实batch shape、激活路径及论文run均O，不写已复现训练错误。 |
| **A6 Meerkat-VL**（ICML 2026 Main，CCF-A） | `9ecb79281492bd491ef65f72647bcef893cba4fa`：[ray_trainer.py L489–553](https://github.com/Tunanzzz/Meerkat-VL/blob/9ecb79281492bd491ef65f72647bcef893cba4fa/verl/trainer/ppo/ray_trainer.py#L489-L553)、[L554–616](https://github.com/Tunanzzz/Meerkat-VL/blob/9ecb79281492bd491ef65f72647bcef893cba4fa/verl/trainer/ppo/ray_trainer.py#L554-L616) | 自评提示含user_intent/safety_warning/harmful_intent和回答；此输入构造仅tokenize文字，未重新加入图像张量。**O**：正式训练是否进入该函数及其版本对应；不据此否定整个模型的视觉能力。 |

**固定发布数据。** VLSU（ICLR 2026，CCF-A）的[作者CSV](https://github.com/apple-aiml-research/ml-vlsu/blob/b7c1780d2d578a82fc5f11a070d93bcd50cb9e45/data/VLSU.csv)固定commit为`b7c1780d2d578a82fc5f11a070d93bcd50cb9e45`，Git blob为`09421adeb2e68eac1d5e829dcbd48848f21a0be6`。本轮直接读取该blob，按CSV记录而非物理文本行重计：8159条9字段记录、严格S-S-U为35、image_grade=not_sure为141。以下独立计数可在下载该固定CSV后执行，不要求私人仓库或模型运行：

```python
import csv
with open("VLSU.csv", encoding="utf-8", newline="") as f:
    rows = list(csv.DictReader(f))
assert all(len(x) == 9 and None not in x for x in rows)
ssu = sum(x["image_grade"] == "safe"
          and x["consensus_text_grade"] == "safe"
          and x["consensus_combined_grade"] == "unsafe" for x in rows)
uncertain = sum(x["image_grade"] == "not_sure" for x in rows)
print(len(rows), ssu, uncertain)  # 8159, 35, 141
```

这是发布文件的S，不是正式PDF的8187/37；差异原因、图片可达性及论文实际评测名单仍O。MMSafeAware的发布编号／图像／重复blob数量、Silent Signals的历史README主集数、MOSSBench的contrast映射数，本轮没有同等级不可变版本链，故从正文与附表撤去精细S整数，仅保留作者P级数据与发布差异待核。版本不一致不自动构成论文实验错误。

<a id="appendix-b"></a>
