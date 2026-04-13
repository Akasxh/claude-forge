# Skeptic — memory-hook-a-v1

## Competing strategies

### Strategy A (current plan): Apply 7 targeted edits to 2 agent files
The plan directly applies the research team's pre-written edit diffs, adapting
old_strings to the current file state. The edits are additive (no existing
content removed). The routing predicate is documented in natural language
inside the Markdown agent file.

**Strengths**: zero new infrastructure, backward-compatible, the research team
already ran adversarial gates on this design (HIGH confidence), edits are minimal.

**Weaknesses**: agent persona files are prompt text, not code — no type system
catches mistakes. If the predicate is subtly wrong, the scribe will silently
misroute lessons in future sessions. No automated test to catch this.

### Strategy B: Implement routing logic as a Python script, call from agent
Instead of documenting the routing predicate as natural language in the agent file,
extract it to a Python script at `~/.claude/scripts/route_topic.py` and have the
scribe invoke it via Bash.

**How it differs**: adds a tested, executable predicate; scribe calls
`python3 ~/.claude/scripts/route_topic.py --lesson <file>` to decide.

**Strengths vs A**: predicate is machine-verifiable, testable with unit tests,
less prone to misinterpretation by the LLM.

**Weaknesses vs A**: introduces new infrastructure (violates AC #4 — no new infra);
adds a dependency on Python path stability; scripts are separate maintenance surface.

**Verdict**: Strategy B violates CHARTER acceptance criterion AC #4 ("no new infra").
Strategy A is correct. If the predicate fires incorrectly in practice, a future
engineering session can add the script.

### Strategy C: Single consolidated section instead of 5 separate edits
Instead of 5 separate edits to research-scribe.md, write a single replacement
for the entire "v2 scope expansion" section.

**How it differs**: one large edit instead of 5 incremental ones.

**Strengths vs A**: simpler execution, fewer edit operations, no risk of partial
application leaving a mixed state.

**Weaknesses vs A**: harder to review, harder to rollback individual edits,
loses the provenance of which change came from which research round. Also risks
blowing the Edit tool's old_string matching on a 100+-line old_string.

**Verdict**: A is better. Granular edits match the research team's tested sequence.
Large edits are MAST FM-1.2 risk.

## Unstated assumptions

| Assumption | Verification needed | Risk if wrong |
|---|---|---|
| Edit old_strings match current file state | Read lines 66-70, 24-27, 134-137 and compare | Edit fails, manual intervention required |
| Edit 1.4 old_string operates on post-1.3 tail | Apply 1.3 first; verify file tail before applying 1.4 | 1.4 fails to match, edit not applied |
| research-scribe.md is unique enough for old_string matching | grep -c each old_string | Edit tool refuses if >1 match |
| No other recent changes to these files were made | git status / stat on the files | Merge conflict or mismatch |
| The routing predicate will be correctly interpreted by future scribe invocations | Read the MEMORY.md after a future session that has long lessons | Silent misrouting |

Verification: grep checks confirm current lines 66-70 and 24-27 match the scribe-edit-plan's old_strings verbatim. Lines 134-137 also match. The edit plan's old_strings are correct.

## What-if analysis

### What if Edit 1.2's nested code fences cause formatting issues?
- Impact on Phase B: Edit fails silently (fences become corrupted), or editor creates
  incorrect fencing in the agent file
- Impact on verifier: verifier's grep checks would still pass (the key identifiers
  "route_to_topic", "scribe-metric:" exist), but the file would be malformed
- Recovery: read the modified section and verify fence count is balanced
- Mitigation: executor reads back the modified section immediately after Edit and
  verifies fence balance

### What if Edit 1.4's old_string doesn't match after Edit 1.3?
- Impact on Phase B: Edit 1.4 fails
- Impact on verifier: grep for "scribe-metric:" returns 0 matches → FAIL
- Recovery: re-read the file post-1.3, use the actual tail as old_string for 1.4
- Mitigation: executor reads file after applying 1.3 and confirms the new tail
  before applying 1.4

## Load-bearing flaws (if any)

None identified. The plan is sound:
- All old_strings verified against current file state
- Ordering correctly handles the 1.3→1.4 dependency
- AC #4 (no new infra) is preserved by Strategy A
- Backward compatibility is maintained (all edits additive)

## Enhancements to the plan

1. **Executor should read back modified sections after each edit** — confirms the edit
   applied correctly, especially for the nested-fence Edit 1.2 case. This is already
   implied by the engineering protocol but worth making explicit.

2. **Verify file starts with `---` (frontmatter) after each edit** — the scribe-edit-plan
   verification checklist includes this. Executor should include it in the post-edit check.

3. **Run the grep verification checklist from scribe-edit-plan after all 7 edits** —
   7 assertions that can be run as a batch via Bash.

## Gate verdict

**PASS** — no load-bearing flaws found. Plan is viable. Enhancements noted above
are advisory. The 1.3→1.4 sequencing dependency is properly handled in the planner's
execution order. Old_string matches confirmed.
