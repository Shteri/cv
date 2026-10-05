// Maintenance engine shared by the app (index.html) and the garage dashboard (garage/index.html).
// Plain script: exposes window.TipulitEngine.
// Schedules may start at a different km than the interval (Hyundai i10/i20: first 15,000, then every 20,000).
// We shift the odometer by (first - interval) so the grid becomes regular, then map back to real km.
(function (g) {
  const gridShift = s => (s.first_service_km || s.interval.km) - s.interval.km;
  // first service on the importer's grid strictly after km
  function gridAfter(s, km) {
    const cyc = s.cycle_km, shift = gridShift(s);
    const k = Math.max(0, km - shift);
    const rel = k % cyc, laps = Math.floor(k / cyc);
    const svc = s.services.find(x => (x.km - shift) > rel);
    return svc ? { svc, km: laps * cyc + svc.km } : { svc: s.services[0], km: (laps + 1) * cyc + s.services[0].km };
  }
  // the grid point a past service belongs to: the one it was logged as (svcKm), else the nearest to where it was done
  function gridOf(s, last) {
    const a = gridAfter(s, last.km - s.interval.km), b = gridAfter(s, a.km);
    const cands = [a, b];
    if (last.svcKm) {
      const same = x => (x.km - last.svcKm) % s.cycle_km === 0;
      const hit = cands.filter(same);
      if (hit.length) return hit.reduce((p, q) => Math.abs(q.km - last.km) < Math.abs(p.km - last.km) ? q : p);
    }
    return Math.abs(b.km - last.km) < Math.abs(a.km - last.km) ? b : a;
  }
  // s: schedule; car: { km, kmMonth, lastService "YYYY-MM" | null, lastSvc { km, svcKm } | null }
  // With lastSvc the next service follows the last one actually done: a skipped service shows as overdue, and the
  // window runs between the importer's grid point and the same distance from where the last service was done
  // (60,000 done at 63,000: next is the 90,000 service, due between 90,000 and 93,000).
  function next(s, car) {
    const last = car.lastSvc && car.lastSvc.km > 0 ? car.lastSvc : null;
    let svc, nextKm, windowFrom, windowTo, lastKm = null;
    if (last) {
      const base = gridOf(s, last);
      let n = gridAfter(s, base.km);
      // several services missed: the one to do now is the latest the car has passed
      for (let m = gridAfter(s, n.km); m.km <= car.km; m = gridAfter(s, m.km)) n = m;
      svc = n.svc; nextKm = n.km; lastKm = last.km;
      const byLast = last.km + (nextKm - base.km);
      windowFrom = Math.min(nextKm, byLast); windowTo = Math.max(nextKm, byLast);
    } else {
      ({ svc, km: nextKm } = gridAfter(s, car.km));
      windowFrom = windowTo = nextKm;
    }
    const remainKm = windowTo - car.km;
    const monthsByKm = remainKm / car.kmMonth;
    let dueDate = new Date(); dueDate.setMonth(dueDate.getMonth() + Math.floor(monthsByKm));
    let byTime = null;
    if (car.lastService) {
      byTime = new Date(car.lastService + "-01"); byTime.setMonth(byTime.getMonth() + s.interval.months);
      if (byTime < dueDate) dueDate = byTime;
    }
    const prevKm = windowTo - s.interval.km;
    const progress = Math.min(1, Math.max(0, (car.km - prevKm) / s.interval.km));
    const daysLeft = Math.round((dueDate - new Date()) / 86400000);
    const level = remainKm <= 0 || daysLeft <= 0 ? "crit" : (windowFrom - car.km <= 1500 || daysLeft <= 30) ? "warn" : "good";
    return { s, svc, nextKm, remainKm, windowFrom, windowTo, lastKm, dueDate, byTime, progress, daysLeft, level };
  }
  g.TipulitEngine = { gridShift, gridAfter, next };
})(typeof window !== "undefined" ? window : globalThis);
