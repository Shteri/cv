import json, os
OUT = '/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/jp4'
ACT = {'I': 'inspect', 'R': 'replace', 'C': 'clean', 'T': 'adjust', 'A': 'adjust', 'O': 'rotate'}
ITEMS = set(l.split(':')[0].strip() for l in open('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/ITEMS.txt') if ':' in l)
RULES = []

class S:
    def __init__(self, id, make, make_he, model, model_he, generation, years, engines, fuel, importer,
                 interval_km, months, interval_note, cycle_km, first_km=None):
        self.d = dict(id=id, make=make, make_he=make_he, model=model, model_he=model_he, generation=generation,
                      years=list(years), engines=list(engines), fuel=fuel, importer=importer,
                      interval=dict(km=interval_km, months=months, note=interval_note), cycle_km=cycle_km)
        if first_km: self.d['first_service_km'] = first_km
        self.first = first_km or interval_km
        self.step = interval_km
        self.svc = {}
        self.long = []
        self.tb = []
        self.specs = {}
        self.sources = []
    def kms(self):
        k = self.first; out = []
        while k <= self.d['cycle_km']:
            out.append(k); k += self.step
        return out
    def add(self, km, item, action, note=None):
        assert item in ITEMS, item
        assert km in self.kms(), (item, km)
        lst = self.svc.setdefault(km, [])
        for x in lst:
            if x['item'] == item:
                if x['action'] == 'inspect' and action != 'inspect':
                    x['action'] = action
                    if note: x['note'] = note
                return
        e = dict(item=item, action=action)
        if note: e['note'] = note
        lst.append(e)
    def every(self, item, action, km, note=None, start=None):
        k = start or km
        while k <= self.d['cycle_km']:
            self.add(k, item, action, note); k += km
    def at(self, item, action, kms, note=None):
        for k in kms: self.add(k, item, action, note)
    def pat(self, item, pattern, col_km, note=None, notes=None):
        """pattern: one char per column (col_km*1, col_km*2 ...), chars I R C T -"""
        pattern = pattern.replace(' ', '')
        for i, ch in enumerate(pattern):
            if ch in ACT:
                self.add(col_km * (i + 1), item, ACT[ch], note)
    def li(self, item, action, **kw):
        assert item in ITEMS, item
        e = dict(item=item, action=action); e.update(kw); self.long.append(e)
    def time(self, item, action, months, note=None):
        assert item in ITEMS, item
        e = dict(item=item, action=action, months=months)
        if note: e['note'] = note
        self.tb.append(e)
    def src(self, url, kind, note):
        self.sources.append(dict(url=url, kind=kind, note=note))
    def write(self, status, notes, specs=None):
        d = dict(self.d)
        d['services'] = [dict(km=k, items=self.svc[k]) for k in sorted(self.svc)]
        d['long_interval'] = self.long
        d['time_based'] = self.tb
        d['specs'] = specs or self.specs
        d['sources'] = self.sources
        d['status'] = status
        d['notes'] = notes
        json.dump(d, open(os.path.join(OUT, d['id'] + '.json'), 'w'), ensure_ascii=False, indent=2)
        return d

def rule(make, names, years, schedule, fuel=None, engine_codes=None):
    r = dict(make=make, names=names, years=list(years))
    if fuel: r['fuel'] = fuel
    if engine_codes: r['engine_codes'] = engine_codes
    r['schedule'] = schedule
    RULES.append(r)

def save_rules(fname):
    json.dump(RULES, open(os.path.join('/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/dl/jp4/rules', fname), 'w'), ensure_ascii=False, indent=1)
