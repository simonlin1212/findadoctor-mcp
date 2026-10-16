# Tool reference: one MCP address for every country

Generated from the live `tools/list` of `https://api.findadoctor.si/mcp` on 2026-10-16 (server version gw-2026-10-16.1). The live server is the source of truth: [`reference/tools.json`](../reference/tools.json) is the same list as JSON. The HTTP APIs and their reply fields are described per country in [`openapi.json`](https://api.findadoctor.si/openapi.json) (United States), [`openapi.json`](https://api-nz.findadoctor.si/openapi.json) (New Zealand) and [`openapi.json`](https://api-fr.findadoctor.si/openapi.json) (France). The New Zealand-only and France-only addresses have their own lists in [tools-nz.md](tools-nz.md) and [tools-fr.md](tools-fr.md).

This one address serves the United States, New Zealand and France. Decide the country first: where the person wants to see a doctor. If that is unclear (no place given, or a place name used in more than one country with no other clue), ask the person before searching; do not guess, and do not search every country. Then pass `country` (`US`, `NZ` or `FR`) to the tools that take it. The schema marks it required; a call without it still uses the United States, for clients set up before other countries were added. Doctor ids carry their country (`dr_` = United States, `nz_` = New Zealand, `fr_` = France), so `get_doctor` needs no `country`. Parameters marked (US only), (NZ only) or (FR only) work for that country only.

All tools are read-only. Each tool also has an HTTP `GET` equivalent on that country's own host, listed under the tool. It takes the same parameters except `country`, which the HTTP APIs do not accept (for `get_doctor`, `doctor_ids` is `ids`, comma-separated), and returns the same JSON.

Doctor ids in the descriptions below (such as `dr_4k9m2x7qph3t`, `dr_8w2c5n1kd7ra`, `fr_4k9m2x7qph3t`, `fr_8w2c5n1kd7ra`, `nz_4k9m2x7qph3t`, `nz_8w2c5n1kd7ra`) are placeholders written by the server, not real doctors.

## `search_doctors`

HTTP: United States `GET /api/v1/search` on `https://api.findadoctor.si`; New Zealand `GET /api/v1/search` on `https://api-nz.findadoctor.si`; France `GET /api/v1/search` on `https://api-fr.findadoctor.si`

Free short list of doctors for a need in one country; use it first whenever the person needs a doctor. Set country to where the person wants to be seen: United States (country=US), New Zealand (country=NZ), France (country=FR); if that is unclear, ask them before searching. Parameters marked (US only), (NZ only) or (FR only) work for that country only.

United States (country=US): Free short list of US doctors for a need; use it first whenever the person needs a US doctor: a specialist who focuses on a condition near a place (for a metro area use within_miles), who does the most of a procedure (sort='volume': Medicare 2024 counts with national and state ranks), or checking named doctors (name=...). Each result: doctor_id, name, degree, NPI, specialty (with its source) and the specialties their hospital website lists, city, state, distance_miles, warnings (federal exclusion list, Medicare opt-out, probably not a physician) and detail_has (what get_doctor adds for this doctor). With a condition or procedure, match_basis says whether the doctor has direct evidence for it (a listed focus, procedure volume or many such patients) or only a fitting specialty. Results are ranked by evidence of focus and experience for the need, not by quality or outcomes. Then call get_doctor with the doctor_ids you are considering (up to 10 at once) for the evidence. Up to 10 results per search and paging stops at 30: narrow the need or the place instead of paging. Conditions are matched to NLM MeSH terms (narrower terms and the general condition above it count too), common names such as 'afib' and clinical abbreviations such as 'CAD'; use English medical names when you can. Pass medicare_patient=true for anyone 65 or older or on Medicare. language= and accepting_new_patients=true filter by hospital-website pages, which most doctors do not have here; insurance cannot be filtered: if the person needs a specific plan, language or new-patient availability, find candidates on the web first when you can browse, then check them here by name. Read warnings.

New Zealand (country=NZ): Free short list of New Zealand doctors for a need; use it first whenever the person needs a doctor or specialist in New Zealand. Give at least one of need, specialty, place or name. need = a condition, procedure or focus in plain English (e.g. 'ACL reconstruction', 'endometriosis', 'skin cancer', 'cataract surgery'); it is matched against the focus areas doctors list first, then the procedures their services list, their specialty, and their own profile text (not shown here). specialty = a name from list_specialties, a word from one (e.g. 'orthopaedic', 'ENT') or a plain word (e.g. 'eye', 'skin', 'heart'); matched word by word (word endings may differ, e.g. 'cardiologist', 'paediatrician'; not fragments inside words), and the reply's specialty_read_as lists the specialty names used. place = a New Zealand city, suburb, or region or Health NZ district (e.g. 'Christchurch', 'North Shore', 'Hawke's Bay', 'Hutt Valley'); when a town search leaves out doctors listed only on the wider region's page or in its other towns, place_note says how many and which place to use instead. Each result: doctor_id, name, specialties, vocational scope, cities, sectors (private, public), match_basis (with a need: stated_focus, services_listed (the doctor's own or a small practice's service page), shared_service_listed (a hospital department or large group page they are linked to, so not necessarily done by this doctor), specialty, specialty_for_symptom (the need is a symptom few doctors list, and their specialty usually sees it; need_note says which specialties), profile_text or partial), place_match (with a place: city_or_address, city_in_region, address_contains or region_page_only), warnings (e.g. not practising on the Medical Council register), specialist_since (year first on the Medical Council vocational, i.e. specialist, register in New Zealand), recognition (New Zealand honours, University of Auckland title), listing (medical_council_register_only when the doctor has no clinic listing here), possibly_same_person_as (another entry with the same name that may be the same doctor) and detail_has (what get_doctor adds). General practitioners are left out unless specialty is general practice (e.g. 'GP') or a name is given; to find a GP clinic use search_gp_practices. Doctors only on the register are included when practising with a specialist scope (any status with a name). Results are ranked first by how directly the doctor's own listing matches the need (doctors who list all its words; then, when the need is a symptom such as back pain, doctors whose specialty usually sees it; then doctors who list some of the words; then words only in profile text), then by place_match (with a place); with experienced_first, longer as a specialist next. Doctors known only from the Medical Council register (no clinic listing) come after all others. Not ranked by quality or outcomes. Then call get_doctor with the doctor_ids you are considering. Up to 10 results per search and paging stops at 30: narrow the need or the place instead of paging.

