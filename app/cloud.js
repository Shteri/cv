// Cloud layer: Supabase auth, sync, community aggregates, receipt storage and extraction.
// Exposes window.TipulitCloud. When config is empty or supabase-js is missing, `enabled` is false
// and the app keeps working on-device only.
(function (g) {
  const cfg = g.TIPULIT_CONFIG || {};
  const lib = g.supabase;
  const enabled = !!(cfg.SUPABASE_URL && cfg.SUPABASE_ANON_KEY && lib && lib.createClient);
  const sb = enabled ? lib.createClient(cfg.SUPABASE_URL, cfg.SUPABASE_ANON_KEY, { auth: { flowType: "implicit", detectSessionInUrl: true, persistSession: true, autoRefreshToken: true } }) : null;
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
  // Implicit flow: tokens come back in the URL hash and supabase-js stores them on load (no stored verifier
  // needed, which some mobile browsers drop between the redirect out and back). We wait for the session and
  // report a readable error if it never arrives.
  async function handleRedirect() {
    if (authError) return { handled: true, error: new Error(authError) };
    const h = new URLSearchParams(location.hash.replace(/^#/, ""));
    const q = new URLSearchParams(location.search);
    if (h.get("access_token")) {
      for (let i = 0; i < 20; i++) { const { data } = await sb.auth.getSession(); if (data.session) return { handled: true, error: null, user: data.session.user }; await new Promise(r => setTimeout(r, 250)); }
      // fall back to setting it ourselves from the hash
      const { data, error } = await sb.auth.setSession({ access_token: h.get("access_token"), refresh_token: h.get("refresh_token") });
      return { handled: true, error, user: data && data.session ? data.session.user : null };
    }
    if (q.get("code")) {
      const { data, error } = await sb.auth.exchangeCodeForSession(q.get("code"));
      if (error && /code verifier/i.test(error.message)) error.hint = "הדפדפן לא שמר את תחילת ההתחברות. נסה שוב, ואם זה חוזר נסה מדפדפן אחר (ספארי או כרום).";
      return { handled: true, error, user: data && data.session ? data.session.user : null };
    }
    return { handled: false, error: null };
  }

  // ---------- cars and records ----------
  // App car -> row
  const carRow = (car, uid) => ({ id: car.cloudId || undefined, user_id: uid, plate: car.plateHold ? null : ((car.plate || "").replace(/\D/g, "") || null), schedule_id: car.schedule, year: car.year || null, km: car.km || 0, km_month: car.kmMonth || 1500, last_service: car.lastService || null, gov: car.gov || null, updated_at: new Date().toISOString() });
  // Row -> app car (records attached separately)
  const rowCar = r => ({ cloudId: r.id, plate: r.plate ? fmtPlate(r.plate) : "", plateReleased: r.released_plate ? fmtPlate(r.released_plate) : null, schedule: r.schedule_id, year: r.year, km: r.km, kmMonth: r.km_month, lastService: r.last_service, gov: r.gov, history: [], added: Date.parse(r.created_at) });
  const fmtPlate = d => d.length <= 7 ? d.replace(/(\d{2})(\d{3})(\d{2})/, "$1-$2-$3") : d.replace(/(\d{3})(\d{2})(\d{3})/, "$1-$2-$3");
  const rowRecord = (r, urls) => ({ id: r.client_id || r.id, cloudId: r.id, kind: r.kind, svcKm: r.svc_km, text: r.text || "", items: r.items || [], date: r.date, km: r.km, where: r.where, garage: r.garage || "", city: r.city || "", price: r.price, back: r.back, extra: r.extra || "", tires: r.tires || null, receiptPaths: r.receipt_paths || [], receipts: urls || [], receipt: (urls || [])[0] || null, share: r.share, source: r.source, at: Date.parse(r.created_at), synced: true });

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

  // Saves for the same car run one after another. Sign-in saves every car while the debounced auto-sync may
  // fire too; run concurrently, two inserts for a car with no cloudId would create two rows.
  const saving = new WeakMap();
  function saveCar(car) {
    const next = (saving.get(car) || Promise.resolve()).catch(() => {}).then(() => saveCarNow(car));
    saving.set(car, next);
    return next;
  }
  async function saveCarNow(car) {
    const uid = (await currentUser())?.id; if (!uid) return;
    let { data, error } = await sb.from("cars").upsert(carRow(car, uid), { onConflict: "id" }).select("id").single();
    // 23505 on cars_plate_unique: the plate is registered on another account (migration 0004).
    if (error && error.code === "23505" && !car.plateHold) { car.plateHold = true; ({ data, error } = await sb.from("cars").upsert(carRow(car, uid), { onConflict: "id" }).select("id").single()); }
    if (error) throw error;
    car.cloudId = data.id;
    for (const rec of car.history || []) {
      if (rec.synced) continue;
      // a record saved again (edited) keeps the receipts it already uploaded
      const paths = (rec.receiptPaths || []).slice();
      for (let i = 0; i < (rec.receipts || []).length; i++) {
        const d = rec.receipts[i]; if (!d || !d.startsWith("data:")) continue;
        const path = `${uid}/${car.cloudId}/${rec.id}-${i}.jpg`;
        const { error: upErr } = await sb.storage.from("receipts").upload(path, await dataUrlToBlob(d), { contentType: "image/jpeg", upsert: true });
        if (!upErr && !paths.includes(path)) paths.push(path);
      }
      const { data: saved, error: rErr } = await sb.from("records").upsert({ car_id: car.cloudId, user_id: uid, kind: rec.kind || "service", svc_km: rec.svcKm || null, text: rec.text || null, items: rec.items || [], date: rec.date || null, km: rec.km, where: rec.where || null, garage: rec.garage || null, city: rec.city || null, price: rec.price || null, back: rec.back || null, extra: rec.extra || null, receipt_paths: paths, tires: rec.tires && rec.tires.length ? rec.tires : null, share: !!rec.share, source: rec.source || "log", client_id: rec.id }, { onConflict: "car_id,client_id" }).select("id").single();
      if (!rErr) { rec.cloudId = saved.id; rec.receiptPaths = paths; rec.synced = true; }
    }
  }
  // one record, with its receipt files
  async function deleteRecord(rec) {
    if (!rec.cloudId) return;
    if ((rec.receiptPaths || []).length) await sb.storage.from("receipts").remove(rec.receiptPaths);
    const { error } = await sb.from("records").delete().eq("id", rec.cloudId);
    if (error) throw error;
  }
  // records and garage links go with the row (on delete cascade); receipts are files, removed first
  async function deleteCar(car) {
    if (!car.cloudId) return;
    const paths = (car.history || []).flatMap(r => r.receiptPaths || []);
    if (paths.length) await sb.storage.from("receipts").remove(paths);
    const { error } = await sb.from("cars").delete().eq("id", car.cloudId);
    if (error) throw error;
  }

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

  // ---------- garage profiles (owners claim a licensed garage) ----------
  // Rows are plain objects mirroring the table; see supabase/migrations/0002_garage_profiles.sql.
  async function myGarageProfiles() {
    const uid = (await currentUser())?.id; if (!uid) return [];
    const { data, error } = await sb.from("garage_profiles").select("*").eq("owner_id", uid).order("created_at");
    if (error) { if (/relation|does not exist|schema cache/i.test(error.message)) return []; throw error; }
    return data || [];
  }
  async function garageProfiles(city) {
    const cols = "id, garage_id, name, city, address, phone, whatsapp, booking_url, booking_enabled, about, makes, services, hours, prices, photos, status, verified_via";
    let { data, error } = await sb.from("garage_profiles").select(cols + ", aka").eq("city", city).eq("status", "verified");
    // a server before migration 0011 has no aka column
    if (error) ({ data, error } = await sb.from("garage_profiles").select(cols).eq("city", city).eq("status", "verified"));
    if (error) return [];
    return data || [];
  }
  async function saveGarageProfile(p) {
    const uid = (await currentUser())?.id; if (!uid) throw new Error("not signed in");
    const photos = [];
    for (let i = 0; i < (p.photos || []).length; i++) {
      const d = p.photos[i];
      if (!d.startsWith("data:")) { photos.push(d); continue; }
      const path = `${uid}/${p.garage_id}/${Date.now()}-${i}.jpg`;
      const { error } = await sb.storage.from("garage-photos").upload(path, await dataUrlToBlob(d), { contentType: "image/jpeg", upsert: true });
      if (!error) photos.push(path);
    }
    const row = { id: p.id || undefined, garage_id: p.garage_id, owner_id: uid, name: p.name, city: p.city, address: p.address || null, phone: p.phone || null, registry_phone: p.registry_phone || null, whatsapp: p.whatsapp || null, booking_url: p.booking_url || null, about: p.about || null, makes: p.makes || [], services: p.services || [], hours: p.hours || {}, prices: p.prices || [], photos, ...(Array.isArray(p.aka) ? { aka: p.aka } : {}) };
    const { data, error } = await sb.from("garage_profiles").upsert(row, { onConflict: "garage_id,owner_id" }).select("*").single();
    if (error) throw error;
    return data;
  }
  async function deleteGarageProfile(id) { const { error } = await sb.from("garage_profiles").delete().eq("id", id); if (error) throw error; }
  const photoUrl = path => path && path.startsWith("data:") ? path : sb.storage.from("garage-photos").getPublicUrl(path).data.publicUrl;
  // Phone verification: links the registry phone to the signed-in account via SMS OTP (needs an SMS provider in
  // Supabase Auth). Then claim-garage (Edge Function) compares it with the registry and flips the status.
  async function startPhoneVerify(phone) { const { error } = await sb.auth.updateUser({ phone: toE164(phone) }); if (error) throw error; }
  async function confirmPhoneVerify(phone, token) { const { error } = await sb.auth.verifyOtp({ phone: toE164(phone), token, type: "phone_change" }); if (error) throw error; }
  const toE164 = p => { const d = p.replace(/\D/g, ""); return d.startsWith("972") ? "+" + d : "+972" + d.replace(/^0/, ""); };
  async function claimGarage(profileId) {
    const { data, error } = await sb.functions.invoke("claim-garage", { body: { profile_id: profileId } });
    if (error) throw error;
    if (data && data.error) throw new Error(data.error);
    return data;
  }
  async function pendingGarageClaims() { const { data, error } = await sb.rpc("pending_garage_claims"); if (error) throw error; return data || []; }
  async function setGarageStatus(id, status) { const { error } = await sb.rpc("set_garage_status", { p_id: id, p_status: status }); if (error) throw error; }

  // ---------- garage customers (migration 0003) ----------
  // Driver side: link a car to a verified garage (consent), list/revoke links, decide on visits a garage logged.
  async function garagePublic(id) {
    const { data, error } = await sb.from("garage_profiles").select("id, garage_id, name, city, address, phone").eq("id", id).eq("status", "verified").maybeSingle();
    if (error) throw error;
    return data;
  }
  async function joinGarage({ garageId, carCloudId, firstName, phone, allowContact, shareHistory }) {
    const uid = (await currentUser())?.id; if (!uid) throw new Error("not signed in");
    const row = { garage_id: garageId, car_id: carCloudId, user_id: uid, first_name: firstName || null, phone: phone || null, allow_contact: !!allowContact, share_history: !!shareHistory };
    const { data, error } = await sb.from("garage_links").upsert(row, { onConflict: "garage_id,car_id" }).select("id").single();
    if (error) throw error;
    return data.id;
  }
  async function myGarageLinks() {
    const cols = g => `id, car_id, allow_contact, share_history, show_garage_names, phone, first_name, created_at, garage_profiles(id, name, city, phone, whatsapp${g})`;
    let { data, error } = await sb.from("garage_links").select(cols(", booking_enabled")).order("created_at");
    // booking_enabled arrives with migration 0006; until then read the links without it
    if (error && /booking_enabled/.test(error.message)) ({ data, error } = await sb.from("garage_links").select(cols("")).order("created_at"));
    if (error) { if (/relation|does not exist|schema cache/i.test(error.message)) return []; throw error; }
    return data || [];
  }
  async function updateGarageLink(id, patch) { const { error } = await sb.from("garage_links").update(patch).eq("id", id); if (error) throw error; }
  async function leaveGarage(id) { const { error } = await sb.from("garage_links").delete().eq("id", id); if (error) throw error; }
  async function pendingGarageEntries() {
    const { data, error } = await sb.from("garage_entries").select("id, car_id, kind, svc_km, km, date, price, text, where, created_at, garage_profiles(name, city)").eq("status", "pending").order("created_at");
    if (error) { if (/relation|does not exist|schema cache/i.test(error.message)) return []; throw error; }
    return data || [];
  }
  async function decideGarageEntry(id, accept) { const { error } = await sb.rpc("decide_garage_entry", { p_id: id, p_accept: !!accept }); if (error) throw error; }
  // Garage side: customers of a verified garage the caller owns, and logging a visit for one of them.
  async function garageCustomers(garageId) { const { data, error } = await sb.rpc("garage_customers", { p_garage: garageId }); if (error) throw error; return data || []; }
  async function garageAddEntry(linkId, e) {
    const { data, error } = await sb.rpc("garage_add_entry", { p_link: linkId, p_kind: e.kind, p_svc_km: e.svcKm || null, p_km: e.km, p_date: e.date || "", p_price: e.price || null, p_text: e.text || "", p_where: e.where || null });
    if (error) throw error;
    return data;
  }

  // ---------- garage book (migration 0005): the garage's own customers, cars and work orders ----------
  const must = ({ data, error }) => { if (error) throw error; return data; };
  const garageBook = garageId => sb.rpc("garage_book", { p_garage: garageId }).then(must);
  const garageCarHistory = garageCarId => sb.rpc("garage_car_history", { p_garage_car: garageCarId }).then(must);
  const workOrders = garageId => sb.from("work_orders").select("*").eq("garage_id", garageId).order("date", { ascending: false }).then(must);
  const addCustomer = row => sb.from("garage_customers").insert(row).select("id").single().then(must);
  const updateCustomer = (id, patch) => sb.from("garage_customers").update({ ...patch, updated_at: new Date().toISOString() }).eq("id", id).then(must);
  const deleteCustomer = id => sb.from("garage_customers").delete().eq("id", id).then(must);
  const addGarageCar = row => sb.from("garage_cars").insert(row).select("id").single().then(must);
  const updateGarageCar = (id, patch) => sb.from("garage_cars").update(patch).eq("id", id).then(must);
  const saveWorkOrder = row => sb.from("work_orders").upsert(row).select("*").single().then(must);
  const sendWorkOrder = (id, where) => sb.rpc("work_order_send", { p_work_order: id, p_where: where }).then(must);
  // Bulk import: customers first (ids come back in order), then their cars.
  async function importCustomers(garageId, rows) {
    const out = { added: 0, skipped: 0 };
    for (let i = 0; i < rows.length; i += 200) {
      const chunk = rows.slice(i, i + 200);
      const custs = must(await sb.from("garage_customers").insert(chunk.map(r => ({ garage_id: garageId, name: r.name, phone: r.phone || null, contact_consent: !!r.consent, source: "import", notes: r.notes || null }))).select("id"));
      for (let k = 0; k < chunk.length; k++) {
        const r = chunk[k];
        const { error } = await sb.from("garage_cars").insert({ garage_id: garageId, customer_id: custs[k].id, plate: r.plate || null, schedule_id: r.schedule_id || null, year: r.year || null, km: r.km || null, km_month: r.km_month || 1500, last_service: r.last_service || null, test_expiry: r.test_expiry || null, gov: r.gov || null });
        if (error) { out.skipped++; await sb.from("garage_customers").delete().eq("id", custs[k].id); } else out.added++;
      }
    }
    return out;
  }

  // ---------- calendar, online booking, extra-work approvals (migration 0006) ----------
  const appointments = (garageId, fromIso, toIso) => sb.from("appointments").select("*").eq("garage_id", garageId).gte("starts_at", fromIso).lt("starts_at", toIso).order("starts_at").then(must);
  // Existing rows are patched by id (a partial upsert would trip NOT NULL columns); new rows are inserted.
  const saveAppointment = ({ id, ...row }) => (id ? sb.from("appointments").update({ ...row, updated_at: new Date().toISOString() }).eq("id", id) : sb.from("appointments").insert(row)).select("*").single().then(must);
  const approvalsFor = garageId => sb.from("work_approvals").select("*").eq("garage_id", garageId).order("created_at", { ascending: false }).limit(200).then(must);
  const createApproval = row => sb.from("work_approvals").insert(row).select("*").single().then(must);
  const updateGarageSettings = (id, patch) => sb.from("garage_profiles").update({ ...patch, updated_at: new Date().toISOString() }).eq("id", id).select("*").single().then(must);
  // ---------- inventory, purchase orders, invoices (migration 0007) ----------
  // rows with an id are patched, rows without are inserted
  const upsertRow = table => ({ id, ...row }) => (id ? sb.from(table).update(row).eq("id", id) : sb.from(table).insert(row)).select("*").single().then(must);
  const listOf = (table, order, asc = false) => garageId => sb.from(table).select("*").eq("garage_id", garageId).order(order, { ascending: asc }).limit(2000).then(must);
  const parts = listOf("parts", "name", true), suppliers = listOf("suppliers", "name", true), purchaseOrders = listOf("purchase_orders", "created_at"), invoices = listOf("invoices", "issued_at");
  const savePart = row => upsertRow("parts")({ ...row, ...(row.id ? { updated_at: new Date().toISOString() } : {}) });
  const deletePart = id => sb.from("parts").delete().eq("id", id).then(must);
  const saveSupplier = upsertRow("suppliers");
  const deleteSupplier = id => sb.from("suppliers").delete().eq("id", id).then(must);
  const savePurchaseOrder = row => upsertRow("purchase_orders")({ ...row, ...(row.id ? { updated_at: new Date().toISOString() } : {}) });
  const deletePurchaseOrder = id => sb.from("purchase_orders").delete().eq("id", id).then(must);
  const receivePurchaseOrder = (id, lines) => sb.rpc("po_receive", { p_po: id, p_lines: lines }).then(must);
  const addStockMove = row => sb.from("stock_moves").insert(row).select("*").single().then(must);
  const partMoves = partId => sb.from("stock_moves").select("*").eq("part_id", partId).order("created_at", { ascending: false }).limit(30).then(must);
  const woConsume = woId => sb.rpc("wo_consume", { p_wo: woId }).then(must);
  const recordInvoice = row => sb.from("invoices").insert(row).select("*").single().then(must);
  const deleteInvoice = id => sb.from("invoices").delete().eq("id", id).then(must);
  const billing = garageId => sb.from("garage_billing").select("garage_id, provider, api_id, has_secret, sandbox, vat_exempt, updated_at").eq("garage_id", garageId).maybeSingle().then(must);
  const billingDelete = garageId => sb.from("garage_billing").delete().eq("garage_id", garageId).then(must);
  const billingSave = (garageId, b) => sb.rpc("billing_save", { p_garage: garageId, p_api_id: b.api_id || "", p_secret: b.secret || "", p_sandbox: !!b.sandbox, p_vat_exempt: !!b.vat_exempt }).then(must);
  // issues through the garage's Morning account (edge function issue-document); the reply carries the provider's error text
  async function issueDocument(body) {
    const { data, error } = await sb.functions.invoke("issue-document", { body });
    if (error) { let m = error.message; try { const j = await error.context.json(); m = [j.error || m, j.detail || j.stop].filter(Boolean).join(": "); } catch (e) {} throw new Error(m); }
    if (data && data.error) throw new Error(data.error);
    return data;
  }

  // ---------- job catalog and vehicle inspection (migration 0008) ----------
  // ---------- AI assist (edge function ai-assist): a short note becomes structured data, shown for review ----------
  async function aiAssist(task, note, context) {
    const { data, error } = await sb.functions.invoke("ai-assist", { body: { task, note, context } });
    if (error) { let m = error.message; try { const j = await error.context.json(); m = [j.error || m, j.detail || j.stop].filter(Boolean).join(": "); } catch (e) {} throw new Error(m); }
    if (data && data.error) throw new Error(data.error);
    return data.result;
  }
  const jobTemplates = garageId => sb.from("job_templates").select("*").eq("garage_id", garageId).order("category").order("name").then(must);
  const saveJob = upsertRow("job_templates");
  const deleteJob = id => sb.from("job_templates").delete().eq("id", id).then(must);
  const approvalChoose = (id, lines) => sb.rpc("approval_choose", { p_id: id, p_lines: lines }).then(must);
  // photos go to the garage's folder in a public bucket under a random name; returns the public URL
  async function uploadInspectionPhoto(garageId, blob) {
    const path = `${garageId}/${crypto.randomUUID()}.jpg`;
    const { error } = await sb.storage.from("inspection-photos").upload(path, blob, { contentType: "image/jpeg", upsert: false });
    if (error) throw error;
    return sb.storage.from("inspection-photos").getPublicUrl(path).data.publicUrl;
  }

  // public (no sign-in)
  const bookingInfo = garageId => sb.rpc("booking_info", { p_garage: garageId }).then(must);
  const bookAppointment = a => sb.rpc("book_appointment", { p_garage: a.garageId, p_starts_at: a.startsAt, p_name: a.name, p_phone: a.phone, p_plate: a.plate || "", p_kind: a.kind || "service", p_note: a.note || "" }).then(must);
  // books and returns { token, needs_ok }; a server before migration 0010 books the old way (no link token)
  const bookSlot = async a => {
    const args = { p_garage: a.garageId, p_starts_at: a.startsAt, p_name: a.name, p_phone: a.phone, p_plate: a.plate || "", p_kind: a.kind || "service", p_note: a.note || "" };
    const { data, error } = await sb.rpc("book_slot", args);
    if (!error) return data;
    if (error.code === "PGRST202" || /book_slot/.test(error.message || "")) { await bookAppointment(a); return { token: null, needs_ok: false }; }
    throw error;
  };
  // the customer's appointment link (/appt/?t=token) and the garage's view of a phone's no-shows
  const apptGet = token => sb.rpc("appt_get", { p_token: token }).then(must);
  const apptRespond = (token, action) => sb.rpc("appt_respond", { p_token: token, p_action: action }).then(must);
  const apptStrikes = (garageId, phone) => sb.rpc("appt_strikes", { p_garage: garageId, p_phone: phone }).then(must);
  const approvalGet = id => sb.rpc("approval_get", { p_id: id }).then(must);
  const approvalDecide = (id, approve) => sb.rpc("approval_decide", { p_id: id, p_approve: !!approve }).then(must);

  // ---------- plate lock (migration 0004) ----------
  const digits = p => String(p || "").replace(/\D/g, "");
  async function plateStatus(plate) { const { data, error } = await sb.rpc("plate_status", { p_plate: digits(plate) }); if (error) throw error; return data; }
  async function claimPlate(plate) { const { data, error } = await sb.rpc("claim_plate", { p_plate: digits(plate) }); if (error) throw error; return data; }
  async function requestPlate(plate, photoDataUrl, note) {
    const uid = (await currentUser())?.id; if (!uid) throw new Error("not signed in");
    let photo_path = null;
    if (photoDataUrl) { photo_path = `${uid}/${digits(plate)}-${Date.now()}.jpg`; const { error } = await sb.storage.from("plate-proofs").upload(photo_path, await dataUrlToBlob(photoDataUrl), { contentType: "image/jpeg" }); if (error) throw error; }
    const { error } = await sb.from("plate_requests").insert({ plate: digits(plate), requester_id: uid, photo_path, note: note || null });
    if (error) throw error;
  }
  async function pendingPlateRequests() {
    const { data, error } = await sb.rpc("pending_plate_requests"); if (error) throw error;
    const paths = (data || []).map(r => r.photo_path).filter(Boolean); let urls = {};
    if (paths.length) { const { data: s } = await sb.storage.from("plate-proofs").createSignedUrls(paths, 3600); for (const u of s || []) if (u.signedUrl) urls[u.path] = u.signedUrl; }
    return (data || []).map(r => ({ ...r, photo_url: urls[r.photo_path] || null }));
  }
  async function decidePlateRequest(id, approve) { const { error } = await sb.rpc("decide_plate_request", { p_id: id, p_approve: !!approve }); if (error) throw error; }

  // ---------- receipt reading: a photo (shrunk on the device) or a PDF, through ai-assist (signed in, daily limit) ----------
  async function extractReceipt(dataUrl, context) {
    const { data, error } = await sb.functions.invoke("ai-assist", { body: { task: "receipt", file: { data: dataUrlToBase64(dataUrl), media_type: mediaOf(dataUrl) }, context } });
    if (error) { let m = error.message; try { const j = await error.context.json(); m = [j.error || m, j.detail || j.stop].filter(Boolean).join(": "); } catch (e) {} throw new Error(m); }
    if (data && data.error) throw new Error(data.error);
    return data.result;
  }

  g.TipulitCloud = { enabled, authError, hasAuthParams, currentUser, onAuth, signInWithGoogle, signOut, handleRedirect, loadCars, saveCar, deleteCar, deleteRecord, communityPrices, communityGarages, extractReceipt, myGarageProfiles, garageProfiles, saveGarageProfile, deleteGarageProfile, photoUrl, startPhoneVerify, confirmPhoneVerify, claimGarage, pendingGarageClaims, setGarageStatus, garagePublic, joinGarage, myGarageLinks, updateGarageLink, leaveGarage, pendingGarageEntries, decideGarageEntry, garageCustomers, garageAddEntry, plateStatus, claimPlate, requestPlate, pendingPlateRequests, decidePlateRequest, garageBook, garageCarHistory, workOrders, addCustomer, updateCustomer, deleteCustomer, addGarageCar, updateGarageCar, saveWorkOrder, sendWorkOrder, importCustomers, appointments, saveAppointment, approvalsFor, createApproval, updateGarageSettings, bookingInfo, bookAppointment, bookSlot, apptGet, apptRespond, apptStrikes, approvalGet, approvalDecide, parts, suppliers, purchaseOrders, invoices, savePart, deletePart, saveSupplier, deleteSupplier, savePurchaseOrder, deletePurchaseOrder, receivePurchaseOrder, addStockMove, partMoves, woConsume, recordInvoice, deleteInvoice, billing, billingSave, billingDelete, issueDocument, jobTemplates, saveJob, deleteJob, approvalChoose, uploadInspectionPhoto, aiAssist };
})(window);
