---
name: forge
description: Dispatch the Capability Forge to detect workforce gaps, scout for existing implementations, or author new skills/MCPs/plugins. Use this skill when the user asks "what capability are we missing", "build a skill for X", "check MCP Registry for Y", "what skills should we add", "extend the workforce", or when a retrospective mentions a recurring capability gap.
---

# Capability Forge dispatch

You are invoking the Capability Forge (forge-lead, H1 architecture).

## What to do

1. Read `~/.claude/agent-memory/forge-lead/MEMORY.md` — authored skills catalog + process lessons.

2. Read `~/.claude/agents/forge-lead.md` — adopt this as your behavioral contract.

3. If the user specifies a gap, skip to step 5. Otherwise:

4. Run `/forge:gap` — inventory the workforce and detect gaps. Read the gap skill at `~/.claude/forge/skills/gap/SKILL.md` and execute its method.

5. Run `/forge:scout` — query MCP Registry + anthropics/skills + marketplaces for existing implementations. Read `~/.claude/forge/skills/scout/SKILL.md`.

6. Decision: INSTALL existing / ADOPT existing / AUTHOR new / DEFER to research.

7. If AUTHOR: run `/forge:draft` → `/forge:test` → `/forge:promote` pipeline.

8. If DEFER: write research-request drop-file and stop.

## Hard rules
- Never author what already exists — check registry + marketplaces first
- Never promote without passing /forge:test (≥3 eval cases, ≥0.8 pass rate)
- Every authored skill gets an ACE-style MEMORY.md bullet with helpful/harmful counters
- Research-request handoff is user-mediated (no automated polling)
