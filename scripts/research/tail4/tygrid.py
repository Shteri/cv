import pymupdf, sys, collections
f=sys.argv[1]
d=pymupdf.open(f); p=d[0]
W=p.get_text('words')
# header: numbers 10..160 in a row near top
cand=[w for w in W if w[4].isdigit() and int(w[4]) in range(10,170,10) and w[1]<200]
ys=collections.Counter(round(w[1]) for w in cand)
hy=ys.most_common(1)[0][0]
hdr={w[4]:(w[0]+w[2])/2 for w in cand if abs(round(w[1])-hy)<=2}
cols=sorted(hdr, key=lambda k:int(k)); xs=[hdr[k] for k in cols]
xmin=min(xs)-10; xmax=max(xs)+10
rows=collections.defaultdict(list)
for w in W:
    if w[1]<hy+5: continue
    rows[round((w[1]+w[3])/2/2)].append(w)  # bucket by 2pt
out=[]
for y in sorted(rows):
    ws=rows[y]
    pat=['-']*len(cols); other=[]; lab=[]
    for w in ws:
        x=(w[0]+w[2])/2
        if xmin<=x<=xmax and w[4] in ('I','R','C','L','T'):
            k=min(range(len(xs)), key=lambda i: abs(xs[i]-x))
            if abs(xs[k]-x)<9: pat[k]=w[4]; continue
        if x>xmax: lab.append(w)
        elif x<xmin: other.append(w[4])
        else: lab.append(w)
    lab=' '.join(w[4] for w in sorted(lab,key=lambda w:-w[0]))
    print(f"{y*2:5d} {''.join(pat)}  | {' '.join(other)[:20]:20s} | {lab[:110]}")
print('cols',cols)
