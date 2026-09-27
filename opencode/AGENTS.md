# OpenCode MCP permissions (lesson learned)

- The default primary agent `orchestrator` runs with default-deny permissions (`permissions:` array, `"*"/"*" → deny` first). Every configured MCP server needs an explicit allow rule matching the action prefix of its injected tools, e.g. `- { action: <server>_<tool>, resource: "*", effect: allow }`. Without it the server can show as connected while none of its tools are injected/exposed to the agent.
- Agent `permissions` arrays run AFTER global rules (last match wins), so an appended MCP allow rule overrides the agent's own catch-all deny; a global block cannot, since global rules run first.
- When diagnosing, do not infer tool availability from MCP resources/templates: tool-only MCP servers may expose neither. Check that the server is configured and enabled, its connection status, the agent's allow rule, and the tools actually injected in a fresh session.
- OpenCode config and agent permissions are loaded at startup; restart OpenCode after changes.
