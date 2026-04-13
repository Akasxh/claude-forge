#!/usr/bin/env bash
# claude-forge installer
# Copies agents, protocols, scripts, hooks, skills, and forge to ~/.claude/
# Backs up existing files before overwriting.

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
CLAUDE_DIR="$HOME/.claude"
BACKUP_TS="$(date +%Y%m%d-%H%M%S)"

echo "=== claude-forge installer ==="
echo "Source:  $SCRIPT_DIR"
echo "Target:  $CLAUDE_DIR"
echo ""

# --- helpers ---
backup_if_exists() {
  local target="$1"
  if [ -e "$target" ]; then
    local backup="${target}.bak-${BACKUP_TS}"
    echo "  backup: $(basename "$target") -> $(basename "$backup")"
    cp -r "$target" "$backup"
  fi
}

copy_dir() {
  local src="$1" dst="$2"
  mkdir -p "$dst"
  if [ -d "$src" ]; then
    cp -r "$src"/. "$dst"/
    echo "  copied: $src -> $dst"
  fi
}

copy_file() {
  local src="$1" dst="$2"
  mkdir -p "$(dirname "$dst")"
  if [ -f "$src" ]; then
    backup_if_exists "$dst"
    cp "$src" "$dst"
    echo "  copied: $(basename "$src")"
  fi
}

# --- agents ---
echo "Installing agents..."
for team in research-team engineering-team; do
  src_dir="$SCRIPT_DIR/agents/$team"
  if [ "$team" = "research-team" ]; then
    dst_dir="$CLAUDE_DIR/agents/research"
  else
    dst_dir="$CLAUDE_DIR/agents/engineering"
  fi
  if [ -d "$src_dir" ]; then
    backup_if_exists "$dst_dir"
    copy_dir "$src_dir" "$dst_dir"
  fi
done

# Forge lead (single file, not a team subdir)
if [ -f "$SCRIPT_DIR/agents/forge/forge-lead.md" ]; then
  copy_file "$SCRIPT_DIR/agents/forge/forge-lead.md" "$CLAUDE_DIR/agents/forge-lead.md"
fi

# --- protocols ---
echo "Installing protocols..."
mkdir -p "$CLAUDE_DIR/teams/research" "$CLAUDE_DIR/teams/engineering"
copy_file "$SCRIPT_DIR/agents/research-team/PROTOCOL.md" "$CLAUDE_DIR/teams/research/PROTOCOL.md"
copy_file "$SCRIPT_DIR/agents/engineering-team/PROTOCOL.md" "$CLAUDE_DIR/teams/engineering/PROTOCOL.md"

