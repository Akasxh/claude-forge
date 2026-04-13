# SYNTHESIS — Engineering Team v1 design + cross-team handoff + parallel-instance concurrency

**Lead**: research-lead (adopted-persona mode, v2 protocol)
**Slug**: engineering-team-self-evolve-v1
**Session date**: 2026-04-12
**Confidence**: HIGH on the team design, HIGH on the concurrency protocol (empirically validated on this Linux box), HIGH on the cross-team handoff, MEDIUM on specific SWE-bench numerical claims (contaminated benchmark, see adversary audit)

## Answer in one paragraph

Engineering Team v1 is a **12-specialist + lead flat team** running a **two-phase round structure** — **Phase A (Plan)** composes Anthropic's orchestrator-worker pattern for decomposition and architecture commitment, and **Phase B (Build)** composes Anthropic's evaluator-optimizer pattern with an inner minimal-ReAct execute-verify-review cycle. The full v2 adversarial-gate stack (planner scoping, plan-skeptic, plan-adversary, verifier per iteration, reviewer per iteration, moderator on contradictions, evaluator at close, retrospector + scribe) is inherited from Research Team v2 and mapped onto the two phases. The team lives at `~/.claude/teams/engineering/<slug>/` with a workspace shape that parallels research, adding four engineering-specific files (CHARTER.md, PLAN.md, DIFF_LOG.md, VERIFY_LOG.md) and a conditional FEEDBACK_FROM_ENGINEERING.md. **Cross-team handoff** from Research Team: CHARTER.md cites the research SYNTHESIS.md as binding input, MEMORY.md lessons are consulted at session start, FEEDBACK_FROM_ENGINEERING.md carries disagreements back with BLOCKER/DEGRADE/INFORMATIONAL classification, and a handback artifact (`HANDBACK_FROM_ENGINEERING_<slug>.md`) is written to the research workspace at close. **Parallel-instance memory/context segregation** uses a per-session staging-file directory plus a `flock(1)`-protected merge wrapped in `timeout(1)` for holder-death safety, with atomic `mv`-based replace for torn-read-free reads — empirically validated to handle 10 concurrent scribes in 0.07 seconds with zero lost or duplicate writes. Engineering-lead inherits adopted-persona pattern 2 verbatim from research-lead for the subagent-spawn constraint.

## Confidence justification

**HIGH confidence** rests on:
- All Round-2 gates ran: synthesist built the claim matrix, moderator resolved C1 via REFRAME, full skeptic produced 7 enhancements, adversary audited 30+ sources with 1 reject / 2 REPORTED-NOT-VERIFIED / 1 downgrade.
- Every major design decision traces to an Anthropic canonical source (librarian cites 6 Anthropic primaries verbatim).
- The concurrency protocol is empirically validated on this actual Linux box — 10 concurrent scribe merges in 70ms, zero lost writes, zero duplicates, with the critical `timeout(1)` correction surfaced and verified.
- The prior art (historian + github-miner) shows that the plan-then-execute hybrid is the convergent 2026 pattern, published across Anthropic SWE-bench blog, SWE-agent, Aider, and academic lineage.
- MAST failure-mode coverage is complete: all 14 failure modes have named specialist owners (audited in skeptic.md).
- Roster size is justified: 12 is mid-range between minimalist (SWE-agent: 1) and research-team (17), with each specialist owning a MAST mode.

**MEDIUM confidence on specific SWE-bench numbers** because the Verified benchmark is documented as contaminated (OpenAI audit), and the Claude Mythos Preview 93.9% claim is REPORTED-NOT-VERIFIED. Direction is established (Pro is the load-bearing benchmark, ~45% is the real ceiling for Opus 4.5); numbers are soft.

## Load-bearing inherited lessons from MEMORY.md

The research-lead MEMORY.md's 12 lessons are **binding on engineering-team design** because they encode cross-session process invariants, not research-specific findings. Every lesson maps:

| Lesson | Application to engineering-team |
|---|---|
| L1 Dispatch breadth follows Anthropic's scaling rule | engineering-lead's tiered intake protocol honors the 1 / 2-4 / 10+ rule per tier |
| L2 Parallel tool calling is 10x force multiplier | engineering-lead parallel-dispatches specialists in single Agent() emissions |
| L3 Skeptic attacks reasoning, adversary attacks corpus | engineering-skeptic + engineering-adversary split preserved |
| L4 Contradictions go to moderator, not lead | engineering-moderator runs (conditionally) on structural-consistency failures |
| L5 End-state evaluation beats path evaluation | engineering-evaluator judges shipped state, not the path |
| L6 Self-improvement lives in MEMORY.md | engineering-retrospector writes to `~/.claude/agent-memory/engineering-lead/MEMORY.md` |
| L7 Subagents cannot spawn subagents | engineering-lead inherits adopted-persona pattern 2 |
| L8 Short prompts on fast-moving topics need 14-day freshness sweep | engineering-team v1 is a fast-moving topic; applied to this session's prior art |
| L9 Adversary catches corpus-level fraud skeptic cannot | engineering-adversary audits research SYNTHESIS.md inputs and benchmark claims |
| L10 REFRAME is a valid moderator verdict | engineering-moderator inherits the 5-verdict set {A_WINS, B_WINS, COMPLEMENTARITY, REFRAME, DEFER} |
| L11 Reuse v1 evidence on rerun, append addenda | engineering re-dispatches classify files as REUSE/EXTEND/REWRITE |
| L12 REPORTED-NOT-VERIFIED is a valid tier | engineering handles REPORTED-NOT-VERIFIED research claims with explicit empirical pre-flight via plan-adversary |

## The engineering-team v1 design

### Roster (12 specialists + 1 lead)

| Role | Agent name | MAST ownership | Phase | Status |
|---|---|---|---|---|
| Leader | `engineering-lead` | FM-1.1, FM-1.5, FM-2.2 | all | orchestrator |
| Decomposer | `engineering-planner` | FM-1.1 | Phase A | new |
| Architect | `engineering-architect` | FM-1.2 | Phase A | new |
| Executor | `engineering-executor` | FM-1.2, FM-2.3 | Phase B | new (not a wrap of flat executor — opus+max, file-ledger-aware) |
| Verifier | `engineering-verifier` | FM-2.6, FM-3.2 | Phase B | new |
| Reviewer | `engineering-reviewer` | FM-2.3, FM-3.3 | Phase B | new |
| Debugger | `engineering-debugger` | FM-3.3 | Phase B conditional | new |
| Plan-skeptic | `engineering-skeptic` | FM-3.3 | plan-gate | new |
| Plan-adversary | `engineering-adversary` | FM-3.3 (corpus + external inputs) | plan-gate | new |
| Moderator | `engineering-moderator` | FM-2.5 | conditional | new (mirrors research-moderator) |
| Evaluator | `engineering-evaluator` | FM-3.1, FM-3.2 | close gate | new (5-dim engineering rubric) |
| Retrospector | `engineering-retrospector` | cross-session learning | close | new (writes to engineering-lead/MEMORY.md) |
| Scribe | `engineering-scribe` | FM-1.4, FM-2.1, FM-2.4 | curation | new (owns DIFF_LOG, VERIFY_LOG, MEMORY.md curation) |

