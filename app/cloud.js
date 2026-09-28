// Cloud layer: Supabase auth, sync, community aggregates, receipt storage and extraction.
// Exposes window.TipulitCloud. When config is empty or supabase-js is missing, `enabled` is false
// and the app keeps working on-device only.
(function (g) {
  const cfg = g.TIPULIT_CONFIG || {};
  const lib = g.supabase;
  const enabled = !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY && lib && lib.createClient);
  const sb = enabled ? lib.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY, { auth: { flowType: "pkce", detectSessionInUrl: false, persistSession: true, autoRefreshToken: true } }) : null;
  // OAuth errors come back in the URL (?error=... or #error=...). Expose them so the app can show them.
  const authError = (() => { const q = new URLSearchParams(location.search), h = new URLSearchParams(location.hash.replace(/^#/, "")); return q.get("error_description") || h.get("error_description") || q.get("error") || h.get("error") || null; })();
  const hasAuthParams = /[?&#](code|access_token|error)=/.test(location.href);

  const dataUrlToBlob = async d => (await fetch(d)).blob();
  const dataUrlToBase64 = d => d.split(",")[1];
  const mediaOf = d => (d.match(/^data:([^;]+);/) || [, "image/jpeg"])[1];

  // getSession reads the stored session (no network) and is safe to call from anywhere.
  async function currentUser() { if (!sb) return null; const { data } = await sb.auth.getSession(); return data.session ? data.session.user : null; }
  // supabase-js deadlocks if other auth calls run inside the onAuthStateChange callback, so defer the app's handler.
  function onAuth(cb) { if (!sb) return; sb.auth.onAuthStateChange((event, session) => { if (event === "TOKEN_REFRESHED") return; setTimeout(() => cb(session ? session.user : null, event), 0); }); }
  async function signInWithGoogle() {
    const redirectTo = location.origin + location.pathname;
    const { error } = await sb.auth.signInWithOAuth({ provider: "google", options: { redirectTo } });
    if (error) throw error;
  }
  async function signOut() { await sb.auth.signOut(); }
  // Finish the OAuth round trip ourselves so failures are visible (supabase-js swallows them when it auto-detects).
  async function handleRedirect() {
    const q = new URLSearchParams(location.search);
    const code = q.get("code");
    if (!code) return { handled: false, error: authError ? new Error(authError) : null };
    const { data, error } = await sb.auth.exchangeCodeForSession(code);
    try { history.replaceState(history.state, "", location.pathname + (location.hash || "")); } catch (e) {}
    if (error && /code verifier/i.test(error.message)) error.hint = "ההתחברות התחילה מכתובת אחרת או מדפדפן אחר. פתח את tipulit.netlify.app ונסה שוב מאותו דפדפן.";
    return { handled: true, error, user: data && data.session ? data.session.user : null };
  }

  // ---------- cars and records ----------
  // App car -> row
  const carRow = (car, uid) => ({ id: car.cloudId || undefined, user_id: uid, plate: (car.plate || "").replace(/\D/g, "") || null, schedule_id: car.schedule, year: car.year || null, km: car.km || 0, km_month: car.kmMonth || 1500, last_service: car.lastService || null, gov: car.gov || null, updated_at: new Date().toISOString() });
  // Row -> app car (records attached separately)
  const rowCar = r => ({ cloudId: r.id, plate: r.plate ? fmtPlate(r.plate) : "", schedule: r.schedule_id, year: r.year, km: r.km, kmMonth: r.km_month, lastService: r.last_service, gov: r.gov, history: [], added: Date.parse(r.created_at) });
  const fmtPlate = d => d.length <= 7 ? d.replace(/(\d{2})(\d{3})(\d{2})/, "$1-$2-$3") : d.replace(/(\d{3})(\d{2})(\d{3})/, "$1-$2-$3");
  const rowRecord = (r, urls) => ({ id: r.client_id || r.id, cloudId: r.id, kind: r.kind, svcKm: r.svc_km, text: r.text || "", items: r.items || [], date: r.date, km: r.km, where: r.where, garage: r.garage || "", city: r.city || "", price: r.price, back: r.back, extra: r.extra || "", receiptPaths: r.receipt_paths || [], receipts: urls || [], receipt: (urls || [])[0] || null, share: r.share, source: r.source, at: Date.parse(r.created_at), synced: true });

  async function loadCars() {
    const uid = (await currentUser())?.id; if (!uid) return [];
    const { data: cars, error } = await sb.from("cars").select("*").order("created_at");
    if (error) throw error;
    const { data: recs } = await sb.from("records").select("*").order("created_at");
    const paths = (recs || []).flatMap(r => r.receipt_paths || []);
    let urlByPath = {};
    if (paths.length) { const { data } = await sb.storage.from("receipts").createSignedUrls(paths, 3600); for (const u of data || []) if (u.signedUrl) urlByPath[u.path] = u.signedUrl; }
    return (cars || []).map(c => { const car = rowCar(c); car.history = (recs || []).filter(r => r.car_id === c.id).map(r => rowRecord(r, (r.receipt_paths || []).map(p => urlByPath[p]).filter(Boolean))); return car; });
  }

  async function saveCar(car) {
    const uid = (await currentUser())?.id; if (!uid) return;
    const row = carRow(car, uid);
    const { data, error } = await sb.from("cars").upsert(row, { onConflict: "id" }).select("id").single();
    if (error) throw error;
    car.cloudId = data.id;
    for (const rec of car.history || []) {
      if (rec.synced) continue;
      const paths = [];
      for (let i = 0; i < (rec.receipts || []).length; i++) {
        const d = rec.receipts[i]; if (!d || !d.startsWith("data:")) continue;
        const path = `${uid}/${car.cloudId}/${rec.id}-${i}.jpg`;
        const { error: upErr } = await sb.storage.from("receipts").upload(path, await dataUrlToBlob(d), { contentType: "image/jpeg", upsert: true });
        if (!upErr) paths.push(path);
      }
      const { data: saved, error: rErr } = await sb.from("records").upsert({ car_id: car.cloudId, user_id: uid, kind: rec.kind || "service", svc_km: rec.svcKm || null, text: rec.text || null, items: rec.items || [], date: rec.date || null, km: rec.km, where: rec.where || null, garage: rec.garage || null, city: rec.city || null, price: rec.price || null, back: rec.back || null, extra: rec.extra || null, receipt_paths: paths, share: !!rec.share, source: rec.source || "log", client_id: rec.id }, { onConflict: "car_id,client_id" }).select("id").single();
      if (!rErr) { rec.cloudId = saved.id; rec.receiptPaths = paths; rec.synced = true; }
    }
  }
  async function deleteCar(car) { if (car.cloudId) await sb.from("cars").delete().eq("id", car.cloudId); }

  // ---------- community ----------
  async function communityPrices(scheduleId, svcKm) {
    const { data, error } = await sb.rpc("community_prices", { p_schedule_id: scheduleId, p_svc_km: svcKm });
    if (error || !data) return null;
    const out = {};
    for (const r of data) out[r.where] = { med: +r.med, lo: +r.p25, hi: +r.p75, n: +r.n, verified: +r.verified, latest: r.latest };
    return out;
  }
  async function communityGarages(scheduleId) {
    const { data, error } = await sb.rpc("community_garages", { p_schedule_id: scheduleId });
    if (error || !data) return [];
    return data.map(r => ({ name: r.garage, city: r.city || "", type: r.where, n: +r.n, prices: r.avg_price ? [+r.avg_price] : [], back: r.back_pct === null ? [] : [r.back_pct >= 50], backPctRaw: r.back_pct }));
  }

  // ---------- receipt extraction (Edge Function -> Claude vision) ----------
  async function extractReceipt(dataUrl, context) {
    const { data, error } = await sb.functions.invoke("extract-receipt", { body: { image_base64: dataUrlToBase64(dataUrl), media_type: mediaOf(dataUrl), context } });
    if (error) throw error;
    if (data && data.error) throw new Error(data.error);
    return data;
  }

  g.TipulitCloud = { enabled, authError, hasAuthParams, currentUser, onAuth, signInWithGoogle, signOut, handleRedirect, loadCars, saveCar, deleteCar, communityPrices, communityGarages, extractReceipt };
})(window);
