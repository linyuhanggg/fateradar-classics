# 消费方数据版本 · t180 贯穿契约的跨提交审计（附自审反例）

日期：2026-09-21。基线提交：`e5973d2`（t179 后）。
**本轮无规则数据变化 → 消费方 `CLASSICS_REV` 不变，仍为
`da11267541a0fc500b96382e1d7b0bed004457d0`。**
全库 `verified: true` 计数仍为 **0**（本轮由审计工具独立复核，不只是 grep 自报）。

## 0. 一句话结论

前 12 轮我一直在**施工**；本轮做的是**自我审计**：把贯穿契约里可机器验证的部分
钉成一条命令 `tools/audit-contract.py`，对 t168 之前的基线做全量比对。

结论：**基线 → HEAD，55 份 `rules.yaml`／1356 条规则，受保护字段违规 0**——
十几轮施工**只动了 `applicable_to` 这一个字段**，`statement`／`quote`／`anchor`／
`verified*`／`caveats`／`school`／`kind`／`rule_id` 与 `book` 块**逐字未改**；
规则不增不减；`verified: true` 为 0；114 条谓词变动**全部可溯源**。

审计当场揪出 **1 条此前无记录的变动**（`TAIWEIFU-018`，§3），已补登。
审计自身也被反例测试（§4），其中一个反例逼出了一个真缺陷（§4.1）。

## 1. 审计口径与结果

```bash
python3 tools/audit-contract.py              # 默认基线 cd41f5b（t168 之前的起点）
python3 tools/audit-contract.py --json
python3 tools/test-audit-contract.py         # 正例 + 三个反例
```

| 检查项 | 结果 |
|---|---|
| 受保护字段违规（10 个字段 + `book` 块） | **0** |
| 规则新增 / 删除 | **0 / 0** |
| `applicable_to` 净变动 | **114** |
| 其中**无台账出处** | **0** |
| 台账谓词与当前文件不一致 | **0** |
| 全库 `verified: true` 行数 | **0** |

**「可溯源」是怎么验的**：不是看台账自称，而是把台账里记的谓词与**当前文件**逐个比对；
台账有三种形态，各配适配器：

- `map-*.json` 的 `applicable_to_yaml`（qimen／branch-group／fixed-value 三份）
- `nayin-ganzhi-map.json` 的 `gan`/`zhi`（按固定模板重建后比对）
- `predicate-decisions/*.json` 的 `decision == "mapped"`（t168 逐条判定台账，扣除复核撤回项）
- `v3-language-migrations.json`（本轮新增，见 §3）

## 2. 这组数字回答了什么

任务书的「不做」四条里，**三条是可机器验证的**，本轮全部落到一条命令上：

| 不做的事 | 审计怎么验 |
|---|---|
| 不硬锚（宁留 `anchor: null`） | `anchor` 字段逐字未改（0 违规）；189 条 `anchor: null` 保持 `null` |
| 不生成让 `verified` 变 true 的自我认定 | 全库 `verified: true` = 0，且 `verified` 字段逐字未改 |
| 不把未实现的救应写成没有救应 | `rescue` 归 t174 的两条门禁管（`RESCUE_GAP`／`RESCUE_NONE_CLAUSE`） |
| 不虚构反例凑三态 | 逐条三态由 `eval-predicates.py` 按盘面算；本轮 114 条变动全部有原文出处 |

**「只动 `applicable_to`」本身就是「不编造」的强证据**：谓词改了、原文一字未动，
说明每条谓词都是在既有原文锚点上写出来的，而不是反过来改原文去迁就谓词。

## 3. 审计揪出的 1 条：`TAIWEIFU-018`

| | |
|---|---|
| 何时改 | t168 的 v3 语言升级提交 `1f25bb5` |
| 改前（v2 平铺） | `[{key: ziwei_palace, value: 疾厄}, {key: ziwei_palace, value: 迁移}]` |
| 改后（v3 组） | `{any_of: [{all_of: [{key: sihua, value: 化忌, scope: {palace: 疾厄}}]}, …迁移…]}` |
| 原文 | 「**忌**暗同居身命**疾厄**，沉困尪羸；凶星会于父母迁移，刑伤破祖」 |

**为什么改是修正而不是改口径**：v2 那两条问的是「疾厄宫事实存在吗／迁移宫事实存在吗」——
**每一张盘都成立**（十二宫恒在），属结构恒真、零筛选。v3 形式改为要求**化忌确实落在该宫**，
才对得上原文的「忌…同居…疾厄」。

