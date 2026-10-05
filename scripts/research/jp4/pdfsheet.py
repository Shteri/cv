import sys,pymupdf
from PIL import Image, ImageDraw
f,a,b,step,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),int(sys.argv[4]),sys.argv[5]
w=int(sys.argv[6]) if len(sys.argv)>6 else 300; cols=int(sys.argv[7]) if len(sys.argv)>7 else 5
d=pymupdf.open(f); ims=[]
for p in range(a,min(b,d.page_count),step):
    pix=d[p].get_pixmap(dpi=40); im=Image.frombytes('RGB',(pix.width,pix.height),pix.samples); im=im.resize((w,int(w*im.height/im.width)))
    ImageDraw.Draw(im).text((3,3),str(p),fill='red'); ims.append(im)
h=max(i.height for i in ims); rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*h),'white')
for k,im in enumerate(ims): S.paste(im,((k%cols)*w,(k//cols)*h))
S.save(out)
