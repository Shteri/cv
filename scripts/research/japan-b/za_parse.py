import pymupdf, sys, re, collections
def parse(f, pn):
    d = pymupdf.open(f); p = d[pn-1]
    W = p.get_text('words')
    # header: km values
    kms = [w for w in W if re.fullmatch(r'\d{1,3}', w[4]) and int(w[4])>=10 and int(w[4])%5==0]
    bands = collections.defaultdict(list)
    for w in kms: bands[round(w[1]/3)].append(w)
    hdr = max(bands.values(), key=lambda b: len(b))
    hdr = sorted(hdr, key=lambda w: w[0])
    cols = [(int(w[4]), (w[0]+w[2])/2) for w in hdr]
    hy = hdr[0][3]
    step = cols[1][1]-cols[0][1]
    x0 = cols[0][1] - step*0.6
    marks = [w for w in W if w[4] in ('I','R','[R]','[I]','R*','I*') and w[1] > hy+15 and w[0] > x0]
    labels = [w for w in W if w[2] < x0 - 5 and w[1] > hy + 15]
    rows = collections.defaultdict(dict)
    for m in marks:
        xc = (m[0]+m[2])/2; yc = (m[1]+m[3])/2
        km = min(cols, key=lambda c: abs(c[1]-xc))[0]
        rows[round(yc)][km] = m[4]
    # merge close rows
    out = []
    for y in sorted(rows):
        if out and y - out[-1][0] <= 3: out[-1][1].update(rows[y]); continue
        out.append([y, rows[y]])
    res = []
    for y, r in out:
        lab = ' '.join(w[4] for w in sorted([w for w in labels if abs((w[1]+w[3])/2 - y) < 7], key=lambda w: w[0]))
        pat = ''.join((r.get(k, '-').replace('[', '').replace(']', '').replace('*','') if r.get(k,'-').startswith('[') is False else r[k][1].lower()) for k, _ in cols)
        res.append((pat, lab))
    return [c[0] for c in cols], res
if __name__ == '__main__':
    cols, res = parse(sys.argv[1], int(sys.argv[2]))
    print(cols)
    for pat, lab in res: print(pat, '|', lab)
