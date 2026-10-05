import pymupdf,sys,re
d=pymupdf.open('carz_warranty.pdf')
for pn in [int(x) for x in sys.argv[1:]]:
    p=d[pn-1]
    words=p.get_text('words')
    # header columns: tokens like 12/20,000
    cols=[(w[0]+w[2])/2 for w in words if re.match(r'^\d+/[\d,]+$',w[4])]
    hdr=[w[4] for w in words if re.match(r'^\d+/[\d,]+$',w[4])]
    order=sorted(zip(cols,hdr))
    print('=== page',pn,'cols (x->hdr):',[(round(x),h) for x,h in order])
    hy=[w[1] for w in words if re.match(r'^\d+/[\d,]+$',w[4])]
    hy=max(hy) if hy else 0
    marks={'החלף','בדוק','בצע','נקז','*'}
    # group by line y
    rows={}
    for w in words:
        if w[1]<=hy+2: continue
        key=round((w[1]+w[3])/2/3)
        rows.setdefault(key,[]).append(w)
    for k in sorted(rows):
        ws=sorted(rows[k],key=lambda w:-w[0])
        label=' '.join(w[4] for w in ws if w[4] not in marks or w[0]>max(cols)+30)
        cells=['']*len(order)
        for w in ws:
            if w[4] in marks and w[0]<max(cols)+30:
                cx=(w[0]+w[2])/2
                i=min(range(len(order)),key=lambda i:abs(order[i][0]-cx))
                cells[i]+=w[4]
        # order columns by km ascending
        kmorder=sorted(range(len(order)),key=lambda i:int(order[i][1].split('/')[1].replace(',','')))
        print(f'{label[:60]:60s} | '+' | '.join(f'{cells[i]:5s}' for i in kmorder))