France (country=FR): Free short list of doctors in France for a need; use it first whenever the person needs a doctor, specialist or GP in France. Give at least one of need, specialty, place, name or hospital_finess. need = condition, procedure or focus, in French or English (e.g. 'endométriose', 'prothèse genou', 'knee replacement', 'cataract'; common English words are also searched in French); matched against the expertise and procedures doctors state, their official competences and university diplomas, hospital departments and roles, and specialty. specialty = French or English (e.g. 'cardiologie', 'dermatology', 'pédiatre', 'ORL', 'GP', 'généraliste'). place = city ('Lyon', 'Paris' includes all arrondissements), postcode ('75015'), arrondissement ('Paris 15', 'Lyon 3e'), département number ('69', '2A') or a practice or hospital name; a text match on practice addresses, not a distance search. Each result: doctor_id, name, gender, specialties (French, as registered), specialties_en, places (up to 3 practices, the ones matching place first), fee_sectors (Ameli category: Secteur 1 = standard fees; Secteur 2 = may charge extra; Non conventionné = not contracted, little reimbursed), optam (agreed to limit extra fees), match_basis (with a need: stated_expertise, official_competence, hospital_department_or_training, several_fields, specialty, specialty_usually_treats, partial), register (rpps, ameli_only = only in the Assurance Maladie directory, website_only = not matched to the official registers), warnings (e.g. barred from practising) and detail_has (what get_doctor adds). With a need, results are ranked by how directly the doctor's own data matches it: all its words in the expertise or procedures the doctor states, then in official competences or university diplomas, then in hospital department, role or training, then spread over several fields, then in the specialty name; then, when the need is a condition few doctors list, doctors in the specialty that usually treats it (specialty_usually_treats); then doctors matching only some of the words. Without a need, doctors with more data (stated expertise, official competences, profile pages) come first, then in a fixed shuffled order. Not ranked by quality, outcomes, fees or industry links. Then call get_doctor with the doctor_ids you are considering. Up to 10 results per search and paging stops at 30: narrow the need or the place instead of paging.

