"""Falsify a deliberately narrow 月令原始正官入口 candidate against real-date charts.

Run: python3 tools/verify-zpr-e-02-single-qi-month-entry.py
This is neither a registered FactKey nor a full ZPR-E-02 implementation.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/ZPR_E_02_SINGLE_QI_MONTH_OFFICER_ENTRY_20260923.json"
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXECUTABLE = ROOT / "references/executable/ziping-zhenquan.json"
FIXTURE_SHA = "6915a56e7fef202a5c3f145106e0205b2ae1590ad2348d7f5d7ade6dd04518fb"
SOURCE_CUES = {
    146: "甲以庚爲煞，以辛爲官",
    147: "庚官而辛煞",
    149: "此所以辛以丁爲煞，而庚以丁爲官",
    328: "專求月令，以日干配月令地支",
    340: "先觀用神之何屬",
    342: "正官佩印",
    419: "除子午卯酉外，餘皆有藏",
    421: "丁生亥月，本爲正官，支全卯未，則化爲印",
    468: "甲透酉官",
    470: "丙生子月，癸水透",
    883: "丙生子月，時逢巳祿，不以爲正官之格",
    929: "以刑沖破害爲忌",
    933: "雜氣正官，透干會支",
    937: "混煞貴乎取清",
    944: "甲用酉官",
    951: "官格透傷用印者，又忌見財",
    953: "地支刑沖，會合可解",
}
SINGLE_QI = {"子": "癸", "卯": "乙", "酉": "辛"}
REGULAR_OFFICER = {
    "甲": "辛", "乙": "庚", "丙": "癸", "丁": "壬", "戊": "乙",
    "己": "甲", "庚": "丁", "辛": "丙", "壬": "己", "癸": "戊",
}


def scoped_values(facts: list[dict], key: str, pillar: str) -> list[str]:
    scope = {"layer": "本命", "pillar": pillar}
    return [fact["value"] for fact in facts if fact.get("key") == key and fact.get("scope") == scope]


def one(values: list[str]) -> str | None:
    distinct = set(values)
    return next(iter(distinct)) if len(distinct) == 1 else None


def decide(facts: list[dict], contract: dict) -> str:
    day = one(scoped_values(facts, "gan", "day"))
    month = one(scoped_values(facts, "zhi", "month"))
    month_order = one(scoped_values(facts, "yueling", "month"))
    if day not in REGULAR_OFFICER or month is None or month != month_order:
        return "信息不足"
    hidden = contract["supportedSingleQiBranches"].get(month)
    if hidden is None:
        return "信息不足"
    if set(scoped_values(facts, "canggan", "month")) != {hidden}:
        return "信息不足"
    return "满足" if hidden == contract["regularOfficerStemByDay"][day] else "不满足"


def without(facts: list[dict], key: str, pillar: str) -> list[dict]:
    scope = {"layer": "本命", "pillar": pillar}
    return [fact for fact in facts if fact.get("key") != key or fact.get("scope") != scope]


def main() -> None:
    contract = json.loads(CONTRACT.read_text())
    assert contract["status"] == "candidate_not_registered_do_not_emit"
    assert contract["scope"] == {"layer": "本命"}
    assert contract["supportedSingleQiBranches"] == SINGLE_QI
    assert contract["regularOfficerStemByDay"] == REGULAR_OFFICER
    assert contract["sourceLines"] == sorted(SOURCE_CUES)
    lines = SOURCE.read_text().splitlines()
    for line, cue in SOURCE_CUES.items():
        assert cue in lines[line - 1], (line, cue)

    rule = next(r for r in json.loads(EXECUTABLE.read_text())["rules"] if r["id"] == "ZPR-E-02")
    assert rule["rescue"] == "unimplemented" and rule["verified"] is False
    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == FIXTURE_SHA
    charts = json.loads(FIXTURE.read_text())["bazi"]
    assert len(charts) == 43

    all_states = {state: [] for state in ("满足", "不满足", "信息不足")}
    for case_id, chart in charts.items():
        all_states[decide(chart["facts"], contract)].append(case_id)
    assert {state: len(cases) for state, cases in all_states.items()} == {
        "满足": 4, "不满足": 7, "信息不足": 32,
    }, "shared chart coverage changed; re-audit candidate"

    results = {}
    for item in contract["fixtures"]:
        case_id = item["caseId"]
        facts = charts[case_id]["facts"]
        actual = decide(facts, contract)
        assert actual == item["expected"], (case_id, actual, item["expected"])
        results[case_id] = actual

    assert list(results.values()).count("满足") == 3
    assert list(results.values()).count("不满足") == 2
    assert list(results.values()).count("信息不足") == 1

    positive = charts["caseP1_010_luck_gui_only"]["facts"]
    assert decide(without(positive, "canggan", "month"), contract) == "信息不足"
    assert decide(without(positive, "gan", "day"), contract) == "信息不足"
    assert decide(without(positive, "yueling", "month"), contract) == "信息不足"
    assert decide(positive + [{"key": "gan", "value": "丁", "scope": {"layer": "本命", "pillar": "day"}}], contract) == "信息不足"
    assert decide(positive + [{"key": "canggan", "value": "庚", "scope": {"layer": "本命", "pillar": "month"}}], contract) == "信息不足"
    # A selected year, a geju label, or a month harm must not change raw month-entry status.
    assert decide(positive + [
        {"key": "geju", "value": "七杀格", "scope": {"layer": "本命"}},
        {"key": "gan", "value": "癸", "scope": {"layer": "流年", "pillar": "year", "year": 2018}},
        {"key": "natal_relation", "value": "六害:戌酉相害@year-month", "scope": {"layer": "本命"}},
    ], contract) == "满足"
    negative = charts["cov2_bazi_3"]["facts"]
    assert decide(without(negative, "zhi", "month"), contract) == "信息不足"

    print(json.dumps({
        "status": "PASS", "claim": contract["claim"], "sourceCues": len(SOURCE_CUES),
        "fixtureSha256": FIXTURE_SHA, "realDateCharts": len(charts), "cases": results,
        "allChartStates": {state: len(cases) for state, cases in all_states.items()},
        "negativeMeaning": "this_single_qi_entry_only", "formalFactRegistered": False,
        "zprE02FullEffectDelivered": False,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
