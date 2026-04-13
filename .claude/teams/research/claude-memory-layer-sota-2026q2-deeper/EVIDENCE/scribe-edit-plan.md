# Hook A — exact Edit-tool diffs for research-scribe.md and research-lead.md

This file contains the exact `old_string` / `new_string` pairs the forthcoming Engineering Team will apply with the Edit tool. Every diff is tested against the current files verbatim (read 2026-04-12). Apply in the order listed.

## File 1: `~/.claude/agents/research/research-scribe.md`

### Edit 1.1 — Add topic-file routing to the `Hard rules` section

**old_string** (from the current scribe.md, verbatim):

```
# Hard rules
- **Never edit the substance** of a specialist's file. Format only. If the
  substance is wrong, tell `research-lead` — don't rewrite.
- Never delete anything. Archiving is moving, never deleting.
- You are the only agent with write access to `INDEX.md`. Others read it.
```

**new_string**:

```
# Hard rules
- **Never edit the substance** of a specialist's file. Format only. If the
  substance is wrong, tell `research-lead` — don't rewrite.
- Never delete anything. Archiving is moving, never deleting.
- You are the only agent with write access to `INDEX.md`. Others read it.
- You are the only agent (besides `research-retrospector`) with write access
  to any file under `~/.claude/agent-memory/research-lead/`. Specialists
  NEVER write to this directory. If a specialist's evidence claims a
  topic-file update, that's a bug — escalate to `research-lead`.
```

### Edit 1.2 — Extend the MEMORY.md curation method with topic-file routing

**old_string** (from the current scribe.md, verbatim — this is the current step 4 of the curation method):

```
4. Check total size. If `MEMORY.md` exceeds 25KB, mark the bottom-quartile
   (oldest, least-reinforced) entries as `Archive candidate`. Do not delete;
   the lead's first 200 lines / 25KB injection is the natural forcing
   function, but you surface the pressure.
```

**new_string**:

```
4. **Topic-file routing** (Hook A — v2.1 addition). For each new or merged
   lesson, apply the routing predicate BEFORE doing the size check:

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

   Evaluate each sub-predicate mechanically:
   - `contains_code_block` — a ` ``` ` fenced block with ≥10 lines
   - `contains_verbatim_quote` — a `> ` blockquote with ≥300 characters
   - `contains_table` — a `|...|` markdown table with ≥10 rows (NOT 5 — post-skeptic-attack-7 correction: 5 is too aggressive and catches summary tables)
   - `contains_reference_dump` — a bullet list of ≥5 URL/arxiv/filepath citations
   - `contains_file_map` — ≥3 entries of the form `<path>:<number>` or `<path>/<subpath>`

   If the predicate returns TRUE, route the lesson to a topic file:

   a. Generate a kebab-case topic slug (≤40 chars, ≤4 words, noun-phrase,
      topic-specific not session-specific). Examples:
      `mempalace-fraud.md`, `latentmas-file-map.md`, `memx-ranker.md`.
   b. Use the Write tool (or Edit with create semantics) to create
      `~/.claude/agent-memory/research-lead/<topic-slug>.md` containing the
      FULL lesson body (prose + code + quote + table + references + file map).
      The topic file starts with a `# <Topic Title>` header and may include
      optional YAML frontmatter per the AKL schema (see Edit 1.3).
   c. Use the Edit tool to replace the lesson's body in MEMORY.md with a
      stub entry following this schema:

      ```markdown
      ### Lesson N — <title>
      - Observed in: <slug> (<date>)
      - Failure mode addressed: <MAST tag>
      - Lesson: <1-2 sentence summary of the body>
      - Rule of thumb: <one-liner, imperative — PRESERVED VERBATIM from the
        original lesson; this field must NOT be compressed>
      - Counter-example / bounds: <one-liner — may be truncated>
      - See: `<topic-slug>.md` for <one-phrase description of content>
      ```

      The `Rule of thumb` field is load-bearing and MUST be preserved
      verbatim. The `See:` field is NEW and only present on topic-routed
      lessons.

   d. Append a machine-parseable line to `LOG.md`:
      `scribe-curator: routed Lesson <N> to topic <topic-slug>.md | reason=<which-predicates-fired>`

   Atomicity: the topic-file write (b), the MEMORY.md stub edit (c), and
   the LOG.md line (d) are a single logical operation. If any step fails,
   roll back the others — do NOT leave orphan topic files or stubless
   index entries.

5. Check total size. If `MEMORY.md` exceeds 25KB AFTER routing, mark the
   bottom-quartile (oldest, least-reinforced) entries as `Archive candidate`.
   Do not delete; the lead's first 200 lines / 25KB injection is the
   natural forcing function, but you surface the pressure. Topic-routing
   from step 4 should have prevented most cases from reaching this step.