- 该提交里 `applicable_to` 变动共 **21** 条：其余 **20** 条是 `[] → 谓词`（新增映射，
  出处已由 `predicate-decisions/*.json` 覆盖），**只有这 1 条是「已有谓词 → 另一个谓词」的语义变动**。
- 已补登 `tools/reports/v3-language-migrations.json`：含 before/after、改动理由、
  **子集披露**（只取「疾厄／迁移」两宫，沿 v2 的宫位选择，未含「身命」，也未表达「暗」星
  与「凶星会于父母」两截），以及语义可判性说明（每盘化忌恰落一宫 → 可判真假）。
- 审计据此接受其为有出处 → 复跑得 0 无出处。

## 4. 审计自身也要被审计：正例＋三个反例

`tools/test-audit-contract.py`（已入 CI）：

| 情形 | 期望 | 结果 |
|---|---|---|
| 正例：当前树 | exit 0；违规 0；无出处 0；变动 >100 | ✅ |
| 反例 A：改一条 `statement` | 报「受保护字段违规」且 exit≠0 | ✅ |
| 反例 B：`applicable_to` 改成台账没有的谓词 | 报无出处／台账不一致 | ✅ |
| 反例 C：`--base deadbeef` | **必须报错退出**，不得静默通过 | ✅ |

破坏性用例全部在 `finally` 里还原，并与原字节比对（`已还原（逐字节相同）`）。

### 4.1 反例 C 逼出的真缺陷（值得记）

初版 `audit-contract.py` 遇到坏基线时：`git ls-tree <坏引用>` 返回空 →
「没有文件 → 没有违规」→ **审计静默通过、exit 0**。

**一条永不说坏的审计等于没有审计**，这比误报危险得多。已显式挡掉：
先 `git rev-parse --verify` 验证引用，且要求该引用下能取到 `rules.yaml`，否则报错退出。

同轮还修了两处自身缺陷：

- **O(规则 × 文件) 重复解析**：台账比对写在双层循环里（每条台账 × 每个文件重新解析 YAML），
  审计一次要几分钟 —— 被测试超时当场抓到；改为先建一次「规则 → `applicable_to`」索引，
  现约 **2 秒**。
- 初版把**绝对路径**传给 `git show`（`cd41f5b:/Users/...`），取不到内容 →
  基线被当成空文件 → 报出「55 份 `book` 块都变了、新增 1356 条规则」这种全盘失真结果。
  已改为只接受工作区相对路径，且取不到内容时**直接报错**而不是静默返回空。

## 5. 未决清单（承接 t179，仅列变化）

t179 那张决策表仍然有效（489 条构成、阻塞项 × 值多少条 × 要谁动、需授权 3 项／需人判 4 项）。
本轮只做加法：

- **新增已完成项**：贯穿契约的可机器验证部分已审计并通过（§1），且审计自身有反例测试（§4）。
- **`TAIWEIFU-018` 从「未记录」变为「已登记」**（§3）。
- t179 §4 的四类「不值得做」结论不变；本轮又量了一个候选：**ziwei 星曜亮度**——
  引擎已算（`s.brightness`），但提亮度的未映射规则只有 4 条，其中 2 条是「命宫总论／综合断法」
  这类**汇总体例**（还要三方四正），另 1 条是「村头庙宇」的假命中 → **不值得单独立键**。

## 6. 可复跑命令

```bash
cd /Users/sync/code/fateradar-classics

# 本轮交付：贯穿契约的跨提交审计
python3 tools/audit-contract.py                 # 期望：违规 0 / 无出处 0 / verified:true 0
python3 tools/audit-contract.py --json | head -20
python3 tools/test-audit-contract.py            # 正例 + 反例 A/B/C（约 10 秒）
git log --oneline cd41f5b..HEAD | wc -l         # 审计覆盖了多少提交

# 台账（「可溯源」的出处）
python3 -c "
import json,glob
for f in sorted(glob.glob('tools/reports/*map*.json'))+['tools/reports/v3-language-migrations.json']:
    d=json.load(open(f)); n=len(d if isinstance(d,list) else d.get('entries') or [])
    print(f'{n:4} {f}')"

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

**不得对外宣称「古籍已校勘」。** 本轮的审计只证明「施工没有越界改原文」，
**不证明**古人文字被影印核验过 —— `verified: true` 全库仍为 0，
电子文本匹配、模型审查与测试都不能代替人工影印核验。