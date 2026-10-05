import json,re,collections,sys
agg=json.load(open('/home/user/cv/data/sources/registry-counts.json'))
rows=agg['model_year_fuel_engine']
def q(pat_model, make_pat=None, years=None, byyear=False):
    c=collections.Counter()
    for r in rows:
        y=int(r['year'])
        if re.search(pat_model,r['model']) and (not make_pat or re.search(make_pat,r['make'])) and (not years or years[0]<=y<=years[1]):
            k=(r['make'],r['model'],r['fuel'],r['engine'])+((y,) if byyear else ())
            c[k]+=r['n']
    for k,v in sorted(c.items(),key=lambda x:-x[1])[:40]: print('  ',v,k)
if __name__=='__main__':
    for a in sys.argv[1:]:
        p,m,y,b=(a.split(';')+['','','',''])[:4]
        y=tuple(map(int,y.split('-'))) if y else None
        print('##',a); q(p,m or None,y,bool(b))
