# Unfinished work (stopped 5.10.2026 at Max's request)

These patches were NOT applied to the data. They are partial, unreviewed changes from
two agents that were stopped mid-task. Apply only after checking them:
`git apply --check wip/<file>.patch`, then validate and compare against the sources.

- `toyota-18col-and-hk-cleanup.partial.patch` — parser support for Toyota sheets with
  18 columns (RAV4 2026 sheet 367, Aygo X hybrid 2026 sheet 366), new
  toyota-rav4-2026-2.5-hybrid. Not finished: re-check of hand-built Toyota/Lexus files,
  Yaris 2006-11 brakes, Hyundai/Kia "severe only" items.
- `draft-audit-fixes.partial.patch` — first fixes from the audit of the 20 biggest draft
  schedules (Honda Civic 2006-11 generator, Corolla 2001-07, time_based key in generators).
  The audit report itself was not written yet.

The two web.archive.org research rounds (arch6, arch6b) were stopped before producing files.
