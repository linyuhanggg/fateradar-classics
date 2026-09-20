# T168 映射作业书：把「未映射」逐条判成「可映射」或「不可映射」

工作目录：`/Users/sync/code/fateradar-classics`（古籍仓，git 已初始化）。

贯穿契约：**不编造、可溯源、原文没写就不写**。这条优先于任何覆盖率数字。
宁可留 `applicable_to: []`，也不许为了数字好看塞一个原文没说的条件。

## 你的产出（两件）

1. **只改** 分配给你的 `references/books/<system>/<slug>/rules.yaml` 里各规则的 `applicable_to`。
   **绝对不许动** `statement` / `quote` / `anchor` / `verified` / `verified_by` / `verified_at` /
   `caveats` / `school` / `kind` / `rule_id`。只改 `applicable_to`。
2. **写** 一个判定台账 `tools/reports/predicate-decisions/<你的art>.json`（UTF-8，见下方格式）。
   台账必须**覆盖你 art 的全部未映射规则**，一条不落。

## 先跑这两条拿到你的作业清单

```bash
cd /Users/sync/code/fateradar-classics
python3 tools/predicate-gap-report.py --art <你的art> --json > /tmp/gap-<你的art>.json
# 逐条读 statement：
python3 -c "
import json;d=json.load(open('/tmp/gap-<你的art>.json'))
for r in d['rows']: print(r['rule_id'],'|',r['statement'][:200])
"
```

`kind` 字段含义：
- `no-chart-token`：statement 里找不到该 art 任何 FactKey 的合法取值
- `single-pair` / `multi-pair-same-key`：能复原出 1 个 / 同 key 多个 (key,value)
- `multi-key`：复原出跨 key 的多个令牌（需要 AND）

## 谓词语法（v3，见 docs/PREDICATE-LANGUAGE-V3.md）

旧形（平铺列表）语义是 **OR**（任一命中即命中）。新形可表达 AND／嵌套／排除／同位置绑定：

```yaml
# 旧形：或
applicable_to:
- key: shishen
  value: 七杀
- key: shishen
  value: 正官

# 新形：且 / 或 / 排除 / 同宫绑定（流式写法最不易写错缩进）
applicable_to: {all_of: [{key: ziwei_star, value: 禄存}, {key: ziwei_star, value: 天马}], same: palace}
applicable_to: {any_of: [{all_of: [{key: bamen, value: 休门}, {key: gongwei, value: 离宫}]}, {all_of: [{key: bamen, value: 伤门}, {key: gongwei, value: 坤宫}]}]}
applicable_to: {any_of: [{key: rizhu, value: 甲}, {key: rizhu, value: 乙}], none_of: [{key: kongwang, value: '*'}]}
```

`scope` 可用字段：`layer`（本命/大运/流年/流月/流日）、`pillar`（year/month/day/time）、
`palace`（**仅 ziwei**，取值须在 `ziwei_palace` 词表；七政用 `xingming` 系统的 gongwei 词表）、
`gong`（**仅 qimen**，整数 1–9）、`yao`（**仅 liuyao**，整数 1–6）。
合法取值域见 `references/vocab/fact-vocab.json`（空数组＝开放值域，任何非空串合法）。

## 判定口径（先读熟，再逐条判）

`applicable_to` 的既定语义是「**命中这些盘面谓词，这条规则才可以被引用**」——即「本盘与此条相关」，
不是「把原文条件逐字逻辑转录」。据此：

### 应该映射（mapped）

原文把**具体盘面取值**当成这条规则的对象／适用范围时：

- 「01 论木（行论 + 甲乙木 × 四季）」→ `{any_of: [{key: rizhu, value: 甲}, {key: rizhu, value: 乙}]}`
  （原文明确本条只论甲乙木）
- 「冬令日主不可无火（暖调）；夏令日主不可无水（寒调）」→
  `{any_of: [{key: yueling, value: 亥}, {key: yueling, value: 子}, {key: yueling, value: 丑}, {key: yueling, value: 巳}, {key: yueling, value: 午}, {key: yueling, value: 未}]}`
- 「神遁 休门与乙奇合九天」→ 原文条件里可被引擎事实覆盖的部分：
  `{all_of: [{key: bamen, value: 休门}, {key: bashen, value: 九天}]}` —— 但**乙奇没有对应 FactKey**，
  所以这条要么不映射，要么在台账里写明「部分覆盖」。**默认选不映射**，除非你能论证
  「乙奇缺失不影响本条与本盘的相关性判断」。不确定就不映射。
