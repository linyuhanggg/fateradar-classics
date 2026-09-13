# 独立复核：A1 / A3 / A7 / A8 证据真实性与时效（2026-09-13）

- 任务：t5（fateradar-closeout，审阅者 `reviewer`）
- 复核时间：2026-09-13 10:05–10:25 (+0800)
- 复核基准（实测，非转抄）：classics `dsh/full-library-classics` = `origin/main` = **eb4cabe**；product `dsh/full-library-product` = `origin/main` = **230effd**（远端经 `git ls-remote` 独立确认，见 §5）
- 立场：**不采信任何成员自报数字**。以下每个数字都由本轮自己重算、自己跑生成器、自己查 gh 得出；账本 `DELIVERY_ACCEPTANCE.json` 的数字只在被复现时引用，未被复现的一律指出。
- 副作用声明：**没有写两个工作树的任何文件**（未 commit/push/merge，未动 contest-evidence 现场，未动 `_probe-a6.test.ts`）。矩阵与 bazi 产物在镜像 `/tmp/rev/product-mirror`（rsync 排除 `.git/.output/.env/artifacts`，`node_modules` 软链回原文）内重新生成；调候产物 `--output` 指向 `/tmp`。未对 `/Users/sync/code/*` 做任何操作。

## 0. 结论速览

| 条目 | 账本状态 | 本轮独立结论 | 是否可判 pass |
| --- | --- | --- | --- |
| A1 | working | 三个核心实测值**完全复现**；但两件被引用的证据物**已过期/自相矛盾**（§1.3、§1.4） | 否（证据时效缺陷） |
| A3 | working | 矩阵在最新 HEAD 重生成，**账本声称的每个数字都复现**；但已提交矩阵仍有 68 行过期（账本自己也登记了） | 否 |
| A7 | working | 救应四值 117/106/30/5 **精确复现**；30 条 unimplemented **每条都有具名理由**；66 条改标 self 有**真实实现**，不是无证据升级 | 否（但本节最大质量风险已排除） |
| A8 | working | CI 两项结论**独立证实**；但「内容导出与代码版本可对应」**实测不成立**：bazi 产物 183 条里 54 条与最新 main 重生成不一致，`CLASSICS_REV` 落后 1750 个提交 | 否（新增可复现阻塞项） |
| （越界发现）A6 | working | 账本「其他七术缺 dedicated free-reading builders」与 HEAD 实况**直接矛盾**（八术早已各有 builder 且已进路由） | 不是 pass 主张，但账本条目必须改写 |

八项验收**无一条**因本轮复核达到 pass 条件；本轮把 A8 一条含糊的「版本钉需复核」变成了可复现的缺口，并推翻了 A6 的一条主要缺口描述。

## 1. A1 全库去向

### 1.1 复现的实测值（自己重算，脚本 `scripts-20260913/count_ann.py`）

扫 `references/annotations/**/*.json` 全量：

```
files 79   distinct bookSlug 53   total entries 62839
review: {source-reviewed: 60004, draft: 2835}
entries without paragraphId: 0
books with draft: 15
```

与账本 `measured_baseline` 的 `annotations_total 62839 / source_reviewed 60004 / draft 2835 / annotation_books 53 / books_with_draft 15` **逐项吻合**。逐书 draft 也与账本清单吻合：`qimen-dunjia-tongzhi 1261`、`daliuren-daquan 773`、`mayi-shenxiang 239`、`yuqia-ji 180`、`mingli-yueyan 162`、`liuren-miben 124`、`huangji-jingshi 40`、`ziwei-doushu-quanshu 40`。

**一处措辞不实（低危）**：账本 A1 remaining 写「其余 7 书 2–4」，实测其余 7 书为 `dili-bianzheng 4、tianyu-jing 4、sanming-tonghui 2、yuzhao-shenying 2、xingxue-dacheng 2、luoluzi-sanming 1、xingli-kaoyuan 1` —— **有 1 书是 1 条，不是 2**；区间应为 1–4。

另：62,839 条**全部**带 `paragraphId`（0 缺失），这是 A2 的「全部带 paragraphId」在数据层的独立支撑（页面展示层不在本轮）。

### 1.2 资料包数与账本措辞

`references/annotations` 53 书 vs 去处表 54 行：差的一本是 `shenshi-xuankong-xue`（**0 条注解**），实测并非漏列。

