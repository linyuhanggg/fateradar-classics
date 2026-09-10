#!/usr/bin/env python3
"""Inventory progress and classification regressions; fixture writes stay in /tmp."""
from __future__ import annotations

import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

SPEC = importlib.util.spec_from_file_location("library_inventory", Path(__file__).with_name("build-library-inventory.py"))
inventory = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(inventory)
KNOWLEDGE_SPEC = importlib.util.spec_from_file_location("knowledge_index", Path(__file__).with_name("build-knowledge-index.py"))
knowledge = importlib.util.module_from_spec(KNOWLEDGE_SPEC)
KNOWLEDGE_SPEC.loader.exec_module(knowledge)
ROOT = Path(__file__).resolve().parents[1]


class FacsimileMappingTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)

    def create_file(self, relative):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(b"fixture: inventory checks file presence, not image collation")
        return relative

    def build_index(self):
        with patch.multiple(inventory, ROOT=self.root, FACSIMILE=self.root / "sources/facsimile"):
            return inventory.facsimile_index()

    def test_ditiansui_shared_files_directory_is_attached_to_its_book(self):
        path = self.create_file("sources/facsimile/wikisource/files/SSID-11335994 滴天髓闡微.pdf")
        self.assertEqual(self.build_index().get("ditiansui-chanwei"), [path])

    def test_shared_0808_volume_can_support_each_named_work_without_duplicate_files(self):
        path = self.create_file("sources/facsimile/wikisource/files/文淵閣四庫全書 0808冊.djvu")
        found = self.build_index()
        for slug in ("hanlong-jing", "yilong-jing", "huangdi-zhaijing", "qingnang-aoyu", "qingnang-xu", "zangfa-daozhang", "zangshu", "tianyu-jing", "daliuren-daquan"):
            self.assertEqual(found.get(slug), [path], slug)
        self.assertNotIn("qingnang-jing", found, "0808 does not contain 青囊经 merely because its title is similar")

    def test_shared_0809_volume_covers_the_three_documented_xingming_works(self):
        path = self.create_file("sources/facsimile/wikisource/files/文淵閣四庫全書 0809冊.djvu")
        found = self.build_index()
        for slug in ("yuzhao-shenying", "xingming-suyuan", "xingxue-dacheng"):
            self.assertEqual(found.get(slug), [path], slug)

    def test_dutian_uses_only_dili_bianzheng_parts_actually_present(self):
        second = self.create_file("sources/facsimile/other/dili-bianzheng/part-02.pdf")
        first = self.create_file("sources/facsimile/other/dili-bianzheng/part-01.pdf")
        found = self.build_index()
        self.assertEqual(found.get("dutian-baozhao-jing"), [first, second])
        self.assertEqual(found.get("dili-bianzheng"), [first, second])

    def test_a_manifest_association_without_a_local_file_is_not_in_repo(self):
        self.create_file("sources/facsimile/wikisource/MANIFEST.md")
        self.assertNotIn("ditiansui-chanwei", self.build_index())
        self.assertNotIn("hanlong-jing", self.build_index())


