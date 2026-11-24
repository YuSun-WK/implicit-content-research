# EMBGuardTest v3 候选清单外部验证

固定数据：`EMBGuard/EMBGuardTest_v3`，提交 `c89d9e597149e22f34fc7c09e5e02125c2e1a521`，发布许可 Apache 2.0。三个使用的 Parquet 的完整 SHA-256 写在 `data_audit.json` 与 `fetch_pinned.py`；`absent_benign` 不属于本轮两个面板。原始图像与动作文本只在获授权的私有目录读取，本目录保存哈希 ID、图像像素哈希、逐条分数和聚合结果。

`fetch_pinned.py` 可按固定提交续传三个文件并核验完整 SHA-256。`prepare.py` 使用 PyArrow 24 读取发布字段，对 `causal_risky × decoupled_benign` 以 `image_path × situation` 对齐，对 `selective_risky` 用双向一致的 `pair_item_id` 配对；按解码 RGB 像素哈希检查每组图像身份，生成 `splits.csv`、`groups.csv`、`excluded_groups.csv` 与私有 `rows.json`。原始发布 ID 经 SHA-256 脱敏后进入清单；同分键是原发布 ID 的 SHA-256。

两款模型的脚本与冻结设置分别位于 `models/thinkingguard/`、`models/qwen/`。它们沿用 ASIMOV 的判定指令、处理器、模板及完整候选回答读出，只将输入正文改为原图和一条发布的 `action`。`situation`、`risk`、`hazard` 和 `type` 均不送入模型。ThinkingGuard 阈值 1.5，Qwen 阈值从 `../ASIMOV_shortlist_safety_qwen2b/threshold.json` 的完整数值复制；二者在本数据集上不校准。`score.py` 先用 `--phase pilot` 检查两条输入，再用 `--phase worker --worker 0 --workers 1` 或分工编号进行正式评分；`finish.py` 合并并保留失败条目。每个模型各应有 254 条逐例记录。

在已有分数上仅用 CPU 复算：

```bash
cd /home/ubuntu/data/project
python 06_experiments/EMBGuard_shortlist_external/replay.py
```

`replay.py` 只读两个模型的 `scores.jsonl`、`config.json` 和发布清单。两模型都成功评分的整组才进入共同分母；输出 `group_results.csv`、`excluded_score_groups.csv`、`metrics.json`。混合面板同一不安全动作分数同时用于单独提交与加入安全选项，保持图像级配对；全拒面板取两个不安全动作的最低风险分。两个面板先按场景、再按解码像素身份图像等权，95% 区间使用固定种子 `20261121` 做 20,000 次图像级重采样。
