# P1 八字六主题规则/事实交接（2026-09-21）

状态：完成本轮审计，六个主题均有可消费的本命结构证据或明确阻塞；另新增 1 条可消费的流年结构证据。旧目标“消化 440 条 `unmapped`”保持暂停；本交接不以 unmapped 数量下降作为算法正确性的证据。

机器清单见 [`P1_BAZI_TOPIC_MANIFEST_20260921.json`](./P1_BAZI_TOPIC_MANIFEST_20260921.json)。它从当前 `rules.yaml` 读取 `statement`、`quote`、`anchor` 和 `applicable_to`，再附加主题、Fact scope、三态样盘和导出版本，产品可以用它把 `Fact → RuleEvaluation → TopicEvaluation` 串起来。

## 基线和边界

- 工作区：`/Users/sync/code/fateradar-classics`，`main`，规则提交 `6321186f6aeebd0737537c45286153eedf49adb4`。
- 产品规则版本：`CLASSICS_REV = 6321186f6aeebd0737537c45286153eedf49adb4`（产品仓 `src/lib/rules/source-link.ts`）。该 revision 包含本轮新增的 `YUANHAIZIPIN-YR-03` 流年结构规则。
- 规则合同：`fateradar-rules-v2`；复合谓词使用 `fateradar-rules-v3` 语言。导出仍由 [`tools/export-rules.py`](../../tools/export-rules.py) 负责。
- 请求中的 `/Users/sync/code/fateradar-classics/docs/ALGORITHM_CLASSICS_HANDOFF.md` 在仓库中不存在；读取了产品仓对应的 `/Users/sync/code/cosmic-fortune-lab/docs/ALGORITHM_CLASSICS_HANDOFF.md`，并以当前古籍仓交接单和产品地基文档为准。
- 古籍仓只交付出处、条件、事实需求、样盘和版本；不改产品页面、叙事、通知、权限或用户输入流程。

## 暂停现场审计

接手时没有 reset、clean、stash 或覆盖工作区。Round 50 原始改动已保存到 `.local/workspace-archive/20260921/p1-bazi-round50-original/`，包含接手时文件清单、SHA-256 和相对基线的 `worktree.patch`，可逐文件恢复。

| 文件 | 结论 | 依据 |
|---|---|---|
| `references/books/bazi/sanming-tonghui/rules.yaml` | Round 50 三条神煞映射退回；当前五条草稿不进入规则数据 | 日柱/月柱 `shensha` scope 虽存在，但固定出处不能证明专禄、阳刃、建禄陈述；神煞代理不等价于格局事实 |
| `references/books/bazi/yuanhai-ziping/rules.yaml` | `YUANHAIZIPIN-014` 映射退回 | 锚点 L2736 是“杂气财官，刑冲则发”，与建禄/阳刃陈述不相干 |
| `references/books/luming-nayin/wuxing-jingji/rules.yaml` | `WX-05-02` 映射退回 | 只允许同柱禄神+驿马保守子集；原锚点 L102 只有卷名，跨柱同支没有事实合同 |
| `references/books/ziwei/taiwei-fu/rules.yaml` | 删除草稿中的 `palace: 伪宫名`；保留原有无 scope 的旧条件，不纳入 P1 八字 | `validate-rules.py` 的 V15 失败日志保留在 `tools/reports/p1-bazi-20260921/round50-schema-before.json` |
| `tools/reports/shensha-position-map.json` | 保留为未采纳草稿/证据，不作为导出输入 | 生成器和样盘证明柱位字段存在，但没有证明神煞与专禄/建禄/阳刃格局等价 |
| `tools/reports/fne-residue-inventory.json` | 保留 t219 生成快照，不把 160 条残余当作 P1 规则 | 其中关系、岁运、计数、历法和格局事实仍是阻塞清单 |
| `tools/reports/facts-sample.json` | 按生成器重建并保留 | 与产品仓 fixture 字节一致；来源、命令和 SHA-256 见下文 |
| `tools/reports/predicate-decisions/bazi-core.json`、`bazi-luming.json` | 修正中止的账本更新 | 五条误写 `mapped` 的条目恢复为 `unmapped`，补 `reason_class` 和审计说明 |

账本核对后，跟踪口径为 464 条未映射；每一条都有理由类别，且没有“账本说 mapped、YAML 却为空”的脱节。这是撤回五条草稿后的事实，不是恢复旧的 440 条目标。

