import re,html,sys
t=open(sys.argv[1],'rb').read().decode('utf-8','replace')
t=re.sub(r'<script.*?</script>|<style.*?</style>','',t,flags=re.S)
t=html.unescape(re.sub(r'<[^>]+>','\n',t)); t=re.sub(r'\n\s*\n+','\n',t)
print(t)
