import pymupdf,sys
d=pymupdf.open(sys.argv[1]); pre=sys.argv[2]; dpi=int(sys.argv[3])
for p in sys.argv[4:]:
    d[int(p)-1].get_pixmap(dpi=dpi).save(f"{pre}-{p}.png")
