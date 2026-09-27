#!/usr/bin/env bash
# install.sh <claude|opencode|antigravity> — copy THIS harness's orchestration files from the repo.
# Backup-then-copy: an existing file that differs from the repo copy is first backed up to
# <dest>/backups/<parent-dir>.<name>.<YYYYmmdd-HHMMSS>.bak, then overwritten. Re-running is idempotent
# (byte-identical files are simply reinstalled, no new backups).
# Claude only: also merges the one PreToolUse hook entry (manager-boundary.sh --global) into
# settings.json — backup-first, atomic mv, skipped when already present.
# Deliberately NOT done here (manual — see docs/): personal MCP/allow rules, OpenCode config
# wiring, enabling the Antigravity plugin in ~/.gemini/config/config.json, any other config edit.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_CMD='~/.claude/hooks/manager-boundary.sh --global'
usage() { echo "usage: $0 <claude|opencode|antigravity>" >&2; exit 1; }
[ $# -eq 1 ] || usage

# $1=mode $2=repo file $3=installed file — back up the old one first if it exists and differs.
place() {
  if [ -f "$3" ] && ! cmp -s "$2" "$3"; then
    cp -p "$3" "$BACKUPS/$(basename "$(dirname "$3")").$(basename "$3").$(date +%Y%m%d-%H%M%S).bak"
  fi
  install -m "$1" "$2" "$3"
}

case "$1" in
claude)
  D="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"; BACKUPS="$D/backups"
  command -v jq >/dev/null || { echo "jq is required" >&2; exit 1; }
  mkdir -p "$D/agents" "$D/hooks" "$BACKUPS"
  for f in "$SRC"/agents/*.md; do place 0644 "$f" "$D/agents/$(basename "$f")"; done
  place 0755 "$SRC/hooks/manager-boundary.sh" "$D/hooks/manager-boundary.sh"
  SETTINGS="$D/settings.json"
  [ -s "$SETTINGS" ] || echo '{}' >"$SETTINGS"   # missing OR empty -> start from {}
  if jq -e --arg c "$HOOK_CMD" '[.hooks.PreToolUse[]?.hooks[]? | select(.command==$c)] | length > 0' "$SETTINGS" >/dev/null; then
    echo "settings.json: manager-boundary hook already present"
  else
    cp -p "$SETTINGS" "$BACKUPS/settings.json.$(date +%Y%m%d-%H%M%S).bak"
    tmp=$(mktemp "$SETTINGS.XXXXXX")           # same directory -> atomic rename
    jq --arg c "$HOOK_CMD" '.hooks.PreToolUse = ((.hooks.PreToolUse // []) + [{matcher:"*",hooks:[{type:"command",command:$c,timeout:10}]}])' "$SETTINGS" >"$tmp"
    chmod --reference="$SETTINGS" "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "settings.json: manager-boundary hook added (backup in $BACKUPS/)"
  fi
  echo "Installed claude agents + manager-boundary hook into $D."
  echo "Start the manager with:  claude --agent manager"
  ;;
opencode)
  D="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"; BACKUPS="$D/backups"
  mkdir -p "$D/agents" "$D/presets" "$BACKUPS"
  for f in "$SRC"/opencode/agents/*.md; do place 0644 "$f" "$D/agents/$(basename "$f")"; done
  for f in "$SRC"/opencode/presets/*.tsv; do place 0644 "$f" "$D/presets/$(basename "$f")"; done
  place 0755 "$SRC/opencode/oc-preset" "$D/oc-preset"
  place 0644 "$SRC/opencode/AGENTS.md" "$D/AGENTS.md"
  echo "Installed opencode agents, oc-preset, presets and AGENTS.md into $D."
  echo "Config wiring and personal MCP allow rules are manual — see docs/opencode.md"
  ;;
antigravity)
  D="${GEMINI_CONFIG_DIR:-$HOME/.gemini/config}"; BACKUPS="$D/backups"; P="$D/plugins/multitask-team"
  mkdir -p "$P/agents" "$P/rules" "$BACKUPS"
  place 0644 "$SRC/antigravity/multitask-team/plugin.json" "$P/plugin.json"
  place 0644 "$SRC/antigravity/multitask-team/rules/AGENTS.md" "$P/rules/AGENTS.md"
  for d in "$SRC"/antigravity/multitask-team/agents/*/; do
    n=$(basename "$d"); mkdir -p "$P/agents/$n"
    place 0644 "${d}agent.md" "$P/agents/$n/agent.md"
  done
  A="${AGYO_BIN_DIR:-$HOME/.local/bin}/agyo"
  mkdir -p "$(dirname "$A")"
  place 0755 "$SRC/antigravity/agyo" "$A"
  echo "Installed antigravity plugin into $P (+ agyo -> $A)."
  echo "Enable the plugin in ~/.gemini/config/config.json — see docs/antigravity.md"
  ;;
*) usage ;;
esac
