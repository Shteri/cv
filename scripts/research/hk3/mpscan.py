import sys,re,html,subprocess,os,json
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
os.makedirs('mpt',exist_ok=True)
def get(slug,p):
    fn=f"mpt/{slug.replace('/','_')}-{p}.txt"
    if os.path.exists(fn): return open(fn).read()
    r=subprocess.run(['curl','-s','-A',UA,f"https://www.manualpdf.co.il/{slug}/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p={p}"],capture_output=True)
    t=r.stdout.decode('utf8','ignore')
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    s=html.unescape(re.sub(r'<[^>]+>',' ',s));s=re.sub(r'\s+',' ',s)
    a=s.find('תן חוות דעת'); b=s.find('זקוק לעזרה?')
    s=s[a:b] if a>=0 and b>a else s[:5000]
    open(fn,'w').write(s); return s
def npages(slug):
    t=get(slug,1); m=re.search(r'(\d+) עמודים',t)
    return int(m.group(1)) if m else None
if __name__=='__main__':
    slug=sys.argv[1]; lo=float(sys.argv[2]) if len(sys.argv)>2 else 0.55; hi=float(sys.argv[3]) if len(sys.argv)>3 else 0.95
    n=npages(slug); first=get(slug,1)
    print(slug,n,first[:300])
    pages=list(range(max(2,int(n*lo)),int(n*hi)+1))
    with ThreadPoolExecutor(12) as ex: txts=list(ex.map(lambda p:get(slug,p),pages))
    for p,t in zip(pages,txts):
        if re.search(r'KILOMETERS|[Kk]m\s*[x×]\s*1,?000|Middle East|MAINTENANCE SCHEDULE|Maintenance schedule|SCHEDULED MAINTENANCE|Normal maintenance',t):
            print(' ',p,t[:200].replace('\n',' '))
