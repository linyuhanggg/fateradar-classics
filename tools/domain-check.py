#!/usr/bin/env python3
"""「取值是否落在键的封闭值域内」检查（t201）。

## 为什么要查这个

若某条谓词写了 `{key: X, value: v}`，而 `X` 是**封闭值域**的键、`v` 又不在该值域里，
那么这条谓词**永远不可能命中**——它是一条**死谓词**，但覆盖率照旧把它算成「已映射」。
现有门禁都不查这一段：

    · `--check-art-keys`    比的是「键是否在该术产出」；
    · `--check-open-values` 只管**开放值域**键的取值是否在样盘出现过；
    · 死引用扫描            只管键，不管值。

本检查补上：「封闭值域键的取值必须在声明值域内」。

## 一处曾被我误判、值得记下的细节

`rizhu` 看着像「日柱」（六十甲子），实际引擎产出的是**日干**（`emit.ts`：
`pushFact(out, "rizhu", input.dayGan, …)`），值域是十天干。
穷通宝鉴那批「日干为乙／丁／癸」的规则写 `{rizhu: 乙}` 是**对的**——
我先入为主以为值域是六十甲子，差点把它当成缺陷。
所以本检查用的是**词表里声明的值域**（由引擎 `toFactVocabJson()` 生成），不是我的记忆。
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from predicate_lang import iter_usable_predicates  # noqa: E402

VOCAB = ROOT / "references/vocab/fact-vocab.json"


def closed_domains() -> dict[str, set[str]]:
    """词表里**声明了值域**的键（空列表＝开放值域，不在此检查范围）。"""
    data = json.loads(VOCAB.read_text(encoding="utf-8"))
    return {k: set(v) for k, v in (data.get("values") or {}).items() if v}


def find_out_of_domain(domains: dict[str, set[str]] | None = None) -> list[tuple[str, str, str, int]]:
    doms = domains if domains is not None else closed_domains()
    bad: list[tuple[str, str, str, int]] = []
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict) or not rule.get("applicable_to"):
                continue
            for clause in iter_usable_predicates(rule["applicable_to"]):
                key, value = clause.get("key"), clause.get("value")
                if not key or value in (None, "*"):
                    continue
                domain = doms.get(key)
                if domain and value not in domain:
                    bad.append((rule["rule_id"], key, value, len(domain)))
    return bad


def main() -> int:
    ap = argparse.ArgumentParser(description="谓词取值 vs 键的封闭值域")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    bad = find_out_of_domain()
    if args.json:
        json.dump(
            [{"rule_id": r, "key": k, "value": v, "domain_size": n} for r, k, v, n in bad],
            sys.stdout,
            ensure_ascii=False,
            indent=1,
        )
        sys.stdout.write("\n")
    else:
        print(f"取值不在键声明值域内的谓词叶子：{len(bad)} 处")
        for r, k, v, n in bad[:20]:
            print(f"  [{r:22}] {k}={v}（值域 {n} 项）")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())