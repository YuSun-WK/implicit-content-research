# TRACE Stage 1B 再验收｜2026-11-20 UTC

执行分支：`repro/trace-aaai2026-20261119`。本轮起点为 `6d7aa0ea3e32fd679f2f51ee39173c0e7432edeb`；同步远端后为 `1063162`。作者 TRACE 固定提交为 `83ecb799f897fe275185e082ee9a669f7d04bfaa`。

| 门禁 | 本轮结果 | 可核对证据 |
|---|---|---|
| G1 官方 FHM | `MANUAL_DATA_ACTION_REQUIRED` | 只检查默认授权目录 `~/data/trace-assets/fhm/`，目录不存在；未收到另一授权路径或本人接受官方许可的确认。未读取 FHM 记录，实际 Split 数量、标签、图片完整性、原始文字与重复情况均未知。 |
| G2 固定 CLIP | `VERIFIED_AND_LOADED` | 离线 `prepare_clip.py` 对固定 revision 的 8/8 文件完成 SHA-256 比对，CPU 实际加载 427,616,513 个参数；`download_requested=false`。[运行记录](stage1b_retry_clip_validation.json) |
| G3 模式 | 诊断模式仅待 G1；`trace_original` 为 `AUTHOR_CAPTIONS_BLOCKED` | 既有包装层保留单原文分类诊断与三候选原始模式的独立门禁。本轮没有获得可追溯的作者 InternVL/Gemini 两列原件。[模式说明](Stage1A_Mode_Semantics.md) |
| G4 FHM GPU Smoke | `TRAINING_NOT_RUN` | G1 未通过；真实 FHM Batch **0**、真实 FHM CUDA `optimizer.step()` **0**。FHM Loss、梯度、显存、单 Step 耗时与 Checkpoint 恢复均无实测。 |
| G5 100 Microbatch | `BLOCKED` | G4 无通过结果；**0/100** FHM Microbatch，未产生短跑 Checkpoint。 |

9 项 Stage 1B 相关 CPU 单元测试通过，见 [测试日志](stage1b_retry_cpu_checks.log)。先前 Stage 1C 的合成张量 CUDA 自检和 MultiOFF 实验均不是 FHM 训练证据，本轮没有将其计入 G4 或 G5。

## 用户需要完成的入场动作

1. 本人登录或注册 [DrivenData 官方 Hateful Memes 许可页](https://www.drivendata.org/competitions/64/hateful-memes/page/214/)，核对并接受规则与数据使用许可，再从 [官方下载页](https://www.drivendata.org/competitions/64/hateful-memes/data/)取得获准访问的原始包。已有合法副本可直接复用。
2. 将获准的原始数据放在服务器私有目录，建议 `~/data/trace-assets/fhm/`，其中应直接包含 `img/`、`train.jsonl`、`dev_seen.jsonl` 和实际取得的其他 Split。保留原始文件名，不要上传图片、标签明细或 Meme 原文到 Git。
3. 告知授权目录、下载日期、包名，并由本人明确确认已接受官方许可。只有该确认后才会在 Git 忽略的私有 YAML 中设置 `authorization_confirmed: true`。作者两列 Caption 若已合法取得，也请提供来源与路径供独立验收。

入场后，先用 `data_manifest.py --verify-images` 校验 Train/Dev 图片、字段、标签、ID 与跨 Split 重复；通过才运行单卡 BF16、Microbatch 1 的 `trace_text_only_diagnostic` 单批 Smoke。若 G4 通过，再按文档至多运行 100 Microbatch，并每 ≤25 批保存 Checkpoint。**Stage 2：`BLOCKED`。**

本轮只修正了既有计划命令的 GNU `timeout` 时间值为 `21540s`（5 小时 59 分钟）；未启动训练。
