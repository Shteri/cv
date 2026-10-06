// Service history from a spreadsheet: any table with dates and odometer readings, whether one row per visit or
// one row per part / labour line (several rows of the same date and km are one visit).
// Columns are found by universal meaning only: date, km, description, garage, price. Header words help when present;
// otherwise the content decides (the column of dates, the column of km that grows with the dates, the longest text).
// Pure: rows in (arrays of cells, as SheetJS sheet_to_json(header: 1) gives them), visits out. Exposes TipulitImport.
(function (g) {
  const norm = s => String(s == null ? "" : s).replace(/["'״׳`]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
  // general words for each field, in Hebrew and English
  const WORDS = {
    date: /תאריך|^date|^day$|^when$/,
    km: /קמ\b|ק\.מ|קילומט|מד ?או?ץ|odometer|mileage|^odo|^km/,
    desc: /תיאור|פירוט|עבוד|פריט|description|details|^work|^item|^service/,
    garage: /מוסך|garage|workshop|^ספק|vendor|^where$|^מקום$/,
    price: /מחיר|סכום|סהכ|עלות|תשלום|price|amount|total|cost|paid/,
  };
  const FIELDS = Object.keys(WORDS);
  const filled = v => v != null && String(v).trim() !== "";
  const numOf = v => typeof v === "number" ? v : /^[\d,.\s]+$/.test(String(v).trim()) ? Number(String(v).replace(/[^\d.]/g, "")) : NaN;
  function columns(rows) {
    // the header row: the first of the top rows with at least two general words
    let head = -1, cols = {};
    for (let i = 0; i < Math.min(rows.length, 15) && head < 0; i++) {
      const found = {};
      (rows[i] || []).forEach((cell, c) => { const h = norm(cell); if (!h || typeof cell === "number") return; for (const f of FIELDS) if (!(f in found) && !Object.values(found).includes(c) && WORDS[f].test(h)) { found[f] = c; break; } });
      if (Object.keys(found).length >= 2) { head = i; cols = found; }
    }
    const body = rows.slice(head + 1).filter(r => r && r.some(filled)), sample = body.slice(0, 300);
    const width = Math.max(0, ...sample.map(r => r.length)), taken = () => new Set(Object.values(cols));
    const share = (c, test) => { const vals = sample.map(r => r[c]).filter(filled); return vals.length ? vals.filter(test).length / vals.length : 0; };
    // a column of dates (real dates or written dates; bare numbers only when the header says so)
    if (cols.date === undefined) for (let c = 0; c < width; c++) if (!taken().has(c) && share(c, v => typeof v !== "number" && toDay(v)) >= 0.6) { cols.date = c; break; }
    // a header named the date column but its cells are not dates: drop it
    if (cols.date !== undefined && share(cols.date, v => toDay(v)) < 0.6) delete cols.date;
    // km: numbers between 100 and 2,000,000 that grow with the dates (an order or card number grows too, but less evenly)
    if (cols.km === undefined) {
      const order = cols.date !== undefined ? sample.map((r, k) => ({ k, d: toDay(r[cols.date]) })).filter(x => x.d) : [];
      let best = null;
      for (let c = 0; c < width; c++) {
        if (taken().has(c) || share(c, v => { const n = numOf(v); return n >= 100 && n <= 2e6; }) < 0.6) continue;
        const pts = order.map(x => ({ d: x.d, n: numOf(sample[x.k][c]) })).filter(x => x.n > 0).sort((a, b) => a.d.localeCompare(b.d));
        let up = 0; for (let k = 1; k < pts.length; k++) if (pts[k].n >= pts[k - 1].n) up++;
        // and a believable pace: 150 to 8,000 km a month between the first and the last reading
        const a = pts[0], z = pts[pts.length - 1], months = a && z ? (Date.parse(z.d) - Date.parse(a.d)) / (30.44 * 86400000) : 0;
        const pace = months > 1 ? (z.n - a.n) / months : null, sane = pace === null || (pace >= 150 && pace <= 8000);
        const score = (pts.length > 1 ? up / (pts.length - 1) : 0) + (sane ? 1 : 0);
        const big = Math.max(...pts.map(x => x.n), 0);
        if (!best || score > best.score || (score === best.score && big > best.big)) best = { c, score, big };
      }
      if (best && (best.score >= 1.6 || cols.date === undefined)) cols.km = best.c;
    }
    // a header word can point at a code column ("item number"): a description must be words
    if (cols.desc !== undefined && share(cols.desc, v => /[a-zא-ת]{2}/i.test(String(v)) && !/^[\w\-*./]+$/.test(String(v).trim())) < 0.6) delete cols.desc;
    // description: the text column with the longest cells; garage: a short text that repeats
    const texts = [];
    for (let c = 0; c < width; c++) {
      if (taken().has(c)) continue;
      const vals = sample.map(r => r[c]).filter(filled).map(String);
      if (vals.length < sample.length * 0.4 || share(c, v => /[a-zא-ת]/i.test(String(v))) < 0.7) continue;
      texts.push({ c, len: vals.reduce((a, v) => a + v.length, 0) / vals.length, distinct: new Set(vals).size, n: vals.length });
    }
    if (cols.desc === undefined) { const d = texts.filter(t => t.len >= 4).sort((a, b) => b.len - a.len)[0]; if (d) cols.desc = d.c; }
    if (cols.garage !== undefined && share(cols.garage, v => /[a-zא-ת]/i.test(String(v))) < 0.7) delete cols.garage;   // a branch code, not a name
    if (cols.garage === undefined) { const gcol = texts.filter(t => t.c !== cols.desc && t.distinct <= Math.max(2, t.n * 0.3) && t.len >= 3).sort((a, b) => a.distinct / a.n - b.distinct / b.n)[0]; if (gcol) cols.garage = gcol.c; }
    if (cols.date === undefined && cols.km === undefined) return null;
    return { row: head, cols };
  }
  const pad = n => String(n).padStart(2, "0");
  // a Date, an Excel serial day, or text: 27/06/2022, 27.6.22, 2022-06-27
  function toDay(v) {
    if (v == null || v === "") return null;
    if (v instanceof Date && !isNaN(v)) return `${v.getFullYear()}-${pad(v.getMonth() + 1)}-${pad(v.getDate())}`;
    if (typeof v === "number" && v > 20000 && v < 80000) { const d = new Date(Date.UTC(1899, 11, 30) + v * 86400000); return `${d.getUTCFullYear()}-${pad(d.getUTCMonth() + 1)}-${pad(d.getUTCDate())}`; }
    const s = String(v).trim();
    let m = s.match(/^(\d{4})-(\d{1,2})-(\d{1,2})/); if (m) return `${m[1]}-${pad(m[2])}-${pad(m[3])}`;
    m = s.match(/^(\d{1,2})[./-](\d{1,2})[./-](\d{2,4})/);
    if (m) { const y = m[3].length === 2 ? 2000 + +m[3] : +m[3]; return `${y}-${pad(m[2])}-${pad(m[1])}`; }
    return null;
  }
  const toNum = v => { if (v == null || v === "") return null; const n = typeof v === "number" ? v : Number(String(v).replace(/[^\d.-]/g, "")); return Number.isFinite(n) && n !== 0 ? n : null; };

  // description -> maintenance item key; order matters (an oil filter is not oil, a cabin filter is not an engine air filter)
  const ITEMS = [
    [/מסנן ?שמן|oil filter/i, "oil_filter"],
    [/מסנן ?(אוו?יר ?)?(מזגן|לתא|תא ?נוסעים|אבקה|פחם|פוליאן)|cabin/i, "cabin_filter"],
    [/מסנן ?אוו?יר|air filter/i, "air_filter"],
    [/מסנן ?דלק|fuel filter/i, "fuel_filter"],
    [/שמן ?(גיר|תיבה|תמסורת)|\batf\b|\bdsg\b|\bcvt\b/i, "transmission_oil"],
    [/שמן|\b\d{1,2}w-?\d{2}\b|engine oil|\boil (change|service)\b/i, "engine_oil"],
    [/מצת|spark plug/i, "spark_plugs"],
    [/נוזל ?בלמים|\bdot ?\d\b|brake fluid/i, "brake_fluid"],
    [/נוזל ?(קירור|קרור)|אנטיפריז|coolant/i, "coolant"],
    [/רפיד|brake pad/i, "brake_pads"],
    [/דיסק(י|ים|ית)? ?(ה)?בלמ|brake disc/i, "brake_discs"],
    [/רצועת ?תזמון|ער(כת)? ?תזמון|timing belt/i, "timing_belt"],
    [/רצועת ?(עזר|אלטרנטור|מזגן)|חגו?\.? ?מנוע|\b\d+pk\d+\b/i, "drive_belt"],
    [/בקרה.*מצבר|חיישן.*מצבר/, null],
    [/מצבר|battery/i, "battery_12v"],
    [/מגב|wiper/i, "wipers"],
    [/גז ?מזגן/, "ac_refrigerant"],
  ];
  const itemOf = desc => { for (const [re, k] of ITEMS) if (re.test(desc)) return k; return undefined; };
  // every item a phrase names: what a rule matched is taken out before the next rule ("שמן ומסנן שמן" = oil and filter)
  function itemsOf(desc) {
    let t = desc, hit = false; const keys = [];
    for (const [re, k] of ITEMS) if (re.test(t)) { hit = true; if (k && !keys.includes(k)) keys.push(k); t = t.replace(new RegExp(re.source, re.flags.includes("g") ? re.flags : re.flags + "g"), " "); }
    return { keys, hit };
  }
  // lines that are notes to the customer or the office, and merchandise, are not work on the car
  const NOTE = /^(\*|יש |בוצע|מתלונן|אישור|הנחה|מזל טוב|עבודה ללא|ע\.?חוץ|נשלח|לקוח)/;
  const MERCH = /חולצה|מטריה|כובע|מחזיק מפתחות|שטיפת רכב|תוסף (דלק|בנזין)|נוזל (ניקוי|שטיפת)|ממותג|דיסקית לפקק|אטם בורג ריקון/;
  const SERVICE = /טיפול(?! ללא)|service|maintenance/i;
  const tidy = s => s.replace(/^פ ?\+ ?ה /, "החלפת ").replace(/\s+/g, " ").trim();

  function fromRows(rows, opts = {}) {
    const keys = opts.itemKeys ? new Set(opts.itemKeys) : null;
    const head = columns(rows || []);
    if (!head) return { visits: [], columns: null, error: "no_columns" };
    const c = head.cols, byKey = new Map();
    let lines = 0;
    for (const r of rows.slice(head.row + 1)) {
      if (!r || r.every(x => x == null || x === "")) continue;
      const day = c.date !== undefined ? toDay(r[c.date]) : null, km = c.km !== undefined ? toNum(r[c.km]) : null;
      if (!day && !km) continue;
      lines++;
      const key = `${day || ""}|${km || ""}`;
      const v = byKey.get(key) || { day, date: day ? day.slice(0, 7) : null, km: km && km > 0 ? Math.round(km) : null, garage: null, items: new Set(), works: [], notes: [], price: 0, service: false };
      if (c.garage !== undefined && r[c.garage] != null && !v.garage) v.garage = String(r[c.garage]).trim() || null;
      const desc = c.desc !== undefined && r[c.desc] != null ? String(r[c.desc]).trim() : "";
      const price = c.price !== undefined ? toNum(r[c.price]) : null;
      if (price) v.price += price;
      if (desc) {
        if (NOTE.test(desc)) v.notes.push(desc.replace(/^\*\s*/, ""));
        else if (!MERCH.test(desc)) {
          if (SERVICE.test(desc)) v.service = true;
          // a visits table may list several parts in one cell: "oil service, oil filter, brake pads"
          for (const part of desc.split(/;|,(?!\d{3})/).map(x => x.trim()).filter(Boolean)) {
            const m = itemsOf(part);
            for (const k of m.keys) if (!keys || keys.has(k)) v.items.add(k);
            if (!m.hit && !SERVICE.test(part)) v.works.push(tidy(part));
          }
        }
      }
      byKey.set(key, v);
    }
    const visits = [...byKey.values()].map(v => {
      const items = [...v.items], service = v.service || (items.includes("engine_oil") && items.includes("oil_filter"));
      const kind = service ? "service" : items.length || v.works.length ? "repair" : "other";
      return { day: v.day, date: v.date, km: v.km, garage: v.garage, kind, items, text: [...new Set(v.works)].join(", ").slice(0, 200) || null,
        notes: v.notes.join(" · ").slice(0, 200) || null, price: v.price ? Math.round(v.price) : null, empty: kind === "other" };
    }).sort((a, b) => (b.day || "").localeCompare(a.day || "") || (b.km || 0) - (a.km || 0));
    return { visits, columns: c, lines };
  }

  // km per month from dated odometer readings (oldest and newest at least 6 months apart), or null
  function kmPerMonth(points) {
    const p = points.filter(x => x.km > 0 && x.day).sort((a, b) => a.day.localeCompare(b.day));
    if (p.length < 2) return null;
    const a = p[0], b = p[p.length - 1], months = (Date.parse(b.day) - Date.parse(a.day)) / (30.44 * 86400000);
    if (months < 6 || b.km <= a.km) return null;
    return Math.max(200, Math.min(6000, Math.round((b.km - a.km) / months / 50) * 50));
  }

  g.TipulitImport = { fromRows, kmPerMonth, toDay, itemOf };
})(typeof window !== "undefined" ? window : globalThis);
