#!/usr/bin/env python3
"""Add the literal 甲日戊岁 entrance to the locked 12-rule P1 handoff."""

from __future__ import annotations

import argparse
import copy
import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BASE_PATH = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923.json"
BASE_SHA = "d14138f81b9ed8ee366c8b9b95530126c1668450a5808e5934cf17a58c17e8d2"
SOURCE_REV = "af53647efa1dde4d967bdacc918ca42913e2bab1"
SOURCE_RULES = "references/books/bazi/sanming-tonghui/rules.yaml"
SOURCE_FULLTEXT = "sources/fulltext/bazi/sanming-tonghui/fulltext.md"
FACT_FIXTURE = ROOT / "tools/reports/facts-sample.json"
EXPORT_PATH = ROOT / "dist/rules/bazi.json"
EXPORT_SHA = "baa69b67dd8fcf7b9b70cefee88af9d41086205bbc6a79d47b26eecb958bd888"
OUTPUT = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V4.json"
RULE_ID = "SANMINGTONGH-P1-010A"
YEAR_VALUES = ["戊子", "戊寅", "戊辰", "戊午", "戊申", "戊戌"]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def committed_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{SOURCE_REV}:{path}"], cwd=ROOT)


def selected_facts(facts: list[dict], year: int) -> list[dict]:
    """Keep natal witnesses and just one selected annual scope."""
    return [
        fact for fact in facts
        if fact.get("scope", {}).get("layer") == "本命"
        or fact.get("scope", {}) == {"layer": "流年", "year": year}
    ]


def evaluation(evaluator, rule: dict, case: dict, year: int) -> dict:
    facts = selected_facts(case["facts"], year)
    result = evaluator.evaluate(rule, facts)
    return {
        "case": case["id"],
        "year": year,
        "factCount": len(facts),
        "verdict": result["verdict"],
        "confidence": result["confidence"],
        "factCoverage": result["fact_coverage"],
        "missingFactKeys": result["missing_fact_keys"],
    }


