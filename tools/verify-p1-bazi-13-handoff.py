#!/usr/bin/env python3
"""Verify the formal 13-rule handoff and the narrow 010A source contract."""

from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
GENERATOR = ROOT / "tools/generate-p1-bazi-13-manifest.py"
MANIFEST = ROOT / "docs/closeout/P1_BAZI_TOPIC_MANIFEST_20260923_V4.json"
RULE_ID = "SANMINGTONGH-P1-010A"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--compare-product-fixture", action="store_true")
    parser.add_argument("--product-root", type=Path, default=Path("/Users/sync/code/cosmic-fortune-lab"))
    args = parser.parse_args()

    spec = importlib.util.spec_from_file_location("p1_13_generator", GENERATOR)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    expected = (json.dumps(module.make_manifest(), ensure_ascii=False, indent=2) + "\n").encode()
    actual = MANIFEST.read_bytes()
    assert actual == expected, "v4 manifest differs from reproducible generator output"
    manifest = json.loads(actual)
    assert manifest["manifestVersion"] == "fateradar-p1-bazi-topic-handoff-v4"
    assert manifest["semanticContractStatus"] == "pending"
    assert manifest["classicsRev"] == module.SOURCE_REV
    assert len(manifest["rules"]) == len({item["ruleId"] for item in manifest["rules"]}) == 13
    assert all(item["verification"]["verified"] is False for item in manifest["rules"])
    previous = json.loads(module.BASE_PATH.read_text())
    assert manifest["rules"][:12] == previous["rules"]
    assert manifest["topics"]["overview"]["ruleIds"][-1] == RULE_ID
    assert all(RULE_ID not in value["ruleIds"] for key, value in manifest["topics"].items() if key != "overview")
    rule = manifest["rules"][-1]
    assert rule["sourceRuleId"] == "SANMINGTONGH-010"
    assert rule["role"] == "structural" and rule["applicableLayers"] == ["流年"]
    assert rule["unsupportedLayers"] == ["本命", "大运", "流月", "流日"]
    assert [item["key"] for item in rule["requiredFacts"]] == ["gan", "liunian_gan_zhi"]
    assert rule["requiredFacts"][0]["scope"] == {"layer": "本命", "pillar": "day"}
    assert rule["requiredFacts"][1]["scope"] == {"layer": "流年", "year": "selected"}
    assert {key: rule["verification"][key]["verdict"] for key in
            ("positive", "negative", "wrongYear", "unknownLuck", "boundary", "missingDay")} == {
                "positive": "满足", "negative": "不满足", "wrongYear": "不满足",
                "unknownLuck": "满足", "boundary": "信息不足", "missingDay": "信息不足",
            }
    assert "不推断救应或吉凶" in rule["semantics"]["satisfied"]
    source = yaml.safe_load((ROOT / module.SOURCE_RULES).read_text())["rules"]
    original = next(item for item in source if item["rule_id"] == "SANMINGTONGH-010")
    assert original["applicable_to"] == [] and original["verified"] is False
    current_export = json.loads(module.EXPORT_PATH.read_text())
    old_export = [item for item in current_export if item["ruleId"] != RULE_ID]
    old_bytes = (json.dumps(old_export, ensure_ascii=False, indent=2) + "\n").encode()
    assert hashlib.sha256(old_bytes).hexdigest() == previous["rules"][-1]["export"]["sha256"]
    old = {item["ruleId"]: item for item in old_export}
    current = {item["ruleId"]: item for item in current_export}
    assert len(old) == 450 and len(current) == 451
    assert set(current) - set(old) == {RULE_ID}
    assert all(current[key] == value for key, value in old.items())
    if args.compare_product_fixture:
        product = args.product_root / "tests/fixtures/facts-sample.json"
        assert product.exists(), product
        assert product.read_bytes() == module.FACT_FIXTURE.read_bytes(), "shared fixture bytes differ"
    print(
        f"PASS 13-rule handoff; sha256={hashlib.sha256(actual).hexdigest()}; "
        f"classicsRev={module.SOURCE_REV}; exportSha256={module.EXPORT_SHA}"
    )


if __name__ == "__main__":
    main()
