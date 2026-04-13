# Cartographer — structural map of existing agent ecosystem

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: structural, module boundaries, naming surface, directory graph

## Inventory: `~/.claude/agents/` (flat primitives)

Observed at session start via `ls /home/akash/.claude/agents/`. These are existing **user-scoped flat agents** that will remain untouched. Engineering-team specialists MUST be `engineering-*` prefixed to avoid collision:

| File | Role | Model | Status vs engineering-team |
|---|---|---|---|
| `analyst.md` | requirements-gap analysis | — | NOT wrapped — distinct flat role |
| `architect.md` | architecture advisor | — | NOT wrapped — distinct flat role; `engineering-architect` mirrors its lens |
| `architect-planner.md` | detailed architectural plan author | opus | NOT wrapped — distinct; inspired `engineering-architect` but not a 1:1 wrap |
| `code-reviewer.md` | severity-rated code review | `claude-opus-4-6` | NOT wrapped — `engineering-reviewer` mirrors its method but scoped to team-session |
| `code-simplifier.md` | refactor-for-clarity | `claude-opus-4-6` | NOT wrapped; optional v1.1 inclusion |
| `critic.md` | critical review | — | NOT wrapped — `engineering-skeptic` owns this lens |
| `debugger.md` | root-cause + build fixes | `claude-sonnet-4-6` | CANDIDATE — see v1 decision below |
| `designer.md` | design advisor | — | NOT wrapped (Design team target) |
| `document-specialist.md` | documentation author | — | NOT wrapped; optional v1.1 inclusion |
| `executor.md` | implementation executor | `claude-sonnet-4-6` | NOT wrapped — `engineering-executor` mirrors method at `model: opus, effort: max` |
| `explore.md` | exploration helper | — | NOT wrapped (used as sub-tool) |
| `git-manager.md` | git operations helper | — | NOT wrapped (called by executor as needed) |
| `git-master.md` | git operations variant | — | NOT wrapped (duplicate surface) |
| `planner.md` | interview-and-save-plan | `claude-opus-4-6` | NOT wrapped — different semantic; `engineering-planner` is dispatch-decomposer not interview-wrapper |
| `qa-tester.md` | QA testing | — | NOT wrapped; partially absorbed by `engineering-verifier` |
| `researcher.md` | solo research | — | NOT wrapped — superseded by research-team |
| `scientist.md` | experimental hypothesis | — | NOT wrapped |
| `security-reviewer.md` | security review | — | NOT wrapped; may be consulted by `engineering-reviewer` |
| `test-engineer.md` | test strategy + TDD | `claude-sonnet-4-6` | NOT wrapped — `engineering-verifier` absorbs the test-execution part, but test authoring remains a consulted flat role |
| `test-writer.md` | test authoring | — | NOT wrapped |
| `tracer.md` | tracing helper | — | NOT wrapped (research-tracer uses this lens) |
| `verifier.md` | evidence-based verification | `claude-sonnet-4-6` | NOT wrapped — `engineering-verifier` upgrades to opus+max effort with team-scope |
| `writer.md` | writing | — | NOT wrapped |

**Key finding**: 24 flat agents exist. Engineering-team is an **orthogonal hierarchy**, not a replacement. None of the flat agents need to be renamed or deleted. The `engineering-*` prefix guarantees zero collision.

## Inventory: `~/.claude/agents/research/` (the model to clone)

```
research-adversary.md        research-lead.md        research-retrospector.md
research-archaeologist.md    research-librarian.md   research-scribe.md
research-cartographer.md     research-linguist.md    research-skeptic.md
research-empiricist.md       research-moderator.md   research-synthesist.md
research-evaluator.md        research-planner.md     research-tracer.md
research-github-miner.md     research-web-miner.md   research-historian.md
```

18 files: 1 lead + 17 specialists. Consistent naming: `research-<role>.md`. Frontmatter convention: `name`, `description`, `model: opus`, `effort: max`, optional `color`. Body: persona + method + deliverable shape + hard rules.

**Rule to inherit**: engineering-team must use the **same directory pattern** (`~/.claude/agents/engineering/engineering-*.md`), the **same frontmatter schema** (`model: opus`, `effort: max` mandatory), and the **same body shape** (persona → method → deliverable → hard rules).

## Inventory: `~/.claude/teams/`

