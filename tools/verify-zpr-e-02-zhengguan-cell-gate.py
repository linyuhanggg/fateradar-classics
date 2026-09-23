"""Recheck whether the current shared charts prove one full ZPR-E-02 正官 cell.

This reports a source/fixture blocker, not an adopted 判格 algorithm.
Run: python3 tools/verify-zpr-e-02-zhengguan-cell-gate.py
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
EXECUTABLE = ROOT / "references/executable/ziping-zhenquan.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXPECTED_FIXTURE_SHA256 = "3f9e7b62c4d35cc4df2006cec7c994a2178d922a50377ab62c39e10d4c5b3dcc"
PILLARS = ("year", "month", "day", "time")
PROPOSED_SEMANTIC_FACTS = {
    "geju.tenGod", "geju.mode", "zpr_e02_month_use_decision",
    "zpr_e02_zhengguan_favorite_effect", "zpr_e02_zhengguan_rescue_effect",
}
SOURCE_CUES = {
    328: "財官印食，此用神之善而順用之者也",
    331: "官喜透財以相生，生印以護官",
    340: "先觀用神之何屬",
    342: "正官佩印",
    364: "官逢財印，又無刑沖破害",
    374: "官逢傷尅刑沖",
    399: "官逢傷，而透印以解之",
    400: "雜煞，而合煞以清之",
    401: "刑沖，而會合以解之",
    929: "以刑沖破害爲忌，則以生之護之爲喜",
    932: "壬印戊財，以乙隔之",
    933: "壬財丁印，二者相合，仍以孤官無輔論",
    935: "以印能護官，亦能洩官，而財生官也",
    937: "遇傷而佩印也",
    951: "官格透傷用印者，又忌見財",
    953: "地支刑沖，會合可解",
}


def values(facts: list[dict], key: str, scope: dict | None = None) -> list[str]:
    return [
        fact["value"] for fact in facts
        if fact.get("key") == key and (scope is None or fact.get("scope") == scope)
    ]


def month_harm_cues(facts: list[dict]) -> list[str]:
    return [
        value for value in values(facts, "natal_relation", {"layer": "本命"})
        if value.startswith(("相刑:", "六冲:", "六害:", "六破:"))
        and "month" in value.rsplit("@", 1)[-1].split("-")
    ]


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    for number, cue in SOURCE_CUES.items():
        assert cue in lines[number - 1], (number, cue)

    rule = next(rule for rule in json.loads(EXECUTABLE.read_text())["rules"] if rule["id"] == "ZPR-E-02")
    assert rule["required_facts"] == ["geju.tenGod", "geju.mode"]
    assert rule["rescue"] == "unimplemented" and rule["verified"] is False

    fixture_bytes = FIXTURE.read_bytes()
    fixture_sha = hashlib.sha256(fixture_bytes).hexdigest()
    assert fixture_sha == EXPECTED_FIXTURE_SHA256, "fixture changed; re-audit the full 正官 cell"
    charts = json.loads(fixture_bytes)["bazi"]
    assert len(charts) == 43, "case count changed; re-audit the full 正官 cell"

    semantic_hits = {
        case_id: sorted({f["key"] for f in chart["facts"]} & PROPOSED_SEMANTIC_FACTS)
        for case_id, chart in charts.items()
        if {f["key"] for f in chart["facts"]} & PROPOSED_SEMANTIC_FACTS
    }
    assert not semantic_hits, semantic_hits

    candidates = []
    for case_id, chart in charts.items():
        facts = chart["facts"]
        if values(facts, "geju", {"layer": "本命"}) != ["正官格"]:
            continue
        pillars = {}
        for pillar in PILLARS:
            scope = {"layer": "本命", "pillar": pillar}
            gan, zhi = values(facts, "gan", scope), values(facts, "zhi", scope)
            assert len(gan) == len(zhi) == 1, (case_id, pillar, gan, zhi)
            pillars[pillar] = gan[0] + zhi[0]
        harms = month_harm_cues(facts)
        assert harms, (case_id, "re-audit: no month harm cue")
        candidates.append({"caseId": case_id, "pillars": pillars, "monthHarmCues": harms})

    assert len(candidates) == 5, "正官格 candidate count changed; re-audit"
    unique_charts = {
        tuple(candidate["pillars"][pillar] for pillar in PILLARS) for candidate in candidates
    }
    assert len(unique_charts) == 4, "deduplication changed; re-audit"

    print(json.dumps({
        "status": "PASS",
        "scope": "current_43_real_date_charts_only",
        "sourceCuesChecked": len(SOURCE_CUES),
        "fixtureSha256": fixture_sha,
        "realDateCharts": len(charts),
        "gejuNameCandidates": len(candidates),
        "distinctCandidatePillars": len(unique_charts),
        "candidates": candidates,
        "formalMonthUseOrPerCellEffectFacts": len(semantic_hits),
        "fullCellPositiveNegativeUnknownTriplet": False,
        "formalContract": "not_adopted",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
