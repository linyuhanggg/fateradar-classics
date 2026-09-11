# MING-477 古籍集成账本（叠已验收 464 tip，合入本轮已审审查稿）

机器可读权威：`docs/integration/ming-477-integration-ledger.json`。

## 基线与叠层
- 已审 tip：`origin/codex/multica-ming-464` @ `538fd1422053e449c9543b33c6a7c7ce5cbc0108`（独立验收 MING-469 `91b1264ccd551b32c711391f665472c21a11c6ed` 通过）
- 独占：`fateradar-multica-ming-477` / `codex/multica-ming-477`
- 合入方式：最小路径 `cherry-pick -x`；禁止整树覆盖；`verified` 保持 false
- **未升** 产品唯一线 `6c1dfa3b` / main / 部署
- **未合入** 452/468 产品定义 ID；未合入尚未独立审查的新书

## 本批已合入（待独立验收）
| Pack | Source tip | 文件 | 合入方式 | 本地 commit | 状态 |
|---|---|---|---|---|---|
| 464 验收稿 | MING-469 `91b1264c` | `ming-464-acceptance-review.md` | `cherry-pick -x` | `9eaa90e` | integrated_pending_acceptance |
| 奇门 NLC remaining 2100–2470 | MING-461 `402393af` | `qimen-dunjia-tongzhi-nlc-layouts-remaining-2100-2470-review.md` | `cherry-pick -x` | `e9466b9` | integrated_pending_acceptance |
| 奇门演義 vol4–9 | MING-462 `e92efab9` | `qimen-dunjia-tongzhi-yanyi-vol4-9-independent-review.md` | `cherry-pick -x` | `0194126` | integrated_pending_acceptance |
| 神峰通考 | MING-463 `80a1734b` | `shenfeng-tongkao-independent-review.md` | `cherry-pick -x` | `4def1e9` | integrated_pending_acceptance |
| 阳宅十书 | MING-465 `c2cf06a7` | `yangzhai-shishu-independent-review.md` | `cherry-pick -x` | `c3ac2fd` | integrated_pending_acceptance |
| 青囊序 | MING-466 `54c7d0a5` | `qingnang-xu-independent-review.md` | `cherry-pick -x` | `cfb4d65` | integrated_pending_acceptance |
| 卜筮正宗 | MING-467 `bfeb02df` | `bushi-zhengzong-independent-review.md` | `cherry-pick -x` | `1d7e60c` | integrated_pending_acceptance |
| 兰台妙选 | MING-472 `2d608eba` | `lantai-miaoxuan-independent-review.md` | `cherry-pick -x` | `c868160` | integrated_pending_acceptance |
| 李虚中命书 | MING-473 `5a8c5daf` | `li-xuzhong-mingshu-independent-review.md` | `cherry-pick -x` | `fce2158` | integrated_pending_acceptance |
| 太微赋 | MING-474 `98b4573e` | `taiwei-fu-independent-review.md` | `cherry-pick -x` | `2314c3b` | integrated_pending_acceptance |

## 验证
- `git diff 538fd142..contentImportTip`：仅 10 个审查/验收 md（账本另计）；`references/annotations/**` **无** diff
- 各合入路径 blob 与源 tip **全等**
- 命理约言 NLC / 奇门 NLC layouts / 秘本等注解 blob 与 464 tip **全等**
- `validate-annotations.py --json`：`ok=true` books=48 files=58 entries=42834 source_reviewed=40410 errors=[]
- 本批触及注解 `verified=true`：**0**；全库 `verified=true`：**0**

## 非宣称
- 不是古籍全书完成；不是本批任一术数全书人工 verified。
- source-reviewed ≠ 人工 verified。
- 不含 452/468 产品定义 ID；未改 chart.* / 账号 / 支付 / 后端 / 产品唯一线。

## 交付 tip
- 内容合入 tip（10 审查/验收路径）：`2314c3b4672849d57ee4d1031f0ef20334cd8401`
- 账本核对 tip：交包后以 `git ls-remote origin refs/heads/codex/multica-ming-477` 为准（施工分支，非 main）
