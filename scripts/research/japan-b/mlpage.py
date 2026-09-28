import re,html,sys,subprocess
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
mid,pages=sys.argv[1],sys.argv[2:]
for p in pages:
    t=subprocess.run(['curl','-sSL','-A',UA,f'https://www.manualslib.com/manual/{mid}/x.html?page={p}'],capture_output=True,text=True).stdout
    open(f'/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/japan-b/ml_{mid}_{p}.html','w').write(t)
    t=re.sub(r'<(script|style).*?</\1>','',t,flags=re.S)
    i=t.find('pdf_page'); seg=t[i:]
    j=seg.find('Related Manuals'); seg=seg[:j] if j>0 else seg[:40000]
    txt=html.unescape(re.sub(r'\s+',' ',re.sub(r'<[^>]+>',' ',seg)))
    print(f'===== page {p}'); print(txt[:4000])
