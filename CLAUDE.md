# Tipulit: notes for agents

Hebrew RTL PWA that tracks a car's condition and maintenance schedule in Israel. Read `HANDOFF.md` for product context and `DESIGN.md` for the design system before changing UI.

## Keep content and design apart
- Visual rules live only in `app/styles/tokens.css` (all literals), `app/styles/app.css` (app) and `app/welcome/welcome.css` (landing).
- In `app/index.html` and `app/welcome/index.html` use classes. No `<style>` blocks, no inline `style=""` except runtime custom properties (`--i`, `--drag`, …), no colours or font names, no `el.style.foo = …` (use classes or `setProperty("--x", …)`).
- New UI: reuse existing components and utilities; if you need a new look, add a class in the stylesheet first.
- Run `node scripts/check-design.mjs` before committing. The build fails if it reports problems.

## Build and checks
- `node scripts/check-design.mjs && node scripts/validate.mjs && node scripts/build-app-data.mjs && node scripts/test-lookup.mjs && node scripts/build-site.mjs`
- `build-site.mjs` writes the deployable site to the repo root (or `SITE_OUT`), including `styles/` and `welcome/`.
- Maintenance data: edit `scripts/build_schedules.py` rules and regenerate; never hand-edit generated schedules.
