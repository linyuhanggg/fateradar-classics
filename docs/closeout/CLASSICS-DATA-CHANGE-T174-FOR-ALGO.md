# 消费方数据版本 · t174 救应标签的两个契约（目标项 3 收口）

日期：2026-09-21。基线提交：`bab4160`（t173 后）。
**本轮只动校验器与其测试，无规则／词表／夹具数据变化 → 消费方 `CLASSICS_REV` 不变，
仍为 `eb9ad74bb1ed3bf5a6557fe70e900fc32a10bac6`。**
全库 `verified: true` 计数仍为 **0**。

## 0. 一句话结论

目标项 3 要求「每批守 schema `fateradar-executable-v2`：三态 · **rescue(含 unimplemented)** ·
**named_gaps** · implementation_assumption · verified 保持 false」。
本轮把其中**救应标签的两个契约**从「靠人记得」变成「**门禁挡住**」。

审计结论：正向契约完好；**反向契约此前完全没人管**（用变异实验证明）；而任务书点名的
「**不把未实现的救应写成没有救应**」此前也无人检查（实测当前 106 条 `rescue=none` **无违规**）。
两条现均已入 `validate-executable.py`，并各配反向测试。

## 1. 覆盖率与闸门（本轮不变）

| art | 基线 | t171 | 本轮 |
|---|---:|---:|---:|
| bazi | 143 (31.9%) | 211 (47.0%) | 211 (47.0%) |
| ziwei | 54 (58.1%) | 63 (67.7%) | 63 (67.7%) |
| qimen | 7 (17.5%) | 24 (60.0%) | 24 (60.0%) |
| liuren | 11 (20.8%) | 11 (20.8%) | 11 (20.8%) |
| liuyao | 21 (30.4%) | 21 (30.4%) | 21 (30.4%) |
| qizheng | 11 (24.4%) | 11 (24.4%) | 11 (24.4%) |

未映射 505 条。4 大门禁全绿；**24** 个 `tools/test-*.py` 全绿；三道谓词门禁 PASS；
`coverage-report --fail-under 54` PASS。`git status` 只动两个文件（校验器与其测试）。

## 2. 审计：救应标签的实际状态

`references/executable/` 258 条记录：

```
rescue: self 117 | none 106 | unimplemented 30 | 指向真实规则 ID 5
named_gaps kinds: unimplemented-reason 30 | source-term 11 | verdict-scope 1   （合计 42）
unimplemented-reason.reason_class: implementation-gap 22 | evidence-undecided 8
```

- **正向契约完好**：30 条 `rescue=unimplemented` **全部**带 `unimplemented-reason` 登记（30/30）。
- `reason_class` 取值合法、`verified=false` **已由校验器强制**（`NAMED_GAPS` / `VERIFIED`），
  本轮不重复实现。

## 3. 找到的两个真缺口

### 3.1 反向契约没人管（**变异实验证明**）

校验器只管正向：`unimplemented-reason` 只许挂在 `rescue=unimplemented` 上。
**反向没人管** —— 我把 `QTB-M-01-02` 的 `rescue` 改成 `unimplemented`、**不写任何登记**，
校验器仍然：

```
OK 15 packages, 258 source-linked rule records, 579 source spans, 42 named gaps
exit=0
```

即「原文有救应、引擎尚未实现」可以是一句**无据声明**，且虚增未决清单而不留痕。
（实验后已用备份还原，`git diff -- references/executable/` 为空。）

→ 新增 **`RESCUE_GAP`**（error）：`rescue=unimplemented` 必须登记一条
`kind=unimplemented-reason` 的具名登记，说明是实现缺口还是证据未决。

### 3.2 「不把未实现的救应写成没有救应」无人检查

`rescue="none"` 的语义是**原文根本没有救应条款**。若本条**自己的来源**里出现救应专词，
那就是错标 —— 这正是任务书「不做」清单里点名的行为。改前无人检查。

→ 新增 **`RESCUE_NONE_CLAUSE`**（error）：扫描该条**自己声明的 `sources`**，
命中救应专词即拒。

判据（有意收窄，写在校验器注释里）：`有救／無救／无救／救應／救应／可解／得解／救神`。
**不含** `制化／通关` —— 它们是条款的常见内容而非救应标记。这条收窄有实测依据：
宽口径下唯一命中项 `QTB-M-10-06` 的原文是「其生剋制化，与五月略同」，
那是**章节互见**，不是救应条款，故该条 `rescue=none` 判定正确。

实测结果：106 条 `rescue=none` 里**救应专词命中 0 条**（正向对照：117 条 `rescue=self` 里
7 条原文含救应专词，方向一致）。即当前库**无违规**，新门禁是把既有事实钉住，不是翻旧账。

