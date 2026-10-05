// Inventory: parts, counts, suppliers and purchase orders (the stock itself is a ledger on the server).
(function (G) {
  const { $, $$, D, api, copy, demo, esc, fmtDate, ico, itemName, money, nf, numIn, oilLiters, openMsgText, qtyOf, setSeg, st, telHref, toast, waHref } = G;
  // other modules, looked up when called
  const renderForecast = (...a) => G.renderForecast(...a);
  // ---------- inventory: parts, suppliers, purchase orders (stock is a ledger on the server) ----------
  const partLabel = p => p.name + (p.sku ? " · " + p.sku : "");
  const partById = id => st.parts.find(p => p.id === id);
  const supById = id => st.sups.find(x => x.id === id);
  const isLow = p => p.active !== false && (+p.min_stock || 0) > 0 && (+p.stock || 0) < (+p.min_stock || 0);
  const PO_ST = { draft: ["טיוטה", ""], sent: ["נשלחה", "warn"], received: ["התקבלה", "ok"], cancelled: ["בוטלה", "crit"] };
  const MOVE = { receive: "התקבל", use: "כרטיס עבודה", adjust: "עדכון ידני" };
  // the part a car's service item takes: same maintenance item, preferring parts whose "fits" names the car
  function partFor(item, c) {
    const list = st.parts.filter(p => p.active !== false && p.item_key === item); if (list.length < 2) return list[0] || null;
    const words = c && c.s ? [c.s.make_he, c.s.model_he, ...(c.s.engines || []).map(e => e && (e.code || e.name || e))].filter(Boolean).map(w => String(w).toLowerCase()) : [];
    const score = p => { const f = String(p.fits || "").toLowerCase(); return f ? words.filter(w => f.includes(w)).length : 0; };
    return list.slice().sort((a, b) => score(b) - score(a) || (+b.stock || 0) - (+a.stock || 0))[0];
  }
  const itemQty = (item, p, c) => item === "engine_oil" && p && p.unit === "liter" ? (oilLiters(c && c.s) || 4.5) : 1;
  // already ordered from a supplier and not yet received
  const onOrder = id => st.pos.filter(o => o.status === "sent").reduce((a, o) => a + (o.lines || []).filter(l => l.part_id === id).reduce((b, l) => b + (+l.qty || 0), 0), 0);
  const shortOf = (p, need) => Math.ceil(Math.max(0, need + (+p.min_stock || 0) - (+p.stock || 0) - onOrder(p.id)));
  async function refreshParts() { if (!demo) { try { st.parts = await api.parts(st.garage.id); } catch (e) {} } }

  let stSeg = "parts";
  const setStockSeg = v => { stSeg = v; renderStock(); };
  function renderStock() {
    const live = st.parts.filter(p => p.active !== false), low = live.filter(isLow), open = st.pos.filter(o => o.status === "draft" || o.status === "sent");
    $("#st-kpis").innerHTML = `<div class="kpi"><b class="num">${live.length}</b><span>חלקים במלאי</span></div><div class="kpi ${low.length ? "due" : ""}"><b class="num">${low.length}</b><span>מתחת למינימום</span></div><div class="kpi"><b class="num">${open.length}</b><span>הזמנות פתוחות</span></div><div class="kpi"><b class="num">${money(live.reduce((a, p) => a + Math.max(0, +p.stock || 0) * (+p.cost || 0), 0))}</b><span>ערך המלאי (מחיר קנייה)</span></div>`;
    setSeg("st-seg", stSeg);
    const q = $("#st-q").value.trim().toLowerCase();
    $("#st-new").textContent = stSeg === "sups" ? "ספק חדש" : stSeg === "pos" ? "הזמנה חדשה" : "חלק חדש";
    $("#st-low").hidden = stSeg === "sups";
    let head = "", rows = "", n = 0, emptyText = "";
    if (stSeg === "parts") {
      const list = live.filter(p => !q || [p.sku, p.name, p.fits, p.brand, p.item_key && itemName(p.item_key)].join(" ").toLowerCase().includes(q))
        .sort((a, b) => isLow(b) - isLow(a) || a.name.localeCompare(b.name, "he"));
      n = list.length;
      head = `<tr><th>מק"ט</th><th>חלק</th><th>פריט בטיפול</th><th class="num-col">במלאי</th><th class="num-col">מינימום</th><th class="num-col">קנייה</th><th class="num-col">ללקוח</th><th>ספק</th><th class="act-col"><span class="sr">פעולות</span></th></tr>`;
      rows = list.map(p => `<tr><td class="num" dir="ltr">${esc(p.sku || "")}</td><td><button class="name-link" data-part="${p.id}">${esc(p.name)}</button>${p.fits || p.location ? `<div class="sub">${esc([p.fits, p.location].filter(Boolean).join(" · "))}</div>` : ""}</td>
        <td>${p.item_key ? esc(itemName(p.item_key)) : `<span class="sub">לא מקושר</span>`}</td>
        <td class="num-col num"><b class="${isLow(p) ? "warn-text" : ""}">${qtyOf(p.stock, p.unit)}</b>${isLow(p) ? `<div class="sub"><span class="tag warn">חסר</span></div>` : ""}</td>
        <td class="num-col num">${+p.min_stock ? qtyOf(p.min_stock, p.unit) : ""}</td><td class="num-col num">${p.cost != null ? money(p.cost) : ""}</td><td class="num-col num">${p.price != null ? money(p.price) : ""}</td>
        <td>${esc((supById(p.supplier_id) || {}).name || "")}</td><td class="act-col"><button class="btn small" data-count="${p.id}">ספירה</button></td></tr>`).join("");
      emptyText = live.length ? "אין חלקים בחיפוש הזה." : "עדיין אין חלקים. הוסיפו את מה שיש במחסן וקשרו כל חלק לפריט בטיפול, כדי שהתחזית תדע מה להזמין.";
    } else if (stSeg === "pos") {
      const list = st.pos.filter(o => !q || [o.number, (supById(o.supplier_id) || {}).name, ...(o.lines || []).map(l => l.name + " " + (l.sku || ""))].join(" ").toLowerCase().includes(q));
      n = list.length;
      head = `<tr><th>מס'</th><th>ספק</th><th>תאריך</th><th>מה</th><th class="num-col">סכום</th><th>מצב</th></tr>`;
      rows = list.map(o => `<tr><td class="num"><button class="name-link" data-po="${o.id}">#${o.number || "?"}</button></td><td>${esc((supById(o.supplier_id) || {}).name || "בלי ספק")}</td><td class="num">${fmtDate(o.received_at || o.sent_at || o.created_at)}</td>
        <td><div class="sub">${esc((o.lines || []).slice(0, 3).map(l => `${l.name} ×${nf(l.qty)}`).join(", "))}${(o.lines || []).length > 3 ? ` ועוד ${o.lines.length - 3}` : ""}</div></td><td class="num-col num">${money(o.total)}</td><td><span class="tag ${PO_ST[o.status][1]}">${PO_ST[o.status][0]}</span></td></tr>`).join("");
      emptyText = "עדיין אין הזמנות. \"הזמן מה שחסר\" יוצר טיוטה לכל ספק לפי המינימום, ומלשונית \"מה להזמין\" אפשר להזמין לפי הטיפולים הקרובים.";
    } else {
      const list = st.sups.filter(x => !q || [x.name, x.contact, x.phone, x.email].join(" ").toLowerCase().includes(q));
      n = list.length;
      head = `<tr><th>ספק</th><th>איש קשר</th><th>טלפון</th><th>מייל</th><th class="num-col">חלקים</th><th class="act-col"><span class="sr">פעולות</span></th></tr>`;
      rows = list.map(x => `<tr><td><button class="name-link" data-sup="${x.id}">${esc(x.name)}</button>${x.notes ? `<div class="sub">${esc(x.notes)}</div>` : ""}</td><td>${esc(x.contact || "")}</td><td class="num" dir="ltr">${esc(x.phone || "")}</td><td dir="ltr">${esc(x.email || "")}</td>
        <td class="num-col num">${st.parts.filter(p => p.supplier_id === x.id && p.active !== false).length}</td><td class="act-col"><div class="acts">${x.phone ? `<a class="ib" href="${waHref(x.phone)}" target="_blank" rel="noopener" aria-label="וואטסאפ לספק">${ico.wa}</a><a class="ib" href="${telHref(x.phone)}" aria-label="חיוג לספק">${ico.phone}</a>` : ""}</div></td></tr>`).join("");
      emptyText = "עדיין אין ספקים.";
    }
    $("#st-head").innerHTML = head; $("#st-rows").innerHTML = rows;
    $("#st-empty").hidden = !!n; $("#st-empty").innerHTML = `<p class="muted">${emptyText}</p>`;
    $("#st-foot").textContent = stSeg === "parts" ? "המלאי יורד לבד כששומרים כרטיס עבודה עם חלק מהמלאי, ועולה כשמאשרים קבלה של הזמנה. ספירה מתקנת את הכמות ונרשמת בהיסטוריה של החלק." : stSeg === "pos" ? "שליחה לספק פותחת וואטסאפ עם רשימת ההזמנה. בקבלת הסחורה מסמנים מה הגיע בפועל, והמלאי והמחיר מתעדכנים." : "";
    $$("#st-rows [data-part]").forEach(b => b.onclick = () => openPart(partById(b.dataset.part)));
    $$("#st-rows [data-count]").forEach(b => b.onclick = () => openCount(partById(b.dataset.count)));
    $$("#st-rows [data-po]").forEach(b => b.onclick = () => openPo(st.pos.find(o => o.id === b.dataset.po)));
    $$("#st-rows [data-sup]").forEach(b => b.onclick = () => openSup(supById(b.dataset.sup)));
  }
  $$("#st-seg button").forEach(b => b.onclick = () => { stSeg = b.dataset.v; renderStock(); });
  $("#st-q").oninput = renderStock;
  $("#st-new").onclick = () => stSeg === "sups" ? openSup(null) : stSeg === "pos" ? openPo(null) : openPart(null);
  $("#st-low").onclick = async () => {
    const lines = st.parts.filter(isLow).map(p => ({ part_id: p.id, sku: p.sku || null, name: p.name, qty: Math.ceil(2 * p.min_stock - p.stock - onOrder(p.id)), cost: p.cost ?? null })).filter(l => l.qty > 0);
    if (!lines.length) return toast(st.parts.some(isLow) ? "מה שחסר כבר הוזמן" : "אין חלקים מתחת למינימום");
    const n = await createDrafts(lines, "השלמת מלאי"); stSeg = "pos"; renderStock(); toast(`${n} טיוטות הזמנה, עד פי 2 מהמינימום`);
  };

  // one draft per supplier; lines for a supplier that already has a draft are added to it
  async function createDrafts(lines, note) {
    const groups = new Map();
    for (const l of lines) { const p = partById(l.part_id), k = (p && p.supplier_id) || ""; if (!groups.has(k)) groups.set(k, []); groups.get(k).push(l); }
    let n = 0;
    for (const [sup, ls] of groups) {
      const prev = st.pos.find(o => o.status === "draft" && (o.supplier_id || "") === sup);
      const merged = prev ? [...prev.lines] : [];
      for (const l of ls) { const m = merged.find(x => x.part_id && x.part_id === l.part_id); if (m) m.qty = Math.max(+m.qty || 0, l.qty); else merged.push(l); }
      const row = { ...(prev ? { id: prev.id } : { garage_id: st.garage.id, status: "draft", note }), supplier_id: sup || null, lines: merged, total: poSum(merged) };
      await savePo(row); n++;
    }
    return n;
  }
  const poSum = lines => Math.round(lines.reduce((a, l) => a + (+l.qty || 0) * (+l.cost || 0), 0) * 100) / 100;
  async function savePo(row) {
    let saved;
    if (demo) { const prev = row.id && st.pos.find(o => o.id === row.id); saved = prev ? Object.assign(prev, row) : { ...row, id: "dpo-" + Date.now() + Math.random().toString(36).slice(2, 6), number: Math.max(0, ...st.pos.map(o => o.number || 0)) + 1, created_at: new Date().toISOString() }; }
    else saved = await api.savePurchaseOrder(row);
    const i = st.pos.findIndex(o => o.id === saved.id); if (i >= 0) st.pos[i] = saved; else st.pos.unshift(saved);
    return saved;
  }

  // ---------- part ----------
  let ptEdit = null, ptUnit = "unit";
  function openPart(p) {
    ptEdit = p || null; const x = p || {};
    $("#pt-title").textContent = p ? p.name : "חלק חדש";
    $("#pt-item").innerHTML = `<option value="">לא קשור לטיפול</option>` + Object.entries(D.items).sort((a, b) => a[1].he.localeCompare(b[1].he, "he")).map(([k, v]) => `<option value="${k}">${esc(v.he)}</option>`).join("");
    $("#pt-sup").innerHTML = `<option value="">בלי ספק</option>` + st.sups.map(s2 => `<option value="${s2.id}">${esc(s2.name)}</option>`).join("");
    $("#pt-sku").value = x.sku || ""; $("#pt-name").value = x.name || ""; $("#pt-item").value = x.item_key || ""; $("#pt-brand").value = x.brand || ""; $("#pt-fits").value = x.fits || "";
    $("#pt-sup").value = x.supplier_id || ""; $("#pt-cost").value = x.cost ?? ""; $("#pt-price").value = x.price ?? ""; $("#pt-loc").value = x.location || ""; $("#pt-min").value = x.min_stock ? nf(x.min_stock) : "";
    $("#pt-stock").value = ""; $("#pt-stock-row").hidden = !!p; ptUnit = x.unit || "unit"; setSeg("pt-unit", ptUnit);
    $("#pt-err").hidden = true; $("#pt-del").hidden = !p; delete $("#pt-del").dataset.armed; $("#pt-del").textContent = "מחק";
    $("#pt-moves-row").hidden = !p; $("#pt-moves").innerHTML = "";
    if (p) (demo ? Promise.resolve(st.moves.filter(m => m.part_id === p.id)) : api.partMoves(p.id)).then(ms => {
      $("#pt-moves").innerHTML = ms.slice(0, 12).map(m => `<div class="approval"><span>${MOVE[m.reason]}${m.note ? " · " + esc(m.note) : ""}${m.purchase_order_id ? ` · הזמנה #${(st.pos.find(o => o.id === m.purchase_order_id) || {}).number || ""}` : ""}</span><b class="num ${m.qty < 0 ? "warn-text" : ""}" dir="ltr">${m.qty > 0 ? "+" : ""}${nf(m.qty)}</b><span class="muted small">${fmtDate(m.created_at)}</span></div>`).join("") || `<p class="muted small">אין תנועות עדיין.</p>`;
    }).catch(() => { $("#pt-moves").innerHTML = ""; });
    $("#dlg-part").showModal(); $(p ? "#pt-name" : "#pt-sku").focus();
  }
  $$("#pt-unit button").forEach(b => b.onclick = () => { ptUnit = b.dataset.v; setSeg("pt-unit", ptUnit); });
  $("#pt-item").onchange = () => { if ($("#pt-item").value === "engine_oil" && !ptEdit) { ptUnit = "liter"; setSeg("pt-unit", ptUnit); } if (!$("#pt-name").value.trim() && $("#pt-item").value) $("#pt-name").value = itemName($("#pt-item").value); };
  $("#pt-save").onclick = async () => {
    const err = m => { $("#pt-err").textContent = m; $("#pt-err").hidden = false; };
    const name = $("#pt-name").value.trim(); if (!name) return err("צריך שם.");
    const sku = $("#pt-sku").value.trim();
    if (sku && st.parts.some(p => p.id !== (ptEdit && ptEdit.id) && (p.sku || "").toLowerCase() === sku.toLowerCase())) return err('המק"ט הזה כבר קיים במלאי.');
    const row = { sku: sku || null, name, item_key: $("#pt-item").value || null, brand: $("#pt-brand").value.trim() || null, fits: $("#pt-fits").value.trim() || null, unit: ptUnit,
      min_stock: numIn($("#pt-min").value) || 0, cost: numIn($("#pt-cost").value), price: numIn($("#pt-price").value), supplier_id: $("#pt-sup").value || null, location: $("#pt-loc").value.trim() || null };
    const opening = ptEdit ? 0 : numIn($("#pt-stock").value) || 0;
    const b = $("#pt-save"); b.disabled = true;
    try {
      let saved;
      if (demo) { saved = ptEdit ? Object.assign(ptEdit, row) : { ...row, id: "dpt-" + Date.now(), garage_id: "demo", stock: 0, active: true }; }
      else saved = await api.savePart(ptEdit ? { id: ptEdit.id, ...row } : { garage_id: st.garage.id, ...row });
      if (!ptEdit) st.parts.push(saved); else Object.assign(ptEdit, saved);
      if (opening) await moveStock(saved, opening, "adjust", "מלאי פתיחה");
      $("#dlg-part").close(); toast(ptEdit ? "החלק עודכן" : "החלק נוסף"); renderStock();
    } catch (e) { err(/duplicate|unique/i.test(e.message || "") ? 'המק"ט הזה כבר קיים במלאי.' : "השמירה נכשלה: " + (e.message || e)); }
    b.disabled = false;
  };
  $("#pt-del").onclick = async () => {
    const b = $("#pt-del"); if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = "בטוח? לחיצה נוספת"; return; }
    try { if (!demo) await api.deletePart(ptEdit.id); st.parts = st.parts.filter(p => p !== ptEdit); $("#dlg-part").close(); toast("החלק נמחק"); renderStock(); }
    catch (e) { $("#pt-err").textContent = "המחיקה נכשלה: " + (e.message || e); $("#pt-err").hidden = false; }
  };
  async function moveStock(p, qty, reason, note, extra = {}) {
    if (!qty) return;
    const row = { garage_id: st.garage.id, part_id: p.id, qty, reason, note: note || null, ...extra };
    if (demo) st.moves.unshift({ ...row, id: "dmv-" + Date.now(), created_at: new Date().toISOString() }); else await api.addStockMove(row);
    p.stock = Math.round(((+p.stock || 0) + qty) * 100) / 100;
  }

  // ---------- count ----------
  let ctFor = null;
  function openCount(p) { ctFor = p; $("#ct-name").textContent = p.name; $("#ct-now").textContent = `לפי המערכת: ${qtyOf(p.stock, p.unit)}`; $("#ct-qty").value = ""; $("#ct-note").value = "ספירה"; $("#ct-err").hidden = true; $("#dlg-count").showModal(); $("#ct-qty").focus(); }
  $("#ct-save").onclick = async () => {
    const actual = numIn($("#ct-qty").value); if (actual === null || actual < 0) { $("#ct-err").textContent = "צריך כמות."; $("#ct-err").hidden = false; return; }
    try { await moveStock(ctFor, Math.round((actual - (+ctFor.stock || 0)) * 100) / 100, "adjust", $("#ct-note").value.trim()); $("#dlg-count").close(); toast("המלאי עודכן"); renderStock(); }
    catch (e) { $("#ct-err").textContent = "העדכון נכשל: " + (e.message || e); $("#ct-err").hidden = false; }
  };

  // ---------- supplier ----------
  let spEdit = null;
  function openSup(x) {
    spEdit = x || null; const v = x || {};
    $("#sp-title").textContent = x ? x.name : "ספק חדש";
    for (const k of ["name", "contact", "phone", "email", "notes"]) $("#sp-" + k).value = v[k] || "";
    $("#sp-err").hidden = true; $("#sp-del").hidden = !x; delete $("#sp-del").dataset.armed; $("#sp-del").textContent = "מחק";
    $("#dlg-sup").showModal(); $("#sp-name").focus();
  }
  $("#sp-save").onclick = async () => {
    const row = Object.fromEntries(["name", "contact", "phone", "email", "notes"].map(k => [k, $("#sp-" + k).value.trim() || null]));
    if (!row.name) { $("#sp-err").textContent = "צריך שם."; $("#sp-err").hidden = false; return; }
    try {
      const saved = demo ? (spEdit ? Object.assign(spEdit, row) : { ...row, id: "dsp-" + Date.now() }) : await api.saveSupplier(spEdit ? { id: spEdit.id, ...row } : { garage_id: st.garage.id, ...row });
      if (!spEdit) st.sups.push(saved); else Object.assign(spEdit, saved);
      $("#dlg-sup").close(); toast("נשמר"); renderStock();
    } catch (e) { $("#sp-err").textContent = "השמירה נכשלה: " + (e.message || e); $("#sp-err").hidden = false; }
  };
  $("#sp-del").onclick = async () => {
    const b = $("#sp-del"); if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = "בטוח? לחיצה נוספת"; return; }
    try { if (!demo) await api.deleteSupplier(spEdit.id); st.sups = st.sups.filter(x => x !== spEdit); for (const p of st.parts) if (p.supplier_id === spEdit.id) p.supplier_id = null; $("#dlg-sup").close(); toast("הספק נמחק"); renderStock(); }
    catch (e) { $("#sp-err").textContent = "המחיקה נכשלה: " + (e.message || e); $("#sp-err").hidden = false; }
  };

  // ---------- purchase order ----------
  let poEdit = null, poLines = [], poRecv = false;
  function openPo(o) {
    poEdit = o || null; poRecv = false;
    poLines = o ? o.lines.map(l => ({ ...l, recv: l.received ?? l.qty })) : [{ part_id: null, name: "", sku: null, qty: 1, cost: null }];
    $("#po-sup").innerHTML = `<option value="">בלי ספק</option>` + st.sups.map(x => `<option value="${x.id}">${esc(x.name)}</option>`).join("");
    $("#po-sup").value = (o && o.supplier_id) || ""; $("#po-note").value = (o && o.note) || "";
    $("#po-parts").innerHTML = st.parts.filter(p => p.active !== false).map(p => `<option value="${esc(partLabel(p))}"></option>`).join("");
    $("#po-err").hidden = true; renderPo(); $("#dlg-po").showModal();
  }
  function renderPo() {
    const o = poEdit, status = o ? o.status : "draft", ro = status === "received" || status === "cancelled" || (status === "sent" && !poRecv);
    $("#po-title").textContent = o ? `הזמנת רכש #${o.number || ""}` : "הזמנת רכש חדשה";
    $("#po-status").textContent = PO_ST[status][0]; $("#po-status").className = "tag " + PO_ST[status][1];
    $("#po-sup").disabled = status !== "draft"; $("#po-note").disabled = status !== "draft";
    const showRecv = poRecv || status === "received"; $("#po-recv-h").hidden = !showRecv;
    $("#po-lines").innerHTML = poLines.map((l, i) => `<tr><td><input data-i="${i}" data-k="name" list="po-parts" value="${esc(l.part_id && partById(l.part_id) ? partLabel(partById(l.part_id)) : l.name)}" autocomplete="off" ${ro || poRecv ? "disabled" : ""} placeholder="מק&quot;ט או שם"></td>
      <td class="num-col"><input class="num qty" data-i="${i}" data-k="qty" value="${esc(l.qty)}" inputmode="decimal" autocomplete="off" ${ro || poRecv ? "disabled" : ""}></td>
      <td class="num-col" ${showRecv ? "" : "hidden"}><input class="num qty" data-i="${i}" data-k="recv" value="${esc(l.recv ?? "")}" inputmode="decimal" autocomplete="off" ${poRecv && l.part_id ? "" : "disabled"}></td>
      <td class="num-col"><input class="num price" data-i="${i}" data-k="cost" value="${esc(l.cost ?? "")}" inputmode="decimal" placeholder="₪" autocomplete="off" ${ro ? "disabled" : ""}></td>
      <td class="num-col num" data-pot="${i}">${(+l.qty || 0) * (+l.cost || 0) ? money((+l.qty || 0) * (+l.cost || 0)) : ""}</td><td>${ro || poRecv ? "" : `<button type="button" class="x" data-del="${i}" aria-label="מחק שורה">×</button>`}</td></tr>`).join("");
    $$("#po-lines input").forEach(x => x.oninput = () => {
      const l = poLines[x.dataset.i];
      if (x.dataset.k === "name") { const p = st.parts.find(q => partLabel(q) === x.value); if (p) { l.part_id = p.id; l.name = p.name; l.sku = p.sku || null; if (l.cost == null || l.cost === "") { l.cost = p.cost; renderPo(); return; } } else { l.part_id = null; l.name = x.value; l.sku = null; } }
      else l[x.dataset.k] = numIn(x.value);
      $(`[data-pot="${x.dataset.i}"]`).textContent = (+l.qty || 0) * (+l.cost || 0) ? money((+l.qty || 0) * (+l.cost || 0)) : ""; $("#po-total").textContent = money(poSum(poLines));
    });
    $$("#po-lines [data-del]").forEach(b => b.onclick = () => { poLines.splice(+b.dataset.del, 1); renderPo(); });
    $("#po-add").hidden = status !== "draft";
    $("#po-total").textContent = money(poSum(poLines));
    $("#po-hint").textContent = poRecv ? "סמנו כמה הגיע מכל חלק. אפשר לתקן גם את המחיר. שורות בלי חלק מהמלאי לא נכנסות למלאי." : status === "draft" ? "בחרו חלק מהמלאי (לפי מק\"ט או שם) כדי שבקבלה הוא ייכנס למלאי." : "";
    const A = [];
    if (status === "draft") A.push(o ? `<button class="btn" type="button" id="po-x">מחק טיוטה</button>` : "", `<button class="btn" type="button" id="po-save">שמור טיוטה</button>`, `<button class="btn primary" type="button" id="po-send">שלח לספק</button>`);
    else if (status === "sent" && !poRecv) A.push(`<button class="btn" type="button" id="po-cancel">בטל הזמנה</button>`, `<button class="btn" type="button" id="po-resend">שלח שוב</button>`, `<button class="btn primary" type="button" id="po-recv">קבלת סחורה</button>`);
    else if (poRecv) A.push(`<button class="btn" type="button" id="po-back">חזרה</button>`, `<button class="btn primary" type="button" id="po-confirm">אישור קבלה</button>`);
    A.push(`<button class="btn" value="close">סגור</button>`);
    $("#po-actions").innerHTML = A.join("");
    const on = (id, f) => { const b = $(id); if (b) b.onclick = f; };
    on("#po-save", () => poPersist("draft").then(() => toast("הטיוטה נשמרה")).catch(poErr));
    on("#po-send", () => poPersist("sent").then(sendPo).catch(poErr));
    on("#po-resend", () => sendPo(poEdit));
    on("#po-recv", () => { poRecv = true; renderPo(); });
    on("#po-back", () => { poRecv = false; renderPo(); });
    on("#po-cancel", () => poPersist("cancelled").then(() => toast("ההזמנה בוטלה")).catch(poErr));
    on("#po-x", async () => { try { if (!demo) await api.deletePurchaseOrder(poEdit.id); st.pos = st.pos.filter(x => x !== poEdit); $("#dlg-po").close(); renderStock(); toast("הטיוטה נמחקה"); } catch (e) { poErr(e); } });
    on("#po-confirm", receivePo);
  }
  const poErr = e => { $("#po-err").textContent = "נכשל: " + (e.message || e); $("#po-err").hidden = false; };
  async function poPersist(status) {
    const lines = poLines.filter(l => (l.name || "").trim() && +l.qty > 0).map(l => ({ part_id: l.part_id || null, sku: l.sku || null, name: l.name.trim(), qty: +l.qty, cost: l.cost == null || l.cost === "" ? null : +l.cost }));
    if (!lines.length) throw new Error("אין שורות");
    const row = { ...(poEdit ? { id: poEdit.id } : { garage_id: st.garage.id }), supplier_id: $("#po-sup").value || null, note: $("#po-note").value.trim() || null, lines, total: poSum(lines), status, ...(status === "sent" ? { sent_at: new Date().toISOString() } : {}) };
    poEdit = await savePo(row); poLines = poEdit.lines.map(l => ({ ...l, recv: l.qty })); renderPo(); renderStock();
    return poEdit;
  }
  function sendPo(o) {
    const sup = supById(o.supplier_id) || {};
    const text = `שלום${sup.contact ? " " + sup.contact.split(" ")[0] : ""}, הזמנה #${o.number || ""} מ${st.garage.name}:\n` + o.lines.map(l => `• ${l.name}${l.sku ? ` (${l.sku})` : ""} × ${nf(l.qty)}`).join("\n") + (o.note ? `\n${o.note}` : "") + "\nתודה!";
    if (sup.phone) openMsgText(sup.name, sup.phone, text); else copy(text, "אין טלפון לספק. ההזמנה הועתקה");
  }
  async function receivePo() {
    const lines = poLines.filter(l => l.part_id).map(l => ({ part_id: l.part_id, qty: +l.recv || 0, cost: l.cost == null || l.cost === "" ? null : +l.cost }));
    const b = $("#po-confirm"); b.disabled = true;
    try {
      if (demo) {
        for (const l of lines) { const p = partById(l.part_id); if (p && l.qty > 0) { await moveStock(p, l.qty, "receive", null, { purchase_order_id: poEdit.id }); if (l.cost != null) p.cost = l.cost; } }
        Object.assign(poEdit, { status: "received", received_at: new Date().toISOString(), lines: poEdit.lines.map(x => ({ ...x, received: (lines.find(l => l.part_id === x.part_id) || {}).qty || 0 })) });
      } else { const o = await api.receivePurchaseOrder(poEdit.id, lines); Object.assign(poEdit, o); await refreshParts(); }
      poRecv = false; poLines = poEdit.lines.map(l => ({ ...l, recv: l.received })); renderPo(); renderStock(); renderForecastIfOpen(); toast("הסחורה נכנסה למלאי");
    } catch (e) { poErr(e); }
    b.disabled = false;
  }
  const renderForecastIfOpen = () => { if (st.tab === "order") renderForecast(); };

  G.register({ id: "stock", name: "מלאי והזמנות רכש", desc: "חלקים עם מק\"ט ומינימום, ספקים, הזמנות רכש בוואטסאפ וקבלת סחורה. כרטיס עבודה מוריד מהמלאי.", groups: "all", tab: "stock", show: renderStock,
    state: { parts: [], sups: [], pos: [], moves: [] },
    async load(id) { const [parts, sups, pos] = await Promise.all([api.parts(id), api.suppliers(id), api.purchaseOrders(id)]); Object.assign(st, { parts, sups, pos }); },
    demo(D) { Object.assign(st, { parts: D.parts, sups: D.sups, pos: D.pos, moves: D.moves || [] }); } });
  Object.assign(G, { createDrafts, itemQty, partById, partFor, partLabel, moveStock, refreshParts, renderStock, shortOf, setStockSeg });
})(window.Garage);
