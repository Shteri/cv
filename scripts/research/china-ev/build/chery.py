from sched import *
import jaecoo
IMPC = "פריסבי (צ'רי ישראל)"
NOSRC = {'url': 'https://cheryisrael.co.il/', 'kind': 'importer', 'note': 'אתר צ\'רי ישראל (פריסבי) אינו מפרסם ספרי רכב או לוחות טיפולים; נבדק גם WordPress media API - רק מפרטים וקטלוגים'}
def sister(fn, id, model, model_he, years, engines, book, rules, make='Chery', make_he="צ'רי", importer=IMPC, gen=None):
    note = (f'טיוטה - דגם אח: לא נמצא ספר רכב עברי או לוח טיפולים של היבואן ל-{model}. הלוח הועתק מספר הרכב העברי של {book} (כלמוביל), '
            f'שלפי קוד המנוע במאגר הרישוי חולק איתו את אותה יחידת הנעה. יש לוודא מול היבואן.')
    s = fn(meta={'id': id, 'make': make, 'make_he': make_he, 'model': model, 'model_he': model_he, 'years': years, 'engines': engines,
                 'importer': importer, 'status': 'draft', 'generation': gen or model}, extra_note=note, rule=False, extra_src=NOSRC if make == 'Chery' else None)
    for names, yrs, kw in rules: s.rule(make, names, yrs, **kw)
    return s
P = "ג'אקו 7 PHEV"
sister(jaecoo.j7phev, 'chery-tiggo-8-pro-phev-2025-2026-1.5t-phev', 'Tiggo 8 Pro PHEV', "טיגו 8 פרו PHEV", [2025, 2026], ['1.5 TGDI PHEV (SQRH4J15) + DHT'], P, [(['TIGGO8PRO PHEV', 'TIGGO 8 PRO PHEV'], [2025, 2026], {})])
sister(jaecoo.j7phev, 'chery-tiggo-7-pro-phev-2025-2026-1.5t-phev', 'Tiggo 7 Pro PHEV', "טיגו 7 פרו PHEV", [2025, 2026], ['1.5 TGDI PHEV (SQRH4J15) + DHT'], P, [(['TIGGO7 PRO PHEV', 'TIGGO 7 PRO PHEV'], [2025, 2026], {})])
sister(jaecoo.j7phev, 'chery-arrizo-8-phev-2025-2026-1.5t-phev', 'Arrizo 8 PHEV', "אריזו 8 PHEV", [2025, 2026], ['1.5 TGDI PHEV (SQRH4J15) + DHT'], P, [(['ARRIZO 8 PHEV', 'ARRIZO8 PHEV'], [2025, 2026], {})])
sister(jaecoo.j7phev, 'chery-tiggo-9-phev-2025-2026-1.5t-phev', 'Tiggo 9 PHEV', "טיגו 9 PHEV", [2025, 2026], ['1.5 TGDI PHEV (SQRH4J15) + DHT'], P, [(['TIGGO 9 PHEV', 'TIGGO9 PHEV'], [2025, 2026], {})])
H = "ג'אקו 5 HEV"
sister(jaecoo.j5hev, 'chery-fx-hev-2025-2026-1.5-hev', 'FX HEV', 'FX היברידי', [2025, 2026], ['1.5 hybrid (SQRH4J15) + DHT'], H, [(['FX HEV'], [2025, 2026], {})])
sister(jaecoo.j5hev, 'chery-tiggo-7-hev-2026-1.5-hev', 'Tiggo 7 HEV', 'טיגו 7 היברידי', [2026, 2026], ['1.5 hybrid (SQRH4J15) + DHT'], H, [(['TIGGO 7 HEV', 'TIGGO7 HEV'], [2026, 2026], {})])
J = "ג'אקו 5 (בנזין, מנוע SQRF4J16C ותיבת 730DHB)"
sister(jaecoo.j5, 'chery-tiggo-8-pro-2022-2026-1.6t', 'Tiggo 8 Pro', 'טיגו 8 פרו', [2022, 2026], ['1.6 TGDI (SQRF4J16) + 7DCT'], J, [(['TIGGO 8 PRO', 'TIGGO8 PRO'], [2022, 2026], {'fuel': ['בנזין']})])
sister(jaecoo.j5, 'chery-tiggo-7-pro-2022-2026-1.6t', 'Tiggo 7 Pro', 'טיגו 7 פרו', [2022, 2026], ['1.6 TGDI (SQRF4J16) + 7DCT'], J, [(['TIGGO 7 PRO', 'TIGGO7 PRO'], [2022, 2026], {'fuel': ['בנזין']})])
sister(jaecoo.j5, 'chery-fx-2022-2026-1.6t', 'FX', 'FX', [2022, 2026], ['1.6 TGDI (SQRF4J16) + 7DCT'], J, [(['FX'], [2022, 2026], {'fuel': ['בנזין']})])
sister(jaecoo.j5, 'jaecoo-7-2024-2025-1.6t', 'Jaecoo 7', "ג'אקו 7", [2024, 2025], ['1.6 TGDI (SQRF4J16F) + 7DCT'], J, [(['JAECOO7', 'JAECOO 7'], [2024, 2025], {'fuel': ['בנזין']})],
       make='Jaecoo', make_he="ג'אקו", importer='כלמוביל')
save_rules('chery')
