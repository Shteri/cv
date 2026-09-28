// Vehicle lookup against the Israeli Ministry of Transport registry on data.gov.il,
// and matching of a registry record to one of our maintenance schedules.
// Plain script: exposes window.TipulitLookup. Works in the browser and in Node (for tests).
(function (global) {
  const CKAN = "https://data.gov.il/api/3/action/datastore_search";
  // "כלי רכב פרטיים ומסחריים" (private and commercial vehicles)
  const VEHICLES = "053cea08-09bc-40ec-8f7a-156f0677aff3";

  const normalizePlate = raw => String(raw || "").replace(/\D/g, "");

  // Registry record -> our normalized vehicle shape. Field names are the registry's own.
  function normalizeRecord(r) {
    const num = v => { const n = parseInt(v, 10); return Number.isFinite(n) ? n : null; };
    const date = v => (v && /^\d{4}-\d{2}-\d{2}/.test(v)) ? v.slice(0, 10) : null;
    return {
      plate: String(r.mispar_rechev || ""),
      make_raw: r.tozeret_nm || "",          // e.g. "טויוטה יפן"
      model_raw: r.degem_nm || "",           // factory model code, e.g. "ZRE212L-DEXNKW"
      commercial_name: r.kinuy_mishari || "",// e.g. "COROLLA"
      trim: r.ramat_gimur || "",
      year: num(r.shnat_yitzur),
      engine_cc: num(r.nefach_manoa),
      engine_code: r.degem_manoa || "",
      fuel: r.sug_delek_nm || "",            // "בנזין" | "דיזל" | "חשמל/בנזין" | "חשמל" ...
      color: r.tzeva_rechev || "",
      tires_front: r.zmig_kidmi || "",
      tires_rear: r.zmig_ahori || "",
      ownership: r.baalut || "",             // "פרטי" | "חברה" | "ליסינג" ...
      on_road_since: r.moed_aliya_lakvish || "",
      last_test: date(r.mivchan_acharon_dt),
      test_expiry: date(r.tokef_dt),
      km_last_test: num(r.kilometer_test_aharon) // present only in some registry extracts
    };
  }

  async function fetchVehicle(plate, { timeoutMs = 8000, fetchImpl } = {}) {
    const digits = normalizePlate(plate);
    if (digits.length < 7 || digits.length > 8) throw new Error("bad_plate");
    const f = fetchImpl || global.fetch;
    const ctrl = typeof AbortController !== "undefined" ? new AbortController() : null;
    const t = ctrl && setTimeout(() => ctrl.abort(), timeoutMs);
    try {
      const url = `${CKAN}?resource_id=${VEHICLES}&filters=${encodeURIComponent(JSON.stringify({ mispar_rechev: Number(digits) }))}&limit=1`;
      const res = await f(url, { signal: ctrl && ctrl.signal });
      if (!res.ok) throw new Error("http_" + res.status);
      const json = await res.json();
      const rec = json && json.result && json.result.records && json.result.records[0];
      return rec ? normalizeRecord(rec) : null;
    } finally { if (t) clearTimeout(t); }
  }

  // The registry writes the maker with its country ("טויוטה יפן", "יונדאי קוריאה", "מזדה יפן").
  // Strip it and map to the English make names used in data/registry_map.json and data/models.json.
  const MAKES = [
    ["טויוטה", "Toyota"], ["אלפא", "Alfa Romeo"], ["יונדאי", "Hyundai"], ["קיה", "Kia"], ["סקודה", "Skoda"],
    ["מאזדה", "Mazda"], ["מזדה", "Mazda"], ["מיצובישי", "Mitsubishi"], ["פורד", "Ford"], ["סיאט", "Seat"],
    ["פולקסווגן", "Volkswagen"], ["סוזוקי", "Suzuki"], ["ניסאן", "Nissan"], ["הונדה", "Honda"],
    ["שברולט", "Chevrolet"], ["סובארו", "Subaru"], ["רנו", "Renault"], ["פיג'ו", "Peugeot"],
    ["סיטרואן", "Citroen"], ["אופל", "Opel"], ["צ'רי", "Chery"], ["ב.מ.וו", "BMW"], ["מרצדס", "Mercedes-Benz"],
    ["אאודי", "Audi"], ["וולוו", "Volvo"], ["לקסוס", "Lexus"], ["דאציה", "Dacia"], ["פיאט", "Fiat"], ["טסלה", "Tesla"]
  ];
  function normalizeMake(raw) {
    if (!raw) return null;
    for (const [he, en] of MAKES) if (raw.startsWith(he)) return en;
    return raw.split(" ")[0];
  }
  const isElectric = v => /^חשמל$/.test((v.fuel || "").trim());

  // Match a vehicle to a schedule using data/registry_map.json rules:
  // { make, names: [exact upper-case commercial names], years: [from, to], fuel?: [..], engine_codes?: [..], schedule }.
  // Rules with engine codes are preferred over rules without, then rules with fuel.
  function resolveSchedule(vehicle, rules) {
    if (!vehicle) return { status: "unknown" };
    if (isElectric(vehicle)) return { status: "electric" };
    const make = normalizeMake(vehicle.make_raw);
    const name = (vehicle.commercial_name || "").toUpperCase().trim();
    const year = Number(vehicle.year);
    const hits = rules.filter(r =>
      r.make === make &&
      r.names.some(n => n === name) &&
      (!year || (year >= r.years[0] && year <= r.years[1])) &&
      (!r.fuel || r.fuel.includes(vehicle.fuel)) &&
      (!r.engine_codes || r.engine_codes.includes(vehicle.engine_code)));
    const score = r => (r.engine_codes ? 2 : 0) + (r.fuel ? 1 : 0);
    hits.sort((a, b) => score(b) - score(a));
    if (hits.length) return { status: "matched", schedule: hits[0].schedule, make };
    const makeKnown = rules.some(r => r.make === make);
    const nameKnown = makeKnown && rules.some(r => r.make === make && r.names.includes(name));
    return { status: makeKnown ? (nameKnown ? "unsupported_year" : "unsupported_model") : "unsupported_make", make };
  }

  global.TipulitLookup = { normalizePlate, normalizeRecord, normalizeMake, fetchVehicle, resolveSchedule, VEHICLES };
})(typeof window !== "undefined" ? window : globalThis);
