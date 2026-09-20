# 消费方数据版本 · t189 飞干格落地（qimen 90.0%）＋ 在消费方钉住嵌套配对语义

日期：2026-09-21。基线提交：`16efa24`（t188 后）。
**数据修订提交（请钉这个）：`9f783dfdc69a06fc7e4febd2284883528b4255d2`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

两件事：**QM-P33 飞干格**落地（qimen **87.5% → 90.0%**），
以及把 t188 那句**未验证的担心**（「若产品侧 matcher 只处理顶层 `same`，需按此补齐」）
先查证、再**在消费方钉成回归测试**——因为现在有 **7 条**奇门规则依赖这个语义。

## 1. 覆盖率前后（口径未改）

| art | 基线 | t171 | 本轮 with_pred | 本轮覆盖 | 通配占比 |
|---|---:|---:|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 222 | 49.4% | 7.2% |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 | 67.7% | 0.0% |
| **qimen** | 7 (17.5%) | 24 (60.0%) | **36** | **90.0%** | **11.1%** |
| liuren | 11 (20.8%) | 11 (20.8%) | 15 | 28.3% | 6.7% |
| liuyao | 21 (30.4%) | 21 (30.4%) | 22 | 31.9% | 13.6% |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 | 24.4% | 9.1% |

未映射 **478 → 477**。4 大门禁全绿；**32** 个 `tools/test-*.py` 全绿；
三道谓词门禁 PASS（完整输出 + exit 0）；`coverage-report --fail-under 54` PASS；
产品侧（带 `FATERADAR_CLASSICS`）**3545 passed / 0 failed**，`tsc --noEmit` exit 0。

## 2. QM-P33 飞干格：反向式枚举配对

正向式（t188）是「天盘固定干 A，**地盘**＝某柱之干」；
**飞干格「日干临庚」是等式两侧互换**：天盘的取值＝日干、地盘固定庚。

```yaml
applicable_to:
  any_of:                     # 逐个地盘/天盘可能的干值
    - all_of:
        - all_of: [{key: gan, value: 癸, scope: {pillar: day}}]      # 日干＝癸
        - all_of: [{key: tianpan_gan, value: 癸}, {key: dipan_gan, value: 庚}]
          same: gong                                                  # 天盘癸压地盘庚
    - … 共 9 支 …
```

**实测**：三样盘均**不满足**（日干壬／己／乙）；
合成盘「日干癸 ＋ 天盘癸压地盘庚」→ **满足**、「日干癸 ＋ 天盘癸压地盘**丙**」→ **不满足**
（配对是本质）。工具已同时支持正／反两式，台账区分 `encoding`。

## 3. 在消费方钉住语义（本轮的另一半）

t188 的交付文档里我写了：

> 若产品侧 matcher 只处理顶层 `same`，需按此补齐。

**那是一句未验证的担心。** 本轮先查证：

- 运行时路径 `src/lib/rules/matcher.ts:22` 确实走 `evaluateApplicableTo`；
- 它的 `evalNode` 是**递归**的，`same` 在**每一层节点各自生效**；
- 用**真实生成谓词**跑通两种情形：庚压庚 → 满足；庚压丙 → 不满足 ✓。

既然 7 条规则依赖这个语义，就把它钉成测试 ——
`tests/rules/nested-same-pairing.test.ts`（6 项，已入产品测试集）：

| 断言 | 为什么必须有 |
|---|---|
| 正向式 庚压庚 → 满足 | 基本成立情形 |
| 正向式 **庚压丙 → 不满足** | **配对是本质**；否则退化成「出现某干即可」的凑数式 |
| 内层 `same` **不得越层**把外层柱干子句拉进同宫绑定 | 柱干事实带 `pillar`、不带 `gong`；越层则整式**永不成立** |
| 反向式（飞干格）成立／不成立各一 | 镜像写法同样依赖该语义 |
| 缺柱干事实时**不得判满足** | 三态不得被冒充 |

> 写这个测试时先红了 2 项——因为 QM-P33 还没同步到产品侧（其 `applicableTo` 仍是空），
> 同步后 6/6 通过。这顺带证明该测试确实在读**真实生成数据**，不是自说自话。

## 4. 未决清单（承接 t179／t185／t187／t188）

