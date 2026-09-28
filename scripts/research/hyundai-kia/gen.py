"""Tiny builder for schedule JSON files (staging only).

rows: list of (item, pattern, note) where pattern is a string with one char per grid
column (I=inspect, R=replace, A=adjust, C=clean, T=rotate, '.'=nothing) or a dict {km: action}.
Grid columns are first_km + n*interval (n=0..).
"""
import json, os

OUT = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/hyundai-kia"
ITEMS = set(l.split(":")[0].strip() for l in open(
    "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/ITEMS.txt") if ":" in l)
ACT = {"I": "inspect", "R": "replace", "A": "adjust", "C": "clean", "T": "rotate"}


def build(meta, rows, long_interval=(), specs=None, time_based=()):
    interval = meta["interval"]["km"]
    first = meta.get("first_service_km", interval)
    cycle = meta["cycle_km"]
    kms = list(range(first, cycle + 1, interval))
    svc = {k: [] for k in kms}
    for row in rows:
        item, pat = row[0], row[1]
        note = row[2] if len(row) > 2 else None
        assert item in ITEMS, item
        if isinstance(pat, dict):
            cols = pat.items()
        else:
            p = pat.replace(" ", "")
            assert len(p) <= len(kms), (item, p, len(kms))
            cols = [(kms[i], ACT[c]) for i, c in enumerate(p) if c != "."]
        for km, act in cols:
            act = ACT.get(act, act)
            e = {"item": item, "action": act}
            if note:
                e["note"] = note
            svc[km].append(e)
    for l in long_interval:
        assert l["item"] in ITEMS, l["item"]
    for t in time_based:
        assert t["item"] in ITEMS, t["item"]
    d = dict(meta)
    d["services"] = [{"km": k, "items": v} for k, v in svc.items() if v]
    d["long_interval"] = list(long_interval)
    d["time_based"] = list(time_based)
    if specs:
        d["specs"] = specs
    order = ["make", "make_he", "importer", "id", "model", "model_he", "generation", "years", "engines", "fuel",
             "interval", "first_service_km", "cycle_km", "services", "long_interval", "time_based", "specs",
             "sources", "status", "notes"]
    d = {k: d[k] for k in order if k in d}
    os.makedirs(OUT, exist_ok=True)
    with open(os.path.join(OUT, d["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(d, f, ensure_ascii=False, indent=2)
    print("wrote", d["id"], len(d["services"]), "services")
    return d


HY = dict(make="Hyundai", make_he="יונדאי", importer="כלמוביל")
KIA = dict(make="Kia", make_he="קיה", importer="טלקאר")
