# 钦定协纪辨方书（主本）· 语义审读进度 · 2026-09-11

独占文件：`references/annotations/selection/xieji-bianfang-shu.json`（新建 primary）与本进度文档。未改源文 `sources/fulltext/selection/xieji-bianfang-shu/fulltext.md`。不碰 HY1521 / SK1609 / 指南 vol3-4 / 五行精纪 / 引擎 / `chart.*`。不是识典 SK1619。

## WORK_PACKAGE_COMPLETE（CP1）

本包 CP1 索引 **0–299**（300 段）全部有实质处理：`source-reviewed` 300（其中 `待核实` 含疑义/阙文/异说未定），`verified` 全 false。不是协纪辨方书全书完成，也不是人工 verified，也不是引擎包；索引 **300–2398** 留给后续包。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-156`
- 分支：`codex/multica-ming-156`（基线继承 `codex/multica-ming-151` @ `9d54a70`）
- `sources/fulltext/selection/xieji-bianfang-shu/fulltext.md` SHA256 = `64cda81a8534ac784b61d8cdcdb2773a65b10d9fb00fb79ff1561d8901fb340d`（与 Issue 一致）
- 段落清单 `references/inventory/paragraphs/selection/xieji-bianfang-shu.json`（2399 段）；稳定 ID 与 `tools/source_paragraphs.py` 对齐
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 不 OCR、不抓站
- 交包前差集：主本原无 annotation JSON；本包新建，无同版本已交段落可差

## 段落账本（300/300 · CP1）

| 区段 | 索引 | 起讫 paragraphId | 处理摘要 |
|---|---|---|---|
| 御序 / 奏议 / 职名 / 目录 | 0–4 | L0003-L0012–L0297 | 编纂宗旨、进爱奏请、职名、三十六卷目录 |
| 本原一（图书卦画五行纳音纳甲） | 5–66 | L0301–L0599 | 河洛先后天、甲历四序辟卦、五行三合纳音纳甲 |
| 本原二（二十四山洪范游年） | 67–104 | L0603–L0791 | 正/双山/缝针/洪范、墓龙变运、大小游年翻卦 |
| 义例一（岁神） | 105–166 | L0795–L1051 | 岁德太岁三煞等岁神及出游/日游 |
| 义例二（建除月神·厌建） | 167–248 | L1055–L1420 | 建除同位丛辰、月厌不将大小会、厌建诸日 |
| 义例三（天德月德等） | 249–295 | L1424–L1666 | 天道天德月德至鸣吠立成 |
| 卷六起标 | 296–299 | L1670–L1681 | 义例四/三合/驿马/劫煞目录层，正文留给后续 |

- 起始：`xieji-bianfang-shu:L0003-L0012`
- 本批止：`xieji-bianfang-shu:L1681-L1681`（索引 299）
- **nextId**：`xieji-bianfang-shu:L1684-L1684`（索引 300）不在本包
- **remaining**：2099（索引 300–2398；全书 2399 段）
- 全书末：`xieji-bianfang-shu:L12779-L12779` 留给后续包

## 质量要点（节录）

- 引书 / 曹震圭 / 考原 / 编者按语分层；建除统摄丛辰、大小游年同变异名、岁德与岁干合名目重叠等处分条
- 条件、宜忌、反转与未知分开；美恶同位（如枝德与小耗）按用事取用
- 禁止模板填白话；短标记（欽定四庫全書、图题目录）仅作序跋目录/术语
- verified 全 false；非人工校勘

### doubtful / unknown / 待核实（本包）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `xieji-bianfang-shu:L0667-L0679` | 81 | `待核实`；山家五行「未」属与火位数「二说未知孰是」 |
| `xieji-bianfang-shu:L1039-L1047` | 165 | `待核实`；日游神历例「其义未明」 |
| `xieji-bianfang-shu:L0932-L0933` | 139 | `待核实`；蚕命今表考原「此恐有误」 |
| `xieji-bianfang-shu:L1154-L1162` | 191 | `待核实`；魁罡「其义未详」、收日生神「或系阙文」（inventory `missing_marker`） |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/selection/xieji-bianfang-shu.json --json
```

结果：`ok=true`，`entries=300`，`source_reviewed=300`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成，也不是引擎包。
