#!/usr/bin/env bash
# Installs the delegation-first multi-agent setup into ~/.claude (user scope).
#   - copies agents/*.md      -> ~/.claude/agents/
#   - copies hooks/*.sh       -> ~/.claude/hooks/
#   - merges ONE PreToolUse entry (manager-boundary.sh --global) into ~/.claude/settings.json
# Existing settings.json is backed up to ~/.claude/backups/settings.json.<timestamp>.bak.
# Re-running is idempotent. Unrelated agents/hooks/settings are never touched.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SETTINGS="$CLAUDE_DIR/settings.json"
HOOK_CMD='~/.claude/hooks/manager-boundary.sh --global'
command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }

mkdir -p "$CLAUDE_DIR/agents" "$CLAUDE_DIR/hooks" "$CLAUDE_DIR/backups"
for f in "$SRC"/agents/*.md; do
  dest="$CLAUDE_DIR/agents/$(basename "$f")"
  if [ -f "$dest" ] && ! cmp -s "$f" "$dest"; then cp -p "$dest" "$CLAUDE_DIR/backups/$(basename "$f").$(date +%Y%m%d-%H%M%S).bak"; fi
  install -m 0644 "$f" "$dest"
done
install -m 0755 "$SRC/hooks/manager-boundary.sh" "$CLAUDE_DIR/hooks/manager-boundary.sh"

[ -s "$SETTINGS" ] || echo '{}' >"$SETTINGS"   # missing OR empty -> start from {}
if jq -e --arg c "$HOOK_CMD" '[.hooks.PreToolUse[]?.hooks[]? | select(.command==$c)] | length > 0' "$SETTINGS" >/dev/null; then
  echo "settings.json: manager-boundary hook already present"
else
  cp -p "$SETTINGS" "$CLAUDE_DIR/backups/settings.json.$(date +%Y%m%d-%H%M%S).bak"
  tmp=$(mktemp "$SETTINGS.XXXXXX")           # same directory -> atomic rename
  jq --arg c "$HOOK_CMD" '.hooks.PreToolUse = ((.hooks.PreToolUse // []) + [{matcher:"*",hooks:[{type:"command",command:$c,timeout:10}]}])' "$SETTINGS" >"$tmp"
  chmod --reference="$SETTINGS" "$tmp"
  mv "$tmp" "$SETTINGS"
  echo "settings.json: manager-boundary hook added (backup in $CLAUDE_DIR/backups/)"
fi
echo "Installed. Agents: $(ls "$SRC"/agents/*.md | xargs -n1 basename | sed 's/\.md$//' | tr '\n' ' ')"
echo "Start the manager with:  claude --agent manager"
