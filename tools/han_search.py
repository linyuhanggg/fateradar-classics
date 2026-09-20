#!/usr/bin/env python3
"""繁简折半检索助手：**先把「查无」当成待验证的断言，而不是结论**。

这个类别的坑我已经踩过三次：

  · t177 —— 用简体「游魂」去检索**繁体**正文，得 0 行，于是结论写成
    「本版没有可锚正文」；实际「遊魂」有 6 行（正文在 L7720–L7730）。
  · t182 —— 「域完备键」漏了一整类，把 25 条恒真少算成 … 实际 64 条。
  · t183 —— 用简体格局名检索繁体术语表，把 8 个**其实有定义**的名字判成「全文 0 次」。

共同点：**检索方式的盲区会伪造出「查无」**，而「查无」一旦被当成结论，
就会一路写进台账与交付文档。

本模块提供唯一入口 `lookup()`：同时按**原字面**与**折半后**检索，
并且**把两种口径的命中数都报出来**——只要两者不一致，就说明字面差异存在，
调用方必须交代清楚是哪种口径得出的结论。
"""

from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

_vr_spec = importlib.util.spec_from_file_location("vr_fold", ROOT / "tools/validate-rules.py")
_vr = importlib.util.module_from_spec(_vr_spec)
sys.modules["vr_fold"] = _vr
assert _vr_spec.loader is not None
_vr_spec.loader.exec_module(_vr)
fold_han = _vr.fold_han


def _has_cjk(text: str) -> bool:
    return any("\u4e00" <= ch <= "\u9fff" for ch in text)


_FOLD_CACHE: dict[Path, list[str]] = {}


def _folded_lines(p: Path) -> list[str]:
    """整份文件只折一次并缓存。

    t183 已经踩过：逐行调 opencc 会让一次检索从秒级变成分钟级，
    并被 60 秒超时杀掉。这里复用同一处置。
    """
    if p not in _FOLD_CACHE:
        _FOLD_CACHE[p] = [fold_han(x) for x in p.read_text(encoding="utf-8").split("\n")]
    return _FOLD_CACHE[p]


def lookup(term: str, files: list[Path] | None = None) -> dict:
    """在语料里检索一个词，**两种口径都查**。

    返回 {literal: [...], folded: [...], diverges: bool, term, folded_term}。
    `diverges=True` 表示「按原字面搜不到、折半后能搜到」（或反之）——
    这种情况**不允许**直接下「查无」的结论。
    """
    if files is None:
        files = sorted((ROOT / "sources/fulltext").rglob("fulltext.md"))
    folded_term = fold_han(term) if _has_cjk(term) else term
    literal: list[dict] = []
    folded: list[dict] = []
    for p in files:
        raw = p.read_text(encoding="utf-8").split("\n")
        folded_lines = _folded_lines(p) if _has_cjk(folded_term) else raw
        for i, line in enumerate(raw, 1):
            if term in line:
                literal.append({"file": p.relative_to(ROOT).as_posix(), "line": i, "quote": line.strip()[:120]})
            if folded_term and folded_term in folded_lines[i - 1]:
                folded.append({"file": p.relative_to(ROOT).as_posix(), "line": i, "quote": line.strip()[:120]})
    return {
        "term": term,
        "folded_term": folded_term,
        "literal": literal,
        "folded": folded,
        "diverges": bool(literal) != bool(folded),
    }


def main() -> int:
    import argparse

    ap = argparse.ArgumentParser(description="繁简折半检索（两种口径都报）")
    ap.add_argument("terms", nargs="+")
    args = ap.parse_args()
    for term in args.terms:
        r = lookup(term)
        print(f"「{term}」（折半后「{r['folded_term']}」）: 原字面 {len(r['literal'])} 行；折半 {len(r['folded'])} 行"
              + ("  ⚠ 两口径不一致——不得直接下「查无」结论" if r["diverges"] else ""))
        for h in r["folded"][:4]:
            print(f"    {h['file'].split('/')[-2]} L{h['line']}: {h['quote'][:78]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())