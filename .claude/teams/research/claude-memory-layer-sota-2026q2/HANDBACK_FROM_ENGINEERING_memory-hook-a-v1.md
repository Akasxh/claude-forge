# HANDBACK FROM ENGINEERING — memory-hook-a-v1

## Shipped

- Session start: 2026-04-12
- Session close: 2026-04-12
- Tier: SCOPED
- Files modified: 2
  - `~/.claude/agents/research/research-scribe.md` (5 edits)
  - `~/.claude/agents/research/research-lead.md` (2 edits)
- Commits: no commits (agent persona files not in a tracked git repo under `~/.claude/agents/`)

## What matches research SYNTHESIS

- **Hook A topic-file routing predicate** — shipped as planned: `route_to_topic := LENGTH >= 1500 AND type_condition` with AND boolean (moderator C-deeper-1), table threshold ≥10 rows (skeptic Attack 7)
- **MEMORY.md stub schema** — shipped with `See: <filename>.md` pointer, `Rule of thumb` preserved verbatim instruction
- **Catch-up routing pass at session start** — shipped (Edit 1.5, skeptic Attack 3 fix)
- **AKL optional frontmatter schema** — shipped with ByteRover arxiv 2604.01599 attribution (MIXED source, spec borrowed not product adopted)
- **Hook B trigger metric** — shipped: `scribe-metric:` LOG format, distinct-miss-events ≥3/10-sessions escalation threshold (skeptic Attack 2 refinement)
- **Research-lead lazy pointer protocol** — shipped: `See: <filename>.md` lazy loading, ≤3 topic files per session ceiling, on-demand not preloaded
- **Topic-file read-only invariant in research-lead** — shipped: `Topic files under ~/.claude/agent-memory/research-lead/ are read-only for you`
- **Flat layout** — shipped: `~/.claude/agent-memory/research-lead/<topic>.md` (not nested `topic/` subdir), per cartographer correction

## What deviated from research SYNTHESIS

- **Edit 1.4 old_string adapted** — the scribe-edit-plan's Edit 1.4 old_string was the pre-Edit-1.3 tail of the file. After Edit 1.3 was applied, the tail changed. Engineering adapted Edit 1.4's old_string to the post-1.3 tail. This was anticipated in the scribe-edit-plan's Notes section ("If applied in sequence with Edit 1.3, target the new location after Edit 1.3 resolves"). No functional deviation — the content is identical to what the research team specified.

## Evaluator verdict

- Verdict: PASS
- Strict dimensions: functional correctness 1.0, test coverage 1.0
- Advisory dimensions: diff minimality 1.0, revert-safety 1.0, style conformance 1.0

## Open items

1. **Smoke test**: The Hook A routing predicate will fire for the first time on the NEXT research session that closes with a long lesson. Run a deliberate smoke test: create a research session with a deliberately long lesson (>1500 chars + code block ≥10 lines) and verify the scribe routes it to a topic file at session close.

2. **Trigger metric verification**: After 10 research sessions, manually count distinct miss events from LOG.md `scribe-metric:` lines. If ≥3, trigger Hook B (SQLite+FTS5+sqlite-vec MCP server per `EVIDENCE/mcp-scaffold.md`).

3. **audit_evidence.py schema gap**: The script reports `[no_terminal]` false positives on engineering Phase A specialist files (planner, architect). This is a research-protocol terminal schema being applied to engineering files. Engineering retrospector filed this as a protocol improvement for the next self-evolve session. Does not affect Hook A correctness.

## Lessons for research-lead MEMORY.md
(Not auto-merged — flagged for research-retrospector to consider at next research session close)

- **Edit-plan old_strings should include a "current-file" verification step as the first step of each task** — the engineering team adapted Edit 1.4's old_string because files had changed since the scribe-edit-plan was produced. Future research scribe-edit-plans could include a `grep -n <unique_phrase>` command as the first step of each edit task, to be run by the executor before applying. This removes a source of uncertainty in the cross-team handoff.
