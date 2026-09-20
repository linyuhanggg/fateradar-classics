# 消费方数据版本 · t170 逐柱干支与纳音入事实层（六十甲子象辞 60 条落地）

日期：2026-09-21。基线提交：`6dc5415`（t169 人工复核台账化后）。
**数据修订提交（请钉这个）：`0c991a01cabef60abb4928969fedd5fa70f9805e`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t168 的结论是「不是缺事实，是谓词语言不够」。t169 把 599 条逐条判完后，
**`fact-not-emitted` 占 277 条（47.7%）——缺事实确实是最大的一块**（与任务书的原判相反）。
本轮处理其中**最大且最便宜**的一类：**事实本来就在引擎里，只是没被当作事实产出。**

新增三个 FactKey（`gan`/`zhi`/`nayin`，四柱天干／地支／纳音），全部由 `emitBaziFacts`
**入参已有的** `ganzhi` 四柱与「纳音」行逐柱产出 —— **不新算排盘、不改既有 `rizhu`/`yueling` 口径**，
符合旧件 3c「引擎必须从已有排盘结果取出，取不到就回退、不许为产出事实改排盘」。

产出：**60 条规则落地**（《李虚中命书》六十甲子纳音象辞），bazi 谓词覆盖 **33.6% → 47.0%**，
未映射 **581 → 521**。

## 1. 覆盖率前后（口径未改，可复跑）

`python3 tools/predicate-report.py`

| art | 基线 with_pred | t169 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 151 (33.6%) | **211** | **47.0%** | 7.6% | 7 → **9** |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 8 (20.0%) | 8 | 20.0% | 12.5% | 4 |
| liuren | 11 (20.8%) | 11 (20.8%) | 11 | 20.8% | 9.1% | 3 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 | 30.4% | 14.3% | 5 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |
| meihua / yili（参考） | 0 | 0 | 0 | 0.0% | 0.0% | 0 |

- 未映射：**581 → 521**（−60）。口径一字未改，**未新增任何 `value: "*"`**。
- 各 art 通配占比全线 ≤ 15%（PASS）；`--check-open-values` / `--check-art-keys` PASS。
- 新键里 `gan`/`zhi` 被 60 条规则各用一次；`nayin` 尚无谓词使用（先入事实层，供后续批次）。

## 2. 三个新 FactKey

| key | 含义 | 取值域 | 来源 |
|---|---|---|---|
| `gan` | 四柱天干，`scope.pillar ∈ year/month/day/time` | 10 天干（= `rizhu` 域） | `ganzhi` 四柱（已在入参） |
| `zhi` | 四柱地支，同上 | 12 地支（= `yueling` 域） | 同上 |
| `nayin` | 纳音，逐柱 | 开放值域 | 入参 `rows` 的「纳音」行 |

**与 `rizhu`/`yueling` 有意重复**：那两个是既有谓词在用的别名（日干／月支），
保留以免打断 143 条既有 bazi 谓词；`gan`/`zhi` 是**完整四柱**的统一取法。
两处词表（古籍仓 `references/vocab/fact-vocab.json` 与产品仓 `vocab.ts` + 导出的 `fact-vocab.json`）
已同步，共有键值域逐项一致（36 键）。

## 3. 六十甲子象辞：60 条如何映射，以及为什么这样映射

《李虚中命书》的六十甲子纳音象辞，形如「**丙寅**祿地元是子母相承之火…」。
忠实映射形态（v3）：

```yaml
applicable_to: {all_of: [{key: gan, value: 丙}, {key: zhi, value: 寅}], same: pillar}
```

即「某一柱的天干是丙、地支是寅」——`same: pillar` 正是 t168 为「同柱／同宫绑定」加的语义。

### 3.1 判据不能是「取引文开头那个干支」

源文**一行并列 2–3 个甲子条目**（实测 L26 同时含「己巳地奇備乃…」与「庚午天祿承是…」），
而这批规则的 `quote` 是**整行**摘录。于是：

