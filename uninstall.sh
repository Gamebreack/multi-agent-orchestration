#!/usr/bin/env bash
# uninstall.sh <claude|opencode|antigravity> [--purge] — remove THIS harness's installed files.
# A file is removed only while it is still byte-identical to the repo copy; user-modified files are
# kept and warned about on stderr. --purge backs a modified file up first, then removes it.
# Claude also drops our exact PreToolUse hook entry from settings.json (backup-first, atomic mv).
# Backups always live in <dest>/backups/ as <parent-dir>.<name>.<YYYYmmdd-HHMMSS>.bak; nothing is ever restored
# automatically. Deliberately NOT done here (manual — see docs/): config wiring, MCP/allow rules,
# the Antigravity plugin enable key in config.json, and any other config edit.
set -euo pipefail
SRC="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
HOOK_CMD='~/.claude/hooks/manager-boundary.sh --global'
usage() { echo "usage: $0 <claude|opencode|antigravity> [--purge]" >&2; exit 1; }
PURGE=0; SKIPPED=0; HARNESS=""
for a in "$@"; do
  case "$a" in
    --purge) PURGE=1 ;;
    *) [ -z "$HARNESS" ] || usage; HARNESS="$a" ;;
  esac
done
case "$HARNESS" in claude|opencode|antigravity) ;; *) usage ;; esac

# $1=repo file $2=installed file — remove only if byte-identical, else keep (or back up + purge).
unplace() {
  [ -f "$2" ] || return 0
  if cmp -s "$1" "$2"; then
    rm -f "$2"
  elif [ "$PURGE" = 1 ]; then
    cp -p "$2" "$BACKUPS/$(basename "$(dirname "$2")").$(basename "$2").$(date +%Y%m%d-%H%M%S).bak"
    rm -f "$2"
  else
    echo "skip (modified): $2" >&2
    SKIPPED=1
  fi
}

case "$HARNESS" in
claude)
  D="${CLAUDE_CONFIG_DIR:-$HOME/.claude}"; BACKUPS="$D/backups"
  mkdir -p "$BACKUPS"
  for f in "$SRC"/agents/*.md; do unplace "$f" "$D/agents/$(basename "$f")"; done
  unplace "$SRC/hooks/manager-boundary.sh" "$D/hooks/manager-boundary.sh"
  SETTINGS="$D/settings.json"
  if [ -f "$SETTINGS" ] && command -v jq >/dev/null &&
     jq -e --arg c "$HOOK_CMD" '[.hooks.PreToolUse[]?.hooks[]? | select(.command==$c)] | length > 0' "$SETTINGS" >/dev/null; then
    cp -p "$SETTINGS" "$BACKUPS/settings.json.$(date +%Y%m%d-%H%M%S).bak"
    tmp=$(mktemp "$SETTINGS.XXXXXX")           # same directory -> atomic rename
    # Remove only OUR hook element; keep sibling hooks in the same group; drop groups left empty.
    jq --arg c "$HOOK_CMD" '
      if (.hooks.PreToolUse | type) == "array" then
        .hooks.PreToolUse |= (map(.hooks |= map(select(.command != $c))) | map(select((.hooks | length) > 0)))
        | (if .hooks.PreToolUse == [] then del(.hooks.PreToolUse) else . end)
        | (if .hooks == {} then del(.hooks) else . end)
      else . end' "$SETTINGS" >"$tmp"
    chmod --reference="$SETTINGS" "$tmp"
    mv "$tmp" "$SETTINGS"
    echo "settings.json: manager-boundary hook entry removed (backup in $BACKUPS/)"
  fi
  echo "Uninstalled claude setup. Backups (if any) in $BACKUPS/"
  ;;
opencode)
  D="${OPENCODE_CONFIG_DIR:-$HOME/.config/opencode}"; BACKUPS="$D/backups"
  mkdir -p "$BACKUPS"
  for f in "$SRC"/opencode/agents/*.md; do unplace "$f" "$D/agents/$(basename "$f")"; done
  for f in "$SRC"/opencode/presets/*.tsv; do unplace "$f" "$D/presets/$(basename "$f")"; done
  unplace "$SRC/opencode/oc-preset" "$D/oc-preset"
  unplace "$SRC/opencode/AGENTS.md" "$D/AGENTS.md"
  echo "Uninstalled opencode setup. Backups (if any) in $BACKUPS/"
  ;;
antigravity)
  D="${GEMINI_CONFIG_DIR:-$HOME/.gemini/config}"; BACKUPS="$D/backups"; P="$D/plugins/multitask-team"
  mkdir -p "$BACKUPS"
  unplace "$SRC/antigravity/multitask-team/plugin.json" "$P/plugin.json"
  unplace "$SRC/antigravity/multitask-team/rules/AGENTS.md" "$P/rules/AGENTS.md"
  for d in "$SRC"/antigravity/multitask-team/agents/*/; do
    n=$(basename "$d")
    unplace "${d}agent.md" "$P/agents/$n/agent.md"
  done
  unplace "$SRC/antigravity/agyo" "${AGYO_BIN_DIR:-$HOME/.local/bin}/agyo"
  echo "Note: the plugin enable key in ~/.gemini/config/config.json stays (manual removal)."
  echo "Uninstalled antigravity setup. Backups (if any) in $BACKUPS/"
  ;;
esac
[ "$SKIPPED" = 0 ] || echo "re-run with --purge to remove modified files (they are backed up first)"
