"""Merge parsed Toyota Israel maintenance sheets into data/sources/toyota-union-sheets.json.

Input: a work dir holding toyota-docs/index.json (fileId, title, models, years,
connectionId, file) and toyota-docs/parsed.json (output of
scripts/toyota_sheet_parse.py: rows = [y, label, pattern, months], lines = the
page text grouped by y). Only sheets missing from the JSON are added, so
re-running is safe. With --refresh, `rows` and `lines` of the sheets already in
the JSON are rewritten from parsed.json too (after a parser fix); the other
fields stay as they are.

Usage: python3 scripts/toyota_sheets_export.py <workdir> [--refresh] [--conn docs.json]

Download links: books.union-motors.co.il/app/api/files/<n>/download takes a CONNECTION id
(from /app/api/search?modelId=&year=), not the document's fileId; a fileId used there returns
some other document. --conn takes a list of {fileId, connectionId} (the search results) and
stores `connection_id` and a working `source` URL per sheet; `checked` is the date the link
was last confirmed to return the same sheet.
"""
import datetime, json, re, sys
import pymupdf

work = sys.argv[1].rstrip("/")
refresh = "--refresh" in sys.argv[2:]
conn = {}
if "--conn" in sys.argv:
    conn = {d["fileId"]: d["connectionId"] for d in json.load(open(sys.argv[sys.argv.index("--conn") + 1]))}
DL = "https://books.union-motors.co.il/app/api/files/{}/download"
OUT = "data/sources/toyota-union-sheets.json"
idx = {e["fileId"]: e for e in json.load(open(f"{work}/toyota-docs/index.json"))}
parsed = json.load(open(f"{work}/toyota-docs/parsed.json"))
sheets = json.load(open(OUT))


def body_rows(e):
    body = []; cols = None
    for y, label, pat, left in e["rows"]:
        if y == "COLS":
            a, b = label.split("..")
            step = 15000 if a == "15" else 10000
            cols = list(range(int(a) * 1000, int(b) * 1000 + 1, step))
            continue
        body.append({"label": label, "pattern": pat, "months": left})
    return body, cols


added = refreshed = 0
for fid, e in parsed.items():
    if "rows" not in e:
        continue
    if fid in sheets:
        if refresh:
            body, _ = body_rows(e)
            if sheets[fid]["rows"] != body or sheets[fid].get("lines") != e.get("lines"):
                sheets[fid]["rows"] = body
                sheets[fid]["lines"] = e.get("lines", [])
                refreshed += 1
        continue
    meta = idx[int(fid)]
    body, cols = body_rows(e)
    doc = pymupdf.open(f"{work}/{meta['file']}")
    text = " ".join(re.sub(r'ק\s*"\s*מ', 'ק"מ', p.get_text()).replace("\n", " ") for p in doc)
    eng = re.search(r"\b\d[A-Z]{1,3}-[A-Z]{2,4}\b", text)
    fl = [l.strip() for l in doc[0].get_text().splitlines() if re.search(r"\b\d\.\d\b|SAE|API|DOT|SLLC|ATF|GL-", l)]
    sheets[fid] = {
        "title": meta["title"], "models": meta["models"], "years": [min(meta["years"]), max(meta["years"])],
        "engine": eng.group(0) if eng else None, "columns_km": cols, "rows": body, "fluid_tokens": fl[:20],
        "source": f"https://books.union-motors.co.il/app (fileId {fid}, connectionId {meta.get('connectionId', '?')})",
        "text": text[:20000], "lines": e.get("lines", []),
    }
    added += 1
for fid, s in sheets.items():
    c = conn.get(int(fid)) or idx.get(int(fid), {}).get("conn")
    if c and (s.get("connection_id") != c or not s["source"].startswith(DL.format(""))):
        s["file_id"] = int(fid)
        s["connection_id"] = c
        s["source"] = DL.format(c)
        s["checked"] = datetime.date.today().isoformat()
json.dump(sheets, open(OUT, "w"), ensure_ascii=False, indent=1)
print(f"added {added}, refreshed {refreshed}, total {len(sheets)}")
