import pymupdf,sys,re
f=sys.argv[1]
d=pymupdf.open(f)
out=[]
print('#',f,d.page_count, d[0].get_text()[:200].replace('\n',' | '))
for i,p in enumerate(d):
    if i>90: break
    t=p.get_text()
    heads=[l.strip() for l in t.split('\n') if re.match(r'^\d\.\d(\.\d)?$',l.strip())]
    j=t.find('Israel')
    if j>=0:
        # find nearest preceding heading line on the page
        pre=t[:j]; hs=re.findall(r'\n(\d\.\d+(?:\.\d+)?)\n([^\n]+)',pre)
        hp=re.findall(r"(?m)^(\d\.\d+(?:\.\d+)?)\n([^\n]+)",t)[:4]
        print('  p%d ISRAEL; before: %s; on page: %s'%(i, hs[-2:] if hs else None, hp))
    if re.search(r'Additional work|Maintenance Tables|Service tables|Service Intervals|service intervals|Additional Procedures',t):
        out.append(f'=== p{i}\n'+t)
open(f.replace('.pdf','_tables.txt'),'w').write('\n'.join(out))
