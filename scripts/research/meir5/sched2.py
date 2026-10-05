import pymupdf,sys,re
f=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
d=pymupdf.open(f)
t=' '.join(re.sub(r'^.*?CRC - [\d/ ]+','',d[i].get_text().replace('\n',' '),count=1) for i in range(a-1,b))
s=t.find('הטיפולים הנדרשים הנוספים עבור רכב בשימוש רגיל כל')
e=t.find('תנאים קשים המחייבים',s)
print('NORMAL:',t[s:e])
s2=t.find('הטיפולים הנדרשים הנוספים עבור רכב בשימוש מאומץ כל')
print('SEVERE:',t[s2:s2+700])
for k in ['בכל חמש שנים','בכל שנתיים','כל שנתיים','מדי10,000','מדי 10,000','מדי12,000','מדי 12,000']:
    if k in t: print('HAS',k)
