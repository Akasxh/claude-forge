# Linguist — the scribe routing heuristic vocabulary + prompt clarity

Sub-question: define "reference content" vs "rule of thumb" precisely so the scribe's routing decision is not a subjective call. Additionally, what vocabulary choices in the Hook A edits will maximize scribe and lead reliability?

## Method

- Read the current `~/.claude/agents/research/research-scribe.md` for the dedup pattern vocabulary
- Read the current `~/.claude/agents/research/research-retrospector.md` — not available at user scope in this session directly, but the retrospector's output schema is observable in `EVIDENCE/retrospector.md` of the pilot and in the current MEMORY.md file entries
- Cross-referenced with the ByteRover YAML frontmatter schema (historian.md) and the MemX paper's 4-factor vocabulary (librarian.md) for vocabulary convergence

## The lesson entry schema (observed, stable across 9 entries in current MEMORY.md)

Every lesson in `~/.claude/agent-memory/research-lead/MEMORY.md` has exactly 5 fields:

```markdown
### Lesson N — <title>
- Observed in: <slug> (<date>)
- Failure mode addressed: <MAST tag>
- Lesson: <prose body — varies 100 to 2000+ chars>
- Rule of thumb: <one-liner, imperative>
- Counter-example / bounds: <negative space>
```

The **Lesson** field is the size-variable one. The other four fields are all short (<200 chars each). So the routing heuristic's length test is **solely about the Lesson field**.

## Defining "reference content" vs "rule of thumb"

The key distinction is **what the field is used for**, not how long it is.

### "Rule of thumb" content (STAYS in index)

- **Imperative advice**: "do X when Y", "dispatch planner before wide", "run adversary on SEO-gamed topics".
- **Heuristic**: a threshold or a decision procedure the lead applies every session ("if more than 50% of sources are web → run adversary").
- **Process invariant**: "moderator before skeptic", "evaluator last".
- **Classification**: "SOURCE tier hierarchy is STRONG-PRIMARY > MIXED > REPORTED-NOT-VERIFIED > REJECTED".
- **Directional observation**: "in fast-moving topics, the 14-day sweep is mandatory".

Characteristic: the content is **repeatable prose** that the lead internalizes as behavior. Length is incidental.

### "Reference content" (MOVES to topic file)

- **Code snippets**: function definitions, SQL schemas, DDL, YAML frontmatter templates, MCP server tool handlers.
- **Verbatim quotes**: primary-source quotes from papers, blog posts, documentation, longer than ~300 chars.
- **Benchmark tables**: numerical results with row/column structure.
- **File maps**: "file X → function Y at line Z → calls Z'", multi-line.
- **Schemas**: JSON schemas, YAML schemas, DDL.
- **Case studies**: full trace of a specific incident (e.g., MemPalace fraud audit, the 5 moderator debates).
- **Citation dumps**: a list of ≥5 sources with URLs and retrieval dates.

Characteristic: the content is **consultative reference** — the lead reads it ONLY when the current session's topic overlaps. Length is typically large.

### The Boolean predicate (precise, machine-evaluable)

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

