# HYPOTHESES — engineering-team-self-evolve-v1

Seeded by research-lead BEFORE dispatch, per v2 protocol Round 0 rule.
These are the competing designs the wide opener will test. The skeptic and
moderator will attack these in Round 2.

## H1 — Flat mirror (clone research, rename)

**Design**: Engineering Team is a near-1:1 structural clone of Research Team v2:
engineering-lead + 11 flat specialists, same Round 0 intake / Round 1 wide
dispatch / Round 2 gates / Round 3 evaluator / retrospector close. Roster:
planner, architect, executor, verifier, reviewer, skeptic, adversary, moderator,
evaluator, retrospector, scribe. Every specialist writes evidence, lead writes
synthesis (call it PLAN.md instead of SYNTHESIS.md).

**Pros**:
- Zero cognitive tax: Akash already knows the research protocol, this inherits the same mental model.
- Validated substrate: the v2 protocol just passed a real session. Known to work.
- Same gates catch the same failure modes that MAST identifies: Research Team v2's gate ordering was designed around MAST categories, and engineering failures overlap heavily (FM-1.1 task-spec violation, FM-2.5 ignored input, FM-3.2 no verification).

**Cons**:
- Research is parallel by nature (8 lenses probing simultaneously). Engineering is inherently sequential in parts (plan → architect → execute → verify). Forcing parallel wide-opener on a sequential activity is MAST FM-1.3 (step repetition) waiting to happen.
- "Synthesist" doesn't have an obvious engineering analogue — who synthesizes what, before execution has happened?
- The round-based clock doesn't match execution reality. Engineering sessions can have 5 execute-verify loops before handback; research has 1 synthesis pass. Fixed round structure will under- or over-iterate.

**Predicted by**: orthodox Anthropic "use the same pattern" advice. But Anthropic's own "Building effective agents" post explicitly distinguishes workflow (fixed path) from agent (dynamic), and engineering is mostly workflow.

## H2 — Pipeline with incremental ReAct inner loop

**Design**: Outer frame is a fixed pipeline — Round 0 intake → Round 1 plan → Round 2 architect → Round 3 execute (inner ReAct loop) → Round 4 verify → Round 5 review → Round 6 retro. Inside Round 3, engineering-executor runs a ReAct-style gather-act-verify-repeat cycle that can back out to engineering-architect if it hits an architectural blocker, or to engineering-planner if it hits a spec blocker. Fixed stages for predictability, dynamic inner loop for reality.

**Pros**:
- Matches Anthropic's "workflow vs agent" framing: predictable stages outside, dynamic inner loop where work actually happens.
- Imports the Claude Agent SDK's published "gather context → take action → verify work → repeat" pattern verbatim.
- Naturally handles the common case of "executor discovers the plan is wrong mid-implementation" — there's a named back-edge.
- Keeps the handoff to Research clean because the pipeline's Round 0 reads CHARTER.md (which reads research SYNTHESIS.md) and produces a plan commitment before touching code.

