# New model/generation files that reuse an engine plan already in the repo (same engine, same source).
import json, copy
from gen import OUT, RULES, WRITTEN

REPO = '/home/user/cv/data/schedules/'

def clone(src_id, new_id, changes, notes_prefix, rules):
    d = json.load(open(REPO + src_id + '.json'))
    d = copy.deepcopy(d)
    d.update(changes)
    d['id'] = new_id
    d['notes'] = notes_prefix + d['notes']
    d['status'] = 'draft'
    json.dump(d, open(f'{OUT}/{new_id}.json', 'w'), ensure_ascii=False, indent=2)
    WRITTEN.append(new_id)
    for r in rules:
        rr = dict(r); rr['schedule'] = new_id; RULES.append(rr)

# Renault Clio V 1.3 TCe (H5H): same Renault Australia table (Kadjar/Arkana/Captur MY21+, 1.3 TCe) as the Captur file.
clone('renault-captur-2020-2026-1.3-tce', 'renault-clio-2020-2022-1.3-tce',
      {'model': 'Clio', 'model_he': 'קליאו', 'generation': 'V (BF)', 'years': [2020, 2022], 'engines': ['1.3 TCe (H5H)']},
      'קליאו 5 עם מנוע 1.3 TCe (H5H), אותו מנוע של קפצ\'ור/ארקנה; הלוח זהה לקובץ של קפצ\'ור 2020 ומבוסס על אותה טבלה של רנו אוסטרליה (שאינה כוללת את קליאו). ',
      [{'make': 'Renault', 'names': ['CLIO'], 'years': [2020, 2022], 'engine_codes': ['H5H', 'H5HB4B']}])

# Citroen C4 (B7) 2015-2016 with 1.2 PureTech 130 (HN02): same engine family/plan as the C4 2021+ PureTech file.
clone('citroen-c4-2021-2026-1.2-puretech', 'citroen-c4-2015-2018-1.2-puretech',
      {'generation': 'B7', 'years': [2015, 2018]},
      'סיטרואן C4 דור B7 (2015-2018) עם מנוע 1.2 PureTech טורבו (HN02), אותו מנוע ואותה תכנית כמו בקובץ של C4 מ-2021. ',
      [{'make': 'Citroen', 'names': ['C4'], 'years': [2014, 2018], 'engine_codes': ['HN01', 'HN02', 'HN05']}])

# Registry-only: C4 SpaceTourer 2018 is registered with engine code "HNY/HN02" (same 1.2 PureTech) -> existing file.
RULES.append({'make': 'Citroen', 'names': ['C4 SPACETOURER', 'C4 PICASSO', 'GRAND C4 PICASSO'], 'years': [2014, 2022],
              'engine_codes': ['HNY/HN02', 'HNY'], 'schedule': 'citroen-c4-spacetourer-2014-2022-1.2-puretech'})

# Registry-only: Renegade registered under make Fiat (engine 55263624 = 1.4 MultiAir) -> existing Jeep Renegade file.
RULES.append({'make': 'Fiat', 'names': ['RENEGADE', 'JEEP RENEGADE'], 'years': [2015, 2019], 'engine_codes': ['55263624'],
              'schedule': 'jeep-renegade-2015-2019-1.4-multiair'})

# Registry-only sister mapping: Opel Adam uses the same 1.4 B14XER engine and Corsa platform; the Hebrew Adam manual
# (public-servicebox.opel.com he_IL Adam 2017, p. 199) puts Israel in the international 15,000 km / 1 year plan, like the Corsa E file.
RULES.append({'make': 'Opel', 'names': ['ADAM'], 'years': [2013, 2019], 'engine_codes': ['B14XER', 'B 14 XER', 'B 1.4 XER', 'A14XER', 'A 1.4 XER'],
              'schedule': 'opel-corsa-2015-2019-1.4'})
