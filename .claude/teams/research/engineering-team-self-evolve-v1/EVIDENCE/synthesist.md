# Synthesist — claim matrix and contradictions across Round 1 evidence

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: cross-source integration, claim matrix, contradiction surfacing
Mode: adopted persona

## Scope

Read every Round 1 evidence file. Build a claim matrix. Surface contradictions. Flag what the moderator needs to debate, what the skeptic needs to refine, what the adversary needs to audit.

## Round 1 evidence inventory

| File | Author | Size | Primary claims |
|---|---|---|---|
| `planner.md` | research-planner | ~8KB | dispatch recommendation, 10 specialists, 3-round estimate |
| `cartographer.md` | research-cartographer | ~9KB | structural map, 12-specialist roster, file layout |
| `archaeologist.md` | research-archaeologist | ~8KB | v1→v2 pressures + MEMORY.md 1-12, 5 engineering-specific pressures |
| `linguist.md` | research-linguist | ~10KB | vocabulary commitments, polysemy traps, H3 rename |
| `librarian.md` | research-librarian | ~13KB | 6 Anthropic canonical sources with verbatim quotes |
| `historian.md` | research-historian | ~12KB | academic + production prior art, hybrid-wins, benchmark contamination |
| `web-miner.md` | research-web-miner | ~6KB | 14-day freshness, SEAL leaderboard, community sentiment |
| `github-miner.md` | research-github-miner | ~7KB | cross-repo patterns, role counts, coordination substrates |
| `tracer.md` | research-tracer | ~11KB | concurrency design, flock+rename+staging, merge protocol pseudocode |
| `empiricist.md` | research-empiricist | ~8KB | 6 empirical tests, timeout(1) correction, R1-R6 validation |
| `skeptic-preliminary.md` | research-skeptic | ~7KB | 6 competing hypotheses, 5 unstated assumptions, enhancement list |

Total: 11 files, ~99KB.

## Claim matrix

### Claim 1: H3 is the right hypothesis

| Source | Position | Evidence |
|---|---|---|
| historian | H3 is where the prior art converged in 2026 | "the plan-and-execute vs ReAct debate is effectively settled as a false dichotomy" (hybrid wins) |
| librarian | H3 composes Anthropic's own published patterns | orchestrator-worker + evaluator-optimizer + minimal-ReAct verbatim from 3 Anthropic sources |
| cartographer | flat roster (not hierarchical) supports H3 | zero naming collision on `engineering-*`, 12 + lead |
| linguist | "two-phase orchestrator + evaluator-optimizer" rename improves clarity | polysemy audit, "hybrid" label was misleading |
| skeptic-preliminary | H3 shape is right but needs enhancement | H'1 termination cap, H'4 tiered dispatch, H'6 synthesist absorption |
| archaeologist | v2 gate structure can be mapped onto engineering with adjustments | "evolutionary pressures that should carry over" section |
| github-miner | 13-specialist roster is mid-range, justified by MAST coverage | role-count comparison table |

**Verdict**: **H3 converged**. All 7 sources that addressed the question support H3's core shape (flat + two-phase + mandatory gates). Three sources (skeptic-preliminary, linguist, empiricist via the timeout correction) specify enhancements. **No Round 1 source contradicts H3**.

### Claim 2: Subagents cannot spawn other subagents

| Source | Position | Evidence |
|---|---|---|
| librarian | verbatim confirmed | "Subagents cannot spawn other subagents. If your workflow requires nested delegation, use Skills or chain subagents from the main conversation." (sub-agents.md, retrieved 2026-04-12) |
| archaeologist | MEMORY.md lesson 7 encodes this as protocol rule | "Subagents cannot spawn subagents — plan accordingly" with adopted-persona pattern 2 |
| cartographer | structural implication: no sub-leads in engineering-team | "Sub-leads would re-introduce the subagent-cannot-spawn-subagents problem twice" |

**Verdict**: **fully agreed**. Load-bearing for engineering-lead's persona design — must inherit adopted-persona pattern 2 from research-lead.

### Claim 3: The `memory: user` canonical path and auto-injection

