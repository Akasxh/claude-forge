# Skeptic (preliminary) — Round 1 red team on H3

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: competing hypotheses, unstated assumptions, premature-convergence check
Mode: adopted persona — writes PRELIMINARY skeptic report before wide-opener completes. The full skeptic.md pass runs in Round 2 after synthesist.

## Note on mode

This is the Round-1 preliminary pass. It reads the hypothesis set, the planner, and the early evidence files, and generates competing-hypothesis attacks that the Round-2 skeptic will refine after the synthesist has built the claim matrix. The final authoritative skeptic report lives in `EVIDENCE/skeptic.md`.

## Leading hypothesis (as I understand it pre-synthesis)

**H3 — Unified Hybrid**: engineering-team v1 has flat roster of 12 specialists + lead, a two-phase round structure (Phase A = plan with plan-skeptic and plan-adversary gates; Phase B = ReAct-shaped build loop with verify-gate and review-gate per iteration), an evaluator gate at close, and retrospector for MEMORY.md lessons. Both phases live in the same workspace under the same lead — the "planners and executors together" constraint. Cross-team handoff via CHARTER.md (reads research SYNTHESIS.md as binding input) and FEEDBACK_FROM_ENGINEERING.md (when disagreeing). Concurrency via flock + atomic rename + per-session staging files, with timeout-wrapped merges for holder-death safety.

If I can't restate this cleanly, that's a problem. I can. It's clean.

## Competing hypotheses

### H'1: "Phase B inner loop will over-iterate and eat the budget"

**Consistent with evidence because**: the Anthropic SWE-bench blog explicitly says the model continues to sample "until the model decides that it is finished, or exceeds its 200k context length." Without a hard iteration cap, the inner loop has no termination guarantee. The Devin year-in-review reports multi-day runs on autonomous loops. MAST FM-1.5 (unaware of termination conditions) is a published failure mode. Our design names this mode as one that engineering-lead "owns" but doesn't specify the mechanism.

**Would be falsified by**: explicit termination rules — max inner iterations (e.g. 5 × plan.task_count), cost budget per phase, user-configurable hard stop.

**Proposed fix for SYNTHESIS.md**: Phase B has a hard cap of `max(5, 2 × PLAN.task_count)` inner iterations. Hitting the cap triggers escalation to lead and optional back-edge to Phase A (replan). Documented as explicit termination rule in PROTOCOL.md.

### H'2: "The plan-gate is weak because the plan-skeptic doesn't have executable verification"

**Consistent with evidence because**: engineering-skeptic attacks the plan by reading it and asking "what if this is wrong?" But the skeptic cannot run code. The kind of plan bug it catches is "you're assuming library X exists" — easy to catch. The kind it MISSES is "you're assuming library X's behavior" which only an executor can verify. In the pilot memory-layer session, the skeptic caught 7 corrections but none of them were "the library doesn't behave this way" — because the skeptic couldn't test.

**Would be falsified by**: a concrete example of the plan-skeptic catching a runtime behavior bug. The memory-layer session has zero such examples; the engineering-team's plan-gate MAY have the same blind spot.

