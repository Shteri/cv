import json
OUT = "/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/tail4/registry/registry_rules.json"
R = []
def rule(make, names, years, schedule, note, engine_codes=None, fuel=None):
    r = {"make": make, "names": names, "years": years}
    if fuel: r["fuel"] = fuel
    if engine_codes: r["engine_codes"] = engine_codes
    r["schedule"] = schedule; r["_note"] = note
    R.append(r)

# ---------------- Toyota: name variants of existing Union-sheet schedules ----------------
rule("Toyota", ["COROLLA TS", "TOYOTA COROLLA", "COROLLA SDN HV", "COROLLA HEV", "COROLLA TS HV"], [2019, 2026], "toyota-corolla-2019-2025-1.8-hybrid",
     "name variants of the E210 1.8 hybrid (engine 2ZR = 2ZR-FXE hybrid; the E210 petrol is 1ZR)", engine_codes=["2ZR"])
rule("Toyota", ["COROLLA"], [2019, 2026], "toyota-corolla-2019-2025-1.8-hybrid",
     "CHANGES AN EXISTING MATCH: the repo rule COROLLA 2019-2026 (no engine codes) sends E210 rows with engine 2ZR (= 1.8 hybrid) to the 1.6 petrol file; this engine-code rule sends them to the hybrid file", engine_codes=["2ZR"])
rule("Toyota", ["COROLLA SEDAN", "COROLLA"], [2021, 2023], "toyota-corolla-2019-2025-1.6",
     "Turkish-built E210 sedan with 1.5 Dynamic Force (M15A-FKS) petrol; the Union Motors books API returns only the petrol sheet 'קורולה סדאן בנזין' (fileId 327, the source of this schedule) for Corolla Sedan 2021-2022, so the importer services it on that sheet", engine_codes=["M15A"])
rule("Toyota", ["YARIS HEV"], [2020, 2026], "toyota-yaris-2020-2025-1.5-hybrid", "name variant (HEV = hybrid), engine M15A(-FXE)", engine_codes=["M15A", "M15AFXE"])
rule("Toyota", ["YARIS CROSS HYB"], [2021, 2026], "toyota-yaris-cross-2021-2025-1.5-hybrid", "name variant of Yaris Cross hybrid", engine_codes=["M15A", "M15AFXE"])
rule("Toyota", ["D/F HILUX VIGO", "HILUX VIGO S"], [2005, 2015], "toyota-hilux-2005-2015-2.5-3.0-diesel", "name variants of Hilux Vigo with 2KD/1KD (same Union sheets 295/296)", engine_codes=["2KD", "1KD", "2KD-FTV", "1KD-FTV"])
rule("Toyota", ["TOYOTA CITY VAN"], [2020, 2026], "toyota-city-2020-2026-1.5-diesel", "name variant: Union Motors lists 'TOYOTA CITY VAN' under model TOYOTA_CITY (sheet 'TOYOTA CITY VAN'), engine YH01 = 1.5 BlueHDi", fuel=["דיזל"])
rule("Toyota", ["LAND CRUISER", "LAND CRIUSER"], [2015, 2019], "toyota-land-cruiser-2016-2019-2.8-diesel",
     "J150 facelift 2.8 D-4D (1GD) registered as 2015 and the misspelling LAND CRIUSER; same engine/generation as the 2016-2019 Union sheet 299", engine_codes=["1GD", "1GD-FTV", "1GDFTV"])
rule("Toyota", ["LAND CRUISER", "LAND CRIUSER"], [2020, 2024], "toyota-land-cruiser-2020-2024-2.8-diesel", "engine code spelling 1GDFTV", engine_codes=["1GDFTV"])
rule("Toyota", ["LAND CRUISER", "LAND CRIUSER"], [2025, 2026], "toyota-land-cruiser-2025-2026-2.8-diesel", "engine code spelling 1GDFTV", engine_codes=["1GDFTV"])
rule("Toyota", ["RAV-4 HYBRID", "RAV4 HEV"], [2020, 2026], "toyota-rav4-2020-2025-2.5-hybrid", "name variants of RAV4 hybrid (A25A)", engine_codes=["A25A", "A25AFXS", "A25A-FXS"])
rule("Toyota", ["C-HR HYBRIB", "CHR"], [2017, 2023], "toyota-c-hr-2016-2023-1.8-hybrid", "misspellings of C-HR hybrid (2ZR) for the first generation", engine_codes=["2ZR", "2ZR-FXE"])
rule("Toyota", ["CAMRY HEV", "CAMRY HYBRIDE"], [2020, 2026], "toyota-camry-2020-2025-2.5-hybrid", "name variants of Camry hybrid (A25A)", engine_codes=["A25A", "A25AFXS"])
rule("Toyota", ["HIGHLANDER HV", "HIGHLANDER HYBR"], [2020, 2026], "toyota-highlander-2021-2025-2.5-hybrid", "name variants of Highlander hybrid (A25A)", engine_codes=["A25A", "A25A-FXS", "A25AFXS"])
rule("Toyota", ["PRIUS HYBRID", "PRIUS"], [2010, 2010], "toyota-prius-2004-2009-1.5-hybrid", "NHW20 with 1NZ registered as 2010 (last stock)", engine_codes=["1NZ", "1NZ-FXE"])

