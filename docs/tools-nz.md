# Tool reference: New Zealand

Generated from the live New Zealand server's `tools/list` on 2026-10-15 (server version nz-2026-10-15.2). The live server is the source of truth: [`reference/tools-nz.json`](../reference/tools-nz.json) is the same list as JSON, and [`openapi.json`](https://api-nz.findadoctor.si/openapi.json) describes the HTTP API and the reply fields. The one MCP address for every country, `https://api.findadoctor.si/mcp`, has the same tools (with `country: "NZ"`): see [tools.md](tools.md).

MCP endpoint: `https://api-nz.findadoctor.si/mcp`. All tools are read-only. Every MCP tool has an HTTP `GET` equivalent on `https://api-nz.findadoctor.si` that takes the same parameters (for `get_doctor`, `doctor_ids` is `ids`, comma-separated) and returns the same JSON.

Doctor ids in the descriptions below (such as `nz_4k9m2x7qph3t`, `nz_8w2c5n1kd7ra`) are placeholders written by the server, not real doctors.

## `search_doctors`

HTTP: `GET /api/v1/search`

Free short list of New Zealand doctors for a need; use it first whenever the person needs a doctor or specialist in New Zealand. Give at least one of need, specialty, place or name. need = a condition, procedure or focus in plain English (e.g. 'ACL reconstruction', 'endometriosis', 'skin cancer', 'cataract surgery'); it is matched against the focus areas doctors list first, then the procedures their services list, their specialty, and their own profile text (not shown here). specialty = a name from list_specialties, a word from one (e.g. 'orthopaedic', 'ENT') or a plain word (e.g. 'eye', 'skin', 'heart'); matched word by word (word endings may differ, e.g. 'cardiologist', 'paediatrician'; not fragments inside words), and the reply's specialty_read_as lists the specialty names used. place = a New Zealand city, suburb, or region or Health NZ district (e.g. 'Christchurch', 'North Shore', 'Hawke's Bay', 'Hutt Valley'); when a town search leaves out doctors listed only on the wider region's page or in its other towns, place_note says how many and which place to use instead. Each result: doctor_id, name, specialties, vocational scope, cities, sectors (private, public), match_basis (with a need: stated_focus, services_listed (the doctor's own or a small practice's service page), shared_service_listed (a hospital department or large group page they are linked to, so not necessarily done by this doctor), specialty, specialty_for_symptom (the need is a symptom few doctors list, and their specialty usually sees it; need_note says which specialties), profile_text or partial), place_match (with a place: city_or_address, city_in_region, address_contains or region_page_only), warnings (e.g. not practising on the Medical Council register), specialist_since (year first on the Medical Council vocational, i.e. specialist, register in New Zealand), recognition (New Zealand honours, University of Auckland title), listing (medical_council_register_only when the doctor has no clinic listing here), possibly_same_person_as (another entry with the same name that may be the same doctor) and detail_has (what get_doctor adds). General practitioners are left out unless specialty is general practice (e.g. 'GP') or a name is given; to find a GP clinic use search_gp_practices. Doctors only on the register are included when practising with a specialist scope (any status with a name). Results are ranked first by how directly the doctor's own listing matches the need (doctors who list all its words; then, when the need is a symptom such as back pain, doctors whose specialty usually sees it; then doctors who list some of the words; then words only in profile text), then by place_match (with a place); with experienced_first, longer as a specialist next. Doctors known only from the Medical Council register (no clinic listing) come after all others. Not ranked by quality or outcomes. Then call get_doctor with the doctor_ids you are considering. Up to 10 results per search and paging stops at 30: narrow the need or the place instead of paging.

