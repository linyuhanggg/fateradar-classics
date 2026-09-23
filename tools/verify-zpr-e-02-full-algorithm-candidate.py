"""Independently audit the full, provisional ZPR-E-02 source candidate.

Run: python3 tools/verify-zpr-e-02-full-algorithm-candidate.py

This validates source-scoped candidate patterns and three-state handling. It
does not register a production rule or claim that full ZPR-E-02 is verified.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
from collections import Counter
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
CONTRACT = ROOT / "docs/closeout/ZPR_E_02_FULL_ALGORITHM_CANDIDATE_20260923.json"
SOURCE = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXECUTABLE = ROOT / "references/executable/ziping-zhenquan.json"
PILLARS = ("year", "month", "day", "time")
EXPOSED_PILLARS = ("year", "month", "time")
VALID_STEMS = set("甲乙丙丁戊己庚辛壬癸")
VALID_BRANCHES = set("子丑寅卯辰巳午未申酉戌亥")
UNKNOWN = "信息不足"
TRUE = "__true__"
FALSE = "__false__"

SOURCE_CUES = {
    328: "八字用神，專求月令",
    330: "財喜食神以相生，生官以護財",
    331: "官喜透財以相生，生印以護官",
    332: "印喜官煞以相生，劫才以護印",
    333: "食喜身旺以相生，生財以護食",
    334: "七煞喜食神以制伏，忌財印以資扶",
    335: "傷官喜佩印以制伏，生財以化傷",
    336: "陽刃喜官煞以制伏，忌官煞之俱無",
    337: "月劫喜透官以制伏，利用財而透食以化劫",
    338: "此順逆之大略也",
    340: "先觀用神之何屬",
    342: "見正官佩印，則以爲官印雙全",
    347: "此皆由不知月令而妄論之故也",
    349: "然亦有月令無用神者",
    350: "如木生寅卯，日與月同",
    351: "然終以月令爲主",
    352: "刃即劫也",
    353: "是亦沈氏自相矛盾之一端也",
    383: "成中有敗，必是帶忌",
    385: "何謂帶忌？",
    396: "是皆謂之帶忌也",
    398: "何謂救應？",
    399: "官逢傷，而透印以解之",
    400: "雜煞，而合煞以清之",
    401: "刑沖，而會合以解之",
    402: "財逢劫，而透食以化之、生官以制之",
    403: "逢煞，而食神制煞以生財、或存財而合煞",
    404: "印逢財，而劫財以解之，或合財而存印",
    405: "食逢梟，而就煞以成格，或生財以護食",
    406: "煞逢食制，印來護煞，而逢財以去印存食",
    407: "傷官生財，透煞而煞逢合",
    408: "陽刃用官煞，帶傷食而重印以護之",
    409: "建祿月劫，用官遇傷而傷被合",
    411: "八字妙用，全在成敗救應",
    419: "不透甲而透丙，則如府官不臨郡，而同知得以作主",
    421: "支全卯未，則化爲印",
    426: "辛生寅月，逢丙而化財爲官",
    427: "壬生戌月，逢辛而化煞爲印",
    428: "癸生寅月，藏甲透丙，會午會戌",
    429: "乙生寅月，透戊爲財，會午會戌",
    432: "丙生寅月，本爲印綬",
    435: "辛生寅月，透丙化官，而又透甲，格成正財",
    436: "乙生申月，透壬化印，而又透戊",
    437: "癸生寅月，透丙化財，而又透甲",
    438: "丙生寅月，午戌會劫，而又或透甲",
    439: "丙生申月，逢壬化煞，而又透戊",
    440: "如此之類甚多，是皆變而不失本格者也",
    452: "辛生寅月，甲丙並透，財與官相生",
    454: "壬生未月，乙己並透，官與傷相尅",
    542: "透干會支，取其清者用之",
    544: "透戊則用偏財，透癸則用正印，透乙則用月劫",
    546: "逢申與子會局，則用水印",
    548: "一透則一用，兼透則兼用，透而又會，則透與會並用",
    550: "何謂有情？",
    551: "順而相成者是也",
    552: "印綬之格也，清而不雜",
    553: "官與印相生，而印又能去辰中暗土以清官",
    554: "透辛爲官，或巳或酉，會成金",
    558: "亥卯以成傷官之局，是透干與會支，合而無情",
    559: "甲生辰月，透戊爲財，又或透壬癸以爲印",
    560: "透壬則財印兩傷",
    561: "甲生戌月，透辛爲官，而又透丁以傷官",
    564: "甲生辰月，逢壬爲印，而又逢丙",
    565: "而火能生土，似又助",
    566: "戌與辰沖，二者爲朋沖而土動",
    569: "癸生辰月，透戊爲官，又有會申會子",
    570: "譬如月劫用官，何傷之有？",
    571: "丙生辰月，透戊爲食，而又透壬爲煞",
    572: "譬如食神帶煞",
    573: "是皆無情而終爲有情也",
    575: "如此之類，不可勝數",
}


def scoped_values(facts: list[dict[str, Any]], key: str, scope: dict[str, str]) -> set[str]:
    return {
        str(fact.get("value"))
        for fact in facts
        if fact.get("key") == key and fact.get("scope") == scope
    }


def one(facts: list[dict[str, Any]], key: str, scope: dict[str, str], valid: set[str]) -> tuple[str, str | None]:
    values = scoped_values(facts, key, scope)
    if len(values) != 1:
        return (UNKNOWN, None)
    value = next(iter(values))
    if value not in valid:
        return (UNKNOWN, None)
    return (TRUE, value)


def aggregate_all(states: list[str]) -> str:
    if FALSE in states:
        return FALSE
    if all(state == TRUE for state in states):
        return TRUE
    return UNKNOWN


def chart_value(facts: list[dict[str, Any]], key: str, pillar: str, valid: set[str]) -> tuple[str, str | None]:
    return one(facts, key, {"layer": "本命", "pillar": pillar}, valid)


def exact_day_month_state(facts: list[dict[str, Any]], match: dict[str, Any]) -> list[str]:
    states: list[str] = []
    if match.get("dayStem") is not None:
        state, value = chart_value(facts, "gan", "day", VALID_STEMS)
        if state != TRUE:
            states.append(state)
        else:
            states.append(TRUE if value == match["dayStem"] else FALSE)

    month_state, month = chart_value(facts, "zhi", "month", VALID_BRANCHES)
    states.append(month_state if month_state != TRUE else (TRUE if month == match["monthBranch"] else FALSE))
    order_state, order = chart_value(facts, "yueling", "month", VALID_BRANCHES)
    if month_state != TRUE or order_state != TRUE:
        states.append(UNKNOWN)
    else:
        states.append(TRUE if order == month else FALSE)
    return states


def complete_month_hidden_state(facts: list[dict[str, Any]], branch: str, hidden_map: dict[str, list[str]]) -> str:
    branch_state, actual_branch = chart_value(facts, "zhi", "month", VALID_BRANCHES)
    if branch_state != TRUE:
        return UNKNOWN
    if actual_branch != branch:
        return FALSE
    actual = scoped_values(facts, "canggan", {"layer": "本命", "pillar": "month"})
    if not actual or actual != set(hidden_map[branch]):
        return UNKNOWN
    return TRUE


def visible_constraint_state(facts: list[dict[str, Any]], stems: list[str], mode: str) -> str:
    by_pillar: dict[str, str | None] = {}
    incomplete = False
    for pillar in EXPOSED_PILLARS:
        state, value = chart_value(facts, "gan", pillar, VALID_STEMS)
        if state != TRUE:
            incomplete = True
            by_pillar[pillar] = None
        else:
            by_pillar[pillar] = value
    known = {value for value in by_pillar.values() if value is not None}
    required = set(stems)
    if mode == "all":
        if not required <= known:
            return UNKNOWN if incomplete else FALSE
        return TRUE
    if mode == "none":
        if required & known:
            return FALSE
        return UNKNOWN if incomplete else TRUE
    if mode == "any":
        if required & known:
            return TRUE
        return UNKNOWN if incomplete else FALSE
    raise AssertionError(f"unknown visible constraint: {mode}")


def branch_constraint_state(facts: list[dict[str, Any]], branches: list[str], mode: str) -> str:
    values: set[str] = set()
    incomplete = False
    for pillar in PILLARS:
        state, value = chart_value(facts, "zhi", pillar, VALID_BRANCHES)
        if state != TRUE:
            incomplete = True
        else:
            assert value is not None
            values.add(value)
    required = set(branches)
    if mode == "all":
        if required <= values:
            return TRUE
        return UNKNOWN if incomplete else FALSE
    if mode == "none":
        if required & values:
            return FALSE
        return UNKNOWN if incomplete else TRUE
    raise AssertionError(f"unknown branch constraint: {mode}")


def evaluate_match(facts: list[dict[str, Any]], pattern: dict[str, Any], hidden_map: dict[str, list[str]]) -> str:
    match = pattern["match"]
    states = exact_day_month_state(facts, match)
    states.append(complete_month_hidden_state(facts, match["monthBranch"], hidden_map))
    for mode in ("all", "none", "any"):
        stems = match.get({"all": "visibleAll", "none": "visibleNone", "any": "visibleAny"}[mode], [])
        if stems:
            states.append(visible_constraint_state(facts, stems, mode))
    for mode, key in (("all", "branchAll"), ("none", "branchNone")):
        branches = match.get(key, [])
        if branches:
            states.append(branch_constraint_state(facts, branches, mode))

    base = aggregate_all(states)
    if base != TRUE:
        return UNKNOWN if base == UNKNOWN else "不满足"
    for clause in pattern.get("ambiguousWhen", []):
        if "visibleAny" in clause:
            state = visible_constraint_state(facts, clause["visibleAny"], "any")
        elif "branchAll" in clause:
            state = branch_constraint_state(facts, clause["branchAll"], "all")
        elif "dayStemAny" in clause:
            day_state, day = chart_value(facts, "gan", "day", VALID_STEMS)
            state = UNKNOWN if day_state != TRUE else (TRUE if day in clause["dayStemAny"] else FALSE)
        else:
            raise AssertionError(f"unknown ambiguity condition: {clause}")
        if state != FALSE:
            return UNKNOWN
    return "满足"


STEM_ELEMENT = {"甲": 0, "乙": 0, "丙": 1, "丁": 1, "戊": 2, "己": 2, "庚": 3, "辛": 3, "壬": 4, "癸": 4}


def ten_god(day: str, target: str) -> str:
    day_element, target_element = STEM_ELEMENT[day], STEM_ELEMENT[target]
    same_polarity = (day in "甲丙戊庚壬") == (target in "甲丙戊庚壬")
    if day_element == target_element:
        return "比肩" if same_polarity else "劫财"
    if target_element == (day_element + 1) % 5:
        return "食神" if same_polarity else "伤官"
    if day_element == (target_element + 1) % 5:
        return "偏印" if same_polarity else "正印"
    if (day_element + 2) % 5 == target_element:
        return "偏财" if same_polarity else "正财"
    assert (target_element + 2) % 5 == day_element
    return "七杀" if same_polarity else "正官"


FOUR_STOREHOUSE_MEETINGS = (
    {"monthBranch": "辰", "otherBranches": {"申", "子"}, "dayStem": "甲", "role": "印", "sourceLine": 546},
    {"monthBranch": "未", "otherBranches": {"亥", "卯"}, "dayStem": "壬", "role": "伤官", "sourceLine": 558},
    {"monthBranch": "戌", "otherBranches": {"寅", "午"}, "dayStem": "甲", "role": "伤官", "sourceLine": 561},
)


def evaluate_four_storehouse(facts: list[dict[str, Any]], hidden_map: dict[str, list[str]]) -> dict[str, Any]:
    result = {"state": UNKNOWN, "entries": [], "useSemantics": UNKNOWN, "ambiguity": []}
    month_state, month = chart_value(facts, "zhi", "month", VALID_BRANCHES)
    order_state, order = chart_value(facts, "yueling", "month", VALID_BRANCHES)
    if month_state != TRUE or order_state != TRUE:
        return result
    if month not in {"辰", "戌", "丑", "未"}:
        return {**result, "state": "不满足"}
    if order != month:
        result["ambiguity"].append("月令与月支冲突")
        return result
    if complete_month_hidden_state(facts, month, hidden_map) != TRUE:
        result["ambiguity"].append("月藏集合缺失、冲突或未能确认为完整")
        return result

    stems: dict[str, str] = {}
    branches: dict[str, str] = {}
    for pillar in PILLARS:
        stem_state, stem = chart_value(facts, "gan", pillar, VALID_STEMS)
        branch_state, branch = chart_value(facts, "zhi", pillar, VALID_BRANCHES)
        if stem_state != TRUE or branch_state != TRUE:
            result["ambiguity"].append(f"本命{pillar}干支不完整")
            return result
        assert stem is not None and branch is not None
        stems[pillar], branches[pillar] = stem, branch

    exposed = [stem for stem in hidden_map[month] if any(stems[pillar] == stem for pillar in EXPOSED_PILLARS)]
    day = stems["day"]
    entries = [
        {"origin": "透干", "sourceStem": stem, "tenGod": ten_god(day, stem), "entryId": f"four-storehouse:{month}:hidden-{stem}:{day}日"}
        for stem in exposed
    ]
    branch_values = set(branches.values())
    meeting_entries = []
    for meeting in FOUR_STOREHOUSE_MEETINGS:
        if month == meeting["monthBranch"] and meeting["otherBranches"] <= branch_values and day == meeting["dayStem"]:
            meeting_entries.append({
                "origin": "会支", "sourceBranches": sorted({month, *meeting["otherBranches"]}),
                "role": meeting["role"], "sourceLine": meeting["sourceLine"],
            })
    if month == "丑" and ("巳" in branch_values or "酉" in branch_values):
        result["ambiguity"].append("L554丑月巳酉会金的‘或巳或酉’边界未裁")

    all_entries = [*entries, *meeting_entries]
    if result["ambiguity"]:
        return {**result, "entries": all_entries}
    if not all_entries:
        return {**result, "state": "不满足", "useSemantics": "未命中本四墓具名入口，不否定其它ZPR-E-02路线"}
    if entries and meeting_entries:
        semantics = "透与会并用"
    elif len(entries) == 1:
        semantics = "一透一用"
    elif len(entries) > 1:
        semantics = "兼透兼用"
    else:
        semantics = "仅命中原文明示的会支入口"
    return {"state": "满足", "entries": all_entries, "useSemantics": semantics, "ambiguity": []}


def evaluate_full_rule(facts: list[dict[str, Any]], contract: dict[str, Any]) -> tuple[str, list[str]]:
    # These are evidence slots, not proposed registered FactKey strings.
    slots = contract["inputContract"]["requiredButNotYetRegisteredSemanticSlots"]
    missing = list(slots)
    # Route-scoped facts are deliberately absent from this observation fixture.
    available_keys = {str(fact.get("key")) for fact in facts}
    observation_keys = set(contract["inputContract"]["observationDoesNotImplyEffect"])
    assert available_keys & observation_keys
    return UNKNOWN, missing


def expected_yin_facts(facts: list[dict[str, Any]]) -> dict[str, str]:
    """Recompute the two source-neutral Yin observation facts from raw rows."""
    stems: dict[str, str] = {}
    branches: dict[str, str] = {}
    for pillar in PILLARS:
        stem_state, stem = chart_value(facts, "gan", pillar, VALID_STEMS)
        branch_state, branch = chart_value(facts, "zhi", pillar, VALID_BRANCHES)
        if stem_state != TRUE or branch_state != TRUE:
            return {}
        assert stem is not None and branch is not None
        stems[pillar] = stem
        branches[pillar] = branch
    natal_day_state, natal_day = chart_value(facts, "natal_day_gan", "day", VALID_STEMS)
    if natal_day_state != TRUE or stems["day"] != natal_day:
        return {}
    if branches["month"] != "寅" or len(scoped_values(facts, "canggan", {"layer": "本命", "pillar": "month"})) != 3:
        return {}
    hidden = scoped_values(facts, "canggan", {"layer": "本命", "pillar": "month"})
    if hidden != {"甲", "丙", "戊"}:
        return {}
    exposed = [stem for stem in ("甲", "丙", "戊") if any(stems[p] == stem for p in EXPOSED_PILLARS)]
    raw_value = "".join(exposed) or "无"
    result = {"natal_yin_hidden_exposure_pattern": raw_value}
    if len(exposed) <= 2 and not {"寅", "午", "戌"} <= set(branches.values()):
        result["natal_yin_simple_hidden_exposure_pattern"] = raw_value
    return result


def registered_p106_state(facts: list[dict[str, Any]]) -> str:
    """Mirror the V6 all_of(day stem, dense simple exposure Fact) truth rule."""
    day_state, day = chart_value(facts, "gan", "day", VALID_STEMS)
    if day_state == UNKNOWN:
        day_result = UNKNOWN
    else:
        day_result = TRUE if day == "辛" else FALSE

    key = "natal_yin_simple_hidden_exposure_pattern"
    scope = {"layer": "本命", "pillar": "month"}
    values = scoped_values(facts, key, scope)
    if key not in {str(f.get("key")) for f in facts} or not values:
        pattern_result = UNKNOWN
    elif len(values) != 1:
        pattern_result = UNKNOWN
    else:
        pattern_result = TRUE if next(iter(values)) == "甲丙" else FALSE
    return "满足" if aggregate_all([day_result, pattern_result]) == TRUE else (
        "不满足" if aggregate_all([day_result, pattern_result]) == FALSE else UNKNOWN
    )


def assert_source(contract: dict[str, Any]) -> None:
    lines = SOURCE.read_text(encoding="utf-8").splitlines()
    for number, cue in SOURCE_CUES.items():
        assert number <= len(lines) and cue in lines[number - 1], (number, cue)
    cited = {
        number
        for pattern in contract["namedSourcePatterns"]
        for number in pattern["sourceLines"]
    }
    cited.update(contract["fourStorehouseRuleCandidate"]["sourceLines"])
    cited.update(contract["effectCandidate"]["sourceLines"])
    cited.update(contract["rescueCandidate"]["sourceLines"])
    cited.update([328, 340, 342, 347, 349, 350, 351, 352, 353, 383, 385, 396, 398, 409, 411])
    assert cited <= set(SOURCE_CUES), sorted(cited - set(SOURCE_CUES))


def assert_contract_integrity(contract: dict[str, Any], fixture: dict[str, Any]) -> None:
    assert contract["status"] == "candidate_not_registered_not_executable_product_contract"
    assert contract["sourceRuleId"] == "ZPR-E-02"
    assert contract["scope"]["layer"] == "本命"
    assert hashlib.sha256(FIXTURE.read_bytes()).hexdigest() == contract["fixture"]["sha256"]
    assert len(fixture) == contract["fixture"]["baziCases"] == 50
    rule = next(r for r in json.loads(EXECUTABLE.read_text(encoding="utf-8"))["rules"] if r["id"] == "ZPR-E-02")
    assert rule["rescue"] == "unimplemented" and rule["verified"] is False
    assert contract["releaseGuard"]["executableRuleChanges"] is False
    assert contract["releaseGuard"]["factVocabularyChanges"] is False
    assert contract["releaseGuard"]["manifestChanges"] is False
    assert contract["releaseGuard"]["productImportEligible"] is False
    assert contract["rescueCandidate"]["state"] == rule["rescue"]
    assert len(contract["effectCandidate"]["perRouteClauses"]) == 8
    assert len(contract["rescueCandidate"]["perRoutePatterns"]) == 11

    ids = [pattern["id"] for pattern in contract["namedSourcePatterns"]]
    assert len(ids) == len(set(ids))
    for pattern in contract["namedSourcePatterns"]:
        assert pattern["match"]["monthBranch"] in contract["supportedHiddenStemSets"]
        assert pattern["sourceLines"]
        assert pattern["output"]


def without_exact(facts: list[dict[str, Any]], key: str, scope: dict[str, str]) -> list[dict[str, Any]]:
    return [fact for fact in facts if fact.get("key") != key or fact.get("scope") != scope]


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    fixture_doc = json.loads(FIXTURE.read_text(encoding="utf-8"))
    fixtures = fixture_doc["bazi"]
    assert_source(contract)
    assert_contract_integrity(contract, fixtures)

    outcomes: dict[str, dict[str, list[str]]] = {}
    whole_rule_counts: Counter[str] = Counter()
    registered_p106_counts: Counter[str] = Counter()
    registered_p106_unknown: list[str] = []
    four_storehouse_outcomes: dict[str, dict[str, list[str]]] = {
        "满足": [], "不满足": [], UNKNOWN: [],
    }
    for pattern in contract["namedSourcePatterns"]:
        result = {"满足": [], "不满足": [], UNKNOWN: []}
        for case_id, case in fixtures.items():
            state = evaluate_match(case["facts"], pattern, contract["supportedHiddenStemSets"])
            result[state].append(case_id)
        outcomes[pattern["id"]] = result

    for case_id, case in fixtures.items():
        state, reasons = evaluate_full_rule(case["facts"], contract)
        assert state == UNKNOWN and reasons
        whole_rule_counts[state] += 1
        registered_state = registered_p106_state(case["facts"])
        registered_p106_counts[registered_state] += 1
        if registered_state == UNKNOWN:
            registered_p106_unknown.append(case_id)
        expected = expected_yin_facts(case["facts"])
        actual = {
            str(fact["key"]): str(fact["value"])
            for fact in case["facts"]
            if fact.get("key") in {
                "natal_yin_hidden_exposure_pattern",
                "natal_yin_simple_hidden_exposure_pattern",
            }
            and fact.get("scope") == {"layer": "本命", "pillar": "month"}
        }
        assert actual == expected, (case_id, actual, expected)
        four_storehouse_state = evaluate_four_storehouse(case["facts"], contract["supportedHiddenStemSets"])
        assert four_storehouse_state["state"] in four_storehouse_outcomes
        four_storehouse_outcomes[four_storehouse_state["state"]].append(case_id)

    four_storehouse_audit = contract["fourStorehouseRuleCandidate"]["currentFixtureAudit"]
    assert four_storehouse_audit["fixtureSha256"] == contract["fixture"]["sha256"]
    assert four_storehouse_audit["caseCount"] == len(fixtures) == 50
    assert {state: len(cases) for state, cases in four_storehouse_outcomes.items()} == four_storehouse_audit["states"]
    assert set(four_storehouse_outcomes[UNKNOWN]) == set(four_storehouse_audit["unknownCases"])
    assert set(four_storehouse_audit["satisfiedProbeCases"]) <= set(four_storehouse_outcomes["满足"])
    assert all(
        evaluate_four_storehouse(fixtures[case_id]["facts"], contract["supportedHiddenStemSets"])["ambiguity"]
        for case_id in four_storehouse_audit["unknownCases"]
    )

    p106 = outcomes["ZPR-L435-XIN-YIN-JIA-BING-PRINCIPAL-COMPANION"]
    assert len(p106["满足"]) == 2
    assert len(p106["不满足"]) == 46
    assert len(p106[UNKNOWN]) == 2
    assert set(p106["满足"]) == {
        "caseP1_ZPR_month_xin_jia_bing_1954",
        "caseP1_ZPR_month_xin_jia_bing_1984",
    }
    assert set(p106[UNKNOWN]) == {
        "caseP1_ZPR_month_xin_jia_bing_wu_1984",
        "caseP1_ZPR_month_xin_jia_bing_meeting_1994",
    }
    assert dict(registered_p106_counts) == {"满足": 2, "不满足": 44, UNKNOWN: 4}
    assert set(registered_p106_unknown) == {
        "caseP1_ZPR_month_xin_jia_bing_wu_1984",
        "caseP1_ZPR_month_xin_jia_bing_meeting_1994",
        "cov1_bazi_4",
        "cov3_bazi_6",
    }
    yin_bing = outcomes["ZPR-L419-YIN-NO-JIA-EXPOSED-BING"]
    assert {
        "caseP1_ZPR_month_yin_bing_only_1969",
        "caseP1_ZPR_month_xin_no_jia_1979",
    } <= set(yin_bing["满足"])
    assert "caseP1_ZPR_month_yin_bing_wu_1979" in yin_bing[UNKNOWN]

    positive_facts = fixtures["caseP1_ZPR_month_xin_jia_bing_1984"]["facts"]
    p106_pattern = next(pattern for pattern in contract["namedSourcePatterns"] if pattern["id"] == "ZPR-L435-XIN-YIN-JIA-BING-PRINCIPAL-COMPANION")
    assert evaluate_match(positive_facts, p106_pattern, contract["supportedHiddenStemSets"]) == "满足"
    assert evaluate_match(
        without_exact(positive_facts, "gan", {"layer": "本命", "pillar": "year"}),
        p106_pattern,
        contract["supportedHiddenStemSets"],
    ) == UNKNOWN
    assert evaluate_match(
        positive_facts + [{"key": "gan", "value": "庚", "scope": {"layer": "本命", "pillar": "year"}}],
        p106_pattern,
        contract["supportedHiddenStemSets"],
    ) == UNKNOWN
    assert evaluate_match(
        positive_facts + [{"key": "gan", "value": "甲", "scope": {"layer": "流年", "pillar": "year", "year": 2018}}],
        p106_pattern,
        contract["supportedHiddenStemSets"],
    ) == "满足"

    assert ten_god("甲", "戊") == "偏财"
    assert ten_god("甲", "癸") == "正印"
    assert ten_god("壬", "乙") == "伤官"
    assert ten_god("辛", "甲") == "正财"
    assert ten_god("辛", "丙") == "正官"
    chen_single = evaluate_four_storehouse(fixtures["caseP1_ZPR_01_wu_only"]["facts"], contract["supportedHiddenStemSets"])
    assert chen_single["state"] == "满足" and chen_single["useSemantics"] == "一透一用"
    assert chen_single["entries"] == [{"origin": "透干", "sourceStem": "戊", "tenGod": "偏财", "entryId": "four-storehouse:辰:hidden-戊:甲日"}]
    chen_multi = evaluate_four_storehouse(fixtures["caseP1_ZPR_01_wu_gui_both"]["facts"], contract["supportedHiddenStemSets"])
    assert chen_multi["state"] == "满足" and chen_multi["useSemantics"] == "兼透兼用"
    assert [(entry["sourceStem"], entry["tenGod"]) for entry in chen_multi["entries"]] == [("戊", "偏财"), ("癸", "正印")]
    chen_meeting = evaluate_four_storehouse(fixtures["caseP1_ZPR_02_shen_zi"]["facts"], contract["supportedHiddenStemSets"])
    assert chen_meeting["state"] == "满足" and chen_meeting["entries"][0]["origin"] == "会支"
    assert chen_meeting["entries"][0]["role"] == "印" and chen_meeting["entries"][0]["sourceLine"] == 546
    chen_none = evaluate_four_storehouse(fixtures["caseP1_ZPR_01_no_wu"]["facts"], contract["supportedHiddenStemSets"])
    assert chen_none["state"] == "不满足"
    assert evaluate_four_storehouse(
        without_exact(fixtures["caseP1_ZPR_01_wu_only"]["facts"], "canggan", {"layer": "本命", "pillar": "month"}),
        contract["supportedHiddenStemSets"],
    )["state"] == UNKNOWN
    assert evaluate_four_storehouse(
        fixtures["caseP1_ZPR_01_wu_only"]["facts"] + [{"key": "gan", "value": "戊", "scope": {"layer": "流年", "pillar": "year", "year": 2018}}],
        contract["supportedHiddenStemSets"],
    ) == chen_single

    named_coverage = {
        pattern_id: {
            "满足": len(states["满足"]),
            "不满足": len(states["不满足"]),
            "信息不足": len(states[UNKNOWN]),
            "positiveCases": states["满足"],
            "unknownCases": states[UNKNOWN],
        }
        for pattern_id, states in outcomes.items()
    }
    print(json.dumps({
        "status": "PASS",
        "sourceCues": len(SOURCE_CUES),
        "namedSourcePatterns": len(outcomes),
        "fixtureSha256": contract["fixture"]["sha256"],
        "fixtureCases": len(fixtures),
        "wholeRule": {"states": dict(whole_rule_counts), "verified": False},
        "sourceLiteralP106": {"states": {"满足": len(p106["满足"]), "不满足": len(p106["不满足"]), UNKNOWN: len(p106[UNKNOWN])}, "unknownCases": p106[UNKNOWN]},
        "registeredV6P106Predicate": {"states": dict(registered_p106_counts), "unknownCases": registered_p106_unknown},
        "fourStorehouseLocalCandidate": {"states": {state: len(cases) for state, cases in four_storehouse_outcomes.items()}, "unknownCases": four_storehouse_outcomes[UNKNOWN], "satisfiedProbeCases": four_storehouse_audit["satisfiedProbeCases"], "singleExposureCase": "caseP1_ZPR_01_wu_only", "multiExposureCase": "caseP1_ZPR_01_wu_gui_both", "meetingCase": "caseP1_ZPR_02_shen_zi", "noNamedEntryCase": "caseP1_ZPR_01_no_wu"},
        "namedPatternCoverage": named_coverage,
        "p106ProjectionChecks": "PASS",
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
