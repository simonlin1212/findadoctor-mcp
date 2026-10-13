"""Search FindADoctor.si over MCP and open the evidence for the first doctor in the list.

Uses the official MCP Python SDK, version 2 (Python 3.10+; tested with mcp 2.3.0):

    pip install "mcp>=2,<3"
    python mcp_client.py

Set FINDADOCTOR_KEY to send an account key; without it the free allowance applies.
"""
from __future__ import annotations

import asyncio
import json
import os

import httpx2  # installed with mcp 2.x
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

URL = "https://api.findadoctor.si/mcp"


def payload(result) -> dict:
    """Tool results are JSON: in structured_content when present, otherwise in the first text block."""
    if result.is_error:
        raise RuntimeError(result.content[0].text if result.content else "tool error")
    if result.structured_content is not None:
        return result.structured_content
    return json.loads(result.content[0].text)


async def main() -> None:
    headers = {"User-Agent": "findadoctor-example/1.0"}
    if os.environ.get("FINDADOCTOR_KEY"):
        headers["Authorization"] = f"Bearer {os.environ['FINDADOCTOR_KEY']}"

    async with httpx2.AsyncClient(headers=headers, timeout=httpx2.Timeout(60.0)) as http:
        async with streamable_http_client(URL, http_client=http) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()

                # Step 1: the free short list.
                try:
                    found = payload(await session.call_tool("search_doctors", {
                        "condition": "atrial fibrillation",
                        "city": "Phoenix",
                        "state": "AZ",
                        "within_miles": 25,
                        "medicare_patient": True,
                        "limit": 5,
                    }))
                except RuntimeError as e:  # e.g. rate limit: say so, don't retry in a loop
                    print("Search failed:", e)
                    return
                print(f"{found['total_matches']} matches")
                for w in found.get("warnings") or []:
                    print("warning:", w)
                for r in found["results"]:
                    print(f"{r['rank']}. {r['name']}, {r.get('degree', '')} | {r.get('specialty', '')} | "
                          f"{r.get('city', '')}, {r.get('state', '')} | {r.get('match_basis', '')}")
                if not found["results"]:
                    return

                # Step 2: open the evidence, counted per day. Open only serious candidates.
                top = found["results"][0]["doctor_id"]
                try:
                    detail = payload(await session.call_tool("get_doctor", {"doctor_ids": [top]}))
                except RuntimeError as e:  # daily allowance used up: tell the person, don't retry in a loop
                    print("Not opened:", e)
                    return
                for doc in detail["doctors"]:
                    print(f"\n{doc['name']}: {doc.get('phone')} ({doc.get('phone_source')})")
                    for p in doc.get("signature_procedures_2024") or []:
                        print(f"  {p['label']}: {p['medicare_patient_days']} Medicare patient-days in 2024, "
                              f"#{p['national_rank']} of {p['national_of']} nationally")
                    for c in doc.get("caveats") or []:
                        print("  caveat:", c)
                # With several ids, some may come back later (not_returned_yet: ask again, free)
                # or not at all today (left_out: daily allowance).
                if detail.get("daily_doctor_limit"):
                    print("\n" + detail["daily_doctor_limit"]["message"])


if __name__ == "__main__":
    asyncio.run(main())
