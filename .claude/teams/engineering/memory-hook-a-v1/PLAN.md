# PLAN — memory-hook-a-v1

Integrated from planner.md + architect.md. Structural consistency check: PASS.

## Summary

Apply 7 edit-diffs to 2 agent persona files:
- 5 edits to `~/.claude/agents/research/research-scribe.md`
- 2 edits to `~/.claude/agents/research/research-lead.md`

No new files created in this session. Topic files at
`~/.claude/agent-memory/research-lead/<topic>.md` are created by the scribe
at RUNTIME during future research sessions.

## Execution order

1. **Task 1** — Edit 1.1: Add access-control rule to research-scribe.md Hard rules
2. **Task 2** — Edit 1.5: Add session-start catch-up routing pass to Method step 1
3. **Task 3** — Edit 1.2: Add routing predicate + stub schema to curation step 4
4. **Task 4** — Edit 1.3: Add AKL frontmatter schema section (append to file)
5. **Task 5** — Edit 1.4: Add Hook B trigger metric section (append after Edit 1.3)
6. **Task 6** — Edit 2.1: Add lazy pointer protocol to research-lead.md intake Step 3
7. **Task 7** — Edit 2.2: Add topic-file invariant to research-lead.md Rules section

## Key design commitments (from architect.md)

- Topic files: flat layout at `~/.claude/agent-memory/research-lead/<topic>.md`
- Routing predicate: `LENGTH ≥ 1500 AND type_condition` (AND, not OR)
- Table threshold: ≥10 rows (not 5)
- `Rule of thumb` in stubs: preserved verbatim
- `See:` pointer: new field, only on topic-routed lessons
- Frontmatter: optional, forward-looking for Hook B

## Acceptance criteria mapping

| Criterion | Tasks | Verification |
|---|---|---|
| AC #1 topic-file routing section | 1, 2, 3, 4 | grep route_to_topic |
| AC #2 research-lead lazy pointer | 6, 7 | grep lazy pointer |
| AC #3 backward-compatible | 1-7 (all additive) | read existing MEMORY.md — no existing entries broken |
| AC #4 no new infra | 1-7 | no new packages, files, or servers |
| AC #5 test plan | 5 + verifier checklist | grep scribe-metric |
