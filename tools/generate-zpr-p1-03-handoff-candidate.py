#!/usr/bin/env python3
"""Build a review-only P1 handoff for ZPR-P1-03, without changing P1 acceptance."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
RULES = ROOT / "references/books/bazi/ziping-zhenquan/rules.yaml"
EXPORTER = ROOT / "tools/export-rules.py"
EVALUATOR = ROOT / "tools/eval-predicates.py"
PREDICATE_LANGUAGE = ROOT / "tools/predicate_lang.py"
FULLTEXT = ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md"
FIXTURE = ROOT / "tools/reports/facts-sample.json"
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json"
DEFAULT_OUTPUT = ROOT / "docs/closeout/ZPR_P1_03_HANDOFF_CANDIDATE_20260923.json"


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    assert spec.loader is not None
    spec.loader.exec_module(module)
    return module


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def without(facts: list[dict], key: str, pillar: str) -> list[dict]:
    return [
        fact for fact in facts
        if not (fact["key"] == key and fact.get("scope", {}).get("layer") == "本命"
                and fact.get("scope", {}).get("pillar") == pillar)
    ]


def build() -> dict:
    source_rules = {r["rule_id"]: r for r in yaml.safe_load(RULES.read_text())["rules"]}
    rule = source_rules["ZPR-P1-03"]
    assert rule["applicable_to"] == source_rules["ZPR-P1-01"]["applicable_to"]
    assert rule["candidate_output"]["entryId"] == "ZPR-P1-01"
    assert rule["verified"] is False
    exporter = load_module(EXPORTER, "export_rules")
    evaluator = load_module(EVALUATOR, "eval_predicates")
    exported = exporter.convert(rule, art="bazi", title="子平真诠", slug_path="bazi/ziping-zhenquan")
    assert exported["candidateOutput"] == rule["candidate_output"]

    fixture = json.loads(FIXTURE.read_text())["bazi"]
    examples = [
        ("positive", "caseP1_ZPR_01_wu_only", "满足"),
        ("coexisting_entry", "caseP1_ZPR_01_wu_gui_both", "满足"),
        ("negative", "caseP1_ZPR_01_no_wu", "不满足"),
        ("different_entry", "caseP1_ZPR_02_shen_zi", "不满足"),
    ]
    verification = []
    for role, name, expected in examples:
        case = fixture[name]
        verdict = evaluator.evaluate(rule, case["facts"])["verdict"]
        assert verdict == expected, (name, verdict)
        verification.append({
            "role": role,
            "case": name,
            "label": case["label"],
            "verdict": verdict,
            "candidateOutput": rule["candidate_output"] if verdict == "满足" else None,
        })
    projections = []
    for name, key, pillar in (
        ("caseP1_ZPR_01_wu_only", "gan", "year"),
        ("caseP1_ZPR_01_wu_only", "canggan", "month"),
        ("caseP1_ZPR_01_no_wu", "gan", "year"),
    ):
        verdict = evaluator.evaluate(rule, without(fixture[name]["facts"], key, pillar))["verdict"]
        assert verdict == "信息不足", (name, key, pillar, verdict)
        projections.append({
            "case": name,
            "removeScoped": {"key": key, "scope": {"layer": "本命", "pillar": pillar}},
            "verdict": verdict,
            "candidateOutput": None,
        })

    current_manifest = json.loads(MANIFEST.read_text())
    assert current_manifest["semanticContractStatus"] == "pending"
    assert "ZPR-P1-03" not in {r["ruleId"] for r in current_manifest["rules"]}
    source_chain = exported["candidateSources"]
    assert [(source["role"], source["anchor"]["startLine"]) for source in source_chain] == [
        ("direction_category", 328), ("entry", 544), ("coexisting_entries", 548)
    ]
    return {
        "manifestVersion": "fateradar-p1-bazi-topic-handoff-candidate-v1",
        "reviewStatus": "proposed_not_importable",
        "art": "bazi",
        "semanticContractStatus": "pending",
        "existingManifest": {
            "path": "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260921.json",
            "sha256AtAudit": sha256(MANIFEST),
            "classicsRev": current_manifest["classicsRev"],
            "acceptedRuleCount": len(current_manifest["rules"]),
        },
        "sourceFiles": {
            "rulesYamlSha256": sha256(RULES),
            "exporterSha256": sha256(EXPORTER),
            "evaluatorSha256": sha256(EVALUATOR),
            "predicateLanguageSha256": sha256(PREDICATE_LANGUAGE),
            "fulltextSha256": sha256(FULLTEXT),
        },
        "sourceChain": source_chain,
        "factFixture": {"path": "tools/reports/facts-sample.json", "sha256": sha256(FIXTURE), "baziCaseCount": len(fixture)},
        "topicProposal": {
            "primaryTopic": "overview",
            "secondaryTopics": [],
            "role": "source_classification",
            "notTopicEffects": ["personality", "career", "wealth", "relationship", "health"],
        },
        "consumption": {
            "kind": "RuleEvaluation.output_metadata",
            "identity": "ruleId + candidateOutput.entryId",
            "multipleEntries": "保留每条规则与入口的独立记录；同盘候选不折叠为单个 geju.mode。",
            "conflict": "同一入口若有相冲方向，标待核而不任选其一；本合同没有统一取用裁决。",
            "satisfied": "仅规则满足时附 candidateOutput；它是来源方向候选，不是本格喜忌或主题结果。",
            "not_satisfied": "保留规则不满足，不附方向；只否定这条入口。",
            "unknown": "保留规则信息不足，不附方向；缺柱位不得作为反证。",
            "factKey": None,
            "feedbackToApplicableTo": False,
        },
        "rule": exported,
        "verification": verification,
        "missingInputProjections": projections,
        "activationRequires": [
            "Product 明确允许新规则 ID，钉住含本合同的 Classics 提交并重导出 bazi 规则；旧 P1 manifest 不会自动接纳本候选。",
            "Product 对外展示本候选时须并列保留 candidateSources 的 L328 分类、L544 入口与 L548 并用锚点；不能只引用主 anchor L328。",
            "Product 仅在 overview 的来源结构证据中显示方向候选；保留 ZPR-E-02 为信息不足及六主题作用语义 pending。",
            "Product 测试入口多值并存、反例不附方向与缺项未知，且不得从 candidateOutput 生成自身 applicableTo 输入。",
        ],
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    payload = json.dumps(build(), ensure_ascii=False, indent=2) + "\n"
    args.output.write_text(payload)
    print(args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