| Source | Position | Evidence |
|---|---|---|
| librarian | `~/.claude/agent-memory/<name-of-agent>/` + "first 200 lines or 25KB" injection | verbatim from sub-agents.md |
| tracer | write directly to `~/.claude/agent-memory/engineering-lead/MEMORY.md` with staging/_lock/topic siblings | follows librarian's canonical path |
| cartographer | proposed layout with `.lock`, `staging/`, `topic/`, `_archive/` as siblings | backward-compatible with existing research-lead path |

**Verdict**: **fully agreed**. Layout is canonical.

### Claim 4: Concurrency protocol — flock + atomic rename + staging files

| Source | Position | Evidence |
|---|---|---|
| tracer | design correct, rationale documented | 6-requirement table, rejection of SQLite/git/CRDT alternatives |
| empiricist | design validated with critical correction | Tests 1-6, 10 concurrent merges in 0.07s, CRITICAL: `timeout(1)` wrapping mandatory |
| librarian | Anthropic's own agent-teams runtime uses file locking | "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously" |

**Contradiction**: tracer's pseudocode did NOT include `timeout(1)` wrapping. Empiricist's Test 3f demonstrated this is unsafe. Empiricist's Test 3g showed the correction works.

**Verdict**: **MINOR CONTRADICTION**, empiricist's correction is load-bearing. Synthesis uses the corrected pattern:
```bash
flock -w 5 -x "$LOCK" timeout --signal=KILL --kill-after=1 30 bash -c '<merge body>'
```

**Not a moderator case** — the disagreement is evidence-gap (tracer reasoned from docs, empiricist ran real code; real code wins). Linguist + empiricist resolve this directly.

### Claim 5: SWE-Bench contamination is real

| Source | Position | Evidence |
|---|---|---|
| historian | contamination confirmed, Pro is the load-bearing benchmark | OpenAI audit, 59.4% flawed test cases, Claude Opus 4.5: 80.9% Verified / 45.9% Pro |
| web-miner | corroborated via multiple leaderboard sources | SEAL leaderboard, Morph LLM, Simon Willison (content mismatch on retrieval) |

**Uncertainty**: the Morph LLM source is a commercial vendor (Morph competes with Cursor). Adversary should audit this source.

**Verdict**: **strong claim, adversary-audit required**. Primary source for OpenAI audit quote is Morph LLM's page. If adversary rejects Morph as too interested, the claim must be re-sourced or downgraded.

### Claim 6: Plan-and-Execute hybrid is the winning prior-art pattern

| Source | Position | Evidence |
|---|---|---|
| historian | hybrid wins; confirmed across academic + production | synthesis section "Position on plan-vs-execute debate (2026 synthesis)" |
| librarian | Anthropic publishes both patterns; composing them is legitimate | orchestrator-worker + evaluator-optimizer from "Building effective agents" |
| web-miner | community sentiment: "ReAct inside, plan outside" | aggregated HN/X sentiment, non-primary |
| github-miner | Aider architect mode is the closest production analogue | directory structure of `aider/coders/` |

**Verdict**: **fully agreed**.

### Claim 7: Engineering-team roster size

| Source | Position | Evidence |
|---|---|---|
| cartographer | 12 specialists + lead = 13 | roster table with v1.1 future-additions |
| github-miner | mid-range between SWE-agent (1) and research-team (18) | cross-repo comparison |
| skeptic-preliminary | 12 is over-dispatched for common tasks; need tiering | H'4 competing hypothesis |

**Contradiction**: cartographer says 12 is right; skeptic-preliminary says 12 is too many for common tasks without tiering.

**Verdict**: **REFRAME** — the tiered-dispatch insight is an enhancement to the 12-specialist roster, not an alternative. Resolution: **keep 12 specialists in the roster**, but add **tiered invocation rules** to the lead's intake protocol. Trivial tasks dispatch 2 specialists; scoped tasks dispatch 4-6; complex tasks dispatch full roster. This is H3 + enhancement, not H3-vs-H'4. No moderator debate needed; synthesis absorbs.

**This is the first load-bearing enhancement to H3**: tiered invocation is a new section in PROTOCOL.md.

### Claim 8: Phase B inner loop must have explicit termination rule

