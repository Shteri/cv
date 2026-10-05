import json,sys,collections
for f in sys.argv[1:]:
    d=json.load(open(f))
    print('##',d['id'],d['status'],d['interval'],d['cycle_km'],d.get('first_service_km'))
    k=collections.defaultdict(list)
    for s in d['services']:
        for it in s['items']: k[(it['item'],it['action'])].append(s['km']//1000)
    for (i,a),v in k.items(): print(f'  {i:22s} {a:8s} {v if len(v)<len(d["services"]) else "ALL"}')
    for l in d.get('long_interval',[]): print('  LI',{x:y for x,y in l.items() if x!='note'}, '|', l.get('note','')[:80])
    for l in d.get('time_based',[]): print('  TB',l)
    print('  specs',d.get('specs'))
    print('  notes',d.get('notes','')[:300])
    for s in d['sources']: print('  src',s)
