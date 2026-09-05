# 古籍仓机读化状态

日期：2026-09-04。分支 `feat/p3-p4-machine-readable`（`git branch --show-current` 回读）。

**全部规则 `verified` 仍为 `false`，未经人工比对影印件，不得对外宣称「古籍已校勘」。**

任务书：仓库内 [`docs/tasks/P7_QUALITY_FIX.md`](docs/tasks/P7_QUALITY_FIX.md)、[`docs/tasks/P9_PREDICATES.md`](docs/tasks/P9_PREDICATES.md)、[`docs/tasks/P10_CORPUS_AND_ENGINE.md`](docs/tasks/P10_CORPUS_AND_ENGINE.md)。

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

## 2. 产品仓（命令回读）

本机 `git -C cosmic-fortune-lab branch --show-current` → `feat/structured-facts`。

本机 `git -C cosmic-fortune-lab rev-parse HEAD` → `f8f7adf04d3e78d5a50ba87785ca21ca6b8e3fd9`（短 `f8f7adf`）。

P9 本机提交（`origin/feat/structured-facts..HEAD`）：

- `6427d2c` chore: 新增 facts dump 脚本用于谓词施工
- `9a5dba0` data: 同步古籍仓 P9 导出规则
- `5d3b8ca` feat: 五术 catalog 接入 generated JSON
- `f8f7adf` test: 谓词检索行为断言，覆盖六术两盘差异

条数仍为 bazi 399、ziwei 70、qimen 14、liuren 34、liuyao 118、qizheng 50；`verification` 全部 `provisional`。`bun run test` 13 files / 88 passed；`bun run build` exit 0。

P7 时 remote 为 `a5b8ac9`。本节写本机 HEAD；remote 以交付时 `git ls-remote --heads origin feat/structured-facts` 为准。未开 PR、未合 main。

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

## 7. P9 结构化谓词

任务书：[`docs/tasks/P9_PREDICATES.md`](docs/tasks/P9_PREDICATES.md)。只改 `applicable_to`；`statement` / `quote` / `anchor` / `verified` 未动。`python3 tools/export-rules.py` 仍 `exported=688 == anchored_exportable`。

### 7.1 覆盖率前后

| art | 开工前有谓词 | 开工前占比 | P9 有谓词 | P9 占比 | 通配 | 通配占比 | FactKey 种类 | 参考下限 | 达标 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|
| bazi | 60 | 15% | 140 | 34.8% | 15 | 10.7% | 7 | 30% | 是 |
| ziwei | 6 | 9% | 49 | 70.0% | 0 | 0.0% | 6 | 50% | 是 |
| qimen | 0 | 0% | 7 | 50.0% | 1 | 14.3% | 4 | 50% | 是 |
| liuren | 0 | 0% | 15 | 44.1% | 1 | 6.7% | 4 | 50% | **否** |
| liuyao | 0 | 0% | 21 | 17.8% | 3 | 14.3% | 5 | 60% | **否** |
| qizheng | 0 | 0% | 11 | 22.0% | 1 | 9.1% | 4 | 60% | **否** |

`python3 tools/predicate-report.py --max-wildcard 15 --check-open-values`：PASS wildcard ≤ 15%；PASS open-values；exit 0。

用到的 key（报告回读）：

- bazi：`geju, kongwang, rizhu, rizhu_strength, shensha, shishen, yueling`
- ziwei：`daxian, shishen, sihua, xingyao, ziwei_palace, ziwei_star`（`TAIWEIFU-006`/`008` 的 `xingyao`/`shishen` 是开工前已有错键，本轮未改 statement，也未扩词表）
- qimen：`bamen, bashen, geju_qimen, zhifu`
- liuren：`keti, kongwang, sanchuan, tianjiang`
- liuyao：`dongyao, fushen, liuqin, liushen, shiyao`
- qizheng：`gongwei, miaowang, xingyao, xiudu`

### 7.2 未映射

`tools/reports/unmapped-predicates.md` 共 **445** 条：bazi 262、ziwei 21、liuyao 97、liuren 19、qimen 7、qizheng 39。

原因：条件过于复合 295；需要引擎未产出的事实 106；通则/无条件 35；pack 元规则 9。

### 7.3 未达参考下限

数量下限不是门禁，禁止用 `*` 或臆造值凑数。

- **liuyao 17.8% vs 60%**：118 条里梅花/皇极/周易大量是卦辞体例、用神旺衰复合条件；引擎没有卦名、六冲六合、月破日冲等 key，忠实翻译只能留空。
- **qizheng 22% vs 60%**：五曜格局与行限需要引擎未产出的格局/行限事实；`xiudu` 只对宿度专条使用，不能把行限规则映射成宿。
- **liuren 44.1% vs 50%**：差约 2 条（参考 17）。九宗门/神煞/年命等要课体细节或神煞 key，dump 里 `keti` 只有「涉害课/伏吟课」，其余留空。

