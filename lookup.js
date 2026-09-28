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

  const isHybrid = v => /חשמל\/בנזין|היבריד|hybrid/i.test(v.fuel || "");
  const isPetrol = v => /בנזין/.test(v.fuel || "") && !isHybrid(v);
  const isElectric = v => /^חשמל$/.test((v.fuel || "").trim());

  // Match a vehicle to a schedule using rules in data/gov-match.json.
  // Rules: { schedule, make: regex on make_raw, model: regex on commercial_name or model_raw,
  //          not_model?: regex, years: [from, to], fuel?: "petrol"|"hybrid"|"any", cc?: [min, max] }
  function resolveSchedule(vehicle, rules) {
    if (!vehicle) return { status: "unknown" };
    if (isElectric(vehicle)) return { status: "electric" };
    const name = `${vehicle.commercial_name} ${vehicle.model_raw}`;
    const hits = rules.filter(r => {
      if (!new RegExp(r.make, "i").test(vehicle.make_raw)) return false;
      if (!new RegExp(r.model, "i").test(name)) return false;
      if (r.not_model && new RegExp(r.not_model, "i").test(name)) return false;
      if (vehicle.year && (vehicle.year < r.years[0] || vehicle.year > r.years[1])) return false;
      if (r.fuel === "hybrid" && !isHybrid(vehicle)) return false;
      if (r.fuel === "petrol" && !isPetrol(vehicle)) return false;
      if (r.cc && vehicle.engine_cc && (vehicle.engine_cc < r.cc[0] || vehicle.engine_cc > r.cc[1])) return false;
      return true;
    });
    if (hits.length === 1) return { status: "matched", schedule: hits[0].schedule };
    if (hits.length > 1) return { status: "matched", schedule: hits[0].schedule, ambiguous: hits.map(h => h.schedule) };
    // Recognized make and model but no schedule for that generation/engine yet
    const makeOnly = rules.some(r => new RegExp(r.make, "i").test(vehicle.make_raw));
    return { status: makeOnly ? "unsupported_model" : "unsupported_make" };
  }

  global.TipulitLookup = { normalizePlate, normalizeRecord, fetchVehicle, resolveSchedule, VEHICLES };
})(typeof window !== "undefined" ? window : globalThis);
