# Examples

Each example does the same two steps: search for a free short list (atrial fibrillation specialists within 25 miles of Phoenix, for a Medicare patient), then open the evidence for the first doctor in the list.

| Example | Needs | Run |
|---|---|---|
| [curl/search-and-open.sh](curl/search-and-open.sh) | curl, jq | `bash curl/search-and-open.sh` |
| [python/http_api.py](python/http_api.py) | Python 3.9+, standard library only | `python3 python/http_api.py` |
| [python/mcp_client.py](python/mcp_client.py) | Python 3.10+, `pip install "mcp>=2"` | `python3 python/mcp_client.py` |
| [typescript/mcp-client.ts](typescript/mcp-client.ts) | Node.js 18+ | `cd typescript && npm install && npm start` |

Set `FINDADOCTOR_KEY` to send an account key. Without one, each network address can open 5 different doctors a day ([Limits](https://findadoctor.si/us/docs/limits/)); running an example again the same day re-opens the same doctor, which is free.

The live replies contain real doctors' names and contact details from public records. The sample replies in [responses/](responses/) show the shape of a reply with made-up values:

- [search_doctors.json](responses/search_doctors.json): the short list.
- [get_doctor.json](responses/get_doctor.json): the evidence for one doctor.
- [daily_limit_reached.json](responses/daily_limit_reached.json): what comes back when the daily allowance runs out.

All examples were run against the live service on 2026-10-13.
