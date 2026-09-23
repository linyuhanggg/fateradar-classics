"""Run with: python3 tools/test-ditiansui-051-shape-contract.py."""
from __future__ import annotations

import json
import unittest

from ditiansui_051_shape_contract import ROOT, evaluate_shape


class SourceShapeContractTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.cases = json.loads((ROOT / "tools/reports/facts-sample.json").read_text())["bazi"]

    @staticmethod
    def hypothetical(element: str, year: int = 2025) -> dict:
        return {
            "status": "adjudicated", "favoriteElement": element,
            "scope": {"layer": "大运", "year": year},
            "sourceRef": "counterfactual test input; no real adjudication",
            "route": "counterfactual test only", "evidenceMode": "counterfactual",
        }

    def test_real_birth_chart_with_hypothetical_favorite(self) -> None:
        # The chart and year-scoped 丁亥 luck pillar are real fixture facts.
        # Only the favorite-element decision is simulated; results cannot be
        # cited as this person's actual luck or as a finished 051 rule.
        facts = self.cases["caseFlowYear"]["facts"]
        listed = evaluate_shape(facts, 2025, "jiejiao", self.hypothetical("火"))
        self.assertEqual((listed["verdict"], listed["luckPillar"], listed["sourceLine"]),
                         ("满足", "丁亥", 13419))
        self.assertEqual(listed["evidenceMode"], "counterfactual")
        self.assertEqual(listed["effectVerdict"], "信息不足")

        unlisted = evaluate_shape(facts, 2025, "jiejiao", self.hypothetical("木"))
        self.assertEqual(unlisted["verdict"], "不满足")
        self.assertEqual(unlisted["reason"], "pair_not_listed_for_shape")
        self.assertEqual(unlisted["effectVerdict"], "信息不足")

    def test_real_birth_chart_without_favorite_decision_stays_unknown(self) -> None:
        facts = self.cases["caseP1_051_tiaohou_candidate"]["facts"]
        result = evaluate_shape(facts, 2025, "jiejiao", None)
        self.assertEqual((result["verdict"], result["luckPillar"]), ("信息不足", "癸酉"))
        self.assertEqual(result["reason"], "favorite_luck_element_not_adjudicated")
        self.assertEqual(result["effectVerdict"], "信息不足")

    def test_missing_selected_year_cannot_use_unscoped_or_another_year(self) -> None:
        facts = self.cases["caseFlowYear"]["facts"]
        result = evaluate_shape(facts, 2100, "jiejiao", self.hypothetical("火", 2100))
        self.assertEqual(result["verdict"], "信息不足")
        self.assertEqual(result["reason"], "selected_year_luck_pillar_missing_or_conflicting")

    def test_candidate_wrong_scope_and_conflicting_pillars_stay_unknown(self) -> None:
        facts = self.cases["caseFlowYear"]["facts"]
        candidate = {**self.hypothetical("火"), "status": "candidate"}
        self.assertEqual(evaluate_shape(facts, 2025, "jiejiao", candidate)["verdict"], "信息不足")
        wrong_year = self.hypothetical("火", 2024)
        self.assertEqual(evaluate_shape(facts, 2025, "jiejiao", wrong_year)["verdict"], "信息不足")
        conflict = facts + [{"key": "dayun_gan_zhi", "value": "甲申",
                             "scope": {"layer": "大运", "year": 2025}}]
        self.assertEqual(evaluate_shape(conflict, 2025, "jiejiao",
                                        self.hypothetical("火"))["verdict"], "信息不足")
        impossible = [{"key": "dayun_gan_zhi", "value": "甲丑",
                       "scope": {"layer": "大运", "year": 2025}}]
        self.assertEqual(evaluate_shape(impossible, 2025, "jiejiao",
                                        self.hypothetical("火"))["verdict"], "信息不足")

    def test_shape_specific_negative_is_not_effect_negative(self) -> None:
        facts = self.cases["caseFlowYear"]["facts"]
        result = evaluate_shape(facts, 2025, "gaitou", self.hypothetical("火"))
        self.assertEqual(result["verdict"], "不满足")
        self.assertEqual(result["effectVerdict"], "信息不足")

    def test_facsimile_corrected_entry(self) -> None:
        # Source-table unit case, not a real birth chart. Tests the documented
        # PDF-503 correction without changing the shared chart fixture.
        facts = [{"key": "dayun_gan_zhi", "value": "己卯",
                  "scope": {"layer": "大运", "year": 2025}}]
        result = evaluate_shape(facts, 2025, "jiejiao", self.hypothetical("土"))
        self.assertEqual((result["verdict"], result["sourceLine"]), ("满足", 13419))


if __name__ == "__main__":
    unittest.main()
