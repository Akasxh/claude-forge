# Documentation & Knowledge Team Protocol v1

The Documentation & Knowledge Team is a **leader + 10 specialists** hierarchy,
**all running on Opus with `effort: max`** (hard contract, no downgrades ever),
coordinating through **files on disk** and producing verified documentation
with full accuracy-gate coverage.

This document is the contract every team member reads before acting.

## Scope model (v1)

The Docs Team separates global infrastructure from per-project sessions:

**Global (~/.claude/) — shared across all projects:**
- `~/.claude/teams/docs/PROTOCOL.md` — this document
- `~/.claude/agents/docs/*.md` — all 11 agent personas
- `~/.claude/agent-memory/docs-lead/` — institutional memory (cross-project)

**Per-project (<cwd>/.claude/) — isolated per project directory:**
- `.claude/teams/docs/INDEX.md` — session index for THIS project only
- `.claude/teams/docs/<slug>/` — all session artifacts (CHARTER, DOC_PLAN, EVIDENCE/, TEST_LOG, LOG, etc.)

This means:
- When you switch to a vLLM repo, docs sessions about vLLM live under
  that repo's `.claude/teams/docs/`, not mixed with other projects.
- Institutional lessons in `~/.claude/agent-memory/docs-lead/MEMORY.md`
  transfer across projects — a lesson learned on project A helps project B.
- Protocols are shared — the v1 protocol applies everywhere.
- Cross-team handoffs (engineering DIFF_LOG → docs CHARTER) work per-project:
  both sessions typically share the same CWD, so paths resolve naturally.

## What this team does

The Documentation & Knowledge Team produces verified, accurate documentation
for any project. It is project-agnostic: README, API docs, architecture docs,
changelogs, onboarding guides, code comments, knowledge base articles.

Core accuracy mechanism: **reader-before-writer**. DocAgent paper (arxiv,
2024) demonstrated that topological code processing achieves 95.7% truthfulness
vs 61.1% for chat-based generation. Every doc target goes through docs-reader
before docs-writer; no documentation is written without grounded source evidence.

## Roster (10 specialists + 1 lead)

| Role | Agent name | MAST ownership | Phase | Notes |
|---|---|---|---|---|
| Leader | `docs-lead` | FM-1.1, FM-1.5, FM-2.2 | all | orchestrator |
| Detector | `docs-detector` | FM-1.1 | Phase A | project detection, mandatory first |
| Planner | `docs-planner` | FM-1.1 | Phase A | coverage gap, priority matrix |
| Reader | `docs-reader` | FM-3.3 | Phase B inner | source code extraction, accuracy ground truth |
| Writer | `docs-writer` | FM-1.2, FM-2.3 | Phase B inner | writes from reader.md only, never invents |
| Tester | `docs-tester` | FM-3.2 | Phase B inner | validates examples, links, cross-refs |
| Reviewer | `docs-reviewer` | FM-2.3, FM-3.3 | Phase B inner | spec compliance, accuracy, style |
| Diagrammer | `docs-diagrammer` | FM-1.2 | Phase B conditional | Mermaid/PlantUML/ASCII diagrams |
| Skeptic | `docs-skeptic` | FM-3.3 | close gate | attacks documentation quality |
| Evaluator | `docs-evaluator` | FM-3.1, FM-3.2 | close gate | 5-dim rubric, PASS/FAIL |
| Retrospector | `docs-retrospector` | cross-session | close | staging writes, lesson extraction |

## Model contract (non-negotiable)

Every agent in this team runs on `opus` with `effort: max`.
This is enforced at the frontmatter level; it is not a prose aspiration.

## Execution model

Claude Code subagents cannot spawn other subagents. There are two valid
ways to run this team:

1. **Main-thread invocation** (`claude --agent docs-lead`): the lead
   is the main thread and dispatches specialists via the `Agent` tool.
2. **Adopted persona** (default when invoked via Agent from another session):
   the lead reads each specialist's persona as a behavioral contract and
   executes its method directly, writing outputs to the specialist's evidence
   files. The protocol's gates still hold; they are procedural, not
   tool-dependent.

## Tier classification (binding)

Every task is classified before work begins. Classification cannot be
overridden DOWNWARD by the user — only upward.

- **Targeted**: document a specific function, class, or module. No plan gate.
  Dispatch: reader + writer + tester + reviewer only.
- **Scoped**: document a subsystem, update existing docs, write changelog.
  Phase A + Phase B. No skeptic unless accuracy risk is high.
