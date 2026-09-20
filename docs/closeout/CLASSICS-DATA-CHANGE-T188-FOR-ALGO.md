# 消费方数据版本 · t188 奇门「X临Y」柱干类 6 条落地（qimen 72.5% → 87.5%）

日期：2026-09-21。基线提交：`de72b4f`（t187 后）。
**数据修订提交（请钉这个）：`6d6e21abd43c8b112c7a67ca5496b79e131f3477`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t173／t179／t184 一直把奇门「X临Y」柱干类记成「**最大的剩余块**，卡在跨键取值相等，
三选一都需授权或跨仓协调」。本轮换了一条**既不需要授权、也不需要新原语**的路：
**枚举有限域 ＋ 分支内配对**，把跨键相等写成精确谓词。

**qimen 72.5% → 87.5%**（29 → 35 条），未映射 **484 → 478**，
而且**全式无通配**（qimen 通配占比 13.8% → **11.4%**）。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| **qimen** | 7 (17.5%) | 24 (60.0%) | **35** | **87.5%** | **11.4%** | 8 |
| liuren | 11 (20.8%) | 11 (20.8%) | 15 | 28.3% | 6.7% | 5 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 22 | 31.9% | 13.6% | 6 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **484 → 478**。4 大门禁全绿；**32** 个 `tools/test-*.py` 全绿；
**三道谓词门禁全部 PASS（完整输出，exit 0）**；`coverage-report --fail-under 54` PASS。

## 2. 问题与办法

原文格表（`qimen-dunjia-tongzhi` L285–306）体例统一为「**X临Y**」＝天盘X压地盘Y：

```
大格 庚临六癸     刑格 庚临六己     小格 庚临壬      ← 固定干，t171 已映射
岁格 庚临岁干     月格 庚临月干     日格 庚临日干    ← 柱干，随盘而变
时格 庚临时干三奇  伏干 庚临日干     飞干格 日干临庚
地罗遮蔽 六壬临时干  天网四张 六癸临时干
```

固定干的（大格／刑格／小格）用 `{all_of:[{tianpan_gan:庚},{dipan_gan:癸}], same:gong}` 就够了，
t171 已落地。**柱干的那几条**要的是「**地盘干的取值 ＝ 某柱之干**」——跨键取值相等，
v3 的 `same` 只绑 **scope 字段**、不绑取值，写不出来。

**本轮的办法**：地盘干只取 **9 个值**（三奇六仪，无甲；中五不立），于是把等式**逐值配对**：

```yaml
applicable_to:
  any_of:
    - all_of:
        - all_of: [{key: gan, value: 庚, scope: {pillar: year}}]           # ① 岁干＝庚
        - all_of: [{key: tianpan_gan, value: 庚}, {key: dipan_gan, value: 庚}]
          same: gong                                                        # ② 天盘庚压地盘庚
    - … 丙丁戊己辛壬癸 共 9 支 …
```

### 2.1 为什么它是**精确**的，不是「枚举凑数」

- **精确**：每个分支把「柱干＝X」与「天盘A压地盘X」**配成一对**，等价于跨键相等。
- **不恒真**：要求天盘 A **恰好压在那个地盘干等于该柱之干的宫**上（`same: gong` 绑定）。
- 与 t168 撤回 `DITIANSUICHA-DR-07`（10 个 `rizhu` 穷尽值域 ⇒ 每盘成立）是**不同**东西：
  那里是**独立的或位枚举**，这里是**成对的分支**。

**实测**（合成盘）：

| 盘 | 结果 |
|---|---|
| 岁干＝庚，且**庚压庚** | **满足** |
| 岁干＝庚，但**庚压丙**（庚在场、压错地盘） | **不满足** ← 配对才是本质 |
| 三个样盘（caseA 岁干庚但庚压丙／caseB 岁干甲／caseC 岁干乙） | 均**不满足** |

因为三样盘都不成立，这 6 条**不会进入 `flat_rules`**，也就不会被
`--discrimination` 的 `domain_covering` 判据误报为「恒真」——这一点我特意查过。

### 2.2 如实披露

**柱干为甲时不表达**：地盘无甲（甲寄六仪）；「庚临值符」是**另一条**（QM-P31，t177 已映射）。
故按**子集**处理，并把该披露写进台账 `tools/reports/qimen-lin-pair-map.json`。

## 3. 落地 6 条

| rule | 原文 | 天盘干／柱位 |
|---|---|---|
| `QM-P27` 岁格 | 庚临岁干 | 庚／年 |
| `QM-P28` 月格 | 庚临月干 | 庚／月 |
| `QM-P29` 日格 | 庚临日干 | 庚／日 |
| `QM-P32` 伏干 | 庚临日干（与日格同文） | 庚／日（式同 P29） |
| `QM-P38` 地罗遮蔽 | 六壬临时干 | 壬／时 |
| `QM-P39` 天网四张 | 六癸临时干 | 癸／时 |

