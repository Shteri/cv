import json, sys, importlib
from gen import RULES, WRITTEN, OUT
for m in sys.argv[1:] or ['psa']:
    importlib.import_module(m)
json.dump(RULES, open(f'{OUT}/registry_rules.json', 'w'), ensure_ascii=False, indent=1)
print(len(WRITTEN), 'schedules,', len(RULES), 'rules')
