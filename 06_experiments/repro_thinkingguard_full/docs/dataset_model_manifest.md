# 数据和模型清单

测试配对键由 split、规范类别和 CSV 原始 index 组成。原始 CSV 行位置、原类别、原标签字段和图片路径一并保留。类别映射中 Train 为 `region_belief`，Test 为 `religion_belief`。实际图片路径由 split、类别目录及原字段中的文件名确定。旧例中的 CSV index 和图片文件编号可能不同。

36 个 CSV 对应 5,600 条图文记录。Train 有 1,932 对，Test 有 868 对。每对两侧各一条、文本逐字一致。数据门槛要求冻结 CSV 的官方 blob 一致、所有 Test 图从对应固定版本取得或由该版本 LFS SHA256 核验，并完整解码。原字段的路径可以在不同 split 重复。实际 HF 路径含 split，并单独用于泄漏检查。泄漏表报告精确文本、规范化文本和 SHA256 覆盖情况。

模型缓存沿用 `76892f9768ce828268265171f4bbc5dfb75eafc3`。四分片 17,534,247,392 B 均与官方 LFS 哈希一致。本地修复索引重新定位官方索引的 118 项映射，实际头部共 750 个 tensor。官方文件与修复文件各自的 SHA256、配置及 tokenizer blob 对照存于 [model_cache_audit.json](../artifacts/model_cache_audit.json)。
