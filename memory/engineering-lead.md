# engineering-lead — persistent agent memory

Curated by engineering-retrospector (writes to staging/) and engineering-scribe (merges via flock+timeout+atomic-rename).
Read first 200 lines at session start.

---

## Starter playbook

(Empty — first engineering session will populate via retrospector.)
## Added from memory-hook-a-v1.md at 2026-04-12

### Agent persona files have no type system — verify old_strings empirically before applying
- **Observed in**: memory-hook-a-v1 (2026-04-12)
- **Failure mode addressed**: FM-2.3 (task derailment) + FM-3.2 (incomplete verification)
- **Lesson**: Research teams produce Edit-tool-ready old/new pairs against a snapshot of the file. The files can change between research session and engineering session (e.g., v2.1 staging pattern added to research-scribe.md between the scribe-edit-plan and this engineering session). Executor must `grep -n <key_phrase>` each old_string against the CURRENT file before attempting the edit. Do not trust "verified against current files (date)" in the research plan — that date was not today. Takes 7 Bash calls; saves 7 potential Edit failures.
- **Rule of thumb**: For any engineering task that applies pre-written Edit-tool diffs from a research plan, run `grep -n <unique_phrase_from_old_string>` on the target file as the FIRST step of each task. Match = safe to apply. No match = read the surrounding lines and adapt.
- **Counter-example / bounds**: If the engineering session runs the same day as the research session that produced the diffs, the risk is low — but still worth the 1-second grep check.

### Sequential-dependent edits need a read-back step between them
- **Observed in**: memory-hook-a-v1 (2026-04-12)
- **Failure mode addressed**: FM-3.2 (incomplete verification)
- **Lesson**: When Edit 1.4's old_string depends on Edit 1.3 having been applied (Edit 1.4 appends after Edit 1.3's new content), the executor cannot use the original old_string from the research plan — it now matches a line that no longer exists at the file's tail. The correct approach: after applying Edit 1.3, call `tail -5 <file>` to find the new tail, use THAT as the old_string for Edit 1.4. This sequencing dependency was correctly anticipated by the planner and architect, but required in-flight adaptation during execution.
- **Rule of thumb**: For sequential edits where B's old_string is derived from the file state AFTER A is applied, add an explicit "read-back step" in the planner: "After Task N, run `tail -10 <file>` and confirm the new tail before Task N+1." This makes the dependency explicit and the adaptation unsurprising.
- **Counter-example / bounds**: Only applies when an edit appends to the END of a file that a prior edit also appended to (or changed). Mid-file sequential edits at disjoint line numbers don't have this dependency.

### The audit_evidence.py `no_terminal` rule is research-protocol-specific, not engineering-universal
- **Observed in**: memory-hook-a-v1 (2026-04-12)
- **Failure mode addressed**: FM-3.2 (incomplete verification) inverted — audit false negatives on valid files
- **Lesson**: `audit_evidence.py` was calibrated on 49 research evidence files that use `## Confidence / ## Verdict` terminal sections. Engineering specialist files (planner, architect) don't use `## Confidence` sections — their outputs are task decompositions and design commitments, not probabilistic claims. The `[no_terminal]` violation fires on valid engineering files. The workaround (add a `## Verdict` terminal to each file) works but is cargo-cult behavior. The audit script should add an engineering-specific terminal schema (just `## Verdict` suffices for plan-phase specialists). File this as a protocol improvement for the next self-evolve session.
- **Rule of thumb**: When audit_evidence.py reports `[no_terminal]` on Phase A engineering specialists (planner, architect), add a minimal `## Verdict` terminal and proceed. Log the schema gap in LOG.md for the next protocol maintenance session. Do not let the false negative block Phase B.
- **Counter-example / bounds**: `[no_terminal]` violations on Phase B specialists (executor, verifier, reviewer) ARE real violations — those files should have outcome verdicts. Only Phase A specialists get the engineering-specific pass.