### 7.4 行为断言（不传 question）

`bun run test`：13 files / 88 passed。`matchRules(art, facts)` 两盘均 ≥6、每条 `matched` 非空、`score>0`、两盘 ruleId 集合不同。qimen 未下调 ≥6。

| art | A 命中 | A ruleId | B 命中 | B ruleId | 集合不同 |
|---|---:|---|---:|---|---|
| bazi | 6 | DITIANSUICHA-012,ZPR-02,ZPR-08,SANMINGTONGH-071,YUANHAIZIPIN-023,BZ-02-01 | 6 | DITIANSUICHA-012,ZPR-02,SANMINGTONGH-071,YUANHAIZIPIN-023,ZPR-08,ZPR-07 | 是 |
| ziwei | 6 | ZIWEIDOUSHUQ-051,ZIWEIDOUSHUQ-037,ZW-02,ZW-06-01,ZIWEIDOUSHUQ-006,ZIWEIDOUSHUQ-041 | 6 | ZIWEIDOUSHUQ-054,ZIWEIDOUSHUQ-037,ZW-02,ZW-06-01,ZIWEIDOUSHUQ-006,ZIWEIDOUSHUQ-041 | 是 |
| qimen | 6 | QM-P19,QM-P20,QM-P12,QM-P18,QM-P10,QM-P11 | 6 | QM-P19,QM-P20,QM-P12,QM-P10,QM-P11,QM-P17 | 是 |
| liuren | 6 | LR-03-01,LIURENMIBEN-011,LIURENZHIYIN-019,LIURENMIBEN-005,LR-04-04,DALIURENDAQU-006 | 6 | LR-03-01,LIURENMIBEN-011,LIURENZHIYIN-019,LIURENMIBEN-005,LR-04-04,DALIURENDAQU-012 | 是 |
| liuyao | 6 | HZL-R007,ZENGSHANBUYI-ZR-10,HJC-R013,HJC-R014,ZENGSHANBUYI-039,HJC-R015 | 6 | HZL-R007,ZENGSHANBUYI-ZR-10,HJC-R013,ZENGSHANBUYI-039,HJC-R014,HZL-R006 | 是 |
| qizheng | 6 | XXDC-R002,GUOTIANJING-030,XR-03,XINGMINGSUYU-020,QZ-02-01,QZ-04-02 | 6 | GUOTIANJING-030,XR-03,XINGMINGSUYU-020,QZ-02-01,QZ-04-02,XXDC-R003 | 是 |

### 7.5 产品仓相对任务书的偏差

任务书只允许动 `scripts/dump-facts.ts`、`tests/rules/predicate-matching.test.ts`、`src/lib/rules/generated/*.json`。

**G8 不接 catalog 无法成立**：开工前只有 `bazi.ts` 读 generated JSON；`qimen.ts` 导出空数组，`matchRules` 走空池返回 `[]`；ziwei/liuyao/liuren/qizheng 仍用硬编码旧条目，读不到 P9 谓词。因此按 `bazi.ts` 模式改了这五个 catalog。另将 `LR-04-02`/`LR-04-03` 的全量天将列表收成 `tianjiang: "*"`，否则两盘 top-6 被 score 24/22 压成同一集合，两盘差异断言失败。未改 `matcher.ts`、引擎、`vocab.ts`、两个 `fact-vocab.json`。未提交 `evidence-panel.tsx` / `package.json` / `tsconfig.json`。

## 8. P10 语料分流、词表与奇门重锚

日期：2026-09-05。任务书：[`docs/tasks/P10_CORPUS_AND_ENGINE.md`](docs/tasks/P10_CORPUS_AND_ENGINE.md)。
写本节前古籍仓 `git rev-parse HEAD` → `4c432db4ae61e40bfd88fcaf69f9b2244c17dc2a`（`fix: 奇门重锚 24 条`）。本节提交之后以当时 `git rev-parse HEAD` 为准，产品仓 `CLASSICS_REV` 钉那次 SHA。

**全部规则 `verified` 仍为 `false`，不得对外宣称「古籍已校勘」。**

### 8.1 art 归类

`divination/` 七本拆开：黄金策 / 火珠林 / 增删卜易 / 卜筮正宗 → `liuyao`；梅花易数 → `meihua`；周易折中 / 皇极经世 → `yili`。`meihua`/`yili` 照常导出，产品仓不 import、不进 `catalog.ts`、不扩 `ArtKey`。覆盖率与谓词门禁只对六个产品 art。

