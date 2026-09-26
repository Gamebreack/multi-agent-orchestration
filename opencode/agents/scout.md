---
mode: subagent
model: openai/gpt-6-luna
variant: medium
hidden: true
permission:
  "*": deny
  read: allow
  glob: allow
  grep: allow
  list: allow
  lsp: allow
  webfetch: allow
  websearch: allow
  edit: deny
  bash: deny
  task:
    "*": deny
  external_directory: ask
---
