// Look up an Israeli licence plate in the government vehicle registry
// (data.gov.il, dataset "כלי רכב פרטיים ומסחריים") and return the fields the
// app needs. No dependencies. Usage:
//
//   node scripts/lookup_plate.mjs 5714838
//
// The API refuses requests without a browser-like User-Agent (returns 403).

const RESOURCE = "053cea08-09bc-40ec-8f7a-156f0677aff3";
const UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0 Safari/537.36";

export async function lookupPlate(plate) {
  const digits = String(plate).replace(/\D/g, "");
  if (digits.length < 5 || digits.length > 8) throw new Error("plate must have 5-8 digits");
  const url = new URL("https://data.gov.il/api/3/action/datastore_search");
  url.searchParams.set("resource_id", RESOURCE);
  url.searchParams.set("filters", JSON.stringify({ mispar_rechev: Number(digits) }));
  url.searchParams.set("limit", "1");
  const res = await fetch(url, { headers: { "User-Agent": UA, Accept: "application/json" } });
  if (!res.ok) throw new Error(`data.gov.il returned ${res.status}`);
  const data = await res.json();
  const r = data?.result?.records?.[0];
  if (!r) return null;
  return {
    plate: r.mispar_rechev,
    make_raw: r.tozeret_nm,            // e.g. "סיאט ספרד" (maker + country of build)
    make: normalizeMake(r.tozeret_nm),
    model_name: r.kinuy_mishari,        // commercial name, e.g. "IBIZA", "COROLLA"
    model_code: r.degem_nm,             // manufacturer type code, e.g. "6J-6P12KZ"
    trim: r.ramat_gimur,
    year: r.shnat_yitzur,
    on_road: r.moed_aliya_lakvish,      // "YYYY-M"
    engine_code: r.degem_manoa,
    fuel: r.sug_delek_nm,               // "בנזין" / "דיזל" / "חשמל/בנזין" (hybrid)
    last_test: r.mivchan_acharon_dt,
    test_valid_until: r.tokef_dt,
    ownership: r.baalut,
    vin: r.misgeret,
    tires: { front: r.zmig_kidmi, rear: r.zmig_ahori },
  };
}

// The registry writes the maker with its country ("טויוטה יפן", "יונדאי קוריאה").
// Strip the country and map to the make names used in data/models.json.
const MAKES = [
  ["טויוטה", "Toyota"], ["אלפא", "Alfa Romeo"], ["יונדאי", "Hyundai"], ["קיה", "Kia"], ["סקודה", "Skoda"],
  ["מאזדה", "Mazda"], ["מזדה", "Mazda"], ["מיצובישי", "Mitsubishi"], ["פורד", "Ford"], ["סיאט", "Seat"],
  ["פולקסווגן", "Volkswagen"], ["סוזוקי", "Suzuki"], ["ניסאן", "Nissan"], ["הונדה", "Honda"],
  ["שברולט", "Chevrolet"], ["סובארו", "Subaru"], ["רנו", "Renault"], ["פיג'ו", "Peugeot"], ["פיגו", "Peugeot"], ["די אס", "DS"],
  ["סיטרואן", "Citroen"], ["אופל", "Opel"], ["צ'רי", "Chery"], ["ב.מ.וו", "BMW"], ["מרצדס", "Mercedes-Benz"],
  ["אאודי", "Audi"], ["אודי", "Audi"], ["וולוו", "Volvo"], ["וולבו", "Volvo"], ["לקסוס", "Lexus"], ["דאציה", "Dacia"], ["דאצ'יה", "Dacia"], ["פיאט", "Fiat"],
  ["ב מ וו", "BMW"], ["בי ווי די", "BYD"], ["ג'אקו", "Jaecoo"], ["מ.ג", "MG"], ["גילי", "Geely"], ["איסוזו", "Isuzu"], ["טסלה", "Tesla"],
  ["מרוטי", "Suzuki"], ["דייהטסו", "Daihatsu"], ["אקספנג", "Xpeng"], ["קרייזלר", "Chrysler"], ["לינק אנד קו", "Lynk & Co"], ["ג'יפ", "Jeep"],
  ["זיקר", "Zeekr"], ["רובר", "Land Rover"], ["לנדרובר", "Land Rover"], ["דיפאל", "Deepal"], ["סרס", "Seres"], ["קאדילאק", "Cadillac"], ["סאנגיונג", "SsangYong"],
  ["קיי גי מוביליט", "KGM"], ["אומודה", "Omoda"], ["אורה", "ORA"], ["דיימלר", "Mercedes-Benz"], ["ליפמוטור", "Leapmotor"], ["מקסוס", "Maxus"],
  ["דונגפנג", "Dongfeng"], ["קופרה", "Cupra"], ["פורשה", "Porsche"], ["סמארט", "Smart"], ["סקיוול", "Skywell"], ["ביואיק", "Buick"], ["איווייס", "Aiways"], ["איויאיסי", "EVEC"],
];
export function normalizeMake(raw) {
  if (!raw) return null;
  for (const [he, en] of MAKES) if (raw.startsWith(he)) return en;
  return raw.split(" ")[0];
}

if (import.meta.url === `file://${process.argv[1]}`) {
  const plate = process.argv[2];
  if (!plate) { console.error("usage: node scripts/lookup_plate.mjs <plate>"); process.exit(2); }
  lookupPlate(plate).then(r => { console.log(JSON.stringify(r, null, 2)); if (!r) process.exit(1); })
    .catch(e => { console.error(e.message); process.exit(1); });
}
