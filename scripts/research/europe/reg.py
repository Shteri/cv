import json,sys,collections
d=json.load(open('/home/user/cv/data/sources/registry-counts.json'))
pat=sys.argv[1]; mpat=sys.argv[2] if len(sys.argv)>2 else None
for m in d['model']:
  if pat in m['make'] and (not mpat or mpat in m['model']):
    mk,md=m['make'],m['model']
    yrs=sorted((x['year'],x['n']) for x in d['model_year'] if x['make']==mk and x['model']==md)
    fu=[(x['fuel'],x['n']) for x in d['model_fuel'] if x['make']==mk and x['model']==md]
    en=[(x['engine'],x['n']) for x in d['model_engine'] if x['make']==mk and x['model']==md]
    print(m['n'],mk,'|',md,'|',fu,'|',en,'|',' '.join(f'{y}:{n}' for y,n in yrs))
