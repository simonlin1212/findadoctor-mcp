# Changelog

Changes to this repository. Changes to the service itself are listed at https://findadoctor.si/us/changelog/.

## 2026-10-15

- New Zealand: a second MCP server, `https://api-nz.findadoctor.si/mcp` (MCP Registry `si.findadoctor.api-nz/nz-doctor-finder`). README section, connection guide, tool reference generated from the live server (`docs/tools-nz.md`, `reference/tools-nz.json`, service version nz-2026-10-15.2) and a copy of its registry entry (`server-nz.json`).
- The plugins for Claude Code, Codex and Gemini CLI now add both servers (`findadoctor` and `findadoctor-nz`), and the `findadoctor` Agent Skill covers New Zealand. Plugin version 2026.10.15.
- US tool reference regenerated for service version 2026-10-15.1 (no change to the tools).

## 2026-10-13

- First version: README, connection guide for Claude, ChatGPT, Claude Code, Codex CLI, Gemini CLI, Cursor and VS Code, tool reference generated from the live server (service version 2026-10-13.3), sample replies, runnable examples (curl, Python, TypeScript) and the `findadoctor` Agent Skill.
- Tool reference regenerated for service version 2026-10-13.4: the `medicare_patient` description now states the emergency and urgent-care exception.
- README: banner, badges, one-click buttons for Cursor and VS Code, a quick start your agent can follow, and a without/with comparison. The repository is now also a plugin for Claude Code, Codex (Agent Plugins) and Gemini CLI, adding the MCP server and the `findadoctor` skill in one install.
