// Invoices: issued in the garage's own Morning account (edge function issue-document) or recorded by hand.
(function (G) {
  const { $, $$, api, demo, download, esc, fmt, fmtDate, money, setSeg, st, toast, why } = G;
  // other modules, looked up when called
  const car = (...a) => G.car(...a);
  // ---------- invoices ----------
  const DOC = { invoice_receipt: "חשבונית מס קבלה", tax_invoice: "חשבונית מס", receipt: "קבלה", other: "מסמך" };
  const PAY = { card: "אשראי", cash: "מזומן", transfer: "העברה", app: "ביט / פייבוקס", check: "צ'ק", other: "אחר", unpaid: "לא שולם" };
  const invOf = woId => st.invoices.find(x => x.work_order_id === woId);
  const woLabel = w => { const c = car(w.garage_car_id); return `${c ? (c.name || "לקוח") + " · " + c.model : "רכב"}${w.kind === "service" && w.svc_km ? " · טיפול " + fmt(w.svc_km) : w.kind === "repair" ? " · תיקון" : ""}`; };
  let ivFor = null, ivKind = "invoice_receipt", ivPay = "card";
  function openInvoice(w) {
    ivFor = w; const c = car(w.garage_car_id), b = st.billing, prev = invOf(w.id);
    $("#iv-who").textContent = `${woLabel(w)}${w.date ? " · " + fmtDate(w.date) : ""}`;
    $("#iv-total").textContent = money(w.total);
    ivKind = b && b.vat_exempt ? "receipt" : "invoice_receipt"; setSeg("iv-kind", ivKind);
    $$("#iv-kind button").forEach(x => x.hidden = !!(b && b.vat_exempt) && x.dataset.v !== "receipt");
    $("#iv-pay-row").hidden = false; $$("#iv-pay .chip").forEach(x => x.classList.toggle("on", x.dataset.v === ivPay));
    const connected = !!(b && b.has_secret);
    $("#iv-morning").hidden = !connected; $("#iv-email").value = "";
    $("#iv-morning-note").innerHTML = prev ? invLine(prev) : demo ? "בהדגמה לא מופק מסמך אמיתי." : b && b.sandbox ? "חשבון ניסיון של מורנינג: המסמך לא אמיתי." : "המסמך יוצא מחשבון המורנינג שלכם, עם המספור שלו.";
    $("#iv-issue").disabled = !!prev;
    $("#iv-manual-note").innerHTML = connected ? "מפיקים במערכת אחרת? רשמו כאן את מספר המסמך." : `אין חיבור למערכת חשבוניות. <button type="button" class="name-link" id="iv-connect">חיבור למורנינג</button>, או רשמו כאן מספר של מסמך שהפקתם במערכת אחרת.`;
    const cn = $("#iv-connect"); if (cn) cn.onclick = () => { $("#dlg-inv").close(); openBillingSettings(); };
    $("#iv-number").value = ""; $("#iv-record").disabled = !!prev; $("#iv-err").hidden = true;
    if (prev && !connected) $("#iv-manual-note").innerHTML = invLine(prev);
    if (!c) toast("הרכב של כרטיס העבודה לא נמצא");
    $("#dlg-inv").showModal();
  }
  const invLine = x => `כבר יש ${DOC[x.kind]} מספר <b class="num">${esc(x.number || "?")}</b>${x.url ? ` · <a href="${esc(x.url)}" target="_blank" rel="noopener">פתיחת המסמך</a>` : ""}`;
  $$("#iv-kind button").forEach(b => b.onclick = () => { ivKind = b.dataset.v; setSeg("iv-kind", ivKind); $("#iv-pay-row").hidden = ivKind === "tax_invoice"; });
  $$("#iv-pay .chip").forEach(b => b.onclick = () => { ivPay = b.dataset.v; $$("#iv-pay .chip").forEach(x => x.classList.toggle("on", x === b)); });
  const ivErr = m => { $("#iv-err").textContent = m; $("#iv-err").hidden = false; };
  function invoiceIssued(x) { st.invoices.unshift(x); $("#iv-morning-note").innerHTML = invLine(x); $("#iv-issue").disabled = $("#iv-record").disabled = true; renderBilling(); const cb = $(`#cc-timeline [data-inv="${x.work_order_id}"]`); if (cb) cb.outerHTML = `<span class="tag ok">${DOC[x.kind]} ${esc(x.number || "")}</span>`; }
  $("#iv-issue").onclick = async () => {
    const w = ivFor, c = car(w.garage_car_id), b = $("#iv-issue"); b.disabled = true; $("#iv-err").hidden = true;
    try {
      let x;
      if (demo) x = { id: "div-" + Date.now(), garage_id: "demo", work_order_id: w.id, kind: ivKind, provider: "morning", number: String(20000 + st.invoices.length + 1), url: null, customer_name: c && c.name, total: w.total, payment: ivKind === "tax_invoice" ? "unpaid" : ivPay, issued_at: new Date().toISOString() };
      else { const r = await api.issueDocument({ work_order_id: w.id, kind: ivKind, payment: ivPay, email: $("#iv-email").value.trim() || null, label: c ? `${c.model} ${c.year || ""}`.trim() : null }); x = r.invoice; if (r.warning) toast(r.warning); }
      invoiceIssued(x); toast(`הופקה ${DOC[x.kind]} ${x.number || ""}`);
    } catch (e) { b.disabled = false; ivErr(/no invoicing account/.test(e.message) ? "אין חיבור למורנינג." : /Failed to send|not found|FunctionsFetchError|FunctionsRelayError/i.test(e.message) ? "שירות החשבוניות לא זמין כרגע. נסו שוב בעוד רגע." : "ההפקה נכשלה: " + why(e)); }
  };
  $("#iv-record").onclick = async () => {
    const number = $("#iv-number").value.trim(); if (!number) return ivErr("צריך מספר מסמך.");
    const w = ivFor, c = car(w.garage_car_id);
    const row = { garage_id: st.garage.id, work_order_id: w.id, kind: ivKind, provider: "manual", number, customer_name: (c && c.name) || null, total: w.total, payment: ivKind === "tax_invoice" ? "unpaid" : ivPay };
    try { const x = demo ? { ...row, id: "div-" + Date.now(), issued_at: new Date().toISOString() } : await api.recordInvoice(row); invoiceIssued(x); toast("נרשם"); }
    catch (e) { ivErr("הרישום נכשל: " + why(e)); }
  };

  // ---------- billing tab ----------
  const ym = d => `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}`;
  function renderBilling() {
    if (!$("#bi-month").value) $("#bi-month").value = ym(new Date());
    const m = $("#bi-month").value, list = st.invoices.filter(x => (x.issued_at || "").slice(0, 7) === m || ym(new Date(x.issued_at)) === m);
    const since = Date.now() - 60 * 86400000, open = st.wos.filter(w => !invOf(w.id) && w.total > 0 && Date.parse(w.date || w.created_at) >= since);
    $("#bi-kpis").innerHTML = `<div class="kpi"><b class="num">${money(list.reduce((a, x) => a + (+x.total || 0), 0))}</b><span>הופק בחודש הזה</span></div><div class="kpi"><b class="num">${list.length}</b><span>מסמכים</span></div><div class="kpi ${open.length ? "due" : ""}"><b class="num">${open.length}</b><span>עבודות בלי חשבונית</span></div>`;
    $("#bi-open-box").hidden = !open.length;
    $("#bi-open").innerHTML = open.slice(0, 12).map(w => `<div class="approval"><span>${esc(woLabel(w))} · <span class="muted small num">${w.date ? fmtDate(w.date) : ""}</span></span><b class="num">${money(w.total)}</b><button type="button" class="btn small" data-inv="${w.id}">הפק חשבונית</button></div>`).join("") + (open.length > 12 ? `<p class="muted small">ועוד ${open.length - 12}</p>` : "");
    $$("#bi-open [data-inv]").forEach(b => b.onclick = () => openInvoice(st.wos.find(w => w.id === b.dataset.inv)));
    $("#bi-rows").innerHTML = list.map(x => `<tr><td class="num">${fmtDate(x.issued_at)}</td><td class="num">${esc(x.number || "")}</td><td>${DOC[x.kind]}${x.provider === "manual" ? ` <span class="tag">נרשם ידנית</span>` : ""}</td><td>${esc(x.customer_name || "")}</td><td class="num-col num">${money(x.total)}</td><td>${PAY[x.payment] || ""}</td>
      <td class="act-col"><div class="acts">${x.url ? `<a class="btn small" href="${esc(x.url)}" target="_blank" rel="noopener">פתח</a>` : ""}${x.provider === "manual" ? `<button type="button" class="btn small" data-unrec="${x.id}">מחק</button>` : ""}</div></td></tr>`).join("");
    $("#bi-empty").hidden = !!list.length; $("#bi-empty").innerHTML = `<p class="muted">אין מסמכים בחודש הזה.</p>`;
    $$("#bi-rows [data-unrec]").forEach(b => b.onclick = async () => { if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = "בטוח?"; return; } try { if (!demo) await api.deleteInvoice(b.dataset.unrec); st.invoices = st.invoices.filter(x => x.id !== b.dataset.unrec); renderBilling(); } catch (e) { toast("נכשל: " + why(e)); } });
    $("#bi-settings").textContent = st.billing && st.billing.has_secret ? "מחובר למורנינג" : "חיבור למורנינג";
  }
  $("#bi-month").onchange = renderBilling;
  $("#bi-csv").onclick = () => {
    const m = $("#bi-month").value, list = st.invoices.filter(x => ym(new Date(x.issued_at)) === m), q = v => `"${String(v ?? "").replace(/"/g, '""')}"`;
    download(`חשבוניות-${st.garage.name}-${m}.csv`, [["תאריך", "מספר", "מסמך", "לקוח", "סכום", "תשלום", "מקור"].map(q).join(","), ...list.map(x => [String(x.issued_at).slice(0, 10), x.number, DOC[x.kind], x.customer_name, x.total, PAY[x.payment] || "", x.provider === "manual" ? "ידני" : "מורנינג"].map(q).join(","))]);
    toast(`ייצאתי ${list.length} מסמכים`);
  };
  $("#bi-settings").onclick = () => openBillingSettings();
  function openBillingSettings() {
    const b = st.billing || {};
    $("#bl-id").value = b.api_id || ""; $("#bl-secret").value = ""; $("#bl-secret").placeholder = b.has_secret ? "שמור. השאירו ריק כדי לא לשנות" : "";
    $("#bl-exempt").checked = !!b.vat_exempt; $("#bl-sandbox").checked = !!b.sandbox; $("#bl-err").hidden = true;
    $("#bl-state").textContent = b.has_secret ? `מחובר${b.sandbox ? " (חשבון ניסיון)" : ""}.` : "לא מחובר.";
    $("#bl-del").hidden = !b.has_secret; $("#bl-test").hidden = !b.has_secret;
    $("#dlg-billing").showModal();
  }
  const blErr = m => { $("#bl-err").textContent = m; $("#bl-err").hidden = false; };
  $("#bl-save").onclick = async () => {
    const v = { api_id: $("#bl-id").value.trim(), secret: $("#bl-secret").value.trim(), sandbox: $("#bl-sandbox").checked, vat_exempt: $("#bl-exempt").checked };
    if (!v.api_id) return blErr("צריך מזהה.");
    if (!v.secret && !(st.billing && st.billing.has_secret)) return blErr("צריך מפתח סודי.");
    try {
      if (demo) st.billing = { api_id: v.api_id, has_secret: true, sandbox: v.sandbox, vat_exempt: v.vat_exempt };
      else { await api.billingSave(st.garage.id, v); st.billing = await api.billing(st.garage.id); }
      $("#bl-secret").value = ""; openBillingSettings(); toast("נשמר"); renderBilling();
    } catch (e) { blErr("השמירה נכשלה: " + why(e)); }
  };
  $("#bl-test").onclick = async () => {
    const b = $("#bl-test"); b.disabled = true; $("#bl-err").hidden = true;
    try { if (!demo) await api.issueDocument({ garage_id: st.garage.id, test: true }); $("#bl-state").textContent = "החיבור עובד."; }
    catch (e) { blErr(/auth/.test(e.message) ? "מורנינג דחה את המפתחות. בדקו את המזהה והמפתח הסודי." : "הבדיקה נכשלה: " + why(e)); }
    b.disabled = false;
  };
  $("#bl-del").onclick = async () => {
    const b = $("#bl-del"); if (!b.dataset.armed) { b.dataset.armed = "1"; b.textContent = "בטוח? לחיצה נוספת"; return; }
    delete b.dataset.armed; b.textContent = "נתק";
    try { if (!demo) await api.billingDelete(st.garage.id); st.billing = null; openBillingSettings(); renderBilling(); toast("החיבור נותק"); } catch (e) { blErr("נכשל: " + why(e)); }
  };

  G.register({ id: "billing", name: "חשבוניות", desc: "הפקת חשבונית מכרטיס העבודה דרך מורנינג, או רישום של מספר ממערכת אחרת. סיכום חודשי לרואה החשבון.", groups: "all", tab: "billing", show: renderBilling,
    state: { invoices: [], billing: null },
    async load(id) { const [invoices, billing] = await Promise.all([api.invoices(id), api.billing(id).catch(() => null)]); Object.assign(st, { invoices, billing }); },
    demo(D) { Object.assign(st, { invoices: D.invoices, billing: D.billing }); } });
  Object.assign(G, { DOC, invOf, openInvoice });
})(window.Garage);
