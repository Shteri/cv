# eu4 generator helpers. Every number in the plan modules was read from a document opened in this session.
import json, os
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/eu4'
os.makedirs(OUT + '/registry', exist_ok=True)
RULES, WRITTEN = [], []

def it(item, action, note=None):
    return (item, action, note)

def build(step, n, cols_items, first=None):
    """cols_items: list of (set_of_column_numbers or 'all', item tuple). Columns are 1-based."""
    out = []
    first = first or step
    for c in range(1, n + 1):
        km = first + (c - 1) * step
        seen, items = set(), []
        for cols, t in cols_items:
            if cols == 'all' or c in cols:
                key = (t[0], t[1])
                if key in seen: continue
                seen.add(key)
                d = {'item': t[0], 'action': t[1]}
                if t[2]: d['note'] = t[2]
                items.append(d)
        out.append({'km': km, 'items': items})
    return out

def LI(item, action, **kw):
    d = {'item': item, 'action': action}; d.update(kw); return d

def write(s, rules):
    order = ['id','make','make_he','model','model_he','generation','years','engines','fuel','importer','interval','first_service_km','cycle_km','services','long_interval','time_based','specs','sources','status','notes']
    s.setdefault('time_based', [])
    s = {k: s[k] for k in order if k in s}
    json.dump(s, open(f"{OUT}/{s['id']}.json", 'w'), ensure_ascii=False, indent=2)
    WRITTEN.append(s['id'])
    for r in rules:
        r = dict(r); r['schedule'] = s['id']; RULES.append(r)

def rule_only(r):
    RULES.append(r)

def save_rules():
    json.dump(RULES, open(OUT + '/registry/registry_rules.json', 'w'), ensure_ascii=False, indent=1)
