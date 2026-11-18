#!/bin/sh
# Enforces the line limits in AGENTS.md (Hard rules): every CONTEXT.md under
# CONTEXT_LIMIT lines, every other tracked Markdown file under DOC_LIMIT lines.
# Append-only records in EXEMPT are skipped.
CONTEXT_LIMIT=80
DOC_LIMIT=200
EXEMPT="CHANGELOG.md docs/megaplan/done.md"

# The loop runs in a subshell (right side of a pipe), so it reports through
# its output, which is collected here.
problems=$(git ls-files '*.md' | while IFS= read -r f; do
  case " $EXEMPT " in *" $f "*) continue ;; esac
  if [ ! -f "$f" ]; then
    case "$f" in
      '"'*) echo "$f: name is quoted by git, cannot check it (error)" ;;
    esac
    continue # tracked but deleted in the working tree
  fi
  case "$f" in
    CONTEXT.md | */CONTEXT.md) limit=$CONTEXT_LIMIT ;;
    *) limit=$DOC_LIMIT ;;
  esac
  # awk counts a final line without a newline; wc -l would not.
  lines=$(awk 'END { print NR }' < "$f")
  if [ "$lines" -ge "$limit" ]; then
    echo "$f: $lines lines (must be under $limit)"
  fi
done)

if [ -n "$problems" ]; then
  echo "$problems"
  exit 1
fi
exit 0
