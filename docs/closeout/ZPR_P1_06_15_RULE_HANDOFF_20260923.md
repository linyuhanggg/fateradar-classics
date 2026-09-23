# ZPR-P1-06 辛寅甲丙主兼入口：15 条来源交接（2026-09-23）

**结论**：Classics 已把《子平真诠》[L435](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L435) 的**辛日寅月甲丙并透**清楚例型登记为 `ZPR-P1-06`，与 V5 的 14 条规则并列进入 [V6 机器交接](./P1_BAZI_TOPIC_MANIFEST_20260923_V6.json)。它仅在本命月令结构完整、甲丙透而戊未透、未见寅午戌全会时，输出两枚可并存的来源入口：甲正财为局部主，丙正官为兼。`ZPR-E-02` 本体仍 `rescue=unimplemented`、`verified=false`；本条也是 `provisional`、`verified=false`，不裁整盘成败、纯杂、作用、救应或流年吉凶。

## 来源与结构合同

- 主锚 L435 的原文直接写正财格、正官兼格；[L452](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L452)用同一甲丙并透例型说明财官相生、两相得。后者是来源**例型关系**，不能把任一真实出生盘的 Product `caige.completion=满足` 当成独立的古籍作用裁决。[L419](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L419)给寅藏甲为本主、丙可变用；[L548](../../sources/fulltext/bazi/ziping-zhenquan/fulltext.md#L548)提醒多透、透会并用，不给三透与全会时的本例型最终主次。
- Product 只生产来源中立的 `natal_yin_hidden_exposure_pattern@{layer:本命,pillar:month}`（八值，保留甲丙戊全部暴露观察）和 `natal_yin_simple_hidden_exposure_pattern@{layer:本命,pillar:month}`（七值，只有完整四柱、月支等于月令寅、月藏完整恰甲丙戊、暴露月藏干不超过两枚且无全寅午戌会时发）。二者是**单值结构事实**；缺键或同 scope 冲突为信息不足。Product 不得把 `geju.name`、`selection.sourceNamedEntries` 或本条 RuleEvaluation 回填为其 `applicableTo` 输入。
- `ZPR-P1-06` 的 `applicableTo` 只读 `gan=辛@{本命,day}` 与 `natal_yin_simple_hidden_exposure_pattern=甲丙@{本命,month}`。满足时规则行顶层 `sourceEntryOutputs` 输出 `ZPR-E-02:month-寅:hidden-甲:辛日正财`（甲／正财／主／L435）和 `ZPR-E-02:month-寅:hidden-丙:辛日正官`（丙／正官／兼／L435），每枚自带 `scope={layer:本命,pillar:month}` 与 `emitOn=满足`。此字段与 P1-03 的**顺用方向候选** `candidateOutput` 不同；后者没有被改写。
- `不满足` 只否定这一辛日寅月**清楚例型**。三透或寅午戌全会虽有完整原始事实，简明结构键故意不发，保留 `信息不足`；缺本命结构键、同 scope 冲突、只有异层事实同样未知。其它日干甲丙并透、丙戊兼透及月劫另取均不能由本条反推出唯一主格。

## 固定真日期盘与可复跑证据

共享 [`facts-sample.json`](../../tools/reports/facts-sample.json) 由 Product `buildBazi` 生成，50 张八字盘，SHA-256 `206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8`。旧 43 张盘去掉两枚新结构事实后逐项全等；两仓 fixture 字节一致。以下四柱只是机械输入，不是原书对现代真盘结局的裁决。

| 样盘 ID（上海黄浦区，时钟时间） | 四柱 | P1-06 |
| --- | --- | --- |
| `caseP1_ZPR_month_xin_jia_bing_1954`，1954-02-14 02:20 | 甲午／丙寅／辛丑／己丑 | 满足 |
| `caseP1_ZPR_month_xin_jia_bing_1984`，1984-02-07 10:20 | 甲子／丙寅／辛未／癸巳 | 满足 |
| `caseP1_ZPR_month_xin_no_jia_1979`，1979-02-13 10:20 | 己未／丙寅／辛亥／癸巳 | 不满足；仅此甲丙主兼例型无甲 |
| `caseP1_ZPR_month_xin_jia_bing_wu_1984`，1984-02-07 20:20 | 甲子／丙寅／辛未／戊戌 | 信息不足；三透 |
| `caseP1_ZPR_month_xin_jia_bing_meeting_1994`，1994-02-14 12:20 | 甲戌／丙寅／辛未／甲午 | 信息不足；寅午戌全会 |

全部 50 盘分布为**满足 2、不满足 44、信息不足 4**；另有从真实正例删除结构键、同 scope 写冲突值、异层污染三项投影均为信息不足。运行：

```sh
python3 tools/verify-p1-bazi-v6-handoff.py --compare-product-fixture
python3 tools/verify-zpr-e-02-xin-yin-jia-bing-priority.py
python3 tools/verify-zpr-e-02-yin-bing-principal.py
python3 tools/validate-rules.py --book bazi/ziping-zhenquan --json
```

V6 整文件 SHA-256 `39e53a6c5c3693334209d80eb2f9e9002339fff2117b64f1988d6f2a02f344a6`，来源提交 `4434c43e7c729c1547f49897bb227870b8d402a0`；V5 整文件 SHA-256 `7ea7b0214f1150c522273133febf3575f8821bc5fddd7c4d2cca1e3b2a36d802`，14 条旧规则对象在 V6 中完全相同。Product 在验证其生成规则与新 `sourceEntryOutputs` 后可运行：

```sh
python3 scripts/import-bazi-topic-handoff.py /Users/sync/code/fateradar-classics/docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json
```

[L419 丙独透候选](./ZPR_E_02_YIN_BING_PRINCIPAL_CANDIDATE_20260923.md)虽有 1969、1979 两枚共享真盘局部正例，仍未正式化为 `ZPR-P1-05`：木日寅月的禄劫另取与丙独透先后，以及丙戊兼透时「前件满足但局部主次未知」，尚无一个只靠现有通用谓词就能忠实表达的三态合同。其 Product 局部观察可保留，但不得以顺手把木日或兼透判“不满足”的方式填补来源门禁。
