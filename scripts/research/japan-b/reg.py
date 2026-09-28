import json,sys,collections
d=json.load(open('/home/user/cv/data/sources/registry-counts.json'))
mk=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else None
import re
tot=collections.Counter()
for m in d['model']:
    if mk in m['make'] and (not pat or re.search(pat,m['model'])): tot[(m['make'],m['model'])]+=m['n']
for (mm,mo),n in tot.most_common(60):
    if n<150: continue
    yrs={int(x['year']):x['n'] for x in d['model_year'] if x['make']==mm and x['model']==mo and x['year'].isdigit()}
    fu={x['fuel']:x['n'] for x in d['model_fuel'] if x['make']==mm and x['model']==mo}
    en={x['engine']:x['n'] for x in d['model_engine'] if x['make']==mm and x['model']==mo}
    print(n,mm,mo,'|',' '.join(f'{y}:{c}' for y,c in sorted(yrs.items())),'|',fu,'|',en)