# ---------------- Toyota: new files from unused Union sheets ----------------
rule("Toyota", ["C-HR HEV", "CHR", "CH-R", "TOYOTA CH-R", "C-HR", "TOYOTA C-HR", "C-HR HYBRID", "TOYOTA C-HR HYBRID"], [2024, 2026], "toyota-c-hr-2024-2026-1.8-hybrid",
     "second-generation C-HR hybrid. Union Motors API returns only sheet 362 (and the 'C-HR HEV 2024' book) for C-HR Hybrid 2024-2025. CHANGES EXISTING MATCHES for C-HR/TOYOTA C-HR/C-HR HYBRID 2024-2026 (repo rules send them to the first-generation file); fuel is set so this rule is more specific",
     engine_codes=["2ZR", "2ZR-FXE", "2ZRFXE"], fuel=["בנזין"])
rule("Toyota", ["AYGO X HYBRID", "AYGO X HV", "AYGO X HEV"], [2026, 2026], "toyota-aygo-x-2026-1.5-hybrid", "Union sheet 'טבלת טיפולים - Aygo X HV' (model aygo-x-hybrid, 2026)", engine_codes=["M15A", "M15AFXE", "M15A-FXE"])
rule("Toyota", ["LAND CRUISER", "LAND CRISER", "LAND CRIUSER", "PRADO"], [2003, 2008], "toyota-land-cruiser-2003-2008-4.0", "J120 Prado 4.0 V6 petrol incl. LPG conversions (draft file from the J150 1GR-FE sheet)", engine_codes=["1GR", "1GR-FE"])

rule("Toyota", ["PROACE", "PROACE VERSO"], [2016, 2026], "toyota-proace-2017-2026-2.0-diesel", "Proace (PSA Expert/Jumpy K0) 2.0 BlueHDi; AH01 = DW10F family per the Union sheets", fuel=["דיזל"])
# ---------------- Mazda ----------------
rule("Mazda", ["BT 50"], [2007, 2026], "mazda-bt-50-2007-2026-diesel", "name spelling 'BT 50' (space); Delek plan covers BT-50 from 2007", fuel=["דיזל"])
rule("Mazda", ["MAZDA 6 WAGON", "MAZDA 6 SW"], [2013, 2026], "mazda-6-2013-2025", "wagon name variants of the GJ/GL Mazda6 (PE/PY), same Delek plan")
rule("Mazda", ["MX 5"], [2006, 2014], "mazda-mx-5-2007-2014-1.8-2.0", "name spelling 'MX 5'; NC generation with LF 2.0 (sold from MY2006)", engine_codes=["LF", "L8"])

# ---------------- Hyundai / Kia ----------------
rule("Hyundai", ["SANTA FE HEV", "SANTA FE HYBRID"], [2021, 2023], "hyundai-santa-fe-2021-2023-2.5-2.2", "TM facelift 1.6 T-GDI hybrid (G4FT); the 2021-2023 Colmobil schedule lists the hybrid engine", engine_codes=["G4FT", "G4FT*"])
rule("Hyundai", ["ELANTRA HYBRID"], [2021, 2021], "hyundai-elantra-2022-2026-1.6-hybrid", "CN7 hybrid (G4LE) registered as MY2021; the only Elantra hybrid generation", engine_codes=["G4LE"])
rule("Kia", ["SPORTAGE"], [2010, 2015], "kia-sportage-2011-2015", "LPG-converted SL 2.0 MPI (G4KD); the existing rule is petrol-only", engine_codes=["G4KD"], fuel=['גפמ"'])
rule("Kia", ["SORENTO"], [2021, 2026], "kia-sorento-2021-2026-2.5-2.2", "Smartstream D2.2 = D4HE (existing rule lists only D4HB); same as hk3 suggestion", engine_codes=["D4HE"])
rule("Kia", ["CERATO"], [2008, 2013], "kia-forte-2009-2013-1.6", "Cerato = Forte TD with Gamma 1.6 MPI G4FC", engine_codes=["G4FC"])

rule("Hyundai", ["ELANTRA N"], [2024, 2026], "hyundai-elantra-n-2025-2026-2.0-turbo", "Elantra N 2.0 T-GDI (G4KH), Colmobil Hebrew book", engine_codes=["G4KH"])

rule("Suzuki", ["LIANA", "ליאנה"], [2001, 2008], "suzuki-liana-2002-2008-1.6", "Liana 1.6 M16A (Latin and Hebrew registry names)", engine_codes=["M16A"])

rule("Hyundai", ["GENESIS  GV70", "GENESIS GV70", "GV70"], [2021, 2026], "genesis-gv70-2021-2026-2.5-turbo", "Genesis is registered under Hyundai with a double space in the name; 2.5T G4KR", engine_codes=["G4KR"])
rule("Hyundai", ["GENESIS  G80", "GENESIS G80", "G80"], [2021, 2026], "genesis-g80-2021-2026-2.5-turbo", "Genesis G80 2.5T G4KR (sister draft from GV70)", engine_codes=["G4KR"])

