// Hologram car: a procedurally built sedan wireframe (CAD-style contour lines), drawn on a 2D canvas.
// Units are metres. x runs along the car (front +), y is up, z is across. Deterministic, no WebGL needed.
window.Holo = (function () {
  const lerp = (a, b, t) => a + (b - a) * t;
  // piecewise-linear lookup with smoothstep between keys
  function curve(keys, x) {
    if (x <= keys[0][0]) return keys[0][1];
    for (let i = 1; i < keys.length; i++) if (x <= keys[i][0]) { const [x0, y0] = keys[i - 1], [x1, y1] = keys[i]; let t = (x - x0) / (x1 - x0); t = t * t * (3 - 2 * t); return lerp(y0, y1, t); }
    return keys[keys.length - 1][1];
  }
  const L = 2.33;                                             // half length
  const belt = [[-L, 0.6], [-2.25, 0.86], [-2.0, 0.98], [-1.6, 0.99], [0.0, 0.96], [0.98, 0.93], [1.6, 0.83], [2.15, 0.72], [L, 0.52]];
  const roof = [[-1.62, 0.99], [-1.15, 1.3], [-0.7, 1.42], [-0.1, 1.44], [0.45, 1.3], [0.98, 0.95]];
  const halfW = [[-L, 0.76], [-2.0, 0.9], [-1.0, 0.93], [1.0, 0.93], [1.9, 0.88], [L, 0.72]];
  const bottom = 0.2;
  function section(x, n) {                                    // closed ring of points around the body at station x
    const w = curve(halfW, x), hb = curve(belt, x), inCab = x > -1.62 && x < 0.98;
    const hr = inCab ? curve(roof, x) : hb, wr = inCab ? w * 0.74 : w * 0.9;
    const prof = [[0, bottom], [w * 0.86, bottom], [w, 0.38], [w, 0.62], [w * 0.97, hb - 0.03], [w * 0.88, hb]];
    if (inCab && hr > hb + 0.05) prof.push([wr, lerp(hb, hr, 0.9)], [wr * 0.82, hr]); else prof.push([w * 0.6, hb + 0.01]);
    prof.push([0, inCab && hr > hb + 0.05 ? hr + 0.01 : hb + 0.015]);
    const half = prof.map(([z, y]) => [x, y, z]);
    return half.concat(half.slice(0, -1).reverse().map(([a, b, c]) => [a, b, -c]));
  }
  const ARCH = [[1.41, 0.34], [-1.41, 0.34]];
  const inArch = v => ARCH.some(([ax, ay]) => Math.hypot(v[0] - ax, v[1] - ay) < 0.43 && Math.abs(v[2]) > 0.55);
  function cut(pts) { const out = []; let cur = []; for (const v of pts) { if (inArch(v)) { if (cur.length > 1) out.push(cur); cur = []; } else cur.push(v); } if (cur.length > 1) out.push(cur); return out; }
  function build() {
    const lines = [], N = 46;
    const xs = []; for (let i = 0; i <= N; i++) xs.push(-L + 0.02 + (2 * L - 0.04) * i / N);
    const rings = xs.map(x => section(x, 0));
    rings.forEach((r, i) => { if (i % 3 === 0 || i === N) cut(r).forEach(pts => lines.push({ pts, kind: "ring" })); });
    const m = rings[0].length;
    for (let j = 0; j < m; j++) cut(rings.map(r => r[Math.min(j, r.length - 1)])).forEach(pts => lines.push({ pts, kind: "long" }));
    // arch outlines
    for (const [ax, ay] of ARCH) for (const sz of [0.9, -0.9]) { const p = []; for (let k = 0; k <= 24; k++) { const a = k / 24 * Math.PI; p.push([ax + Math.cos(a) * 0.45, ay + Math.sin(a) * 0.45, sz * 0.985]); } lines.push({ pts: p, kind: "wheel" }); }
    // wheels: tyre (two rings) + rim + spokes, at both axles and sides
    const wheels = [];
    for (const ax of [1.41, -1.41]) for (const sz of [0.82, -0.82]) {
      const R = 0.34, r = 0.22, ring = (rad, z) => { const p = []; for (let k = 0; k <= 36; k++) { const a = k / 36 * Math.PI * 2; p.push([ax + Math.cos(a) * rad, R + Math.sin(a) * rad, z]); } return p; };
      lines.push({ pts: ring(R, sz), kind: "wheel" }, { pts: ring(R, sz - Math.sign(sz) * 0.2), kind: "wheel" }, { pts: ring(r, sz), kind: "rim" });
      for (let k = 0; k < 5; k++) { const a = k / 5 * Math.PI * 2; lines.push({ pts: [[ax, R, sz], [ax + Math.cos(a) * r, R + Math.sin(a) * r, sz]], kind: "rim" }); }
      wheels.push([ax, R, sz]);
    }
    // parts inside the car, lit one by one
    const box = (x0, x1, y0, y1, z0, z1) => { const c = [[x0, y0, z0], [x1, y0, z0], [x1, y1, z0], [x0, y1, z0], [x0, y0, z1], [x1, y0, z1], [x1, y1, z1], [x0, y1, z1]]; return [[0, 1, 2, 3, 0], [4, 5, 6, 7, 4], [0, 4], [1, 5], [2, 6], [3, 7]].map(ix => ix.map(i => c[i])); };
    const parts = {
      engine: box(1.25, 1.95, 0.42, 0.82, -0.36, 0.36),
      brakes: [[1.41, 0.34, 0.66], [1.41, 0.34, -0.66], [-1.41, 0.34, 0.66], [-1.41, 0.34, -0.66]].map(([x, y, z]) => { const p = []; for (let k = 0; k <= 30; k++) { const a = k / 30 * Math.PI * 2; p.push([x + Math.cos(a) * 0.17, y + Math.sin(a) * 0.17, z]); } return p; }),
      cabin: box(0.55, 0.85, 0.75, 0.92, -0.45, 0.45),
      tires: [[1.41, 0.82], [1.41, -0.82], [-1.41, 0.82], [-1.41, -0.82]].map(([x, z]) => { const p = []; for (let k = 0; k <= 36; k++) { const a = k / 36 * Math.PI * 2; p.push([x + Math.cos(a) * 0.35, 0.34 + Math.sin(a) * 0.35, z]); } return p; })
    };
    return { lines, wheels, parts, anchors: { engine: [1.6, 0.85, 0], brakes: [1.41, 0.34, 0.82], tires: [-1.41, 0.34, 0.82], cabin: [0.7, 0.92, 0] } };
  }
  function project(v, p) {
    const cy = Math.cos(p.yaw), sy = Math.sin(p.yaw), cp = Math.cos(p.pitch), sp = Math.sin(p.pitch);
    const x = v[0], y = v[1] - 0.7, z = v[2];
    const x1 = x * cy - z * sy, z1 = x * sy + z * cy;
    const y2 = y * cp - z1 * sp, z2 = y * sp + z1 * cp;
    const d = p.dist / (p.dist + z2);
    return [p.cx + x1 * p.scale * d, p.cy - y2 * p.scale * d, z2];
  }
  function stroke(ctx, pts, p, rgb, a, w) {
    ctx.strokeStyle = `rgba(${rgb}, ${a})`; ctx.lineWidth = w; ctx.beginPath();
    pts.forEach((v, i) => { const q = project(v, p); i ? ctx.lineTo(q[0], q[1]) : ctx.moveTo(q[0], q[1]); }); ctx.stroke();
  }
  function draw(ctx, car, p) {
    ctx.clearRect(0, 0, ctx.canvas.width, ctx.canvas.height);
    ctx.lineJoin = "round"; ctx.lineCap = "round";
    const base = p.color || "247, 201, 72", A = p.alpha == null ? 1 : p.alpha;
    // ground: elliptical rings under the car
    for (let k = 1; k <= 3; k++) { const g = []; for (let i = 0; i <= 60; i++) { const a = i / 60 * Math.PI * 2; g.push([Math.cos(a) * (1.6 + k * 0.55), 0, Math.sin(a) * (1.0 + k * 0.4)]); } stroke(ctx, g, p, base, 0.12 * A / k, 1.5); }
    const reveal = p.reveal == null ? 1 : p.reveal;           // 0..1 builds the car from the rear to the front
    const scanX = p.scan == null ? null : lerp(-2.6, 2.6, p.scan);
    for (const pass of [0, 1]) for (const ln of car.lines) {
      const pts = ln.pts.filter(v => (v[0] + L) / (2 * L) <= reveal + 0.001);
      if (pts.length < 2) continue;
      const k0 = ln.kind === "long" ? 0.5 : ln.kind === "ring" ? 0.42 : ln.kind === "rim" ? 0.6 : 0.75;
      // per segment, so the scan band only lights what it passes over
      for (let i = 1; i < pts.length; i++) {
        let k = k0; const mx = (pts[i][0] + pts[i - 1][0]) / 2;
        if (scanX != null) k += Math.max(0, 1 - Math.abs(mx - scanX) / 0.3) * 1.3;
        if (pass === 0) stroke(ctx, [pts[i - 1], pts[i]], p, base, 0.12 * k * A, 7);
        else stroke(ctx, [pts[i - 1], pts[i]], p, "255, 244, 214", Math.min(1, 0.6 * k) * A, 1.4);
      }
    }
    for (const [name, segs] of Object.entries(car.parts)) {
      const lit = (p.parts || {})[name] || 0; if (!lit) continue;
      const rgb = (p.partColor || {})[name] || base;
      for (const s of segs) { stroke(ctx, s, p, rgb, 0.35 * lit * A, 10); stroke(ctx, s, p, rgb, 0.95 * lit * A, 2.4); }
    }
  }
  return { build, draw, at: project };
})();
