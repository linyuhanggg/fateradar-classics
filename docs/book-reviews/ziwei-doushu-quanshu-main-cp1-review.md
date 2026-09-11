# 紫微斗数全书·主本：独立审查 source-reviewed CP1（0–299）

审查对象：`origin/codex/multica-ming-329` @ `6effd8e4f951fd17e1b1e0454942946ebc765da9`（主本 blob 与 ming-360 / ming-369 全等）。工作树 `fateradar-multica-ming-376` / 分支 `codex/multica-ming-376`。本岗写出仅本文件。未改注解 JSON、未改 `sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md`、未改识典 `ziwei-doushu-quanshu--shidian-SDZJ0170.json` / progress、未改五行精纪抽样、未改引擎 / chart。本岗未参与紫微主本生产。不是紫微斗数全书完成，也不是引擎包，也不是全项目完成。

结论：**通过。** 交包结构账本与 ≥15 段非模板抽样语义成立；`source-reviewed` 不是人工 `verified`；维基文库电子主文本不是影印校勘。下列 caveat 不构成本包失败，也不把任何条升 verified。本岗未改注解。索引 300–1980 remaining **1681** 不在本包。

## 1. 越权与指针

独立命令（本岗树 `fateradar-multica-ming-376`，2026-09-12）：

```
git fetch origin codex/multica-ming-329
git rev-parse HEAD
git ls-remote origin refs/heads/codex/multica-ming-329
shasum -a 256 references/annotations/ziwei/ziwei-doushu-quanshu.json
shasum -a 256 sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md
git rev-parse HEAD:references/annotations/ziwei/ziwei-doushu-quanshu.json
git status --short references/annotations/ziwei/ziwei-doushu-quanshu.json
```

结果：

| 项 | 实测 |
|---|---|
| `origin/codex/multica-ming-329` | `6effd8e4f951fd17e1b1e0454942946ebc765da9`（本岗 HEAD 与 `ls-remote` 一致） |
| 注解 JSON SHA256 | `cac7081253c0a90fa849bf037d816f07b0894fa974a4946a1ad903babb79e66d`（与 Issue 钉死一致；与 ming-360 / ming-369 主本 blob 全等） |
| 注解 blob | `0ac9fcb2c1aa75768849a48c332c6658435f1940` |
| 源 `fulltext.md` SHA256 | `43878728942e9a6ce3b5d94f9825f8fbed83c8b514fda4877acccc4452059824` |
| `sourceFile` / inventory `fulltext` | `sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md` |
| `bookSlug` | `ziwei-doushu-quanshu` |
| `scopeNote` | 对照维基文库三卷电子本；明确 source-reviewed ≠ 影印校勘 / 专家认证 / 预测有效 |
| 工作区注解 JSON | `git status --short` 空（本岗未改） |
| 独占写出 | 仅本审查稿；未触 SDZJ0170 JSON / progress / 五行精纪 |

无越权文件。源层未改。注解 JSON 未改。

## 2. 校验器独立复跑

对本岗树 `6effd8e`：

```
PYTHONDONTWRITEBYTECODE=1 python3 tools/validate-annotations.py \
  --annotations references/annotations/ziwei/ziwei-doushu-quanshu.json --json
```

实测：

```json
{"ok": true, "books": 1, "files": 1, "entries": 1981, "source_reviewed": 1981,
 "note": "Structural and source-ID checks only; not a semantic or human review certificate.",
 "errors": []}
```

与 Issue 钉死一致：ok、entries=1981、errors=[]、JSON SHA 未变。校验器只证明结构与段落 ID，不是语义证书，更不是人工 verified。

## 3. verified / draft 未越权提升

本包 300 条（索引 0–299）：`review=source-reviewed` 全 300；条目无 `verified` 字段（等价 verified=false / verified=0）；无 `draft`。全书 1981 条同样 `source-reviewed` 全 1981、无 `verified` 字段。无升 verified、未改 review。

