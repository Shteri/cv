import pymupdf,sys,re
from collections import defaultdict
d=pymupdf.open(sys.argv[1])
for i in [int(x) for x in sys.argv[2].split(',')]:
    W=d[i].get_text('words')
    hdr=[w for w in W if w[4] in ('A','B')]
    # header positions: first A and B occurrences in a row
    ys=defaultdict(list)
    for w in hdr: ys[round(w[1])].append(w)
    hy=min(y for y in ys if len(ys[y])>=2)
    cols={w[4]:(w[0]+w[2])/2 for w in ys[hy]}
    rows=defaultdict(lambda: {'t':[], 'm':set()})
    for w in W:
        if w[1]<=hy+2: continue
        k=round((w[1]+w[3])/2/5)
        if w[4]=='●':
            c=min(cols,key=lambda c: abs(cols[c]-(w[0]+w[2])/2)); rows[k]['m'].add(c)
        else: rows[k]['t'].append(w[4])
    print('== page',i,cols)
    for k in sorted(rows):
        r=rows[k]; print(''.join(sorted(r['m'])).ljust(3),' '.join(r['t'])[:110])
