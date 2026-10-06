---
name: design-md
description: Use a DESIGN.md design-system document (Google Stitch format, curated by VoltAgent/awesome-design-md) as the source of truth for look and feel when building or restyling UI. Use when asked to "make it look like X", to pick a design direction, or to write a DESIGN.md for this project.
---

# DESIGN.md as the design source of truth

A DESIGN.md is a plain markdown design system: colors, type scale, spacing, radius, shadows, component rules, tone. Agents read it and produce consistent UI without Figma.

## How to use

1. If the project has its own `DESIGN.md` at the repo root, read it first and follow it over any example here.
2. To borrow a direction, read one file from `examples/` (linear.app, apple, airbnb, cal, stripe, supabase) and apply its tokens and rules, adapted to the product. Do not copy brand names, logos or copy.
3. The full collection (74 brands) lives at https://github.com/VoltAgent/awesome-design-md/tree/main/design-md. Fetch another brand's DESIGN.md from there when a closer reference exists.
4. When asked to write a DESIGN.md for this project, use the same section structure as the examples: overview, colors (with hex and roles), typography (families, scale, weights), spacing and layout, radius and elevation, components, motion, do/don't.

## For this repository (Tipulit)

The app is a Hebrew, RTL, mobile-first product UI. Fonts: Heebo (body), Rubik (display). Accent #215FBA, plate yellow #F7C948 as the one subject-specific color. Keep semantic colors (good/warn/crit) separate from the accent. Prefer the "cal" and "linear.app" examples for product screens; "airbnb" for a future landing page.
