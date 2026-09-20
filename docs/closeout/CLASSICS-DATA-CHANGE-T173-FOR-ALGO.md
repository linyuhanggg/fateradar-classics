# 消费方数据版本 · t173 事实层补完（liuyao_seq · 值符/值使落宫）与 3 条无据 statement 的拒绝

日期：2026-09-21。基线提交：`f1306ab`（t172 后）。
**数据修订提交（请钉这个）：`eb9ad74bb1ed3bf5a6557fe70e900fc32a10bac6`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

延续 t170／t171 的路子（**事实在引擎里，只是没被当事实产出**），本轮补两项：
六爻世序／卦体分类 `liuyao_seq`、值符／值使落宫。**但没有据此新增任何谓词**——
因为候选的 3 条六爻规则，其 statement 断言的概念在锚定原文里**根本不出现**（§3）。

**本轮谓词覆盖率不变**；变化在事实层，改善的是 **executable 层的可判性**。

## 1. 覆盖率（口径未改，本轮不变）

| art | 基线 | t171 | 本轮 | 通配占比 |
|---|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 211 (47.0%) | 7.6% |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 (67.7%) | 0.0% |
| qimen | 7 (17.5%) | 24 (60.0%) | 24 (60.0%) | 4.2% |
| liuren | 11 (20.8%) | 11 (20.8%) | 11 (20.8%) | 9.1% |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 (30.4%) | 14.3% |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 (24.4%) | 9.1% |

未映射 **505 条**（不变）。4 大门禁全绿；**24** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS。

## 2. 两个新事实

| key | 含义 | 取值域 | 来源（都已在排盘结果里） |
|---|---|---|---|
| `liuyao_seq` | 六爻世序／卦体分类 | 本宫·一世·二世·三世·四世·五世·游魂·归魂（封闭 8 值） | `main.sequence`（`liuyao-base` 的 `SEQ_NAME[s]`，**本就是名**） |
| `zhifu`／`zhishi` + `scope.gong` | 值符星落宫／值使门落宫 | 宫 1–9 | `layout.starPalace`／`layout.doorPalace` |

- 都是**透传**，不新算排盘。
- `zhifu`／`zhishi` 既有**未声明 scope** 的谓词行为不变（scope 只会更严，不会更松）；
  产品仓相关测试（含 `qimen-methods` 34 项）全绿。
- 实测样本：caseA `zhifu=天柱@gong2`、`zhishi=惊门@gong4`；liuyao caseA `本宫`、caseB `三世`。

### 2.1 收益：executable 层两条记录由「信息不足」变「满足」

`zhifu.palace`／`timedry.palace` 此前在 `FIELD_MAP` 里如实标着「引擎未产出」。
本轮接上后：

```
全库：满足 65→67   不满足 143   信息不足 38→36   未提供定义表 12
QMD-E-01（伏吟落宫）→ 满足 conf=1.0
QMD-E-02            → 满足 conf=1.0
```

**这条缺口被两条独立路径同时点名**：t171 我从谓词侧判断「QM-P01／P02／P31 需要值符落宫」，
而 executable 层 `QMD-E-01` 的 `required_facts` 早就写着 `zhifu.palace`。现已由测试钉住
（`test-eval-executable.py` D 组）。

## 3. 本轮**拒绝**了 3 条映射——这是本轮最重要的判断

`liuyao_seq` 一产出，3 条六爻规则立刻可写谓词（statement 明写归魂／游魂）：

| rule_id | statement 断言 | 锚定原文含该概念？ | 对应度 |
|---|---|---|---|
| `ZR-09` | 归魂卦／游魂卦 | **否**（L5410 通篇无此二字） | 0.300 |
| `ZR-13` | 游魂卦不宜远行 | **否**（同锚同行） | 0.591 |
| `ZENGSHANBUYI-ZR-13` | 临归魂——速归 | **否**（L1967 讲用神动克世） | 0.522 |

三条的 `quote` 都确为锚定行的**逐字片段**（所以 V5／V13 都过），但**锚定原文里没有那个概念**。
V14 的阈值是 <0.15，0.30／0.52／0.59 都在阈值之上，故既有门禁**不会**报。

**若照 statement 写谓词，就是把无据断言打扮成有据**——这比留空更坏，因为它让消费方以为
这条有原文支撑。故**保持 `applicable_to: []`**，并把证据登记到
`tools/reports/ungrounded-claims.json`（含锚点、是否逐字、对应度）。
要收口需在古籍侧先解决 statement↔anchor 不符（改锚到真正讲归魂／游魂的原文，或把 statement
标为编者综述）。

### 3.1 相关负结论：不能拿 `terms.yaml` 当「概念落地」判据

本想把这类检查做成工具，实测**不行**：