class ClassificationTests(unittest.TestCase):
    def test_original_shu_shangshu_case_keeps_its_range(self):
        lines = (ROOT / "sources/fulltext/bazi/ziping-zhenquan/fulltext.md").read_text(encoding="utf-8").splitlines()
        _, paragraphs = inventory.split_paragraphs(lines)
        case = next(p for p in paragraphs if p["start_line"] == 1505)
        self.assertEqual(case["id"], "L1505-L1505")
        self.assertEqual(case["end_line"], 1505)
        self.assertEqual(case["kind"], "案例")
        self.assertEqual(case.get("classification_method"), "pattern")
        self.assertEqual(case.get("four_pillar_sequences"), [["丁亥", "壬子", "辛巳", "丁酉"]])

    def test_formula_is_detected_in_body_without_markdown_heading(self):
        text = "取课先从下贼呼，如无下贼上克初。初传之上名中次，中上加临是末居。"
        self.assertEqual(inventory.classify_paragraph(text, "理论"), "操作步骤")
        self.assertEqual(inventory.classify_paragraph("天机正月起丑逆数。", "理论"), "操作步骤")

    def test_bare_four_pillars_with_comment_are_case_but_calendar_list_is_not(self):
        self.assertEqual(inventory.classify_paragraph("乙亥、乙酉、乙卯、丁丑（煞旺食強身健）", "理论"), "案例")
        self.assertNotEqual(inventory.classify_paragraph("甲子、乙丑、丙寅、丁卯、戊辰、己巳，六十甲子排列。", "理论"), "案例")

    def test_unmatched_body_does_not_become_reviewed_theory(self):
        _, paragraphs = inventory.split_paragraphs(["# 正文", "", "尚未做语义处理的一段材料。"])
        self.assertEqual(paragraphs[0]["kind"], "待分类")
        self.assertEqual(paragraphs[0].get("classification_method"), "unclassified")

    def test_existing_paragraph_ids_and_ranges_are_not_recut(self):
        for path in sorted((ROOT / "references/inventory/paragraphs").glob("*/*.json")):
            old = json.loads(path.read_text(encoding="utf-8"))
            _, new = inventory.split_paragraphs((ROOT / old["fulltext"]).read_text(encoding="utf-8").splitlines())
            before = [(p["id"].split(":", 1)[1], p["start_line"], p["end_line"]) for p in old["paragraphs"]]
            after = [(p["id"], p["start_line"], p["end_line"]) for p in new]
            self.assertEqual(before, after, path.name)


class ProgressTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.write("references/catalog/catalog.json", {"ready_count": 1, "ready_reference_packs": [{"system": "bazi", "slug": "sample", "title": "例书"}]})
        pack = self.root / "references/books/bazi/sample"
        pack.mkdir(parents=True)
        (pack / "rules.yaml").write_text("rules:\n- rule_id: OLD-01\n  verified: false\n", encoding="utf-8")
        source = self.root / "sources/fulltext/bazi/sample/fulltext.md"
        source.parent.mkdir(parents=True)
        source.write_text("# 正文\n\n尚未作白话的一段文字，仅作为可检索原文等待语义整理。\n\n舒尚書命：丁亥、壬子、辛巳、丁酉\n\n天机正月起丑逆数。\n\n尚未作白话的一段文字，仅作为可检索原文等待语义整理。\n", encoding="utf-8")
        self.write("references/executable/sample.json", {"book": {"slug": "sample", "system": "bazi"}, "rules": [{"id": "S-E-01", "vernacular": "这只是规则条目的白话。", "verified": False}]})
        self.annotation = {"bookSlug": "sample", "entries": [
            {"paragraphId": "sample:L0003-L0003", "kind": "理论", "vernacular": "这段说明一个传统概念。", "terms": [], "notes": [], "review": "source-reviewed"},
            {"paragraphId": "sample:L0005-L0005", "kind": "案例", "vernacular": "草稿记录了四柱，具体断法尚待逐句核对。", "terms": [], "notes": [], "review": "draft"},
        ]}

    def write(self, relative, data):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")

    def build(self):
        with patch.multiple(inventory, ROOT=self.root, CATALOG=self.root / "references/catalog/catalog.json", BOOKS=self.root / "references/books", FULLTEXT=self.root / "sources/fulltext", FACSIMILE=self.root / "sources/facsimile", OUT_DIR=self.root / "references/inventory", DOC_OUT=self.root / "docs/LIBRARY_INVENTORY.md"):
            (self.root / "docs").mkdir(exist_ok=True)
            with contextlib.redirect_stdout(io.StringIO()):
                inventory.main()
        return json.loads((self.root / "references/inventory/library-inventory.json").read_text(encoding="utf-8"))

    def test_progress_comes_from_annotations_not_rule_array_or_slug(self):
        self.write("references/annotations/bazi/sample.json", self.annotation)
        result = self.build()
        counts = result["counts"]
        self.assertEqual(counts.get("annotated_paragraphs"), 2)
        self.assertEqual(counts.get("vernacular_paragraphs"), 2)
        self.assertEqual(counts.get("source_reviewed_paragraphs"), 1)
        self.assertEqual(counts.get("source_reviewed_vernacular_paragraphs"), 1)
        self.assertEqual(counts.get("rule_definitions"), 1)
        self.assertEqual(counts.get("rule_definitions_with_vernacular"), 1)
        self.assertEqual(counts.get("paragraphs_without_vernacular"), 2)
        self.assertEqual(counts.get("verified_rule_flags"), 0)
        paragraphs = json.loads((self.root / "references/inventory/paragraphs/bazi/sample.json").read_text(encoding="utf-8"))["paragraphs"]
        self.assertEqual(paragraphs[0].get("classification_method"), "annotation")
        self.assertEqual(paragraphs[0].get("annotation_review"), "source-reviewed")
        self.assertNotEqual(paragraphs[0].get("verified"), True)
        self.assertEqual(paragraphs[-1].get("same_text_as"), "sample:L0003-L0003")
        self.assertNotIn("本轮接入可执行规则", (self.root / "docs/LIBRARY_INVENTORY.md").read_text(encoding="utf-8"))

    def test_no_annotations_means_no_semantic_or_vernacular_progress(self):
        result = self.build()
        self.assertEqual(result["counts"].get("annotated_paragraphs"), 0)
        self.assertEqual(result["counts"].get("vernacular_paragraphs"), 0)
        self.assertEqual(result["counts"].get("rule_definitions_with_vernacular"), 1)

    def test_local_facsimile_is_a_candidate_not_a_collation_result(self):
        path = self.root / "sources/facsimile/other/sample/part-01.pdf"
        path.parent.mkdir(parents=True)
        path.write_bytes(b"fixture facsimile")
        result = self.build()
        self.assertEqual(result["packs"][0]["facsimile_status"], "in_repo")
        self.assertEqual(result["counts"]["source_reviewed_paragraphs"], 0)
        self.assertEqual(result["counts"]["verified_rule_flags"], 0)
        report = (self.root / "docs/LIBRARY_INVENTORY.md").read_text(encoding="utf-8")
        self.assertIn("已存影印／候选底本", report)
        self.assertIn("不代表与电子本文字完全一致", report)

    def test_unknown_paragraph_does_not_inflate_progress(self):
        self.annotation["entries"][0]["paragraphId"] = "sample:L0003-L0005"
        self.write("references/annotations/bazi/sample.json", self.annotation)
        with self.assertRaisesRegex(ValueError, "paragraphId"):
            self.build()

    def test_duplicate_annotations_do_not_count_as_two_processed_paragraphs(self):
        self.annotation["entries"].append(dict(self.annotation["entries"][0]))
        self.write("references/annotations/bazi/sample.json", self.annotation)
        with self.assertRaisesRegex(ValueError, "duplicate|重复"):
            self.build()

    def test_empty_explanation_is_not_a_semantic_annotation(self):
        self.annotation["entries"][0]["vernacular"] = " "
        self.write("references/annotations/bazi/sample.json", self.annotation)
        with self.assertRaisesRegex(ValueError, "vernacular"):
            self.build()

    def test_knowledge_samples_keep_unclassified_text_without_claiming_review(self):
        result = self.build()
        result["packs"][0]["destination"] = "knowledge"
        self.write("references/inventory/library-inventory.json", result)
        # A source paragraph can be searchable before it has semantic annotation.
        with patch.multiple(knowledge, ROOT=self.root, INV=self.root / "references/inventory/library-inventory.json", PARA_DIR=self.root / "references/inventory/paragraphs", OUT=self.root / "references/inventory/knowledge-index.json"):
            with contextlib.redirect_stdout(io.StringIO()):
                knowledge.main()
        samples = json.loads((self.root / "references/inventory/knowledge-index.json").read_text(encoding="utf-8"))["packs"][0]["sample_paragraphs"]
        candidate = next((p for p in samples if p["id"] == "sample:L0003-L0003"), None)
        self.assertIsNotNone(candidate)
        self.assertEqual(candidate.get("classification_method"), "unclassified")
        self.assertNotEqual(candidate.get("annotation_review"), "source-reviewed")


if __name__ == "__main__":
    unittest.main()
