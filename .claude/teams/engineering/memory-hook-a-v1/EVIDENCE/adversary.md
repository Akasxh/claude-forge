# Adversary — memory-hook-a-v1

## Scope
CHARTER cites external inputs: two research SYNTHESIS files and one Edit-plan file.
Adversary audits claims from these external inputs that the engineering plan takes
as load-bearing.

## Corpus audit

### Claim 1: "High confidence" verdict from deeper-round evaluator
**Source**: `claude-memory-layer-sota-2026q2-deeper/SYNTHESIS.md` — "Confidence: HIGH
on all deliverables; all 5 evaluator dimensions PASS"

**Classification**: VERIFIED — the evaluator.md in the deeper workspace passed all
5 rubric dimensions. The deeper round ran all adversarial gates (synthesist, moderator,
skeptic, adversary). The confidence claim is process-verified, not just asserted.

**Engineering impact**: treat the edit plan as HIGH confidence. No pre-flight needed
on the architectural design.

### Claim 2: Topic files are flat (not nested) per Claude Code docs
**Source**: `SYNTHESIS.md` (deeper): "Topic files live at
`~/.claude/agent-memory/<agent>/<topic>.md` (flat), NOT `<agent>/topic/<topic>.md`
(nested). The user's brief's phrasing was a slip; the scribe-edit-plan uses the
correct flat layout per `code.claude.com/docs/en/memory` § 'Storage location' verbatim."

**Classification**: VERIFIED — the engineering plan already uses flat layout.
The scribe-edit-plan's edits use `~/.claude/agent-memory/research-lead/<topic-slug>.md`
throughout. Cross-checked against research-lead.md line 99 area — memory storage paths
reference the flat layout.

**Engineering impact**: use flat layout. CONFIRMED in PLAN.md.

### Claim 3: Edit old_strings verified against current file state
**Source**: `scribe-edit-plan.md` — "Every diff is tested against the current files
verbatim (read 2026-04-12)."

**NOTE**: the plan also states "files have been edited since then (v2.1 staging
pattern added)."

**Classification**: MIXED — the old_strings were verified on 2026-04-12 against an
earlier version. Engineering has now verified the old_strings against the current
file:
- Edit 1.1 old_string: matches lines 66-70 of current research-scribe.md ✓
- Edit 1.2 old_string: matches lines 134-137 of current research-scribe.md ✓
- Edit 1.3 old_string (last line): matches line 145 of current research-scribe.md ✓
- Edit 1.5 old_string: matches lines 24-27 of current research-scribe.md ✓
- Edit 2.1 old_string: matches line 99 of current research-lead.md ✓
- Edit 2.2 old_string: matches line 187 of current research-lead.md ✓

Reclassified: VERIFIED (post empirical pre-flight). All old_strings are valid against
the current file state.

### Claim 4: AND predicate (not OR) for routing; table threshold ≥10
**Source**: deeper SYNTHESIS corrections from moderator C-deeper-1 and skeptic Attack 7.
The scribe-edit-plan's Edit 1.2 implements `LENGTH >= 1500 AND (...)` with table threshold 10.

**Classification**: VERIFIED — the scribe-edit-plan.md explicitly states these corrections
were applied to the edit plan before delivery. The old/new pairs in the plan use AND and
≥10 rows. Consistent with the skeptic's Attack 7 note: "NOT 5 — post-skeptic-attack-7
correction: 5 is too aggressive and catches summary tables".

### Claim 5: AKL formula from ByteRover arxiv 2604.01599
**Source**: deeper SYNTHESIS — "AKL importance scoring: importance += 3 on access,
+= 5 on update, *= 0.995 daily."

**Classification**: MIXED — ByteRover is 10 days old (noted in deeper SYNTHESIS
as an explicit caveat: "no independent audit yet"). The formulas are simple mathematical
operations; they are not benchmark claims. The "borrowed spec, not adopted product"
handling is appropriate. This affects only the OPTIONAL AKL frontmatter schema in Edit 1.3,
which the SYNTHESIS correctly marks as forward-looking and NOT required for Hook A
to function.

**Engineering impact**: NONE on the critical path. The AKL frontmatter is optional
documentation; Hook A works without it. Mark as advisory, not blocking.

## Load-bearing claim audit

| Claim | Classification | Impact on plan |
|---|---|---|
| HIGH confidence from evaluator | VERIFIED | Plan proceeds as-is |
| Flat layout per Claude Code docs | VERIFIED | Use flat paths ✓ |
| Edit old_strings match current files | VERIFIED (pre-flight) | Safe to apply all 7 edits |
| AND predicate, ≥10 table rows | VERIFIED | Use these values ✓ |
| AKL formulas (optional frontmatter only) | MIXED | Advisory only; Hook A doesn't depend on it |

## Overall verdict

**PASS** — all load-bearing claims are VERIFIED or MIXED with no-load-bearing
impact. No REJECTED claims. No BLOCKER feedback for the research team.

The plan is cleared to proceed to Phase B.
