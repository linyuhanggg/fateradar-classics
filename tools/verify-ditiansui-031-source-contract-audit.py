#!/usr/bin/env python3
"""Read-only evidence checks for the DITIANSUICHA-031 source audit."""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SOURCE_PATH = Path("sources/fulltext/bazi/ditiansui-chanwei/fulltext.md")
RULES_PATH = Path("references/books/bazi/ditiansui-chanwei/rules.yaml")
ANNOTATIONS_PATH = Path("references/annotations/bazi/ditiansui-chanwei.json")
SOURCE_CASES_PATH = Path("references/cases/source-cases.json")
MANIFEST_PATH = Path("docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json")
FIXTURE_PATH = Path("tools/reports/facts-sample.json")
AUDIT_PATH = Path("docs/closeout/DITIANSUICHA_031_SOURCE_CONTRACT_AUDIT_20260923.md")
FIXTURE_SHA256 = "206638e12e5390ea8d41f8140d23f61efcee673dfa5aebd65e2dc95c937df5f8"
SOURCE_PILLARS = ["辛卯", "丁酉", "庚午", "丙子"]
SOURCE_BRANCHES = ["卯", "酉", "午", "子"]


def read_json(relative_path: Path):
    return json.loads((ROOT / relative_path).read_text(encoding="utf-8"))


def check_source_text() -> None:
    lines = (ROOT / SOURCE_PATH).read_text(encoding="utf-8").splitlines()
    expected = {
        96: "天干庚辛丙丁，正配火炼秋金；",
        97: "地支子午卯酉，又配坎离震兑。",
        98: "支全四正，气贯八方，然五行无土，虽诞秋令，不作旺论。",
        99: "最喜子午逢冲，水克火，使午火不破酉金，足以辅主；",
        100: "更妙卯酉逢冲，金克木，则卯木不助午火，制伏得宜。",
        101: "卯酉为震兑，主仁义之真极；",
        6157: "震兑主仁义之真机，势不两立，而有相成者存。",
        6160: "主之所喜者在震，以兑为敌国，必用火攻；",
        6163: "主之所喜者在兑，以震为游兵，易于灭而不可党震也；",
        6166: "然金忌木，木不带火，木不伤土者，不必去木也。",
        6167: "若木忌金，而金强者不可战，惟囚金而木茂，木终不能为金之害，反以成金之义；",
        6168: "春木而金盛，金实足以制木之性，反以全木之仁。",
        6179: "余细究之，震兑之理有五，攻、成、润、从、暖也。",
        6180: "春初之木，木嫩金坚，火以攻之；",
        6181: "仲春之木，木旺金衰，土以成之；",
        6182: "夏令之木，木泄金燥，水以润之；",
        6183: "秋令之木，木凋金锐，土以从之；",
        6184: "冬令之木，木衰金寒，火以暖之。",
        6187: "当泄则泄，当制则制，须观其金木之竟向，不必拘执而分内外也。",
        11: "> [注] 任氏曰：干为天元，支为地元，支中所藏为人元。人之禀命，万有不齐，总不越此三元之理，所谓万法宗也。阴阳本乎太极，是谓帝载，五行播于四时，是谓神功，乃三才之统系，万物之本原。《滴天髓》首明天道如此。",
    }
    for line_number, quote in expected.items():
        actual = lines[line_number - 1]
        if actual != quote:
            raise AssertionError(
                f"{SOURCE_PATH}:{line_number} changed: expected {quote!r}, got {actual!r}"
            )


def check_rule_is_still_pending() -> None:
    text = (ROOT / RULES_PATH).read_text(encoding="utf-8")
    match = re.search(
        r"(?ms)^- rule_id: DITIANSUICHA-031\n(.*?)(?=^- rule_id:|\Z)", text
    )
    if not match:
        raise AssertionError("DITIANSUICHA-031 rule entry is missing")
    body = match.group(1)
    required = (
        "anchor:\n    file: sources/fulltext/bazi/ditiansui-chanwei/fulltext.md\n"
        "    start_line: 101\n    end_line: 101",
        "applicable_to: {all_of: [{key: zhi, value: 卯}, {key: zhi, value: 酉}]}",
        "verified: false",
    )
    for fragment in required:
        if fragment not in body:
            raise AssertionError(f"DITIANSUICHA-031 changed unexpectedly: {fragment!r}")


