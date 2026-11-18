# H1-K3：匿名人工审核准备（仅CPU）

状态：**PREPARED_FOR_HUMAN_REVIEW**；同时 **HUMAN_REVIEW_PENDING**。本目录不提供人类判断，不确认风险表示衰减，也不自动启动后续实验。

从固定H1-K2提交 `e6d80b030d43918ca502091717e9334aaab5b561` 独立建立准备分支。K2裁决为PIVOT；A6/B12/C18是非盲助手筛查，不能当人审结果。原始36对、72张图片及180条预测保留，单模态/联合任务目标混杂尚需独立人审与后续任务控制。

- [准备报告](H1_K3_Preparation_Report.md)
- [中立审核指南](H1_K3_Review_Guidelines.md)（同一内容随匿名包交付）
- [UI字段schema](schema.json)、[导出JSON Schema](export_schema.json)
- [CPU/泄露检查结果](evidence/integrity_report.json)、[保存恢复导出检查](evidence/ui_flow_report.json)

## 本地生成与检查

在本目录运行，Python需Pillow；不需要PyTorch、CUDA或模型。实际已复用缓存，无图片网络下载。

```bash
python scripts/build_review.py
python scripts/check_integrity.py
python scripts/summarize_reviews.py
```

生成器从固定Git blob读取Manifest和180条预测，私有保存原数据关联，仅将原文和原图片字节装入匿名包。重跑使用原private种子；已存在文件若内容不一致即拒绝覆盖，不能靠清理准备目录重建来代替恢复。人审开始后不要改动材料或匿名ID；如必须变更，另行建立版本并保留全部旧结果。

`packages/ReviewerA/index.html` 与 `packages/ReviewerB/index.html` 可分别用浏览器打开。也可只启动一个匿名包的回环服务：

```bash
python scripts/serve_review.py --reviewer ReviewerA --port 8765
```

服务只绑定127.0.0.1，只允许匿名页面、资源与空表，不提供整个仓库、private目录或任意目录列表。按Ctrl-C退出。若服务器无图形界面，优先把各自ZIP下载到审核者本机解压；已有SSH连接也可做本机端口转发。不要把整个worktree、K2审计或private映射发给审核者。

## 分发与回收

协调人将artifacts中的A/B单独ZIP分别交给两位不同人。总ZIP供协调人保存，不应将另一人的答案或私有目录发给审核者。包内无外部网络依赖。

每位审核者交回stage1和stage2各一份final JSON；CSV是替代格式或查看副本，不要把同一阶段的JSON/CSV当两份独立结果同时送入汇总。草稿用独立draft backup JSON恢复；它不是final交回文件。独立性需要协调人现实确认，两个匿名ID并不能证明是两位人类。

```bash
python scripts/summarize_reviews.py \
  --review /path/ReviewerA_stage1_final.json \
  --review /path/ReviewerA_stage2_final.json \
  --review /path/ReviewerB_stage1_final.json \
  --review /path/ReviewerB_stage2_final.json \
  --confirm-independent-humans
```

`--confirm-independent-humans`只能在协调人确认真实独立人类审核后使用；不能拿助手或另一模型顶替。遗漏、重复、未知ID、不同版本混入、草稿、格式错误、阶段冻结回执不一致均保持HUMAN_REVIEW_PENDING，不能选择“最新文件”静默覆盖。未给该确认标志也不关联GT/模型结果。默认无输入时只输出pending，不评价投入门槛。

完整人审后，输出单侧原始一致率（含U与双方可判定分别统计）、左右映射对齐后的配对一致率、分歧和前后阶段变化、与原GT/模型的关联，以及原36对和人审支持对比子集并列指标。保留所有Underdetermined与分母。软件只计算人审标签一致下的模型错误**候选**及计数；不判断理由是否科学可信，不将子集或配对标签对比当严格单因素因果认证。

投入计数条件保持：一般诊断≥4个可信错误、≥2类且有明确人审理由；程序以单侧错误候选计数并另报不同pair数量。11例专门子问题≥6/11仍在请求后果目标下支持Unsafe且对比成立；该子问题要求对应单侧人审与配对中原两侧Safe/Unsafe对比均有一致人审或显式人工裁决支持。任何条件都不是显著性标准；只能供研究者审阅下一阶段建议，永不自动执行GPU。

汇总输出新建带时间/随机后缀的private/summary目录，原始输入按SHA256保存回执；不覆盖来源文件。真实结果仅可写private或results，不允许写网站包目录。

## 分歧与人工裁决

可选 `--adjudications /path/adjudications.jsonl`。每条为人类裁决事件，至少有event_id、human_adjudicator_id、created_at（含时区ISO时间）、rationale、stage、来自private映射的pair_id。单侧事件另有side（safe/unsafe，研究者私有关联）和judgment（Safe/Unsafe/Underdetermined）；配对事件另有contrast_supported（Yes/No/Underdetermined）及judgments对象（safe、unsafe两个原侧别的独立判断）。这不是给审核者的导出格式。

同一键的修订必须用supersedes显式指向上一event_id，否则拒绝汇总；原事件、原分歧及原阶段判断始终保留，不静默取最后一条。不允许从K2筛查自动生成裁决。裁决记录仅存私有目录，不进入Git。

## CPU测试

应用不依赖npm。仅DOM开发测试使用本地jsdom26.1.0，锁文件在tests；依赖在忽略的.tools目录，安装时禁用生命周期脚本，不改全局配置。

```bash
mkdir -p .tools
cp tests/jsdom_package.json .tools/package.json
cp tests/jsdom_package-lock.json .tools/package-lock.json
npm ci --prefix .tools --ignore-scripts
node tests/SYNTHETIC/test_app.cjs
python -m unittest discover -s tests -p 'test_*.py'
```

所有填入的技术测试记录只在tests/SYNTHETIC/generated，含SYNTHETIC标记，真实汇总默认拒绝。DOM测试不是实际浏览器视觉或file://存储策略的跨浏览器认证。生成审核包无任何真实人审填答。

## 私有材料和恢复

private/为0700目录，种子和映射为0600。单独安全备份private、审核包ZIP以及收到的原始人审文件；不要把private压进审核者ZIP、上传Git或当HTTP根。private/RECOVERY.md、private/RESTORE_STEPS.md含恢复说明，private/H1_K3_Private_Recovery.zip为独立协调人恢复备份。

匿名化只降低意外泄露；原文重复、图片识别或故意公开检索仍可能关联样本。阶段二匿名配对资源在本地包内，界面按流程锁定而非加密访问控制，不宣称完全盲法或防篡改系统。图像来源许可未重新认证，默认不公开上传图像。
