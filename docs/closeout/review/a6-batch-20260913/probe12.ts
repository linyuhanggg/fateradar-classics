/** t8 追加：导出 token 兼容性。argv[2] = 输出文件路径。打印 3 段与 4 段 token 的导出 JSON。 */
import { writeFileSync } from "node:fs";
import { exportReadingReport, readBackReadingReport } from "./src/lib/reading-input-export";
import { subjectOf } from "./tests/helpers/subject";

const place = { gender: "男" as const, province: "上海", city: "上海", district: "黄浦区" };
const base = subjectOf({ ...place, year: 1990, month: 1, day: 20, hour: 13, minute: 20 });
const subject = { ...base, arts: ["ziwei"] as const, timeBasis: "clock" as const };

const make = (focusPosition: string) =>
  exportReadingReport({
    subject: subject as never,
    focusArt: "ziwei",
    focusPosition,
    exportedAt: "2026-09-13T03:00:00.000Z",
  });

const out: Record<string, unknown> = {};
for (const [label, token] of [
  ["old3seg", "命宫@2024-06-01@12"],
  ["new4seg", "命宫@2024-06-01@12@流年"],
  ["new4segYuemo", "命宫@2024-06-01@12@流月"],
  ["new4segBogus", "命宫@2024-06-01@12@不存在层"],
  ["natalNoDate", "命宫"],
] as [string, string][]) {
  try {
    const report = make(token);
    const back = readBackReadingReport(JSON.stringify(report));
    out[label] = {
      ok: true,
      focusPosition: back.input.focusPosition,
      pointCount: back.points.length,
      factsWithTransit: back.points
        .flatMap((p) => p.usedFacts ?? [])
        .filter((f) => f.startsWith("运限") || f.startsWith("流曜")),
      firstBodyTail: String(back.points[0]?.body ?? "").slice(-60),
    };
  } catch (error) {
    out[label] = { ok: false, error: String(error).slice(0, 200) };
  }
}

if (process.argv[2]) writeFileSync(process.argv[2], JSON.stringify(make("命宫@2024-06-01@12"), null, 1), "utf8");
console.log(JSON.stringify({ tree: process.cwd(), out }, null, 1));