## 4. 本轮我自己的补丁里出过一个 bug（记下来）

新加的 `RESCUE_NONE_CLAUSE` 初版报了一条**误报**：`QTB-M-02-06` 声称来源含「可解」。
可它的 `sources` 里并没有「可解」。

原因：该检查写在了 `sources = rule.get("sources")` **之前**，读到的 `sources` 变量是
**上一条规则遗留的值**（循环泄漏）。修法：直接读 `rule.get("sources")`，并在注释里标明这个坑。

**发现方式值得一提**：我自己独立做的审计说 0 条命中，校验器说 1 条 —— 两边不一致。
我没有选信一边，而是去查差异，结果查出的是我自己补丁的 bug。
现在两者一致（都 0），且测试里留了反向用例防止回归。

## 5. 测试

`tools/test-validate-executable.py`：**27 → 29** 项，全绿。

- 新增 `test_unimplemented_requires_a_reason_registration`：`rescue=unimplemented` 且无登记 → `RESCUE_GAP`。
- 新增 `test_rescue_none_cannot_hide_a_rescue_clause`：来源含「無救」且 `rescue=none` → `RESCUE_NONE_CLAUSE`。
- 共享夹具按新契约调整：基准 `rescue` 由 `unimplemented` 改为 `self`（不需要 reason 登记），
  需要测 unimplemented 的 3 个用例各自显式设回 —— 因为**基准夹具本身**在新契约下已不合规，
  这正是新门禁生效的证据（改前 4 项测试因此变红，改夹具后转绿）。

两条新门禁都在既有 CI（`validate-rules.yml` 的 `validate-executable.py` 与其测试）内，每批必过。

## 6. 未决清单（承接 t170–t173）

1. **`rescue=none` 的错标若出现在 `quote` 而非 `sources`**：本轮判据只看该条自己的 `sources`
   （与 schema 的「理由只能挂在条款自己的原文上」一致）。`quote` 是 sources 的拼接，理论上同源，
   但若某条 `quote` 与 `sources` 不一致，判据会漏 —— 目前未发现。
2. **`rescue` 指向真实规则 ID 的 5 条**：其依赖由校验器解析，本轮未变。
3. **两处词表漂移**：产品仓多 `meihua_gua`／`xiaoliuren_palace`（本仓无），t168 已登记。
4. **15% 通配闸门挡住 4 条奇门规则**（t173 §5）：`QM-P01／P02／P26／P31` 事实已齐，
   但只能写成 `{all_of:[{zhifu,"*"},{dipan_gan,X}], same: gong}`；闸门按规则数计会到 17.9%。
   **未放宽闸门、未挑 2 条凑数**。需二选一授权（闸门加存在性判据／另设派生事实键）。
5. **statement↔anchor 不符 3 条**（t173 §3，`ungrounded-claims.json`）：需古籍侧先收口。
6. t169–t173 其余：`daxian`/`liunian_taisui` 事实现状、`liuyao.structure` 打包名、
   ziwei 11 条命名格局缺定义表、`fold_han` 不处理古异体字、`nayin` 尚无谓词使用、
   189 条重述是否换真引文、V11 111 vs G1 <50、25 条既有结构恒真映射。

## 7. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 救应契约（本轮新增的两条门禁）
python3 tools/validate-executable.py                 # RESCUE_GAP / RESCUE_NONE_CLAUSE 生效
python3 tools/test-validate-executable.py            # 29 项，含两条反向用例

# 全部门禁（本轮全绿）
python3 tools/validate-rules.py
python3 tools/validate-annotations.py
python3 tools/validate-figure-evidence.py
for f in tools/test-*.py; do python3 "$f" || echo "FAIL $f"; done
python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys
python3 tools/coverage-report.py --fail-under 54

# 救应标签现状（只读）
python3 - <<'PY'
import json, glob
from collections import Counter
recs=[r for f in glob.glob("references/executable/*.json") for r in json.load(open(f)).get("rules") or []]
print("rescue:", dict(Counter(r.get("rescue") for r in recs)))
print("kinds:", dict(Counter(g.get("kind") for r in recs for g in r.get("named_gaps") or [])))
PY
```

## 8. 给 cosmic 的版本钉

**本轮无规则数据变化**，`CLASSICS_REV` **不变** = `eb9ad74bb1ed3bf5a6557fe70e900fc32a10bac6`；
产品仓无需重新导出。

**不得对外宣称「古籍已校勘」。** `verified: true` 全库仍为 0；
电子文本匹配、模型审查与测试都不能代替人工影印核验。