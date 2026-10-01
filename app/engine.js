// Maintenance engine shared by the app (index.html) and the garage dashboard (garage/index.html).
// Plain script: exposes window.TipulitEngine.
// Schedules may start at a different km than the interval (Hyundai i10/i20: first 15,000, then every 20,000).
// We shift the odometer by (first - interval) so the grid becomes regular, then map back to real km.
(function (g) {
  const gridShift = s => (s.first_service_km || s.interval.km) - s.interval.km;
  // s: schedule; car: { km, kmMonth, lastService "YYYY-MM" | null }
  function next(s, car) {
    const cyc = s.cycle_km, shift = gridShift(s);
    const k = Math.max(0, car.km - shift);
    const rel = k % cyc, laps = Math.floor(k / cyc);
    let svc = s.services.find(x => (x.km - shift) > rel);
    let nextKm;
    if (svc) nextKm = laps * cyc + svc.km;
    else { svc = s.services[0]; nextKm = (laps + 1) * cyc + svc.km; }
    const remainKm = nextKm - car.km;
    const monthsByKm = remainKm / car.kmMonth;
    let dueDate = new Date(); dueDate.setMonth(dueDate.getMonth() + Math.floor(monthsByKm));
    let byTime = null;
    if (car.lastService) {
      byTime = new Date(car.lastService + "-01"); byTime.setMonth(byTime.getMonth() + s.interval.months);
      if (byTime < dueDate) dueDate = byTime;
    }
    const prevKm = nextKm - s.interval.km;
    const progress = Math.min(1, Math.max(0, (car.km - prevKm) / s.interval.km));
    const daysLeft = Math.round((dueDate - new Date()) / 86400000);
    const level = remainKm <= 0 || daysLeft <= 0 ? "crit" : (remainKm <= 1500 || daysLeft <= 30) ? "warn" : "good";
    return { s, svc, nextKm, remainKm, dueDate, byTime, progress, daysLeft, level };
  }
  g.TipulitEngine = { gridShift, next };
})(typeof window !== "undefined" ? window : globalThis);
