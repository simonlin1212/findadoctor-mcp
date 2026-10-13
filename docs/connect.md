# Connect FindADoctor.si to your agent

MCP endpoint (Streamable HTTP):

```text
https://api.findadoctor.si/mcp
```

No sign-in is needed. If you have an account key (for a higher daily allowance), send it as the header `Authorization: Bearer <key>`.

Client menus change often. These steps were checked against each client's own guide or CLI help on 2026-10-12 and 2026-10-13. If a step no longer matches, follow the linked guide and [open an issue](https://github.com/simonlin1212/findadoctor-mcp/issues/new/choose) so we can update this page.

## One-step installs

- **Cursor** and **VS Code**: the **Add to Cursor** and **Add to VS Code** buttons at the top of the [README](../README.md) add the server for you.
- **Claude Code**, **Codex CLI** and **Gemini CLI**: this repository is also a plugin that adds the MCP server and the `findadoctor` Agent Skill together. See [Install as a plugin](../README.md#install-as-a-plugin). The steps below add only the MCP server.

## Claude (claude.ai and Claude Desktop)

Available on Free, Pro, Max, Team and Enterprise. The Free plan allows one custom connector.

1. Customize → Connectors → **+ Add** → **Add custom connector**.
2. Enter a name (for example `FindADoctor.si`) and the MCP URL, then **Continue**.
3. Review the authentication settings Claude detected, then **Continue**.
4. Under Authentication choose **No sign in**, then **Add**. To use an account key instead, add it under Request headers as `Authorization: Bearer <key>`.
5. In a chat, turn it on with **+** → **Connectors**.

On Team and Enterprise, an Owner adds the connector first under Organization settings → Connectors, and members then connect it.

Guide: [Get started with custom connectors using remote MCP](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

## ChatGPT

Where your plan and workspace allow custom MCP servers:

1. **Plugins** → **+** → **Add custom MCP server**.
2. Enter a name and the MCP URL, and choose no authentication.
3. **Create** it as a plugin and install it.
4. Start a new chat. If the home page has **Chat** and **Work** tabs, switch to **Work** first.
5. Type **@** and pick it.

OpenAI's menus differ between plans and have changed recently. Guides: [Connect from ChatGPT](https://developers.openai.com/plugins/deploy/connect-chatgpt), [Quickstart](https://developers.openai.com/plugins/quickstart)

## Claude Code

```bash
claude mcp add --transport http findadoctor https://api.findadoctor.si/mcp
```

Add `--scope user` to make it available in every project. With an account key, add `--header "Authorization: Bearer $FINDADOCTOR_KEY"` (kept in your own Claude Code settings, not in the project). To share it with a project, put this in `.mcp.json` at the project root:

```json
{
  "mcpServers": {
    "findadoctor": {
      "type": "http",
      "url": "https://api.findadoctor.si/mcp"
    }
  }
}
```

`.mcp.json` is usually committed, so never put a key itself in it. If the project needs one, add `"headers": {"Authorization": "Bearer ${FINDADOCTOR_KEY}"}` and let each person set `FINDADOCTOR_KEY`.

## Codex CLI

```bash
codex mcp add findadoctor --url https://api.findadoctor.si/mcp
```

Or add this to `~/.codex/config.toml`:

```toml
[mcp_servers.findadoctor]
url = "https://api.findadoctor.si/mcp"
```

With an account key, add `--bearer-token-env-var FINDADOCTOR_KEY` to the command, or set `bearer_token_env_var = "FINDADOCTOR_KEY"` in the config, and put the key in that environment variable.

## Gemini CLI

```bash
gemini mcp add --transport http findadoctor https://api.findadoctor.si/mcp
```

Or in `~/.gemini/settings.json` (all projects) or `.gemini/settings.json` (one project):

```json
{
  "mcpServers": {
    "findadoctor": {
      "httpUrl": "https://api.findadoctor.si/mcp"
    }
  }
}
```

`gemini mcp add` saves to the project's `.gemini/settings.json` unless you add `--scope user`. With an account key, keep it out of project files: use your user settings and refer to the key by its environment variable, which Gemini CLI fills in when it loads the settings:

```bash
gemini mcp add --scope user --transport http --header 'Authorization: Bearer ${FINDADOCTOR_KEY}' findadoctor https://api.findadoctor.si/mcp
```

The single quotes keep your shell from writing the key itself into the file. In `settings.json` the same is `"headers": {"Authorization": "Bearer ${FINDADOCTOR_KEY}"}`.

Guides: [MCP servers with the Gemini CLI](https://github.com/google-gemini/gemini-cli/blob/main/docs/tools/mcp-server.md), [environment variables in settings](https://github.com/google-gemini/gemini-cli/blob/main/docs/reference/configuration.md)

## Cursor

Add to `~/.cursor/mcp.json` (all projects) or `.cursor/mcp.json` (one project):

```json
{
  "mcpServers": {
    "findadoctor": {
      "url": "https://api.findadoctor.si/mcp"
    }
  }
}
```

With an account key, add `"headers": {"Authorization": "Bearer ${env:FINDADOCTOR_KEY}"}` next to `url`; Cursor fills in the environment variable.

Guide: [Model Context Protocol in Cursor](https://cursor.com/docs/mcp)

## VS Code (GitHub Copilot agent mode)

Run **MCP: Add Server** from the Command Palette and give it the URL, or add this to `.vscode/mcp.json`:

```json
{
  "servers": {
    "findadoctor": {
      "type": "http",
      "url": "https://api.findadoctor.si/mcp"
    }
  }
}
```

With an account key, let VS Code prompt for it and store it:

```json
{
  "inputs": [
    { "type": "promptString", "id": "findadoctor-key", "description": "FindADoctor.si account key", "password": true }
  ],
  "servers": {
    "findadoctor": {
      "type": "http",
      "url": "https://api.findadoctor.si/mcp",
      "headers": { "Authorization": "Bearer ${input:findadoctor-key}" }
    }
  }
}
```

Guide: [Add and manage MCP servers in VS Code](https://code.visualstudio.com/docs/agent-customization/mcp-servers)

## Any other MCP client

Use Streamable HTTP with the URL above. The server supports MCP protocol versions `2025-11-25`, `2025-06-18` and `2025-03-26`. Its [server card](https://api.findadoctor.si/mcp/server-card) and [MCP Registry entry](https://registry.modelcontextprotocol.io/v0.1/servers/si.findadoctor.api%2Fus-doctor-finder/versions/latest) describe it in machine-readable form. When it connects, the server also sends usage instructions, and the `findadoctor://guide/how-to-use` resource holds the full guide.

## No MCP: the HTTP API

Every tool is also a plain `GET` endpoint that returns the same JSON:

```text
https://api.findadoctor.si/api/v1/search?condition=...&city=...&state=...
https://api.findadoctor.si/api/v1/doctors?ids=dr_...,dr_...
```

OpenAPI 3.1 description: https://api.findadoctor.si/openapi.json. An agent that can only fetch web pages can follow the [Agent Skill](../skills/findadoctor/SKILL.md) or [`/llms.txt`](https://findadoctor.si/llms.txt).
