"""Search FindADoctor.si over the plain HTTP API and open the evidence for the first doctor in the list.

Standard library only (Python 3.9+):

    python3 http_api.py

Set FINDADOCTOR_KEY to send an account key; without it the free allowance applies.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request

BASE = "https://api.findadoctor.si/api/v1"


def get(path: str, **params: object) -> dict:
    query = urllib.parse.urlencode({k: str(v).lower() if isinstance(v, bool) else v for k, v in params.items()})
    headers = {"Accept": "application/json", "User-Agent": "findadoctor-example/1.0"}
    if os.environ.get("FINDADOCTOR_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['FINDADOCTOR_KEY']}"
    req = urllib.request.Request(f"{BASE}{path}?{query}", headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.load(r)
    except urllib.error.HTTPError as e:
        # 429: daily doctor allowance or rate limit. The body says which and when it resets.
        body = e.read().decode(errors="replace")
        try:
            data = json.loads(body)
            message = data.get("message") or data.get("error") or body
        except ValueError:
            message = body
        raise RuntimeError(f"HTTP {e.code}: {message}") from None


def main() -> int:
    # Step 1: the free short list.
    try:
        found = get("/search", condition="atrial fibrillation", city="Phoenix", state="AZ",
                    within_miles=25, medicare_patient=True, limit=5)
    except RuntimeError as e:  # e.g. rate limit: say so, don't retry in a loop
        print("Search failed:", e, file=sys.stderr)
        return 1
    print(f"{found['total_matches']} matches")
    for w in found.get("warnings") or []:
        print("warning:", w)
    for r in found["results"]:
        print(f"{r['rank']}. {r['name']}, {r.get('degree', '')} | {r.get('specialty', '')} | "
              f"{r.get('city', '')}, {r.get('state', '')} | {r.get('match_basis', '')}")
        for w in r.get("warnings") or []:
            print("  ", w)
    if not found["results"]:
        return 0

    # Step 2: open the evidence, counted per day. Open only serious candidates (up to 10 ids at once).
    top = found["results"][0]["doctor_id"]
    try:
        detail = get("/doctors", ids=top)
    except RuntimeError as e:  # tell the person; don't retry in a loop
        print("Not opened:", e, file=sys.stderr)
        return 1
    for doc in detail["doctors"]:
        print(f"\n{doc['name']}")
        # Read each doctor's warnings first (Medicare opt-out, federal exclusion list, probably not a physician).
        for w in doc.get("warnings") or []:
            print(" ", w)
        print(f"  phone: {doc.get('phone')} ({doc.get('phone_source')})")
        for p in doc.get("signature_procedures_2024") or []:
            print(f"  {p['label']}: {p['medicare_patient_days']} Medicare patient-days in 2024, "
                  f"#{p['national_rank']} of {p['national_of']} nationally")
        for c in doc.get("caveats") or []:
            print("  caveat:", c)
    # With several ids, some may come back later (not_returned_yet: ask again, free)
    # or not at all today (left_out: daily allowance).
    for d in (detail.get("not_returned_yet") or {}).get("doctors") or []:
        print(f"Ask again (free): {d['doctor_id']}")
    for d in detail.get("left_out") or []:
        print(f"Not opened today: {d['doctor_id']} ({d['reason']})")
    if detail.get("daily_doctor_limit"):
        print("\n" + detail["daily_doctor_limit"]["message"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
