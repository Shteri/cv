import pymupdf, re, sys
def parse(f, pno):
    d = pymupdf.open(f); p = d[pno-1]
    lines = []
    for b in p.get_text('dict')['blocks']:
        for l in b.get('lines', []):
            t = ''.join(s['text'] for s in l['spans']).strip()
            if t: lines.append((l['bbox'], l['dir'], t))
    cols = []
    for bb, dr, t in lines:
        m = re.match(r'([\d,]+)\s*ק"?מ', t)
        if dr[1] != 0 and m: cols.append(((bb[0]+bb[2])/2, int(m.group(1).replace(',', ''))))
    if not cols: return None
    xmin = min(c[0] for c in cols) - 8
    hb = max(bb[3] for bb, dr, t in lines if dr[1] != 0)
    marks = [(bb, t) for bb, dr, t in lines if t in ('@', '✓', 'Ⓢ', 'X', '•') and bb[0] >= xmin]
    labels = [(bb, t) for bb, dr, t in lines if dr[1] == 0 and bb[2] < xmin + 2 and bb[1] > hb and t not in ('@',)]
    rows = []
    for bb, t in sorted(labels, key=lambda x: (round(x[0][1]), -x[0][2])):
        if rows and bb[1] - rows[-1]['y1'] < 2.0: 
            if abs(bb[1]-rows[-1]['ylast'])<1.5: rows[-1]['t'] += t
            else: rows[-1]['t'] += ' ' + t
            rows[-1]['y1'] = max(rows[-1]['y1'], bb[3]); rows[-1]['ylast']=bb[1]
        else: rows.append({'t': t, 'y0': bb[1], 'y1': bb[3], 'ylast': bb[1], 'k': []})
    for bb, t in marks:
        yc = (bb[1]+bb[3])/2; xc = (bb[0]+bb[2])/2
        r = min(rows, key=lambda r: 0 if r['y0']-1.5 <= yc <= r['y1']+1.5 else min(abs(yc-r['y0']), abs(yc-r['y1'])))
        km = min(cols, key=lambda c: abs(c[0]-xc))[1]
        r['k'].append(km)
    return sorted(c[1] for c in cols), [(r['t'], sorted(r['k'])) for r in rows]
if __name__ == '__main__':
    f = sys.argv[1]
    for pg in sys.argv[2:]:
        res = parse(f, int(pg))
        if not res: print('== page', pg, 'no cols'); continue
        print('== page', pg, 'cols', [c//1000 for c in res[0]])
        for t, k in res[1]: print(f'  {t[:80]:80s} {[x//1000 for x in k]}')
