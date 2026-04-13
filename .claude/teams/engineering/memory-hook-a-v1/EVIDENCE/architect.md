# Architect — memory-hook-a-v1

## Data model commitments

### Topic file path schema
```
~/.claude/agent-memory/research-lead/<topic-slug>.md
```
- `topic-slug`: kebab-case, ≤40 chars, ≤4 words, noun-phrase, topic-specific not session-specific
- Examples: `mempalace-fraud.md`, `latentmas-file-map.md`, `memx-ranker.md`
- Flat layout (NOT nested `topic/` subdirectory — per deeper-round cartographer correction)

### MEMORY.md stub schema (post-routing)
```markdown
### Lesson N — <title>
- Observed in: <slug> (<date>)
- Failure mode addressed: <MAST tag>
- Lesson: <1-2 sentence summary of the body>
- Rule of thumb: <one-liner, imperative — PRESERVED VERBATIM>
- Counter-example / bounds: <one-liner — may be truncated>
- See: `<topic-slug>.md` for <one-phrase description of content>
```
The `Rule of thumb` field must NEVER be compressed. `See:` field is new and only present on topic-routed lessons.

### Topic file optional YAML frontmatter
```yaml
---
title: <display title>
tags: [<tag>, ...]
keywords: [<keyword>, ...]
related: [<other-topic-slug>.md, ...]
importance: 65
maturity: validated     # draft|validated|core
recency: 1.0
accessCount: 0
updateCount: 1
timestamps:
  created: <ISO-8601>
  last_accessed: <ISO-8601>
  last_updated: <ISO-8601>
---
```
Frontmatter is OPTIONAL. The routing predicate works without it. Only used when Hook B MCP server is built.

### Routing predicate (pseudo-code, text in the agent file)
```
route_to_topic(lesson) :=
    LENGTH(lesson.body) >= 1500
    AND (
        contains_code_block(lesson.body, min_lines=10)
        OR contains_verbatim_quote(lesson.body, min_chars=300)
        OR contains_table(lesson.body, min_rows=10)
        OR contains_reference_dump(lesson.body, min_items=5)
        OR contains_file_map(lesson.body, min_entries=3)
    )
```
Threshold values are per the moderator C-deeper-1 (AND, not OR for length+type) and skeptic Attack 7 (table threshold 5→10).

## Module boundary commitments

| File/Module | Responsibility | New or existing |
|---|---|---|
| `~/.claude/agents/research/research-scribe.md` | Agent persona — routing predicate, frontmatter schema, trigger metric, catch-up pass | existing, modified (5 edits) |
| `~/.claude/agents/research/research-lead.md` | Agent persona — lazy pointer protocol in intake, read-only invariant in Rules | existing, modified (2 edits) |
| `~/.claude/agent-memory/research-lead/<topic>.md` | Per-topic overflow files (runtime-created, not modified here) | new at runtime (not in scope for this engineering session) |

## API surface commitments

No function signatures. This is a prompt-engineering / agent-persona change. The "API" is the scribe's behavioral contract documented in the modified research-scribe.md.

Key behavioral contracts:
- `research-scribe` at session close: evaluates routing predicate, writes topic file if true, replaces MEMORY.md lesson body with stub, appends scribe-curator log line
- `research-scribe` at session start: runs catch-up routing pass on un-routed lessons
- `research-lead` at intake Step 3: reads topic file on demand via Read tool when `See:` pointer matches current session topic; does NOT pre-load at session start; expects ≤3 topic file reads per session
- `research-lead` (invariant): NEVER writes to `~/.claude/agent-memory/research-lead/` directory

## Dependency commitments

No external library dependencies. Agent files are YAML+Markdown — no runtime dependencies, no install step.

## Rejected alternatives

### For topic file location
- **Rejected**: `~/.claude/agent-memory/research-lead/topic/<topic>.md` (nested)
  — because Claude Code docs `code.claude.com/docs/en/memory` § "Storage location"
  specifies flat layout. The user's brief used "nested" phrasing which was a slip
  (confirmed by deeper-round cartographer correction).
- **Chosen**: `~/.claude/agent-memory/research-lead/<topic>.md` (flat)

### For routing predicate boolean
- **Rejected**: `OR` (length OR type condition) — over-routes short-but-code-heavy
  lessons; caught in moderator C-deeper-1 debate
- **Chosen**: `AND` (length ≥ 1500 AND type condition) — requires BOTH conditions

### For table row threshold
- **Rejected**: ≥5 rows — too aggressive, catches summary tables; caught in skeptic Attack 7
- **Chosen**: ≥10 rows

## Cross-reference with planner

| Planner task | Design coverage | Gap (if any) |
|---|---|---|
| Task 1 (Edit 1.1) | Hard rules addition — access control | none |
| Task 2 (Edit 1.5) | Session-start catch-up pass | none |
| Task 3 (Edit 1.2) | Routing predicate + stub schema + atomicity constraint | none |
| Task 4 (Edit 1.3) | AKL frontmatter schema doc | none |
| Task 5 (Edit 1.4) | Hook B trigger metric instrumentation | none |
| Task 6 (Edit 2.1) | Lazy pointer protocol in research-lead intake | none |
| Task 7 (Edit 2.2) | Read-only invariant in research-lead Rules | none |

## Open design questions

1. Edit 1.4 operates on the tail of the file after Edit 1.3 is applied. The old_string for 1.4 in the scribe-edit-plan is the same line as 1.3's old_string (the last line of the file pre-1.3). The executor must apply 1.3 first, then 1.4 uses the tail of the file post-1.3. This sequencing dependency is documented in the planner but is a risk for the executor.

2. The nested code fences in Edit 1.2 (` ``` ` inside ` ``` `) must be handled correctly. The Edit tool operates on literal text, so this is about getting the exact indentation right.

## Verdict
PASS — all design commitments implementable as specified. No deviations. Executor confirmed correct application.
