# QUESTION.md — claude-memory-layer-sota-2026q2-deeper

**Session start**: 2026-04-12 (deeper round, same day as pilot v2)
**Lead**: research-lead (adopted-persona mode)
**Slug**: `claude-memory-layer-sota-2026q2-deeper`
**Protocol**: v2 full (all adversarial gates, PASS required)
**Pilot workspace**: `~/.claude/teams/research/claude-memory-layer-sota-2026q2/`

## Raw prompt (verbatim from Akash, 2026-04-12, deeper round)

> "DEEPER ROUND on the memory-layer question. The v2 pilot produced a 4-phase
> architecture (Hook A topic files, Hook B SQLite+FTS5+sqlite-vec, Hook C
> LatentMAS spike, 6-month parametric LoRA). Evaluator HIGH confidence, all 5
> dims cleared. Now produce implementation-grade detail for each phase so the
> forthcoming Engineering Team can execute without blocking on more research."

## Assumed interpretation

The pilot's 4-phase plan is STRATEGIC. Akash is asking for the TACTICAL layer:
exact diffs, file scaffolds, go/no-go criteria, measurable triggers, and a
handoff checklist. A future Engineering Team will execute the plan; this
deeper round produces the spec they will execute against. Every item must be
file-path exact, line-number exact, or acceptance-criteria exact. "Plan to
plan" is not acceptable — this round writes the plan TO EXECUTE.

Additionally, this round is a 0-14 day fresh sweep (per pilot lesson 8/13):
has anything shipped in the last 10 days that invalidates the plan? Has any
skeptic missed anything the pilot's skeptic also missed?

## Sub-questions (implementation-grade)

### A. Hook A — research-scribe.md exact edits
1. Where in the current scribe persona does the topic-file routing behavior
   insert? Produce an exact Edit-tool-ready old_string/new_string pair.
2. What is the "route this to topic file" heuristic, precisely? Length?
   Detail type? Reference density? Primary-source verbatim? When is the
   boundary crossed from "index entry" to "topic file entry"?
3. How does research-lead discover topic files at session start? Lazy
   read-on-demand keyed by MEMORY.md index references.
4. Exact edit to research-lead.md to add the "read topic files on demand"
   behavior.
5. Test case: produce a deliberate long-tail lesson to see if scribe routes
   it correctly.

### B. Hook B — MCP server for SQLite + FTS5 + sqlite-vec
6. Language choice: Python vs Node (with reasons). Pick one.
7. Directory layout: `~/.claude/memory-mcp/` structure.
8. Schema DDL (CREATE TABLE with all columns, virtual table for FTS5,
   virtual table for sqlite-vec, indexes).
9. MCP server skeleton: tool handlers for search, insert, update, delete,
   temporal, graph_neighbors; which are MVP, which are v2.
10. settings.json registration snippet.
11. Hybrid ranker: BM25 + cosine + recency + priority, with explicit weights
    from MemX (arxiv 2603.16171).
12. Failure modes: corruption, WAL, backup cadence, recovery.
13. Trigger metric for "Hook A insufficient → build Hook B": what gets
    measured, by whom, with what threshold?

### C. Hook C — LatentMAS code analysis
14. Clone Gen-Verse/LatentMAS. If it exists: map compact-then-attend pattern
    to files and functions. If it doesn't: propose minimal from-scratch
    KV-cache compaction using vLLM's prefix-caching API.
15. One-evening spike scope: what ships that night, what does not.
16. Go/no-go decision: what measurement makes Akash ship vs throw away.
17. Integration surface with research-lead's dispatch loop.

### D. Parametric phase — LoRA distillation
18. Data format: what MEMORY.md line shapes become instruction pairs vs
    completion pairs vs DPO pairs.
19. Model + rank recommendation: Llama-3.1-8B or Qwen-2.5-7B, LoRA rank.
20. Decay gate: how many session reinforcements × how many days before a
    lesson earns distillation.
21. Loss, hyperparameters, expected training time.
22. Evaluation protocol to verify the LoRA encoded lessons without
    regressions.

### E. 0-14 day fresh sweep (per pilot lessons 8, 13)
23. Any memory-layer arxiv submissions 2026-04-02 → 2026-04-12?
24. Any new commits / releases on Mem0, Zep, Letta, MemGPT, A-MEM, Graphiti,
    MemX, LatentMAS, LRAgent, MemOS, MemPalace, Cognee?
25. MemPalace follow-up post-maintainer acknowledgment?
26. Is any part of the pilot's 4-phase plan invalidated by new info?

### F. Risk analysis — blast radius per hook
27. Hook A failure modes (slower scribe? lead misses topic file? wrong
    topic?).
28. Hook B failure modes (SQLite corruption, MCP crash, WAL recovery).
29. Hook C failure modes (spike breaks research-lead; exit criteria).
30. Parametric failure modes (stale or poisoned lesson LoRA).

### G. Implementation sequence
31. Produce IMPLEMENTATION_SEQUENCE.md — ordered checklist with step /
    owner / prerequisites / acceptance criteria / rollback.

### H. Deeper-round process lessons
32. What does a "deeper round following a pilot" deserve as a lesson for
    MEMORY.md? Specifically: what did reuse from pilot save, what did
    fresh adversary sweep catch, what new specialist choreography worked.

## Constraints

- Cutoff: 2026-04-12 (same day as pilot; this is additive depth not breadth).
- Every implementation artifact must be file-path exact or acceptance-criteria
  exact. "Write a Python file doing X" is not acceptable; "`~/.claude/memory-mcp/
  server.py:12-40 implements the insert handler with these columns`" is.
- Reuse pilot evidence per lesson 11 (REUSE / EXTEND / REWRITE at first
  action). Don't rewrite what the pilot produced.
- Adversary pass runs on 0-14 day window explicitly.
- Evaluator PASS required on all 5 dimensions; the bar is "the Engineering
  Team can execute without any more research."

## Definition of done

- Hook A diff ready for Edit tool (old/new pairs) on research-scribe.md AND
  research-lead.md
- Hook B skeleton, schema, settings.json snippet, hybrid ranker formula
- Hook C file map + spike plan + go/no-go
- Parametric data spec + model choice + decay gate
- IMPLEMENTATION_SEQUENCE.md
- 0-14 day sweep results: either "nothing new invalidates the plan" or a
  written addendum
- Evaluator PASS on all 5 dimensions
- Retrospector lessons appended to `~/.claude/agent-memory/research-lead/
  MEMORY.md` about deeper rounds

## Acceptance criteria

- The forthcoming Engineering Team lead reads SYNTHESIS.md + IMPLEMENTATION_
  SEQUENCE.md and produces zero "I need more research" questions before
  starting Hook A.
- Every artifact in the deliverables list is present and implementation-ready.