| # | 事项 | 值多少条 | 卡在哪 |
|---|---|---:|---|
| ★1 | `QM-P30` 时格「庚临时干**三奇**」 | 1 | 「三奇」是限定时干∈乙丙丁，还是另要三奇得使？**原文两读**，不猜 |
| 2 | `QM-P26` 直使加地丁 | 1 | 需**无取值子句**；「算不算通配」口径待裁定（不是撞闸门） |
| 3 | 八字**透干**类（`SANMINGTONGH-R-02`／`YUANHAIZIPIN-008`） | 2 | 需引擎产出**藏干**（按本气／中气／余气）＋一笔约定；之后可用同一配对技术 |
| 4 | 六壬课体余项 | 2–4 | `DALIURENDAQU-007` 昴星引擎未实现；`LIURENZHIYIN-008` statement（返吟）与 quote（伏吟）不符 |
| 5 | 紫微命名格局 | 4 条 executable | 只差宫地支一笔 passthrough |
| 6 | 3 条无据 statement | 3 | 可解的人判项（t185） |
| 7 | 其余 | — | 沿用 t179：需授权（引擎投入、`daxian`）＋需人判（189 条重述、**25→64 恒真**、V11） |

**奇门已接近收尾**：36/40 = 90.0%，剩下的 4 条是 2 条（P26／P30，各有口径问题）
＋ not-a-condition 等。t179 的「★1 需授权项」在 t188／t189 两轮里**已基本消解**。

## 5. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付
python3 tools/map-qimen-lin-pairs.py --dry-run      # 幂等；正/反两式
python3 tools/map-qimen-lin-pairs.py
python3 tools/test-map-qimen-stems.py

# 语义（配对是本质）
python3 - <<'PY'
import json,sys,importlib.util,yaml
from pathlib import Path
spec=importlib.util.spec_from_file_location("ev","tools/eval-predicates.py"); ev=importlib.util.module_from_spec(spec); sys.modules["ev"]=ev; spec.loader.exec_module(ev)
bk=[f"{ (yaml.safe_load(p.read_text()).get('book') or {}).get('system')}/{(yaml.safe_load(p.read_text()).get('book') or {}).get('slug')}"
    for p in Path("references/books/san-shi").glob("*/rules.yaml")
    if any(r.get("rule_id")=="QM-P33" for r in yaml.safe_load(p.read_text()).get("rules") or [])][0]
rules={r["rule_id"]:r for r in ev.load_rules(bk,None)}
def f(k,v,**sc): return {"key":k,"value":v,"scope":sc,"derivedFrom":["test"]}
print("正向 岁干庚+庚压庚 →", ev.evaluate(rules["QM-P27"],[f("gan","庚",layer="本命",pillar="year"),f("tianpan_gan","庚",layer="本命",gong=9),f("dipan_gan","庚",layer="本命",gong=9)])["verdict"])
print("正向 岁干庚+庚压丙 →", ev.evaluate(rules["QM-P27"],[f("gan","庚",layer="本命",pillar="year"),f("tianpan_gan","庚",layer="本命",gong=4),f("dipan_gan","丙",layer="本命",gong=4),f("dipan_gan","庚",layer="本命",gong=9)])["verdict"])
print("反向 日干癸+癸压庚 →", ev.evaluate(rules["QM-P33"],[f("gan","癸",layer="本命",pillar="day"),f("tianpan_gan","癸",layer="本命",gong=2),f("dipan_gan","庚",layer="本命",gong=2)])["verdict"])
PY

# 消费方语义回归（产品仓）
cd /Users/sync/code/cosmic-fortune-lab
FATERADAR_CLASSICS=/Users/sync/code/fateradar-classics npx vitest run tests/rules/nested-same-pairing.test.ts

# 闸门（本轮全绿；完整输出 + exit code，不要接 tail）
cd /Users/sync/code/fateradar-classics
python3 tools/validate-rules.py
python3 tools/validate-executable.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54
python3 tools/audit-contract.py
```

## 6. 给 cosmic 的版本钉

`CLASSICS_REV` = **`9f783dfdc69a06fc7e4febd2284883528b4255d2`**。
产品仓 `generated/qimen.json` 已同步覆盖（36 条带谓词）；
`tsc --noEmit` exit 0；产品侧测试集 **3545 passed / 0 failed**（含新增 6 项语义回归）。

**给消费方的一条状态更新**：t188 里那句「若 matcher 只处理顶层 `same` 需补齐」
**已查证为不需要**——运行时确实递归求值、`same` 逐层生效；
并且现在有 `tests/rules/nested-same-pairing.test.ts` 把它钉住，
所以这 7 条奇门规则的配对语义不会静默退化。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0。