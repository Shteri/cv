# DESIGN.md — טיפולית (Tipulit)

Design source of truth for Tipulit: the app (`app/index.html`) and the landing page (`app/welcome/index.html`) share one system, called "night drive". Agents and people building any screen, page or asset read this first. Format follows the DESIGN.md convention (Google Stitch / awesome-design-md). Tokens are written as `{group.name}` and map to the CSS custom properties in `app/styles/tokens.css`, the single source for both.

## Overview

Tipulit is a Hebrew, right-to-left, mobile-first product for car owners in Israel. Its main job is **tracking the car's condition**: what was replaced, what is approaching, what is overdue and what is unknown, item by item. Next to that it tells the driver what the next service is, what it includes according to the importer's schedule, and what to verify at the garage.

The look is a night drive: graphite surfaces, light as the material (soft glows, a scan beam, glass on floating chrome), and one accent taken from the product's own subject, the yellow of an Israeli licence plate. Hierarchy comes from information design (count tiles, status dots, one big tabular number) rather than decoration. Motion is there to explain state: things arrive, filters morph, sheets slide and can be swiped away.

**Key characteristics**
- Dark and light are both first-class and follow the system setting. Grey family is cool and neutral, never warm.
- One accent, `{colors.accent}` (#F7C948), used as a **fill** (primary buttons, active tab, selected chip, toggles, next-service ring). Text in the accent colour uses `{colors.accent-text}`, which is yellow in dark and a dark amber in light, so it stays readable.
- The licence plate is a first-class element: yellow, 2–3px near-black border, blue "IL" tab, Rubik 700, always LTR.
- Semantic colours (good / warn / crit / unknown) only mark state and are always paired with text.
- Typography: IBM Plex Sans Hebrew for text, Rubik for display and numbers. Numbers are always tabular.
- The next-service card is the one graphite hero card, identical in both themes.

## Colors

### Accent
- **Accent** `{colors.accent}` #F7C948, text on it `{colors.accent-ink}` #101214.
- **Accent soft** `{colors.accent-soft}` light #FCEFC7 / dark #3A3014: "replace" chips, tags, halo on the next timeline dot.
- **Accent text** `{colors.accent-text}` light #7A5A00 / dark #F7C948: links and accent-coloured text.
- **Plate** #F7C948 with ink #101214 and IL tab #1747A8. Plate colours do not change with the theme.

### Surfaces (light / dark)
- **Ground** `{colors.ground}` #F1F2F4 / #08090B.
- **Surface** `{colors.surface}` #FFFFFF / #14171C: cards, sheets, fields.
- **Surface 2** `{colors.surface-2}` #ECEEF1 / #1C2027: inset panels, count tiles inside cards, segmented control track.
- **Surface 3** `{colors.surface-3}` #E2E5EA / #252A32: toggle track, pressed rows.
- **Line** `{colors.line}` #DDE0E5 / #262B33: 1px dividers, 1.5px borders.
- **Hero card** #111418 with a soft yellow glow in the corner, text #F3F4F6, in both themes.

### Text (light / dark)
- **Ink** `{colors.ink}` #0C0F12 / #F3F4F6. **Muted** `{colors.muted}` #555C66 / #9BA2AC. **Faint** `{colors.faint}` #868D97 / #626A75 (unknown values, secondary meta only).

### Semantic (light / dark, with soft backgrounds)
- **Good** #148A55 / #3FD58B: done, fine, remaining life.
- **Warn** #9A6700 / #F0B04A: approaching (≤3,000 km or ≤45 days), data caveats.
- **Crit** #C8352B / #FF6B5E: overdue, inline errors. An overdue dot gets a slow pulsing halo.
- **Unknown**: faint grey dot and "?".

## Logo
- Wordmark only: lowercase **tipulit** in Unbounded 600, tracking -0.03em, followed by a square full stop in plate yellow (`{colors.accent}`). No Hebrew in the logo and no letter mark.
- One implementation for every surface: `app/styles/brand.css`, markup documented at the top of that file. Size with `--brand-size` (app 1.25rem, landing nav 1.4rem); the full stop scales with it.
- `{font.brand}` (Unbounded) is for the wordmark only, never UI text.
- App icon: a geometric "t" in off-white with the same yellow square, on the graphite hero colour (#111418). Drawn as shapes in `scripts/build-site.mjs`, so it renders without any font.
- The product name in running Hebrew copy stays "טיפולית"; page titles and the installed-app name use "Tipulit".

## Typography
- **IBM Plex Sans Hebrew** 400/500/600: body, labels, buttons, notes.
- **Rubik** 500–800: headings, big numbers, the plate, odometer digits, counts.
Both are Hebrew-native; never substitute a Latin-only face.

| Token | Size | Weight | Face | Tracking | Use |
|---|---|---|---|---|---|
| `{type.display}` | 2.8rem (app) / clamp up to 5.4rem (landing) | 800 | Rubik | -0.04em | next-service km, landing hero |
| `{type.h1}` | 1.9rem | 700 | Rubik | -0.03em | screen titles |
| `{type.h2}` | 1.3rem | 700 | Rubik | -0.015em | sheet titles |
| `{type.h3}` | 1.08rem | 600 | Rubik | -0.01em | card titles |
| `{type.body}` | 16px | 400 | Plex | 0 | running text |
| `{type.small}` | 14px | 400 | Plex | 0 | meta, notes |
| `{type.label}` | 12.8px | 500 | Plex | 0 | eyebrows (sentence case, no uppercase tracking) |
| `{type.plate}` | 17px (mini) / 1.7rem (input) | 700 | Rubik | +0.06–0.1em | licence plate, LTR |

Numbers use `font-variant-numeric: tabular-nums` and `Intl.NumberFormat("he-IL")`; currency is prefixed with ₪. Copy is plain Hebrew, second person, no exclamation marks; loading states end with an ellipsis (…).

## Layout
- App: single column, `max-width: 480px`, 16px gutter, 18px between cards, bottom padding 112px to clear the floating nav.
- Landing: `max-width: 1280px`, 16px gutter on phones and 40px from 768px.
- Base unit 4px. Screens are flex columns with `gap`, not per-element margins.

## Elevation & depth
- Cards: 1px line border + `{shadow.card}` (a soft neutral drop) + a 1px inner top highlight (`{edge}`).
- The hero card and the primary button carry a yellow-tinted shadow; nothing else glows.
- Floating chrome (bottom nav, landing FAB, landing console) is frosted glass: translucent surface + `backdrop-filter: blur(20px) saturate(160%)`, with a solid fallback under `prefers-reduced-transparency`. This is a web approximation, not Apple's Liquid Glass.
- Sheets slide up over a 50% scrim, radius 26px at the top, with a grab handle.

## Shapes
| Token | Radius | Use |
|---|---|---|
| `{radius.card}` | 22px (app), 28px (landing panels) | cards, hero card |
| `{radius.control}` | 14px | buttons, segmented control, banners |
| `{radius.field}` | 12px | inputs, selects, thumbnails |
| `{radius.pill}` | 999px | chips, status pills, action chips, toggles, toast |
| `{radius.plate}` | 8px (mini) / 10px (input) | licence plate |

## Components
- **Instrument cluster** (home, `.cluster`): a graphite panel, the same in both themes, with two dials. The next-service dial is a progress ring with km to go in the centre. The condition dial is a ring split into status arcs (overdue, approaching, fine, unknown) with the number of items that need attention in the centre. The odometer and test expiry sit in its footer. Both dials are buttons: next service opens the timeline, condition opens the car screen.
- **Dock** (`.dock`): four quick actions (log a service, update km, invoice, garage) as equal tiles with a Phosphor icon on a yellow square.
- **Attention rail** (`.attn-rail`, `.attn-card`): swipeable cards for overdue and approaching items, with a status strip, the due km or month and a remaining-life bar. When nothing needs attention, a green `.all-good` line replaces it; with no records at all, the start card does.
- **Next-service card** (`.next-card`): km and status, the items to replace as chips, the price folded away, then "מה לוודא במוסך".
- **Car screen**: sticky filter tabs with counts (`.tabs`, `.tab`), then a two-column tile grid (`.tiles`, `.tile`), one tile per item, with a top strip in the status colour, the due value and a remaining-life bar.
- **Bottom nav**: a floating glass bar 12px from the edges; four tabs (בית, הרכב, ציר טיפולים, אני); the active tab gets a surface-2 pill and its icon sits on a yellow rounded square.
- **Condition summary** (home, above the next-service card): four count tiles (באיחור, מתקרב, בסדר, לא ידוע) and up to three rows that need attention. The overdue tile turns crit-soft when above zero.
- **Condition row**: 10px status dot, item name with category, one-line history, due km or month on the left in Rubik.
- **Next-service hero card**: graphite, status pill ("בזמן" / "מתקרב" / "הגיע הזמן לטיפול"), big km, a 112px ring filled in yellow (warn / crit colours when late), what the service includes, price tiles, a yellow primary action.
- **Primary button**: yellow fill, dark text, light sweep on hover, springy press (`scale(.97)`); busy state pulses its label.
- **Secondary button**: surface fill, 1.5px line border. **Ghost button**: muted text.
- **Chip**: pill, 1.5px border; selected = yellow fill.
- **Segmented control**: surface-2 track, the selected segment is a raised surface pill.
- **Toggle**: surface-3 track, yellow when on, springy knob.
- **Checklist row**: custom 22px yellow checkbox with an animated tick; a checked label is struck through.
- **Timeline item**: 28px dot + card; done = good, next = yellow dot with a breathing halo and a yellow border.
- **Odometer**: six small surface tiles, LTR, Rubik 700.
- **Sheet**: slides up; drag the handle or title row down to dismiss (over 110px closes, less snaps back).
- **Toast**: ink pill that springs up from below the nav, `aria-live="polite"`, 2.2s.
- **Banner**: warn-soft box, 14px radius.

## Motion
- Only transform, opacity, colour, border and shadow animate. Durations 200–500ms; easing `cubic-bezier(.16, 1, .3, 1)`, and a spring `cubic-bezier(.34, 1.56, .64, 1)` for presses, toggles and chevrons.
- Screens fade and rise 10px when shown. Timeline items open with a short slide.
- Taps that change something send a 6ms vibration where supported (Android).
- `prefers-reduced-motion: reduce` switches off all animation and transitions.

## Landing page specifics
- The hero holds a live, landing-scale "מצב הרכב" console with sample data (labelled "נתוני דוגמה"). On desktop it stays pinned while scroll steps highlight overdue, remaining life, unknown and test; on phones the steps are a swipe deck.
- Models: a search field (Hebrew or English names) plus make filter pills and a paged grid. The catalogue is generated by `scripts/build-site.mjs` from `data/schedules/` into an inline JSON block, so it scales to hundreds of models without hand edits. Make logos come from Simple Icons (`app/welcome/logos/`); a make without a logo shows its first letter.
- Icons are Phosphor (regular), inlined at build time from `app/welcome/icons/`.
- The plate form hands off to the app with `?plate=<digits>`, which prefills the add-car step.

## Design in code (how the look survives product changes)

The design lives in three stylesheets; markup and scripts only carry content, state and data.

| File | Holds | May contain |
|---|---|---|
| `app/styles/tokens.css` | every colour, font, radius and easing, light and dark | literals (the only file that may) |
| `app/styles/brand.css` | the logo lockup, shared by both pages | `var(--token)` only |
| `app/styles/app.css` | app components + a short list of layout utilities | `var(--token)` only |
| `app/welcome/welcome.css` | landing components | `var(--token)` only |
| `app/index.html`, `app/welcome/index.html` | markup, copy, data, behaviour | classes, and `style="--x: …"` for runtime data |

Rules, enforced by `node scripts/check-design.mjs` (runs first in the Netlify build and in the GitHub workflow, and fails the build):
1. No literal colours or font names outside `tokens.css`. Need a new shade? Add a token, or derive it with `color-mix(in srgb, var(--token) 40%, transparent)`.
2. No `<style>` blocks in HTML. No inline `style=""` except custom properties that pass data to CSS (`--i`, `--k`, `--r`, `--s`, `--c`, `--n`, `--h`, `--x`, `--y`, `--mx`, `--my`, `--rx`, `--ry`, `--p`, `--drag`, `--vt`). New runtime properties are added to the list in the checker and here.
3. JavaScript changes the look only by toggling classes or calling `el.style.setProperty("--name", value)`.
4. SVG colour comes from CSS classes; `fill`/`stroke` attributes may only be `none` or `currentColor`. Geometry (x, y, r, dasharray) may be computed in JS.
5. Every `var(--x)` must resolve to a token, a property set in the same stylesheet, or a runtime property.
6. Every class written in markup or JS templates must exist in the page's stylesheet (behaviour-only hooks are listed in the checker).

In practice: a new screen or feature reuses the existing components and utilities (`.card`, `.stack`, `.row`, `.btn.*`, `.chip`, `.status.*`, `.g-*`, `.grow`, …). If something new is needed, add a class to the stylesheet first, then use it. Changing the palette, fonts or radii is a `tokens.css` edit and nothing else.

## Do's and don'ts
- Do keep one accent. State is expressed with the semantic set, never a second brand colour.
- Do show the plate as a plate.
- Do put condition first: what needs attention, then the next service, then detail.
- Do use real data or clearly labelled examples ("נתוני דוגמה"); never invent verified-looking numbers.
- Do provide hover, pressed, focus-visible and busy states on every control.
- Don't use yellow for text on light backgrounds; use `{colors.accent-text}`.
- Don't add a fifth nav tab; secondary destinations open from cards.
- Don't render cards inside cards; use dividers and surface-2 insets.
- Don't rely on colour alone: pair every status colour with text.

## Responsive behavior
- App designed at 400px, verified at 360–480px; above 480px the column is centred.
- Touch targets ≥ 44px; chips ≥ 36px.
- Sheets cap at 92vh and scroll internally with `overscroll-behavior: contain`.
- Text containers use `min-width: 0` and `overflow-wrap: anywhere`.
- The nav, sheets and the landing FAB add safe-area insets to their own padding.

## Known gaps
- App icons in the bottom nav are still hand-drawn 2px outline SVGs; move them to Phosphor like the landing page.
- Onboarding illustrations are simple inline SVGs; replace with real screenshots or generated art when available.
- Community price and garage data are placeholders until the backend exists; keep the "נתוני דוגמה" label until then.
