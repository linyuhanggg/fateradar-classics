# 消费方数据版本 · t186 奇门四柱干支入事实层 · QM-P36 时干入墓落地（qimen 70%→72.5%）

日期：2026-09-21。基线提交：`268c055`（t185 后）。
**数据修订提交（请钉这个）：`5afa6456e9c06e439e5eb92fc79f60118087f86b`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

两件事：**奇门四柱干支入事实层**（`gan`/`zhi` 按 `scope.pillar` 透传），
并据此用 t176 的「显式柱位枚举对」技术落地 **QM-P36 时干入墓**。
qimen 谓词覆盖 **70.0% → 72.5%**（28→29），未映射 **488 → 487**。

同时把「**X临Y」8 条块**的决定依据刷新：那一块的**事实已齐**，
只剩「跨键取值相等」这一件表达力。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 | FactKey 种类 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% | 10 |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% | 5 |
| **qimen** | 7 (17.5%) | 24 (60.0%) | **29** | **72.5%** | **13.8%** | 6 → **8** |
| liuren | 11 (20.8%) | 11 (20.8%) | 12 | 22.6% | 8.3% | 5 |
| liuyao | 21 (30.4%) | 21 (30.4%) | 22 | 31.9% | 13.6% | 6 |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% | 4 |

未映射 **488 → 487**。4 大门禁全绿；**32** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS
（`--max-wildcard 15` 实测 4/29 = 13.8%）；`coverage-report --fail-under 54` PASS。

## 2. 事实层：奇门四柱干支

延续 t170／t171／t173／t176／t178 的同一路子 —— **事实在引擎里，只是没被当事实产出**：
奇门排盘早就有 `facts.ganZhi.{year,month,day,time}`，而 `emitQimenFacts` 只收
`grid/patterns/meta/zhifuPalace/zhishiPalace`。

- 产品侧：`emitQimenFacts` 新增 `pillars` 入参，按柱位透传 `gan`/`zhi`；
  调用方传 `facts.ganZhi`。
- **与 bazi 共用 `gan`/`zhi` 键、按 `scope.pillar` 区分**。V16 只校验 `scope.pillar`
  的取值是否在 `year/month/day/time` 内、**不限定术**，故无需放宽任何闸门。
- `ART_EMIT_KEYS[qimen]` 补入两键（两份报告脚本同步）。

实测样本：caseA 四柱 `庚午/甲申/壬子/丁未`，caseB `甲子/丙寅/己巳/甲子`（与 bazi 同源）。

### 2.1 两个自己踩的坑（记下来）

1. **补丁插错了函数**：我用 `const out = []; const natal = …` 作锚，而这个片段在
   `emitBaziFacts` 里先出现 —— 结果四柱透传插进了 bazi（那里本来就有逐柱 gan/zhi）。
   是 `tsc` 报「`input.pillars` 不存在」才暴露的。已改用 qimen 独有的
   `Object.fromEntries(input.meta)` 作锚，**并加断言**校验「该块只在 qimen 函数体内、全文件只出现一次」。
2. **`Object.entries` 让字面量类型退化**：`pillar` 变成 `string`，对不上 `natalScope` 的
   `PillarKey | undefined`。改为显式列 `["year","month","day","time"] as const`。

## 3. QM-P36 时干入墓

原文（qimen-faqiao）：**「时干入墓，戊戌、壬辰、丙戌、癸未、丁丑、己丑也」**
—— 条件就是「**时柱**等于所列六对干支之一」。用 t176 的显式柱位技术，不需要 `same`：

```yaml
applicable_to: {any_of: [{all_of: [{key: gan, value: 戊, scope: {pillar: time}},
                                    {key: zhi, value: 戌, scope: {pillar: time}}]}, …六对]}
```

**为什么不用 `same: pillar`**：六个候选对是互为**或**的独立组；`same` 会把它们绑到同一柱
（t176 已记过同一理由）。

**实测**：合成盘上 戊戌／壬辰／丁丑 **满足**，甲子 **不满足**；两样本盘（丁未／甲子）
均为**不满足** —— 说明该式**不是恒真**、有区分度。

> 台账一致性闸门再次当场报红（`QM-P36` 台账仍写 `unmapped`）—— 与 t184 一样，
> 正是 t181 那道闸门该做的事；已改 `mapped` 并记 `mapped_by: fixed-value-map.json`。

## 4. 成绩单更新：「X临Y」8 条块现在只差一件表达力

`tools/qimen-lin-block.py` 已随本轮刷新：

| 需要什么 | t184 时 | **本轮** |
|---|---|---|
| `tianpan_gan` / `dipan_gan` | 已有 | 已有 |
| 奇门侧四柱干事实 | **缺**（引擎已算、事实层未产出） | **已补**（本轮 passthrough） |
| 把「地盘干取值」与「某柱干」绑定 | 真卡点 | **仍是唯一卡点** |

三方案的闸门算术也随之刷新：显式通配现在算作 **(4+8)/(29+8) = 32.4%**（仍 FAIL）；
「限柱位不限取值」仍需口径裁定；「语言 v4 value-join」仍是唯一 PASS 且不需要放宽闸门的路线，
但需**消费方同步实现**。**在得到授权前不动规则、不动闸门。**

