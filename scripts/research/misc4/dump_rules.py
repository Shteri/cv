import json, glob, importlib.util, sys
sys.path.insert(0,'.')
from rules import R
json.dump(R, open('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/misc4/registry/registry_rules.json','w'), ensure_ascii=False, indent=1)
print(len(R),'rules')
