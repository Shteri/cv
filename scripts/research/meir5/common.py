import json, os
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/meir5'
ITEMS = set(json.load(open('/home/user/cv/data/items.json')).keys())
CHEV = 'https://www.chevrolet.co.il/media/'
def I(item, action='inspect', note=None):
    assert item in ITEMS, item
    d = {'item': item, 'action': action}
    if note: d['note'] = note
    return d
def L(item, action, note=None, **kw):
    assert item in ITEMS, item
    d = {'item': item, 'action': action}; d.update(kw)
    if note: d['note'] = note
    return d
def T(item, action, months, note=None):
    assert item in ITEMS, item
    d = {'item': item, 'action': action, 'months': months, 'every_months': months}
    if note: d['note'] = note
    return d
def write(d):
    keys = ['id','make','make_he','model','model_he','generation','years','engines','fuel','importer','interval','first_service_km','cycle_km','services','long_interval','time_based','specs','sources','status','notes']
    o = {k: d[k] for k in keys if k in d and d[k] is not None}
    # sanity
    kms = [s['km'] for s in o['services']]
    assert kms == sorted(kms) and len(set(kms)) == len(kms)
    for s in o['services']:
        seen=set()
        for it in s['items']:
            k=(it['item'],it['action'])
            assert k not in seen, (o['id'], s['km'], k); seen.add(k)
    json.dump(o, open(os.path.join(OUT, o['id'] + '.json'), 'w'), ensure_ascii=False, indent=2)
    print('wrote', o['id'], o['status'], len(o['services']), 'services')
