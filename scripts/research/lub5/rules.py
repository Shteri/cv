import json
OUT='/tmp/claude-0/-home-user-cv/519cb72b-7b93-59d3-bcdf-37f8177b3821/scratchpad/staging/lub5/registry/'
B='בנזין'; D='דיזל'
R = [
 # MG new rows
 {"make":"MG","names":["HS HYBRID"],"years":[2025,2026],"fuel":[B],"engine_codes":["15FKE"],"schedule":"mg-hs-hybrid-2025-2026-1.5-hybrid"},
 {"make":"MG","names":["HS"],"years":[2025,2026],"fuel":[B],"engine_codes":["15FDE"],"schedule":"mg-hs-2025-2026-1.5t"},
 {"make":"MG","names":["MG4 ELECTRIC"],"years":[2023,2026],"fuel":["חשמל"],"schedule":"mg-4-2023-2026-ev"},
 {"make":"MG","names":["MG5 ELECTRIC"],"years":[2023,2024],"fuel":["חשמל"],"schedule":"mg-5-2023-2024-ev"},
 {"make":"MG","names":["CYBERSTER"],"years":[2025,2026],"fuel":["חשמל"],"schedule":"mg-4-2023-2026-ev"},
 {"make":"MG","names":["MARVEL R"],"years":[2022,2022],"schedule":"mg-marvel-r-2023-2024-ev"},
 # Citroen, Israeli 2009 booklet
 {"make":"Citroen","names":["C4","C3"],"years":[2002,2010],"fuel":[B],"engine_codes":["NFU"],"schedule":"citroen-c4-c3-2004-2010-1.6-16v"},
 {"make":"Citroen","names":["C3","C4","DS3","C3 PICASSO"],"years":[2009,2015],"fuel":[B],"engine_codes":["5FS","5F01","5FW"],"schedule":"citroen-c3-c4-ds3-2009-2015-1.6-vti"},
 {"make":"Citroen","names":["C5","C4 PICASSO","C4"],"years":[2006,2011],"fuel":[B],"engine_codes":["RFJ"],"schedule":"citroen-c5-c4-picasso-2006-2011-2.0"},
 {"make":"Citroen","names":["JUMPY","JUMPY HDI"],"years":[2004,2017],"fuel":[D],"engine_codes":["RH02","RHK","RHZ"],"schedule":"citroen-jumpy-berlingo-2004-2017-2.0-hdi"},
 {"make":"Citroen","names":["BERLINGO"],"years":[2002,2008],"fuel":[D],"engine_codes":["RHY"],"schedule":"citroen-jumpy-berlingo-2004-2017-2.0-hdi"},
 {"make":"Citroen","names":["C-ELYSEE","C ELYSEE"],"years":[2013,2016],"fuel":[B],"engine_codes":["NFP"],"schedule":"citroen-c-elysee-2013-2014-1.6-vti"},
 {"make":"Citroen","names":["C5","C4 GD PICASSO","C4 PICASSO","GRAND C4 PICASSO"],"years":[2011,2016],"fuel":[B],"engine_codes":["5F02"],"schedule":"citroen-c4-picasso-c5-aircross-2011-2023-1.6-thp"},
 # Peugeot sisters (draft)
 {"make":"Peugeot","names":["207","208","2008","308","308 SALOON","308SW","308 SW"],"years":[2007,2016],"fuel":[B],"engine_codes":["5FS","5FW","5F01","5FS-5F01"],"schedule":"peugeot-207-208-308-2008-2016-1.6-vti"},
 {"make":"Peugeot","names":["206","206+","307","PARTNER"],"years":[2000,2012],"fuel":[B],"engine_codes":["NFU","KFW","KFT"],"schedule":"peugeot-206-307-partner-2002-2012-1.4-1.6"},
 {"make":"Peugeot","names":["407","307"],"years":[2004,2011],"fuel":[B],"engine_codes":["RFJ"],"schedule":"peugeot-407-307-2006-2011-2.0"},
 {"make":"Peugeot","names":["301"],"years":[2013,2017],"fuel":[B],"engine_codes":["NFP"],"schedule":"peugeot-301-2013-2016-1.6-vti"},
 {"make":"Peugeot","names":["508","3008","5008","RCZ"],"years":[2010,2016],"fuel":[B],"engine_codes":["5F02"],"schedule":"peugeot-3008-5008-508-2010-2023-1.6-thp"},
]
json.dump(R, open(OUT+'registry_rules.json','w'), ensure_ascii=False, indent=1)
# Rows that are ALREADY matched by older draft rules; these new rules point them at the reviewed files.
# They only win if the lead puts them before the existing Citroen BERLINGO / C3 PICASSO rules (same specificity).
O = [
 {"make":"Citroen","names":["BERLINGO"],"years":[2008,2013],"fuel":[D],"engine_codes":["9HX","9HW","9H02","9HP","9HN","9H06","9HF"],"schedule":"citroen-berlingo-c3-c4-2008-2013-1.6-hdi"},
 {"make":"Citroen","names":["C3","C3 PICASSO","C4"],"years":[2009,2013],"fuel":[D],"engine_codes":["9HP","9H06","9HR","9H05","9HX","9HZ"],"schedule":"citroen-berlingo-c3-c4-2008-2013-1.6-hdi"},
 {"make":"Citroen","names":["JUMPY HDI","JUMPY"],"years":[2007,2012],"fuel":[D],"engine_codes":["9HU"],"schedule":"citroen-jumpy-2007-2012-1.6-hdi"},
]
json.dump({"_note":"These rows are currently matched by existing draft rules (citroen-berlingo-2008-2019-1.6-hdi, citroen-c3-c4-picasso-cactus-2010-2018-1.6-hdi). The new reviewed files come from the Israeli importer booklet. To use them, insert these rules BEFORE the existing ones (same specificity, first wins) or narrow the old rules' years.","rules":O}, open(OUT+'registry_rules_override.json','w'), ensure_ascii=False, indent=1)
print(len(R), len(O))
