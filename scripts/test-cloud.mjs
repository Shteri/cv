// Unit test for app/cloud.js without a network: node scripts/test-cloud.mjs
// Two concurrent saveCar calls for a new car must produce one insert, then an update of the same row.
import { readFileSync } from "node:fs";
const ops = [], takenPlates = new Set();
const fakeClient = { auth: { getSession: async () => ({ data: { session: { user: { id: "u1" } } } }), onAuthStateChange() {} },
  from: t => ({ upsert: row => ({ select: () => ({ single: async () => { await new Promise(r => setTimeout(r, 30)); ops.push({ t, id: row.id, plate: row.plate }); if (t === "cars" && row.plate && takenPlates.has(row.plate)) return { data: null, error: { code: "23505", message: "duplicate key value violates unique constraint \"cars_plate_unique\"" } }; const id = row.id || "row-" + ops.filter(o => !o.id && o.t === t).length; return { data: { id }, error: null }; } }) }) }),
  storage: { from: () => ({}) } };
globalThis.window = globalThis; globalThis.location = { search: "", hash: "", href: "https://x/", origin: "https://x", pathname: "/" };
globalThis.TIPULIT_CONFIG = { SUPABASE_URL: "u", SUPABASE_ANON_KEY: "k" }; globalThis.supabase = { createClient: () => fakeClient };
eval(readFileSync(new URL("../app/cloud.js", import.meta.url), "utf8"));
const car = { schedule: "x", km: 1, history: [] };
await Promise.all([TipulitCloud.saveCar(car), TipulitCloud.saveCar(car)]);
const carOps = ops.filter(o => o.t === "cars");
const inserts = carOps.filter(o => !o.id).length;
if (inserts !== 1) { console.error(`FAIL concurrent saveCar made ${inserts} inserts`); process.exit(1); }
// a plate registered on another account: the car still syncs, without the plate, and is flagged
takenPlates.add("1234567"); ops.length = 0;
const sold = { plate: "12-345-67", schedule: "x", km: 1, history: [] };
await TipulitCloud.saveCar(sold);
const tries = ops.filter(o => o.t === "cars");
if (!sold.plateHold || !sold.cloudId || tries.length !== 2 || tries[1].plate !== null) { console.error("FAIL plate conflict handling", tries, sold); process.exit(1); }
console.log("cloud tests passed");
