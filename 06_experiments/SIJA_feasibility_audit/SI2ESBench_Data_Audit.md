# SI2ESBench 数据审计

核查时间：2026-11-16 UTC。独立结构检查，不是标注质量或图像内容审查。

[官方元数据](https://huggingface.co/api/datasets/xianminye/SI2ESBench)；固定 revision `4087764c55ea76946bac6634aa4d63b2ad7bb5a0`。[固定文件树](https://huggingface.co/datasets/xianminye/SI2ESBench/tree/4087764c55ea76946bac6634aa4d63b2ad7bb5a0)。公开、private=false、gated=false；卡片仅28字节，声明 Apache-2.0，未提供逐图片来源权利清单。官方GitHub说明仅用于安全学术研究；不得据此推断所有衍生图像版权均已厘清。

文件：`.gitattributes` 2504 B、`README.md` 28 B、`SI2ESBench.zip` 1,003,437,789 B。ZIP LFS SHA256 `a6eacee3626d8b38c88d73dcb2342c972cfbf64e3dd167fc56138e2987fe3ef6`（服务器声明，未下载整包计算）。

使用 HTTP 206 Range 读取尾部、central directory和唯一JSON成员（压缩13,716 B，解压211,764 B）；未下载或解码任何PNG。首次连接超时，重试成功。结构结果见 [日志](logs/data_structure.json)。全包CRC与图像可解码性未检验。路径存在仅证明ZIP目录声明，不能证明图像字节完整。

| 检查项 | 论文声明 B.3 | 实际观察 | 一致性 | 证据 |
|---|---|---|---|---|
| 样本数 | 766 | information.json 766条、766唯一id | 是 | 本地结构日志 |
| 源图 | 每条提供 | 766个声明路径全部命中ZIP目录 | 结构一致 | source_image/ |
| 动作图标 | action-icon-path | 字段不存在；无独立图标目录 | 否 | JSON字段/ZIP目录 |
| 规格图片 | edit-spec-path | 766条字段存在，路径全部未命中 | 否 | 指向cue_image/edit_spec/ |
| 定位文字 | prompt | 766条非空 | 结构一致，语义未验 | JSON |
| 风险标签 | category | 766条非空列表，10类 | 是 | 日志分布 |
| 语义注释 | action/spec-annotation | 两字段非空；无独立referent框或规范三元组金标 | 部分 | JSON |
| 完整Cue | 由图标和规格组合 | cue_images/{id}.png 766个全部存在 | 结构支持，语义未验 | 适配映射 |
| 作者生成结果 | 非B.3必需 | 无输出目录 | 未发布于此ZIP | 目录审计 |
| 匹配TJA/VJA/SIJA | 论文做配对实验 | 无独立TJA/VJA输入包 | 不完整 | 目录/字段审计 |

实际目录：`source_image/` 766 PNG，`cue_images/` 766 PNG，`information.json`，两个目录项；合计1535 entries。实际字段为 `id, image-path, action, edit-spec-path, spec-annotation, prompt, category`。未将敏感文本或图片入库。

适配方案：保持源图和prompt不变，按id加载合成cue；必须逐条核验少量安全可审查样本与论文输入语义一致，再固定映射。不可把损坏的edit-spec-path静默替换后声称原始schema完整。类别、action、spec-annotation仅留评价侧。当前可做结构级使用；完整可用性 PARTIAL。
