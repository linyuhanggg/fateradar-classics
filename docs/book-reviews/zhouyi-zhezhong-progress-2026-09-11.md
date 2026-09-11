# 御纂周易折中 · 语义审读进度 · 2026-09-11

独占文件：`references/annotations/divination/zhouyi-zhezhong.json`（新建 primary）与本进度文档。未改源文 `sources/fulltext/divination/zhouyi-zhezhong/fulltext.md`。不碰 HY1521 / SK1609 / SDZJ0170 / 六壬大全秘本 / 指南 vol3-4 / 五行精纪识典 / 引擎 / `chart.*`。

## WORK_PACKAGE_COMPLETE（CP1）

本包 CP1 索引 **0–299**（300 段）全部有实质处理：`source-reviewed` 300（其中 `待核实` 1），`verified` 全 false。不是御纂周易折中全书完成，也不是人工 verified，也不是引擎包；索引 **300–1621** 留给后续包。

## 源核

- worktree：`/Users/yuhanglin/.codex/worktrees/fateradar-multica-ming-151`
- 分支：`codex/multica-ming-151`（基线继承 `codex/multica-ming-133` @ `1967145`）
- `sources/fulltext/divination/zhouyi-zhezhong/fulltext.md` SHA256 = `9243167aa893f7c85baf8b5fdd37e300341b6b94b70a60efd96cd0d89b607a26`（与 Issue 一致）
- 段落清单 `references/inventory/paragraphs/divination/zhouyi-zhezhong.json`（1622 段）；稳定 ID 与 `tools/source_paragraphs.py` 对齐
- 电子语义阅读升注解 `source-reviewed`，不等于影印校勘或人工 verified
- 不 OCR、不抓站

## 段落账本（300/300 · CP1）

| 区段 | 索引 | 起讫 paragraphId | 处理摘要 |
|---|---|---|---|
| 御制序 / 引用姓氏 / 职名 / 提要 | 0–5 | L0003-L0007–L0315 | 纂修宗旨、征引名录、馆职、四库提要；BOM 空白行单列元数据 |
| 凡例 | 6–7 | L0319–L0337 | 以本义为主、经传次第与纲领体例 |
| 卷首纲领与义例 | 8–15 | L0341–L0599 | 纲领一–三；时/位/德/卦主通例 |
| 卷一上经（乾起） | 16–74 | L0603–L1034 | 乾坤及后续卦爻本义·程传·集说 |
| 卷二 | 75–130 | L1038–L1419 | 续上经卦爻分层注 |
| 卷三 | 131–199 | L1423–L1853 | 续上经至卷末标记 |
| 卷四 | 200–270 | L1857–L2300 | 续至下经交接前 |
| 卷五下经起（咸/恒/遯/大壮初） | 271–299 | L2304–L2488-L2489 | 咸至大壮初九；恒彖辞 doubtful 保留 unknown |

- 起始：`zhouyi-zhezhong:L0003-L0007`
- 本批止：`zhouyi-zhezhong:L2488-L2489`（索引 299）
- **nextId**：`zhouyi-zhezhong:L2493-L2502`（索引 300）不在本包
- **remaining**：1322（索引 300–1621；全书 1622 段）
- 全书末：`zhouyi-zhezhong:L10774-L10774` 留给后续包

## 质量要点（节录）

- 条件/救应/反转/未知分开：如屯九五「小贞吉大贞凶」、咸六二「动凶静吉」、大过九五象占与九二相反、遯「小利贞」小人/大小异读等分条
- 本义占辞、程传义理、集说诸家、案语折中分层，不把集说升为已定单面断
- 禁止模板填白话；短标记（欽定四庫全書、卦画〔…〕、周易上下经）仅作序跋目录
- verified 全 false；非人工校勘

### doubtful / unknown（2 处 inventory，本包 1 处）

| paragraphId | 索引 | 处理 |
|---|---|---|
| `zhouyi-zhezhong:L2376-L2378` | 281 | `待核实`；集说「古字作□」缺字保留 unknown，不补造；义理层可读处已摘，不作可执行断法 |
| `zhouyi-zhezhong:L10604-L10621` | 1587（非本包） | 四象相交为十六事图；留给后续包，同样不补造 |

## 校验

```text
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/divination/zhouyi-zhezhong.json --json
```

结果：`ok=true`，`entries=300`，`source_reviewed=300`，`errors=[]`。校验器只做结构与 ID，不是语义证书。

## 边界

不 OCR、不抓站、不改其他书；不 main 合并/部署/force push。电子阅读 ≠ 预测有效。本包不是全书完成，也不是引擎包。
