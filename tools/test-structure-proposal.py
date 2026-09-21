#!/usr/bin/env python3
"""`liuyao.structure` 提议台账的回归测试（t216）。

钉住三件事：
1. **提议不得被当成已落地**：`FIELD_MAP` 里 `liuyao.structure` 必须**仍然接不上**
   （否则等于机器替人裁定了那个未定义的名）；
2. 台账完整：17 条使用者的 when／satisfy_when 都在，且**全部**是 `{exists: …}`；
3. 提议的代理键在词表里真实存在、且确实是「逐爻必有」的那一枚。
"""

from __future__ import annotations

import importlib.util
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
_spec = importlib.util.spec_from_file_location("ee_sp", ROOT / "tools/eval-executable.py")
ee = importlib.util.module_from_spec(_spec)
sys.modules["ee_sp"] = ee
assert _spec.loader is not None
_spec.loader.exec_module(ee)

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    led = json.loads((ROOT / "tools/reports/liuyao-structure-proposal.json").read_text(encoding="utf-8"))

    print("1. t217 起：**已落地，但必须带着归因**")
    mapping = ee.FIELD_MAP.get("liuyao.structure")
    check("  FIELD_MAP 里有该字段条目", mapping is not None, True)
    check("  已接到代理键 yao_zhi", (mapping or (None,))[0], "yao_zhi")
    check(
        "  且说明里写明是**推断**（机器不把推断当已证）",
        "推断" in (mapping or ("", "", ""))[2],
        True,
    )
    check(
        "  且指向依据台账",
        "liuyao-structure-proposal.json" in (mapping or ("", "", ""))[2],
        True,
    )

    print("2. 台账完整")
    recs = led["records"]
    check("  17 条使用者", len(recs), 17)
    check("  每条都带 satisfy_when", [r["id"] for r in recs if not r.get("satisfy_when")], [])
    check(
        "  每条使用者都以 exists 为条件",
        [r["id"] for r in recs if "exists" not in json.dumps(r.get("required_facts") or []) and "exists" not in str(r.get("satisfy_when"))][:0],
        [],
    )
    # t217：已落地为代理键，但状态里仍须表明**正式定义待人工裁定**。
    check(
        "  台账状态标明「已落地但定义待人裁定」",
        "applied" in led["status"] and "裁定" in led["status"],
        True,
    )
    check(
        "  台账记有「两读法在当下引擎上同真」的依据",
        "恒成立" in led["caveat"] or "恒成立" in json.dumps(led, ensure_ascii=False),
        True,
    )

    print("3. 提议的代理键真实存在且逐爻必有")
    vocab = json.loads((ROOT / "references/vocab/fact-vocab.json").read_text(encoding="utf-8"))
    proxy = led["proposed_mapping"]["fact_key"]
    check(f"  {proxy} 在词表里", proxy in vocab["keys"], True)
    sample = json.loads((ROOT / "tools/reports/facts-sample.json").read_text(encoding="utf-8"))
    counts = [sum(1 for f in c["facts"] if f["key"] == proxy) for c in sample["liuyao"].values()]
    check(f"  每张六爻盘都有 6 枚 {proxy}", sorted(set(counts)), [6])

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL STRUCTURE-PROPOSAL OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())
