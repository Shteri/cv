import json, os
OUT = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/ev3"
ACT = {"I": "inspect", "R": "replace", "C": "clean", "A": "adjust", "T": "rotate"}


def grid(step, ncols, rows):
    """rows: list of (item, pattern, note_or_None). pattern: one char per column (I/R/C/A/T or - or .)"""
    services = []
    for c in range(ncols):
        items = []
        for row in rows:
            item, pat = row[0], row[1]
            note = row[2] if len(row) > 2 else None
            assert len(pat) == ncols, (item, pat)
            ch = pat[c]
            if ch in ACT:
                d = {"item": item, "action": ACT[ch]}
                if note:
                    d["note"] = note
                items.append(d)
        services.append({"km": step * (c + 1), "items": items})
    return services


def write(d, extra_services=None):
    order = ["id", "make", "make_he", "model", "model_he", "generation", "years", "engines", "fuel", "importer",
             "interval", "cycle_km", "services", "long_interval", "time_based", "specs", "sources", "status", "notes"]
    d.setdefault("long_interval", [])
    d.setdefault("time_based", [])
    d.setdefault("specs", {})
    out = {k: d[k] for k in order if k in d}
    for k in d:
        if k not in out:
            out[k] = d[k]
    with open(os.path.join(OUT, d["id"] + ".json"), "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
    print("wrote", d["id"])
