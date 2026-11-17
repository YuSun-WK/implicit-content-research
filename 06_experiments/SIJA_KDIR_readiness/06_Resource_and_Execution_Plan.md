# 本轮资源与后续执行

本轮CPU资料任务：零研究GPU推理/训练、零编辑生成、零新权重下载；未触碰旧模型缓存、共享环境、代理或sing-box。只读盘点现有缓存：ThinkingGuard-8B 4/4 indexed shards存在，共17,534,339,448 B，过去成功加载；未重新逐字验证官方权重hash。基础Qwen3-VL-4B固定revision目录只有generation_config/config/merges/chat_template等小文件，没有完整index/shards。不能将8B改名4B比较。详见logs/model_inventory.json。

本轮新增资料主要为37,462,506 B完整SIJA v2 PDF、约0.6MB HTML、小型SafetyPairs代码和元数据、2张目标图；含失败重试仍远低于2GiB目标，未下载整包敏感数据。最终保存目录字节另见logs/resource_summary.json（是留存量，不冒充精确网络计费量）。资料审核包仅少量已有图片。没有安装新依赖，使用已有Python/Pillow/pypdf/bs4作CPU读取。

需要继续的顺序：①合法取得带指令证据的风险去除配对；②32组小型输入盲审及二审，冻结8/24与B*选择流程；③单独取得/完整性核验4B，未来无害Smoke测真实峰值/吞吐；④运行512调用/家族。当前停在①，审核包可先确认已有资料应否排除。无需为了本轮修改网络出口；OpenAI可访问不证明HF数据/权重链路畅通。

未来软件：专属venv，固定torch/transformers/Pillow版本与processor配置hash，明确单GPU设备、bf16。预处理和解码配置、policy/prompt、图片及顺序进入完整manifest，任何改变不复用旧完成键。四格source+request不传目标图/类别；若需cue只能使用已核实资产且四条件一致，不启动生成流水线造cue。

成本是条件性估算：32组/128输入、四条件512调用；额外8 Smoke另计。按每次30/60秒估计约4.27/8.53 GPUh，不含权重下载和加载；每块≤6h，吞吐差需预注册拆块。同组四条件不能依结果删样本。人工审核上限建议≤2人日、≤32组，不用大规模标注修补数据不可得。

清理仅限本轮无用的空/失败clone目录与重复代码压缩临时件；保留本轮来源证据、有效审核包及所有FA2活跃缓存。不会删除他人模型或旧研究结果。