- 去处表 §1 有 **54 个书行 + 1 个 `files` 伪行**；表内合计行写「**合计（55 书）**」——把伪行算成了书。
- `sources/fulltext/**/fulltext.md` 实测 **54 份**，与 54 个书行**完全同集**（双向差集皆空）；`sources/facsimile` 下 PDF 实测 **41 份**，与表内影印列合计一致。
- 因此账本 A1 的「55 个资料包（**54 全文 + 2 补充 MD**）」在算术上讲不通（54+2=56≠55），且「55」实际是「54 书 + 1 伪行」。建议改为：「54 书（53 有注解条目 + 1 无条目）+ 1 影印杂项行；全文 54 份、影印 41 份」。

### 1.3 证据物已过期：`FULL-LIBRARY-DISPOSITION-20260912.md` 的救应列

该文件是 A1 的首条证据（`kind: script-generated+classified`），但其 §1 合计行的救应与当前数据不符：

| 位置 | 文件写的 | 本轮实测 |
| --- | --- | --- |
| §1 合计行 | `116/32/105/5`（self/unimpl/none/交叉） | **117/30/106/5** |
| `qiongtong-baojian` 行 | `66/11/43/0` | **66/10/44/0** |
| `sanming-tonghui` 行 | `4/7/9/0` | **5/6/9/0** |

差值自洽：`-2 unimplemented`、`+1 self`、`+1 none`，正好是账本 A7 登记的两次裁决（`QTB-M-02-12 → none`、`QTB-M-05-11 → self`）与 `SMTH-E-14 → self` 之后的快照漂移。**当前数据才是对的**（与账本 recomputed-now 及本轮重算三方一致），过期的是这份文档。

**建议**：A1 保持 working，并把「去处表合计行/逐书救应列按当前 `references/executable` 重生成」写成剩余项——它是脚本生成的产物，重跑即可，但这正是「报告已写 ≠ pass」的实例。

### 1.4 证据物已过期：`GAP_LEDGER.json` 的顶层计数与基线

A1 第二条证据引用 `GAP_LEDGER.json`（`drafts_by_file`、`page_consumers`、`recovered`）。逐字段实测：

| 字段 | GAP_LEDGER 写的 | 本轮实测/现状 |
| --- | --- | --- |
| `counts.source_reviewed` | 59,934 | **60,004** |
| `counts.draft` | 2,905 | **2,835**（账本已承认这一处） |
| `baselines.classics_origin_main` | `4cb96e3` | **eb4cabe** |
| `baselines.product_origin_main` | `48f68a8` | **230effd** |
| `counts.merged_main` | **false** | **true**（两分支 HEAD 均为各自 origin/main，见 §5） |
| `drafts_by_file` | 17 项合计 2,905 | 17 个文件含 draft，合计 **2,835** |

`draft_files = 17`（文件数）是对的；把 17 误读成「15 书」是维度混淆（15 是**书**数，17 是**文件**数）。`merged_main: false` 是**当前可直接证伪**的字段，账本的「其余为本次直接实测」不覆盖它。**建议**：把 GAP_LEDGER 的过期字段列出为 A1 的显式剩余项，不要让它继续被下游当现状引用（历史轮次已有同类教训：`docs/CLOSEOUT_20260912.md:8` 与 `GOAL_CHECKPOINT.md:33` 的旧计数）。

## 2. A3 规则可追（矩阵重生成）

### 2.1 重生成方法与可复现命令

```
rsync -a --exclude .git --exclude node_modules --exclude .output --exclude .env \
      --exclude .tanstack --exclude artifacts <product>/ /tmp/rev/product-mirror/
ln -s <product>/node_modules /tmp/rev/product-mirror/node_modules
cd /tmp/rev/product-mirror
FATERADAR_CLASSICS_ROOT=/Users/yuhanglin/fateradar-goal-20260912/classics \
  bun scripts/art-verdict-judgment-gap-matrix.ts
```

产物已存档在 `docs/closeout/review/art-verdict-judgment-gap-matrix-REGEN-20260913.{json,md}`（json md5 `c5fe97cf394a8ebbe7177f5d0d571fb2`）。

