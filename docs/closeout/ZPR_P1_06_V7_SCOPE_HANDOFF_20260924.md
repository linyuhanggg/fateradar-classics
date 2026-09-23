# ZPR-P1-06 适用域修正候选：V7（2026-09-24）

**结论**：V7 是待 Product 单独审核的 Classic 侧候选 handoff，直接在 [V6 manifest](./P1_BAZI_TOPIC_MANIFEST_20260923_V6.json) 之后增加本命月支与月令为寅的显式谓词。V6 原文件保持不变。此修正只让原文“辛生寅月”的局部例型不再把已知丑月、辰月盘误留为未知；不升级 `ZPR-E-02` 的完整算法、`rescue`、`verified`、整体成败或任何作用结论。

## Predicate 与来源范围

《子平真诠》L435 写“如辛生寅月，透丙化官，而又透甲，格成正財，正官乃其兼格也”。依正式 [谓词语言 V3](../PREDICATE-LANGUAGE-V3.md)，V7 的 `applicableTo` 是一个 `all_of`，读取四条精确作用域事实：

```json
{
  "all_of": [
    {"key": "gan", "value": "辛", "scope": {"layer": "本命", "pillar": "day"}},
    {"key": "zhi", "value": "寅", "scope": {"layer": "本命", "pillar": "month"}},
    {"key": "yueling", "value": "寅", "scope": {"layer": "本命", "pillar": "month"}},
    {"key": "natal_yin_simple_hidden_exposure_pattern", "value": "甲丙", "scope": {"layer": "本命", "pillar": "month"}}
  ]
}
```

月支 `zhi` 与月令 `yueling` 都来自共享 fixture 已有的逐柱事实；没有新加 FactKey、样盘或规则效果推论。V7 仅在四条都满足时输出 V6 已有的甲正财主、丙正官兼两个来源入口。结构事实缺失／同 scope 冲突仍为信息不足；戊也透与寅午戌全会的两盘继续未知。月支、月令若已知为非寅，则只否定这个辛日寅月例型，不否定其它月令入口。

## 固定样盘重算

共享 50 盘 fixture SHA-256 为 `206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8`。V6 谓词结果是满足 2、不满足 44、信息不足 4；V7 用相同 fixture 的现有事实重算为满足 2、不满足 46、信息不足 2。

| 输入 | V7 结果 | 解释 |
| --- | --- | --- |
| `caseP1_ZPR_month_xin_jia_bing_1954`，辛日、寅月、甲丙清楚结构 | 满足 | 保留两枚来源入口 |
| `cov1_bazi_4`，辛日、月支与月令均为丑 | 不满足 | 已知不属“辛生寅月”例型；甲丙结构键未发不再导致未知 |
| `cov3_bazi_6`，辛日、月支与月令均为辰 | 不满足 | 已知不属“辛生寅月”例型；甲丙结构键未发不再导致未知 |
| `caseP1_ZPR_month_xin_jia_bing_wu_1984`，甲丙戊三透 | 信息不足 | 仍无三透时的原文主兼裁法 |
| `caseP1_ZPR_month_xin_jia_bing_meeting_1994`，寅午戌全会 | 信息不足 | L548 的“透而又会，并用”未与本例型合并裁决 |

另外移除月支、移除月令、移除结构键，或制造单键同 scope 冲突／异层污染，校验器都要求返回信息不足。两张新不满足盘的月支和月令均明确且相互一致。

## 版本锁与状态

- [V6 SHA-256](./P1_BAZI_TOPIC_MANIFEST_20260923_V6.json)：`39e53a6c5c3693334209d80eb2f9e9002339fff2117b64f1988d6f2a02f344a6`。V7 `previousHandoff` 精确锁定此文件。
- [V7 manifest](./P1_BAZI_TOPIC_MANIFEST_20260924_V7.json) 整文件 SHA-256 为 `f3d689cf0c24ca61685548ee4246461701bf1436191d3580c461a3c6e068f306`，由 `tools/generate-p1-bazi-v7-manifest.py` 生成；独立门禁为 `python3 tools/verify-p1-bazi-v7-handoff.py`。
- `semanticContractStatus` 仍是 `pending`，全部规则 `verified=false`。V7 是候选谓词，不写回 Classic `rules.yaml` 或 `dist/rules/bazi.json`；manifest 内原有 export hash 继续表示 V6 基线，不表示 V7 已导出。
- 不新增或推断整盘成格、纯杂、喜忌、财官实际相生、救应、成败、吉凶或流年效果。P1-06 与整个 ZPR-E-02 的适用范围仍局部且未完备。

复验命令：

```sh
python3 tools/generate-p1-bazi-v7-manifest.py
python3 tools/verify-p1-bazi-v7-handoff.py
python3 tools/verify-p1-bazi-v6-handoff.py
```