```

### Edit 1.3 — Optional frontmatter schema note for topic files

**old_string** (from the current scribe.md, verbatim — the very last line of file):

```
- You log every curation action to `LOG.md` with the prefix
  `scribe-curator:`.
```

**new_string**:

```
- You log every curation action to `LOG.md` with the prefix
  `scribe-curator:`.

# Topic file optional YAML frontmatter (Hook A v2.1)

Topic files in `~/.claude/agent-memory/research-lead/` may optionally
include YAML frontmatter for AKL (Adaptive Knowledge Lifecycle) scoring.
This is forward-looking: the Hook B MCP server (if built) uses these
fields for ranking; the plain text below the frontmatter is still valid
markdown if the frontmatter is absent.

```yaml
---
title: <display title>
tags: [<tag>, ...]
keywords: [<keyword>, ...]
related: [<other-topic-slug>.md, ...]   # @-annotations to related topic files
importance: 65                          # 0-100 (AKL score)
maturity: validated                     # draft|validated|core
recency: 1.0                            # exp(-Δt/30); 1.0 at creation
accessCount: 0
updateCount: 1
timestamps:
  created: <ISO-8601>
  last_accessed: <ISO-8601>
  last_updated: <ISO-8601>
---

# <Topic Title>

<body content>
```

**AKL scoring rules** (per ByteRover paper `arxiv 2604.01599` § 3.2.3):
- Each access event: `importance += 3`
- Each update event: `importance += 5`
- Daily decay: `importance *= 0.995`
- Maturity transitions (with hysteresis):
  - draft → validated at `importance ≥ 65`, demote at `< 35`
  - validated → core at `importance ≥ 85`, demote at `< 60`
- Recency: `recency = exp(-days_since_last_update / 30)` → ~21-day half-life

**When the AKL fields matter**: only if Hook B MCP server is built to
consume them. Until then, topic files work fine without frontmatter.
```

### Edit 1.4 — Add the "insufficient" metric instrumentation (optional but recommended)

**old_string** (the same location as Edit 1.3):

```
- You log every curation action to `LOG.md` with the prefix
  `scribe-curator:`.
```

(Note: this edit operates on the line added in Edit 1.3. If applied in
sequence with Edit 1.3, target the new location after Edit 1.3 resolves.)

**new_string** (appended after the frontmatter section from Edit 1.3):

```

# Hook A → Hook B trigger metric (v2.1)

At session close, after dedup and routing, perform a topic-file-hit audit:

1. Glob all `*.md` files in `~/.claude/agent-memory/research-lead/`
   except `MEMORY.md`.
2. For each topic file, check whether its slug or its title keywords
   appear in this session's:
   - `QUESTION.md` (sub-questions)
   - `SYNTHESIS.md`
   - any `EVIDENCE/*.md` file
3. Count as RELEVANT any topic file whose keywords overlap with the
   session's subject matter (simple case-insensitive substring match on
   the slug or the title).
4. Count as CITED any relevant topic file that was actually Read by the
   lead or a specialist (check for file path mentions in LOG.md or
   EVIDENCE files).
5. Compute `hit_rate = cited / (relevant+epsilon)` and `miss_rate = 1 - hit_rate`.
6. Append to LOG.md:

   ```
   scribe-metric: topic-file-check | slug=<session-slug> | total=<N> | relevant=<R> | cited=<C> | missed=<R-C> | hit-rate=<C/R>
   ```

