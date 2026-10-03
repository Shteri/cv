import json,sys,collections
d=json.load(open('/home/user/cv/data/sources/registry-counts.json'))
mk=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else ''
import re
rows=[r for r in d['model_year_fuel_engine'] if mk in r['make'] and re.search(pat,r['model'])]
agg=collections.defaultdict(int)
for r in rows: agg[(r['make'],r['model'],r['fuel'],r['engine'])]+=r['n']
for k,v in sorted(agg.items(),key=lambda x:-x[1])[:40]:
  yrs=sorted([(r['year'],r['n']) for r in rows if (r['make'],r['model'],r['fuel'],r['engine'])==k])
  print(v,k,' '.join(f'{y}:{n}' for y,n in yrs))