`fne-residue-inventory.json` 另行核对为 160 条、160 个唯一 `rule_id`，全部仍在当前 YAML；它是 t219 的事实缺口快照，不替代 predicate decision ledger。

## P0 输入合同

产品读取每条导出规则的 `ruleId`、`art`、`statement`、`quote`、`source/anchor`、`applicableTo`、`caveats` 和 `verification`，再用 manifest 的 `primaryTopic`、`requiredFacts`、时间层和冲突说明组织主题。规则输入不在浏览器重新解释 YAML。

三态必须保持：

- `satisfied`／`满足`：完整条件命中，`matchedFacts` 是见证集。
- `not_satisfied`／`不满足`：所需 FactKey 已存在，但条件没有命中；它只表示这条传统条件在当前盘面不成立，不表示现实事件不会发生。
- `unknown`／`信息不足`：FactKey 缺失、时间层未实现、性别/计数/关系合同缺失，或未在 manifest 允许的 scope 内。不得把它降级成 `not_satisfied`。

本批 7 条规则只适用 `本命`；新增 `YUANHAIZIPIN-YR-03` 仅适用选定 `scope.layer=流年`，必须先按 `scope.year` 过滤。`大运`、`流月` 和 `流日` 没有被复制成同义规则。所有交付规则 `verified: false`，因为固定样盘只能验证求值和输入覆盖，不能证明现实预测准确率。

## P1 六主题交接

下表是产品入口；每个 ruleId 的完整 `statement / quote / anchor / applicableTo / requiredFacts / 三态语义 / caveats / fixture result / export / CLASSICS_REV` 在 JSON manifest 的 `rules` 数组中。

| 主题 | 当前状态 | 可直接消费的本命结构证据 | 产品仍需保留的阻塞 |
|---|---|---|---|
| `overview` 命格总览 | `partial` | `DITIANSUICHA-003`, `DITIANSUICHA-DR-03`, `DITIANSUICHA-DR-06`, `SANMINGTONGH-015`, `DITIANSUICHA-032`, `SANMINGTONGH-097` | 格局成败、用神细节和岁运触发不是这些谓词的充分条件 |
| `personality` 性格 | `partial` | `DITIANSUICHA-003`, `DITIANSUICHA-004`, `DITIANSUICHA-DR-03`, `SANMINGTONGH-097` | 只写稳定倾向和现实核对问题，不写绝对人格标签 |
| `career` 事业 | `partial` | `DITIANSUICHA-DR-06`, `SANMINGTONGH-015` | 职位/行业、完整格局成败、取用和时间窗口尚未形成合同 |
| `wealth` 财运 | `partial` | `DITIANSUICHA-DR-06`（极弱/从格入口，辅助证据） | 财星位置、身财两停、比劫夺财和岁运触发缺失；不输出金额或事件 |
| `relationship` 感情 | `partial` | `SANMINGTONGH-015`, `DITIANSUICHA-032`（三合/子午结构证据） | 性别、配偶星、夫宫、关系反馈缺少完整 Fact 合同；冲合不等于婚姻事件 |
| `health` 健康 | `partial` | `DITIANSUICHA-003`, `DITIANSUICHA-DR-03`（中和/偏枯的传统关注点） | 没有医疗、症状、作息事实；只作养生关注点，不作诊断 |

产品当前已有的八字事实键可支撑这批规则：`rizhu`、`yueling`、`gan`、`zhi`、`rizhu_strength`、`geju`、`yongshen`、`shishen`、`canggan`，以及带柱位的 `shensha`。当前固定样盘共 289 条 `shensha` fact，全部带 `scope.layer=本命` 与四柱 `scope.pillar`；逐条证明保存在 `tools/reports/p1-bazi-20260921/shensha-scope-proof.json`。岁运并临和大运—流年结构关系现在已有带年份的事实及“是/否/信息不足”样盘，但刃杀财官印绶、救应和主题作用语义仍缺；关系主题还需要产品决定是否建立性别/配偶星/夫宫的明确合同。相关古籍规则继续 `unknown`，不以相邻字段近似。

## 采纳、阻塞、退回

### 采纳为 provisional evidence（8 条）

`DITIANSUICHA-003`, `DITIANSUICHA-004`, `DITIANSUICHA-DR-03`, `DITIANSUICHA-DR-06`, `SANMINGTONGH-015`, `DITIANSUICHA-032`, `SANMINGTONGH-097`。

它们均有稳定 `ruleId`、可读的原文锚点、现有 FactKey 条件和固定样盘的正例/反例/缺键边界例；这只批准进入产品证据层，不批准现实预测或 `verified: true`。

