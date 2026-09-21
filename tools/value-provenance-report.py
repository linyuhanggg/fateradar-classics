#!/usr/bin/env python3
"""谓词取值的**溯源分类**（t212）。

## 为什么做这个

贯穿契约第一条是「**不编造、可溯源、原文没写就不写**」。覆盖率、验证深度、死引用这些检查
管的是「谓词能不能跑通」，**没有一项在管「谓词里的取值是怎么来的」**。

本报告对每个取值叶子问一句：**这个值在**本条**规则的 statement／quote 里吗？**
不在的话，它是怎么来的？分四类：

    literal       取值（繁简折叠后）**字面出现在**本条 statement 或 quote 里
    enumerated    取值是本条为「跨键相等／组形条件」**枚举出的值域**之一
                  （如奇门「庚临岁干」逐干展开、六爻用神旬空的五亲展开）
    canonical     取值**既非字面、也非枚举、也非引擎态**——这一类**要读**：
                  它同时装着两种东西，报告不替人区分：
                    · 真·**名目对译**：原文俗称／异名 → 规范名
                      （如原文「财」→ 六亲规范名「妻财」；「七煞」→「七杀」；
                        「官祿宮」→ 引擎宫名「事业」）；
                    · **本条只是没提这个值**：如 section 标题、就绪条件式 statement
                      （「三传及日干五行均由已验证事实层给出」）——值本身是规范名，
                      但原文那句话里确实没写它。
    engine-state  取值由**引擎产出**（月建强度、活动状态、墓位…），本来就不是我写进原文的

## 这份报告有什么用

- 前三类合起来说明「值从哪来」；**canonical 一类是需要人抽检的**：
  每个对译都是一次「把原文词换成规范名」的判断，报告把**对译清单**直接列出来；
- 它同时给出一个可核对的总账：多少值是字面的、多少是枚举/规范名/引擎态，
  于是「原文没写就不写」这条**第一次有了可读的数字**。

**只报告，不改任何字段。**
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from predicate_lang import iter_usable_predicates  # noqa: E402

_spec = importlib.util.spec_from_file_location("vr_vp", ROOT / "tools/validate-rules.py")
vr = importlib.util.module_from_spec(_spec)
sys.modules["vr_vp"] = vr
assert _spec.loader is not None
_spec.loader.exec_module(vr)

# 「枚举编码」：本条在同一个键上展开了 ≥3 个取值——那是值域展开，不是原文用词。
ENUM_MIN_VALUES = 3
# 「引擎态」：这些键的取值由引擎判定产出，不是从原文抄的。
ENGINE_STATE_KEYS = frozenset(
    {
        "rizhu_strength",
        "geju",
        "yongshen",
        "liuyao_month_strength",
        "liuyao_activity",
        "liuyao_kong",
        "liuyao_progression",
        "liuyao_tomb",
        "liuyao_reversal",
        "liuyao_yongshen",
        "liuyao_yongshen_state",
        "liuyao_seq",
        "keti",
        "liuren_ke_relation",
        "liuren_ke_completeness",
        "liuren_yaoke",
        "liuren_shehai",
        "geju_qimen",
        "miaowang",
        "xiudu",
        "xingyao",
        "gongwei",
        "qizheng_ascendant",
        "shensha",
        "shi_shen",
        "nayin",
        "kongwang",
        "tianjiang",
        "yuejiang",
        "xiaoliuren_palace",
    }
)


EQUIVALENCES = ROOT / "tools/reports/value-equivalences.json"


def _reviewed() -> dict[tuple[str, str], dict]:
    """已逐组读过的「名目对译／原文未提」——读过的不再进待读清单（t213 起）。"""
    try:
        data = json.loads(EQUIVALENCES.read_text(encoding="utf-8"))
    except OSError:
        return {}
    return {(e["key"], str(e["value"])): e for e in data.get("entries", [])}


def classify() -> dict:
    per_class = Counter()
    canonical_pairs: dict[tuple[str, str], dict] = {}
    enumerated_keys = Counter()
    rows = 0
    for path in sorted((ROOT / "references/books").glob("*/*/rules.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        book = data.get("book") or {}
        for rule in data.get("rules") or []:
            if not isinstance(rule, dict) or not rule.get("applicable_to"):
                continue
            rows += 1
            text = vr.fold_han((rule.get("statement") or "") + (rule.get("quote") or ""))
            leaves = list(iter_usable_predicates(rule["applicable_to"]))
            per_key = Counter(c["key"] for c in leaves if c.get("value") not in (None, "*"))
            for c in leaves:
                value = c.get("value")
                if value in (None, "*"):
                    continue
                key = c["key"]
                if vr.fold_han(str(value)) in text:
                    per_class["literal"] += 1
                    continue
                if per_key[key] >= ENUM_MIN_VALUES:
                    per_class["enumerated"] += 1
                    enumerated_keys[key] += 1
                    continue
                if key in ENGINE_STATE_KEYS:
                    per_class["engine-state"] += 1
                    continue
                reviewed = _reviewed()
                pair_key = (key, str(value))
                if pair_key in reviewed:
                    per_class["canonical-reviewed"] += 1
                    continue
                per_class["canonical"] += 1
                slot = canonical_pairs.setdefault(
                    (key, str(value)),
                    {
                        "key": key,
                        "value": str(value),
                        "sample_rule": rule.get("rule_id"),
                        "sample_statement": (rule.get("statement") or "")[:70],
                        "count": 0,
                    },
                )
                slot["count"] += 1
    total = sum(per_class.values())
    return {
        "report": "谓词取值的溯源分类",
        "generated_by": "t212",
        "question": "每个取值叶子，在本条规则的 statement／quote 里吗？不在的话是怎么来的？",
        "classes": {
            "literal": "取值字面出现在本条 statement／quote 里（繁简折叠后）",
            "enumerated": f"本条在同一键上展开 ≥{ENUM_MIN_VALUES} 个取值——值域枚举，不是原文用词",
            "canonical": (
                "取值既非字面、也非枚举、也非引擎态——**这一类需要人读**："
                "既有真·名目对译（财→妻财、七煞→七杀、官祿宮→事业），"
                "也有「本条只是没提这个值」（section 标题、就绪条件式 statement）。"
            ),
            "engine-state": "取值由引擎判定产出（列举在工具里的 ENGINE_STATE_KEYS）",
            "canonical-reviewed": "同上，但**已逐组读过并登记**在 tools/reports/value-equivalences.json（t213 起）",
        },
        "rules_scanned": rows,
        "value_leaves": total,
        "tally": dict(per_class),
        "enumerated_keys": dict(enumerated_keys),
        "canonical_pairs": sorted(canonical_pairs.values(), key=lambda x: -x["count"]),
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="谓词取值的溯源分类")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    data = classify()
    if args.write:
        out = ROOT / "tools/reports/value-provenance.json"
        out.write_text(json.dumps(data, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"写入 {out.relative_to(ROOT)}")
    if args.json:
        json.dump(data, sys.stdout, ensure_ascii=False, indent=1)
        sys.stdout.write("\n")
        return 0
    t = data["tally"]
    total = data["value_leaves"]
    print(f"取值叶子 {total} 处（{data['rules_scanned']} 条带谓词的规则）：")
    for k in ("literal", "enumerated", "canonical", "canonical-reviewed", "engine-state"):
        n = t.get(k, 0)
        print(f"   {n:5} ({n / total * 100:4.1f}%)  {k:13} {data['classes'][k]}")
    print(f"\n枚举编码涉及的键：{data['enumerated_keys']}")
    print(f"\n需人读的一组（既非字面／枚举／引擎态）共 {len(data['canonical_pairs'])} 组，前 12 组：")
    print("  注意：这一类里既有真·名目对译，也有「本条只是没提这个值」（section 标题、就绪条件式）。")
    for pair in data["canonical_pairs"][:12]:
        print(f"   {pair['count']:4}× {pair['key']}={pair['value']}   例：{pair['sample_rule']} 「{pair['sample_statement'][:34]}」")
    return 0


if __name__ == "__main__":
    sys.exit(main())