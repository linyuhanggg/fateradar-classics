"""Recheck the evidence boundary before adopting a 051 effect contract.

This checks source anchors and the current shared real-date fixture. It does
not infer 喜行, 用神, 忌神, or real-world outcomes from structural facts.

Run: python3 tools/verify-ditiansui-051-effect-gate.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
RULES = ROOT / "dist/rules/bazi.json"
EXPECTED_FIXTURE_SHA256 = "3f9e7b62c4d35cc4df2006cec7c994a2178d922a50377ab62c39e10d4c5b3dcc"

# Distinct source branches: the same listed shape is not an effect verdict.
SOURCE_CUES = {
    13402: "权其轻重，看喜行行何运，忌行何运",
    13407: "一运看十年切勿上下截看",
    13417: "喜木运而遇庚寅辛卯",
    13419: "喜木运而遇甲申、乙酉",
    13423: "金绝寅卯，谓之无根",
    13424: "原局天干有丙丁透露",
    13425: "因盖头有庚辛之克",
    13426: "原局地支有早点酉之冲",
    13428: "原局天干透壬登",
    13430: "太岁管一年否泰",
    13431: "日主旺相虽凶无碍",
    13434: "战冲不和之故",
    13455: "辛卯截脚，局中丁火回克",
    13475: "足以用木生火",
    13477: "乙酉截脚之木",
    13479: "癸酉年水逢金生，又在冬令",
    13480: "必克丁火无疑",
}

MISSING_SEMANTIC_FACTS = {
    "favorite_luck_element_decision_record",
    "yongshen",
    "natal_favorable_context",
    "yongshen_effective",
    "jishen_empowered",
    "transit_effect_semantics",
}


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    for number, cue in SOURCE_CUES.items():
        assert cue in lines[number - 1], (number, cue)

    fixture_bytes = FIXTURE.read_bytes()
    fixture_sha = hashlib.sha256(fixture_bytes).hexdigest()
    assert fixture_sha == EXPECTED_FIXTURE_SHA256, "fixture changed; re-audit 051 effect examples"
    charts = json.loads(fixture_bytes)["bazi"]
    assert len(charts) == 43, "case count changed; re-audit 051 effect examples"

    semantic_hits = {
        case_id: sorted({fact["key"] for fact in chart["facts"]} & MISSING_SEMANTIC_FACTS)
        for case_id, chart in charts.items()
        if {fact["key"] for fact in chart["facts"]} & MISSING_SEMANTIC_FACTS
    }
    assert not semantic_hits, semantic_hits

    cases_with_selected_luck = sum(
        any(
            fact.get("key") == "dayun_gan_zhi"
            and fact.get("scope", {}).get("layer") == "大运"
            and isinstance(fact.get("scope", {}).get("year"), int)
            for fact in chart["facts"]
        )
        for chart in charts.values()
    )
    rule = next(rule for rule in json.loads(RULES.read_text()) if rule["ruleId"] == "DITIANSUICHA-051")
    assert rule["applicableTo"] == [] and rule["verification"] == "provisional"

    print(json.dumps({
        "status": "PASS",
        "scope": "current_43_real_date_charts_only",
        "sourceCuesChecked": len(SOURCE_CUES),
        "fixtureSha256": fixture_sha,
        "realDateCharts": len(charts),
        "chartsWithYearScopedLuck": cases_with_selected_luck,
        "chartsWithAdjudicatedFavoriteOrEffectFact": len(semantic_hits),
        "positiveEffectCases": 0,
        "negativeEffectCases": 0,
        "formalEffectContract": "not_adopted",
        "reason": "missing_source_adjudicated_favorite_and_effect_branch_fixtures",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