rule("Hyundai", ["GENESIS  GV60", "GENESIS GV60", "GV60"], [2022, 2026], "genesis-gv60-2022-2026-ev", "Genesis GV60 EV (E-GMP, EM17/EM18); sister draft from the Colmobil Ioniq 5 book", fuel=["חשמל"])

rule("Kia", ["OPTIMA"], [2012, 2018], "kia-optima-2012-2018-1.7-diesel", "Optima 1.7 CRDi D4FD (sister draft from Israeli Carens D4FD book)", engine_codes=["D4FD"], fuel=["דיזל"])
rule("Kia", ["OPTIMA HEV", "OPTIMA HYBRID", "OPTIMA PHEV"], [2016, 2021], "kia-optima-2016-2020-2.0-hybrid", "Optima JF hybrid G4NG (sister of Sonata LF hybrid)", engine_codes=["G4NG"])
rule("Kia", ["SORENTO", "SORENT0"], [2010, 2012], "kia-sorento-2010-2012-2.4", "Sorento XM 2.4 G4KE incl. registry typo SORENT0 (sister of Santa Fe CM 2.4)", engine_codes=["G4KE"])
rule("Kia", ["FORTE", "CERATO"], [2016, 2018], "kia-forte-2016-2018-1.6-diesel", "Forte/Cerato YD 1.6 CRDi D4FB (sister of Ceed JD diesel)", engine_codes=["D4FB"], fuel=["דיזל"])
rule("Kia", ["SOUL"], [2011, 2017], "kia-soul-2011-2017-1.6-diesel", "Soul 1.6 CRDi D4FB (sister of Ceed JD diesel)", engine_codes=["D4FB"], fuel=["דיזל"])

rule("Suzuki", ["IGNIS", "איגניס"], [2001, 2008], "suzuki-ignis-2001-2007-1.3", "first-generation Ignis 1.3 M13A (Latin and Hebrew names)", engine_codes=["M13A"])

rule("Suzuki", ["SX4CROSSOVER"], [2013, 2017], "suzuki-sx4-crossover-2014-2016-1.6", "name spelling without space", engine_codes=["M16A"])

rule("Suzuki", ["GRAND VITARA"], [1998, 2006], "suzuki-grand-vitara-1998-2005-1.6-2.0", "first-generation Grand Vitara 1.6 G16B (the existing J20A/J24B rule starts at 2005 = JT generation)", engine_codes=["G16B", "G16A"])
rule("Suzuki", ["GRAND VITARA"], [1998, 2004], "suzuki-grand-vitara-1998-2005-1.6-2.0", "first-generation Grand Vitara 2.0 J20A (SQ420) before the JT generation", engine_codes=["J20A"])

rule("Hyundai", ["MATRIX"], [2001, 2010], "hyundai-matrix-2001-2010-1.6-1.8", "Matrix FC 1.6 G4ED / 1.8", engine_codes=["G4ED", "G4GB"])
rule("Hyundai", ["ELANTRA"], [2000, 2007], "hyundai-elantra-2001-2006-1.6", "Elantra XD 1.6 G4ED (sister draft from Matrix FC, same platform and engine)", engine_codes=["G4ED"])

rule("Hyundai", ["STARIA HYBRID", "STARIA HEV"], [2024, 2026], "hyundai-staria-hybrid-2025-2026-1.6", "Staria 1.6 T-GDI hybrid G4FT (sister draft from Israeli Sorento MQ4 HEV book)", engine_codes=["G4FT", "G4FT*"])

rule("Hyundai", ["SONATA"], [2020, 2024], "hyundai-sonata-2020-2024-1.6-turbo", "Sonata DN8 1.6 T-GDI G4FP (sister draft from Colmobil Tucson NX4 book)", engine_codes=["G4FP"], fuel=["בנזין"])

rule("Kia", ["SPORTAGE"], [2010, 2015], "kia-sportage-2011-2015-2.0-diesel", "Sportage SL 2.0 CRDi D4HA (diesel table of the same Kia Israel book)", engine_codes=["D4HA"], fuel=["דיזל"])
rule("Hyundai", ["IX35", "IX 35"], [2010, 2015], "hyundai-ix35-2010-2015-2.0-diesel", "ix35 2.0 CRDi D4HA (sister draft from Sportage SL diesel)", engine_codes=["D4HA"], fuel=["דיזל"])
rule("Hyundai", ["IX35", "IX 35"], [2010, 2015], "hyundai-ix35-2010-2015-2.4", "ix35 2.4 G4KE (sister draft from Sportage SL)", engine_codes=["G4KE"])

def dump():
    json.dump(R, open(OUT, "w"), ensure_ascii=False, indent=1)
    print(len(R), "rules")
if __name__ == "__main__":
    dump()
