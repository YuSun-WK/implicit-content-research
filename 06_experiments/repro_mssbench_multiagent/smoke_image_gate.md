# Smoke 图片门槛 · PASS

固定 `kzhou35/mssbench@12396d24157427b671d97f23a2e370fca98fdf55`。复用 Stage 0 的已锁 JSON，在获取图片前重新核对 JSON、主 manifest、Smoke pair 与文件清单的文本哈希、路径、版本、大小、SHA256 和配对关系。清单为 20 对、40 个独立输入，各有 10 对 Chat 和 Embodied。四个任务 × Safe/Unsafe 组各有 10 张图。

40/40 文件大小、HF LFS SHA256、`PIL.Image.verify()`、独立重新打开、`load()` 与 RGB 转换检查通过。共 38,483,771 字节，JPEG 23 张、PNG 17 张；宽 300–6,646、高 266–4,433 像素。配对与文件列表完全匹配，未替换样本。源图大小保存在审计表，适配后的尺寸由未来每个真实调用单独记录。

第一种传输在 5 个目标上遇到连接重置。随后仅对同 5 个固定路径执行大小受限的 curl 下载并复查全量 40 个文件。下载内容保留在独立缓存，库内提交逐文件审计和第一次运行的错误清单。 [最终逐文件审计](image_decode_audit.csv) · [首轮证据](logs/stage1/image_first_attempt.csv)