- 按引文开头取干支 → 「庚午」条会被锚成「己巳」（`LIXUZHONGMIN-007` 实测如此）。
- 正确做法：从 **statement 的象辞**出发，在锚定行内**逐条目切分后反查**，要求**唯一命中**。

工具：`tools/map-nayin-ganzhi.py`（`--dry-run` 可先看）。

### 3.2 自证：反查序列 == 六十甲子规范序列

```
甲子 乙丑 丙寅 丁卯 戊辰 己巳 庚午 辛未 壬申 癸酉 甲戌 乙亥
丙子 丁丑 戊寅 己卯 庚辰 辛巳 壬午 癸未 甲申 乙酉 丙戌 丁亥
戊子 己丑 庚寅 辛卯 壬辰 癸巳 甲午 乙未 丙申 丁酉 戊戌 己亥
庚子 辛丑 壬寅 癸卯 甲辰 乙巳 丙午 丁未 戊申 己酉 庚戌 辛亥
壬子 癸丑 甲寅 乙卯 丙辰 丁巳 戊午 己未 庚申 辛酉 壬戌 癸亥
```

**60 条映射，0 跳过，顺序、无重复、无缺漏**。任一映错都会在序列里留下重复或缺号，
所以这条断言比逐条人眼核对更强 —— 已入 `tools/test-map-nayin-ganzhi.py`。

### 3.3 端到端求值验收

| 样本 | 四柱 | 甲子条 | 己巳条 | 戊午条 |
|---|---|---|---|---|
| caseA | 庚午／甲申／壬子／丁未 | 不满足 | 不满足 | 不满足 |
| caseB | 甲子／丙寅／己巳／甲子 | **满足** | **满足** | 不满足 |

与四柱逐一对得上（caseB 年柱与时柱皆甲子、日柱己巳）。`confidence=1.0`（引用键齐全、无通配）。

### 3.4 顺带查出：`fold_han` 不处理古异体字

`validate-rules.py` 的 `fold_han` 走 opencc t2s，能处理繁简，但 **逺/㳺/蔵/隂 等异体字形原样保留**。
后果：statement 写「流远澄清之水」、源文作「流逺澄清之水」，归一后仍不相等 →
象辞匹配失败、条目被误判成「找不到干支」（实测 5 条因此漏出）。
本轮只在映射工具内补一张**小字表**（只列实际撞到的字形），**未改 `fold_han` 本身**
（改它会影响 V11/V14 的判据，属另一笔）。

## 4. 事实层与产品仓的同步

- 产品仓：`vocab.ts`（类型 + `FACT_KEYS` + `FACT_VALUES`）、`emit.ts`（`emitBaziFacts` 三处逐柱 push）。
  已验证 `vocab.ts` 与导出的 `fact-vocab.json` **逐项一致**（用 jiti 直接 import 源文件比对，
  不靠手抄）。`tsc --noEmit` exit 0。
- 夹具重新生成：本机无 `bun`，改用 `jiti` 加载 `scripts/dump-facts.ts`（自动解析 `@/` 别名），
  **夹具来自引擎而不是手写**。
- `tools/export-rules.py` 重导 → `exported=846 == anchored_exportable=846`；
  `dist/rules/*.json` 已同步覆盖产品仓 `generated/`（bazi 446 条、211 条带谓词）。
- 产品仓 `CLASSICS_REV` 钉到 **`0c991a0`**。产品仓相关 8 个测试文件 **69 项全绿**。

## 5. 顺带查出：夹具已落后于引擎，且 `daxian`/`liunian_taisui` 消失

重新生成夹具后出现的差异（**都不是本轮改动造成的**，是夹具原本就陈旧）：

| art | 差异 | 影响 |
|---|---|---|
| bazi | `shishen` 31→21、`yongshen` 3→1（caseA） | 引擎侧已变，夹具未跟 |
| liuren | 新增 `liuqin` 键 | 其他工作流新增的产出 |
| ziwei | **`daxian`、`liunian_taisui` 两个键整个消失** | 见下 |

