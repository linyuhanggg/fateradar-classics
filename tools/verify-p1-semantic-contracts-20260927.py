"""Verify the 2026-09-27 delegated-adjudication Bazi semantic contracts.

Checks, all of which must pass:

1. every quoted anchor appears verbatim inside its pinned line range;
2. the pinned fulltext tree equals both HEAD and origin/main (citations stay
   remotely checkable);
3. the fixture bytes match the contract's declared SHA-256;
4. an independent Python implementation of the adjudication tables recomputes
   every semantic value in the 24 real-chart cases and the 4,500 yearly sample
   rows produced by the product engine, row by row;
5. each semantic contract satisfies the product's acceptance gate shape and its
   declared fixtures carry the declared values;
6. each L1 rule, evaluated with three-valued logic on the case facts, yields the
   declared satisfied / not-satisfied / unknown verdicts, and the resulting
   polarity equals the fixture's expected polarity.

The script is read-only except for its JSON report.
"""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CONTRACTS = ROOT / "docs/closeout/P1_BAZI_SEMANTIC_CONTRACTS_20260927.json"
REPORT = ROOT / "tools/reports/p1-bazi-20260927/semantic-contract-verification.json"

# --- 裁决书第 3 节：结构对照表（按原文独立写出，不读产品代码） ---------------------
ELEMENT = {"甲": "木", "乙": "木", "丙": "火", "丁": "火", "戊": "土", "己": "土", "庚": "金", "辛": "金", "壬": "水", "癸": "水"}
BRANCH_MAIN = {"子": "水", "丑": "土", "寅": "木", "卯": "木", "辰": "土", "巳": "火", "午": "火", "未": "土", "申": "金", "酉": "金", "戌": "土", "亥": "水"}
KE = {"木": "土", "土": "水", "水": "火", "火": "金", "金": "木"}
SHENG = {"木": "火", "火": "土", "土": "金", "金": "水", "水": "木"}
YANG = set("甲丙戊庚壬")
HE = {"甲": "己", "己": "甲", "乙": "庚", "庚": "乙", "丙": "辛", "辛": "丙", "丁": "壬", "壬": "丁", "戊": "癸", "癸": "戊"}
TIANDE = {"寅": "丁", "辰": "壬", "巳": "辛", "未": "甲", "申": "癸", "戌": "丙", "亥": "乙", "丑": "庚"}
YUEDE = {}
for months, stem in (("寅午戌", "丙"), ("亥卯未", "甲"), ("申子辰", "壬"), ("巳酉丑", "庚")):
    for month in months:
        YUEDE[month] = stem
YANG_REN = {"甲": "卯", "丙": "午", "戊": "午", "庚": "酉", "壬": "子"}
YIN_LU_QIAN = {"乙": "辰", "丁": "未", "己": "未", "辛": "戌", "癸": "丑"}


def ten_god(day: str, other: str) -> str:
    same = (day in YANG) == (other in YANG)
    d, o = ELEMENT[day], ELEMENT[other]
    if d == o:
        return "比肩" if same else "劫财"
    if SHENG[d] == o:
        return "食神" if same else "伤官"
    if KE[d] == o:
        return "偏财" if same else "正财"
    if KE[o] == d:
        return "七杀" if same else "正官"
    return "偏印" if same else "正印"


def fan(day: str | None, year_stem: str | None) -> str:
    if day not in ELEMENT or year_stem not in ELEMENT:
        return "信息不足"
    if KE[ELEMENT[day]] != ELEMENT[year_stem]:
        return "否"
    if HE[day] == year_stem:
        return "信息不足"
    return "是"


def sample_or_none(stems: list[str | None], branches: list[str | None], dayun: str | None):
    if not dayun or len(dayun) != 2 or dayun[0] not in ELEMENT or dayun[1] not in BRANCH_MAIN:
        return None
    if any(s not in ELEMENT for s in stems) or any(b not in BRANCH_MAIN for b in branches):
        return None
    return list(stems) + [dayun[0]], list(branches) + [dayun[1]]


def rescue_control(day, year_stem, stems, branches, dayun) -> str:
    state = fan(day, year_stem)
    if state == "否":
        return "不适用"
    if state == "信息不足":
        return "信息不足"
    sample = sample_or_none(stems, branches, dayun)
    if sample is None:
        return "信息不足"
    all_stems, all_branches = sample
    controller = next(e for e in KE if KE[e] == ELEMENT[day])
    output = SHENG[ELEMENT[day]]
    has_c = any(ELEMENT[s] == controller for s in all_stems)
    has_f = any(ELEMENT[s] == output for s in all_stems)
    if has_c and not has_f:
        return "成立"
    if has_c or has_f:
        return "信息不足"
    if any(BRANCH_MAIN[b] == controller for b in all_branches):
        return "信息不足"
    return "不成立"


