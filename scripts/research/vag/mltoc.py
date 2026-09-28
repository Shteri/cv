import sys,re,subprocess,os,html
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for path in sys.argv[1:]:
    mid=path.split('/')[2]
    fn=f'ml_{mid}_1.html'
    if not os.path.exists(fn): subprocess.run(['curl','-s','-A',UA,'-o',fn,'https://www.manualslib.com'+path])
    s=open(fn,errors='ignore').read()
    title=re.search(r'<title>(.*?)</title>',s,re.S).group(1).strip()
    ed=re.findall(r'(Maintenance - Edition [0-9.]+|Edition [0-9.]+)',s)[:1]
    print('=====',path,title[:100],ed)
    seen=set()
    for m in re.finditer(r'<a[^>]*href="/manual/%s/[^"]*page=(\d+)[^"]*"[^>]*>(.*?)</a>'%mid,s,flags=re.S):
        t=html.unescape(re.sub(r'<[^>]+>|\s+',' ',m.group(2)).strip())
        if re.search(r'interval|service|dust|countr|inspection|toothed|brake fluid|spark|DSG|gearbox|haldex|all wheel|coupling',t,re.I) and t not in seen and not t.startswith('Page'):
            seen.add(t); print('  ',m.group(1),t[:100])
