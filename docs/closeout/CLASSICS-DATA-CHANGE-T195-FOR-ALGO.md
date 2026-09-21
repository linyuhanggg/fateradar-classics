# 消费方数据版本 · t195 藏干入事实层 · 透干两条（bazi 49.4% → 49.9%）· 修正覆盖判据误报

日期：2026-09-21。基线提交：`f514fc8`（t194 后）。
**数据修订提交（请钉这个）：`e27a07ff51e0808eba9ce9466e8bcdba96650c42`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

三件事：**藏干入事实层**（`canggan`）、**透干两条落地**（bazi **49.4% → 49.9%**），
以及**修正我自己判别工具的一个假阳性** —— 后者比前两件更重要。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| **bazi** | 143 (31.9%) | 211 (47.0%) | **224** | **49.9%** | 7.1% | 10 → **11** |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | 90.0% | 11.1% | 8 |
| liuren | 11 (20.8%) | 11 (20.8%) | 15 | 28.3% | 6.7% | 5 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 27 | 39.1% | 11.1% | 9 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **472 → 470**。4 大门禁全绿；**33** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用扫描 **0 处**；
`coverage-report --fail-under 54` PASS；产品侧 **3545 passed / 0 failed**，`tsc` exit 0。

## 2. 藏干入事实层

`calendar.ts` 的 `PillarFact.hidden` **本就注明「藏干，本气在前」**，
而 `emitBaziFacts` **早就在读它算十神** —— 只是没把藏干本身当事实产出。
本轮逐柱产出 `canggan`（值域＝十天干）。与 t170／t178／t186／t193 是同一路子：
**数据在引擎里，事实层没暴露**。

## 3. 透干两条

原文（三命通会／渊海子平同说）：

> 月令所藏天干分本气、中气、余气，按节气分日数分配司令；
> **取格优先看本气透干，本气不透看中气、余气**。

「透干」＝某个藏干**也出现在天干上**（藏与透同值）→ 又是跨键取值相等。
用**枚举十天干**配对写：

```yaml
any_of:
  - all_of: [{key: canggan, value: 甲, scope: {pillar: month}}, {key: gan, value: 甲}]
  - … 十支 …
```

第二句**不带 scope**（任一天干皆可）；**全域无通配、无 `same`**。

**适用范围**取「月令藏干有透干者」——该条所处理的那局面（本气透或中气余气透）；
「完全无透干」不在本式内，属**子集**，已在台账披露。

**实测**：两样盘均满足（都有月令藏干透干）；
合成「月令藏辛 ＋ 天干辛」→ **满足**、「月令藏辛 ＋ 天干甲」→ **不满足**（配对是本质）。

## 4. 修正判别工具的假阳性（本轮最重要的一件）

新映射一落地，`--discrimination` 立刻把它们判成 `hard=True`，判据是
`covering=['gan','canggan']` —— **假阳性**：那两个键的取值在十支里是**成对**出现的
（`gan:X` 配 `canggan:X`），**覆盖整个值域并不等于恒真**。

这正是我在 t188 的设计注释里预警过的形状（当时 qimen 那批因为不被样盘满足而没触发）。

**修法**：旧版把「覆盖」判在**整个表达式**上；现在只在下面这种形状才判恒真 ——
**或位的每个备选各自只约束同一个键**（同名、不写 scope），且各支取值合起来覆盖该键值域。
例如 10 个 `rizhu` 穷尽天干（t168 撤回的 `DR-07` 就是这一形状）、5 个 `liuqin` 穷尽六亲。

**双向验证**：

| 规则 | 形状 | 判定 |
|---|---|---|
| `SANMINGTONGH-R-02`／`YUANHAIZIPIN-008` | 十支**成对**约束两个键 | `hard=False` ✓（误报消除） |
| `HZL-R007`／`ZENGSHANBUYI-ZR-10` | 平铺枚举**全部五个六亲** | 仍 `hard=True` ✓（真阳性保留） |

**恒真登记册仍为 64 条**（`domain-complete 42 / wildcard 20 / domain-covering 2`）——
真阳性一条没少。

## 5. 顺带：词表改由引擎生成

`facts.test.ts` 报「committed vocab json 与引擎表不符」，根因是**键的顺序**：
我手改 JSON 把 `canggan` 插在 `gan` 之后，而引擎的 `FACT_KEYS` 把它排在 `liuyao_seq` 之后。

