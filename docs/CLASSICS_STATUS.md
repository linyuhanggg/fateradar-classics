# 古籍仓机读化状态

日期：2026-09-04。分支 `feat/p3-p4-machine-readable`。HEAD 含 P6 质检（任务 0–8）。

**全部规则 `verified` 仍为 `false`，未经人工比对影印件，不得对外宣称「古籍已校勘」。**

本机未找到 `FATERADAR_CLASSICS_P6_GOAL.md`。任务 0→8 按 nmem 会话 `claude-code-ddeb375d-2209-4b50-a61d-7776ccd62cfd` 的任务书摘要施工，不以未读文件的 G1–G7 原文冒充已读。

## 1. 六术锚点覆盖率与导出条数

覆盖率 = 带可用 `anchor` 的规则数 / 该 art 规则总数。导出只含有锚点的 `doctrine`（`dist/rules/`）与 `procedure`（`dist/procedures/`）。

P6 **不追覆盖率**。标题 / 元数据 / 署名 / 短句无句读 / 对应度 &lt; 0.15 的锚点已降级为 `null`。覆盖率跌破 85% 是正确结果，未回填。

| art | 规则 | P5 锚点 | P5 覆盖率 | P6 锚点 | P6 覆盖率 | P6 doctrine | P6 procedure |
|---|---:|---:|---:|---:|---:|---:|---:|
| bazi | 522 | 453 | 86.8% | 397 | 76.0% | 394 | 3 |
| ziwei | 104 | 94 | 90.4% | 62 | 59.6% | 62 | 0 |
| qimen | 40 | 38 | 95.0% | 14 | 35.0% | 14 | 0 |
| liuren | 62 | 62 | 100% | 31 | 50.0% | 31 | 0 |
| liuyao | 168 | 143 | 85.1% | 113 | 67.3% | 113 | 0 |
| qizheng | 89 | 77 | 86.5% | 50 | 56.2% | 50 | 0 |

合计（进产品）：985 条规则，P5 锚点 867（88.0%）→ P6 锚点 667（67.7%）。`fengshui` / `physiognomy` / `selection` / 太乙不进产品。

`python3 tools/coverage-report.py --fail-under 35`：PASS（最低 qimen 35.0%）。CI 由 85 下调到 35，见 `.github/workflows/validate-rules.yml`。未把已降级锚点填回去以过 85。

`python3 tools/export-rules.py`：`exported=667 == anchored_exportable`；`skipped_no_anchor=318`；`skipped_other_system=372`。`dist/` 被 gitignore，条数记在 `tools/reports/p6-export.md`。`tools/reports/anchor-mismatch.json` 长度 0。

产品仓 `cosmic-fortune-lab` 分支 `feat/structured-facts` 仅拷贝 `src/lib/rules/generated/{bazi,ziwei,qimen,liuren,liuyao,qizheng}.json`（commit `c2d1d54`）。条数：bazi 394、ziwei 62、qimen 14、liuren 31、liuyao 113、qizheng 50；`verification` 全部 `provisional`。`bun run test` 12 files / 76 passed；`bun run build` 通过。产品仓未 push。

## 2. 无法锚定（`tools/reports/unanchorable.md`）

共 **462** 条保持 `anchor: null`（P5 为 158）。六术 318，其他系统 144。

六术未锚：bazi 125、ziwei 42、qimen 26、liuren 31、liuyao 55、qizheng 39。无锚点规则不导出。

P6 任务 5：扩行保留 10，短句无句读降级 46，对应度 &lt; 0.15 降级 252。完整清单 `tools/reports/p6-downgrade.md`。

## 3. 需要人来定（`tools/reports/needs-human-review.md`）

- `qimen-faqiao` QM-P26、QM-P36：仓库无 fulltext，保持无锚。未碰 `san-shi/qimen-faqiao`。
- pack 元规则（安全改写 / 并读 / 不替代）：神峰通考、兰台妙选、卜筮正宗、星命溯源部分条。
- 原文多处出现、无法唯一落点：星命溯源若干星曜名、梅花易数五行配卦、周易折中经文。
- 现代概括：皇极经世「非占断 / 非国运 / 非个人命术」等。
- P6 灰区（对应度 0.15–0.30）：机器未动，约 260 条仍带锚，留人抽检。不要为覆盖率把 &lt; 0.15 已降级条目填回去。
- V11：见下一节。

## 4. 校验器

实测：`python3 tools/validate-rules.py` exit 0；55 files，**errors 0**；**warnings 112，全部 V11**；**V12 = 0、V13 = 0、V14 = 0**。`python3 tools/test-validate-gates.py`：四道门禁 ALL GATES OK（reverse1 V5 ZPR-01；reverse2 V4 sha256；reverse3 V7 fake key；reverse4 V13 heading quote）。

P6 只新增 V13（劣质 quote ERROR）与 V14（对应度 &lt; 0.15 WARN）。`git diff` 相对 P5：V1–V12 判据字符串零删除。

G1 写 V11 允许残留但需 &lt; 50。当前 **112**（未锚 paraphrase + 已锚原文与 `book.script` 不一致）。未清空未锚 quote（会触发 V9），未对 quote 做简繁转换，未改正 `book.script`，未放宽 V11。

## 5. 校勘声明

全库 1357 条规则 **`verified: true` 计数 = 0**。导出 JSON 的 `verification` 全部为 `provisional`。

机器只做了：按句读分行、能定位的规则写入行号锚点、V13/V14 质检、标题/元数据/低对应度降级、覆盖率门禁随最低 art 下调、导出交付。

**不得对外宣称「古籍已校勘」。**
