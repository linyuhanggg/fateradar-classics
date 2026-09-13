/**
 * 跨八术「解读点 ID 冒充规则/段落锚点」扫描（reviewer / t8）。
 * 判据（同 reading-point-source.tsx）：点的自身 ID 若出现在自己的 ruleIds 或 paragraphIds 里，
 * 页面会把它显示成「规则 ID · <点ID>」/「段落 ID · <点ID>」，即把白话解读点冒充古籍规则/原文锚点。
 */
import { buildZiwei } from "./src/lib/engine/ziwei";
import { buildZiweiFreeReading } from "./src/lib/engine/ziwei-free-reading";
import { buildQimen } from "./src/lib/engine/qimen";
import { buildQimenFreeReading } from "./src/lib/engine/qimen-free-reading";
import { buildLiuren } from "./src/lib/engine/liuren";
import { buildLiurenFreeReading } from "./src/lib/engine/liuren-free-reading";
import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { buildLiuyaoFreeReading } from "./src/lib/engine/liuyao-free-reading";
import { buildMeihua } from "./src/lib/engine/meihua";
import { buildMeihuaFreeReading } from "./src/lib/engine/meihua-free-reading";
import { buildXiaoliuren } from "./src/lib/engine/xiaoliuren";
import { buildXiaoliurenFreeReading } from "./src/lib/engine/xiaoliuren-free-reading";
import { buildQizheng } from "./src/lib/engine/qizheng";
import { buildQizhengFreeReading } from "./src/lib/engine/qizheng-free-reading";
import { subjectOf } from "./tests/helpers/subject";

const place = { gender: "男" as const, province: "上海", city: "上海", district: "黄浦区" };
const clockSubject = (y: number, mo: number, d: number, h: number) => ({
  ...subjectOf({ ...place, year: y, month: mo, day: d, hour: h, minute: 0 }),
  timeBasis: "clock" as const,
});
const sub = clockSubject(1990, 1, 20, 13);

const meihuaOf = (lunarDay: number) =>
  buildMeihua({
    yearBranch: "午",
    lunarMonth: 7,
    lunarDay,
    hourBranch: "申",
    monthBranch: "申",
    lunarLabel: `丙午年 7月${lunarDay}日`,
    solarLabel: "2026-09-06 16:00",
    fourPillars: "丙午 丙申 癸未 庚申",
  } as never);
const xlrOf = (lunarDay: number, hourBranch = "辰") =>
  buildXiaoliuren({ lunarMonth: 3, lunarDay, hourBranch, lunarLabel: `三月${lunarDay}日`, solarLabel: "2024-04-01 08:00" } as never);
const linesOf = (symbols: string): LiuyaoLines =>
  [...symbols].map((s) => ({ yin: s === "阳" || s === "○" ? 1 : 0, moving: s === "○" || s === "ㄨ" })) as unknown as LiuyaoLines;

type P = { instanceId?: string; id?: string; ruleIds?: readonly string[]; paragraphIds?: readonly string[] };
const offenders: Record<string, { point: string; kind: string }[]> = {};

function scan(art: string, points: readonly P[]) {
  for (const p of points) {
    const own = String(p.id ?? "");
    if (!own) continue;
    // 只有「白话解读点 ID」才算冒充：真正的规则 ID（ZSB-E-03、ZWD-E-02…）写进 ruleIds 是正确的
    if (!/free-|provenance|-missing-/.test(own)) continue;
    const inRule = (p.ruleIds ?? []).includes(own);
    const inPara = (p.paragraphIds ?? []).includes(own);
    if (!inRule && !inPara) continue;
    (offenders[art] ??= []).push({
      point: own,
      kind: [inRule ? "ruleIds" : "", inPara ? "paragraphIds" : ""].filter(Boolean).join("+"),
    });
  }
}

scan("liuyao-overview", buildLiuyaoFreeReading(buildLiuyao({ lines: linesOf("○阴阴阴阴阴"), dayGanZhi: "甲子", monthZhi: "卯", useRelative: "世爻" } as never)).points);
for (let li = 0; li < 6; li++)
  scan(`liuyao-line${li}`, buildLiuyaoFreeReading(buildLiuyao({ lines: linesOf("○阴阴阴阴阴"), dayGanZhi: "甲子", monthZhi: "卯", useRelative: "世爻" } as never), { lineIndex: li }).points);
scan("liuyao-missing", buildLiuyaoFreeReading(buildLiuyao({ lines: linesOf("○阴阴阴阴阴"), dayGanZhi: "甲子", monthZhi: "卯", useRelative: "世爻" } as never), { lineIndex: 9 }).points);

const zw = buildZiwei(sub, "2024-06-01", 12);
scan("ziwei", buildZiweiFreeReading(zw, { palace: "命宫", scope: "流年" }).points);
scan("ziwei-missing", buildZiweiFreeReading(zw, { palace: "不存在宫" }).points);

scan("qimen", buildQimenFreeReading(buildQimen(sub)).points);
scan("liuren", buildLiurenFreeReading(buildLiuren(sub)).points);
scan("qizheng", buildQizhengFreeReading(buildQizheng(sub)).points);
for (const d of [1, 7, 15]) scan("meihua", buildMeihuaFreeReading(meihuaOf(d)).points);
for (const d of [1, 5, 12]) scan("xiaoliuren", buildXiaoliurenFreeReading(xlrOf(d)).points);

const summary: Record<string, number> = {};
for (const [k, v] of Object.entries(offenders)) summary[k] = new Set(v.map((x) => x.point)).size;
console.log(JSON.stringify({ tree: process.cwd(), offenderKinds: summary, detail: Object.fromEntries(Object.entries(offenders).map(([k, v]) => [k, [...new Set(v.map((x) => `${x.point} (${x.kind})`))]])) }, null, 1));
