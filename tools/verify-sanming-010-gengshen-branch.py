#!/usr/bin/env python3
"""Verify the SMTH-010 named natal 庚申 witness without inferring suppression."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
HY = ROOT / "sources/normalized/shidianguji/HY1521/text.md"
SK = ROOT / "sources/normalized/shidianguji/SK1610/text.md"
PDF = ROOT / "sources/facsimile/other/sanming-tonghui/NLC416-13jh000156-94145.pdf"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
HASHES = {
    SOURCE: "ef01ff5ff538a2c64af7fda15b1393b4eeb9f75a311fe3dda7f39f0ecaa66298",
    HY: "707ac9bc6796bdb679833fc280040485d95b36da6f7aca0b3e2adbb9e57d19d3",
    SK: "4f705b654672fe6d8106353401541634de9d3db6e300271bfab7ca7e427f24dd",
    PDF: "c6eac6fca6411e45cb801f9b771aca6dd6a6d2dfb57ecc36ea5f42ecf1ac8bf9",
    FIXTURE: "6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb",
}
PILLARS = ("year", "month", "day", "time")


def scoped_value(facts: list[dict], key: str, scope: dict) -> tuple[str | None, bool]:
    values = {
        fact.get("value") for fact in facts
        if fact.get("key") == key and fact.get("scope") == scope
    }
    if len(values) > 1:
        return None, True
    return (next(iter(values)) if values else None), False


def named_natal_gengshen(facts: list[dict]) -> str:
    """Three states for one literal natal witness, never for effective 有救."""
    incomplete = False
    for pillar in PILLARS:
        scope = {"layer": "本命", "pillar": pillar}
        gan, gan_conflict = scoped_value(facts, "gan", scope)
        zhi, zhi_conflict = scoped_value(facts, "zhi", scope)
        if gan_conflict or zhi_conflict:
            incomplete = True
            continue
        if gan == "庚" and zhi == "申":
            return "present"
        if gan is None or zhi is None:
            incomplete = True
    return "undetermined" if incomplete else "absent"


def main() -> None:
    for path, expected in HASHES.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
    source = SOURCE.read_text().splitlines()
    assert "四柱元有庚申金或大運中亦有将甲木制伏純粹不能尅戊土為有救" in source[1081]
    assert "甲寅生人為身旺嵗月見庚申為煞旺柱中不透火制地支子辰㑹印成局則煞生印印生身作權貴㸔" in source[3086]
    assert "四柱元有庚申金，" in HY.read_text()
    assert "或大運中亦有將甲木制伏純粹" in HY.read_text()
    assert "四柱元有庚申金，或大運中亦有将甲木制伏純粹" in SK.read_text()

    cases = json.loads(FIXTURE.read_text())["bazi"]
    same = cases["caseP1_010_same_only"]["facts"]
    assert named_natal_gengshen(same) == "present"
    assert named_natal_gengshen(cases["caseP1_010_natal_gui_only"]["facts"]) == "absent"
    missing = [fact for fact in same if not (fact["key"] == "zhi" and fact["scope"] == {"layer": "本命", "pillar": "year"})]
    assert named_natal_gengshen(missing) == "undetermined"
    conflict = [*same, {"key": "zhi", "value": "戌", "scope": {"layer": "本命", "pillar": "year"}}]
    assert named_natal_gengshen(conflict) == "undetermined"
    assert not any(f["key"] in {"effectiveSuppression", "rescue_condition", "transit_effect_semantics"} for f in same)
    print("PASS SMTH-010 natal 庚申 literal branch: present / absent / undetermined; no effect Fact inferred")


if __name__ == "__main__":
    main()
