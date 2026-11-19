# TRACE-S1A · 官方 CLIP 权重

**G2 `VERIFIED_AND_LOADED`。** 官方仓库 `openai/clip-vit-large-patch14` 的固定 revision `32bd64288804d66eefd0ccbe215aa642df71cc41` 已备齐。原本的默认缓存没有此模型。仓库外的固定 revision 目录中，8 个所需文件全部匹配 `upstream_manifest.json` 的 SHA-256。模型文件实测 **1,710,540,580 bytes**，SHA-256 为 `a2bf730a0c7debf160f7a6b50b3aaf3703e7e88ac73de7a314903141db026dcb`。

普通 Hugging Face Hub 快照尝试遇到连接重置，按文件下载遇到 CDN 读取超时。在官方 Hugging Face Git LFS 下载接口上取得相同对象并续传，经 HTTP Content-Range 区段核对和整文件 SHA-256 比对后才安装完整模型。原始网络日志和分段临时文件位于 Git 之外或忽略目录。

用本机隔离环境在 CPU 上执行实际 `CLIPModel.from_pretrained` 和 tokenizer/processor 加载，成功加载 **427,616,513** 个 CLIP 参数，dtype 为 `torch.float32`。`prepare_clip.py` 的完整验证与加载耗时 **7.199 秒**，没有触发缺失或尺寸不匹配的参数错误。该结果来自 CLIP 加载阶段。Stage 0 的 TRACE 全装配参数量是独立的配置级证据。 [逐文件大小、SHA 和加载日志](stage1a_clip_validation.json)

## 可复用的权重命令

权重目录位于仓库外的 `~/data/trace-assets/clip/32bd64288804d66eefd0ccbe215aa642df71cc41/`。下列命令使用固定版本和固定文件集。在可访问官方 Hugging Face 的机器下载后，可将同一目录离线传到服务器。

```bash
REV=32bd64288804d66eefd0ccbe215aa642df71cc41
CLIP_DIR="$HOME/data/trace-assets/clip/$REV"
HF_ENDPOINT=https://huggingface.co hf download openai/clip-vit-large-patch14 \
  model.safetensors config.json preprocessor_config.json tokenizer_config.json \
  tokenizer.json special_tokens_map.json merges.txt vocab.json \
  --revision "$REV" --local-dir "$CLIP_DIR"
```

跨机器传输时，在联网机器执行下列命令，将 `server` 换成项目的 SSH 登录目标。

```bash
rsync -a --partial --exclude='.cache/' "$CLIP_DIR/" "server:~/data/trace-assets/clip/$REV/"
```

然后在服务器的 `06_experiments/repro_trace` 目录执行实际 SHA 与 CPU 加载检查。

```bash
REV=32bd64288804d66eefd0ccbe215aa642df71cc41
CLIP_DIR="$HOME/data/trace-assets/clip/$REV"
CUDA_VISIBLE_DEVICES='' /tmp/trace-s0-py310/bin/python prepare_clip.py --model-dir "$CLIP_DIR"
```

也可给 `prepare_clip.py` 加 `--download`，用当前隔离环境直接获取官方固定快照并校验。以脚本 JSON 中的 `VERIFIED_AND_LOADED` 和退出码 0 为准。报告只包含固定模型、文件大小、哈希与加载状态。

[官方固定快照](https://huggingface.co/openai/clip-vit-large-patch14/tree/32bd64288804d66eefd0ccbe215aa642df71cc41) · [固定资产清单](upstream_manifest.json)
