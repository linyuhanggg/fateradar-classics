# 消费方数据版本 · t182 恒真映射口径更正：25 → **64**

日期：2026-09-21。基线提交：`2a21c32`（t181 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`da11267541a0fc500b96382e1d7b0bed004457d0`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

我此前**每一轮**未决清单里都写着「既有结构恒真映射 25 条」。
本轮证明**那个数字漏了一整类**，真数是 **64 条**。

起因很偶然：复核 human-review 的 `v14-low-correspondence` 时，看到
`FEIXINGZIWEI-008` 的谓词里有一句 `{key: ziwei_palace, value: 事业}`——
实测它在两个样本盘上都**满足**，而且命中的**正是这一句**。

根因：`--discrimination` 的 `hard` 档原只认两种形态——
**含通配 `*`**、或**把封闭值域整段覆盖**（如 10 个 `rizhu` 穷尽天干）。
它**漏了第三种**：在「**域完备键**」上只写**单个取值**。

## 1. 为什么会漏

`{key: ziwei_palace, value: 事业}` 看起来完全不像凑数：值域合法、只取一个值。
但引擎**每盘都产出全部十二宫（另加身宫标记）**，于是这条子句对**任何盘**都成立；
它若出现在**或位**（平铺列表成员，或某个 `any_of` 分支整体恒真），**整条规则就恒真**
——既没有筛选作用，又会把证据面板挤满。
这与 t168 撤回 `DITIANSUICHA-DR-07`（10 个 `rizhu` 穷尽值域）是**同一个后果，换了写法**。

## 2. 修法：补上第三档，并逐键核引擎证据

`eval-predicates.py` 新增 `DOMAIN_COMPLETE_KEYS`，**每个键都注明产出方式**（不是「样本里都出现」）：

| 键 | 为何域完备（已核产出代码） |
|---|---|
| `liuyao.liushen` | 六神按固定次序轮排六爻 → 6 神每盘齐 |
| `qimen.bamen` / `jiuxing` | 八门／九星固定布列八宫（中五寄坤，天禽随 `hostedStar`） |
| `ziwei.sihua` | 禄权科忌各落一星 → 4 化每盘齐 |
| `ziwei.ziwei_palace` | 十二宫恒在，另加「身宫」标记 |
| `liuren.sanchuan` | 三传恒有 → 初／中／末每盘齐 |

**有意不含** `bazi.shishen`、`qizheng.gongwei/xingyao/miaowang`：
它们虽在两个样本里恰好齐，但取值由**可变输入**派生（四柱十神、七政宫位），
**不足以判定结构完备**。宁可漏报也不误报——这类以 `sample_complete` 单列备查。

## 3. 更正后的登记册

`tools/tautology-register.py` → `tools/reports/tautological-mappings.json`：

| | 条数 |
|---|---:|
| **合计** | **64** |
| 域完备键上的单值子句（**新类**） | 42 |
| 通配 `*` | 20 |
| 整段覆盖值域 | 2 |

（旧口径 25 与新类 42 重叠 3 条 → 25 ＋ 42 − 3 ＝ 64。）

| art | 此前口径 | **更正后** |
|---|---:|---:|
| bazi | 17 | 17 |
| **ziwei** | **0** | **26** |
| qimen | 1 | 7 |
| liuren | 3 | 9 |
| liuyao | 3 | 4 |
| qizheng | 1 | 1 |

**ziwei 从 0 条变成 26 条**，这是本次更正最大的盲区。

## 4. 处置：只登记，不改规则

清理既有恒真映射**会下调既有覆盖率**（这些规则目前都算「已映射」），
故属 t179 §6「需人判 ⑥」，由人决定；机器不擅自改。
本轮**不改任何规则**，只把口径改对、把册子立起来、把测试钉上。

## 5. 测试（`test-tautology-register.py`，已入 CI）

| 断言 | 目的 |
|---|---|
| 册子与 `--discrimination` **现算**结果一致（条数与 `rule_id` 集合） | 快照不得自行过期 |
| `FEIXINGZIWEI-008` 判 `hard`，且给出的正是 `{ziwei_palace: 事业}` 且**无 scope** | 新形态确实被抓到 |
| `all_of` 内的同类子句**不**命中；`any_of` 分支整体恒真**才**命中 | 合取位不改变结论，不得误报 |
| 带 `scope` 的单值子句**不**命中 | 有位置限定就不是恒真 |
| `hard ≡ (通配 ∨ 整段覆盖 ∨ 域完备子句)` | **样本完备子句永不参与判定** |

> 最后一条是我自己写测试时踩到的：初版断言「含 `shishen` 子句者不得 hard」，
> 结果 `YUANHAIZIPIN-013` 报红——它**另有**通配 `{shishen: "*"}` 而 hard，
> 与 `shishen` 无关。正确的性质是「样本完备子句不参与 hard」，已改成不变量断言。

## 6. 未决清单（承接 t179／t181，仅改数字）

t179 的决策表仍然有效，**只有一处数字要更正**：需人判 ⑥ 从「25 条既有结构恒真映射」
改为 **64 条**（分类见 §3）。其余三项需授权、三项需人判不变。

需要强调的是：这 64 条**不影响**六术覆盖率数字（它们都算已映射），
所以「清理会下调覆盖率」这件事的分量比原先估计的更大。

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：恒真映射登记册与其测试
python3 tools/tautology-register.py            # 重新生成册子（期望 64 条）
python3 tools/test-tautology-register.py       # 五项断言，含 all_of 不误报
python3 tools/eval-predicates.py --art ziwei --discrimination   # 单术现算
python3 tools/eval-predicates.py --art ziwei --discrimination --json | \
  python3 -c "import json,sys; d=json.load(sys.stdin); print(sum(1 for r in d['flat_rules'] if r['hard']), 'hard')"
python3 -c "
import json; d=json.load(open('tools/reports/tautological-mappings.json'))
print(d['counts']); print('域完备键:', d['domain_complete_keys'])"

# 其余闸门（本轮全绿）
python3 tools/audit-contract.py
python3 tools/test-ledger-consistency.py
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
```

## 8. 给 cosmic 的版本钉

**本轮无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 零改动），
`CLASSICS_REV` **不变** = `da11267541a0fc500b96382e1d7b0bed004457d0`。
六术覆盖率不变：bazi 49.4%／ziwei 67.7%／qimen 67.5%／liuren 22.6%／liuyao 31.9%／qizheng 24.4%。

**给消费方的一条实用提醒**：这 64 条规则对**每一张盘**都返回「满足」。
产品侧若要按规则命中来组织证据面板，建议先按
`tools/reports/tautological-mappings.json` 过滤这批规则，
否则它们会常驻面板占位（这也是「清理会下调覆盖率」之外的另一层理由）。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。