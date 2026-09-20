# 消费方数据版本 · t181 判定台账与规则实况对齐（97 条脱节）＋一致性闸门

日期：2026-09-21。基线提交：`39a979e`（t180 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`da11267541a0fc500b96382e1d7b0bed004457d0`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

t180 审计了「施工有没有越界改原文」；本轮审计**账本有没有跟上施工**——
新加的一致性闸门一上来就抓到 **97 条台账与规则实况不符**：

- **92 条**写 `unmapped`，而规则**其实已有谓词**（t170–t178 所映射，台账没跟着改）；
- **5 条**写 `mapped`，而规则**其实是空的**（t168 复核撤回项）。

台账是「每条未映射规则为什么没映射」的唯一账本，也是 t179 那张决策表的数字来源，
此前却没有任何东西检查它是否与实况相符。本轮全部对齐，并留下闸门防复发。

## 1. 为什么这件事重要

t173 我给 `predicate-gap-report.py --fact-gaps` 加过一句「**已按 live `applicable_to` 过滤**」，
当时写的是「台账是过程记录，t170／t171 已映射的条目仍写着 fact-not-emitted，
不过滤会把已完成的算成待办」。

**那只是绕过症状。** 本轮把账本本身治了：条目现在会随施工一起更新，
并且由测试保证「台账不得声称映射了空规则，反之亦然」。

数字层面的影响：t179 §2 那张表我把 5 条列为「未复核（台账缺条目）」，
实际情况是这 5 条**就是复核撤回项**、理由类别为 `not-a-condition`。更正后：

| 理由类别 | t179 原表 | **更正后** |
|---|---:|---:|
| `not-a-condition` | 226 | **231** |
| `fact-not-emitted` | 188 | 188 |
| `condition-too-vague` | 35 | 35 |
| `meta-rule` | 35 | 35 |
| 未复核（台账缺条目） | 5 | **0** |
| **合计** | **489** | **489** |

「契约上永久留空」合计 **266**（231 ＋ 35）＝ 54%，比原来的 261 更高一点。
**未映射总数 489 不变**，六术覆盖率不变。

## 2. 两类脱节的处置

### 2.1 92 条「写着 unmapped，其实已映射」

逐条改为 `decision: "mapped"`，并补两个字段：

- `mapped_by`：**出处台账文件**（`nayin-ganzhi-map.json` 60 条、`qimen-stem-map.json`、
  `branch-group-map.json`、`fixed-value-map.json`）
- `mapped_note`：说明「t170–t178 施工中已映射，台账原先仍写 unmapped，t181 据实况改正」
- 原 `reason_class` **保留为历史判定**（它记录的是当时为什么没映射，本身是有用的语料判断）

### 2.2 5 条「写着 mapped，其实是空的」

逐条改为 `decision: "reverted"`，并据 `captain-audit.json` 补上
`reason_class: not-a-condition`、`reverted_by`、`reverted_why`（撤回理由全文）、`reverted_note`：

| rule_id | 撤回理由（摘要） |
|---|---|
| `DITIANSUICHA-DR-07` | 10 个 `rizhu` 取值穷尽该 key 值域 ⇒ 恒真零区分度 |
| `TAIWEIFU-021` | 映射取自 quote 的**起景句**，不是判辞 |
| `ZIWEIDOUSHUQ-ZW-04` | 拿 quote 的**举例句**当适用条件，把通则收窄 |
| `ZR-04` | 取用神**取法**；六爻每盘都含全部六亲 ⇒ 恒真 |
| `HZL-R001` | 同上（枚举 5 个六亲中的 4 个 ⇒ 恒真） |

## 3. 一致性闸门：五种「台账说谎」的方式

`tools/test-ledger-consistency.py`（已入 CI）：

