// What each AI task asks Claude and what it must return. Pure (no I/O), so scripts/test-ai.mjs can check it.
// The client sends a short Hebrew note plus context it already has (the car, schedule state, stock, catalog);
// Claude returns structured data that the client shows for review before anything is saved.
import { z } from "zod";

export type Task = "wo" | "insp" | "record" | "quote" | "receipt";
export const GARAGE_TASKS: Task[] = ["wo", "insp"];
export const LIMITS = { garage: 300, driver: 40 };   // requests per user per day
export const MAX_NOTE = 2000, MAX_CONTEXT = 40000;  // characters
// receipt: one photo (JPEG/PNG/WebP, shrunk on the device) or a PDF, base64
export const FILE_TYPES = ["image/jpeg", "image/png", "image/webp", "application/pdf"];
export const MAX_FILE = 6_000_000;  // base64 characters, about 4.5 MB

const WoLine = z.object({
  type: z.enum(["part", "labor"]),
  desc: z.string().describe("Short Hebrew description, e.g. 'רפידות בלם קדמיות' or 'עבודה'"),
  qty: z.number().describe("Quantity; liters for oil when a liter stock part is used; 1 for labour"),
  price: z.number().nullable().describe("Unit price in ILS only if the note states it, else null (the system prices from stock and the catalog)"),
  hours: z.number().nullable().describe("Labour hours if the note states them, else null"),
  part_id: z.string().nullable().describe("id from STOCK when the line is that stock part, else null"),
  item: z.string().nullable().describe("key from ITEMS that this part replaces, else null"),
  job_id: z.string().nullable().describe("id from CATALOG when a labour line is that job, else null"),
});
export const schemas = {
  wo: z.object({
    kind: z.enum(["service", "repair"]).describe("service = periodic maintenance by the schedule; repair = anything else"),
    svc_km: z.number().int().nullable().describe("For service: the service interval in km, e.g. 'טיפול 60' = 60000; else null"),
    km: z.number().int().nullable().describe("Odometer reading if stated, else null"),
    lines: z.array(WoLine),
    notes: z.string().nullable().describe("Anything else worth keeping, in Hebrew, else null"),
  }),
  insp: z.object({
    checks: z.array(z.object({
      key: z.string().describe("key from CHECKLIST"),
      status: z.enum(["ok", "soon", "now"]).describe("now = needs fixing now / dangerous; soon = worn, fix in the coming months; ok = fine"),
      note: z.string().nullable().describe("Short Hebrew detail from the note, e.g. 'נשארו 2 מ\"מ', else null"),
    })),
    rest_ok: z.boolean().describe("true if the note says everything else is fine"),
  }),
  record: z.object({
    kind: z.enum(["service", "repair", "other"]),
    date: z.string().nullable().describe("YYYY-MM if stated (use TODAY for relative dates like 'אתמול'), else null"),
    km: z.number().int().nullable(),
    price: z.number().int().nullable().describe("Total paid in ILS, else null"),
    garage: z.string().nullable(),
    city: z.string().nullable(),
    where: z.enum(["importer", "independent", "self"]).nullable().describe("importer = importer's service center; independent = private garage; self = the driver did it"),
    svc_km: z.number().int().nullable().describe("For service: interval km, e.g. 'טיפול 60 אלף' = 60000"),
    items: z.array(z.string()).describe("Keys from ITEMS that were replaced"),
    text: z.string().nullable().describe("For repair/other: one short Hebrew line, else null"),
  }),
  receipt: z.object({
    kind: z.enum(["service", "repair", "other"]).describe("service = periodic maintenance; repair = a fault fixed or a part replaced outside the routine; other = anything else"),
    date: z.string().nullable().describe("Service date as YYYY-MM, or null if not on the document"),
    km: z.number().int().nullable().describe("Odometer at this visit: as printed or handwritten on the document; if missing, inferred from the date and HISTORY (see the rules); null only when there is no date either"),
    km_estimated: z.boolean().describe("true when km is not on the document and you inferred it; false when it is printed or handwritten"),
    price: z.number().int().nullable().describe("Total paid in ILS including VAT, else null"),
    garage: z.string().nullable().describe("Garage or business name as printed, else null"),
    city: z.string().nullable().describe("City of the garage if printed, else null"),
    where: z.enum(["importer", "independent"]).nullable().describe("importer = an importer's own service center (e.g. יוניון מוטורס, כלמוביל, טלקאר, דלק מוטורס, צ'מפיון); independent = any other garage; null if unclear"),
    svc_km: z.number().int().nullable().describe("For a periodic service: the km of the SCHEDULE_SERVICES entry this visit was (see the rules); else null"),
    items: z.array(z.string()).describe("Keys from ITEMS that were REPLACED or refilled according to the document (not just inspected)"),
    text: z.string().nullable().describe("One short Hebrew line naming the work beyond the routine service, e.g. 'החלפת מצבר' or 'החלפת צינור מזגן', else null"),
    confidence: z.enum(["high", "medium", "low"]).describe("How readable and complete the document was"),
    duplicate_of: z.string().nullable().describe("id of the HISTORY record that is this same visit (see the rules), else null"),
    notes: z.string().nullable().describe("Anything the driver should double-check, in Hebrew, else null"),
  }),
  quote: z.object({
    lines: z.array(z.object({
      desc: z.string().describe("Short Hebrew name of the work or part"),
      price: z.number().nullable(),
      item: z.string().nullable().describe("key from ITEM_STATE, else null"),
      due: z.enum(["due", "soon", "not_yet", "not_in_schedule", "unknown"]).describe("Judged ONLY from ITEM_STATE and SCHEDULE"),
      note: z.string().nullable().describe("One short Hebrew sentence why, else null"),
    })),
    total: z.number().nullable(),
    price_verdict: z.enum(["fair", "high", "low", "unknown"]).describe("Judged ONLY against COMMUNITY_PRICES; unknown when they don't cover this work"),
    summary: z.string().describe("2-3 short Hebrew sentences for the driver"),
    questions: z.array(z.string()).describe("Up to 3 short Hebrew questions worth asking the garage"),
  }),
};
export type Result<T extends Task> = z.infer<(typeof schemas)[T]>;

