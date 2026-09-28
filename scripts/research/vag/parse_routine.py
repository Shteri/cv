import re,html,json
from html.parser import HTMLParser
s=open('champion_routine.html').read()
opts=dict(re.findall(r'<option value="(\d+-\d+)" data-string="\d">([^<]+)</option>',s))
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.cur=None; s.row=None; s.cell=None; s.depth=0
    def handle_starttag(s,tag,a):
        a=dict(a)
        if tag=='div' and 'table-rap' in (a.get('class') or ''):
            s.cur={'key':a.get('data-string'),'rows':[]}; s.tables.append(s.cur)
        if s.cur is None: return
        if tag=='tr': s.row=[]; s.cur['rows'].append(s.row)
        if tag in('td','th') and s.row is not None:
            s.cell={'cls':a.get('class',''),'txt':'','icons':[], 'colspan':a.get('colspan')}; s.row.append(s.cell)
        if tag=='path' and s.cell is not None:
            d=a.get('d','')
            s.cell['icons'].append('R' if d.startswith('M16.6666 9.1') else ('I' if d.startswith('M10 15C9.72') else 'X:'+d[:20]))
    def handle_endtag(s,tag):
        if tag in('td','th'): s.cell=None
    def handle_data(s,d):
        if s.cell is not None: s.cell['txt']+=d
p=P(); p.feed(s)
out={}
for t in p.tables:
    name=opts.get(t['key'],t['key'])
    print('=====',t['key'],name)
    hdr=None
    rows=[]
    for r in t['rows']:
        vis=[c for c in r if 'hidden' not in c['cls']]
        txts=[c['txt'].strip() for c in vis]
        if vis and vis[0]['cls']=='name' and txts[0]=='' and len(vis)>2:
            hdr=txts[1:]; print('HDR',hdr); continue
        if not vis or 'bheader' in str(r): pass
        line=[]
        for c in vis[1:]:
            v=''.join(sorted(set(c['icons'])))
            if c['txt'].strip(): v+=('['+c['txt'].strip()+']')
            if c.get('colspan'): v+='{cs%s}'%c['colspan']
            line.append(v or '-')
        print(f"{txts[0][:40]:40s} | "+' '.join(f'{x:>3}' for x in line))
        rows.append((txts[0],line))
    out[name]={'hdr':hdr,'rows':rows}
json.dump(out,open('champion_routine.json','w'),ensure_ascii=False,indent=1)
