// Scheduled service: what the coming services need, from each car's importer schedule.
(function (G) {
  const { $, $$, download, esc, fmt, itemName, nf, oilLiters, qtyOf, showTab, st, toast, today, on } = G;
  // other modules, looked up when called
  const createDrafts = (...a) => G.createDrafts(...a);
  const itemQty = (...a) => G.itemQty(...a);
  const partById = (...a) => on("stock") ? G.partById(...a) : null;   // nothing from stock when the module is off
  const partFor = (...a) => on("stock") ? G.partFor(...a) : null;   // nothing from stock when the module is off
  const setStockSeg = (...a) => G.setStockSeg(...a);
  const shortOf = (...a) => G.shortOf(...a);
  // ---------- what to order: parts for the services coming up ----------
  const engineLabel = s => `${s.make_he} ${s.model_he}${s.engines && s.engines[0] ? " " + (s.engines[0].name || s.engines[0].code || s.engines[0]) : ""}`;
  // per maintenance item, and per stock part when the garage linked one (need = what the coming services take)
  function forecast(days) {
    const until = Date.now() + days * 86400000, due = st.rows.filter(c => c.n && (c.n.level === "crit" || c.n.dueDate.getTime() <= until));
    const by = new Map();
    for (const c of due) for (const it of c.n.plan.replace.map(item => ({ item }))) {
      const e = by.get(it.item) || { item: it.item, n: 0, models: new Map(), liters: 0, litersKnown: 0, parts: new Map(), unmatched: 0 };
      e.n++; const lbl = engineLabel(c.s); e.models.set(lbl, (e.models.get(lbl) || 0) + 1);
      if (it.item === "engine_oil") { const l = oilLiters(c.s); if (l) { e.liters += l; e.litersKnown++; } }
      const p = partFor(it.item, c); if (p) e.parts.set(p.id, (e.parts.get(p.id) || 0) + itemQty(it.item, p, c)); else e.unmatched++;
      by.set(it.item, e);
    }
    const items = [...by.values()].sort((a, b) => b.n - a.n);
    for (const e of items) { const ps = [...e.parts].map(([id, need]) => ({ p: partById(id), need })); e.stock = ps.reduce((a, x) => a + (+x.p.stock || 0), 0); e.short = ps.reduce((a, x) => a + shortOf(x.p, x.need), 0); e.covered = ps.every(x => (+x.p.stock || 0) >= x.need + (+x.p.min_stock || 0)); e.unit = ps.length && ps.every(x => x.p.unit === "liter") ? "liter" : "unit"; e.linked = ps.length > 0; }
    return { due, items };
  }
  function renderForecast() {
    const f = forecast(st.fcDays);
    $("#fc-sub").textContent = f.due.length ? `${f.due.length} רכבים מגיעים לטיפול ב-${st.fcDays} הימים הקרובים או כבר באיחור.` : "";
    $("#fc-rows").innerHTML = f.items.map(e => `<tr><td><b>${esc(itemName(e.item))}</b>${e.item === "engine_oil" && e.litersKnown ? `<div class="sub">כ-${fmt(e.liters)} ליטר ל-${e.litersKnown} מתוך ${e.n} רכבים</div>` : ""}</td><td class="num-col num"><b>${e.n}</b></td>
      <td class="num-col num">${e.linked ? qtyOf(e.stock, e.unit) : `<span class="sub">אין במלאי</span>`}${e.linked && e.unmatched ? `<div class="sub">${e.unmatched} רכבים בלי חלק מתאים</div>` : ""}</td>
      <td class="num-col num">${e.linked ? (e.short ? `<b class="warn-text">${qtyOf(e.short, e.unit)}</b>` : e.covered ? `<span class="tag ok">יש</span>` : `<span class="tag">הוזמן</span>`) : ""}</td><td><div class="tags">${[...e.models].sort((a, b) => b[1] - a[1]).map(([m, n]) => `<span class="tag"><bdi>${esc(m)}</bdi> ×${n}</span>`).join("")}</div></td></tr>`).join("");
    $("#fc-empty").hidden = !!f.items.length; $("#fc-empty").innerHTML = `<p class="muted">אין טיפולים צפויים בתקופה הזו.</p>`;
    $$("#fc-window .chip").forEach(b => b.classList.toggle("on", +b.dataset.d === st.fcDays));
  }
  $$("#fc-window .chip").forEach(b => b.onclick = () => { st.fcDays = +b.dataset.d; renderForecast(); });
  $("#fc-po").onclick = async () => {
    const f = forecast(st.fcDays), lines = [];
    for (const e of f.items) for (const [id, need] of e.parts) { const p = partById(id), q = shortOf(p, need); if (q > 0) lines.push({ part_id: p.id, sku: p.sku || null, name: p.name, qty: q, cost: p.cost ?? null }); }
    const unlinked = f.items.filter(e => !e.linked).length;
    if (!lines.length) return toast(unlinked ? `אין מה להזמין לפי המלאי. ${unlinked} פריטים לא מקושרים לחלק במלאי.` : "יש במלאי את כל מה שצריך");
    try { const n = await createDrafts(lines, `לטיפולים ב-${st.fcDays} הימים הקרובים`); showTab("stock"); setStockSeg("pos"); toast(`${n} טיוטות הזמנה נוצרו${unlinked ? `. ${unlinked} פריטים לא מקושרים למלאי` : ""}`); }
    catch (e) { toast("יצירת ההזמנה נכשלה: " + (e.message || e)); }
  };
  $("#fc-csv").onclick = () => { const f = forecast(st.fcDays), q = v => `"${String(v ?? "").replace(/"/g, '""')}"`; download(`הזמנה-${st.fcDays}-יום-${today()}.csv`, [["פריט", "רכבים", "במלאי", "להזמין", "פירוט"].map(q).join(","), ...f.items.map(e => [itemName(e.item), e.n, e.linked ? nf(e.stock) : "", e.linked ? nf(e.short) : "", [...e.models].map(([m, n]) => `${m} ×${n}`).join(" / ")].map(q).join(","))]); toast("רשימת ההזמנה יוצאה"); };

  G.register({ id: "service", name: "טיפולים לפי ספר היבואן", desc: "מה להזמין לטיפולים הקרובים, לפי לוח היבואן של כל רכב.", groups: ["mech"], tab: "order", show: renderForecast, state: { fcDays: 30 } });
  Object.assign(G, { renderForecast });
})(window.Garage);