- `references/vocab/terms.yaml` 1023 条里 **791 条 `kind: imported`**，含整句
  （如「日柱及其纳音条文语义。」）；
- 条目的 `fact_key` 是**分术**的：「六合」→ `fact_key: bashen`（奇门六合**神**），
  而六爻规则要的是**地支六合**——照它套会串术。

同样，机器批量判据（概念词后缀启发式）在本库噪声过大：初版在 316 个概念词里报 292 个「缺失」，
绝大多数是「的命局」「须按命局」这类散文残片。**故不作为工具出货**，只登记逐条复核过的 3 条。

## 4. 顺带：可复跑的下批优先级

`predicate-gap-report.py` 新增 `--fact-gaps`：按 **live `applicable_to`** 过滤后，
把当前仍为 `fact-not-emitted` 的 **201 条**按缺口归因排序。
（此前的临时统计是**错的**——台账是当时的过程记录，t170／t171 已映射的条目仍写着
fact-not-emitted，不过滤会把已完成的算成待办。）

```
201 条：其他/未归类 34 · 柱干支 30 · 神煞 30 · 六爻 25 · 梅花 21 · 纳音 18 · 奇门 16 · …
```

分类**带 art 约束**（初版出现过「八字条目的『时干』被归到奇门」的串档，已修）。

## 5. 未决清单（按优先级）

1. **statement↔anchor 不符的收口**（§3）：3 条已登记；是否有同类条目需更精确的判据（§3.1 已说明
   现有两条路都不精确）。
2. **神煞具体名 30 条**：需要扩 `shensha` 的取法表（古典实现工作），不是 FactKey 问题。
3. **柱干支 30 条**：多为「时柱／日支」类，且含**性别**（本仓无 gender 事实）。
   奇门侧的柱干还缺**跨键取值相等**的表达力（「庚临岁干」＝天盘庚与岁干同宫取值相同），
   v3 的 `same` 只绑 scope 字段、不绑取值——属语言或事实的设计问题。
4. **六爻 25 条**：月建／日辰／变卦／旺衰／空亡入墓，需要新事实与关系判定。
5. **梅花 21 条**：本仓**无梅花事实层**（体用／互变卦都没有），要做得先有引擎。
6. **15% 通配闸门挡住 4 条奇门规则**：`QM-P01／P02／P26／P31` 现在事实齐了，
   但只能写成 `{all_of:[{zhifu, value:"*"}, {dipan_gan, X}], same: gong}`——
   这里的 `*` 语义是「值符事实存在，取值不限」，**不是凑数**；可是闸门按规则数计：
   qimen 1/24=4.2% → 5/28=**17.9%**，会**红**。**未放宽闸门**，也未挑 2 条凑数通过。
   要收口需二选一：给闸门加一条「存在性通配 vs 凑数通配」的判据（口径变更，需授权），
   或为「值符宫天/地盘干」另设派生事实键（可写死取值、无需通配）。
7. t170／t171／t172 遗留：`daxian`/`liunian_taisui` 事实现状；
   `liuyao.structure`（17 条）是**打包名**、无单一 FactKey 对应，需古籍侧拆分声明；
   ziwei 11 条命名格局缺定义表；`fold_han` 不处理古异体字；`nayin` 尚无谓词使用。
8. t169 遗留：189 条重述是否换成真引文、V11 111 vs G1 <50、25 条既有结构恒真映射。

## 6. 不变量与可复跑命令

不变量：不改 `statement`／`quote`／`anchor`／`verified*`；不新增 `value: "*"`；
不硬锚；不把未实现的救应写成没有救应；不生成让 `verified` 变 true 的自我认定。
`verified: true` 全库 **0**；executable 层 `rescue=unimplemented` 30 条、`named_gaps` 31 条照旧。

```bash
cd /Users/sync/code/fateradar-classics

# 本轮新增：下批优先级（按 live 状态过滤）
python3 tools/predicate-gap-report.py --fact-gaps
python3 tools/predicate-gap-report.py --fact-gaps --json | head -30

# executable 层求值（t172 起；本轮两条记录转为可判）
python3 tools/eval-executable.py --all
python3 tools/test-eval-executable.py            # 30 项，含 D 组「值符落宫已接上」

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 无据 statement 登记
python3 -c "import json;d=json.load(open('tools/reports/ungrounded-claims.json'));print(len(d['entries']),'条')"
```

## 7. 给 cosmic 的版本钉

`CLASSICS_REV` = **`eb9ad74bb1ed3bf5a6557fe70e900fc32a10bac6`**。
产品仓 `generated/*.json` 已同步覆盖；两处 `fact-vocab.json` 共有键值域逐项一致（39 键）；
`tsc --noEmit` exit 0；相关 7 个测试文件 **80 项全绿**。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。