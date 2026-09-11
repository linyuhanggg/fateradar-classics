# 皇極經世書 · 识典 SK1573 · 语义审读进度 · 2026-09-11

独占文件：`references/annotations/divination/huangji-jingshi--shidian-SK1573.json` 与本进度文档。未改源文 `sources/normalized/shidianguji/SK1573/**`。不碰主本 `huangji-jingshi.json`、HY1521、HY1442、SK1603、DZ1040、指南、chart、引擎、MING-163 审查稿。

## WORK_PACKAGE_COMPLETE（CP2）

本包 CP2 索引 **300–669**（370 段）全部有实质处理：`source-reviewed` 370（其中 `待核实` 1），连同 CP1 共 **670/670**。`verified` 全 false。不是皇极经世全书完成（其他版本/主本未在本包），也不是人工 verified，也不是引擎包。禁止重做索引 0–299（MING-155 CP1）。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-168`
- 分支：`codex/multica-ming-168`（继承 `origin/codex/multica-ming-155` @ `40f17d1dbbb2f76a1bf13f206a8c893e81591046`）
- `sources/normalized/shidianguji/SK1573/text.md` SHA256 = `c101c5a29e96da89e45fdb3b01c879308c74767d1071531e202706c50791e34a`（与 Issue 一致）
- `paragraphs.json` 670 段；稳定 ID 与 `tools/source_paragraphs.py` 对齐
- `catalogComplete: false`；缺章不补造；网站章节名 ≠ 印本卷号核定
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 不 OCR、不抓站
- 禁止重做命海 HY1442、星命溯源 SK1603

## 段落账本（370/370 · CP2；全书累计 670/670）

| 区段 | 索引 | 起讫 paragraphId | 处理摘要 |
|---|---|---|---|
| 观物外篇上（续） | 300–457 | `…P7637911008657833993`–`…P7637911009664188454` | 圆方裁数、运行/生物数、蓍卦体用策数、真数参两、八卦阴阳、律吕开合 |
| 卷十四卷端 | 458–460 | `…P7637911009916059699`–`…P7637911009916092467` | 钦定四库 / 卷题卷十四 / 宋邵雍撰 |
| 观物外篇下 | 461–669 | `…P7637911009916108851`–`…P7637911015330775090` | 太极神数象器、天地日月、五行形质、人物情性、为学至诚；全书末段含卷题 |

- 起始（本包）：`huangji-jingshi:shidian-SK1573:P7637911008657833993`（索引 300）
- 本批止 / 全书末：`huangji-jingshi:shidian-SK1573:P7637911015330775090`（索引 669）
- **nextId**：无（本版 SK1573 段落集已尽）
- **remaining**：0（相对本注解文件 paragraphId 集合）
- 不宣称主本/DZ1040/其他版本完成

### CP1 继承（不重做）

| 区段 | 索引 | 状态 |
|---|---|---|
| 卷端 / 提要 / 以运经世 / 外篇上（起） | 0–299 | MING-155 @ `40f17d1`；本包只读继承 |

## 质量要点

- 禁止模板空白话；外篇上/下分别写实质去向与简短义理 gloss
- 观物外篇标 `理论`（数理/义理，不是占断/预测有效）
- 卷端标 `序跋目录` / 撰人标 `评注或元数据`
- `verified` 全 false；非人工校勘
- 不与 DZ1040 / 主本混写；不替代主文本投票

### doubtful / unknown（本包 1 处）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `huangji-jingshi:shidian-SK1573:P7637911011882680347` | 516 | `待核实`；「月半盈半𧇊」含罕见字形，疑缺/异体，保留 unknown，不补造改正文 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/huangji-jingshi--shidian-SK1573.json --json
```

结果：`ok=true`，`entries=670`，`source_reviewed=670`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包完成识典 SK1573 本文件段落集，不是皇极经世全书/引擎完成。