export const SYSTEM: Record<Task, string> = {
  wo: `You turn an Israeli mechanic's short Hebrew note into lines of a work order. The context lists the car, the garage's STOCK (parts with ids), its CATALOG of standard jobs (ids, hours) and the maintenance ITEMS (keys).
Use only ids and keys that appear in the context. When the note names a part that matches a stock part, set part_id and item and leave price null. Put labour as its own line: when it matches a catalog job set job_id; when the note gives hours put them in hours. Never make up a price the note doesn't state. Write desc in short Hebrew.`,
  insp: `You map an Israeli mechanic's short Hebrew inspection note onto a fixed CHECKLIST of keys. Return one entry per checklist item the note mentions, with status now/soon/ok and a short Hebrew note with any measurement. Do not return items the note doesn't mention; set rest_ok when the note says the rest is fine.`,
  record: `You turn an Israeli driver's short Hebrew description of a garage visit into a service record. Use only item keys from ITEMS. Leave a field null when the description doesn't give it; never guess numbers.`,
  receipt: `You read an Israeli car service receipt or invoice (Hebrew, sometimes English; a photo or a PDF) and turn it into one structured record. The context gives the car (current km, km per month), TODAY, the car's HISTORY (every record so far: id, date, km, kind, service, garage, price, parts, description), the importer's SCHEDULE_SERVICES (km of each periodic service, repeating every CYCLE_KM) and the maintenance ITEMS (keys with Hebrew names).
Read the document as a mechanic would and reason about it:
- date: the visit date on the document, as YYYY-MM.
- km: use the odometer printed in the km field, or written by hand anywhere on the page. Garages often leave the km field empty; then infer the odometer for the visit date from HISTORY (interpolate between the visits around it, or extrapolate from the nearest visit or from today's km at KM_PER_MONTH), round to the nearest 100 and set km_estimated. Never copy today's km for an older visit.
- "טיפול 15000" and the like usually name the garage's service interval or the service type, not the odometer. For a periodic service, set svc_km to the SCHEDULE_SERVICES entry closest to the odometer at the visit (considering the cycle repeats), so "טיפול 15000" at about 147,000 km is the 150,000 service when the schedule has one there.
- kind: "service" when the document includes a periodic service (oil, filters, "טיפול"), even if other work was done too; then put the other work in text. "repair" for fault fixes and part replacements without a periodic service.
- items: parts replaced or refilled (oil, filters, plugs, fluids, pads, battery, AC gas after "ואקום ומילוי גז", etc.), mapped to ITEMS keys only; ignore inspections, cleaning additives and merchandise.
- price: the final total paid including VAT, in ILS.
- duplicate_of: drivers upload the same receipt twice, or another photo of it. If a HISTORY record is this same visit (same month and the same total, or the same garage and the same work within a few weeks), return its id; a different visit to the same garage is not a duplicate.
Use HISTORY as the car's story: the km between visits, which services were done, what was replaced when.
Put anything uncertain the driver should check, in short Hebrew, in notes.`,
  quote: `You help an Israeli driver understand a garage's quote. For each line decide whether it is due, using ONLY the car's ITEM_STATE (when each item was last replaced and when it is next due) and its importer SCHEDULE. Judge the price ONLY against COMMUNITY_PRICES (what other drivers of this model paid for this service); if they don't cover the work, price_verdict is unknown. Never use outside price knowledge. Be neutral and practical, never accuse the garage, and remember the mechanic may have seen wear the schedule can't know about. Write in plain Hebrew.`,
};

