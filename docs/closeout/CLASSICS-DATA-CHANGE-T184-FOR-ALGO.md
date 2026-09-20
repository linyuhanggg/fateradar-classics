# 消费方数据版本 · t184 三奇得使落地（qimen 67.5%→70%）＋ 奇门「X临Y」块分析

日期：2026-09-21。基线提交：`1d46075`（t183 后）。
**数据修订提交（请钉这个）：`d5b84e2ffe7b1e4da0e18c8a2e45e5923394dbf3`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

本轮三件事：**落地一条**（QM-P25 三奇得使，qimen **67.5% → 70.0%**）、
**把最大的剩余块算清并摆出三选一**（奇门「X临Y」8 条，需授权或跨仓协调）、
以及**一次系统扫描的负结论**（当前事实集下没有新的可映射规则）。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| **qimen** | 7 (17.5%) | 24 (60.0%) | **28** | **70.0%** | **14.3%** | 6 |
| liuren | 11 (20.8%) | 11 (20.8%) | 12 | 22.6% | 8.3% | 5 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 22 | 31.9% | 13.6% | 6 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **489 → 488**。4 大门禁全绿；**31** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS
（`--max-wildcard 15` 实测 4/28 = 14.3%）；`coverage-report --fail-under 54` PASS。

## 2. 落地：QM-P25 三奇得使——它是怎么被发现的

本轮本来在调查 8 条「X临Y」格块（§3），过程中看 `predicate-report` 的
`fact_key_names` 时注意到奇门事实层**早就有一个 `geju_qimen` 键**——
引擎把**格名当事实产出**，而 `QM-P14 伏吟局`／`QM-P15 反吟局` 正是按
`[{key: geju_qimen, value: …}]` 写的。

`QM-P25`「三奇得使 乙奇加甲午甲戌 丙奇加甲子甲申 丁奇加甲寅甲辰」的格名
引擎已产出（`patterns`／`ruleChecks`），于是：

```yaml
applicable_to: [{key: geju_qimen, value: 三奇得使}]
```

**为什么不是「凑近似名」**：`qimen-analysis.ts` 的配对表
`ENVOY = {乙:[己,辛], 丙:[戊,庚], 丁:[壬,癸]}` 与原文逐项吻合 ——
甲午／甲戌旬首＝辛／己、甲子／甲申＝戊／庚、甲寅／甲辰＝壬／癸，
正是原文「乙奇加甲午甲戌／丙奇加甲子甲申／丁奇加甲寅甲辰」的三组配对。

**实测**：caseA 格名含「三奇得使」→ **满足**；caseB 只有「伏吟局」→ **不满足**（有区分度）。

### 2.1 新加的一致性闸门立刻报了红

我刚映射完，`test-ledger-consistency.py`（t181 加的）就因
「QM-P25 台账仍写 `unmapped`、规则却有谓词」报红 —— **正是它该做的事**。
已改 `decision: mapped` 并记 `mapped_by: qimen-stem-map.json`。

## 3. 奇门「X临Y」格块（8 条）：算清了，但**不是我能单方面定的**

`tools/qimen-lin-block.py`（可复跑）。原文是 qimen-faqiao 选段的格表：

```
岁格 庚临岁干     月格 庚临月干     日格 庚临日干     时格 庚临时干三奇
伏干 庚临日干     飞干格 日干临庚   地罗遮蔽 六壬临时干  天网四张 六癸临时干
```

**语义已明确**：「临」＝天盘压地盘（「日干临庚」是反向，可见体例一致）。
八条的公共条件都是：**某宫天盘干为 A，且该宫地盘干等于某柱之干**。

| 需要什么 | 状态 |
|---|---|
| `tianpan_gan` / `dipan_gan` | **已有**（t171） |
| 奇门侧四柱干事实 | 引擎已算（`facts.ganZhi`），事实层未产出 —— 一笔 passthrough |
| **把「地盘干取值」与「某柱干」绑起来** | ← **真卡点** |

### 3.1 三种编码各自的闸门后果（已算，可复跑）

| 方案 | 写法 | 闸门 |
|---|---|---|
| 显式通配 | `{all_of:[{tianpan_gan,庚},{dipan_gan,"*"}], same:gong}` | (4+8)/(27+8) = **34.3% → FAIL** |
| 限柱位不限取值 | 引擎产出「柱干临宫」事实，子句 `{key:zhu_gan_lin, scope:{pillar:year}}`（限定柱位、不限定取值） | 字面不含 `*`，但语义等价存在性 → **需口径裁定** |
| 语言 v4 value-join | 允许无取值子句 + `same` 接受 `value`（两句所命中事实的 value 须相等） | 不产生通配子句 → PASS，但**需消费方同步实现** |

