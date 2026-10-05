import sys
from PIL import Image
pref,a,b,out=sys.argv[1],int(sys.argv[2]),int(sys.argv[3]),sys.argv[4]
w=int(sys.argv[5]) if len(sys.argv)>5 else 300; cols=int(sys.argv[6]) if len(sys.argv)>6 else 4
ims=[]
from PIL import ImageDraw
for p in range(a,b+1):
    im=Image.open(f'{pref}{p}.webp').convert('RGB'); im=im.resize((w,int(w*im.height/im.width)))
    ImageDraw.Draw(im).text((3,3),str(p),fill='red'); ims.append(im)
h=max(i.height for i in ims); rows=(len(ims)+cols-1)//cols
S=Image.new('RGB',(cols*w,rows*h),'white')
for k,im in enumerate(ims): S.paste(im,((k%cols)*w,(k//cols)*h))
S.save(out)
