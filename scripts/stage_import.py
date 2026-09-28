"""Import hand-researched schedules from a staging dir into data/schedules.

Staging layout (one dir per research group): <id>.json schedule files that pass
`node scripts/validate.mjs <dir>`, plus registry_rules.json (list of rules in the
data/registry_map.json format). Files whose id is produced by build_schedules.py
are never overwritten; an existing hand-staged file is replaced only with --force.

Usage: python3 scripts/stage_import.py <staging_dir> [--force] [--dry-run]
"""
import json, os, re, subprocess, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
SCHED = os.path.join(ROOT, "data", "schedules")
args = [a for a in sys.argv[1:] if not a.startswith("--")]
force, dry = "--force" in sys.argv, "--dry-run" in sys.argv
stage = args[0]

gen_src = open(os.path.join(ROOT, "scripts", "build_schedules.py"), encoding="utf-8").read()
generated = set(re.findall(r'"id":\s*"([a-z0-9.-]+)"', gen_src)) | set(re.findall(r'^\s*(?:toyota|hk|ford|mazda_plan|mazda)\("([a-z0-9.-]+)"', gen_src, re.M))

import shutil, tempfile
tmp = tempfile.mkdtemp()
for f in os.listdir(stage):
    if f.endswith(".json") and f != "registry_rules.json":
        shutil.copy(os.path.join(stage, f), tmp)
v = subprocess.run(["node", os.path.join(ROOT, "scripts", "validate.mjs"), tmp], capture_output=True, text=True)
print(v.stdout.strip() or v.stderr.strip())
if "all schedules valid" not in v.stdout:
    print(v.stderr); sys.exit("staging dir does not validate")

added, skipped = [], []
for f in sorted(os.listdir(stage)):
    if not f.endswith(".json") or f == "registry_rules.json":
        continue
    s = json.load(open(os.path.join(stage, f), encoding="utf-8"))
    dst = os.path.join(SCHED, f)
    if s["id"] in generated:
        skipped.append((f, "id is produced by build_schedules.py")); continue
    if os.path.exists(dst) and not force:
        skipped.append((f, "exists (use --force)")); continue
    added.append(f)
    if not dry:
        json.dump(s, open(dst, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
        open(dst, "a").write("\n")

new_rules = []
for rp in (os.path.join(stage, "registry_rules.json"), os.path.join(stage, "registry", "registry_rules.json")):
    if os.path.exists(rp):
        new_rules += json.load(open(rp, encoding="utf-8"))
mp = os.path.join(ROOT, "data", "registry_map.json")
m = json.load(open(mp, encoding="utf-8"))
have = {(r["schedule"], tuple(r["names"]), tuple(r["years"])) for r in m["rules"]}
known = {f[:-5] for f in os.listdir(SCHED) if f.endswith(".json")} | {a[:-5] for a in added}
nr = 0
for r in new_rules:
    key = (r["schedule"], tuple(r["names"]), tuple(r["years"]))
    if key in have:
        continue
    if r["schedule"] not in known:
        print("  rule for unknown schedule skipped:", r["schedule"]); continue
    r = {k: r[k] for k in ("make", "names", "years", "fuel", "engine_codes", "schedule") if k in r}
    r["names"] = [n.upper().strip() for n in r["names"]]
    m["rules"].append(r); have.add(key); nr += 1
if not dry:
    json.dump(m, open(mp, "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    open(mp, "a").write("\n")
print(f"added {len(added)} schedules, {nr} rules; skipped {len(skipped)}")
for f, why in skipped:
    print("  skip", f, "-", why)
