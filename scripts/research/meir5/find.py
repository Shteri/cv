import pymupdf,sys,re
for f in sys.argv[1:]:
    d=pymupdf.open(f); out=[]
    for i,p in enumerate(d):
        t=p.get_text()
        n=len(re.findall(r'\b\d{2,3},000\b',t))
        if n>=5 or re.search(r'תחזוקה מתוכננת|תכנית תחזוקה|תוכנית תחזוקה|מועדי טיפולים|לוח טיפולים|טיפולים נוספים נדרשים|שירותים נוספים נדרשים',t): out.append((i+1,n))
    print(f,d.page_count,out)
