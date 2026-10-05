import json, os
ST = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/tail4"
ITEMS = json.load(open("/home/user/cv/data/items.json"))
ACT = {"I": "inspect", "R": "replace", "C": "clean", "A": "adjust", "T": "rotate", "-": None, ".": None}
def grid(cols, rows):
    """rows: (item, pattern[, note]) one char per column"""
    out = []
    for ci, km in enumerate(cols):
        items = []; seen = set()
        for row in rows:
            item, pat = row[0], row[1]; note = row[2] if len(row) > 2 else None
            assert len(pat) == len(cols), (item, pat, len(cols))
            assert item in ITEMS, item
            a = ACT[pat[ci]]
            if not a or (item, a) in seen: continue
            seen.add((item, a)); e = {"item": item, "action": a}
            if note: e["note"] = note
            items.append(e)
        # drop inspect of an item replaced in the same service
        rep = {e["item"] for e in items if e["action"] == "replace"}
        items = [e for e in items if not (e["item"] in rep and e["action"] != "replace")]
        out.append({"km": km, "items": items})
    return out
def L(item, action, **kw):
    assert item in ITEMS, item
    d = {"item": item, "action": action}; d.update(kw); return d
def write(d):
    order = ["id", "make", "make_he", "model", "model_he", "generation", "years", "engines", "fuel", "importer", "interval", "cycle_km",
             "services", "long_interval", "time_based", "specs", "sources", "status", "notes"]
    d = {k: d[k] for k in order if k in d}
    d.setdefault("long_interval", []); d.setdefault("time_based", [])
    p = os.path.join(ST, d["id"] + ".json")
    json.dump(d, open(p, "w"), ensure_ascii=False, indent=2)
    print("wrote", d["id"])
def copy_sister(src_id, new_id, **over):
    d = json.load(open(f"/home/user/cv/data/schedules/{src_id}.json"))
    d.update(over); d["id"] = new_id
    return d
