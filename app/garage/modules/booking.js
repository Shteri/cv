// Online booking: settings, booking link and printable QR sign (the public page is /book/).
(function (G) {
  const { $, api, copy, demo, loadQr, st, toast } = G;
  // other modules, looked up when called
  const renderCalendar = (...a) => G.renderCalendar(...a);
  // ---------- online booking settings ----------
  const bookUrl = id => location.origin + location.pathname.replace(/garage\/[^/]*$/, "") + "book/?g=" + id;
  function openSettings() {
    const g = st.garage, url = demo ? location.origin + "/book/?demo" : bookUrl(g.id);
    $("#bk-on").checked = !!g.booking_enabled; $("#bk-bays").value = g.bays || 2; $("#bk-slot").value = String(g.slot_minutes || 60); if (!$("#bk-slot").value) $("#bk-slot").value = "60";
    $("#bk-link").value = url; $("#bk-garage").textContent = g.name; $("#bk-err").hidden = true;
    $("#bk-wa").href = "https://wa.me/?text=" + encodeURIComponent(`לקביעת תור ב${g.name}: ${url}`);
    $("#bk-qr").innerHTML = `<p class="muted small">טוען…</p>`;
    loadQr().then(qrcode => { const q = qrcode(0, "M"); q.addData(url); q.make(); $("#bk-qr").innerHTML = q.createSvgTag({ cellSize: 6, margin: 1, scalable: true }); }).catch(() => { $("#bk-qr").innerHTML = ""; });
    $("#dlg-settings").showModal();
  }
  $("#cal-settings").onclick = openSettings;
  $("#bk-copy").onclick = () => copy($("#bk-link").value, "הקישור הועתק");
  $("#bk-print").onclick = () => { document.body.classList.add("printing"); window.print(); setTimeout(() => document.body.classList.remove("printing"), 500); };
  $("#bk-save").onclick = async () => {
    const patch = { booking_enabled: $("#bk-on").checked, bays: Math.max(1, Math.min(30, +$("#bk-bays").value || 2)), slot_minutes: +$("#bk-slot").value || 60 };
    try { if (!demo) await api.updateGarageSettings(st.garage.id, patch); Object.assign(st.garage, patch); $("#dlg-settings").close(); toast(patch.booking_enabled ? "התורים האונליין פתוחים" : "נשמר"); renderCalendar(); }
    catch (e) { $("#bk-err").textContent = "השמירה נכשלה: " + (e.message || e); $("#bk-err").hidden = false; }
  };

  G.register({ id: "booking", name: "תורים אונליין", desc: "קישור ושלט QR שבהם לקוחות קובעים תור לבד, לפי שעות הפתיחה והעמדות הפנויות.", groups: "all" });
})(window.Garage);
