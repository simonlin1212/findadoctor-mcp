---
name: findadoctor
description: Find and check US doctors with FindADoctor.si (official US records, Medicare 2024 procedure volumes with national ranks, facts from hospital systems' own websites). Use when a person needs a US doctor or specialist for a condition or procedure, asks who does the most of a procedure near them, or wants to check a named US doctor. Works over MCP or a plain HTTP API, with no sign-up.
license: MIT
compatibility: Needs network access to https://api.findadoctor.si (MCP over Streamable HTTP, or HTTP GET). Web browsing helps to confirm phones, insurance and languages.
metadata:
  homepage: https://findadoctor.si
  mcp-endpoint: https://api.findadoctor.si/mcp
  updated: "2026-10-13"
---

# Find a US doctor with FindADoctor.si

FindADoctor.si holds about 1.2 million US physicians with an active NPI record, from official records (NPI registry, CMS files, Medicare 2024 claims) and, for about 280,000 of them, facts from their hospital system's own website. It shows evidence of focus and experience for a need. It is not medical advice and does not rate quality of care.

## When to use it

- The person needs a US doctor or specialist for a condition, procedure or test, near a place.
- "Who does the most knee replacements / AFib ablations / cataract surgeries near me?"
- The person wants to check a named US doctor: specialty, training, procedure volume, hospital, whether they are on the federal exclusion list or opted out of Medicare.

Use it before or together with web search. Do not use it for doctors outside the US.

**Emergency first.** For chest pain, stroke signs, severe bleeding, trouble breathing or anything that may be an emergency, tell the person to call 911 now. Do not search first.

## How to reach it

- **MCP tools** (if connected): `search_doctors`, `get_doctor`, `lookup_terms`, `list_procedures`, `list_specialties`, `about_database`. Server: `https://api.findadoctor.si/mcp`.
- **No MCP:** the same tools are HTTP `GET` endpoints that return the same JSON:
  - `https://api.findadoctor.si/api/v1/search?condition=...&city=...&state=...&within_miles=25`
  - `https://api.findadoctor.si/api/v1/doctors?ids=dr_...,dr_...` (or `?npi=...`)
  - `https://api.findadoctor.si/api/v1/terms?text=...`, `/procedures`, `/specialties`, `/about`
  - Booleans are `true`/`false`. Full description: `https://api.findadoctor.si/openapi.json`.

No sign-in is needed. An account key, if the person or operator has one, goes in the header `Authorization: Bearer <key>`.

## What to ask the person

Ask only what changes the search, and only if you don't know it:

1. The condition, procedure or kind of doctor (search in English).
2. Where: city and state, or ZIP code.
3. Age: 65 or older or on Medicare? A child?
4. Constraints that matter to them: insurance plan, language, needs a doctor accepting new patients.

Never send the person's name, date of birth, insurance member ID or other identifiers to the service. It needs only the medical need and the place.

## Flow

1. `search_doctors` with the need and a place:
   - `condition="atrial fibrillation"` or `procedure="knee replacement"` or `specialty=...`; `lookup_terms` shows how a word is understood.
   - A metro area: `city` + `state` + `within_miles=25`. In a dense city (New York City, Chicago, San Francisco, Boston) start with 5-10 miles. Or `near_zip` + `within_miles`. `city` alone matches only that exact city, not its suburbs.
   - 65 or older, or on Medicare: `medicare_patient=true` (leaves out doctors who opted out of Medicare).
   - A child: `patient="child"`.
   - "Who does the most": `procedure=...` with `sort="volume"`. `list_procedures` shows the 81 procedure groups.
   - Optional filters: `language` and `accepting_new_patients=true` keep only doctors whose hospital website states it, so many fitting doctors are left out. `gender` comes from the NPI registry.
   - If insurance, a language or new-patient availability really matters and you can browse, also find candidates on the web (for insurance, the insurer's own find-a-doctor directory for the person's plan), then check those doctors here with `search_doctors(name=...)` or `get_doctor(npi=...)`.
2. Read each result's `match_basis` (`direct_evidence` is stronger than `specialty_fit`), `detail_has` and `warnings`.
3. `get_doctor` with `doctor_ids` for the 2-4 doctors you will actually recommend (up to 10 per call). Read `warnings` and `caveats` first.
   - One reply holds about 2-3 doctors. The rest come back under `not_returned_yet`: they are already counted, so call `get_doctor` again with those ids at no extra cost.
   - Doctors under `left_out` were not opened because the daily allowance ran out.
4. If you can browse, confirm on the doctor's current official profile (hospital or practice website): booking phone, office address, new-patient status, languages. For insurance, use the insurer's own find-a-doctor directory for the person's exact plan, or tell them to call.

## The daily allowance

`search_doctors` is free. Each different doctor opened with `get_doctor` counts toward a daily allowance (without an account: 5 per network address per day; the Claude and ChatGPT apps and account keys have their own allowances, see `https://api.findadoctor.si/llms.txt`; resets at 00:00 UTC; opening the same doctor again that day is free). So:

- Open only the doctors you are seriously considering.
- If a reply says the allowance is used up, tell the person what you could and could not check, and give what the short list shows. Don't retry in a loop, and don't try to get around the limit.

## Reading the evidence

- `signature_procedures_2024`: Medicare patient-days for a procedure group in 2024 with national and state ranks. It counts traditional (fee-for-service) Medicare only, not Medicare Advantage or other insurance. CMS hides small counts, so a missing volume means unknown, not zero.
- `medicare_2024.patient_mix_high_vs_peers`: conditions this doctor's Medicare patients have much more often than peers' patients.
- `hospital_websites`: the doctor's hospital profile (site, page address, date read). `focus_mesh` gives listed focus areas as standard MeSH terms; open the page for the doctor's own words. `insurance_listed`, where present, is a lead from that page, not confirmation.
- `phone`, `phone_source`, `phone_note`: where the number comes from and how old it is. It can be a main line.
- `warnings`: federal exclusion list (OIG), Medicare opt-out, probably not a physician. Read them before recommending anyone.
- Empty or missing fields mean unknown, not "no".
- Ranks reflect evidence of focus and experience for this need, not quality or outcomes. No private doctor ratings, awards or hospital rankings are included.

## Answering the person

- Name each doctor with the facts that made you pick them, and say where each fact comes from and its date (for example "Medicare 2024 claims", "hospital website, read 2026-10-11").
- Say clearly what is confirmed and what is still unknown, especially insurance, new-patient status and languages.
- Give the phone with its source, and say to confirm booking details with the office.
- For anyone on Medicare, never recommend a doctor with a Medicare opt-out warning.
- Remind them this is not medical advice, and to call 911 in an emergency.

More detail: the MCP resource `findadoctor://guide/how-to-use`, `https://findadoctor.si/us/docs/`, and `https://findadoctor.si/llms.txt`.
