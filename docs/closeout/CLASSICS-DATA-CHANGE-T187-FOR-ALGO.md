# 消费方数据版本 · t187 六壬课体三条落地 · 补齐缺失样盘 · 更正 t186 的门禁误报

日期：2026-09-21。基线提交：`a39501c`（t186 后）。
**数据修订提交（请钉这个）：`c8a887236e55d7d16f04f736566bbe4fccc00d8e`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

三件事：**liuren 22.6% → 28.3%**（伏吟／返吟／八专三条落地）、
**补齐缺失样盘**使两道门禁真正变绿、
以及**更正 t186 的门禁误报**——t186 报的「三道谓词门禁 PASS」是错的，
真实情况是其中两道在 FAIL，而我没看见，因为**用 `tail -3` 截断了输出**。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 29 | 72.5% | 13.8% | 8 |
| **liuren** | 11 (20.8%) | 11 (20.8%) | **15** | **28.3%** | **6.7%** | 5 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 22 | 31.9% | 13.6% | 6 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **487 → 484**。三道谓词门禁 **全部 PASS（exit 0，完整输出见 §3）**；
**32** 个 `tools/test-*.py` 全绿；`coverage-report --fail-under 54` PASS。

## 2. 落地：六壬课体三条

引擎按取传结果定**课体名**（`liuren-transmissions.ts`），而 `keti` 事实层早就产出它；
既有映射也已经这么写（`DALIURENDAQU-006` 蒿矢/弹射、`LIURENZHIYIN-017` 元首/重审）。

| rule | 原文 | 谓词 |
|---|---|---|
| `DALIURENDAQU-010` | 伏吟有克还为用，无克刚干柔取辰 | `[{key: keti, value: 伏吟课}]` |
| `DALIURENDAQU-011` | 返吟有克亦为用，无克别有井栏名 | `[{key: keti, value: 返吟课}]` |
| `LIURENZHIYIN-009` | 八專以逆順為真 | `[{key: keti, value: 八专课}]` |

**为什么忠实**：「伏吟／返吟／八专」在原文里既是**课体名**也是**条件**——
adapter 的 `is_fuyin`／`is_fanyin`／`is_bazhuan` 判的就是这些；引擎在
「月将支与占时支同位／相冲」「干支同位」时分别定这三课，与原文的成因一致。

**实测**（7 个样盘）：caseB 课体=伏吟课 → `DALIURENDAQU-010` **满足**，
其余六盘（元首／重审／弹射／蒿矢／涉害）均**不满足**；返吟／八专在本批样盘上不成立
（故另补样盘，见 §3）。

## 3. 更正 t186 的门禁误报（我的过程错误，两处根因也是我的）

t186 我写「三道谓词门禁 PASS」。**那是错的**：`--check-open-values` 与 `--check-art-keys`
当时都在 FAIL，而我没看见 —— 因为命令末尾用了 `tail -3`，把 FAIL 行和退出码一起截掉了。

两处根因都在 t186 自己的补丁里：

1. **`--check-art-keys`**（`QM-P36 key='gan' not in emit.ts`）：
   补丁锚在第一个 `"geju_qimen",` 上 —— 而那一处在 **`OPEN_KEYS`** 而不是
   `ART_EMIT_KEYS["qimen"]`。后果有两层：qimen 的 emit 集**始终没拿到 `gan`/`zhi`**（QM-P36 报红）；
   同时 `gan`/`zhi` 被误加进 `OPEN_KEYS`，导致大批 bazi 规则因 `zhi='辰'` 等不在两盘样本里而报红。
   → 已还原 `OPEN_KEYS`，并把 `gan`/`zhi` 正确加进 qimen 的 emit 集（两份报告脚本同步）。
2. **`--check-open-values`**（`QM-P15 geju_qimen='反吟局'`）：这条**自 t171 起就在 FAIL**，
   不是本轮才有的 —— 同样被我历轮的截断输出盖住了。

**修法是补样盘，不是放宽闸门**：由遍历日期/时辰找出真实输入（都由完整日期排盘生成），
加进 `scripts/dump-facts.ts`：

| 新样盘 | 输入 | 用途 |
|---|---|---|
| qimen `caseC` 反吟局 | 2026-01-01 11:00 | 让 `geju_qimen='反吟局'`（QM-P15）有盘可证 |
| liuren `caseH` 返吟课 | 2026-01-01 13:00 | 让 `keti='返吟课'` 有盘可证 |
| liuren `caseI` 八专课 | 2026-02-02 01:00 | 让 `keti='八专课'` 有盘可证 |
| liuren `caseJ` 别责课 | 2026-01-23 03:00 | 六壬开放课体覆盖（引擎产出但此前无盘） |

**现三道门禁完整输出**：

```
PASS wildcard ≤ 15%
PASS open-values
PASS art-keys
exit=0
```

