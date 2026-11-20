# TRACE-S1C · MultiOFF 官方数据验收

**`COMPLETE_CASE_ADMITTED`。** MultiOFF 原作者论文指向作者 GitHub，README 指向作者公开 Google Drive，并要求研究使用引用论文。原作者入口允许公开下载及研究使用的证据来自这两处。该入口未给整个图像包另列可验证的通用再分发许可。数据仅作本地研究，没有随仓库发布。Zenodo 同名条目载有论文 PDF。 [MultiOFF 论文](https://aclanthology.org/2020.trac-1.6/) · [作者仓库](https://github.com/bharathichezhiyan/Multimodal-Meme-Classification-Identifying-Offensive-Content-in-Image-and-Text) · [作者 Drive](https://drive.google.com/drive/folders/1hKLOtpVmF45IoBmJPwojgq6XraLtHmV6) · [Zenodo 文件清单](https://zenodo.org/records/3899868)

从作者发布目录下载三个官方 CSV 和 `Labelled Images` 中列出的 746 个图片文件。三份 CSV 通过独立的直接下载与 Drive 原始文件下载逐字节比对。图片下载逐个核对 Drive 列示的字节大小，训练或评价所用图片全部经过本地解码。网络连接重置通过相同作者入口重试和 Google Drive 原始文件下载解决。数据保存在仓库外 `~/data/trace-assets/multioff/`。

| 官方 CSV | 原始行数 | 原始 offensive / non-offensive | 缺图 | 验收行数 | 验收 offensive / non-offensive |
|---|---:|---:|---:|---:|---:|
| `Training_meme_dataset.csv` | 445 | 187 / 258 | 1 | 444 | 186 / 258 |
| `Validation_meme_dataset.csv` | 149 | 58 / 91 | 1 | 148 | 57 / 91 |
| `Testing_meme_dataset.csv` | 149 | 58 / 91 | 1 | 148 | 57 / 91 |

CSV 字段为 `image_name`、`sentence`、`label`。实际标签编码为 `offensive` 和 `Non-offensiv`。原数据论文 Table 1 同样报告 445/149/149，其 Dev/Test 正类均写作 59，本轮取得的官方目录 CSV 各为 58，评价遵循文件中的实际标签。 [原数据论文 Table 1](https://aclanthology.org/2020.trac-1.6.pdf)

三条缺图对应文件名均不存在于作者发布目录的完整清单，余下 6 张已发布图像没有任何 CSV 引用。默认严格验收会失败。本轮在训练之前明示启用 `--complete-case`，仅依同名图是否存在排除这三条记录，保留原 split。实际被排除的三条恰为 offensive。未替换图像或按标签选样。其余 740 条记录没有格式错误、不可解码图像、重复名称或重复图像字节，且三个 split 未发现相同图像字节。原 CSV 与各 split 实际图像序列的聚合 SHA-256 已保存。评价结论只涵盖此完整样本子集。 [聚合验收与哈希](stage1c_multioff_admission.json)
