import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/hk3/'
ITEMS=set(l.split(':')[0] for l in open('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/ITEMS.txt') if ':' in l)
A={'I':'inspect','R':'replace','A':'adjust','C':'clean','T':'rotate'}
def grid(step, rows, ncols=None, every=None):
    """rows: (item, pattern, note?) ; pattern one char per column of `step` km. returns {km:[items]}"""
    n=ncols or max(len(r[1]) for r in rows)
    out={}
    for c in range(n):
        km=step*(c+1)
        for r in rows:
            item,pat=r[0],r[1]; note=r[2] if len(r)>2 else None
            assert item in ITEMS, item
            if c<len(pat) and pat[c] in A:
                it={'item':item,'action':A[pat[c]]}
                if note: it['note']=note
                out.setdefault(km,[]).append(it)
    return out
def merge(*gs):
    out={}
    for g in gs:
        for km,its in g.items():
            lst=out.setdefault(km,[])
            for it in its:
                # drop duplicates of same item: keep replace over inspect
                ex=[x for x in lst if x['item']==it['item']]
                if ex:
                    if it['action']=='replace' and ex[0]['action']!='replace': lst.remove(ex[0]); lst.append(it)
                    continue
                lst.append(it)
    return out
def write(meta, svc):
    d=dict(meta)
    d['services']=[{'km':k,'items':svc[k]} for k in sorted(svc)]
    for l in d.get('long_interval',[]): assert l['item'] in ITEMS, l['item']
    d.setdefault('time_based',[])
    assert d['services'][-1]['km']<=d['cycle_km']
    json.dump(d,open(OUT+d['id']+'.json','w'),ensure_ascii=False,indent=2)
    print('wrote',d['id'],len(d['services']))
def lst(*pairs):
    """cumulative list helper: pairs of (item, action letter, note?)"""
    return [{'item':p[0],'action':A[p[1]],**({'note':p[2]} if len(p)>2 and p[2] else {})} for p in pairs]
