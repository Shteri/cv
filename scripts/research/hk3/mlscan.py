import sys,re,html,subprocess,os
from concurrent.futures import ThreadPoolExecutor
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
os.makedirs('mlt',exist_ok=True)
def get(mid,p):
    fn=f"mlt/{mid.replace('/','_')}-{p}.txt"
    if os.path.exists(fn): return open(fn).read()
    r=subprocess.run(['curl','-s','-A',UA,f"https://www.manualslib.com/manual/{mid}.html?page={p}"],capture_output=True)
    t=r.stdout.decode('utf8','ignore')
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    i=s.find('class="pdf'); s=html.unescape(re.sub(r'<[^>]+>',' ',s[i:i+30000])); s=re.sub(r'\s+',' ',s)
    s=s.split('Table of Contents Previous Page')[0]
    open(fn,'w').write(s); return s
if __name__=='__main__':
    mid=sys.argv[1]; lo=int(sys.argv[2]); hi=int(sys.argv[3])
    pages=range(lo,hi+1)
    with ThreadPoolExecutor(8) as ex: txts=list(ex.map(lambda p:get(mid,p),pages))
    for p,t in zip(pages,txts):
        if re.search(r'(?i)maintenance schedule|KILOMETERS|km\s*[x×]\s*1,?000|middle east',t): print(p,t[11:220])