工具：`tools/map-qimen-lin-pairs.py`（幂等；判据必须命中 statement 才落盘；台账带
`applicable_to_yaml` 供跨提交审计比对）。

## 4. 顺带修掉自己测试里两条**已经过时**的断言

t187 刚记过「不要钉一条已不成立的结论」，本轮自己的测试里就有两条：

1. `QM-P27 仍为空（需跨键取值相等）` —— 现已映射。改为钉**新的事实**：
   已映射、且为枚举配对式、**全式无通配**。
2. `即使再加 QM-P26 也会超限（(wild+1)/(total+1) > 15%）` —— qimen 谓词数从 24 增到 35 后
   **闸门已有余量**，那条算术不再成立。改为**即时重算**并断言当前余量（<13%）。

> 同时把 `QM-P26`（直使加地丁）的**不映射理由**更正：它**不是**撞闸门，而是它必须写成
> 「值使门所在宫的地盘干＝丁」，其中值使门名随盘而变 → 需要**无取值子句**（存在性），
> 而「无取值子句算不算通配／算不算凑数」这条口径**尚未裁定**（t179 待授权项 ①）。

## 5. 未决清单（承接 t179／t184／t185／t187）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---:|---|
| ★1 | 奇门「X临Y」余项 | 2 | `QM-P30` 时格「庚临时干**三奇**」多一截口径（时干是否限乙丙丁）需判；`QM-P33` 飞干格是反向（天盘日干压地盘庚）——同一技术可做，但本轮未纳入 |
| 2 | `QM-P26` 直使加地丁 | 1 | 需**无取值子句**；「算不算通配」口径待裁定（不是撞闸门） |
| 3 | 六壬课体余项 | 2–4 | `DALIURENDAQU-007` 昴星引擎未实现；`LIURENZHIYIN-008` statement（返吟）与 quote（伏吟）不符，属人判 |
| 4 | 紫微命名格局 | 4 条 executable | 只差宫地支一笔 passthrough |
| 5 | 3 条无据 statement | 3 | 可解的人判项（t185：正文在 L7720–L7730，但与 statement 措辞不符） |
| 6 | 其余 | — | 沿用 t179：需授权（引擎投入、`daxian`）＋需人判（189 条重述、**25→64 恒真**、V11） |

**本轮把 t179 的「★1 需授权项」部分消解了**：那一块本来要「授权闸门判据／授权口径裁定／
跨仓实现语言 v4」三选一，现在用枚举配对绕开了——**既没动闸门，也没加原语**。

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-qimen-lin-pairs.py --dry-run     # 幂等
python3 tools/map-qimen-lin-pairs.py
python3 tools/test-map-qimen-stems.py              # 含「QM-P27 已映射且全式无通配」

# 语义（配对才是本质）
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("san-shi/qimen-dunjia-tongzhi",None)}
def f(k,v,**sc): return {"key":k,"value":v,"scope":sc,"derivedFrom":["test"]}
print("岁干庚+庚压庚 →", ev.evaluate(rules["QM-P27"],[f("gan","庚",layer="本命",pillar="year"),f("tianpan_gan","庚",layer="本命",gong=9),f("dipan_gan","庚",layer="本命",gong=9)])["verdict"])
print("岁干庚+庚压丙 →", ev.evaluate(rules["QM-P27"],[f("gan","庚",layer="本命",pillar="year"),f("tianpan_gan","庚",layer="本命",gong=4),f("dipan_gan","丙",layer="本命",gong=4),f("dipan_gan","庚",layer="本命",gong=9)])["verdict"])
PY

# 闸门（本轮全绿；**完整输出与 exit code，不要接 tail**）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 7. 给 cosmic 的版本钉

`CLASSICS_REV` = **`6d6e21abd43c8b112c7a67ca5496b79e131f3477`**。
产品仓 `generated/qimen.json` 已同步覆盖（35 条带谓词）；`tsc --noEmit` exit 0；
产品侧完整回归（带 `FATERADAR_CLASSICS`）**3539 passed / 0 failed**。

**给消费方的一条说明**：这 6 条的 `applicableTo` 是**嵌套组**：

```
any_of ─┬─ all_of ─┬─ all_of [gan@pillar, 取值为该柱之干]
        │          └─ all_of [tianpan_gan, dipan_gan]，same: gong
        └─ …（9 个分支，逐个地盘干取值）
```

求值器需支持「`same` 出现在内层 `all_of` 上、作用域仅该层」。这是 v3 既有语义
（t168 起 `same` 就是组字段），但**嵌套 + 内层绑定**是首次实际使用；
若产品侧 matcher 只处理顶层 `same`，需按此补齐。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。