**`daxian`/`liunian_taisui` 消失的实际后果**：11 个 ziwei 谓词叶子引用这两个键
（`daxian` 8 个、`liunian_taisui` 3 个，涉及 `ZIWEIDOUSHUQ-051`/-054/-055/-056、`-ZW-06`、`TAIWEIFU-020`），
在重生成后的样本里这些键不存在 → 三态给出 **「信息不足」**，即**这些规则当前永远无法满足**。

这正是三态设计要暴露的东西：**缺输入不伪装成「不满足」，也不伪装成命中**。
（按 P10 记录，`liunian_taisui` 曾由 `momentFacts + new Date()` 取当前年柱地支 —— 属**时钟相关**产出，
夹具因此不可跨日期复现；`daxian` 取自 `decadal.accent`。）**需产品侧确认这两个键的现状**，
本轮只登记，不擅自改引擎产出。

## 6. 未决清单

1. **`daxian`/`liunian_taisui` 的事实现状**（§5）：要么恢复产出，要么承认 11 个谓词叶子作废。
   建议产品侧确认；古籍仓不擅自改读数。
2. **fact-not-emitted 仍是最大块（277 → 217）**，剩余集中在：
   纳音取象（其余书，非六十甲子表）、神煞具体名 23、六爻月建日辰／变卦 36、
   奇门天盘干 25（**已确认 `QimenCell` 本就带 `sky`/`earth`，只是 `emitQimenFacts` 没接**——
   下轮最便宜的解锁）、六壬四课细节 4、七政格局行限 6。
3. **`nayin` 已入事实层但尚无谓词使用**：李虚中其余纳音取象条目、以及三命通会「论海中金」类，
   需按各自 statement 逐个判（不批量）。
4. **`fold_han` 不处理异体字**（§3.4）：影响 V11/V14 判据，建议单独一笔评估。
5. **夹具陈旧与时钟相关产出**（§5）：夹具应在产品侧稳定重生成，并考虑固定时刻。
6. t169 未决项仍在：189 条重述是否换成真引文、V11 111 vs G1 <50、25 条既有结构恒真映射。

## 7. 不变量与可复跑命令

不变量：不改 `statement`/`quote`/`anchor`/`verified*`；不新增 `value: "*"`；不硬锚；
不把未实现的救应写成没有救应；不生成让 `verified` 变 true 的自我认定。`verified: true` 全库 **0**。

本轮改动均经**字段级审计**：`applicable_to` 之外无任何字段变动（含 book block 与 rule set）。

```bash
cd /Users/sync/code/fateradar-classics

# 六十甲子映射（含自证断言）
python3 tools/map-nayin-ganzhi.py --dry-run      # 已映射后应报 0 条可映射
python3 tools/test-map-nayin-ganzhi.py           # 断言：反查序列 == 规范六十甲子

# 闸门（本轮全绿）
python3 tools/validate-rules.py                  # OK 55 file(s), 285 warning(s)
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 覆盖率与未映射
python3 tools/predicate-report.py                # bazi 47.0%
python3 tools/predicate-gap-report.py            # 521 条

# 三态求值（入参盘面状态 → 结论 + 置信度 + 出处）
python3 tools/eval-predicates.py --art bazi --case caseB -v | grep -A2 "LX-01"

# 导出与产品仓同步
python3 tools/export-rules.py                    # exported == anchored_exportable
```

产品仓（本机无 `bun`，用 `jiti` 跑 TS）：
`tests/fixtures/facts-sample.json` 由 `scripts/dump-facts.ts` 重生成；
`tsc --noEmit` exit 0；与本轮数据/契约相关的 8 个测试文件 69 项全绿。

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`0c991a01cabef60abb4928969fedd5fa70f9805e`**（本轮数据修订提交）。
不可写 `main`：锚点行号按该 commit 的 fulltext 分行算出。
产品仓 `src/lib/rules/generated/*.json` 已同步覆盖，`fact-vocab.json` 与 `vocab.ts` 一致。

**不得对外宣称「古籍已校勘」。** 电子文本匹配、模型审查与测试都不能代替人工影印核验。