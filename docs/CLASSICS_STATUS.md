# 古籍仓机读化状态

日期：2026-09-04。分支 `feat/p3-p4-machine-readable`。

**全部规则 `verified` 仍为 `false`，未经人工比对影印件，不得对外宣称「古籍已校勘」。**

## 1. 六术锚点覆盖率与导出条数

覆盖率 = 带可用 `anchor` 的规则数 / 该 art 规则总数。导出只含有锚点的 `doctrine`（`dist/rules/`）与 `procedure`（`dist/procedures/`）。

| art | 规则 | 锚点前 | 覆盖率前 | 锚点后 | 覆盖率后 | doctrine 导出前 | doctrine 导出后 | procedure |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| bazi | 522 | 38 | 7% | 453 | 86.8% | 35 | 450 | 3 |
| ziwei | 104 | 0 | 0% | 94 | 90.4% | 0 | 94 | 0 |
| qimen | 40 | 29 | 72% | 38 | 95.0% | 29 | 38 | 0 |
| liuren | 62 | 62 | 100% | 62 | 100% | 62 | 62 | 0 |
| liuyao | 168 | 25 | 15% | 143 | 85.1% | 25 | 143 | 0 |
| qizheng | 89 | 25 | 28% | 77 | 86.5% | 25 | 77 | 0 |

合计（进产品）：985 条规则，锚点 179 → 867（18% → 88.0%）。`fengshui` / `physiognomy` / `selection` / 太乙不进产品。

`python3 tools/coverage-report.py --fail-under 85`：PASS。`python3 tools/export-rules.py`：`exported=867 == anchored_exportable`。`dist/rules/ziwei.json` = 94（≥60），`dist/rules/bazi.json` = 450（≥400）。`tools/reports/anchor-mismatch.json` 长度 0。

产品仓 `cosmic-fortune-lab` 分支 `feat/structured-facts` 仅拷贝 `src/lib/rules/generated/*.json`。`bun run test` 12 files / 76 passed；`bun run build` 通过。产品仓未 push。

## 2. 无法锚定（`tools/reports/unanchorable.md`）

共 158 条保持 `anchor: null`。六术 118，其他系统 40。

| 原因 | 条数 |
|---|---:|
| quote 在 fulltext 中无法唯一定位（现代概括或多次出现） | 123 |
| pack 元规则 / 目录标题，原文无对应句 | 33 |
| `san-shi/qimen-faqiao` 仅有摘录、禁止抓现代出版社本 | 2 |

六术未锚：bazi 69、liuyao 25、qizheng 12、ziwei 10、qimen 2、liuren 0。无锚点规则不导出。

## 3. 需要人来定（`tools/reports/needs-human-review.md`）

- `qimen-faqiao` QM-P26、QM-P36：仓库无 fulltext，保持无锚。
- pack 元规则（安全改写 / 并读 / 不替代）：神峰通考、兰台妙选、卜筮正宗、星命溯源部分条。
- 原文多处出现、无法唯一落点：星命溯源若干星曜名、梅花易数五行配卦、周易折中经文。
- 现代概括：皇极经世「非占断 / 非国运 / 非个人命术」等。
- V11 与 G1：见下一节。

## 4. 校验器残留警告

实测：`python3 tools/validate-rules.py` exit 0；55 files，**113 warning，全部 V11**；**V12 = 0**。`python3 tools/test-validate-gates.py`：ALL GATES OK。

G1 写 V11 允许残留但需 < 50。当前 113 = 未锚 paraphrase 75 + 已锚原文与 `book.script` 不一致 38。

未做的处理及原因：

- 清空未锚 quote → 触发 V9 错误。
- 对 quote 做简繁转换 → 改写 quote，禁止。
- 改正 `book.script` 或放宽 V11 → 禁止放宽校验器；script 是否应随 fulltext 改，留给人。

未改 `tools/validate-rules.py` 的 V1–V12 判据。

## 5. 校勘声明

全库 1357 条规则 **`verified: true` 计数 = 0**。导出 JSON 的 `verification` 全部为 `provisional`。

机器只做了：按句读分行、把能在原文唯一（或目录+正文双处）定位的规则改写为原文连续句并写入行号锚点、覆盖率报告、CI sparse-checkout、导出交付。

**不得对外宣称「古籍已校勘」。**
