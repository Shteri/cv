// Reminders and confirmations: a list of tomorrow's (or today's) appointments with a ready WhatsApp reminder that
// carries the customer's link (/appt/?t=token): confirm, reschedule or cancel. Also the garage's no-show policy.
(function (G) {
  const { $, $$, DEMO, api, demo, esc, fmtPlate, openMsgText, setSeg, st, toast, why } = G;
  const hm = d => `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
  const KIND = { service: "טיפול", repair: "תיקון", test: "הכנה לטסט", other: "תור" };
  const apptUrl = token => location.origin + location.pathname.replace(/garage\/[^/]*$/, "") + "appt/?" + (demo ? "demo&" : "") + "t=" + token;
  let rmDay = 1, rmList = [];
  // the day the list is for: today, or the next day the garage is open
  function dayOf(offset) {
    const d = new Date(); d.setHours(0, 0, 0, 0); d.setDate(d.getDate() + offset);
    const hours = G.hoursOf ? G.hoursOf(st.garage) : null;
    for (let i = 0; offset && hours && !hours[d.getDay()] && i < 6; i++) d.setDate(d.getDate() + 1);
    return d;
  }
  const dayWord = d => { const t = new Date(); t.setHours(0, 0, 0, 0); const n = Math.round((d - t) / 86400000); return n === 0 ? "היום" : n === 1 ? "מחר" : "ב" + new Intl.DateTimeFormat("he-IL", { weekday: "long" }).format(d); };
  async function load() {
    const from = dayOf(rmDay), to = new Date(from); to.setDate(to.getDate() + 1);
    if (demo) rmList = DEMO.appts.filter(a => { const t = Date.parse(a.starts_at); return t >= from && t < to; });
    else { try { rmList = await api.appointments(st.garage.id, from.toISOString(), to.toISOString()); } catch (e) { rmList = []; toast("טעינת התורים נכשלה"); } }
    rmList = rmList.filter(a => a.status !== "no_show").sort((a, b) => Date.parse(a.starts_at) - Date.parse(b.starts_at));
    render();
  }
  const stateOf = a => a.status === "cancelled" ? ["crit", a.cancelled_by === "customer" ? "ביטל" + (a.cancelled_late ? " (מאוחר)" : "") : "בוטל"]
    : a.needs_ok ? ["warn", "צריך אישור שלך"] : a.confirmed_at ? ["ok", "אישר הגעה"] : a.status !== "booked" ? ["", "הגיע"]
    : a.reminded_at ? ["warn", "נשלחה תזכורת, עוד לא ענה"] : ["", "לא נשלחה תזכורת"];
  function render() {
    const d = dayOf(rmDay), live = rmList.filter(a => a.status !== "cancelled");
    $("#rm-title").textContent = `תזכורות · ${dayWord(d)}, ${new Intl.DateTimeFormat("he-IL", { day: "numeric", month: "long" }).format(d)}`;
    const ok = live.filter(a => a.confirmed_at).length, waiting = live.filter(a => a.status === "booked" && !a.confirmed_at && !a.needs_ok);
    $("#rm-sum").textContent = live.length ? `${live.length} תורים · ${ok} אישרו הגעה · ${waiting.length} עוד לא אישרו` : "אין תורים ביום הזה.";
    $("#rm-list").innerHTML = rmList.map(a => {
      const [tag, txt] = stateOf(a), canSend = a.status === "booked" && !a.confirmed_at && a.phone && Date.parse(a.starts_at) > Date.now();
      return `<div class="approval"><span><b>${hm(new Date(a.starts_at))} · ${esc(a.customer_name)}</b> <span class="muted small">${KIND[a.kind] || ""}${a.plate ? " · " + esc(fmtPlate(a.plate)) : ""}</span></span>
        <span class="tag ${tag}">${txt}</span>${canSend ? `<button type="button" class="btn small" data-rm="${esc(a.id)}">${a.reminded_at ? "שלח שוב" : "שלח תזכורת"}</button>` : a.phone || a.confirmed_at ? "" : `<span class="muted small">אין טלפון</span>`}</div>`;
    }).join("");
    $$("#rm-list [data-rm]").forEach(b => b.onclick = () => remind(rmList.find(a => a.id === b.dataset.rm)));
    $("#rm-hint").hidden = !rmList.some(a => !a.token);
  }
  async function remind(a) {
    if (!a) return;
    const s = new Date(a.starts_at), d = new Date(s); d.setHours(0, 0, 0, 0);
    const c = G.apCar ? G.apCar(a) : null, first = a.customer_name.split(" ")[0];
    const link = a.token ? apptUrl(a.token) : "";
    const policy = st.garage.cancel_hours ? ` אם צריך לבטל, נשמח לדעת עד ${st.garage.cancel_hours} שעות לפני.` : "";
    const text = `היי ${first}, כאן ${st.garage.name}. תזכורת לתור ${dayWord(d)} (${new Intl.DateTimeFormat("he-IL", { day: "numeric", month: "numeric" }).format(s)}) בשעה ${hm(s)}${c ? ` ל${c.model}` : ""}. `
      + (link ? `לאישור הגעה, שינוי או ביטול: ${link}` : "נשמח לאישור הגעה בתשובה להודעה.") + policy;
    // the reminder counts as sent when the message opens; the list shows who has not answered yet
    if ("reminded_at" in a || demo) { if (G.patchAppt) await G.patchAppt(a, { reminded_at: new Date().toISOString() }); else a.reminded_at = new Date().toISOString(); }
    render(); G.call("renderCalendar");
    openMsgText(a.customer_name, a.phone, text);
  }
  function open() {
    rmDay = 1; setSeg("rm-day", "1");
    $("#rm-cancel").value = String(st.garage.cancel_hours ?? 12); if (!$("#rm-cancel").value) $("#rm-cancel").value = "12";
    $("#rm-limit").value = String(st.garage.noshow_limit ?? 2); if (!$("#rm-limit").value) $("#rm-limit").value = "2";
    $("#rm-err").hidden = true; $("#rm-list").innerHTML = `<p class="muted small">טוען…</p>`;
    $("#dlg-remind").showModal(); load();
  }
  $("#cal-remind").onclick = open;
  $$("#rm-day button").forEach(b => b.onclick = () => { rmDay = +b.dataset.v; setSeg("rm-day", b.dataset.v); load(); });
  // when the message dialog closes, the list shows the new state
  $("#dlg-msg").addEventListener("close", () => { if ($("#dlg-remind").open) render(); });
  $("#rm-save").onclick = async () => {
    const patch = { cancel_hours: +$("#rm-cancel").value, noshow_limit: +$("#rm-limit").value };
    try { if (!demo) await api.updateGarageSettings(st.garage.id, patch); Object.assign(st.garage, patch); toast("המדיניות נשמרה"); $("#rm-err").hidden = true; }
    catch (e) { $("#rm-err").textContent = /cancel_hours|noshow_limit|schema cache/i.test(e.message || "") ? "השרת עוד לא מוכן (צריך להריץ את מיגרציה 0010)." : "השמירה נכשלה: " + why(e); $("#rm-err").hidden = false; }
  };

  G.addAction("appt", { module: "reminders", label: "שלח תזכורת", when: ctx => ctx.appt.status === "booked" && !!ctx.appt.phone && Date.parse(ctx.appt.starts_at) > Date.now(), run: ctx => remind(ctx.appt) });
  G.register({ id: "reminders", name: "תזכורות ואישור הגעה", desc: "תזכורת בוואטסאפ יום לפני, עם קישור שבו הלקוח מאשר הגעה, משנה מועד או מבטל. מי שלא הגיע פעמיים צריך אישור שלך לתור הבא.", groups: "all" });
})(window.Garage);
