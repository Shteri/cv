// Garage dashboard core: shared helpers, state, the message dialog, screens, demo data and the module registry.
// Feature modules live in modules/*.js; they read these through the Garage object and register themselves.
(function () {
  const G = window.Garage = {};
  const D = window.TIPULIT_DATA, Cloud = window.TipulitCloud || { enabled: false }, E = window.TipulitEngine, L = window.TipulitLookup;
  const $ = (s, r = document) => r.querySelector(s), $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const fmt = n => Math.round(n).toLocaleString("he-IL");
  const esc = x => String(x ?? "").replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/"/g, "&quot;");
  const fmtDate = iso => { try { return new Intl.DateTimeFormat("he-IL", { day: "2-digit", month: "2-digit", year: "2-digit" }).format(new Date(iso)); } catch (e) { return iso; } };
  const monthName = d => new Intl.DateTimeFormat("he-IL", { month: "long", year: "numeric" }).format(d);
  const fmtPlate = d => d.length <= 7 ? d.replace(/(\d{2})(\d{3})(\d{2})/, "$1-$2-$3") : d.replace(/(\d{3})(\d{2})(\d{3})/, "$1-$2-$3");
  const digits = v => String(v || "").replace(/\D/g, "");
  const schedById = id => D.schedules.find(s => s.id === id);
  const itemName = k => (D.items[k] && D.items[k].he) || k;
  const today = () => new Date().toISOString().slice(0, 10);
  const why = e => window.TipulitCloud && TipulitCloud.why ? TipulitCloud.why(e) : "נסו שוב בעוד רגע.";
  const toastEl = $("#toast"); let toastT;
  const toast = m => { toastEl.textContent = m; toastEl.classList.add("show"); clearTimeout(toastT); toastT = setTimeout(() => toastEl.classList.remove("show"), 2600); };
  const telHref = p => "tel:" + p.replace(/[^\d+*#]/g, "");
  const waHref = (p, text) => "https://wa.me/" + p.replace(/\D/g, "").replace(/^0/, "972") + (text ? "?text=" + encodeURIComponent(text) : "");
  const theModel = m => /^[A-Za-z0-9]/.test(m) ? "ה-" + m : "ה" + m;
  const ico = {
    wa: `<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 20l1.3-3.9A8 8 0 1 1 8.2 19z"/><path d="M9 9.5c0 3 2.5 5.5 5.5 5.5l1-1.5-2-1-1 1a4 4 0 0 1-2-2l1-1-1-2z"/></svg>`,
    phone: `<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 4h4l2 5-2.5 1.5a11 11 0 0 0 5 5L15 13l5 2v4a2 2 0 0 1-2 2A16 16 0 0 1 3 6a2 2 0 0 1 2-2z"/></svg>`,
    wrench: `<svg aria-hidden="true" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.5 2.5-2.4-.6-.6-2.4z"/></svg>`
  };
  const demo = new URLSearchParams(location.search).has("demo");
  // Every write goes through this, so the demo can run the same screens on in-memory data.
  const api = demo ? null : Cloud;

  // ---------- state ----------
  const st = { garage: null, garages: [], rows: [], wos: [], recalls: {}, filter: "all", sort: "due", q: "", tab: "customers", groups: [] };
  const monthsSince = iso => iso ? Math.max(0, (Date.now() - Date.parse(iso)) / (30.44 * 86400000)) : 0;
  // what this garage replaced on a car, for parts replaced off the schedule (engine planAt)
  const recordsOf = carId => st.wos.filter(w => w.garage_car_id === carId && w.km > 0).map(w => ({ km: w.km, items: w.items || [], kind: w.kind }));
  function view(r) {
    const s = schedById(r.schedule_id), kmMonth = r.km_month || 1500;
    const estKm = r.km ? Math.round(r.km + kmMonth * monthsSince(r.km_at)) : null;
    // the last periodic service this garage recorded: the next one is counted from where it was actually done
    const lastSvc = st.wos.filter(w => w.garage_car_id === r.car_id && w.kind === "service" && w.km > 0).reduce((a, w) => !a || w.km > a.km ? { km: w.km, svcKm: w.svc_km || null } : a, null);
    let n = null; try { if (s && estKm !== null) n = E.next(s, { km: Math.max(estKm, lastSvc ? lastSvc.km : 0), kmMonth, lastService: r.last_service, lastSvc, records: recordsOf(r.car_id) }); } catch (e) {}
    const testDays = r.test_expiry ? Math.round((Date.parse(r.test_expiry) - Date.now()) / 86400000) : null;
    const plateDigits = digits(r.plate);
    return { ...r, s, estKm, n, testDays, plateDigits, plate: plateDigits ? fmtPlate(plateDigits) : "",
      lapsed: monthsSince(r.last_visit || r.created_at) > 12,
      model: s ? `${s.make_he} ${s.model_he}` : (r.gov && r.gov.commercial_name) || "רכב" };
  }
  const recallsOf = c => st.recalls[c.plateDigits] || [];
  const isDue = c => c.n && c.n.level === "warn";
  const isOver = c => c.n && c.n.level === "crit";
  const isTest = c => c.testDays !== null && c.testDays <= 45;
  const FILTERS = [["all", "כל הלקוחות"], ["due", "מגיעים לטיפול"], ["over", "באיחור"], ["test", "טסט קרוב"], ["recall", "ריקול פתוח"], ["lapsed", "לא היו מעל שנה"], ["app", "באפליקציה"]];
  const match = (c, f) => f === "all" || (f === "due" && isDue(c)) || (f === "over" && isOver(c)) || (f === "test" && isTest(c)) || (f === "recall" && recallsOf(c).length) || (f === "lapsed" && c.lapsed) || (f === "app" && c.linked);

  function message(c) {
    const hi = `היי${c.name ? " " + c.name.split(" ")[0] : ""}, כאן ${st.garage.name}. `, m = c.s ? `${c.s.make_he} ${c.s.model_he}` : "רכב";
    const f = st.filter;
    if (f === "recall" || (f === "all" && recallsOf(c).length)) return hi + `לרכב שלך (${c.model} ${c.year || ""}) יש ריקול פתוח של היצרן. התיקון בלי תשלום במרכזי השירות של היבואן. רוצה שנתאם?`;
    if (f === "test" || (f === "all" && isTest(c) && !isOver(c) && !isDue(c))) return hi + `הטסט של ${theModel(m)} שלך בתוקף עד ${fmtDate(c.test_expiry)}. רוצה שנכין אותו לטסט?`;
    if (f === "lapsed") return hi + `מזמן לא ראינו את ${theModel(m)} שלך. ${c.n ? `לפי לוח היבואן הטיפול הבא הוא ${fmt(c.n.nextKm)} ק"מ. ` : ""}רוצה לקבוע תור?`;
    if (isOver(c)) return hi + `לפי לוח היבואן ${theModel(m)} שלך כבר עבר את מועד טיפול ${fmt(c.n.nextKm)}. רוצה לקבוע תור?`;
    if (c.n) return hi + `לפי לוח היבואן ${theModel(m)} שלך מגיע לטיפול ${fmt(c.n.nextKm)} בסביבות ${monthName(c.n.dueDate)}. רוצה לקבוע תור?`;
    return hi + "רוצה לקבוע תור לטיפול?";
  }

  // ---------- message ----------
  let msgFor = null;
  function openMsg(c) {
    msgFor = c; $("#msg-to").textContent = c.name || "הלקוח"; $("#msg-text").value = message(c);
    $("#msg-note").textContent = demo ? "מצב הדגמה: ההודעה לא נשלחת. בגרסה האמיתית הכפתור פותח את הוואטסאפ של המוסך עם ההודעה מוכנה." : "ההודעה נפתחת בוואטסאפ של המוסך. אפשר לערוך לפני השליחה.";
    syncMsg(); $("#dlg-msg").showModal();
  }
  const syncMsg = () => { const a = $("#msg-send"); if (demo) { a.removeAttribute("href"); a.classList.add("disabled"); } else { a.href = waHref(msgFor.phone, $("#msg-text").value); a.classList.remove("disabled"); } };
  $("#msg-text").oninput = syncMsg;
  $("#msg-send").onclick = e => { if (demo) { e.preventDefault(); toast("בהדגמה לא נשלחות הודעות"); } else $("#dlg-msg").close(); };
  $("#msg-copy").onclick = () => copy($("#msg-text").value, "ההודעה הועתקה");
  function copy(text, ok) { const done = () => toast(ok); if (navigator.clipboard && navigator.clipboard.writeText) navigator.clipboard.writeText(text).then(done).catch(() => fallbackCopy(text, done)); else fallbackCopy(text, done); }
  function fallbackCopy(text, done) { const t = document.createElement("textarea"); t.value = text; document.body.appendChild(t); t.select(); try { document.execCommand("copy"); done(); } catch (e) {} t.remove(); }

  function showTab(tab) {
    const prev = modules.find(m => m.tab === st.tab);
    st.tab = tab; $$(".tab").forEach(x => { x.classList.toggle("on", x.dataset.tab === tab); x.setAttribute("aria-selected", x.dataset.tab === tab ? "true" : "false"); });
    $$(".view").forEach(v => { v.hidden = v.id !== "view-" + tab; });
    if (prev && prev.tab !== tab && prev.hide) prev.hide();
    const m = modules.find(x => x.tab === tab); if (m && m.show) m.show();
  }
  $$(".tab").forEach(t => t.onclick = () => showTab(t.dataset.tab));
  const setSeg = (id, v) => $$(`#${id} button`).forEach(b => b.classList.toggle("on", b.dataset.v === v));
  // free-text WhatsApp message (reuses the message dialog)
  function openMsgText(name, phone, text) {
    msgFor = { phone }; $("#msg-to").textContent = name; $("#msg-text").value = text;
    // in the demo the customer's link opens here, so the other side can be tried too
    const link = demo && (text.match(/https?:\/\/\S+\/(?:approve|book|appt)\/\S*/) || [])[0];
    $("#msg-note").innerHTML = demo ? `מצב הדגמה: ההודעה לא נשלחת.${link ? ` <a href="${esc(link)}" target="_blank" rel="noopener">לפתוח את הקישור כמו הלקוח</a>` : ""}` : "ההודעה נפתחת בוואטסאפ של המוסך. אפשר לערוך לפני השליחה.";
    syncMsg(); $("#dlg-msg").showModal();
  }
  let qrLib = null;
  const loadQr = () => qrLib || (qrLib = new Promise((res, rej) => { const sc = document.createElement("script"); sc.src = "https://cdn.jsdelivr.net/npm/qrcode-generator@1.4.4/qrcode.js"; sc.onload = () => res(window.qrcode); sc.onerror = () => { qrLib = null; rej(new Error("qr")); }; document.head.appendChild(sc); }));
  function download(name, lines) { const blob = new Blob(["﻿" + lines.join("\r\n")], { type: "text/csv;charset=utf-8" }); const a = document.createElement("a"); a.href = URL.createObjectURL(blob); a.download = name; document.body.appendChild(a); a.click(); a.remove(); setTimeout(() => URL.revokeObjectURL(a.href), 2000); }
  const numIn = v => { const n = parseFloat(String(v ?? "").replace(/[^\d.-]/g, "")); return Number.isFinite(n) ? n : null; };
  const nf = n => (+n || 0).toLocaleString("he-IL", { maximumFractionDigits: 2 });
  const money = n => "₪" + nf(Math.round((+n || 0) * 100) / 100);
  const qtyOf = (n, unit) => nf(n) + (unit === "liter" ? " ל'" : "");
  const oilLiters = s => { const t = s && s.specs && s.specs.oil_capacity; if (!t) return null; const m = t.match(/(\d+(?:\.\d+)?)\s*ליטר/g); if (!m || m.length !== 1) { const all = t.match(/\d+(?:\.\d+)?/g); return all && all.length === 1 ? +all[0] : null; } return +m[0].match(/\d+(?:\.\d+)?/)[0]; };

  // ---------- modules ----------
  // Every feature beyond the core lives in modules/*.js and calls Garage.register(). Core modules are always on; the
  // others are switched per garage (garage_profiles.modules) and, until the garage chooses, follow what it is licensed
  // for in the Ministry of Transport registry (professions grouped below).
  // A module: { id, name, desc, core, groups ("all" or group keys), tab, show(), hide(), state, load(garageId), demo(DEMO) }
  const modules = [];
  const GROUPS = { mech: [10, 15, 20, 22, 23], elec: [30, 144, 205], tire: [90, 91, 130, 135, 143, 195], body: [70, 80, 100, 175, 177], check: [170, 180, 181, 187, 188, 300], spec: [33, 60, 81, 145, 160, 206] };
  const GROUP_NAMES = { mech: "מכונאות", elec: "חשמל ומיזוג", tire: "צמיגים ומתלים", body: "פחחות וצבע", check: "בדיקות ורישוי", spec: "עבודות מומחה" };
  let enabled = null;   // Set of switched-on module ids; null = all
  const register = m => { modules.push(m); };
  // Buttons a module adds to another module's screens: place = "appt" (appointment card) or "car" (car box in the customer card).
  // action: { module, label, when(ctx), run(ctx) }
  const actions = { appt: [], car: [] };
  // Rows a module adds to the customer card's history: fn(cars) -> [{ date, km, html }]
  const timelines = [];
  const addTimeline = (module, fn) => timelines.push({ module, fn });
  const timelineFor = cars => timelines.filter(t => on(t.module)).flatMap(t => t.fn(cars));
  const addAction = (place, a) => actions[place].push(a);
  function renderActions(place, ctx, cls = "btn") {
    const list = actions[place].filter(a => on(a.module) && (!a.when || a.when(ctx)));
    return { html: list.map((a, i) => `<button type="button" class="${cls}" data-act-${place}="${i}">${esc(a.label)}</button>`).join(""),
      bind: root => $$(`[data-act-${place}]`, root).forEach(b => b.onclick = () => list[+b.getAttribute(`data-act-${place}`)].run(ctx)) };
  }
  const on = id => { const m = modules.find(x => x.id === id); return !!m && (m.core || !enabled || enabled.has(id)); };
  const call = (name, ...a) => typeof G[name] === "function" ? G[name](...a) : undefined;
  const clone = o => JSON.parse(JSON.stringify(o));
  const resetModules = () => { for (const m of modules) if (m.state) Object.assign(st, clone(m.state)); };
  let registry = null;
  const loadRegistry = () => registry || (registry = fetch("../garages.json").then(r => r.json()).then(d => new Map(d.garages.map(r => [r[0], r[6] || []]))).catch(() => new Map()));
  async function resolveModules(g) {
    const codes = g.garage_id ? ((await loadRegistry()).get(+g.garage_id) || []) : [];
    st.groups = Object.keys(GROUPS).filter(k => codes.some(c => GROUPS[k].includes(c)));
    if (Array.isArray(g.modules)) enabled = new Set(g.modules);
    else enabled = st.groups.length ? new Set(modules.filter(m => !m.core && (m.groups === "all" || (m.groups || []).some(x => st.groups.includes(x)))).map(m => m.id)) : null;
  }
  function applyModules() {
    $$("[data-module]").forEach(el => { el.hidden = !on(el.dataset.module); });
    const cur = modules.find(m => m.tab === st.tab);
    if (cur && !on(cur.id)) showTab("customers");
  }
  // "what shows on the board": the garage switches modules on and off
  function openModules() {
    const opt = modules.filter(m => !m.core);
    $("#md-from").textContent = st.groups.length ? `לפי הרישיון במשרד התחבורה המוסך עוסק ב: ${st.groups.map(k => GROUP_NAMES[k]).join(", ")}.` : ""; $("#md-from").hidden = !st.groups.length;
    $("#md-list").innerHTML = opt.map(m => `<label class="check"><input type="checkbox" data-mod="${m.id}" ${on(m.id) ? "checked" : ""}><span><b>${esc(m.name)}</b><br><span class="muted small">${esc(m.desc || "")}</span></span></label>`).join("");
    $("#md-err").hidden = true; $("#dlg-modules").showModal();
  }
  $("#btn-modules").onclick = openModules;
  // a garage that already has office software keeps it for invoices and stock
  $("#md-other").onclick = () => { for (const id of ["billing", "stock"]) { const x = $(`#md-list [data-mod="${id}"]`); if (x) x.checked = false; } toast("חשבוניות ומלאי כובו. לחצו שמור"); };
  $("#md-save").onclick = async () => {
    const list = $$("#md-list [data-mod]").filter(x => x.checked).map(x => x.dataset.mod);
    try {
      if (!demo) await api.updateGarageSettings(st.garage.id, { modules: list });
      st.garage.modules = list; $("#dlg-modules").close();
      if (demo) { enabled = new Set(list); applyModules(); call("renderRows"); } else await openGarage(st.garage);
      toast("נשמר");
    } catch (e) { $("#md-err").textContent = "השמירה נכשלה: " + why(e); $("#md-err").hidden = false; }
  };

  // ---------- recalls ----------
  async function loadRecalls(only) {
    if (demo || !L || !L.fetchRecalls) return;
    const plates = only || [...new Set(st.rows.map(c => c.plateDigits).filter(Boolean))];
    for (let i = 0; i < plates.length; i += 4) {
      await Promise.all(plates.slice(i, i + 4).map(p => L.fetchRecalls(p).then(r => { st.recalls[p] = r; }).catch(() => {})));
      call("renderRows");
    }
  }

  // ---------- screens ----------
  function showGate(title, text, actions) {
    $("#dash").hidden = true; $("#gate").hidden = false;
    $("#gate-title").textContent = title; $("#gate-text").textContent = text; $("#gate-actions").innerHTML = actions;
  }
  function showDash() {
    $("#gate").hidden = true; $("#dash").hidden = false; $("#demo-note").hidden = !demo;
    if (demo) demoSave();
    if (demo) $("#demo-reset").onclick = () => { if (confirm("למחוק את כל מה ששיניתם בהדגמה ולהתחיל מחדש?")) demoReset(); };
    $("#g-name").textContent = st.garage.name;
    $("#g-sub").textContent = [st.garage.address, st.garage.city].filter(Boolean).join(", ");
    $("#bar-garage").innerHTML = st.garages.length > 1 ? `<select id="g-pick" aria-label="בחירת מוסך">${st.garages.map(g => `<option value="${g.id}" ${g.id === st.garage.id ? "selected" : ""}>${esc(g.name)}</option>`).join("")}</select>` : "";
    const gp = $("#g-pick"); if (gp) gp.onchange = () => openGarage(st.garages.find(g => g.id === gp.value));
    applyModules(); call("renderRows");
  }
  async function reload() {
    const id = st.garage.id, soft = (f, empty = []) => Promise.resolve().then(f).catch(() => empty);
    const [book, wos] = await Promise.all([api.garageBook(id), soft(() => api.workOrders(id))]);
    st.wos = wos; st.rows = book.map(view);
    // each switched-on module loads its own data; a module whose tables are not on the server yet just shows empty
    await Promise.all(modules.filter(m => m.load && on(m.id)).map(m => soft(() => m.load(id), null)));
  }
  async function openGarage(g) {
    st.garage = g; st.rows = []; st.wos = []; st.recalls = {}; st.filter = "all"; resetModules();
    try { localStorage.setItem("tipulit-garage", g.id); } catch (e) {}
    await resolveModules(g);
    showDash(); $("#rows").innerHTML = `<tr><td colspan="7" class="muted">טוען לקוחות…</td></tr>`;
    try { await reload(); }
    catch (e) { showGate("הטעינה נכשלה", /schema cache|does not exist|garage_book/i.test(e.message || "") ? "השרת עדיין לא מוכן לספר הלקוחות (צריך להריץ את מיגרציה 0005)." : (e.message || String(e)), `<a class="btn" href="./">נסה שוב</a>`); return; }
    call("renderRows"); loadRecalls();
  }
  function renderUser(u) {
    $("#bar-user").innerHTML = demo ? `<a class="btn small" href="./">יציאה מההדגמה</a>` : u ? `<span class="muted small">${esc(u.email)}</span><button class="btn small" id="sign-out">התנתק</button>` : "";
    const so = $("#sign-out"); if (so) so.onclick = async () => { try { await Cloud.signOut(); } catch (e) {} location.reload(); };
  }
  const signInBtn = `<button class="btn primary" id="sign-in">התחברות עם Google</button>`;
  function wireSignIn() { const b = $("#sign-in"); if (b) b.onclick = () => { try { sessionStorage.setItem("tipulit-return", location.pathname); } catch (e) {} Cloud.signInWithGoogle().catch(e => toast("ההתחברות נכשלה: " + why(e))); }; }

  async function start() {
    if (demo) { st.garages = [st.garage = DEMO.garage]; st.wos = DEMO.wos; st.rows = DEMO.rows.map(view); st.recalls = DEMO.recalls; resetModules(); for (const m of modules) if (m.demo) m.demo(DEMO); enabled = DEMO.modules ? new Set(DEMO.modules) : null; renderUser(null); showDash(); return; }
    if (!Cloud.enabled) { showGate("השרת לא מחובר", "אפשר לראות איך זה נראה בהדגמה.", `<a class="btn primary" href="?demo">הדגמה</a>`); return; }
    if (Cloud.hasAuthParams) { const r = await Cloud.handleRedirect(); if (r.error) toast("ההתחברות נכשלה: " + why(r.error)); try { history.replaceState(null, "", location.pathname); } catch (e) {} }
    const u = await Cloud.currentUser(); renderUser(u);
    if (!u) { showGate("ניהול הלקוחות של המוסך", "מי מגיע לטיפול, מה להזמין, וההיסטוריה של כל רכב. לפי לוח היבואן של כל דגם.", signInBtn + `<a class="btn" href="?demo">הדגמה בלי התחברות</a>`); wireSignIn(); return; }
    let mine = []; try { mine = await Cloud.myGarageProfiles(); } catch (e) {}
    st.garages = mine.filter(p => p.status === "verified");
    if (!st.garages.length) {
      const pending = mine.some(p => p.status === "pending");
      showGate(pending ? "המוסך שלך בבדיקה" : "עוד אין לך מוסך מאומת", pending ? "אחרי שנאמת שהמוסך שלך, הלוח ייפתח כאן." : "רשמו את המוסך באפליקציה: מחפשים אותו במאגר המוסכים המורשים וממלאים פרופיל. אחרי אימות הלוח ייפתח כאן.", `<a class="btn primary" href="../?garage=claim">רישום המוסך</a><a class="btn" href="?demo">הדגמה</a>`);
      return;
    }
    let last = null; try { last = localStorage.getItem("tipulit-garage"); } catch (e) {}
    openGarage(st.garages.find(x => x.id === last) || st.garages[0]);
  }

  // ---------- demo: a garage with a few years of history that follows each car's real schedule ----------
  // Nothing is sent. What you change is kept in this browser (localStorage), and the customer pages opened from
  // the demo (approval link, online booking) write back to the same place, so both sides can be tried.
  const DEMO_KEY = "tipulit-garage-demo", DEMO_V = 2;
  const newToken = () => (crypto.randomUUID ? crypto.randomUUID() : "t" + Date.now().toString(36) + Math.random().toString(36).slice(2));
  const PRICE = { engine_oil: 52, oil_filter: 55, air_filter: 95, cabin_filter: 90, brake_fluid: 70, spark_plugs: 75, coolant: 140, transmission_oil: 320, brake_pads: 340, brake_discs: 520, battery_12v: 520, wipers: 110, timing_belt: 1400, drive_belt: 240, fuel_filter: 160 };
  function genDemo() {
    let seed = 11; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280, rint = (a, b) => a + Math.floor(rnd() * (b - a + 1)), chance = p => rnd() < p;
    const DAY = 86400000, now = Date.now(), dateAt = t => new Date(t).toISOString().slice(0, 10), iso = days => new Date(now + days * DAY).toISOString(), rate = 280;
    const models = ["toyota-corolla-2013-2019-1.6", "toyota-corolla-2019-2025-1.8-hybrid", "kia-picanto-2017-2025", "hyundai-i10-2014-2019", "hyundai-i20-2015-2017", "mazda-3-2013-2019",
      "skoda-octavia-2017-2026-1.0-1.5-tsi", "kia-sportage-2016-2018", "hyundai-tucson-2015-2020-1.6-2.0", "kia-niro-2016-2022-1.6-hybrid", "toyota-yaris-2011-2019-1.33-1.5", "mazda-cx-5-2012-2025",
      "hyundai-i10-2020-2025", "toyota-rav4-2016-2019-2.5-hybrid", "kia-sportage-2022-2025-1.6-2.0"].map(schedById).filter(Boolean);
    const names = ["דני כהן", "מיכל לוי", "יוסי מזרחי", "רונית פרץ", "אבי ביטון", "נועה אברהם", "משה דהן", "שירה אזולאי", "איתי פרידמן", "ליאת שלום", "עומר חדד", "תמר גבאי", "רועי עמר", "הדס כץ", "אלון יוסף", "מאיה בן דוד", "גיא אוחיון", "יעל שטרן", "עידו חזן", "אורית מלכה", "ניר וקנין", "קרן סויסה", "שי אלון", "ענבל רוזן", "בני גולן", "סיגל נחום", "אסף טל", "דנה קורן", "חיים אדרי", "רחל שגיא", "תומר זילבר", "אורנה ברק"];
    const part = (k, s, qty) => ({ type: "part", item: k, desc: itemName(k), qty: qty || (k === "engine_oil" ? oilLiters(s) || 4 : k === "spark_plugs" ? 4 : k === "wipers" ? 2 : 1), price: PRICE[k] || 120 });
    const labor = (desc, h) => ({ type: "labor", desc, qty: 1, price: Math.round(h * rate / 10) * 10 });
    const total = lines => Math.round(lines.reduce((a, l) => a + l.qty * l.price, 0));
    // repairs that happen to real cars; some replace a part that is also on the schedule
    const FAULTS = [
      { text: "רעידות במנוע בהתנעה, הוחלפו מצתים", items: ["spark_plugs"], h: 1 },
      { text: "נורת מנוע, מסנן אוויר סתום", items: ["air_filter"], h: .3 },
      { text: "דוושת בלם רכה, הוחלף נוזל בלמים", items: ["brake_fluid"], h: .8 },
      { text: "חריקה מהמנוע, הוחלפה רצועת עזר", items: ["drive_belt"], h: 1.2 },
      { text: "המזגן לא מקרר, מילוי גז ובדיקת דליפות", items: [], h: 1.5, extra: [{ type: "part", desc: "גז מזגן", qty: 1, price: 250 }] },
      { text: "החלפת נורת פנס קדמי", items: [], h: .3, extra: [{ type: "part", desc: "נורה H7", qty: 1, price: 45 }] },
      { text: "דליפת נוזל קירור מהצינור העליון", items: ["coolant"], h: 1.5, extra: [{ type: "part", desc: "צינור קירור עליון", qty: 1, price: 180 }] }];
    const rows = [], wos = [];
    names.forEach((name, i) => {
      const s = models[i % models.length], y0 = Math.max(s.years[0], 2012), y1 = Math.min(s.years[1], 2025), year = rint(y0, Math.max(y0, y1));
      const kmMonth = [700, 1000, 1300, 1500, 1500, 1800, 2300][rint(0, 6)], ageMonths = Math.max(4, (2026 - year) * 12 + rint(-4, 6));
      let km = Math.round(ageMonths * kmMonth * (0.85 + rnd() * .3) / 100) * 100;
      const fresh = i < 3, newcomer = i % 9 === 8;
      // a quarter of the cars are a few hundred km from their next service
      if (!fresh && i % 4 === 1) km = E.gridAfter(s, km).km - rint(200, 1300);
      // three cars were here this week, so there is something to invoice
      if (fresh) { const g = E.gridAfter(s, km - s.interval.km); km = g.km + rint(200, 900); }
      const timeAt = k => now - (km - k) / kmMonth * 30.44 * DAY;
      const phone = chance(.88) ? `05${[0, 2, 3, 4, 8][rint(0, 4)]}-${rint(2000000, 9899999)}` : null;
      const r = { car_id: "dcar-" + i, customer_id: "dcus-" + i, name, phone, own_phone: phone, can_contact: !!phone, source: i % 5 === 0 ? "app" : i % 3 === 0 ? "import" : "manual", notes: null,
        plate: String(rint(10, 99)) + String(rint(100, 999)) + String(rint(10, 99)) + (year >= 2017 ? String(rint(0, 9)) : ""), schedule_id: s.id, year, km, km_month: kmMonth, km_at: iso(-rint(0, 40)),
        last_service: null, test_expiry: iso(rint(-20, 330)).slice(0, 10), linked: i % 5 === 0, share_history: i % 10 === 0, last_visit: null, visits: 0, pending: 0, created_at: iso(-rint(30, 1400)) };
      rows.push(r);
      if (newcomer) return;
      // customer since: some since the first service, most for the last two to five years
      const since = chance(.3) ? 0 : Math.max(0, km - rint(24, 60) * kmMonth);
      const recs = [], add = (kind, k, extra) => { if (k <= since || k > km) return; recs.push({ kind, km: k, ...extra }); };
      // periodic services on the importer's grid, mostly a little late, now and then skipped
      for (let g = E.gridAfter(s, since); g.km <= km; g = E.gridAfter(s, g.km)) {
        if (!fresh && chance(.08) && g.km < km - s.interval.km) continue;
        const k = fresh && E.gridAfter(s, g.km).km > km ? km - rint(50, 150) : g.km + rint(-1500, 3500);
        add("service", Math.min(k, km - 100), { svc: g });
      }
      // wear: brake pads, battery, wipers
      for (let k = since + rint(35000, 55000); k < km; k += rint(40000, 60000)) add("repair", k, { text: "רפידות בלם קדמיות שחוקות", items: ["brake_pads"], h: .8 });
      for (let k = since + rint(40, 60) * kmMonth; k < km; k += rint(44, 60) * kmMonth) add("repair", k, { text: "המצבר לא החזיק, הוחלף", items: ["battery_12v"], h: .3 });
      if (chance(.35)) { const f = FAULTS[rint(0, FAULTS.length - 1)]; add("repair", km - rint(3000, 25000), f); }
      recs.sort((a, b) => a.km - b.km);
      const done = [];
      for (const x of recs) {
        let items, lines, kind = x.kind, notes = null;
        if (kind === "service") {
          items = E.planAt(s, done, x.svc.svc, x.svc.km).replace;
          lines = [...items.map(k => part(k, s)), labor("עבודה, טיפול תקופתי", .8 + items.length * .15)];
          if (chance(.25)) { lines.push(part("wipers", s)); items = [...items, "wipers"]; }
        } else {
          items = x.items; lines = [...items.map(k => part(k, s)), ...(x.extra || []), labor("עבודה", x.h)]; notes = x.text;
        }
        const t = timeAt(x.km);
        wos.push({ id: "dwo-" + i + "-" + wos.length, garage_car_id: r.car_id, kind, svc_km: kind === "service" ? x.svc.km : null, km: x.km, date: dateAt(t), items, lines, total: total(lines), notes, entry_id: r.linked ? "x" : null });
        done.push({ km: x.km, items, kind });
        if (kind === "service") r.last_service = dateAt(t).slice(0, 7);
        r.last_visit = dateAt(t); r.visits++;
      }
      if (fresh) r.km_at = new Date(timeAt(km - 100)).toISOString();
    });
    wos.sort((a, b) => b.date.localeCompare(a.date));
    // drivers who share their app history: services from before they came here
    const history = {};
    for (const r of rows.filter(x => x.share_history)) {
      const s = schedById(r.schedule_id), first = wos.filter(w => w.garage_car_id === r.car_id).pop(), upto = first ? first.km - 5000 : r.km;
      const g = E.gridAfter(s, Math.max(0, upto - s.interval.km * 1.5));
      if (g.km < upto) history[r.car_id] = [{ date: iso(-Math.round((r.km - g.km) / r.km_month * 30.44)).slice(0, 7), km: g.km + 800, kind: "service", svc_km: g.km, items: g.svc.items.filter(x => x.action === "replace").map(x => x.item), garage: "מוסך היבואן", verified: true, own: false }];
    }
    const recalls = {}; for (const i of [2, 9, 17]) recalls[rows[i].plate] = [{ system: ["כריות אוויר", "מערכת בלימה", "חשמל ומיזוג"][i % 3] }];
    // calendar: cars that are due come in for service; a couple of repairs and a test prep
    const due = rows.map(r => { const s = schedById(r.schedule_id); let n = null; try { n = E.next(s, { km: r.km, kmMonth: r.km_month, lastService: r.last_service, records: wos.filter(w => w.garage_car_id === r.car_id), lastSvc: (w => w ? { km: w.km, svcKm: w.svc_km } : null)(wos.find(w => w.garage_car_id === r.car_id && w.kind === "service")) }); } catch (e) {} return { r, n }; })
      .filter(x => x.n && x.n.level !== "good").map(x => x.r);
    const appts = genAppts(rows, due, rnd), approvals = [];
    // a customer who did not show up twice: their new online booking tomorrow waits for the garage
    const ns = rows[6], tmr = new Date(); tmr.setHours(0, 0, 0, 0); tmr.setDate(tmr.getDate() + (tmr.getDay() === 5 ? 2 : 1));
    const nsAppt = (days, h, status, extra = {}) => ({ id: `dap-ns-${days}`, garage_id: "demo", garage_car_id: ns.car_id, customer_name: ns.name, phone: ns.phone || "052-7000007", plate: ns.plate, kind: "service", note: null, starts_at: new Date(new Date(tmr).setHours(h, 0) + days * DAY).toISOString(), minutes: 60, bay: 3, status, source: "online", work_order_id: null, token: newToken(), ...extra });
    appts.push(nsAppt(-19, 9, "no_show"), nsAppt(-74, 11, "no_show"), nsAppt(0, 15, "booked", { needs_ok: true }));
    const wa = appts.find(a => a.status === "waiting_approval");
    if (wa) approvals.push({ id: "daw-1", garage_id: "demo", garage_car_id: wa.garage_car_id, appointment_id: wa.id, message: "בזמן הטיפול ראינו שרפידות הבלם הקדמיות שחוקות (נשארו 2 מ\"מ). מומלץ להחליף עכשיו.", lines: [{ desc: "רפידות בלם קדמיות", price: 340 }, { desc: "עבודה", price: 220 }], total: 560, status: "pending", created_at: new Date().toISOString() });
    // a past vehicle inspection, answered by the customer
    const ir = rows[1];
    approvals.push({ id: "dins-1", garage_id: "demo", garage_car_id: ir.car_id, appointment_id: null, message: "תוצאות בדיקת הרכב", km: ir.km - 2000, created_at: iso(-20), decided_at: iso(-20), status: "approved", approved_lines: [0],
      lines: [{ desc: "רפידות בלם קדמיות", price: 560, check: "brakes_front", urgent: true }, { desc: "החלפת מגבים", price: 110, check: "wipers" }], total: 670,
      checks: [{ key: "brakes_front", label: "בלמים קדמיים", status: "now", note: "נשארו 2 מ\"מ" }, { key: "wipers", label: "מגבים ונוזל שמשות", status: "soon", note: "משאירים פסים" }, { key: "tires", label: "צמיגים", status: "ok" }, { key: "lights", label: "אורות", status: "ok" }, { key: "battery", label: "מצבר", status: "ok", note: "12.6V" }] });
    // inventory: common service parts, two suppliers, one order on the way and one received
    const sups = [{ id: "dsp-1", name: "חלפים מרכז", contact: "אבי", phone: "03-5550101", email: null, notes: "אספקה למחרת" }, { id: "dsp-2", name: "שמנים ישיר", contact: "רינה", phone: "054-5550202", email: null, notes: null }, { id: "dsp-3", name: "מצברים ובלמים", contact: "שלומי", phone: "052-5550303", email: null, notes: "מגיע פעמיים בשבוע" }];
    const P = (id, sku, name, item_key, stock, min, cost, price, sup, extra = {}) => ({ id, garage_id: "demo", sku, name, item_key, stock, min_stock: min, cost, price, supplier_id: sup, unit: "unit", active: true, brand: null, fits: null, location: null, ...extra });
    const parts = [
      P("dpt-1", "OIL-5W30-208", "שמן מנוע 5W-30 (חבית)", "engine_oil", 46, 40, 28, 52, "dsp-2", { unit: "liter", fits: "סקודה, מאזדה, יונדאי, קיה", location: "חבית 1" }),
      P("dpt-2", "OIL-0W20-208", "שמן מנוע 0W-20 (חבית)", "engine_oil", 18, 30, 34, 62, "dsp-2", { unit: "liter", fits: "טויוטה, קיה נירו", location: "חבית 2" }),
      P("dpt-3", "W712/95", "מסנן שמן MANN W712/95", "oil_filter", 9, 6, 24, 60, "dsp-1", { fits: "סקודה", location: "מדף 1" }),
      P("dpt-4", "90915-YZZE1", "מסנן שמן טויוטה", "oil_filter", 3, 6, 22, 55, "dsp-1", { fits: "טויוטה", location: "מדף 1" }),
      P("dpt-5", "26300-35505", "מסנן שמן יונדאי/קיה", "oil_filter", 12, 6, 18, 50, "dsp-1", { fits: "יונדאי, קיה", location: "מדף 1" }),
      P("dpt-12", "PE01-14-302", "מסנן שמן מאזדה", "oil_filter", 5, 4, 26, 60, "dsp-1", { fits: "מאזדה", location: "מדף 1" }),
      P("dpt-6", "CU-2939", "מסנן מזגן", "cabin_filter", 4, 5, 30, 90, "dsp-1", { location: "מדף 2" }),
      P("dpt-7", "C-27009", "מסנן אוויר", "air_filter", 7, 4, 35, 95, "dsp-1", { location: "מדף 2" }),
      P("dpt-8", "DOT4-1L", "נוזל בלמים DOT4", "brake_fluid", 2, 3, 25, 70, "dsp-2", { unit: "liter", location: "מדף 3" }),
      P("dpt-9", "NGK-ILKAR7", "מצת NGK", "spark_plugs", 16, 8, 32, 75, "dsp-1", { location: "מגירה 1" }),
      P("dpt-13", "COOL-G12-5L", "נוזל קירור G12", "coolant", 10, 5, 22, 45, "dsp-2", { unit: "liter", location: "מדף 3" }),
      P("dpt-10", "BAT-60", "מצבר 60 אמפר", "battery_12v", 2, 2, 290, 520, "dsp-3", { location: "מחסן" }),
      P("dpt-14", "BAT-70", "מצבר 70 אמפר", "battery_12v", 1, 1, 340, 590, "dsp-3", { fits: "רכבי שטח", location: "מחסן" }),
      P("dpt-11", "BP-F-COR", "רפידות בלם קדמיות טויוטה", "brake_pads", 2, 2, 140, 340, "dsp-3", { fits: "טויוטה", location: "מדף 4" }),
      P("dpt-15", "BP-F-HK", "רפידות בלם קדמיות יונדאי/קיה", "brake_pads", 3, 2, 120, 320, "dsp-3", { fits: "יונדאי, קיה", location: "מדף 4" }),
      P("dpt-16", "WB-600", "מגב 60 ס\"מ", "wipers", 8, 6, 22, 55, "dsp-1", { location: "מדף 5" }),
    ];
    const pos = [
      { id: "dpo-3", garage_id: "demo", number: 3, supplier_id: "dsp-3", status: "draft", note: null, created_at: iso(0), lines: [{ part_id: "dpt-10", sku: "BAT-60", name: "מצבר 60 אמפר", qty: 3, cost: 290 }], total: 870 },
      { id: "dpo-2", garage_id: "demo", number: 2, supplier_id: "dsp-1", status: "sent", note: null, sent_at: iso(-1), created_at: iso(-1), lines: [{ part_id: "dpt-4", sku: "90915-YZZE1", name: "מסנן שמן טויוטה", qty: 10, cost: 22 }, { part_id: "dpt-6", sku: "CU-2939", name: "מסנן מזגן", qty: 6, cost: 30 }], total: 400 },
      { id: "dpo-1", garage_id: "demo", number: 1, supplier_id: "dsp-2", status: "received", note: null, sent_at: iso(-12), received_at: iso(-10), created_at: iso(-12), lines: [{ part_id: "dpt-1", sku: "OIL-5W30-208", name: "שמן מנוע 5W-30 (חבית)", qty: 60, cost: 28, received: 60 }], total: 1680 },
    ];
    // every visit in the last 14 months has a document, except this week's
    const pays = ["card", "card", "card", "cash", "transfer", "app"], byName = Object.fromEntries(rows.map(r => [r.car_id, r.name])), cut = dateAt(now - 400 * DAY), week = dateAt(now - 7 * DAY);
    let no = 20001; const invoices = wos.filter(w => w.date >= cut && w.date < week).reverse().map(w => ({ id: "div-" + w.id, garage_id: "demo", work_order_id: w.id, kind: "invoice_receipt", provider: chance(.85) ? "morning" : "manual", number: String(no++), url: null, customer_name: byName[w.garage_car_id], total: w.total, payment: pays[rint(0, pays.length - 1)], issued_at: w.date + "T12:00:00Z" })).reverse();
    return { v: DEMO_V, garage: { id: "demo", name: "מוסך הדגמה", city: "חולון", address: "הפלד 40", phone: "03-5551234", bays: 3, slot_minutes: 60, booking_enabled: true, hours: {}, labor_rate: rate, cancel_hours: 12, noshow_limit: 2 },
      rows, wos, history, recalls, appts, approvals, parts, sups, pos, moves: [], invoices, billing: { api_id: "demo", has_secret: true, sandbox: false, vat_exempt: false }, jobs: null, modules: null };
  }
  // today and the next two working days, with statuses that match the time of day
  function genAppts(rows, due, rnd) {
    const appts = [], kinds = ["service", "service", "service", "repair", "service", "test"], notes = { repair: ["רעש מהבלמים בנסיעה", "נורת מנוע דולקת", "המזגן לא מקרר", "רעידות בהגה"], test: ["הכנה לטסט"] };
    let n = 0, nr = 0;
    for (let d = 0, made = 0; made < 3 && d < 6; d++) {
      const day = new Date(); day.setHours(0, 0, 0, 0); day.setDate(day.getDate() + d);
      if (day.getDay() === 6) continue; made++;
      const close = day.getDay() === 5 ? 13 : 17;
      // the demo's "now" is always inside a working day, so every status is visible: outside opening hours it is a
      // working morning, and late in the day it stops a few hours before closing
      const hr = new Date().getHours(), clock = d > 0 ? Date.now() : hr < 8 || hr >= close ? new Date(day).setHours(10, 45) : Math.min(Date.now(), new Date(day).setHours(close - 3, 15));
      for (let k = 0, h = 8; h < close - 1 && k < 14; k++) {
        const kind = kinds[k % kinds.length], r = kind === "service" && due.length ? due[n++ % due.length] : rows[(7 + nr++ * 5) % rows.length];
        const start = new Date(day); start.setHours(h, rnd() < .5 ? 0 : 30);
        const minutes = kind === "test" ? 60 : [60, 90, 120][Math.floor(rnd() * 3)], bay = 1 + (k % 3);
        const past = start.getTime() + minutes * 60000 < clock, nowish = start.getTime() < clock && !past;
        const status = past ? (rnd() < .9 ? "done" : "no_show") : nowish ? ["in_progress", "waiting_approval", "arrived"][k % 3] : "booked";
        // tomorrow some customers already answered the reminder, some got it and did not answer yet
        const answer = d === 0 ? {} : rnd() < .4 ? { reminded_at: new Date(Date.now() - 3 * 3600000).toISOString(), confirmed_at: new Date(Date.now() - 2 * 3600000).toISOString() } : rnd() < .5 ? { reminded_at: new Date(Date.now() - 3 * 3600000).toISOString() } : {};
        const nl = notes[kind]; appts.push({ id: `dap-${day.getTime()}-${k}`, garage_id: "demo", garage_car_id: r.car_id, customer_name: r.name, phone: r.phone, plate: r.plate, kind, note: nl ? nl[k % nl.length] : null, starts_at: start.toISOString(), minutes, bay, status, source: k % 3 === 2 ? "online" : "garage", work_order_id: null, token: newToken(), ...answer });
        if (k % 3 !== 0) h += 1;
      }
    }
    const today = appts.filter(a => new Date(a.starts_at).toDateString() === new Date().toDateString());
    const lastDone = today.filter(a => a.status === "done").pop(); if (lastDone) lastDone.status = "ready";
    if (!today.some(a => a.status === "waiting_approval")) { const b = today.find(a => a.status === "in_progress" || a.status === "arrived" || a.status === "booked"); if (b) b.status = "waiting_approval"; }
    return appts;
  }
  // the saved demo, or a fresh one; a saved demo from an earlier day gets a new calendar
  function loadDemo() {
    let x = null; try { x = JSON.parse(localStorage.getItem(DEMO_KEY) || "null"); } catch (e) {}
    if (!x || x.v !== DEMO_V) return genDemo();
    // demos saved before appointment links get a token per appointment
    for (const a of x.appts) if (!a.token) a.token = newToken();
    if (x.garage.cancel_hours === undefined) Object.assign(x.garage, { cancel_hours: 12, noshow_limit: 2 });
    const midnight = new Date().setHours(0, 0, 0, 0);
    if (!x.appts.some(a => Date.parse(a.starts_at) >= midnight)) { let sd = Date.now() % 233280; x.appts.push(...genAppts(x.rows, x.rows.slice(0, 12), () => (sd = (sd * 9301 + 49297) % 233280) / 233280)); }
    return x;
  }
  const DEMO = demo ? loadDemo() : null;
  // what the demo looks like now, merged with what the customer pages wrote (approvals answered, bookings made)
  function demoSave() {
    if (!demo || !st.garage) return;
    let saved = null; try { saved = JSON.parse(localStorage.getItem(DEMO_KEY) || "null"); } catch (e) {}
    const changed = saved && saved.v === DEMO_V ? demoMerge(saved) : false;
    Object.assign(DEMO, { garage: st.garage, rows: st.rows.map(({ s, n, ...r }) => r), wos: st.wos, recalls: st.recalls, modules: enabled ? [...enabled] : null });
    for (const k of ["parts", "sups", "pos", "moves", "invoices", "billing", "jobs"]) if (k in st) DEMO[k] = st[k];
    try { localStorage.setItem(DEMO_KEY, JSON.stringify(DEMO)); } catch (e) {}
    return changed;
  }
  function demoMerge(saved) {
    let changed = false;
    for (const x of saved.approvals || []) { const m = DEMO.approvals.find(a => a.id === x.id); if (m && m.status === "pending" && x.status !== "pending") { Object.assign(m, { status: x.status, approved_lines: x.approved_lines, decided_at: x.decided_at }); changed = true; } }
    for (const a of saved.appts || []) if (a.source === "online" && !DEMO.appts.some(b => b.id === a.id)) { DEMO.appts.push(a); changed = true; }
    // the customer's answers from the appointment page: confirmed, or cancelled (also when rescheduling)
    for (const x of saved.appts || []) {
      const m = DEMO.appts.find(a => a.id === x.id); if (!m) continue;
      if (x.confirmed_at && !m.confirmed_at) { m.confirmed_at = x.confirmed_at; changed = true; }
      if (x.status === "cancelled" && x.cancelled_by === "customer" && m.status === "booked") { Object.assign(m, { status: "cancelled", cancelled_by: "customer", cancelled_late: x.cancelled_late }); changed = true; }
    }
    return changed;
  }
  // an open dialog is left alone; the screen behind it refreshes
  function demoRefresh() { if (demoSave()) { showTab(st.tab); toast("עדכון מהלקוח הגיע"); } }
  if (demo) {
    setInterval(demoSave, 3000);
    addEventListener("pagehide", demoSave);
    addEventListener("storage", e => { if (e.key === DEMO_KEY) demoRefresh(); });
    addEventListener("focus", demoRefresh);
  }
  const demoReset = () => { try { localStorage.removeItem(DEMO_KEY); } catch (e) {} location.reload(); };

  Object.assign(G, { addAction, renderActions, addTimeline, timelineFor, D, Cloud, E, L, $, $$, fmt, esc, fmtDate, monthName, fmtPlate, digits, schedById, itemName, today, toast, why, telHref, waHref, theModel, ico, demo, api, st, monthsSince, view, recordsOf, recallsOf, isDue, isOver, isTest, FILTERS, match, message, openMsg, copy, showTab, setSeg, openMsgText, loadQr, download, numIn, nf, money, qtyOf, oilLiters, register, on, call, loadRecalls, reload, openGarage, DEMO, demoReset });
  G.boot = () => start().catch(e => showGate("משהו השתבש", why(e), `<a class="btn" href="./">נסה שוב</a>`));
})();