```
research/
  ├── PROTOCOL.md                         # v2 canonical
  ├── PROTOCOL.v1.bak                     # historical — v1 for archaeology
  ├── INDEX.md                            # session ledger (scribe owned)
  ├── claude-memory-layer-sota-2026q2/   # pilot v2 session, HIGH confidence
  ├── claude-memory-layer-sota-2026q2-deeper/  # possible follow-up workspace
  ├── vllm-moe-ep-routing-2026q2/        # earlier session
  └── engineering-team-self-evolve-v1/   # CURRENT session (this)
```

No `~/.claude/teams/engineering/` directory exists yet. The engineering team creates it at first invocation.

**Structural recommendation**: mirror the research layout exactly.

```
~/.claude/teams/engineering/
├── PROTOCOL.md                           # engineering v1 canonical (to be written)
├── INDEX.md                              # session ledger (engineering-scribe owned)
├── _archive/                             # rotation target for > 90 day sessions
└── <slug>/
    ├── CHARTER.md                        # input: reads research SYNTHESIS.md if cross-team
    ├── PLAN.md                           # lead-owned, analogue of research SYNTHESIS.md
    ├── HYPOTHESES.md                     # competing implementation designs (same as research)
    ├── EVIDENCE/                         # per-specialist files
    │   ├── planner.md
    │   ├── architect.md
    │   ├── executor.md
    │   ├── verifier.md
    │   ├── reviewer.md
    │   ├── skeptic.md
    │   ├── adversary.md
    │   ├── moderator.md      # contradiction debates
    │   ├── evaluator.md      # final gate
    │   ├── retrospector.md
    │   └── scribe.md
    ├── DIFF_LOG.md                       # NEW — every executor change recorded
    ├── VERIFY_LOG.md                     # NEW — every verifier run recorded
    ├── LOG.md                            # append-only activity log
    ├── OPEN_QUESTIONS.md                 # blockers needing lead decision
    └── FEEDBACK_FROM_ENGINEERING.md      # conditional — written when engineering disagrees with research input
```

Two files are new relative to the research layout:

1. **`DIFF_LOG.md`** — engineering specifically writes code. Every executor change appends `<ts> <file>:<line-range> <change-type> <one-line-why>`. Analogue to research's "LOG.md appends" but code-specific, machine-readable, rollbackable.
2. **`VERIFY_LOG.md`** — engineering specifically verifies code. Every verifier run appends `<ts> <test-command> <exit-code> <N-passed/N-failed> <artifact-path>`. Analogue to empiricist's raw-output blocks but named explicitly so the reviewer can trace "did these tests pass BEFORE this edit."

Everything else mirrors research-team.

## Inventory: `~/.claude/agent-memory/`

```
~/.claude/agent-memory/
├── architect-planner/      # (existing, from flat architect-planner.md)
├── research-lead/
│   └── MEMORY.md           # 12 lessons, ~25KB, curated by research-retrospector + research-scribe
└── research-retrospector/
    └── (meta-lessons about retrospection, seeded empty today)
```

No `engineering-lead/` memory directory exists. The engineering team creates it at first session close (retrospector writes there).

**Parallel-instance observation**: today the research-lead memory file is **read-at-start, written-at-close, single-writer-per-session assumed**. With two research sessions running concurrently, their retrospectors race on the close-write. This is the problem Akash identified. The fix (detailed in tracer.md and synthesized in SYNTHESIS.md) is a per-session staging directory + lock-protected merge.

**Structural recommendation for the memory layout**:

```
~/.claude/agent-memory/
├── engineering-lead/
│   ├── MEMORY.md                 # canonical, read at session start
│   ├── .lock                     # flock advisory target
│   ├── staging/                  # per-session append-only delta
│   │   └── <slug>.md             # retrospector writes here first, never direct to MEMORY.md
│   └── topic/                    # (Hook A overflow, per memory-layer SYNTHESIS)
├── engineering-retrospector/
│   ├── MEMORY.md                 # meta-lessons
│   ├── .lock
│   └── staging/
├── research-lead/
│   ├── MEMORY.md                 # existing + upgraded to staging pattern
│   ├── .lock                     # NEW
│   ├── staging/                  # NEW
│   └── topic/                    # NEW (memory-layer Hook A target)
└── research-retrospector/
    └── (upgraded to staging pattern)
```

This is a **backward-compatible upgrade**: existing `MEMORY.md` files stay where they are. The `.lock` and `staging/` directory are added alongside. Readers continue to read `MEMORY.md` directly without locking (the file is append-mostly and readers tolerate slight staleness, per MEMORY.md lesson 10 on REPORTED-NOT-VERIFIED tolerance — the analogue here is READ-STALE tolerance).

## Naming collision check

