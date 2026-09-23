#!/usr/bin/env python3
"""Verify the V7 candidate scope correction against pinned V6 and facts."""
from __future__ import annotations

import hashlib
import importlib.util
import json
import subprocess
import sys
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/generate-p1-bazi-v7-manifest.py"
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260924_V7.json"
V6_PATH = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V6.json"
V6_SHA = "39e53a6c5c3693334209d80eb2f9e9002339fff2117b64f1988d6f2a02f344a6"
RULE_ID = "ZPR-P1-06"


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def main() -> None:
    v6_bytes = V6_PATH.read_bytes()
    assert sha256(v6_bytes) == V6_SHA, "historical V6 changed"
    v6 = json.loads(v6_bytes)
    actual_bytes = MANIFEST.read_bytes()
    manifest = json.loads(actual_bytes)
    generator = load_module(GENERATOR, "p1_v7_generator")
    expected = generator.make_manifest()
    expected_bytes = (json.dumps(expected, ensure_ascii=False, indent=2) + "\n").encode()
    assert actual_bytes == expected_bytes, "V7 differs from locked V6, source schema, or fixture"

    assert manifest["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v7"
    assert manifest["generatedAt"] == "2026-09-24"
    assert manifest["semanticContractStatus"] == "pending"
    assert manifest["handoffStatus"] == "candidate_pending_product_import"
    assert manifest["classicsRev"] == v6["classicsRev"]
    assert manifest["sourceHeadAtAudit"] == generator.AUDIT_HEAD
    assert manifest["previousHandoff"] == {
        "path": str(V6_PATH.relative_to(ROOT)), "sha256": V6_SHA, "ruleCount": 15,
    }
    assert manifest["rules"][:14] == v6["rules"][:14]
    assert len(manifest["rules"]) == len({rule["ruleId"] for rule in manifest["rules"]}) == 15
    assert all(rule["verification"]["verified"] is False for rule in manifest["rules"])
    assert manifest["topics"] == v6["topics"]
    assert manifest["factFixture"] == v6["factFixture"]

    old = v6["rules"][-1]
    entry = manifest["rules"][-1]
    assert old["ruleId"] == entry["ruleId"] == RULE_ID
    for field in (
        "status", "role", "sourceRuleId", "statement", "quote", "anchor",
        "supportingSources", "sourceEntryOutputs", "applicableLayers", "unsupportedLayers",
        "export",
    ):
        assert entry[field] == old[field], field
    assert entry["applicableTo"] == {"all_of": generator.PREDICATES}
    assert [fact["key"] for fact in entry["requiredFacts"]] == [
        "gan", "zhi", "yueling", "natal_yin_simple_hidden_exposure_pattern",
    ]
    assert entry["sourceEntryOutputs"] == old["sourceEntryOutputs"]
    assert entry["verification"]["verified"] is False
    assert entry["verification"]["allRealChartStates"] == {
        "满足": 2, "不满足": 46, "信息不足": 2,
    }
    for label in (
        "positive", "secondPositive", "negative", "nonYinMonthBranchNegative",
        "nonYinMonthOrderNegative", "tripleExposureUnknown", "meetingUnknown",
        "missingStructuralFact", "missingMonthBranch", "missingMonthOrder",
        "conflictingStructuralFact", "conflictingMonthBranch", "conflictingMonthOrder",
        "foreignLayerGuard",
    ):
        assert label in entry["verification"]
    assert entry["verification"]["nonYinMonthBranchNegative"]["verdict"] == "不满足"
    assert entry["verification"]["nonYinMonthOrderNegative"]["verdict"] == "不满足"
    assert entry["verification"]["tripleExposureUnknown"]["verdict"] == "信息不足"
    assert entry["verification"]["meetingUnknown"]["verdict"] == "信息不足"
    assert manifest["scopeCorrection"]["priorV6Counts"] == {
        "满足": 2, "不满足": 44, "信息不足": 4,
    }
    assert manifest["scopeCorrection"]["candidateV7Counts"] == {
        "满足": 2, "不满足": 46, "信息不足": 2,
    }
    assert manifest["exportState"]["candidateOnly"] is True
    assert manifest["exportState"]["sourceRuleYamlChanged"] is False
    assert manifest["exportState"]["classicsDistChanged"] is False

    source_rev = manifest["classicsRev"]
    rules_yaml = "references/books/bazi/ziping-zhenquan/rules.yaml"
    source_rules = subprocess.check_output(["git", "show", f"{source_rev}:{rules_yaml}"], cwd=ROOT)
    assert (ROOT / rules_yaml).read_bytes() == source_rules
    original_rule = next(rule for rule in yaml.safe_load(source_rules)["rules"]
                         if rule["rule_id"] == RULE_ID)
    assert original_rule["verified"] is False
    assert original_rule["applicable_to"] == {
        "all_of": [
            {"key": "gan", "value": "辛", "scope": generator.DAY_SCOPE},
            {
                "key": "natal_yin_simple_hidden_exposure_pattern",
                "value": "甲丙",
                "scope": generator.MONTH_SCOPE,
            },
        ]
    }
    executable_path = "references/executable/ziping-zhenquan.json"
    executable_bytes = subprocess.check_output(
        ["git", "show", f"{source_rev}:{executable_path}"], cwd=ROOT
    )
    executable_rule = next(
        rule for rule in json.loads(executable_bytes)["rules"] if rule["id"] == "ZPR-E-02"
    )
    assert executable_rule["rescue"] == "unimplemented"
    assert executable_rule["verified"] is False
    exported = ROOT / entry["export"]["artifact"]
    assert sha256(exported.read_bytes()) == old["export"]["sha256"]

    print(
        "PASS V7 candidate; "
        f"v6Sha256={V6_SHA}; v7Sha256={sha256(actual_bytes)}; "
        f"states={entry['verification']['allRealChartStates']}; "
        f"fixtureSha256={manifest['factFixture']['sha256']}"
    )


if __name__ == "__main__":
    main()