**结论**：三选一都不是我能单方面定的 —— 前两条要**授权**（闸门判据／口径裁定），
第三条要**跨仓协调**（产品侧评估器也要实现同一语义）。故本轮**只分析、不动规则、不动闸门**。

**这一块的分量**：解开后奇门可从 70% 升到接近 90%，是当前**单个可识别块里最大的一块**。

## 4. 系统扫描的负结论（附一条方法论教训）

用**当前**事实集（含 t170–t178 新增的 `yao_zhi`/`bian_yao_zhi`/`tianpan_gan`/`dipan_gan`/
`nayin`/`liuqin@liuren` 等）对**全部**未映射规则做了一次扫描：
「statement 里是否含该术已产出键的取值」。

- 命中 **152** 条；
- 但只算**多字取值**（长度 ≥2）后落回 **30** 条 —— **正是已登记的那批残留**
  （残留台账 27 条 ＋ 3 条 `anchor: null`），**没有一条新的可映射规则**。

**教训**：单字取值（`gan=丁`、`zhi=子`、`xiudu=星`、`yongshen=木`）会让这类扫描
假命中率极高 —— 152 条里 122 条是这种噪声。同类扫描以后应先按取值长度过滤。

## 5. 未决清单（承接 t179／t181／t182／t183）

t179 的决策表仍有效（需人判 ⑥ 已按 t182 由 25 更正为 **64**）。本轮把它**量化得更细**：

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---:|---|
| ★1 | **奇门「X临Y」块** | **8**（qimen 70%→~90%） | 三选一：授权闸门判据／授权口径裁定＋一笔 passthrough／语言 v4＋跨仓协调 |
| 2 | 紫微命名格局 | 4 条 executable 记录只差**宫地支** | 一笔 passthrough；但只值 4 条记录 0 条规则（按 t179 客户数标准未立） |
| 3 | `QM-P26` 直使加地丁 | 1 | 形态与已映射三条同构，但会到 5/28 = 17.9% → 闸门红（算术已被测试钉住） |
| 4 | 其余需授权 2 项／需人判 3 项 | — | 沿用 t179（引擎投入、`daxian`；189 条重述、3 条无据、25→64 恒真、V11） |

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/qimen-lin-block.py                    # 「X临Y」8 条：语义/缺什么/三方案闸门算术
python3 tools/qimen-lin-block.py --json | head -30
python3 tools/map-qimen-stems.py --dry-run          # 幂等：已落实的会跳过
python3 tools/test-map-qimen-stems.py               # 形态 + 语义 + 闸门算术（含 QM-P26 会超限）

# 三态求值（入参盘面状态 → 结论 + 置信度 + 出处）
python3 tools/eval-predicates.py --art qimen --case caseA -v | grep -A2 "QM-P25"
python3 tools/eval-predicates.py --art qimen --case caseB -v | grep -A2 "QM-P25"

# 系统扫描（§4）：只算多字取值
python3 - <<'PY'
import json,subprocess,yaml,sys,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("pr","tools/predicate-report.py"); pr=importlib.util.module_from_spec(spec); sys.modules["pr"]=pr; spec.loader.exec_module(pr)
vocab=json.load(open("references/vocab/fact-vocab.json"))["values"]
rows=json.loads(subprocess.run([sys.executable,"tools/predicate-gap-report.py","--json"],capture_output=True,text=True).stdout)["rows"]
un={(r["book"],r["rule_id"]) for r in rows}; n=0
for p in Path("references/books").glob("*/*/rules.yaml"):
    d=yaml.safe_load(p.read_text()); b=d.get("book") or {}
    for r in d.get("rules") or []:
        if (f"{b.get('system')}/{b.get('slug')}",r.get("rule_id")) not in un: continue
        art=pr.art_of(b.get("system"),b.get("slug")); st=r.get("statement") or ""
        hits={f"{k}={v}" for k in (pr.ART_EMIT_KEYS.get(art) or frozenset()) for v in (vocab.get(k) or []) if len(str(v))>=2 and str(v) in st}
        if hits: n+=1
print("多字取值命中（应落回残留规模）:", n)
PY

# 闸门（本轮全绿）
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

`CLASSICS_REV` = **`d5b84e2ffe7b1e4da0e18c8a2e45e5923394dbf3`**。
产品仓 `generated/qimen.json` 已同步覆盖（28 条带谓词）；`tsc --noEmit` exit 0；
相关测试文件全绿（含 `qimen-methods`）。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。