import re,html,sys
h=open(sys.argv[1],encoding='utf-8').read()
i=h.find('class="pf w0 h0"')
j=h.find('</main>',i) if h.find('</main>',i)>0 else i+200000
seg=h[i:j]
seg=re.sub(r'<style.*?</style>|<script.*?</script>','',seg,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>','|',seg)); t=re.sub(r'\|+','|',t)
print(t[:int(sys.argv[2]) if len(sys.argv)>2 else 3000])
