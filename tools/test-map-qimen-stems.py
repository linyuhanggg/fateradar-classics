#!/usr/bin/env python3
"""tools/map-qimen-stems.py 的回归测试。

钉住四件事：
  1. 16 条映射的 statement 复核片段确实在原文里（判据基于原文，不是自报）；
  2. 落盘谓词形态正确：干干相配用 `same: gong` 绑定，点名宫位的用 `scope.gong`；
  3. **中五不立天地盘干事实**——引擎既有不变量（无任何 fact 带 gong=5），
     事实样本与产品测试都依赖它；本批不得破坏；
  4. `甲` 绝不作为取值出现（甲寄六仪，天地盘只有九干）。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
BOOK = "san-shi/qimen-dunjia-tongzhi"
YAML_PATH = ROOT / "references/books" / BOOK / "rules.yaml"
SAMPLE = ROOT / "tools/reports/facts-sample.json"
PRODUCT_VOCAB = Path("/Users/sync/code/cosmic-fortune-lab/src/lib/engine/facts/fact-vocab.json")

FAILED: list[str] = []


def check(tag: str, got, want) -> None:
    if got != want:
        FAILED.append(f"{tag}: got {got!r} want {want!r}")
        print(f"  FAIL {tag}: got {got!r} want {want!r}")
    else:
        print(f"  ok   {tag}")


def main() -> int:
    ledger = json.loads((ROOT / "tools/reports/qimen-stem-map.json").read_text(encoding="utf-8"))
    data = yaml.safe_load(YAML_PATH.read_text(encoding="utf-8"))
    rules = {r["rule_id"]: r for r in data["rules"]}

    print("1. 台账 16 条，且复核片段仍在原文里")
    check("  条数 20（t184 增 三奇得使）", len(ledger), 20)
    miss = [
        x["rule_id"]
        for x in ledger
        if x["evidence_from_statement"] not in (rules.get(x["rule_id"], {}).get("statement") or "")
    ]
    check("  statement 片段全部命中", miss, [])

    print("2. 落盘谓词形态")
    bad_shape = []
    for x in ledger:
        cur = rules[x["rule_id"]].get("applicable_to")
        if not cur:
            bad_shape.append(f"{x['rule_id']}: 空")
            continue
        s = json.dumps(cur, ensure_ascii=False)
        if "geju_qimen" in s:
            continue  # 伏吟局/反吟局：单谓词
        if "same" in s:
            if '"same": "gong"' not in s:
                bad_shape.append(f"{x['rule_id']}: same 不是 gong")
        elif "gong" not in s:
            bad_shape.append(f"{x['rule_id']}: 既无 same: gong 也无 scope.gong")
    check("  形态全部合规", bad_shape, [])

    print("3. 中五不立天地盘干事实（引擎既有不变量）")
    sample = json.loads(SAMPLE.read_text(encoding="utf-8"))
    gong5 = [
        f["key"]
        for c in sample["qimen"].values()
        for f in c["facts"]
        if f["scope"].get("gong") == 5
    ]
    check("  样本中无任何 fact 带 gong=5", gong5, [])
    for case, c in sample["qimen"].items():
        for key in ("tianpan_gan", "dipan_gan"):
            n = len([f for f in c["facts"] if f["key"] == key])
            if n != 0 and n != 8:
                FAILED.append(f"{case} {key} 条数 {n}（应为 8：八宫，中五不立）")
                print(f"  FAIL {case} {key} 条数 {n}")
    check("  天地盘干各 8 条/盘（八宫）", True, True)

    print("3b. 值符类三条：存在性通配 + same: gong 绑定（t178）")
    ZHIFU_RULES = ("QM-P01", "QM-P02", "QM-P31")
    bad_z = []
    for rid in ZHIFU_RULES:
        ap = rules[rid].get("applicable_to")
        s_ = json.dumps(ap, ensure_ascii=False)
        if '"same": "gong"' not in s_:
            bad_z.append(f"{rid}: 缺 same: gong")
        wild = [b for b in (ap or {}).get("all_of", []) if b.get("value") == "*"]
        if len(wild) != 1 or wild[0]["key"] != "zhifu":
            bad_z.append(f"{rid}: 通配子句应恰为一条 zhifu 存在性子句")
    check("  三条形态合规（值符存在性 + same: gong）", bad_z, [])

    def _f(k, v, **sc):
        return {"key": k, "value": v, "scope": sc, "derivedFrom": ["test"]}

    import importlib.util as _ilu

    _spec = _ilu.spec_from_file_location("ev_q", ROOT / "tools/eval-predicates.py")
    _ev = _ilu.module_from_spec(_spec)
    sys.modules["ev_q"] = _ev
    assert _spec.loader is not None
    _spec.loader.exec_module(_ev)
    qrules = {r["rule_id"]: r for r in _ev.load_rules("san-shi/qimen-dunjia-tongzhi", None)}
    chart = [
        _f("zhifu", "天芮", layer="本命", gong=2),
        _f("dipan_gan", "丙", layer="本命", gong=2),
        _f("tianpan_gan", "庚", layer="本命", gong=2),
    ]
    check("  值符宫地盘干为丙 → 龙回首成立", _ev.evaluate(qrules["QM-P01"], chart)["verdict"], "满足")
    check("  值符宫天盘干为庚 → 伏宫成立", _ev.evaluate(qrules["QM-P31"], chart)["verdict"], "满足")
    check(
        "  鸟跌穴要天盘丙在值符宫（本例丙在 3 宫）→ 不成立",
        _ev.evaluate(qrules["QM-P02"], chart)["verdict"],
        "不满足",
    )
    check(
        "  值符宫地盘干不是丙 → 不成立",
        _ev.evaluate(qrules["QM-P01"], [_f("zhifu", "天芮", layer="本命", gong=2), _f("dipan_gan", "戊", layer="本命", gong=2)])["verdict"],
        "不满足",
    )

    print("4. 甲不得作为取值（甲寄六仪）")
    for f in ("references/vocab/fact-vocab.json", str(PRODUCT_VOCAB)):
        v = json.loads((ROOT / f).read_text(encoding="utf-8")) if not f.startswith("/") else json.loads(Path(f).read_text(encoding="utf-8"))
        for key in ("tianpan_gan", "dipan_gan"):
            dom = v["values"].get(key) or []
            check(f"  {f.split('/')[-1]} {key} 值域 9 干且无甲", (len(dom), "甲" in dom), (9, False))

    print("5. 仍未映射的同类规则不得被顺手映射（且原因要写清）")
    # t188 更新：QM-P27 岁格**已映射**——用「枚举有限域＋分支内配对」表达了跨键相等
    # （见 tools/map-qimen-lin-pairs.py）；这里改钉它的形态，而不再钉「仍为空」。
    qm27 = rules["QM-P27"].get("applicable_to")
    check("  QM-P27 已映射且为枚举配对式", isinstance(qm27, dict) and "any_of" in qm27, True)
    check(
        "  QM-P27 全式无通配",
        any(x.get("value") == "*" for x in __import__("predicate_lang").iter_usable_predicates(qm27)),
        False,
    )
    # QM-P26 直使加地丁：**现在仍不映射，但理由变了** ——
    # 不再是「会撞 15% 闸门」（qimen 变大后闸门已有余量），而是它必须写成
    # 「值使门所在宫的地盘干＝丁」，其中值使门名随盘而变 → 需要**无取值子句**（存在性），
    # 而「无取值子句算不算通配、算不算凑数」这条口径尚未裁定（t179 待授权项 ①）。
    faqiao = {
        r["rule_id"]: r
        for r in yaml.safe_load(
            (ROOT / "references/books/san-shi/qimen-faqiao/rules.yaml").read_text(encoding="utf-8")
        )["rules"]
    }
    check("  QM-P26 仍为空（需无取值子句，口径待裁定）", faqiao["QM-P26"].get("applicable_to") or [], [])
    # 计数必须走共享的叶子遍历：v3 组里的通配（如 {all_of:[{value:"*"}]}）
    # 用「只看平铺列表」的朴素写法**数不到**——这正是 t168 修过的那类缺陷。
    sys.path.insert(0, str(ROOT / "tools"))
    from predicate_lang import iter_usable_predicates  # noqa: E402

    both = dict(rules)
    both.update(faqiao)
    wild = sum(
        1
        for r in both.values()
        if any(x.get("value") == "*" for x in iter_usable_predicates(r.get("applicable_to")))
    )
    total = sum(1 for r in both.values() if r.get("applicable_to"))
    print(f"     qimen 实测：通配 {wild}/{total} = {wild / total * 100:.1f}%（须 ≤15%）")
    # t188 起不再断言「再加一条就会超限」——qimen 谓词数已从 24 增到 35，
    # 闸门有余量了；继续钉那条旧算术就是钉一条**已经不成立**的结论（t187 才刚记过这类教训）。
    check("  闸门尚有明确余量（<13%）", wild / total < 0.13, True)
    check("  若再加一条存在性通配仍在闸门内（应即时重算而非引用旧数）", (wild + 1) / (total + 1) <= 0.15, True)

    if FAILED:
        print(f"\n{len(FAILED)} 项失败:", file=sys.stderr)
        for f in FAILED:
            print("  " + f, file=sys.stderr)
        return 1
    print("\nALL QIMEN-STEM MAP OK")
    return 0


if __name__ == "__main__":
    sys.exit(main())