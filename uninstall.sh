#!/usr/bin/env bash
# Removes ONLY what install.sh added: the seven agents, manager-boundary.sh and its
# settings.json PreToolUse entry. Other agents, hooks and settings are left untouched.
set -euo pipefail
CLAUDE_DIR="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"
SETTINGS="$CLAUDE_DIR/settings.json"
HOOK_CMD='~/.claude/hooks/manager-boundary.sh --global'
for a in manager explorer mechanical-worker worker hard-worker reviewer verifier; do
  rm -f "$CLAUDE_DIR/agents/$a.md"
done
rm -f "$CLAUDE_DIR/hooks/manager-boundary.sh"
if [ -f "$SETTINGS" ] && command -v jq >/dev/null; then
  cp -p "$SETTINGS" "$CLAUDE_DIR/backups/settings.json.$(date +%Y%m%d-%H%M%S).uninstall.bak"
  tmp=$(mktemp "$SETTINGS.XXXXXX")
  # Remove only OUR hook element; keep sibling hooks in the same group; drop groups left empty.
  jq --arg c "$HOOK_CMD" '
    if (.hooks.PreToolUse | type) == "array" then
      .hooks.PreToolUse |= (map(.hooks |= map(select(.command != $c))) | map(select((.hooks | length) > 0)))
      | (if .hooks.PreToolUse == [] then del(.hooks.PreToolUse) else . end)
      | (if .hooks == {} then del(.hooks) else . end)
    else . end' "$SETTINGS" >"$tmp"
  chmod --reference="$SETTINGS" "$tmp"
  mv "$tmp" "$SETTINGS"
fi
echo "Uninstalled multi-agent orchestration setup. Backups remain in $CLAUDE_DIR/backups/."
