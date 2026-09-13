/** t8 追加：专门触发 ZSB-E-09（旬空）确认它也能在逐爻焦点里回来。 */
import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { buildLiuyaoFreeReading } from "./src/lib/engine/liuyao-free-reading";

const STEMS = "甲乙丙丁戊己庚辛壬癸";
const BRANCHES = "子丑寅卯辰巳午未申酉戌亥";
const dayGanZhi: string[] = [];
for (let i = 0; i < 60; i++) dayGanZhi.push(STEMS[i % 10]! + BRANCHES[i % 12]!);

const patterns = ["○阴阴阴阴阴", "阴阴阴阴阴阴", "阳阴阴阳阴阴", "阴阴阳阳阴阳"];
const lines = (symbols: string): LiuyaoLines =>
  [...symbols].map((s) => ({ yin: s === "阳" || s === "○" ? 1 : 0, moving: s === "○" || s === "ㄨ" })) as unknown as LiuyaoLines;

let charts = 0;
let overviewHasE09 = 0;
let lineFocusMissingE09 = 0;
const sample: unknown[] = [];
for (const day of dayGanZhi) {
  for (const p of patterns) {
    let chart;
    try {
      chart = buildLiuyao({ lines: lines(p), dayGanZhi: day, monthZhi: "卯", useRelative: "世爻" } as never);
    } catch {
      continue;
    }
    charts++;
    const ovIds = buildLiuyaoFreeReading(chart).points.map((x) => String(x.instanceId ?? x.id));
    const e09 = ovIds.filter((id) => id.includes("ZSB-E-09"));
    if (!e09.length) continue;
    overviewHasE09++;
    if (sample.length < 3) sample.push({ day, p, ovIds: e09 });
    for (let li = 0; li < 6; li++) {
      const ids = new Set(buildLiuyaoFreeReading(chart, { lineIndex: li }).points.map((x) => String(x.instanceId ?? x.id)));
      if (!e09.every((id) => ids.has(id))) lineFocusMissingE09++;
    }
  }
}
console.log(JSON.stringify({ tree: process.cwd(), charts, overviewHasE09, lineFocusMissingE09, sample }, null, 1));
