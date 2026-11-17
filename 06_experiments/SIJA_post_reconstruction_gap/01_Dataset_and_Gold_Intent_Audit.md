# 数据与意图审核

SIJA固定revision `4087764c55ea76946bac6634aa4d63b2ad7bb5a0`。继承FA的766条metadata和ZIP central directory；本轮实际读取选定成员并验证解压尺寸、CRC32和Pillow解码，不下载整包。

技术Pilot候选为I7的192条，按id排序后seed20261117 shuffle取4条：[402,329,310,312]；不是依据预测筛选，非正式held-out。4张源图均解码，329/310的Cue解码，402/312的Cue因URLError失败，没有替换成容易成功的样本。共6个PNG成功，2次成员下载失败；详见日志。只有329实际进入自然条件推理；310因共享GPU冲突未执行。视觉检查329/310源图与Cue确认非血腥、可读，仍不是独立人工金标。

Gold审核：4条SOURCE_METADATA起草，referent暂用prompt文本、action/spec用源注释，均PENDING/UNVERIFIED；独立HUMAN_VERIFIED=0。私有review_queue.json保留完整内容，GitHub只提交schema和样本id/哈希。Codex图像查看不能冒充独立人工复核。未把category或源action/spec提供给natural条件；仅draft-intent显式额外提供三字段。

MagicBrush元数据revision `6c254560879df7851233ea0fd2ae2a62764d0ef2`；viewer API返回dev前32条。API结果未带commit绑定，所以只作发现候选，不能声称已固定图像字节至该revision。seed随机选row_idx [16,20,13,21]的4个旧源图链接首次全部HTTPError；随后逐行刷新链接，4张源图全部成功解码（见magic_fresh_decode.json）。无正常图片入模。不能把MagicBrush全体自动标ALLOW。未构造匹配视觉Cue，FORMAT_CONFOUND_UNRESOLVED。

当前正常候选源图4、正常模型研究输入0、SIJA结构完整2、实际自然推理1；安全可靠金标0、可靠意图金标0。因此主分析分母为0，不计算任何准确率或gap率。不是“0% gap”。后续先修复固定revision图像获取并审核16+16，再扩展实验。

[SIJA数据](https://huggingface.co/datasets/xianminye/SI2ESBench)、[MagicBrush数据](https://huggingface.co/datasets/osunlp/MagicBrush)。完整样本、图像和私人标注均不入Git。