**镜像 = HEAD 内容（逐文件字节级证明，非状态推断）**：镜像快照取自 2026-09-13 约 10:03–10:04（矩阵 `generated_at` = `2026-09-13T02:04:04Z`）。事后按 `git ls-files` 取矩阵输入范围（`src/engine`、`tests/engine`、`docs/implementation`、矩阵脚本本身）共 **271 个 tracked 文件**，逐个与 `git show HEAD:<path>` 的 md5 比对：

```
271 个文件中，与 HEAD 不同的只有 2 个：
  docs/implementation/art-verdict-judgment-gap-matrix.json   ← 本轮重生成（预期）
  docs/implementation/art-verdict-judgment-gap-matrix.md     ← 本轮重生成（预期）
缺失文件：0
```

即除我自己重生成的矩阵两件产物外，**其余 269 个输入文件与 HEAD `230effd` 逐字节相同**，`product_head` 记 null 只是镜像内无 `.git`。

**时间线提醒**：快照之后（10:06–10:16）product 工作树被另一名成员的在途工作改动（A6 六爻/紫微免费解读消费者方向，见 §6），因此「工作树干净」只在快照时刻成立，不能当成现状；本节所有结论仍以 10:04 快照（= HEAD）为准。

### 2.2 账本 A3 声称的每个数字都复现

| 账本 A3 evidence 声称 | 本轮重生成实测 | 结论 |
| --- | --- | --- |
| `static_parse_matches_runtime=true` | `true`（静态 252 / 运行时 252） | ✅ |
| `coverage_index_missing=0` | `0`（wired 258 / missing 0） | ✅ |
| `ids_without_probe` 空 | `[]` | ✅ |
| `assertions_parsed=418` | `418`，28 文件，逐文件分布一致 | ✅ |
| `0 条无归因` | `status_assertions_unattributed = 0`；另有 356 条经真实执行确认「实际==断言」、45 条运行时执行不可得（**非**无归因） | ✅ |
| `runtime_probe_status_mismatch_assertions` | `0` | ✅ |
| `duplicate_classics_ids` / `ids_missing_from_classics_executable` | `[]` / `[]` | ✅ |
| 古籍 executable 258 条 / 15 文件 | `258 / 15` | ✅ |

### 2.3 已提交矩阵与最新 HEAD 的差异：仅限救应字段，共 68 行

旧矩阵（`product_head=cdb5f9c`、`classics_head=74edada`）与本轮重生成逐字段比对：

- `summary` 只有 **2 个键**不同：`classics_rescue_vocabulary`（旧 `{none:106, unimplemented:97, self:50, 交叉5}` → 新 `{self:117, none:106, unimplemented:30, 交叉5}`）与 `consumer_scan`（消费者文件清单顺序/成员的差异）。
- `rows` 252 行中 **68 行**变化，变化字段**只有** `classicsRescue`（68 行）与 `classicsUnknownWhen`（2 行：`QTB-M-02-12`、`QTB-M-05-11`）。
- 68 行的迁移分布：`unimplemented→self` 66 条、`unimplemented→none` 1 条、`none→self` 1 条。对应 classics 侧提交 `8cdbc0f/6c20e9c/35d85e9`（调候救应三批）、`058de2e`、`6ef9ac8`、`7f11f66`。
- **断言/归因/覆盖/缺口等判定性字段全部不变**：418 断言、0 无归因、`gap_fail_ids=[]`、`gap_unknown_ids=[DLD-E-02…E-09]`、三态齐全 30、覆盖索引 0 缺失。

**结论**：账本「矩阵需在最新 main 重新生成」这一剩余项**为真且代价很小**（只有救应字段会变），但**已提交产物仍过期**，故 A3 不能判 pass，除非把重生成产物归档。缺口侧的真实读数（供 A4 使用，非本轮结论）：信息不足分支 `asserted 49 / not-applicable 195 / gap 8`；不满足分支 `asserted 224 / not-applicable 28 / gap 0`；三态齐全 30；64 条规则在任何产物里查不到其 ID（矩阵自述为「编号不上页面」，并附字段路径弱证据）。

## 3. A7 已知错误与救应

### 3.1 救应四值精确复现（脚本 `count_exe.py` / `per_book_rescue.py`）

扫 `references/executable/*.json`（15 个 json 文件）：

```
total rules 258        by art {bazi:183, liuren:23, liuyao:21, ziwei:12,
                               qimen:6, qizheng:6, xiaoliuren:6, meihua:1}
rescue {self:117, none:106, unimplemented:30, ZPR-E-03:2, ZPR-E-08:2, ZPR-E-05:1}
duplicate ids: []      missing keys: {}
```

