// Customers: the book of cars, reminders by the importer schedule, customer card with one history, add by plate, import, export, invite.
(function (G) {
  const { $, $$, D, DEMO, FILTERS, L, api, call, copy, demo, digits, download, esc, fmt, fmtDate, fmtPlate, ico, isDue, isOver, isTest, itemName, loadQr, loadRecalls, match, monthName, on, openMsg, recallsOf, reload, schedById, st, telHref, toast, today, view } = G;
  // other modules, looked up when called
  const invOf = (...a) => G.invOf(...a);
  const openInvoice = (...a) => G.openInvoice(...a);
  const openWo = (...a) => G.openWo(...a);
  // ---------- customers view ----------
  function renderKpis() {
    const r = st.rows, c = f => r.filter(x => match(x, f)).length;
    const tiles = [["all", r.length, "רכבים"], ["due", c("due"), "מגיעים לטיפול בחודש הקרוב"], ["over", c("over"), "באיחור לטיפול"], ["test", c("test"), "טסט ב-45 יום"], ["recall", c("recall"), "ריקול פתוח"]];
    $("#kpis").innerHTML = tiles.map(([f, n, t]) => `<button class="kpi ${f} ${st.filter === f ? "on" : ""}" data-f="${f}"><b class="num">${n}</b><span>${t}</span></button>`).join("");
    $$("#kpis .kpi").forEach(b => b.onclick = () => setFilter(b.dataset.f));
    $("#filters").innerHTML = FILTERS.map(([f, t]) => `<button class="chip ${st.filter === f ? "on" : ""}" data-f="${f}">${t}${f !== "all" ? ` <span class="num">${c(f)}</span>` : ""}</button>`).join("");
    $$("#filters .chip").forEach(b => b.onclick = () => setFilter(b.dataset.f));
  }
  const order = { due: c => c.n ? (isOver(c) ? -1e6 : 0) + c.n.daysLeft : 1e6, name: c => c.name || "", km: c => -(c.estKm || 0), test: c => c.testDays === null ? 1e6 : c.testDays };
  function rowsList() {
    const q = st.q.trim().toLowerCase().replace(/-/g, ""), key = order[st.sort] || order.due;
    return st.rows.filter(c => match(c, st.filter))
      .filter(c => !q || [c.name, c.model, c.plateDigits, digits(c.phone)].join(" ").toLowerCase().includes(q))
      .sort((a, b) => { const x = key(a), y = key(b); return typeof x === "string" ? x.localeCompare(y, "he") : x - y; });
  }
  function renderRows() {
    renderKpis();
    $$(".sort").forEach(b => b.classList.toggle("on", b.dataset.sort === st.sort));
    const list = rowsList();
    $("#rows").innerHTML = list.map(c => {
      const rc = recallsOf(c);
      const due = c.n ? (c.n.remainKm <= 0 ? 'עבר בק"מ' : c.n.daysLeft <= 0 ? "עבר הזמן" : monthName(c.n.dueDate)) : "";
      return `<tr>
        <td><button class="name-link" data-cust="${c.customer_id}">${esc(c.name || "לקוח")}</button>${c.phone ? `<div class="sub num" dir="ltr">${esc(c.phone)}</div>` : `<div class="sub">בלי הסכמה לפניות</div>`}</td>
        <td>${esc(c.model)} ${c.year || ""}${c.plate ? `<div class="sub"><span class="plate-mini num">${esc(c.plate)}</span></div>` : ""}</td>
        <td class="num-col num">${c.estKm !== null ? fmt(c.estKm) : "?"}</td>
        <td>${c.n ? `<b class="num">${fmt(c.n.nextKm)}</b>${c.n.windowTo !== c.n.windowFrom ? `<div class="sub num">בין ${fmt(c.n.windowFrom)} ל-${fmt(c.n.windowTo)}</div>` : ""}<div class="sub">${due}${c.n.remainKm > 0 && c.n.daysLeft > 0 ? ` · עוד ${fmt(c.n.remainKm)} ק"מ` : ""}</div>` : `<span class="sub">${c.s ? 'חסר ק"מ' : "אין לוח לדגם"}</span>`}</td>
        <td>${c.test_expiry ? `<span class="${isTest(c) ? "warn-text" : ""}">${fmtDate(c.test_expiry)}</span>` : `<span class="sub">לא ידוע</span>`}</td>
        <td><div class="tags">${!c.n ? "" : isOver(c) ? `<span class="tag crit">באיחור</span>` : isDue(c) ? `<span class="tag warn">מגיע לטיפול</span>` : `<span class="tag ok">בזמן</span>`}${isTest(c) ? `<span class="tag warn">${c.testDays < 0 ? "טסט פג" : "טסט קרוב"}</span>` : ""}${rc.length ? `<span class="tag crit" title="${esc(rc.map(x => x.system).join(", "))}">ריקול</span>` : ""}${c.lapsed ? `<span class="tag">לא היה שנה</span>` : ""}${c.linked ? `<span class="tag mine">באפליקציה</span>` : ""}${c.pending ? `<span class="tag mine">ממתין לאישור</span>` : ""}</div></td>
        <td class="act-col"><div class="acts">${c.phone ? `<button class="ib" data-msg="${c.car_id}" title="הודעת וואטסאפ" aria-label="הודעת וואטסאפ ל${esc(c.name || "לקוח")}">${ico.wa}</button><a class="ib" href="${telHref(c.phone)}" title="חיוג" aria-label="חיוג">${ico.phone}</a>` : ""}<button class="ib" data-wo="${c.car_id}" title="כרטיס עבודה" aria-label="כרטיס עבודה">${ico.wrench}</button></div></td>
      </tr>`; }).join("");
    $$("[data-msg]").forEach(b => b.onclick = () => openMsg(car(b.dataset.msg)));
    $$("#rows [data-wo]").forEach(b => b.onclick = () => openWo(car(b.dataset.wo)));
    $$("#rows [data-cust]").forEach(b => b.onclick = () => openCustomer(b.dataset.cust));
    const empty = $("#empty");
    if (!st.rows.length) { empty.hidden = false; empty.innerHTML = `<b>עדיין אין לקוחות</b><p class="muted">הוסיפו לקוח לפי מספר רכב, ייבאו את הרשימה מהמערכת הקיימת, או הדפיסו שלט לדלפק.</p><div class="dlg-actions"><button class="btn" id="empty-import">ייבוא מאקסל</button><button class="btn primary" id="empty-add">לקוח חדש</button></div>`; $("#empty-add").onclick = () => openAdd(); $("#empty-import").onclick = openImport; }
    else if (!list.length) { empty.hidden = false; empty.innerHTML = `<p class="muted">אין לקוחות בסינון הזה.</p>`; }
    else empty.hidden = true;
    if (st.tab === "order") call("renderForecast");
  }
  const car = id => st.rows.find(c => c.car_id === id);
  function setFilter(f) { st.filter = f; renderRows(); }
  $("#q").oninput = e => { st.q = e.target.value; renderRows(); };
  $$(".sort").forEach(b => b.onclick = () => { st.sort = b.dataset.sort; renderRows(); });

  // ---------- customer card: details, cars, one history (this garage's work orders + the driver's shared history) ----------
  let ccId = null;
  async function openCustomer(customerId) {
    ccId = customerId;
    const cars = st.rows.filter(c => c.customer_id === customerId), c0 = cars[0];
    $("#cc-name").textContent = c0.name || "לקוח";
    $("#cc-in-name").value = c0.name || ""; $("#cc-in-phone").value = c0.phone || c0.own_phone || ""; $("#cc-in-consent").checked = !!c0.can_contact; $("#cc-in-notes").value = c0.notes || "";
    $("#cc-in-phone").disabled = $("#cc-in-consent").disabled = !!c0.linked;
    $("#cc-src").textContent = c0.linked ? "הצטרף דרך האפליקציה. הטלפון וההסכמה בשליטת הלקוח." : c0.source === "import" ? "יובא מקובץ." : "נוסף ידנית.";
    const carActs = cars.map(c => G.renderActions("car", { car: c }, "btn small"));
    $("#cc-cars").innerHTML = cars.map((c, i) => `<div class="box" data-carbox="${i}"><div class="row-between"><b>${esc(c.model)} ${c.year || ""}</b>${c.plate ? `<span class="plate-mini num">${esc(c.plate)}</span>` : ""}</div>
      <div class="muted small">${c.estKm !== null ? `~${fmt(c.estKm)} ק"מ` : 'ק"מ לא ידוע'}${c.test_expiry ? ` · טסט עד ${fmtDate(c.test_expiry)}` : ""}</div>
      ${c.n ? `<div class="small">טיפול הבא: <b class="num">${fmt(c.n.nextKm)}</b>${c.n.windowTo !== c.n.windowFrom ? ` <span class="num">(בין ${fmt(c.n.windowFrom)} ל-${fmt(c.n.windowTo)}, לפי הטיפול האחרון ב-${fmt(c.n.lastKm)})</span>` : ""} · ${monthName(c.n.dueDate)}</div><div class="muted small">${c.n.plan.replace.map(itemName).join(", ")}${c.n.plan.skip.length ? ` · לא הפעם: ${c.n.plan.skip.map(x => `${itemName(x.item)} (הוחלף ב-${fmt(x.doneKm)})`).join(", ")}` : ""}</div>` : ""}
      ${recallsOf(c).length ? `<div class="small warn-text">ריקול פתוח: ${esc(recallsOf(c).map(x => x.system).join(", "))}</div>` : ""}
      <div class="dlg-actions start"><button class="btn small primary" type="button" data-wo="${c.car_id}">כרטיס עבודה</button>${carActs[i].html}</div></div>`).join("");
    carActs.forEach((x, i) => x.bind($(`#cc-cars [data-carbox="${i}"]`)));
    $$("#cc-cars [data-wo]").forEach(b => b.onclick = () => openWo(car(b.dataset.wo)));
    $("#cc-timeline").innerHTML = `<p class="muted small">טוען…</p>`;
    $("#dlg-cust").showModal();
    // history: own work orders + shared driver records
    let shared = [];
    for (const c of cars.filter(x => x.linked && x.share_history)) {
      try { const h = demo ? (DEMO.history[c.car_id] || []) : await api.garageCarHistory(c.car_id); shared.push(...h.filter(r => !r.own).map(r => ({ ...r, car: c }))); } catch (e) {}
    }
    const own = st.wos.filter(w => cars.some(c => c.car_id === w.garage_car_id)).map(w => ({ ...w, car: car(w.garage_car_id) }));
    const items = [...own.map(w => ({ t: "own", date: w.date, km: w.km, w })), ...shared.map(r => ({ t: "other", date: r.date, km: r.km, r })), ...G.timelineFor(cars).map(x => ({ t: "extra", ...x }))]
      .sort((a, b) => (b.km || 0) - (a.km || 0) || String(b.date).localeCompare(String(a.date)));
    const anyLinked = cars.some(c => c.linked), anyShared = cars.some(c => c.linked && c.share_history);
    $("#cc-hist-note").textContent = anyShared ? "כולל טיפולים במוסכים אחרים, באישור הלקוח" : anyLinked ? "הלקוח לא שיתף את ההיסטוריה ממוסכים אחרים" : "";
    $("#cc-timeline").innerHTML = items.map(x => x.t === "extra" ? x.html : x.t === "own" ? `<div class="tl-row own">
        <div class="tl-head"><b>${x.w.kind === "service" && x.w.svc_km ? "טיפול " + fmt(x.w.svc_km) : x.w.kind === "repair" ? "תיקון" : "ביקור"}</b><span class="tag mine">אצלנו</span>${x.w.entry_id ? `<span class="tag ok">נשלח ללקוח</span>` : ""}<span class="muted small num">${x.w.date ? fmtDate(x.w.date) : ""}${x.w.km ? " · " + fmt(x.w.km) + ' ק"מ' : ""}</span></div>
        ${(x.w.items || []).length ? `<div class="small">${x.w.items.map(itemName).join(", ")}</div>` : ""}
        ${(x.w.lines || []).length ? `<div class="muted small">${x.w.lines.map(l => `${esc(l.desc)}${l.qty > 1 ? " ×" + l.qty : ""}${l.price ? " ₪" + fmt(l.price * (l.qty || 1)) : ""}`).join(" · ")}</div>` : ""}
        ${x.w.notes ? `<div class="muted small">${esc(x.w.notes)}</div>` : ""}${x.w.total ? `<div class="row-between"><b class="num small">₪${fmt(x.w.total)}</b>${!on("billing") ? "" : invOf(x.w.id) ? `<span class="tag ok">${G.DOC[invOf(x.w.id).kind]} ${esc(invOf(x.w.id).number || "")}</span>` : `<button type="button" class="btn small" data-inv="${x.w.id}">חשבונית</button>`}</div>` : ""}</div>`
      : `<div class="tl-row other">
        <div class="tl-head"><b>${x.r.kind === "service" && x.r.svc_km ? "טיפול " + fmt(x.r.svc_km) : x.r.kind === "repair" ? (esc(x.r.text) || "תיקון") : "רשומה"}</b><span class="tag">${esc(x.r.garage || "בלי מוסך")}</span>${x.r.verified ? `<span class="tag ok">מאומת</span>` : `<span class="tag">רשם הלקוח</span>`}<span class="muted small num">${x.r.date || ""}${x.r.km ? " · " + fmt(x.r.km) + ' ק"מ' : ""}</span></div>
        ${(x.r.items || []).length ? `<div class="small">${x.r.items.map(itemName).join(", ")}</div>` : ""}</div>`).join("") || `<p class="muted small">עדיין אין ביקורים. כרטיס עבודה ייכנס לכאן.</p>`;
    $$("#cc-timeline [data-inv]").forEach(b => b.onclick = () => openInvoice(st.wos.find(w => w.id === b.dataset.inv)));
  }
  $("#cc-save").onclick = async () => {
    const patch = { name: $("#cc-in-name").value.trim() || "לקוח", notes: $("#cc-in-notes").value.trim() || null };
    const c0 = st.rows.find(c => c.customer_id === ccId);
    if (!c0.linked) { patch.phone = $("#cc-in-phone").value.trim() || null; patch.contact_consent = $("#cc-in-consent").checked; }
    try {
      if (!demo) await api.updateCustomer(ccId, patch);
      for (const c of st.rows.filter(x => x.customer_id === ccId)) { c.name = patch.name; c.notes = patch.notes; if (!c.linked) { c.own_phone = patch.phone; c.can_contact = patch.contact_consent; c.phone = patch.contact_consent ? patch.phone : null; } }
      $("#cc-name").textContent = patch.name; renderRows(); toast("נשמר");
    } catch (e) { toast("השמירה נכשלה: " + (e.message || e)); }
  };

  // ---------- add a customer by plate (registry fills model, year, test) ----------
  let adCar = null;
  function openAdd(pre = {}) { adCar = null; for (const id of ["ad-plate", "ad-name", "ad-phone", "ad-km", "ad-last"]) $("#" + id).value = ""; if (pre.plate) $("#ad-plate").value = fmtPlate(pre.plate); if (pre.name) $("#ad-name").value = pre.name; if (pre.phone) $("#ad-phone").value = pre.phone; $("#ad-car").textContent = ""; $("#ad-err").hidden = true; $("#dlg-add").showModal(); $("#ad-plate").focus(); }
  async function identify(plate) {
    const d = digits(plate); if (d.length < 7 || d.length > 8) return { error: "מספר רכב הוא 7 או 8 ספרות" };
    if (demo) { const s = D.schedules[Math.floor(Math.random() * D.schedules.length)]; return { plate: d, schedule_id: s.id, year: s.years[1] - 2, test_expiry: null, gov: null, label: `${s.make_he} ${s.model_he} (הדגמה)` }; }
    let v = null; try { v = await L.fetchVehicle(d); } catch (e) { return { plate: d, label: "לא הצלחנו לבדוק במאגר כרגע. אפשר להוסיף בכל זאת." }; }
    if (!v) return { plate: d, label: "הרכב לא נמצא במאגר הרכב. אפשר להוסיף בכל זאת." };
    const r = L.resolveSchedule(v, D.registryMap), s = r.status === "matched" ? schedById(r.schedule) : null;
    return { plate: d, schedule_id: s ? s.id : null, year: v.year, test_expiry: v.test_expiry, gov: v, label: `${v.make_raw} ${v.commercial_name} ${v.year || ""}${s ? "" : " · אין עדיין לוח טיפולים לדגם"}` };
  }
  $("#ad-find").onclick = async () => { $("#ad-car").textContent = "בודק…"; adCar = await identify($("#ad-plate").value); $("#ad-car").textContent = adCar.error || adCar.label; };
  $("#ad-save").onclick = async () => {
    const err = m => { $("#ad-err").textContent = m; $("#ad-err").hidden = false; };
    const name = $("#ad-name").value.trim(); if (!name) return err("צריך שם.");
    if (!adCar || adCar.plate !== digits($("#ad-plate").value)) { adCar = await identify($("#ad-plate").value); $("#ad-car").textContent = adCar.error || adCar.label; }
    if (adCar.error) return err(adCar.error);
    if (st.rows.some(c => c.plateDigits === adCar.plate)) return err("הרכב הזה כבר ברשימה שלך.");
    const phone = $("#ad-phone").value.trim(), consent = $("#ad-consent").checked, km = +digits($("#ad-km").value) || null;
    const b = $("#ad-save"); b.disabled = true;
    try {
      const cust = demo ? { id: "dc-" + Date.now() } : await api.addCustomer({ garage_id: st.garage.id, name, phone: phone || null, contact_consent: consent, source: "manual" });
      const carRow = { garage_id: st.garage.id, customer_id: cust.id, plate: adCar.plate, schedule_id: adCar.schedule_id || null, year: adCar.year || null, km, km_month: 1500, last_service: $("#ad-last").value || null, test_expiry: adCar.test_expiry || null, gov: adCar.gov || null };
      const gc = demo ? { id: "dg-" + Date.now() } : await api.addGarageCar(carRow);
      st.rows.push(view({ car_id: gc.id, customer_id: cust.id, name, phone: consent ? phone : null, own_phone: phone, can_contact: consent, source: "manual", ...carRow, km_at: new Date().toISOString(), linked: false, share_history: false, visits: 0, pending: 0, created_at: new Date().toISOString() }));
      $("#dlg-add").close(); toast("הלקוח נוסף"); renderRows(); loadRecalls([adCar.plate]);
    } catch (e) { err(/duplicate|unique/i.test(e.message || "") ? "הרכב הזה כבר ברשימה שלך." : "ההוספה נכשלה: " + (e.message || e)); }
    b.disabled = false;
  };
  $("#btn-add").onclick = () => openAdd();

  // ---------- import from Excel / CSV ----------
  let imRows = null, imHead = [];
  function openImport() { imRows = null; $("#im-file").value = ""; $("#im-file-lbl").textContent = "בחרו קובץ"; $("#im-map").hidden = true; $("#im-consent-row").hidden = true; $("#im-status").textContent = ""; $("#im-progress").hidden = true; $("#im-go").disabled = true; $("#dlg-import").showModal(); }
  $("#btn-import").onclick = openImport;
  function parseCsv(text) {
    const rows = [], sep = (text.split("\n")[0].match(/;/g) || []).length > (text.split("\n")[0].match(/,/g) || []).length ? ";" : ",";
    let row = [], cur = "", q = false;
    for (let i = 0; i < text.length; i++) { const ch = text[i];
      if (q) { if (ch === '"' && text[i + 1] === '"') { cur += '"'; i++; } else if (ch === '"') q = false; else cur += ch; }
      else if (ch === '"') q = true; else if (ch === sep) { row.push(cur); cur = ""; } else if (ch === "\n") { row.push(cur); rows.push(row); row = []; cur = ""; } else if (ch !== "\r") cur += ch; }
    if (cur || row.length) { row.push(cur); rows.push(row); }
    return rows.filter(r => r.some(x => x.trim()));
  }
  let xlsxLib = null;
  const loadXlsx = () => xlsxLib || (xlsxLib = new Promise((res, rej) => { const sc = document.createElement("script"); sc.src = "https://cdn.jsdelivr.net/npm/xlsx@0.18.5/dist/xlsx.full.min.js"; sc.onload = () => res(window.XLSX); sc.onerror = () => { xlsxLib = null; rej(new Error("xlsx")); }; document.head.appendChild(sc); }));
  const FIELDS = [["name", "שם", /שם|name|לקוח/i], ["phone", "טלפון", /טל|נייד|phone|mobile/i], ["plate", "מספר רכב", /רכב|לוחית|רישוי|plate|license/i], ["km", 'ק"מ', /ק"?מ|קילומ|km|mileage|odometer/i]];
  $("#im-file").onchange = async e => {
    const f = e.target.files[0]; if (!f) return;
    $("#im-file-lbl").textContent = f.name; $("#im-status").textContent = "קורא…";
    try {
      let table;
      if (/\.xlsx?$/i.test(f.name)) { const X = await loadXlsx(); const wb = X.read(await f.arrayBuffer()); table = X.utils.sheet_to_json(wb.Sheets[wb.SheetNames[0]], { header: 1, raw: false }).filter(r => r.some(x => String(x || "").trim())); }
      else table = parseCsv((await f.text()).replace(/^﻿/, ""));
      imHead = table[0].map(h => String(h || "").trim()); imRows = table.slice(1);
      $("#im-map").innerHTML = FIELDS.map(([k, t, re]) => { const guess = imHead.findIndex(h => re.test(h)); return `<label class="field"><span>${t}</span><select data-map="${k}"><option value="-1">לא קיים</option>${imHead.map((h, i) => `<option value="${i}" ${i === guess ? "selected" : ""}>${esc(h || "עמודה " + (i + 1))}</option>`).join("")}</select></label>`; }).join("");
      $("#im-map").hidden = false; $("#im-consent-row").hidden = false;
      $("#im-status").textContent = `${imRows.length} שורות בקובץ.`; $("#im-go").disabled = false;
    } catch (err) { $("#im-status").textContent = "לא הצלחנו לקרוא את הקובץ. נסו לשמור אותו כ-CSV."; }
  };
  $("#im-go").onclick = async () => {
    const map = Object.fromEntries($$("#im-map select").map(s => [s.dataset.map, +s.value]));
    if (map.name < 0 || map.plate < 0) { $("#im-status").textContent = "צריך לבחור עמודה של שם ועמודה של מספר רכב."; return; }
    const known = new Set(st.rows.map(c => c.plateDigits));
    const rows = imRows.map(r => ({ name: String(r[map.name] || "").trim(), phone: map.phone >= 0 ? String(r[map.phone] || "").trim() : "", plate: digits(r[map.plate]), km: map.km >= 0 ? +digits(r[map.km]) || null : null }))
      .filter(r => { if (!r.name || r.plate.length < 7 || r.plate.length > 8 || known.has(r.plate)) return false; known.add(r.plate); return true; });
    if (!rows.length) { $("#im-status").textContent = "אין שורות חדשות לייבוא (חסר שם או מספר רכב, או שהרכבים כבר ברשימה)."; return; }
    const consent = $("#im-consent").checked, b = $("#im-go"); b.disabled = true;
    $("#im-progress").hidden = false; const bar = $("#im-bar");
    let done = 0;
    for (let i = 0; i < rows.length; i += 4) {
      await Promise.all(rows.slice(i, i + 4).map(async r => { const v = await identify(r.plate).catch(() => ({})); Object.assign(r, { schedule_id: v.schedule_id || null, year: v.year || null, test_expiry: v.test_expiry || null, gov: v.gov || null, consent }); }));
      done = Math.min(rows.length, i + 4); bar.style.setProperty("--p", (done / rows.length * 100).toFixed(1) + "%"); $("#im-status").textContent = `מזהה רכבים במאגר… ${done}/${rows.length}`;
    }
    try {
      let res;
      if (demo) { res = { added: rows.length, skipped: 0 }; for (const r of rows) st.rows.push(view({ car_id: "di-" + r.plate, customer_id: "dci-" + r.plate, name: r.name, phone: consent ? r.phone : null, own_phone: r.phone, can_contact: consent, source: "import", plate: r.plate, schedule_id: r.schedule_id, year: r.year, km: r.km, km_month: 1500, km_at: new Date().toISOString(), test_expiry: r.test_expiry, linked: false, visits: 0, pending: 0, created_at: new Date().toISOString() })); }
      else { res = await api.importCustomers(st.garage.id, rows); await reload(); }
      $("#im-status").textContent = `יובאו ${res.added} לקוחות${res.skipped ? `, ${res.skipped} דולגו` : ""}.`; toast(`יובאו ${res.added} לקוחות`); renderRows();
    } catch (e) { $("#im-status").textContent = "הייבוא נכשל: " + (e.message || e); }
    b.disabled = false;
  };

  // ---------- invite ----------
  const joinUrl = id => location.origin + location.pathname.replace(/garage\/[^/]*$/, "") + "?join=" + id;
  function openInvite() {
    const url = demo ? location.origin + "/?join=demo" : joinUrl(st.garage.id);
    $("#inv-link").value = url; $("#poster-garage").textContent = st.garage.name;
    $("#inv-wa").href = "https://wa.me/?text=" + encodeURIComponent(`הצטרפו ל${st.garage.name} בטיפולית: תזכורת לפני כל טיפול לפי ספר היבואן, וכל הטיפולים במקום אחד. ${url}`);
    $("#qr").innerHTML = `<p class="muted small">טוען…</p>`;
    loadQr().then(qrcode => { const q = qrcode(0, "M"); q.addData(url); q.make(); $("#qr").innerHTML = q.createSvgTag({ cellSize: 6, margin: 1, scalable: true }); }).catch(() => { $("#qr").innerHTML = `<p class="muted small">ה-QR לא נטען. אפשר להעתיק את הקישור.</p>`; });
    $("#dlg-invite").showModal();
  }
  $("#btn-invite").onclick = openInvite;
  $("#inv-copy").onclick = () => copy($("#inv-link").value, "הקישור הועתק");
  $("#inv-print").onclick = () => { document.body.classList.add("printing"); window.print(); setTimeout(() => document.body.classList.remove("printing"), 500); };

  // ---------- export ----------
  $("#btn-csv").onclick = () => {
    const list = rowsList(), q = v => `"${String(v ?? "").replace(/"/g, '""')}"`;
    const head = ["שם", "טלפון", "מותר לפנות", "דגם", "שנה", "לוחית", 'ק"מ משוער', "טיפול הבא", "מועד משוער", "תוקף טסט", "ביקור אחרון", "ריקול פתוח"];
    download(`לקוחות-${st.garage.name}-${today()}.csv`, [head.map(q).join(","), ...list.map(c => [c.name, c.phone || "", c.phone ? "כן" : "לא", c.model, c.year || "", c.plate, c.estKm || "", c.n ? c.n.nextKm : "", c.n ? c.n.dueDate.toISOString().slice(0, 10) : "", c.test_expiry || "", c.last_visit || "", recallsOf(c).map(x => x.system).join(" / ")].map(q).join(","))]);
    toast(`ייצאתי ${list.length} רכבים`);
  };

  G.register({ id: "customers", core: true, tab: "customers", show: renderRows });
  Object.assign(G, { car, openAdd, openCustomer, renderRows });
})(window.Garage);
