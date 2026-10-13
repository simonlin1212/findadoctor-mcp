// Search FindADoctor.si over MCP and open the evidence for the first doctor in the list.
//
//   npm install
//   npm start
//
// Set FINDADOCTOR_KEY to send an account key; without it the free allowance applies.
import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StreamableHTTPClientTransport } from "@modelcontextprotocol/sdk/client/streamableHttp.js";

const URL_MCP = new URL("https://api.findadoctor.si/mcp");

type ToolResult = {
  isError?: boolean;
  structuredContent?: Record<string, unknown>;
  content?: Array<{ type: string; text?: string }>;
};

// Tool results are JSON: in structuredContent when present, otherwise in the first text block.
function payload(result: ToolResult): any {
  const text = result.content?.find((c) => c.type === "text")?.text;
  if (result.isError) throw new Error(text ?? "tool error");
  return result.structuredContent ?? JSON.parse(text ?? "{}");
}

async function main(client: Client): Promise<void> {
  // Step 1: the free short list.
  let found: any;
  try {
    found = payload(
      (await client.callTool({
        name: "search_doctors",
        arguments: {
          condition: "atrial fibrillation",
          city: "Phoenix",
          state: "AZ",
          within_miles: 25,
          medicare_patient: true,
          limit: 5,
        },
      })) as ToolResult,
    );
  } catch (e) {
    // e.g. rate limit: say so, don't retry in a loop.
    console.log("Search failed:", (e as Error).message);
    return;
  }
  console.log(`${found.total_matches} matches`);
  for (const w of found.warnings ?? []) console.log("warning:", w);
  for (const r of found.results) {
    console.log(`${r.rank}. ${r.name}, ${r.degree ?? ""} | ${r.specialty ?? ""} | ${r.city}, ${r.state} | ${r.match_basis ?? ""}`);
  }
  if (found.results.length === 0) return;

  // Step 2: open the evidence, counted per day. Open only serious candidates (up to 10 ids at once).
  let detail: any;
  try {
    detail = payload(
      (await client.callTool({ name: "get_doctor", arguments: { doctor_ids: [found.results[0].doctor_id] } })) as ToolResult,
    );
  } catch (e) {
    // Daily allowance used up: tell the person, don't retry in a loop.
    console.log("Not opened:", (e as Error).message);
    return;
  }
  for (const doc of detail.doctors) {
    console.log(`\n${doc.name}: ${doc.phone} (${doc.phone_source})`);
    for (const p of doc.signature_procedures_2024 ?? []) {
      console.log(`  ${p.label}: ${p.medicare_patient_days} Medicare patient-days in 2024, #${p.national_rank} of ${p.national_of} nationally`);
    }
    for (const c of doc.caveats ?? []) console.log("  caveat:", c);
  }
  // With several ids, some may come back later (not_returned_yet: ask again, free)
  // or not at all today (left_out: daily allowance).
  if (detail.daily_doctor_limit) console.log("\n" + detail.daily_doctor_limit.message);
}

const headers: Record<string, string> = { "User-Agent": "findadoctor-example/1.0" };
if (process.env.FINDADOCTOR_KEY) headers.Authorization = `Bearer ${process.env.FINDADOCTOR_KEY}`;

const client = new Client({ name: "findadoctor-example", version: "1.0.0" });
await client.connect(new StreamableHTTPClientTransport(URL_MCP, { requestInit: { headers } }));
try {
  await main(client);
} finally {
  await client.close();
}
