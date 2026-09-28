import json,sys
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/hk2/'
ITEMS=set(l.split(':')[0] for l in open('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/ITEMS.txt') if ':' in l)
A={'I':'inspect','R':'replace','A':'adjust','C':'clean','T':'rotate'}
def build(meta, km, rows, first=None):
    """rows: list of (item, pattern, note or None). pattern chars per column I/R/-."""
    n=max(len(r[1]) for r in rows)
    services=[]
    for c in range(n):
        items=[]
        for r in rows:
            item,pat=r[0],r[1]
            assert item in ITEMS, item
            if c<len(pat) and pat[c] in A:
                it={'item':item,'action':A[pat[c]]}
                if len(r)>2 and r[2]: it['note']=r[2]
                items.append(it)
        if items: services.append({'km':(first or km)+c*km if first else km*(c+1),'items':items})
    d=dict(meta)
    d.setdefault('cycle_km',km*n)
    d['services']=services
    for l in d.get('long_interval',[]): assert l['item'] in ITEMS, l['item']
    d.setdefault('time_based',[])
    json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
    print('wrote',d['id'],len(services))