与账本 A7 的「self 117 / none 106 / unimplemented 30 / 交叉 5（ZPR-E-03×2、ZPR-E-05×1、ZPR-E-08×2）」**完全一致**；`rules_by_art` 也与 `measured_baseline` 逐项一致。**注意**：1.3 节那份去处表合计行（116/32/105/5）是三方里唯一不符者。

### 3.2 30 条 unimplemented 是否「逐条具名理由」——是

取出 30 条 ID 后逐条回查 `docs/closeout/RESCUE-LABEL-AUDIT-20260912.md`（232 个判定行）：**30/30 全部命中**，即每条都有判定 + 置信 + 逐字引文 + 理由。抽查 `SMTH-E-08`（劫煞落柱）在 `has_rescue` 组内，理由为「劫煞本为凶煞（古歌云劫煞为灾不可当），原文另立逢生、遇官星则反成显贵掌兵权之救应」，并在该文件 §`SMTH-E-08` 专节明写「**保持 `unimplemented`**（只是条件层建起来了）」。

**一处账本枚举不全（低危）**：A7 remaining 列了 `SMTH-E-04/06/07/10` 与 `SMTH-E-09`，但同为 unimplemented 的 **`SMTH-E-08` 未列入**。建议补上（A4 的「30 条逐条具名」口径不受影响，因审计文件已覆盖全部 30 条）。

### 3.3 66 条「改标 self」是有实现支撑的，不是无证据升级 —— 本轮最重要的一条否定性结论

风险点：把 `unimplemented` 改成 `self` 等于宣称「本条自身即救应条款且已实现」，若只改标签就是账本最忌讳的「无证据升级」。独立验证：

```
tiaohou-rescue.ts 内提取 id: "QTB-…"  → 66 条，去重 66
QTB 规则中 rescue=self              → 66 条
两者差集：双向皆空（完美一一对应）
```

66 条逐条在 `implementation_assumption` 里写明实现位置与口径，例如 `QTB-M-01-03`：「救应句『若有壬癸破火，堪作秀才。』已实现（产品仓 `src/lib/engine/bazi/tiaohou-rescue.ts`）：只判原文点名的天干在不在盘上——原文说『透／出干／露』的按透干判，只说『见／有／得』的按透干或藏支判（仅藏支时两读并列、给信息不足，不择一）」。`tiaohou-rescue.ts` 头部另用 30 条量级的具名理由解释**每条**仍留 `unimplemented` 的原因（如 `QTB-M-02-04`「救应落在大运不在原局」、`QTB-M-10-09`「一句话里四者并见，必要条件原文未分」）。抽查 `QTB-M-06-12` 未在头部单独出现，实为与 `QTB-M-06-11` 同句并写（`QTB-M-06-11`／`06-12`），**不是缺理由**。

**结论**：A7 的救应标签体系当前自洽、可追溯、有实现与原文双重支撑。**但这不等于 A7 可判 pass**——A7 还要求「明确不支持的学派/能力**单列清单**需与 unimplemented 30 条对齐」：我在 `product/docs`、`product/src` 全量检索后**未找到**任何文档把 30 条 unimplemented 集中成「不支持的学派/能力」单列清单（`docs/SCHOOL_DIVERGENCE.md` 是排盘口径与流派差异，不含这 30 条）。该剩余项**属实**。

## 4. A8 两仓检查、版本对应、集成验收

### 4.1 CI 与远端（独立查证，账本此行属实）

| 项 | 账本写的 | 本轮独立查证 |
| --- | --- | --- |
| classics main + CI | `eb4cabe`，run 34731428150 success | `git ls-remote` → `refs/heads/main = eb4cabe49506b0…`；`gh run view` → `validate-rules`，`headBranch=main`，`headSha=eb4cabe…`，`conclusion=success` ✅ |
| product main + CI | `230effd`，run 34731425370 success | `git ls-remote` → `refs/heads/main = 230effd2f5a3e8…`；`gh run view` → `ci`，`headBranch=main`，`headSha=230effd…`，`conclusion=success` ✅ |
| 分支已集成 | 两分支 HEAD 均为 origin/main 祖先 | 本地 `dsh/…` HEAD 与 `origin/main` 同点 ✅ |

