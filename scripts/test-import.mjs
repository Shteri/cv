// Tests for app/history-import.js: a dealer-system export (one row per part / labour line) and a simple visits table.
const root = new URL("../", import.meta.url).pathname;
await import(root + "app/history-import.js");
const I = globalThis.TipulitImport;
import { readFileSync } from "node:fs";
const items = JSON.parse(readFileSync(root + "data/items.json", "utf8")), keys = Object.keys(items.items || items);
let fail = 0;
const check = (label, ok, got) => { console.log(`${ok ? "OK  " : "FAIL"} ${label}${ok ? "" : " got " + JSON.stringify(got)}`); if (!ok) fail++; };

// a garage system export: one row per line, extra columns the importer does not use (branch code, card, codes, type)
const H = ["תא.פתיחה", "מוסך", "כרטיס", "חשבונית", "מד אוץ", "ש.מ", "סוג", "אח.", "מספר פריט/עבודה", "תיאור פריט/עבודה", "כמות", "שם מוסך"];
const L = (d, card, km, type, code, desc, qty = 1) => [d, 10, card, null, km, 0, type, "ל", code, desc, qty, "מוסך הדוגמה 10"];
const rows = [H,
  L("27/06/2022", 84053, 110405, "ע", "*", "אישור עבודה חתום"),
  L("27/06/2022", 84053, 110405, "ע", "0010H01", "טיפול שנה שמינית", 0.85),
  L("27/06/2022", 84053, 110405, "חלק", "ALFA-M", "חולצה ממותגת"),
  L("27/06/2022", 84053, 110405, "חלק", 73500049, "מסנן שמן"),
  L("27/06/2022", 84053, 110405, "חלק", "70547", "2LT שמן מנוע 5W40", 2),
  L("17/03/2022", 82659, 104903, "ע", "3330D30", "פ + ה משאבת ואקום", 0.8),
  L("17/03/2022", 82659, 104903, "חלק", 55233645, "אטם מש ואקום"),
  [new Date(2019, 9, 7), 10, 73152, null, 69777, null, "חלק", "ל", 50511785, "מסנן אויר מזגן GIULIETTA", 1, "מוסך הדוגמה 10"],
  [new Date(2019, 9, 7), 10, 73152, null, 69777, null, "חלק", "ל", 51854025, "קרב מסנן אויר GIULIETTA", 1, "מוסך הדוגמה 10"],
  [new Date(2019, 9, 7), 10, 73155, null, 69777, null, "ע", "ל", "1032B10", "פ + ה רצועת תזמון", 1.8, "מוסך הדוגמה 10"],
  [new Date(2019, 9, 7), 10, 73152, null, 69777, null, "ע", "ל", "0010K60", 'טיפול 60,000 ק"מ', 2.5, "מוסך הדוגמה 10"],
  [new Date(2019, 9, 7), 10, 73152, null, 69777, null, "חלק", "ל", 55249868, "מצת מנוע", 4, "מוסך הדוגמה 10"],
  [new Date(2019, 9, 7), 10, 73152, null, 69777, null, "חלק", "ל", 10261060, "דיסקית לפקק ריקון", 1, "מוסך הדוגמה 10"],
  ["14/07/2020", 10, 76791, null, 83984, null, "חלק", "ל", 77367959, "סט רפידות בלם קד'", 1, "מוסך הדוגמה 10"],
  ["14/07/2020", 10, 76791, null, 83984, null, "חלק", "ל", 50555748, "בקרה אלקטרונית למצבר", 1, "מוסך הדוגמה 10"],
  ["26/04/2021", 10, 79185, null, 91744, null, "ע", "ל", "*", "מתלונן על העברת הילוכים לקויה.", 0, "מוסך הדוגמה 10"],
];
const r = I.fromRows(rows, { itemKeys: keys });
const by = d => r.visits.find(v => v.day === d) || {};
check("columns: the garage name, not the branch code", r.columns && r.columns.garage === 11 && r.columns.km === 4 && r.columns.desc === 9, r.columns);
check("lines grouped into visits by date and km", r.visits.length === 5, r.visits.map(v => v.day));
check("service visit: oil and filter, merchandise and notes left out", by("2022-06-27").kind === "service" && by("2022-06-27").items.sort().join() === "engine_oil,oil_filter" && /אישור/.test(by("2022-06-27").notes), by("2022-06-27"));
check("repair visit: the work, in plain words", by("2022-03-17").kind === "repair" && /^החלפת משאבת ואקום/.test(by("2022-03-17").text), by("2022-03-17"));
check("two job cards on one day are one visit; cabin and engine air filters told apart", by("2019-10-07").items.sort().join() === "air_filter,cabin_filter,spark_plugs,timing_belt" && by("2019-10-07").kind === "service", by("2019-10-07"));
check("a battery sensor is not a battery", !by("2020-07-14").items.includes("battery_12v") && by("2020-07-14").items.includes("brake_pads"), by("2020-07-14"));
check("a visit with only notes is marked empty", by("2021-04-26").empty === true && by("2021-04-26").kind === "other");
check("garage name and km", by("2022-06-27").garage === "מוסך הדוגמה 10" && by("2022-06-27").km === 110405);

// a simple table: one row per visit, English headers, Excel serial dates, prices
const simple = I.fromRows([["Date", "Mileage", "Description", "Total"], [44927, "45,200", "Oil service, oil filter", 890], [45292, 60100, "Brake pads", "1,200"]], { itemKeys: keys });
check("simple table: serial dates, km with commas, prices", simple.visits.length === 2 && simple.visits[1].day === "2023-01-01" && simple.visits[1].km === 45200 && simple.visits[1].price === 890 && simple.visits[1].items.sort().join() === "engine_oil,oil_filter" && simple.visits[0].items.includes("brake_pads"), simple.visits);
// headers that mean nothing: the content decides (dates, km that grows with them, the longest text, a repeating name)
const blind = I.fromRows([["A", "B", "C", "D", "E"],
  ["12/01/2023", 4471, 45200, "החלפת שמן ומסנן שמן, מסנן אוויר", "מוסך השכונה"],
  ["03/02/2024", 5120, 61100, "רפידות בלם קדמיות", "מוסך השכונה"],
  ["20/08/2022", 3980, 30050, "טיפול 30,000", "מוסך השכונה"]], { itemKeys: keys });
check("unknown headers: columns found by content", blind.columns && blind.columns.date === 0 && blind.columns.km === 2 && blind.columns.desc === 3 && blind.columns.garage === 4, blind.columns);
check("unknown headers: visits read", blind.visits.length === 3 && blind.visits[0].km === 61100 && blind.visits[0].items.includes("brake_pads") && blind.visits[1].items.sort().join() === "air_filter,engine_oil,oil_filter", blind.visits);
check("no date or km column: nothing guessed", I.fromRows([["שם", "טלפון"], ["דני", "050"]]).visits.length === 0);
check("km per month from readings", I.kmPerMonth([{ day: "2015-01-01", km: 1000 }, { day: "2022-06-27", km: 110405 }]) === 1200 && I.kmPerMonth([{ day: "2022-01-01", km: 1000 }, { day: "2022-03-01", km: 3000 }]) === null);
if (fail) { console.error(`${fail} failed`); process.exit(1); }
console.log("import ok");
