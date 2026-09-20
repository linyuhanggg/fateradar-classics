#!/usr/bin/env python3
"""谓词语言 v3 的共享叶子遍历。契约见 docs/PREDICATE-LANGUAGE-V3.md。

`applicable_to` 有两种形态：旧平铺列表（＝any_of），以及 v3 组 mapping
（`{any_of|all_of: [...], none_of?: [...], same?: 字段}`，可嵌套）。

**只按 `isinstance(x, list)` 判断的旧代码会把 v3 组整体当成「没有谓词」**：
对 mapping 做 `for pred in raw` 会迭代出键名字符串，`isinstance(pred, dict)` 全假，
于是 `applicable_to` 被读成空 —— 覆盖率少算、未映射报告多算，且没有任何报错。
本模块是唯一实现，覆盖报告、导出与校验都必须用它。
"""

from __future__ import annotations

BRANCHES = ("any_of", "all_of", "none_of")


def iter_predicates(node):
    """深度优先产出 node 里所有叶子 predicate（mapping 且带 `key`）。"""
    if isinstance(node, list):
        for item in node:
            yield from iter_predicates(item)
        return
    if not isinstance(node, dict):
        return
    if "key" in node:
        yield node
        return
    for branch in BRANCHES:
        for child in node.get(branch) or []:
            yield from iter_predicates(child)


def iter_usable_predicates(node):
    """只要 key 与 value 都到位的叶子（与 predicate-report.py 旧判据一致）。"""
    for pred in iter_predicates(node):
        if pred.get("key") and pred.get("value") is not None:
            yield pred


def has_predicates(node) -> bool:
    return next(iter_usable_predicates(node), None) is not None


def leaf_count(node) -> int:
    return sum(1 for _ in iter_usable_predicates(node))