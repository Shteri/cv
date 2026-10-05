// Job catalog: the garage's standard jobs (hours, labour price, the maintenance items they replace) and the
// hourly labour rate. A job becomes work-order lines or approval lines in one click; parts are priced from stock per car.
(function (G) {
  const { $, $$, D, api, demo, esc, itemName, money, nf, numIn, on, st, toast } = G;
  const partFor = (...a) => on("stock") ? G.partFor(...a) : null;
  const itemQty = (...a) => G.itemQty(...a);

  // Ready-made starting points, by the kind of work the garage is licensed for. Hours are typical, not a standard:
  // each garage edits them. parts: maintenance items from data/items.json.
  const SUGGESTED = [
    ["בלמים", "רפידות בלם קדמיות", 1, [["brake_pads", 1]], ["mech", "tire"]],
    ["בלמים", "רפידות ודיסקים קדמיים", 1.5, [["brake_pads", 1], ["brake_discs", 2]], ["mech", "tire"]],
    ["בלמים", "החלפת נוזל בלמים", 0.7, [["brake_fluid", 1]], ["mech"]],
    ["מנוע", "רצועת טיימינג", 4, [["timing_belt", 1]], ["mech"]],
    ["מנוע", "רצועת אביזרים", 0.7, [["drive_belt", 1]], ["mech"]],
    ["מנוע", "החלפת מצתים", 0.7, [["spark_plugs", 4]], ["mech"]],
    ["מנוע", "החלפת נוזל קירור", 0.8, [["coolant", 1]], ["mech"]],
    ["תיבת הילוכים", "החלפת מצמד", 5, [["clutch", 1]], ["mech"]],
    ["תיבת הילוכים", "שמן תיבה אוטומטית", 1, [["transmission_oil", 1]], ["mech", "spec"]],
    ["חשמל", "החלפת מצבר", 0.3, [["battery_12v", 1]], ["mech", "elec"]],
    ["חשמל", "אבחון תקלה במחשב", 0.5, [], ["mech", "elec"]],
    ["חשמל", "החלפת נורות", 0.3, [["lights", 1]], ["mech", "elec"]],
    ["מיזוג", "מילוי גז למזגן", 0.7, [["ac_refrigerant", 1]], ["elec", "mech"]],
    ["מיזוג", "החלפת מסנן מזגן", 0.3, [["cabin_filter", 1]], ["mech", "elec"]],
    ["מתלים והיגוי", "בולמים קדמיים", 2, [["suspension", 2]], ["mech", "tire"]],
    ["מתלים והיגוי", "כיוון פרונט", 0.7, [["wheel_alignment", 1]], ["tire", "mech"]],
    ["צמיגים", "החלפת 4 צמיגים", 1, [["tires", 4]], ["tire"]],
    ["צמיגים", "רוטציה וגיבוי", 0.5, [["tire_rotation", 1]], ["tire"]],
    ["כללי", "החלפת מגבים", 0.2, [["wipers", 1]], ["mech", "elec", "tire"]],
    ["בדיקות", "הכנה לטסט", 1, [], ["mech", "check"]],
    ["בדיקות", "בדיקה לפני קנייה", 1, [], ["mech", "check"]],
  ].map(([category, name, hours, parts, groups]) => ({ category, name, hours, parts: parts.filter(([k]) => D.items[k]).map(([item, qty]) => ({ item, qty })), groups }));
  const suggestedFor = () => SUGGESTED.filter(j => !st.groups.length || j.groups.some(g => st.groups.includes(g)));

  // what a job costs on a given car: labour, plus parts priced from stock when the module is on
  const rate = () => +st.garage.labor_rate || 0;
  function estimate(job, car) {
    const labor = job.price != null && job.price !== "" ? +job.price : Math.round((+job.hours || 0) * rate());
    let parts = 0, unknown = 0;
    for (const p of job.parts || []) { const part = partFor(p.item, car); if (part && part.price != null) parts += (+part.price) * (p.qty || itemQty(p.item, part, car)); else unknown++; }
    return { labor, parts, unknown, total: labor + parts };
  }
  // work-order lines for a job on the car the work order is for
  const jobLines = job => [...(job.parts || []).map(p => G.woPartLine(p.item, p.qty)), { type: "labor", desc: job.name, qty: 1, price: estimate(job).labor || "" }];

  // ---------- catalog tab ----------
  let cgCat = "";
  function renderCatalog() {
    $("#cg-rate").value = st.garage.labor_rate ? nf(st.garage.labor_rate) : "";
    const cats = [...new Set(st.jobs.map(j => j.category || "כללי"))].sort((a, b) => a.localeCompare(b, "he"));
    $("#cg-cats").innerHTML = [`<button class="chip ${cgCat ? "" : "on"}" data-cat="">הכל</button>`, ...cats.map(c => `<button class="chip ${cgCat === c ? "on" : ""}" data-cat="${esc(c)}">${esc(c)}</button>`)].join("");
    $$("#cg-cats .chip").forEach(b => b.onclick = () => { cgCat = b.dataset.cat; renderCatalog(); });
    const q = $("#cg-q").value.trim().toLowerCase();
    const list = st.jobs.filter(j => j.active !== false && (!cgCat || (j.category || "כללי") === cgCat) && (!q || [j.name, j.category, ...(j.parts || []).map(p => itemName(p.item))].join(" ").toLowerCase().includes(q)));
    $("#cg-rows").innerHTML = list.map(j => { const e = estimate(j); return `<tr><td><button class="name-link" data-job="${j.id}">${esc(j.name)}</button></td><td>${esc(j.category || "כללי")}</td><td class="num-col num">${nf(j.hours)}</td>
      <td><div class="sub">${esc((j.parts || []).map(p => itemName(p.item) + (p.qty > 1 ? " ×" + p.qty : "")).join(", "))}</div></td>
      <td class="num-col num">${e.labor ? money(e.labor) : `<span class="sub">חסר מחיר שעה</span>`}</td><td class="num-col num">${e.parts ? money(e.parts) : ""}${e.unknown ? `<div class="sub">${e.unknown} בלי מחיר</div>` : ""}</td><td class="num-col num"><b>${money(e.total)}</b></td></tr>`; }).join("");
    $("#cg-empty").hidden = !!list.length;
    $("#cg-empty").innerHTML = st.jobs.length ? `<p class="muted">אין עבודות בסינון הזה.</p>` : `<b>עוד אין עבודות במחירון</b><p class="muted">התחילו מרשימה מוכנה לפי סוג המוסך, ותקנו שעות ומחירים לפי הניסיון שלכם.</p><div class="dlg-actions"><button class="btn primary" id="cg-empty-sug">הוספה מרשימה מוכנה</button></div>`;
    const es = $("#cg-empty-sug"); if (es) es.onclick = openSuggest;
    $$("#cg-rows [data-job]").forEach(b => b.onclick = () => openJob(st.jobs.find(j => j.id === b.dataset.job)));
  }
  $("#cg-q").oninput = renderCatalog;
  $("#cg-rate").onchange = async () => {
    const v = numIn($("#cg-rate").value);
    try { if (!demo) await api.updateGarageSettings(st.garage.id, { labor_rate: v }); st.garage.labor_rate = v; renderCatalog(); toast("מחיר השעה נשמר"); }
    catch (e) { toast("השמירה נכשלה: " + (e.message || e)); }
  };

  // ---------- one job ----------
  const COMMON = ["engine_oil", "oil_filter", "air_filter", "cabin_filter", "fuel_filter", "spark_plugs", "drive_belt", "timing_belt", "coolant", "brake_fluid", "brake_pads", "brake_discs", "battery_12v", "wipers", "lights", "transmission_oil", "clutch", "suspension", "ac_refrigerant", "tires", "wheel_alignment"].filter(k => D.items[k]);
  let jbEdit = null, jbParts = [];
  function openJob(j) {
    jbEdit = j || null; const x = j || {};
    $("#jb-title").textContent = j ? j.name : "עבודה חדשה";
    $("#jb-name").value = x.name || ""; $("#jb-cat").value = x.category || ""; $("#jb-hours").value = x.hours != null ? nf(x.hours) : ""; $("#jb-price").value = x.price != null ? nf(x.price) : "";
    $("#jb-cats").innerHTML = [...new Set([...st.jobs.map(y => y.category), ...SUGGESTED.map(y => y.category)].filter(Boolean))].map(c => `<option value="${esc(c)}"></option>`).join("");
    jbParts = (x.parts || []).map(p => ({ ...p }));
    $("#jb-err").hidden = true; $("#jb-del").hidden = !j; delete $("#jb-del").dataset.armed; $("#jb-del").textContent = "מחק";
    renderJobParts(); $("#dlg-job").showModal(); $("#jb-name").focus();
  }
  function renderJobParts() {
    const keys = [...new Set([...COMMON, ...jbParts.map(p => p.item)])];
    $("#jb-items").innerHTML = keys.map(k => `<button type="button" class="chip ${jbParts.some(p => p.item === k) ? "on" : ""}" data-it="${k}">${esc(itemName(k))}</button>`).join("");
    $$("#jb-items .chip").forEach(b => b.onclick = () => { const k = b.dataset.it, i = jbParts.findIndex(p => p.item === k); if (i >= 0) jbParts.splice(i, 1); else jbParts.push({ item: k, qty: 1 }); renderJobParts(); });
    $("#jb-qty").innerHTML = jbParts.map((p, i) => `<label class="field"><span>${esc(itemName(p.item))}: כמות</span><input class="num" data-i="${i}" value="${esc(p.qty)}" inputmode="decimal" autocomplete="off"></label>`).join("");
    $$("#jb-qty input").forEach(x => x.oninput = () => { jbParts[x.dataset.i].qty = numIn(x.value) || 1; });
    $("#jb-qty").hidden = !jbParts.length;
  }
  $("#jb-save").onclick = async () => {
    const name = $("#jb-name").value.trim(); if (!name) { $("#jb-err").textContent = "צריך שם."; $("#jb-err").hidden = false; return; }
    const row = { name, category: $("#jb-cat").value.trim() || null, hours: numIn($("#jb-hours").value) || 0, price: numIn($("#jb-price").value), parts: jbParts };
    try {
      const saved = demo ? (jbEdit ? Object.assign(jbEdit, row) : { ...row, id: "djb-" + Date.now(), active: true }) : await api.saveJob(jbEdit ? { id: jbEdit.id, ...row } : { garage_id: st.garage.id, ...row });
      if (!jbEdit) st.jobs.push(saved); else Object.assign(jbEdit, saved);
      $("#dlg-job").close(); toast("נשמר"); renderCatalog();
    } catch (e) { $("#jb-err").textContent = "השמירה נכשלה: " + (e.message || e); $("#jb-err").hidden = false; }
  };
  $("#jb-del").onclick = async () => {
    const b = $("#jb-del"); if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = "בטוח? לחיצה נוספת"; return; }
    try { if (!demo) await api.deleteJob(jbEdit.id); st.jobs = st.jobs.filter(j => j !== jbEdit); $("#dlg-job").close(); renderCatalog(); }
    catch (e) { $("#jb-err").textContent = "המחיקה נכשלה: " + (e.message || e); $("#jb-err").hidden = false; }
  };
  $("#cg-new").onclick = () => openJob(null);

  // ---------- ready-made list ----------
  function openSuggest() {
    const have = new Set(st.jobs.map(j => j.name)), list = suggestedFor().filter(j => !have.has(j.name));
    $("#sg-list").innerHTML = list.map((j, i) => `<label class="check"><input type="checkbox" data-sg="${i}" checked><span><b>${esc(j.name)}</b> <span class="muted small">${esc(j.category)} · ${nf(j.hours)} שעות${j.parts.length ? " · " + esc(j.parts.map(p => itemName(p.item)).join(", ")) : ""}</span></span></label>`).join("") || `<p class="muted">כל העבודות מהרשימה כבר במחירון.</p>`;
    $("#sg-go").disabled = !list.length; $("#sg-go").onclick = async () => {
      const pick = $$("#sg-list [data-sg]").filter(x => x.checked).map(x => list[+x.dataset.sg]);
      try {
        for (const j of pick) { const row = { name: j.name, category: j.category, hours: j.hours, price: null, parts: j.parts }; st.jobs.push(demo ? { ...row, id: "djb-" + Math.random().toString(36).slice(2), active: true } : await api.saveJob({ garage_id: st.garage.id, ...row })); }
        $("#dlg-sug").close(); renderCatalog(); toast(`נוספו ${pick.length} עבודות. עדכנו שעות ומחירים לפי הניסיון שלכם.`);
      } catch (e) { toast("ההוספה נכשלה: " + (e.message || e)); }
    };
    $("#dlg-sug").showModal();
  }
  $("#cg-suggest").onclick = openSuggest;

  // ---------- pick a job (work order, approval) ----------
  let pkDone = null, pkCar = null;
  function openPick(car, done) {
    pkCar = car; pkDone = done; $("#pk-q").value = ""; renderPick(); $("#dlg-pick").showModal(); $("#pk-q").focus();
  }
  function renderPick() {
    const q = $("#pk-q").value.trim().toLowerCase(), list = st.jobs.filter(j => j.active !== false && (!q || [j.name, j.category].join(" ").toLowerCase().includes(q)));
    $("#pk-list").innerHTML = list.map(j => { const e = estimate(j, pkCar); return `<button type="button" class="approval pick" data-pk="${j.id}"><span><b>${esc(j.name)}</b> <span class="muted small">${esc(j.category || "")} · ${nf(j.hours)} שעות</span></span><b class="num">${money(e.total)}</b></button>`; }).join("")
      || `<p class="muted">${st.jobs.length ? "אין עבודה כזו במחירון." : "המחירון ריק. אפשר למלא אותו בלשונית מחירון."}</p>`;
    $$("#pk-list [data-pk]").forEach(b => b.onclick = () => { const j = st.jobs.find(x => x.id === b.dataset.pk); $("#dlg-pick").close(); pkDone(j); });
  }
  $("#pk-q").oninput = renderPick;
  $("#wo-add-job").onclick = () => { const car = G.woCar(); openPick(car, j => { G.woAddLines(jobLines(j)); toast(`נוסף: ${j.name}`); }); };
  $("#aw-add-job").onclick = () => openPick(null, j => G.awAddLines([{ desc: j.name, price: estimate(j).total || "" }]));

  G.register({ id: "catalog", name: "מחירון עבודות", desc: "עבודות קבועות עם שעות, מחיר שעה והחלקים שהן דורשות. עבודה נכנסת לכרטיס עבודה או להצעת מחיר בלחיצה.", groups: "all", tab: "catalog", show: renderCatalog,
    state: { jobs: [] },
    async load(id) { st.jobs = await api.jobTemplates(id); },
    demo(D) { st.jobs = D.jobs || suggestedFor().map((j, i) => ({ id: "djb-" + i, name: j.name, category: j.category, hours: j.hours, price: null, parts: j.parts, active: true })); } });
  Object.assign(G, { jobEstimate: estimate, jobsFor: item => st.jobs.filter(j => j.active !== false && (j.parts || []).some(p => p.item === item)) });
})(window.Garage);
