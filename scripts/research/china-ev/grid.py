# usage: grid.py pdf page header_values(comma) [marks]
import sys, pymupdf, re
pdf, pg = sys.argv[1], int(sys.argv[2])
hv = [s for s in sys.argv[3].split(',')]
marks = set((sys.argv[4] if len(sys.argv)>4 else 'IRLTCA'))
p = pymupdf.open(pdf)[pg]
W = p.get_text("words")
# header: find words equal to hv values; choose a y row with most matches
from collections import defaultdict
rows = defaultdict(list)
for w in W:
    if w[4] in hv: rows[round(w[1])].append(w)
hy = max(rows, key=lambda y: len(set(x[4] for x in rows[y])))
cols = sorted(rows[hy], key=lambda w: float(w[4]))
cx = [((w[0]+w[2])/2, w[4]) for w in cols]
print("header y", hy, [c[1] for c in cx])
lines = defaultdict(list)
for w in W:
    yc = (w[1]+w[3])/2
    lines[round(yc/4)].append(w)
xs=[c[0] for c in cx]; minx, maxx = min(xs)-25, max(xs)+25
for k in sorted(lines):
    ws = lines[k]
    if any(abs(((w[1]+w[3])/2) - hy) < 3 for w in ws) and len(ws)>5: continue
    grid = ['.']*len(cx); label=[]
    for w in sorted(ws, key=lambda w:-w[0]):
        mid=(w[0]+w[2])/2
        if w[4] in marks and minx<=mid<=maxx:
            i=min(range(len(cx)), key=lambda i: abs(cx[i][0]-mid)); grid[i]=w[4]
        else: label.append(w[4])
    if any(g!='.' for g in grid) or label:
        print(''.join(grid), '|', ' '.join(label)[:90])
