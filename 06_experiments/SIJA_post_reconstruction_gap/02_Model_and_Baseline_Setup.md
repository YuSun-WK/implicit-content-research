# 模型与运行配置

目标4B：Qwen/Qwen3-VL-4B-Instruct，revision `ebb281ec70b05090aa6165b016eac8ec08e71b17`，Apache-2.0。公开卡仍可访问；专属缓存snapshot_download尝试失败（HEAD连接重置/超时，CAS五次重试失败）。部分小文件与未完成稀疏权重保留私有目录，磁盘实际约67MiB；**未取得完整4B模型，4B推理0次**。直接curl取得config，但不能弥补权重缺失。[官方模型](https://huggingface.co/Qwen/Qwen3-VL-4B-Instruct)。

替代技术诊断：已有本地Sandy124/ThinkingGuard-8B，revision目录 `76892f9768ce828268265171f4bbc5dfb75eafc3`。本轮标准4个safetensors及本地index已存在，实际成功加载；与FA上一日缓存完整性状态不同，不覆盖旧记录。此模型经过安全训练，不能替代基础4B公平比较，未称作者官方防御复现。未更改原缓存，未验证本地每字节等于官方权重。

专属venv310使用Python3.10.19并只读继承现有ESTMM包：torch2.9.1+cu128、transformers4.57.3；无全局安装。bf16，无量化，SDPA；单张物理卡、显式cuda:0，未用device_map=auto。目标≤16GiB、硬上限20GiB。图像RGB、长边512、保持比例不裁剪；greedy、512tokens、batch1、seed20261117。system消息需content列表；首次字符串形式触发TypeError，在Smoke开发阶段修复。提示词内容未修改。

实测无害双图：首次失败1次，修复后完成1次；生成10.24s、126tokens；allocated/reserved 16.48/16.63GiB。只证明1条接口通过，不能据此宣称Gate0的总体≥90%稳定性。

SIJA探索性：完成natural与draft-intent各1次；matched第1次期间中断，direct/strong未开始。计划10条任务，未选择性保留优胜结果；中断即保留已完成日志。两次生成合计48.91s。全部完成输出合计59.15s，最高allocated/reserved 16.54/16.65GiB；不含加载/下载/中断调用耗时，不能当总墙钟时间。

GPU型号服务器报RTX4090、每卡49140MiB，驱动580.82.09，CUDA兼容13.0。05:38开始环境检查，08:28中断本轮最后GPU任务（UTC）；准备/下载及执行窗口约2h50，非持续GPU时间。后续CPU报告整理不计推理时间。GPU0初始空闲，Smoke曾用0及5；Pilot在0空闲后启动，随后检测另一约14GiB任务，与本任务约17GiB短暂共卡，立即仅中断自己的进程，确认释放；不能声称全程独占或完全零影响。没有杀其它用户进程。当前所有卡占用，不继续启动。

B0/B2原FA定义已归档configs/prompts.json但本轮未执行。B1 Original完整包含C.5例子；B3 Gold被HUMAN_VERIFIED门控，不可用draft绕过。DRAFT-INTENT是额外诊断，不能命名Gold；B4只预备了中性三字段，额外文本长度/token尚未严格匹配，禁止因果比较。每次调用原始输出私有保留，公开仅计数/时延/token/hash。
