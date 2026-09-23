#!/usr/bin/env python3
"""Verify the source-literal branches in SMTH-010 L1082, not the full outcome."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/SANMINGTONGH_010_L1082_BRANCH_AUDIT_20260923.json"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
PILLARS = ("year", "month", "day", "time")
GAN = set("甲乙丙丁戊己庚辛壬癸")
ZHI = set("子丑寅卯辰巳午未申酉戌亥")
UNKNOWN = "信息不足"
NOT_APPLICABLE = "不适用"


def scoped_values(facts: list[dict], keys: set[str], scope: dict) -> set[str]:
    return {
        fact["value"]
        for fact in facts
        if fact.get("key") in keys and fact.get("scope") == scope and isinstance(fact.get("value"), str)
    }


def one_value(facts: list[dict], keys: set[str], scope: dict, domain: set[str] | None = None) -> tuple[str | None, bool]:
    values = scoped_values(facts, keys, scope)
    if len(values) > 1:
        return None, True
    value = next(iter(values)) if values else None
    if value is not None and domain is not None and value not in domain:
        return None, True
    return value, False


def entry(facts: list[dict], selected_year: int) -> str:
    day, day_conflict = one_value(
        facts, {"gan", "natal_day_gan"}, {"layer": "本命", "pillar": "day"}, GAN
    )
    annual, annual_conflict = one_value(
        facts, {"liunian_gan"}, {"layer": "流年", "year": selected_year}, GAN
    )
    if day_conflict or annual_conflict:
        return UNKNOWN
    if (day is not None and day != "甲") or (annual is not None and annual != "戊"):
        return NOT_APPLICABLE
    if day is None or annual is None:
        return UNKNOWN
    return "满足"


def natal_gengshen_branch(facts: list[dict], selected_year: int) -> str:
    gate = entry(facts, selected_year)
    if gate != "满足":
        return gate
    pairs: list[tuple[str, str]] = []
    # The source says 四柱元有庚申金. This branch needs all four complete,
    # conflict-free Gan/Zhi pairs before either presence or absence is stated.
    for pillar in PILLARS:
        scope = {"layer": "本命", "pillar": pillar}
        gan, gan_conflict = one_value(facts, {"gan"}, scope, GAN)
        zhi, zhi_conflict = one_value(facts, {"zhi"}, scope, ZHI)
        if gan_conflict or zhi_conflict or gan is None or zhi is None:
            return UNKNOWN
        pairs.append((gan, zhi))
    return "满足" if ("庚", "申") in pairs else "不满足"


def named_guiwu_branch(facts: list[dict], selected_year: int) -> str:
    gate = entry(facts, selected_year)
    if gate != "满足":
        return gate

    natal_gans: list[str] = []
    for pillar in PILLARS:
        value, conflict = one_value(facts, {"gan"}, {"layer": "本命", "pillar": pillar}, GAN)
        if conflict or value is None:
            return UNKNOWN
        natal_gans.append(value)

    # Lifetime Dayun rows without `year` are intentionally ignored.
    active_luck, luck_conflict = one_value(
        facts,
        {"dayun_gan_zhi"},
        {"layer": "大运", "year": selected_year},
    )
    if luck_conflict or active_luck is None or len(active_luck) != 2:
        return UNKNOWN
    if active_luck[0] not in GAN or active_luck[1] not in ZHI:
        return UNKNOWN

    gui_count = natal_gans.count("癸") + (active_luck[0] == "癸")
    if gui_count == 1:
        return "满足"
    if gui_count == 0:
        return "不满足"
    # L1082 specifies 一癸. Multiple candidates and their competition are
    # unresolved, so this local clause cannot choose one.
    return UNKNOWN


def evaluate(facts: list[dict], selected_year: int) -> dict[str, str]:
    gate = entry(facts, selected_year)
    gengshen = natal_gengshen_branch(facts, selected_year)
    guiwu = named_guiwu_branch(facts, selected_year)
    if gate != "满足":
        return {
            "entry": gate,
            "natalGengshenBranch": gengshen,
            "namedGuiWuBranch": guiwu,
            "effectiveSuppressionInput": gate,
            "localAffinityInput": gate,
            "localL1082Tier": gate,
            "full010Effect": gate,
        }

    # A source-positive natal 庚申 is enough for this L1082 input. Its absence
    # cannot disprove the independent, still-unmodeled Dayun pure-suppression
    # alternative.
    suppression = "proven" if gengshen == "满足" else "undetermined"
    affinity = {
        "满足": "proven",
        "不满足": "ruled_out",
        UNKNOWN: "undetermined",
    }[guiwu]
    tier = conditional_tier(suppression, affinity)
    return {
        "entry": gate,
        "natalGengshenBranch": gengshen,
        "namedGuiWuBranch": guiwu,
        "effectiveSuppressionInput": suppression,
        "localAffinityInput": affinity,
        "localL1082Tier": tier,
        # L1086/L1087/L9697 and their precedence remain unimplemented.
        "full010Effect": UNKNOWN,
    }


def conditional_tier(suppression: str, affinity: str) -> str:
    allowed = {"proven", "ruled_out", "undetermined"}
    if suppression not in allowed or affinity not in allowed:
        raise ValueError("invalid L1082 source-input state")
    if "undetermined" in {suppression, affinity}:
        return UNKNOWN
    return {
        ("proven", "proven"): "凶反为吉",
        ("proven", "ruled_out"): "凶半",
        ("ruled_out", "proven"): "凶半",
        ("ruled_out", "ruled_out"): "凶莫能解",
    }[(suppression, affinity)]


def assert_source_audit(contract: dict) -> None:
    source = contract["source"]
    source_bytes = (ROOT / source["path"]).read_bytes()
    assert hashlib.sha256(source_bytes).hexdigest() == source["sha256"]
    lines = source_bytes.decode("utf-8").splitlines()
    assert {row["role"] for row in source["clauses"]} == {
        "entry", "two_alternative_rescue_branches", "local_gui_wu_branch",
        "conditional_ladder", "later_clause_not_resolved",
        "later_exception_not_resolved", "separate_ten_gan_naming_context",
    }
    for clause in source["clauses"]:
        assert clause["quote"] in lines[clause["line"] - 1], clause

    for witness in contract["editorialWitnesses"]:
        text_lines = (ROOT / witness["path"]).read_text(encoding="utf-8").splitlines()
        assert witness["quote"] in text_lines[witness["line"] - 1], witness

    facsimile = contract["facsimile"]
    assert hashlib.sha256((ROOT / facsimile["path"]).read_bytes()).hexdigest() == facsimile["sha256"]
    assert facsimile["pdfPagesVisuallyReviewed"] == [121, 122, 125]
    assert facsimile["imprintPages"] == [43, 44, 47]


def input_projection(cases: dict) -> dict:
    projected: dict[str, dict] = {}
    suffixes = (
        "both", "same_only", "split_only", "split_and_gui", "natal_gui_only",
        "luck_gui_only", "neither", "wrong_day", "wrong_year", "unknown_luck",
    )
    for suffix in suffixes:
        case_id = f"caseP1_010_{suffix}"
        selected_year = 2017 if suffix == "wrong_year" else 2018
        consumed = []
        for fact in cases[case_id]["facts"]:
            scope = fact["scope"]
            key = fact["key"]
            if key in {"gan", "natal_day_gan"} and scope == {"layer": "本命", "pillar": "day"}:
                consumed.append(fact)
            elif key in {"gan", "zhi"} and scope.get("layer") == "本命" and scope.get("pillar") in PILLARS:
                consumed.append(fact)
            elif key == "liunian_gan" and scope == {"layer": "流年", "year": selected_year}:
                consumed.append(fact)
            elif key == "dayun_gan_zhi" and scope == {"layer": "大运", "year": selected_year}:
                consumed.append(fact)
        projected[case_id] = {"label": cases[case_id]["label"], "facts": consumed}
    return projected


def test_synthetic_boundaries(cases: dict) -> None:
    both = cases["caseP1_010_both"]["facts"]
    assert natal_gengshen_branch(both, 2018) == "满足"
    assert named_guiwu_branch(both, 2018) == "满足"

    # Completeness is required before asserting either true or false for the
    # whole-natal same-pillar branch, even if another known pillar is 庚申.
    missing_pillar = [
        fact for fact in both
        if not (fact["key"] == "zhi" and fact["scope"] == {"layer": "本命", "pillar": "time"})
    ]
    assert natal_gengshen_branch(missing_pillar, 2018) == UNKNOWN
    conflict_pillar = [
        *both, {"key": "zhi", "value": "戌", "scope": {"layer": "本命", "pillar": "year"}}
    ]
    assert natal_gengshen_branch(conflict_pillar, 2018) == UNKNOWN

    # The real split_only chart has 庚 in year and 申 in day; no pair may be
    # assembled across pillars.
    assert natal_gengshen_branch(cases["caseP1_010_split_only"]["facts"], 2018) == "不满足"

    # Conflicting selected-year inputs stay unknown.
    annual_conflict = [
        *both, {"key": "liunian_gan", "value": "丁", "scope": {"layer": "流年", "year": 2018}}
    ]
    assert evaluate(annual_conflict, 2018)["entry"] == UNKNOWN
    natal_day_conflict = [
        *both, {"key": "natal_day_gan", "value": "乙", "scope": {"layer": "本命", "pillar": "day"}}
    ]
    assert evaluate(natal_day_conflict, 2018)["entry"] == UNKNOWN

    # Repeated visible 癸 and contradictory same-year luck are not silently
    # reduced to a positive or negative affinity input.
    natal_multi_gui = [
        ({**fact, "value": "癸"} if fact.get("key") == "gan"
         and fact.get("scope") == {"layer": "本命", "pillar": "time"} else fact)
        for fact in cases["caseP1_010_natal_gui_only"]["facts"]
    ]
    assert named_guiwu_branch(natal_multi_gui, 2018) == UNKNOWN
    active_luck_conflict = [
        *both, {"key": "dayun_gan_zhi", "value": "癸巳", "scope": {"layer": "大运", "year": 2018}}
    ]
    assert named_guiwu_branch(active_luck_conflict, 2018) == UNKNOWN

    # Keep unscoped lifetime luck in place while deleting the selected-year
    # row. It cannot fill that missing scope.
    missing_selected_luck = [
        fact for fact in both
        if not (fact["key"] == "dayun_gan_zhi" and fact["scope"] == {"layer": "大运", "year": 2018})
    ]
    assert named_guiwu_branch(missing_selected_luck, 2018) == UNKNOWN

    # Past-year 癸 must not satisfy the selected-year 2018 combination.
    luck_case = cases["caseP1_010_luck_gui_only"]["facts"]
    selected_luck_without_gui = [
        ({**fact, "value": "丙戌"} if fact.get("key") == "dayun_gan_zhi"
         and fact.get("scope") == {"layer": "大运", "year": 2018} else fact)
        for fact in luck_case
    ]
    assert named_guiwu_branch(selected_luck_without_gui, 2018) == "不满足"

    # Another Wu year elsewhere in the same chart cannot satisfy selected 丁.
    assert evaluate(both, 2017)["entry"] == NOT_APPLICABLE

    ladder = {
        ("proven", "proven"): "凶反为吉",
        ("proven", "ruled_out"): "凶半",
        ("ruled_out", "proven"): "凶半",
        ("ruled_out", "ruled_out"): "凶莫能解",
    }
    for states, expected in ladder.items():
        assert conditional_tier(*states) == expected
    assert conditional_tier("proven", "undetermined") == UNKNOWN


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    assert contract["schema"] == "fateradar-smth-010-l1082-branch-audit-v1"
    assert contract["status"] == "local_source_branch_audit_only"
    assert_source_audit(contract)

    fixture = contract["fixture"]
    fixture_bytes = FIXTURE.read_bytes()
    assert hashlib.sha256(fixture_bytes).hexdigest() == fixture["sha256"]
    bazi = json.loads(fixture_bytes)["bazi"]
    assert len(bazi) == fixture["baziCaseCount"] == 50
    expected_ids = set(fixture["010CaseIds"])
    actual_ids = {case_id for case_id in bazi if case_id.startswith("caseP1_010_")}
    assert actual_ids == expected_ids and len(actual_ids) == 10

    projection = input_projection(bazi)
    projection_bytes = json.dumps(projection, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(projection_bytes).hexdigest() == fixture["inputProjectionSha256"]

    expectations = contract["realChartProjection"]
    assert set(expectations) == expected_ids
    for case_id, expected in expectations.items():
        selected_year = 2017 if case_id.endswith("wrong_year") else 2018
        actual = evaluate(bazi[case_id]["facts"], selected_year)
        assert actual == expected, (case_id, actual, expected)

    test_synthetic_boundaries(bazi)

    source_rules = yaml.safe_load((ROOT / "references/books/bazi/sanming-tonghui/rules.yaml").read_text())
    original = next(row for row in source_rules["rules"] if row["rule_id"] == "SANMINGTONGH-010")
    assert original["applicable_to"] == [] and original["verified"] is False
    semantic_keys = {"rescue_condition", "transit_effect_semantics"}
    assert not any(
        fact["key"] in semantic_keys
        for case_id in expected_ids
        for fact in bazi[case_id]["facts"]
    )

    print(
        "PASS SMTH-010 L1082 branch audit: source/facsimile hashes; 50-case fixture; "
        "10 scoped real charts; local Geng-Shen and Gui-Wu positive/negative/unknown; "
        "no full 010 outcome promoted"
    )


if __name__ == "__main__":
    main()
