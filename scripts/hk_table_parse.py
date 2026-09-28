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
    km_tokens = {str(k) for k in range(15, 151, 15)} | {str(k) for k in range(10, 161, 10)}
    bands = {}
    for w in words:
        if w[4] in km_tokens:
            bands.setdefault(round(w[1] / 4), {})[w[4]] = ((w[0] + w[2]) / 2, w[1])
    if not bands:
        return None
    header = max(bands.values(), key=len)
    if len(header) < 6:
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

def free_text(page):
    """Lines that carry a km figure but are not table cells (long-interval notes)."""
    t = page.get_text()
    t = re.sub(r'ק\s*"\s*מ', 'ק"מ', t)
    return [l.strip() for l in t.splitlines() if re.search(r"\d{1,3},\d{3}", l)]

if __name__ == "__main__":
    doc = pymupdf.open(sys.argv[1])
    for pn in [int(x) for x in sys.argv[2:]]:
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