// the user message: the context as JSON, the note last
export function userMessage(task: Task, note: string, context: unknown): string {
  const today = new Date().toISOString().slice(0, 7);
  return `TODAY: ${today}\nCONTEXT:\n${JSON.stringify(context)}\n\nNOTE (${task}):\n${note}`;
}

export const EFFORT: Record<Task, "low" | "medium" | "high"> = { wo: "low", insp: "low", record: "low", quote: "medium", receipt: "high" };

// Drop anything that points outside the context, so the client can trust ids and keys.
export function clean<T extends Task>(task: T, out: Result<T>, context: any): Result<T> {
  const items = new Set<string>((context?.items || []).map((i: any) => i.key ?? i.item ?? i));
  if (task === "wo") {
    const parts = new Set((context?.stock || []).map((p: any) => p.id)), jobs = new Set((context?.catalog || []).map((j: any) => j.id));
    const o = out as Result<"wo">;
    o.lines = o.lines.filter(l => l.desc && l.desc.trim()).map(l => ({ ...l, part_id: l.part_id && parts.has(l.part_id) ? l.part_id : null, job_id: l.job_id && jobs.has(l.job_id) ? l.job_id : null, item: l.item && items.has(l.item) ? l.item : null, qty: l.qty > 0 ? l.qty : 1 }));
  }
  if (task === "insp") {
    const keys = new Set((context?.checklist || []).map((c: any) => c.key));
    const o = out as Result<"insp">; o.checks = o.checks.filter(c => keys.has(c.key));
  }
  if (task === "record" || task === "receipt") { const o = out as Result<"record">; o.items = o.items.filter(k => items.has(k)); }
  if (task === "receipt") { const o = out as Result<"receipt">, ids = new Set((context?.history || []).map((h: any) => String(h.id))); if (o.duplicate_of && !ids.has(o.duplicate_of)) o.duplicate_of = null; }
  if (task === "quote") {
    const st = new Set((context?.item_state || []).map((i: any) => i.item));
    const o = out as Result<"quote">; o.lines = o.lines.map(l => ({ ...l, item: l.item && st.has(l.item) ? l.item : null })); o.questions = o.questions.slice(0, 3);
  }
  return out;
}
