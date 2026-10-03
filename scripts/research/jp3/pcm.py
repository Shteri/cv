import re,base64,subprocess,sys,json
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
K='pdf-lazy-loader-secure-key-2024'
def get(u): return subprocess.run(['curl','-s','-L','-A',UA,u],capture_output=True,text=True,errors='ignore').stdout
def pdfs(page):
    t=get(page); out=[]
    for enc in re.findall(r'data-pdf-lazy-original-src-enc="([^"]+)"',t):
        s=base64.b64decode(enc).decode('latin1'); u=''.join(chr(ord(c)^ord(K[i%len(K)])) for i,c in enumerate(s))
        m=re.search(r'pdfemb-data=([A-Za-z0-9_-]+)',u)
        if m:
            b=m.group(1); b+='='*(-len(b)%4); out.append(json.loads(base64.urlsafe_b64decode(b).decode()))
    links=[l for l in re.findall(r'href="(https://procarmanuals.com/pdf-online-[^"]+)"',t)]
    return out,sorted(set(links))
for p in sys.argv[1:]:
    o,l=pdfs(p); print('==',p); 
    for x in o: print('  PDF',x.get('url'),x.get('title',''))
    for x in l: print('  LINK',x)
