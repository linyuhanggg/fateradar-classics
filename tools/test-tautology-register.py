#!/usr/bin/env python3
"""恒真映射登记册的回归测试（t182 口径更正：25 → 64）。

钉住四件事：

1. **登记册与实况一致**：册子里的条数/分类必须与 `--discrimination` 现算结果相同
   （册子是快照，快照不能自己过期）。
2. **新形态确实被抓到**：`{key: ziwei_palace, value: X}` 单值子句出现在**或位**时，
   整条规则必然恒真——此前只认「通配 `*`」与「整段覆盖值域」，漏了这一类。
3. **`all_of` 里的同类子句不算**：合取位置上的恒真子句不影响结论，不得误报。
4. **样本完备但结构性未核的键不计入**（如 `bazi.shishen`）：宁可漏报也不误报。
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTER = ROOT / "tools/reports/tautological-mappings.json"

spec = importlib.util.spec_from_file_location("ev_t", ROOT / "tools/eval-predicates.py")
ev = importlib.util.module_from_spec(spec)
sys.modules["ev_t"] = ev
assert spec.loader is not None
spec.loader.exec_module(ev)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def live() -> dict:
    raw = json.loads((ROOT / "tools/reports/facts-sample.json").read_text(encoding="utf-8"))
    vocab = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
    out = {}
    for art in ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng"):
        out[art] = ev.discrimination_report(art, raw[art], vocab.get("values") or {})
    return out


def main() -> int:
    reg = json.loads(REGISTER.read_text(encoding="utf-8"))
    rep = live()

    print("1. 登记册与实况一致")
    live_hard = sorted(r["rule_id"] for rows in rep.values() for r in rows if r["hard"])
    reg_ids = sorted(e["rule_id"] for e in reg["entries"])
    check("  条数一致", len(reg_ids), len(live_hard))
    check("  rule_id 集合一致", reg_ids, live_hard)
    check("  总数 64（旧口径 25 + 新类 42 − 重叠 3）", reg["counts"]["total"], 64)

    print("2. 新形态被抓到：域完备键上的单值子句（或位）")
    dc = [
        (r["rule_id"], r["domain_complete_clause"])
        for rows in rep.values() for r in rows if r["hard"] and r["domain_complete_clause"]
    ]
    check("  该形态条数 42", len(dc), 42)
    ziwei = {r["rule_id"]: r for r in rep["ziwei"]}
    check("  FEIXINGZIWEI-008 被判 hard", ziwei["FEIXINGZIWEI-008"]["hard"], True)
    check(
        "  且给出的正是那条子句",
        ziwei["FEIXINGZIWEI-008"]["domain_complete_clause"],
        {"key": "ziwei_palace", "value": "事业"},
    )
    check("  该子句确实无 scope（有 scope 就不是恒真）", "scope" in ziwei["FEIXINGZIWEI-008"]["domain_complete_clause"], False)

    print("3. all_of 里的同类子句不得误报")
    keys = ev.DOMAIN_COMPLETE_KEYS["ziwei"]
    check(
        "  平铺列表／或位 → 命中",
        ev._or_position_taut([{"key": "ziwei_palace", "value": "命宫"}], keys),
        {"key": "ziwei_palace", "value": "命宫"},
    )
    check(
        "  all_of 内 → 不命中",
        ev._or_position_taut(
            {"all_of": [{"key": "ziwei_palace", "value": "命宫"}, {"key": "ziwei_star", "value": "紫微"}]},
            keys,
        ),
        None,
    )
    check(
        "  any_of 分支整体恒真 → 命中",
        ev._or_position_taut(
            {"any_of": [{"all_of": [{"key": "ziwei_palace", "value": "命宫"}]}, {"all_of": [{"key": "ziwei_star", "value": "紫微"}]}]},
            keys,
        ),
        [{"key": "ziwei_palace", "value": "命宫"}],
    )
    check(
        "  带 scope 的单值子句 → 不命中（不是恒真）",
        ev._or_position_taut([{"key": "sihua", "value": "化忌", "scope": {"palace": "迁移"}}], keys),
        None,
    )

    print("4. 样本完备但结构性未核的键不计入")
    # 要断言的不是「含 shishen 子句就不能 hard」——一条规则可以**另有**通配/整段覆盖而 hard。
    # 真正要钉的是：**sample_complete_clause 永不参与 hard 的判定**。
    offends = [
        (art, r["rule_id"])
        for art, rows in rep.items() for r in rows
        if r["hard"] != bool(r["wildcard"] or r["domain_covering"] or r["domain_complete_clause"])
    ]
    check("  hard 恒等于（通配 ∨ 整段覆盖 ∨ 域完备子句）——样本完备子句不参与", offends, [])
    check("  shishen 不在域完备键表里", "shishen" in ev.DOMAIN_COMPLETE_KEYS.get("bazi", set()), False)
    check("  shishen 在「样本完备」表里（备查）", "shishen" in ev.SAMPLE_COMPLETE_KEYS.get("bazi", set()), True)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL TAUTOLOGY-REGISTER OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())