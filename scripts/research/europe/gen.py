# Generator for the "europe" group schedules. Every number below was read from a
# document opened in this session (see SRC dict and REPORT.md).
import json, os, copy

OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/europe'
os.makedirs(OUT, exist_ok=True)
RULES = []
WRITTEN = []

def I(item, note=None): return (item, 'inspect', note)
def R(item, note=None): return (item, 'replace', note)
def C(item, note=None): return (item, 'clean', note)
def A(item, note=None): return (item, 'adjust', note)

def grid(step, n, every, extra=None):
    """every: list of tuples applied at every service; extra: {multiple_of_km: [tuples]}"""
    out = []
    for k in range(1, n + 1):
        km = step * k
        its = list(every)
        for m, lst in (extra or {}).items():
            if km % m == 0:
                its += lst
        out.append((km, its))
    return out

def mk_services(g):
    res = []
    for km, its in g:
        seen = set(); items = []
        for it in its:
            key = (it[0], it[1])
            if key in seen: continue
            seen.add(key)
            d = {'item': it[0], 'action': it[1]}
            if it[2]: d['note'] = it[2]
            items.append(d)
        res.append({'km': km, 'items': items})
    return res

def LI(item, action, **kw):
    d = {'item': item, 'action': action}
    d.update(kw)
    return d

def write(v, plan, rules):
    s = {
        'make': v['make'], 'make_he': v['make_he'], 'importer': v['importer'], 'id': v['id'],
        'model': v['model'], 'model_he': v['model_he'], 'generation': v.get('generation', ''),
        'years': v['years'], 'engines': v['engines'], 'fuel': v['fuel'],
        'interval': plan['interval'], 'cycle_km': plan['cycle_km'],
        'services': mk_services(plan['grid']),
        'long_interval': plan.get('long', []), 'time_based': plan.get('time_based', []),
        'specs': {**plan.get('specs', {}), **v.get('specs', {})},
        'sources': v.get('sources', plan['sources']),
        'status': v.get('status', plan['status']),
        'notes': v.get('notes', plan['notes']),
    }
    if plan.get('first_service_km'): s['first_service_km'] = plan['first_service_km']
    if not s['generation']: del s['generation']
    json.dump(s, open(f"{OUT}/{v['id']}.json", 'w'), ensure_ascii=False, indent=2)
    WRITTEN.append(v['id'])
    for r in rules:
        rr = {'make': v['rule_make'] if 'rule_make' in v else v['make']}
        rr.update(r); rr['schedule'] = v['id']
        RULES.append(rr)
