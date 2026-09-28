import json,sys,collections
d=json.load(open('/home/user/cv/data/sources/registry-counts.json'))
for name in sys.argv[1:]:
    mk,md=name.split(':')
    rows=[r for r in d['model_year_fuel_engine'] if mk in r['make'] and r['model']==md]
    agg=collections.defaultdict(int)
    for r in rows: agg[(r['year'],r['fuel'],r['engine'])]+=r['n']
    print('==',name, sum(agg.values()))
    for k in sorted(agg): 
        if agg[k]>=30: print('  ',k,agg[k])
