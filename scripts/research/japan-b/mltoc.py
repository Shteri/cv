import re,html,sys,subprocess
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for mid in sys.argv[1:]:
    t=subprocess.run(['curl','-sSL','-A',UA,f'https://www.manualslib.com/manual/{mid}/x.html'],capture_output=True,text=True).stdout
    title=re.findall(r'<title>([^<]+)',t); pages=re.findall(r'of (\d+)\)',t)
    desc=re.findall(r'name="Description" content="([^"]{0,200})',t)
    toc=[]
    for h,x in re.findall(r'href="/manual/\d+/[^"]*page=(\d+)[^"]*"[^>]*>([^<]{2,80})</a>',t):
        x=html.unescape(x.strip())
        if re.search(r'aint|ervice|chedule|Specif',x,re.I) and (h,x) not in toc: toc.append((h,x))
    print('####',mid,title[:1],desc[:1]); 
    for h,x in toc[:14]: print('   ',h,x)
