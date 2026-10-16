# Tool reference: France

Generated from the live France server's `tools/list` on 2026-10-16 (server version fr-2026-10-16.1). The live server is the source of truth: [`reference/tools-fr.json`](../reference/tools-fr.json) is the same list as JSON, and [`openapi.json`](https://api-fr.findadoctor.si/openapi.json) describes the HTTP API and the reply fields. The one MCP address for every country, `https://api.findadoctor.si/mcp`, has the same tools (with `country: "FR"`): see [tools.md](tools.md).

MCP endpoint: `https://api-fr.findadoctor.si/mcp`. All tools are read-only. Every MCP tool has an HTTP `GET` equivalent on `https://api-fr.findadoctor.si` that takes the same parameters (for `get_doctor`, `doctor_ids` is `ids`, comma-separated) and returns the same JSON.

Doctor ids in the descriptions below (such as `fr_4k9m2x7qph3t`, `fr_8w2c5n1kd7ra`) are placeholders written by the server, not real doctors.

## `search_doctors`

HTTP: `GET /api/v1/search`

Free short list of doctors in France for a need; use it first whenever the person needs a doctor, specialist or GP in France. Give at least one of need, specialty, place, name or hospital_finess. need = condition, procedure or focus, in French or English (e.g. 'endométriose', 'prothèse genou', 'knee replacement', 'cataract'; common English words are also searched in French); matched against the expertise and procedures doctors state, their official competences and university diplomas, hospital departments and roles, and specialty. specialty = French or English (e.g. 'cardiologie', 'dermatology', 'pédiatre', 'ORL', 'GP', 'généraliste'). place = city ('Lyon', 'Paris' includes all arrondissements), postcode ('75015'), arrondissement ('Paris 15', 'Lyon 3e'), département number ('69', '2A') or a practice or hospital name; a text match on practice addresses, not a distance search. Each result: doctor_id, name, gender, specialties (French, as registered), specialties_en, places (up to 3 practices, the ones matching place first), fee_sectors (Ameli category: Secteur 1 = standard fees; Secteur 2 = may charge extra; Non conventionné = not contracted, little reimbursed), optam (agreed to limit extra fees), match_basis (with a need: stated_expertise, official_competence, hospital_department_or_training, several_fields, specialty, specialty_usually_treats, partial), register (rpps, ameli_only = only in the Assurance Maladie directory, website_only = not matched to the official registers), warnings (e.g. barred from practising) and detail_has (what get_doctor adds). With a need, results are ranked by how directly the doctor's own data matches it: all its words in the expertise or procedures the doctor states, then in official competences or university diplomas, then in hospital department, role or training, then spread over several fields, then in the specialty name; then, when the need is a condition few doctors list, doctors in the specialty that usually treats it (specialty_usually_treats); then doctors matching only some of the words. Without a need, doctors with more data (stated expertise, official competences, profile pages) come first, then in a fixed shuffled order. Not ranked by quality, outcomes, fees or industry links. Then call get_doctor with the doctor_ids you are considering. Up to 10 results per search and paging stops at 30: narrow the need or the place instead of paging.

| Parameter | Type | Description |
|---|---|---|
| `need` | string | Condition, procedure or focus, in French or English. |
| `specialty` | string | Specialty in French or English, e.g. 'cardiologie', 'dermatology', 'ORL', 'GP' (see list_specialties). |
| `place` | string | City, postcode, arrondissement ('Paris 15'), département number ('69', '2A') or a practice or hospital name. |
| `name` | string | Doctor's name or part of it, to check a named doctor. |
| `gender` | `female` \\| `male` | Only when the person asks. From the register's civil title (Madame/Monsieur); recorded for almost all doctors. |
| `language` | string | Language other than French, e.g. 'English', 'Arabic', 'anglais'. Only known for doctors with a Maiia or hospital profile (about 1,800 list one); many others speak it too. |
| `fee_sector` | `any` \\| `secteur_1` \\| `secteur_1_or_optam` \\| `secteur_2` | Assurance Maladie fee category. secteur_1 = standard fees, no extra charges; secteur_1_or_optam = standard fees or agreed limits on extra fees; secteur_2 = may charge extra. Kept if ANY of the doctor's practices has it (it can differ by practice): check each practice in get_doctor. Most hospital-only doctors have no category. Default any. |
| `online_booking` | boolean | True keeps doctors whose Maiia or hospital page shows online booking (Doctolib is not covered). |
| `teleconsultation` | boolean | True keeps doctors offering video consultations on Maiia. |
| `hospital_finess` | string | Keep doctors whose register address is this hospital site (FINESS number from hospital_procedure_volumes): mostly salaried hospital doctors. |
| `limit` | integer 1–10 | Default 10. |
| `offset` | integer 0–20 | For paging (at most 20, so 30 results in all: narrow the search instead). |