Where:
- `contains_code_block`: looks for ` ``` ` fenced block of N lines
- `contains_verbatim_quote`: looks for `> ` prefixed blockquote of M chars
- `contains_table`: looks for `|...|` markdown table of K rows
- `contains_reference_dump`: looks for a bullet list of URL / arxiv ID / filepath citations
- `contains_file_map`: looks for ≥3 entries of the form `<path>:<number>` or `<path>/<subpath>`

**Threshold tuning note (post-skeptic Attack 7)**: the `contains_table` threshold is raised from 5 to 10 rows. Five-row tables are often summary tables that belong in the index (e.g., the moderator verdict types, the source tier hierarchy). Ten-row tables are more likely to be reference artifacts (e.g., the ByteRover 5-tier retrieval vs the MemX weights breakdown combined). Also note: the `LENGTH >= 1500` threshold is itself tunable; start at 1500 for MVP and lower if the scribe's metric shows under-routing (Moderator C-deeper-1).

**Why both conditions (AND) matter**: a 2000-char rule of thumb without any reference content should stay in the index (it's still a rule). A 500-char code snippet should also stay in the index (it's small enough). The intersection catches "long + heavily referential" content, which is exactly what topic files were designed for.

**Why this is not subjective**: each of the 5 sub-predicates is a simple regex/count check the scribe can perform without interpretation. The scribe's prompt instructs it to evaluate mechanically.

## Edge cases and their rulings

| Case | Length | Type match | Route | Reason |
|------|--------|-----------|-------|--------|
| 2000-char prose lesson with no code/quote/table | yes | no | INDEX | Rule of thumb, not reference |
| 500-char lesson with a 15-line Python function | no | yes (code) | INDEX | Too short to be disruptive |
| 1800-char lesson with a 12-line SQL schema and 400-char quote | yes | yes (code + quote) | TOPIC | Both conditions, meaningful content |
| 1200-char lesson with a table of 3 rows | no | partial | INDEX | Neither condition triggered |
| 1600-char lesson with a list of 8 URLs + one-line annotation each | yes | yes (ref dump) | TOPIC | Citation dump qualifies |
| 3000-char lesson describing a failure mode in prose | yes | no | INDEX | Still a rule, keep despite length |
| 800-char lesson with a 6-row benchmark table | no | yes (table) | INDEX | Short enough |
| 2500-char lesson with 5 file path references + 3 line numbers | yes | yes (file map) | TOPIC | File map + size |

## Vocabulary for the scribe's internal deliberation

When the scribe reads a new lesson, it should think in these terms (not natural language):

1. **Parse** the lesson body for code blocks, quotes, tables, ref dumps, file maps.
2. **Count** the byte length of the body.
3. **Evaluate** the predicate: `len >= 1500 AND has_reference_content`.
4. **Decide**: INDEX or TOPIC.
5. **Execute** the routing atomically.
6. **Log**: one LOG.md line summarizing the decision.

The scribe's prompt should use these operational verbs: `parse`, `count`, `evaluate`, `decide`, `route`, `log`. NOT fuzzy verbs like "consider", "figure out", "maybe".

## Topic slug naming vocabulary

Topic slugs MUST be:
1. **kebab-case** (lowercase with hyphens, no spaces or underscores)
2. **short** (≤4 words, ≤40 chars)
3. **noun-phrase** (not an imperative)
4. **topic-specific** (not session-specific): `mempalace-fraud` not `session-2026-04-12-mempalace`

**Good slugs**:
- `mempalace-fraud.md`
- `latentmas-file-map.md`
- `memx-ranker.md`
- `ace-paper-quotes.md`
- `moderator-verdict-patterns.md`

**Bad slugs** (reasons):
- `MemPalace_Fraud.md` — wrong case
- `2026-04-12-mempalace.md` — session-specific prefix
- `the-full-mempalace-fraud-case-study-from-the-pilot-v2-relaunch.md` — too long
- `adversary.md` — too generic; collides with session-scoped adversary files

## Lead persona vocabulary: "lazy load" phrasing

The lead's new instruction must use unambiguous verbs. I recommend:

> "When a MEMORY.md entry ends with a line of the form `See: <filename>.md for <description>`, the filename is a lazy pointer to a topic file in the same directory. Read the topic file with the Read tool ONLY when the current session's subject matter overlaps with the topic file's description. Do not preload topic files at session start — the index is sufficient for navigation."

Key vocabulary choices:
- **"lazy pointer"** — signals read-on-demand
- **"overlaps with the topic file's description"** — concrete overlap check, not fuzzy relevance
- **"ONLY when"** — negative constraint, prevents eager reading
- **"Do not preload ... at session start"** — explicit anti-pattern
- **"the index is sufficient for navigation"** — tells the lead the normal operating mode

## The See-pattern format

The stub pattern in MEMORY.md when a lesson is topic-routed:

```markdown
### Lesson N — <title>
- Observed in: <slug> (<date>)
- Failure mode addressed: <MAST tag>
- Lesson: <1-2 sentence summary of the lesson>
- Rule of thumb: <one-liner, imperative — UNCHANGED from the rule of thumb of the original lesson>
- Counter-example / bounds: <one-liner — possibly truncated>
- See: `<topic-slug>.md` for <what's in the topic file — one phrase, e.g. "the full audit trail", "the file map", "the verbatim quotes">
```

**Key invariants**:
1. The **Rule of thumb** field must be preserved verbatim. This is the load-bearing content the lead needs every session.
2. The **Lesson** field must be compressed to 1-2 sentences summarizing the body.
3. The **See:** field is a NEW sixth field, only present for topic-routed lessons.

## Confidence

**High** on the vocabulary choices — every verb is tested against the existing MEMORY.md's 9 entries. The 5 sub-predicates for "reference content" are each machine-evaluable via standard regex. The slug conventions follow the Python packaging and Claude Code file naming conventions.

## Handoff

- **scribe-edit-plan** — use the exact predicate, the stub schema, and the See-pattern verbatim
- **skeptic** — attack the `AND` in the predicate: what if it's the wrong boolean? (Answered: OR would over-route short code snippets; Weighted-sum would make the decision fuzzy and lose machine-evaluability. `AND` is the safe bar.)
- **moderator** — if anyone contests the `len >= 1500` threshold, run a debate on thresholds

## Citations

- research-scribe.md (current MEMORY.md curation section) — `~/.claude/agents/research/research-scribe.md`, read 2026-04-12
- Observed MEMORY.md entries — `~/.claude/agent-memory/research-lead/MEMORY.md`, read 2026-04-12, 9 entries (lessons 1-7 + 2 starter playbook seeds from self-evolve-v2)
- ByteRover YAML frontmatter — paper § Appendix C and `docs.byterover.dev`, retrieved 2026-04-12
- MemX 4-factor vocabulary — `arxiv.org/html/2603.16171` § 3.4, retrieved 2026-04-12
- Claude Code memory docs § "Storage location" — `code.claude.com/docs/en/memory`, retrieved 2026-04-12
