/** t8 追加：用六亲做用神（可能出现伏神）触发 ZSB-E-09，确认它也在逐爻焦点里回来。 */
import { buildLiuyao, type LiuyaoLines } from "./src/lib/engine/liuyao";
import { buildLiuyaoFreeReading } from "./src/lib/engine/liuyao-free-reading";

const linesOf = (bits: number, movingMask: number): LiuyaoLines =>
  Array.from({ length: 6 }, (_, i) => ({
    yin: (bits >> i) & 1 ? 0 : 1,
    moving: Boolean((movingMask >> i) & 1),
  })) as unknown as LiuyaoLines;

const REL = ["妻财", "官鬼", "父母", "子孙", "兄弟"];
const DAYS: [string, string][] = [
  ["甲子", "卯"],
  ["丙寅", "午"],
  ["戊辰", "酉"],
  ["庚午", "子"],
  ["壬申", "辰"],
];

let charts = 0;
let overviewHasE09 = 0;
let lineFocusMissingE09 = 0;
const sample: unknown[] = [];
for (const [day, month] of DAYS) {
  for (let bits = 0; bits < 64; bits += 3) {
    for (const rel of REL) {
      let chart;
      try {
        chart = buildLiuyao({ lines: linesOf(bits, 1), dayGanZhi: day, monthZhi: month, useRelative: rel } as never);
      } catch {
        continue;
      }
      charts++;
      const ovIds = buildLiuyaoFreeReading(chart).points.map((x) => String(x.instanceId ?? x.id));
      const e09 = ovIds.filter((id) => id.includes("ZSB-E-09"));
      if (!e09.length) continue;
      overviewHasE09++;
      if (sample.length < 3) sample.push({ day, bits, rel, e09 });
      for (let li = 0; li < 6; li++) {
        const ids = new Set(buildLiuyaoFreeReading(chart, { lineIndex: li }).points.map((x) => String(x.instanceId ?? x.id)));
        if (!e09.every((id) => ids.has(id))) lineFocusMissingE09++;
      }
    }
  }
}
console.log(JSON.stringify({ tree: process.cwd(), charts, overviewHasE09, lineFocusMissingE09, sample }, null, 1));
