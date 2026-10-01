// Unit test for app/cloud.js without a network: node scripts/test-cloud.mjs
// Two concurrent saveCar calls for a new car must produce one insert, then an update of the same row.
import { readFileSync } from "node:fs";
const ops = [];
const fakeClient = { auth: { getSession: async () => ({ data: { session: { user: { id: "u1" } } } }), onAuthStateChange() {} },
  from: t => ({ upsert: row => ({ select: () => ({ single: async () => { await new Promise(r => setTimeout(r, 30)); const id = row.id || "row-" + ops.filter(o => !o.id).length; ops.push({ t, id: row.id }); return { data: { id }, error: null }; } }) }) }),
  storage: { from: () => ({}) } };
globalThis.window = globalThis; globalThis.location = { search: "", hash: "", href: "https://x/", origin: "https://x", pathname: "/" };
globalThis.TIPULIT_CONFIG = { SUPABASE_URL: "u", SUPABASE_ANON_KEY: "k" }; globalThis.supabase = { createClient: () => fakeClient };
eval(readFileSync(new URL("../app/cloud.js", import.meta.url), "utf8"));
const car = { schedule: "x", km: 1, history: [] };
await Promise.all([TipulitCloud.saveCar(car), TipulitCloud.saveCar(car)]);
const carOps = ops.filter(o => o.t === "cars");
const inserts = carOps.filter(o => !o.id).length;
if (inserts !== 1) { console.error(`FAIL concurrent saveCar made ${inserts} inserts`); process.exit(1); }
console.log("cloud tests passed");
