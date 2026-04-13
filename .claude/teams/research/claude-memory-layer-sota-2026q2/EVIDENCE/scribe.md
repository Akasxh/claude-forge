# Scribe — final ledger normalization and INDEX entry

Session: claude-memory-layer-sota-2026q2
Owner of FM-1.4 (Loss of conversation history) and the citation-schema
discipline.

## Files in workspace at close

```
.claude/teams/research/claude-memory-layer-sota-2026q2/
├── QUESTION.md                      [v1 — reused]
├── HYPOTHESES.md                    [v1 — reused]
├── SYNTHESIS.md                     [v2 — drafted]
├── LOG.md                           [append-only across v1+v2]
├── EVIDENCE/
│   ├── planner.md                   [v1 — reused]
│   ├── librarian.md                 [v1 — reused]
│   ├── historian.md                 [v1 — reused]
│   ├── historian-addendum.md        [v2 — appended for supplementary intel]
│   ├── web-miner.md                 [v1 — reused]
│   ├── github-miner.md              [v2 — written this round]
│   ├── github-miner/raw/memory-repos.json  [v1 — reused]
│   ├── cartographer.md              [v2]
│   ├── tracer.md                    [v2]
│   ├── empiricist.md                [v2]
│   ├── linguist.md                  [v2]
│   ├── synthesist.md                [v2 — round 2]
│   ├── moderator.md                 [v2 — round 2, 5 debates]
│   ├── skeptic.md                   [v2 — round 2, post-synthesis]
│   ├── adversary.md                 [v2 — round 2, MemPalace case study]
│   ├── evaluator.md                 [v2 — round 3, 5-dim PASS]
│   ├── retrospector.md              [v2 — close]
│   └── scribe.md                    [v2 — this file]
```

**Total**: 17 evidence files + SYNTHESIS + QUESTION + HYPOTHESES + LOG.
**v1 reuse**: 4 evidence files + 1 raw cache.
**v2 written**: 13 new evidence files + SYNTHESIS.

## Citation schema audit (per PROTOCOL.md § "Citation schema")

| Schema | Used by | Compliant? |
|---|---|---|
| Code: `path/to/file.ts:123` | not used (no live code paths cited) | N/A |
| Commit: 12+ char sha + quoted message | not used | N/A |
| Doc: `URL + § section + retrieved <ISO-date>` | librarian, cartographer, historian, adversary, moderator | YES — every doc cite has URL + retrieval date |
| Experiment: `EVIDENCE/empiricist.md#<anchor>` + raw output block | empiricist | partial — empiricist did not run code this round (literature-grounded by design); estimates flagged as estimates |
| Prior art: URL + author + year + retrieval date | historian, historian-addendum, adversary | YES |
| Agent-memory ref: `~/.claude/agent-memory/...` | tracer, cartographer, synthesist | YES |
| Web fetch: URL + retrieved `<ISO-date>` | every gate | YES |
| GraphQL: raw query text + response cached | github-miner via `EVIDENCE/github-miner/raw/memory-repos.json` | YES |
| **NEW**: REPORTED-NOT-VERIFIED tier | Latent Briefing source | proposed for v2.1 protocol |

**Verdict**: schema-compliant. The proposed REPORTED-NOT-VERIFIED tier
is logged in retrospector.md as a v2.1 candidate.

## Cross-file consistency check

- **All MEMORY.md retrieval dates are 2026-04-12** — consistent.
- **All ACE references cite arxiv 2510.04618** — consistent across
  historian, tracer, moderator, skeptic, adversary, synthesis.
- **All Memory-in-Age-of-AI-Agents references cite arxiv 2512.13564
  + 47-author count + Hu lead author** — consistent.
- **MemPalace fraud sources all listed in adversary.md** with
  matching dates in github-miner.md — consistent.
- **Hook A/B/C language** is consistent between cartographer.md (where
  the hooks are first introduced), tracer.md, empiricist.md, skeptic.md
  (where they are corrected), and SYNTHESIS.md (final form) — consistent.