product CI 的 19 个步骤全绿，含 `lint:ci`、`lint:backend`、`typecheck`、`test`、`FATERADAR_TARGET=node build`、`build:worker`、`playwright test`（`test:e2e`）。也就是说**冻结提交上确实跑过端到端集成**——比账本 A8 自己列的证据（都早于第 43/44 轮）更新，且 CI 是正确的检查结论来源。

### 4.2 实测不成立的一条：「内容导出与代码版本可对应」

**（a）`CLASSICS_REV` 落后 1750 个提交。** `product/src/lib/rules/source-link.ts`：

```
export const CLASSICS_REV = "3dc9d01b69bbefdd85e3fefb548d4d0831d36626";  // 2026-09-07
```

`git -C classics` 实测：该提交存在、是 `eb4cabe` 的祖先、**落后 1750 个提交**（2026-09-07 14:12）。该常量用于生成**用户可见**的原文行号链接（`classicsSourceUrl`），并写入 `evidence.ts` / `readings/context.ts` / `evidence-db.server.ts` 的 `classicsRevision`；product CI 也把同一 SHA 钉在 `.github/workflows/ci.yml`（`ref: 3dc9d01…`）作稀疏检出。

**（b）但锚点本身当前仍然对得上——本轮做了最严的一遍**（脚本 `anchor_exact.py`）：从 `src/lib/rules/generated/*.json` 取出**全部 643 条带 anchor 的规则**，对每条把 **完整引文**（去空白归一化后）与锚点行区间 `[startLine, endLine]` 的**拼接原文**做包含判定，分别在 `3dc9d01` 与当前 `eb4cabe` 两份 blob 上跑：

```
643 / 643 在锚点区间内（@pin 3dc9d01）
643 / 643 在锚点区间内（@HEAD eb4cabe）
失败 0 条；23 个锚点文件在两个 revision 均存在
```

→ 结论要**分开说**：钉的提交很旧，但**行号锚点没有漂移**，当前不会产生「链到别处」的引文错误（A2 的规则级可回溯性在此得到强支撑；页面渲染层不在本轮）。

**（c）真正不成立的是生成产物本身：`bazi-anchor-rule-index.json` 与最新 main 重生成不一致。** 该产物自带 `sourceRevision = df73f2324c899b2f316d136de06be560c0ce4054`（落后 42）。在镜像内用 product 自己的生成器重跑（`CLASSICS_ROOT` 指向真 classics）：

```
committed sourceRevision = df73f23…   fresh sourceRevision = eb4cabe…
除 revision 外完全相同？ False
  rules[183] 中 54 条不同（长度 158,666 → 173,722 字节）
  逐条差异：quote / fragments 的原文范围被扩展，补入救应句所在段
```

例：`QTB-M-01-03` 旧产物只含 `L0089`；重生成后含 `L0089 + L0093 + L0099`（正是「若有壬癸破火，堪作秀才」那句所在的段）。这正是 §3.3 那批救应实现的直接后果——**classics 侧已进 main，product 侧的生成产物没有跟着重导出**。

作为对照，`tiaohou-profiles.json`（`sourceRevision 83c654b`，落后 23）重生成后**除 revision 字段外逐字节相同**（profiles/book/sources 三段全同）——即该文件的钉只是**戳记过期**，内容没过期。

**建议（A8 明确剩余项，替换原来含糊的「版本钉需复核」）**：
1. 重导出 `src/lib/engine/generated/bazi-anchor-rule-index.json`（183 条里 54 条过期），归档并核对；重导出时 `sourceRevision` 会自然更新到当时 classics HEAD。
2. 复核 `CLASSICS_REV` 与 CI 的 classics `ref`：本轮证据表明二者**可以**保持（643/643 锚点未漂移），但必须写明「钉的提交 ≠ 内容来源提交」，或把它更新到与产物 `sourceRevision` 一致的提交后重验锚点。
3. 顺带核对其余生成产物：`liuren/liuyao/qimen/qizheng/ziwei-source-rules.json`、`reading-notes.json` 的 `sourceRevision` 分别为 `a6c0182(1490 落后)/b8150a7(1403)/5379881(1570)/3fbef8c(1399)/3ca4a47(1627)/a8edc92(1650)`，本轮**未**逐条重导出比对（它们在 product 侧的生成器不在 `scripts/` 的既有清单里，需要先定位生成器），列为待办而非结论。

