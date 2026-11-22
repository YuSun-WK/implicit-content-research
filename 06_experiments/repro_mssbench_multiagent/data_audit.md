# Data Audit · PARTIAL

固定数据为 `kzhou35/mssbench@12396d24157427b671d97f23a2e370fca98fdf55`，`combined.json` 308,884 字节，SHA256 为 `9b426a03e9abe3519b112d4f367c73577651a554539f9c8077f4989e9b546bca`。在数据卷、挂载目录和可见 Hugging Face 缓存未发现已有副本。本轮获取 JSON 和固定版本文件树元数据。 [固定数据发布页](https://huggingface.co/datasets/kzhou35/mssbench/tree/12396d24157427b671d97f23a2e370fca98fdf55)

| 口径 | Chat | Embodied | 合计 |
|---|---:|---:|---:|
| 原始记录 / 图对 | 300 | 76 | 376 |
| 每行多文本 | 2 queries | 每侧 5 instructions | |
| IF / CoT / Multi-Agent / QC 展开对 | 600 | 380 | 980 |
| Safe / Unsafe 输入 | 600 / 600 | 380 / 380 | 980 / 980 |
| 展开输入合计 | 1,200 | 760 | 1,960 |
| 展开后同文字 / 异文字对 | 600 / 0 | 150 / 230 | 750 / 230 |
| IC 单意图/指令展开对 | 300 | 76 | 376 |
| IC 同文字 / 异文字对 | 300 / 0 | 27 / 49 | 327 / 49 |
| 唯一路径 | 600 | 152 | 752 |

对单任务的字段全量扫描，必填字段全部存在且通过非空文本或列表检查。Chat 可选 `reason` 出现在 189 行，缺省 111 行。Embodied 每侧 5 个 instruction，所有行长度匹配。空字段、目录穿越路径、完全重复的原始记录、相同图路径的左右对、重复的路径-文本-标签组合均为 0。Chat query 每侧有 598 个不同文本和 2 组跨记录重用；Embodied 每侧有 91 / 106 个不同文本和 74 / 92 组重用。未逐条复核 query 与预设意图的语义一致性。

文件树覆盖 752 / 752 条引用，未发现额外图片路径。在原始记录槽中每条图片路径出现一次；展开后按 2 或 5 次复用。HF LFS 元数据标明 31 组不同路径具有相同 SHA256，涉及 62 个路径（Chat 22 组，Embodied 9 组），均跨记录，无同组左右图命中。尚未下载、解码、测像素或本地重算哈希。按路径去重无法避免同一内容跨实验切分，之后应以内容哈希做跨切分审计。

## 论文 Table 1 对账

| 类别输入数 | Chat HF / 论文 | Embodied HF / 论文 | 合计 HF / 论文 |
|---|---:|---:|---:|
| `harmful` / Physical Harm | 508 / 508 | 140 / 120 | 648 / 628 |
| `property` / Property Damage | 236 / 236 | 620 / 640 | 856 / 876 |
| `offensive` / Offensive Behavior | 268 / 268 | 0 / 0 | 268 / 268 |
| `illegal` / Illegal Activities | 188 / 188 | 0 / 0 | 188 / 188 |

按发布 broad category 对齐，Embodied 物理伤害多 20 条、财产损害少 20 条。20 条等于两条原始记录的展开规模，证据无法定位论文对应记录或判定差异来自重分类还是版本差异。保存完整发布口径，Stage 0 Gate 标记 STOP。Embodied 子任务的发布输入为 Place 460、Toggle 100、Drop 60、Heat 40、Pick_Place 100。 [正式论文 Table 1](https://proceedings.iclr.cc/paper_files/paper/2025/file/1cb57fcf7ff3f6d37eebae5becc9ea6d-Paper-Conference.pdf)

## 可复建清单

- [manifest.csv](manifest.csv) 共有 2,712 条输入索引，分 query 和 intent 两套分母。用 `record_index` 与 `text_index` 在固定 JSON 重建原文，并核对文本哈希。HF 哈希字段为远端元数据。
- [smoke_pairs.csv](smoke_pairs.csv) 20 对、40 个输入。每任务 10 对，每原始记录择首条文本，照类别、子任务、是否同文字轮询，并按发布内容哈希避免重复。仅作覆盖性测试。
- [smoke_images.csv](smoke_images.csv) 40 个唯一待下载路径、38,483,771 字节估算，含固定 URL 和预期大小。实取后须检查根目录约束、大小和哈希，先 `PIL.Image.verify()`，重新打开并 `load()`，记录尺寸和失败码。
- [data_audit.json](data_audit.json) 含完整字段、计数与 LFS 内容重复组。命令见 [README](README.md)。
