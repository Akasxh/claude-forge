# Linguist — vocabulary audit for engineering-team-self-evolve-v1

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: polysemy, semantic drift, naming commitments

## Why this pass exists

MAST FM-2.6 (reasoning-action mismatch) and FM-2.5 (ignored other agent's input) frequently reduce to polysemy: two specialists use the same word for different things, the synthesist sees a "contradiction," the moderator runs a needless debate. This pass pre-empts those false contradictions by committing the vocabulary up front.

Per MEMORY.md lesson 11 (moderator REFRAME), polysemy is the biggest class of "debates that shouldn't have run." Handle it here.

## Term-by-term audit

### "Planner"

The word collides across **three** distinct existing meanings in `~/.claude/agents/`:

| Source | Role | Method | Output |
|---|---|---|---|
| `~/.claude/agents/planner.md` | **Interview-and-save-plan** role. Asks user one question at a time via AskUserQuestion, spawns explore for codebase facts, generates a 3-6 step plan with acceptance criteria, saves to `.omc/plans/{name}.md`. | Consultative interview. | `.omc/plans/{name}.md` |
| `~/.claude/agents/architect-planner.md` | **Blueprint architect**. Produces a 7-section technical plan (Problem Statement, Research & Context, Proposed Architecture, Affected Areas, Risks, Phases, Open Questions). Model: opus. | Research first, then write plan. | Markdown technical plan document |
| `~/.claude/agents/research/research-planner.md` | **Dispatch breadth advisor**. Runs once at session start after QUESTION.md. Reads question + HYPOTHESES + MEMORY.md. Writes dispatch recommendation (which specialists, how many, in what groupings). Does NOT plan the work itself. | Meta-planning — "how to dispatch the team" | `EVIDENCE/planner.md` in session workspace |

**Three meanings**: interview-and-ask, write-a-blueprint, and meta-plan-the-dispatch. The proposed `engineering-planner` must pick ONE.

**Commit**: **engineering-planner is the "decomposition + blueprint" role**. It reads CHARTER.md (which cites research SYNTHESIS.md as binding input) and produces `PLAN.md` with a dependency-graphed task list, blast-radius estimates, and rollback sketches. This is closest to `architect-planner.md` semantically but scoped to a single engineering session and wrapped in the team protocol.

**NOT the research-planner analogue**. The research-planner's "advise on dispatch breadth" role is absorbed into the engineering-lead's own judgment, because engineering-team dispatch is simpler (fewer hypotheses, more sequential) and doesn't need a separate meta-planner. A future `engineering-dispatcher` specialist could be added in v2 if dispatch-planning turns out to be load-bearing.

**NOT the flat `planner.md` analogue**. That role's "interview the user one question at a time" method doesn't fit a team-session flow. Engineering-lead does the user intake, the planner receives an already-framed CHARTER.

**Definition for engineering-team**:
> `engineering-planner` reads the CHARTER.md (which cites a research SYNTHESIS.md if cross-team), decomposes the work into an atomic task dependency-graph, estimates blast radius per task, sketches rollback per task, writes `PLAN.md` (the lead's binding plan document) and appends to `EVIDENCE/planner.md`. It does NOT execute, interview, or dispatch.

### "Architect"

Three sources:

| Source | Role |
|---|---|
| `~/.claude/agents/architect.md` | General architectural advisor |
| `~/.claude/agents/architect-planner.md` | Plan authorship (absorbed above) |
| Convention in multi-agent lit (MetaGPT, ChatDev) | Role owning component design, API contracts, data model |

**Commit for engineering-architect**: **commits to design decisions that the planner left underspecified**. Data models, module boundaries, API surfaces, dependency choices. Reads PLAN.md and produces `EVIDENCE/architect.md` with the decisions. Does NOT write implementation code.

**Distinction from engineering-planner**: planner says "we need feature X composed of tasks T1-T5." Architect says "for T2, the data model is `{a: int, b: string}`, the API is `POST /x/y`, the dependency is library foo v2.3." Planner is about *decomposition*; architect is about *commitment*.

### "Executor"

Two sources:

| Source | Role | Model |
|---|---|---|
| `~/.claude/agents/executor.md` | Implementation executor. Edit/Write/Bash. Smallest viable diff. TodoWrite for 2+ steps. TDD optional. | `claude-sonnet-4-6` |
| Convention | "the one who writes code" | opus or sonnet depending on cost model |

**Commit for engineering-executor**: **writes code**. Uses Edit, Write, Bash. Makes atomic changes corresponding to one planner task. Records every change to `DIFF_LOG.md` AND `EVIDENCE/executor.md`. Does NOT make architectural decisions (escalates to architect), does NOT run final verification (delegates to verifier), does NOT review its own work (delegates to reviewer). **Upgrade from flat executor: `model: opus, effort: max`** because this is team-session work and the never-downgrade doctrine applies.

### "Verifier"

Two sources:

| Source | Role |
|---|---|
| `~/.claude/agents/verifier.md` | Evidence-based verification. "No approval without fresh evidence." Runs test suite, lsp_diagnostics, build. Issues PASS/FAIL/INCOMPLETE. |
| `~/.claude/agents/research/research-evaluator.md` | Quality-gate judge on research synthesis. 5-dim rubric. |

**Commit for engineering-verifier**: **runs tests and diagnostics, produces fresh evidence, issues PASS/FAIL**. Method inherits verbatim from flat `verifier.md` but upgraded to opus+max-effort and scoped to the current engineering session. Absorbs the `qa-tester.md` integration-probe lens and the test-execution part of `test-engineer.md`, but NOT test authorship — test authorship is the executor's job (following TDD discipline) unless the task explicitly requires a dedicated test-writing pass.

**Distinction from engineering-evaluator** (see below): verifier runs per-inner-iteration, quickly, with fresh test output. Evaluator runs ONCE at handback, judges the whole PLAN-vs-SHIPPED delta against the CHARTER acceptance criteria. Same as research's synthesist (per-round) vs evaluator (final gate) relationship.

### "Reviewer"

One source:

| Source | Role |
|---|---|
| `~/.claude/agents/code-reviewer.md` | Two-stage review (spec-compliance first, then code quality). Severity-rated feedback. Read-only (`disallowedTools: Write, Edit`). |

**Commit for engineering-reviewer**: **reads the DIFF_LOG + modified files, runs two-stage review, issues APPROVE/REQUEST_CHANGES/COMMENT per code-reviewer's method**. Inherits `disallowedTools: Write, Edit` to enforce read-only. Upgraded to opus+max-effort. Runs per-inner-iteration after verifier passes — "did the executor's changes meet spec AND match code quality standards."

### "Skeptic"

One source:

| Source | Role |
|---|---|
| `~/.claude/agents/research/research-skeptic.md` | Attacks reasoning. Competing hypotheses. Unstated assumptions. |

**Commit for engineering-skeptic**: **attacks the PLAN and the design decisions**. Reads PLAN.md + architect.md. Generates ≥ 2 competing implementation strategies. Asks "what if the plan is wrong?" Audits unstated assumptions (e.g. "the planner assumed library X is maintained — is it?"). Does NOT attack corpus — that's engineering-adversary's job.

**Distinction from engineering-reviewer**: reviewer reads SHIPPED CODE against spec. Skeptic reads PLAN against reality. Reviewer runs after executor; skeptic runs after planner (before executor).

### "Adversary"

One source:

| Source | Role |
|---|---|
| `~/.claude/agents/research/research-adversary.md` | Attacks corpus. SEO farms, citation-laundering, staleness, astroturfing. |

**Commit for engineering-adversary**: **attacks EXTERNAL INPUTS to the engineering session**. Specifically: (a) the research SYNTHESIS.md that CHARTER cites — is any claim in it REPORTED-NOT-VERIFIED? Does anything need empirical validation before the executor commits to it? (b) the library docs the architect is depending on — is the cited version current? Has the API changed? (c) the task spec itself — is it ambiguous? Internally contradictory? Out of date? (d) published benchmark numbers — are they reproducible?

**Distinction from engineering-skeptic**: skeptic asks "is the plan we wrote sound?" Adversary asks "are the inputs we're basing the plan on sound?" Orthogonal lenses, both mandatory on the plan-gate.

### "Moderator"

Inherited from `research-moderator.md` verbatim. Same 3-round debate protocol. Same 5 verdict types (`{A_WINS, B_WINS, COMPLEMENTARITY, REFRAME, DEFER}` — with REFRAME honored per MEMORY.md lesson 10). Runs on contradictions between engineering specialists (e.g. architect says "use library X," skeptic says "X is broken on platform Y, use Z").

### "Evaluator"

Inherited from `research-evaluator.md` with a **different rubric**. Research evaluator uses Anthropic's 5-dim (factual accuracy, citation accuracy, completeness, source quality, tool efficiency). Engineering evaluator needs an engineering-specific 5-dim rubric. Candidates:

1. **Functional correctness**: do the changes meet the acceptance criteria in PLAN.md?
2. **Test coverage**: does the shipped diff have adequate test evidence? (VERIFY_LOG.md shows tests passing with fresh output.)
3. **Diff minimality**: is the diff the smallest that achieves the behavior change, or did the executor over-engineer?
4. **Revert-safety**: can the diff be cleanly reverted? No schema drift, no partial migrations, no destructive data changes without reversible alternatives.
5. **Style conformance**: does the shipped code match the project's existing conventions?

Optional candidates for v1.1:
- Performance non-regression (hard to run on every session, reserved for special cases)
- Security posture (owned by security-reviewer, consulted by reviewer)

**Commit**: v1 evaluator uses **5 dimensions: functional correctness, test coverage, diff minimality, revert-safety, style conformance**. All 5 must clear a pass threshold for "ship" verdict.

### "Retrospector"

Inherited verbatim from `research-retrospector.md`. Writes lessons to `~/.claude/agent-memory/engineering-lead/MEMORY.md`. Lessons are about the engineering PROCESS, not about the code shipped. Same ACE generator/reflector/curator pattern.

### "Scribe"

Inherited from `research-scribe.md`. Normalizes evidence file formats, enforces citation schema, owns `INDEX.md` for engineering-team, dedupes MEMORY.md after retrospector writes. Additionally: owns `DIFF_LOG.md` and `VERIFY_LOG.md` schema enforcement (every line matches the format). Scribe is the only specialist with write access to INDEX.md.

### "Debugger"

One source:

| Source | Role |
|---|---|
| `~/.claude/agents/debugger.md` | Root-cause analysis, stack trace analysis, build/compilation error resolution. 3-failure circuit breaker. Minimal-diff bias. |

**Commit for engineering-debugger**: **runs when verifier fails**. Reads VERIFY_LOG.md to see which test/diagnostic/build command failed, then runs the flat debugger's method (reproduce → gather evidence → hypothesize → minimal-diff fix → 3-failure circuit breaker). Upgraded to opus+max. Does NOT fix root causes outside the current task's blast radius — escalates to architect if the root cause is in a dependency or an upstream module.

### "Lead"

The orchestrator role. Inherited in shape from `research-lead.md` but with engineering-specific workflow. Key distinction: engineering-lead owns `PLAN.md` (not `SYNTHESIS.md`), `CHARTER.md` (if cross-team), and the ownership of the Round 0 → Phase A (plan gates) → Phase B (build inner loop) → close sequencing.

## Terminology commitments (canonical for engineering-team)

| Term | Canonical meaning for engineering-team v1 |
|---|---|
| **CHARTER.md** | The binding input spec for an engineering session. Written by engineering-lead at Round 0. Cites research SYNTHESIS.md if cross-team. |
| **PLAN.md** | The lead-owned design document. Equivalent of research `SYNTHESIS.md`. Lives at the session root. |
| **DIFF_LOG.md** | Append-only log of every executor change. Schema: `<ISO-ts> <file>:<line-range> <type=new|edit|delete|move> — <one-line-reason>` |
| **VERIFY_LOG.md** | Append-only log of every verifier run. Schema: `<ISO-ts> <test-cmd> <exit-code> <pass/fail/skip counts> artifact=<path>` |
| **FEEDBACK_FROM_ENGINEERING.md** | Conditional file written when engineering disagrees with the research input. Lives in the engineering session workspace AND gets copied to the research session workspace at handback. |
| **Phase A** | Plan phase: intake → plan → architect → skeptic-gate → adversary-gate. Produces a committed PLAN.md. |
| **Phase B** | Build phase: inner ReAct loop (execute → verify → review, back-edge to architect on blocker, back-edge to planner on spec blocker). Closes when acceptance criteria pass or budget trips. |
| **inner iteration** | One executor → verifier → reviewer cycle inside Phase B. Atomic unit of work. |
| **plan-gate** | The phase boundary between Phase A and Phase B. Plan-skeptic + plan-adversary MUST pass. |
| **verify-gate** | The per-iteration gate inside Phase B. Verifier must PASS before reviewer runs. |
| **evaluator-gate** | The final gate before handback. Engineering-evaluator's 5-dim rubric must clear all 5 thresholds. |
| **handback** | Session close. Writes a handback file to the research session's workspace if cross-team. Writes lessons to engineering-lead/MEMORY.md. |
| **CHARTER input** | The research SYNTHESIS.md referenced in CHARTER.md, treated as binding spec. |
| **blast radius** | The maximum set of files/modules/behaviors a task can affect. Planner estimates per-task; architect validates. |
| **acceptance criteria** | Checkable conditions in CHARTER.md / PLAN.md that the evaluator grades against. |
| **rollback sketch** | Per-task note: "if this task fails verification, undo via <git revert <sha> OR manual Edit OR nothing-to-undo>". Planner writes; executor follows. |

## Hypothesis vocabulary audit

The HYPOTHESES.md defines H1 through H5. Each uses the words "flat," "hierarchical," "pipeline," "ReAct," "plan-and-execute," "phase," "workflow," "agent," "orchestrator-worker," "evaluator-optimizer." These are heavily overloaded. Quick commits:

- **flat** = all specialists report to one lead, no sub-leads. (Research-team is flat.)
- **hierarchical** = lead delegates to sub-leads who delegate to specialists. (Ruled out structurally.)
- **pipeline** = fixed-N ordered stages with a designated owner at each stage. (Rejected by H3 in favor of 2-phase.)
- **ReAct** = Reasoning + Acting interleaved via Thought/Action/Observation trace (Yao et al. 2022, arxiv 2210.03629). Dynamic, reactive, unfixed length.
- **Plan-and-Execute / Plan-and-Solve** = commit to a full plan first, execute the plan sequentially, optionally replan if stuck (Wang et al. 2023 "Plan-and-Solve Prompting" arxiv 2305.04091).
- **phase** = a bounded block of the session where a specific set of gates run. Not the same as a "round" (round is time-scoped, phase is purpose-scoped).
- **workflow** (Anthropic "Building effective agents") = LLM+tools with a fixed, scripted path.
- **agent** (Anthropic) = LLM+tools with a dynamic, self-directed path.
- **orchestrator-worker** = one orchestrator decomposes and dispatches to workers; workers return results.
- **evaluator-optimizer** = one agent does the work, a separate agent evaluates, the work agent retries until the evaluator accepts.

**Hypothesis rewording using committed vocabulary**:
- **H1 flat mirror**: flat roster, single-phase with fixed rounds like research-team.
- **H2 pipeline with inner ReAct**: fixed 6-stage pipeline, inner ReAct loop inside the "execute" stage.
- **H3 unified hybrid**: flat roster, 2-phase structure, Phase A is a bounded workflow (plan-and-execute for planning), Phase B is an evaluator-optimizer loop (executor + verifier iterates).
- **H4 pure ReAct**: flat roster, unbounded single-phase ReAct trajectory.
- **H5 two-team split**: ruled out.

**Observation**: H3 is **not actually "hybrid"** in the sense that makes it suspect. It's a clean composition: Anthropic's "orchestrator-worker" pattern for Phase A plus Anthropic's "evaluator-optimizer" pattern for Phase B. Both patterns are from the same "Building effective agents" post. The "hybrid" label in HYPOTHESES.md is misleading — the linguist's recommendation is to call H3 **"two-phase orchestrator + evaluator-optimizer"** when the synthesist writes the final claim matrix. This avoids the perception that it's a stapled-together Frankenstein.

## Polysemy flags for the synthesist

When the synthesist builds the claim matrix, watch for these likely false contradictions:

1. **"planner" meaning drift**: librarian/historian will cite Anthropic on orchestrator-worker's "planner" (meta-role) while the planner.md flat agent uses "planner" (interview-and-write). Synthesist: force the distinction.
2. **"verify" meaning drift**: verifier (per-iteration, test-execution) vs evaluator (final gate, rubric). Both are "verification" but at different scopes.
3. **"plan" meaning drift**: PLAN.md (document) vs "plan" (the mental model the team commits to) vs "plan-and-execute" (the academic pattern). Triple-overloaded. Synthesist: prefer PLAN.md for the document, "committed plan" for the commitment, "Plan-and-Solve prompting" for the academic citation.
4. **"agent" meaning drift**: Anthropic's "agent" (dynamic path) vs "agent" (any LLM-with-tools) vs "agent" (a team member). Synthesist: use "specialist" for team members consistently.
5. **"phase" vs "round"**: phase is purpose-scoped (Phase A plan, Phase B build), round is time-scoped (Round 0 intake, Round 1 wide opener). Research-team uses rounds; engineering-team uses phases. Don't mix.

## Confidence in this audit

**HIGH** — all vocabulary sources are directly readable (existing agent files, hypothesis file, research PROTOCOL), and the polysemy flags are concrete enough that the synthesist can act on them without further clarification.
