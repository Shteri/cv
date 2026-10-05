# Parse MG Israel (Car East) A/B maintenance tables: prints row no, marks per column, text.
import pymupdf, sys, re
def parse(pdf, pages):
    d = pymupdf.open(pdf)
    out = []
    for pno in pages:
        p = d[pno-1]
        W = p.get_text("words")
        # header columns: words exactly 'A' / 'B' (also C?) in top area of table
        cols = {}
        for w in W:
            if w[4] in ('A','B','C') and w[0] < 150 and w[1] < 200:
                cols.setdefault(w[4], (w[0]+w[2])/2)
        bullets = [((w[0]+w[2])/2, (w[1]+w[3])/2) for w in W if '‰' in w[4] or w[4] in ('•','●')]
        # lines with bbox
        lines = []
        for b in p.get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                t = ''.join(s["text"] for s in l["spans"]).strip()
                if t: lines.append((l["bbox"], t))
        nums = [ (int(w[4]), (w[1]+w[3])/2, w) for w in W if re.fullmatch(r'\d{1,2}', w[4]) and w[0] > 520 ]
        # section headings: lines centered without number, bold - approximate: lines whose x0>150 and x1<520 and y not near any number
        nums.sort(key=lambda x: x[1])
        rows = []
        for i,(n,y,w) in enumerate(nums):
            rows.append([n, y, [], []])
        for bx,by in bullets:
            if not rows: continue
            r = min(rows, key=lambda r: abs(r[1]-by))
            if abs(r[1]-by) > 14: 
                print('  !! unassigned bullet', pno, bx, by); continue
            c = min(cols, key=lambda k: abs(cols[k]-bx)) if cols else '?'
            r[2].append(c)
        for bb,t in lines:
            if bb[0] < 120 or bb[2] > 560 and re.fullmatch(r'\d{1,2}',t): continue
            yc = (bb[1]+bb[3])/2
            if not rows: continue
            r = min(rows, key=lambda r: abs(r[1]-yc))
            if abs(r[1]-yc) < 14 and bb[2] < 560: r[3].append(t)
        heads = [t for bb,t in lines if all(abs((bb[1]+bb[3])/2 - r[1]) > 14 for r in rows) and 120 < bb[0] and bb[1] > 60]
        out.append((pno, cols, heads, rows))
        print(f'=== p{pno} cols={ {k:round(v) for k,v in cols.items()} }')
        print('   heads:', heads[:6])
        for n,y,m,t in rows:
            print(f'{n:>3} {"".join(sorted(set(m))):<4} {len(m)} | {" ".join(t)[:150]}')
    return out
if __name__ == '__main__':
    parse(sys.argv[1], [int(x) for x in sys.argv[2:]])
