# Tipulit: notes for agents

Hebrew RTL PWA that tracks a car's condition and maintenance schedule in Israel. Read `HANDOFF.md` for product context and `DESIGN.md` for the design system before changing UI.

## Keep content and design apart
- Visual rules live only in `app/styles/tokens.css` (all literals), `app/styles/app.css` (app) and `app/welcome/welcome.css` (landing).
- In `app/index.html` and `app/welcome/index.html` use classes. No `<style>` blocks, no inline `style=""` except runtime custom properties (`--i`, `--drag`, …), no colours or font names, no `el.style.foo = …` (use classes or `setProperty("--x", …)`).
- New UI: reuse existing components and utilities; if you need a new look, add a class in the stylesheet first.
- Run `node scripts/check-design.mjs` before committing. The build fails if it reports problems.

## Build and checks
- `node scripts/check-design.mjs && node scripts/validate.mjs && node scripts/build-app-data.mjs && node scripts/test-lookup.mjs && node scripts/test-engine.mjs && node scripts/build-site.mjs`
- `build-site.mjs` writes the deployable site to `site/` (or `SITE_OUT`), including `styles/` and `welcome/`. Netlify publishes `site/` from `main`.
- Maintenance data: edit `scripts/build_schedules.py` rules and regenerate; never hand-edit generated schedules.

## Garage dashboard is modular
- `app/garage/core.js` holds helpers, state, screens, demo data and the module registry. Features live in `app/garage/modules/*.js`; each calls `Garage.register({ id, name, desc, core, groups, tab, show, hide, state, load, demo })`.
- Modules talk only through the `Garage` object (`G.on(id)`, `G.call(name)`, `G.addAction("appt"|"car", …)`, `G.addTimeline(…)`). A new feature is a new module plus its markup in `app/garage/index.html` tagged `data-module="<id>"`; don't wire it into other modules' code.
- Which modules a garage sees: `garage_profiles.modules`, or by default the professions it is licensed for (`data/garages.json`, groups in core.js).

