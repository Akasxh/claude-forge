#!/usr/bin/env bash
# Setup scheduled agents for self-evolution
# Run this once to register the schedules.
# Requires: Claude Code with remote trigger support.

cat << 'EOF'
=== Scheduled Self-Evolution Agents ===

To set up these schedules, run each command in a Claude Code session:

1. Weekly Forge gap analysis (Sundays 2am UTC):
   /schedule create --name "forge-weekly-gap" --cron "0 2 * * 0" --prompt "Read ~/.claude/agents/forge-lead.md and adopt it. Run /forge:gap to inventory the full workforce and produce a gap report. Write to ~/.claude/forge/gap-reports/$(date +%Y-%m-%d)-scheduled.md"

2. Monthly memory consolidation (1st of month, 3am UTC):
   /schedule create --name "memory-monthly-consolidation" --cron "0 3 1 * *" --prompt "Read ~/.claude/agent-memory/research-lead/MEMORY.md. Identify lessons >90 days old that were never reinforced. Mark them Stale. Identify lessons reinforced 3+ times. Promote their rule-of-thumb to the top of MEMORY.md as a 'core principle'. Write a consolidation report."

3. Weekly infrastructure self-test (Saturdays 1am UTC):
   /schedule create --name "infra-weekly-test" --cron "0 1 * * 6" --prompt "Run bash ~/.claude/scripts/test-infrastructure.sh and report results. If any test fails, write a detailed failure report to ~/.claude/infra-test-results/$(date +%Y-%m-%d).md"

To list active schedules: /schedule list
To run one manually: /schedule run <name>
To disable: /schedule update <name> --enabled false
EOF