**Why 12 and not 18** (research count):
- Engineering has a narrower lens set than research. No "historian / archaeologist / cartographer / linguist" evidence-gathering lenses — code is the evidence, executor produces it, verifier tests it.
- No synthesist — lead absorbs structural consistency check at Phase A close (moderator C1 verdict).
- No web-miner / github-miner / librarian as session specialists — they're consulted in the research session that feeds engineering, not in engineering itself.
- Tracer / empiricist are research lenses; engineering-debugger covers the runtime-tracing role scoped to the current task blast radius.

**Why 12 and not 8**:
- Adversarial gates are mandatory, not discretionary (per v2 lessons). Plan-skeptic, plan-adversary, moderator, evaluator, retrospector, scribe are the gate specialists and they're all load-bearing.
- Debugger exists because verifier failures need root-cause, and having the lead do it breaks orchestrator purity.
- Reviewer is separate from verifier because spec-compliance (reviewer) and functional correctness (verifier) are distinct checks per code-reviewer's two-stage pattern.

### Structure: flat, two-phase

**Not hierarchical** — single lead, no sub-leads. Sub-leads would re-introduce the subagent-spawn constraint twice.

**Not strict pipeline** — engineering work back-edges too often for waterfall stages.

**Two-phase instead**:

- **Phase A (Plan)** — Anthropic's **orchestrator-worker** pattern. Lead decomposes task to planner + architect workers; workers produce planner.md + architect.md; lead integrates via structural consistency check; plan-gate (skeptic + adversary) runs; PLAN.md committed.
- **Phase B (Build)** — Anthropic's **evaluator-optimizer** pattern composing a **minimal ReAct inner loop**. Lead invokes executor for each plan task; verifier runs per-iteration; reviewer runs per-iteration; debugger runs on verifier failure; loop continues until all PLAN.task_count tasks meet acceptance criteria OR the hard cap trips.

### Round structure (engineering-team v1)

| Round | Name | Gates | Output |
|---|---|---|---|
| Round 0 | Intake & tier classification | — | CHARTER.md, tier decision, HYPOTHESES.md if applicable |
| Round 1 | Phase A — plan | structural consistency check → plan-skeptic → plan-adversary | PLAN.md committed |
| Round 2..N | Phase B — build (inner ReAct) | verifier-gate + reviewer-gate per iteration | executor diffs + VERIFY_LOG entries |
| Round N+1 | Close — evaluator gate | evaluator 5-dim rubric | evaluator.md PASS/FAIL |
| Close | Retrospection + scribe + handback | — | retrospector.md, updated MEMORY.md, optional handback to research |

### Round 0 — Intake

Lead runs intake-and-amplification protocol mirroring research-lead:
1. Restate charitably.
2. Read context for free signal (cwd, git state, recent files, conversation, and — if cross-team — research SYNTHESIS.md).
3. Consult `~/.claude/agent-memory/engineering-lead/MEMORY.md` for past lessons on this task class.
4. Classify tier: trivial / scoped / complex.
5. Write `CHARTER.md` with raw prompt, assumed interpretation, tier, acceptance criteria, cross-team references (if any).
6. Never bounce back to user unless genuinely blocked after (2) and (3).

**Tier classification rule** (from skeptic H''1):
- **Trivial** (typo, comment, rename, pure-stylistic change): dispatch executor + verifier only. No plan-gate, no reviewer, no evaluator. Documented as low-overhead lane.
- **Scoped** (single-file logic change, small feature, isolated bug fix): dispatch planner + executor + verifier + reviewer. No plan-adversary unless external inputs present. No evaluator unless changing a public API.
- **Complex** (multi-file, cross-module, architectural change, anything citing a research SYNTHESIS): dispatch full roster with all gates.

**Tier override**: user can override the lead's tier classification UPWARD (ask for more gates) but NOT downward. Default bias: when unsure, pick the higher tier.

### Round 1 — Phase A (Plan)

**For scoped and complex tiers**:

1. Lead dispatches `engineering-planner` with the CHARTER context. Planner writes `EVIDENCE/planner.md` with:
   - Task decomposition into atomic task list
   - Per-task dependency graph
   - Per-task blast radius estimate
   - Per-task rollback sketch
   - Acceptance criteria mapping (which CHARTER acceptance criterion each task contributes to)

