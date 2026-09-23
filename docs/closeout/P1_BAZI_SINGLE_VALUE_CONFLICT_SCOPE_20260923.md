# P1 八字单值事实冲突的三态求值边界

这是谓词求值器的输入一致性门禁，不新增古籍规则、作用 FactKey、吉凶解释或 `verified=true`。相同 `key` 与完全相同的 `scope` 若本应只有一个值，却同时收到两个不同值，任一值都不能作规则的满足见证；该子句为 `信息不足`，并在 `missing_fact_keys` 中标出此键。相同值的重复记录不冲突，另一年份或另一柱位的值也不冲突。

当前按单值处理的八字键为：`rizhu`、`natal_day_gan`、`yueling`、`gender`、`spouse_palace_zhi`、逐柱 `gan/zhi/gan_element/nayin`、`rizhu_strength`、`geju`、`tiaohou_profile_status`、`dayun_direction`、按有效年取值的 `dayun_gan_zhi`、`liunian_gan/zhi/gan_zhi`、`dayun_liunian_relation_class`、`suiyun_binglin`、`suiyun_same_zhi`，以及未来语义合同预留的 `rescue_condition`、`liunian_activation`、`yongshen_effective`、`jishen_empowered`。`shishen`、`canggan`、`natal_relation` 等同一作用域可有多值，不适用此门禁。冲突只令依赖它的子句未知；复合条件仍按原有三态逻辑合成，例如独立的已知反例仍可令 `all_of` 不满足。

真实交接规则的边界是：010A 的本命甲日与所选 2018 戊戌年本来满足入口，若同一流年 scope 另有丁酉，则不能选戊戌作正例；011A 的所选 1984 甲子年与 `suiyun_binglin=是` 本来满足字面并临，若同 scope 又有 `信息不足`，也不能选“是”作正例。两者都应返回 `信息不足`，不据此推断原 010／011 的作用。

Classics 参考实现为 [`tools/eval-predicates.py`](../../tools/eval-predicates.py)，回归为 `python3 tools/test-eval-predicates.py`；Cosmic 消费实现为 `src/lib/engine/facts/vocab.ts`，010A／011A 真规则回归另验证服务端主题仍显示冲突未知。两侧只改变矛盾输入的求值，现有 13 条 P1 规则、源 manifest、共享真盘 fixture 与原文锚点不变。