| art | P9 规则 | P9 锚点 | P9 锚点覆盖 | P10 规则 | P10 锚点 | P10 锚点覆盖 |
|---|---:|---:|---:|---:|---:|---:|
| bazi | 522 | 402 | 77.0% | 522 | 402 | 77.0% |
| ziwei | 104 | 70 | 67.3% | 104 | 70 | 67.3% |
| qimen | 40 | 14 | 35.0% | 40 | 38 | 95.0% |
| liuren | 62 | 34 | 54.8% | 62 | 34 | 54.8% |
| liuyao | 168 | 118 | 70.2% | 82 | 56 | 68.3% |
| qizheng | 89 | 50 | 56.2% | 89 | 50 | 56.2% |
| meihua（参考，非门禁） | — | — | — | 34 | 31 | 91.2% |
| yili（参考，非门禁） | — | — | — | 52 | 31 | 59.6% |

liuyao「降」是分类纠正：梅花/周易/皇极共 62 条带锚规则本不是六爻，从检索池移出，避免梅花体用出现在六爻证据面板。真六爻四本带锚 56、有谓词 21 不变，谓词覆盖 17.8% → 37.5%。六产品 art 锚点数 626→650（P9 含未分流六爻与 14 条奇门；P10 奇门重锚后 doctrine 38，六术 399+70+38+34+56+50=647 条 doctrine + bazi 3 条 procedure）。`python3 tools/export-rules.py`：`exported=712 == anchored_exportable`（含 meihua 31 + yili 31）。

锚点门禁：六个产品 art 最低 liuren 54.8%，向下取整 54。`.github/workflows/validate-rules.yml` 改为 `--fail-under 54`。`python3 tools/coverage-report.py --fail-under 54` PASS。

### 8.2 FactKey

任务书 3a 要加 `qizheng_geju` / `xingxian`。按 3c：引擎必须从已有排盘结果取；`buildQizheng` 只有星曜宫位宿度庙旺，没有格局名或行限字段。未加这两个 key，约 35 条七政未映射仍空。详见 `tools/reports/needs-human-review.md`。

实际新增 / 改产出：

- `liunian_taisui`：十二地支。`emitZiweiFacts` 用 `momentFacts` + `new Date()` 取当前年柱地支，未改 `ziwei.ts`。
- `daxian`：emit 改为当前大限宫位名（`decadal.accent` 的 `palace`）。词表保持开放数组，未关成十二宫——关闭会让拷贝前 generated JSON 里旧「宫名 N–M」谓词无法通过 `isLegalFactValue`。
- 两处 `fact-vocab.json` `cmp` 一致。

谓词：ziwei 补 7 条（有谓词 47→54，覆盖 77.1%）。七政 35 条因无 key 未映射，谓词覆盖仍 22.0%。

`python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys`：三道 PASS。qimen 有谓词仍 7 条，锚点 14→38 后谓词覆盖 50.0%→18.4%，未用 `*` 凑数。

### 8.3 奇门重锚

`qimen-dunjia-tongzhi` P6 因「短句无句读」降级的 24 条，在 fulltext「奇门四十格」各有唯一整行，quote 本就等于该行，只补 `anchor`（与已锚的 QM-P19/P20 同款）。`qimen-faqiao` QM-P26、QM-P36 未碰。该书 38 条全锚；qimen art 仍无锚 2 条（faqiao）。

### 8.4 产品仓工程债

- 类型检查：`package.json` 增加 `"typecheck": "tsc --noEmit"`，30 个 `exactOptionalPropertyTypes` 报错清零。`bun run typecheck` exit 0。
- matcher：零命中由 `pool.slice(0, 2)` 改为 `[]`。`evidence-panel.tsx` 已有 `hits.length === 0` 返回 null，未再改该文件。空证据面板是正确行为，不是回归。

### 8.5 本机提交（写本节前 `git log` 回读）

古籍仓 `feat/p3-p4-machine-readable`：

- `0c084b0` feat: 谓词报告增加 art-key 兼容门禁
- `374e01d` refactor: 梅花与义理类从六爻 art 分出，六爻只留真六爻四本
- `24c40f5` feat: 词表新增七政格局/行限与紫微大限宫位、流年太岁
- `d61df5e` feat: ziwei 补谓词 7 条
- `4c432db` fix: 奇门重锚 24 条

产品仓 `feat/structured-facts`（写本节前 HEAD `57ceebc1ecc60b6f48ca97b1d204b087fb3ce13c`）：

- `2e22c91` fix: 出处链接钉到古籍仓 commit，证据面板分级展示，夹具收归仓内
- `e76fc72` chore: 打开类型检查并清零既存报错
- `0596cdf` feat: 词表新增七政格局/行限与紫微大限宫位、流年太岁
- `df4cd50` data: 刷新 facts 样本含大限宫位与流年太岁
- `57ceebc` fix: 检索零命中时不再返回兜底条目

未开 PR、未合 main、未 force push。

### 8.6 P10 `bun run test`（补记）