## 5. 顺带的负结论：最大的分类桶经得起复核

未映射的 226 条 `not-a-condition`（占 48%，是**最大的一个桶**，此前从未系统复核过）。
本轮做了定向复核：找「statement 里**同时**含该术已产出键的**多字取值**、且含条件标记
（则／即／主／若／忌／宜／须／见／逢／遇）」的条目 —— **只有 3 条**，
且三条都早已逐条判过（`ZIWEIDOUSHUQ-ZW-04` 因拿引文举例当条件已撤回、
`GUOTIANJING-004` 原文自称「仅作语义参考，不作硬判断输入」、`HJC-R007` 是取象表）。

即：**这个最大的桶在定向复核下站得住**，不是误判堆积。

## 6. 未决清单（承接 t179／t182／t184／t185）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---:|---|
| ★1 | **奇门「X临Y」块** | **8**（qimen 72.5%→~90%） | 事实已齐，只差「跨键取值相等」：三选一（授权闸门判据／授权口径裁定／语言 v4＋跨仓协调） |
| 2 | 奇门 `QM-P26` 直使加地丁 | 1 | 会到 5/30 = 16.7% → 闸门红（算术被测试钉住） |
| 3 | 紫微命名格局 4 条记录 | 4 条 executable | 只差宫地支一笔 passthrough（按客户数标准暂未立） |
| 4 | 3 条无据 statement | 3 | **已从「无解」改为「可解的人判项」**（t185：正文在 L7720–L7730） |
| 5 | 其余 | — | 沿用 t179：需授权（引擎投入、`daxian`）＋需人判（189 条重述、**25→64 恒真**、V11） |

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-fixed-values.py --dry-run         # 幂等：已落实的跳过
python3 tools/test-map-fixed-values.py              # 5 条台账 + 形态 + 语义
python3 tools/qimen-lin-block.py                    # 8 条块：事实已齐、只剩表达力（三方案算术）
python3 tools/eval-predicates.py --book san-shi/qimen-faqiao --case caseA -v | grep -A2 "QM-P36"

# 四柱干支确实进了事实层
python3 -c "
import json
d=json.load(open('tools/reports/facts-sample.json'))['qimen']
for case,c in d.items():
    p={}
    for f in c['facts']:
        if f['key'] in ('gan','zhi'): p.setdefault(f['scope']['pillar'],{})[f['key']]=f['value']
    print(case, {k: v.get('gan','')+v.get('zhi','') for k,v in p.items()})"

# §5 的定向复核（not-a-condition 桶）
python3 - <<'PY'
import json,yaml,sys,subprocess,importlib.util
from pathlib import Path
spec=importlib.util.spec_from_file_location("pr","tools/predicate-report.py"); pr=importlib.util.module_from_spec(spec); sys.modules["pr"]=pr; spec.loader.exec_module(pr)
vocab=json.load(open("references/vocab/fact-vocab.json"))["values"]
led={}
for f in Path("tools/reports/predicate-decisions").glob("*.json"):
    if "captain-audit" in f.name: continue
    for x in json.load(f.open())["decisions"]: led[(x["book"],x["rule_id"])]=x
rows=json.loads(subprocess.run([sys.executable,"tools/predicate-gap-report.py","--json"],capture_output=True,text=True).stdout)["rows"]
un={(r["book"],r["rule_id"]) for r in rows}; n=0
for p in Path("references/books").glob("*/*/rules.yaml"):
    d=yaml.safe_load(p.read_text()); b=d.get("book") or {}
    art=pr.art_of(b.get("system"),b.get("slug"))
    for r in d.get("rules") or []:
        k=(f"{b.get('system')}/{b.get('slug')}",r.get("rule_id"))
        if k not in un or (led.get(k) or {}).get("reason_class")!="not-a-condition": continue
        st=r.get("statement") or ""
        hit={f"{key}={v}" for key in (pr.ART_EMIT_KEYS.get(art) or frozenset()) for v in (vocab.get(key) or []) if len(str(v))>=2 and str(v) in st}
        if hit and any(c in st for c in ("则","即","主","若","忌","宜","须","见","逢","遇")): n+=1
print("not-a-condition 桶里的可疑条目（应仍为 3）:", n)
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

## 8. 给 cosmic 的版本钉

`CLASSICS_REV` = **`5afa6456e9c06e439e5eb92fc79f60118087f86b`**。
产品仓 `generated/qimen.json` 已同步覆盖（29 条带谓词，含 `QM-P36` 的
`{any_of:[{all_of:[{gan:戊,scope:{pillar:time}},{zhi:戌,scope:{pillar:time}}]}, …]}`）；
`tsc --noEmit` exit 0；相关 5 个测试文件 **63 项全绿**。

**给消费方的一条提醒**：奇门事实层现在也有 `gan`/`zhi`（按 `scope.pillar` 区分柱位）。
若你的检索或面板按 key 聚合，注意这两个键**跨 bazi 与 qimen 两术**，
需按 art 或按 `scope.pillar` 分开处理。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。