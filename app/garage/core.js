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
  function view(r) {
    const s = schedById(r.schedule_id), kmMonth = r.km_month || 1500;
    const estKm = r.km ? Math.round(r.km + kmMonth * monthsSince(r.km_at)) : null;
    // the last periodic service this garage recorded: the next one is counted from where it was actually done
    const lastSvc = st.wos.filter(w => w.garage_car_id === r.car_id && w.kind === "service" && w.km > 0).reduce((a, w) => !a || w.km > a.km ? { km: w.km, svcKm: w.svc_km || null } : a, null);
    let n = null; try { if (s && estKm !== null) n = E.next(s, { km: Math.max(estKm, lastSvc ? lastSvc.km : 0), kmMonth, lastService: r.last_service, lastSvc }); } catch (e) {}
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
  function openMsgText(name, phone, text) { msgFor = { phone }; $("#msg-to").textContent = name; $("#msg-text").value = text; $("#msg-note").textContent = demo ? "מצב הדגמה: ההודעה לא נשלחת." : "ההודעה נפתחת בוואטסאפ של המוסך. אפשר לערוך לפני השליחה."; syncMsg(); $("#dlg-msg").showModal(); }
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
  $("#md-save").onclick = async () => {
    const list = $$("#md-list [data-mod]").filter(x => x.checked).map(x => x.dataset.mod);
    try {
      if (!demo) await api.updateGarageSettings(st.garage.id, { modules: list });
      st.garage.modules = list; $("#dlg-modules").close();
      if (demo) { enabled = new Set(list); applyModules(); call("renderRows"); } else await openGarage(st.garage);
      toast("נשמר");
    } catch (e) { $("#md-err").textContent = "השמירה נכשלה: " + (e.message || e); $("#md-err").hidden = false; }
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
  function wireSignIn() { const b = $("#sign-in"); if (b) b.onclick = () => { try { sessionStorage.setItem("tipulit-return", location.pathname); } catch (e) {} Cloud.signInWithGoogle().catch(e => toast("ההתחברות נכשלה: " + e.message)); }; }

  async function start() {
    if (demo) { st.garages = [st.garage = DEMO.garage]; st.wos = DEMO.wos; st.rows = DEMO.rows.map(view); st.recalls = DEMO.recalls; resetModules(); for (const m of modules) if (m.demo) m.demo(DEMO); enabled = null; renderUser(null); showDash(); return; }
    if (!Cloud.enabled) { showGate("השרת לא מחובר", "אפשר לראות איך זה נראה בהדגמה.", `<a class="btn primary" href="?demo">הדגמה</a>`); return; }
    if (Cloud.hasAuthParams) { const r = await Cloud.handleRedirect(); if (r.error) toast("ההתחברות נכשלה: " + (r.error.message || r.error)); try { history.replaceState(null, "", location.pathname); } catch (e) {} }
    const u = await Cloud.currentUser(); renderUser(u);
    if (!u) { showGate("ניהול הלקוחות של המוסך", "מי מגיע לטיפול, מה להזמין, וההיסטוריה של כל רכב. לפי לוח היבואן של כל דגם.", signInBtn + `<a class="btn" href="?demo">הדגמה בלי התחברות</a>`); wireSignIn(); return; }
    let mine = []; try { mine = await Cloud.myGarageProfiles(); } catch (e) {}
    st.garages = mine.filter(p => p.status === "verified");
    if (!st.garages.length) {
      const pending = mine.some(p => p.status === "pending");
      showGate(pending ? "המוסך שלך בבדיקה" : "עוד אין לך מוסך מאומת", pending ? "אחרי שנאמת שהמוסך שלך, הלוח ייפתח כאן." : "מצאו את המוסך שלכם ברשימת המוסכים באפליקציה ולחצו \"זה המוסך שלי\".", `<a class="btn primary" href="../">לאפליקציה</a><a class="btn" href="?demo">הדגמה</a>`);
      return;
    }
    let last = null; try { last = localStorage.getItem("tipulit-garage"); } catch (e) {}
    openGarage(st.garages.find(x => x.id === last) || st.garages[0]);
  }

  // ---------- demo: realistic customers, work orders and shared history; nothing is sent or stored ----------
  const DEMO = (() => {
    const pick = ["toyota-corolla", "kia-picanto", "hyundai-i10", "hyundai-tucson", "mazda-3", "skoda-octavia", "kia-sportage", "toyota-yaris", "hyundai-i20", "mazda-cx-5", "kia-niro", "toyota-rav4"];
    const scheds = pick.map(p => D.schedules.filter(s => s.id.startsWith(p + "-"))).filter(a => a.length).map(a => a[Math.floor(a.length / 2)]);
    const names = ["דני כהן", "מיכל לוי", "יוסי מזרחי", "רונית פרץ", "אבי ביטון", "נועה אברהם", "משה דהן", "שירה אזולאי", "איתי פרידמן", "ליאת שלום", "עומר חדד", "תמר גבאי", "רועי עמר", "הדס כץ", "אלון יוסף", "מאיה בן דוד", "גיא אוחיון", "יעל שטרן", "עידו חזן", "אורית מלכה", "ניר וקנין", "קרן סויסה", "שי אלון", "ענבל רוזן", "בני גולן", "סיגל נחום", "אסף טל", "דנה קורן", "חיים אדרי", "רחל שגיא", "תומר זילבר", "אורנה ברק"];
    let seed = 7; const rnd = () => (seed = (seed * 9301 + 49297) % 233280) / 233280;
    const iso = days => new Date(Date.now() + days * 86400000).toISOString();
    const rows = names.map((name, i) => {
      const s = scheds[i % scheds.length], year = Math.max(s.years[0], Math.min(s.years[1], 2015 + Math.floor(rnd() * 10)));
      const kmMonth = [800, 1200, 1500, 1500, 2000][Math.floor(rnd() * 5)], age = 2026 - year;
      const phone = rnd() < .85 ? `05${Math.floor(rnd() * 9)}-${String(1000000 + Math.floor(rnd() * 8999999)).slice(0, 7)}` : null;
      return { car_id: "dcar-" + i, customer_id: "dcus-" + i, name, phone, own_phone: phone, can_contact: !!phone, source: i % 5 === 0 ? "app" : i % 3 === 0 ? "import" : "manual", notes: null,
        plate: String(10000000 + Math.floor(rnd() * 89999999)).slice(0, year >= 2017 ? 8 : 7), schedule_id: s.id, year,
        km: Math.round((age * kmMonth * 12 * (0.85 + rnd() * .3)) / 100) * 100, km_month: kmMonth, km_at: iso(-Math.floor(rnd() * 120)),
        last_service: rnd() < .75 ? iso(-(20 + Math.floor(rnd() * 360))).slice(0, 7) : null, test_expiry: iso(-20 + Math.floor(rnd() * 330)).slice(0, 10),
        linked: i % 5 === 0, share_history: i % 10 === 0, last_visit: null, visits: 0, pending: 0, created_at: iso(-Math.floor(30 + rnd() * 700)) };
    });
    const wos = [], history = {};
    rows.forEach((r, i) => {
      if (i % 3 === 2) return;
      const s = schedById(r.schedule_id), km = Math.max(5000, r.km - 9000 - Math.floor(rnd() * 6000)), gp = E.gridAfter(s, km - s.interval.km / 2), sv = gp.svc;
      const items = sv.items.filter(x => x.action === "replace").map(x => x.item);
      const lines = [...items.map(k => ({ type: "part", desc: itemName(k), qty: 1, price: 40 + Math.floor(rnd() * 160) })), { type: "labor", desc: "עבודה, טיפול תקופתי", qty: 1, price: 250 + Math.floor(rnd() * 150) }];
      const date = iso(-(60 + Math.floor(rnd() * 420))).slice(0, 10);
      wos.push({ id: "dwo-" + i, garage_car_id: r.car_id, kind: "service", svc_km: gp.km, km, date, items, lines, total: lines.reduce((a, l) => a + l.price, 0), notes: null, entry_id: r.linked ? "x" : null });
      r.last_visit = date; r.visits = 1; r.lapsed = false;
    });
    for (const r of rows.filter(x => x.share_history)) {
      const s = schedById(r.schedule_id);
      history[r.car_id] = [{ date: iso(-500).slice(0, 7), km: Math.max(1000, r.km - 25000), kind: "service", svc_km: s.services[0].km, items: s.services[0].items.filter(x => x.action === "replace").map(x => x.item), garage: "מוסך אחר", verified: true, own: false },
        { date: iso(-300).slice(0, 7), km: Math.max(1000, r.km - 14000), kind: "repair", items: ["battery_12v"], text: "החלפת מצבר", garage: null, verified: false, own: false }];
    }
    const recalls = {}; for (const i of [2, 9, 17]) recalls[rows[i].plate] = [{ system: ["כריות אוויר", "מערכת בלימה", "חשמל ומיזוג"][i % 3] }];
    // calendar: today and the next two days, statuses that match the time of day
    const appts = [], approvals = [], kinds = ["service", "service", "service", "repair", "test"];
    for (let d = 0; d < 3; d++) {
      const day = new Date(); day.setHours(0, 0, 0, 0); day.setDate(day.getDate() + d);
      if (day.getDay() === 6) continue;
      const close = day.getDay() === 5 ? 13 : 17;
      // outside opening hours the demo shows today as a working morning, so every status is visible
      const hr = new Date().getHours(), clock = d === 0 && (hr < 8 || hr >= close) ? new Date(day).setHours(10, 45) : Date.now();
      for (let k = 0, h = 8; h < close - 1 && k < 9; k++) {
        const r = rows[(d * 9 + k * 4) % rows.length], start = new Date(day); start.setHours(h, rnd() < .5 ? 0 : 30);
        const minutes = [60, 60, 90, 120][Math.floor(rnd() * 4)], bay = 1 + (k % 3);
        const past = start.getTime() + minutes * 60000 < clock, now = start.getTime() < clock && !past;
        const status = past ? (rnd() < .85 ? "done" : "no_show") : now ? ["in_progress", "waiting_approval", "arrived"][k % 3] : (d === 0 && k === 1 ? "ready" : "booked");
        appts.push({ id: `dap-${d}-${k}`, garage_id: "demo", garage_car_id: r.car_id, customer_name: r.name, phone: r.phone, plate: r.plate, kind: kinds[k % kinds.length], note: k % 4 === 3 ? "רעש מהבלמים בנסיעה" : null, starts_at: start.toISOString(), minutes, bay, status, source: k % 3 === 2 ? "online" : "garage", work_order_id: null });
        if (k % 3 === 2) h += 1; else if (k % 3 === 0) h += 0; else h += 1;
      }
    }
    const lastDone = appts.filter(a => a.id.startsWith("dap-0-") && a.status === "done").pop(); if (lastDone) lastDone.status = "ready";
    const wa = appts.find(a => a.status === "waiting_approval");
    if (wa) approvals.push({ id: "daw-1", appointment_id: wa.id, message: "רפידות הבלם הקדמיות שחוקות", lines: [{ desc: "רפידות בלם קדמיות", price: 380 }, { desc: "עבודה", price: 150 }], total: 530, status: "pending", created_at: new Date().toISOString() });
    // a past vehicle inspection, answered by the customer
    approvals.push({ id: "dins-1", garage_id: "demo", garage_car_id: rows[1].car_id, appointment_id: null, message: "תוצאות בדיקת הרכב", km: rows[1].km - 2000, created_at: iso(-20), decided_at: iso(-20), status: "approved", approved_lines: [0],
      lines: [{ desc: "רפידות בלם קדמיות", price: 460, check: "brakes_front", urgent: true }, { desc: "החלפת מגבים", price: 110, check: "wipers" }], total: 570,
      checks: [{ key: "brakes_front", label: "בלמים קדמיים", status: "now", note: "נשארו 2 מ\"מ" }, { key: "wipers", label: "מגבים ונוזל שמשות", status: "soon", note: "משאירים פסים" }, { key: "tires", label: "צמיגים", status: "ok" }, { key: "lights", label: "אורות", status: "ok" }, { key: "battery", label: "מצבר", status: "ok", note: "12.6V" }] });
    // inventory: common service parts, two suppliers, one order on the way and one received; some invoices
    const sups = [{ id: "dsp-1", name: "חלפים מרכז", contact: "אבי", phone: "03-5550101", email: null, notes: "אספקה למחרת" }, { id: "dsp-2", name: "שמנים ישיר", contact: "רינה", phone: "054-5550202", email: null, notes: null }];
    const P = (id, sku, name, item_key, stock, min, cost, price, sup, extra = {}) => ({ id, garage_id: "demo", sku, name, item_key, stock, min_stock: min, cost, price, supplier_id: sup, unit: "unit", active: true, brand: null, fits: null, location: null, ...extra });
    const parts = [
      P("dpt-1", "OIL-5W30-208", "שמן מנוע 5W-30 (חבית)", "engine_oil", 46, 40, 28, 52, "dsp-2", { unit: "liter", location: "חבית 1" }),
      P("dpt-2", "OIL-0W20-208", "שמן מנוע 0W-20 (חבית)", "engine_oil", 18, 30, 34, 62, "dsp-2", { unit: "liter", fits: "טויוטה, קיה נירו, יונדאי", location: "חבית 2" }),
      P("dpt-3", "W712/95", "מסנן שמן MANN W712/95", "oil_filter", 9, 6, 24, 60, "dsp-1", { fits: "סקודה, מאזדה", location: "מדף 1" }),
      P("dpt-4", "90915-YZZE1", "מסנן שמן טויוטה", "oil_filter", 3, 6, 22, 55, "dsp-1", { fits: "טויוטה קורולה, יאריס, RAV4", location: "מדף 1" }),
      P("dpt-5", "26300-35505", "מסנן שמן יונדאי/קיה", "oil_filter", 12, 6, 18, 50, "dsp-1", { fits: "יונדאי, קיה", location: "מדף 1" }),
      P("dpt-6", "CU-2939", "מסנן מזגן", "cabin_filter", 4, 5, 30, 90, "dsp-1", { location: "מדף 2" }),
      P("dpt-7", "C-27009", "מסנן אוויר", "air_filter", 7, 4, 35, 95, "dsp-1", { location: "מדף 2" }),
      P("dpt-8", "DOT4-1L", "נוזל בלמים DOT4", "brake_fluid", 2, 3, 25, 70, "dsp-2", { unit: "liter" }),
      P("dpt-9", "NGK-ILKAR7", "מצת NGK", "spark_plugs", 16, 8, 32, 75, "dsp-1"),
      P("dpt-10", "BAT-60", "מצבר 60 אמפר", "battery_12v", 2, 2, 290, 520, "dsp-1"),
      P("dpt-11", "BP-F-COR", "רפידות בלם קדמיות קורולה", "brake_pads", 2, 2, 140, 320, "dsp-1", { fits: "טויוטה קורולה" }),
    ];
    const pos = [
      { id: "dpo-2", garage_id: "demo", number: 2, supplier_id: "dsp-1", status: "sent", note: null, sent_at: iso(-1), created_at: iso(-1), lines: [{ part_id: "dpt-4", sku: "90915-YZZE1", name: "מסנן שמן טויוטה", qty: 10, cost: 22 }, { part_id: "dpt-6", sku: "CU-2939", name: "מסנן מזגן", qty: 6, cost: 30 }], total: 400 },
      { id: "dpo-1", garage_id: "demo", number: 1, supplier_id: "dsp-2", status: "received", note: null, sent_at: iso(-12), received_at: iso(-10), created_at: iso(-12), lines: [{ part_id: "dpt-1", sku: "OIL-5W30-208", name: "שמן מנוע 5W-30 (חבית)", qty: 60, cost: 28, received: 60 }], total: 1680 },
    ];
    const pays = ["card", "card", "cash", "transfer", "app"];
    const invoices = wos.filter(w => Date.parse(w.date) > Date.now() - 400 * 86400000).slice(0, 9).map((w, i) => ({ id: "div-" + i, garage_id: "demo", work_order_id: w.id, kind: "invoice_receipt", provider: i % 4 === 3 ? "manual" : "morning", number: String(i % 4 === 3 ? 5400 + i : 20000 + i), url: null, customer_name: rows.find(r => r.car_id === w.garage_car_id).name, total: w.total, payment: pays[i % 5], issued_at: w.date + "T12:00:00Z" }));
    // a few recent visits without an invoice yet, so the billing tab has something to do
    rows.slice(0, 3).forEach((r, i) => { const s = schedById(r.schedule_id), gp = E.gridAfter(s, r.km - s.interval.km / 2), sv = gp.svc, items = sv.items.filter(x => x.action === "replace").map(x => x.item); const lines = [...items.map(k => ({ type: "part", desc: itemName(k), qty: 1, price: 60 + i * 15 })), { type: "labor", desc: "עבודה, טיפול תקופתי", qty: 1, price: 320 }]; wos.unshift({ id: "dwo-r" + i, garage_car_id: r.car_id, kind: "service", svc_km: gp.km, km: r.km, date: iso(-(i * 3 + 1)).slice(0, 10), items, lines, total: lines.reduce((a, l) => a + l.price, 0), notes: null, entry_id: null }); });
    // this month's invoices
    wos.filter(w => w.id.startsWith("dwo-")).slice(3, 7).forEach((w, i) => invoices.unshift({ id: "divm-" + i, garage_id: "demo", work_order_id: null, kind: "invoice_receipt", provider: "morning", number: String(20100 + i), url: null, customer_name: rows[(i * 5 + 4) % rows.length].name, total: 480 + i * 130, payment: pays[i], issued_at: new Date(Date.now() - i * 5 * 3600000).toISOString() }));
    return { garage: { id: "demo", name: "מוסך הדגמה", city: "חולון", address: "הפלד 40", bays: 3, slot_minutes: 60, booking_enabled: true, hours: {}, labor_rate: 280 }, rows, wos, history, recalls, appts, approvals, parts, sups, pos, invoices, billing: { api_id: "demo", has_secret: true, sandbox: false, vat_exempt: false } };
  })();


  Object.assign(G, { addAction, renderActions, addTimeline, timelineFor, D, Cloud, E, L, $, $$, fmt, esc, fmtDate, monthName, fmtPlate, digits, schedById, itemName, today, toast, telHref, waHref, theModel, ico, demo, api, st, monthsSince, view, recallsOf, isDue, isOver, isTest, FILTERS, match, message, openMsg, copy, showTab, setSeg, openMsgText, loadQr, download, numIn, nf, money, qtyOf, oilLiters, register, on, call, loadRecalls, reload, openGarage, DEMO });
  G.boot = () => start().catch(e => showGate("משהו השתבש", e.message || String(e), `<a class="btn" href="./">נסה שוב</a>`));
})();
