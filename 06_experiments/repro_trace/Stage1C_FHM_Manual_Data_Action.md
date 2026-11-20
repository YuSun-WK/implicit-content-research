# TRACE-S1C · FHM 入场

**`FHM_MANUAL_ACTION_REQUIRED`。** 2026-11-19 UTC 对默认授权目录 `~/data/trace-assets/fhm/` 做了一次存在性检查，结果为缺失。FHM 读取、真实训练和 CUDA 更新均为 0。两条独立路线继续执行。

请本人登录 DrivenData，按 **Compete** 提示核对并接受官方许可，从 **Data Download** 下载，再上传并解压到服务器授权私有目录。该目录应包含 `img/`、`train.jsonl`、`dev_seen.jsonl` 和实际获得的其他 split。已有授权副本时提供其服务器路径，并确认已接受官方许可。 [许可页](https://www.drivendata.org/competitions/64/hateful-memes/page/214/) · [官方 Data Download](https://www.drivendata.org/competitions/64/hateful-memes/data/)

```bash
FHM="$HOME/data/trace-assets/fhm"
CLIP_DIR="$HOME/data/trace-assets/clip/32bd64288804d66eefd0ccbe215aa642df71cc41"
/tmp/trace-s0-py310/bin/python data_manifest.py --image-root "$FHM" --verify-images \
  --split-file train "$FHM/train.jsonl" --split-file dev_seen "$FHM/dev_seen.jsonl" \
  --tokenizer "$CLIP_DIR" --output .local/fhm-summary.json
```

按实际可用文件加入其他 `--split-file`。训练与开发验收通过后才能执行 `trace_text_only_diagnostic` 的真实 smoke，再推进不超过 100 批。原始作者 Caption 另需来源与样本对齐证据。 [FHM 包装配置](Stage1A_Mode_Semantics.md)
