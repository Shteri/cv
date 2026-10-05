import pymupdf,sys,re
f=sys.argv[1]; a=int(sys.argv[2]); b=int(sys.argv[3])
d=pymupdf.open(f)
t=' '.join(re.sub(r'^.*?CRC - [\d/ ]+','',d[i].get_text().replace('\n',' '),count=1) for i in range(a-1,b))
i=t.find('מדי1'); 
for key in ['מומלץ לבצע טיפולים אלה','בכל חמש','בכל שנתיים','החלפת שמן מנוע','סבב גלגלים וטיפולים','הטיפולים הנדרשים הנוספים עבור רכב בשימוש רגיל','הטיפולים הנדרשים הנוספים עבור רכב בשימוש מאומץ','חומר הייבוש']:
    for m in re.finditer(re.escape(key),t): print('>>',t[m.start():m.start()+ (900 if 'נוספים' in key else 250)]); print()
