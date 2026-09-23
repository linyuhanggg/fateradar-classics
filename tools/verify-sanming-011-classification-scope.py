"""Check 011's unadopted, source-scoped classification evidence proposal.

This verifies chart provenance and conflicting raw labels, not a fortune verdict.
No FactKey, executable rule, or shared fixture is generated from this draft.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "tools/reports/p1-bazi-20260922/sanming-011-classification-scope-candidate.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
SOURCE = ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
RULES = ROOT / "references/books/bazi/sanming-tonghui/rules.yaml"

BENEFICIAL_NAMES = {"正财", "偏财", "正官", "正印", "偏印"}


def one(facts: list[dict], key: str, layer: str, year: int) -> dict | None:
    found = [
        fact for fact in facts
        if fact["key"] == key
        and fact.get("scope", {}).get("layer") == layer
        and fact.get("scope", {}).get("year") == year
    ]
    assert len(found) <= 1, (key, layer, year, found)
    return found[0] if found else None


def selected_value(facts: list[dict], key: str, layer: str, year: int) -> str | None:
    fact = one(facts, key, layer, year)
    return fact["value"] if fact else None


def natal_raw_groups(facts: list[dict]) -> dict[str, bool]:
    natal = [fact for fact in facts if fact.get("scope", {}).get("layer") == "本命"]
    for fact in natal:
        if fact["key"] in {"shishen", "shensha"}:
            assert fact.get("scope", {}).get("pillar") in {"year", "month", "day", "time"}, fact
            assert fact.get("derivedFrom"), fact
    return {
        "七杀": any(f["key"] == "shishen" and f["value"] == "七杀" for f in natal),
        "财官印绶": any(f["key"] == "shishen" and f["value"] in BENEFICIAL_NAMES for f in natal),
        "羊刃": any(f["key"] == "shensha" and f["value"] == "羊刃" for f in natal),
    }


def stem_raw_groups(facts: list[dict], year: int) -> list[str]:
    names = {
        selected_value(facts, "shishen", layer, year)
        for layer in ("大运", "流年")
    }
    return [group for group, seen in (
        ("七杀", "七杀" in names),
        ("财官印绶", bool(names & BENEFICIAL_NAMES)),
    ) if seen]


def verify_source() -> set[str]:
    lines = SOURCE.read_text().splitlines()
    anchors = {
        1084: ["甲子流年又是甲子運", "獨羊刃七煞為凶財官印綬亦吉"],
        1624: ["乙之正位為陰木之極"],
        1635: ["五陰干無刃"],
        3459: ["甲日生人時上見乙卯"],
        3468: ["命元有煞刄歲運又逄", "命有刃有印無煞歲運逄煞反轉成厚福"],
        3471: ["月令合財官印綬或合他格", "當以他格斷"],
        4959: ["六甲日丁卯時斷"],
        4962: ["甲日丁卯時", "柱有七煞合刃行財官印綬大貴"],
        8893: ["官印有用", "財帛有用", "大運是庚午歲是戊午"],
        10158: ["歳運併臨若損用神必有禍"],
    }
    for line, snippets in anchors.items():
        assert all(snippet in lines[line - 1] for snippet in snippets), line

    # 甲日卯时的合法时干是丁；两种源文读数均保留，不能造乙卯真盘。
    assert "甲乙丙丁戊己庚辛壬癸"[3] == "丁"
    text = RULES.read_text()
    block = re.search(r"(?ms)^- rule_id: SANMINGTONGH-011\n(.*?)(?=^- rule_id:|\Z)", text)
    assert block
    assert re.search(r"(?m)^  applicable_to: \[\]$", block.group(0))
    assert re.search(r"(?m)^  verified: false$", block.group(0))
    return {f"L{line}" for line in anchors}


def main() -> None:
    source_anchors = verify_source()
    contract = json.loads(CONTRACT.read_text())
    assert contract["schema"] == "sanming-011-classification-scope-candidate-v1"
    assert contract["status"] == "unadopted_draft"
    assert contract["factKeyStatus"] == "not_registered_do_not_emit"
    assert contract["scope"] == {"layer": "流年", "year": "selected"}
    assert contract["valueShape"]["effectVerdict"] == ["未裁决"]

    chart_cases = json.loads(FIXTURE.read_text())["bazi"]
    assert len(contract["cases"]) == 6
    observed = []
    for row in contract["cases"]:
        case_id, year = row["case"], row["year"]
        facts = chart_cases[case_id]["facts"]
        assert not {"natal_binglin_class", "suiyun_binglin_semantics", "sanming_011_classification_evidence"} & {f["key"] for f in facts}
        assert selected_value(facts, "suiyun_binglin", "流年", year) == row["shape"]
        assert selected_value(facts, "suiyun_same_zhi", "流年", year) == row["sameBranch"]
        assert natal_raw_groups(facts) == row["natalRaw"]
        for layer, label in (("大运", row["selectedLuckStem"]), ("流年", row["selectedYearStem"])):
            fact = one(facts, "shishen", layer, year)
            assert (fact["value"] if fact else None) == label, (case_id, year, layer)
            if fact:
                assert fact.get("derivedFrom"), fact
                assert ("dayun.selected" if layer == "大运" else "liunian") in fact["derivedFrom"]
        assert row["effectVerdict"] == "未裁决"
        observed.append(f"{case_id}@{year}")

    by_case = {(row["case"], row["year"]): row for row in contract["cases"]}
    assert by_case["caseFlowYearBinglin", 1993]["natalRaw"]["七杀"]
    assert by_case["caseFlowYearBinglin", 1993]["natalRaw"]["财官印绶"]
    assert not by_case["caseP1_011_seven_killer", 2031]["natalRaw"]["七杀"]
    assert by_case["caseP1_011_seven_killer", 2031]["selectedYearStem"] == "七杀"
    assert by_case["caseP1_011_proper_officer", 1960]["natalRaw"]["七杀"]
    assert by_case["caseP1_011_proper_officer", 1960]["selectedYearStem"] == "正官"
    assert by_case["caseFlowYearUnknown", 2100]["selectedLuckStem"] is None
    witnesses = contract["scopeAmbiguityWitnesses"]
    assert {(item["case"], item["year"]) for item in witnesses} == {
        ("caseFlowYearBinglin", 1993),
        ("caseP1_011_seven_killer", 2031),
        ("caseP1_011_proper_officer", 1960),
    }
    for witness in witnesses:
        facts = chart_cases[witness["case"]]["facts"]
        natal = natal_raw_groups(facts)
        assert witness["natalRawGroups"] == [
            group for group in ("七杀", "财官印绶") if natal[group]
        ], witness
        assert witness["selectedStemRawGroups"] == stem_raw_groups(facts, witness["year"]), witness
    expected_blockers = {
        "source_scoped_classification": {
            "sourceAnchors": {"L1084", "L1624", "L1635", "L3459", "L4959", "L4962"},
            "fixtureWitnesses": {"caseFlowYearBinglin@1993", "caseP1_011_seven_killer@2031", "caseP1_011_proper_officer@1960"},
        },
        "coexistence_and_conditional_order": {
            "sourceAnchors": {"L1084", "L3468", "L3471"},
            "fixtureWitnesses": {"caseFlowYearBinglin@1993", "caseP1_011_seven_killer@2031", "caseP1_011_proper_officer@1960"},
        },
        "effect_and_tristate_examples": {
            "sourceAnchors": {"L1084", "L3468", "L3471", "L8893", "L10158"},
            "fixtureWitnesses": set(observed),
        },
    }
    assert {item["id"] for item in contract["minimumBlockingDecisions"]} == set(expected_blockers)
    for blocker in contract["minimumBlockingDecisions"]:
        expected = expected_blockers[blocker["id"]]
        assert set(blocker["sourceAnchors"]) == expected["sourceAnchors"]
        assert set(blocker["sourceAnchors"]) <= source_anchors
        assert set(blocker["fixtureWitnesses"]) == expected["fixtureWitnesses"]
        assert set(blocker["fixtureWitnesses"]) <= set(observed)
    print(json.dumps({"ruleId": contract["ruleId"], "status": contract["status"], "checked": observed}, ensure_ascii=False))


if __name__ == "__main__":
    main()
