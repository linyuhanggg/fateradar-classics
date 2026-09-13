import { buildZiwei } from "./src/lib/engine/ziwei";
import { buildZiweiFreeReading } from "./src/lib/engine/ziwei-free-reading";
import { subjectOf } from "./tests/helpers/subject";

const place = { gender: "男" as const, province: "上海", city: "上海", district: "黄浦区" };
const subject = {
  ...subjectOf({ ...place, year: 1990, month: 1, day: 20, hour: 13, minute: 20 }),
  timeBasis: "clock" as const,
};

const dates: string[] = [];
for (let y = 1920; y <= 2080; y += 40) dates.push(`${y}-01-15`, `${y}-07-15`);
dates.push("1900-01-01", "2100-12-31", "1990-01-20", "2024-06-01");

const hits: unknown[] = [];
let checked = 0;
for (const date of dates) {
  let chart;
  try {
    chart = buildZiwei(subject, date, 12);
  } catch {
    continue;
  }
  checked++;
  for (const s of chart.transit?.scopes ?? []) {
    if (s.available) continue;
    const free = buildZiweiFreeReading(chart, { palace: "命宫", scope: s.name });
    const text = free.paragraphs.join("");
    hits.push({
      date,
      name: s.name,
      sentence: /所选运限层[^。]*。/.exec(text)?.[0] ?? text.slice(-90),
      facts: (free.points[0]?.usedFacts ?? []).filter((f) => f.startsWith("运限")),
      unknownHit: (free.points[0]?.unknowns ?? []).some((u) => u.includes(s.name)),
    });
  }
}
console.log(JSON.stringify({ tree: process.cwd(), checked, hits: hits.length, sample: hits.slice(0, 4) }, null, 1));