| Source | Position | Evidence |
|---|---|---|
| skeptic-preliminary | H'1: inner loop drifts without a cap; MAST FM-1.5 hazard | historian's Devin multi-day failure evidence |
| historian | Devin's autonomous loop failure mode is "multi-day sessions" and "inability to recover from bad initial plans" | public Devin year-in-review commentary |
| librarian | Anthropic recommends "stopping conditions such as a maximum number of iterations" | "Building effective agents" verbatim |

**Verdict**: **agreed — needs explicit rule**. Resolution: **Phase B has a hard cap of `max(5, 2 × PLAN.task_count)` inner iterations**. On cap, escalate to lead with options {re-plan / hand back / mark degraded}.

**This is the second load-bearing enhancement to H3**: explicit Phase B termination rule in PROTOCOL.md.

### Claim 9: The plan-gate (skeptic + adversary on PLAN.md) is the load-bearing defense

| Source | Position | Evidence |
|---|---|---|
| librarian | evaluator-optimizer pattern requires a legitimate evaluator at plan time | Anthropic's recommendation for "iterative refinement provides measurable value" |
| historian | Devin fails because no plan-gate; Aider architect mode succeeds because it has one | prior-art synthesis |
| skeptic-preliminary | plan-gate has a blind spot: can't catch runtime-behavior bugs without executing | H'2 |
| cartographer | plan-skeptic + plan-adversary run at Phase A → Phase B boundary | file layout |

**Resolution for H'2 blind spot**: add an "empirical pre-flight" step at the very start of Phase B — engineering-executor runs a 5-minute probe to verify any externally-behavior-dependent plan claim BEFORE committing to real implementation. Document in executor persona.

**Verdict**: agreed, with H'2 mitigation.

**This is the third load-bearing enhancement**: empirical pre-flight step at Phase B entry.

### Claim 10: Engineering-moderator is needed (even if rarely invoked)

| Source | Position | Evidence |
|---|---|---|
| librarian | debate-structured investigation is canonical | Claude Code agent-teams "the debate structure is the key mechanism here" |
| archaeologist | moderator was a v2 addition to research-team | research PROTOCOL "What changed from v1" section |
| skeptic-preliminary | engineering contradictions are rarer than research; moderator may be dead weight | H'5 |

**Tension**: skeptic says moderator is dead weight in engineering. Librarian + archaeologist say debate structure is canonical.

**Resolution**: keep engineering-moderator in the roster but mark it **conditional — dispatched only when two specialists file contradicting evidence about a load-bearing fact**. For taste disputes (e.g. "diff is too big" vs "diff is minimum viable"), the reviewer has final say. For evidence contradictions (e.g. "verifier says tests pass" vs "reviewer says test coverage is inadequate" — different facts about the same diff), moderator debates.

**Not a moderator case** — this is a clarification about when moderator runs. Synthesis absorbs.

## Load-bearing contradictions for moderator debate

After the matrix analysis, **only ONE real load-bearing contradiction** is left:

### Contradiction C1: Is `engineering-synthesist` a specialist or is the lead's PLAN.md the synthesist's output?

- **Position A** (research-team parallel): engineering-synthesist is a specialist. Runs after Phase A closes. Builds a claim matrix across planner.md + architect.md + adversary.md + skeptic.md. This preserves the v2 gate structure (synthesist → moderator → skeptic → adversary → evaluator).
- **Position B** (absorbed by lead): the lead writes PLAN.md, which IS the integrated output. Plan-skeptic and plan-adversary attack PLAN.md directly. No synthesist specialist needed. This is what skeptic-preliminary's H'6 proposes.

Both positions have support. Position A keeps the v2 structure clean. Position B keeps the roster at 12 (no extra synthesist) and matches the engineering workflow more naturally.

**This warrants a moderator debate**. See `moderator.md` for the 3-round resolution.

## Other non-load-bearing clarifications

