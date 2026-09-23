"""Verify the source-example table for 滴天髓阐微 051, without judging 吉凶.

The electronic source stays unchanged. The sole in-table correction comes from
the existing facsimile collation note; this verifier does not infer effects.
"""
from __future__ import annotations

import json
import re
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "sources/fulltext/bazi/ditiansui-chanwei/fulltext.md"
COLLATION = ROOT / "sources/normalized/bazi/ditiansui-chanwei/collation-notes.md"
TABLE = ROOT / "tools/reports/p1-bazi-20260922/ditiansui-051-shape-examples.json"
GANZHI = re.compile(r"[甲乙丙丁戊己庚辛壬癸][子丑寅卯辰巳午未申酉戌亥]")
ELEMENTS = "木火土金水"
EXPECTED_COUNTS = {"gaitou": 12, "jiejiao": 25}
CORRECTION = ("jiejiao", "土", "乙卯", "己卯")


def source_examples(lines: list[str], line_number: int, shape: str) -> list[tuple[str, str, str, int]]:
    line = lines[line_number - 1]
    groups = re.findall(r"喜([木火土金水])运而遇([^，。]+)", line)
    assert [element for element, _ in groups] == list(ELEMENTS), (line_number, groups)
    result = []
    for element, text in groups:
        pillars = GANZHI.findall(text)
        assert pillars, (line_number, element)
        # All non-Ganzhi characters are separators, the opening 如, or the closing 是也.
        assert re.sub(r"[、，。\s]|是也", "", GANZHI.sub("", text)) == "", (line_number, text)
        result.extend((shape, element, pillar, line_number) for pillar in pillars)
    return result


def main() -> None:
    lines = SOURCE.read_text().splitlines()
    notes = COLLATION.read_text()
    table = json.loads(TABLE.read_text())

    assert lines[13416 - 1] == "何谓盖头？"
    assert lines[13418 - 1] == "何谓截脚？"
    assert "PDF 503" in notes
    assert "喜土的截脚例为己卯，电子L13419误乙卯" in notes
    assert "喜金运次列项为戊申，电子L13411误戌申" in notes

    expected = source_examples(lines, 13417, "gaitou") + source_examples(lines, 13419, "jiejiao")
    assert Counter(shape for shape, _, _, _ in expected) == EXPECTED_COUNTS
    assert len(expected) == 37
    assert table["ruleId"] == "DITIANSUICHA-051"
    assert table["status"] == "source_morphology_only"
    assert table["electronicSource"] == str(SOURCE.relative_to(ROOT))
    assert table["collationSource"] == str(COLLATION.relative_to(ROOT))
    rows = table["rows"]
    assert len(rows) == len(expected)

    observed = []
    for row, (shape, element, electronic, line_number) in zip(rows, expected, strict=True):
        assert set(row) == {"favoriteElement", "shape", "luckPillar", "sourceLine", "collation"}
        assert (row["shape"], row["favoriteElement"], row["sourceLine"]) == (shape, element, line_number)
        collation = row["collation"]
        assert collation["electronicLuckPillar"] == electronic
        corrected = CORRECTION[3] if (shape, element, electronic) == CORRECTION[:3] else electronic
        assert row["luckPillar"] == corrected
        assert collation["correctedLuckPillar"] == corrected
        if corrected != electronic:
            assert collation == {
                "electronicLuckPillar": electronic,
                "correctedLuckPillar": corrected,
                "status": "facsimile_corrected",
                "facsimilePage": 503,
            }
        else:
            assert collation == {
                "electronicLuckPillar": electronic,
                "correctedLuckPillar": corrected,
                "status": "unchanged",
            }
        observed.append((shape, element, corrected))

    assert len(set(observed)) == len(rows), "duplicate shape/element/corrected-pillar row"
    assert Counter(row["shape"] for row in rows) == EXPECTED_COUNTS
    assert sum(row["collation"]["status"] == "facsimile_corrected" for row in rows) == 1
    print(f"PASS: {len(rows)} source morphology examples (12 gaitou, 25 jiejiao); one PDF-503 correction")


if __name__ == "__main__":
    main()
