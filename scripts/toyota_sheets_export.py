"""Merge parsed Toyota Israel maintenance sheets into data/sources/toyota-union-sheets.json.

Input: a work dir holding toyota-docs/index.json (fileId, title, models, years,
connectionId, file) and toyota-docs/parsed.json (output of the coordinate parser:
rows = [y, label, pattern, months]). Only sheets missing from the JSON are added,
so re-running is safe. Usage: python3 scripts/toyota_sheets_export.py <workdir>
"""
import json, re, sys
import pymupdf

work = sys.argv[1].rstrip("/")
OUT = "data/sources/toyota-union-sheets.json"
idx = {e["fileId"]: e for e in json.load(open(f"{work}/toyota-docs/index.json"))}
parsed = json.load(open(f"{work}/toyota-docs/parsed.json"))
sheets = json.load(open(OUT))
added = 0
for fid, e in parsed.items():
    if fid in sheets or "rows" not in e:
        continue
    meta = idx[int(fid)]
    rows = e["rows"]
    cols = None
    body = []
    for y, label, pat, left in rows:
        if y == "COLS":
            a, b = label.split("..")
            step = 15000 if a == "15" else 10000
            cols = list(range(int(a) * 1000, int(b) * 1000 + 1, step))
            continue
        body.append({"label": label, "pattern": pat, "months": left})
    doc = pymupdf.open(f"{work}/{meta['file']}")
    text = " ".join(re.sub(r'ק\s*"\s*מ', 'ק"מ', p.get_text()).replace("\n", " ") for p in doc)
    eng = re.search(r"\b\d[A-Z]{1,3}-[A-Z]{2,4}\b", text)
    fl = [l.strip() for l in doc[0].get_text().splitlines() if re.search(r"\b\d\.\d\b|SAE|API|DOT|SLLC|ATF|GL-", l)]
    sheets[fid] = {
        "title": meta["title"], "models": meta["models"], "years": [min(meta["years"]), max(meta["years"])],
        "engine": eng.group(0) if eng else None, "columns_km": cols, "rows": body, "fluid_tokens": fl[:20],
        "source": f"https://books.union-motors.co.il/app (fileId {fid}, connectionId {meta.get('connectionId', '?')})",
        "text": text[:20000],
    }
    added += 1
json.dump(sheets, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"added {added}, total {len(sheets)}")
