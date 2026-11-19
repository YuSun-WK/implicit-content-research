# TRACE-S1B · FHM 正规入场

**G1 `MANUAL_DATA_ACTION_REQUIRED`。** 默认授权路径 `~/data/trace-assets/fhm/` 不存在，本轮没有收到其他授权路径或用户许可确认。只检查了该路径。读取的 FHM 记录数为 0；下载日期、官方归档名称、归档 SHA-256 与实际数据覆盖均未知。 [本轮预检日志](stage1b_preflight.log)

| Split | 文件、图像、ID、原始文字和标签 | 可审计的计数 |
|---|---|---|
| `train` | 未验收 | 未知 |
| `dev_seen` | 未验收 | 未知 |
| `dev_unseen` | 未验收 | 未知 |
| `test_seen` | 未验收 | 未知 |
| `test_unseen` | 未验收 | 未知 |

缺失值、标签分布、重复、跨 split 重叠和图片可解码性均待验收。作者两列增强 Caption 延续上一轮未核实状态。Test 只登记实际提供的标签状态，本轮无 Test 评分。

1. 请本人登录 DrivenData，在许可页点击 **Compete** 并按提示核对并接受竞赛规则和数据使用许可。官方下载页在未登录时跳转登录。 [DrivenData 官方许可](https://www.drivendata.org/competitions/64/hateful-memes/page/214/) · [官方 Data Download](https://www.drivendata.org/competitions/64/hateful-memes/data/)
2. 从官方入口取得归档，将原始文件解压到有访问权限的私有路径，建议 `~/data/trace-assets/fhm/`。目标目录应直接包含 `img/`、`train.jsonl`、`dev_seen.jsonl` 和其他实际取得的 split 文件。请确认已接受官方许可，并告知路径、下载日期和包名。已具备授权副本时请直接提供现有路径。
3. 输入准备后再运行 `data_manifest.py --verify-images --split-file …`，按 split 检查 ID、路径安全、图片解码、文本、标签及重复，并检查 Train 与已提供的留出 split 是否重复。运行器以文件指定的 split 正规化无 `split` 的 JSONL，授权确认只写入私有 YAML。