def check_source_case_registry() -> None:
    annotations = read_json(ANNOTATIONS_PATH)
    matching_annotations = [
        entry
        for entry in annotations["entries"]
        if entry.get("paragraphId") == "ditiansui-chanwei:L0096-L0104"
    ]
    if len(matching_annotations) != 1:
        raise AssertionError("Expected one annotation for L0096-L0104")
    annotated = matching_annotations[0]
    if annotated.get("case", {}).get("pillars") != SOURCE_PILLARS:
        raise AssertionError("Annotated source chart changed")
    if "不补" not in " ".join(annotated.get("notes", [])):
        raise AssertionError("Source case annotation no longer records its evidence limits")

    cases = read_json(SOURCE_CASES_PATH)["cases"]
    matching_cases = [
        case
        for case in cases
        if case.get("id") == "ditiansui-chanwei:L0096-L0104"
    ]
    if len(matching_cases) != 1:
        raise AssertionError("Expected one source-case record for L0096-L0104")
    case = matching_cases[0]
    if case.get("pillars") != SOURCE_PILLARS:
        raise AssertionError("Source-case pillars changed")
    if case.get("verified") is not False:
        raise AssertionError("The historical source case must remain unverified")
    unavailable = set(case.get("unavailable", []))
    if not {"公历生日", "出生地与时制", "起运"}.issubset(unavailable):
        raise AssertionError("Source-case missing inputs were removed")


def natal_branches(chart: dict) -> dict[str, str]:
    result: dict[str, str] = {}
    for fact in chart.get("facts", []):
        scope = fact.get("scope", {})
        if (
            fact.get("key") == "zhi"
            and scope.get("layer") == "本命"
            and scope.get("pillar") in {"year", "month", "day", "time"}
        ):
            result[scope["pillar"]] = fact.get("value")
    return result


def has_source_relations(chart: dict) -> bool:
    relations = [
        fact.get("value", "")
        for fact in chart.get("facts", [])
        if fact.get("key") == "natal_relation"
        and fact.get("scope", {}).get("layer") == "本命"
    ]
    relation_text = " ".join(relations)
    return "六冲:卯酉相冲" in relation_text and (
        "六冲:子午相冲" in relation_text or "六冲:午子相冲" in relation_text
    )


def check_frozen_fixture() -> None:
    manifest = read_json(MANIFEST_PATH)
    fixture_info = manifest.get("factFixture", {})
    if fixture_info.get("path") != str(FIXTURE_PATH):
        raise AssertionError("v6 fixture path changed")
    if fixture_info.get("sha256") != FIXTURE_SHA256:
        raise AssertionError("v6 manifest fixture SHA changed")
    if fixture_info.get("caseCount") != 50:
        raise AssertionError("v6 fixture caseCount changed")

    fixture_bytes = (ROOT / FIXTURE_PATH).read_bytes()
    actual_hash = hashlib.sha256(fixture_bytes).hexdigest()
    if actual_hash != FIXTURE_SHA256:
        raise AssertionError(f"v6 fixture bytes changed: {actual_hash}")
    fixture = json.loads(fixture_bytes)
    charts = fixture["bazi"]
    if len(charts) != 50:
        raise AssertionError(f"Expected 50 Bazi cases, got {len(charts)}")
    if b"1951-09-26" in fixture_bytes:
        raise AssertionError("1951 date candidate unexpectedly entered the frozen fixture")

    exact_source_shapes = []
    for case_id, chart in charts.items():
        branches = natal_branches(chart)
        if (
            len(branches) == 4
            and set(branches.values()) == set(SOURCE_BRANCHES)
            and has_source_relations(chart)
        ):
            exact_source_shapes.append(case_id)
    if exact_source_shapes:
        raise AssertionError(
            "Expected the exact source shape to be absent from v6 fixture; found "
            + ", ".join(exact_source_shapes)
        )

    control = charts.get("caseA")
    if not control or control.get("label") != "甲 1990-08-15 13:20 男 上海":
        raise AssertionError("Expected caseA negative shape control")
    if natal_branches(control) != {
        "year": "午",
        "month": "申",
        "day": "子",
        "time": "未",
    }:
        raise AssertionError("caseA branch facts changed")
    if not any(
        fact.get("key") == "natal_relation"
        and fact.get("value") == "六冲:午子相冲@year-day"
        for fact in control.get("facts", [])
    ):
        raise AssertionError("caseA no longer provides the intended 午子-only control")


def main() -> None:
    if not (ROOT / AUDIT_PATH).is_file():
        raise AssertionError(f"Audit report missing: {AUDIT_PATH}")
    check_source_text()
    check_rule_is_still_pending()
    check_source_case_registry()
    check_frozen_fixture()
    print("PASS: DITIANSUICHA-031 source anchors and five seasonal routes verified")
    print("PASS: source case remains four-pillars-only and unverified")
    print("PASS: rule 031 remains anchored at L101 and verified=false")
    print(f"PASS: v6 fixture SHA-256 {FIXTURE_SHA256}; 50 cases unchanged")
    print("PASS: source-shape sample is absent; complete caseA is a narrow negative control")
    print("NOTE: no outcome/auspiciousness contract is adopted by this audit")


if __name__ == "__main__":
    main()
