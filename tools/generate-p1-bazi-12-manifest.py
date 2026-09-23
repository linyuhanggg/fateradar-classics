#!/usr/bin/env python3
"""Extend the locked 11-rule P1 handoff with the literal 甲子岁运 companion."""

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
BASE_PATH = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json"
BASE_SHA = "dd2293b4bee38edf4aea3020769c2f4be8f09419b94135abd7d7ca12e20a5e7c"
SOURCE_REV = "a6ab65a182c1936a1938c0e1a1ea15bd2ea2e6f9"
SOURCE_RULES = "references/books/bazi/sanming-tonghui/rules.yaml"
VOCAB = "references/vocab/fact-vocab.json"
BAZI_EXPORT_SHA = "781e5c5f31dfe4747f06e5f9fce758e89eed136166987c5c233cc43f66a6a1b2"
CANDIDATE_PATH = ROOT / "tools/reports/p1-bazi-20260922/sanming-011-literal-companion-candidate.json"
FIXTURE_PATH = ROOT / "tools/reports/p1-bazi-20260922/sanming-011-literal-chart-fixture.json"
OUTPUT = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923.json"
EXPECTED = {
    "literal_jiazi_positive": (1984, "满足"),
    "literal_jiazi_wrong_luck": (1984, "不满足"),
    "literal_jiazi_no_active_luck": (1984, "信息不足"),
    "literal_jiazi_prior_year": (1983, "不满足"),
}


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def committed_bytes(path: str) -> bytes:
    return subprocess.check_output(["git", "show", f"{SOURCE_REV}:{path}"], cwd=ROOT)


def evaluation(evaluator, rule: dict, case: dict) -> dict:
    year = case["selectedYear"]
    facts = [fact for fact in case["facts"] if fact.get("scope", {}).get("year") == year]
    output = evaluator.evaluate(rule, facts)
    return {
        "case": case["id"],
        "year": year,
        "factCount": len(facts),
        "verdict": output["verdict"],
        "confidence": output.get("confidence"),
        "factCoverage": output.get("fact_coverage"),
        "missingFactKeys": output.get("missing_fact_keys", []),
    }


