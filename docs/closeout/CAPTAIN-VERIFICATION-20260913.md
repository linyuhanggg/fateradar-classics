# Captain 独立核查记录（2026-09-13，goal round 2）

> 本文件由 captain 直接执行命令得出，不转抄任何成员或旧检查点数字。
> 用途：为 `docs/closeout/DELIVERY_ACCEPTANCE.json` 的 A8（版本对应）与 Goal 状态提供可复现证据。
> 合并方式：账本由 captain 单写者统一折入，避免与成员并发改同一 JSON。

## 1. A8：内容导出与代码版本可对应（实测）

方法：读出 product 仓生成物里的版本钉，逐个在 classics 仓验证「是否真实存在」且「是否为当前 main 的祖先」。

命令（product 侧取值，classics 侧验证）：

```bash
git -C <classics> cat-file -t <sha>
git -C <classics> merge-base --is-ancestor <sha> HEAD   # HEAD=eb4cabe=origin/main
```

结果：**10/10 全部为真实 commit，且全部是当前 main 的祖先**（无一悬空、无一来自未集成分支）。

| 内容钉（product 内位置） | revision | classics 存在 | 是 main 祖先 |
|---|---|---|---|
| `src/lib/rules/source-link.ts` `CLASSICS_REV` | `3dc9d01b69bbefdd85e3fefb548d4d0831d36626` | 是 | 是 |
| `src/lib/engine/generated/tiaohou-profiles.json` | `83c654b9638d9b75f8c26cbb9ea5f3825b077d15` | 是 | 是 |
| `src/lib/knowledge/generated/knowledge-index.json` | `37bbde0ab2f43ba1f6fd22ec90b70c18a08cce3a` | 是 | 是 |
| `src/lib/engine/generated/bazi-anchor-rule-index.json` | `df73f2324c899b2f316d136de06be560c0ce4054` | 是 | 是 |
| `src/lib/engine/generated/liuren-source-rules.json` | `a6c018208778ef89f44876449cbd5f19bf81e122` | 是 | 是 |
| `src/lib/engine/generated/liuyao-source-rules.json` | `b8150a7231cbe18a0e5b656f8386b8512b6848dc` | 是 | 是 |
| `src/lib/engine/generated/qimen-source-rules.json` | `5379881dbbc2af1af7419070ef6f9a8276088a88` | 是 | 是 |
| `src/lib/engine/generated/qizheng-source-rules.json` | `3fbef8c50c859074a2139ecbb38e2d297fe0ba35` | 是 | 是 |
| `src/lib/engine/generated/reading-notes.json` | `a8edc922aefac20ca0fe87f1ca48f0e28d5249f3` | 是 | 是 |
| `src/lib/engine/generated/ziwei-source-rules.json` | `3ca4a47d7ff2716a627a0c48a346f1a316e7d70c` | 是 | 是 |

口径说明（摘自 product `src/lib/reading-input-export.ts` 的 pins 块）：这些是 **generated-file pins，不是 live origin/main HEAD**——即内容快照按设计可落后于 main HEAD，但必须能解析到真实提交。本次核查确认它满足该要求。

**A8 该子项的结论**：版本对应关系**可验证且一致**；但 A8 仍需（a）页面/导出在最新 main 上重跑（page-acceptance t4）、（b）最终集成时的全量必要检查。

## 2. 两仓 main 与 CI（实测）

| 仓 | 工作树 HEAD | origin/main | CI（main HEAD） |
|---|---|---|---|
| classics | `eb4cabe` + 1（账本 `01bccafe`，在分支未合 main） | `eb4cabe49506b0574de1cd1626f07d6c18153ae9` | success（gh run `34731428150`） |
| product | `230effd` | `230effd2f5a3e8fee9426ce0659d3ddf9853c485` | success（gh run `34731425370`） |

两分支 HEAD 均为各自 origin/main 的祖先（成果已集成），main 领先于分支（classics 22、product 16）。

## 3. Goal 状态复核（本轮再次实测，未变化）

- 会话 `session-34e9b471-…` 的 Goal：`goal-06dc2771-4b72-46fb-84e9-b8ffb3930327`，`phase=active`，`revision=1`。
- 自动续行：**已启用**——本轮 `<goal_round>` 即 goal-round-driver 准入的 Round 2/256。
- 模型面 goal 工具：**仍不可见**。实测方法：

```bash
zstd -dc <session.jsonl.zstd> > /tmp/mysess2.jsonl
grep -c '"name": "get_goal"' /tmp/mysess2.jsonl     # -> 0
# 解析最后一个 request/header：tools 40 项，无任何 goal 工具；
# system == 'You are a helpful software engineer assistant.'（minimal preset 的 complete persona）
```

- 根因未变：会话 agent preset = `minimal`；`dsh-web-app` 有意 `disabled` 了 host-plane 的 `tool-goal` 行，改由 per-session preset 提供；`minimal` 只挂 persona(complete)+persistent bash+str_replace_editor。
- 因此 `maxGoalRounds` 仍是部署默认 **256**；提高到 1024 只能在 preset 切换后由 `update_goal(action=edit, max_goal_rounds=1024)` 完成。
- **未做**：未注入 host-plane 的 `@deepseek-ai/dsh-tool-goal` 副本（会与 standard-preset 会话内的同名注册形成竞争），未重启任何调度器，未创建第二个 Goal，未标记任何旧 Goal 完成。

## 4. 已知过期来源登记（引用时不得直接采信）

| 来源 | 过期点 | 实测取而代之的值 |
|---|---|---|
| `docs/closeout/GAP_LEDGER.json` | `counts.draft=2905`、`source_reviewed=59934`、`rules[].level`（level1=164/level2=88） | 实测 draft **2835**、source-reviewed **60004**；规则级状态以 product 缺口矩阵为准 |
| `docs/closeout/GAP_LEDGER.json` | `page_consumers.other_arts` = "dedicated free-reading builders missing except bazi" **不成立** | 实测八术均有 dedicated 模块：`src/lib/engine/{liuren,liuyao,meihua,qimen,qizheng,xiaoliuren,ziwei}-free-reading.ts` + `bazi/free-reading.ts`。该字段为旧快照，已由 algo-impl 在 A6 纠正，captain 独立复核确认 |
| `product/docs/implementation/art-verdict-judgment-gap-matrix.json` | `product_head=cdb5f9c` / `classics_head=74edada` 已不是当前 main（230effd / eb4cabe） | 需在最新 HEAD 重生成后方可作为 A3 证据（登记为 A3 执行项） |
| `product/docs/implementation/E-PAGE-ACCEPTANCE-VERIFICATION.md`、`C3-EIGHT-ARTS-EXPORT-ACCEPTANCE.md`、`C-EXPORT-READBACK-VERIFICATION.md` | 均为 2026-09-12 14:08–19:24 产出，早于第 43/44 轮 main 合入 | A6/A8 必须在新 main 重跑（page-acceptance t4） |

> 纪律：这些来源仍可用于**定位**，但不得用于**判 pass**。账本的 `measured_baseline` 与 criterion 结论只认实测值。

## 5. 团队状态目录位置（如实记录）

AgentTeams 平台把团队状态目录建在 **`/Users/sync/code/fateradar-classics/.agent-teams/fateradar-closeout/`**（由会话 cwd 决定）。该路径属于本任务明令禁止覆盖的其他任务现场。

处理：captain **不提交、不推送、不写入**该仓的任何内容；团队状态仅作平台元数据。所有实际代码/数据改动只落在 `/Users/yuhanglin/fateradar-goal-20260912/{classics,product}`。
