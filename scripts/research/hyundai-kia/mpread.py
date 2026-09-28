import sys,re
t=open(sys.argv[1]).read() if False else None
import subprocess
t=subprocess.run(['python3','mptext.py',sys.argv[1],'200000'],capture_output=True,text=True).stdout
out=[]
for seg in t.split('|'):
  s=seg.strip()
  if not s: continue
  if any('֐'<=c<='׿' for c in s):
    s=s[::-1]
    s=re.sub(r'\d[\d,.]*', lambda m: m.group(0)[::-1], s)
  out.append(s)
s=' | '.join(out)
k=s.find('הרזעל קוקז'); k2=s.find('זקוק לעזרה')
cut=[x for x in (k,k2) if x>0]
if cut: s=s[:min(cut)]
print(s)
