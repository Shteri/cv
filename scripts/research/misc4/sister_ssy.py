import json
from lib import write, OUT
d = json.load(open(OUT + '/ssangyong-rexton-2018-2021-2.2-diesel.json'))
d.update(id='ssangyong-rodius-rexton-w-2016-2019-2.2-diesel', model='Rodius / Rexton W', model_he='רודיוס / רקסטון W',
         generation='Rodius II (Turismo) / Rexton W', years=[2016,2019], engines=['2.2 טורבו דיזל (D22DTR, קוד רישוי 672.960)'], status='draft')
d['sources'] = d['sources'] + [{'url': 'https://kgm.co.il/ספרי-רכב/', 'kind': 'importer', 'note': 'באתר KGM ישראל אין ספר נהג לרודיוס או לרקסטון W; נבדק גם WordPress media API של האתר'}]
d['notes'] = 'טיוטה (דגם אחות): נלקח מטבלת D22DTR הכללית בספר הנהג העברי של רקסטון 2018 (אותו מנוע 2.2 דיזל, הנעה אחורית/4x4 עם תיבת העברה). ספר נהג של רודיוס או רקסטון W לא נמצא. ' + d['notes']
write(d)
