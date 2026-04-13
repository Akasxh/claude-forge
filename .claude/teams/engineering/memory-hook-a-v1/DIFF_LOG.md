# DIFF_LOG — memory-hook-a-v1

Schema: ## Iteration N — Task <task_id>: <title> / File / Change / Reason / Acceptance criterion addressed

## Iteration 1 — Task 1: Edit 1.1 — Hard rules access-control addition
- **File**: `~/.claude/agents/research/research-scribe.md`
- **Change**: Added 4-line access-control rule to the `# Hard rules` section after the INDEX.md line. States that only scribe + retrospector write to `~/.claude/agent-memory/research-lead/`.
- **Reason**: Minimum viable addition; no existing content modified. Establishes the access-control invariant needed for topic-file routing integrity.
- **Acceptance criterion addressed**: AC #1 (topic routing infrastructure), AC #3 (backward-compatible — additive only)

## Iteration 2 — Task 2: Edit 1.5 — Session-start catch-up routing pass
- **File**: `~/.claude/agents/research/research-scribe.md`
- **Change**: Added "Catch-up routing pass (Hook A v2.1)" paragraph to Method step 1 (session start). Reads MEMORY.md for un-routed lessons from skipped closes, applies routing predicate as recovery, logs with `scribe-curator: catch-up routed Lesson <N>`.
- **Reason**: Addresses skeptic Attack 3 — if scribe is skipped at session close, new lessons never get routed. Recovery pass is idempotent and runs only if un-routed lessons exist.
- **Acceptance criterion addressed**: AC #1, AC #3

## Iteration 3 — Task 3: Edit 1.2 — Routing predicate + stub schema (core Hook A)
- **File**: `~/.claude/agents/research/research-scribe.md`
- **Change**: Replaced the single-step "Check total size" (old step 4) with a new step 4 (topic-file routing predicate with full predicate logic, sub-predicate definitions, steps a-d, and atomicity constraint) and a new step 5 (the size check, now AFTER routing). 
- **Reason**: This is the core Hook A behavior. The predicate is `LENGTH >= 1500 AND type_condition` (AND, not OR; moderator C-deeper-1). Table threshold ≥10 rows (skeptic Attack 7). Rule of thumb field preserved verbatim. See: pointer is new.
- **Acceptance criterion addressed**: AC #1 (topic-file routing section — primary), AC #3

## Iteration 4 — Task 4: Edit 1.3 — AKL frontmatter schema section
- **File**: `~/.claude/agents/research/research-scribe.md`
- **Change**: Appended a new section "Topic file optional YAML frontmatter (Hook A v2.1)" after the Hard rules for MEMORY.md curation section. Includes YAML schema with AKL scoring fields and the AKL formulas from ByteRover arxiv 2604.01599 § 3.2.3.
- **Reason**: Forward-looking documentation for Hook B MCP server compatibility. The frontmatter is OPTIONAL — Hook A works without it. Adopts ByteRover's formulas as spec (not product).
- **Acceptance criterion addressed**: AC #1 (topic file format), AC #4 (no new infra — pure documentation)

## Iteration 5 — Task 5: Edit 1.4 — Hook B trigger metric section
- **File**: `~/.claude/agents/research/research-scribe.md`
- **Change**: Appended a new section "Hook A → Hook B trigger metric (v2.1)" at end of file. Specifies the 7-step topic-file-hit audit, the `scribe-metric:` LOG line format, and the rolling-window distinct-miss-event escalation thresholds (≥3/10 sessions → Hook B warranted).
- **Reason**: Provides the empirical trigger for Hook B (SQLite+FTS5+sqlite-vec MCP). Skeptic Attack 2 refinement: distinct-miss-events is noise-robust for small sample sizes vs. miss_rate > 20%.
- **Acceptance criterion addressed**: AC #5 (test plan — empirical trigger for Hook B)

## Iteration 6 — Task 6: Edit 2.1 — Lazy pointer protocol in research-lead.md intake Step 3
- **File**: `~/.claude/agents/research/research-lead.md`
- **Change**: Added "Topic files — lazy pointer protocol (v2.1, Hook A)" paragraph to intake Step 3 (Consult MEMORY.md). Describes `See: <filename>.md` lazy pointer, on-demand Read only when topic matches, ≤3 topic files per session as expected ceiling.
- **Reason**: Teaches research-lead to consume topic files created by the scribe. Lazy loading (not preload at session start) prevents context bloat.
- **Acceptance criterion addressed**: AC #2 (research-lead knows to read topic files lazily)

## Iteration 7 — Task 7: Edit 2.2 — Topic-file invariant in research-lead.md Rules section
- **File**: `~/.claude/agents/research/research-lead.md`
- **Change**: Added "Topic files under ~/.claude/agent-memory/research-lead/ are read-only for you" rule after "Files are the memory" rule. States lead may Read but must NEVER WRITE; scribe is the writer.
- **Reason**: Enforces the access-control invariant (Edit 1.1 established it in scribe; Edit 2.2 establishes the complementary invariant in lead).
- **Acceptance criterion addressed**: AC #2, AC #3