> **两条教训**（写下来免得再犯）：
> ① **门禁输出不得截断** —— 我要看的是 exit code 与 FAIL 行，不是「最后三行」；
> ② **锚点必须选目标处独有的字符串** —— `"geju_qimen",` 在两个常量里都出现。

## 4. 试过但**撤回**的一个收紧：`keti` 闭域

本轮本想借机给 `keti` 加**闭域**（12 个课体名），好让 V16 直接校验笔误。产品测试立刻报红：

`src/lib/rules/quarantine.ts` 里的**隔离规则正当地引用了「昴星课」**，而引擎**并不产出**该值
（那正是它们被隔离的原因）。闭域等于宣称「引擎能产出该值」，与事实不符。

→ **撤回闭域**（三处 vocab 同步还原为 `keti: []`）。取值安全改由
`--check-open-values`（取值须在样盘中出现过）＋ §3 新增的样盘共同保证。

这算一条产品契约对古典侧的反向约束：**隔离规则可以命名引擎尚未实现的值**，
所以「引擎能产出的值域」不能拿来当这些规则的合法性判据。

## 5. 产品侧一处**与本次无关**的既有失败（供参考，不由我改）

`tests/engine/tiaohou-rescue.test.ts` 假定经典仓在**同级目录 `../classics`**，
而实际是 `../fateradar-classics`：

```
Error: 无法定位含调候 pin 83c654b9638d9b75f8c26cbb9ea5f3825b077d15 的经典仓；
       设 FATERADAR_CLASSICS 或提供同级 classics 工作树。
```

该 pin **确实存在**（是 classics HEAD 的祖先）。设 `FATERADAR_CLASSICS=/Users/sync/code/fateradar-classics`
后 **12/12 通过**。属产品侧路径/配置问题。

**本次产品侧完整回归（带该环境变量）**：**3539 passed / 9 skipped / 0 failed**，
`tsc --noEmit` exit 0。

## 6. 未决清单（承接 t179／t184／t185／t186）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---:|---|
| ★1 | 奇门「X临Y」块 | **8**（qimen 72.5%→~90%） | 事实已齐（t186），只差「跨键取值相等」：三选一（授权闸门判据／授权口径裁定／语言 v4＋跨仓协调） |
| 2 | 六壬课体余项 | 2–4 | `DALIURENDAQU-007`（昴星）引擎未实现；`LIURENZHIYIN-008` 的 quote 讲伏吟而 statement 写返吟——**statement↔quote 不符**，属人判 |
| 3 | 紫微命名格局 4 条记录 | 4 条 executable | 只差宫地支一笔 passthrough |
| 4 | 3 条无据 statement | 3 | 可解的人判项（t185：正文在 L7720–L7730，但与 statement 措辞不符） |
| 5 | 其余 | — | 沿用 t179：需授权（引擎投入、`daxian`）＋需人判（189 条重述、**25→64 恒真**、V11） |

**新增待办（本轮发现）**：`LIURENZHIYIN-008` 的 statement 说「十二神各临冲位（返吟）」，
而其 quote 引的是「若諸神歸於本位…乃伏吟之象也」——**两者不符**。
按 t173／t185 的口径，这类应进「statement↔原文不符」的登记，而不是照 statement 映射。

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-fixed-values.py --dry-run      # 幂等
python3 tools/test-map-fixed-values.py           # 8 条台账
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
#   ↑ 必须看**完整输出与 exit code**，不要接 tail —— t186 的误报就是这么来的

# 新样盘确实覆盖了那些取值
python3 -c "
import json
d=json.load(open('tools/reports/facts-sample.json'))
print('qimen 格名:', [ [f['value'] for f in c['facts'] if f['key']=='geju_qimen'] for c in d['qimen'].values()])
print('liuren 课体:', [ [f['value'] for f in c['facts'] if f['key']=='keti'] for c in d['liuren'].values()])"

# 落地三条的语义
python3 tools/eval-predicates.py --art liuren --case caseB -v | grep -A2 "DALIURENDAQU-010"
python3 tools/eval-predicates.py --art liuren --case caseH -v | grep -A2 "DALIURENDAQU-011"
python3 tools/eval-predicates.py --art liuren --case caseI -v | grep -A2 "LIURENZHIYIN-009"

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`c8a887236e55d7d16f04f736566bbe4fccc00d8e`**。
产品仓 `generated/liuren.json` 已同步覆盖（15 条带谓词）；
`tsc --noEmit` exit 0；产品侧完整回归 **3539 passed / 0 failed**。

**两条给消费方的提醒**：
1. 跑 `tests/engine/tiaohou-rescue.test.ts` 需要 `FATERADAR_CLASSICS` 指向经典仓
   （测试内假定同级目录名是 `../classics`，与实际不符）。
2. 隔离规则（`src/lib/rules/quarantine.ts`）**可以**命名引擎尚未产出的取值（如 `keti=昴星课`）；
   古典侧**不会**把这类值写进 `fact-vocab` 的值域——闭域只表达「引擎能产出什么」。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。