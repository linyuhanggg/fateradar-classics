# 消费方数据版本 · t211 执行层跨盘汇总（修掉只取首盘的口径）＋小六壬样盘

日期：2026-09-21。基线提交：`adaf834`（t210 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

修掉一个**会系统性掩盖改进**的报告口径：`eval-executable` 只取各术**首个**样盘，
于是「只在某些盘上才可判」的改进**看不见**（t210 自己那两条就是这样被掩盖的）。
新增 `--across` 跨盘汇总——它当场找出一类此前完全看不见的缺口：
**本仓从来没有「小六壬」这一术的样盘**，而执行层有 6 条小六壬记录。

补上后：**满足 72 → 75**、**信息不足 30 → 27**、跨盘可判 **226 → 229**。

## 1. 新口径：跨盘汇总

```bash
python3 tools/eval-executable.py --all --across          # 人读
python3 tools/eval-executable.py --all --across --json    # 机器读
```

每条记录在**本术全部样盘**上求值，分「至少一张盘可判（满足/不满足）」与「任何盘都判不了」，
后者**按原因归类**：

| | 条数 |
|---|---:|
| **至少一张盘可判** | **229** |
| **任何盘都判不了** | **29** |
| ├ 引用接不上 FactKey 的字段 | 21 |
| ├ 语料无构成定义 | 4 |
| ├ 事实键在任何样盘都不在场 | 3 |
| └ **本仓没有该术的样盘**（补样盘即可判） | **1** |

最后一类是本轮新分出来的、**可操作**的一类。默认输出保持不变（仍取首盘），`--across` 是增量口径。

## 2. 跨盘汇总当场找出的缺口：本仓没有「小六壬」样盘

执行层有 **6 条小六壬**记录（`references/executable/yuxiaji-xiaoliuren.json`）
＋ 1 条梅花，而本仓样盘**从来没有小六壬这一术**——它们在**任何**盘上都判不了，
**首盘口径完全看不出来**（在首盘口径下它们只是混在「信息不足」里）。

而引擎本来就产事实：

- `xiaoliuren-base.ts` 产 `xiaoliuren_palace`（`scope.palace` 为「月宫／日宫／时宫」）；
- 该键**一直在词表里**——FIELD_MAP 的旧注「古籍仓词表无」**早已过期**
  （t195 起词表由引擎 `toFactVocabJson()` 生成）。

修法三步：

1. dump 补两张小六壬样盘（`lunarCastFromSubject` → `buildXiaoliuren`）；
2. FIELD_MAP 把三宫接上：
   `xiaoliuren.palace.month/day/hour` → `xiaoliuren_palace` ＋ `scope.palace`「月宫／日宫／时宫」；
3. `ART_EMIT_KEYS` 补 `xiaoliuren` 一项（参考术，不在六术门禁内）。

## 3. 效果

| | t210 | **t211** |
|---|---:|---:|
| 满足 | 72 | **75** |
| 不满足 | 152 | 152 |
| **信息不足** | **30** | **27** |
| 未提供定义表 | 4 | 4 |
| 跨盘可判（新口径） | 226 | **229** |
| 任何盘都判不了 | 32 | **29** |

小六壬仍有 3 条判不了（`xiaoliuren.hour.branch`、`xiaoliuren.count.good`、`农历月/日`）——
它们是**输入或计数**，引擎未产成事实，如实留在「接不上 FactKey」里。

## 4. 测试（写时先红了两处）

`test-eval-executable.py` 补第 6 节，钉 `--across` 的四条不变量：

1. **跨盘可判 ⊇ 首盘可判**（首盘判得出 ⇒ 至少一张盘判得出）；
2. `decidable_cases` 与 `decidable_somewhere` 一致；
3. `per_case` 覆盖该术**全部**样盘（不是子集）；
4. 标了 `no_sample_for_art` 的，必须**确实**无样盘。

写测试时先红了两处，都值得记：

- 无样盘的记录走**早退分支**、本就没有 `across` —— 我的首版断言太严（正确行为被判失败）；
- 新接的键**必须在 `ART_EMIT_KEYS` 里** —— 这正是第 2 节那道老断言抓出来的，
  说明那道断言**有效**（它防的正是「对照表引用了某术并不产出的键」）。

## 5. 台账

`tools/reports/executable-across.json`（随仓提交）：三态计数 ＋ 29 条判不了的明细与原因，
供人直接看「哪些记录在任何盘上都判不了、为什么」。

## 6. 未决清单（承接 t210）

| # | 事项 | 变化 |
|---|---|---|
| 1 | ~~executable 报告只取首盘~~ | **本轮已修**（`--across`） |
| 2 | 梅花 1 条（`MHY-E-01`） | **新增**：本仓无梅花样盘，补样盘即可判（梅花引擎有 `meihua_gua` 事实） |
| 3 | 小六壬余 3 条 | 需产出输入类事实（时辰支、农历月日）与计数（吉类计数） |
| 4 | `liuyao.structure` 17 条 | 两仓无定义，需人给定义（现居「接不上」之首） |
| 5 | `day.gan.element` 1 ／ `year.gan.doushu` 1 | 前者引擎有五行表未产出该键；后者未产出 |
| 6 | 计数语义（独发／独静／用神两现） | t207：唯一有真实需求的语言缺口 |
| 7 | `TAIWEIFU-010`「魁钺同行」；跨键关系 7–9 条 | 待人裁定；建议由引擎产判定名 |
| 8 | `v14-low-correspondence`／`p6-grey-zone` | t202：不可机器推进，改交 40 条人眼读单 |
| 9 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/eval-executable.py --all --across          # 229 可判 / 29 判不了
python3 tools/eval-executable.py --package references/executable/yuxiaji-xiaoliuren.json --case caseA
python3 tools/test-eval-executable.py                    # 含 --across 的四条不变量

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

## 8. 给 cosmic 的版本钉

**无规则/谓词数据变化**，`CLASSICS_REV` **不变** =
`658ee6c531a86ec0290b8c2b62a0c5e244fbe51f`。
产品仓 `generated/*.json` 已同步覆盖（导出无变化）；`tsc --noEmit` exit 0；
产品侧 **3571 passed / 0 failed**。六术谓词覆盖率不变。

**给消费方的一条说明**：本仓样盘新增了 `xiaoliuren` 一术（两张盘）。
若你的测试遍历 `facts-sample.json` 的术，请容许多出这一术；
若你要评估执行层的小六壬记录，三宫用 `xiaoliuren_palace` + `scope.palace`（月宫／日宫／时宫）即可。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。