def make_manifest() -> dict:
    base_bytes = BASE_PATH.read_bytes()
    assert sha256(base_bytes) == BASE_SHA
    base = json.loads(base_bytes)
    assert base["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v2"
    assert base["semanticContractStatus"] == "pending" and len(base["rules"]) == 11
    assert len({rule["ruleId"] for rule in base["rules"]}) == 11

    candidate = json.loads(CANDIDATE_PATH.read_text())
    fixture_bytes = FIXTURE_PATH.read_bytes()
    assert candidate["baseHandoff"]["sha256"] == BASE_SHA
    assert candidate["fixture"]["sha256"] == sha256(fixture_bytes)
    assert candidate["rule"]["verified"] is False
    cases = json.loads(fixture_bytes)["cases"]
    assert set(cases) == set(EXPECTED)

    source_bytes = committed_bytes(SOURCE_RULES)
    vocab_bytes = committed_bytes(VOCAB)
    assert (ROOT / SOURCE_RULES).read_bytes() == source_bytes
    source_rules = yaml.safe_load(source_bytes)["rules"]
    source = next(rule for rule in source_rules if rule["rule_id"] == "SANMINGTONGH-P1-011A")
    assert sum(rule["rule_id"] == source["rule_id"] for rule in source_rules) == 1
    assert source["verified"] is False
    candidate_rule = candidate["rule"]
    assert source["statement"] == candidate_rule["statement"]
    assert source["quote"] == candidate_rule["quote"]
    assert source["applicable_to"] == candidate_rule["applicableTo"]
    assert source["anchor"] == {
        "file": candidate_rule["anchor"]["file"],
        "start_line": candidate_rule["anchor"]["startLine"],
        "end_line": candidate_rule["anchor"]["endLine"],
    }
    source_line = (ROOT / source["anchor"]["file"]).read_text().splitlines()[1083]
    assert source["quote"] in source_line
    assert "甲子日見甲子太嵗" in source_line
    assert candidate_rule["primaryTopic"] == "overview"
    assert candidate_rule["secondaryTopics"] == []
    assert candidate_rule["role"] == "structural"
    assert candidate_rule["requiredFacts"] == [
        {"key": "liunian_gan_zhi", "scope": {"layer": "流年", "year": "selected"}},
        {"key": "suiyun_binglin", "scope": {"layer": "流年", "year": "selected"}},
    ]

    spec = importlib.util.spec_from_file_location("p1_evaluator", ROOT / "tools/eval-predicates.py")
    assert spec and spec.loader
    evaluator = importlib.util.module_from_spec(spec)
    sys.modules["p1_evaluator"] = evaluator
    spec.loader.exec_module(evaluator)
    results = {}
    for case_id, (year, verdict) in EXPECTED.items():
        case = {**cases[case_id], "id": case_id}
        result = evaluation(evaluator, source, case)
        assert result["year"] == year and result["verdict"] == verdict, result
        results[case_id] = result
    assert results["literal_jiazi_no_active_luck"]["missingFactKeys"] == ["suiyun_binglin"]

    foreign = next(f for f in cases["literal_jiazi_positive"]["facts"] if f["key"] == "suiyun_binglin")
    contaminated = copy.deepcopy(cases["literal_jiazi_no_active_luck"])
    contaminated["facts"].append({**foreign, "scope": {"layer": "流年", "year": 1983}})
    assert evaluator.evaluate(source, contaminated["facts"])["verdict"] == "满足"
    assert evaluation(evaluator, source, {**contaminated, "id": "foreign_year_guard"})["verdict"] == "信息不足"

    manifest = copy.deepcopy(base)
    manifest["manifestVersion"] = "fateradar-p1-bazi-topic-handoff-v3"
    manifest["generatedBy"] = "tools/generate-p1-bazi-12-manifest.py"
    manifest["classicsRev"] = SOURCE_REV
    manifest["sourceHeadAtAudit"] = SOURCE_REV
    manifest["previousHandoff"] = {"path": str(BASE_PATH.relative_to(ROOT)), "sha256": BASE_SHA, "ruleCount": 11}
    manifest["sourceFingerprint"]["sanmingRulesYamlSha256"] = sha256(source_bytes)
    manifest["sourceFingerprint"]["factVocabSha256"] = sha256(vocab_bytes)
    manifest["supplementalFactFixture"] = {
        "path": str(FIXTURE_PATH.relative_to(ROOT)),
        "sha256": sha256(fixture_bytes),
        "caseCount": 4,
        "producer": "cosmic buildBazi(..., selectedYear, undefined, {buildVertical:false})",
        "replay": "python3 tools/verify-p1-bazi-12-handoff.py --replay-product",
    }
    manifest["contract"]["layerPolicy"] = (
        "当前 10 条本命规则只适用于本命；YUANHAIZIPIN-YR-03 和 SANMINGTONGH-P1-011A 只适用于所选流年。"
        "两条流年规则求值前必须按 scope.year=selectedYear 筛选，未选年与缺事实均保留信息不足。"
    )
    manifest["topics"]["overview"]["ruleIds"].append(source["rule_id"])
    manifest["topics"]["overview"]["requiredFactKeys"].extend(["liunian_gan_zhi", "suiyun_binglin"])
    manifest["statusSummary"]["adopted"] = sorted([*manifest["statusSummary"]["adopted"], source["rule_id"]])

    entry = {
        "ruleId": source["rule_id"], "art": "bazi", "book": "bazi/sanming-tonghui",
        "primaryTopic": "overview", "secondaryTopics": [],
        "status": "adopted_as_provisional_evidence", "role": "structural",
        "sourceRuleId": "SANMINGTONGH-011", "statement": source["statement"],
        "quote": source["quote"], "anchor": candidate_rule["anchor"],
        "applicableTo": source["applicable_to"],
        "requiredFacts": [
            {**item, "predicateScope": [{"layer": "流年"}]}
            for item in candidate_rule["requiredFacts"]
        ],
        "factSlicePolicy": candidate_rule["factSlicePolicy"],
        "applicableLayers": ["流年"], "unsupportedLayers": ["本命", "大运", "流月", "流日"],
        "semantics": {
            "satisfied": "仅所选年甲子流年且有效大运也是甲子时，确认原文字面形态；不推断吉凶。",
            "notSatisfied": "该年已知流年或有效大运不符甲子组合；只否定本条字面例。",
            "unknown": "缺所选年流年或有效大运时为信息不足；异年事实不能补缺。",
        },
        "caveats": source["caveats"], "exceptionsAndBreaks": source["caveats"],
        "conflictNotes": ["SANMINGTONGH-011 的刃杀／财官印绶分类合同仍 pending；本条不填补。"],
        "verification": {
            "verified": False, "fixtureSource": str(FIXTURE_PATH.relative_to(ROOT)),
            "positive": results["literal_jiazi_positive"],
            "negative": results["literal_jiazi_wrong_luck"],
            "boundary": results["literal_jiazi_no_active_luck"],
            "wrongYear": results["literal_jiazi_prior_year"],
            "foreignYearGuard": "异年并临事实未过滤会误报满足；按所选年过滤后保持信息不足。",
            "result": "四个真盘年与污染门禁通过；只验证来源形态和三态，不证明现实预测准确率。",
        },
        "export": {"artifact": "dist/rules/bazi.json", "classicsRev": SOURCE_REV, "sha256": BAZI_EXPORT_SHA},
    }
    manifest["rules"].append(entry)
    assert manifest["rules"][:11] == base["rules"]
    assert len(manifest["rules"]) == 12
    assert all(item["verification"]["verified"] is False for item in manifest["rules"])
    assert manifest["semanticContractStatus"] == "pending"
    return manifest


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    args = parser.parse_args()
    result = make_manifest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n")
    print(f"wrote {args.output} rules=12 fixtureCases=4")


if __name__ == "__main__":
    main()