## `get_doctor`

HTTP: `GET /api/v1/doctors?ids=… · GET /api/v1/doctors/{doctor_id}`

Evidence for doctors in France from search_doctors: pass doctor_ids (up to 10 at once) or one doctor_id. Each different doctor you open counts toward a daily limit for your connection (replies show daily_doctor_limit when it matters); opening a doctor again the same day is free. Open the doctors you are seriously considering, not every result. Each doctor: RPPS number (check on annuaire.sante.fr), official specialties, official extra competences and university diplomas (DU/DIU), practice modes; every practice from the RPPS register and the Ameli directory with address, phone, setting, role, fee category (Secteur 1/2, OPTAM) and hospital FINESS number; from Maiia or hospital pages when the doctor has one: stated expertise, procedures offered, hospital department and role, qualifications, languages, consultation fees, online booking, video consultations, whether online booking is open to new patients; source pages with read dates; and industry_links: Transparence Santé declarations by drug and device companies (agreements, benefits, payments) by year, company and purpose, shown as declared (licence CC BY-NC-SA 4.0; not evidence of expertise or wrongdoing). Profile text is not reproduced: give the person the source page link for the doctor's own words.

| Parameter | Type | Description |
|---|---|---|
| `doctor_ids` | array of string, up to 10 | Up to 10 doctor_ids from search_doctors, e.g. ['fr_4k9m2x7qph3t', 'fr_8w2c5n1kd7ra']. |
| `doctor_id` | string | One doctor_id from search_doctors, e.g. 'fr_4k9m2x7qph3t'. |

## `hospital_procedure_volumes`

HTTP: `GET /api/v1/procedure-volumes`

Which French hospitals and private clinics perform a procedure most, from Open CCAM (ATIH): number of acts per hospital site per year, 2021-2025, public and private. Counts hospital stays and day cases only (PMSI MCO); procedures done in a doctor's office or a hospital outpatient clinic are not counted, and a site with fewer than 11 stays for an act is not listed. procedure = English or French text ('cataract', 'knee replacement', 'prothèse genou', 'coloscopie', 'ablation fibrillation auriculaire') or CCAM codes; the reply lists the CCAM acts it added up, so check they fit the need (add-on codes and pathology are left out of text matches). For 'aneurysm' or 'stent' say where (brain, aorta, heart, carotid). place = city, postcode, Paris/Lyon/Marseille arrondissement, département number or a hospital FINESS number; without place it ranks all of France. Hospital-level only: it does not say which surgeon operates. Then use search_doctors with hospital_finess (salaried hospital doctors) or with the hospital's postcode and the specialty (self-employed surgeons at private clinics). Free.

| Parameter | Type | Description |
|---|---|---|
| `procedure` | string | Procedure in English or French, or CCAM codes (e.g. 'BFGA427'; an 8th phase digit is dropped). |
| `codes` | array of string, up to 15 | Exact CCAM codes to add up (use instead of procedure to narrow). |
| `place` | string | City, postcode, arrondissement ('Paris 15'), département number (2A, 2B, 971-976), or hospital FINESS number. |
| `year` | integer 2021–2025 | Default latest (2025). |
| `limit` | integer 1–20 | Default 10. |
| `offset` | integer 0–100 | For paging (at most 100). |

## `list_specialties`

HTTP: `GET /api/v1/specialties`

Specialty names in this database (official French names from RPPS and Ameli, and English labels) with doctor counts. Free.

No parameters.

## `about_database`

HTTP: `GET /api/v1/about`

Sources, licences, read dates, coverage counts and known gaps. Free.

No parameters.
