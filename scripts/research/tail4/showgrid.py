import json,sys
A={'replace':'R','inspect':'I','adjust':'A','clean':'C','rotate':'T'}
for p in sys.argv[1:]:
    d=json.load(open(p))
    kms=[s['km'] for s in d['services']]
    print('##',d['id'],d['status'],'interval',d['interval'].get('km'),'cycle',d['cycle_km'],'cols',[k//1000 for k in kms])
    rows={}
    for i,s in enumerate(d['services']):
        for e in s['items']:
            r=rows.setdefault(e['item'],['-']*len(kms))
            r[i]=r[i]+A[e['action']] if r[i]!='-' else A[e['action']]
    for k,v in rows.items(): print(f'  {k:28s}',''.join(x if len(x)==1 else '['+x+']' for x in v))
    for l in d['long_interval']: print('  LONG',{a:b for a,b in l.items() if a!='note'}, '|', l.get('note','')[:150])
    for l in d.get('time_based',[]): print('  TIME',l)
    print('  SPECS',d.get('specs'))
    print('  NOTES',d['notes'][:1500])
