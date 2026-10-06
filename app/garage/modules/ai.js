// AI assist: describe the job or the inspection in a few words (or dictate them to the phone keyboard) and the
// card fills itself. The note and the garage's own context go to the ai-assist edge function; nothing is saved
// until the garage reviews and presses save. In the demo a simple keyword match stands in for the AI.
(function (G) {
  const { $, D, demo, on, st } = G;
  const ERR = { "ai not configured": "ה-AI עוד לא מחובר בשרת.", "daily limit": "הגעתם למכסה היומית. אפשר להמשיך ידנית.", "not signed in": "צריך להתחבר מחדש.", "not allowed": "רק למוסך מאומת.", refused: "ה-AI לא הצליח לעבד את הטקסט הזה.", busy: "ה-AI עמוס כרגע. נסו שוב בעוד רגע." };
  const errText = e => ERR[e.message] || "לא הצלחנו לעבד את התיאור. אפשר למלא ידנית.";

  // ---------- work order ----------
  function woContext(car) {
    return {
      car: car ? { model: car.model, year: car.year, km: car.estKm ? Math.round(car.estKm) : null } : null,
      items: Object.entries(D.items).map(([key, v]) => ({ key, he: v.he })),
      stock: on("stock") ? st.parts.filter(p => p.active !== false).slice(0, 300).map(p => ({ id: p.id, name: p.name, sku: p.sku || null, item: p.item_key || null, unit: p.unit })) : [],
      catalog: on("catalog") ? st.jobs.filter(j => j.active !== false).slice(0, 200).map(j => ({ id: j.id, name: j.name, hours: +j.hours || 0 })) : [],
      labor_rate: +st.garage.labor_rate || null,
    };
  }
  // stock prices for parts, the catalog or the hourly rate for labour
  function priceLines(lines, car) {
    const rate = +st.garage.labor_rate || 0;
    return lines.map(l => {
      if (l.type === "part") {
        const p = l.part_id && st.parts.find(x => x.id === l.part_id);
        return { type: "part", desc: p ? p.name : l.desc, qty: l.qty || 1, price: l.price ?? (p && p.price != null ? p.price : ""), item: l.item || (p && p.item_key) || null, part_id: p ? p.id : null };
      }
      const j = l.job_id && st.jobs && st.jobs.find(x => x.id === l.job_id);
      const price = l.price ?? (l.hours && rate ? Math.round(l.hours * rate) : j ? G.jobEstimate(j, car).labor : "");
      return { type: "labor", desc: j ? j.name : l.desc, qty: 1, price: price || "" };
    });
  }
  $("#wo-ai-go").onclick = async () => {
    const note = $("#wo-ai").value.trim(); if (!note) return $("#wo-ai").focus();
    const car = G.woCar(), ctx = woContext(car), b = $("#wo-ai-go"); b.disabled = true; $("#wo-ai-msg").textContent = "ממלא…";
    try {
      const r = demo ? demoWo(note, ctx, car) : await G.api.aiAssist("wo", note, ctx);
      G.woSet({ ...r, lines: priceLines(r.lines, car) });
      $("#wo-ai-msg").textContent = demo ? "הדגמה: זיהוי פשוט של מילים, בלי AI. בדקו לפני שמירה." : "מולא. בדקו לפני שמירה.";
    } catch (e) { $("#wo-ai-msg").textContent = errText(e); }
    b.disabled = false;
  };

  // ---------- inspection ----------
  $("#in-ai-go").onclick = async () => {
    const note = $("#in-ai").value.trim(); if (!note) return $("#in-ai").focus();
    const car = G.inspCar(), ctx = { car: car ? { model: car.model, year: car.year } : null, checklist: G.inspRows() }, b = $("#in-ai-go"); b.disabled = true; $("#in-ai-msg").textContent = "ממלא…";
    try {
      const r = demo ? demoInsp(note, ctx) : await G.api.aiAssist("insp", note, ctx);
      G.inspSet(r);
      $("#in-ai-msg").textContent = demo ? "הדגמה: זיהוי פשוט של מילים, בלי AI. בדקו לפני שליחה." : "מולא. בדקו לפני שליחה.";
    } catch (e) { $("#in-ai-msg").textContent = errText(e); }
    b.disabled = false;
  };

  // ---------- demo stand-in: words that appear in the note ----------
  const has = (note, name) => name.split(/\s+/).filter(w => w.length > 2).slice(0, 2).every(w => note.includes(w));
  function demoWo(note, ctx, car) {
    const lines = [];
    // items named in the note, each with the stock part that fits this car
    for (const it of ctx.items) if (has(note, it.he)) { const p = on("stock") ? G.partFor(it.key, car) : null; lines.push({ type: "part", desc: p ? p.name : it.he, qty: p && p.unit === "liter" ? 4.5 : 1, price: null, part_id: p ? p.id : null, item: it.key }); }
    const h = /שעתיים/.test(note) ? 2 : /שעה וחצי/.test(note) ? 1.5 : /(\d+(?:\.\d+)?)\s*שעות/.test(note) ? +RegExp.$1 : /שעה/.test(note) ? 1 : null;
    lines.push({ type: "labor", desc: "עבודה", qty: 1, price: null, hours: h, job_id: null });
    const svc = note.match(/טיפול\s*(\d+)/);
    return { kind: svc ? "service" : "repair", svc_km: svc ? (+svc[1] < 1000 ? +svc[1] * 1000 : +svc[1]) : null, km: null, notes: null, lines };
  }
  function demoInsp(note, ctx) {
    const parts = note.split(/[,.\n]/).map(s => s.trim()).filter(Boolean), checks = [];
    for (const c of ctx.checklist) {
      const part = parts.find(p => c.label.split(/\s+/).some(w => w.length > 2 && p.includes(w.replace(/ים$|ות$/, ""))));
      if (!part) continue;
      const status = /דחוף|להחליף עכשיו|מסוכן|[0-3]\s*מ/.test(part) ? "now" : /בקרוב|שחוק|פסים|חלש|נזיל/.test(part) ? "soon" : "ok";
      checks.push({ key: c.key, status, note: part });
    }
    return { checks, rest_ok: /השאר תקין|כל השאר|השאר בסדר/.test(note) };
  }

  G.register({ id: "ai", name: "עוזר AI", desc: "כותבים במילים או מכתיבים לטלפון, וה-AI ממלא את כרטיס העבודה ואת בדיקת הרכב. הכל לבדיקה לפני שמירה.", groups: "all" });
})(window.Garage);