def make_manifest() -> dict:
    base_bytes = BASE_PATH.read_bytes()
    assert sha256(base_bytes) == BASE_SHA
    base = json.loads(base_bytes)
    assert base["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v3"
    assert base["semanticContractStatus"] == "pending" and len(base["rules"]) == 12
    assert len({entry["ruleId"] for entry in base["rules"]}) == 12

    source_bytes = committed_bytes(SOURCE_RULES)
    assert (ROOT / SOURCE_RULES).read_bytes() == source_bytes
    source_rules = yaml.safe_load(source_bytes)["rules"]
    matching = [item for item in source_rules if item["rule_id"] == RULE_ID]
    assert len(matching) == 1
    source = matching[0]
    assert source["verified"] is False
    assert source["anchor"] == {"file": SOURCE_FULLTEXT, "start_line": 1081, "end_line": 1081}
    assert source["quote"] in (ROOT / SOURCE_FULLTEXT).read_text().splitlines()[1080]
    clauses = source["applicable_to"]["all_of"]
    assert clauses[0] == {"key": "gan", "value": "甲", "scope": {"layer": "本命", "pillar": "day"}}
    assert [item["value"] for item in clauses[1]["any_of"]] == YEAR_VALUES
    assert all(item["key"] == "liunian_gan_zhi" and item["scope"] == {"layer": "流年"} for item in clauses[1]["any_of"])

    assert sha256(EXPORT_PATH.read_bytes()) == EXPORT_SHA
    exported = json.loads(EXPORT_PATH.read_text())
    export_match = [item for item in exported if item["ruleId"] == RULE_ID]
    assert len(export_match) == 1
    assert export_match[0]["quote"] == source["quote"]
    assert export_match[0]["applicableTo"] == source["applicable_to"]
    assert export_match[0]["anchor"] == {"file": SOURCE_FULLTEXT, "startLine": 1081, "endLine": 1081}

    spec = importlib.util.spec_from_file_location("p1_evaluator", ROOT / "tools/eval-predicates.py")
    assert spec and spec.loader
    evaluator = importlib.util.module_from_spec(spec)
    sys.modules["p1_evaluator"] = evaluator
    spec.loader.exec_module(evaluator)
    fixture_bytes = FACT_FIXTURE.read_bytes()
    assert sha256(fixture_bytes) == base["factFixture"]["sha256"]
    cases = json.loads(fixture_bytes)["bazi"]
    probes = {
        "positive": ("caseP1_010_both", 2018, "满足"),
        "negative": ("caseP1_010_wrong_day", 2018, "不满足"),
        "wrongYear": ("caseP1_010_wrong_year", 2017, "不满足"),
        "unknownLuck": ("caseP1_010_unknown_luck", 2018, "满足"),
    }
    results = {}
    for label, (case_id, year, verdict) in probes.items():
        result = evaluation(evaluator, source, {**cases[case_id], "id": case_id}, year)
        assert result["verdict"] == verdict, result
        results[label] = result

    positive = {**cases["caseP1_010_both"], "id": "caseP1_010_both_minus_selected_year"}
    positive["facts"] = [
        fact for fact in positive["facts"]
        if not (fact["key"] == "liunian_gan_zhi" and fact.get("scope", {}).get("year") == 2018)
    ]
    boundary = evaluation(evaluator, source, positive, 2018)
    assert boundary["verdict"] == "信息不足" and boundary["missingFactKeys"] == ["liunian_gan_zhi"]
    missing_day = {**cases["caseP1_010_both"], "id": "caseP1_010_both_minus_day_gan"}
    missing_day["facts"] = [
        fact for fact in missing_day["facts"]
        if not (fact["key"] == "gan" and fact.get("scope") == {"layer": "本命", "pillar": "day"})
    ]
    day_boundary = evaluation(evaluator, source, missing_day, 2018)
    assert day_boundary["verdict"] == "信息不足" and day_boundary["missingFactKeys"] == ["gan"]
    assert evaluator.evaluate(source, cases["caseP1_010_wrong_year"]["facts"])["verdict"] == "满足", "foreign year guard must be observable"

    manifest = copy.deepcopy(base)
    manifest["manifestVersion"] = "fateradar-p1-bazi-topic-handoff-v4"
    manifest["generatedBy"] = "tools/generate-p1-bazi-13-manifest.py"
    manifest["classicsRev"] = SOURCE_REV
    manifest["sourceHeadAtAudit"] = SOURCE_REV
    manifest["previousHandoff"] = {"path": str(BASE_PATH.relative_to(ROOT)), "sha256": BASE_SHA, "ruleCount": 12}
    manifest["sourceFingerprint"]["sanmingRulesYamlSha256"] = sha256(source_bytes)
    manifest["contract"]["layerPolicy"] = (
        "当前 10 条本命规则只适用于本命；YUANHAIZIPIN-YR-03、SANMINGTONGH-P1-011A 和 "
        "SANMINGTONGH-P1-010A 只适用于所选流年。三条流年规则求值前必须保留本命事实、只取 "
        "scope.year=selectedYear 的流年事实；未选年与缺事实均保留信息不足。"
    )
    manifest["topics"]["overview"]["ruleIds"].append(RULE_ID)
    manifest["statusSummary"]["adopted"] = sorted([*base["statusSummary"]["adopted"], RULE_ID])
    entry = {
        "ruleId": RULE_ID,
        "art": "bazi",
        "book": "bazi/sanming-tonghui",
        "primaryTopic": "overview",
        "secondaryTopics": [],
        "status": "adopted_as_provisional_evidence",
        "role": "structural",
        "sourceRuleId": "SANMINGTONGH-010",
        "statement": source["statement"],
        "quote": source["quote"],
        "anchor": {"file": SOURCE_FULLTEXT, "startLine": 1081, "endLine": 1081},
        "applicableTo": source["applicable_to"],
        "requiredFacts": [
            {"key": "gan", "scope": {"layer": "本命", "pillar": "day"}, "predicateScope": [{"layer": "本命", "pillar": "day"}]},
            {"key": "liunian_gan_zhi", "scope": {"layer": "流年", "year": "selected"}, "predicateScope": [{"layer": "流年"}] * 6},
        ],
        "factSlicePolicy": "保留本命日柱 gan；仅传所选流年 year 的 liunian_gan_zhi。不得用异年戊干支补缺。",
        "applicableLayers": ["流年"],
        "unsupportedLayers": ["本命", "大运", "流月", "流日"],
        "semantics": {
            "satisfied": "仅确认本命甲日遇所选戊流年的原文示例入口；不推断救应或吉凶。",
            "notSatisfied": "已知日干或所选年干支不符；只否定本条字面例，不否定其它日犯岁君条件。",
            "unknown": "本命日干或所选年干支缺失时为信息不足；异年事实不能补缺。",
        },
        "caveats": source["caveats"],
        "exceptionsAndBreaks": source["caveats"],
        "conflictNotes": ["原 SANMINGTONGH-010 的有救、有情及 L1085–1087 后续条件仍未完成；本条不填补。"],
        "verification": {
            "verified": False,
            "fixtureSource": str(FACT_FIXTURE.relative_to(ROOT)),
            "positive": results["positive"],
            "negative": results["negative"],
            "wrongYear": results["wrongYear"],
            "unknownLuck": results["unknownLuck"],
            "boundary": boundary,
            "missingDay": day_boundary,
            "foreignYearGuard": "整袋含 2018 戊年会让 2017 错年误报；按所选年切片后为不满足。",
            "result": "三个真实盘边界与两种删键未知通过；只验证来源入口和三态，不证明作用或现实准确率。",
        },
        "export": {"artifact": "dist/rules/bazi.json", "classicsRev": SOURCE_REV, "sha256": EXPORT_SHA},
    }
    manifest["rules"].append(entry)
    assert manifest["rules"][:12] == base["rules"]
    assert len(manifest["rules"]) == 13
    assert all(item["verification"]["verified"] is False for item in manifest["rules"])
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = make_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {args.output} rules=13")


if __name__ == "__main__":
    main()