7. A separate rolling-window analysis (manually or via a small script)
   counts the **distinct miss events** over the last 10 sessions (per
   skeptic Attack 2 correction — noise-robust for small samples):
   - **≥ 3 distinct miss events** (3+ distinct topic files that should
     have been read but weren't, across the last 10 sessions) → escalate:
     Hook B MCP server is warranted
   - **1-2 distinct miss events** → Hook A is MARGINAL, monitor 10 more
   - **0 distinct miss events** → Hook A is sufficient; Hook B not needed

The instrumentation is cheap (2 Read calls + ~50 tokens of reasoning per
session). Do not skip it — this is the empirical trigger for Hook B.
```

### Edit 1.5 — Session-start catch-up routing pass (post-skeptic Attack 3)

**Problem**: if the retrospector or scribe is skipped at session close, new
MEMORY.md lessons never get routed. Hook A silently fails.

**Fix**: the scribe's session-start ledger routine runs a catch-up routing
pass on any un-routed lessons.

**old_string** (the current scribe.md Method step 1):

```
1. On session start: create the directory skeleton
   (`QUESTION.md`, `HYPOTHESES.md`, `EVIDENCE/`, `SYNTHESIS.md`, `LOG.md`,
   `OPEN_QUESTIONS.md`) if it doesn't exist. Stamp `LOG.md` with the session
   id, start time, and research-lead's initial framing.
```

**new_string**:

```
1. On session start: create the directory skeleton
   (`QUESTION.md`, `HYPOTHESES.md`, `EVIDENCE/`, `SYNTHESIS.md`, `LOG.md`,
   `OPEN_QUESTIONS.md`) if it doesn't exist. Stamp `LOG.md` with the session
   id, start time, and research-lead's initial framing.

   **Catch-up routing pass (Hook A v2.1)**: After creating the skeleton,
   read `~/.claude/agent-memory/research-lead/MEMORY.md` and grep for
   lessons added since the last `scribe-curator:` LOG.md entry across
   any prior session. If a previous session added new lessons and never
   ran the routing pass (because scribe was skipped), apply the routing
   predicate from step 4 NOW as a recovery operation. Log each catch-up
   routing action as `scribe-curator: catch-up routed Lesson <N>`. This
   is a cheap idempotent operation — if there are no un-routed lessons,
   it is a no-op.
```

## File 2: `~/.claude/agents/research/research-lead.md`

### Edit 2.1 — Extend the "Consult MEMORY.md" step of the intake protocol

**old_string** (from the current research-lead.md, verbatim — this is Step 3 of the Intake & amplification protocol):

```
3. **Consult MEMORY.md.** Read `~/.claude/agent-memory/research-lead/MEMORY.md`. Check for lessons about this question class or similar past sessions. If the runtime auto-injected it, you already have it; otherwise read it yourself as Step 3.
```

**new_string**:

```
3. **Consult MEMORY.md.** Read `~/.claude/agent-memory/research-lead/MEMORY.md`. Check for lessons about this question class or similar past sessions. If the runtime auto-injected it, you already have it; otherwise read it yourself as Step 3.

   **Topic files — lazy pointer protocol (v2.1, Hook A)**: When a MEMORY.md lesson ends with a line of the form `See: <filename>.md for <description>`, the filename is a lazy pointer to a topic file in the same directory (`~/.claude/agent-memory/research-lead/<filename>.md`). Read the topic file with the Read tool ONLY when the current session's subject matter overlaps with the topic file's description. Do not preload topic files at session start — the index is sufficient for navigation. Typical case: 0-3 topic files read per session. If you find yourself reading more than 3, the routing heuristic is over-firing and the next retrospector pass should surface that as a lesson.
```

### Edit 2.2 — Add the topic-file invariant to the Rules section

**old_string** (from the current research-lead.md, verbatim — the rules section has this line):

```
- **Files are the memory.** Findings not written to `EVIDENCE/*.md` do not exist.
```

**new_string**:

```
- **Files are the memory.** Findings not written to `EVIDENCE/*.md` do not exist.
- **Topic files under `~/.claude/agent-memory/research-lead/` are read-only for you.** You may (and should) READ topic files on demand per the lazy-pointer protocol in intake Step 3. You must NEVER WRITE to topic files — that's the scribe's job, dispatched by you at session close. Specialists also never write to this directory.
```

## Verification checklist for the Engineering Team

After applying all 5 edits:

- [ ] `grep -n "route_to_topic" ~/.claude/agents/research/research-scribe.md` — returns 1 match
- [ ] `grep -n "scribe-metric:" ~/.claude/agents/research/research-scribe.md` — returns 1 match  
- [ ] `grep -n "lazy pointer" ~/.claude/agents/research/research-lead.md` — returns 1 match
- [ ] `grep -n "Topic files under" ~/.claude/agents/research/research-lead.md` — returns 1 match
- [ ] The research-scribe.md file is still valid YAML+markdown (frontmatter parses, no dangling fences)
- [ ] The research-lead.md file is still valid YAML+markdown
- [ ] Both files pass `head -1` showing `---` (frontmatter start preserved)

## Rollback

If Hook A causes session-start regressions (e.g., scribe over-routes and important lessons end up in topic files without their rule-of-thumb preserved), roll back by reverting the 5 edits:

```bash
cd ~/.claude/agents/research
git checkout -- research-scribe.md research-lead.md  # if using git, or
git stash pop  # if stashed, or
# otherwise, re-apply the reverse diffs from this file
```

The behavior returns to pilot v2's MEMORY.md-only pattern. Topic files created during the Hook A run can stay on disk; they become orphans but do not break the index.

## Notes

- **Ordering**: apply Edit 1.1 first, then 1.2, then 1.3, then 1.4, then 2.1, then 2.2. If applied in this order, each old_string is uniquely resolvable.
- **Uniqueness check**: before applying, run each old_string through a `grep -c` to confirm uniqueness. If an old_string returns >1 match, add surrounding context to disambiguate (the edits above have been structured to have unique markers already).
- **The AKL frontmatter is OPTIONAL**: the scribe's routing logic works without it. Adopt the frontmatter only if Hook B is later built and needs the fields for ranking.
