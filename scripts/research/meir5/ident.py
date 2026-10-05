import pymupdf,glob,os,re,shutil,json
T='/root/.claude/projects/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/tool-results'
os.makedirs('raw',exist_ok=True)
seen=json.load(open('seen.json')) if os.path.exists('seen.json') else {}
for f in sorted(glob.glob(T+'/webfetch-*.pdf')):
    b=os.path.basename(f)
    if b in seen: continue
    d=pymupdf.open(f)
    hdr=''
    for i in range(3,min(12,d.page_count)):
        t=d[i].get_text()
        m=re.search(r'.{0,60}Localizing.{0,40}|.{0,80}(Owner Manual|ספר נהג|Owner\'s).{0,40}',t)
        if m: hdr=m.group(0).replace('\n',' '); break
    if not hdr: hdr=d[min(3,d.page_count-1)].get_text()[:120].replace('\n',' ')
    seen[b]={'pages':d.page_count,'hdr':hdr,'title':d.metadata.get('title','')}
    shutil.copy(f,'raw/'+b)
    print(b,d.page_count,'|',d.metadata.get('title','')[:40],'|',hdr[:150])
json.dump(seen,open('seen.json','w'),ensure_ascii=False,indent=0)