### 阻塞，暂不进入六主题规则池（8 条）

- `DITIANSUICHA-DR-02`：V14 低对应度；固定锚点只有“合有宜不宜”，不能追溯到三合/方局的具体谓词。
- `DITIANSUICHA-012`：谓词只列十神/格局，未表达声明中的月令、透干、司令和破格；当前样盘 24/24 满足，不能作为区分性规则。
- `SANMINGTONGH-102`：声明有年柱、时柱、日坐、身强和比劫冲夺，谓词只有无柱位 `shishen` OR；当前样盘 24/24 满足。
- `YUANHAIZIPIN-023`：正财谓词缺柱位和身能任财条件，古代妻财语义不能直接转成现代伴侣/收入结论。
- `YUANHAIZIPIN-024`、`SANMINGTONGH-069`：女命、夫宫和子星条件缺少产品合同，保持 `unknown`。
- `DITIANSUICHA-031`：当前固定样盘没有卯酉同现的正例，不能声称通过正反例回归。
- `SANMINGTONGH-R-02`、`YUANHAIZIPIN-008`：月令藏干/透干谓词的锚点没有支持完整陈述，等待正确出处。

### Round 50 退回（5 条）及紫微无效 scope（1 条）

- 退回：`SANMINGTONGH-051`, `SANMINGTONGH-065`, `SANMINGTONGH-066`, `YUANHAIZIPIN-014`, `WX-05-02`。`shensha-position-map.json` 仍保留发现，但不进入 YAML 导出。
- 退回：`TAIWEIFU-004` 的 `palace: 伪宫名`。V15 失败日志保留；本 P1 只消费八字，紫微规则不以“修到能过”冒充完成。

## 生成和验证

事实样盘重建命令：

```bash
cd /Users/sync/code/cosmic-fortune-lab
bun scripts/dump-facts.ts /Users/sync/code/fateradar-classics
```

结果：八字 26 个固定 case；产品仓 `tests/fixtures/facts-sample.json` 与古籍仓 `tools/reports/facts-sample.json` `cmp` 相同，SHA-256 为 `d53d3a8a64ca11826950276791ef2e84abaa7f01d914fdfb1e38f51dc200b47c`。生成输入为产品仓 HEAD `93c7245db2dbfa82e3a8ce69cc74ab318391b988` 的未提交工作树，`scripts/dump-facts.ts` SHA-256 为 `d21e8f48638653199e56363d844ab7ad4b9c461c1beba2fea6edabeb7d6105f2`；因此这是当前工作树生成证据，不是新的产品提交版本。相对古籍仓旧快照为 `11584 insertions / 1559 deletions`，原因是重建本命/大运/流年时间层、`suiyun_binglin`、`dayun_liunian_relation`、逐柱 `gan/zhi/canggan/shensha scope` 和覆盖样盘。

规则导出和 manifest 命令：

```bash
cd /Users/sync/code/fateradar-classics
python3 tools/export-rules.py \
  --out-rules .local/staging/p1-bazi-20260921/rules \
  --out-procedures .local/staging/p1-bazi-20260921/procedures
python3 tools/generate-p1-bazi-manifest.py \
  --output docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json \
  --export-file .local/staging/p1-bazi-20260921/rules/bazi.json
```

结果：导出共 846 条（八字 doctrine 446、procedure 3）；八字导出 SHA-256 为 `95d884c10cd01864d1d252f52ea3b51483acffb87c45a4d75b4945d8729e3625`。manifest 生成 8 条采纳规则；每条都验证 `满足 / 不满足 / 信息不足` 三态，全部 `verified=false`。

当前 manifest SHA-256：`8b54f89fe7c63b85cbbcdd7efbd8b55d111baa46e5e16886e864d06ee7f76993`。

版本锁复核：8 条采纳 ruleId 均存在于 `CLASSICS_REV=6321186f6aeebd0737537c45286153eedf49adb4` 指向的提交，且 `applicable_to` 与当前源文件一致；本轮因实际新增流年规则而更新版本锁。

已运行的闸门：

```bash
python3 tools/validate-rules.py --book bazi/ditiansui-chanwei --json
python3 tools/validate-rules.py --book bazi/sanming-tonghui --json
python3 tools/validate-rules.py --book bazi/yuanhai-ziping --json
python3 tools/validate-rules.py --book luming-nayin/wuxing-jingji --json
python3 tools/validate-rules.py --book ziwei/taiwei-fu --json
python3 tools/validate-executable.py --json
python3 tools/predicate-report.py --json --check-open-values --check-art-keys
python3 tools/test-ledger-consistency.py
python3 tools/verification-depth-report.py --json
python3 tools/audit-contract.py --base 6321186 --json
git diff --check
```

