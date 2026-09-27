# Maintenance schedule data

Each file in `schedules/` describes the periodic maintenance plan for one
make + model + generation + engine family as sold in Israel.

Rules:

- Written in our own words. Facts (what is replaced at which km) are not
  copyrightable; book text is. Never paste passages from a service book.
- Every file names its sources and a `status`:
  `draft` (collected from the web), `reviewed` (we read it end to end),
  `verified` (checked against the importer's own book).
- Item keys come from `items.json`. Add a key there before using it.
- Israeli importer intervals win over global manufacturer intervals when
  they differ. Note the difference in `interval.note`.
- `cycle_km` is where the plan starts over, so a 20-year-old car at 300,000 km
  still gets a sensible answer.

Validate: `node scripts/validate.mjs` (to be added).
