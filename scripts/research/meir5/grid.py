import pymupdf,sys
# print each text line with x positions of marks ( ) and header numbers
f=sys.argv[1]; pages=[int(x) for x in sys.argv[2:]]
d=pymupdf.open(f)
for pg in pages:
    p=d[pg-1]; print('=== page',pg, p.rect)
    words=p.get_text('words')
    rows={}
    for w in words:
        x0,y0,x1,y1,t=w[:5]
        key=round((y0+y1)/2/3)
        rows.setdefault(key,[]).append((x0,t))
    for k in sorted(rows):
        r=sorted(rows[k],reverse=True)
        print(f'{k*3:5d}', '  '.join(f'{t}@{x:.0f}' for x,t in r))
