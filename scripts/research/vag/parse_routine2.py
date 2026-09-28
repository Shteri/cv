import re,json
from html.parser import HTMLParser
s=open('champion_routine.html').read()
opts=dict(re.findall(r'<option value="(\d+-\d+)" data-string="\d">([^<]+)</option>',s))
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.cur=None; s.row=None; s.cell=None
    def handle_starttag(s,tag,a):
        a=dict(a)
        if tag=='div' and 'table-rap' in (a.get('class') or ''):
            s.cur={'key':a.get('data-string'),'rows':[]}; s.tables.append(s.cur)
        if s.cur is None: return
        if tag=='tr': s.row=[]; s.cur['rows'].append(s.row)
        if tag in('td','th') and s.row is not None:
            s.cell={'cls':a.get('class',''),'grp':a.get('data-group'),'txt':'','icons':[],'colspan':a.get('colspan')}; s.row.append(s.cell)
        if tag=='path' and s.cell is not None:
            d=a.get('d','')
            s.cell['icons'].append('R' if d.startswith('M16.6666 9.1') else ('I' if d.startswith('M10 15C9.72') else 'X'))
    def handle_endtag(s,tag):
        if tag in('td','th'): s.cell=None
    def handle_data(s,d):
        if s.cell is not None: s.cell['txt']+=d
p=P(); p.feed(s)
for t in p.tables:
    if not t['key'].startswith('2-'): continue
    print('=====',opts[t['key']])
    for r in t['rows']:
        name=r[0]['txt'].strip()[:45] if r else ''
        cells=[]
        for c in r[1:]:
            v=''.join(sorted(set(c['icons']))) or ('-' if not c['txt'].strip() else '['+c['txt'].strip()[:40]+']')
            cells.append((c['grp'],v))
        g1=' '.join(f'{v:>3}' for g,v in cells if g in('1',None))
        g2=' '.join(f'{v:>3}' for g,v in cells if g=='2')
        print(f'{name:45s}| {g1} || {g2}')
