import json, os
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/misc4'
ITEMS = set(json.load(open('/home/user/cv/data/items.json')).keys())

def grid(interval, cycle, rows, first=None):
    """rows: list of (item, action, when, note). when: 'all' | int n (every n-th service) | set/list of km | callable(km)->bool"""
    first = first or interval
    kms = list(range(first, cycle + 1, interval))
    services = []
    for k in kms:
        idx = (k - first)//interval + 1
        items = []
        for row in rows:
            item, action, when = row[0], row[1], row[2]
            note = row[3] if len(row) > 3 else None
            assert item in ITEMS, item
            if when == 'all': ok = True
            elif isinstance(when, int): ok = idx % when == 0
            elif callable(when): ok = when(k)
            else: ok = k in set(when)
            if ok:
                it = {'item': item, 'action': action}
                if note: it['note'] = note
                items.append(it)
        services.append({'km': k, 'items': items})
    return services

def write(d):
    for li in d.get('long_interval', []): assert li['item'] in ITEMS, li['item']
    for li in d.get('time_based', []): assert li['item'] in ITEMS, li['item']
    order = ['id','make','make_he','model','model_he','generation','years','engines','fuel','importer','interval','first_service_km','cycle_km','services','long_interval','time_based','specs','sources','status','notes']
    o = {k: d[k] for k in order if k in d}
    with open(os.path.join(OUT, d['id'] + '.json'), 'w') as f:
        json.dump(o, f, ensure_ascii=False, indent=2)
    print('wrote', d['id'])