改为用引擎自己的 `toFactVocabJson()` 生成两份 `fact-vocab.json`
（古籍仓与产品仓**完全一致**，共 47 键）——从此不再手改，顺序也不会再漂。

## 6. 未决清单（承接 t179／t192／t194）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---|--|
| ★1 | 八字**化气/有根**类（`DITIANSUICHA-045`、`SANMINGTONGH-013`、`DITIANSUICHA-024`） | 3 | `canggan` 已就位，但仍需**五行关系**（化神当令、有根＝藏干五行与日主同类）＋冲克判定 |
| 2 | 六爻用神×旺衰/关系类（`HJC-R004/005`、`ZENGSHANBUYI-013`、`ZR-05`） | 4–6 | 需关系判定；其中数条其实是**通则/断法**，其 `fact-not-emitted` 分类本身待复核 |
| 3 | 六爻余项（回头生克、旬空、反吟伏吟、用神两现计数） | 若干 | 引擎已算未产出的分类（旬空／反吟伏吟）或需计数语义 |
| 4 | `QM-P30` 时格「庚临时干三奇」／`QM-P26` 直使加地丁 | 各 1 | 原文两读不猜／需无取值子句（口径待裁定） |
| 5 | 六壬课体余项 / 紫微命名格局 / 3 条无据 statement | 2–4 / 4 / 3 | 沿用 t187／t183／t185 |
| 6 | 其余 | — | 需授权（引擎投入）＋需人判（189 条重述、**25→64 恒真**、V11） |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-bazi-tougan.py --dry-run       # 幂等
python3 tools/map-bazi-tougan.py
python3 tools/tautology-register.py               # 仍 64 条（真阳性未削弱）
python3 tools/test-tautology-register.py

# 语义（配对是本质）
python3 - <<'PY'
import json,sys,importlib.util
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
rules={r["rule_id"]:r for r in ev.load_rules("bazi/sanming-tonghui",None)}
d=json.load(open("tools/reports/facts-sample.json"))["bazi"]
for case,c in d.items(): print(case, ev.evaluate(rules["SANMINGTONGH-R-02"], c["facts"])["verdict"])
def f(k,v,**sc): return {"key":k,"value":v,"scope":sc,"derivedFrom":["test"]}
print("藏辛+干辛 →", ev.evaluate(rules["SANMINGTONGH-R-02"], [f("canggan","辛",layer="本命",pillar="month"), f("gan","辛",layer="本命",pillar="year")])["verdict"])
print("藏辛+干甲 →", ev.evaluate(rules["SANMINGTONGH-R-02"], [f("canggan","辛",layer="本命",pillar="month"), f("gan","甲",layer="本命",pillar="year")])["verdict"])
PY

# 判据双向验证（假阳性消除 / 真阳性保留）
python3 -c "
import json,subprocess
for art,ids in (('bazi',('SANMINGTONGH-R-02','YUANHAIZIPIN-008')),('liuyao',('HZL-R007','ZENGSHANBUYI-ZR-10'))):
    d=json.loads(subprocess.run(['python3','tools/eval-predicates.py','--art',art,'--discrimination','--json'],capture_output=True,text=True).stdout[d and 0:] if False else subprocess.run(['python3','tools/eval-predicates.py','--art',art,'--discrimination','--json'],capture_output=True,text=True).stdout)
    for r in d['flat_rules']:
        if r['rule_id'] in ids: print(art, r['rule_id'], 'hard=', r['hard'], 'covering=', r['domain_covering'])"

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/dead-reference-report.py
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`e27a07ff51e0808eba9ce9466e8bcdba96650c42`**。
产品仓 `generated/bazi.json` 已同步覆盖（224 条带谓词）；
两仓 `fact-vocab.json` **完全一致**（47 键，由引擎 `toFactVocabJson()` 生成）；
`tsc --noEmit` exit 0；产品侧 **3545 passed / 0 failed**。

**给消费方的一条提醒**：`canggan`（藏干）是**逐柱、可多个**的事实，
且 `calendar.ts` 约定「**本气在前**」——若你的取值聚合依赖顺序，
请注意事实列表本身的顺序**不承载**该语义（本仓只在 `derivedFrom` 里记来源）；
需要「本气」时请按该约定取首次出现，或等本仓另立专门键。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。