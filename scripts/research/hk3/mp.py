import sys,re,html,subprocess,os
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
def page(slug,p):
    fn=f"mpc/{slug.replace('/','_')}-{p}.html"
    os.makedirs('mpc',exist_ok=True)
    if not os.path.exists(fn) or os.path.getsize(fn)<1000:
        subprocess.run(['curl','-s','-A',UA,'-o',fn,f"https://www.manualpdf.co.il/{slug}/%D7%9E%D7%93%D7%A8%D7%99%D7%9A?p={p}"])
    t=open(fn,encoding='utf8',errors='ignore').read()
    # page text container
    m=re.search(r'<div[^>]*class="[^"]*viewer-page[^"]*"(.*?)</div>\s*</div>',t,flags=re.S)
    return t
def text(t):
    s=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
    s=html.unescape(re.sub(r'<[^>]+>',' ',s));s=re.sub(r'\s+',' ',s)
    a=s.find('עמוד:'); 
    return s
if __name__=='__main__':
    slug=sys.argv[1]
    for p in sys.argv[2:]:
        s=text(page(slug,p))
        i=s.find(' / ')
        print('=====',p); print(s[:4000])
