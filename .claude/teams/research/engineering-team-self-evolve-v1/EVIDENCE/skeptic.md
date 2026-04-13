# Skeptic — full Round 2 red team on enhanced H3

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: internal consistency, unstated assumptions, premature convergence, competing hypotheses
Mode: adopted persona — runs AFTER synthesist and moderator, BEFORE adversary

## Scope

Round-2 skeptic reads the full workspace: all Round-1 evidence, synthesist.md, moderator.md, the preliminary skeptic pass, and the current draft state of SYNTHESIS.md (still being composed). Attacks the **enhanced H3** (H3 + 6 enhancements from synthesist) for premature convergence, unstated assumptions, and weak evidence.

## Leading hypothesis as I understand it (post-enhancements)

**Enhanced H3** — engineering-team v1:

- **Roster**: 12 specialists + lead (engineering-lead, engineering-planner, engineering-architect, engineering-executor, engineering-verifier, engineering-reviewer, engineering-skeptic, engineering-adversary, engineering-moderator, engineering-evaluator, engineering-debugger, engineering-retrospector, engineering-scribe).
- **Structure**: flat roster, two-phase round structure.
- **Phase A (Plan)**: intake → planner → architect → structural consistency check → plan-skeptic gate → plan-adversary gate → PLAN.md committed.
- **Phase B (Build)**: ReAct-shaped inner loop with executor + verifier + reviewer per iteration. Empirical pre-flight step at Phase B entry. Hard cap of `max(5, 2 × PLAN.task_count)` inner iterations.
- **Session close**: evaluator → retrospector → scribe → handback.
- **Tiered invocation**: trivial/scoped/complex dispatch tiering in the lead's intake.
- **Concurrency**: flock + atomic rename + staging + timeout(1)-wrapped merge (corrected snippet).
- **Cross-team handoff**: CHARTER.md reads research SYNTHESIS.md; FEEDBACK_FROM_ENGINEERING.md writes back when disagreeing; handback artifact at session close.
- **Moderator conditional**: runs only on detected contradictions, not taste disputes.
- **Synthesist absorbed**: lead performs structural consistency check at Phase A close; no dedicated synthesist specialist.

This is a richer hypothesis than my preliminary pass. Good — the synthesist + moderator passes have done their job.

## Competing hypotheses (Round 2 attacks)

### H''1 — "Tiered invocation creates a silent downgrade channel"

**Claim**: The tiered-invocation enhancement (trivial/scoped/complex) is in tension with the never-downgrade doctrine. If "trivial" means "only dispatch executor + verifier," that's a 2-specialist team for real work — same as raw executor usage with no team at all. The user who wanted an engineering team and said "small bug fix" has effectively opted out of the team.

**Is this actually a downgrade?** Not in the model sense — both specialists still run at `opus + effort: max`. But it IS a downgrade in the gate sense: plan-skeptic, plan-adversary, reviewer, and evaluator are skipped.

**Consistent with evidence because**: Anthropic's scaling rule ("simple fact-finding: 1 agent, 3-10 tool calls") supports minimal dispatch. But Anthropic also says "human review remains crucial for ensuring solutions align with broader system requirements" — even on simple changes.

**Would be falsified by**: a specific "trivial" task that would have gone wrong without the skipped gates. Without a concrete example, it's hypothetical.

**Proposed mitigation**: tiered invocation must have explicit floors:
- **Trivial tier** (typo, comment fix, rename): executor + verifier. NO reviewer, NO evaluator. Documented as the "low-overhead lane" — the user is trading gate coverage for speed, explicitly.
- **Scoped tier** (single-file logic change, small feature, bug fix): executor + verifier + reviewer. NO plan-skeptic, NO plan-adversary, NO evaluator.
- **Complex tier** (multi-file, cross-module, architectural): full roster with all gates.

**Critical addition**: the lead's tier classification MUST be shown to the user at intake, and the user can override upward ("I want the complex-tier gates for this scoped task") but NOT downward. Default upward bias — prefer false-positive over-dispatch to false-negative under-dispatch.

**Resolution**: add "tier classification is user-overridable upward, not downward" as a protocol rule. Enhancement accepted with constraint.

### H''2 — "Phase B termination cap is arbitrary and can't be defended"

**Claim**: The cap `max(5, 2 × PLAN.task_count)` has zero empirical grounding. Why not `3 × task_count`? Why not a token budget instead of an iteration count? An arbitrary magic number pretending to be a termination rule is worse than no cap — at least an unbounded loop is honest about its risk.

**Consistent with evidence because**: Anthropic's "Building effective agents" says "include stopping conditions such as a maximum number of iterations" but does NOT specify the number. Academic work on plan-and-solve has various caps (often 10, sometimes 20). Our `max(5, 2 × N)` was invented on the spot during synthesis.

