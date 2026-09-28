import re,json,subprocess,urllib.parse,sys
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36"
for s in ['peugeot','citroen','opel','dsautomobiles']:
    t=open(f'gb_{s}.html',encoding='utf-8',errors='replace').read()
    i=t.find('var modelsYears = ')
    if i<0: print(s,'no data'); continue
    data,_=json.JSONDecoder().raw_decode(t[i+len('var modelsYears = '):])
    for mod in data:
        for dt in mod['docType']:
            form=[('action','get_clearmash_doc_url'),('docIds[]',str(dt['docId'])),('model',mod['modelName']),(f"docs[{dt['docId']}]",dt['docType']),(f"docTypes[{dt['docId']}]",dt['docTypeId'])]
            body=urllib.parse.urlencode(form)
            r=subprocess.run(['curl','-s','-A',UA,'-X','POST','--data',body,f'https://online.{s}.co.il/wp-admin/admin-ajax.php'],capture_output=True,text=True).stdout
            links=sorted(set(re.findall(r'https?://[^"\'\s<>]+',r)))
            print(s,'|',mod['modelName'],'|',dt['range'],'|',dt['docType'],'|',' '.join(links)[:400])
