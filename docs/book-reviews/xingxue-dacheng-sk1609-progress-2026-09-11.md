# 星學大成 · 识典 SK1609 语义审读进度 · 2026-09-11

独占文件：`references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json` 与本进度文档。未改主本 `xingxue-dacheng.json`，不碰 SK1602/MING-114、SK1605/MING-102/MING-107、三命 HY1521/MING-98、李虛中 SK1601、六壬主文、`geju-transit*`、`chart.*` 或共享 core。未改源文 `sources/normalized/shidianguji/SK1609/**`。未把主本注释复制进识典。

## WORK_PACKAGE_COMPLETE（CP2）

本包 CP2 索引 **300–397**（98 段）全部有实质处理：`source-reviewed` 97，`draft` 1（阙文），`verified` 全 false。承 MING-123 CP1 @ `8def9f0`（0–299 未重做）。不是星學大成三十卷全书完成，也不是人工 verified；识典全书 398 段注解已齐，仍非主本全帙。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-135`
- 分支：`codex/multica-ming-135`（基线继承 `origin/codex/multica-ming-123` @ `8def9f0`）
- `sources/normalized/shidianguji/SK1609/text.md` SHA256 = `0d0f3106f2865b4e4b2f10a9c9433785b6009575b53105bbf8718dde48ffa948`（与队列一致）
- 源层 `sourceStatus=reference-text`；`catalogComplete=false`（缺章见 provenance，未补造）
- 网站章节名不等于印本卷号；识典补本不替代主本、不作独立投票证据
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified

## 段落账本（98/98 · CP2；累计 398/398）

| 区段 | 索引 | 起讫 paragraphId 尾 | 处理摘要 |
|---|---|---|---|
| 论轻耀续·二交火土孛等 | 300–336 | P…3405200422–P…4152081458 | 接 CP1 火月局；二交身命/四宫/南北；中限灾迍与截断句不补；奴仆奔波、依豪富身贫、紫炁相挠、金炁相刑、寅申破散等反向保留 |
| 五星四余标目诗格 | 337–348 | P…4152097842–P…4152278066 | 金木水火土/炁·孛月计月罗月多局；先贵后刑、损亲、文星有无分途 |
| 二交专题长段 | 349–358 | P…4152294450–P…4264524850 | 日月陷宫不善终；金水土火月文武分途；木火土孛第一格/帅师/沉溺穷尽对读 |
| 阙 + 后续二交 | 359–396 | P…4264541234–P…4265147442 | 阙保持 draft；铨衡封侯起；烦冗寿不高；金将水文；沉溺转学问；赐紫着绯/富翁分档 |
| 收束多格 | 397 | P…4265163826 | 武僚/状元/贵无伦/优游分档；CP2 止 |

ID 前缀：`xingxue-dacheng:shidian-SK1609:`。

- 起始：`xingxue-dacheng:shidian-SK1609:P7640428573405200422`（索引 300）
- 本批止：`xingxue-dacheng:shidian-SK1609:P7640428574265163826`（索引 397）
- **nextId**：无（识典 398 段已齐）；后续若开包须新范围/新 Issue，不得重做本文件已审段
- **remaining**：0（本识典注解包）

## 质量要点（节录）

- 吉凶同条：权豪少富、依豪富身贫、先贵后刑、荣华寿不高、沉溺转文声
- 高强与沉溺对读（木火土孛）；水火错则恶疾
- 电子截断「鎡基」不补字；「阙」不补造
- 禁止模板填白话；未改 0–299

疑文/未决：口授心授细节未知；缺章不补造；图像/版面不补字；已亥/己亥等字形不改正文；catalogComplete=false。

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json --json
```

结果：`ok=true`，`entries=398`，`source_reviewed=396`，`errors=[]`（draft=2：CP1 版面 + CP2 阙）。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成。
