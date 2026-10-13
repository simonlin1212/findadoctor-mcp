#!/usr/bin/env bash
# Search FindADoctor.si over the HTTP API and open the evidence for the first doctor in the list.
# Needs curl and jq. Set FINDADOCTOR_KEY to send an account key; without it the free allowance applies.
set -euo pipefail

BASE="https://api.findadoctor.si/api/v1"
AUTH=()
if [ -n "${FINDADOCTOR_KEY:-}" ]; then AUTH=(-H "Authorization: Bearer ${FINDADOCTOR_KEY}"); fi
call() { curl -sS -A "findadoctor-example/1.0" ${AUTH[@]+"${AUTH[@]}"} "$@"; }
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# Step 1: the free short list.
status=$(call -G -o "$TMP/search.json" -w '%{http_code}' "$BASE/search" \
  --data-urlencode "condition=atrial fibrillation" \
  --data-urlencode "city=Phoenix" \
  --data-urlencode "state=AZ" \
  --data-urlencode "within_miles=25" \
  --data-urlencode "medicare_patient=true" \
  --data-urlencode "limit=5")
if [ "$status" != "200" ]; then
  # e.g. 429 rate limit: say so, don't retry in a loop.
  echo "Search failed (HTTP $status): $(jq -r '.message // .error' "$TMP/search.json")"
  exit 0
fi
jq -r '"\(.total_matches) matches", (.warnings // [] | .[] | "warning: \(.)"),
  (.results[] | "\(.rank). \(.name), \(.degree // "") | \(.specialty // "") | \(.city), \(.state) | \(.match_basis // "")")' "$TMP/search.json"

# Step 2: open the evidence, counted per day. Open only serious candidates (up to 10 ids, comma-separated).
ID=$(jq -r '.results[0].doctor_id // empty' "$TMP/search.json")
[ -n "$ID" ] || exit 0
status=$(call -o "$TMP/doctor.json" -w '%{http_code}' "$BASE/doctors?ids=$ID")
if [ "$status" != "200" ]; then
  # 429: daily doctor allowance or rate limit. Tell the person; don't retry in a loop.
  echo "Not opened (HTTP $status): $(jq -r '.message // .error' "$TMP/doctor.json")"
  exit 0
fi
jq -r '.doctors[] | "\n\(.name): \(.phone) (\(.phone_source))",
  (.signature_procedures_2024 // [] | .[] | "  \(.label): \(.medicare_patient_days) Medicare patient-days in 2024, #\(.national_rank) of \(.national_of) nationally"),
  (.caveats // [] | .[] | "  caveat: \(.)")' "$TMP/doctor.json"
# With several ids, some may come back later (not_returned_yet: ask again, free)
# or not at all today (left_out: daily allowance).
jq -r '.daily_doctor_limit.message // empty' "$TMP/doctor.json"
