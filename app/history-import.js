// Service history from a spreadsheet: a garage system export (one row per part or labour line, like an importer's
// DMS: date, odometer, job card, description, quantity, garage) or a simple one-row-per-visit table.
// Pure: rows in (arrays of cells, as SheetJS sheet_to_json(header: 1) gives them), visits out. Exposes TipulitImport.
(function (g) {
  const norm = s => String(s == null ? "" : s).replace(/["'״׳`]/g, "").replace(/\s+/g, " ").trim().toLowerCase();
  // header -> field; the first matching rule wins, and each column is used once
  const COLS = [
    ["date", /תאריך|תא\.? ?פתיחה|^פתיחה|^date|^day/],
    ["km", /מד ?או?ץ|^קמ$|^ק\.?מ\b|קילומט|odometer|mileage|^km$/],
    ["card", /כרטיס|הזמנת? עבודה|מס\.? ?הזמנה|work ?order|^card/],
    ["desc", /תיאור|פירוט|description|^עבודה$|^פריט$/],
    ["qty", /כמות|qty|quantity/],
    ["code", /מספר פריט|מקט|^קוד|part ?(no|number)|^code/],
    ["type", /^סוג$|^type$|סוג שורה/],
    ["garage", /שם ?מוסך|garage|workshop|^מוסך$|^ספק$/],
    ["price", /מחיר|סכום|^סהכ|price|amount|total|עלות/],
  ];
  function findHeader(rows) {
    let best = null;
    for (let i = 0; i < Math.min(rows.length, 15); i++) {
      const cols = {}, used = new Set();
      (rows[i] || []).forEach((cell, c) => {
        const h = norm(cell); if (!h) return;
        for (const [f, re] of COLS) if (!(f in cols) && !used.has(c) && re.test(h)) { cols[f] = c; used.add(c); break; }
      });
      // several "garage" columns: a numeric one is a branch code, the text one is the name
      const n = Object.keys(cols).length;
      if ((cols.date !== undefined || cols.km !== undefined) && n >= 2 && (!best || n > best.n)) best = { row: i, cols, n };
    }
    if (best && best.cols.garage !== undefined) {
      const body = rows.slice(best.row + 1, best.row + 30), numeric = c => body.filter(r => r && r[c] != null && r[c] !== "").every(r => /^\d+$/.test(String(r[c]).trim()));
      if (numeric(best.cols.garage)) {
        const alt = (rows[best.row] || []).findIndex((cell, c) => c !== best.cols.garage && /מוסך|garage/.test(norm(cell)) && !numeric(c));
        if (alt >= 0) best.cols.garage = alt; else delete best.cols.garage;
      }
    }
    return best;
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
  const toNum = v => { if (v == null || v === "") return null; const n = typeof v === "number" ? v : Number(String(v).replace(/[^\d.-]/g, "")); return Number.isFinite(n) ? n : null; };

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
  // lines that are notes to the customer or the office, and merchandise, are not work on the car
  const NOTE = /^(\*|יש |בוצע|מתלונן|אישור|הנחה|מזל טוב|עבודה ללא|ע\.?חוץ|נשלח|לקוח)/;
  const MERCH = /חולצה|מטריה|כובע|מחזיק מפתחות|שטיפת רכב|תוסף (דלק|בנזין)|נוזל (ניקוי|שטיפת)|ממותג|דיסקית לפקק|אטם בורג ריקון/;
  const SERVICE = /טיפול(?! ללא)|service|maintenance/i;
  const tidy = s => s.replace(/^פ ?\+ ?ה /, "החלפת ").replace(/\s+/g, " ").trim();

  function fromRows(rows, opts = {}) {
    const keys = opts.itemKeys ? new Set(opts.itemKeys) : null;
    const head = findHeader(rows || []);
    if (!head) return { visits: [], columns: null, error: "no_header" };
    const c = head.cols, byKey = new Map();
    let lines = 0;
    for (const r of rows.slice(head.row + 1)) {
      if (!r || r.every(x => x == null || x === "")) continue;
      const day = c.date !== undefined ? toDay(r[c.date]) : null, km = c.km !== undefined ? toNum(r[c.km]) : null;
      if (!day && !km) continue;
      lines++;
      const key = `${day || ""}|${km || ""}`;
      const v = byKey.get(key) || { day, date: day ? day.slice(0, 7) : null, km: km && km > 0 ? Math.round(km) : null, garage: null, items: new Set(), works: [], notes: [], price: 0, service: false, cards: new Set() };
      if (c.garage !== undefined && r[c.garage] != null && !v.garage) v.garage = String(r[c.garage]).trim() || null;
      if (c.card !== undefined && r[c.card] != null) v.cards.add(String(r[c.card]));
      const desc = c.desc !== undefined && r[c.desc] != null ? String(r[c.desc]).trim() : "";
      const code = c.code !== undefined && r[c.code] != null ? String(r[c.code]).trim() : "";
      const price = c.price !== undefined ? toNum(r[c.price]) : null;
      if (price) v.price += price;
      if (desc) {
        if (code === "*" || /^x$/i.test(code) || NOTE.test(desc)) v.notes.push(desc.replace(/^\*\s*/, ""));
        else if (!MERCH.test(desc)) {
          if (SERVICE.test(desc)) v.service = true;
          // a visits table may list several parts in one cell: "oil service, oil filter, brake pads"
          for (const part of desc.split(/[,;]/).map(x => x.trim()).filter(Boolean)) {
            const k = itemOf(part);
            if (k && (!keys || keys.has(k))) v.items.add(k);
            else if (k === undefined && !SERVICE.test(part)) {
              const type = c.type !== undefined ? norm(r[c.type]) : "";
              if (!type || /^ע|work|labou?r/.test(type)) v.works.push(tidy(part));
            }
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
