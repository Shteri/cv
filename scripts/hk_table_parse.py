"""Parse the periodic-maintenance table of a Hebrew Hyundai/Kia owner's book (PyMuPDF).

The Israeli books are translations of the global manual: a table whose header row
lists km x1000 (15 30 45 ... 120) and months (12 24 ... 96), one item per row with
I / R / - per column, engine-variant labels in the middle, and free-text notes
("החלף לאחר 210,000 ק"מ ...") for long intervals. This script only reads what is
on the page: for each row it prints the label, the pattern (one char per km
column, right-to-left order converted to ascending km) and any inline text.

Usage: python3 scripts/hk_table_parse.py book.pdf 484 485 486
"""
import sys, re, json
import pymupdf

CELLS = {"I", "R", "-", "C", "T", "|R", "I|", "R|", "|I"}

def page_rows(page):
    words = page.get_text("words")
    # header: the y band holding the most of 15,30,...,150 tokens
    km_tokens = {str(k) for k in range(15, 151, 15)} | {str(k) for k in range(10, 161, 10)} | {str(k) for k in range(30, 241, 30)}
    bands = {}
    for w in words:
        if w[4] in km_tokens:
            bands.setdefault(round(w[1] / 4), {})[w[4]] = ((w[0] + w[2]) / 2, w[1])
    vbands = {}
    for w in words:
        if w[4] in km_tokens:
            vbands.setdefault(round(w[0] / 4), {})[w[4]] = ((w[1] + w[3]) / 2, w[0])
    header = max(bands.values(), key=len) if bands else {}
    vheader = max(vbands.values(), key=len) if vbands else {}
    if len(vheader) > len(header) and len(vheader) >= 6:
        return transposed_rows(page, words, vheader)
    if len(header) < 6:
        vh = truncated_header(page)
        if vh:
            return transposed_rows(page, words, vh)
        return None
    cols = sorted(((float(k), x) for k, (x, y) in header.items()), key=lambda kv: kv[1])  # by x
    xs = [x for _, x in cols]
    step = (xs[-1] - xs[0]) / (len(xs) - 1)
    header_y = min(y for x, y in header.values())
    lo, hi = xs[0] - step * 0.6, xs[-1] + step * 0.6
    rows = {}
    for w in words:
        t = w[4].strip("|")
        if not t or w[1] < header_y + 4:
            continue
        xc = (w[0] + w[2]) / 2
        yc = round((w[1] + w[3]) / 2)
        if w[4] in CELLS and lo < xc < hi:
            km = min(cols, key=lambda kv: abs(kv[1] - xc))[0]
            rows.setdefault(yc, {})[km] = t
    ys = sorted(rows)
    merged = []
    for y in ys:
        if merged and y - merged[-1][0] <= 5:
            merged[-1][1].update(rows[y])
        else:
            merged.append([y, dict(rows[y])])
    out = []
    for y, marks in merged:
        if len(marks) < 4:
            continue
        near = [w for w in words if abs((w[1] + w[3]) / 2 - y) < 9 and (w[0] > hi or w[2] < lo) and w[4] not in CELLS]
        right = " ".join(w[4] for w in sorted([w for w in near if w[0] > hi], key=lambda w: -w[0]))
        left = " ".join(w[4] for w in sorted([w for w in near if w[2] < lo], key=lambda w: -w[0]))
        pat = "".join(marks.get(k, ".") for k, _ in sorted(cols))  # ascending km
        out.append({"y": y, "pattern": pat, "label": right, "left": left})
    kms = [k for k, _ in sorted(cols)]
    return {"km_columns": kms, "rows": out}

def truncated_header(page):
    """Some Hyundai books lose digits of the rotated km header ("1", "3", "4", "6",
    "7", "90", "1 0", "1 2"). Find the vertical "1,000" line, take the short numeric
    lines in the same x column above it and number them 15, 30, ... from the bottom."""
    d = page.get_text("dict")
    lines = []
    for b in d["blocks"]:
        for l in b.get("lines", []):
            t = "".join(sp["text"] for sp in l["spans"]).strip()
            if t and abs(l["dir"][1]) > 0.9:
                lines.append((l["bbox"], t))
    anchor = [bb for bb, t in lines if re.fullmatch(r"1\s*,\s*0\s*0\s*0", t)]
    if not anchor:
        return None
    ax0, ay0, ax1, ay1 = anchor[0]
    xc = (ax0 + ax1) / 2
    ticks = [bb for bb, t in lines if abs((bb[0] + bb[2]) / 2 - xc) < 6 and bb[3] <= ay0 + 1 and re.fullmatch(r"[\d ]{1,4}", t)]
    if len(ticks) < 6:
        return None
    ticks.sort(key=lambda bb: -bb[1])  # bottom first = smallest km
    return {str(15 * (i + 1)): (((bb[1] + bb[3]) / 2), bb[0]) for i, bb in enumerate(ticks)}