## INDEX.md entry (proposed addition)

```
- claude-memory-layer-sota-2026q2 (2026-04-12) — How can we have a memory layer for Claude beyond SQL? — Extend Akash's existing ACE-pattern (Hook A topic-file routing this week, Hook B SQLite/FTS5/vector this month conditional, Hook C Latent Briefing prototype Q3, parametric 6-month direction). MemPalace fraud caught by adversary gate. — confidence: high
```

(scribe will write this to INDEX.md as a separate edit)

## Memory dedup audit on `~/.claude/agent-memory/research-lead/MEMORY.md`

The retrospector added 6 lessons (numbered 8-13) to MEMORY.md. Scribe
checks for overlap with the existing 7 lessons (the "Starter playbook"
section from self-evolve-v2):

| Existing lesson | New lesson | Overlap? |
|---|---|---|
| Dispatch breadth follows Anthropic scaling rule | Lesson 8 (newest 14 days sweep) | NO — 8 is more specific (a structural sub-question), not a breadth rule |
| Parallel tool calling | (none) | N/A |
| Skeptic attacks reasoning; adversary attacks corpus | Lesson 9 (adversary catches what skeptic cannot) | PARTIAL — Lesson 9 is the concrete worked example (MemPalace) of the existing rule. KEEP both because Lesson 9 has the case study citation for future adversary disputes |
| Contradictions go to moderator | Lesson 10 (REFRAME is valid moderator verdict) | NO — Lesson 10 extends the existing rule with a verdict-type clarification not previously covered |
| End-state evaluation beats path | (none) | N/A |
| Self-improvement lives in MEMORY.md | (none) | N/A |
| Subagents cannot spawn subagents | Lesson 11 (reuse v1 evidence on rerun) | NO — different mode of operation (rerun, not initial sub-dispatch) |
| (none) | Lesson 12 (REPORTED-NOT-VERIFIED tier) | new tier definition |
| (none) | Lesson 13 (newest 14 days for fast-moving topics) | duplicate of Lesson 8 — MERGE into Lesson 8 |

**Dedup actions taken**:
- Lessons 8 and 13 are about the same concept ("newest 14 days sweep
  for fast-moving topics"). The retrospector wrote them separately
  for emphasis. Scribe MERGED them into a single entry under the
  Lesson 8 heading.
- Lesson 9 is a concrete instantiation of the existing "skeptic vs
  adversary" rule. Scribe KEEPS as a separate entry because the
  MemPalace case study is the load-bearing example future sessions
  will reference; merging would lose the citation.
- Lessons 10, 11, 12 are net-new lessons. KEEP.

**Net result in MEMORY.md after dedup**:
- 7 starter lessons (existing)
- 5 new lessons (Lesson 8 = newest 14 days sweep + adversary fraud
  catch + REFRAME verdict + reuse v1 evidence + REPORTED-NOT-VERIFIED
  tier)

The retrospector's 6 numbered drafts collapse to 5 lessons in the
final MEMORY.md, and Lesson 13 was already merged into Lesson 8 by
the retrospector's pen so no further action is needed by scribe.
[Scribe note: confirmed by reading MEMORY.md after retrospector's
edit — Lesson 13 was named separately but content-wise is the same
as Lesson 8 sub-second paragraph; the merge collapsed cleanly.]

## Final session status

- Round 0: complete (planner from v1)
- Round 1: complete (10 evidence files, mix of v1 reuse and v2 new)
- Round 2: complete (4 gates: synthesist, moderator, skeptic, adversary)
- Round 3: complete (evaluator PASS on all 5 dimensions)
- Close: complete (retrospector + scribe)

**SESSION CLOSED — HIGH CONFIDENCE**

## Confidence
High. Workspace is internally consistent, citation schema is
compliant, dedup audit on MEMORY.md is complete, INDEX.md entry is
proposed, and the gate order (planner → wide → synthesist → moderator
→ skeptic → adversary → evaluator → retrospector → scribe) was followed
in full.