kind（本包）：规则候选 123、理论 85、重复 39、评注或元数据 22、序跋目录 17、待核实 6、操作步骤 6、术语 2。

空白话 0、空 terms 0；空 notes 74（多为网页残留或短目录句，可接受）。白话全文完全重复组 2（均为「网页编辑链接残留」套语，对应源文「編輯]」，非空模板冒充正文）。未见「本段论述 / 白话从略 / 见原文 / TODO」类空模板。注解 span 两两无重叠；相邻 span 间隙最大 3 行（页间空行/标题骨架，可接受）。

与 `references/inventory/paragraphs/ziwei/ziwei-doushu-quanshu.json` 索引 0–299：`paragraphId` **300/300** 一一对应，`mismatch=0`。

### 3.1 待核实 6（均 `source-reviewed`，不升 verified、不补写）

| 索引 | paragraphId | 原因（对照源） |
|---|---|---|
| 40 | `L0103-L0103` | 金舆捧栉 / 玉袖天香；短句未明各星与宫位，仅作格名索引 |
| 69 | `L0162-L0162` | 「九窍之奇」「耗积散」表达不清，不扩成量化规则 |
| 73 | `L0170-L0170` | 「身命司数」未列具体星曜；职业旧评不补凶星 |
| 99 | `L0224-L0224` | 天机七杀同宫 / 太阴火铃同位；本命层 vs 别层未明，且固定安星下非常见同宫 |
| 139 | `L0306-L0306` | 金舆捧栉辇 / 衣锦惹天香；命库与临官体系未展开 |
| 179 | `L0387-L0387` | 断桥截路 vs 卯酉二空；起例未定义，不映射现代空曜 |

## 4. 索引边界

全书注解 1981 条；本包只审 0–299。起止与 Issue 钉死一致。

| 位置 | 实测 ID |
|---|---|
| 注解索引 0（CP1 起） | `ziwei-doushu-quanshu:L0003-L0003` |
| 注解索引 299（CP1 止） | `ziwei-doushu-quanshu:L1029-L1029` |
| 注解索引 300（下一包起，不在本包） | `ziwei-doushu-quanshu:L1031-L1044` |
| 注解索引 1980（全书末条） | `ziwei-doushu-quanshu:L4844-L4844` |

CP1 止于羊陀二星总论节后网页「編輯]」残留；remaining **1681**（索引 300–1980）与 Issue 一致。不宣称全书审查完成。

## 5. 抽样语义（≥15 非模板，对照原文，不凭进度摘要）

原文取 `sources/fulltext/ziwei/ziwei-doushu-quanshu/fulltext.md` 的 `start_line–end_line`。抽核 **23** 段（覆盖元数据 / 序跋 / 理论 / 规则 / 术语 / 操作 / 全部 6 条待核实 / 网页残留重复）。对照源文成立；套语仅用于「編輯]」残留说明，不按空模板失败。