### 4.3 网页端到端验收

CI 在 `230effd` 上跑过 Playwright e2e（步骤 19 success），这是**最新 main 上真实的端到端集成证据**，比账本 A8 现列的三份记录更新。但两点限制：(1) CI 的 classics 检出是被钉的旧提交（§4.2a），故 e2e 没有在**当前**古籍内容上跑；(2) A6 的「八术栏目免费解释 + 切换资料/位置后更新」属于浏览器实测口径，不在本轮（属 `page-acceptance`）。**A8 的「端到端集成验收需在最新 main 重跑」建议改写为**：CI e2e 已在 230effd 通过（可作证据），但需补一次以当前 classics 内容为准的浏览器验收记录。

## 5. 越界但高优先：账本 A6 的主要缺口描述与 HEAD 实况矛盾

`DELIVERY_ACCEPTANCE.json` A6 remaining 第 1 条：「**其他七术缺 dedicated free-reading builders**（紫微/奇门/六壬/六爻/梅花/小六壬/七政主要栏目）」；`GAP_LEDGER.json#page_consumers.other_arts`：「dedicated free-reading builders missing except bazi」。

在 product HEAD `230effd`（= main）上**实测**：

```
src/lib/engine/{bazi/,}free-reading 族（tracked at HEAD）：
  bazi/free-reading.ts, ziwei-free-reading.ts, liuren-free-reading.ts, liuyao-free-reading.ts,
  meihua-free-reading.ts, qimen-free-reading.ts, qizheng-free-reading.ts, xiaoliuren-free-reading.ts
src/components/art-free-reading.tsx（共享组件）
8 个路由均已 import 并使用 ArtFreeReading：
  chart.bazi / chart.ziwei / chart.liuren / chart.liuyao / chart.meihua / chart.qimen / chart.qizheng / chart.xiaoliuren
testId：liuren 4 处，ziwei/liuyao/meihua/qimen/qizheng/xiaoliuren 各 2 处
测试：tests/engine/art-free-reading-round1.test.ts、art-free-reading-testids.test.ts（均在 HEAD，CI 已跑过）
```

最后一次改动 `73cc539`（2026-09-13 07:29 +0800），**早于**账本 `generated_at = 2026-09-13T02:05:00Z`（= 10:05 +0800）。

**建议**：A6 remaining 第 1 条改为「八术主要栏目免费解释的**浏览器实测覆盖面**与**切换资料/位置后旧结论不残留**（切换项已是第 2 条）」，并重新基线化 `GAP_LEDGER.page_consumers`。这不构成 A6 pass（页面实测未做），但账本现在这句是**事实错误**，会误导后续派单与收尾判断。另：复核结束时已看到同队成员正在该方向施工（未跟踪 `docs/implementation/A6-LIUYAO-ZIWEI-FREE-READING.md` + `tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts`，并改了 `ziwei/liuyao-free-reading.ts`、`evidence-panel.tsx`、`chart.ziwei.tsx`，见 §6），与「builder 早已存在、当前缺的是消费者接线与实测」这一判断同向。

## 6. 工作树卫生（不影响任何计数，但会影响提交）

**快照时刻（10:03–10:04）**的 product 工作树：除队长已知的 5 项 contest-evidence 现场外，另有 1 个未跟踪文件 `tests/engine/_probe-a6.test.ts`（mtime 10:03，`ziwei-free-reading`/`liuyao-free-reading` 的打表临时探针，含 `console.log`）。该文件当时**不影响矩阵计数**（矩阵只解析 `tests/engine/art-verdict-judgment-*.test.ts`，实测 28 文件合计 418 条断言，不含它），也不影响 CI（未跟踪）。我在快照里保留了它的副本（`/tmp/rev/product-mirror/tests/engine/_probe-a6.test.ts`），**未改动它**。

**复核结束时（10:20）再查**：该探针文件已被其作者删除；同一成员的在途改动扩展到：

