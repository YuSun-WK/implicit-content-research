# Table 1 对账 · 分类差异未解，功能性 Smoke 采用固定发布版

正式稿 §3.3–3.4 和 Table 1 的 Embodied 是 760 个图文输入，其中 Physical Harm 120、Property Damage 640。发布 JSON 每条 Embodied 记录有两侧各五条指令。固定版的 76 条记录分为 14 条 `harmful` 和 62 条 `property`，展开为 140 和 620。论文附录 A.6 的场景示例、A.7 Prompt、A.8 示例与官方 README、推理代码都未提供 Table 1 所用的逐条路径/类别交叉表。 [ICLR 正式稿](https://proceedings.iclr.cc/paper_files/paper/2025/file/1cb57fcf7ff3f6d37eebae5becc9ea6d-Paper-Conference.pdf) · [官方代码](https://github.com/UCSB-AI/MSSBench/tree/1602193f49cb6925bfa3751be157d0bbf5439779)

| HF 版本 | combined.json 实际结果 | Embodied 展开类别计数 |
|---|---|---|
| `4475d74fc48b03fe1925cc4b9414c286603fa3c8` | HTTP 404，无 JSON | — |
| `4d252925b58f1997bc0e8ea339b74ab9343d953d`、`4a9f96759acd76b076e637f1ca09ce1a876c2ad5` | 两文件 SHA256 同为 `8ee01047dc85712cf581c3c39610aefd627c2c7c9b57a5ad8da7c6cddec9f2b8`，62 条 | harmful 140 / property 480 |
| `429d0cbe61d9fbd87d254aff613841c4adb69125`、`12396d24157427b671d97f23a2e370fca98fdf55` | 两文件 SHA256 同为 `9b426a03e9abe3519b112d4f367c73577651a554539f9c8077f4989e9b546bca`，76 条 | harmful 140 / property 620 |

按 safe/unsafe 文件对连接，旧版 62 条记录与新版对应对象完全一致，包括类别字段。新版追加了下表中索引 62–75 的 14 条 `property`。公开历史没有记录能够解释从 paper 120/640 到发布 140/620 的两条标签移动。 [官方版本历史](https://huggingface.co/datasets/kzhou35/mssbench/commits/main)

| record_index（0 起） | HF 类别 | 任务 | safe / unsafe 文件（相对于 embodied/） | 证据范围 |
|---:|---|---|---|---|
| 20 | harmful | Place | `40.png` / `41.png` | 假设仅重分类时的候选池 |
| 21 | harmful | Place | `42.png` / `43.png` | 假设仅重分类时的候选池 |
| 22 | harmful | Place | `44.png` / `45.png` | 假设仅重分类时的候选池 |
| 23 | harmful | Place | `46.png` / `47.png` | 假设仅重分类时的候选池 |
| 24 | harmful | Place | `48.png` / `49.png` | 假设仅重分类时的候选池 |
| 25 | harmful | Place | `50.png` / `51.png` | 假设仅重分类时的候选池 |
| 26 | harmful | Place | `52.png` / `53.png` | 假设仅重分类时的候选池 |
| 27 | harmful | Place | `54.png` / `55.png` | 假设仅重分类时的候选池 |
| 28 | harmful | Place | `56.png` / `57.png` | 假设仅重分类时的候选池 |
| 29 | harmful | Place | `58.png` / `59.png` | 假设仅重分类时的候选池 |
| 30 | harmful | Place | `60.png` / `61.png` | 假设仅重分类时的候选池 |
| 31 | harmful | Place | `62.png` / `63.png` | 假设仅重分类时的候选池 |
| 56 | harmful | Drop | `112.jpg` / `113.png` | 假设仅重分类时的候选池 |
| 57 | harmful | Drop | `114.jpg` / `115.png` | 假设仅重分类时的候选池 |
| 62 | property | Heat | `124.png` / `125.png` | 仅在 v1.1 追加 |
| 63 | property | Heat | `126.png` / `127.png` | 仅在 v1.1 追加 |
| 64 | property | Heat | `128.png` / `129.png` | 仅在 v1.1 追加 |
| 65 | property | Pick_Place | `130.png` / `131.png` | 仅在 v1.1 追加 |
| 66 | property | Pick_Place | `132.png` / `133.png` | 仅在 v1.1 追加 |
| 67 | property | Pick_Place | `134.png` / `135.png` | 仅在 v1.1 追加 |
| 68 | property | Pick_Place | `136.png` / `137.png` | 仅在 v1.1 追加 |
| 69 | property | Pick_Place | `138.png` / `139.png` | 仅在 v1.1 追加 |
| 70 | property | Pick_Place | `140.png` / `141.png` | 仅在 v1.1 追加 |
| 71 | property | Pick_Place | `142.png` / `143.png` | 仅在 v1.1 追加 |
| 72 | property | Pick_Place | `144.png` / `145.png` | 仅在 v1.1 追加 |
| 73 | property | Pick_Place | `146.png` / `147.png` | 仅在 v1.1 追加 |
| 74 | property | Heat | `148.png` / `149.png` | 仅在 v1.1 追加 |
| 75 | property | Pick_Place | `150.png` / `151.png` | 仅在 v1.1 追加 |

如果样本集合相同且差异只来自粗类别重分类，净差等于两个 `harmful` 记录。这是一个无法逐条定位的假设，表中的 14 条仅为该假设下的候选池。没有证据支持改动其中任意标签，也无法排除论文使用不同的样本集合。按 Stage 1 任务书，保留固定 HF 原标签，允许功能性 Smoke。按类别报告时注明发布版口径，Table 1 类别严格复现仍为 unresolved。
