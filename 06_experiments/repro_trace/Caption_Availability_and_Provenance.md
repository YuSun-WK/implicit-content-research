# FHM 数据及 Caption 门禁

**DATA_BLOCKED。** 本轮未找到可确认且具授权的本地 FHM 原图、Train/Dev/Test 标签源、两列作者原始 Caption，或可用于训练的本地 ViT-L/14 权重。

- 检查了项目根及同项目检出的文件名、目标分支已跟踪文件、作者固定路径和本地 Hugging Face / CLIP 缓存的目标模型目录。对共享目录下三个 `project*.zip` 仅扫描了中央目录条目名，按 FHM、目标 Caption、常见 split JSONL、常见 FHM 图片路径和 CLIP 关键词筛查。范围内没有可确认的候选。文件名筛查无法识别任意改名或嵌套文件；归档内容保持原状。
- 作者固定树有通用 open-images 标签描述，未包含 FHM 真实图像、标签或训练入口所需的合并 Caption JSON。私有路径 `/backup/girish_datasets/Hateful_Memes_Extended/ivl_plus_gemini_captions_complete.json` 在本机不可用。已核对的公开树不能回答作者是否在其他渠道提供文件。 [固定源码](https://github.com/surrey-nlp/TRACE/tree/83ecb799f897fe275185e082ee9a669f7d04bfaa)
- 因未读到授权标签源，Train/Dev/Test 各 split 的样本数、正负类数、缺图、缺 Caption、占位字符串、重复和值域皆为未知。汇总 JSON 用 `null` 表示未知。论文 Table 2 的 8,500 / 500 / 1,000 为作者报告，未填入本地统计。 [作者 Table 2](https://arxiv.org/html/2504.17902v2)
- `data_manifest.py` 可读合并 FHM JSON/JSONL 或分别传入官方 split 文件；按 split 计算标签、路径内图片存在、重复记录/ID/引用、三类候选覆盖以及已知 provenance 字段存在率。传入本地 CLIP tokenizer 时才统计未截断 token 最大值。汇总只保留计数；数据来源、许可和两列作者生成记录需结合项目授权材料人工核对。MultiOFF 的文件和标注协议独立于本清单。任何缺少有效标签的 split 都会标记不可评分。
- 本轮仅从官方 Hugging Face 取 CLIP 公开配置、tokenizer 和 image processor 配置；固定快照公布的权重 SHA 来自 Hugging Face API 元数据。未获取模型权重或 FHM 数据，也未调用 Caption API。 [FHM 官方许可入口](https://www.drivendata.org/competitions/64/hateful-memes/page/214/) · [CLIP 固定快照](https://huggingface.co/openai/clip-vit-large-patch14/tree/32bd64288804d66eefd0ccbe215aa642df71cc41)
