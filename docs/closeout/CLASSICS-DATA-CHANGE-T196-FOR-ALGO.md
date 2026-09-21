# 消费方数据版本 · t196 六壬四柱干支入事实层 · liuren 28.3% → 30.2% · 合并状态复核

日期：2026-09-21。基线提交：`0783940`（t195 后）。
**数据修订提交（请钉这个）：`224604f446a73262a217f9dad3e645d2158a0e05`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

两件事：**六壬四柱干支入事实层**（与 t186 给奇门的那笔同形）并据此落地
`DALIURENDAQU-009`（**liuren 28.3% → 30.2%**）；以及一次**合并状态复核**
（上次是 t179，已隔 8 轮）。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 224 | 49.9% | 7.1% | 11 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| qimen | 7 (17.5%) | 24 (60.0%) | 36 | **90.0%** | 11.1% | 8 |
| **liuren** | 11 (20.8%) | 11 (20.8%) | **16** | **30.2%** | **6.2%** | 5 → **7** |
| liuyao | 21 (30.4%) | 21 (30.4%) | 27 | 39.1% | 11.1% | 9 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **470 → 469**。4 大门禁全绿；**33** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；死引用扫描 **0 处**；
`coverage-report --fail-under 54` PASS；产品侧 **3545 passed / 0 failed**，`tsc` exit 0。

## 2. 六壬四柱干支 + DALIURENDAQU-009

`facts.ganZhi` 本就有（引擎用它起课），`emitLiurenFacts` 只是没把它当事实产出 ——
与 t186 给奇门、t195 给八字藏干是同一路子。逐柱产出 `gan`/`zhi`
（与 bazi／qimen **共用键**、按 `scope.pillar` 区分；V16 只校验取值，不限定术）。

`DALIURENDAQU-009`「日柱属于癸丑、甲寅、丁未、己未、庚申，**且**干支同位形成两课结构」：
条件的一半就是**日柱**等于列举之一 → 用 t176 的显式柱位枚举对落地。
**子集**：「干支同位形成两课结构」是**四课去重结果**（引擎未产出），已如实披露。

**实测（十盘）**：只有 caseI（日柱 **丁未**）→ **满足**，其余九盘不满足 —— 有区分度。

## 3. 合并状态复核（上次 t179，已隔 8 轮）

未映射 **469** 的构成：

| 理由类别 | 条数 | 性质 |
|---|---:|---|
| `not-a-condition` | **231** | 通论／体例／取象表／起例取法 —— **契约上永久留空** |
| `fact-not-emitted` | **168** | 需要引擎未产出的事实（**t173 时是 201**） |
| `condition-too-vague` | 35 | 原文有条件但口径未定，或原文自己拒绝单一条件断 |
| `meta-rule` | 35 | pack 元规则／调用条件 —— **永久留空** |

- **契约上永久留空 266 条（231＋35）＝ 57%**。覆盖率的**分母天然含这一块**——
  这是本库的性质，不是施工欠账；有讨论余地的只有 **203 条**。
- `fact-not-emitted` 从 **201 → 168**：t175–t196 的施工把 **33 条**从这一桶里拿走。

| art | 未映射 | 其中 fact-not-emitted |
|---|---:|---:|
| bazi | 225 | ~72 |
| qizheng | 65 | 12 |
| liuyao | 42 | ~25 |
| liuren | 37 | 16 |
| meihua（参考） | 33 | 21 |
| yili（参考） | 33 | 6 |
| ziwei | 30 | 11 |
| **qimen** | **4** | **2** |

**奇门只剩 4 条**（90.0%），其中 2 条各有口径问题（§4 ★1／2）、其余属 not-a-condition 等。

## 4. 未决清单（本轮合并更新）

