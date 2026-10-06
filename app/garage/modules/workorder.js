// Work order: what was done, parts and labour lines, sent to the driver for approval.
(function (G) {
  const { $, $$, D, E, api, demo, digits, esc, fmt, itemName, qtyOf, setSeg, st, toast, today, view, on, why } = G;
  // other modules, looked up when called
  const itemQty = (...a) => G.itemQty(...a);
  const moveStock = (...a) => G.moveStock(...a);
  const openInvoice = (...a) => G.openInvoice(...a);
  const partById = (...a) => on("stock") ? G.partById(...a) : null;   // nothing from stock when the module is off
  const partFor = (...a) => on("stock") ? G.partFor(...a) : null;   // nothing from stock when the module is off
  const partLabel = (...a) => G.partLabel(...a);
  const refreshParts = (...a) => G.refreshParts(...a);
  const renderRows = (...a) => G.renderRows(...a);
  // ---------- work order ----------
  let woFor = null, woKind = "service", woWhere = "independent", woLines = [], woItems = new Set();
  function svcOptions(c) {
    if (!c.s || c.estKm === null) return [];
    const s = c.s, sh = E.gridShift(s), laps = Math.floor(Math.max(0, c.estKm - sh) / s.cycle_km), out = [];
    for (let lap = Math.max(0, laps - 1); lap <= laps + 1; lap++) for (const sv of s.services) out.push(lap * s.cycle_km + sv.km);
    return [...new Set(out)].filter(k => Math.abs(k - c.estKm) <= 30000).sort((a, b) => a - b);
  }
  const svcAt = (s, km) => { const sh = E.gridShift(s), rel = ((km - sh) % s.cycle_km) + sh; return s.services.find(x => x.km === rel) || s.services.find(x => x.km === km); };
  function fillFromService() {
    const km = +$("#wo-svc").value, c = woFor;
    woItems = new Set(); woLines = woLines.filter(l => l.type === "labor" || l.manual);
    if (woKind === "service" && c.s && km) { const sv = svcAt(c.s, km); if (sv) for (const k of E.planAt(c.s, G.recordsOf(c.car_id), sv, km).replace.reverse()) { woItems.add(k); woLines.unshift(partLine(k)); } }
    if (!woLines.some(l => l.type === "labor")) woLines.push({ type: "labor", desc: woKind === "service" ? "עבודה, טיפול תקופתי" : "עבודה", qty: 1, price: "" });
    renderWoItems(); renderWoLines();
  }
  function renderWoItems() {
    const pool = new Set([...woItems, ...(woFor.s ? woFor.s.services.flatMap(sv => sv.items.filter(i => i.action === "replace").map(i => i.item)) : []), "battery_12v", "brake_pads", "brake_discs", "wipers"].filter(k => D.items[k]));
    $("#wo-items").innerHTML = [...pool].map(k => `<button type="button" class="chip ${woItems.has(k) ? "on" : ""}" data-it="${k}">${esc(itemName(k))}</button>`).join("");
    $$("#wo-items .chip").forEach(b => b.onclick = () => { const k = b.dataset.it; if (woItems.has(k)) { woItems.delete(k); woLines = woLines.filter(l => l.item !== k); } else { woItems.add(k); woLines.splice(woLines.findIndex(l => l.type === "labor") >= 0 ? woLines.findIndex(l => l.type === "labor") : woLines.length, 0, partLine(k)); } renderWoItems(); renderWoLines(); });
  }
  // a service item becomes a line with the matching stock part (name, price, liters of oil) when there is one
  function partLine(item, qty) {
    const p = partFor(item, woFor);
    return { type: "part", desc: p ? p.name : itemName(item), qty: qty || itemQty(item, p, woFor), price: p && p.price != null ? p.price : "", item, part_id: p ? p.id : null };
  }
  // other modules (the job catalog) add lines: parts go before the labour lines
  function woAddLines(lines) {
    for (const l of lines) { if (l.type === "part") { woLines.splice(Math.max(0, woLines.findIndex(x => x.type === "labor")), 0, { ...l, manual: true }); if (l.item) woItems.add(l.item); } else woLines.push({ ...l, manual: true }); }
    renderWoItems(); renderWoLines();
  }
  const typeTag = l => l.type === "labor" ? `<span class="tag mine">עבודה</span>` : l.part_id && partById(l.part_id) ? `<span class="tag ok" title="במלאי: ${esc(qtyOf(partById(l.part_id).stock, partById(l.part_id).unit))}">מהמלאי</span>` : `<span class="tag">חלק</span>`;
  const lineTotal = l => (+l.qty || 0) * (+String(l.price).replace(/[^\d.]/g, "") || 0);
  function renderWoLines() {
    $("#wo-lines").innerHTML = woLines.map((l, i) => `<tr><td data-ty="${i}">${typeTag(l)}</td>
      <td><input data-i="${i}" data-k="desc" value="${esc(l.part_id && partById(l.part_id) ? partLabel(partById(l.part_id)) : l.desc)}" autocomplete="off" ${l.type === "part" ? `list="wo-parts"` : ""}></td>
      <td class="num-col"><input class="num qty" data-i="${i}" data-k="qty" value="${esc(l.qty)}" inputmode="decimal" autocomplete="off"></td>
      <td class="num-col"><input class="num price" data-i="${i}" data-k="price" value="${esc(l.price)}" inputmode="decimal" placeholder="₪" autocomplete="off"></td>
      <td class="num-col num" data-tot="${i}">${lineTotal(l) ? "₪" + fmt(lineTotal(l)) : ""}</td><td><button type="button" class="x" data-del="${i}" aria-label="מחק שורה">×</button></td></tr>`).join("");
    $$("#wo-lines input").forEach(x => x.oninput = () => {
      const l = woLines[x.dataset.i]; l[x.dataset.k] = x.value; l.manual = true;
      if (x.dataset.k === "desc" && l.type === "part") {
        const p = st.parts.find(q => q.active !== false && partLabel(q) === x.value);
        if (p) { l.part_id = p.id; l.desc = p.name; if (l.price === "" && p.price != null) { l.price = p.price; $(`#wo-lines input[data-i="${x.dataset.i}"][data-k="price"]`).value = p.price; } }
        else if (l.part_id && x.value !== partLabel(partById(l.part_id) || {}) ) l.part_id = null;
        $(`[data-ty="${x.dataset.i}"]`).innerHTML = typeTag(l);
      }
      $(`[data-tot="${x.dataset.i}"]`).textContent = lineTotal(l) ? "₪" + fmt(lineTotal(l)) : ""; woTotal();
    });
    $$("#wo-lines [data-del]").forEach(b => b.onclick = () => { const l = woLines.splice(+b.dataset.del, 1)[0]; if (l.item) woItems.delete(l.item); renderWoItems(); renderWoLines(); });
    woTotal();
  }
  const woTotal = () => { const t = woLines.reduce((a, l) => a + lineTotal(l), 0); $("#wo-total").textContent = "₪" + fmt(t); return Math.round(t); };
  function openWo(c) {
    if (!c) return; woFor = c; woLines = []; woItems = new Set();
    $("#wo-parts").innerHTML = st.parts.filter(p => p.active !== false).map(p => `<option value="${esc(partLabel(p))}">${esc(qtyOf(p.stock, p.unit))} במלאי</option>`).join("");
    $("#wo-who").textContent = `${c.name || "לקוח"} · ${c.model} ${c.year || ""}${c.plate ? " · " + c.plate : ""}`;
    const opts = svcOptions(c), near = opts.length ? opts.reduce((a, b) => Math.abs(b - c.estKm) < Math.abs(a - c.estKm) ? b : a, opts[0]) : null;
    $("#wo-svc").innerHTML = opts.map(k => `<option value="${k}" ${k === near ? "selected" : ""}>טיפול ${fmt(k)} ק"מ</option>`).join("") + `<option value="">טיפול אחר</option>`;
    $("#wo-km").value = c.estKm || ""; $("#wo-date").value = today(); $("#wo-notes").value = ""; $("#wo-err").hidden = true;
    try { woWhere = localStorage.getItem("tipulit-gx-where-" + st.garage.id) || "independent"; } catch (e) {}
    woKind = "service"; setSeg("wo-kind", woKind); setSeg("wo-where", woWhere); $("#wo-svc-row").hidden = false;
    $("#wo-send-row").hidden = !c.linked; $("#wo-send").checked = true;
    fillFromService();
    if ($("#dlg-cust").open) $("#dlg-cust").close();
    $("#dlg-wo").showModal();
  }
  $$("#wo-kind button").forEach(b => b.onclick = () => { woKind = b.dataset.v; setSeg("wo-kind", woKind); $("#wo-svc-row").hidden = woKind !== "service"; fillFromService(); });
  $$("#wo-where button").forEach(b => b.onclick = () => { woWhere = b.dataset.v; setSeg("wo-where", woWhere); });
  $("#wo-svc").onchange = fillFromService;
  $("#wo-add-part").onclick = () => { woLines.splice(Math.max(0, woLines.findIndex(l => l.type === "labor")), 0, { type: "part", desc: "", qty: 1, price: "", manual: true }); renderWoLines(); };
  $("#wo-add-labor").onclick = () => { woLines.push({ type: "labor", desc: "עבודה", qty: 1, price: "", manual: true }); renderWoLines(); };
  $("#wo-save").onclick = () => saveWo(false);
  $("#wo-save-inv").onclick = () => saveWo(true);
  async function saveWo(invoice) {
    const km = +digits($("#wo-km").value) || null, err = m => { $("#wo-err").textContent = m; $("#wo-err").hidden = false; };
    if (!km) return err('צריך ק"מ.');
    if (!woLines.some(l => l.desc.trim())) return err("צריך לפחות שורה אחת.");
    const row = { garage_id: st.garage.id, garage_car_id: woFor.car_id, kind: woKind, svc_km: woKind === "service" ? (+$("#wo-svc").value || null) : null, km, date: $("#wo-date").value || today(),
      items: [...woItems], lines: woLines.filter(l => String(l.desc).trim()).map(l => ({ type: l.type, desc: String(l.desc).trim(), qty: +l.qty || 1, price: +String(l.price).replace(/[^\d.]/g, "") || 0, ...(l.part_id ? { part_id: l.part_id } : {}) })), total: woTotal() || null, notes: $("#wo-notes").value.trim() || null };
    if (invoice && !row.total) return err("אין סכום לחשבונית.");
    const b = $("#wo-save"), b2 = $("#wo-save-inv"); b.disabled = b2.disabled = true;
    try {
      const saved = demo ? { ...row, id: "wo-" + Date.now(), created_at: new Date().toISOString() } : await api.saveWorkOrder(row);
      // parts taken from stock leave the inventory
      if (row.lines.some(l => l.part_id)) {
        if (demo) { for (const l of row.lines.filter(x => x.part_id)) { const p = partById(l.part_id); if (p) await moveStock(p, -l.qty, "use", null, { work_order_id: saved.id }); } }
        else { try { await api.woConsume(saved.id); await refreshParts(); } catch (e) { toast("כרטיס העבודה נשמר, אבל המלאי לא עודכן"); } }
      }
      let sent = false;
      if (woFor.linked && $("#wo-send").checked) { if (!demo) saved.entry_id = await api.sendWorkOrder(saved.id, woWhere); else saved.entry_id = "demo"; sent = true; woFor.pending = (woFor.pending || 0) + 1; }
      try { localStorage.setItem("tipulit-gx-where-" + st.garage.id, woWhere); } catch (e) {}
      // the car's known km and last service move forward
      const patch = { km, km_at: new Date().toISOString(), ...(woKind === "service" ? { last_service: row.date.slice(0, 7) } : {}) };
      if (!demo) await api.updateGarageCar(woFor.car_id, patch).catch(() => {});
      st.wos.unshift(saved);
      Object.assign(woFor, patch); Object.assign(woFor, view(woFor)); woFor.last_visit = row.date; woFor.visits = (woFor.visits || 0) + 1; woFor.lapsed = false;
      if (G.woAppt) { const ap = G.woAppt; G.woAppt = null; ap.work_order_id = saved.id; try { if (!demo) await api.saveAppointment({ id: ap.id, garage_id: ap.garage_id, work_order_id: saved.id }); } catch (e) {} }
      $("#dlg-wo").close(); toast(sent ? (demo ? "נשמר. בהדגמה: היה נשלח ללקוח לאישור" : "נשמר ונשלח ללקוח לאישור") : "כרטיס העבודה נשמר"); renderRows();
      if (invoice) openInvoice(saved);
    } catch (e) { err("השמירה נכשלה: " + why(e)); }
    b.disabled = b2.disabled = false;
  }

  G.register({ id: "workorder", core: true });
  // the AI module fills the card from a note: kind, service, km, notes and already-priced lines
  function woSet(r) {
    if (r.kind) { woKind = r.kind; setSeg("wo-kind", woKind); $("#wo-svc-row").hidden = woKind !== "service"; }
    if (r.svc_km && [...$("#wo-svc").options].some(o => +o.value === r.svc_km)) $("#wo-svc").value = String(r.svc_km);
    if (r.km) $("#wo-km").value = r.km;
    if (r.notes) $("#wo-notes").value = r.notes;
    woLines = r.lines.map(l => ({ ...l, manual: true })); woItems = new Set(r.lines.map(l => l.item).filter(Boolean));
    if (!woLines.some(l => l.type === "labor")) woLines.push({ type: "labor", desc: "עבודה", qty: 1, price: "" });
    renderWoItems(); renderWoLines();
  }
  Object.assign(G, { openWo, woSet, woAddLines, woPartLine: partLine, woCar: () => woFor });
})(window.Garage);