**Would be falsified by**: an empirical run showing the cap is too tight (blocks legitimate iteration) or too loose (doesn't prevent drift).

**Proposed mitigation**: **two-level termination**, not one:
- **Soft cap**: `2 × PLAN.task_count` inner iterations. On hit: log warning to LOG.md, NOT escalate — just notify.
- **Hard cap**: `5 × PLAN.task_count`. On hit: force-halt and escalate to lead for `replan/handback/abort`.
- **Token budget** (orthogonal): track total tool-call count per session; if it exceeds 500k tool calls, force halt regardless of iteration count.

This gives the team room to work but caps catastrophic drift. The soft/hard split is a defense-in-depth pattern that doesn't depend on the exact magic number being correct.

**Resolution**: replace the single cap with soft/hard cap + token budget. Enhancement refined.

### H''3 — "The empirical pre-flight step leaks Phase B behavior into Phase A"

**Claim**: The Phase-A→Phase-B transition is supposed to be the plan-gate (plan skeptic + plan adversary both pass on PLAN.md). Adding an "empirical pre-flight" inside Phase B means we're running code BEFORE the plan-gate actually closes — because the pre-flight is validating plan assumptions, which is plan-gate's job. Either fold the pre-flight into plan-adversary's method, or admit we don't actually have a clean Phase A/B boundary.

**Consistent with evidence because**: plan-gate's purpose is to catch plan errors before execution. "Empirical probe to verify library behavior" IS catching a plan error. It should run BEFORE the gate closes, not after.

**Would be falsified by**: the empirical pre-flight catching something plan-adversary couldn't. My preliminary skeptic pass said the plan-skeptic can't catch runtime-behavior bugs without executing. But plan-**adversary** — which reads external inputs and has the ability to run tool calls — could run such a probe.

**Proposed mitigation**: **move the empirical pre-flight from Phase B entry to plan-adversary's method**. plan-adversary's job already includes "attacks external inputs to the engineering session" (library docs, task spec). Extend that to "if plan-adversary flags any claim as runtime-behavior-dependent, it runs a 5-minute probe via engineering-executor delegation OR runs tool calls itself to verify." This keeps the clean Phase A/B boundary.

**Implementation note**: plan-adversary can run small tool calls (Bash, WebFetch, Read) to verify. It can also dispatch engineering-executor in "probe mode" — a short-scope executor task that returns results to plan-adversary without committing to the full PLAN.md yet. Plan-adversary's method section gets a new "runtime behavior verification" beat.

**Resolution**: move the empirical pre-flight out of Phase B entry and into plan-adversary's method. Enhancement improved — cleaner boundary.

### H''4 — "FEEDBACK_FROM_ENGINEERING.md is underspecified"

**Claim**: The cross-team handoff has a forward path (CHARTER reads research SYNTHESIS.md) and a conditional back-channel (FEEDBACK_FROM_ENGINEERING.md). But what happens OPERATIONALLY when feedback is filed?
- Does engineering block on its own plan?
- Does it send the feedback and proceed with best-interpretation?
- Does it escalate to the user?
- Does it trigger a research re-dispatch?

None of these are specified. The handoff looks clean in the diagram; the operational flow is hand-wavy.

**Consistent with evidence because**: the cross-team handoff section in this session's scope is one of the 21 sub-questions; nothing in Round 1 gave an operational answer.

**Proposed mitigation**: explicit feedback-handling protocol:

1. Engineering discovers a research claim is wrong or underspecified.
2. Engineering-lead writes `FEEDBACK_FROM_ENGINEERING.md` in the engineering workspace AND copies (hardlinks or mv'd copy) to the research workspace at `teams/research/<research-slug>/FEEDBACK_FROM_ENGINEERING_<engineering-slug>.md`.
3. Engineering-lead classifies the feedback:
   - **BLOCKER**: engineering cannot proceed without re-research. Phase A returns to intake, session pauses. Lead escalates to user.
   - **DEGRADE**: engineering can proceed with a documented caveat ("shipping against the wrong library version, this works"). Session continues. Lead updates PLAN.md with the caveat.
   - **INFORMATIONAL**: research was wrong about a minor detail, engineering proceeds unchanged, feedback is logged for the next research session. No impact.
4. Feedback file includes: what research claim was wrong, what was actually observed, severity, proposed correction.

**Resolution**: add this 4-step protocol to PROTOCOL.md's cross-team handoff section. Enhancement accepted.

### H''5 — "Git identity hook under parallel session load"

**Claim**: `~/.claude/lib/git-identity.sh` switches the active `gh` account based on repo origin. If two Claude Code sessions run concurrently — one on repo A (gh account alpha), one on repo B (gh account beta) — and both try to commit at the same time, `gh auth switch` is globally scoped. The last-switcher wins. Session A can commit as beta when it meant to commit as alpha.

**Consistent with evidence because**: I read `git-identity.sh` directly; lines 41-45 invoke `gh auth switch --hostname github.com --user "$target"`. This is a **global** state change (writes `~/.config/gh/hosts.yml`), not per-repo.

The `--local` invocations of `git config` at the end set per-repo identity, but the intermediate `gh auth switch` is global. If session B runs `gh auth switch` to beta while session A is between its `gh auth switch` and its `git commit`, session A uses beta.

**Would be falsified by**: evidence that `gh auth switch` is per-process or that gh has concurrent account access. It isn't.

**Proposed mitigation**:
- Option 1: Add `flock` to git-identity.sh so only one invocation runs at a time, serializing gh account switches.
- Option 2: Skip `gh auth switch` entirely and use `GH_TOKEN` environment variable per session (requires knowing which token to use for which repo — doable but needs a lookup table).
- Option 3: Accept the race as a known risk; document "don't run parallel commit-generating sessions across multiple gh accounts."

**Most pragmatic**: Option 1 (add flock to git-identity.sh). The lock is local and short-held (microseconds during the switch). Add this as a concrete v1.1 enhancement to git-identity.sh. For v1 engineering-team, document the risk in PROTOCOL.md and mark it v1.1-TODO.

**Resolution**: explicit risk acknowledgment + v1.1 patch to git-identity.sh. Enhancement deferred to v1.1 but flagged.

### H''6 — "Evaluator rubric has 3 subjective dimensions"

**Claim** (from preliminary skeptic, restated): engineering-evaluator's 5-dim rubric has:
- Functional correctness — objective (tests pass)
- Test coverage — objective (coverage number)
- Diff minimality — subjective (what's "minimum viable"?)
- Revert-safety — subjective
- Style conformance — subjective

3 of 5 dimensions are LLM-as-judge calls. Anthropic's own Claude Agent SDK blog warns: "This is generally not a very robust method, and can have heavy latency tradeoffs."

**Consistent with evidence because**: librarian quoted this verbatim. It IS Anthropic's caution.

**Would be falsified by**: an empirical study showing LLM-as-judge on these dimensions is accurate. Our sample size is zero — this is untested in the engineering domain.

**Proposed mitigation**: make the objective dimensions strict-pass and the subjective dimensions softer:
- **Strict pass** (hard threshold): functional correctness ≥ 1.0 (all tests pass — no wiggle), test coverage ≥ existing baseline (no regression — objectively measurable).
- **Soft pass** (LLM judgment with thresholds): diff minimality ≥ 0.7, revert-safety ≥ 0.7, style conformance ≥ 0.7. These are advisory judgments; the evaluator explains its reasoning; the user can override.
- **Override protocol**: if the lead disagrees with the evaluator on a soft dimension, the lead writes the override rationale to `evaluator.md#lead-override` and proceeds. This preserves user agency.

The rubric STRUCTURE stays 5-dim; the PASSING mechanism splits into 2 strict + 3 advisory. This matches Anthropic's own guidance to "use LLM-as-judge where any boost in performance is worth the cost" but not to treat it as ground truth.

**Resolution**: engineering-evaluator's rubric has strict vs advisory dimensions. Enhancement refined.

### H''7 — "MAST FM coverage claim is hand-waved"

**Claim**: the cartographer + roster table claims "every specialist owns a MAST failure mode." Let me actually check all 14 MAST modes:

| MAST mode | Owned by (engineering-team) |
|---|---|
| FM-1.1 Disobey task spec | planner + lead (same as research) |
| FM-1.2 Disobey role spec | architect + executor |
| FM-1.3 Step repetition | planner + retrospector |
| FM-1.4 Loss of conversation history | scribe |
| FM-1.5 Unaware of termination | lead + evaluator (explicit termination cap) |
| FM-2.1 Conversation reset | scribe (LOG.md) |
| FM-2.2 Fail to ask for clarification | lead (intake protocol, never bounce) |
| FM-2.3 Task derailment | reviewer + lead |
| FM-2.4 Information withholding | scribe |
| FM-2.5 Ignored other agent's input | moderator (conditional) |
| FM-2.6 Reasoning-action mismatch | reviewer + verifier |
| FM-3.1 Premature termination | evaluator |
| FM-3.2 No/incomplete verification | verifier + evaluator |
| FM-3.3 Incorrect verification | verifier + reviewer + adversary + skeptic |

Every MAST mode has a named owner. **This is not hand-waved** — each mode maps cleanly. Claim accepted.

**Resolution**: no change needed, but SYNTHESIS.md should include this explicit table so future readers can audit.

## Unstated assumptions (full audit)

1. ~~"Inner loop terminates on acceptance criteria"~~ → addressed by H''2 soft/hard cap.
2. "Research SYNTHESIS.md is binding" → addressed by H''4 feedback protocol classification (BLOCKER/DEGRADE/INFORMATIONAL).
3. "Executor uses smallest-viable-diff by default" → still unstated; the reviewer runs too late to enforce. **Mitigation**: the executor persona explicitly constrains diff size in its hard rules, not just in the reviewer's rubric. "Default to smallest viable change" is the first hard rule.
4. "git-identity.sh works under parallel session load" → addressed by H''5.
5. "5-dim rubric is measurable objectively" → addressed by H''6 strict vs advisory split.
6. **NEW**: "Handback artifact fits the research workspace" — when engineering writes the handback file to `teams/research/<slug>/`, it's modifying another session's workspace. Research-scribe owns that directory. The handback write is a cross-team ownership violation unless we have an explicit rule. **Mitigation**: the handback file uses a distinct name prefix (`HANDBACK_FROM_ENGINEERING_<engineering-slug>.md`) and research-scribe's curation method explicitly allows engineering handbacks. Update research-scribe in PROTOCOL v2.1.

## Evidence quality audit (the "is our reasoning sound" pass)

- **H3 won across all 7 sources that addressed the question**. That's strong.
- **Synthesist found only 1 contradiction**. That's suspiciously clean. Either (a) the evidence genuinely converges, (b) the synthesist's pass was shallow, or (c) I (preliminary skeptic) didn't surface enough tension. Let me look: the 6 enhancements from synthesist are all refinements to H3, not challenges to it. No alternative got serious treatment.

**Test**: could a competent engineer read this workspace and argue for a genuinely different design? Yes:
- A strict pipeline advocate (MetaGPT/ChatDev lineage) could argue that Phase A needs explicit CEO/PM/Architect/Engineer/QA role separation, not just planner+architect.
- A pure ReAct advocate (Anthropic SWE-bench blog + SWE-agent) could argue that the entire Phase A is over-engineering on top of a system that works fine with just Bash + Edit + careful tool spec.
- An autonomous-agent advocate (Devin) could argue that inserting human gates and explicit phase boundaries defeats the point of autonomy.

**Why did none of these appear in Round 1?**
- Pipeline advocate: historian cited MetaGPT/ChatDev but rejected them on the "together" constraint and the waterfall overhead. The rejection was reasoned, not dismissive. Acceptable.
- Pure ReAct advocate: Anthropic's SWE-bench blog IS the minimal-ReAct argument, and it's cited. But historian reconciled it with "workflow outer, agentic inner" and H3 incorporates this. Acceptable.
- Autonomous-agent advocate: Devin's failure modes (multi-day runs, cost explosion) are cited as direct evidence AGAINST the autonomous approach. Acceptable.

The convergence is genuine. H3 is not "the only hypothesis I imagined" — it's the pattern the published prior art is converging on as of April 2026.

## Verdict

**Prematurely converged?** No — the convergence is evidence-backed, but the 7 enhancements from this full skeptic pass are required before "high confidence" can be stamped.

**Safe to raise confidence to "high"?** YES, conditionally on:
1. Enhancement H''1: tiered invocation with "override upward only" rule.
2. Enhancement H''2: soft/hard cap + token budget for Phase B termination.
3. Enhancement H''3: empirical pre-flight moved to plan-adversary's method.
4. Enhancement H''4: FEEDBACK_FROM_ENGINEERING.md classification protocol (BLOCKER/DEGRADE/INFORMATIONAL).
5. Enhancement H''5: git-identity.sh parallel-session risk documented, v1.1 patch with flock flagged as TODO.
6. Enhancement H''6: evaluator rubric strict/advisory split.
7. Unstated assumption #6: handback artifact naming convention + research-scribe extension in PROTOCOL v2.1.

**Required next probes before close**:
- Adversary must audit the Morph LLM source (our primary for SWE-bench contamination), the Devin failure-mode claims, the Claude Mythos Preview claim, the 25K-task X claim, and the aggregator sources.
- Evaluator must run the 5-dim rubric over the full SYNTHESIS.md after all 7 enhancements are incorporated.

## Confidence

**HIGH** on H3's core shape. **HIGH** that the 7 enhancements close the gaps I can see. **MEDIUM** that I caught everything — confirmation bias applies to skeptics too. Adversary + evaluator runs will catch what I missed.
