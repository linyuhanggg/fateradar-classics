# 消费方数据版本 · t202 低对应度档位分诊：字符串方法判不了锚点，产出人眼读单

日期：2026-09-21。基线提交：`ca33d46`（t201 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`aba931afe78fcc7fec2b0f350eff5b35ea442d9e`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

本轮去碰 `needs-human-review` 里的 `v14-low-correspondence`／`p6-grey-zone` 两档。
**结论是负面的、但有用**：这两档**不是可机器推进的档位**——
对应度是**汉字集合召回率**，而字符串方法（单字、二元组我都试过）**判不了锚点对不对**。
产出改为**人眼读单**（40 条），并把我自己**两次被实读推翻**的过程记进台账。

## 1. 先看这一档有多大

全库有 statement + quote 的规则 **1356** 条，对应度分布：

| 档位 | 条数 |
|---|---:|
| **< 0.15** | **205** |
| 0.15–0.30（P6 灰区） | 242 |
| 0.30–0.50 | 234 |
| ≥ 0.50 | 675 |

## 2. 我走了两步，**两次都被实读推翻**（本轮最该记的一条）

### 第一步：单字分诊 → 报出一个「锚点错位」，实读是巧合

单字版报出：

> ⚠ `GUOTIANJING-007` anchor 疑应移到同文件 L7891（内容字覆盖 0.52）

**读过去发现**：L7891 一带讲的是「入庙、乘旺、乐宫、喜宫、殿垣、度数、合格」，
而 statement 是「**童限**自婴幼期起按古歌分配各宫」——**毫无关系** ✗。

原因：**单字集合在中文里几乎必然重叠**（星／宫／之／分…），0.52 是常用字造成的巧合。

### 第二步：改用二元组 → 仍有 9 条「另有更匹配窗口」，实读多半也不是错位

二元组把分布洗成 `no-overlap-anywhere` 23 / `higher-overlap-window-found` 9 / `near-anchor` 8，
但那 9 条逐条读过去，多半是**韵语引文 vs 白话归纳**造成的结构性低重叠
（例如 `DALIURENDAQU-010` 的引文「伏吟有克还为用…」与 statement 讲的**正是**伏吟）——不是锚点错位。

### 结论

**字符串方法（单字／二元组）判不了锚点对不对。** 于是本工具**降格**：
只做**分诊线索 + 人眼读单**，三类标签在文件头与输出里都明确标注「只是线索，不可当判定」。

## 3. 产出（不改任何受保护字段）

| 文件 | 内容 |
|---|---|
| `tools/low-correspondence-triage.py` | 列出「对应度 < 0.05」的规则及 anchor／引文／statement 摘要；**statement／quote／anchor 一律不动** |
| `tools/reports/low-correspondence-triage.json` | 40 条读单 ＋ 方法说明 ＋ 自我推翻的记录 |
| `tools/test-low-correspondence.py` | 入 CI：钉读单成形、钉「no-overlap 占多数」这一结论、**反例**证明二元组非恒真 |

**读单分布**：相法 `shenxiang-quanbian` 10、紫微全鉴 5、大六壬 3、果老星宗 3、滴天髓阐微 2、沈氏玄空 2…

那 23 条「三处都无重叠」的，多半是**现代归纳／包级声明**（不是书中原句），
例如「原书列富格／贵格／寿相格…本 pack 仅作…」「本 pack 是公开网页转写层…」。

## 4. 对 needs-human-review 的建议

`v14-low-correspondence` 与 `p6-grey-zone`：

- **不建议**继续用字符串指标推；
- 两条路：① 改用**语义方法**（需模型判断，属另一类投入）；② 把人眼成本压到最小——
  直接用这份 **40 条读单**（比原来的 205/242 条小一个量级）。
- 无论走哪条，**anchor 由人改**；机器不硬锚（本仓一贯纪律）。

## 5. 未决清单（承接 t201）

| # | 事项 | 变化 |
|---|---|---|
| 1 | `v14-low-correspondence`／`p6-grey-zone` | **本轮查证：不可机器推进**；改交 40 条人眼读单（或改用语义方法） |
| 2 | 余 38 条未被样盘演示 | 37 目录式（结构性自证）＋ 1 条 `TAIWEIFU-010`（可换网格再搜） |
| 3 | 六壬「遥克／四课去重」2 条 | 引擎有遥克候选逻辑但未产出 |
| 4 | 六爻用神×关系、八字化气/有根 7–9 条 | 需五行**关系**判定（写成谓词会爆炸） |
| 5 | 八字神煞 30 条 | t201 已改判：横跨三套神煞体系，不是可做的块 |
| 6 | `ZENGSHANBUYI-025` 反吟／伏吟；`QM-P30`「三奇」两读；`QM-P26` 无取值子句 | 各 1–2 条，卡在罕见结构／原文两读／口径待裁 |
| 7 | 需人判 | 189 条重述换真引文、**25→64 恒真映射清理**、V11 111 vs G1 <50 |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/low-correspondence-triage.py                 # 40 条读单（线索标签）
python3 tools/low-correspondence-triage.py --write         # 写入台账
python3 tools/test-low-correspondence.py                   # 读单成形 + 结论 + 反例

# 两档多大（对应度分布）
python3 - <<'PY'
import importlib.util, yaml, sys
from pathlib import Path
spec=importlib.util.spec_from_file_location("vr","tools/validate-rules.py"); vr=importlib.util.module_from_spec(spec); sys.modules["vr"]=vr; spec.loader.exec_module(vr)
from collections import Counter
band=Counter()
for p in Path("references/books").glob("*/*/rules.yaml"):
    for r in (yaml.safe_load(p.read_text()) or {}).get("rules") or []:
        if isinstance(r,dict) and r.get("statement") and r.get("quote"):
            c=vr.correspondence(r["statement"], r["quote"])
            band["<0.15" if c<0.15 else "0.15-0.30" if c<0.30 else "0.30-0.50" if c<0.50 else ">=0.50"]+=1
print(dict(band))
PY

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

## 7. 给 cosmic 的版本钉

**无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 未变），
`CLASSICS_REV` **不变** = `aba931afe78fcc7fec2b0f350eff5b35ea442d9e`；产品仓无需重新导出。
六术覆盖率不变；验证深度不变（341/379 = 90%）。

**给消费方的一条提醒**：`correspondence()` 只是**汉字集合召回率**，
**不要**把它当「引文是否支持命题」的判据——本仓已用实读证明它会把
「韵语引文 + 白话归纳」和「表格型引文 + 概括陈述」判成低对应度。
若产品侧也用它排序或过滤，会得到同样的误报。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。