# Codex Stage 1｜VLSU ICLR 2026 图片获取与可评测性审计（2026-11-19）

## 唯一目标与执行门槛
在 Stage 0 HEAD `0dbe4a58209f1460d0a087604e647b5553bfa47b` 之上继续原论文复现。**只用 CPU/网络；不得加载模型、占GPU、训练或修改研究方向。**
目标是逐 UUID 审计官方冻结 CSV 的8159行，在不更换、不补造图片的前提下，测出图片 HTTP 成功、字节完整、解码成功与任务可评测覆盖，并提供可恢复的本地 Manifest。先离线集成测试→限制性真实 Smoke→检查通过后全量覆盖。任何安全、许可、网络或解析门未通过时立即BLOCK，不能以“已写代码”冒充下载完成。

## 必读来源和范围
- 仓库 `YuSun-WK/implicit-content-research`，分支 `repro/vlsu-original-20261119`。阅读 `00_Stage0_Source_Protocol_Audit.md`、`01_Codex_Stage0_Task.md`、`Run_Stage0.md`、`protocol/Original_Experiment_Matrix.md`、`protocol/Image_Download_Design.md`、`protocol/Output_Parsing_and_Metrics.md`、`reports/stage0/*`、已有 `scripts/stage0_image_checks.py` 和 `scripts/stage0_audit_csv.py`。
- Apple 数据锁定 commit `cbe363a26d2129ff1b526c283af0a2b7aa3d9b28`，Git Blob `09421adeb2e68eac1d5e829dcbd48848f21a0be6`，CSV SHA256 `9a4cd53fce796dd0c2bcae3a97c7ba6caf976c34f473aab2806cc2c325c8b74f`。不可静默使用主分支后续版本、不可增删行。
- 对照 Apple `utils/save_dataset_images.py`，可借鉴解码，但需要针对错误处理、恢复、限速实现独立审计；代码许可需要标注。PR #78 的132URL小试108成功**不代表新一轮覆盖率**。

## Stage 1A：本地可运行且可恢复的 CPU 下载器
文件建议 `scripts/stage1_download.py`, `scripts/stage1_report.py`, `scripts/stage1_manifest.py`, `configs/stage1_download.yaml`，并复用现有`stage0_image_checks.py`。
1. 首先在本机校验 CSV Blob和SHA256，且8159完整UUID；对每条记录持久化 `uuid, original_url, I/T/J labels, pattern, original_csv_row`。以URL去重下载，但对8159 UUID全部fan-out；8157唯一URL，原始 URL重复不等于图像语义相同。把状态文件和下载内容放在.gitignore覆盖的 `.local/` 或外部数据目录，支持用户配置路径。
2. 用SQLite或等价可靠状态库储存 `queued/inflight/success_http/success_decode/failed_terminal/retryable/deferred`、每次attempt原因、status、final URL、redirect链、日期、raw bytes、hash、MIME、像素、重试时间和复核信息；多次run保留历史与异常，不覆盖审计证据。持久化时使用原子更新，崩溃/CTRL+C后可从UUID、URL状态恢复，已验证且hash匹配的图片不重复下载。
3. SSRF防护：只允许HTTP(S)，拒绝credentials、非标准端口、localhost、私网/回环/link-local/multicast/reserved 地址，包含IPv4-mapped IPv6和替代地址表示。每次DNS解析和重定向都必须校验并固定实际连接目标，同时保持正确的Host与TLS SNI和证书校验；禁止自动不受控redirect、继承不可信代理或跳到未审核目标。**无法实现/测试上述保证则BLOCK live，绝不能退化为普通requests.get(url)绕过安全门。** 不允许下载403受限资源的镜像替代或绕过站点防护。
4. 低扰动网络政策：global worker默认<=8，per-host并发<=1、访问频率<=1req/s，全局节流，5s连接/10s读等待/30s请求总时限；max redirects<=5；最多3次重试，网络暂时错误/408/429/5xx指数退避并尊重Retry-After。401/403/404/410/非许可目标立即终止，记录而非无限重试。所有参数在YAML并打印运行快照；共享网络不能因高并发受影响。
5. 有限流式下载与恢复：默认单图20MiB字节上限、25MP解码像素上限，磁盘剩余空间门槛、temp file与atomic rename，字节/hash/MIME/Pillow verify/reopen+load、解压炸弹防护、图片第一帧可读性。Range断点续传**仅**在强ETag、If-Range、206/Content-Range等条件全部验证时允许；不满足则丢弃partial重新下载并留下原因。所有错误分开记录：HTTP失败/传输失败/格式错误/解码失败/下载但不符合限制。
6. 防止内网URL攻击之外，针对不可信图片采用受限解码进程及运行时间/内存上限；完整图片内容和危险原prompt不得放公开日志。不能以本地 PIL 报错后无检查地接受扩展名或自动代替图片。
7. 本阶段仅获得图片：不对图片内容给出人为安全解释，不修改标签、不做跨数据迁移、不引入训练数据。

## Stage 1B：严格测试
在 `tests/test_stage1.py` 建立CPU离线HTTP fixture/mock server，不访问真实第三方站点，覆盖：
- 同URL多UUID fan-out、非重复URL去重；中断恢复及已成功文件不重复请求。
- 200成功、非图字节、MIME不符、损坏PNG/JPEG/WebP、25MP/20MiB限制、hash记录。
- 301/302重定向到 localhost/私网、DNS rebinding、IPv4-mapped地址、认证凭据URL、HTTP到HTTPS的正确校验；实际连接目标/Host/SNI一致。
- 403/404/410终止、429 Retry-After、5xx与timeout重试限额、每host并发和节流。
- 断点文件、Etags、206正确、200忽略Range、416和Content-Range错误均有明确处理；任务被中断和磁盘满时仍可重启。
- 各模式总分母保留8016（paper17）、2（额外两个单例）、141（含not_sure），联合总8159、image有效8018、text8159。
执行 `python -m pytest -q` 与 `git diff --check`，记录原始真实命令、输出、执行环境版本、失败/修复过程。至少33个Stage0用例仍需通过，不得只报Stage1用例。