- 「天机为兄弟主星，入命主智慧善变」→ `{all_of: [{key: ziwei_star, value: 天机}], same: palace}` 不够；
  要绑到命宫：`{all_of: [{key: ziwei_star, value: 天机, scope: {palace: 命宫}}]}`

### 不许映射（unmapped）——四类，各给 reason_class

1. `not-a-condition`：**通论、体例、取象表、起例取法**。原文没有盘面适用条件。
   例：「理为体，气为用」「木主仁、性直」「六亲以本卦所属宫的五行为基准…」
   「阳干见刃位（甲见卯、丙见午…）为阳刃」（这是**怎么取**阳刃，不是**何时用**本条）、
   「十二宫次序」「十干配天文地理」「三合组合表」「旬空由十干配十二支未到之位确定」。
2. `meta-rule`：pack 元规则、调用条件、工程约束。
   例：「想调用毕法赋中的某一法」「准备引用本书…」「已按问题域确定类神，LM-R00 已通过」
   「凡查询事实层运算，必须 tool.divination.huangji，严禁 LLM 手算」。
3. `fact-not-emitted`：需要引擎**未产出**的 FactKey。写清楚缺的是哪个事实。
   例：奇门的天盘干（乙奇/丙奇/六庚）、七政的格局名与行限、六爻的卦名/六冲六合/月建日辰、
   八字的日支/大运干支/神煞具体名。
4. `condition-too-vague`：原文有条件但无法量化或读法待定。
   例：「须结合身强身弱、合冲化解综合判断，非铁定为祸」「顺逆需结合气势」
   「不能仅凭三干齐全定为有效贵格」——原文**自己**在说不能单一条件断，映射反而失真。

判不准时选 `unmapped` + `condition-too-vague` 或 `fact-not-emitted`，并在 `note` 写清理由。

### 硬禁止

- 不许用 `value: "*"` 凑数（有 `--max-wildcard 15` 门禁；`*` 只在原文确实「任意取值皆适用」时才用）。
- 不许给一条规则塞几十个枚举值来「提高命中」。
- 不许改 `statement` 去迁就谓词。
- 不许把 `kind: doctrine` 改成 `procedure` 来回避判定（本批不动 kind）。
- 不许新增/删改 FactKey 词表。

## 台账格式

`tools/reports/predicate-decisions/<art>.json`：

```json
{
  "art": "qimen",
  "generated_by": "T168 mapper",
  "decisions": [
    {
      "book": "san-shi/qimen-dunjia-tongzhi",
      "rule_id": "QM-P37",
      "decision": "mapped",
      "applicable_to_yaml": "{any_of: [{all_of: [{key: bamen, value: 休门}, {key: gongwei, value: 离宫}]}]}",
      "evidence_from_statement": "休加离",
      "note": "原文八组「门加宫」，逐组 AND、组间 OR"
    },
    {
      "book": "san-shi/qimen-dunjia-tongzhi",
      "rule_id": "QM-P01",
      "decision": "unmapped",
      "reason_class": "fact-not-emitted",
      "missing_fact": "天盘干（甲/丙）",
      "evidence_from_statement": "龙回首 甲值符加地盘丙奇",
      "note": "引擎无天盘干 FactKey，只有 bashen=值符，单映射会失真"
    }
  ]
}
```

`decision` 只能是 `mapped` / `unmapped`。`unmapped` 必须给 `reason_class` ∈
`not-a-condition` / `meta-rule` / `fact-not-emitted` / `condition-too-vague`。

## 收尾自检（必须全绿再交）

```bash
python3 tools/validate-rules.py                     # 必须 exit 0
python3 tools/test-validate-gates.py                # 必须 ALL GATES OK
python3 tools/predicate-report.py                   # 看你的 art 覆盖率变化
python3 tools/predicate-gap-report.py --art <你的art>   # 未映射条数应下降
python3 -c "
import json;d=json.load(open('tools/reports/predicate-decisions/<你的art>.json'))
print(len(d['decisions']),'条判定')"
```

台账条数必须等于你 art 的未映射总数（`predicate-gap-report.py` 报的那个数）。