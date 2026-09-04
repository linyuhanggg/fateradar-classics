# 古籍仓机读化状态

日期：2026-09-04。分支 `feat/p3-p4-machine-readable`（`git branch --show-current` 回读）。

**全部规则 `verified` 仍为 `false`，未经人工比对影印件，不得对外宣称「古籍已校勘」。**

任务书：仓库内 [`docs/tasks/P7_QUALITY_FIX.md`](docs/tasks/P7_QUALITY_FIX.md)。

## 1. 六术锚点覆盖率与导出条数

覆盖率 = 带可用 `anchor` 的规则数 / 该 art 规则总数。导出只含有锚点的 `doctrine`（`dist/rules/`）与 `procedure`（`dist/procedures/`）。

| art | 规则 | P6 锚点 | P6 覆盖率 | P7 锚点 | P7 覆盖率 | P7 doctrine | P7 procedure |
|---|---:|---:|---:|---:|---:|---:|---:|
| bazi | 522 | 397 | 76.0% | 402 | 77.0% | 399 | 3 |
| ziwei | 104 | 62 | 59.6% | 70 | 67.3% | 70 | 0 |
| qimen | 40 | 14 | 35.0% | 14 | 35.0% | 14 | 0 |
| liuren | 62 | 31 | 50.0% | 34 | 54.8% | 34 | 0 |
| liuyao | 168 | 113 | 67.3% | 118 | 70.2% | 118 | 0 |
| qizheng | 89 | 50 | 56.2% | 50 | 56.2% | 50 | 0 |

P7 未追覆盖率。重测最低 art 仍是 qimen 35.0%，向下取整 35。`.github/workflows/validate-rules.yml` 已是 `--fail-under 35`，未改文件。

`python3 tools/export-rules.py`：`exported=688 == anchored_exportable`；`skipped_no_anchor=297`；`skipped_other_system=372`。`tools/reports/anchor-mismatch.json` 长度 0。

## 2. 产品仓（命令回读，已 push）

本机 `git -C cosmic-fortune-lab branch --show-current` → `feat/structured-facts`。

本机 `git -C cosmic-fortune-lab rev-parse --short HEAD` → `a5b8ac9`。

`git log --oneline -1` → `a5b8ac9 data: 同步古籍仓 P7 导出规则`。该提交只含 `src/lib/rules/generated/{bazi,liuren,liuyao,ziwei}.json`（qimen/qizheng 与上一份字节相同，无 diff）。

条数：bazi 399、ziwei 70、qimen 14、liuren 34、liuyao 118、qizheng 50；`verification` 全部 `provisional`。`bun run test` 12 files / 76 passed；`bun run build` exit 0。

`git -C cosmic-fortune-lab push -u origin feat/structured-facts` 成功。`git ls-remote --heads origin feat/structured-facts` → `a5b8ac9b9b6b2cbbee7caba392cb92d5765f61eb	refs/heads/feat/structured-facts`。未开 PR、未合 main。

> 任务书第四节写「本机没有 feat/structured-facts、c2d1d54 不存在、generated 未跟踪」。那是另一台机器的状态。**本机实测上述分支和 hash 均存在**，按诚实性硬规定写本机回读结果，不把任务书里的「不存在」抄进文档。

## 3. P7 做了什么

1. **繁简表**：`fold_han()` 不再用 52 对 `SCRIPT_PAIRS`。本机 `python3 -c "from zhconv import convert"` 失败（未装 zhconv，PEP 668 不能 pip）。按任务书回退到已装的 `opencc` t2s。`SCRIPT_PAIRS` / V11 未改。自检 `fold_han('相衝者')=='相冲者'`、`correspondence('冲破六冲', …) >= 0.3` 通过（实测 0.333）。
2. **恢复 33 条**：从 `0abcf1e` 原样取回 `anchor`（quote 与 P5 已一致，未改字）。`FZ` 仍为 `anchor: null`。原名单第 34 条 `LZ`（`physiognomy/liuzhuang-xiangfa`）quote 是 `source_base:` 元数据，名单误列，已撤回为 `anchor: null`。
3. **V13**：增补 `>` 前缀；署名正则收紧为朝代 + 2–6 个连续汉字人名 + `撰|輯|編|著述|辑录|輯錄`（不再用 `\S{0,12}`，避免把「清濁…著三才」判成署名）。`META_QUOTE_RE` 已覆盖 `raw_file|section_note|source_base`。`LIURENMIBEN-020` 找不到正文断辞，`anchor: null`。`test-validate-gates.py` 有 reverse5。

## 4. 校验器（实测）

- `python3 tools/validate-rules.py`：exit 0。`OK  55 file(s), 114 warning(s)`，**errors 0**。warnings：V11 = 112，V14 = 2（`FEIXINGZIWEI-008` 0.140、`ZIWEIDOUSHUQ-ZW-05` 0.106）。V12 = 0，V13 = 0。
- `python3 tools/test-validate-gates.py`：reverse1–5 ALL GATES OK。
- `python3 tools/coverage-report.py`：六术与上一份相同（LZ 是相法，不进产品）——bazi 77.0% / ziwei 67.3% / qimen 35.0% / liuren 54.8% / liuyao 70.2% / qizheng 56.2%。
- `python3 tools/export-rules.py`：`exported=688 == anchored_exportable`。
- V1–V12 判据字符串与 `SCRIPT_PAIRS` 未改。

## 5. 无法锚定与人审

`tools/reports/unanchorable.md` 仍以 P6 的 462 为底，P7 追加 `LIURENMIBEN-020`，并记入撤回的 `LZ`（原因：quote 是 source_base 元数据，P7 恢复名单误列，已撤回），未重扫全表。`qimen-faqiao` QM-P26、QM-P36 未碰。灰区未动。详见 `tools/reports/needs-human-review.md`。

## 6. 校勘声明

全库 1357 条规则 **`verified: true` 计数 = 0**。导出 JSON 的 `verification` 全部为 `provisional`。

**不得对外宣称「古籍已校勘」。**