def transposed_rows(page, words, header):
    """Landscape pages (Hyundai): the table is rotated, km values run down one x
    column and each maintenance item is a vertical line of text. Use dict mode
    to get whole lines with their direction."""
    kms = sorted(((float(k), y) for k, (y, x) in header.items()), key=lambda kv: kv[1])
    ys = [y for _, y in kms]
    step = (ys[-1] - ys[0]) / (len(ys) - 1)
    lo, hi = ys[0] - step * 0.6, ys[-1] + step * 0.6
    header_x = max(x for y, x in header.values())
    d = page.get_text("dict")
    cells = []   # (x, y, mark)
    labels = []  # (x, text)
    for b in d["blocks"]:
        for l in b.get("lines", []):
            txt = "".join(sp["text"] for sp in l["spans"]).strip()
            if not txt:
                continue
            x0, y0, x1, y1 = l["bbox"]; xc = (x0 + x1) / 2; yc = (y0 + y1) / 2
            if xc >= header_x - 2:
                continue
            if txt in CELLS and lo < yc < hi:
                cells.append((xc, yc, txt.strip("|")))
            elif abs(l["dir"][1]) > 0.9 and len(txt) > 1:
                labels.append((xc, y0, y1, txt))
    cols = {}
    for xc, yc, t in cells:
        km = min(kms, key=lambda kv: abs(kv[1] - yc))[0]
        cols.setdefault(round(xc), {})[km] = t
    xs = sorted(cols); merged = []
    for x in xs:
        if merged and x - merged[-1][0] <= 6:
            merged[-1][1].update(cols[x])
        else:
            merged.append([x, dict(cols[x])])
    out = []
    order = sorted(kms)  # ascending km
    for x, marks in merged:
        if len(marks) < 4:
            continue
        near = sorted([lb for lb in labels if abs(lb[0] - x) < 10], key=lambda lb: lb[1])
        label = " ".join(lb[3] for lb in near if lb[2] > hi - step)   # label side (below km band)
        other = " ".join(lb[3] for lb in near if lb[2] <= hi - step)
        # the first cell is often glued to the end of the label line ("מצב המצברI")
        m = re.search(r"([IR])$", label)
        if m and order[0][0] not in marks:
            marks[order[0][0]] = m.group(1); label = label[:-1].strip()
        pat = "".join(marks.get(k, ".") for k, _ in order)
        out.append({"y": x, "pattern": pat, "label": label, "left": other})
    return {"km_columns": [k for k, _ in order], "rows": out, "transposed": True}

def free_text(page):
    """Lines that carry a km figure but are not table cells (long-interval notes)."""
    t = page.get_text()
    t = re.sub(r'ק\s*"\s*מ', 'ק"מ', t)
    return [l.strip() for l in t.splitlines() if re.search(r"\d{1,3},\d{3}", l)]

if __name__ == "__main__":
    args = sys.argv[1:]
    out_json = None
    if "--json" in args:
        i = args.index("--json"); out_json = args[i + 1]; del args[i:i + 2]
    doc = pymupdf.open(args[0])
    if out_json:
        res = {"file": args[0], "pages": []}
        for pn in [int(x) for x in args[1:]]:
            r = page_rows(doc[pn]) or {}
            res["pages"].append({"page": pn, "km_columns": r.get("km_columns"), "rows": r.get("rows", []), "txt": free_text(doc[pn])})
        json.dump(res, open(out_json, "w"), ensure_ascii=False, indent=1)
        sys.exit(0)
    for pn in [int(x) for x in args[1:]]:
        page = doc[pn]
        r = page_rows(page)
        print(f"\n===== page {pn} =====")
        if not r:
            print("(no km header found)")
            for l in free_text(page): print("  txt:", l)
            continue
        print("km columns:", r["km_columns"])
        for row in r["rows"]:
            print(f"  {row['pattern']:10} | {row['label'][:70]:70} | {row['left'][:60]}")
        for l in free_text(page): print("  txt:", l)
