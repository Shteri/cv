import json
R = []
def rule(make, names, years, schedule, engine_codes=None, fuel=None, note=None):
    r = {'make': make, 'names': names, 'years': years}
    if engine_codes: r['engine_codes'] = engine_codes
    if fuel: r['fuel'] = fuel
    r['schedule'] = schedule
    if note: r['_note'] = note
    R.append(r)

# KGM / SsangYong
rule('KGM', ['REXTON'], [2021,2026], 'kgm-rexton-2021-2026-2.2-diesel', ['672980'], ['דיזל'])
rule('SsangYong', ['REXTON'], [2021,2026], 'kgm-rexton-2021-2026-2.2-diesel', ['672980'], ['דיזל'])
rule('SsangYong', ['REXTON'], [2017,2021], 'ssangyong-rexton-2018-2021-2.2-diesel', ['672960'], ['דיזל'])
rule('KGM', ['MUSSO'], [2024,2026], 'kgm-musso-2024-2026-2.2-diesel', ['672980'], ['דיזל'])
rule('SsangYong', ['MUSSO'], [2024,2026], 'kgm-musso-2024-2026-2.2-diesel', ['672980'], ['דיזל'])
rule('KGM', ['TORRES'], [2024,2026], 'kgm-torres-2024-2026-1.5t', ['175950'], ['בנזין'])
rule('KGM', ['TORRES'], [2025,2026], 'kgm-torres-hybrid-2025-2026-1.5t-hev', ['177910'], ['בנזין'])
rule('KGM', ['TIVOLI'], [2020,2026], 'kgm-torres-2024-2026-1.5t', ['175950'], ['בנזין'], note='sister: same 1.5T G15DTF engine code 175950 as Torres; Korando C300 Hebrew book petrol table pp.6-11..6-13 is identical to the Torres table; no Tivoli 1.5T book found')
rule('SsangYong', ['KORANDO','TIVOLI'], [2020,2026], 'kgm-torres-2024-2026-1.5t', ['175950'], ['בנזין'], note='sister: same 1.5T engine code 175950 as Torres')
rule('SsangYong', ['KORANDO','TIVOLI XLV','TIVOLI'], [2018,2023], 'ssangyong-korando-tivoli-2018-2023-1.6-diesel', ['673910'], ['דיזל'])
# GM
rule('Cadillac', ['XT5'], [2016,2019], 'cadillac-xt5-2017-2019-3.6', ['LGX'])
rule('Cadillac', ['XT5','XT6'], [2020,2026], 'cadillac-xt5-xt6-2020-2026-3.6', ['LGX'])
rule('Cadillac', ['XT4','XT5'], [2019,2026], 'cadillac-xt4-xt5-2019-2026-2.0t', ['LSY'])
rule('Cadillac', ['SRX'], [2013,2016], 'cadillac-srx-2013-2016-3.6', ['LFX'])
rule('Cadillac', ['ATS','CTS'], [2013,2019], 'cadillac-ats-cts-2013-2019-2.0t', ['LTG'], note='CTS mapped as sister (same LTG engine, ATS manual)')
rule('Buick', ['LACROSSE'], [2010,2012], 'buick-lacrosse-2010-2012-2.4-3.0-3.6', ['4CB','4DB','4GA'], note='data.gov.il model table: 4CB = degem G95GC 2.4 (2384cc), 4DB = G95GD 3.6 (3564cc), 4GA = GC5GG 3.0 (3000cc)')
rule('Buick', ['LACROSSE'], [2012,2016], 'buick-lacrosse-2012-2016-2.4-3.6', ['LFX'])
rule('Cadillac', ['SRX'], [2010,2012], 'cadillac-srx-2010-2012-3.0', ['LF1'])
rule('Chevrolet', ['TRAVERSE'], [2025,2026], 'chevrolet-traverse-2025-2026-2.5t', ['LK0'])
rule('Chevrolet', ['TRAVERSE'], [2009,2014], 'chevrolet-traverse-2009-2017-3.6', ['NDA','NDB'], note='existing repo schedule; NDA/NDB = degem CR14526, 3564cc 281hp = 3.6 LLT per data.gov.il model table')
# Chrysler
rule('Chrysler', ['GRAND VOYAGER','TOWN COUNTRY','TOWN & COUNTRY'], [2011,2017], 'chrysler-grand-voyager-2011-2017-3.6', ['G'], ['בנזין','גפמ"'])
rule('Chrysler', ['JOURNEY','DODGE JOURNEY'], [2008,2014], 'dodge-journey-2008-2014-2.4-3.6', ['ED3','G'], ['בנזין'])
rule('Chrysler', ['PACIFICA'], [2017,2026], 'chrysler-pacifica-2017-2026-3.6', ['G'], ['בנזין'])
rule('Chevrolet', ['AVEO'], [2004,2011], 'chevrolet-aveo-optra-2004-2010-1.4-1.6', ['F14D3','F14D4'], note='sister: US 2008 Aveo (1.6 F16D3 E-TEC II) schedule; F14D4 is the later 1.4 of the same family')
rule('Chevrolet', ['OPTRA','OPTRA LS'], [2004,2011], 'chevrolet-aveo-optra-2004-2010-1.4-1.6', ['F16D3'], note='sister: same F16D3 engine as the US 2004-2008 Aveo')
# Isuzu (existing repo schedules)
rule('Isuzu', ['PICK-UP','PICK - UP','PICK -UP','D-MAX'], [2007,2011], 'isuzu-d-max-2007-2011-3.0-diesel', ['4JK1'], ['דיזל'], note='existing repo schedule; sister: 4JK1 (2.5) is the smaller version of the 4JJ1 family in the same TF D-Max; the KB P190 workshop manual covers 4JK1 vehicles but its GENERAL EXPORT schedule rows name only 4JJ1 - verify')
rule('Isuzu', ['PICK -UP'], [2012,2020], 'isuzu-d-max-2012-2020-2.5-1.9-diesel', ['4JK1','RZ4E','4JJ1'], ['דיזל'], note='existing repo schedule; adds the name spelling PICK -UP missing from the current rule')
rule('Isuzu', ['PICK-UP','PICK - UP','PICK -UP'], [2021,2026], 'isuzu-d-max-2021-2026-1.9-diesel', ['RZ4E'], ['דיזל'], note='existing repo schedule; current rule lists only D-MAX')
rule('SsangYong', ['RODIUS','REXTON'], [2016,2019], 'ssangyong-rodius-rexton-w-2016-2019-2.2-diesel', ['672.960'], ['דיזל'], note='sister: Rexton 2018 Hebrew book D22DTR table; same engine')
rule('Chrysler', ['GRAND VOYAGER','TOWN COUNTRY'], [2008,2011], 'chrysler-grand-voyager-2008-2010-3.8', ['EGL'], ['בנזין','גפמ"'])
rule('Chrysler', ['PATRIOT','JEEP PATRIOT','CALIBER','DODGE CALIBER'], [2007,2012], 'jeep-patriot-dodge-caliber-2007-2012-2.0-2.4', ['ED3','ECN'], ['בנזין'])
rule('Chrysler', ['COMPASS','JEEP COMPASS'], [2007,2016], 'jeep-patriot-dodge-caliber-2007-2012-2.0-2.4', ['ED3','ECN'], ['בנזין'], note='sister: Compass MK is the Patriot twin (same platform and World Engine)')
rule('Chevrolet', ['CAPTIVA'], [2011,2012], 'chevrolet-captiva-sport-2012-2015-2.4', ['LE5'], ['בנזין'], note='existing repo schedule; sister: Captiva C100 with 2.4 LE5 = same body/engine family as the US Captiva Sport 2012 (LE5) - verify')
