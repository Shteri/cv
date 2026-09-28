# Research generators (hand-researched schedules)

Each folder holds the Python scripts a research pass used to write the schedule JSON
files for one brand group (all transcribed numbers live in these scripts). The output
was staged outside the repo and imported with `scripts/stage_import.py`; the per-group
source notes are in `data/sources/research/<group>.md`. They reference scratch paths
from the original session, so treat them as the record of what was transcribed, not as
a build step. Schedules produced by `scripts/build_schedules.py` are separate.
