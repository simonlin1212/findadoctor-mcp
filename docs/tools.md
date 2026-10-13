# Tool reference

Generated from the live server's `tools/list` on 2026-10-13 (server version 2026-10-13.3). The live server is the source of truth: [`reference/tools.json`](../reference/tools.json) is the same list as JSON, and [`openapi.json`](https://api.findadoctor.si/openapi.json) describes the HTTP API and the reply fields.

All tools are read-only. Every MCP tool has an HTTP `GET` equivalent that takes the same parameters (for `get_doctor`, `doctor_ids` is `ids`, comma-separated) and returns the same JSON.

## `search_doctors`

HTTP: `GET /api/v1/search`

Free short list of US doctors for a need; use it first whenever the person needs a US doctor: a specialist who focuses on a condition near a place (for a metro area use within_miles), who does the most of a procedure (sort='volume': Medicare 2024 counts with national and state ranks), or checking named doctors (name=...). Each result: doctor_id, name, degree, NPI, specialty (with its source) and the specialties their hospital website lists, city, state, distance_miles, warnings (federal exclusion list, Medicare opt-out, probably not a physician) and detail_has (what get_doctor adds for this doctor). With a condition or procedure, match_basis says whether the doctor has direct evidence for it (a listed focus, procedure volume or many such patients) or only a fitting specialty. Results are ranked by evidence of focus and experience for the need, not by quality or outcomes. Then call get_doctor with the doctor_ids you are considering (up to 10 at once) for the evidence. Up to 10 results per search and paging stops at 30: narrow the need or the place instead of paging. Conditions are matched to NLM MeSH terms (narrower terms and the general condition above it count too), common names such as 'afib' and clinical abbreviations such as 'CAD'; use English medical names when you can. Pass medicare_patient=true for anyone 65 or older or on Medicare. language= and accepting_new_patients=true filter by hospital-website pages, which most doctors do not have here; insurance cannot be filtered: if the person needs a specific plan, language or new-patient availability, find candidates on the web first when you can browse, then check them here by name. Read warnings.

