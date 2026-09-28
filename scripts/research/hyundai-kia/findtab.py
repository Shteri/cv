import pymupdf,sys
d=pymupdf.open(sys.argv[1])
for i,p in enumerate(d):
    w=p.get_text("words")
    n=sum(1 for x in w if x[4] in ('I','R'))
    if n>=25: print(i+1, n, ' '.join(x[4] for x in w[:12]))
