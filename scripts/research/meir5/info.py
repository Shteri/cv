import pymupdf,sys,re
for f in sys.argv[1:]:
    d=pymupdf.open(f)
    t=d[min(5,d.page_count-1)].get_text()[:120].replace('\n',' ')
    hits=[i+1 for i,p in enumerate(d) if re.search(r'X ?1,000|1,000 ?ק"מ|x1000',p.get_text())]
    print(f,d.page_count,'|',t,'|',hits[:12])