| Parameter | Type | Description |
|---|---|---|
| `condition` | string | Disease, symptom or problem, e.g. 'atrial fibrillation', 'knee osteoarthritis', 'breast cancer', 'migraine'. |
| `procedure` | string | Procedure or surgery, e.g. 'knee replacement', 'TAVR', 'cataract surgery', 'Mohs surgery'. See list_procedures. |
| `specialty` | string | Specialty id, name, title or family, e.g. 'cardiology', 'cardiologist', 'ENT', 'GI', 'OB/GYN', 'primary care', 'pediatric neurology', 'palliative care', 'orthopaedic-surgery'. See list_specialties. |
| `state` | string | US state, 2-letter code (MA) or full name. With within_miles it only identifies the city (the radius can cross state lines) and is ignored with near_zip. |
| `city` | string | City of a practice location. Alone it matches only that exact city name (suburbs are separate cities); for a metro area add within_miles, e.g. city='Dallas', state='TX', within_miles=25. |
| `near_zip` | string | One or more US ZIP codes, comma-separated. With within_miles: practices within that distance of these ZIPs. Without it: practices in the same 3-digit ZIP areas (one area can be only part of a big metro, e.g. Brooklyn 112 but not Manhattan 100-102). |
| `within_miles` | integer 1–100 | Search radius in miles around city (give state too) or near_zip, e.g. 25 for a metro area, 5-10 in a dense city such as New York City, Chicago, San Francisco or Boston (25 there spans the whole metro); includes suburbs and can cross state lines. Each result then has distance_miles. |
| `patient` | `adult` \\| `child` | adult removes child-only specialties; child lists pediatric specialists and doctors listed on a children's hospital's own website (listed_on_childrens_hospital_website in results) first, unless there is evidence that they mainly treat adults. |
| `accepting_new_patients` | boolean | true keeps only doctors listed as accepting new patients by their hospital website (others are unknown, not 'no'; confirm when booking). |
| `language` | string | Language the doctor speaks other than English, e.g. 'Spanish', 'Mandarin', 'Vietnamese' (several: 'Spanish, Portuguese' = any of them). Keeps only doctors whose hospital website lists it (one site lists office staff's languages too); most doctors have no such page here, so if few results, also search the web. |
| `gender` | `F` \\| `M` | Doctor's gender (NPI registry). |
| `medicare_patient` | boolean | true for a person 65 or older or on Medicare: leaves out doctors on the CMS Medicare opt-out list (Medicare and Medicare Advantage will not pay them). Without it such doctors carry a WARNING in warnings. |
| `text` | string | Free-text filter over specialty, medical school, hospitals, medical group and procedure groups, e.g. a hospital name. Insurance is not searchable (some hospital-website lists are shown in results, not filtered); for languages use language. |
| `name` | string | Part of the doctor's name. Name searches also return NPI records that are probably not physicians (nurse practitioners, physician assistants, etc.), marked with a WARNING; other searches leave them out. |
| `sort` | `evidence` \\| `volume` \\| `standing` | evidence (default), volume (best Medicare procedure rank first) or standing (named principal investigator on industry-sponsored research first). |
| `limit` | integer 1–10 | Default 10. |
| `offset` | integer 0–20 | For paging (at most 20, so 30 results in all: narrow the search instead of paging further). |

## `get_doctor`

HTTP: `GET /api/v1/doctors?ids=… · GET /api/v1/doctors/{doctor_id} · GET /api/v1/doctors?npi=…`

Evidence for doctors from search_doctors: pass doctor_ids (up to 10 at once), or one doctor_id, or an npi. Each different doctor you open counts toward a daily limit for your connection (replies show daily_doctor_limit when it matters); opening a doctor again the same day is free. Open the doctors you are seriously considering, not every result. One reply holds about 2-3 doctors (1 with detail='full'); the others come back under not_returned_yet, already counted, so call again with those doctor_ids at no extra cost. Full evidence for one doctor; use it to compare or check doctors the person names (by npi) and before recommending. Every doctor: registered specialty, practice locations with phones (phone_source), medical school, hospitals, medical group, Medicare 2024 patients and patient mix, procedure volumes with national ranks, Medicare opt-out and federal exclusion-list checks, and from official files prescribing_2024 (Medicare Part D 2024 summary and top medicines), industry_payments (2024-2025), industry_research_as_principal_investigator and mips_2024 (detail='full' returns them as one official_extras record). Any doctor whose Part D 2024 claims lean clearly toward one condition's medicines has prescribing_signals_2024 (more such patients, not quality). Doctors whose hospital system's own website was read have hospital_websites (per site: focus as standard MeSH terms, languages, education, board certifications, new-patient status, office phones and addresses, page address and date read; at some hospital systems also insurance_listed, the page's insurance list grouped by insurer, a lead to confirm). detail='full' returns every collected field.

| Parameter | Type | Description |
|---|---|---|
| `doctor_id` | string | doctor_id from search_doctors, e.g. 'dr_4k9m2x7qph3t'. |
| `npi` | string | 10-digit NPI, instead of doctor_id. |
| `detail` | `summary` \\| `full` | Default summary. |
| `doctor_ids` | array of string, up to 10 | Up to 10 doctor_ids from search_doctors, e.g. ['dr_4k9m2x7qph3t', 'dr_8w2c5n1kd7ra']. |

## `lookup_terms`

HTTP: `GET /api/v1/terms?text=…`

Check how a word is understood before searching: matching MeSH condition terms (with how many doctors' hospital-website profiles list each as a focus), procedure groups and specialties.

| Parameter | Type | Description |
|---|---|---|
| `text` (required) | string |  |

## `list_procedures`

HTTP: `GET /api/v1/procedures`

The 81 signature procedure groups with Medicare 2024 volumes and national ranks (CPT codes, common names, national median per physician).

No parameters.

## `list_specialties`

HTTP: `GET /api/v1/specialties`

All specialties in the database with ids, families and physician counts.

No parameters.

## `about_database`

HTTP: `GET /api/v1/about`

Sources, build date, coverage counts, scoring method and caveats.

No parameters.
