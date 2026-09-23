"""Audit the L419 寅月不透甲而透丙 local-principal candidate.

Run: python3 tools/verify-zpr-e-02-yin-bing-principal.py
Only the clean local entry is tested. This does not register a FactKey or
adjudicate full ZPR-E-02, a final 格, 兼格, 救应, or effect.
"""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PRODUCT = ROOT.parent / "cosmic-fortune-lab"
CONTRACT = ROOT / "docs/closeout/ZPR_E_02_YIN_BING_PRINCIPAL_CANDIDATE_20260923.json"
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXECUTABLE = ROOT / "references/executable/ziping-zhenquan.json"
SOURCE_CUES = {
    328: "八字用神，專求月令",
    340: "先觀用神之何屬",
    419: "不透甲而透丙，則如府官不臨郡，而同知得以作主",
    421: "支全卯未，則化爲印",
    542: "透干會支，取其清者用之",
    548: "兼透則兼用，透而又會，則透與會並用",
}
GAN = set("甲乙丙丁戊己庚辛壬癸")
ZHI = set("子丑寅卯辰巳午未申酉戌亥")
PILLARS = ("year", "month", "day", "time")
EXPOSED = ("year", "month", "time")
UNKNOWN = "信息不足"


def scoped_values(facts: list[dict], key: str, pillar: str) -> set[str]:
    scope = {"layer": "本命", "pillar": pillar}
    return {str(fact["value"]) for fact in facts if fact.get("key") == key and fact.get("scope") == scope}


def one(facts: list[dict], key: str, pillar: str) -> str | None:
    values = scoped_values(facts, key, pillar)
    return next(iter(values)) if len(values) == 1 else None


def decide(facts: list[dict]) -> dict[str, str]:
    result = {"premiseState": UNKNOWN, "localPrincipalStem": UNKNOWN}
    month = one(facts, "zhi", "month")
    order = one(facts, "yueling", "month")
    if month not in ZHI or order != month:
        return result
    if month != "寅":
        return {**result, "premiseState": "不满足"}
    if scoped_values(facts, "canggan", "month") != {"甲", "丙", "戊"}:
        return result

    stems: dict[str, str | None] = {}
    for pillar in EXPOSED:
        values = scoped_values(facts, "gan", pillar)
        if len(values) > 1 or any(value not in GAN for value in values):
            return result
        stems[pillar] = next(iter(values)) if values else None

    if "甲" in stems.values():
        return {**result, "premiseState": "不满足"}
    if any(stem is None for stem in stems.values()):
        return result
    if "丙" not in stems.values():
        return {**result, "premiseState": "不满足"}
    result["premiseState"] = "满足"
    # This is a conservative Product consumption gate, not a claim that L419
    # alone settles the L349–351 甲/乙日禄劫 route or an incomplete chart.
    chart_complete = all(
        one(facts, key, pillar) in (GAN if key == "gan" else ZHI)
        for key in ("gan", "zhi")
        for pillar in PILLARS
    )
    day = one(facts, "gan", "day")
    if "戊" not in stems.values() and chart_complete and day in GAN - {"甲", "乙"}:
        result["localPrincipalStem"] = "丙"
    return result


def without(facts: list[dict], key: str, pillar: str) -> list[dict]:
    scope = {"layer": "本命", "pillar": pillar}
    return [fact for fact in facts if fact.get("key") != key or fact.get("scope") != scope]


def pillars(facts: list[dict]) -> dict[str, str]:
    return {pillar: one(facts, "gan", pillar) + one(facts, "zhi", pillar) for pillar in PILLARS}


def product_chart(birth: dict[str, str]) -> dict:
    script = '''
import { buildBazi } from "./src/lib/engine/bazi";
const birth = JSON.parse(process.env.ZPR_BIRTH);
const chart = buildBazi({ name: "ZPR L419 true-date probe", gender: "男",
  ...birth, arts: ["bazi"], province: "上海", city: "上海",
  district: "黄浦区", timeBasis: "clock" });
console.log(JSON.stringify({ pillars: chart.ganzhi, facts: chart.facts }));
'''
    env = {**os.environ, "ZPR_BIRTH": json.dumps(birth, ensure_ascii=False)}
    completed = subprocess.run(
        ["bun", "-e", script], cwd=PRODUCT, env=env,
        text=True, capture_output=True, check=True,
    )
    return json.loads(completed.stdout.strip())