| # | 事项 | 值多少条 | 卡在哪 | 谁 |
|---|---|---|--|--|
| ★1 | `QM-P30` 时格「庚临时干**三奇**」 | 1 | 「三奇」两读：限定时干∈乙丙丁，还是另要三奇得使 | **人判**（原文两读，不猜） |
| 2 | `QM-P26` 直使加地丁 | 1 | 需**无取值子句**；「算不算通配／凑数」这条口径尚未裁定 | **需授权** |
| 3 | 六爻**用神×旺衰/关系**类（`HJC-R004/005`、`ZENGSHANBUYI-013`、`ZR-05`） | 4–6 | 需**关系判定**（生克冲合/墓/克破）；其中数条是通则/断法，其 `fact-not-emitted` 分类本身待复核 | 混合 |
| 4 | 八字**化气/有根**类（`DITIANSUICHA-045`、`SANMINGTONGH-013`、`DITIANSUICHA-024`） | 3 | `canggan` 已就位，但仍需**五行关系**（化神当令、有根）＋冲克 | 混合 |
| 5 | 六爻余项（回头生克、旬空、反吟伏吟、用神两现计数） | 若干 | 引擎已算**未产出**的具名分类（旬空／反吟伏吟）或需**计数**语义 | 引擎／语言 |
| 6 | 六壬四课（`DALIURENDAQU-007/008`、`LIURENZHIYIN-004`） | 3 | 引擎有 `ke4`（四课）但未产出；且需**上下直接克/遥克**关系 | 引擎 |
| 7 | 八字神煞名（关煞/元辰/德秀…） | 30 | 需在 `shensha.ts` 补约 20 项**取法** | 引擎（工作量大） |
| 8 | 梅花体用生克 | 21 | 本仓**无梅花事实层**；产品引擎有体用五行，可照 t170–t196 的路子补 | 引擎 |
| 9 | 六壬课体余项 / 紫微命名格局 / 3 条无据 statement | 2–4 / 4 / 3 | 沿用 t187／t183／t185 | 混合 |
| 10 | **189 条重述是否换真引文**、**25→64 恒真映射是否清理**、V11 111 vs G1 <50 | — | 都会改数据或下调覆盖率 | **人判** |

**t179 那张表里的「需授权★1」（奇门「X临Y」块，值 8 条）已在 t188／t189 消解** ——
用枚举配对写出来了，既没动闸门也没加原语。

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-fixed-values.py --dry-run       # 幂等；现 11 条
python3 tools/test-map-fixed-values.py
python3 tools/eval-predicates.py --book san-shi/daliuren-daquan --case caseI -v | grep -A2 "DALIURENDAQU-009"

# 合并状态（§3 的数字来源）
python3 tools/predicate-gap-report.py --json > /tmp/g.json
python3 - <<'PY'
import json
from pathlib import Path
from collections import Counter
rows=json.load(open('/tmp/g.json'))['rows']
led={}
for f in Path('tools/reports/predicate-decisions').glob('*.json'):
    if 'captain-audit' in f.name: continue
    for x in json.load(f.open())['decisions']: led[(x['book'],x['rule_id'])]=x
c=Counter((led.get((r['book'],r['rule_id'])) or {}).get('reason_class') or '未复核' for r in rows)
print('未映射', len(rows), dict(c))
print('按术', dict(Counter(r['art'] for r in rows)))
print('永久留空', c.get('not-a-condition',0)+c.get('meta-rule',0))
PY

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

## 6. 给 cosmic 的版本钉

`CLASSICS_REV` = **`224604f446a73262a217f9dad3e645d2158a0e05`**。
产品仓 `generated/liuren.json` 已同步覆盖（16 条带谓词）；`tsc --noEmit` exit 0；
产品侧 **3545 passed / 0 failed**。

**给消费方的一条提醒**：`gan`／`zhi` 现在是**跨三术**的共用键
（bazi＝四柱、qimen＝四柱、liuren＝四柱），语义一致、按 `scope.pillar` 区分。
若你的检索或面板按 key 聚合，请按 art 或按 `scope.pillar` 分开处理。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。