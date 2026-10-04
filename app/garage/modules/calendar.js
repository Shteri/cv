// Calendar: appointments per bay, appointment card, extra-work approval by link, car-ready message.
(function (G) {
  const { $, $$, DEMO, api, copy, demo, digits, esc, fmt, fmtDate, fmtPlate, ico, on, openMsgText, setSeg, st, telHref, toast } = G;
  // other modules, looked up when called
  const car = (...a) => G.car(...a);
  const invOf = (...a) => G.invOf(...a);
  const openAdd = (...a) => G.openAdd(...a);
  const openCustomer = (...a) => G.openCustomer(...a);
  const openInvoice = (...a) => G.openInvoice(...a);
  const openWo = (...a) => G.openWo(...a);
  // ---------- calendar: one column per bay, one row per slot ----------
  const STATUS = { booked: "נקבע", arrived: "הגיע", in_progress: "בעבודה", waiting_approval: "ממתין לאישור", ready: "מוכן לאיסוף", done: "נמסר", cancelled: "בוטל", no_show: "לא הגיע" };
  const KIND = { service: "טיפול", repair: "תיקון", test: "הכנה לטסט", other: "אחר" };
  const DEFAULT_HOURS = { 0: { open: "08:00", close: "17:00" }, 1: { open: "08:00", close: "17:00" }, 2: { open: "08:00", close: "17:00" }, 3: { open: "08:00", close: "17:00" }, 4: { open: "08:00", close: "17:00" }, 5: { open: "08:00", close: "13:00" }, 6: null };
  const hoursOf = g => (g.hours && Object.keys(g.hours).length ? g.hours : DEFAULT_HOURS);
  const ymd = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
  const hm = d => `${String(d.getHours()).padStart(2, "0")}:${String(d.getMinutes()).padStart(2, "0")}`;
  const toMin = t => { const [h, m] = t.split(":").map(Number); return h * 60 + m; };
  const atLocal = (dateStr, timeStr) => new Date(`${dateStr}T${timeStr}:00`);
  const SLOT = 30;  // grid resolution in minutes
  const cal = { day: new Date(), appts: [], approvals: [], timer: null };
  cal.day.setHours(0, 0, 0, 0);
  const isLive = a => !["cancelled", "no_show"].includes(a.status);
  function dayWindow() {
    const h = hoursOf(st.garage)[cal.day.getDay()];
    let from = h ? toMin(h.open) : 8 * 60, to = h ? toMin(h.close) : 17 * 60;
    for (const a of cal.appts) { const s = new Date(a.starts_at), m = s.getHours() * 60 + s.getMinutes(); from = Math.min(from, Math.floor(m / 60) * 60); to = Math.max(to, m + a.minutes); }
    return { from: Math.floor(from / SLOT) * SLOT, to: Math.ceil(to / SLOT) * SLOT, closed: !h };
  }
  // Show appointments without a bay in the first bay that is free at that time.
  function placeBays(list) {
    const bays = st.garage.bays || 2, taken = [];
    const fits = (b, s, e) => !taken.some(t => t.b === b && t.s < e && t.e > s);
    return list.slice().sort((a, b) => Date.parse(a.starts_at) - Date.parse(b.starts_at)).map(a => {
      const s = Date.parse(a.starts_at), e = s + a.minutes * 60000;
      let b = a.bay && a.bay <= bays && fits(a.bay, s, e) ? a.bay : null;
      if (!b) for (let i = 1; i <= bays; i++) if (fits(i, s, e)) { b = i; break; }
      if (!b) b = a.bay || 1;
      if (isLive(a)) taken.push({ b, s, e });
      return { a, b };
    });
  }
  function renderCalendar() {
    const bays = st.garage.bays || 2, w = dayWindow(), rows = (w.to - w.from) / SLOT;
    $("#cal-date").textContent = new Intl.DateTimeFormat("he-IL", { weekday: "long", day: "numeric", month: "long" }).format(cal.day) + (w.closed ? " · סגור" : "");
    $("#cal-pick").value = ymd(cal.day);
    const live = cal.appts.filter(isLive);
    const waiting = live.filter(a => a.status === "waiting_approval").length, ready = live.filter(a => a.status === "ready").length;
    $("#cal-kpis").innerHTML = `<div class="kpi"><b class="num">${live.length}</b><span>תורים ביום הזה</span></div><div class="kpi due"><b class="num">${waiting}</b><span>ממתינים לאישור לקוח</span></div><div class="kpi"><b class="num">${ready}</b><span>מוכנים לאיסוף</span></div>`;
    const head = `<div class="cal-h cal-corner"></div>` + Array.from({ length: bays }, (_, i) => `<div class="cal-h" style="--c:${i + 2}">עמדה ${i + 1}</div>`).join("");
    const times = Array.from({ length: rows }, (_, r) => { const m = w.from + r * SLOT; return m % 60 === 0 ? `<div class="cal-t" style="--r:${r + 2}">${String(m / 60).padStart(2, "0")}:00</div>` : ""; }).join("");
    const cells = []; for (let r = 0; r < rows; r++) for (let b = 1; b <= bays; b++) { const m = w.from + r * SLOT; cells.push(`<button class="cal-cell ${m % 60 === 0 ? "hour" : ""}" style="--r:${r + 2};--c:${b + 1}" data-slot="${m}" data-bay="${b}" aria-label="תור חדש ${String(Math.floor(m / 60)).padStart(2, "0")}:${String(m % 60).padStart(2, "0")} עמדה ${b}"></button>`); }
    const blocks = placeBays(cal.appts).map(({ a, b }) => {
      const s = new Date(a.starts_at), m = s.getHours() * 60 + s.getMinutes(), r = Math.max(0, Math.floor((m - w.from) / SLOT)), span = Math.max(1, Math.round(a.minutes / SLOT));
      return `<button class="appt ${isLive(a) ? "" : "off"}" data-st="${a.status}" style="--r:${r + 2};--s:${span};--c:${b + 1}" data-appt="${a.id}">
        <b>${esc(a.customer_name)}</b><span>${hm(s)} · ${KIND[a.kind] || ""}${a.plate ? " · " + esc(fmtPlate(a.plate)) : ""}</span><span class="st">${STATUS[a.status]}${a.source === "online" ? " · אונליין" : ""}</span></button>`;
    }).join("");
    const grid = $("#cal"); grid.style.setProperty("--bays", bays); grid.style.setProperty("--rows", rows);
    grid.innerHTML = head + times + cells.join("") + blocks;
    $$("#cal .cal-cell").forEach(c => c.onclick = () => openNewAppt({ date: ymd(cal.day), time: `${String(Math.floor(c.dataset.slot / 60)).padStart(2, "0")}:${String(c.dataset.slot % 60).padStart(2, "0")}`, bay: +c.dataset.bay }));
    $$("#cal .appt").forEach(b => b.onclick = () => openAppt(b.dataset.appt));
  }
  async function loadDay() {
    const from = new Date(cal.day), to = new Date(cal.day); to.setDate(to.getDate() + 1);
    if (demo) cal.appts = DEMO.appts.filter(a => { const t = Date.parse(a.starts_at); return t >= from && t < to; });
    else { try { const [ap, aw] = await Promise.all([api.appointments(st.garage.id, from.toISOString(), to.toISOString()), api.approvalsFor(st.garage.id)]); cal.appts = ap; cal.approvals = aw; } catch (e) { toast(/schema cache|does not exist|appointments/i.test(e.message || "") ? "היומן עוד לא מוכן בשרת (צריך להריץ את מיגרציה 0006)" : "טעינת היומן נכשלה"); cal.appts = []; } }
    renderCalendar();
    if ($("#dlg-appt").open && apFor) { const fresh = cal.appts.find(a => a.id === apFor.id); if (fresh) { apFor = fresh; renderAppt(); } }
  }
  const shiftDay = n => { cal.day.setDate(cal.day.getDate() + n); loadDay(); };
  $("#cal-prev").onclick = () => shiftDay(-1); $("#cal-next").onclick = () => shiftDay(1);
  $("#cal-today").onclick = () => { cal.day = new Date(); cal.day.setHours(0, 0, 0, 0); loadDay(); };
  $("#cal-pick").onchange = e => { if (!e.target.value) return; cal.day = new Date(e.target.value + "T00:00:00"); loadDay(); };
  // While the calendar is open, pick up online bookings and customers' answers.
  function calPolling(on) { clearInterval(cal.timer); cal.timer = on && !demo ? setInterval(() => { if (!document.hidden) loadDay(); }, 30000) : null; }

  // ---------- one appointment ----------
  let apFor = null;
  const apCar = a => a.garage_car_id ? car(a.garage_car_id) : st.rows.find(c => a.plate && c.plateDigits === a.plate);
  function openAppt(id) { apFor = cal.appts.find(a => a.id === id); if (!apFor) return; renderAppt(); $("#dlg-appt").showModal(); }
  function renderAppt() {
    const a = apFor, s = new Date(a.starts_at), c = apCar(a), phone = a.phone || (c && c.phone);
    $("#ap-title").textContent = a.customer_name;
    $("#ap-sub").textContent = `${new Intl.DateTimeFormat("he-IL", { weekday: "long", day: "numeric", month: "long" }).format(s)} · ${hm(s)} · ${a.minutes} דק' · ${KIND[a.kind]}${c ? " · " + c.model + " " + (c.year || "") : ""}${a.plate ? " · " + fmtPlate(a.plate) : ""}${a.source === "online" ? " · נקבע אונליין" : ""}`;
    $("#ap-status").innerHTML = Object.entries(STATUS).map(([k, t]) => `<button type="button" class="chip ${a.status === k ? "on" : ""}" data-st="${k}">${t}</button>`).join("");
    $$("#ap-status .chip").forEach(b => b.onclick = () => setApptStatus(b.dataset.st));
    const wo = a.work_order_id && st.wos.find(w => w.id === a.work_order_id);
    const apActs = G.renderActions("appt", { appt: a, car: c });
    $("#ap-actions").innerHTML = [
      phone ? `<button type="button" class="btn" id="ap-wa">${ico.wa} וואטסאפ</button><a class="btn" href="${telHref(phone)}">${ico.phone} חיוג</a>` : "",
      c ? `<button type="button" class="btn" id="ap-card">כרטיס לקוח</button><button type="button" class="btn" id="ap-wo">${wo ? "כרטיס עבודה (פתוח)" : "כרטיס עבודה"}</button>` : `<button type="button" class="btn" id="ap-addcust">הוסף ללקוחות</button>`,
      `<button type="button" class="btn" id="ap-approve">בקש אישור לעבודה נוספת</button>`,
      wo && on("billing") ? `<button type="button" class="btn" id="ap-inv">${invOf(wo.id) ? "חשבונית " + esc(invOf(wo.id).number || "") : "חשבונית"}</button>` : "",
      apActs.html,
      phone ? `<button type="button" class="btn primary" id="ap-ready">הרכב מוכן, עדכן את הלקוח</button>` : ""
    ].join("");
    apActs.bind($("#ap-actions"));
    const wa = $("#ap-wa"); if (wa) wa.onclick = () => openMsgText(a.customer_name, phone, `היי ${a.customer_name.split(" ")[0]}, כאן ${st.garage.name}. `);
    const cc = $("#ap-card"); if (cc) cc.onclick = () => { $("#dlg-appt").close(); openCustomer(c.customer_id); };
    const wb = $("#ap-wo"); if (wb) wb.onclick = () => { $("#dlg-appt").close(); G.woAppt = a; openWo(c); };
    const ad = $("#ap-addcust"); if (ad) ad.onclick = () => { $("#dlg-appt").close(); openAdd({ plate: a.plate, name: a.customer_name, phone: a.phone }); };
    $("#ap-approve").onclick = () => openApproval(a);
    const iv = $("#ap-inv"); if (iv) iv.onclick = () => openInvoice(wo);
    const rd = $("#ap-ready"); if (rd) rd.onclick = async () => {
      await setApptStatus("ready");
      const inv = wo && on("billing") && invOf(wo.id), total = wo && wo.total ? ` הסכום לתשלום: ₪${fmt(wo.total)}.${inv && inv.url ? ` החשבונית: ${inv.url}` : ""}` : "";
      openMsgText(a.customer_name, phone, `היי ${a.customer_name.split(" ")[0]}, כאן ${st.garage.name}. הרכב${c ? ` (${c.model})` : ""} מוכן לאיסוף.${total} נתראה!`);
    };
    const mine = (demo ? DEMO.approvals : cal.approvals).filter(x => x.appointment_id === a.id);
    $("#ap-approvals-row").hidden = !mine.length;
    $("#ap-approvals").innerHTML = mine.map(x => `<div class="approval" data-st="${x.status}"><span>${esc(x.message || "עבודה נוספת")} · <b class="num">₪${fmt(approvedTotal(x))}</b>${x.status === "approved" && partial(x) ? ` <span class="muted small">(${x.approved_lines.length} מתוך ${x.lines.length})</span>` : ""}</span><span class="tag ${x.status === "approved" ? "ok" : x.status === "declined" ? "crit" : "warn"}">${x.status === "approved" ? (partial(x) ? "אושר חלקית" : "אושר") : x.status === "declined" ? "נדחה" : "ממתין"}</span>${x.decided_at ? `<span class="muted small">${fmtDate(x.decided_at)} ${hm(new Date(x.decided_at))}</span>` : `<button type="button" class="btn small" data-resend="${x.id}">שלח שוב</button>`}</div>`).join("");
    $$("[data-resend]").forEach(b => b.onclick = () => { const x = mine.find(y => y.id === b.dataset.resend); sendApprovalLink(a, x); });
    $("#ap-note").textContent = a.note ? "הערה: " + a.note : "";
  }
  // a customer may approve only some lines (approval_choose); the total shown is what was approved
  const partial = x => Array.isArray(x.approved_lines) && x.approved_lines.length < (x.lines || []).length;
  const approvedTotal = x => x.status === "approved" && Array.isArray(x.approved_lines) ? x.approved_lines.reduce((s, i) => s + (+((x.lines || [])[i] || {}).price || 0), 0) : x.total;
  async function setApptStatus(status) {
    const a = apFor, prev = a.status; a.status = status;
    try { if (!demo) Object.assign(a, await api.saveAppointment({ id: a.id, garage_id: a.garage_id, status })); renderAppt(); renderCalendar(); toast(STATUS[status]); }
    catch (e) { a.status = prev; toast("העדכון נכשל: " + (e.message || e)); }
  }

  // ---------- new / moved appointment ----------
  let naEdit = null, naKind = "service", naCar = null;
  function openNewAppt(pre = {}) {
    naEdit = pre.edit || null; naCar = null;
    const a = naEdit;
    $("#na-title").textContent = a ? "שינוי מועד" : "תור חדש"; $("#na-save").textContent = a ? "שמור" : "קבע תור";
    $("#na-dl").innerHTML = st.rows.map(c => `<option value="${esc(c.name)} · ${esc(c.plate || c.model)}"></option>`).join("");
    $("#na-find").value = a ? a.customer_name : ""; $("#na-phone").value = a ? (a.phone || "") : ""; $("#na-plate").value = a && a.plate ? fmtPlate(a.plate) : "";
    $("#na-find").disabled = !!a;
    const s = a ? new Date(a.starts_at) : null;
    $("#na-date").value = a ? ymd(s) : (pre.date || ymd(cal.day)); $("#na-time").value = a ? hm(s) : (pre.time || "08:00");
    $("#na-min").value = String(a ? a.minutes : (st.garage.slot_minutes || 60)); if (!$("#na-min").value) $("#na-min").value = "60";
    $("#na-bay").innerHTML = `<option value="">אוטומטי</option>` + Array.from({ length: st.garage.bays || 2 }, (_, i) => `<option value="${i + 1}">עמדה ${i + 1}</option>`).join("");
    $("#na-bay").value = a && a.bay ? String(a.bay) : pre.bay ? String(pre.bay) : "";
    naKind = a ? a.kind : "service"; setSeg("na-kind", naKind); $("#na-note").value = a ? (a.note || "") : ""; $("#na-err").hidden = true;
    if (a) naCar = apCar(a) || null;
    $("#dlg-newappt").showModal(); if (!a) $("#na-find").focus();
  }
  $("#na-find").oninput = () => { const v = $("#na-find").value, c = st.rows.find(x => `${x.name} · ${x.plate || x.model}` === v); naCar = c || null; if (c) { $("#na-find").value = c.name; $("#na-phone").value = c.phone || c.own_phone || ""; $("#na-plate").value = c.plate || ""; } };
  $$("#na-kind button").forEach(b => b.onclick = () => { naKind = b.dataset.v; setSeg("na-kind", naKind); });
  $("#na-save").onclick = async () => {
    const err = m => { $("#na-err").textContent = m; $("#na-err").hidden = false; };
    const name = $("#na-find").value.trim(); if (!name) return err("צריך שם.");
    if (!$("#na-date").value || !$("#na-time").value) return err("צריך תאריך ושעה.");
    const starts = atLocal($("#na-date").value, $("#na-time").value), minutes = +$("#na-min").value, bay = +$("#na-bay").value || null;
    const clash = cal.appts.filter(x => isLive(x) && (!naEdit || x.id !== naEdit.id) && Date.parse(x.starts_at) < starts.getTime() + minutes * 60000 && Date.parse(x.starts_at) + x.minutes * 60000 > starts.getTime());
    if (bay && clash.some(x => x.bay === bay)) return err(`עמדה ${bay} תפוסה בזמן הזה.`);
    if (clash.length >= (st.garage.bays || 2)) return err("כל העמדות תפוסות בזמן הזה.");
    const row = naEdit ? { id: naEdit.id, garage_id: st.garage.id, starts_at: starts.toISOString(), minutes, bay, kind: naKind, note: $("#na-note").value.trim() || null, phone: $("#na-phone").value.trim() || null }
      : { garage_id: st.garage.id, garage_car_id: naCar ? naCar.car_id : null, customer_name: name, phone: $("#na-phone").value.trim() || null, plate: digits($("#na-plate").value) || null, kind: naKind, note: $("#na-note").value.trim() || null, starts_at: starts.toISOString(), minutes, bay, source: "garage", status: "booked" };
    const b = $("#na-save"); b.disabled = true;
    try {
      const saved = demo ? { ...(naEdit || {}), ...row, id: naEdit ? naEdit.id : "dap-" + Date.now(), status: naEdit ? naEdit.status : "booked", created_at: new Date().toISOString() } : await api.saveAppointment(row);
      if (demo) { const i = DEMO.appts.findIndex(x => x.id === saved.id); if (i >= 0) DEMO.appts[i] = saved; else DEMO.appts.push(saved); }
      $("#dlg-newappt").close(); toast(naEdit ? "המועד עודכן" : "התור נקבע");
      cal.day = new Date(starts); cal.day.setHours(0, 0, 0, 0); await loadDay();
      if (naEdit) { apFor = cal.appts.find(x => x.id === saved.id); if (apFor) { renderAppt(); } }
    } catch (e) { err("השמירה נכשלה: " + (e.message || e)); }
    b.disabled = false;
  };
  $("#cal-new").onclick = () => openNewAppt({});
  $("#ap-edit").onclick = () => { const a = apFor; $("#dlg-appt").close(); openNewAppt({ edit: a }); };

  // ---------- extra-work approval by link ----------
  let awFor = null, awLines = [];
  function openApproval(a) {
    awFor = a; awLines = [{ desc: "", price: "" }]; $("#aw-msg").value = ""; $("#aw-err").hidden = true; renderAwLines();
    $("#dlg-appt").close(); $("#dlg-approval").showModal(); $("#aw-msg").focus();
  }
  function renderAwLines() {
    $("#aw-lines").innerHTML = awLines.map((l, i) => `<tr><td><input data-i="${i}" data-k="desc" value="${esc(l.desc)}" autocomplete="off" placeholder="למשל רפידות בלם קדמיות"></td><td class="num-col"><input class="num price" data-i="${i}" data-k="price" value="${esc(l.price)}" inputmode="decimal" placeholder="₪" autocomplete="off"></td><td><button type="button" class="x" data-del="${i}" aria-label="מחק שורה">×</button></td></tr>`).join("");
    $$("#aw-lines input").forEach(x => x.oninput = () => { awLines[x.dataset.i][x.dataset.k] = x.value; awTotal(); });
    $$("#aw-lines [data-del]").forEach(b => b.onclick = () => { awLines.splice(+b.dataset.del, 1); if (!awLines.length) awLines.push({ desc: "", price: "" }); renderAwLines(); });
    awTotal();
  }
  const awTotal = () => { const t = awLines.reduce((s, l) => s + (+String(l.price).replace(/[^\d.]/g, "") || 0), 0); $("#aw-total").textContent = "₪" + fmt(t); return Math.round(t); };
  $("#aw-add").onclick = () => { awLines.push({ desc: "", price: "" }); renderAwLines(); };
  const approveUrl = id => location.origin + location.pathname.replace(/garage\/[^/]*$/, "") + "approve/?id=" + id;
  function sendApprovalLink(a, x) {
    const c = apCar(a), phone = a.phone || (c && c.phone);
    const link = demo ? location.origin + "/approve/?demo" + ((x.checks || []).length ? "&insp" : "") : approveUrl(x.id), hi = `היי ${a.customer_name.split(" ")[0]}, כאן ${st.garage.name}. `;
    const now = (x.checks || []).filter(k => k.status === "now").length, soon = (x.checks || []).filter(k => k.status === "soon").length;
    const text = (x.checks || []).length
      ? hi + `סיימנו לבדוק את הרכב. ${now || soon ? `מצאנו ${[now ? (now === 1 ? "דבר אחד לטיפול עכשיו" : now + " דברים לטיפול עכשיו") : "", soon ? (soon === 1 ? "דבר אחד שכדאי לטפל בו בקרוב" : soon + " דברים שכדאי לטפל בהם בקרוב") : ""].filter(Boolean).join(", ו")}. התמונות, המחירים והאישור כאן` : "הכל תקין. הדוח המלא כאן"}: ${link}`
      : hi + `${x.message ? x.message + ". " : ""}העבודה הנוספת עולה ₪${fmt(x.total)}. לפרטים ולאישור: ${link}`;
    if (phone) openMsgText(a.customer_name, phone, text); else { copy(text, "אין טלפון ללקוח. ההודעה הועתקה"); }
  }
  $("#aw-send").onclick = async () => {
    const err = m => { $("#aw-err").textContent = m; $("#aw-err").hidden = false; };
    const lines = awLines.filter(l => l.desc.trim()).map(l => ({ desc: l.desc.trim(), price: +String(l.price).replace(/[^\d.]/g, "") || 0 }));
    if (!lines.length) return err("צריך לפחות שורה אחת עם תיאור.");
    const a = awFor, c = apCar(a), total = awTotal();
    const row = { garage_id: st.garage.id, appointment_id: a.id, car_label: c ? `${c.model} ${c.year || ""}`.trim() : (a.plate ? fmtPlate(a.plate) : null), message: $("#aw-msg").value.trim() || null, lines, total };
    const b = $("#aw-send"); b.disabled = true;
    try {
      const x = demo ? { ...row, id: "daw-" + Date.now(), status: "pending", created_at: new Date().toISOString() } : await api.createApproval(row);
      if (demo) DEMO.approvals.unshift(x); else cal.approvals.unshift(x);
      $("#dlg-approval").close(); apFor = a; await setApptStatus("waiting_approval"); sendApprovalLink(a, x);
    } catch (e) { err("השליחה נכשלה: " + (e.message || e)); }
    b.disabled = false;
  };

  G.register({ id: "calendar", core: true, tab: "calendar", show() { loadDay(); calPolling(true); }, hide() { calPolling(false); } });
  // used by modules that send their own approval links (vehicle inspection)
  const addApproval = x => { (demo ? G.DEMO.approvals : cal.approvals).unshift(x); };
  const markAwaiting = async a => { apFor = a; await setApptStatus("waiting_approval"); };
  const awAddLines = lines => { awLines = awLines.filter(l => l.desc.trim() || l.price !== ""); awLines.push(...lines.map(l => ({ desc: l.desc, price: String(l.price || "") }))); renderAwLines(); };
  Object.assign(G, { renderCalendar, sendApprovalLink, addApproval, markAwaiting, awAddLines, apCar });
})(window.Garage);
