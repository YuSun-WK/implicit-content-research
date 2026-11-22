# Stage 1-Fix · 下载、依赖与 G1 设置

模型仍为 `liuhaotian/llava-v1.6-vicuna-7b@deae57a8c0ccb0da4c2661cc1891cc9d06503d11`，视觉塔仍为 `openai/clip-vit-large-patch14-336@ce19dc912ca5cd21c8a653c79e251e808ccabcd1`。原生 LLaVA source 仍锁定在 `c121f0432da27facab705978f83c4ada465e46fd`。 [原始 LLaVA 发布](https://huggingface.co/liuhaotian/llava-v1.6-vicuna-7b/tree/deae57a8c0ccb0da4c2661cc1891cc9d06503d11) · [CLIP 发布](https://huggingface.co/openai/clip-vit-large-patch14-336/tree/ce19dc912ca5cd21c8a653c79e251e808ccabcd1)

## 传输诊断

| 路线 | 已观察结果 |
|---|---|
| 默认代理 | 多个主机的 CONNECT 返回 200 后 TLS/传输被重置。HF 小 API 也不稳定，无法仅据这些错误定位代理或上游的责任。 |
| 官方 HF 1 MiB Range | 部分 HTTP 206 成功按 Content-Range 持续推进，保存分片 2 的 5,242,880 B、分片 3 的 6,291,456 B、CLIP 的 10,721,839 B。分片 1 在目标缓存中仍 0 B。分片累积只有最终整文件 SHA256 通过后才可使用。 |
| 直连 HF / PyTorch | 更换直连 DNS 路由后，HF 前端仍超时或 TLS 重置。Xet CDN 根路径可握手并返回 403，无法证明接受任意未授权对象请求。PyPI 元数据有时直连成功，大 torch wheel 仍读超时。 |
| ModelScope 镜像 | API 元数据查到 `AI-ModelScope/llava-v1.6-vicuna-7b@9bc88088944aefd1a04cb8e60f7799855c680b44` 和 `AI-ModelScope/clip-vit-large-patch14-336@ff5f616e6203df089a05407938e295f4de2bf7ed`。四份大文件的大小和 SHA256 元数据逐一匹配官方。代理下分片 1 的独立 1 MiB 探针成功返回 `206` 和正确总长度，4/64 MiB 批量续传在固定次数内失败。直连 CDN、显式解析 CDN IP 和国际域名探针也未完成有效数据段。 |

续传器只在最终 HTTP 206、Content-Range 起止点和总长、实收字节都匹配时追加；保留连续前缀，单块最多三次。最终文件重算官方 SHA256，普通 Git 对象重算 blob OID，全部通过才原子写出 `weights_verified.json`。镜像用于传输同一对象。镜像签名 URL、模型二进制和 venv 都留在本机未跟踪路径。 [传输日志](logs/stage1fix/transfer.log) · [固定哈希和文件状态](stage1_fix_weights.csv)

## 环境和预检

原有环境保持只读。独立 (Python 3.10.19) venv 用本地缓存和单包安装得到 Transformers 4.37.2、tokenizers 0.15.1、sentencepiece 0.1.99、HF Hub 0.23.5、NVML 12.560.30、shortuuid 1.0.13。通过 venv 内的 `.pth` 只读复用 ESTMM 的 Torch 2.9.1 / CUDA 12.8、torchvision 0.24.1，以及本机已有 Accelerate 1.12.0。使用本地 bitsandbytes 0.48.2 wheel。固定 tokenizer 实际配置为 `legacy=false`，CPU 运行先暴露缺 protobuf；从本机已有环境复制纯 Python protobuf 3.20.3 到独立 venv 后复测通过。此依赖组合是本地运行差异，模型和源代码未替换。真实 GPU 的 NF4 内核、模型驻留和生成仍待验证。 [完整版本](logs/stage1fix/environment_freeze.txt) · [带出处的 CPU 日志](logs/stage1fix/cpu_native_import.log)

执行时将实验缓存根目录设为 `.stage0-local/stage1`。镜像 JSON 由 ModelScope 的 `/api/v1/models/<repo>/repo/files?Revision=master&Recursive=true` 取得。运行器还会校验条目内固定 file revision，因此 listing 中改变对象会阻断传输。

```bash
stage=.stage0-local/stage1
python stage1_weights.py "$stage" --range-mib 1
python stage1_weights.py "$stage" --mirror-metadata "$stage" --range-mib 64
timeout -k 5s 200s python stage1_weights.py "$stage" --mirror-metadata "$stage" --range-mib 4
```

模型文件完整后使用下列命令。GPU UUID 须重新核对空闲，两个独立探针与 G1 共用一个模型实例。探针记录 text-only、有图的 embeddings 长度、原始回答、Token、耗时和显存。G1 仍按既有角色和断点策略运行，模型空输出或格式不遵循与工程异常分开记录。

```bash
stage=.stage0-local/stage1
gpu=GPU-79ea6ee8-2e76-d36e-1508-7813c1589ec1
CUDA_VISIBLE_DEVICES="$gpu" HF_HUB_OFFLINE=1 PYTHONDONTWRITEBYTECODE=1 \
PYTHONPATH="$stage/LLaVA-c121f0432da27facab705978f83c4ada465e46fd" \
"$stage/native-venv/bin/python" stage1_smoke.py \
  --data-root "$stage/data" --model-root "$stage" --official-source /tmp/mssbench-stage0-official \
  --output "$stage/g1-fix" --gpu-uuid "$gpu" --preliminary-probes --through g1
```
