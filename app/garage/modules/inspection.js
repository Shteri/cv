// Vehicle inspection: a checklist per visit (ok / soon / now, note, photos from the phone), recommended jobs priced
// from the catalog, sent to the customer on the approval link where each job is approved on its own.
(function (G) {
  const { $, $$, D, api, demo, esc, fmt, fmtDate, money, numIn, on, st, toast } = G;

  // what is checked, which maintenance items a fix replaces (to suggest a job), and which kinds of garage check it
  const CHECKS = [
    ["brakes_front", "בלמים קדמיים", ["brake_pads", "brake_discs"], ["mech", "tire"]],
    ["brakes_rear", "בלמים אחוריים", ["brake_pads", "brake_discs", "brake_drums"], ["mech", "tire"]],
    ["brake_fluid", "נוזל בלמים", ["brake_fluid"], ["mech"]],
    ["tires", "צמיגים", ["tires"], ["mech", "tire", "check"]],
    ["alignment", "כיוון פרונט ושחיקה", ["wheel_alignment", "tire_rotation"], ["tire", "mech"]],
    ["suspension", "בולמים ומתלים", ["suspension"], ["mech", "tire", "check"]],
    ["steering", "היגוי", ["steering", "power_steering_fluid"], ["mech", "tire", "check"]],
    ["oil", "שמן מנוע ונזילות", ["engine_oil", "oil_filter"], ["mech"]],
    ["coolant", "נוזל קירור וצנרת", ["coolant", "coolant_hoses"], ["mech"]],
    ["belts", "רצועות", ["drive_belt", "timing_belt"], ["mech"]],
    ["battery", "מצבר", ["battery_12v"], ["mech", "elec"]],
    ["lights", "אורות", ["lights"], ["mech", "elec", "check"]],
    ["wipers", "מגבים ונוזל שמשות", ["wipers", "washer_fluid"], ["mech", "elec"]],
    ["ac", "מיזוג", ["ac_system", "ac_refrigerant", "cabin_filter"], ["elec", "mech"]],
    ["exhaust", "אגזוז", ["exhaust"], ["mech", "spec", "check"]],
    ["body", "מרכב ושמשות", [], ["body", "check"]],
  ].map(([key, label, items, groups]) => ({ key, label, items: items.filter(k => D.items[k]), groups }));
  const STATUS = { ok: "תקין", soon: "בקרוב", now: "דחוף" };

  let inCtx = null, inRows = [], uploads = 0;
  function openInspection(ctx) {
    const c = ctx.car, a = ctx.appt;
    inCtx = ctx;
    inRows = CHECKS.filter(k => !st.groups.length || k.groups.some(g => st.groups.includes(g))).map(k => ({ ...k, status: "", note: "", photos: [], job: "", price: "" }));
    $("#in-who").textContent = [c ? (c.name || "לקוח") : a && a.customer_name, c ? `${c.model} ${c.year || ""}` : "", c && c.plate].filter(Boolean).join(" · ");
    $("#in-km").value = c && c.estKm ? Math.round(c.estKm) : "";
    $("#in-err").hidden = true; renderInspection(); $("#dlg-appt").open && $("#dlg-appt").close(); $("#dlg-cust").open && $("#dlg-cust").close();
    $("#dlg-insp").showModal();
  }
  function jobsFor(r) { return on("catalog") ? [...new Set(r.items.flatMap(k => G.jobsFor(k)))] : []; }
  function renderInspection() {
    $("#in-rows").innerHTML = inRows.map((r, i) => {
      const jobs = jobsFor(r), fix = r.status === "soon" || r.status === "now";
      return `<div class="insp-row" data-st="${r.status}" data-i="${i}">
        <b>${esc(r.label)}</b>
        <div class="seg">${Object.entries(STATUS).map(([k, t]) => `<button type="button" data-v="${k}" class="${r.status === k ? "on" : ""}">${t}</button>`).join("")}</div>
        <input data-k="note" value="${esc(r.note)}" placeholder="הערה, למשל 30% רפידה" autocomplete="off">
        <label class="btn small">תמונה<input type="file" accept="image/*" capture="environment" multiple hidden data-photo="${i}"></label>
        ${r.photos.length ? `<div class="thumbs">${r.photos.map(u => `<img class="thumb" src="${esc(u)}" alt="">`).join("")}</div>` : ""}
        ${fix ? `<div class="insp-fix">${jobs.length ? `<select data-k="job"><option value="">בלי עבודה מהמחירון</option>${jobs.map(j => `<option value="${j.id}" ${r.job === j.id ? "selected" : ""}>${esc(j.name)}</option>`).join("")}</select>` : `<span class="muted small">${on("catalog") ? "אין עבודה מתאימה במחירון" : ""}</span>`}<input class="num price" data-k="price" value="${esc(r.price)}" inputmode="decimal" placeholder="₪ מחיר" autocomplete="off"></div>` : ""}
      </div>`; }).join("");
    $$("#in-rows .insp-row").forEach(row => {
      const r = inRows[+row.dataset.i];
      $$(".seg button", row).forEach(b => b.onclick = () => {
        r.status = r.status === b.dataset.v ? "" : b.dataset.v;
        if ((r.status === "soon" || r.status === "now") && !r.job && !r.price) { const j = jobsFor(r)[0]; if (j) { r.job = j.id; r.price = String(G.jobEstimate(j, inCtx.car).total || ""); } }
        renderInspection();
      });
      $$("[data-k]", row).forEach(x => x.oninput = x.onchange = () => {
        r[x.dataset.k] = x.value;
        if (x.dataset.k === "job") { const j = st.jobs.find(y => y.id === x.value); if (j) { r.price = String(G.jobEstimate(j, inCtx.car).total || ""); renderInspection(); } }
        else inTotal();
      });
    });
    $$("#in-rows [data-photo]").forEach(x => x.onchange = () => addPhotos(inRows[+x.dataset.photo], [...x.files]));
    inTotal();
  }
  const fixes = () => inRows.filter(r => (r.status === "soon" || r.status === "now") && (numIn(r.price) > 0 || r.job));
  function inTotal() {
    const t = fixes().reduce((s, r) => s + (numIn(r.price) || 0), 0), n = s => inRows.filter(r => r.status === s).length;
    $("#in-total").textContent = money(t);
    $("#in-sum").textContent = `${n("ok")} תקין · ${n("soon")} בקרוב · ${n("now")} דחוף`;
  }
  $("#in-allok").onclick = () => { for (const r of inRows) if (!r.status) r.status = "ok"; renderInspection(); };

  // photos are shrunk on the phone before upload (about 1280px, JPEG)
  async function shrink(file) {
    const bmp = await createImageBitmap(file), k = Math.min(1, 1280 / Math.max(bmp.width, bmp.height));
    const c = document.createElement("canvas"); c.width = Math.round(bmp.width * k); c.height = Math.round(bmp.height * k);
    c.getContext("2d").drawImage(bmp, 0, 0, c.width, c.height);
    return new Promise(res => c.toBlob(res, "image/jpeg", 0.8));
  }
  async function addPhotos(r, files) {
    uploads += files.length; $("#in-send").disabled = true;
    for (const f of files) {
      try { const blob = await shrink(f); r.photos.push(demo ? URL.createObjectURL(blob) : await api.uploadInspectionPhoto(st.garage.id, blob)); }
      catch (e) { toast("התמונה לא עלתה: " + (e.message || e)); }
      uploads--;
    }
    $("#in-send").disabled = uploads > 0; renderInspection();
  }

  $("#in-send").onclick = async () => {
    const err = m => { $("#in-err").textContent = m; $("#in-err").hidden = false; };
    const checks = inRows.filter(r => r.status).map(r => ({ key: r.key, label: r.label, status: r.status, ...(r.note.trim() ? { note: r.note.trim() } : {}), ...(r.photos.length ? { photos: r.photos } : {}) }));
    if (!checks.length) return err("סמנו לפחות סעיף אחד.");
    const lines = fixes().map(r => { const j = st.jobs && st.jobs.find(y => y.id === r.job); return { desc: j ? j.name : r.label + (r.note.trim() ? ": " + r.note.trim() : ""), price: numIn(r.price) || 0, check: r.key, urgent: r.status === "now" }; });
    const c = inCtx.car, a = inCtx.appt;
    const row = { garage_id: st.garage.id, appointment_id: a ? a.id : null, garage_car_id: c ? c.car_id : null, car_label: c ? `${c.model} ${c.year || ""}`.trim() : (a && a.plate) || null,
      message: "תוצאות בדיקת הרכב", lines, total: lines.reduce((s, l) => s + l.price, 0), checks, km: numIn($("#in-km").value) };
    const b = $("#in-send"); b.disabled = true;
    try {
      const x = demo ? { ...row, id: "dins-" + Date.now(), status: "pending", created_at: new Date().toISOString() } : await api.createApproval(row);
      st.insps.unshift(x); G.addApproval(x);
      if (a && lines.length) await G.markAwaiting(a);
      $("#dlg-insp").close();
      G.sendApprovalLink(a || { customer_name: (c && c.name) || "לקוח", phone: c && c.phone, garage_car_id: c && c.car_id }, x);
    } catch (e) { err("השליחה נכשלה: " + (e.message || e)); }
    b.disabled = false;
  };

  // entry points: the appointment card and the car box in the customer card
  G.addAction("appt", { module: "inspection", label: "בדיקת רכב", run: ctx => openInspection(ctx) });
  G.addAction("car", { module: "inspection", label: "בדיקת רכב", run: ctx => openInspection(ctx) });
  // inspections in the customer card's history
  G.addTimeline("inspection", cars => st.insps.filter(x => cars.some(c => c.car_id === x.garage_car_id)).map(x => {
    const n = s => (x.checks || []).filter(k => k.status === s).length, ok = x.status === "approved" ? (x.approved_lines || []).length : 0;
    return { date: x.created_at, km: x.km, html: `<div class="tl-row own"><div class="tl-head"><b>בדיקת רכב</b><span class="tag mine">אצלנו</span>${n("now") ? `<span class="tag crit">${n("now")} דחוף</span>` : ""}${n("soon") ? `<span class="tag warn">${n("soon")} בקרוב</span>` : ""}<span class="muted small num">${fmtDate(x.created_at)}${x.km ? " · " + fmt(x.km) + ' ק"מ' : ""}</span></div>
      <div class="small">${esc((x.checks || []).filter(k => k.status !== "ok").map(k => k.label + (k.note ? " (" + k.note + ")" : "")).join(", ") || "הכל תקין")}</div>
      ${(x.lines || []).length ? `<div class="muted small">${x.status === "pending" ? "ממתין לתשובת הלקוח" : x.status === "declined" ? "הלקוח לא אישר" : `הלקוח אישר ${ok} מתוך ${x.lines.length}`}</div>` : ""}</div>` };
  }));

  G.register({ id: "inspection", name: "בדיקת רכב", desc: "רשימת בדיקה בכל ביקור עם תמונות מהטלפון. הלקוח מקבל קישור, רואה מה מצאתם ומאשר כל עבודה בנפרד.", groups: ["mech", "elec", "tire", "check"],
    state: { insps: [] },
    async load(id) { st.insps = (await api.approvalsFor(id)).filter(x => (x.checks || []).length); },
    demo(Dm) { st.insps = Dm.approvals.filter(x => (x.checks || []).length); } });
})(window.Garage);
