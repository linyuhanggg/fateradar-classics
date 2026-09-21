#!/usr/bin/env python3
"""跨实现一致性探针：把「经典侧判定」写成产品侧可复放的夹具（t203）。

## 为什么需要它

同一套谓词有**两个求值器**：经典侧 `tools/eval-predicates.py`（Python）与
产品侧 `evaluateApplicableTo`（TypeScript，消费方真正跑的那个）。
两边各写各的，就可能**悄悄分叉**：同一盘面、同一规则，一边判「满足」、一边判「信息不足」。

t203 手工比对过一次（`LIURENZHIYIN-004` 三态两侧一致），但手工比对不是回归。
本工具把**一组探针**（规则 × 合成盘面）连同**经典侧的判定结果**写成 JSON 夹具，
放到产品仓，由 `tests/rules/eval-agreement.test.ts` 复放并逐条比对。

夹具里的 `expected_*` 是**经典侧算出来的**，不是手抄的——这样一旦两边的三态语义分叉，
产品测试会红，而不是等到线上才发现。

用法：`python3 tools/eval-agreement-fixture.py --write`
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
PRODUCT_FIXTURE = Path("/Users/sync/code/cosmic-fortune-lab/tests/fixtures/eval-agreement-probes.json")

_spec = importlib.util.spec_from_file_location("ev_ag", ROOT / "tools/eval-predicates.py")
ev = importlib.util.module_from_spec(_spec)
sys.modules["ev_ag"] = ev
assert _spec.loader is not None
_spec.loader.exec_module(ev)


def f(key: str, value: str, **scope) -> dict:
    return {"key": key, "value": value, "scope": {"layer": "本命", **scope}, "derivedFrom": ["probe"]}


# 探针表：每条 = 一个规则 × 一组合成盘面。三种情形都要覆盖：
#   ① 成立（满足）② 明确不成立（不满足）③ 缺键（信息不足）
PROBES: list[dict] = [
    {
        "rule_id": "LIURENZHIYIN-004",
        "book": "san-shi/liuren-zhiyin",
        "why": "none_of 表达的全称判断 + 正句保证键在场（t200）",
        "cases": [
            {"name": "全无直接克且非八专", "facts": [f("liuren_ke_relation", "无直接克"), f("keti", "弹射课")]},
            {
                "name": "有下贼上",
                "facts": [f("liuren_ke_relation", "无直接克"), f("liuren_ke_relation", "下贼上"), f("keti", "弹射课")],
            },
            {"name": "全无直接克但是八专课", "facts": [f("liuren_ke_relation", "无直接克"), f("keti", "八专课")]},
            {"name": "缺键", "facts": [f("keti", "弹射课")]},
        ],
    },
    {
        "rule_id": "QM-P27",
        "book": "san-shi/qimen-dunjia-tongzhi",
        "why": "嵌套 all_of + 内层 same 的配对（t188）",
        "cases": [
            {
                "name": "岁干庚且庚压庚",
                "facts": [f("gan", "庚", pillar="year"), f("tianpan_gan", "庚", gong=9), f("dipan_gan", "庚", gong=9)],
            },
            {
                "name": "岁干庚但庚压丙",
                "facts": [
                    f("gan", "庚", pillar="year"),
                    f("tianpan_gan", "庚", gong=4),
                    f("dipan_gan", "丙", gong=4),
                    f("dipan_gan", "庚", gong=9),
                ],
            },
            {"name": "缺柱干", "facts": [f("tianpan_gan", "庚", gong=9), f("dipan_gan", "庚", gong=9)]},
        ],
    },
    {
        "rule_id": "ZENGSHANBUYI-ZR-08",
        "book": "divination/zengshan-buyi",
        "why": "5 六亲 × 6 爻 的枚举配对（t197）",
        "cases": [
            {
                "name": "用神妻财所在之爻旬空",
                "facts": [f("liuyao_yongshen", "妻财"), f("liuqin", "妻财", yao=3), f("liuyao_kong", "空", yao=3)],
            },
            {
                "name": "用神妻财在 3 爻、空在 5 爻",
                "facts": [f("liuyao_yongshen", "妻财"), f("liuqin", "妻财", yao=3), f("liuyao_kong", "空", yao=5)],
            },
            {"name": "缺用神", "facts": [f("liuqin", "妻财", yao=3), f("liuyao_kong", "空", yao=3)]},
        ],
    },
    {
        "rule_id": "SANMINGTONGH-R-02",
        "book": "bazi/sanming-tonghui",
        "why": "枚举十天干做「藏与透同值」（t195）",
        "cases": [
            {"name": "月令藏辛且天干有辛", "facts": [f("canggan", "辛", pillar="month"), f("gan", "辛", pillar="year")]},
            {"name": "月令藏辛但天干无辛", "facts": [f("canggan", "辛", pillar="month"), f("gan", "甲", pillar="year")]},
            {"name": "缺藏干", "facts": [f("gan", "辛", pillar="year")]},
        ],
    },
    {
        "rule_id": "HZL-R004",
        "book": "divination/huozhu-lin",
        "why": "6 爻 × 2 六亲 的持世配对（t194）",
        "cases": [
            {"name": "妻财持世", "facts": [f("liuqin", "妻财", yao=2), f("shiyao", "二爻", yao=2)]},
            {"name": "父母持世", "facts": [f("liuqin", "父母", yao=2), f("shiyao", "二爻", yao=2)]},
            {"name": "缺世爻", "facts": [f("liuqin", "妻财", yao=2)]},
        ],
    },
]


def build() -> dict:
    out: list[dict] = []
    for probe in PROBES:
        rules = {r["rule_id"]: r for r in ev.load_rules(probe["book"], None)}
        rule = rules.get(probe["rule_id"])
        if rule is None:
            raise SystemExit(f"找不到规则 {probe['rule_id']}（{probe['book']}）")
        cases = []
        for case in probe["cases"]:
            result = ev.evaluate(rule, case["facts"])
            cases.append(
                {
                    "name": case["name"],
                    "facts": case["facts"],
                    "expected_verdict": result["verdict"],
                }
            )
        out.append(
            {
                "rule_id": probe["rule_id"],
                "book": probe["book"],
                "why": probe["why"],
                "cases": cases,
            }
        )
    return {
        "fixture": "跨实现一致性探针",
        "generated_by": "t203",
        "method": (
            "经典侧 tools/eval-predicates.py 对每条探针求出三态，写成 expected_verdict；"
            "产品侧 tests/rules/eval-agreement.test.ts 用**同一批 facts** 复放 generated 谓词并比对。"
            "两边分叉（例如「缺键」在一侧算不满足）就会红。"
        ),
        "probes": out,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="生成跨实现一致性夹具")
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    payload = build()
    n = sum(len(p["cases"]) for p in payload["probes"])
    if args.write:
        PRODUCT_FIXTURE.parent.mkdir(parents=True, exist_ok=True)
        PRODUCT_FIXTURE.write_text(json.dumps(payload, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
        print(f"写入 {PRODUCT_FIXTURE}：{len(payload['probes'])} 条规则 / {n} 个探针")
    else:
        print(json.dumps(payload, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())