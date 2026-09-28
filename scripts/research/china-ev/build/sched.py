import json, os
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/china-ev'
ITEMS = set(json.load(open('/home/user/cv/data/items.json')))
RANK = {'replace': 5, 'rotate': 4, 'adjust': 3, 'clean': 2, 'inspect': 1}
LET = {'I': 'inspect', 'R': 'replace', 'C': 'clean', 'T': 'adjust', 'A': 'adjust', 'L': 'inspect', 'G': 'inspect', 'X': 'rotate'}
RULES = []

class Sched:
    def __init__(self, **kw):
        self.d = dict(kw)
        iv = kw['interval']
        self.km, self.months = iv['km'], iv['months']
        self.first = kw.get('first_service_km', self.km)
        self.cycle = kw['cycle_km']
        self.kms = list(range(self.first, self.cycle + 1, self.km))
        self.svc = {k: [] for k in self.kms}
        self.long = []; self.srcs = []; self.specs = {}
    def add(self, km, item, action, note=None):
        assert item in ITEMS, item
        lst = self.svc[km]
        for it in lst:
            if it['item'] == item:
                if RANK[action] > RANK[it['action']]: it['action'] = action
                if note and note not in it.get('note', ''):
                    it['note'] = (it.get('note', '') + '; ' + note).strip('; ')
                return
        e = {'item': item, 'action': action}
        if note: e['note'] = note
        lst.append(e)
    def row(self, item, pattern, note=None, lnote=None):
        """pattern: one char per service column (I/R/C/T/L/.)"""
        pattern = pattern.replace(' ', '')
        assert len(pattern) == len(self.kms), (item, pattern, len(self.kms))
        for km, ch in zip(self.kms, pattern):
            if ch == '.': continue
            n = note
            if ch in 'LG': n = ((note + '; ') if note else '') + 'גירוז/שימון'
            self.add(km, item, LET[ch], n)
    def every(self, item, action, every_km, note=None, start=None, other=None):
        """action at km where (km-start)%every_km==0; 'other' action at the remaining services"""
        start = start or every_km
        for km in self.kms:
            if km >= start and (km - start) % every_km == 0: self.add(km, item, action, note)
            elif other: self.add(km, item, other, note)
    def all(self, item, action='inspect', note=None):
        for km in self.kms: self.add(km, item, action, note)
    def li(self, item, action, note=None, **kw):
        assert item in ITEMS, item
        e = {'item': item, 'action': action}; e.update(kw)
        if note: e['note'] = note
        self.long.append(e)
    def src(self, url, kind, note): self.srcs.append({'url': url, 'kind': kind, 'note': note})
    def spec(self, **kw): self.specs.update(kw)
    def rule(self, make, names, years, schedule=None, fuel=None, engine_codes=None):
        r = {'make': make, 'names': names, 'years': years}
        if fuel: r['fuel'] = fuel
        if engine_codes: r['engine_codes'] = engine_codes
        r['schedule'] = schedule or self.d['id']
        RULES.append(r)
    def write(self):
        d = self.d
        o = {k: d[k] for k in ['id','make','make_he','model','model_he','generation','years','engines','fuel','importer','interval'] if k in d}
        if 'first_service_km' in d: o['first_service_km'] = d['first_service_km']
        o['cycle_km'] = self.cycle
        o['services'] = [{'km': k, 'items': self.svc[k]} for k in self.kms]
        o['long_interval'] = self.long
        o['time_based'] = []
        o['specs'] = self.specs
        o['sources'] = self.srcs
        o['status'] = d['status']
        o['notes'] = d['notes']
        json.dump(o, open(os.path.join(OUT, d['id'] + '.json'), 'w'), ensure_ascii=False, indent=2)
        print('wrote', d['id'])

def save_rules(name):
    json.dump(RULES, open(os.path.join(os.path.dirname(__file__), 'rules_' + name + '.json'), 'w'), ensure_ascii=False, indent=2)