| Parameter | Type | Description |
|---|---|---|
| `need` | string | Condition, procedure or focus, plain English. |
| `specialty` | string | Specialty name, a word from one, or a plain word like 'eye' (see list_specialties). |
| `place` | string | New Zealand city, suburb, or region or Health NZ district (e.g. 'Waikato', 'Hawke's Bay', 'Capital and Coast'). |
| `name` | string | Doctor's name or part of it, to check a named doctor. |
| `sector` | `any` \\| `private` \\| `public` | private = the doctor lists a private service; public = a public (Health NZ) service. Default any. |
| `child` | boolean | True when the patient is a child: among doctors in the same place who match the need equally well, those in paediatrics or who list children in their focus come first, then those whose services say they see children; doctors whose services list only adult ages are left out. Most listings do not say, so those doctors stay in. |
| `language` | string | Language other than English the doctor, or a small clinic (3 doctors or fewer) they work in, lists, e.g. 'Mandarin', 'Hindi', 'Samoan'. |
| `gender` | `female` \\| `male` | Only when the person asks. Gender is recorded for only a small share of doctors (when their Healthpoint page states it); doctors without it are left out and gender_note says how many. |
| `southern_cross_affiliated` | boolean | True keeps doctors whose own Healthpoint page or at least one of whose service pages says Southern Cross Affiliated Provider (cover still depends on the policy and often prior approval; confirm). |
| `experienced_first` | boolean | True when the person wants an experienced or senior doctor: among doctors who match equally well, those longer on the New Zealand specialist (vocational) register come first. Time on the register is not quality, and doctors who trained overseas may have practised longer than it shows. |
| `limit` | integer 1–10 | Default 10. |
| `offset` | integer 0–20 | For paging (at most 20, so 30 results in all: narrow the search instead). |

## `get_doctor`

HTTP: `GET /api/v1/doctors?ids=… · GET /api/v1/doctors/{doctor_id}`

Evidence for New Zealand doctors from search_doctors: pass doctor_ids (up to 10 at once) or one doctor_id. Each different doctor you open counts toward a daily limit for your connection (replies show daily_doctor_limit when it matters); opening a doctor again the same day is free. Open the doctors you are seriously considering, not every result. Each doctor: specialties, title, qualifications, focus areas and subspecialties they list, further training, languages, whether their services see children; every private and public service with clinic addresses, phone numbers and websites, procedures and conditions the service lists, fee categories and fee lines, ages, hours, how to get referred, and whether it says Southern Cross Affiliated Provider or nib First Choice (insurer_notes also says whether the doctor's own page says so); the Medical Council register entry (status, scope of practice, conditions, qualifications, practising certificate); experience (each vocational scope with the date it was granted and years since, first New Zealand registration, primary medical degree year, New Zealand honours with citation, University of Auckland title and hospital appointments, approximate count of papers with a New Zealand affiliation and a link to the list); hospital website links; and source links with read dates. For a GP, services include the practice's enrolment status and fee table. Profiles are not reproduced: give the person the Healthpoint link (sources.healthpoint) for the doctor's own words.

| Parameter | Type | Description |
|---|---|---|
| `doctor_ids` | array of string, up to 10 | Up to 10 doctor_ids from search_doctors, e.g. ['nz_4k9m2x7qph3t', 'nz_8w2c5n1kd7ra']. |
| `doctor_id` | string | One doctor_id from search_doctors, e.g. 'nz_4k9m2x7qph3t'. |

## `search_gp_practices`

HTTP: `GET /api/v1/gp-practices`

Free list of New Zealand general practices (GP clinics), or urgent care clinics, near a place, from Healthpoint. Use it when the person needs a GP, wants to enrol with a practice, or needs urgent but not emergency care. Each practice: whether it says it is enrolling new patients (yes; restricted = only some people, e.g. family of patients or people living nearby; no; does not apply = urgent care that does not enrol; unknown = the page does not say), the practice's own enrolment note, its fee table (the first fee table on its page, usually fees for enrolled patients by age, without and with a Community Services Card; with age, the row for that age), addresses, phone numbers, website, online booking link, languages, hours, the doctors listed there (doctor_ids for get_doctor) and the date Healthpoint says the page was last updated. In New Zealand most people enrol with one general practice: visits cost less once enrolled, and a GP referral is the usual way to a public specialist. Give place or name. Practices are not doctors, so this does not count toward the daily doctor limit. Enrolment and fees change often: tell the person to phone the practice to confirm.

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

## `list_specialties`

HTTP: `GET /api/v1/specialties`

Specialty names used in this database (Healthpoint categories) with doctor counts. Free.

No parameters.

## `public_waitlist`

HTTP: `GET /api/v1/waitlist`

Public-system waiting lists from Health NZ by district and specialty (latest month and the same month a year earlier): people waiting for a first specialist assessment (FSA) and for planned treatment (surgery), and the share waiting over 120 days. Use it when the person is weighing public against private, or which district is faster. Give specialty and/or district. Free.

| Parameter | Type | Description |
|---|---|---|
| `specialty` | string | e.g. 'Orthopaedic', 'ENT', 'General Surgery', 'eye'. An exact name is matched first, then names containing each word, then the same without words like 'surgery' and with common plain words mapped (eye → Ophthalmology, heart surgery → Cardiothoracic, cardiologist → Cardiology, internal medicine → General Medicine), then part of a name; both of Health NZ's names for the same specialty are returned (e.g. Orthopaedics and Orthopaedic Surgery). |
| `district` | string | Health NZ district, e.g. 'Auckland', 'Canterbury', 'Capital and Coast'. Part of a name also matches (Canterbury includes South Canterbury); a city or region is read as its district (Wellington → Capital and Coast, Dunedin → Southern), shown in district_read_as. |

## `about_database`

HTTP: `GET /api/v1/about`

Sources, read dates, coverage counts and known gaps. Free.

No parameters.