# --- scripts ---
echo "Installing scripts..."
mkdir -p "$CLAUDE_DIR/scripts"
for f in "$SCRIPT_DIR"/scripts/*; do
  [ -f "$f" ] && copy_file "$f" "$CLAUDE_DIR/scripts/$(basename "$f")"
done
chmod +x "$CLAUDE_DIR/scripts/"*.sh 2>/dev/null || true
chmod +x "$CLAUDE_DIR/scripts/"*.py 2>/dev/null || true

# --- hooks ---
echo "Installing hooks..."
mkdir -p "$CLAUDE_DIR/hooks"
for f in "$SCRIPT_DIR"/hooks/*; do
  [ -f "$f" ] && copy_file "$f" "$CLAUDE_DIR/hooks/$(basename "$f")"
done
chmod +x "$CLAUDE_DIR/hooks/"*.sh 2>/dev/null || true

# --- memory seeds ---
echo "Installing memory seeds..."
for agent in research-lead engineering-lead forge-lead research-retrospector; do
  src="$SCRIPT_DIR/memory/${agent}.md"
  dst="$CLAUDE_DIR/agent-memory/$agent/MEMORY.md"
  if [ -f "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    if [ -f "$dst" ]; then
      echo "  skip (exists): $agent/MEMORY.md"
    else
      cp "$src" "$dst"
      echo "  seeded: $agent/MEMORY.md"
    fi
  fi
done

# Create staging dirs
for agent in research-lead engineering-lead; do
  mkdir -p "$CLAUDE_DIR/agent-memory/$agent/staging"
done

# --- forge ---
echo "Installing Capability Forge..."
if [ -d "$SCRIPT_DIR/agents/forge" ]; then
  mkdir -p "$CLAUDE_DIR/forge/.claude-plugin"
  [ -f "$SCRIPT_DIR/agents/forge/plugin.json" ] && \
    copy_file "$SCRIPT_DIR/agents/forge/plugin.json" "$CLAUDE_DIR/forge/.claude-plugin/plugin.json"
  for skill_dir in "$SCRIPT_DIR"/agents/forge/skills/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$CLAUDE_DIR/forge/skills/$skill_name"
    [ -f "$skill_dir/SKILL.md" ] && \
      copy_file "$skill_dir/SKILL.md" "$CLAUDE_DIR/forge/skills/$skill_name/SKILL.md"
  done
fi

# Create forge working dirs
mkdir -p "$CLAUDE_DIR/forge/drafts" "$CLAUDE_DIR/forge/outputs" \
  "$CLAUDE_DIR/forge/workspaces" "$CLAUDE_DIR/forge/gap-reports" \
  "$CLAUDE_DIR/forge/scout-reports" "$CLAUDE_DIR/forge/research-requests" \
  "$CLAUDE_DIR/forge/registry-cache"

# --- skills ---
echo "Installing skills..."
if [ -d "$SCRIPT_DIR/skills" ]; then
  for skill_dir in "$SCRIPT_DIR"/skills/*/; do
    skill_name=$(basename "$skill_dir")
    mkdir -p "$CLAUDE_DIR/skills/$skill_name"
    [ -f "$skill_dir/SKILL.md" ] && \
      copy_file "$skill_dir/SKILL.md" "$CLAUDE_DIR/skills/$skill_name/SKILL.md"
  done
fi

# --- hooks registration in settings.json ---
echo "Registering hooks in settings.json..."
SETTINGS="$CLAUDE_DIR/settings.json"
if [ -f "$SETTINGS" ]; then
  # Merge hooks using Python
  python3 -c "
import json, sys

with open('$SETTINGS') as f:
    settings = json.load(f)

hooks = settings.setdefault('hooks', {})

# Add Stop hook if missing
if 'Stop' not in hooks:
    hooks['Stop'] = [{'matcher': '', 'hooks': [{'type': 'command', 'command': '\$HOME/.claude/hooks/session-capture.sh'}]}]
    print('  added: Stop hook')

# Add PostToolUse hook if missing
if 'PostToolUse' not in hooks:
    hooks['PostToolUse'] = [{'matcher': 'Write|Edit', 'hooks': [{'type': 'command', 'command': '\$HOME/.claude/hooks/log-evidence-writes.sh'}]}]
    print('  added: PostToolUse hook')

with open('$SETTINGS', 'w') as f:
    json.dump(settings, f, indent=2)
" 2>/dev/null || echo "  warning: could not merge hooks into settings.json (merge manually)"
else
  echo "  skip: no settings.json found (hooks will need manual registration)"
fi

# --- verification ---
echo ""
echo "=== Verification ==="
echo -n "Research agents:    "; ls "$CLAUDE_DIR/agents/research/"*.md 2>/dev/null | wc -l
echo -n "Engineering agents: "; ls "$CLAUDE_DIR/agents/engineering/"*.md 2>/dev/null | wc -l
echo -n "Forge skills:       "; ls "$CLAUDE_DIR/forge/skills/"*/SKILL.md 2>/dev/null | wc -l
echo -n "Scripts:            "; ls "$CLAUDE_DIR/scripts/" 2>/dev/null | wc -l
echo -n "Hooks:              "; ls "$CLAUDE_DIR/hooks/" 2>/dev/null | wc -l

echo ""
echo "=== Done ==="
echo "Restart Claude Code to pick up the new agents and hooks."
echo "Then try: claude  ->  'research how X works'"
