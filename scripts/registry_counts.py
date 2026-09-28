"""Aggregate the data.gov.il vehicle registry CSV into data/sources/registry-counts.json.

The dump (~875 MB, pipe-delimited, windows-1255) is at
https://data.gov.il/dataset/7a338622-63bb-4cfd-b3f7-0d2e8cf71033/resource/053cea08-09bc-40ec-8f7a-156f0677aff3/download/053cea08-09bc-40ec-8f7a-156f0677aff3.csv
(needs a browser User-Agent; the e.data.gov.il link in resource_show redirects to a login).
Usage: python3 scripts/registry_counts.py <registry.csv> [YYYY-MM-DD]
"""
import sys, csv, json, collections, datetime
csv.field_size_limit(10**8)
src = sys.argv[1]
snap = sys.argv[2] if len(sys.argv) > 2 else datetime.date.today().isoformat()
make, model, my, mf, me = (collections.Counter() for _ in range(5))
with open(src, encoding="cp1255", errors="replace", newline="") as f:
    for r in csv.DictReader(f, delimiter="|"):
        mk = (r.get("tozeret_nm") or "").strip(); km = (r.get("kinuy_mishari") or "").strip()
        yr = (r.get("shnat_yitzur") or "").strip(); fu = (r.get("sug_delek_nm") or "").strip()
        en = (r.get("degem_manoa") or "").strip()
        make[(mk,)] += 1; model[(mk, km)] += 1; my[(mk, km, yr)] += 1; mf[(mk, km, fu)] += 1; me[(mk, km, en)] += 1
def pack(c, keys, minn):
    out = []
    for k, v in c.most_common():
        if v < minn: break
        d = dict(zip(keys, k)); d["n"] = v; out.append(d)
    return out
out = {"_note": "Counts of registered vehicles by maker/model/year from the data.gov.il registry. Built by scripts/registry_counts.py; read by scripts/registry_coverage.mjs.",
       "snapshot": snap, "rows": sum(make.values()),
       "make": pack(make, ["make"], 1), "model": pack(model, ["make", "model"], 50),
       "model_year": pack(my, ["make", "model", "year"], 50), "model_fuel": pack(mf, ["make", "model", "fuel"], 50),
       "model_engine": pack(me, ["make", "model", "engine"], 200)}
json.dump(out, open("data/sources/registry-counts.json", "w"), ensure_ascii=False)
print("rows", out["rows"])