- **Comprehensive**: full documentation audit, new doc site, complete overhaul.
  Full roster with all gates. Mandatory skeptic + evaluator.

Default bias: when in doubt, pick the higher tier.

## Round structure (v1)

| Round | Name | Gates | Output |
|---|---|---|---|
| Round 0 | Intake | — | CHARTER.md, tier decision |
| Round 1 | Phase A — Plan | — | DOC_PLAN.md |
| Round 2..N | Phase B — Author | tester-gate + reviewer-gate per target | doc files + TEST_LOG entries |
| Round N+1 | Phase C — Quality Gate | docs-skeptic → docs-evaluator | evaluator.md PASS/FAIL |
| Close | Retrospection + handback | — | MEMORY.md updated, INDEX.md entry |

### Round 0 — Intake

1. Lead runs intake-and-amplification protocol.
2. Reads `~/.claude/agent-memory/docs-lead/MEMORY.md` (first 200 lines).
3. Classifies tier.
4. Dispatches `docs-detector` (mandatory, non-skippable).
5. Writes CHARTER.md citing detector results.

### Round 1 — Phase A (Plan)

1. Lead dispatches `docs-planner` with detector output + CHARTER.
2. Planner writes `EVIDENCE/planner.md` (coverage analysis, priority matrix, doc plan).
3. Lead writes DOC_PLAN.md integrating planner output.

### Round 2..N — Phase B (Author)

Inner reader-before-writer loop for each doc target i in DOC_PLAN.md:

1. **Read source**: `docs-reader` extracts signatures, types, behaviors, examples.
   Writes `EVIDENCE/reader-<target>.md`. This is the accuracy ground truth.
2. **Write docs**: `docs-writer` consumes reader.md ONLY. Never invents.
   Writes draft to `<cwd>/<doc-path>`.
3. **Diagram** (if architectural): `docs-diagrammer` reads reader evidence.
   Writes `EVIDENCE/diagrammer-<target>.md`.
4. **Test examples**: `docs-tester` runs every code example, checks links.
   Appends to `TEST_LOG.md` and `EVIDENCE/tester.md`.
5. **Review**: `docs-reviewer` checks accuracy vs reader evidence, style, spec compliance.
   Writes `EVIDENCE/reviewer.md`.
6. **Branch**:
   - tester PASS + reviewer PASS → mark target complete, i+1.
   - tester FAIL → writer revises using tester output. 3-failure circuit breaker.
   - reviewer REQUEST_CHANGES → writer retries with reviewer feedback.
   - reviewer finds accuracy error → reader re-reads source (back-edge to step 1).

**Termination caps**:
- Soft cap: `2 × DOC_PLAN.target_count` iterations. Log WARNING, continue.
- Hard cap: `5 × DOC_PLAN.target_count` iterations. Force-halt, escalate to user.
- Floor for 1-target sessions: 5 soft, 10 hard.

### Phase C — Quality Gate

1. Lead writes DOC_PLAN-vs-shipped delta to LOG.md.
2. `docs-skeptic` attacks documentation quality. Writes `EVIDENCE/skeptic.md`.
3. `docs-evaluator` runs 5-dimension rubric:
   - **Strict** (1.0 required): accuracy, example correctness.
   - **Advisory** (0.7, lead override allowed): completeness, readability, style conformance.
4. PASS → retrospection.
5. FAIL on strict → return to Phase B. Hard cap: 2 evaluator re-runs.
6. FAIL on advisory only → lead decides.

### Session close — Retrospection + handback

1. `docs-retrospector` extracts 3-7 lessons to staging/.
2. Lead merges staging lessons into MEMORY.md (flock + atomic rename).
3. Lead writes INDEX.md entry at `<cwd>/.claude/teams/docs/INDEX.md`.
4. If cross-team: lead writes HANDBACK_FROM_DOCS to engineering/research workspace.

## Prior art this protocol imports

- **DocAgent** (Lyu et al., arxiv 2024) — reader-before-writer pattern.
- **Anthropic "Building effective agents"** — orchestrator-worker, evaluator-optimizer.
- **MAST** (Cemri et al., arxiv 2503.13657) — 14 failure mode taxonomy.
- **ACE** (Zhang et al., arxiv 2510.04618) — evolving playbook, grow-and-refine curation.
- **Engineering Team PROTOCOL v1** — adversarial gates, staging merge protocol.
