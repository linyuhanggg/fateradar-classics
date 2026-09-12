#!/usr/bin/env python3
"""coverage-report 的证据列自检（第 19 批加）。

`quote_verbatim / quote_restatement / quote_empty` 三列是这一批的实质产出：
它们把「规则的 quote 是逐字引文还是编者重述」分开报。这个区分不是装饰——
实测 1,356 条规则里有 156 条的 quote 与 statement 逐字相同且无 anchor，其中只有 2 条能在
fulltext 里逐字找到；不分开报，读者会把重述当引文。

因此本测试钉住三件事：
1. 三列相加必须等于该术的 total（账目闭合，不能有规则掉在缝里）；
2. 三列与逐文件直读 YAML 的结果一致（不是另一套算法自说自话）；
3. `verbatim` 的定义与 validate-rules 的 V15 契约一致：显式 restatement 之外、有 quote 的才算引文，
   且「quote==statement 且无 anchor」这种写法在 V15 下只能声明为 restatement。
"""

import importlib.util
import json
import subprocess
import sys
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]


def load_coverage() -> dict:
    out = subprocess.run(
        [sys.executable, "tools/coverage-report.py", "--json"],
        cwd=ROOT,
        capture_output=True,
        text=True,
        check=True,
    ).stdout
    return json.loads(out)


def art_of(system: str, slug: str) -> str:
    """与 coverage-report 同源的术数映射（单独实现一份，避免「调用被测对象」）。"""
    if system == "bazi":
        return "bazi"
    if system == "ziwei":
        return "ziwei"
    if system == "san-shi":
        return {"qimen-dunjia-tongzhi": "qimen", "daliuren-daquan": "liuren"}.get(slug, slug)
    if system == "divination":
        return {
            "huangjin-ce": "liuyao",
            "huozhu-lin": "liuyao",
            "zengshan-buyi": "liuyao",
            "bushi-zhengzong": "liuyao",
            "meihua-yishu": "meihua",
            "zhouyi-zhezhong": "yili",
            "huangji-jingshi": "yili",
        }.get(slug, slug)
    if system == "xingming":
        return "qizheng"
    return slug


def direct_counts() -> dict[str, dict[str, int]]:
    """直接从 rules.yaml 数一遍，不经过 coverage-report 的实现。"""
    acc: dict[str, dict[str, int]] = {}
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        book = data.get("book") or {}
        art = f"{book.get('system')}/{book.get('slug')}"  # 与 coverage-report 的 books[].book 同键
        rules = [r for r in (data.get("rules") or []) if isinstance(r, dict)]
        row = acc.setdefault(art, {"total": 0, "verbatim": 0, "restatement": 0, "empty": 0})
        for r in rules:
            row["total"] += 1
            quote = (r.get("quote") or "").strip()
            if not quote:
                row["empty"] += 1
            elif r.get("quote_kind") == "restatement":
                row["restatement"] += 1
            else:
                row["verbatim"] += 1
    return acc


class CoverageEvidenceColumns(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.payload = load_coverage()
        cls.direct = direct_counts()

    def test_columns_close_the_books_for_every_art(self):
        for group in ("arts", "reference_arts"):
            for art, d in self.payload[group].items():
                with self.subTest(art=art):
                    self.assertEqual(
                        d["quote_verbatim"] + d["quote_restatement"] + d["quote_empty"],
                        d["total"],
                        f"{art} 的三列之和应等于 total",
                    )

    def test_columns_match_a_direct_read_of_the_yaml(self):
        # 逐**书**对账（coverage-report 的 books[] 与直读同键：system/slug），
        # 再把直读结果按术汇总与 arts[] 对账——两层都核，避免只对上总数对不上明细。
        for rec in self.payload["books"]:
            row = self.direct.get(rec["book"])
            self.assertIsNotNone(row, f"{rec['book']} 在直读结果里不存在")
            with self.subTest(book=rec["book"]):
                self.assertEqual(rec["verbatim"], row["verbatim"])
                self.assertEqual(rec["restatement"], row["restatement"])
                self.assertEqual(rec["no_quote"], row["empty"])

        rolled: dict[str, dict[str, int]] = {}
        for rec in self.payload["books"]:
            art = rec["art"]
            row = rolled.setdefault(art, {"verbatim": 0, "restatement": 0, "empty": 0})
            row["verbatim"] += self.direct[rec["book"]]["verbatim"]
            row["restatement"] += self.direct[rec["book"]]["restatement"]
            row["empty"] += self.direct[rec["book"]]["empty"]
        for art, d in self.payload["arts"].items():
            row = rolled.get(art, {"verbatim": 0, "restatement": 0, "empty": 0})
            with self.subTest(art=art):
                self.assertEqual(d["quote_verbatim"], row["verbatim"])
                self.assertEqual(d["quote_restatement"], row["restatement"])
                self.assertEqual(d["quote_empty"], row["empty"])

    def test_quote_equals_statement_without_anchor_must_be_declared(self):
        # V15 的独立复核：**只有当 quote 与 statement 逐字相同**时，「无 anchor」才必须
        # 声明为 restatement。quote 与 statement 不同、又没有 anchor 的规则是允许的——
        # 意思是「这句引文尚未定位到行」，此时 coverage 报的 anchor 覆盖率已把它算作未锚。
        # （第 19 批初版测试把两者混为一谈，误报 243 条；这里写明差别。）
        offenders = []
        for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            for i, r in enumerate(data.get("rules") or []):
                if not isinstance(r, dict):
                    continue
                q = (r.get("quote") or "").strip()
                st = (r.get("statement") or "").strip()
                if not q or q != st:
                    continue
                if r.get("quote_kind") == "restatement":
                    continue
                if not isinstance(r.get("anchor"), dict):
                    offenders.append(f"{path.relative_to(ROOT)} rules[{i}]")
        self.assertEqual(offenders, [], f"quote==statement 且无 anchor 却未声明 restatement：{offenders[:5]}")


if __name__ == "__main__":
    unittest.main()
