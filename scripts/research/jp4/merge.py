import json,glob,os
D='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/jp4/registry'
out=[]
for f in sorted(glob.glob('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/jp4/rules/rules_*.json')): out+=json.load(open(f))
ids={os.path.basename(f)[:-5] for f in glob.glob(D+'/../*.json')}
ex={os.path.basename(f)[:-5] for f in glob.glob('/home/user/cv/data/schedules/*.json')}
for r in out: assert r['schedule'] in ids or r['schedule'] in ex, r
json.dump(out,open(D+'/registry_rules.json','w'),ensure_ascii=False,indent=1); print(len(out),'rules')
