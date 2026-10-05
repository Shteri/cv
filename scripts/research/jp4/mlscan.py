import sys,re
from concurrent.futures import ThreadPoolExecutor
from mls import page
slug=sys.argv[1]; a,b=int(sys.argv[2]),int(sys.argv[3]); pat=sys.argv[4]
def f(p):
    s,bg=page(slug,p); return p,s,bg
with ThreadPoolExecutor(8) as ex:
    for p,s,bg in ex.map(f,range(a,b+1)):
        n=s.replace(' ','')
        if re.search(pat,n,re.I): print(p,bg,n[:250])
