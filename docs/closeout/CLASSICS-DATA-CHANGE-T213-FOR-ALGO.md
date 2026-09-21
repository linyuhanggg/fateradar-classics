# 消费方数据版本 · t213 撤回 5 条「按样本拟合」的谓词（ziwei 67.7% → 62.4%）

日期：2026-09-21。基线提交：`ef5f1bd`（t212 后）。
**数据修订提交（请钉这个）：`6a51140eb1c16cb46a13749ea087babcb519724c`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t212 的**取值溯源检查**把「取值不在本条 statement/quote 里」的组列成人读清单（23 组）。
本轮逐组读过去，**查出 5 条是把样本观测量当成了条件**——这是**此前所有检查都漏掉的一类真缺陷**。

**撤回了它们，覆盖率因此下降：ziwei 67.7% → 62.4%。** 契约第一条是
「可溯源优先于覆盖率」，所以这个下降是**正确方向**。

## 1. 查出的 5 条

| rule | 原谓词 | 原文讲的是什么 | 结论 |
|---|---|---|---|
| `TAIWEIFU-020` | `{liunian_taisui: 午}` | 童子限/老人限…遇杀无制 | **取值与原文无关** |
| `ZIWEIDOUSHUQ-ZW-06` | `{daxian:子女, daxian:田宅, liunian_taisui:午}` | 三限合参定吉凶（通则） | **三个取值都不在原文里** |
| `ZIWEIDOUSHUQ-055` | `{liunian_taisui:午, 化忌入命宫, 禄存入财帛}` | 同左 | 首句无关；后两句**逐字可查** |
| `ZIWEIDOUSHUQ-051` | `{daxian: 子女}` | 章节标题「06 大限/小限/流年运程」 | 宫位原文未写 |
| `ZIWEIDOUSHUQ-054` | `{daxian: 田宅}` | **南斗/北斗诸星宫**两类断法 | 宫位与之无关 |
| `ZIWEIDOUSHUQ-065` | `{daxian: 子女/田宅}` | 先贫后富之象（大限早凶后吉、武贪格） | 宫位原文未写 |

（共 6 条规则涉及，其中 055 只删一个子句、其余 5 条撤回谓词。）

## 2. 为什么别的检查都漏了

这类谓词**照样能命中**——命中那些「流年支为午」「大限落某宫」的盘——
所以：

- **覆盖率**照算 ✓（它们计为已映射）；
- **验证深度**也不报警 ✓（它们确实在某张盘上成立）；
- 取值域检查／死引用／art-keys 全过 ✓（键与取值都合法）。

**只有「取值是否出自原文」这一问能查出来。** 这正是 t212 那道检查的价值——
它上岗一轮就查出 5 条真缺陷。

## 3. 处理

| rule | 处理 | 重新归类 |
|---|---|---|
| `ZIWEIDOUSHUQ-055` | 删去未落原文的 `午` 子句，保留两句逐字可查的 | 仍 mapped（谓词更窄但**全部可溯源**） |
| `ZIWEIDOUSHUQ-ZW-06`／`-051` | **撤回谓词** | `meta-rule`（适用前提是「三限齐备」，属就绪条件） |
| `TAIWEIFU-020` | **撤回谓词** | `fact-not-emitted`（缺「限类型」与「制化判定」） |
| `ZIWEIDOUSHUQ-054` | **撤回谓词** | `fact-not-emitted`（缺「星属南斗/北斗」与「大限所行宫」） |
| `ZIWEIDOUSHUQ-065` | **撤回谓词** | `fact-not-emitted`（缺大限序列与武贪格判定） |

## 4. 数字

| | t212 | **t213** |
|---|---:|---:|
| ziwei 已映射 | 63 | **58** |
| **ziwei 覆盖率** | **67.7%** | **62.4%** |
| 六术合计已映射 | 383 | **378** |
| 未映射 | 463 | **468** |
| 验证深度 | 382/383 | **377/378（100%）** |

其余五术覆盖率不变（bazi 49.9%／qimen 90.0%／liuren 35.9%／liuyao 43.5%／qizheng 24.4%）。

## 5. 闭环：把读过的对译登记下来

新增 `tools/reports/value-equivalences.json`，逐组登记裁定，两类：

- **`legit-transcription`**（真·名目对译）：七煞/偏官→**七杀**、财→**妻财**、忌→**化忌**、
  官禄→**事业**、奴仆→**交友**、妻宫→**夫妻**、命→**命宫**、魁→**天魁**、钺→**天钺**、禄→**禄存**；
- **`statement-doesnt-name`**（原文那句确实没写）：穷通宝鉴按日干分章、
  三传位名、章节标题／就绪条件式。

溯源工具接上登记表后：**「待读」由 44 → 0**（已读 35）。
测试相应改为**不要求** `canonical > 0`——待读为零是**好状态**，
并要求「待读为空 ⇔ 已读非空」这条一致性。

## 6. 顺带查明：审计的变更溯源有个设计要点

`audit-contract.py` 的变更溯源只认 `tools/reports/*map*.json` 的 `applicable_to_yaml`
与 `v3-language-migrations.json`。也就是说：**「清空谓词」这件事必须落在 `*map*.json` 里**才算「有出处」，
单靠 `predicate-decisions` 的 `unmapped`／`reverted` 条目**不算**——
我先只更新了决策台账，审计立刻报出「无台账出处 3 条」。已新增 `t213-reverted-map.json` 记录这 5 条撤回。

## 7. 未决清单（承接 t212）

| # | 事项 | 变化 |
|---|---|---|
| 1 | ~~23 组待读取值~~ | **本轮读完并登记**（待读 0）；其中 5 条查出真缺陷并撤回 |
| 2 | 撤回谓词 5 条所需事实 | **新增**：限类型／制化、星属南斗北斗、大限序列与武贪格（引擎投入） |
| 3 | `value-equivalences.json` 的维护 | **新增**：新增谓词后若出现未登记取值，待读清单会重新非空——那是**要看**的信号 |
| 4 | 梅花 1 条（`MHY-E-01`） | 本仓无梅花样盘，补样盘即可判 |
| 5 | 小六壬余 3 条 | 需产出输入类事实与计数 |
| 6 | `liuyao.structure` 17 条 | 两仓无定义，需人给定义 |
| 7 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 8 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 9 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机械推进，改交 40 条人眼读单 |
| 10 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 8. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：撤回与登记
python3 tools/value-provenance-report.py            # 待读应为 0，已读 35
python3 tools/test-value-provenance.py
python3 -c "import json;d=json.load(open('tools/reports/t213-reverted-map.json'));print([e['rule_id'] for e in d])"
python3 tools/predicate-report.py | grep -E '^ziwei'   # 期望 58 / 62.4%

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
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 9. 给 cosmic 的版本钉

`CLASSICS_REV` = **`6a51140eb1c16cb46a13749ea087babcb519724c`**。
产品仓 `generated/ziwei.json` 已同步覆盖（**58 条带谓词**，比上版少 3 条；
`ZIWEIDOUSHUQ-055` 的谓词也变窄了）；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。

**给消费方的一条重要说明**：**本次是数据回撤**——`ZIWEIDOUSHUQ-051/054/065/ZW-06` 与
`TAIWEIFU-020` 的 `applicableTo` 现在是**空数组**，它们在产品侧不会再命中；
`ZIWEIDOUSHUQ-055` 的命中范围也收窄了（不再要求流年支为午）。
原因：这 5 条的取值**查不到原文出处**（把样本观测量当成了条件）。
若你的面板或缓存里还留着旧版命中，请按新数据重算。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。