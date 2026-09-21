# 消费方数据版本 · t217 解掉 17 条长期阻塞的记录（满足 75→92、信息不足 27→10）

日期：2026-09-21。基线提交：`d5cc313`（t216 后）。
**本轮无规则/谓词数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`c5bba9be08c4080107a5a001a6e0b886ae34a558`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

`liuyao.structure` 自 t183 起「两仓无定义」、17 条记录长期只能报「信息不足」。
t216 给出提议后，本轮找到一个**决定性性质**：两种候选读法在**当下引擎**上**恒成立**，
因此 `{exists: …}` 的判定**不依赖选哪种读法**；代理键又**只在该层存在时为真**（保守）。
于是**落地并如实归因**——说明里标明「推断」、指向依据台账、并写明回改条件。
效果：可执行层**满足 75 → 92**、**信息不足 27 → 10**。

## 1. 为什么这次可以落地（t216 时还不行）

| 候选读法 | 在当下引擎上 |
|---|---|
| ①「本卦逐爻结构层已就位」 | 恒成立——构建成功的六爻盘就有逐爻事实（六枚 `yao_zhi`） |
| ②「引擎已算完结构分析」 | 恒成立——`liuyao-analysis` 的 `ruleChecks`（ZSB-E-01…E-19）随盘产出 |

**两者同真 ⇒ `{exists: "liuyao.structure"}` 的真假与读法选择无关。**
且代理键 `yao_zhi` 的语义是「逐爻结构在场」，**只在该层存在时为真**（每盘恰好六枚）
⇒ 判定**保守**：不会因为引擎少算而误判成立。

落地时三条都写进代码与台账：

1. `FIELD_MAP` 的说明里标明「**推断**」（机器不把推断当已证）；
2. 说明里指向依据台账 `tools/reports/liuyao-structure-proposal.json`；
3. 台账记下「两读法同真」「为何保守」「**若人裁定另有所指，回改一条即可**」。

**正式定义仍待人工裁定**——本轮只落地一个带标注的代理键。

## 2. 顺带补上 17 条使用者的前置项：爻五行

`liuyao.node.element`（爻五行）引擎节点状态里一直有，事实层没产出 → 新增 **`liuyao_node_element`**
（`scope.yao`，值域五行）。

同时把**六条直接对应**（字段名与引擎结构一一对得上，**不涉推断**）也接上：

| 字段 | FactKey |
|---|---|
| `liuyao.node.branch` | `yao_zhi` |
| `liuyao.changed.branch` | `bian_yao_zhi` |
| `liuyao.node.moving` | `dongyao` |
| `liuyao.node.activity` | `liuyao_activity` |
| `liuyao.node.element` | `liuyao_node_element`（本轮产出） |
| `liuyao.hidden` | `fushen` |
| `question.useRelative` | `liuyao_yongshen` |

**未接**的只剩：`liuyao.node.state`／`liuyao.node.position`／`liuyao.interactions`／
`day.ganzhi`／`month.zhi`——含义多歧或引擎未产出，**不猜**。

## 3. 效果（跨盘口径）

| | t216 | **t217** |
|---|---:|---:|
| **满足** | 75 | **92** |
| 不满足 | 152 | 152 |
| **信息不足** | **27** | **10** |
| 未提供定义表 | 4 | 4 |
| **至少一张盘可判** | 229 | **246** |
| **任何盘都判不了** | 29 | **12** |
| 接不上 FactKey 的字段引用 | 22 | **5** |

剩下 12 条判不了的构成：5 条引用接不上的字段（小六壬的时辰支／农历月／吉类计数、
`day.gan.element`、`year.gan.doushu`）、4 条语料无构成定义、3 条事实键在任何样盘都不在场。

其余不变：`rescue=unimplemented` 30、带 `named_gaps` 31、**`verified=true` 0**、
`validate-executable.py` OK（15 包 / 258 条 / 579 来源跨度 / 42 具名缺口）。

## 4. 两处闸门各抓到一次（说明它们有效）

1. `test-eval-executable.py` 的老断言「FIELD_MAP 的 FactKey 必须被某引擎产出」
   **立刻报出** `liuyao.node.element→liuyao_node_element` 漏登记 `ART_EMIT_KEYS`
   （这正是它当年修过的那类缺陷）；
2. `test-structure-proposal.py` 的「提议**未落地**」断言随本轮状态变化——
   改为「**已落地但带归因**」，并**新增两条**：说明里必须含「推断」、必须指向依据台账。

两处都是**该改就改、但不放宽**：改后仍钉住真实性质（而不是删掉断言）。

## 5. 未决清单（承接 t216）

| # | 事项 | 变化 |
|---|---|---|
| 1 | **`liuyao.structure` 的正式定义** | **本轮落地代理键并归因**；正式定义仍待人工裁定（裁定后回改一条映射即可） |
| 2 | ~~`liuyao.node.element` 前置项~~ | **本轮已产出** |
| 3 | 剩余 12 条判不了的记录 | 5 字段（小六壬输入/计数、日干五行、年干斗数）＋4 无定义＋3 键不在场 |
| 4 | 梅花余项／易理余项 | 断法表（恒真）不写；`-016` 变卦所指有歧义；`-007` 卦主口径多歧；`-026` 需计数与爻辞层 |
| 5 | 撤回谓词 5 条所需事实 | 限类型／制化、星属南斗北斗、大限序列与武贪格 |
| 6 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 7 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 8 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/eval-executable.py --all                    # 期望 满足 92 / 信息不足 10
python3 tools/eval-executable.py --all --across | sed -n '5,12p'   # 可判 246 / 判不了 12
python3 tools/test-structure-proposal.py                  # 落地 + 带归因 + 依据台账
python3 -c "
import json;d=json.load(open('tools/reports/liuyao-structure-proposal.json'))
print(d['status']); print(d['applied']['why_safe'])"
python3 -c "
import json;d=json.load(open('tools/reports/facts-sample.json'))['liuyao']['caseA']
print('爻五行:', [f['value'] for f in d['facts'] if f['key']=='liuyao_node_element'])"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/domain-check.py
python3 tools/verification-depth-report.py
python3 tools/audit-contract.py
```

## 7. 给 cosmic 的版本钉

**无规则/谓词数据变化**，`CLASSICS_REV` **不变** =
`c5bba9be08c4080107a5a001a6e0b886ae34a558`
（本轮只动求值器的 `FIELD_MAP`、产品侧的事实产出与标签表，规则数据未变）；`tsc --noEmit` exit 0；
产品侧 **3574 passed / 0 failed**。

**给消费方的两条说明**：

1. 事实层新增 `liuyao_node_element`（爻五行，`scope.yao`，值域五行）——
   已在 `LABELS` 登记（t215 起的回归测试会拦住漏登记的情况）。
2. 可执行层新落地一条 **带归因的推断映射**（`liuyao.structure → yao_zhi`）：
   它让 17 条记录变为可判；该映射在代码说明、依据台账与测试里三处都标着「推断」，
   **不是**被当作已证事实。若你方对 `liuyao.structure` 的正式定义有裁定，
   回改 `FIELD_MAP` 一条即可，本仓会同步交付文档。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。