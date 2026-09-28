import sys,re,html,subprocess,os
mid,slug,pages=sys.argv[1],sys.argv[2],sys.argv[3]
a,b=map(int,pages.split('-'))
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for p in range(a,b+1):
    fn=f'ml_{mid}_{p}.html'
    if not os.path.exists(fn) or os.path.getsize(fn)<1000:
        subprocess.run(['curl','-s','-A',UA,'-o',fn,f'https://www.manualslib.com/manual/{mid}/{slug}.html?page={p}'])
    s=open(fn,errors='ignore').read()
    # manualslib page text lives in divs with class pdf... ; extract text of the page container
    m=re.search(r'<div[^>]*class="[^"]*pdf[^"]*"[^>]*>(.*?)<div[^>]*class="[^"]*(?:pagination|manual-nav|bottom)',s,flags=re.S)
    body=m.group(1) if m else s
    body=re.sub(r'<script.*?</script>|<style.*?</style>','',body,flags=re.S)
    body=re.sub(r'</div>|<br\s*/?>','\n',body)
    t=html.unescape(re.sub(r'<[^>]+>','',body))
    t=re.sub(r'[ \t]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
    print(f'######## PAGE {p}\n'+t.strip())
