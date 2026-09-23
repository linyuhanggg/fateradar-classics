#!/usr/bin/env python3
"""Audit the local SMTH-010 named 癸/戊 clause, never effective affinity."""

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
}
CASE_INPUT_SHA256 = "c77a70123c85db8a5089e651b2cdad2f1005265494c463a32a6728f2c58773ad"
PILLARS = ("year", "month", "day", "time")
GAN = set("甲乙丙丁戊己庚辛壬癸")
ZHI = set("子丑寅卯辰巳午未申酉戌亥")
UNKNOWN = {"信息不足", "未知"}
EXPECTED = {
    "both": "present",
    "same_only": "absent",
    "split_only": "absent",
    "split_and_gui": "present",
    "natal_gui_only": "present",
    "luck_gui_only": "present",
    "neither": "absent",
    "unknown_luck": "undetermined",
    "wrong_day": "not_applicable",
    "wrong_year": "not_applicable",
}


def one_value(facts: list[dict], key: str, scope: dict) -> str | None:
    values = {fact.get("value") for fact in facts if fact.get("key") == key and fact.get("scope") == scope}
    return next(iter(values)) if len(values) == 1 else None


def classify(facts: list[dict], selected_year: int) -> str:
    """Classify only the named local clause, not its effectiveness or fortune."""
    day = one_value(facts, "gan", {"layer": "本命", "pillar": "day"})
    year = one_value(facts, "liunian_gan", {"layer": "流年", "year": selected_year})
    if day not in GAN or year not in GAN:
        return "undetermined"
    if day != "甲" or year != "戊":
        return "not_applicable"

    natal = [one_value(facts, "gan", {"layer": "本命", "pillar": pillar}) for pillar in PILLARS]
    active_luck = one_value(facts, "dayun_gan_zhi", {"layer": "大运", "year": selected_year})
    if any(value not in GAN for value in natal):
        return "undetermined"
    if active_luck is None or active_luck in UNKNOWN or len(active_luck) != 2:
        return "undetermined"
    if active_luck[0] not in GAN or active_luck[1] not in ZHI:
        return "undetermined"
    gui_count = natal.count("癸") + (active_luck[0] == "癸")
    if gui_count == 1:
        return "present"
    if gui_count == 0:
        return "absent"
    return "undetermined"  # L1082 says 一癸; L1122 warns of competing pairs.


def case_input_projection(cases: dict) -> dict:
    """Pin only the 010 inputs consumed here; other theme facts may evolve."""
    projected = {}
    for suffix in EXPECTED:
        name = f"caseP1_010_{suffix}"
        case = cases[name]
        selected_year = 2017 if suffix == "wrong_year" else 2018
        relevant = []
        for fact in case["facts"]:
            scope = fact["scope"]
            if fact["key"] == "gan" and scope.get("layer") == "本命" and scope.get("pillar") in PILLARS:
                relevant.append(fact)
            elif fact["key"] == "liunian_gan" and scope == {"layer": "流年", "year": selected_year}:
                relevant.append(fact)
            elif fact["key"] == "dayun_gan_zhi" and scope == {"layer": "大运", "year": selected_year}:
                relevant.append(fact)
        projected[name] = {"label": case["label"], "facts": relevant}
    return projected


def main() -> None:
    for path, expected in HASHES.items():
        assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, path
    lines = SOURCE.read_text().splitlines()
    anchors = {
        1081: "日犯嵗君如甲日尅戊年",
        1082: "如大運并四柱中有一癸字與戊相合為有情",
        1118: "戊與癸何名為無情之合",
        1122: "合者貴平得中而不偏",
        1124: "内有衝破受傷合中有刑煞皆為不吉",
        3926: "得癸卯時癸合去戊為壬以癸妹妻戊",
        8035: "有情乃合氣也",
        9700: "此言人之性情心術",
    }
    for number, quote in anchors.items():
        assert quote in lines[number - 1], (number, quote)
    assert "并四柱中有一癸字，與戊相合，爲有情" in HY.read_text()
    assert "如大運并四柱中有一癸字與戊相合為有情" in SK.read_text()
    assert "戊與癸何名爲無情之合" in HY.read_text()
    assert "戊與癸，何名為無情之合" in SK.read_text()

    cases = json.loads(FIXTURE.read_text())["bazi"]
    assert {key for key in cases if key.startswith("caseP1_010_")} == {f"caseP1_010_{suffix}" for suffix in EXPECTED}
    projection = case_input_projection(cases)
    projection_bytes = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(projection_bytes).hexdigest() == CASE_INPUT_SHA256
    for suffix, expected in EXPECTED.items():
        facts = cases[f"caseP1_010_{suffix}"]["facts"]
        selected_year = 2017 if suffix == "wrong_year" else 2018
        assert classify(facts, selected_year) == expected, suffix
        assert not any(
            fact["key"] in {"affinity", "effectiveAffinity", "rescue_condition", "transit_effect_semantics"}
            for fact in facts
        ), suffix

    base = cases["caseP1_010_natal_gui_only"]["facts"]
    assert classify([*base, {"key": "gan", "value": "癸", "scope": {"layer": "本命", "pillar": "time"}}], 2018) == "undetermined"
    assert classify([fact for fact in base if not (fact["key"] == "gan" and fact["scope"] == {"layer": "本命", "pillar": "month"})], 2018) == "undetermined"
    assert classify([*base, {"key": "dayun_gan_zhi", "value": "癸巳", "scope": {"layer": "大运", "year": 2019}}], 2018) == "present"
    doubled = [
        {**fact, "value": "癸"} if fact["key"] == "gan" and fact["scope"] == {"layer": "本命", "pillar": "time"} else fact
        for fact in base
    ]
    assert classify(doubled, 2018) == "undetermined"
    print("PASS SMTH-010 Gui/Wu local clause: 4 present / 3 absent / 1 undetermined / 2 not-applicable; effective affinity unadjudicated")


if __name__ == "__main__":
    main()
