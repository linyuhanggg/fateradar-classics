/** 紫微运限层分支探针（reviewer / t8）：available / 在列表但不可用 / 不在列表 三分支。 */
import { buildZiwei } from "./src/lib/engine/ziwei";
import { buildZiweiFreeReading } from "./src/lib/engine/ziwei-free-reading";
import { subjectOf } from "./tests/helpers/subject";

const place = { gender: "男" as const, province: "上海", city: "上海", district: "黄浦区" };
const subject = {
  ...subjectOf({ ...place, year: 1990, month: 1, day: 20, hour: 13, minute: 20 }),
  timeBasis: "clock" as const,
};

const viewDates = [
  "1990-01-20", "1995-06-01", "2000-03-15", "2005-09-09", "2010-12-31",
  "2015-07-07", "2020-02-29", "2024-06-01", "2028-11-11", "2035-04-04", "2050-08-08",
];

const out: unknown[] = [];
const natalChart = buildZiwei(subject);
out.push({
  natalChartTransitScopes: (natalChart.transit?.scopes ?? []).length,
  natalNoScopeText: buildZiweiFreeReading(natalChart, { palace: "命宫" }).paragraphs.join("").slice(-80),
});

let availableOk = 0, availableBad = 0, unavailableOk = 0, unavailableBad = 0, absentOk = 0, absentBad = 0;
const bad: unknown[] = [];

for (const date of viewDates) {
  const chart = buildZiwei(subject, date, 12);
  const scopes = chart.transit?.scopes ?? [];
  const requests: { label: string; kind: "available" | "unavailable" | "absent"; name: string }[] = [];
  for (const s of scopes) {
    requests.push({ label: s.name, kind: s.available ? "available" : "unavailable", name: s.name });
  }
  requests.push({ label: "不存在层", kind: "absent", name: "不存在层" });
  requests.push({ label: "(none)", kind: "absent", name: "" });
  for (const r of requests) {
    const focus: { palace: string; scope?: string } = { palace: "命宫" };
    if (r.name) focus.scope = r.name;
    const free = buildZiweiFreeReading(chart, focus);
    const text = free.paragraphs.join("");
    const facts = [...(free.points[0]?.usedFacts ?? [])];
    const unknowns = [...(free.points[0]?.unknowns ?? [])];
    if (r.kind === "available") {
      const overlay = (chart.transit?.scopes ?? []).find((s) => s.name === r.name)!;
      const ok =
        text.includes(`当前运限层${r.name}${overlay.ganzhi}叠在本宫`) &&
        facts.includes(`运限层=${r.name}`);
      ok ? availableOk++ : (availableBad++, bad.push({ date, ...r, facts, tail: text.slice(-120) }));
    } else if (r.kind === "unavailable") {
      const ok =
        text.includes(`所选运限层${r.name}在当前浏览日期不可用`) &&
        !text.includes(`当前运限层${r.name}`) &&
        facts.includes("运限叠宫=信息不足");
      ok ? unavailableOk++ : (unavailableBad++, bad.push({ date, ...r, facts, tail: text.slice(-120) }));
    } else if (r.name === "") {
      // 未指定层＝本命层：不得出现任何运限层正文
      const ok = !text.includes("当前运限层") && facts.includes("运限叠宫=信息不足");
      ok ? absentOk++ : (absentBad++, bad.push({ date, ...r, facts, tail: text.slice(-120) }));
    } else {
      const ok =
        (text.includes(`所选运限层「${r.name}」不在本盘运限列表`) ||
          text.includes(`本次按本命层解读`)) &&
        !text.includes("当前运限层") &&
        unknowns.some((u) => u.includes(r.name));
      ok ? absentOk++ : (absentBad++, bad.push({ date, ...r, facts, unknowns, tail: text.slice(-140) }));
    }
  }
}

console.log(
  JSON.stringify(
    { tree: process.cwd(), availableOk, availableBad, unavailableOk, unavailableBad, absentOk, absentBad, bad: bad.slice(0, 6), natal: out },
    null,
    1,
  ),
);
