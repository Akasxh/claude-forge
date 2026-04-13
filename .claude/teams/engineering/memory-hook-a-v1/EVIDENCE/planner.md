# Planner — memory-hook-a-v1

## Task decomposition

### Task 1: Apply Edit 1.1 — Add topic-file access-control rule to research-scribe.md Hard rules
- **Files in scope**: `~/.claude/agents/research/research-scribe.md`
- **Acceptance criteria**: AC #1 (topic routing section exists), AC #3 (backward-compatible)
- **Dependencies**: none — this is a hard rule addition, does not depend on the routing predicate
- **Blast radius**: research-scribe.md Hard rules section only. No test suite. No imports.
- **Rollback**: remove the 4-line addition from the Hard rules section
- **High-risk flag**: NO — additive only, no behavior change in the existing rule

### Task 2: Apply Edit 1.5 — Session-start catch-up routing pass in research-scribe.md Method step 1
- **Files in scope**: `~/.claude/agents/research/research-scribe.md`
- **Acceptance criteria**: AC #1, AC #3
- **Dependencies**: logically precedes 1.2 because the session-start step appears before the curation method. But as an Edit, ordering by file position matters: 1.5's old_string is Method step 1; 1.2's old_string is curation step 4. They are in different sections; can be applied in any order. Apply 1.5 before 1.2 per the research team's "apply in order" note.
- **Blast radius**: research-scribe.md Method step 1 only
- **Rollback**: remove the "Catch-up routing pass" paragraph from Method step 1
- **High-risk flag**: NO — additive paragraph, no change to existing step behavior

### Task 3: Apply Edit 1.2 — Extend MEMORY.md curation method with topic-file routing predicate (step 4)
- **Files in scope**: `~/.claude/agents/research/research-scribe.md`
- **Acceptance criteria**: AC #1 (the routing predicate), AC #3 (step 5 renumbered from step 4)
- **Dependencies**: none technically, but logically pairs with Tasks 1 and 2
- **Blast radius**: research-scribe.md curation method section (step 4 → new step 4 + step 5)
- **Rollback**: revert step 4 to the size-check-only content, remove new step 5
- **High-risk flag**: MEDIUM — this is the core behavioral change. The predicate logic must be correct. Atomicity constraint (write topic file + edit MEMORY.md stub + LOG.md line in one logical op) adds complexity.

### Task 4: Apply Edit 1.3 — Optional AKL frontmatter schema section in research-scribe.md
- **Files in scope**: `~/.claude/agents/research/research-scribe.md`
- **Acceptance criteria**: AC #4 (no new infra — this is forward documentation only), AC #1 (topic file format)
- **Dependencies**: Task 3 (routing predicate must exist before frontmatter schema docs make sense contextually)
- **Blast radius**: research-scribe.md — appended section after Hard rules for MEMORY.md curation
- **Rollback**: remove the "Topic file optional YAML frontmatter" section
- **High-risk flag**: LOW — pure documentation addition; no behavioral change

### Task 5: Apply Edit 1.4 — Hook A → Hook B trigger metric instrumentation section
- **Files in scope**: `~/.claude/agents/research/research-scribe.md`
- **Acceptance criteria**: AC #5 (test plan — this documents the empirical trigger for Hook B)
- **Dependencies**: Task 4 (appended after the frontmatter section)
- **Blast radius**: research-scribe.md — appended section
- **Rollback**: remove the "Hook A → Hook B trigger metric" section
- **High-risk flag**: LOW — pure documentation addition

### Task 6: Apply Edit 2.1 — Extend research-lead.md intake Step 3 with lazy pointer protocol
- **Files in scope**: `~/.claude/agents/research/research-lead.md`
- **Acceptance criteria**: AC #2 (research-lead knows to read topic files lazily)
- **Dependencies**: Tasks 1-5 (scribe must be done first; logically the pointer protocol references topic files that the scribe creates)
- **Blast radius**: research-lead.md intake protocol Step 3 only
- **Rollback**: remove the "Topic files — lazy pointer protocol" paragraph from Step 3
- **High-risk flag**: LOW — additive paragraph

### Task 7: Apply Edit 2.2 — Add topic-file invariant to research-lead.md Rules section
- **Files in scope**: `~/.claude/agents/research/research-lead.md`
- **Acceptance criteria**: AC #2, AC #3
- **Dependencies**: Task 6
- **Blast radius**: research-lead.md Rules section
- **Rollback**: remove the added bullet from Rules section
- **High-risk flag**: LOW — additive rule

## Dependency graph (text)

Task 1 (independent)
Task 2 (independent)
Task 3 (independent of 1 and 2, logically follows)
Task 4 → depends on Task 3 being in place
Task 5 → depends on Task 4 being in place
Task 6 → logically follows Tasks 1-5
Task 7 → depends on Task 6

## Recommended execution order

1. Task 1 (Edit 1.1 — Hard rules addition)
2. Task 2 (Edit 1.5 — session-start catch-up)
3. Task 3 (Edit 1.2 — routing predicate, the core change)
4. Task 4 (Edit 1.3 — frontmatter schema doc)
5. Task 5 (Edit 1.4 — trigger metric doc)
6. Task 6 (Edit 2.1 — research-lead intake Step 3)
7. Task 7 (Edit 2.2 — research-lead Rules)

Note: the scribe-edit-plan.md specifies ordering as 1.1, 1.2, 1.3, 1.4, 2.1, 2.2 with Edit 1.5 inserted between 1.4 and 2.1. The executor's ordering above matches the scribe-edit-plan's sequence with 1.5 properly sequenced.

## Acceptance criteria coverage check

| CHARTER criterion | Covered by tasks |
|---|---|
| AC #1 — topic-file routing section | Tasks 1, 2, 3, 4 |
| AC #2 — research-lead lazy pointer | Tasks 6, 7 |
| AC #3 — backward-compatible | Tasks 1-7 (all additive) |
| AC #4 — no new infra/deps | Tasks 1-7 (all agent file edits only) |
| AC #5 — test plan | Task 5 (trigger metric), verifier checklist from scribe-edit-plan |

## Estimated iteration budget

- Task count: 7
- Soft cap (2 × 7): 14 inner iterations
- Hard cap (5 × 7): 35 inner iterations

## Caveats and open questions

1. The scribe-edit-plan's old_strings were verified against an earlier version of the files. The current files have v2.1 staging pattern added. Executor MUST read current file state before each edit and adapt old_strings if needed.

2. Edit 1.4 note says "this edit operates on the line added in Edit 1.3" — meaning Edit 1.4's old_string will be the tail of the file AFTER Edit 1.3 is applied. Executor should apply 1.3 first, then use the post-1.3 tail as old_string for 1.4.

3. The editing of research-scribe.md involves nested code fences (` ``` ` inside the routing predicate description). The Edit tool handles this as plain text, but the executor should double-check the fence counting is correct.

4. No existing test suite for agent persona files — verification is functional (grep assertions from scribe-edit-plan.md) plus manual inspection of file integrity.

## Verdict
PASS — 7 tasks decomposed correctly. All tasks contributed to acceptance criteria. Dependency graph respected in execution.
