# P1 classics release candidate 清单（2026-09-22）

本清单只描述发布前的可复核边界，不代表已经提交或推送。当前产品锁定的规则版本是 `CLASSICS_REV=6321186f6aeebd0737537c45286153eedf49adb4`；该对象目前只存在于本地 classics 历史，远端 `origin` 尚无同名 ref。

## 发布内容

发布 candidate 必须保留 `6321186f` 的完整源树和规则历史，不能只发布 P1 文档或单个流年规则文件。可选两种方式：

1. 将现有 `main` 从 `cd41f5b5` 快进发布到包含 `6321186f` 的完整提交链；或
2. 从远端 `main` 构造一个完整树快照的 squash candidate，再由维护者审核后发布。

无论采用哪种方式，P1 handoff 引用的以下四个证据文件都必须进入 candidate，否则远端文档无法独立复核：

- `tools/reports/fne-residue-inventory.json`
- `tools/reports/shensha-position-map.json`
- `tools/reports/p1-bazi-20260921/round50-schema-before.json`
- `tools/reports/p1-bazi-20260921/shensha-scope-proof.json`

同时纳入本轮已审核的 manifest、响应、生成器和 fixture 更新：
`docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json`、
`docs/closeout/CLASSICS_TO_COSMIC_P1_RESPONSE_20260922.{json,md}`、
`docs/closeout/COSMIC_P1_REQUEST_POINTER_20260922.md`、
`tools/generate-p1-bazi-manifest.py`、
`tools/reports/facts-sample.json` 及对应 P1 审计报告。

`pelican-bike.html` 与本清单无关，不得纳入 candidate。`docs/closeout/DSH_HANDOFF_20260921.md` 和 `docs/goals/CLASSICS_GOAL_PROMPT_20260921.md` 是历史/过程材料，除非另有审核决定，也不作为 P1 发布依赖。

## 发布后验收

远端发布后，先确认对象可获取，再在 cosmic 的干净 runner 验证：

```bash
git ls-remote origin 6321186f6aeebd0737537c45286153eedf49adb4
git -C /path/to/cosmic-fortune-lab ls-remote origin 6321186f6aeebd0737537c45286153eedf49adb4
```

随后重跑 source-link 测试，并核对 manifest 与 fixture：

```bash
cd /Users/sync/code/cosmic-fortune-lab
FATERADAR_CLASSICS_ROOT=/path/to/fateradar-classics \
  bunx vitest run \
  tests/engine/bazi-reading-source-link.test.ts \
  tests/engine/shensha-source-link.test.ts \
  tests/engine/tiaohou-source-link.test.ts

cd /path/to/fateradar-classics
python3 tools/audit-flow-year-unknown.py
python3 tools/test-expressible-residue.py
python3 tools/test-ledger-consistency.py
python3 tools/validate-executable.py --json
sha256sum tools/reports/facts-sample.json docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json
sha256sum tools/reports/facts-sample.json \
  /Users/sync/code/cosmic-fortune-lab/tests/fixtures/facts-sample.json
```

cosmic 侧还需确认 `CLASSICS_REV` 指向可获取的提交、source-link 全文行号测试通过，且产品 fixture SHA 与 handoff/manifest 中记录的 SHA 一致。发布前不得把本地工作区状态、未推送 SHA 或 `pelican-bike.html` 当作远端验收证据。
