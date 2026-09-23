"""Run with: python3 tools/test-ditiansui-051-favorite-record.py."""
from __future__ import annotations

import json
import unittest

from ditiansui_051_favorite_record import (
    CONTRACT_ID,
    ROOT,
    favorite_element_verdict,
    validate_candidate_record,
)


ROUTE_ANCHORS = {
    "month_command_and_revealed_use": (2663, "先观月令所得何支"),
    "suppress_support_or_follow": (2942, "旺则抑之，如不可抑，反宜扶之"),
    "extreme_following": (2945, "盖旺极者抑之，抑之反激而有害"),
    "root_and_strength": (3209, "有如春木虽强，金太重而木亦危"),
    "favorite_and_hidden_use_branches": (7315, "日主元神厚者，以壬癸亥子为喜神"),
    "favorite_avoidance_enemy_idle_roles": (8998, "木有余，以火为喜神，以金为忌神"),
    "selected_year_reselection": (13402, "必先明一日主，配合七字"),
}


def anchor(line: int, cue: str, role: str = "任氏曰") -> dict:
    return {
        "file": "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md",
        "line": line,
        "cue": cue,
        "sourceRole": role,
    }


def candidate_record(*, record_status: str = "candidate", scope: dict | None = None) -> dict:
    scope = scope or {"layer": "流年", "year": 2025}
    all_anchors = [anchor(line, cue) for line, cue in ROUTE_ANCHORS.values()]
    route_reviews = {}
    for route_id, (line, _cue) in ROUTE_ANCHORS.items():
        route_reviews[route_id] = {
            "state": "unresolved",
            "reason": "当前材料只能证明该分支存在，尚未裁决其对本盘的适用与冲突优先级。",
            "sourceLines": [line],
            "evidenceRefs": [],
        }
    return {
        "contractId": CONTRACT_ID,
        "recordId": "test:cov3_bazi_1:wood",
        "chartRef": "cov3_bazi_1",
        "recordStatus": record_status,
        "scope": scope,
        "element": "木",
        "decision": {"status": "candidate", "disposition": "喜神", "sourceAnchors": [anchor(7315, ROUTE_ANCHORS["favorite_and_hidden_use_branches"][1])]},
        "sourceAnchors": all_anchors,
        "routeReviews": route_reviews,
        "routeConflict": {
            "status": "unresolved",
            "reason": "本命常格、从强/顺势、体用扶抑与所选年重取之间尚无来源裁决。",
            "competingRouteIds": ["suppress_support_or_follow", "extreme_following", "selected_year_reselection"],
        },
        "yearReview": {
            "status": "unresolved" if scope.get("layer") == "流年" else "not_applicable",
            "selectedYear": scope.get("year"),
            "natalBaselineRef": "test:cov3_bazi_1:natal",
            "evidenceRefs": [],
        } if scope.get("layer") == "流年" else {"status": "not_applicable"},
        "unresolvedItems": [
            "寅中甲木是否为用神",
            "旺衰及从强/顺势分支",
            "所选年份是否随岁运重取",
        ],
    }


class FavoriteRecordCandidateTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        fixture = json.loads((ROOT / "tools/reports/facts-sample.json").read_text())
        cls.charts = fixture["bazi"]

    def test_real_cov3_illustrative_overlap_remains_unknown(self) -> None:
        # It has 戊日寅月 and 甲 hidden, but the favorite record's premises are
        # not adjudicated. This is a real-date chart, not a favorite decision.
        chart = self.charts["cov3_bazi_1"]
        facts = chart["facts"]
        def values(key: str, scope: dict | None = None) -> set[str]:
            return {
                fact["value"] for fact in facts
                if fact.get("key") == key and (scope is None or fact.get("scope") == scope)
            }
        self.assertEqual(values("rizhu", {"layer": "本命", "pillar": "day"}), {"戊"})
        self.assertEqual(values("yueling", {"layer": "本命", "pillar": "month"}), {"寅"})
        self.assertEqual(values("rizhu_strength", {"layer": "本命"}), {"极强"})
        self.assertEqual(values("tiaohou_candidate_gan", {"layer": "本命"}), {"丙", "甲", "癸"})
        self.assertFalse(values("favorite_luck_element_decision_record"))
        record = candidate_record()
        result = favorite_element_verdict(record, 2025, "木")
        self.assertEqual(result, {"favoriteElementVerdict": "信息不足", "effectVerdict": "信息不足"})

    def test_real_tiaohou_candidates_and_effective_luck_do_not_become_favorite(self) -> None:
        facts = self.charts["caseP1_051_tiaohou_candidate"]["facts"]
        candidate_gans = {
            fact["value"] for fact in facts
            if fact.get("key") == "tiaohou_candidate_gan"
            and fact.get("scope") == {"layer": "本命"}
        }
        selected_luck = {
            fact["value"] for fact in facts
            if fact.get("key") == "dayun_gan_zhi"
            and fact.get("scope") == {"layer": "大运", "year": 2025}
        }
        self.assertEqual(candidate_gans, {"壬", "戊"})
        self.assertEqual(selected_luck, {"癸酉"})
        record = candidate_record()
        record["chartRef"] = "caseP1_051_tiaohou_candidate"
        record["element"] = "水"
        record["decision"]["disposition"] = "喜神"
        self.assertEqual(favorite_element_verdict(record, 2025, "水")["favoriteElementVerdict"], "信息不足")

    def test_candidate_value_cannot_be_promoted_to_favorite(self) -> None:
        record = candidate_record()
        record["decision"]["disposition"] = "喜神"
        report = validate_candidate_record(record)
        self.assertTrue(report["valid"])
        self.assertFalse(report["structurallyAdjudicated"])
        self.assertEqual(favorite_element_verdict(record, 2025, "木")["favoriteElementVerdict"], "信息不足")

    def test_selected_year_requires_exact_scope_and_natal_baseline(self) -> None:
        record = candidate_record(scope={"layer": "流年", "year": 2025})
        self.assertEqual(favorite_element_verdict(record, 2024, "木")["favoriteElementVerdict"], "信息不足")
        record["yearReview"]["selectedYear"] = 2024
        report = validate_candidate_record(record)
        self.assertFalse(report["valid"])
        self.assertTrue(any("selectedYear" in issue for issue in report["errors"]))

    def test_natal_baseline_cannot_be_used_as_selected_year_decision(self) -> None:
        record = candidate_record(scope={"layer": "本命"})
        self.assertTrue(validate_candidate_record(record)["valid"])
        self.assertEqual(favorite_element_verdict(record, 2025, "木")["favoriteElementVerdict"], "信息不足")

    def test_missing_route_or_modern_proxy_route_is_rejected(self) -> None:
        record = candidate_record()
        del record["routeReviews"]["extreme_following"]
        record["routeReviews"]["modern_ratio_strength_score"] = {
            "state": "applies", "reason": "modern test proxy", "sourceLines": [3209],
            "evidenceRefs": ["test-only:proxy"],
        }
        report = validate_candidate_record(record)
        self.assertFalse(report["valid"])
        self.assertTrue(any("unsupported route ID" in issue for issue in report["errors"]))
        self.assertTrue(any("route_reviews_missing" in blocker for blocker in report["blockers"]))

    def test_source_anchor_must_match_cited_edition_line(self) -> None:
        record = candidate_record()
        record["sourceAnchors"][0]["cue"] = "a modern strength score determines the favorite element"
        report = validate_candidate_record(record)
        self.assertFalse(report["valid"])
        self.assertTrue(any("does not occur at the cited line" in issue for issue in report["errors"]))

    def test_adjudicated_label_is_blocked_while_route_conflict_is_unresolved(self) -> None:
        record = candidate_record(record_status="adjudicated")
        record["decision"]["status"] = "adjudicated"
        record["decision"]["sourceAnchors"] = [anchor(7315, ROUTE_ANCHORS["favorite_and_hidden_use_branches"][1])]
        report = validate_candidate_record(record)
        self.assertTrue(report["valid"])
        self.assertFalse(report["structurallyAdjudicated"])
        self.assertIn("route_conflict_unresolved", report["blockers"])
        self.assertIn("adjudicated_record_has_unresolved_route", report["blockers"])

    def test_candidate_unknown_is_not_negative_and_effect_never_emerges(self) -> None:
        # An explicit candidate “仇神” is still not an adjudicated negative.
        record = candidate_record()
        record["decision"]["disposition"] = "仇神"
        result = favorite_element_verdict(record, 2025, "木")
        self.assertEqual(result["favoriteElementVerdict"], "信息不足")
        self.assertEqual(result["effectVerdict"], "信息不足")

    def test_supported_classifications_are_closed_domain(self) -> None:
        record = candidate_record()
        record["decision"]["disposition"] = "有利五行"
        report = validate_candidate_record(record)
        self.assertFalse(report["valid"])
        self.assertTrue(any("source roles or 信息不足" in issue for issue in report["errors"]))

    def test_malformed_json_types_are_rejected_without_crashing(self) -> None:
        record = candidate_record()
        record["recordStatus"] = []
        record["element"] = []
        record["decision"]["disposition"] = []
        record["routeConflict"]["status"] = []
        record["routeReviews"]["month_command_and_revealed_use"]["state"] = []
        record["sourceAnchors"][0]["sourceRole"] = []
        report = validate_candidate_record(record)
        self.assertFalse(report["valid"])
        self.assertEqual(favorite_element_verdict(record, 2025, [])["favoriteElementVerdict"], "信息不足")


if __name__ == "__main__":
    unittest.main()
