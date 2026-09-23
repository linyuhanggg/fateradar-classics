"""Verify a neutral, unadopted 011 evidence projection against source and real charts.

The only executable verdict is equality on a selected year's raw luck-stem label.
No source category, effect, or new FactKey is inferred.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CANDIDATE = ROOT / "tools/reports/p1-bazi-20260922/sanming-011-neutral-raw-label-candidate.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
SOURCE = ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
RULES = ROOT / "references/books/bazi/sanming-tonghui/rules.yaml"
PILLARS = {"year", "month", "day", "time"}


def selected(facts: list[dict], key: str, layer: str, year: int) -> dict | None:
    matches = [
        fact for fact in facts
        if fact["key"] == key
        and fact.get("scope", {}).get("layer") == layer
        and fact.get("scope", {}).get("year") == year
    ]
    assert len(matches) <= 1, (key, layer, year, matches)
    return matches[0] if matches else None


def probe(fact: dict | None) -> str:
    if fact is None or fact["value"] == "信息不足":
        return "信息不足"
    return "满足" if fact["value"] == "七杀" else "不满足"


def verify_source() -> None:
    lines = SOURCE.read_text().splitlines()
    anchors = {
        781: ("印綬梟神", "吉凶禍福逈不同"),
        1084: ("甲子流年又是甲子運", "獨羊刃七煞為凶財官印綬亦吉"),
        3084: ("有制謂之偏官無制謂之七煞",),
        3468: ("命元有煞刄歲運又逄", "命有刃有印無煞歲運逄煞反轉成厚福"),
        3471: ("月令合財官印綬或合他格", "當以他格斷"),
        4962: ("柱有七煞合刃行財官印綬大貴",),
    }
    for line, snippets in anchors.items():
        assert all(snippet in lines[line - 1] for snippet in snippets), line
    rule = re.search(r"(?ms)^- rule_id: SANMINGTONGH-011\n(.*?)(?=^- rule_id:|\Z)", RULES.read_text())
    assert rule
    assert re.search(r"(?m)^  applicable_to: \[\]$", rule.group(0))
    assert re.search(r"(?m)^  verified: false$", rule.group(0))


def main() -> None:
    verify_source()
    candidate = json.loads(CANDIDATE.read_text())
    assert candidate["schema"] == "sanming-011-neutral-raw-label-candidate-v1"
    assert candidate["ruleId"] == "SANMINGTONGH-011"
    assert candidate["status"] == "isolated_unadopted_candidate"
    assert candidate["registeredFactKey"] is False
    assert candidate["caseLabelsAreDeduplicatedDisplayOnly"] is True
    assert candidate["sourceAnchors"] == ["L781", "L1084", "L3084", "L3468", "L3471", "L4962"]
    assert candidate["selectedScope"] == {"layer": "流年", "year": "selectedYear"}
    assert candidate["neutralProbe"]["id"] == "selected_dayun_stem_raw_qisha"
    assert candidate["projection"]["classification"] == candidate["projection"]["effect"] == "未裁决"

    chart_cases = json.loads(FIXTURE.read_text())["bazi"]
    observed = {}
    for row in candidate["cases"]:
        case_id, year = row["case"], row["year"]
        assert (case_id, year) not in observed
        facts = chart_cases[case_id]["facts"]
        natal = [fact for fact in facts if fact["key"] == "shishen" and fact.get("scope", {}).get("layer") == "本命"]
        assert natal
        for fact in natal:
            assert fact["scope"].get("pillar") in PILLARS, fact
            assert fact.get("derivedFrom"), fact
        assert sorted({fact["value"] for fact in natal}) == row["natalObservedLabels"]

        for layer, field, origin in (
            ("大运", "selectedDayunStem", "dayun.selected"),
            ("流年", "selectedLiunianStem", "liunian"),
        ):
            fact = selected(facts, "shishen", layer, year)
            assert (fact["value"] if fact else None) == row[field], (case_id, year, field)
            if fact:
                assert origin in fact.get("derivedFrom", []), fact
        shape = selected(facts, "suiyun_binglin", "流年", year)
        assert shape and shape["value"] == row["suiyunShape"]
        assert probe(selected(facts, "shishen", "大运", year)) == row["neutralProbeVerdict"]
        assert row["classification"] == row["effect"] == "未裁决"
        observed[case_id, year] = row

    assert len(observed) == 6
    assert {row["neutralProbeVerdict"] for row in observed.values()} == {"满足", "不满足", "信息不足"}
    assert observed["caseP1_011_seven_killer", 2031]["neutralProbeVerdict"] == "满足"
    assert observed["caseP1_011_proper_officer", 1960]["neutralProbeVerdict"] == "不满足"
    unknown = observed["caseFlowYearUnknown", 2100]
    assert unknown["selectedDayunStem"] is None and unknown["neutralProbeVerdict"] == "信息不足"
    assert selected(chart_cases["caseFlowYearUnknown"]["facts"], "dayun_gan_zhi", "大运", 2100) is None
    assert observed["caseFlowYear", 2019]["natalObservedLabels"] == observed["caseFlowYear", 2026]["natalObservedLabels"]
    assert observed["caseFlowYear", 2019]["selectedLiunianStem"] != observed["caseFlowYear", 2026]["selectedLiunianStem"]
    print(json.dumps({
        "ruleId": candidate["ruleId"],
        "status": candidate["status"],
        "caseCount": len(observed),
        "neutralProbeVerdicts": {f"{case}@{year}": row["neutralProbeVerdict"] for (case, year), row in observed.items()},
        "classification": "未裁决",
        "effect": "未裁决",
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