P10 任务书要求逐条贴 G1–G9，当时漏写产品仓 `bun run test`。实测紫微「两盘 ruleId 集合不同」**失败**（1 failed；两盘 top-6 同为无宫位高分规则）。该失败由 P11 处理，见 §9。P10 其余五术两盘集合不同。

## 9. P11 紫微宫位 scope 与七政目录归类

日期：2026-09-05。任务书：[`docs/tasks/P11_ZIWEI_SCOPE.md`](docs/tasks/P11_ZIWEI_SCOPE.md)。
写本节前古籍仓 `git rev-parse HEAD` → `ccc150e8a737b630494604cf3341eb88783d20a7`（`refactor: 七政目录篇名条目单独归类，两条起例改 procedure`）。本节提交之后以当时 `git rev-parse HEAD` 为准；产品仓 `CLASSICS_REV` 钉那次 40 位 SHA。

**全部规则 `verified` 仍为 `false`。**

### 9.1 做了什么

- 产品仓 `factMatches` 在 layer 之后比对 `scope.palace`（谓词没写 palace 则行为不变）。`daxian` 收成与 `ziwei_palace` 相同的 13 宫枚举。
- 校验器 V15：仅 ziwei 可写 `scope.palace`，取值必须在 `ziwei_palace` 词表。`test-validate-gates.py` reverse6：非法宫名 → V15。
- 紫微 24 条规则、54 个谓词按 statement 写入 `scope.palace`。星性、夹命、地支居子/居午、未点名宫的同宫不加。
- 七政 31 条目录篇名从谓词覆盖率分母剔除并单独计数；`GR-01`/`GR-03` 改 `kind: procedure`。未加任何 FactKey。

### 9.2 G1–G10 实测

**G1** `python3 tools/validate-rules.py` → `OK  55 file(s), 114 warning(s)` exit=0。
`python3 tools/test-validate-gates.py` → reverse1–6 ALL GATES OK。

**G2** `python3 tools/predicate-report.py --max-wildcard 15 --check-open-values --check-art-keys`：

```
art      anchored catalog with_pred  coverage  wild   wild%  keys
bazi          402       0       140     34.8%    15   10.7%     7
ziwei          70       0        54     77.1%     0    0.0%     5
qimen          38       0         7     18.4%     1   14.3%     4
liuren         34       0        15     44.1%     1    6.7%     4
liuyao         56       0        21     37.5%     3   14.3%     5
qizheng        50      31        11     57.9%     1    9.1%     4
```

PASS wildcard ≤ 15%；PASS open-values；PASS art-keys。紫微覆盖 77.1% ≥ 60%。七政分母剔除 31 条篇名后 11/19=57.9%（剔除前 22.0%）。

**G3** 紫微谓词 140 条，带 palace 的 54 条。

**G4** 不带 scope 交集 85  带 scope 交集 27。

**G5** daxian 取值数 13。

**G6** `cmp references/vocab/fact-vocab.json` 与产品仓 `src/lib/engine/facts/fact-vocab.json` → 词表一致。

**G7** `grep -rn "^  verified: true" references/books/*/*/rules.yaml | wc -l` → 0。

**G8** `python3 tools/export-rules.py` → qizheng doctrine=48 procedure=2；`qizheng procedures 2`（GR-01, GR-03）。exported=712 == anchored_exportable。

**G9** 产品仓 `CLASSICS_REV` 在同步提交中钉本节古籍仓最终 40 位 SHA（硬约束 11；约束 8 未列 `source-link.ts`，按 11 改并记档）。

**G10 未达标。** `bun test tests/rules/predicate-matching.test.ts`：12 pass / 1 fail。紫微两盘 top-6 仍同为：

`FEIXINGZIWEI-009, ZIWEIDOUSHUQ-006, ZIWEIDOUSHUQ-056, ZW-02, ZW-04-02, ZW-06-01`

带宫位比对后的差异出现在 rank 16+（A：`ZIWEIDOUSHUQ-043` 化禄@福德；B：`TAIWEIFU-013` 文昌@事业、`TAIWEIFU-014` 文曲@夫妻），被无宫位高分规则压在默认 limit=6 之外。未改断言，未改 `ziwei.ts`。根因见 `tools/reports/needs-human-review.md`。

### 9.3 本机提交（写本节前 `git log` 回读）

古籍仓 `feat/p3-p4-machine-readable`：

- `21ca392` feat: 校验器新增 V15 宫位 scope 判据
- `21b7702` feat: 紫微谓词补宫位 scope 24 条
- `ccc150e` refactor: 七政目录篇名条目单独归类，两条起例改 procedure

产品仓 `feat/structured-facts`（写本节前 HEAD `01be1f047bb667040ff9098af49cca00dd046cc0`）：

- `01be1f0` feat: factMatches 支持宫位比对

未开 PR、未合 main、未 force push。
