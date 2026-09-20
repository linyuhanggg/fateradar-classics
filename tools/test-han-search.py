#!/usr/bin/env python3
"""繁简折半检索与其教训的回归测试（t185）。

背景：同一类「检索盲区伪造出查无」的错已犯三次——
t177（简体「游魂」搜繁体正文，得 0 行 → 误判「本版无正文」）、
t182（域完备键漏一类 → 恒真 25 少算成 64）、
t183（简体格局名搜繁体术语表 → 8 个有定义的名字判成「全文 0 次」）。

本测试钉住：

1. `han_search.lookup` **两种口径都报**，且两口径不一致时 `diverges=True`；
2. 具体反例：简体「月朗天门」「贪火相逢」原字面 0 行、折半有命中 → 必须报 diverges；
3. t177 的错案必须**可复现地被纠正**：「游魂」折半后能搜到 zengshan-buyi L7720–L7730；
4. 台账里的更正（`t185_correction`）引文逐字落在所引行上。
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("hs", ROOT / "tools/han_search.py")
hs = importlib.util.module_from_spec(_spec)
sys.modules["hs"] = hs
assert _spec.loader is not None
_spec.loader.exec_module(hs)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    print("1. 两口径都报，且不一致时报警")
    r = hs.lookup("月朗天门")
    check("  原字面 0 行", len(r["literal"]), 0)
    check("  折半后有命中", len(r["folded"]) > 0, True)
    check("  标记 diverges", r["diverges"], True)

    r2 = hs.lookup("贪火相逢")
    check("  贪火相逢同样 diverges", r2["diverges"], True)

    r3 = hs.lookup("完全不存在的词")
    check("  真·查无：两口径皆 0", (len(r3["literal"]), len(r3["folded"])), (0, 0))
    check("  真·查无不标 diverges", r3["diverges"], False)

    print("2. t177 错案可复现地被纠正")
    r4 = hs.lookup("游魂")
    zsb = [h for h in r4["folded"] if "zengshan-buyi" in h["file"]]
    check("  折半后能在曾删卜易里搜到", len(zsb) > 0, True)
    lines = {h["line"] for h in zsb}
    check("  含 L7720–L7730 段内的行", bool(lines & {7720, 7724, 7728}), True)
    check("  繁体原字面也搜得到（说明语料是繁体）", len(r4["literal"]) > 0, True)

    print("3. 台账更正：引文逐字落在所引行")
    d = json.loads((ROOT / "tools/reports/ungrounded-claims.json").read_text(encoding="utf-8"))
    corr = d.get("t185_correction")
    check("  t185_correction 存在", isinstance(corr, dict), True)
    bad = []
    for s in corr["evidence"]:
        p = ROOT / s["file"]
        if not p.is_file():
            bad.append(f"文件不存在 {s['file']}")
            continue
        ls = p.read_text(encoding="utf-8").split("\n")
        if s["line"] > len(ls) or s["quote"] not in ls[s["line"] - 1]:
            bad.append(f"{s['file']} L{s['line']}")
    check(f"  {len(corr['evidence'])} 处引文逐字", bad, [])
    check("  三条各自的分析都在", sorted(corr["per_rule"]), ["ZENGSHANBUYI-ZR-13", "ZR-09", "ZR-13"])
    check("  记下了「须以用神为主」这一告诫", "用神" in corr["decisive_caveat"], True)
    check("  处置仍是保持空（不由机器改 statement）", "applicable_to: []" in corr["disposition"], True)
    # 三条仍未映射（结论没变，变的是理由）
    import yaml

    live = {}
    for p in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        for rr in yaml.safe_load(p.read_text(encoding="utf-8")).get("rules") or []:
            if isinstance(rr, dict):
                live.setdefault(rr["rule_id"], rr.get("applicable_to"))
    check("  三条仍为空", [rid for rid in ("ZR-09", "ZR-13", "ZENGSHANBUYI-ZR-13") if live.get(rid)], [])

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL HAN-SEARCH OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())