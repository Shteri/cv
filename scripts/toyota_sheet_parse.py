#!/usr/bin/env python3
"""Coordinate parser for the Union Motors (Toyota Israel) one-page maintenance sheets.

The sheets come from books.union-motors.co.il/app (API: /app/api/models,
/app/api/search?modelId&year, /app/api/files/{connectionId}/download).

    python3 scripts/toyota_sheet_parse.py <workdir> [fileId ...]

reads <workdir>/toyota-docs/index.json (fileId, title, models, years, file) and
writes <workdir>/toyota-docs/parsed.json: per sheet the grid rows
[y, label, pattern, months] and `lines` (every text line of the page, words
joined right to left by their y position). `scripts/toyota_sheets_export.py`
merges that into data/sources/toyota-union-sheets.json.

Why `lines`: the page text in reading order puts a row's label and its
free-text interval far apart ("החלפה מדי90,000 ק"מ ... מסנן דלק מצתים"), so the
generator could not tell which interval belongs to which item. Grouping words by
their y position keeps "מצתים" and "החלפה מדי 90,000" on one line.

Glyph note: some sheets (283, 284, 288, 307, 308, 318, 324, 325) print a few
"I" marks in another font whose text layer reads "ן"; they are read as I.
A one-letter word glued to other text inside the grid (the "ב" of "ב 105,000"
in a merged drive-belt cell) is not a mark.
"""
import json
import re
import sys

import pymupdf

COLS15 = ['15', '30', '45', '60', '75', '90', '105', '120', '135', '150']
COLS10 = [str(k) for k in range(10, 181, 10)]
# Hebrew marks on diesel sheets (ב בדיקה, ה החלפה, ג גירוז, ח הידוק, נ ניקוי) and
# the "ן" glyph that some sheets use for an I mark.
HEB = {'ב': 'I', 'ה': 'R', 'ג': 'G', 'ח': 'T', 'נ': 'C', 'ן': 'I'}
MARKS = set('IRCTL') | set(HEB)


def page_lines(page, tol=3.0):
    """All words of the page grouped into lines by y centre, right to left."""
    ws = sorted(page.get_text("words"), key=lambda w: (w[1] + w[3]) / 2)
    groups = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if groups and yc - groups[-1][0] <= tol:
            groups[-1][1].append(w)
        else:
            groups.append([yc, [w]])
    out = []
    for _, g in groups:
        t = " ".join(w[4] for w in sorted(g, key=lambda w: -w[0]))
        out.append(re.sub(r'ק\s*"\s*מ', 'ק"מ', t))
    return out


