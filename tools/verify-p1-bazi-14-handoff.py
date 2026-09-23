#!/usr/bin/env python3
"""Verify V5 adds exactly the narrow ZPR month entry to immutable V4."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/generate-p1-bazi-14-manifest.py"
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V5.json"
RULE_ID = "ZPR-P1-04"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-product-fixture", action="store_true")
    parser.add_argument("--product-root", type=Path, default=Path("/Users/sync/code/cosmic-fortune-lab"))
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("p1_14_generator", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected_bytes = (json.dumps(module.make_manifest(), ensure_ascii=False, indent=2) + "\n").encode()
    actual_bytes = MANIFEST.read_bytes()
    assert actual_bytes == expected_bytes, "V5 differs from reproducible generator output"
    manifest = json.loads(actual_bytes)
    previous = json.loads(module.BASE_PATH.read_text())
    assert hashlib.sha256(module.BASE_PATH.read_bytes()).hexdigest() == module.BASE_SHA
    assert manifest["previousHandoff"] == {
        "path": str(module.BASE_PATH.relative_to(ROOT)),
        "sha256": module.BASE_SHA,
        "ruleCount": 13,
    }
    assert manifest["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v5"
    assert manifest["semanticContractStatus"] == "pending"
    assert manifest["classicsRev"] == module.SOURCE_REV
    assert manifest["factFixture"]["sha256"] == module.FACT_SHA
    assert manifest["rules"][:13] == previous["rules"]
    assert len(manifest["rules"]) == len({rule["ruleId"] for rule in manifest["rules"]}) == 14
    assert all(rule["verification"]["verified"] is False for rule in manifest["rules"])
    assert manifest["topics"]["overview"]["ruleIds"] == [
        *previous["topics"]["overview"]["ruleIds"], RULE_ID,
    ]
    assert all(RULE_ID not in topic["ruleIds"] for name, topic in manifest["topics"].items() if name != "overview")
    assert all(manifest["topics"][name] == previous["topics"][name]
               for name in previous["topics"] if name != "overview")

    entry = manifest["rules"][-1]
    assert entry["ruleId"] == RULE_ID and entry["sourceRuleId"] == "ZPR-E-02"
    assert entry["role"] == "structural" and entry["primaryTopic"] == "overview"
    assert entry["secondaryTopics"] == [] and entry["applicableLayers"] == ["本命"]
    assert entry["unsupportedLayers"] == ["大运", "流年", "流月", "流日"]
    assert [item["key"] for item in entry["requiredFacts"]] == ["gan", module.FACT_KEY]
    assert entry["requiredFacts"][0]["scope"] == module.DAY_SCOPE
    assert entry["requiredFacts"][1]["scope"] == module.FACT_SCOPE
    assert [item["role"] for item in entry["supportingSources"]] == [
        "officer_killer_mapping", "single_qi_boundary", "jia_you_officer_example", "bing_zi_officer_example",
    ]
    source_lines = (ROOT / module.SOURCE_FULLTEXT).read_text().splitlines()
    for source in entry["supportingSources"]:
        anchor = source["anchor"]
        assert anchor["file"] == module.SOURCE_FULLTEXT
        assert source["quote"] in "\n".join(source_lines[anchor["startLine"] - 1:anchor["endLine"]])
    assert "generated bazi.json 当前仅有主锚" in entry["sourceDisplayPolicy"]
    assert {label: entry["verification"][label]["verdict"] for label in (
        "positive", "negative", "unknown", "missingStructuralFact",
        "conflictingStructuralFact", "foreignLayerGuard",
    )} == {
        "positive": "满足", "negative": "不满足", "unknown": "信息不足",
        "missingStructuralFact": "信息不足", "conflictingStructuralFact": "信息不足",
        "foreignLayerGuard": "信息不足",
    }
    assert entry["verification"]["allRealChartStates"] == {
        "满足": 4, "不满足": 7, "信息不足": 32,
    }

    source_rules = yaml.safe_load((ROOT / module.SOURCE_RULES).read_text())["rules"]
    source = [rule for rule in source_rules if rule["rule_id"] == RULE_ID]
    assert len(source) == 1 and source[0]["verified"] is False
    assert source[0]["applicable_to"] == entry["applicableTo"]
    original = next(rule for rule in json.loads((ROOT / "references/executable/ziping-zhenquan.json").read_text())["rules"]
                    if rule["id"] == "ZPR-E-02")
    assert original["rescue"] == "unimplemented" and original["verified"] is False

    if args.compare_product_fixture:
        product = args.product_root / "tests/fixtures/facts-sample.json"
        assert product.read_bytes() == module.FACT_FIXTURE.read_bytes(), "shared fixture bytes differ"

    print(
        f"PASS 14-rule V5 handoff; sha256={hashlib.sha256(actual_bytes).hexdigest()}; "
        f"classicsRev={module.SOURCE_REV}; fixtureSha256={module.FACT_SHA}; "
        f"exportSha256={module.EXPORT_SHA}"
    )


if __name__ == "__main__":
    main()