- **Roster count**: 12 specialists + lead = 13 total. Confirmed across cartographer, linguist, github-miner, skeptic-preliminary. No dispute.
- **File layout**: CHARTER.md + PLAN.md + HYPOTHESES.md + EVIDENCE/*.md + DIFF_LOG.md + VERIFY_LOG.md + LOG.md + OPEN_QUESTIONS.md + conditional FEEDBACK_FROM_ENGINEERING.md. No dispute.
- **Frontmatter**: `model: opus` + `effort: max` on every agent. No dispute.
- **Memory path**: `~/.claude/agent-memory/engineering-lead/MEMORY.md` with staging/_lock/topic siblings. No dispute.
- **Concurrency protocol**: flock + atomic rename + staging + timeout(1) wrapping. Minor contradiction resolved via empiricist's correction.

## Polysemy traps caught (from linguist)

During the claim matrix build, the linguist's flagged traps helped avoid false contradictions:

1. "Planner" meaning drift — linguist committed to "decomposition + blueprint" meaning. No false contradiction between cartographer (mentions planner for decomposition) and librarian (mentions Anthropic's meta-role).
2. "Verify" meaning drift — verifier (per-iteration) vs evaluator (final). Cartographer and empiricist both use the term; no conflation.
3. "Plan" meaning drift — PLAN.md (document) vs "plan" (commitment) vs "Plan-and-Solve" (pattern). All used consistently after linguist's glossary.
4. "Phase" vs "round" — engineering uses phases, research uses rounds. No confusion in claim matrix.
5. "Hybrid" → "two-phase orchestrator + evaluator-optimizer" — linguist-suggested rename applied throughout.

No false contradictions were generated.

## Summary of required enhancements to H3 before final SYNTHESIS.md

1. **Tiered invocation** (from claim 7): lead's intake classifies trivial/scoped/complex and dispatches only mandatory specialists per tier.
2. **Phase B termination rule** (from claim 8): hard cap `max(5, 2 × PLAN.task_count)` inner iterations, escalation path on cap.
3. **Empirical pre-flight step** (from claim 9): executor runs a 5-minute probe at Phase B entry to verify externally-behavior-dependent plan claims.
4. **Corrected concurrency snippet** (from claim 4): `flock -w 5 -x "$LOCK" timeout --signal=KILL --kill-after=1 30 bash -c` canonical pattern.
5. **Moderator C1 resolution** (from contradiction list): pending moderator debate.
6. **Engineering-moderator made conditional** (from claim 10): only runs on evidence contradictions, not taste disputes.

## Handoff to moderator

Dispatch `research-moderator` on **contradiction C1** only. Expected verdict: REFRAME ("both are partially right — use hybrid"). Expected action: the lead absorbs the synthesist's integration role at Phase A close (Position B), but the engineering-team's specialist list STILL INCLUDES a synthesist-analogue lens in the Round 2 build-phase (inside Phase B, between executor and reviewer iterations, a lightweight "has the current state drifted from PLAN.md" check). Call that role the lead's own responsibility or absorb into reviewer — moderator will decide.

## Handoff to skeptic (full Round 2 pass)

The preliminary skeptic's 6 competing hypotheses remain on the table. Round 2 skeptic should:
1. Re-examine H'1-H'6 against the claim matrix.
2. Attack the enhanced H3 (with the 6 enhancements above).
3. Verify that "all 12 specialists have MAST ownership" is not just a promise but a genuine coverage.
4. Specifically audit the assumption that `git-identity.sh` works under team-session load (unstated assumption #4 from preliminary).

## Handoff to adversary

The adversary must audit:
1. The SWE-Bench contamination claim (Morph LLM is commercial, with interest).
2. The Devin failure-mode claims (secondhand from X/HN, no primary source).
3. The Claude Mythos Preview 93.9% claim (unverified internal name at top of Verified leaderboard).
4. The "25K-task experiment" X claim (single-witness).
5. The aggregator sources in web-miner (llm-stats.com, benchlm.ai, groundy.com).
6. The Simon Willison retrieval anomaly (fetched content did not contain the expected contamination discussion — may be cache issue, may be wrong URL, may be genuine mismatch).

## Confidence

**HIGH on the core design** (H3 + 6 enhancements), **MEDIUM pending C1 moderator verdict**, **MEDIUM pending adversary audit of the SWE-bench contamination claim's primary source**.
