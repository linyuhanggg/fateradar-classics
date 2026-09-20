#!/usr/bin/env python3
"""「死引用」扫描：谓词引用的键，在样盘里**从未出现过**。

## 这一类此前没人查

`--check-art-keys` 比的是谓词的键 vs `ART_EMIT_KEYS`（**我声明**引擎会产出什么）；
`--check-open-values` 只覆盖开放值域的**取值**。两者都不检查
「这条谓词引用的键，是否真的在任何一张样盘上出现过」。
于是一类问题可以长期潜伏：键在词表里、在我的 emit 表里，但**样盘从不产出它**
→ 规则永远算「信息不足」，看起来像「事实缺失」，实为**样盘没覆盖那一层**。

t192 首次跑这个扫描，命中 8 条 ziwei 规则引用 `daxian` / `liunian_taisui` ——
这正是 t170 起就挂在未决清单里的那一条（当时记成「要恢复产出，还是承认它们作废」）。
实际根因是：`emitZiweiFacts` **确实产出**这两键，但 `daxian` 要 `d.accent`、
`liunian_taisui` 要 `viewYear` —— 而 dump 里建 ziwei 盘时**没给参照日期**，
所以运限层从未出现在样盘中。补一张带参照日期的样盘后归零。

## 判据

对每个受门禁的术：把样盘中出现过的 `key` 集合取出来，
谓词里每片叶子的 `key` 都必须落在其中。空集不报（该术没有样盘时另行处理）。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

_spec = importlib.util.spec_from_file_location("pr_dr", ROOT / "tools/predicate-report.py")
pr = importlib.util.module_from_spec(_spec)
sys.modules["pr_dr"] = pr
assert _spec.loader is not None
_spec.loader.exec_module(pr)

sys.path.insert(0, str(ROOT / "tools"))
from predicate_lang import iter_usable_predicates  # noqa: E402

ARTS = ("bazi", "ziwei", "qimen", "liuren", "liuyao", "qizheng")
DUMP = ROOT / "tools/reports/facts-sample.json"


def observed_keys(dump_path: Path = DUMP) -> dict[str, set[str]]:
    """每个术：样盘里真正出现过的 key 集合。"""
    dump = json.loads(dump_path.read_text(encoding="utf-8"))
    out: dict[str, set[str]] = defaultdict(set)
    for art, cases in dump.items():
        for sample in (cases or {}).values():
            for fact in sample.get("facts") or []:
                if isinstance(fact, dict) and fact.get("key"):
                    out[art].add(fact["key"])
    return dict(out)


def find_dead(observed: dict[str, set[str]] | None = None) -> list[tuple[str, str, str]]:
    """返回 [(art, rule_id, key)]，即引用了该术样盘中从未出现的键的叶子。"""
    seen = observed if observed is not None else observed_keys()
    dead: list[tuple[str, str, str]] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        book = data.get("book") or {}
        art = pr.art_of(book.get("system"), book.get("slug"))
        if art not in ARTS:
            continue
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict):
                continue
            ap = rule.get("applicable_to")
            if not ap:
                continue
            for clause in iter_usable_predicates(ap):
                key = clause.get("key")
                if key and key not in seen.get(art, set()):
                    dead.append((art, rule["rule_id"], key))
    return dead


def main() -> int:
    ap = argparse.ArgumentParser(description="死引用扫描（谓词的键是否在任何样盘中出现过）")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    dead = find_dead()
    if args.json:
        json.dump([{"art": a, "rule_id": r, "key": k} for a, r, k in dead], sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
    else:
        print(f"引用了「该术样盘中从未出现的键」的谓词叶子：{len(dead)} 处")
        for a, r, k in sorted(set(dead))[:20]:
            print(f"  [{a:8}] {r:22} key={k}")
    return 1 if dead else 0


if __name__ == "__main__":
    sys.exit(main())