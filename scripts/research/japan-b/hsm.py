# parse Honda ESM HTML maintenance tables into grid rows
import sys, re, html
from html.parser import HTMLParser
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.tables=[]; s.row=None; s.cell=None; s.depth=0
    def handle_starttag(s, tag, a):
        a=dict(a)
        if tag=='table': s.tables.append([])
        elif tag=='tr': s.row=[]
        elif tag in ('td','th'): s.cell={'t':'','cs':int(a.get('colspan',1)),'rs':int(a.get('rowspan',1))}
        elif tag=='br' and s.cell is not None: s.cell['t']+=' '
    def handle_endtag(s, tag):
        if tag in ('td','th') and s.cell is not None and s.row is not None: s.row.append(s.cell); s.cell=None
        elif tag=='tr' and s.row is not None:
            if s.tables: s.tables[-1].append(s.row)
            s.row=None
    def handle_data(s, d):
        if s.cell is not None: s.cell['t']+=d
def grid(fn):
    t=open(fn,errors='ignore').read()
    p=P(); p.feed(t)
    out=[]
    for tb in p.tables:
        # expand rowspans
        pending={}  # col -> (remaining, text)
        rows=[]
        for r in tb:
            line=[]; ci=0; it=iter(r)
            cells=list(r); k=0
            while k < len(cells) or any(c>=ci for c in pending):
                if ci in pending:
                    rem,txt=pending[ci]; line.append(txt+'^')
                    if rem>1: pending[ci]=(rem-1,txt)
                    else: del pending[ci]
                    ci+=1; continue
                if k>=len(cells): break
                c=cells[k]; k+=1
                txt=html.unescape(re.sub(r'\s+',' ',c['t'])).strip()
                for j in range(c['cs']):
                    line.append(txt if j==0 else '<')
                    if c['rs']>1: pending[ci]=(c['rs']-1,txt)
                    ci+=1
            rows.append(line)
        out.append(rows)
    return out
if __name__=='__main__':
    for tb in grid(sys.argv[1]):
        print('=== table')
        for r in tb:
            lab=r[0][:70] if r else ''
            marks=''.join('X' if x.strip() in ('l','●','•') else ('.' if x.strip()=='' else ('<' if x=='<' else '?')) for x in r[1:])
            extra=[x for x in r[1:] if x.strip() not in ('l','','<') and not x.endswith('^')]
            print(f'{lab:70s} | {marks} | {extra[:3]}')