| Parameter | Type | Description |
|---|---|---|
| `country` (required) | `US` \\| `NZ` \\| `FR` | Where the person wants to be seen: United States (country=US), New Zealand (country=NZ), France (country=FR). Decide it before searching; if unclear, ask the person. Older clients that leave it out get United States. |
| `condition` | string | (US only) Disease, symptom or problem, e.g. 'atrial fibrillation', 'knee osteoarthritis', 'breast cancer', 'migraine'. |
| `procedure` | string | (US only) Procedure or surgery, e.g. 'knee replacement', 'TAVR', 'cataract surgery', 'Mohs surgery'. See list_procedures. |
| `specialty` | string | US: Specialty id, name, title or family, e.g. 'cardiology', 'cardiologist', 'ENT', 'GI', 'OB/GYN', 'primary care', 'pediatric neurology', 'palliative care', 'orthopaedic-surgery'. See list_specialties. NZ: Specialty name, a word from one, or a plain word like 'eye' (see list_specialties). FR: Specialty in French or English, e.g. 'cardiologie', 'dermatology', 'ORL', 'GP' (see list_specialties). |
| `state` | string | (US only) US state, 2-letter code (MA) or full name. With within_miles it only identifies the city (the radius can cross state lines) and is ignored with near_zip. |
| `city` | string | (US only) City of a practice location. Alone it matches only that exact city name (suburbs are separate cities); for a metro area add within_miles, e.g. city='Dallas', state='TX', within_miles=25. |
| `near_zip` | string | (US only) One or more US ZIP codes, comma-separated. With within_miles: practices within that distance of these ZIPs. Without it: practices in the same 3-digit ZIP areas (one area can be only part of a big metro, e.g. Brooklyn 112 but not Manhattan 100-102). |
| `within_miles` | integer 1–100 | (US only) Search radius in miles around city (give state too) or near_zip, e.g. 25 for a metro area, 5-10 in a dense city such as New York City, Chicago, San Francisco or Boston (25 there spans the whole metro); includes suburbs and can cross state lines. Each result then has distance_miles. |
| `patient` | `adult` \\| `child` | (US only) adult removes child-only specialties; child lists pediatric specialists and doctors listed on a children's hospital's own website (listed_on_childrens_hospital_website in results) first, unless there is evidence that they mainly treat adults. |
| `accepting_new_patients` | boolean | (US only) true keeps only doctors listed as accepting new patients by their hospital website (others are unknown, not 'no'; confirm when booking). |
| `language` | string | US: Language the doctor speaks other than English, e.g. 'Spanish', 'Mandarin', 'Vietnamese' (several: 'Spanish, Portuguese' = any of them). Keeps only doctors whose hospital website lists it (one site lists office staff's languages too); most doctors have no such page here, so if few results, also search the web. NZ: Language other than English the doctor, or a small clinic (3 doctors or fewer) they work in, lists, e.g. 'Mandarin', 'Hindi', 'Samoan'. FR: Language other than French, e.g. 'English', 'Arabic', 'anglais'. Only known for doctors with a Maiia or hospital profile (about 1,800 list one); many others speak it too. |
| `gender` | `female` \\| `male` | female or male. US: Doctor's gender (NPI registry). NZ: Only when the person asks. Gender is recorded for only a small share of doctors (when their Healthpoint page states it); doctors without it are left out and gender_note says how many. FR: Only when the person asks. From the register's civil title (Madame/Monsieur); recorded for almost all doctors. |
| `medicare_patient` | boolean | (US only) true for a person 65 or older or on Medicare: leaves out doctors on the CMS Medicare opt-out list (Medicare and Medicare Advantage plans will not pay them except for emergency or urgent care). Without it such doctors carry a WARNING in warnings. |
| `text` | string | (US only) Free-text filter over specialty, medical school, hospitals, medical group and procedure groups, e.g. a hospital name. Insurance is not searchable (some hospital-website lists are shown in results, not filtered); for languages use language. |
| `name` | string | US: Part of the doctor's name. Name searches also return NPI records that are probably not physicians (nurse practitioners, physician assistants, etc.), marked with a WARNING; other searches leave them out. NZ: Doctor's name or part of it, to check a named doctor. FR: Doctor's name or part of it, to check a named doctor. |
| `sort` | `evidence` \\| `volume` \\| `standing` | (US only) evidence (default), volume (best Medicare procedure rank first) or standing (named principal investigator on industry-sponsored research first). |
| `limit` | integer 1–10 | Default 10. |
| `offset` | integer 0–20 | US: For paging (at most 20, so 30 results in all: narrow the search instead of paging further). NZ: For paging (at most 20, so 30 results in all: narrow the search instead). FR: For paging (at most 20, so 30 results in all: narrow the search instead). |
| `need` | string | NZ: Condition, procedure or focus, plain English. FR: Condition, procedure or focus, in French or English. |
| `place` | string | NZ: New Zealand city, suburb, or region or Health NZ district (e.g. 'Waikato', 'Hawke's Bay', 'Capital and Coast'). FR: City, postcode, arrondissement ('Paris 15'), département number ('69', '2A') or a practice or hospital name. |
| `sector` | `any` \\| `private` \\| `public` | (NZ only) private = the doctor lists a private service; public = a public (Health NZ) service. Default any. |
| `child` | boolean | (NZ only) True when the patient is a child: among doctors in the same place who match the need equally well, those in paediatrics or who list children in their focus come first, then those whose services say they see children; doctors whose services list only adult ages are left out. Most listings do not say, so those doctors stay in. |
| `southern_cross_affiliated` | boolean | (NZ only) True keeps doctors whose own Healthpoint page or at least one of whose service pages says Southern Cross Affiliated Provider (cover still depends on the policy and often prior approval; confirm). |
| `experienced_first` | boolean | (NZ only) True when the person wants an experienced or senior doctor: among doctors who match equally well, those longer on the New Zealand specialist (vocational) register come first. Time on the register is not quality, and doctors who trained overseas may have practised longer than it shows. |
| `fee_sector` | `any` \\| `secteur_1` \\| `secteur_1_or_optam` \\| `secteur_2` | (FR only) Assurance Maladie fee category. secteur_1 = standard fees, no extra charges; secteur_1_or_optam = standard fees or agreed limits on extra fees; secteur_2 = may charge extra. Kept if ANY of the doctor's practices has it (it can differ by practice): check each practice in get_doctor. Most hospital-only doctors have no category. Default any. |
| `online_booking` | boolean | (FR only) True keeps doctors whose Maiia or hospital page shows online booking (Doctolib is not covered). |
| `teleconsultation` | boolean | (FR only) True keeps doctors offering video consultations on Maiia. |
| `hospital_finess` | string | (FR only) Keep doctors whose register address is this hospital site (FINESS number from hospital_procedure_volumes): mostly salaried hospital doctors. |

## `get_doctor`

HTTP: United States `GET /api/v1/doctors?ids=… · GET /api/v1/doctors/{doctor_id} · GET /api/v1/doctors?npi=…` on `https://api.findadoctor.si`; New Zealand `GET /api/v1/doctors?ids=… · GET /api/v1/doctors/{doctor_id}` on `https://api-nz.findadoctor.si`; France `GET /api/v1/doctors?ids=… · GET /api/v1/doctors/{doctor_id}` on `https://api-fr.findadoctor.si`

Evidence for doctors from search_doctors, by doctor_id. The id says the country (dr_ = United States, nz_ = New Zealand, fr_ = France), so no country parameter is needed; open one country's doctors per call. Parameters marked (US only), (NZ only) or (FR only) work for that country only.

United States (dr_ ids): Evidence for doctors from search_doctors: pass doctor_ids (up to 10 at once), or one doctor_id, or an npi. Each different doctor you open counts toward a daily limit for your connection (replies show daily_doctor_limit when it matters); opening a doctor again the same day is free. Open the doctors you are seriously considering, not every result. One reply holds about 2-3 doctors (1 with detail='full'); the others come back under not_returned_yet, already counted, so call again with those doctor_ids at no extra cost. Full evidence for one doctor; use it to compare or check doctors the person names (by npi) and before recommending. Every doctor: registered specialty, practice locations with phones (phone_source), medical school, hospitals, medical group, Medicare 2024 patients and patient mix, procedure volumes with national ranks, Medicare opt-out and federal exclusion-list checks, and from official files prescribing_2024 (Medicare Part D 2024 summary and top medicines), industry_payments (2024-2025), industry_research_as_principal_investigator and mips_2024 (detail='full' returns them as one official_extras record). Any doctor whose Part D 2024 claims lean clearly toward one condition's medicines has prescribing_signals_2024 (more such patients, not quality). Doctors whose hospital system's own website was read have hospital_websites (per site: focus as standard MeSH terms, languages, education, board certifications, new-patient status, office phones and addresses, page address and date read; at some hospital systems also insurance_listed, the page's insurance list grouped by insurer, a lead to confirm). detail='full' returns every collected field.

New Zealand (nz_ ids): Evidence for New Zealand doctors from search_doctors: pass doctor_ids (up to 10 at once) or one doctor_id. Each different doctor you open counts toward a daily limit for your connection (replies show daily_doctor_limit when it matters); opening a doctor again the same day is free. Open the doctors you are seriously considering, not every result. Each doctor: specialties, title, qualifications, focus areas and subspecialties they list, further training, languages, whether their services see children; every private and public service with clinic addresses, phone numbers and websites, procedures and conditions the service lists, fee categories and fee lines, ages, hours, how to get referred, and whether it says Southern Cross Affiliated Provider or nib First Choice (insurer_notes also says whether the doctor's own page says so); the Medical Council register entry (status, scope of practice, conditions, qualifications, practising certificate); experience (each vocational scope with the date it was granted and years since, first New Zealand registration, primary medical degree year, New Zealand honours with citation, University of Auckland title and hospital appointments, approximate count of papers with a New Zealand affiliation and a link to the list); hospital website links; and source links with read dates. For a GP, services include the practice's enrolment status and fee table. Profiles are not reproduced: give the person the Healthpoint link (sources.healthpoint) for the doctor's own words.

France (fr_ ids): Evidence for doctors in France from search_doctors: pass doctor_ids (up to 10 at once) or one doctor_id. Each different doctor you open counts toward a daily limit for your connection (replies show daily_doctor_limit when it matters); opening a doctor again the same day is free. Open the doctors you are seriously considering, not every result. Each doctor: RPPS number (check on annuaire.sante.fr), official specialties, official extra competences and university diplomas (DU/DIU), practice modes; every practice from the RPPS register and the Ameli directory with address, phone, setting, role, fee category (Secteur 1/2, OPTAM) and hospital FINESS number; from Maiia or hospital pages when the doctor has one: stated expertise, procedures offered, hospital department and role, qualifications, languages, consultation fees, online booking, video consultations, whether online booking is open to new patients; source pages with read dates; and industry_links: Transparence Santé declarations by drug and device companies (agreements, benefits, payments) by year, company and purpose, shown as declared (licence CC BY-NC-SA 4.0; not evidence of expertise or wrongdoing). Profile text is not reproduced: give the person the source page link for the doctor's own words.

| Parameter | Type | Description |
|---|---|---|
| `doctor_id` | string | One doctor_id from search_doctors (dr_... = United States, nz_... = New Zealand, fr_... = France). |
| `npi` | string | (US only) 10-digit NPI, instead of doctor_id. |
| `detail` | `summary` \\| `full` | (US only) Default summary. |
| `doctor_ids` | array of string, up to 10 | Up to 10 doctor_ids from search_doctors, all from one country (dr_... = United States, nz_... = New Zealand, fr_... = France). |

## `lookup_terms`

HTTP: United States `GET /api/v1/terms?text=…` on `https://api.findadoctor.si`

United States only. Check how a word is understood before searching: matching MeSH condition terms (with how many doctors' hospital-website profiles list each as a focus), procedure groups and specialties.

| Parameter | Type | Description |
|---|---|---|
| `text` (required) | string |  |

## `list_procedures`

HTTP: United States `GET /api/v1/procedures` on `https://api.findadoctor.si`

United States only. The 81 signature procedure groups with Medicare 2024 volumes and national ranks (CPT codes, common names, national median per physician).

No parameters.

## `list_specialties`

HTTP: United States `GET /api/v1/specialties` on `https://api.findadoctor.si`; New Zealand `GET /api/v1/specialties` on `https://api-nz.findadoctor.si`; France `GET /api/v1/specialties` on `https://api-fr.findadoctor.si`

Specialty names one country's database uses. Set country: United States (country=US), New Zealand (country=NZ), France (country=FR).

United States (country=US): All specialties in the database with ids, families and physician counts.

New Zealand (country=NZ): Specialty names used in this database (Healthpoint categories) with doctor counts. Free.

France (country=FR): Specialty names in this database (official French names from RPPS and Ameli, and English labels) with doctor counts. Free.

| Parameter | Type | Description |
|---|---|---|
| `country` (required) | `US` \\| `NZ` \\| `FR` | Where the person wants to be seen: United States (country=US), New Zealand (country=NZ), France (country=FR). Decide it before searching; if unclear, ask the person. Older clients that leave it out get United States. |

## `about_database`

HTTP: United States `GET /api/v1/about` on `https://api.findadoctor.si`; New Zealand `GET /api/v1/about` on `https://api-nz.findadoctor.si`; France `GET /api/v1/about` on `https://api-fr.findadoctor.si`

What one country's database holds: sources, dates, counts and coverage. Set country: United States (country=US), New Zealand (country=NZ), France (country=FR).

United States (country=US): Sources, build date, coverage counts, scoring method and caveats.

New Zealand (country=NZ): Sources, read dates, coverage counts and known gaps. Free.

France (country=FR): Sources, licences, read dates, coverage counts and known gaps. Free.

| Parameter | Type | Description |
|---|---|---|
| `country` (required) | `US` \\| `NZ` \\| `FR` | Where the person wants to be seen: United States (country=US), New Zealand (country=NZ), France (country=FR). Decide it before searching; if unclear, ask the person. Older clients that leave it out get United States. |

## `search_gp_practices`

HTTP: New Zealand `GET /api/v1/gp-practices` on `https://api-nz.findadoctor.si`

New Zealand only. Free list of New Zealand general practices (GP clinics), or urgent care clinics, near a place, from Healthpoint. Use it when the person needs a GP, wants to enrol with a practice, or needs urgent but not emergency care. Each practice: whether it says it is enrolling new patients (yes; restricted = only some people, e.g. family of patients or people living nearby; no; does not apply = urgent care that does not enrol; unknown = the page does not say), the practice's own enrolment note, its fee table (the first fee table on its page, usually fees for enrolled patients by age, without and with a Community Services Card; with age, the row for that age), addresses, phone numbers, website, online booking link, languages, hours, the doctors listed there (doctor_ids for get_doctor) and the date Healthpoint says the page was last updated. In New Zealand most people enrol with one general practice: visits cost less once enrolled, and a GP referral is the usual way to a public specialist. Give place or name. Practices are not doctors, so this does not count toward the daily doctor limit. Enrolment and fees change often: tell the person to phone the practice to confirm.

| Parameter | Type | Description |
|---|---|---|
| `place` | string | New Zealand city, suburb or region (e.g. 'Papanui', 'Hamilton', 'North Shore', 'Canterbury'). |
| `name` | string | Practice name or part of it, to check a named practice. |
| `enrolling` | `any` \\| `yes` \\| `yes_or_restricted` | yes = only practices that say they are enrolling new patients; yes_or_restricted also keeps practices enrolling only some people (read enrolling_note). Default any (enrolling practices come first). |
| `age` | integer 0–120 | The patient's age: each result then shows the fee row for that age. |
| `language` | string | Language other than English the practice lists, e.g. 'Mandarin', 'Samoan', 'te reo Maori'. |
| `kind` | `gp` \\| `urgent_care` \\| `any` | gp = general practices (default; also nurse-led, online, student and rest-home practices, named so in each result's kind); urgent_care = accident and urgent medical care and after-hours clinics (no enrolment needed); any = both. |
| `limit` | integer 1–10 | Default 10. |
| `offset` | integer 0–40 | For paging (at most 40). |

## `public_waitlist`

HTTP: New Zealand `GET /api/v1/waitlist` on `https://api-nz.findadoctor.si`

New Zealand only. Public-system waiting lists from Health NZ by district and specialty (latest month and the same month a year earlier): people waiting for a first specialist assessment (FSA) and for planned treatment (surgery), and the share waiting over 120 days. Use it when the person is weighing public against private, or which district is faster. Give specialty and/or district. Free.

| Parameter | Type | Description |
|---|---|---|
| `specialty` | string | e.g. 'Orthopaedic', 'ENT', 'General Surgery', 'eye'. An exact name is matched first, then names containing each word, then the same without words like 'surgery' and with common plain words mapped (eye → Ophthalmology, heart surgery → Cardiothoracic, cardiologist → Cardiology, internal medicine → General Medicine), then part of a name; both of Health NZ's names for the same specialty are returned (e.g. Orthopaedics and Orthopaedic Surgery). |
| `district` | string | Health NZ district, e.g. 'Auckland', 'Canterbury', 'Capital and Coast'. Part of a name also matches (Canterbury includes South Canterbury); a city or region is read as its district (Wellington → Capital and Coast, Dunedin → Southern), shown in district_read_as. |

## `hospital_procedure_volumes`

HTTP: France `GET /api/v1/procedure-volumes` on `https://api-fr.findadoctor.si`

France only. Which French hospitals and private clinics perform a procedure most, from Open CCAM (ATIH): number of acts per hospital site per year, 2021-2025, public and private. Counts hospital stays and day cases only (PMSI MCO); procedures done in a doctor's office or a hospital outpatient clinic are not counted, and a site with fewer than 11 stays for an act is not listed. procedure = English or French text ('cataract', 'knee replacement', 'prothèse genou', 'coloscopie', 'ablation fibrillation auriculaire') or CCAM codes; the reply lists the CCAM acts it added up, so check they fit the need (add-on codes and pathology are left out of text matches). For 'aneurysm' or 'stent' say where (brain, aorta, heart, carotid). place = city, postcode, Paris/Lyon/Marseille arrondissement, département number or a hospital FINESS number; without place it ranks all of France. Hospital-level only: it does not say which surgeon operates. Then use search_doctors with hospital_finess (salaried hospital doctors) or with the hospital's postcode and the specialty (self-employed surgeons at private clinics). Free.

| Parameter | Type | Description |
|---|---|---|
| `procedure` | string | Procedure in English or French, or CCAM codes (e.g. 'BFGA427'; an 8th phase digit is dropped). |
| `codes` | array of string, up to 15 | Exact CCAM codes to add up (use instead of procedure to narrow). |
| `place` | string | City, postcode, arrondissement ('Paris 15'), département number (2A, 2B, 971-976), or hospital FINESS number. |
| `year` | integer 2021–2025 | Default latest (2025). |
| `limit` | integer 1–20 | Default 10. |
| `offset` | integer 0–100 | For paging (at most 100). |