def rescue_combine(day, year_stem, stems, branches, dayun) -> str:
    state = fan(day, year_stem)
    if state == "否":
        return "不适用"
    if state == "信息不足":
        return "信息不足"
    sample = sample_or_none(stems, branches, dayun)
    if sample is None:
        return "信息不足"
    all_stems, _ = sample
    count = sum(1 for s in all_stems if s == HE[year_stem])
    if count == 0:
        return "不成立"
    if count >= 2 or year_stem in all_stems:
        return "信息不足"
    return "成立"


def tianyue(day, month) -> str:
    if day not in ELEMENT or month not in BRANCH_MAIN:
        return "信息不足"
    return "是" if TIANDE.get(month) == day or YUEDE.get(month) == day else "否"


def binglin_class(day, binglin, ganzhi) -> str:
    if binglin == "否":
        return "不适用"
    if binglin != "是" or day not in ELEMENT or not ganzhi or len(ganzhi) != 2:
        return "信息不足"
    stem, branch = ganzhi[0], ganzhi[1]
    if stem not in ELEMENT or branch not in BRANCH_MAIN:
        return "信息不足"
    god = ten_god(day, stem)
    good = god in {"正财", "偏财", "正官", "正印"}
    if god == "七杀":
        return "羊刃七杀"
    if day in YANG and YANG_REN[day] == branch:
        return "信息不足" if good else "羊刃七杀"
    uncertain = (
        (day not in YANG and YIN_LU_QIAN[day] == branch)
        or god == "劫财"
        or (day not in YANG and god == "伤官")
    )
    if uncertain:
        return "信息不足"
    return "财官印绶" if good else "其他"


# --- 三值求值（与产品 evaluateApplicableTo 同义） ------------------------------------
UNKNOWN = "信息不足"


def eval_node(node: dict, facts: list[dict]) -> str:
    if "key" in node:
        layer = node.get("scope", {}).get("layer")
        scoped = [f for f in facts if f["key"] == node["key"] and (layer is None or f["scope"]["layer"] == layer)]
        present = any(f["key"] == node["key"] and f["value"] != UNKNOWN for f in facts)
        if not present:
            return UNKNOWN
        if any(f["value"] == node["value"] for f in scoped if f["value"] != UNKNOWN):
            return "满足"
        return UNKNOWN if any(f["value"] == UNKNOWN for f in scoped) else "不满足"
    children = [eval_node(child, facts) for child in node.get("any_of", node.get("all_of", []))]
    if "any_of" in node:
        if "满足" in children:
            return "满足"
        return UNKNOWN if UNKNOWN in children else "不满足"
    if "不满足" in children:
        return "不满足"
    return UNKNOWN if UNKNOWN in children else "满足"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], cwd=ROOT, check=True, capture_output=True, text=True).stdout.strip()


