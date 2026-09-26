## OpenCode MCP permissions (lesson learned)

- The default primary agent `orchestrator` runs with default-deny permissions. Every configured
  MCP server needs an explicit rule matching the prefix of its injected tools, e.g.
  `<server-name>_*: allow`. Without it the server can show as connected while none of its
  tools are injected/exposed to the agent.
- When diagnosing, do not infer tool availability from MCP resources/templates: tool-only MCP
  servers may expose neither. Check that the server is configured and enabled, its connection
  status, the agent's permission prefix, and the tools actually injected in a fresh session.
- OpenCode config and agent permissions are loaded at startup; restart OpenCode after changes.