**Proposed mitigation**: for plans that cite any externally-behaved claim (a library's behavior, a benchmark's reproducibility, a tool's output shape), the plan-adversary gate includes an "empirical pre-flight" step: engineering-empiricist (wait, does that exist?) runs a minimal probe to verify the claim before Phase B commits. **Note**: engineering-team v1 roster doesn't have an empiricist. Either add one, or make engineering-executor perform a 5-minute probe pass at the very start of Phase B before "real" implementation. The latter is simpler and is what I recommend.

### H'3: "The concurrency protocol defends against the wrong failure mode"

**Consistent with evidence because**: the tracer + empiricist focused on "multiple sessions writing MEMORY.md simultaneously." That's a real problem, but it's NOT the most common concurrency failure. The MOST COMMON is: **one session's retrospector writes a new lesson that is semantically equivalent to an existing lesson, and the scribe's dedup logic — running LLM-dedup after the merge — doesn't actually catch the duplicate because the LLM phrases it slightly differently**. This is a "slow duplicate accumulation" failure, not a "race" failure, and flock doesn't help.

**Would be falsified by**: running the protocol for 5 sessions and measuring MEMORY.md size growth vs lesson count. If lessons grow faster than unique insights, dedup is broken.

**Proposed mitigation**: the scribe dedup pass must include a semantic-equivalence check, not just a string-prefix match. And the MEMORY.md ceiling (200 lines / 25KB per the runtime) acts as a forcing function — stale or duplicate lessons fall out the bottom eventually. This is acceptable but the Round-2 synthesist should flag that the concurrency design is primarily about multi-session safety, NOT about dedup quality — those are orthogonal concerns.

### H'4: "12 specialists is over-dispatched for the common engineering session"

**Consistent with evidence because**: Anthropic's "3-5 teammates for most workflows" recommendation. A small bug fix doesn't need a planner, architect, skeptic, adversary, moderator, evaluator, retrospector — it needs an executor and a verifier. The v1 roster of 12 will feel heavy on common tasks.

**Would be falsified by**: running the team on a small bug fix and measuring token cost and elapsed time. If a "fix a typo in line 42" task burns 100K tokens through the full 12-specialist flow, the protocol is broken.

**Proposed mitigation**: **tiered invocation** — the lead's intake protocol classifies task size (trivial, scoped, complex) and dispatches only the mandatory specialists at each tier:
- Trivial: executor + verifier. Skip planner, architect, skeptic, adversary, moderator, reviewer (run evaluator only if changing a public API).
- Scoped: planner, executor, verifier, reviewer. Optional skeptic.
- Complex: full roster.

Research-team doesn't have this tiering because research is always multi-lens. Engineering has a much wider task-size distribution and NEEDS tiering. **This is load-bearing; synthesist should include tiering in the round structure.**

### H'5: "The moderator is dead weight in engineering-team"

**Consistent with evidence because**: research contradictions are the norm (different corpora, different lenses). Engineering contradictions are rarer (executor did X, verifier said X passed — not a contradiction, it's a pass). When contradictions DO arise in engineering, they're usually "reviewer says the diff is too big, executor says the diff is minimum viable" — which is a taste dispute, not an evidence dispute. Moderator's 3-round debate is wasteful for taste disputes.

**Would be falsified by**: a specific engineering-contradiction case that benefits from 3-round debate.

**Proposed mitigation**: make moderator CONDITIONAL — only dispatched when synthesist-analogue (which we don't have in engineering; see H'6) flags an evidence contradiction. For taste disputes, the reviewer has final say (appeal to lead if contested). Keep moderator in the roster for edge cases but make it rarely-invoked.

### H'6: "Engineering-team has no synthesist analogue — who builds the claim matrix?"

**Consistent with evidence because**: research-team's synthesist runs between Round 1 and Round 2 and builds a claim matrix that the moderator debates. Engineering has nothing structurally equivalent. Plan-phase gates run directly on the planner.md + architect.md output without a "here's everything we know so far" integration pass.

**Would be falsified by**: no failure mode this causes.

**Proposed fix**: the engineering-lead absorbs the synthesist role implicitly at the phase boundary: at the end of Phase A, the lead writes PLAN.md which IS the claim matrix. Plan-skeptic + plan-adversary then attack PLAN.md directly. This is structurally cleaner than adding a dedicated `engineering-synthesist` specialist. Document this in the lead's persona: "at phase boundary, you write PLAN.md including the architect's decisions and the planner's task list; this is the claim matrix for the gates."

## Unstated assumptions in H3

1. **"The inner ReAct loop terminates on acceptance criteria."** What if acceptance criteria are ambiguous? The plan-skeptic should explicitly audit CHARTER.md's acceptance criteria for measurability before Phase A exits. Unmeasurable acceptance criteria are a first-class blocker.

2. **"The research SYNTHESIS.md is binding."** What if engineering discovers the research was wrong? H3 has a FEEDBACK_FROM_ENGINEERING.md mechanism, but it doesn't say what to DO with a feedback file — does engineering block? Proceed with its best interpretation? Escalate to the user? The flow is underspecified.

3. **"The executor uses smallest-viable-diff by default."** That's the flat executor's contract but team-session dynamics might pressure for larger diffs to "show progress." No mechanism in H3 enforces small diffs beyond the reviewer's "diff minimality" rubric dimension, which runs LATE.

4. **"The git identity hook just works."** The pilot memory-layer session didn't commit code. Engineering-team will. The `~/.claude/lib/git-identity.sh` script has been tested but not under team-session load. Risk of the wrong account being active when engineering-executor commits.

5. **"The 5-dim engineering rubric is measurable objectively."** Functional correctness = yes (tests pass). Test coverage = yes (coverage number). Diff minimality = subjective (what's "minimum viable"?). Revert-safety = subjective (is the migration reversible in principle but expensive in practice?). Style conformance = subjective depending on project. Three of five dimensions are subjective judgments by an LLM-as-judge, which Anthropic's Claude Agent SDK blog explicitly cautions against.

## Evidence quality audit

- `librarian.md` — STRONG. Six Anthropic primaries cited with verbatim quotes. Low risk.
- `historian.md` — MOSTLY STRONG. The SWE-bench contamination finding has multiple corroborating sources. The "25K-task experiment" X claim is correctly flagged REPORTED-NOT-VERIFIED. The specific Devin numbers are appropriately marked as contested.
- `web-miner.md` — MEDIUM. Some claims are aggregated from search-snippet-only sources. Reddit gap is flagged.
- `github-miner.md` — MEDIUM. Synthesized from public architecture descriptions without real gh-api queries. Structural claims are load-bearing; engagement metric claims are not present (and are not needed).
- `tracer.md` — STRONG. flock/rename/POSIX man pages are authoritative primaries.
- `empiricist.md` — VERY STRONG. Tests run on this actual Linux box with raw outputs. CRITICAL CORRECTION to tracer.md (timeout wrapping required) is surfaced and fixed.
- `cartographer.md` — STRONG on directly-observable facts (file existence, naming collisions).
- `archaeologist.md` — STRONG on v1→v2 diff and MEMORY.md lessons. Medium on v1 PROTOCOL backup content (not read).
- `linguist.md` — STRONG on vocabulary audit. Opinion-leaning but well-grounded.

## Premature convergence check

**Am I converging on H3 prematurely?** Honestly: yes, somewhat. H3 was the planner's leading hypothesis, the historian and librarian both point to it, and no evidence has directly contradicted it. BUT:

- I have not seriously considered H'4's tiered invocation, which is a STRUCTURAL modification to H3, not an alternative.
- I have not tested H'5 (moderator is dead weight) with a concrete engineering-contradiction case.
- I have not challenged the assumption that the v2 research protocol's gate ORDER is optimal for engineering (it was designed for research).

**Required next probes before Round 2 synthesist pass**:
1. Explicitly consider tiered dispatch as a modification to H3 — this is not an alternative, it's an enhancement. Synthesist should incorporate.
2. Test the moderator's value with a fabricated engineering-contradiction scenario. If it adds no value on that scenario, synthesis should make it conditional.
3. Verify that the gate order (plan-skeptic → plan-adversary → verify → review → evaluator) is the right ORDER for engineering. Research does (synthesist → moderator → skeptic → adversary → evaluator); engineering reorders because the phase boundary is different.

## Verdict

**Prematurely converged?** Partial yes — H3 is probably right in shape but needs enhancement (tiering, explicit termination rules, feedback-loop semantics).

**Safe to raise confidence to "high"?** Not yet. Three specific enhancements from H'1, H'4, H'6 must be incorporated before the Round-2 skeptic pass can clear the gate. Plus the critical `timeout(1)` correction from empiricist must be in PROTOCOL.md.

**Required next probes**:
1. Round-2 synthesist: build the full claim matrix integrating all Round-1 evidence, surface any contradictions I might have missed.
2. Round-2 skeptic: take this preliminary report, run it against the final synthesis draft, see if any competing hypothesis has survived.
3. Round-2 adversary: audit the source quality of the 14-day freshness findings, the SWE-bench contamination claim, the Morph LLM aggregator, and the X "25K-task" claim.
4. Round-2 moderator: IF synthesist reports an H3-vs-H'4 contradiction on tiering, run a 3-round debate.

## Confidence

**MEDIUM** — 6 competing hypotheses generated, 5 unstated assumptions named, 1 critical correction to tracer.md surfaced, but the final authoritative skeptic run happens in Round 2 after synthesist. Preliminary confidence is medium by design — the point of this pass is to seed the Round-2 skeptic with attack vectors, not to close them.
