import sys,re
from concurrent.futures import ThreadPoolExecutor
from mls import page
slug,pat,a,b=sys.argv[1],sys.argv[2],int(sys.argv[3]),int(sys.argv[4])
def f(p):
    s,bg=page(slug,p); return p,s,bg
with ThreadPoolExecutor(12) as ex:
    for p,s,bg in sorted(ex.map(f,range(a,b+1))):
        m=re.search(pat,s,re.I)
        if m: print(p,bg,'...',s[max(0,m.start()-120):m.start()+200])
