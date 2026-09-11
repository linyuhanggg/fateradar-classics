# 大六壬秘本：独立审查 CP4 博戏 vern 错位修复（L5920–L5926）

审查对象：`origin/codex/multica-ming-397` @ `6f9ae5139f3a1cdd6e26496a12f0961e8ff5cdc6`。对照基线 `origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`。缺陷出处 [MING-389](mention://issue/01a09165-503b-7b84-8763-9f6958918ce7) 审查稿 `docs/book-reviews/liuren-miben-cp4-review.md` @ `e62980e0eeb29f656903f1db641f5352b61706b5`。生产交包 [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18)。工作树 `fateradar-multica-ming-403` / 分支 `codex/multica-ming-403`。本岗未参与 [MING-397](mention://issue/01a0916e-7db8-7309-afdf-18d41be13a18) 修复，未改注解 JSON，未改 CP4 原稿，未抢 [MING-401](mention://issue/01a09171-2869-79d4-90a0-fa858264cd5e) CP7 审查稿。

结论：**本包范围内通过。** 相对 329 仅 `liuren-miben.json`；语义差集仅 4 条；MING-389 具名错位链已按 paragraphId 解开；validator `ok=true` entries=2643；verified 全 false。`source-reviewed` ≠ 人工 `verified`。不宣称全书完成。

## 1. 指针与越权核验

独立命令（本岗树 `fateradar-multica-ming-403`，2026-09-12）：

```
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-397 refs/heads/codex/multica-ming-329
git diff --name-status 6effd8e4f951fd17e1b1e0454942946ebc765da9 HEAD
shasum -a 256 references/annotations/san-shi/liuren-miben.json
shasum -a 256 sources/fulltext/san-shi/liuren-miben/fulltext.md
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
```

结果：

| 项 | 实测 |
|---|---|
| 本地 HEAD / 对象 | `6f9ae5139f3a1cdd6e26496a12f0961e8ff5cdc6` |
| `origin/codex/multica-ming-397` | `6f9ae5139f3a1cdd6e26496a12f0961e8ff5cdc6`（与 Issue 钉死 SHA 一致） |
| 基线 `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9` |
| 相对 329 文件差 | 仅 `M references/annotations/san-shi/liuren-miben.json` |
| 注解 JSON SHA256 | `2789a72972a3a1521ae2d0dfa5179e8b6affd92189445064419d1cf4414ad347`（与 Issue / 397 交包一致） |
| 基线 JSON SHA256 | `30b9b2b915089ead2c54bf88999131b4e7558097d996453fc27bf135d3054821` |
| 全文 `fulltext.md` SHA256 | `3152e2446147976fe65e81483c0fd4a47c02500d35aa547cd4356c9200cd68b3`（与 MING-389 记录相同；本修复未动全文） |
| `bookSlug` / `sourceTitle` / `scopeNote` | 与基线全等 |
| 本岗写出 | 仅本文件 |

无越权文件。未触碰注解 JSON、CP4–CP7 审查稿、大六壬大全 / 识典、fulltext。

## 2. 差集：仅 4 条，其余 2639 条全等

独立加载基线与对象 JSON，按 `paragraphId` 深比较：

| 项 | 实测 |
|---|---|
| entries | 2643 / 2643；ID 序列全等；唯一 ID 2643 |
| 内容不等的条目 | **恰好 4 条**：索引 1189–1192 |
| 其余条目 | **2639 条逐字段全等** |
| 4 条改动字段 | `L5920` vern+notes；`L5922` vern+notes；`L5924` vern+notes；`L5926` 仅 vern（notes 未改） |
| 4 条未改字段 | `kind` / `terms` / `review` / `verified` 均与基线相同 |
| 邻段 | `L5916` / `L5918` / `L5928` / `L5930` 与基线全等 |

与 MING-389 具名失败 ID 一一对应，未见扩改 CP4 其余条目，未见重做 0–899。

## 3. 校验器独立复跑

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/san-shi/liuren-miben.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 2643, "source_reviewed": 2554,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

`review` 计数仍为 source-reviewed 2554 + draft 89（与基线相同，draft 未升 SR）。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 4. verified 未越权提升

| 项 | 实测 |
|---|---|
| 全书 `verified` | 2643 / 2643 = `false` |
| 本 4 条 `verified` | 全 `false`（修复前后均 false） |
| 本 4 条 `review` | 全 `source-reviewed`（未升、未降） |
| draft | 89 处保持 draft，未见升 SR |

## 5. 四条 vern 与原文按 paragraphId 对齐

原文取 `sources/fulltext/san-shi/liuren-miben/fulltext.md` 对应行（电子主文本，非影印）。MING-389 失败链：`L5920` 尾句误入 `L5922`；`L5922` 源误入 `L5924`；`L5924` 后半误入 `L5926`。

### 5.1 对齐表

| paragraphId | 源行要点 | 基线 vern（错位） | 修复后 vern | 判定 |
|---|---|---|---|---|
| `L5920-L5920` | 「年上吉神雖立勝，遭彼凶神克也輸。三人以上皆詳此只看行年上立」 | 仅前句；尾句缺失 | 前句+尾句均回本条；释「吉神被克仍输」「多人仍各看行年」 | **通过** |
| `L5922-L5922` | 「同年主客以乘除如二人同年，即看主客」 | 全文是上条「三人以上…」 | 仅同年主客；「同年才改主客」 | **通过** |
| `L5924-L5924` | 「先起為客應為主，客是乾兮主是支。支干上下言凶吉，克處之時使可為」 | 叠入上条「同年主客…」；后半缺失 | 前后半均回本条；去掉同年前缀 | **通过** |
| `L5926-L5926` | 「對敵從何推勝負…龍常旺相並難爭」 | 叠入上条「支干上下言凶吉…」 | 去掉前缀污染；对敌/择强/龙常旺相仍在 | **通过** |

特征短语落点（修复后，仅本条，不再出现在邻条 vern/notes）：

| 短语 | 落点 |
|---|---|
| 「三人以上」「遭彼凶神」 | 仅 `L5920` |
| 「同年主客」「二人同年」 | 仅 `L5922` |
| 「先起为客」「支干上下言凶吉」 | 仅 `L5924` |
| 「对敌从何」「龙常旺相」 | 仅 `L5926` |

邻段抽核：`L5916` 博戏三传吉将、`L5918` 两人行年吉凶将对克、`L5928` 占近出标题、`L5930` 出门时加日支——均仍绑本行，未见错位链再滑一格。

### 5.2 错位链已解开

CP4 索引 900–1199 启发式：本条源文前 8 个汉字出现在下条 vern → **0 条**。MING-389 所记「本条源首句出现在下条 vern」链在本对象上不再成立。

## 6. Caveat（不改注解，不构成本包失败）

1. **`L5924` 源作「客是乾兮主是支」， vern 作「客是干兮主是支」**：电子源用「乾」，白话按干支对读写成「干」，notes「先起为客＝干，主＝支」。此读法已在基线错位稿中存在，本修复只是把该句搬回本条，未新造。不视为错位复现，也不升 verified。
2. **电子阅读 ≠ 影印校勘 ≠ 预测有效**。本 4 条仍 `source-reviewed` / `verified=false`。
3. **CP4 其余条目 / 索引 1200–2642 不在本包**。MING-389 其余 caveat（15 条 draft 疑字等）不因本修复消失。
4. 校验器 `ok` 不是语义证书。

## 7. 质量账本

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| 对象 commit / JSON SHA | `6f9ae513` / `2789a729…` | 与 Issue 钉死一致 |
| 基线 commit / JSON SHA | `6effd8e4` / `30b9b2b9…` | 一致 |
| 文件差 vs 329 | 仅 `liuren-miben.json` | 通过 |
| 条目差 | 仅 4 条；其余 2639 全等 | 通过 |
| validator | `ok=true` entries=2643 sr=2554 errors=[] | 结构通过 |
| verified | 全书 2643 false | 未越权提升 |
| 四条对齐 / 错位链 | 按 paragraphId 解开；CP4 源首句漏入下条 = 0 | **本包通过** |
| remaining | 索引 1200–2642 仍 1443；全书未完成 | 不是全书完成 |

## 未决（本岗不施工）

- 不改注解 JSON。
- 不把任何条目标成人工 verified。
- 不宣称大六壬秘本全书 / 引擎 / 产品完成。
- CP4 其余审查结论仍以 MING-389 稿为准；本文件只覆盖这 4 条修复。
- remaining 1443 交后续 CP。识典补本不得与主文本混计。
- `L5924`「乾/干」对读保留 caveat，不回改。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-403`。对象 commit `6f9ae5139f3a1cdd6e26496a12f0961e8ff5cdc6`。
