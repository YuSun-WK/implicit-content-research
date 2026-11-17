# SIJA-FA2 执行与复算

先读00协议及06结论。原始样本、图像、完整输出、review_queue及下载缓存在工作区独立私有目录，均不提交。公开日志只有脱敏id/hash、实际耗时及状态。

- prepare_data.py：输入私有元数据JSON和FA的central-directory entries，以固定seed选择并Range下载验证CRC；运行时指定--private-dir。元数据/entries通过FA audit_remote_zip.py产生，不入Git。
- run_guard.py：--model本地完整snapshot --manifest私有列表 --output私有JSONL；外部CUDA_VISIBLE_DEVICES必须只有一张空闲卡。记录样本级异常；相同id/condition成功记录可恢复跳过。Gold强制HUMAN_VERIFIED。不要将输出目录指向Git仓库。
- manifest每项：id、condition、images(两个本地路径)、text；gold追加referent/action/specification/review_status；matched追加neutral_context。system可指定Direct/Strong。默认C.5完整prompt。
- metrics.py：输入人工审核JSONL（id/group/review_status/policy_status/gold/answer/R/A/S/condition）；仅HUMAN_VERIFIED、policy MATCH、ALLOW/DENY进入主分母。必须按条件分别调用summarize，paired用于natural/gold/matched，禁止跨条件混算总体率。
- checks.py：标准库CPU验证解析与指标边界，不含真实安全结果。

本轮没有完成可信E2；neutral长度控制尚未冻结，不应直接开展held-out。snapshot下载需独立缓存、固定run.json中的revision。原prompt是FA保留的HTML空白规范化文本，未改语义。对外称SIJA Prompt – Independent Adaptation。

运行后的共享资源保护改进：runner现在在加载前检查显存，并在加载完成后每2秒检查显存相对本进程reserved的额外占用，发现疑似其它分配则SIGINT退出；这部分仅做CPU编译检查，尚未GPU实测，不能追溯宣称本轮Pilot已有自动保护。部分调用前后输入token日志是后续新增，已完成输出仅保留真实记录，不补造值。

fetch_magic_candidates.py修复viewer签名链接过期问题，记录固定revision查询参数及图像hash；服务未返回revision绑定，不能将查询参数当作commit字节一致性证明。configs/original_prompt.txt保留FA字节，包括行末空格，保证实际执行版本可追踪。
