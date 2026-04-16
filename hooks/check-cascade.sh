#!/usr/bin/env bash
# Check for pending cascade suggestions at session start
CASCADES="$(pwd)/.claude/cascade/pending-*.md"
COUNT=$(ls $CASCADES 2>/dev/null | wc -l)
if [ "$COUNT" -gt 0 ]; then
  echo "[cascade] $COUNT pending research→engineering suggestions in .claude/cascade/" >&2
  for f in $CASCADES; do
    echo "  - $(head -3 "$f" | tail -1)" >&2
  done
fi
exit 0
