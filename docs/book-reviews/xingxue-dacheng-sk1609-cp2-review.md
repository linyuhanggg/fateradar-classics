# 星學大成 · 识典 SK1609：独立审查 CP2（300–397）

审查对象：`origin/codex/multica-ming-135` @ `3b578879499082cc67d9eb12ed7c9efb54515bd1`（父 `8def9f05e75e98d8e7594780f836f02f252023c0`，即 MING-123 CP1 / MING-137 已过钉死点）。工作树只读参考 `fateradar-multica-ming-135`，本岗写出仅本文件。未改注解 JSON、未改源文、未改主本 `xingxue-dacheng.json`、未改 SK1602 / SK1605 / 三命 HY1521 / 六壬 / `geju-transit*` / chart。不是星學大成三十卷全帙完成，也不是全项目完成。不重做 CP1（0–299）。

结论：**通过。** 交包结构账本与抽样语义成立；`source-reviewed` 不是人工 `verified`；电子阅读不是影印校勘。下列 caveat 不构成本包失败，也不把 draft 升 verified。本岗未改注解。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-150`，2026-09-11）：

```
git fetch origin codex/multica-ming-135
git rev-parse HEAD origin/codex/multica-ming-135
git ls-remote origin refs/heads/codex/multica-ming-135
git diff 8def9f0..3b57887 --name-only
shasum -a 256 sources/normalized/shidianguji/SK1609/text.md
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-135` | `3b578879499082cc67d9eb12ed7c9efb54515bd1`（本地 HEAD / 跟踪 / `ls-remote` 一致） |
| 父提交（CP1 钉死） | `8def9f05e75e98d8e7594780f836f02f252023c0` |
| 相对 CP1 文件 | 仅 2 个：`references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json`、`docs/book-reviews/xingxue-dacheng-sk1609-progress-2026-09-11.md` |
| diffstat | `+2165 / -22`（注解扩展 + 进度更新） |
| 源 `text.md` SHA256 | `0d0f3106f2865b4e4b2f10a9c9433785b6009575b53105bbf8718dde48ffa948`（与 Issue / 进度一致；本提交未改源层） |
| `provenance.json` `sourceStatus` | `reference-text` |
| `catalogComplete` | `false`（`missingChapters` 938 条，未补造） |
| 0–299 对象级比对 | 与 CP1 `8def9f0` 注解文件前 300 条 **完全相同**（`mismatch=0`） |
| 源文 / 主本 | `git diff 8def9f0..3b57887` 不含 `SK1609/**` 与主本 `xingxue-dacheng.json` |

无越权文件。源层未改。主本未覆盖、未把主本 vernacular 整段复制进识典（CP2 与主本白话精确重叠 = 0）。`relatedParagraphIds` 全部落在全书 398 条内；索引 300 回指 CP1 止点 299，衔接正确。

## 2. 校验器独立复跑

对 `3b57887` 树（本岗从该 commit 检出的独立副本，非 ming-135 活树）：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/xingming/xingxue-dacheng--shidian-SK1609.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 398, "source_reviewed": 396,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

与交包宣称 `ok=true entries=398 source_reviewed=396 errors=[]` 一致。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

全书 398 条：`verified` 全 `false`。`review=draft` 共 2 处（CP1 遗留 1 + CP2 本包 1）：

| 索引 | paragraphId 尾 | 范围 | 源要点 | 判定 |
|---|---|---|---|---|
| 6 | `P7430056317387145267` | CP1（已过，未改） | 版面无字 | 保持 draft，未升 sr/verified |
| 359 | `P7640428574264541234` | **CP2** | 源仅「闕」（L1133） | 白话「不补造格局或诗句」；保持 draft，未升 sr/verified |

CP2 切片 300–397（98 段）：`source-reviewed` 97，`draft` 1，`verified` 全 false。本包 `figureCount>0` 为 0。terms 空 0/98。白话无空、无互重复。

kind（CP2）：规则候选 94、术语 3、待核实 1。

## 4. 索引边界

`paragraphs.json` 全书 398 段；CP2 必须从索引 300 起，止 397。进度文档已纠正 CP1 审查 caveat 中的 nextId 错指：现写起始 `P…3405200422`、止 `P…4265163826`，**nextId 无**（识典注解包已齐），remaining 0。

| 位置 | 实测 ID |
|---|---|
| 注解索引 299（CP1 止，未改） | `xingxue-dacheng:shidian-SK1609:P7640428573405184038` |
| 注解索引 300（CP2 起） | `xingxue-dacheng:shidian-SK1609:P7640428573405200422` |
| 注解索引 359（CP2 draft 阙） | `xingxue-dacheng:shidian-SK1609:P7640428574264541234` |
| 注解索引 397（CP2 / 全书末） | `xingxue-dacheng:shidian-SK1609:P7640428574265163826` |

网站章节仍为「論輕耀」。不得把全书末 ID 再写成下一包起点——本识典包已无下一索引。

## 5. 抽样语义（≥15，对照原文，不凭进度摘要）

原文取 `sources/normalized/shidianguji/SK1609/text.md` 的 `start_line–end_line`。未发现「本段论述 / 白话从略 / 见原文 / 待补」类空模板；无把整段原文粘进 vernacular 冒充处理；无只写「续」的空截。吉凶同条、截断不补、阙不补造均成立。

| 索引 | 尾 ID | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 300 | `P…5200422` | 规则 / sr | L938「土星天吏爲扶引，東岳生儲活世人。」接 CP1 火月局；不补前缺句 | 通过 |
| 301 | `P…` | 规则 / sr | L940 二交身命好精神→王侯将相；身命定位 | 通过 |
| 305 | `P…` | 规则 / sr | L948 罗孛台元土同、二交临照四宫 | 通过 |
| 306 | `P…` | 规则 / sr | L950 火星会月居闲极：权豪而少富丰——两向并存 | 通过 |
| 321 | `P…` | 规则 / sr | L980 截断于「鎡基」；白话标明电子源截断、不补后文 | 通过 |
| 322 | `P…` | 规则 / sr | 续截「此中不可安」；中限灾迍，不因前句富贵删忌 | 通过 |
| 330 | `P…` | 规则 / sr | L998 不逢紫炁相挠才达侯门；有挠不取 | 通过 |
| 336 | `P…` | 规则 / sr | L1010 资财破散兼伤祖伤身；有财不删凶 | 通过 |
| 337 | `P…` | 术语 / sr | L1012–1014 标目金木水火土·孛月；子辰申火土孛条件 | 通过 |
| 340 | `P…` | 规则 / sr | L1022–1028 水炁关照朱紫；依豪富身贫困同旨保留 | 通过 |
| 341 | `P…` | 规则 / sr | L1030–1033 后刑先贵；福宫金计反向 | 通过 |
| 348 | `P…` | 规则 / sr | L1065–1069 文星有无分途：无文星偏钱谷 | 通过 |
| 349 | `P…` | 规则 / sr | L1071–1074 日月火同+陷宫+月弱→不善终 | 通过 |
| 352 | `P…` | 规则 / sr | L1090–1093 金木文章 vs 水火错恶疾两向 | 通过 |
| 353 | `P…` | 规则 / sr | L1095–1104 第一格/帅师 vs 木孛沉溺穷尽对读 | 通过 |
| 355 | `P…` | 规则 / sr | L1111–1116 两府横金；不学亦挂紫衣与勤学分读 | 通过 |
| 358 | `P…` | 规则 / sr | L1128–1131 火孛刚强忌淫荒 vs 聚交丰财两层 | 通过 |
| 359 | `P…4541234` | 待核实 / draft | L1133 仅「闕」；不补造 | 通过 |
| 360 | `P…` | 规则 / sr | L1135 铨衡封侯；前阙不连补 | 通过 |
| 361 | `P…` | 规则 / sr | L1137–1142 播九州 vs 荣华寿不高；烦冗格保留 | 通过 |
| 370 | `P…` | 规则 / sr | L1187 福星沉溺转学问文声，不取官禄厚 | 通过 |
| 397 | `P…5163826` | 规则 / sr | L1263–1272 武僚/状元/贵无伦/优游分档，不混一断；CP2 止 | 通过 |

关键条件与源行（抽核）：

- CP2 起句土星天吏：L938
- 权豪少富：L950
- 「鎡基」截断不补：L980
- 紫炁相挠忌：L998
- 破财伤祖伤身：L1010
- 先贵后刑 / 福宫金计：L1030–1033
- 不善终（陷宫+月弱）：L1071–1074
- 水火错恶疾：L1090–1093
- 高强/沉溺对读：L1095–1104
- 阙：L1133
- 荣华寿不高：L1137–1142
- 沉溺转文声：L1187
- 收束多格分档：L1263–1272

## 6. source-reviewed ≠ 人工 verified

识典补本 `sourceStatus=reference-text`。CP2 97 条电子语义阅读升 `source-reviewed`，只表示对照电子段落实了层次/条件/救应/反转/未知去向，不是影印逐字校勘，也不是预测有效证据。补本不替代主文本 `xingxue-dacheng.json`，不计独立投票。不得把 396 条累计 source-reviewed（含 CP1）写成已人工 verified。识典 398 段注解已齐 ≠ 三十卷全帙，也不是产品交付。

## 7. 质量账本（只记录，不回改）

| 账本项 | 独立实测 | 处理 |
|---|---|---|
| CP2 draft | 1/98，仅索引 359「阙」 | 不升 sr/verified |
| CP1 0–299 | 相对 `8def9f0` 对象级未改 | 不重做 |
| 截断句 | 321–322「鎡基 / 此中不可安」标明不补 | 不回改 |
| 吉凶同条 | 306 权豪少富、336 破散伤祖、341 先贵后刑、353 沉溺对读、361 寿不高 等 | 反向保留成立 |
| 进度 nextId | 已改为「无」；起止 ID 正确指向 300 / 397 | CP1 caveat 已消化；不回改 |
| 主本 | diff 未触；白话无整段复制 | 通过 |

## Caveat（不改注解，留给后续若有新包）

1. **识典注解包已齐**：398/398。后续不得重做 0–397；新范围须新 Issue。
2. **索引 359 阙**：保持 draft。不补造。
3. **电子截断**（如「鎡基」）：不补后文成立；接入规则库前须对照他本/邻段，不能当完整公式。
4. **网站章节名 ≠ 印本卷号**：論輕耀是网站章。引用以段落 ID 为准。缺章见 provenance，未补造。
5. **口授心授 / 字形异文 / catalogComplete=false**：一律 unknown/draft 路径，不升 verified。

## 未决（本岗不施工）

- 索引 6、359 保持 draft。
- 识典待校、缺章、图像/版面，不升 verified。
- 主本 `xingxue-dacheng.json` 不在本包范围；识典审完不等于星學大成全书完成。
- 本审查不把任何条目标成人工 verified。

## 本岗范围

只新增本文件。审查分支 `codex/multica-ming-150`。
