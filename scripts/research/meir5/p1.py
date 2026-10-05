import mpscan,sys,re
from concurrent.futures import ThreadPoolExecutor
slugs=sys.argv[1:]
def f(s):
    t=mpscan.get(s,1)
    m=re.search(r'(\d+) עמודים (\S+)',t)
    return s, (m.group(1),m.group(2)) if m else None, t[60:330]
with ThreadPoolExecutor(10) as ex:
    for s,m,t in ex.map(f,slugs): print(s,m,'|',t)