**Cons**:
- Pipeline stage boundaries are artificial: if engineering-executor wants to question the plan, is it in Round 3 (execute) or back in Round 1 (plan)? Ambiguous state.
- Fixed pipeline can still under-iterate on "small bug fix" (shouldn't need a full 6-round dance) and over-iterate on "multi-week feature" (needs 5 plan-execute cycles, not 1).
- The Round 3 inner-ReAct loop has its own termination problem (MAST FM-1.5 unaware-of-termination).

**Predicted by**: ChatDev's CTO-PM-programmer-tester waterfall pattern literally does this; SWE-agent's trajectory pattern does this; Devin's "plan + execute + check" dance does this. The pattern works in production; the post-mortems are about tuning inner-loop termination.

## H3 — Unified hybrid: flat roster + two-phase round structure

**Design**: Single lead, flat roster (no sub-leads), but round structure is **two-phase** instead of 6-stage:
- **Phase A — Plan** (rounds 0–1): intake, plan commitment, architect design, plan-skeptic gate, plan-adversary gate. Produces PLAN.md.
- **Phase B — Build** (rounds 2–N): ReAct loop of execute-verify-review until all acceptance criteria pass, then retro. Variable N.

The "together" constraint is solved by having planner and executor in the same lead's roster, same workspace, same ledger, with an explicit phase gate between them. Plan-phase gates (skeptic on the plan, adversary on the research CHARTER it cites) run ONCE at the phase boundary. Build-phase gates (verifier, reviewer) run EACH inner iteration.

**Pros**:
- Mirrors "orchestrator-worker with evaluator-optimizer" from Anthropic's "Building effective agents" post verbatim.
- Only two mandatory gates on the critical path (plan-skeptic at phase boundary, evaluator at handback), everything else is conditional — keeps simple sessions cheap.
- The inner build loop can iterate as many times as needed without forcing Akash to define "rounds" upfront.
- Clean R→E handoff: CHARTER.md is the Phase-A input; handback is the Phase-B output; nothing in the middle needs to touch the research workspace.
- Same lead, same files, same memory: matches the "together" constraint literally.

**Cons**:
- Two-phase machinery needs to explain what happens if Phase B discovers Phase A was wrong (back-edge to planner, recompute phase gate).
- "Variable N" inner loop is a termination landmine if not bounded. Needs explicit termination rules per-task.
- Doesn't map 1:1 to research protocol; Akash has to learn a second mental model.

**Predicted by**: Anthropic's own "evaluator-optimizer" pattern from the blog post, Aider's architect-mode, Cursor's "plan then apply" behavior, the SWE-agent trajectory structure.

## H4 — Pure ReAct with no explicit phases

**Design**: engineering-lead runs a single big ReAct loop from intake to handback. Every "round" is a tool call. Specialists are lenses invoked within the loop as needed, not as fixed gate-holders. Plan, execute, verify, review happen interleaved. Closes when acceptance criteria are met or a budget cap trips.

**Pros**:
- Maximum flexibility: small tasks close in 2-3 iterations, big tasks run 50.
- No artificial phase boundaries to debate.
- Matches Devin-style autonomous loop most closely.

**Cons**:
- Zero structural memory: without phases, the retrospector can't see where the failure modes hit.
- MAST FM-1.5 (unaware of termination) gets no explicit defense — pure ReAct loops are known to drift.
- Plan-review is not a gate, it's a sub-tool-call — Akash can't inject human review at "the plan" moment because there is no "plan" moment, just a running trajectory.
- Contradicts the research-team substrate. Akash's mental model is gate-based.

**Predicted by**: Cognition (Devin), early SWE-agent. Post-mortems from both show that unbounded ReAct loops are harder to debug than phased flows.

## H5 — Two-team split (ruled out by Akash's constraint)

**Design**: Separate Planning Team and Execution Team under different leads, handoff between them.

**Ruled out by**: the explicit constraint "a team of planners and executers that are **together**". Noting it for completeness so the skeptic doesn't re-propose it.

## Ranking (provisional, to be tested by wide opener)

- **Most likely to win**: **H3 (unified hybrid)**. It matches the "together" constraint, inherits research-protocol mental model for gates, imports Anthropic's orchestrator-worker + evaluator-optimizer verbatim, and has a clean phase boundary for the plan-review gate.
- **Runner-up**: **H2 (pipeline with inner ReAct)**. Cleaner for "one-shot feature" work, worse for "progressive discovery" work.
- **H1 flat-mirror**: cargo-cult risk. Gets dismissed after wide-opener unless prior art supports it.
- **H4 pure ReAct**: ruled out on structural-memory and termination grounds unless the skeptic has a strong counterargument.

## What the gates will test

- **Wide opener**: does the prior art (Devin, SWE-agent, OpenHands, Aider, AutoGen, MetaGPT, ChatDev, CrewAI, Claude Agent SDK) converge on H2 or H3? Or does it reveal an H6 we haven't seen?
- **Moderator**: if two specialists disagree on phase-vs-pipeline-vs-flat, run a 3-round debate.
- **Skeptic**: attack the leading hypothesis for (a) premature convergence, (b) single-source dependency, (c) MAST FM-1.5 termination defense, (d) what happens when the inner loop contradicts the outer frame.
- **Adversary**: audit the SWE-bench leaderboard, the Devin demo claims, any Medium / Substack / aggregator content about "AI engineering agents." This corpus is contested; run the adversary pre-emptively.
- **Evaluator**: 5-dim rubric on the final design document — but the engineering-team rubric needs its own shape. (This session's evaluator runs the RESEARCH-team 5-dim rubric, not the engineering one, because this is a research session about engineering-team design.)

## Open sub-question for the planner

The meta-task asks for a "minimum roster" of 11 and asks whether to add debugger, simplifier, documenter, migrator. The planner should return a recommendation on the roster count AND the gate structure AND the round count AND the inner-loop termination rule. That's four independent design decisions; the planner should enumerate them and say which the wide opener can validate in parallel vs which need to be synthesized after the opener returns.
