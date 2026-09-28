import re,sys,html
h=open(sys.argv[1],encoding='utf-8').read()
css={}
for m in re.finditer(r'\.([a-z_]*[0-9a-f]*)\{([^}]*)\}',h):
    css.setdefault(m.group(1),m.group(2))
def val(cls,prop):
    s=css.get(cls,'')
    m=re.search(prop+r':(-?[\d.]+)px',s)
    return float(m.group(1)) if m else None
i=h.find('class="pf w0 h0" data-page-no'); j=h.find('</main>',i); seg=h[i:j if j>0 else i+300000]
for m in re.finditer(r'<(h\d|div) class="t ([^"]*)">(.*?)</\1>',seg,re.S):
    cls=m.group(2).split(); inner=m.group(3)
    x=[c for c in cls if re.fullmatch(r'x[0-9a-f]+',c)]; y=[c for c in cls if re.fullmatch(r'y[0-9a-f]+',c)]
    X=val(x[0],'left') if x else None; Y=val(y[0],'bottom') if y else None
    # tokens
    toks=[]
    for t in re.split(r'(<span class="_ _[0-9a-f]+"></span>|<[^>]+>)',inner):
        mm=re.match(r'<span class="_ (_[0-9a-f]+)"></span>',t)
        if mm:
            c=mm.group(1)[1:]
            w=val('_'+c,'width') or val('_'+c,'margin-left')
            toks.append(f'[{w}]')
        elif t.startswith('<'): continue
        elif t: toks.append(html.unescape(t))
    s=''.join(toks)
    if re.search(r'[IR]',s) and len(re.sub(r'[^A-Za-z]','',s))<=20: print(f'x={X} y={Y} :: {s[:160]}')
