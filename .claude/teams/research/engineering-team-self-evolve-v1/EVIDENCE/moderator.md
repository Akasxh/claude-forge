# Moderator — 3-round debate on C1 (engineering-synthesist: specialist or lead-absorbed?)

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: structured debate, DebateCV protocol, REFRAME-aware verdicts
Mode: adopted persona

## The contradiction

**Claim X (Position A)**: Engineering-team should have a dedicated `engineering-synthesist` specialist that runs after Phase A closes, builds a claim matrix, and feeds moderator+skeptic+adversary gates. Preserves the v2 research-team gate ordering (synthesist → moderator → skeptic → adversary → evaluator).

Supported by: **the v2 research-team structural analogy**, `archaeologist.md` (the v2 gate order was the load-bearing addition), `librarian.md` (debate structure requires a pre-debate claim matrix). `EVIDENCE/archaeologist.md#v1-to-v2-diff`, `EVIDENCE/librarian.md#the-debate-structure`.

**Claim not-X (Position B)**: Engineering-team's lead absorbs the synthesist role implicitly at the Phase A close — lead writes `PLAN.md` which IS the integrated claim matrix, and plan-skeptic + plan-adversary attack PLAN.md directly without an intermediate synthesist. Eliminates one specialist from the roster and matches the natural engineering workflow where PLAN.md is the authored artifact, not a derived matrix.

Supported by: **skeptic-preliminary's H'6**, `EVIDENCE/skeptic-preliminary.md#H6-absent-synthesist`, structural parsimony.

Reported by: `synthesist.md#contradictions`
Load-bearing for final design? **YES** — changes the roster count (12 vs 13) and the Phase A structure.

## Round 1 — opening statements

### Position A's case (in the voice of the "preserve v2 structure" camp)

In research-team v2, the synthesist is not decorative. It is the specialist that converts scattered specialist-output into a single integrated claim matrix with contradictions flagged. The moderator needs this matrix as its input ("here are the contradictions that need debate"). The skeptic needs it as its attack surface. The adversary needs it to identify which corpus-audit findings are load-bearing. Without the synthesist pass, each downstream specialist builds its own partial view of the evidence and has to re-derive the integrated state, which is FM-1.3 (step repetition) multiplied across 3 specialists.

The research-team v2 pilot session (claude-memory-layer-sota-2026q2) proves the synthesist adds value: 5 load-bearing contradictions surfaced, each one became a moderator debate that changed the final synthesis direction. Without a synthesist pass, those contradictions would have been invisible.

For engineering-team, the same pattern applies at the Phase A close: planner output (task decomposition), architect output (design decisions), and any empirical output from the plan-adversary's pre-flight probes form a multi-lens evidence set that needs integration. If the lead authors PLAN.md directly without a synthesist step, the lead is doing TWO jobs at once (integrate AND commit), which is exactly the "orchestrator also owns synthesis" anti-pattern that v1 research-team had and v2 fixed.