```
M  src/components/evidence-panel.tsx
M  src/lib/engine/liuyao-free-reading.ts
M  src/lib/engine/ziwei-free-reading.ts
M  src/lib/reading-input-export.ts
M  src/routes/chart.ziwei.tsx
M  tests/engine/c-export-readback-seven-arts.test.ts
M  tests/engine/reading-input-export-link.test.ts
M  tests/engine/ziwei-viewdate-free-reading.test.ts
M  benchmarks/mingli-contest-2024/README.md
?? docs/implementation/A6-LIUYAO-ZIWEI-FREE-READING.md
?? tests/engine/a6-liuyao-ziwei-free-reading-consumers.test.ts
?? benchmarks/mingli-contest-2024/resolutions.template.json
?? scripts/contest-evidence.ts
?? scripts/lib/contest-evidence.ts
?? tests/contest-evidence.test.ts
```

这是**另一个批次（A6 六爻/紫微免费解读消费者）的现场**，我全程只读、未 clean / 未 stash / 未改动。提示两点：①它与 §5 的 A6 结论同向——A6 的消费者侧工作正在推进，账本那条「builder 缺失」更确定是过期描述；②这些改动落在 `tests/engine`、`src/lib/engine` 内，**会让后续「在最新 HEAD 上重跑矩阵/测试」的快照不再等于 HEAD**——任何人重跑前必须先固定快照（本轮用的镜像法可复用），否则会把在途工作算进 HEAD 证据。

## 7. 对账本的逐条建议改动

| 条目 | 现在 | 建议 |
| --- | --- | --- |
| A1 | working | 保持 working。新增两项剩余：①`FULL-LIBRARY-DISPOSITION-20260912.md` §1 合计行与两行逐书救应列重生成（116/32/105/5 → 117/30/106/5）；②`GAP_LEDGER.json` 顶层计数与基线刷新（60,004/2,835、main eb4cabe/230effd、`merged_main:true`）。另修措辞：「55 个资料包（54 全文 + 2 补充 MD）」→「54 书 + 1 影印杂项行」；「其余 7 书 2–4」→「1–4」。 |
| A3 | working | 保持 working。剩余项「矩阵需在最新 main 重生成」**经本轮证实为真**，且代价已知：仅 68 行救应字段 + 2 行 unknown_when + 2 个 summary 键会变，判定性字段全不变。可把 `docs/closeout/review/art-verdict-judgment-gap-matrix-REGEN-20260913.{json,md}` 作为重生成结果先归档（我已附在 review 目录，未写入 product 工作树）。 |
| A7 | working | 保持 working。剩余项「不支持学派/能力单列清单与 30 条对齐」**属实且尚未存在**（已全量检索确认）。补登 `SMTH-E-08`。**新增正面证据**：66 条 self 改标与 `tiaohou-rescue.ts` 是 66↔66 一一对应，可写明「非无证据升级」。 |
| A8 | working | 保持 working。把「版本钉需复核」替换为可复现缺口：`bazi-anchor-rule-index.json` 183 条中 **54 条**与最新 classics main 重生成不一致；`CLASSICS_REV` = `3dc9d01`（落后 1750）；CI classics 检出同钉旧提交。**同时补正面证据**：643/643 锚点在 pin 与 HEAD 两处均未漂移；CI run 34731428150 / 34731425370 已独立核实为 success，且 product CI 在 230effd 上跑过 Playwright e2e。 |
| A6 | working | 不是本轮范围，但 remaining 第 1 条与 HEAD 实况矛盾（§5），建议立即改写并重基线 `page_consumers`。 |

**八项均不建议在本轮判 pass**；A1/A3/A7 的证据质量在复现后是可信的，A8 新增一条硬缺口，A6 的描述需要修正。

## 8. 复现清单

- 复核脚本：`docs/closeout/review/scripts-20260913/*.py`（注解计数、executable/救应计数、逐书救应、资料包集合比对、unimplemented 具名理由、666→66 实现一一对应、643 锚点两 revision 精确比对、矩阵新旧 diff、bazi/调候产物重生成 diff、过期字段扫描）。
- 重生成产物：`docs/closeout/review/art-verdict-judgment-gap-matrix-REGEN-20260913.json`（md5 `c5fe97cf394a8ebbe7177f5d0d571fb2`）与同名 `.md`；`bazi-anchor-rule-index-REGEN-20260913.json`；`tiaohou-profiles-REGEN-20260913.json`。
- 未写入：`/Users/yuhanglin/fateradar-goal-20260912/{classics,product}` 的任何**已存在**文件；未 commit / push / merge；未触碰 `/Users/sync/code/*`。