def main() -> None:
    contract = json.loads(CONTRACT.read_text())
    assert contract["status"] == "candidate_not_registered_do_not_emit"
    assert contract["scope"] == {"layer": "本命"}
    assert contract["source"]["lines"] == sorted(SOURCE_CUES)
    assert contract["supportedMonth"] == "寅"
    assert contract["expectedMonthHiddenStems"] == ["甲", "丙", "戊"]
    lines = SOURCE.read_text().splitlines()
    for line, cue in SOURCE_CUES.items():
        assert cue in lines[line - 1], (line, cue)

    rule = next(r for r in json.loads(EXECUTABLE.read_text())["rules"] if r["id"] == "ZPR-E-02")
    assert rule["rescue"] == "unimplemented" and rule["verified"] is False
    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == contract["fixture"]["sha256"]
    charts = json.loads(FIXTURE.read_text())["bazi"]
    assert len(charts) == contract["fixture"]["baziCases"] == 43

    real_date_results = {}
    for probe in contract["realDateProbes"]:
        if probe["producer"].startswith("Product buildBazi"):
            calculated = product_chart(probe["birth"])
            facts = calculated["facts"]
            assert calculated["pillars"] == probe["pillars"], probe["id"]
        else:
            facts = charts[probe["id"]]["facts"]
            assert pillars(facts) == probe["pillars"], probe["id"]
        actual = decide(facts)
        expected = {key: probe[key] for key in ("premiseState", "localPrincipalStem")}
        assert actual == expected, (probe["id"], actual, expected)
        real_date_results[probe["id"]] = actual
        if probe["id"] == "yin_bing_only_1969":
            positive = facts

    partial = contract["partialInputProbe"]
    assert partial["fromRealDateProbe"] == "yin_bing_only_1969"
    removed = partial["remove"]
    assert decide(without(positive, removed["key"], removed["scope"]["pillar"])) == {
        "premiseState": partial["premiseState"],
        "localPrincipalStem": partial["localPrincipalStem"],
    }
    # A conflicting same-scope fact is not permission to choose a preferred version.
    assert decide(positive + [{"key": "gan", "value": "甲", "scope": {"layer": "本命", "pillar": "year"}}]) == {
        "premiseState": UNKNOWN, "localPrincipalStem": UNKNOWN,
    }
    assert decide(without(positive, "canggan", "month")) == {
        "premiseState": UNKNOWN, "localPrincipalStem": UNKNOWN,
    }
    assert decide(without(positive, "gan", "day")) == {
        "premiseState": "满足", "localPrincipalStem": UNKNOWN,
    }
    # Flow-year stems and an existing Product 格 label cannot change this natal-only result.
    assert decide(positive + [
        {"key": "gan", "value": "甲", "scope": {"layer": "流年", "pillar": "year", "year": 2018}},
        {"key": "geju", "value": "正官格", "scope": {"layer": "本命"}},
    ]) == {"premiseState": "满足", "localPrincipalStem": "丙"}

    competing = product_chart({"year": "1979", "month": "2", "day": "11", "hour": "7", "minute": "20"})
    assert competing["pillars"] == {"year": "己未", "month": "丙寅", "day": "己酉", "time": "戊辰"}
    assert decide(competing["facts"]) == {"premiseState": "满足", "localPrincipalStem": UNKNOWN}

    yin_cases = {}
    for case_id, chart in charts.items():
        if one(chart["facts"], "zhi", "month") == "寅":
            yin_cases[case_id] = decide(chart["facts"])
    assert len(yin_cases) == 5
    assert all(result["localPrincipalStem"] == UNKNOWN for result in yin_cases.values())
    print(json.dumps({
        "status": "PASS", "sourceCues": len(SOURCE_CUES),
        "fixtureSha256": contract["fixture"]["sha256"],
        "sharedRealDateCharts": len(charts), "sharedYinMonthCharts": yin_cases,
        "additionalRealDateProbes": real_date_results,
        "competingWuExposure": decide(competing["facts"]),
        "fullZprE02Delivered": False,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
