#!/usr/bin/env python3
"""生成「必然恒真映射」登记册（t182 更正口径：25 → 64）。

背景：`eval-predicates.py --discrimination` 原先把「结构上恒真」只判两种形态——
含通配 `*`、或把某个封闭值域**整段覆盖**（如 10 个 rizhu 穷尽天干）。
**它漏了第三种**：在「域完备键」上只写**单个取值**。

例如 `{key: ziwei_palace, value: 事业}`：值域合法、只取一个值、看起来不像凑数，
但引擎**每盘都产出全部十二宫（加身宫）**，所以这条子句对任何盘都成立；
它若出现在**或位**（平铺列表成员，或某个 `any_of` 分支整体恒真），整条规则就恒真。

这类规则既没有筛选作用，又会把证据面板挤满 —— 与 t168 撤回 `DITIANSUICHA-DR-07`
（10 个 rizhu 穷尽值域）是**同一个后果**，只是换了写法。

本册只登记、不修改规则：清理既有恒真映射会**下调**覆盖率，属已登记的待决项
（t179 §6 需人判 ⑥），由人决定，机器不擅自改。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

spec = importlib.util.spec_from_file_location("ev_reg", ROOT / "tools/eval-predicates.py")
ev = importlib.util.module_from_spec(spec)
sys.modules["ev_reg"] = ev
assert spec.loader is not None
spec.loader.exec_module(ev)

ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")


def main() -> int:
    ap = argparse.ArgumentParser(description="恒真映射登记册")
    ap.add_argument("--out", default="tools/reports/tautological-mappings.json")
    args = ap.parse_args()

    entries = []
    for art in ARTS:
        rules = ev.load_rules(None, art)
        raw = json.loads((ROOT / "tools/reports/facts-sample.json").read_text(encoding="utf-8"))
        vocab = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
        report = ev.discrimination_report(art, raw[art], vocab.get("values") or {})
        by_id = {r["rule_id"]: r for r in rules}
        for row in report:
            if not row["hard"]:
                continue
            rule = by_id[row["rule_id"]]
            if row["domain_complete_clause"]:
                klass = "domain-complete-key-single-value"
                clause = row["domain_complete_clause"]
            elif row["wildcard"]:
                klass = "wildcard"
                clause = None
            else:
                klass = "domain-covering-enumeration"
                clause = None
            entries.append({
                "art": art,
                "book": row["book"],
                "rule_id": row["rule_id"],
                "class": klass,
                "clause": clause,
                "domain_covering": row["domain_covering"],
                "statement": rule.get("statement"),
            })

    out = {
        "report": "必然恒真（零区分度）映射登记册 —— 只登记、不改规则",
        "generated_by": "t182",
        "why": ("`--discrimination` 的 hard 档原只认「通配 *」与「整段覆盖封闭值域」，"
                "漏掉「域完备键上写单个取值」这一形态；t182 补上后 hard 由 25 条增至 64 条。"),
        "disposition": ("**清理会下调既有覆盖率**（这些规则目前都算「已映射」），"
                        "故属 t179 §6 需人判 ⑥，由人决定；机器不擅自改。"),
        "domain_complete_keys": {k: sorted(v) for k, v in ev.DOMAIN_COMPLETE_KEYS.items()},
        "sample_complete_keys_excluded": {k: sorted(v) for k, v in ev.SAMPLE_COMPLETE_KEYS.items()},
        "counts": {
            "total": len(entries),
            **{a: sum(1 for e in entries if e["art"] == a) for a in ARTS},
            "by_class": {
                c: sum(1 for e in entries if e["class"] == c)
                for c in ("domain-complete-key-single-value", "wildcard", "domain-covering-enumeration")
            },
        },
        "entries": entries,
    }
    path = ROOT / args.out
    path.write_text(json.dumps(out, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    print(f"{path.relative_to(ROOT)}：{len(entries)} 条")
    print("  按类:", out["counts"]["by_class"])
    print("  按术:", {a: out["counts"][a] for a in ARTS})
    return 0


if __name__ == "__main__":
    sys.exit(main())