# 六壬指南 · 张洪注本 vol3-4（golla 对照层）语义审读进度 · 2026-09-11

独占文件：`references/annotations/san-shi/liuren-zhiyin--annotated-vol3-4.json` 与本进度文档。未改大全/秘本、HY1521、引擎 `liuren*`、`chart.*` 或九宗门主文。未改源文 `sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md`。

## WORK_PACKAGE_COMPLETE（差集续包 · 继承 corpus-2 后）

本包在 corpus-2 已有 **1500** 条 source-reviewed（首 `L0003` 尾 `L3003`）之上，只注解差集中严格晚于 `L3003-L3003` 的段落 **300/467**。`verified` 全 false。不是六壬指南全书完成，也不是人工 verified。MING-136 CP1 产物不计入本包 remaining；禁止重写 0–1499 / L0003–L3003。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-158`
- 分支：`codex/multica-ming-158`（基线继承只读 corpus-2 @ `c86a06e`，源 hash 一致）
- `sources/fulltext/san-shi/liuren-zhiyin/supplemental-annotated-golla-vol3-4.md` SHA256 = `2d03b731c84ad3a0f26c02bd1a3bdac860e7984632136c203d3daf4bc85012ae`
- edition `annotated-vol3-4` 共 **1967** 段；差集 **467**；本包处理后文件 entries=**1800**
- 本层为 golla 补缺对照，含注者重编、张注、后加史注与增补课例，不能冒充陈公献未注原典
- 电子语义阅读升 `source-reviewed`，不等于影印校勘或人工 verified

## 段落账本（300/300 · 差集续）

| 区段 | 本包序 | 起讫 paragraphId 尾 | 处理摘要 |
|---|---|---|---|
| 占验三张注续 | 0–7 | L3005–L3019 | 初攻末守、忌临畏地、戌城刑冲、内奸偷降、交车合/铸印冲破；勾陈屠城放狱存疑 |
| 兵占验四至十三 | 8–101 | L3021–L3207 | 金兵东下、姜瓖乱、武昌、扬城、真定、勤王、泽州、南都、东省、岁内兵警；盘式挂本课；清史稿/明史后加注 |
| 三合章第三十 | 102–113 | L3209–L3231 | 三合歌诀与断法提醒；golla 潍坊现代占例（错课正断） |
| 神煞指南 | 114–299 | L3233–L3604 | 全图读法、岁/月/日煞表行与义例；天目宅例与雨煞现代例；盘式残行挂本例 |

- 继承止：`liuren-zhiyin:annotated-vol3-4:L3003-L3003`（corpus-2，未改）
- 本批起：`liuren-zhiyin:annotated-vol3-4:L3005-L3005`
- 本批止：`liuren-zhiyin:annotated-vol3-4:L3604-L3604`
- **nextId**：`liuren-zhiyin:annotated-vol3-4:L3606-L3606`
- **remaining**：167（差集 467−300；全书对照层仍 1967，已注 1800）

## 质量要点（节录）

- 禁止覆盖已有 1500 条 SR；首 1500 与 corpus-2 字节级一致
- 盘式残行带本课/本例标签与可见天将干支六亲，`relatedParagraphIds` 挂起例
- 张注 / golla 史地注 / 现代增补课例保留 `sourceAttribution`，不并称陈公献原断
- 条件/救应/反转（旺气内外、贵德消祸须其余地方吉、交车合却冲破等）分向记
- `verified` 全 false；电子阅读 ≠ 预测有效

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-zhiyin--annotated-vol3-4.json --json
```

结果：`ok=true`，`entries=1800`，`source_reviewed=1800`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改九宗门/大全/秘本/引擎/chart；不 main 合并/部署/force push。本包不是六壬指南全书完成。
