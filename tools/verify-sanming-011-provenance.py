"""Verify the source-scoped, non-semantic evidence boundary for SANMINGTONGH-011.

This is an audit of real chart facts, not an executable fortune rule. It does
not assign a favorable/unfavorable class or mutate the shared fixture.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
RULES = ROOT / "references/books/bazi/sanming-tonghui/rules.yaml"
FIXTURE = ROOT / "tools/reports/facts-sample.json"

CASES = {
    ("caseFlowYearBinglin", 1993): ("癸酉", "癸酉", "正财", "正财", "是", "是"),
    ("caseP1_011_seven_killer", 2031): ("辛亥", "辛亥", "七杀", "七杀", "是", "是"),
    ("caseP1_011_proper_officer", 1960): ("庚子", "庚子", "正官", "正官", "是", "是"),
    ("caseFlowYear", 2019): ("丁亥", "己亥", "正财", "正官", "否", "是"),
    ("caseFlowYear", 2026): ("丁亥", "丙午", "正财", "偏财", "否", "否"),
    ("caseFlowYearUnknown", 2100): (None, "庚申", None, "偏印", "信息不足", "信息不足"),
}


def one(facts: list[dict], key: str, layer: str, year: int | None = None) -> dict | None:
    matches = [
        fact for fact in facts
        if fact["key"] == key
        and fact.get("scope", {}).get("layer") == layer
        and fact.get("scope", {}).get("year") == year
    ]
    assert len(matches) <= 1, (key, layer, year, matches)
    return matches[0] if matches else None


def value(facts: list[dict], key: str, layer: str, year: int) -> str | None:
    item = one(facts, key, layer, year)
    return item["value"] if item else None


def gan_zhi_parts(ganzhi: str | None) -> tuple[str, str] | None:
    if ganzhi is None:
        return None
    assert len(ganzhi) == 2, ganzhi
    return ganzhi[0], ganzhi[1]


def source_checks() -> None:
    lines = SOURCE.read_text().splitlines()
    needles = {
        1084: ("甲子流年又是甲子運", "獨羊刃七煞為凶財官印綬亦吉", "甲子日見甲子太嵗"),
        1635: ("五陰干無刃",),
        3459: ("甲日生人時上見乙卯",),
        3468: ("命元有煞刄歲運又逄", "命有刃有印無煞歲運逄煞反轉成厚福"),
        3471: ("月令合財官印綬或合他格", "當以他格斷"),
        4959: ("六甲日丁卯時斷",),
        8893: ("大運是庚午歲是戊午", "歲運並臨亦為吉㑹"),
        10158: ("歳運併臨若損用神必有禍",),
    }
    for line_number, fragments in needles.items():
        assert all(fragment in lines[line_number - 1] for fragment in fragments), line_number

    # Five-rat hour stem for 甲/己 day starts at 甲子; 卯 is the fourth hour.
    # L4959 independently names 丁卯. L3459's 甲日乙卯時 is thus not a
    # realizable birth hour; source text is preserved instead of emended.
    stems = "甲乙丙丁戊己庚辛壬癸"
    assert stems[3] == "丁" and stems[3] != "乙"

    text = RULES.read_text()
    match = re.search(r"(?ms)^- rule_id: SANMINGTONGH-011\n(.*?)(?=^- rule_id:|\Z)", text)
    assert match, "missing SANMINGTONGH-011"
    block = match.group(0)
    assert re.search(r"(?m)^  applicable_to: \[\]$", block)
    assert re.search(r"(?m)^  verified: false$", block)


def natal_markers(facts: list[dict]) -> dict[str, list[dict]]:
    observed = {"七杀": [], "财官印绶": [], "原始羊刃标签": []}
    good = {"正财", "偏财", "正官", "正印", "偏印"}
    for fact in facts:
        scope = fact.get("scope", {})
        if scope.get("layer") != "本命":
            continue
        if fact["key"] == "shishen" and fact["value"] == "七杀":
            bucket = "七杀"
        elif fact["key"] == "shishen" and fact["value"] in good:
            bucket = "财官印绶"
        elif fact["key"] == "shensha" and fact["value"] == "羊刃":
            bucket = "原始羊刃标签"
        else:
            continue
        observed[bucket].append({
            "value": fact["value"],
            "pillar": scope["pillar"],
            "derivedFrom": fact["derivedFrom"],
        })
    return observed


def main() -> None:
    source_checks()
    samples = json.loads(FIXTURE.read_text())["bazi"]
    result = []
    for (case_id, year), expected in CASES.items():
        facts = samples[case_id]["facts"]
        assert not {"natal_binglin_class", "suiyun_binglin_semantics", "transit_effect_semantics"} & {
            fact["key"] for fact in facts
        }, case_id
        luck = value(facts, "dayun_gan_zhi", "大运", year)
        annual = value(facts, "liunian_gan_zhi", "流年", year)
        luck_shishen = value(facts, "shishen", "大运", year)
        annual_shishen = value(facts, "shishen", "流年", year)
        exact = value(facts, "suiyun_binglin", "流年", year)
        same_zhi = value(facts, "suiyun_same_zhi", "流年", year)
        assert (luck, annual, luck_shishen, annual_shishen, exact, same_zhi) == expected, (case_id, year)
        annual_fact = one(facts, "shishen", "流年", year)
        luck_fact = one(facts, "shishen", "大运", year)
        assert annual_fact and "liunian" in annual_fact["derivedFrom"]
        if luck is None:
            assert luck_fact is None
            assert exact == same_zhi == "信息不足"
        else:
            assert luck_fact and "dayun.selected" in luck_fact["derivedFrom"]
            assert exact == ("是" if luck == annual else "否")
            assert same_zhi == ("是" if gan_zhi_parts(luck)[1] == gan_zhi_parts(annual)[1] else "否")
        markers = natal_markers(facts)
        result.append({
            "case": case_id,
            "year": year,
            "luck": luck,
            "annual": annual,
            "luckStemTenGod": luck_shishen,
            "annualStemTenGod": annual_shishen,
            "exactShape": exact,
            "sameBranchShape": same_zhi,
            "natalMarkers": markers,
            "effectVerdict": "未裁决",
        })

    by_case = {(row["case"], row["year"]): row for row in result}
    mixed = by_case["caseFlowYearBinglin", 1993]["natalMarkers"]
    assert mixed["七杀"] and {m["value"] for m in mixed["财官印绶"]} >= {"正财", "正官", "正印"}
    assert by_case["caseP1_011_proper_officer", 1960]["natalMarkers"]["七杀"]
    assert by_case["caseP1_011_proper_officer", 1960]["annualStemTenGod"] == "正官"
    assert by_case["caseFlowYear", 2019]["exactShape"] == "否"
    assert by_case["caseFlowYear", 2019]["sameBranchShape"] == "是"
    assert all(row["effectVerdict"] == "未裁决" for row in result)
    print(json.dumps({"ruleId": "SANMINGTONGH-011", "caseCount": len(result), "cases": result}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
