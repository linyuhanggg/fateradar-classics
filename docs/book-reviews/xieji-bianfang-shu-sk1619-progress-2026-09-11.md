# 協紀辨方書 · 识典 SK1619 · 语义审读进度 · 2026-09-11

独占文件：`references/annotations/selection/xieji-bianfang-shu--shidian-SK1619.json`（新建）与本进度文档。未改源文 `sources/normalized/shidianguji/SK1619/**`。禁止改主本 `references/annotations/selection/xieji-bianfang-shu.json`，不碰折中、指南、撼龙、青囊、引擎、`chart.*`。

## WORK_PACKAGE_COMPLETE（全量 0–292）

本包索引 **0–292**（293 段）全部有实质处理：`source-reviewed` 293（其中 `待核实` 1），`verified` 全 false。不是协纪辨方书三十六卷全书完成，也不是人工 verified，也不是引擎包；**remaining = 0**（索引口径）。不是主本 `xieji-bianfang-shu.json` 线（MING-156/166/178/186/188/192/194/196 已覆盖主本 0–2398），勿开主本 CP9。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-206`
- 分支：`codex/multica-ming-206`（自权威树 `fateradar-classics-grok-full-library` @ `1fd3a37` 新建）
- `sources/normalized/shidianguji/SK1619/paragraphs.json` SHA256 = `d797791833eac0ba76aac23eaf6a76a1f262de35c02c6826cefb0e50175ca9a2`（293 段；与 Issue 一致）
- `sources/normalized/shidianguji/SK1619/text.md` SHA256 = `ed5986c8460a312efc160a423844ab542d590641dca722b6be6feecc0fc942f7`（与 Issue 一致）
- 既有识典注解差集：交包前该文件不存在 → 新建 primary 全量 293
- 稳定 ID 与 `tools/source_paragraphs.py` 对齐；不 OCR、不抓站
- 网站章节名 ≠ 印本卷号；与主本 `L####` 段落 ID 不同，禁止混写

## 段落账本（293/293）

| 区段 | 索引 | 起讫 paragraphId | 处理摘要 |
|---|---|---|---|
| 御制序 / 四库端 | 0–6 | `xieji-bianfang-shu:shidian-SK1619:P7537536093446045696`–`xieji-bianfang-shu:shidian-SK1619:P7537536093446144000` | 四库行、序题与御制序分段；署乾隆六年十二月望日 |
| 气候 | 7–179 | 气候标题 → 七十二候 / 昼夜 / 朦影 → 卷十二收束 | 候名物与历算表值分层；不作神煞断 |
| 卷十三 / 公规二 | 180–182 | 四库行、卷十三、公规二 | 目录层；本补本仅局部 |
| 更漏中星 | 183–191 | 标题、星图步天歌、图占位、源流、春分立成局部 | 图像占位 `待核实`；立成表值 |
| 夏至後日躔未宫 | 192–284 | 标目 + 贵登天门定局 | 月将/阴阳贵人加临立成；不单面吉凶 |
| 卷三十六 / 辨譌端 | 285–292 | 卷端、辨譌总叙、神煞同位异名及斗首/尊星帝星/神在标目 | 驳俗术口径；标目未收细论不补造 |

- 起始：`xieji-bianfang-shu:shidian-SK1619:P7537536093446045696`
- 本批止：`xieji-bianfang-shu:shidian-SK1619:P7537537497228984354`（索引 292）
- **nextId**：无（全量完成）
- **remaining**：0（索引口径）

## 质量要点

- 禁止模板填白话；序/气候表值/更漏/贵人定局/辨譌分别写实质去向
- 条件、救应、反转、未知分开；`verified` 全 false
- 不与主本 `L####` 混写；不替代主文本投票

### doubtful / unknown（本包 1 处）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `xieji-bianfang-shu:shidian-SK1619:P7537536730670006307` | 185 | `待核实`；识典「此处为图像，未转文字」，保留 unknown，不补造星名度数 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/selection/xieji-bianfang-shu--shidian-SK1619.json --json
```

结果：`ok=true`，`entries=293`，`source_reviewed=293`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书与主本协纪；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成，也不是引擎包；remaining 0 ≠ 人工 verified，不是三十六卷影印校勘完成。