**Steel-man of Position B**: I concede that engineering Phase A has fewer specialists than research Round 1 (planner + architect + plan-skeptic + plan-adversary = 4, vs research's 8-10 wide-opener). With fewer specialists, there's less matrix-integration work. A lighter synthesist pass — maybe just a "structural consistency check" — may be enough. I don't need a full v2-research-grade synthesist; I need a scoped integration pass.

### Position B's case (in the voice of the "lead absorbs" camp)

The research-team synthesist exists because research has 8-10 parallel lenses producing 8-10 independent evidence files, each focused on a different corpus, with significant overlap and contradiction potential. Engineering Phase A has only 2-4 specialists producing evidence files (planner, architect, plus optional skeptic/adversary) and the integration work is orders of magnitude smaller.

The engineering-lead is NOT a passive orchestrator like research-lead. Engineering-lead has more judgment and fewer gates because engineering decisions are deterministic-ish (does this code work? is this diff safe?), not evidence-probabilistic (do these 10 sources converge?). The lead writing PLAN.md IS the integration — the lead reads planner.md and architect.md, commits to a plan, documents it. That's not "two jobs" — that's ONE job at the right level.

Adding an `engineering-synthesist` specialist adds rostering overhead (another persona file, another dispatch, another gate) for marginal gain. The "integrate before gates" function is served by the lead's intake protocol.

**Steel-man of Position A**: I concede that if Phase A ever grows to 5+ specialists (e.g. we add security-reviewer, perf-reviewer, api-reviewer), the integration load becomes non-trivial and a synthesist would help. For v1 with 2-4 Phase-A specialists, the marginal gain doesn't justify the extra role.

## Round 2 — cross-examination

### A asks B

"If the lead writes PLAN.md directly, what happens when planner.md and architect.md contain contradicting recommendations? Who surfaces the contradiction for moderator debate? The lead is NOT disinterested — it's going to author PLAN.md, so it has confirmation-bias stake in whichever direction it's already leaning. MEMORY.md lesson 4 ('contradictions go to the moderator, not to your own judgment') says EXPLICITLY that the lead cannot be trusted to arbitrate contradictions. How does Position B solve this?"

**Evidence demanded**: a concrete Phase-A contradiction-handling flow that preserves lead disinterestedness on contradictions.

### B asks A

"Show me a concrete Phase-A contradiction you expect between planner.md and architect.md. Research contradictions are frequent because 10 lenses probe the same topic and disagree on framing. Engineering has 2 specialists with specified roles (planner = decomposition, architect = commitment). If the architect commits to a decision the planner didn't foresee, that's not a contradiction — that's the architect doing its job. If the planner's task decomposition is infeasible given the architect's decisions, that's not a contradiction either — that's a re-plan signal, handled by phase back-edge. Where's the actual contradiction-shaped problem that needs synthesist + moderator?"

**Evidence demanded**: a concrete engineering-team scenario where two Phase-A specialists genuinely disagree on an evidence claim (not a role-handoff or re-plan situation).

### Classification of the disagreement

**Scope mismatch**. Position A is reasoning about research-like contradictions (multi-source convergence disagreements). Position B is reasoning about engineering workflows where "contradictions" are usually role handoffs or re-plan signals. They're using the word "contradiction" to mean different things.

This is not a real disagreement. It's a polysemy issue that the linguist's audit flagged pre-emptively ("plan" and "verify" meaning drift), and the moderator's REFRAME verdict (MEMORY.md lesson 10) is the right tool.

## Round 3 — verdict

**Winner**: **REFRAME** — both sides are partially right, the question is mis-posed.

**Reasoning**:

1. Position B is right that Phase A has few enough specialists that a dedicated synthesist specialist is overkill.
2. Position A is right that the lead cannot be trusted to arbitrate contradictions if any arise.
3. The reframe: **what we need is NOT a synthesist specialist — what we need is a lightweight "integration step" in the lead's Phase A close protocol, with an explicit contradiction detection rule that, on detection, dispatches the engineering-moderator.**

### The committed resolution

**Phase A close protocol** (this goes into PROTOCOL.md, not a new specialist file):

1. Lead reads `EVIDENCE/planner.md` and `EVIDENCE/architect.md`.
2. Lead performs a **structural consistency check** (not a full claim matrix — just "do these two artifacts reference the same task list and agree on the architectural decisions"):
   - If planner.task[i] references a module X, architect.md must have a design for module X.
   - If architect.md commits to library Y at version V, planner.md's blast-radius estimates must account for Y-V.
   - If either the planner or architect flags a risk, the other must acknowledge it.
3. **If structural consistency holds**: lead writes `PLAN.md` as the integrated plan and proceeds to plan-skeptic + plan-adversary gates. No contradiction, no moderator.
4. **If structural inconsistency detected**: lead writes the inconsistency to `OPEN_QUESTIONS.md` and **dispatches engineering-moderator** with the two contradicting sources. Moderator runs its 3-round debate, issues a verdict, lead updates PLAN.md with the verdict direction.
5. **If either planner or architect reports a blocker ("this task is infeasible given known constraints")**: lead dispatches back to planner or architect for replan/redesign, not moderator.

### What changes in the roster

**No `engineering-synthesist` specialist in v1**. The lead absorbs the structural consistency check as a protocol step, not a dispatchable role. Roster stays at 12 specialists + lead.

**`engineering-moderator` remains in the roster** — it runs CONDITIONALLY on detected contradictions, same protocol as research-moderator. In the common case (planner and architect converge), moderator is not dispatched; in the contradiction case, moderator's 3-round debate pattern applies.

### What changes in the gates

**Plan-gate** (Phase A close) becomes:

1. Lead reads planner.md + architect.md
2. Lead runs structural consistency check (protocol step, not dispatch)
3. If contradiction: dispatch moderator (rare); else skip
4. Dispatch engineering-skeptic on PLAN.md (mandatory)
5. Dispatch engineering-adversary on CHARTER.md sources (mandatory if CHARTER cites a research SYNTHESIS.md or external library docs)
6. If any gate FAILs: return to planner or architect for re-work
7. If all pass: proceed to Phase B

This preserves the v2 research protocol's gate rhythm (skeptic + adversary + moderator) without adding a synthesist specialist.

**Evidence that tipped it**: MEMORY.md lesson 4 (contradictions go to moderator, not lead) is the WHY for Position A's concern. But lesson 4 also says "Any contradiction flagged in synthesist.md that affects the final answer gets a moderator dispatch, no exceptions." The key word is "flagged" — something has to flag the contradiction. In research, synthesist flags. In engineering, the structural consistency check flags. Mechanism differs; function preserved.

### Action required

1. **SYNTHESIS.md**: document the Phase-A close protocol with the structural consistency check.
2. **PROTOCOL.md**: "Round structure (engineering-team v1)" section lists the Phase-A close protocol as a step in the lead's workflow.
3. **engineering-lead persona**: explicit method for the structural consistency check and when to dispatch moderator.
4. **No new specialist file**: `engineering-synthesist.md` is NOT written for v1. If v2 adds enough Phase-A specialists (security-reviewer, perf-reviewer, etc.) that integration becomes non-trivial, revisit.

## Confidence in verdict

**HIGH** — the REFRAME is clean, both sides' strongest arguments are preserved, the committed resolution preserves the v2 gate rhythm while keeping the roster at 12. This is the canonical REFRAME pattern from MEMORY.md lesson 10.

## Handoff

SYNTHESIS.md section "Round structure — Phase A close" will implement this verdict. Lead's persona will document the structural consistency check. Roster stays at 12. No new specialist file needed.
