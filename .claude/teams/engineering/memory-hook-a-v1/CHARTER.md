# CHARTER — memory-hook-a-v1

## Raw prompt (verbatim)
Implement Hook A from the memory-layer research: extend `research-scribe`'s
MEMORY.md curation to ALSO route long-tail overflow to per-topic files at
`~/.claude/agent-memory/research-lead/<topic-slug>.md`, leave reference pointer
in MEMORY.md.

## Assumed interpretation
Apply the 7 edit-diffs from `EVIDENCE/scribe-edit-plan.md` to two agent
files. The edits add topic-file routing predicate, AKL frontmatter schema,
Hook B trigger metric, catch-up routing pass, and lazy-pointer protocol
to research-lead. Adapt old_strings to current file state (files were updated
after scribe-edit-plan.md was written — v2.1 staging pattern was added).

## Tier
**SCOPED** (stated in prompt). 2 files, isolated behavior change, no new
infrastructure. Plan-adversary required because CHARTER cites research SYNTHESIS.

## Acceptance criteria (measurable)

1. `~/.claude/agents/research/research-scribe.md` has a topic-file routing
   section: when a lesson body ≥ 1500 chars AND contains a qualifying block
   (code ≥10 lines / verbatim quote ≥300 chars / table ≥10 rows /
   reference dump ≥5 items / file map ≥3 entries), extract body into
   `~/.claude/agent-memory/research-lead/<topic-slug>.md`, leave stub +
   `See:` pointer in MEMORY.md.
2. `~/.claude/agents/research/research-lead.md` knows to read topic files
   lazily when a topic becomes relevant (lazy pointer protocol in intake Step 3).
3. Backward-compatible with existing MEMORY.md entries (no existing entry
   structure is broken).
4. No new infra, no new dependencies.
5. A brief test plan for verification.

## Cross-team references

- PRIMARY (binding): `~/.claude/teams/research/claude-memory-layer-sota-2026q2/SYNTHESIS.md`
  Phase 1 (Hook A) — HIGH confidence
- PRIMARY (binding): `~/.claude/teams/research/claude-memory-layer-sota-2026q2-deeper/SYNTHESIS.md`
  — engineering-grade detail, evaluator PASS on all 5 dims
- EDIT PLAN (binding): `~/.claude/teams/research/claude-memory-layer-sota-2026q2-deeper/EVIDENCE/scribe-edit-plan.md`
  — 7 Edit-tool-ready old/new pairs. NOTE: old_strings verified against
  an earlier version. Must read current files first and adapt.

## Session slug
memory-hook-a-v1

## Session start
2026-04-12
