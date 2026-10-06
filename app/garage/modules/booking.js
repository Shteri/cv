// Online booking: settings, booking link and printable QR sign (the public page is /book/).
(function (G) {
  const { $, api, copy, demo, loadQr, st, toast, why } = G;
  // other modules, looked up when called
  const renderCalendar = (...a) => G.renderCalendar(...a);
  // ---------- online booking settings ----------
  // ---------- opening hours: one row per weekday (0 = Sunday), the format of garage_profiles.hours ----------
  const DAYS = ["ראשון", "שני", "שלישי", "רביעי", "חמישי", "שישי", "שבת"];
  function renderHours(h) {
    $("#bk-hours").innerHTML = DAYS.map((n, i) => { const d = h[i]; return `<tr><td>${n}</td><td><label class="check"><input type="checkbox" data-hd="${i}" ${d ? "checked" : ""}> פתוח</label></td><td><input type="time" class="num" data-ho="${i}" value="${d ? d.open : "08:00"}" aria-label="פתיחה ביום ${n}" ${d ? "" : "disabled"}></td><td><input type="time" class="num" data-hc="${i}" value="${d ? d.close : "17:00"}" aria-label="סגירה ביום ${n}" ${d ? "" : "disabled"}></td></tr>`; }).join("");
    for (const cb of document.querySelectorAll("#bk-hours [data-hd]")) cb.onchange = () => { const i = cb.dataset.hd; for (const x of document.querySelectorAll(`#bk-hours [data-ho="${i}"], #bk-hours [data-hc="${i}"]`)) x.disabled = !cb.checked; };
  }
  function readHours() {
    const out = {};
    DAYS.forEach((n, i) => {
      if (!$(`#bk-hours [data-hd="${i}"]`).checked) { out[i] = null; return; }
      const open = $(`#bk-hours [data-ho="${i}"]`).value, close = $(`#bk-hours [data-hc="${i}"]`).value;
      if (!open || !close || open >= close) { const m = `ביום ${n} שעת הסגירה צריכה להיות אחרי שעת הפתיחה`; throw Object.assign(new Error(m), { userMessage: m }); }
      out[i] = { open, close };
    });
    if (!Object.values(out).some(Boolean)) throw Object.assign(new Error("צריך לפחות יום פתוח אחד"), { userMessage: "צריך לפחות יום פתוח אחד" });
    return out;
  }
  const sameHours = (a, b) => JSON.stringify(a) === JSON.stringify(b);
  const bookUrl = id => location.origin + location.pathname.replace(/garage\/[^/]*$/, "") + "book/?g=" + id;
  function openSettings() {
    const g = st.garage, url = demo ? bookUrl("demo").replace("?g=demo", "?demo") : bookUrl(g.id);
    $("#bk-on").checked = !!g.booking_enabled; $("#bk-bays").value = g.bays || 2; $("#bk-slot").value = String(g.slot_minutes || 60); if (!$("#bk-slot").value) $("#bk-slot").value = "60";
    $("#bk-link").value = url; $("#bk-garage").textContent = g.name; $("#bk-err").hidden = true;
    renderHours(G.hoursOf(g)); $("#bk-demo").hidden = !demo;
    $("#bk-wa").href = "https://wa.me/?text=" + encodeURIComponent(`לקביעת תור ב${g.name}: ${url}`);
    $("#bk-qr").innerHTML = `<p class="muted small">טוען…</p>`;
    loadQr().then(qrcode => { const q = qrcode(0, "M"); q.addData(url); q.make(); $("#bk-qr").innerHTML = q.createSvgTag({ cellSize: 6, margin: 1, scalable: true }); }).catch(() => { $("#bk-qr").innerHTML = ""; });
    $("#dlg-settings").showModal();
  }
  $("#cal-settings").onclick = openSettings;
  $("#bk-clear").onclick = () => { const n = G.demoSamples(true); toast(n ? `נוקו ${n} תורים לדוגמה. היומן ודף קביעת התור ריקים מהם` : "אין תורים לדוגמה"); renderCalendar(); };
  $("#bk-sample").onclick = () => { if (G.DEMO) G.DEMO.noSample = false; G.demoSamples(false); toast("התורים לדוגמה חזרו"); renderCalendar(); };
  $("#bk-copy").onclick = () => copy($("#bk-link").value, "הקישור הועתק");
  $("#bk-print").onclick = () => { document.body.classList.add("printing"); window.print(); setTimeout(() => document.body.classList.remove("printing"), 500); };
  $("#bk-save").onclick = async () => {
    const patch = { booking_enabled: $("#bk-on").checked, bays: Math.max(1, Math.min(30, +$("#bk-bays").value || 2)), slot_minutes: +$("#bk-slot").value || 60 };
    try {
      patch.hours = readHours();
      const moved = !sameHours(patch.hours, G.hoursOf(st.garage));
      if (!demo) await api.updateGarageSettings(st.garage.id, patch);
      Object.assign(st.garage, patch);
      // the demo's sample appointments follow the new week, so the calendar and the booking page agree
      if (demo && moved) G.demoSamples(false); else if (demo) G.demoSave && G.demoSave();
      $("#dlg-settings").close(); toast(patch.booking_enabled ? "התורים האונליין פתוחים" : "נשמר"); renderCalendar();
    }
    catch (e) { $("#bk-err").textContent = "השמירה נכשלה: " + why(e); $("#bk-err").hidden = false; }
  };

  G.register({ id: "booking", name: "תורים אונליין", desc: "קישור ושלט QR שבהם לקוחות קובעים תור לבד, לפי שעות הפתיחה והעמדות הפנויות.", groups: "all" });
})(window.Garage);
