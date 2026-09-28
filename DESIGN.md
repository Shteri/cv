# DESIGN.md — טיפולית (Tipulit)

Design source of truth for the Tipulit app. Agents and people building any screen, page or asset for this product read this first. Format follows the DESIGN.md convention (Google Stitch / awesome-design-md). Tokens are written as `{group.name}` and map 1:1 to the CSS custom properties in `app/index.html`.

## Overview

Tipulit is a Hebrew, right-to-left, mobile-first product UI for car owners in Israel. Its job is practical: tell the driver what the next service is, what it includes according to the importer's book, what it should cost, and what to verify at the garage. The visual language is a calm workshop: cool light-grey ground, white cards only where elevation carries meaning, one desaturated blue accent, and a single subject-specific color, the yellow of an Israeli licence plate.

The page is scanned and operated, not read top to bottom. Hierarchy comes from information design (a status pill, a progress ring, a big tabular number) more than from decoration. Nothing animates for show; motion is limited to hover, press and one soft pulse on a busy control.

**Key characteristics**
- Ground `{colors.ground}` (#F3F5F8) with white cards `{colors.surface}` (#FFFFFF); grey family is cool (blue-tinted), never warm.
- One accent, `{colors.accent}` (#215FBA), saturation kept under 75%. Shadows are tinted with the accent hue.
- The licence plate is a first-class element: yellow `{colors.plate}` (#F7C948), black 2px border, blue "IL" tab, Rubik 700, always LTR.
- Semantic colors (good / warn / crit) are separate from the accent and only mark state.
- Typography: Heebo for text, Rubik for display and numbers. Numbers are always tabular.
- Cards are rounded 18px; inner elements 12–14px; chips and status pills are full pills.
- Every screen works at 400px wide with a 16px gutter and a fixed bottom navigation with four tabs: בית, הרכב, ציר טיפולים, אני.

## Colors

### Brand & accent
- **Accent** `{colors.accent}` #215FBA — primary buttons, active nav tab, progress ring at rest, links. Press/hover deepens to `{colors.accent-deep}` #1A4C95.
- **Accent soft** `{colors.accent-soft}` #E4ECF8 — "replace" chips, selected chip background, ring halo, avatar background.
- **Accent ink** `{colors.accent-ink}` #FFFFFF — text on accent.
- **Plate** `{colors.plate}` #F7C948 with `{colors.plate-ink}` #1A1A1A and the IL tab #1747A8 — used only for the licence plate and the onboarding plate illustration. Never as a general accent.

### Surface
- **Ground** `{colors.ground}` #F3F5F8 — page background.
- **Surface** `{colors.surface}` #FFFFFF — cards, sheets, bottom nav.
- **Surface 2** `{colors.surface-2}` #EAF0F7 — inset panels (price tiles, inspect chips, onboarding art), ring track.
- **Line** `{colors.line}` #D9E0E8 — 1px dividers and 1.5px input/chip borders.

### Text
- **Ink** `{colors.ink}` #15202B — body and headings.
- **Muted** `{colors.muted}` #5E6B78 — secondary text, eyebrows, notes. Contrast on ground ≥ 4.5:1.

### Semantic (state only, never decoration)
- **Good** `{colors.good}` #1E8A55 on `{colors.good-soft}` #DFF3E8 — "everything fine", done timeline dots, reviewed status.
- **Warn** `{colors.warn}` #B96E00 on `{colors.warn-soft}` #FBEFD6 — approaching, draft data banner, long-interval item within range.
- **Crit** `{colors.crit}` #C4383A on `{colors.crit-soft}` #FBE3E3 — overdue, inline errors.

### Dark theme
Same roles, remapped: ground #0E141B, surface #172029, surface-2 #1F2A35, ink #EDF2F7, muted #9AA8B6, line #2B3844, accent #6FA3EA (accent-ink #0B1420, accent-soft #1B2D45, accent-deep #8CB6F0), good #4CC183 / #163526, warn #F0B04A / #3A2C10, crit #F07173 / #3F1D1E. Plate colors do not change. `color-scheme: dark` is set wherever the dark palette applies.

## Typography

### Font family
- **Heebo** (Google Fonts) — body, labels, buttons, notes. Weights 400, 500, 700. Fallback: "Segoe UI", Arial, sans-serif.
- **Rubik** (Google Fonts) — headings, big numbers, the plate, odometer digits. Weights 500, 600, 700. Fallback: Heebo.
Both are Hebrew-native. Do not substitute Inter, Geist or other Latin-only faces; Hebrew glyphs would fall back and the page would look broken.

### Hierarchy
| Token | Size | Weight | Face | Tracking | Use |
|---|---|---|---|---|---|
| `{type.display}` | 36px | 700 | Rubik | -0.02em | next-service km on home |
| `{type.h1}` | 28px | 600 | Rubik | -0.015em | screen titles, car name on home |
| `{type.h2}` | 20px | 600 | Rubik | 0 | card titles |
| `{type.h3}` | 17px | 600 | Rubik | 0 | section titles inside cards |
| `{type.body}` | 16px | 400 | Heebo | 0 | running text, list items |
| `{type.small}` | 14px | 400 | Heebo | 0 | meta, notes, hints |
| `{type.eyebrow}` | 12px | 500 | Heebo | +0.06em, uppercase | section labels |
| `{type.chip}` | 11.5px | 600 | Heebo | 0 | action chips, tags |
| `{type.plate}` | 17px | 700 | Rubik | +0.05em | licence plate, LTR |

### Principles
- Numbers are always `font-variant-numeric: tabular-nums` and formatted with `Intl.NumberFormat("he-IL")`; currency is prefixed with ₪.
- Headings use `text-wrap: balance`. Body line-height 1.5, headings 1.25.
- Copy is sentence case, active voice, second person, no exclamation marks. Loading states end with an ellipsis (…).
- Hebrew text is RTL; plates, engine codes and part numbers are wrapped LTR.

## Layout

### Spacing
Base unit 4px. Common steps: 6, 8, 10, 12, 16, 18, 20. Screen padding 20px top, 16px sides, 96px bottom (clears the nav). Card padding 18px. Gap between stacked cards 16–20px; inside cards 8–14px.

### Grid & container
Single column, `max-width: 480px`, centered. Screens are `display:flex; flex-direction:column` with `gap`, never per-element margins. Two-up rows (price tiles, button pairs) use flex with `gap` 8–10px and wrap at narrow widths.

### Whitespace
Let the next-service card breathe; everything else is compact. Lists inside cards use 1px dividers and 10–12px vertical padding instead of extra cards.

## Elevation & depth
- `{shadow.card}`: `0 10px 28px rgba(33,95,186,.10), 0 1px 2px rgba(33,95,186,.06)` — cards on the ground only.
- `{shadow.button}`: `0 2px 6px rgba(33,95,186,.18)`; hover `0 6px 16px rgba(33,95,186,.25)`.
- Timeline cards use a 1.5px border instead of shadow; the "next" card uses the accent border and a 5px accent-soft halo on its dot.
- Sheets slide from the bottom over a 45% black scrim, radius 22px on the top corners.
- Onboarding art gets one quiet radial tint from accent-soft into surface-2. No gradients elsewhere.

## Shapes
| Token | Radius | Use |
|---|---|---|
| `{radius.card}` | 18px | cards |
| `{radius.control}` | 14px | primary/secondary buttons, empty-state boxes |
| `{radius.field}` | 12px | inputs, selects, avatar (rounded square, not circle) |
| `{radius.inner}` | 10–12px | receipt thumbnails, price tiles |
| `{radius.chip}` | 6px | action chips, tags |
| `{radius.pill}` | 999px | filter chips, status pills, toasts, toggles |
| `{radius.plate}` | 8px | licence plate |

## Components
- **Bottom nav**: four tabs (בית, הרכב, ציר טיפולים, אני), 24px outline icons + 11.5px label, active tab in accent. Fixed, respects `env(safe-area-inset-bottom)`.
- **Condition row**: 10px status dot (good / warn / crit / line for unknown), item name with category, one-line history ("הוחלף ב-45,000 ק"מ, ינואר 2026"), due km on the left in Rubik. Unknown rows show "?" and the schedule's next grid km.
- **Count tiles**: four surface-2 tiles (באיחור, מתקרב, בסדר, לא ידוע) with a Rubik number in the semantic color; used on home and on the car screen.
- **Document grid**: four square thumbnails per row with a date label strip; tapping opens the record.
- **Primary button**: accent fill, 14px radius, 14px/18px padding, 600 weight; busy state keeps the width and pulses the label.
- **Secondary button**: surface fill, 1.5px line border; hover fills surface-2.
- **Ghost button**: muted text, no fill; used for "back" and tertiary actions.
- **Licence plate**: see Colors; input variant is the same plate with a centered 1.6rem Rubik field.
- **Odometer**: six ink tiles with ground-colored digits, LTR.
- **Status pill**: 12.8px 600 text with a 7px dot, semantic colors only.
- **Progress ring**: 108px, 10px stroke, track surface-2, fill accent (good) or the semantic color.
- **Action chip**: החלפה (accent-soft), בדיקה (surface-2), ניקוי/סבב/כיוון (warn-soft).
- **Timeline item**: 28px dot + card; done = good, next = accent with halo and open by default.
- **Checklist row**: 22px native checkbox, label is the hit target, note in small muted.
- **Price tiles**: two surface-2 tiles side by side, median in Rubik 600, range and sample size in small muted.
- **Garage row**: name + "דיווחת" tag, meta line (type, city, reports, % would return), average price on the left.
- **Sheet**: bottom sheet with title row and a ghost close button, fields stacked 14px apart, primary action last.
- **Toast**: ink pill on ground text, bottom 90px, `aria-live="polite"`, 2.2s.
- **Banner**: warn-soft box, 12px radius, for data caveats and upcoming long-interval items.
- **Empty state**: dashed line box with bold headline, one explanatory sentence and one secondary action.

## Do's and don'ts

### Do
- Keep one accent. State is expressed with the semantic set, never with a second brand color.
- Show the plate as a plate. It is the product's identity element.
- Put the summary before the detail: next service first, items second, sources last.
- Use real data or clearly labelled examples ("נתוני דוגמה"); never invent verified-looking numbers.
- Provide hover, pressed, focus-visible and busy states on every control.
- Write in plain Hebrew a garage customer uses; expand jargon the first time.

### Don't
- Don't use gradients, glassmorphism, grain or purple-blue hero blocks. This is a tool, not a landing page.
- Don't add a fifth nav tab; secondary destinations (garages, checklist) open from cards and go back with the browser history.
- Don't render cards inside cards. Use dividers and inset surface-2 panels.
- Don't use warm greys, pure black, or a saturated blue.
- Don't show a dashboard-style number wall; one big number per screen.
- Don't rely on color alone: pair every semantic color with text.

## Responsive behavior
- Designed at 400px; verified at 360–480px. Above 480px the column is centered on the ground.
- Touch targets ≥ 44px; chips ≥ 36px tall with 8px gaps.
- Sheets cap at 92vh and scroll internally with `overscroll-behavior: contain`.
- Text containers use `min-width: 0` and `overflow-wrap: anywhere`; long garage names and notes wrap, never clip.
- The bottom nav and sheets add the safe-area insets to their own padding.

## Motion
- Transitions 120–200ms on transform, background-color, border-color, box-shadow, opacity only. Never `transition: all`.
- Press: `scale(.985) translateY(1px)`. Busy: 1.2s opacity pulse. Toast: 200ms fade.
- `prefers-reduced-motion: reduce` disables all transitions.

## Known gaps
- No landing page yet; when one is built use `design-taste-frontend` and this palette, not a new one.
- Icons are hand-drawn 2px outline SVGs; if the set grows, adopt Phosphor at 1.5–2px stroke for consistency.
- Community price and garage data are placeholders until the backend exists; keep the "נתוני דוגמה" label until then.
