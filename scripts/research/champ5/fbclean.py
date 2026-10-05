import re,sys
def pages(fn):
    t=open(fn,encoding='utf-8').read()
    P={}
    for blk in re.split(r'### PAGE ',t)[1:]:
        n,_,body=blk.partition('\n')
        words=[]
        for line in body.split('\n'):
            m=re.match(r'^(.*?)R\d{3,}',line)
            w=m.group(1) if m else (line if not re.match(r'^\d+$',line) else '')
            if w: words.append(w)
        P[int(n)]=' '.join(words)
    return P
if __name__=='__main__':
    P=pages(sys.argv[1]); pat=sys.argv[2] if len(sys.argv)>2 else 'טיפול'
    for n,s in P.items():
        if re.search(pat,s): print('PAGE',n,':',s[:1500]); print()
