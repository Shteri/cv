import re,json,html as H,sys
h=open(sys.argv[1],encoding='utf-8').read()
names={}
for m in re.finditer(r'<option value="(\d-\d+)"[^>]*>([^<]*)</option>',h): names[m.group(1)]=H.unescape(m.group(2))
out={}
for m in re.finditer(r'<div class="table-rap[^"]*" data-string="([\d-]+)">\s*<table data-count="(\d+)">(.*?)</table>',h,re.S):
    key,cnt,body=m.group(1),int(m.group(2)),m.group(3)
    rows=[]
    hdr=[H.unescape(re.sub(r'<[^>]+>','',x)).strip() for x in re.findall(r'<th[^>]*>(.*?)</th>',body,re.S)]
    for tr in re.findall(r'<tr>(.*?)</tr>',body,re.S):
        nm=re.search(r'<td class="name">(.*?)(<div class="tooltip-rap">.*?<p>(.*?)</p>.*?)?</td>',tr,re.S)
        if not nm: continue
        name=H.unescape(re.sub(r'<[^>]+>','',nm.group(1))).strip()
        tip=H.unescape(re.sub(r'<[^>]+>','',nm.group(3) or '')).strip()
        cells=[]
        for td in re.finditer(r'<td class="tcol[^"]*"[^>]*data-count="(\d+)"[^>]*>(.*?)</td>|<td colspan="(\d+)">(.*?)</td>',tr,re.S):
            if td.group(1):
                x=td.group(2)
                cells.append('-' if 'class="none"' in x else 'R' if 'M16.6666 9.16671' in x else 'I' if 'M10 15C' in x else '?')
            else: cells.append('['+H.unescape(re.sub(r'<[^>]+>','',td.group(4))).strip()+']')
        rows.append([name,tip,cells])
    out[key]={'name':names.get(key),'count':cnt,'hdr':hdr,'rows':rows}
json.dump(out,open(sys.argv[2],'w'),ensure_ascii=False,indent=0)
for k,v in out.items():
    print(k,v['name'],v['count'],v['hdr'][:3],'...',len(v['rows']))