Searched existing `~/.claude/agents/` for any file starting with `engineering-`. **Zero collisions**. The `engineering-*` prefix is unclaimed. Safe to use:

- `engineering-lead`
- `engineering-planner`
- `engineering-architect`
- `engineering-executor`
- `engineering-verifier`
- `engineering-reviewer`
- `engineering-skeptic`
- `engineering-adversary`
- `engineering-moderator`
- `engineering-evaluator`
- `engineering-retrospector`
- `engineering-scribe`
- `engineering-debugger` (optional, see v1 decision)

No existing agent holds any of these names.

## Debugger inclusion decision (requested blind-spot flag)

The meta-task asks whether to include `engineering-debugger`, `engineering-simplifier`, `engineering-documenter`, `engineering-migrator` in the v1 roster.

**Recommendation**:
- **`engineering-debugger`**: **include in v1** as optional-dispatch. Rationale: when verifier fails, someone has to root-cause. Today that's the lead's job (bad — orchestrator doing implementation). A dedicated debugger is the clean abstraction. Flat `debugger.md` exists as the pattern source; wrap it as `engineering-debugger` with `model: opus, effort: max` and a lens-specific scope (debug WITHIN the current task's blast radius, do not expand scope).
- **`engineering-simplifier`**: **EXCLUDE from v1, add in v1.1**. Rationale: simplification is a refactor pass, runs AFTER verify-passes. It's the equivalent of the scribe's "normalize format only" for code. Useful but not mandatory for v1. Document as a future addition.
- **`engineering-documenter`**: **EXCLUDE from v1, add in v1.1**. Rationale: docs are a separate Documentation Team concern (per CLAUDE.md "Teams under construction" list). Engineering-reviewer verifies that public APIs are documented; a full docs-writer is outside scope.
- **`engineering-migrator`**: **EXCLUDE from v1**. Rationale: migrations are a special case of executor work (schema changes, data migrations). engineering-architect designs them, engineering-executor implements them. No dedicated role until a session shows the need.

v1 roster final count: **12 specialists + 1 lead** (lead, planner, architect, executor, verifier, reviewer, skeptic, adversary, moderator, evaluator, debugger, retrospector, scribe).

## Sub-lead decision (structural)

Three topologies were on the table:

- **Flat**: all 12 specialists report to engineering-lead. No sub-leads.
- **Hierarchical**: engineering-lead → sub-leads (e.g. plan-lead, build-lead, verify-lead) → specialists.
- **Pipeline**: fixed ordering, no sub-leads, but each stage's "owner" specialist runs serial.

**Structural recommendation: flat**. Justification:

1. Akash explicit constraint: "a team of planners and executors that are **together**." Hierarchical sub-leads create an organizational boundary ("plan-lead owns planning, build-lead owns building") that violates this constraint.
2. Research Team v2 is flat (17 specialists direct to lead) and works well. No structural pressure to add sub-leads.
3. Sub-leads would re-introduce the subagent-cannot-spawn-subagents problem twice: lead can't dispatch sub-lead which can't dispatch specialist. Two layers of the same constraint is strictly worse than one.
4. MAST FM-1.4 (loss of conversation history) is worse in hierarchies — the sub-lead summarizes upward, losing detail. Flat with file-backed coordination preserves all signal.

## What changes vs research-team structurally

Same layout. Same directory conventions. Same persona file schema. Additional files: `CHARTER.md`, `PLAN.md` (renames `SYNTHESIS.md`), `DIFF_LOG.md`, `VERIFY_LOG.md`, conditional `FEEDBACK_FROM_ENGINEERING.md`. Additional staging directory under each agent-memory path for concurrency (backward compatible).

## Key structural citations

- `/home/akash/.claude/agents/research/research-lead.md` — frontmatter schema + execution model to mirror
- `/home/akash/.claude/teams/research/PROTOCOL.md` — v2 protocol to clone with engineering-specific diffs
- `/home/akash/.claude/agents/code-reviewer.md:4-7` — `disallowedTools: Write, Edit` pattern useful for engineering-reviewer to inherit (review-only, no authoring)
- `/home/akash/.claude/agent-memory/research-lead/MEMORY.md` — lesson 12 (subagent spawn constraint) to embed in engineering-lead persona

## Verdict

No structural blockers. The engineering-team can mirror the research-team layout with a clean `engineering-*` prefix, add 4 engineering-specific files (CHARTER, PLAN, DIFF_LOG, VERIFY_LOG), and introduce the per-agent `.lock` + `staging/` concurrency pattern as a backward-compatible extension to agent-memory.
