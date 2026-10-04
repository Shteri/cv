// What each AI task asks Claude and what it must return. Pure (no I/O), so scripts/test-ai.mjs can check it.
// The client sends a short Hebrew note plus context it already has (the car, schedule state, stock, catalog);
// Claude returns structured data that the client shows for review before anything is saved.
import { z } from "zod";

export type Task = "wo" | "insp" | "record" | "quote";
export const GARAGE_TASKS: Task[] = ["wo", "insp"];
export const LIMITS = { garage: 300, driver: 40 };   // requests per user per day
export const MAX_NOTE = 2000, MAX_CONTEXT = 40000;  // characters

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
  quote: `You help an Israeli driver understand a garage's quote. For each line decide whether it is due, using ONLY the car's ITEM_STATE (when each item was last replaced and when it is next due) and its importer SCHEDULE. Judge the price ONLY against COMMUNITY_PRICES (what other drivers of this model paid for this service); if they don't cover the work, price_verdict is unknown. Never use outside price knowledge. Be neutral and practical, never accuse the garage, and remember the mechanic may have seen wear the schedule can't know about. Write in plain Hebrew.`,
};

// the user message: the context as JSON, the note last
export function userMessage(task: Task, note: string, context: unknown): string {
  const today = new Date().toISOString().slice(0, 7);
  return `TODAY: ${today}\nCONTEXT:\n${JSON.stringify(context)}\n\nNOTE (${task}):\n${note}`;
}

export const EFFORT: Record<Task, "low" | "medium"> = { wo: "low", insp: "low", record: "low", quote: "medium" };

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
  if (task === "record") { const o = out as Result<"record">; o.items = o.items.filter(k => items.has(k)); }
  if (task === "quote") {
    const st = new Set((context?.item_state || []).map((i: any) => i.item));
    const o = out as Result<"quote">; o.lines = o.lines.map(l => ({ ...l, item: l.item && st.has(l.item) ? l.item : null })); o.questions = o.questions.slice(0, 3);
  }
  return out;
}