结果：五个受影响 YAML `ok=true`（清除伪宫名后紫微也通过）；`validate-executable` 为 `ok=true, files=15, rules=258, source_spans=579, named_gaps=42`；开放值和 art key 检查通过；账本为 `ALL LEDGER-CONSISTENCY OK`，463 条未映射全部有理由；当前验证深度为 379 条口径内映射、378 条有满足样本，唯一未示范项为已知紫微 `TAIWEIFU-010` 的 structurally-unsatisfiable，不属于本 P1 八字采纳集；`git diff --check` 通过。规则校验保留已有 V11/V14 警告，低对应度的 `DITIANSUICHA-DR-02` 已列为阻塞，不伪装成采纳。

`audit-contract.py --base 6321186 --json` 通过：`protected_violations=[]`、`untraced_changes=[]`、`ledger_mismatches=[]`、`verified_true_lines=0`。以旧基线 `cd41f5b` 运行时会明确报告本轮 `YUANHAIZIPIN-YR-03` 的受保护字段变化和新增谓词；该失败证据对应实际规则数据变更，不被隐藏。

复合谓词和三态求值回归也通过：`python3 tools/test-predicate-lang.py`、`python3 tools/test-eval-predicates.py`、`python3 tools/test-verification-depth.py` 均为 `ALL ... OK`；其中缺键明确得到 `信息不足`，不会被当作 `不满足`。

`predicate-report.py` 当前八字为 449 条 anchored、224 条带谓词、49.89%（覆盖率是规则表达统计，不是预测准确率）；紫微为 93/58/62.37%。这两个数字不作为本 Goal 的成功标准。

## 给产品仓的下一步

1. 产品算法负责人：锁定 manifest 的 `classicsRev` 和事实样盘 hash，在服务端把 `applicableTo` 评价结果映射成 `satisfied / not_satisfied / unknown`，再按 `topics.*.ruleIds` 生成 `RuleEvaluation` 和 `TopicEvaluation`。
2. 产品事实层负责人：确认本命/流年/流月过滤，以及是否建立性别、配偶星、夫宫、计数和跨柱关系合同；没有合同的规则保持 `unknown`。
3. 古籍维护者：若要恢复 Round 50，先补正确原文锚点、神煞代理等价性说明和独立边界样盘；另开授权批次，重新验证后才考虑更新 `CLASSICS_REV`。
4. 人工流派评审：裁决三合/冲、从格、财星和健康传统语义的适用边界。映射条数增加不能替代这一步。

本轮停止扩展古籍覆盖面，不恢复 440 条 `unmapped` 旧目标。

## 2026-09-22 求值边界纠正

首次运行 `python3 tools/audit-flow-year-unknown.py` 曾失败（exit 1），失败证据保留在 `tools/reports/p1-bazi-20260922/flow-year-unknown-before.json`；当时 2100 的 Fact 值“信息不足”被参考求值器降成“不满足”。classics 已修正两个已登记流年 FactKey 的显式未知传递，并以固定三态诊断复跑通过；当前报告为 `tools/reports/p1-bazi-20260922/flow-year-unknown.json`。新增 `tools/audit-flow-year-yr03.py` 对 `YUANHAIZIPIN-YR-03` 按 `scope.year` 过滤后也通过满足/不满足/信息不足三态。该规则只交付结构性“忌象候选”，不表达制化、喜忌或现实事件。

## 产品只读验收记录（2026-09-22）

古籍仓只读运行 cosmic 的八字垂直测试，命令与失败输出见 `tools/reports/p1-bazi-20260922/cosmic-integration-before.log`；结果 `22/24`，exit 1。失败均属于产品测试与当前已锁定事实合同的对齐问题：

1. 流年关系测试把 2027 期望写成 `相克`，而共享 facts fixture（SHA `d53d3a8a64ca11826950276791ef2e84abaa7f01d914fdfb1e38f51dc200b47c`）明确为 `其他`。
2. 交接规则通用 harness 未按 manifest 的 `scope.year` 选择器过滤多年份事实，导致 `YUANHAIZIPIN-YR-03` 反例误命中。

产品需修正测试 fixture 期望及年份过滤后重跑；古籍仓不修改规则语义，也不把跨年份混合求值当成通过。