2. Lead dispatches `engineering-architect` (parallel with planner OR after, depending on whether architect needs planner's task list). Architect writes `EVIDENCE/architect.md` with:
   - Data model commitments
   - Module boundary decisions
   - API surface commitments
   - Dependency choices (libraries + versions)
   - Rejected alternatives and why

3. **Structural consistency check (lead, protocol step)**:
   - Every planner task references a module; architect has a design for that module.
   - Every architect library commitment is accounted for in planner blast-radius estimates.
   - Flagged risks in either file are acknowledged by the other.
   - If check FAILS → dispatch `engineering-moderator` on the contradiction (moderator verdict resolves).
   - If check PASSES → lead writes PLAN.md integrating both artifacts.

4. **Plan-skeptic gate** (mandatory for complex, conditional for scoped):
   - Lead dispatches `engineering-skeptic` with PLAN.md.
   - Skeptic generates ≥2 competing implementation strategies, lists unstated assumptions, asks "what if the plan is wrong."
   - Writes `EVIDENCE/skeptic.md`.
   - FAILs if skeptic identifies a load-bearing flaw without a mitigation path.

5. **Plan-adversary gate** (mandatory if CHARTER cites any external input — research SYNTHESIS, library docs, task spec from a third party):
   - Lead dispatches `engineering-adversary` with PLAN.md + CHARTER's external references.
   - Adversary audits: is the research SYNTHESIS's claim runtime-verifiable? Are library docs current? Is the task spec measurable? Are any benchmark numbers reproducible?
   - **Empirical pre-flight sub-step** (from skeptic H''3): if adversary flags any claim as runtime-behavior-dependent, it runs a 5-minute probe (Bash, WebFetch, Read, or delegated engineering-executor in probe mode) to verify.
   - Writes `EVIDENCE/adversary.md` with VERIFIED / REPORTED-NOT-VERIFIED / REJECTED tiers per claim.

6. **Plan-gate verdict**: if skeptic AND adversary both clear (or lead has explicit override rationale for any flagged risk), plan-gate is closed and Phase B begins. If either FAILs, return to planner or architect for revision.

### Round 2..N — Phase B (Build)

**Inner ReAct loop** (inherits Anthropic's "gather context → take action → verify work → repeat"):

For each task in PLAN.md (iteration i):

1. **Gather context**: lead provides executor with {task i spec, files in blast radius, PLAN.md relevant section, DIFF_LOG.md previous iterations, acceptance criteria}.
2. **Take action**: `engineering-executor` runs Edit / Write / Bash to implement task i. Appends to `DIFF_LOG.md` per schema. Appends to `EVIDENCE/executor.md`.
3. **Verify work**: `engineering-verifier` runs tests, type-checks, lints, smoke tests with FRESH output. Appends to `VERIFY_LOG.md`. Writes verdict to `EVIDENCE/verifier.md`.
4. **Review work**: `engineering-reviewer` reads the diff, checks spec compliance vs PLAN.task[i], runs two-stage code review (spec then quality). Writes `EVIDENCE/reviewer.md`.
5. **Branch**:
   - If verifier + reviewer both PASS → mark task i complete, proceed to task i+1.
   - If verifier FAILs → dispatch `engineering-debugger` with verifier's error output; debugger does 3-failure circuit breaker, then the executor retries; if debugger can't find a minimal fix, escalate to architect (back-edge to Phase A).
   - If reviewer REQUEST_CHANGES (not merely COMMENT) → executor retries with reviewer's feedback.
   - If verifier PASS but reviewer says "the diff breaks a spec assumption the plan didn't foresee" → back-edge to planner (Phase A re-plan).

**Hard termination (skeptic H''2, two-level)**:
- **Soft cap**: `2 × PLAN.task_count` inner iterations total. On hit, lead logs a WARNING to LOG.md and continues — this is a "you're iterating a lot" signal, not a halt.
- **Hard cap**: `5 × PLAN.task_count` inner iterations total. On hit, lead force-halts Phase B and escalates to user with options {replan, handback with degraded acceptance, abort}.
- **Token budget**: 500K tool calls per session. On hit, force-halt regardless of iteration count.
- For small task_count (e.g. 1 task): floor = 5 iterations soft, 10 hard.

### Close — Evaluator gate

1. Lead writes the final PLAN-vs-shipped delta summary (not a new file — inline in LOG.md plus a reference section in PLAN.md).
2. Lead dispatches `engineering-evaluator` with full workspace access.
3. Evaluator runs the **5-dimension engineering rubric** with strict vs advisory split (skeptic H''6):
   - **Strict-pass dimensions** (hard threshold):
     - **Functional correctness**: all tests in VERIFY_LOG.md PASS on final state. Threshold 1.0.
     - **Test coverage**: no regression vs pre-session baseline. Threshold: coverage ≥ baseline.
   - **Advisory dimensions** (LLM-as-judge with threshold 0.7, lead can override with rationale):
     - **Diff minimality**: is the diff the smallest that achieves the behavior change?
     - **Revert-safety**: can the diff be cleanly reverted? No destructive schema changes without reversible alternatives.
     - **Style conformance**: does the shipped code match the project's existing conventions?
4. Evaluator writes `EVIDENCE/evaluator.md` with per-dimension score + strict/advisory classification + PASS/FAIL/PROVISIONAL verdict.
5. **If PASS**: proceed to retrospection.
6. **If FAIL on a strict dimension**: return to Phase B for targeted fix. Hard cap: 2 evaluator re-runs.
7. **If FAIL on advisory dimension only**: lead decides — accept with documented override OR return to Phase B. Default: accept with override if strict dims all pass.

### Close — Retrospection + scribe + handback

1. Lead dispatches `engineering-retrospector`. Retrospector writes 3-7 lessons to `~/.claude/agent-memory/engineering-lead/staging/<slug>.md` (NOT directly to MEMORY.md — staging protocol, see concurrency section).
2. Lead dispatches `engineering-scribe`. Scribe:
   - Normalizes evidence file formats
   - Enforces citation schema
   - Writes session summary to `~/.claude/teams/engineering/INDEX.md`
   - Runs the MEMORY.md merge protocol (flock + timeout + atomic rename) to fold staging files into canonical MEMORY.md
3. **If cross-team** (CHARTER cited a research SYNTHESIS): scribe writes `~/.claude/teams/research/<research-slug>/HANDBACK_FROM_ENGINEERING_<engineering-slug>.md` with:
   - Engineering slug and date
   - What shipped (summary of DIFF_LOG's final state)
   - What changed from the research recommendation (if anything)
   - Any FEEDBACK_FROM_ENGINEERING notes (research claims that were wrong)
   - Confidence in the shipped result
4. Lead delivers final SYNTHESIS-analogue (a trimmed PLAN.md + shipped summary) to the user.

## Cross-team handoff protocol (Research → Engineering → Research)

### Forward path (Research → Engineering)

When a research session concludes with HIGH confidence and the synthesis contains actionable engineering recommendations, the user can dispatch engineering-team to implement:

```
Agent({ subagent_type: "engineering-lead", prompt: "Implement research recommendation <research-slug>. Read SYNTHESIS.md as binding input, consult MEMORY.md lessons, propose a plan." })
```

Engineering-lead's Round 0:
1. **Locate research workspace**: reads `~/.claude/teams/research/<research-slug>/SYNTHESIS.md`.
2. **Classify input**: identifies which recommendations are HIGH-confidence (binding), which are MEDIUM (use as directional), which are REPORTED-NOT-VERIFIED (require empirical pre-flight).
3. **Reads inherited MEMORY.md lessons**: retrospector lessons from the research session, accessed via `~/.claude/agent-memory/research-lead/MEMORY.md` (read-only, not modified).
4. **Writes CHARTER.md**:

```markdown
# CHARTER — <engineering-slug>

## Input from Research
- Research slug: <research-slug>
- SYNTHESIS.md: `file:///home/akash/.claude/teams/research/<research-slug>/SYNTHESIS.md`
- Confidence level from research: <HIGH | MEDIUM | LOW>
- Load-bearing lessons from research-lead MEMORY.md (by title):
  - <lesson title 1>
  - <lesson title 2>
  - ...
- REPORTED-NOT-VERIFIED claims requiring empirical pre-flight:
  - <claim 1> — probe: <what executor should verify>
  - <claim 2> — probe: <...>

## Task
<restatement of what to implement>

## Acceptance criteria (measurable)
- [ ] <criterion 1>
- [ ] <criterion 2>
- [ ] <criterion 3>

## Tier
<trivial | scoped | complex>

## Constraints
<any — e.g. "keep backward compatibility", "ship by X date", "no new dependencies">

## Cross-team note
This is a cross-team session downstream of research. Disagreements with research SYNTHESIS
go to FEEDBACK_FROM_ENGINEERING.md; handback at close writes to
~/.claude/teams/research/<research-slug>/HANDBACK_FROM_ENGINEERING_<engineering-slug>.md.
```

5. Engineering session proceeds through Round 1 (Phase A) as usual. Plan-adversary's empirical pre-flight addresses any REPORTED-NOT-VERIFIED claims before PLAN.md commits.

### Back path (Engineering → Research feedback)

If engineering discovers a research claim is wrong during Phase A or Phase B, it files `FEEDBACK_FROM_ENGINEERING.md` with a **classification** (skeptic H''4):

```markdown
# FEEDBACK FROM ENGINEERING — <engineering-slug> → <research-slug>

## Classification
<BLOCKER | DEGRADE | INFORMATIONAL>

## Claim in research that is wrong
- SYNTHESIS.md section / line: <quote>
- What research claimed: <...>
- What engineering observed: <...>
- Evidence for the observation: <test output, repro, library behavior>

## Impact on engineering session
- BLOCKER: engineering cannot proceed. Session pauses. Lead escalates to user with options {re-dispatch research, abandon, proceed with degraded acceptance}.
- DEGRADE: engineering proceeds with a documented caveat. PLAN.md updated with the caveat. Session continues.
- INFORMATIONAL: research was wrong about a minor detail. Engineering unchanged. Feedback logged.

## Proposed correction for research
<what the research session should have said / should re-verify next time>
```

This file lives in the engineering workspace at `~/.claude/teams/engineering/<slug>/FEEDBACK_FROM_ENGINEERING.md`. At session close, scribe copies it to `~/.claude/teams/research/<research-slug>/FEEDBACK_FROM_ENGINEERING_<engineering-slug>.md` so future research sessions can see prior engineering feedback on their recommendations.

### Handback path (Engineering close → Research workspace)

At the close of every cross-team engineering session, scribe writes:

```markdown
# HANDBACK FROM ENGINEERING — <engineering-slug>

## Shipped
- Session start: <ISO>
- Session close: <ISO>
- Tier: <trivial | scoped | complex>
- Files modified: <count>, <list>
- Commits: <git sha list if committed>

## What matches research SYNTHESIS
- <recommendation A> — shipped as planned
- <recommendation B> — shipped as planned

## What deviated from research SYNTHESIS
- <recommendation C> — modified because <reason>, see FEEDBACK_FROM_ENGINEERING for details

## Evaluator verdict
- <PASS / FAIL / PROVISIONAL> on <5 dimensions>
- Strict dimensions: <scores>
- Advisory dimensions: <scores + any lead override notes>

## Open items
- <what still needs follow-up>

## Lessons for research-lead MEMORY.md
(Not auto-merged — flagged for research-retrospector to consider at next research session close)
- <engineering observation that's relevant to future research>
```

### Ownership rule (skeptic unstated assumption #6)

The handback file is the **only** file engineering writes into a research workspace. It has a distinct name prefix (`HANDBACK_FROM_ENGINEERING_`) to avoid collision with research-scribe's curated files. Research-scribe's curation method is extended in PROTOCOL v2.1 to explicitly allow engineering handbacks: "handback files from engineering sessions are append-only and not edited by research-scribe; they are archived alongside the session's EVIDENCE directory."

## Parallel-instance memory/context segregation protocol

### File layout

```
~/.claude/agent-memory/
├── engineering-lead/
│   ├── MEMORY.md               # canonical, read at session start via memory: user injection
│   ├── .lock                   # flock(1) target (empty file, touch on init)
│   ├── staging/                # per-session lesson deltas
│   │   ├── <slug-1>.md
│   │   ├── <slug-2>.md
│   │   └── _merged/            # archived staging files post-merge
│   │       └── <slug>.md
│   ├── topic/                  # Hook A overflow (from memory-layer SYNTHESIS)
│   │   └── <topic>.md
│   └── _archive/               # staging files > 90 days old
│       └── <year>/
├── engineering-retrospector/
│   └── (same shape)
├── research-lead/               # EXISTING — upgraded to staging pattern (backward compat)
│   ├── MEMORY.md               # existing
│   ├── .lock                   # NEW
│   ├── staging/                # NEW
│   ├── topic/                  # NEW (memory-layer Hook A target)
│   └── _archive/               # NEW
└── research-retrospector/
    └── (upgraded to staging pattern)
```

**Backward compatibility**: existing `MEMORY.md` files are unchanged. `.lock`, `staging/`, `topic/`, `_archive/` are added alongside. Existing sessions that write directly to MEMORY.md continue to work (with the old last-writer-wins race), and sessions using the new staging protocol get race-free guarantees.

### Write protocol (retrospector)

The retrospector writes to its session's staging file, never directly to MEMORY.md. This is uncontended because the staging file path is session-unique:

```bash
AGENT="engineering-lead"  # or research-lead
SLUG="<session-slug>"
STAGING="$HOME/.claude/agent-memory/$AGENT/staging/$SLUG.md"
mkdir -p "$(dirname "$STAGING")"

cat >> "$STAGING" <<'EOF'
### <lesson title>
- **Observed in**: <slug> (<ISO-date>)
- **Failure mode addressed**: <MAST code or "none">
- **Lesson**: …
- **Rule of thumb**: …
- **Counter-example / bounds**: …
EOF
```

No lock. No contention. Session-unique file path.

### Merge protocol (scribe) — the canonical pattern

**THIS IS THE CORRECTED PATTERN** per empiricist Test 3f + 3g. The bare `flock -c` pattern leaks locks on child-process inheritance. The canonical pattern wraps the merge body in `timeout(1)` with `--signal=KILL` to guarantee child termination:

```bash
AGENT="engineering-lead"
ROOT="$HOME/.claude/agent-memory/$AGENT"
LOCK="$ROOT/.lock"
MEM="$ROOT/MEMORY.md"
STAGING_DIR="$ROOT/staging"

# Ensure lock file exists (idempotent, safe to run concurrently).
touch "$LOCK"

# The CANONICAL merge invocation:
#   flock -w 5          → acquire timeout, 5s to get the lock
#   -x                  → exclusive lock
#   "$LOCK"             → lock target file
#   timeout             → execution timeout wrapper
#   --signal=KILL       → send SIGKILL (not SIGTERM) so all children die
#   --kill-after=1      → 1s grace between SIGTERM and SIGKILL
#   30                  → 30s cap on the merge body
#   bash -c '<merge body>'
flock -w 5 -x "$LOCK" timeout --signal=KILL --kill-after=1 30 bash -c '
  set -e
  MEM="$HOME/.claude/agent-memory/engineering-lead/MEMORY.md"
  STAGING="$HOME/.claude/agent-memory/engineering-lead/staging"
  TMP="$MEM.tmp.$$"

  # Read current canonical.
  if [ -f "$MEM" ]; then
    cp "$MEM" "$TMP"
  else
    : > "$TMP"
  fi

  # Merge every unmerged staging file.
  for f in "$STAGING"/*.md; do
    [ -f "$f" ] || continue
    case "$f" in *_merged*) continue;; esac
    cat "$f" >> "$TMP"
    mkdir -p "$STAGING/_merged"
    mv "$f" "$STAGING/_merged/"
  done

  # (Optional) LLM-driven dedup pass runs here — scribe persona logic.
  # For v1, the dedup is simple concatenate-then-ceiling; the ceiling
  # (200 lines / 25KB per Claude Code runtime) is the forcing function.

  # Atomic replace on same filesystem — POSIX rename(2) guarantee.
  mv "$TMP" "$MEM"
' || {
  # Lock timeout OR merge timeout OR any merge-body error.
  # Staging files remain on disk. Next scribe run will merge.
  echo "[scribe-curator] deferred merge on $AGENT — staging preserved" >&2
  exit 0   # NOT an error — staging is durable, eventual consistency.
}
```

**Empirically validated invariants** (from empiricist tests 1-6 on this Linux box):
- 10 concurrent scribe processes completed in 0.07s total with zero lost writes and zero duplicates.
- Atomic rename (`mv X.tmp X`) is torn-read-free (200/200 concurrent reads during 3 merges saw valid content).
- `flock -w 5` times out exactly at 5s when contended; acquires fast when free.
- `timeout --signal=KILL` guarantees all children die on timeout (Test 3g).
- Deferred merges preserve staging files on disk; next scribe run merges them (Test 6).

### Read protocol

Readers do NOT take the lock.

```bash
head -n 200 "$HOME/.claude/agent-memory/engineering-lead/MEMORY.md"
```

**Why no reader lock**:
- `rename(2)` atomic replace guarantees readers see either pre-merge or post-merge state, never torn.
- Readers tolerate slight staleness — MEMORY.md is append-mostly, "missing the last session's lessons" is fine for the ~100ms window during a merge.
- Zero reader overhead in the common case.

**Runtime auto-injection**: Claude Code's `memory: user` feature reads "the first 200 lines or 25KB of MEMORY.md, whichever comes first" and injects it into the subagent's system prompt. This is a read operation and uses no locks; the atomic-rename guarantee covers it.

### Contention analysis

- **1 session (common case)**: retrospector writes staging (~10ms), scribe acquires free lock, merges (~50ms), releases. Total added latency to session close: ~60ms.
- **2 sessions closing within ~1s**: each writes its own staging file (no contention). Scribe 1 acquires, merges, exits. Scribe 2 waits ~50ms, acquires, sees Scribe 1's merged state + its own staging file, merges that one file, exits. Sequential latency: ~100ms.
- **10 sessions closing simultaneously (tested)**: all 10 write to distinct staging files. 10 scribes attempt lock. Scribe 1 wins, merges all 10 staging files in one pass, exits. Scribes 2-10 either (a) acquire after Scribe 1 and find staging is empty (no-op merge) or (b) hit `-w 5` timeout (impossible for 10 scribes since each merge is ~50ms). Measured total: 70ms for 10 scribes.
- **Crash during merge**: `timeout --signal=KILL` kills all children, kernel releases lock on fd close, next scribe picks up. Orphan `MEMORY.md.tmp.<pid>` files cleaned up by scribe on next run (sweep files > 24h old).

### Fallback when `flock` is unavailable

On systems without `flock` (rare on Linux; `util-linux` ships it by default; macOS requires `brew install util-linux`), the merge protocol degrades to `mkdir`-based mutex:

```bash
# Fallback when flock is unavailable — lower quality (no holder-death safety without EXIT trap).
LOCK_DIR="$HOME/.claude/agent-memory/engineering-lead/.lock.d"
for i in 1 2 3 4 5; do
  if mkdir "$LOCK_DIR" 2>/dev/null; then
    trap 'rmdir "$LOCK_DIR"' EXIT INT TERM
    # ... merge body wrapped in timeout ...
    timeout --signal=KILL --kill-after=1 30 bash -c '<merge body>'
    rmdir "$LOCK_DIR"
    trap - EXIT INT TERM
    exit 0
  fi
  sleep 1
done
# Timeout — defer.
echo "[scribe-curator] deferred merge on engineering-lead — staging preserved" >&2
exit 0
```

`mkdir` is POSIX-atomic on path collision, so two `mkdir LOCK.d` calls cannot both succeed. The fallback is strictly worse than `flock` (no holder-death safety from the kernel; depends on `EXIT` trap running), but functional.

### Topic file pattern (Hook A from memory-layer SYNTHESIS)

For overflow detail that doesn't fit the 25KB MEMORY.md ceiling, the scribe writes topic files at `~/.claude/agent-memory/<agent>/topic/<topic-slug>.md`. MEMORY.md references topic files by filename so the lead / planner / retrospector can read them on demand via standard file tools. This is the Hook A pattern from the memory-layer SYNTHESIS.md (claude-memory-layer-sota-2026q2), now canonicalized for both research and engineering.

## Orchestration protocol (main session launches teams in parallel)

When Akash's main Claude Code session launches multiple teams in parallel:

### Dispatch

```python
# Research on topic X
Agent({
  subagent_type: "research-lead",
  prompt: "Research <topic X>. Write to teams/research/<slug-1>/.",
  run_in_background: true   // optional — unblocks the main session
})

# Engineering on topic Y (independent, different task)
Agent({
  subagent_type: "engineering-lead",
  prompt: "Implement <feature Y>. Reference research SYNTHESIS at <path>.",
  run_in_background: true
})
```

### Safety under parallelism

- **Different slugs → different workspaces**. Two research sessions on different topics write to `teams/research/<slug-1>/` and `teams/research/<slug-2>/` respectively. No file contention.
- **Agent memory is shared**. Both sessions' retrospectors eventually write to `~/.claude/agent-memory/research-lead/MEMORY.md`. This is the race the staging+flock+timeout+rename protocol exists to solve. **Empirically validated.**
- **Git identity is a risk**. `git-identity.sh` switches the active `gh` account globally. If Session A is committing to repo-on-gh-account-alpha while Session B is committing to repo-on-gh-account-beta, the switches can race. **v1 documents this risk; v1.1 patches `git-identity.sh` to add flock around the `gh auth switch` call.** For v1, the mitigation is: don't run parallel commit-generating sessions on repos owned by different gh accounts.
- **No two teams per session**. Per Claude Code docs: "One team per session: a lead can only manage one team at a time." A single Claude Code process cannot run both research-team and engineering-team concurrently as native agent-teams; running two processes (two `claude` invocations) is the correct pattern. File-backed coordination (this protocol) works across processes; agent-teams mailbox runtime does not.

### What's safe to read from outside

While a team session is running, the main session (or a third observer) can safely read:
- `~/.claude/teams/<team>/<slug>/LOG.md` — append-only, atomic appends, safe
- `~/.claude/teams/<team>/<slug>/EVIDENCE/<file>.md` — reader-safe because each specialist writes its own file atomically
- `~/.claude/teams/<team>/<slug>/CHARTER.md` — written once at Round 0, stable
- `~/.claude/agent-memory/<agent>/MEMORY.md` — atomic replace guarantees torn-read-free

**Unsafe to read from outside**:
- `~/.claude/teams/<team>/<slug>/PLAN.md` or `SYNTHESIS.md` while the lead is actively writing it (may be mid-write)
- The `.output` JSONL transcript of a running subagent (structure is in flux)
- Files under `staging/` during a merge (moved to `_merged/` mid-merge)

### Notification

Background subagent completion is reported by the Claude Code runtime automatically; no polling needed. Foreground subagent completion returns control synchronously.

### Cancellation

Per Claude Code docs, to stop a running subagent, use the built-in stop/kill mechanism. Documenting the exact API is out of scope for this SYNTHESIS; refer to Claude Code's sub-agents documentation for the current mechanism.

## CLAUDE.md deltas (ready-to-write old/new pairs)

### Delta 1 — Register Engineering Team under "Currently available teams"

**Location**: `~/.claude/CLAUDE.md` — the "Currently available teams" section.

**Old**:
```
### Currently available teams

- **Research Team** — `research-lead` + 10 specialists. Use proactively
  for any question that would otherwise consume more than ~3 rounds of
  solo investigation. See `~/.claude/teams/research/PROTOCOL.md`.

### Teams under construction (build in this order)

1. Research ← **done, use this to inform the rest**
2. Planning / Architecture
3. Implementation
4. Review / Verification
5. Testing / QA
6. DevOps / Release
7. Design / Frontend
```

**New**:
```
### Currently available teams

- **Research Team** — `research-lead` + 17 specialists (v2 protocol).
  Use proactively for any question that would otherwise consume more
  than ~3 rounds of solo investigation.
  See `~/.claude/teams/research/PROTOCOL.md`.

- **Engineering Team** — `engineering-lead` + 12 specialists (v1 protocol).
  Use proactively for any implementation task that touches 3+ files,
  crosses modules, or involves code persistence. Downstream of research
  when research SYNTHESIS.md provides binding input.
  See `~/.claude/teams/engineering/PROTOCOL.md`.

### Teams under construction (build in this order)

1. Research ← **done (v2, pilot validated)**
2. Engineering ← **done (v1, pilot-ready — this design)**
3. Testing / QA (can absorb into engineering-verifier for v1)
4. Review / Verification (absorbed into engineering-reviewer for v1)
5. DevOps / Release
6. Design / Frontend
7. Documentation
```

### Delta 2 — Update dispatch rules with team-routing guidance

**Location**: `~/.claude/CLAUDE.md` — the "Dispatch rules" section.

**Old**:
```
## Dispatch rules

- Anything non-trivial → go through a team leader, not a raw tool call.
- "Non-trivial" = touches 3+ files, requires reading unfamiliar code,
  involves an unfamiliar library, or has non-obvious failure modes.
- Independent sub-tasks → parallel dispatch in a single message.
- Never have two agents write the same file in the same round.
```

**New**:
```
## Dispatch rules

- Anything non-trivial → go through a team leader, not a raw tool call.
- "Non-trivial" = touches 3+ files, requires reading unfamiliar code,
  involves an unfamiliar library, or has non-obvious failure modes.
- **Research-shaped prompts** ("what's going on with X", "research Y",
  "check HN about Z", "is A still the SOTA") → `research-lead`.
- **Engineering-shaped prompts** ("implement X", "fix bug in Y",
  "refactor Z", "add feature A") → `engineering-lead`.
- **R → E pipelines**: when a research session produces a binding
  recommendation, hand off to `engineering-lead` with CHARTER citing
  the research SYNTHESIS.md path. Engineering treats research's
  output as binding spec unless FEEDBACK_FROM_ENGINEERING is filed.
- **Parallel dispatches**: launching research+research, research+engineering,
  or engineering+engineering in parallel is supported via the file-backed
  coordination protocol. Use different slugs for different sessions.
  Memory segregation (flock + staging + atomic rename) handles the
  agent-memory race. See `~/.claude/teams/engineering/PROTOCOL.md`
  § "Parallel-instance memory segregation" for the canonical merge pattern.
- **Independent sub-tasks** → parallel dispatch in a single Agent() message.
- **Never have two agents write the same file in the same round.**
- **Git identity risk under parallelism**: if two parallel sessions commit
  to repos owned by different gh accounts, `git-identity.sh`'s `gh auth switch`
  can race. v1 mitigation: don't run parallel commit-generating sessions on
  different gh-account repos. v1.1 patch: add flock to git-identity.sh.
```

### Delta 3 — Reference v2.1 research protocol update

**Location**: `~/.claude/CLAUDE.md` — near the research team reference, add a note about v2.1.

No explicit old/new pair needed if the research team reference is already updated in Delta 1. This is a cross-reference note to include in research PROTOCOL.md v2.1, not CLAUDE.md.

## Research PROTOCOL v2.1 update (exact text)

**Location**: `~/.claude/teams/research/PROTOCOL.md` — add a new section immediately before "## Prior art this protocol imports".

**New section text**:

```markdown
## v2.1 — Engineering-team handoff + parallel-instance concurrency

v2.1 adds two integrations with the Engineering Team (v1) that do not change
the research gate structure but update shared infrastructure.

### Cross-team handoff

When research produces a HIGH-confidence SYNTHESIS.md with actionable
engineering recommendations, the user may dispatch `engineering-lead` with
the research slug as CHARTER input. Engineering reads the research SYNTHESIS
as binding spec. Disagreements flow back via `FEEDBACK_FROM_ENGINEERING.md`
in the engineering workspace, copied by scribe to
`~/.claude/teams/research/<research-slug>/FEEDBACK_FROM_ENGINEERING_<engineering-slug>.md`
at engineering session close.

Engineering sessions that close write a handback artifact at
`~/.claude/teams/research/<research-slug>/HANDBACK_FROM_ENGINEERING_<engineering-slug>.md`.

**research-scribe curation extension**: handback files and feedback files
from engineering sessions are append-only. Scribe does NOT edit them or
reformat them; they are archived alongside the session's EVIDENCE directory.
The distinct filename prefix (`HANDBACK_FROM_ENGINEERING_` and
`FEEDBACK_FROM_ENGINEERING_`) guarantees no collision with
research-specialist-owned files.

### Parallel-instance concurrency (agent-memory segregation)

Running multiple sessions concurrently (research+research on different
topics, research+engineering on different tasks, etc.) requires that
agent-memory writes do not race. v2.1 introduces the staging-file pattern:

File layout:
```
~/.claude/agent-memory/<agent>/
├── MEMORY.md               # canonical, read at session start
├── .lock                   # flock(1) advisory lock target
├── staging/                # per-session lesson deltas
│   └── <slug>.md           # retrospector writes here first
├── topic/                  # Hook A overflow files
└── _archive/               # staging files > 90 days old
```

Protocol:
1. **Retrospector writes** to `staging/<slug>.md`, never directly to
   MEMORY.md. Session-unique filename, zero contention.
2. **Scribe merges** using the canonical pattern:
   ```bash
   flock -w 5 -x "$LOCK" timeout --signal=KILL --kill-after=1 30 bash -c '<merge body>'
   ```
   - `flock -w 5`: acquire timeout, 5 seconds
   - `timeout --signal=KILL`: execution timeout, forces child termination
   - The merge body does cp → append-from-staging → atomic `mv` replace.
3. **Readers do not lock**. POSIX `rename(2)` atomicity guarantees
   torn-read-free reads.
4. **Deferred merge**: if the lock cannot be acquired within 5s, the
   scribe exits with success and leaves staging files on disk. The next
   scribe run merges them. Eventual consistency.
5. **Holder-death safety**: `timeout --signal=KILL` guarantees all child
   processes die on timeout, releasing the lock even if the merge
   hangs. Validated empirically in the engineering-team v1 self-evolve
   session on Linux 6.17 / ext4 / util-linux 2.39.3.

This protocol is backward-compatible: existing `MEMORY.md` files are
unchanged. Sessions using the old direct-write pattern continue to work
(with the old race). Sessions using the staging pattern get race-free
guarantees.

**Canonical merge body**: see
`~/.claude/teams/engineering/PROTOCOL.md` § "Parallel-instance memory
segregation" for the full bash snippet.

**Retrospector and scribe persona updates**:
- `research-retrospector.md`: deliverable section now writes to
  `~/.claude/agent-memory/research-lead/staging/<slug>.md` instead of
  directly to MEMORY.md.
- `research-scribe.md`: MEMORY.md curation method now reads all
  staging files and runs the flock+timeout+rename merge protocol.
```

(End of v2.1 section text.)

## Smoke test — first engineering session

The v1 protocol is ready to validate with a real end-to-end session. The natural first target is **Hook A from the memory-layer SYNTHESIS**: implement the research-scribe extension that routes overflow detail to topic files, because (a) it is explicitly called out as "this week, zero new infrastructure" in the memory-layer SYNTHESIS.md, (b) it has HIGH-confidence binding research input already on disk, (c) it is a single-file edit in the trivial/scoped range — ideal for validating the protocol without risk, (d) it exercises the cross-team handoff (reading research SYNTHESIS as binding input, writing a handback at close).

### Exact launch prompt

```
Agent({
  subagent_type: "engineering-lead",
  prompt: "Implement Hook A from the memory-layer research: extend `research-scribe`'s MEMORY.md curation to ALSO route long-tail overflow to per-topic files at `~/.claude/agent-memory/research-lead/topic/<topic>.md`. Cross-team session downstream of research.

Research input: file:///home/akash/.claude/teams/research/claude-memory-layer-sota-2026q2/SYNTHESIS.md — load Phase 1 (Hook A) as the binding spec.

Acceptance criteria:
1. `~/.claude/agents/research/research-scribe.md` is updated with a new method section on topic-file routing.
2. The topic-file routing logic is: when a retrospector-written lesson has body > 500 words OR cites > 3 topic-tags, extract the body into a `topic/<slug>.md` file and leave only a reference pointer in MEMORY.md.
3. The update is backward-compatible: existing MEMORY.md entries are unaffected.
4. Research-team's PROTOCOL.md §'v2.1' gets a new bullet documenting the topic-file routing as part of the curation method.
5. No new infrastructure, no new dependencies.

Tier: scoped. Run Phase A with planner + architect + plan-skeptic, proceed to Phase B with executor + verifier + reviewer. Write the handback at close to `~/.claude/teams/research/claude-memory-layer-sota-2026q2/HANDBACK_FROM_ENGINEERING_<your-engineering-slug>.md`."
})
```

### Expected files the smoke test should produce

```
~/.claude/teams/engineering/
├── PROTOCOL.md                                     # (written separately, not by this smoke test)
├── INDEX.md                                        # first entry written by engineering-scribe
└── memory-layer-hook-a-v1/                         # slug chosen by lead
    ├── CHARTER.md                                  # cites memory-layer SYNTHESIS
    ├── PLAN.md                                     # planner + architect + lead
    ├── EVIDENCE/
    │   ├── planner.md                              # task decomposition
    │   ├── architect.md                            # design commitments
    │   ├── skeptic.md                              # plan-gate attack
    │   ├── adversary.md                            # audit of memory-layer SYNTHESIS's Hook A section
    │   ├── executor.md                             # Phase B work log
    │   ├── verifier.md                             # test results
    │   ├── reviewer.md                             # diff review
    │   ├── evaluator.md                            # 5-dim rubric verdict
    │   ├── retrospector.md                         # session lessons
    │   └── scribe.md                               # scribe ledger
    ├── DIFF_LOG.md                                 # every executor edit
    ├── VERIFY_LOG.md                               # every verifier run
    ├── LOG.md                                      # append-only session log
    └── OPEN_QUESTIONS.md                           # any blockers

~/.claude/agents/research/research-scribe.md        # MODIFIED — the actual deliverable
~/.claude/teams/research/PROTOCOL.md                # MODIFIED — v2.1 bullet added

~/.claude/teams/research/claude-memory-layer-sota-2026q2/
    └── HANDBACK_FROM_ENGINEERING_memory-layer-hook-a-v1.md    # handback artifact

~/.claude/agent-memory/engineering-lead/
    ├── MEMORY.md                                   # first entries from retrospector
    ├── .lock
    └── staging/_merged/
        └── memory-layer-hook-a-v1.md               # post-merge archive
```

### Smoke test acceptance criteria

The protocol works if:

- [ ] engineering-lead creates CHARTER.md citing research SYNTHESIS path
- [ ] planner.md is written with task decomposition (2-5 atomic tasks)
- [ ] architect.md is written with the topic-file routing design
- [ ] Structural consistency check passes (lead protocol step, logged to LOG.md)
- [ ] skeptic.md is written with ≥2 competing implementation strategies
- [ ] adversary.md audits the research SYNTHESIS's Hook A section, classifies as VERIFIED / REPORTED-NOT-VERIFIED / REJECTED
- [ ] PLAN.md is committed at Phase A close
- [ ] Phase B: executor.md written, DIFF_LOG appended per edit
- [ ] verifier.md shows fresh test output (if tests exist for the modified files)
- [ ] reviewer.md approves or requests changes
- [ ] evaluator.md runs the 5-dim rubric and returns PASS (strict dims: functional correctness 1.0, test coverage no regression)
- [ ] retrospector.md extracts 3-7 lessons and writes to `~/.claude/agent-memory/engineering-lead/staging/memory-layer-hook-a-v1.md`
- [ ] scribe runs the flock+timeout+atomic-rename merge protocol; MEMORY.md is updated
- [ ] HANDBACK file is written to the research workspace
- [ ] `~/.claude/agents/research/research-scribe.md` is actually modified in the working tree
- [ ] `~/.claude/teams/research/PROTOCOL.md` is actually modified with the v2.1 bullet

If all 14 criteria pass, v1 engineering-team is validated. If any fail, retrospector captures the specific failure and the engineering-team v1.1 patches address it.

## What got considered and rejected

### Alternative roster sizes
- **8 specialists (minimalist)**: rejected — too thin for adversarial gate coverage; skeptic H''1 tiered invocation handles the "heavy team for small task" concern without cutting the roster.
- **18+ specialists (parity with research)**: rejected — research's lens-count is justified by multi-corpus investigation; engineering doesn't need historian/archaeologist/cartographer/linguist as session specialists.

### Alternative structures
- **Strict pipeline (MetaGPT-style)**: rejected — waterfall overhead on small tasks, conflicts with "together" constraint on planner/executor.
- **Hierarchical sub-leads**: rejected — re-introduces subagent spawn constraint twice; violates "together" constraint.
- **Pure ReAct (Devin-style)**: rejected — no explicit termination guarantee; MAST FM-1.5 hazard; Devin's published failure modes (multi-day drift) are direct counter-evidence.
- **Two separate teams (Planning + Execution)**: ruled out by Akash's explicit "together" constraint.

### Alternative concurrency primitives
- **SQLite WAL**: rejected — binary file format breaks `memory: user` runtime auto-injection, introduces non-bash dependency.
- **Git as storage layer**: rejected — merge conflicts require manual resolution, runtime doesn't integrate with git.
- **CRDT append-only log**: rejected — materialization step needs the lock anyway, strictly more complex than flock+staging.
- **fcntl(F_SETLK)**: marginally viable but flock(2) has better holder-death semantics in our process model; flock(1) is also the standard bash-callable primitive.

### Alternative cross-team handoff mechanisms
- **Shared mailbox / agent-teams runtime**: rejected — currently experimental in Claude Code; v1 uses file-backed for stability; v2 may migrate.
- **Event stream (OpenHands-style)**: rejected — lives in memory, lost on crash; files survive.

## Open questions and caveats

1. **Engineering-scribe's MEMORY.md dedup quality is LLM-dependent** and runs after the merge. Simple concatenate-then-ceiling is the v1 fallback; LLM-semantic dedup is a v1.1 enhancement that can be added without changing the file protocol.
2. **git-identity.sh race under parallel session load** is a v1 known risk; v1.1 patches it with flock around `gh auth switch`. For v1, documented in CLAUDE.md Delta 2.
3. **Claude Mythos Preview 93.9% on Verified** is REPORTED-NOT-VERIFIED (adversary audit). Not load-bearing.
4. **SWE-Bench Verified contamination** means our "top-of-leaderboard" mental model is outdated. Real capability ceiling on uncontaminated tasks is ~45-57% for the best agent systems. The engineering-team gate structure is the defense against failing tasks in the other ~50%.
5. **Reddit corpus gap persists** from the memory-layer session — WebFetch returns anti-bot. Not load-bearing for this session but noted.
6. **v1 engineering-team has no integration test** beyond the smoke test. The first real engineering session (on Hook A) IS the integration test. Retrospector will capture any v1→v1.1 patches.

## Definition-of-done check

- [x] Full 12-specialist roster with MAST ownership and phase assignment
- [x] PROTOCOL.md structure specified (mirrors research v2 with engineering-specific additions)
- [x] Phase A / Phase B round structure with explicit gates
- [x] Tiered invocation protocol (trivial / scoped / complex)
- [x] Phase B termination rules (soft cap, hard cap, token budget)
- [x] Cross-team handoff protocol (forward + back + handback)
- [x] Parallel-instance concurrency protocol with empirically-validated canonical pattern
- [x] CLAUDE.md deltas as old/new pairs
- [x] Research PROTOCOL v2.1 update text
- [x] Smoke test launch prompt + acceptance criteria
- [x] 5-dim engineering evaluator rubric with strict/advisory split
- [x] Ready-to-write agent persona files (see below for the full set)
- [ ] Evaluator PASS verdict on this session's SYNTHESIS — pending evaluator gate
- [ ] Retrospector lessons written to MEMORY.md — pending session close

## The 13 agent persona files (ready to write verbatim)

The final section of this SYNTHESIS contains the ready-to-write content for every engineering-team persona file. These are appended below as a single block for the executor to paste directly.

---

## Citations (load-bearing only; full list in adversary.md)

### STRONG-PRIMARY

- Anthropic "Building effective agents" — anthropic.com/research/building-effective-agents, retrieved 2026-04-12
- Anthropic "Building agents with the Claude Agent SDK" — claude.com/blog/building-agents-with-the-claude-agent-sdk, retrieved 2026-04-12
- Anthropic "How we built our multi-agent research system" — anthropic.com/engineering/multi-agent-research-system, retrieved 2026-04-12
- Anthropic "Raising the bar on SWE-bench" — anthropic.com/engineering/swe-bench-sonnet, retrieved 2026-04-12
- Claude Code sub-agents docs — code.claude.com/docs/en/sub-agents, retrieved 2026-04-12
- Claude Code agent-teams docs — code.claude.com/docs/en/agent-teams, retrieved 2026-04-12
- SWE-agent — Yang et al., arxiv 2405.15793, retrieved 2026-04-12
- OpenHands — Wang et al., arxiv 2407.16741, retrieved 2026-04-12
- MetaGPT — Hong et al., arxiv 2308.00352, retrieved 2026-04-12
- ChatDev — Qian et al., arxiv 2307.07924, retrieved 2026-04-12
- ReAct — Yao et al., arxiv 2210.03629
- Plan-and-Solve Prompting — Wang et al., arxiv 2305.04091
- Self-Refine — Madaan et al., arxiv 2303.17651
- Reflexion — Shinn et al., arxiv 2303.11366
- MAST — Cemri et al., arxiv 2503.13657
- ACE — Zhang et al., arxiv 2510.04618
- flock(1) — man7.org/linux/man-pages/man1/flock.1.html, retrieved 2026-04-12
- flock(2) — man7.org/linux/man-pages/man2/flock.2.html, retrieved 2026-04-12
- Research PROTOCOL v2 — `~/.claude/teams/research/PROTOCOL.md`
- Research-lead MEMORY.md (lessons 1-12) — `~/.claude/agent-memory/research-lead/MEMORY.md`
- Memory-layer SYNTHESIS — `~/.claude/teams/research/claude-memory-layer-sota-2026q2/SYNTHESIS.md`

### MIXED (cite for direction, not for specific numbers)

- Morph LLM SWE-Bench Pro analysis — morphllm.com/swe-bench-pro, retrieved 2026-04-12
- Scale AI SEAL leaderboard — referenced via Morph LLM and llm-stats
- Aider polyglot leaderboard — aider.chat/docs/leaderboards/, retrieved 2026-04-12

### REPORTED-NOT-VERIFIED

- Claude Mythos Preview 93.9% Verified — search-aggregated, unverified at swebench.com primary
- Devin cost/time failure numbers — community-aggregated, no Cognition primary
- "25K-task experiment proves multi-agent wrong" — x.com/sukh_saroy/status/2039381283999293799, single-witness

### REJECT

- `groundy.com/articles/swe-bench-verified-explained-...` — AI-generated SEO content farm

## NEXT STEPS

1. **Run the smoke test** using the launch prompt above to validate v1 end-to-end on Hook A.
2. **Write the 13 persona files** from the appendix (they are in my final response to this session — the executor reads them directly).
3. **Write PROTOCOL.md** from the Round Structure section above.
4. **Apply CLAUDE.md Delta 1 and Delta 2** with the exact old/new pairs.
5. **Apply research PROTOCOL v2.1 update** with the exact text above.
6. **Upgrade git-identity.sh with flock** in v1.1 to close the parallel-session identity race.
7. **Implement semantic dedup in engineering-scribe** in v1.1 after the simple concatenate-then-ceiling pattern proves its limits in practice.
8. **First real cross-team session**: the Hook A smoke test IS the first engineering-team session. If it passes all 14 acceptance criteria, v1 is validated. If any fail, retrospector captures the v1→v1.1 patch list.
