import pymupdf,sys,collections
f=sys.argv[1]; pn=int(sys.argv[2])
d=pymupdf.open(f); p=d[pn-1]
ws=[w for w in p.get_text("words") if w[4] in ('I','R','T','C','R:','I:')]
xs=collections.Counter(round((w[0]+w[2])/2) for w in ws)
print(sorted(xs.items()))
rows=collections.defaultdict(list)
for w in ws: rows[round((w[1]+w[3])/2)].append((round((w[0]+w[2])/2),w[4]))
lines=collections.defaultdict(list)
for w in p.get_text("words"): lines[round((w[1]+w[3])/2)].append(w)
for y in sorted(rows):
    lab=' '.join(w[4] for w in sorted(lines[y],key=lambda w:-w[0]) if w[4] not in ('I','R','T','C'))
    print(y, sorted(rows[y]), lab[:80])
