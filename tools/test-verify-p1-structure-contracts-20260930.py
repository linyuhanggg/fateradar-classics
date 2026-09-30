"""Regression and rejection tests; all mutations stay in memory."""
from __future__ import annotations

import copy
import hashlib
import importlib.util
import json
from pathlib import Path
import sys
import unittest

sys.dont_write_bytecode = True
SPEC = importlib.util.spec_from_file_location(
    "structure_verifier", Path(__file__).with_name("verify-p1-structure-contracts-20260930.py"))
V = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(V)
IDS = ["SANMINGTONGH-015-L1-STRUCT", "SMTH-CHONGJI-ZIWU-L1-STRUCT",
       "SMTH-CHONGJI-MAOYOU-L1-STRUCT", "ZPR-P1-01-L1-STRUCT"]


class StructureContractsTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.original = json.loads(V.CONTRACTS.read_text(encoding="utf-8"))

    def setUp(self):
        self.contract = copy.deepcopy(self.original)

    def case(self, name):
        return next(c for c in self.contract["syntheticCases"] if c["id"] == name)

    def evaluate(self, name):
        return V.evaluate_chart(self.case(name)["facts"], self.contract)

    def pending(self):
        c = copy.deepcopy(self.original)
        c["status"], c["verified"], c["fixture"] = "pending_product_fixture", False, None
        return c

    def test_baseline_pending(self):
        self.assertEqual(V.verify(self.pending())["productFixture"], "pending")

    def test_committed_contract_matches_its_declared_state(self):
        report = V.verify(self.contract)
        if self.contract["status"] == "accepted":
            self.assertEqual(report["productFixture"], "verified")
            self.assertEqual(report["productRows"], self.contract["fixture"]["rowCount"])
        else:
            self.assertEqual(report["productFixture"], "pending")

    def test_a_changed_quote_rejected(self):
        self.contract["anchors"][0]["quote"] += "錯"
        with self.assertRaisesRegex(V.VerificationError, "anchor"):
            V.verify(self.contract)

    def test_b_chongji_statement_must_not_cross_1283(self):
        anchor = next(a for a in self.contract["anchors"] if a["id"] == "smth-chongji-definition")
        anchor["endLine"] = 1284
        with self.assertRaisesRegex(V.VerificationError, "chongji"):
            V.verify(self.contract)

    def test_c_two_triad_letters_missing_time_is_unknown(self):
        row = self.evaluate("sanhe_two_time_missing")["results"][IDS[0]]
        self.assertEqual(row["state"], "unknown")
        self.assertEqual(row["unknownPillars"], ["time"])
        self.assertEqual(row["missingKeys"], [{"key": "zhi", "pillar": "time"}])

    def test_d_three_hidden_stems_are_not_a_conflict(self):
        row = self.evaluate("R2_hour_wu")["results"][IDS[3]]
        self.assertEqual(row["state"], "satisfied")
        self.assertEqual(row["positions"], {"戊": ["time"]})
        self.assertNotIn("conflicts", row)

    def test_e_branch_conflict_overrides_satisfaction(self):
        rows = self.evaluate("conflict_day_zhi")["results"]
        for rid in IDS[:3]:
            self.assertEqual(rows[rid]["state"], "unknown")
            self.assertEqual(rows[rid]["conflicts"], [{"key": "zhi", "pillar": "day", "values": ["子", "酉"]}])
        self.assertEqual(rows[IDS[3]]["state"], "satisfied")

    def test_f_accepted_or_verified_needs_fixture(self):
        for field, value in (("status", "accepted"), ("verified", True)):
            with self.subTest(field=field):
                c = self.pending()
                c[field] = value
                with self.assertRaisesRegex(V.VerificationError, "fixture"):
                    V.verify(c)

    def test_g_cap_keeps_first_two_and_exports_third(self):
        row = self.evaluate("R1_cap")
        self.assertEqual(row["display"], IDS[:2])
        third = row["results"][IDS[3]]
        self.assertEqual(third["state"], "satisfied")
        self.assertFalse(third["displayed"])
        self.assertEqual(third["notDisplayedReason"], "display_cap")

    def test_h_forbidden_copy_rejected_including_fold(self):
        for slot in ("statement", "fold"):
            with self.subTest(slot=slot):
                c = copy.deepcopy(self.original)
                c["rules"][0]["copy"]["water"][slot] += "取用"
                with self.assertRaisesRegex(V.VerificationError, "copy|content"):
                    V.verify(c)

    def test_i_source_rule_id_table_is_fixed(self):
        self.contract["rules"][1]["sourceRuleId"] = "DITIANSUICHA-032"
        with self.assertRaisesRegex(V.VerificationError, "identity"):
            V.verify(self.contract)

    def test_stem_conflict_overrides_known_year_wu(self):
        row = self.evaluate("conflict_time_gan")["results"][IDS[3]]
        self.assertEqual(row["state"], "unknown")
        self.assertEqual(row["conflicts"], [{"key": "gan", "pillar": "time", "values": ["戊", "庚"]}])

    def test_all_declared_cases(self):
        for case in self.contract["syntheticCases"]:
            with self.subTest(case=case["id"]):
                got = V.evaluate_chart(case["facts"], self.contract)
                self.assertEqual({k: v["state"] for k, v in got["results"].items()}, case["expected"])
                self.assertEqual(got["display"], case["expectedDisplay"])
                self.assertEqual({k: v["positions"] for k, v in got["results"].items() if "positions" in v}, case["expectedPositions"])
                self.assertEqual(got["statements"], case["expectedStatements"])

    def test_scope_unrelated_keys_and_same_value_duplicates(self):
        facts = self.case("R1_cap")["facts"]
        original = V.evaluate_chart(facts, self.contract)
        facts.extend([copy.deepcopy(facts[0]),
                      {"key": "zhi", "value": "酉", "scope": {"layer": "流年", "pillar": "day"}},
                      {"key": "irrelevant", "value": "anything", "scope": {"layer": "本命", "pillar": "day"}}])
        self.assertEqual(V.evaluate_chart(facts, self.contract), original)

    def test_position_join_order(self):
        self.assertEqual(V.join_positions(["year"]), "年柱")
        self.assertEqual(V.join_positions(["year", "day"]), "年柱和日柱")
        self.assertEqual(V.join_positions(["year", "month", "time"]), "年柱、月柱和时柱")

    def test_js_word_boundaries_next_to_chinese(self):
        for phrase in ("这是SANMINGTONGH-015规则", "值unknown不能显示", "字段rule_id", "看L1283原文", "文档x.md结束", "百分之三十"):
            with self.subTest(phrase=phrase):
                self.assertTrue(V.content_policy_hits(phrase))
        self.assertFalse(V.content_policy_hits("你的盘里申在年柱和月柱"))
        self.assertFalse(V.content_policy_hits("١٢%"))  # JS \d is ASCII.

    def fixture(self):
        # A test double for fixture protocol only, never real product acceptance.
        rows = []
        for case_id, cohort in (("R1_cap", "coverage388"), ("R2_hour_wu", "named"), ("R2_time_removed", "time_removed")):
            case = self.case(case_id)
            got = self.evaluate(case_id)
            rows.append({"id": case_id, "cohort": cohort, "facts": case["facts"],
                         "product": got["results"], "productDisplay": got["display"],
                         "productStatements": got["statements"]})
        return {"rows": rows}

    def verify_fixture(self, fixture, correct_hash=True):
        raw = (json.dumps(fixture, ensure_ascii=False) + "\n").encode()
        self.contract["fixture"] = {"path": self.contract["fixtureFormat"]["path"],
                                    "sha256": hashlib.sha256(raw).hexdigest() if correct_hash else "0" * 64}
        return V.verify(self.contract, fixture_bytes=raw)

    def test_fixture_protocol_and_deduplicated_coverage(self):
        fixture = self.fixture()
        report = self.verify_fixture(fixture)
        self.assertEqual(report["productFixture"], "verified")
        self.assertEqual(report["cohorts"]["coverage388"]["atLeastOneStatementCharts"], 1)
        self.assertEqual(report["cohorts"]["coverage388"]["displayedStatements"], 2)
        self.assertEqual(report["cohorts"]["time_removed"]["atLeastOneStatementCharts"], 0)
        self.contract["status"], self.contract["verified"] = "accepted", True
        self.assertEqual(self.verify_fixture(fixture)["result"], "PASS")

    def test_fixture_hash_rejected(self):
        with self.assertRaisesRegex(V.VerificationError, "sha256"):
            self.verify_fixture(self.fixture(), correct_hash=False)

    def test_fixture_empty_rejected(self):
        with self.assertRaisesRegex(V.VerificationError, "rows"):
            self.verify_fixture({"rows": []})

    def test_fixture_mismatches_rejected(self):
        for field in ("state", "positions", "missingKeys", "conflicts", "displayed", "notDisplayedReason", "productDisplay", "productStatements"):
            with self.subTest(field=field):
                fixture = self.fixture()
                row = fixture["rows"][0]
                if field.startswith("product"):
                    row[field] = []
                else:
                    row["product"][IDS[0]][field] = "wrong"
                with self.assertRaisesRegex(V.VerificationError, "product"):
                    self.verify_fixture(fixture)

    def test_dry_run_checks_an_external_fixture_and_writes_nothing(self):
        import tempfile
        before = V.CONTRACTS.read_bytes()
        with tempfile.TemporaryDirectory() as tmp:
            report_path = Path(tmp) / "report.json"
            original_report, V.REPORT = V.REPORT, report_path
            try:
                good = Path(tmp) / "good.json"
                good.write_text(json.dumps(self.fixture(), ensure_ascii=False) + "\n", encoding="utf-8")
                self.assertEqual(V.main(["--fixture", str(good)]), 0)
                bad_fixture = self.fixture()
                bad_fixture["rows"][0]["product"][IDS[1]]["state"] = "not_satisfied"
                bad = Path(tmp) / "bad.json"
                bad.write_text(json.dumps(bad_fixture, ensure_ascii=False) + "\n", encoding="utf-8")
                self.assertEqual(V.main(["--fixture", str(bad)]), 1)
                self.assertFalse(report_path.exists())
            finally:
                V.REPORT = original_report
        self.assertEqual(V.CONTRACTS.read_bytes(), before)

    def test_semantic_and_anchor_role_mutations_rejected(self):
        for mutation in ("structure", "anchorRole", "display"):
            with self.subTest(mutation=mutation):
                c = copy.deepcopy(self.original)
                if mutation == "structure":
                    c["rules"][1]["structure"]["branches"] = ["子", "酉"]
                elif mutation == "anchorRole":
                    c["rules"][1]["statementAnchors"] = ["dts-ziwu-name"]
                else:
                    c["displayPolicy"]["maxStatements"] = 3
                with self.assertRaises(V.VerificationError):
                    V.verify(c)


if __name__ == "__main__":
    unittest.main(verbosity=2)
