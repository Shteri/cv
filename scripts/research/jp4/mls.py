import re,html,subprocess,sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def page(slug,p):
    t=subprocess.run(['curl','-s','-L','-A',UA,f'https://www.manua.ls/{slug}/manual?p={p}'],capture_output=True,text=True,errors='ignore').stdout
    m=re.search(r'<div id="pf%x".*?(?=<div class="viewer-toolbar__main)'%p,t,re.S)
    s=m.group(0) if m else ''
    bg=re.search(r"url\('(/viewer/[^']+)'\)",s)
    s=re.sub(r'<[^>]+>',' ',s); s=html.unescape(re.sub(r'\s+',' ',s))
    return s,(bg.group(1) if bg else None)
if __name__=='__main__':
    slug=sys.argv[1]; pat=sys.argv[2] if len(sys.argv)>2 else None
    for p in [int(x) for x in sys.argv[3].split(',')] if len(sys.argv)>3 else range(1,10):
        s,bg=page(slug,p)
        if pat is None or re.search(pat,s,re.I): print(p,bg,s[:300])
