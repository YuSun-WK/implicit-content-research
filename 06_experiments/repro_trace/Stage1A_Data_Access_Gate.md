# TRACE-S1A · FHM 入场

**G1 `MANUAL_DATA_ACTION_REQUIRED`。G3 作者两列 Caption `BLOCKED`。**

按 S1A 规范复查授权项目工作区、既有报告中的项目共享目录以及预期入场目录。文件名筛查未发现可确认的 FHM 图像、官方 JSONL、合并数据或作者两列 Caption。对三个项目归档仅扫描目录索引，没有解压归档、访问未授权目录或下载 FHM。按文件名筛查无法识别任意改名或嵌套数据。逐 split 计数保留为未知。 [统计证据](stage1a_data_summary.json)

| Split | JSONL | ID、图像、标签、原始文字 | 作者 InternVL / Gemini |
|---|---|---|---|
| train | 未确认 | 未知 | 未找到 |
| dev_seen | 未确认 | 未知 | 未找到 |
| dev_unseen | 未确认 | 未知 | 未找到 |
| test_seen | 未确认 | 未知 | 未找到 |
| test_unseen | 未确认 | 未知 | 未找到 |

## 需要用户完成

1. 登录或注册 DrivenData。在 Hateful Memes 页面按许可页指引点击 **Compete**，本人核对并接受 Competition Rules 和 Dataset License Agreement。直接进入 **Data Download** 可返回登录页。登录后的下载资格和按钮可见性由账户决定。 [官方数据许可](https://www.drivendata.org/competitions/64/hateful-memes/page/214/) · [官方 Data Download](https://www.drivendata.org/competitions/64/hateful-memes/data/)
2. 从账户获准访问的下载页取得官方归档，解压到仅项目授权人员可访问的服务器目录，例如 `~/data/trace-assets/fhm/`。配置的 `image_root` 应是包含 `img/` 和 split 文件的那层目录。保留原始文件名和路径。资料说明 Train/Dev 含标签，竞赛 Test 通常不发标签。仅登记实际标签状态，本轮无测试评分。 [官方字段与 Split](https://www.drivendata.org/competitions/64/hateful-memes/page/206/)
3. 诊断模式到此即可走输入验收。若要启用严格模式，经授权渠道取得作者实际使用的 InternVL 与 Gemini 文件及来源记录，再按 ID、split 和相对图片路径与官方文字及标签交叉核对。自行生成的 Caption 和 `No caption` 等占位值皆不能满足此门禁。固定上游公开树未附这两列完整原件。 [固定官方代码](https://github.com/surrey-nlp/TRACE/tree/83ecb799f897fe275185e082ee9a669f7d04bfaa)

传入原始 split JSONL 时，包装层只从指定 split 文件补入缺失的 `split` 字段，原始 ID、图片引用和文本保持原值。冲突 split 被拒绝。清单支持分别统计缺图、非法路径、解码失败、编号错配、重复 ID、原始和生成 Caption 覆盖。文件中的 Caption 列名、非空比例和哈希都无法单独证明作者来源，需核对来源记录并在私有配置中确认。两个模式均只接受有授权及完整图文标签的 Train 和所选 Dev，并阻止 Train 与已给定的 held-out split 共用样本 ID 或解析后的图片路径。其他 Dev split 之间的重复仅作报告，官方说明两份 Dev 有部分重叠。