## Stage 1C：安全真实 Smoke Test（不直接全量）
- 在正式8159行中按真实I/T/J组合分层、使用固定种子 `20261119`，每论文组至少1且优先2；另包含2额外单例与6个含?组，目标`40–60`条唯一UUID，固定可再生的UUID名单，禁止按预期可用性挑选。对稀少组按可用数取样。
- 命令必须提供 `--dry-run`、`--phase smoke`、`--max-requests`、`--resume`；默认dry-run，不静默开网。需要保存软件版本、请求时间、URL/UUID私有失败清单、HTTP/解码结果、模式级覆盖；对重复/同域重试展示限速和resume行为。
- 测试集适当包含重复原URL，不超越60条UUID，避免不必要的请求；有403/429即按礼貌速率处理，不进行绕过。
- **Smoke PASS gate**：安全测试通过，成功图片均可解码并有SHA256，失败有对应原因，UUID全集可追踪，ctrl+C/第二次运行不会重新下载已验证文件，能安全恢复，限速与字节上限生效。若任何项失败，停在BLOCK，修复后重测。不要为了达“高成功率”跳过失败样本。

## Stage 1D：全量CPU获取（仅 1C PASS 后）
- `--phase full --resume` 默认全8159UUID，严格限制workers <=8和每host<=1；小批次持久化、定期checkpoint；磁盘/网络资源风险时温和暂停、保留清单。即使不是所有 URL 成功，也应在可控重试耗尽后报告完成；提供可继续重试的明确政策而不是无限循环。
- 如果工作环境网络/权限/磁盘/时间不允许全量完成，输出PARTIAL和明确未处理UUID数；绝不写FULL PASS。实际任务运行在用户认可的有网机器上，不能声称在GitHub插件里已执行了真实网络。
- 同一URL若内容已改变，保存hash/时间且保留旧状态以审计，不能静默更换历史已记录图片。
- 整理`release_roster` (8159UUID) 与 `joint_decoded`、`image_decoded_gold`、`text_only_eligible`、`three_modality_intersection` 等不可变ID清单，全部用 CSV hash+download snapshot+脚本版本生成；复制前校验。

## Stage 1E：可报告成果及严格分母
只提交非敏感的聚合报告与manifest摘要，建议 `reports/stage1/Stage1_Image_Coverage.md`, `Stage1_Execution_Log.txt`, `coverage_by_pattern.csv`, `coverage_by_label.csv`, `coverage_by_failure_type.csv`, `coverage_summary.json`, `coverage_manifest.sha256`。私有原始URL/UUID级失败清单只在`.local/`保存，报告仅包含count/hash，不泄露图片。
必须输出：
- PAPER_N=8187 (AUTHOR-REPORTED), RELEASE_N=8159 (PINNED CSV)；
- 可请求UUID数、唯一URL总数、尝试/未尝试URL、HTTP成功URL数、有效字节数、解码成功URL数、经UUID映射可评测的联合样本数（若图像成功即可，含141个not_sure图像标签）、image-only可评测数（剔除141或相应交集）、text-only独立有效数、Figure4/5三金标可评测上限；
- `decoded_joint_coverage = decoded_joint_UUID / 8159` 与每模式`decoded_n / release_n`，另对每个模式给success/failed/not_attempted，别把后者当404；
- 失败原因分类、HTTP失败域数、解码失败数、重复URL映射数、资源上限触发数、下载时间分布、失败集中度及偏差；明确URL可访问和图像语义正确是不同问题；
- 按真实17论文模式、2个额外单例、6个问号组输出（含零计数）。S-S-U、S-S-B、U-S-B、U-S-U、B-B-U五类强制高亮；可选Wilson95%仅做本地覆盖比例区间，不要把它当分类准确率CI。
- E2/E3/E5使用共同可解码joint UUID清单；E1 image/text各有自己的可评估清单；E6/Figure4需要三标签有效且图像可用；不同模态报告同一UUID交集范围。
- 本阶段任何分类精度、F1、模型性能均标NOT RUN。

## 独立质量门与完成汇报
- 对`stage0_metrics.py`的未来预测评分设计增加“官方UUID任务名单强一致性检查”前置校验（不能只依赖传入JSONL自证完整）；不破坏Stage0已通过的测试。可以先交新增`scripts/stage1_manifest.py`的验证方法/单元测试，正式推理脚本留Stage2。
- 将 Stage0 Prompt 人工逐字审阅缺口继续列OPEN，不虚报已解决；图像面积单位与原论文配置、Qwen precision/revision仍UNKNOWN，Stage1无需解决。
- 严格禁提交图片、权重、原始发布CSV副本、完整原prompt、含风险文本的原始输出、许可证不允许再分发的数据。仅本目录代码+configs+聚合报告和文档；不得碰综述、H1、PR#78。
- 将成果提交同一分支（不合main），给commit SHA、完整改动文件、真实run/test日志、阶段完成级别（STAGE1A/B/SMOKE/FULL）、成功/失败/未尝试UUID与分组覆盖、数据缓存本地相对位置和恢复命令、Stage2是否可开始以及阻断原因。
- **Stage 2 仅在 Stage1可解码样本清单可重复和可审核后才提议**；这次不实际运行GPU。