def relabel(rows, words, colmin, colmax, step):
    """Labels from the row's own text line. The window used above can take words from the line
    above or below, which on the dense 16-column diesel sheets (and next to rows whose cells hold
    a sentence) gives a row its neighbour's label. A row labelled only 'רגילה' / 'מחמירה' takes
    the item name printed on its own line: below a 'רגילה' row, above a 'מחמירה' row."""
    ws = sorted(words, key=lambda w: (w[1] + w[3]) / 2)
    groups = []
    for w in ws:
        yc = (w[1] + w[3]) / 2
        if groups and yc - groups[-1][0] <= 3:
            groups[-1][1].append(w)
        else:
            groups.append([yc, [w]])
    def right_text(g):
        return ' '.join(w[4] for w in sorted([w for w in g if w[0] > colmax + step * 0.7 and w[4] not in MARKS], key=lambda w: -w[0]))
    def bare(g):  # a label line: text right of the grid, nothing in the grid or the notes column
        return bool(right_text(g)) and not any(w[2] < colmax + step * 0.6 for w in g)
    def core(s):
        return re.sub(r'רגילה|מחמירה|^רגיל\b|\bרגיל$', '', s).strip(' -')
    out = []
    for y, right, pat, left in rows:
        i = min(range(len(groups)), key=lambda k: abs(groups[k][0] - y))
        if abs(groups[i][0] - y) > 4:
            out.append((y, right, pat, left)); continue
        own = right_text(groups[i][1])
        own_words = set(own.split())
        borrowed = any(t not in own_words for t in right.split())
        if core(right) and not borrowed and core(own) not in ('בדיקה', 'החלפה'):
            out.append((y, right, pat, left)); continue
        nb = lambda k: 0 <= k < len(groups) and bare(groups[k][1])
        if core(own) in ('בדיקה', 'החלפה'):
            # the inspect / replace sub-rows of a two-line item ("בדיקה" / name / "החלפה"): the name is
            # the bare line below a 'בדיקה' row and above a 'החלפה' row. Without it the replace mark of
            # the timing belt (Hilux 2005-2015) was read as coolant.
            order = [i + 1, i - 1] if core(own) == 'בדיקה' else [i - 1, i + 1]
            k = next((k for k in order if nb(k)), None)
            out.append((y, right_text(groups[k][1]) + ' ' + own if k is not None else right, pat, left)); continue
        if not core(own):
            if not own and nb(i - 1) and nb(i + 1):  # a name printed on the lines above and below
                own = right_text(groups[i - 1][1]) + ' ' + right_text(groups[i + 1][1])
            else:
                order = [i - 1, i + 1] if 'מחמירה' in own and 'רגיל' not in own else [i + 1, i - 1]
                for k in order:
                    if nb(k):
                        own = (right_text(groups[k][1]) + ' ' + own).strip()
                        break
        out.append((y, own, pat, left))
    return out