def main() -> int:
    contracts = json.loads(CONTRACTS.read_text(encoding="utf-8"))
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: object = None) -> None:
        checks.append({"check": name, "ok": bool(ok), **({"detail": detail} if detail is not None else {})})
        if not ok:
            raise AssertionError(f"{name}: {detail}")

    check("status", contracts["semanticContractStatus"] == "accepted" and contracts["verificationMethod"] == "delegated_adjudication")

    # 1. anchors
    sources = {key: (ROOT / path).read_text(encoding="utf-8").splitlines() for key, path in contracts["sources"].items()}
    anchors = {a["id"]: a for a in contracts["anchors"]}
    for anchor in contracts["anchors"]:
        lines = sources[anchor["source"]][anchor["startLine"] - 1 : anchor["endLine"]]
        check(f"anchor:{anchor['id']}", anchor["quote"] in "".join(lines), anchor["quote"])
    for rule in contracts["rules"]:
        text = (ROOT / rule["anchor"]["file"]).read_text(encoding="utf-8").splitlines()
        lines = text[rule["anchor"]["startLine"] - 1 : rule["anchor"]["endLine"]]
        check(f"rule-anchor:{rule['ruleId']}", rule["quote"] in "".join(lines), rule["quote"])
        check(f"rule-supporting:{rule['ruleId']}", all(ref in anchors for ref in rule["supportingAnchors"]))
    for contract in contracts["semanticContracts"].values():
        check("contract-anchors-known", all(ref in anchors for ref in contract["anchors"]))

    # 2. source pin
    pin = contracts["sourcePin"]
    check("source-pin:HEAD", git("rev-parse", f"HEAD:{pin['path']}") == pin["gitTree"])
    check("source-pin:origin", git("rev-parse", f"origin/main:{pin['path']}") == pin["gitTree"])
    check("source-pin:remote-commit", git("rev-parse", f"{pin['remoteCommit']}:{pin['path']}") == pin["gitTree"])

    # 3. fixture bytes
    fixture_path = ROOT / contracts["fixture"]["path"]
    raw = fixture_path.read_bytes()
    check("fixture-sha256", hashlib.sha256(raw).hexdigest() == contracts["fixture"]["sha256"])
    fixture = json.loads(raw)
    cases = fixture["cases"]
    check("fixture-case-count", len(cases) == contracts["fixture"]["caseCount"])
    check("fixture-sample-rows", len(fixture["sample"]) == contracts["fixture"]["sampleRows"])
    check("fixture-adjudication", fixture["adjudication"] == contracts["adjudication"]["id"])

    # 4. independent recomputation
    def case_inputs(case: dict) -> dict:
        facts = case["facts"]
        year = case["selectedYear"]

        def natal(key: str, pillar: str | None = None) -> str | None:
            values = {f["value"] for f in facts if f["key"] == key and f["scope"]["layer"] == "本命" and (pillar is None or f["scope"].get("pillar") == pillar)}
            return values.pop() if len(values) == 1 else None

        def yearly(key: str, layer: str = "流年") -> str | None:
            values = {f["value"] for f in facts if f["key"] == key and f["scope"]["layer"] == layer and f["scope"].get("year") == year}
            return values.pop() if len(values) == 1 else None

        return {
            "day": natal("gan", "day"),
            "stems": [natal("gan", p) for p in ("year", "month", "time")],
            "branches": [natal("zhi", p) for p in ("year", "month", "day", "time")],
            "month": natal("zhi", "month"),
            "dayun": yearly("dayun_gan_zhi", "大运"),
            "liunian": yearly("liunian_gan_zhi"),
            "binglin": yearly("suiyun_binglin"),
            "emitted": {
                "rizhu_tianyue_de": natal("rizhu_tianyue_de"),
                "rizhu_fan_suijun": yearly("rizhu_fan_suijun"),
                "suijun_rescue_control": yearly("suijun_rescue_control"),
                "suijun_rescue_combine": yearly("suijun_rescue_combine"),
                "suiyun_binglin_class": yearly("suiyun_binglin_class"),
            },
        }

    def recompute(day, stems, branches, month, dayun, liunian, binglin) -> dict:
        year_stem = liunian[0] if liunian else None
        return {
            "rizhu_tianyue_de": tianyue(day, month),
            "rizhu_fan_suijun": fan(day, year_stem),
            "suijun_rescue_control": rescue_control(day, year_stem, stems, branches, dayun),
            "suijun_rescue_combine": rescue_combine(day, year_stem, stems, branches, dayun),
            "suiyun_binglin_class": binglin_class(day, binglin, liunian),
        }

    mismatches: list[dict] = []
    for case_id, case in cases.items():
        inputs = case_inputs(case)
        mine = recompute(inputs["day"], inputs["stems"], inputs["branches"], inputs["month"], inputs["dayun"], inputs["liunian"], inputs["binglin"])
        declared = {k: v for k, v in case["values"].items() if k != "suiyun_binglin"}
        if mine != inputs["emitted"] or mine != declared:
            mismatches.append({"case": case_id, "python": mine, "emitted": inputs["emitted"], "declared": declared})
    check("case-recompute", not mismatches, mismatches[:5])

    columns = fixture["sampleColumns"]
    sample_mismatches: list[dict] = []
    for row in fixture["sample"]:
        r = dict(zip(columns, row))
        mine = recompute(
            r["day"], [r["yearStem"], r["monthStem"], r["hourStem"]],
            [r["yearBranch"], r["monthBranch"], r["dayBranch"], r["hourBranch"]],
            r["monthBranch"], r["dayun"], r["liunian"], r["suiyun_binglin"],
        )
        emitted = {key: r[key] for key in mine}
        if mine != emitted:
            sample_mismatches.append({"row": r, "python": mine})
    check("sample-recompute", not sample_mismatches, sample_mismatches[:5])
    distribution: dict[str, dict[str, int]] = {}
    for row in fixture["sample"]:
        r = dict(zip(columns, row))
        for key in ("rizhu_fan_suijun", "suijun_rescue_control", "suijun_rescue_combine", "suiyun_binglin_class"):
            distribution.setdefault(key, {}).setdefault(r[key], 0)
            distribution[key][r[key]] += 1

    # 5. contract shape (same rules as the product gate) and declared fixtures
    synthetic = contracts["syntheticCases"]
    for key, contract in contracts["semanticContracts"].items():
        domain = contract["valueDomain"]
        check(f"shape:{key}:domain", "信息不足" in domain)
        check(f"shape:{key}:layer", contract["scope"]["layer"] in {"本命", "大运", "流年", "流月", "流日"})
        fx = contract["fixtures"]
        for state in ("satisfied", "not_satisfied", "unknown"):
            entry = fx[state]
            check(f"shape:{key}:{state}", isinstance(entry.get("case"), str) and entry["expectedValue"] in domain)
            if contract["scope"].get("year") == "selected":
                check(f"shape:{key}:{state}:year", isinstance(entry.get("year"), int))
            check(f"shape:{key}:{state}:unknown-policy", (entry["expectedValue"] == "信息不足") == (state == "unknown"))
        check(f"shape:{key}:distinct", fx["satisfied"]["expectedValue"] != fx["not_satisfied"]["expectedValue"])
        for entry in [*fx.values(), *contract.get("examples", [])]:
            if entry["case"] in synthetic:
                s = synthetic[entry["case"]]["input"]
                value = tianyue(s.get("dayGan"), s.get("monthZhi")) if key == "rizhu_tianyue_de" else None
                check(f"synthetic:{entry['case']}", value == entry["expectedValue"] == synthetic[entry["case"]]["expected"][key])
                continue
            case = cases[entry["case"]]
            if "year" in entry:
                check(f"fixture-year:{key}:{entry['case']}", case["selectedYear"] == entry["year"])
            check(f"fixture-value:{key}:{entry['case']}", case["values"][key] == entry["expectedValue"], (case["values"][key], entry["expectedValue"]))

    # 6. rule verdicts and polarity
    polarity_mismatches: list[dict] = []
    verdict_table: dict[str, dict[str, str]] = {}
    for case_id, case in cases.items():
        labels = set()
        for rule in contracts["rules"]:
            verdict = eval_node(rule["applicableTo"], case["facts"])
            verdict_table.setdefault(rule["ruleId"], {})[case_id] = verdict
            if verdict == "满足":
                labels.add(rule["label"])
        polarity = "冲突" if labels == {"吉", "凶"} else (labels.pop() if labels else None)
        if polarity != case["expectedPolarity"]:
            polarity_mismatches.append({"case": case_id, "python": polarity, "fixture": case["expectedPolarity"]})
    check("polarity", not polarity_mismatches, polarity_mismatches)
    state_name = {"satisfied": "满足", "not_satisfied": "不满足", "unknown": "信息不足"}
    for rule in contracts["rules"]:
        for state, case_ids in rule["fixtures"].items():
            for case_id in case_ids:
                got = verdict_table[rule["ruleId"]][case_id]
                check(f"rule-fixture:{rule['ruleId']}:{case_id}", got == state_name[state], got)
        for field in ("topic", "layer", "contractPurpose", "semanticContractId", "plainSummary"):
            check(f"rule-field:{rule['ruleId']}:{field}", bool(rule.get(field)))
        check(f"rule-label:{rule['ruleId']}", rule["label"] in {"吉", "凶"})
        used = {leaf for leaf in json.dumps(rule["applicableTo"], ensure_ascii=False).split('"') if leaf in contracts["semanticContracts"]}
        check(f"rule-keys-accepted:{rule['ruleId']}", bool(used))

    report = {
        "result": "PASS",
        "contractVersion": contracts["contractVersion"],
        "fixtureSha256": contracts["fixture"]["sha256"],
        "cases": len(cases),
        "sampleRows": len(fixture["sample"]),
        "checks": len(checks),
        "sampleDistribution": distribution,
        "ruleVerdicts": verdict_table,
    }
    REPORT.parent.mkdir(parents=True, exist_ok=True)
    REPORT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"PASS: {len(checks)} checks, {len(cases)} cases, {len(fixture['sample'])} sample rows")
    return 0


if __name__ == "__main__":
    sys.exit(main())