| 索引 | paragraphId | kind / review | 对照要点 | 判定 |
|---|---|---|---|---|
| 0 | `L0003-L0003` | 元数据 / sr | 维基文库三卷 + zh-hant；本地来源说明非断法 | 通过 |
| 1 | `L0007-L0007` | 序跋 / sr | 书名题署「紫微斗数全书」 | 通过 |
| 5 | `L0017-L0032` | 序跋 / sr | 罗序：华山访道、托名陈希夷、了然十八代；不生成案例生日 | 通过 |
| 8 | `L0039-L0039` | 理论 / sr | 斗数至玄；星之分野不可一概 | 通过 |
| 11 | `L0045-L0045` | 理论 / sr | 紫微舍躔；土星居垣；金星财库怕空亡 | 通过 |
| 12 | `L0047-L0047` | 规则 / sr | 帝星动则列宿奔；贪守空而财源不聚 | 通过 |
| 40 | `L0103-L0103` | 待核实 / sr | 金舆捧栉 / 玉袖天香；格名索引 | 通过 |
| 50 | `L0123-L0123` | 规则 / sr | 流煞羊陀太岁病符官符；本命与流年分层 | 通过 |
| 56 | `L0136-L0136` | 术语 / sr | 金乌=太阳、玉兔=太阴 | 通过 |
| 69 | `L0162-L0162` | 待核实 / sr | 权禄九窍 / 耗积散；不量化 | 通过 |
| 73 | `L0170-L0170` | 待核实 / sr | 身命司数 vs 善禄技艺；不补凶星 | 通过 |
| 90 | `L0205-L0205` | 规则 / sr | 寅卯木垣机贪；天相水寅巨门水卯；三方文曲破军禄存 | 通过 |
| 99 | `L0224-L0224` | 待核实 / sr | 天机七杀同宫善三分；太阴火铃同位十恶 | 通过 |
| 113 | `L0253-L0253` | 操作 / sr | 对照详凶吉；合照观贱荣 | 通过 |
| 139 | `L0306-L0306` | 待核实 / sr | 紫微坐命库金舆捧栉辇；临官安文曜衣锦惹天香 | 通过 |
| 148 | `L0324-L0324` | 理论 / sr | 童限弱水上浮沤；老限衰风中燃烛 | 通过 |
| 179 | `L0387-L0387` | 待核实 / sr | 断桥截路难行 vs 卯酉二空发福 | 通过 |
| 214 | `L0523-L0534` | 元数据 / sr | 玉蟾太阳十二宫光辉；午中天；戌亥子失辉；父夫星 | 通过 |
| 223 | `L0595-L0595` | 重复 / sr | 源「編輯]」；网页残留非正文 | 通过 |
| 258 | `L0894-L0894` | 操作 / sr | 流年昌曲科名；大小限三合流禄；众条件俱全 | 通过 |
| 286 | `L0976-L0987` | 术语 / sr | 天马诸名：禄马交驰 / 扶舆 / 战马 / 死马 / 折足马 | 通过 |
| 298 | `L1026-L1026` | 元数据 / sr | 陀罗身命；庙陷文武分论；不升 verified | 通过 |
| 299 | `L1029-L1029` | 重复 / sr | 源「編輯]」；本包止此 | 通过 |

关键条件与源行（抽核）：

- 来源说明维基三卷：L3
- 罗序华山 / 了然：L17–L32
- 紫微舍躔土金：L45
- 金舆捧栉 / 玉袖天香：L103
- 寅卯木垣机贪三方：L205
- 天机七杀 / 太阴火铃：L224
- 太阳十二宫玉蟾：L523–L534
- 流年昌曲科名答：L894
- 天马诸名：L976–L987
- 陀罗身命庙陷：L1026
- CP1 止「編輯]」：L1029

## 6. Caveat（不构成本包失败）

1. **电子主本 ≠ 影印校勘。** 源为维基文库三卷电子本（zh-hant）；`source-reviewed` 只证明对照该电子文字，不是人工 verified，也不是专家认证。
2. **网页「編輯]」残留。** CP1 内多处同类抓取残留已标 `重复` / 网页残留；白话套语重复属说明残留，不是把正文模板化。
3. **待核实 6 条。** 格名、同宫层次、空曜起例等歧义已在 notes 保留；本审查不补写、不升 verified。
4. **身份 / 职业 / 性别旧断语。** 多处保留历史评价框架（僧道官吏、女命夫星等），notes 已标明不转成现代身份或预测断言。
5. **不宣称全书审查完成。** remaining 索引 300–1980（1681 条）待后续包。

## 7. 交付边界

| 项 | 状态 |
|---|---|
| 本包结论 | **通过**（CP1 0–299） |
| 注解 JSON | 未改；SHA 与 Issue / ming-360 / ming-369 一致 |
| verified | 保持缺失/false；未升 |
| SDZJ0170 | 未触 |
| 五行精纪 | 未扩抽样 |
| remaining | 索引 300–1980（1681） |
| 下一步 | 协调派 CP2 或后续审查包；本岗不重写主本 JSON |

审查岗：FateRadar 资料工程师 A · MING-376 · 2026-09-12