def parse(path):
    d = pymupdf.open(path); page = d[0]; words = page.get_text("words")
    # header columns: numbers 15..150 (or 10..180) on one y band
    best = None
    for COLS in (COLS15, COLS10):
        cand = {}
        for w in words:
            if w[4] in COLS:
                cand.setdefault(round(w[1] / 5), {}).setdefault(w[4], (w[0] + w[2]) / 2)
        if not cand:
            continue
        h = max(cand.values(), key=len)
        if best is None or len(h) > len(best[0]):
            best = (h, COLS)
    if best is None:
        raise ValueError("no km header found (scanned sheet?)")
    header, COLS = best
    COLS = [c for c in COLS if c in header] if len(header) >= len(COLS) - 2 else COLS
    colx = sorted(header.items(), key=lambda kv: kv[1])
    xs = [x for _, x in colx]; colmin, colmax = min(xs), max(xs); step = (colmax - colmin) / (len(COLS) - 1)
    def in_text(m):
        # a one-letter word inside a sentence is not a mark: the merged cell
        # "אבחון ראשון ב 105,000 ק"מ ( או 72 ח ') ..." has a lone "ב" over the 45 column and
        # a "ח" over the 90 column. Such a letter is glued to other text, or its line has
        # several words of text across the grid.
        ym = (m[1] + m[3]) / 2
        same = [o for o in words if o is not m and re.search(r"\w\w", o[4]) and abs((o[1] + o[3]) / 2 - ym) < 3]
        if any(0 <= m[0] - o[2] < 3.5 or 0 <= o[0] - m[2] < 3.5 for o in same):
            return True
        return sum(1 for o in same if colmin - step * 0.6 < (o[0] + o[2]) / 2 < colmax + step * 0.6) >= 2
    rows = {}
    for w in words:
        t = w[4]; yc = round((w[1] + w[3]) / 2); xc = (w[0] + w[2]) / 2
        if t in MARKS and colmin - step * 0.6 < xc < colmax + step * 0.6:
            # text letters still shape the row bands (pitch, labels), but never become marks
            t = '-' if in_text(w) else HEB.get(t, t)
            col = min(header.items(), key=lambda kv: abs(kv[1] - xc))[0]
            m = rows.setdefault(yc, {}).setdefault('marks', {})
            if t != '-' or col not in m:
                m[col] = t
    # merge rows within 4px
    ys = sorted(rows); merged = []
    for y in ys:
        if merged and y - merged[-1][0] <= 4:
            for c, t in rows[y]['marks'].items():
                if t != '-' or c not in merged[-1][1]:
                    merged[-1][1][c] = t
        else:
            merged.append([y, dict(rows[y]['marks'])])
    out = []
    ys_m = [y for y, _ in merged]
    diffs = sorted(b - a for a, b in zip(ys_m, ys_m[1:]) if b - a > 2)
    pitch = diffs[len(diffs) // 2] if diffs else 14
    win = min(7, pitch * 0.45)
    for y, marks in merged:
        # label: words on the same band outside the column area
        lab = [w for w in words if abs((w[1] + w[3]) / 2 - y) < win and (w[0] > colmax + step * 0.7 or w[2] < colmin - step * 0.7) and w[4] not in MARKS]
        right = ' '.join(w[4] for w in sorted([w for w in lab if w[0] > colmax], key=lambda w: -w[0]))
        left = ' '.join(w[4] for w in sorted([w for w in lab if w[2] < colmin], key=lambda w: -w[0]))
        pat = ''.join(marks.get(c, '-') for c in COLS)
        out.append((y, right, pat, left))
    # rows labelled only 'רגילה'/'מחמירה' (or nothing) belong to an item whose name sits on its
    # own line between the two rows: attach the nearest unattached right-side label
    used_y = set()
    for y, _, _, _ in out:
        for w in words:
            if abs((w[1] + w[3]) / 2 - y) < win:
                used_y.add(round((w[1] + w[3]) / 2))
    orphans = {}
    for w in words:
        yc = round((w[1] + w[3]) / 2)
        if w[0] > colmax + step * 0.7 and yc not in used_y and w[4] not in MARKS and not any(abs(yc - y) < win for y, _, _, _ in out):
            orphans.setdefault(yc, []).append(w)
    og = []  # group orphan words within 3px
    for yc in sorted(orphans):
        if og and yc - og[-1][0] <= 3:
            og[-1][1].extend(orphans[yc])
        else:
            og.append([yc, list(orphans[yc])])
    fixed = []
    for y, right, pat, left in out:
        core = right.replace('רגילה', '').replace('מחמירה', '').strip(' -')
        if core == '' and og:
            g = min(og, key=lambda g: abs(g[0] - y))
            if abs(g[0] - y) <= pitch * 1.3:
                txt = ' '.join(w[4] for w in sorted(g[1], key=lambda w: -w[0]))
                right = (txt + ' ' + right).strip()
        if pat.strip('-'):  # drop bands that only had letters of a sentence (merged cells)
            fixed.append((y, right, pat, left))
    fixed = relabel(fixed, words, colmin, colmax, step)
    out = [('COLS', COLS[0] + '..' + COLS[-1], '', ''), *fixed]
    return out, page_lines(page)


if __name__ == '__main__':
    work = sys.argv[1].rstrip("/")
    idx = json.load(open(f'{work}/toyota-docs/index.json'))
    allout = {}
    for e in idx:
        try:
            rows, lines = parse(f"{work}/{e['file']}")
            allout[e['fileId']] = {'title': e['title'], 'models': e['models'], 'years': e['years'], 'rows': rows, 'lines': lines}
        except Exception as ex:
            allout[e['fileId']] = {'title': e['title'], 'err': str(ex)}
    json.dump(allout, open(f'{work}/toyota-docs/parsed.json', 'w'), ensure_ascii=False, indent=1)
    for fid in [int(x) for x in sys.argv[2:]]:
        e = allout[fid]; print(f"\n==================== {fid} {e['title']} {e.get('models')} {e.get('years')}")
        for y, right, pat, left in e.get('rows', []):
            print(f"  {pat}  | {right[:60]:60} | {left[:50]}")