| 检查 | 对应哪种说谎 |
|---|---|
| `decision: mapped` ⇒ 规则 `applicable_to` **非空** | 台账过期（本轮 92 条） |
| `decision: unmapped` ⇒ 规则**为空** | 台账冒进 |
| `decision: reverted` ⇒ 规则为空**且**有 `reason_class` | 撤回没留理由 |
| `captain-audit.json` 的撤回项 ⇒ 台账里必须有、且不仍写 `mapped` | 撤回没落账（本轮 5 条） |
| 跟踪口径下每条未映射规则 ⇒ 必须有条目**且**带 `reason_class` | 漏账 |

## 4. 精确对账（与 t180 的审计互相印证）

审计口径（基线 `cd41f5b` → HEAD）的 **114 条** `applicable_to` 净变动：

| 出处 | 条数 |
|---|---:|
| 判定台账 `decision: mapped`（t168 的 18 ＋ 后续 92） | **110** |
| 无判定台账条目、但有 map 台账出处 | **4** |

那 4 条正是：`SANMINGTONGH-018`、`ZR-07`、`ZENGSHANBUYI-ZR-07`（三条 `anchor: null`，
不在跟踪口径内 → 判定台账本就不覆盖；出处是 `branch-group-map.json`）
与 `TAIWEIFU-018`（v3 迁移，出处是 `v3-language-migrations.json`）。

→ **114 条全部有出处**，与 `audit-contract.py` 报的「无出处 0」一致。
两条独立的检查（一个查规则字段、一个查账本）在同一组数字上互相印证。

## 5. 未决清单（承接 t179／t180）

t179 的决策表仍然有效，只按本轮更正一处数字（§1：`not-a-condition` 226→231、
「未复核」5→0、「永久留空」261→266）。三项需授权、四项需人判不变：

- **需授权**：① 15% 通配闸门判据（`QM-P26` 会到 5/28 = 17.9%）或另设派生键；
  ② 是否投引擎实现（神煞取法 ~30 条、梅花事实层 21 条、七政格局行限 12 条）；
  ③ `daxian`／`liunian_taisui` 事实现状（11 个 ziwei 叶子恒为「信息不足」）。
- **需人判**：④ 189 条 `restatement` 是否换真引文（会改 `quote`）；
  ⑤ 3 条无据 statement（本版该章无正文）；⑥ 25 条既有结构恒真映射（清理会下调覆盖率）；
  ⑦ V11 111 vs G1 <50。

t180 §4 的「审计自身也要被审计」结论不变；本轮新增的闸门同样是**会红的**闸门
（它不是空跑：一上线就报了 97 条）。

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：台账 ↔ 实况一致性
python3 tools/test-ledger-consistency.py

# 账本现状（decision 分布 + 未映射理由分布）
python3 -c "
import json,glob
from collections import Counter
c=Counter()
for f in glob.glob('tools/reports/predicate-decisions/*.json'):
    if 'captain-audit' in f: continue
    for x in json.load(open(f)).get('decisions') or []: c[x.get('decision')]+=1
print('decision:', dict(c))"
python3 tools/predicate-gap-report.py --json | python3 -c "
import json,sys,glob
from collections import Counter
rows=json.load(sys.stdin)['rows']
led={}
for f in glob.glob('tools/reports/predicate-decisions/*.json'):
    if 'captain-audit' in f: continue
    for x in json.load(open(f)).get('decisions') or []: led[(x['book'],x['rule_id'])]=x
c=Counter((led.get((r['book'],r['rule_id'])) or {}).get('reason_class') or '无' for r in rows)
print('未映射', len(rows), dict(c))"

# t180 的契约审计（两条检查应互相印证）
python3 tools/audit-contract.py

# 闸门（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
```

## 7. 给 cosmic 的版本钉

**本轮无规则数据变化**（`references/books/`、`references/vocab/`、`dist/` 零改动），
`CLASSICS_REV` **不变** = `da11267541a0fc500b96382e1d7b0bed004457d0`；产品仓无需重新导出。
六术覆盖率不变：bazi 49.4%／ziwei 67.7%／qimen 67.5%／liuren 22.6%／liuyao 31.9%／qizheng 24.4%。

**不得对外宣称「古籍已校勘」。** 本轮只证明**账本与规则相符**，
不证明古人文字被影印核验过 —— `verified: true` 全库仍为 0。