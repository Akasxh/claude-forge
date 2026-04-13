# Testing/QA Team Protocol v1

The Testing/QA Team is the 4th fully-collaborative subagent team in this
setup. It is a **leader + 11 specialists** hierarchy, **all running on
Opus with `effort: max`** (hard contract, no downgrades ever), coordinating
through **files on disk** and validating code quality with full adversarial
gate coverage.

This document is the contract every team member reads before acting.

## Scope model (v1)

The Testing/QA Team separates global infrastructure from per-project sessions:

**Global (~/.claude/) — shared across all projects:**
- `~/.claude/teams/testing/PROTOCOL.md` — this document
- `~/.claude/agents/testing/*.md` — all 12 agent personas (lead + 11 specialists)
- `~/.claude/agent-memory/testing-lead/` — institutional memory (cross-project)

**Per-project (<cwd>/.claude/) — isolated per project directory:**
- `.claude/teams/testing/INDEX.md` — session index for THIS project only
- `.claude/teams/testing/<slug>/` — all session artifacts

## What this team does

Engineering Team ships code. Testing/QA Team independently validates that
code by writing new tests, analyzing coverage gaps, running mutation testing,
detecting regressions, and ensuring test quality.

The boundary is clear: **Engineering-verifier RUNS existing tests.
Testing-writer WRITES new tests.**

## Roster (11 specialists + 1 lead)

| Role | Agent name | MAST ownership | Phase | Notes |
|---|---|---|---|---|
| Leader | `testing-lead` | FM-1.1, FM-1.5, FM-2.2 | all | orchestrator |
| Detector | `testing-detector` | FM-1.1 | Phase A | project-agnostic detection |
| Planner | `testing-planner` | FM-1.1 | Phase A | coverage gap analysis |
| Writer | `testing-writer` | FM-1.2, FM-2.3 | Phase B | unit/integration/E2E |
| Property | `testing-property` | FM-1.2 | Phase B | property-based tests |
| Mutator | `testing-mutator` | FM-3.2 | Phase B | mutation testing |
| Fixture | `testing-fixture` | FM-1.2 | Phase B | mocks, stubs, factories |
| Runner | `testing-runner` | FM-2.6, FM-3.2 | Phase B | 3x fresh execution |
| Skeptic | `testing-skeptic` | FM-3.3 | gate | test quality attack |
| Evaluator | `testing-evaluator` | FM-3.1, FM-3.2 | close gate | 6-dim rubric |
| Retrospector | `testing-retrospector` | cross-session | close | lessons staging |
| Scribe | `testing-scribe` | FM-1.4, FM-2.1, FM-2.4 | close | ledger + merge |

## Tier classification (binding)

- **Targeted**: test a specific function/module. Writer + runner only.
- **Coverage**: fill coverage gaps. Full Phase A + Phase B + skeptic gate.
- **Comprehensive**: full test audit. Full roster. Mutation + property testing mandatory.

Default bias: when in doubt, pick the higher tier.

## Round structure (v1)

| Round | Name | Gates | Output |
|---|---|---|---|
| Round 0 | Intake + Detection | detector (mandatory) | CHARTER.md, detector.md |
| Round 1 | Phase A — Plan | skeptic pre-flight | TEST_PLAN.md |
| Round 2..N | Phase B — Generate + Validate | runner (3x) + mutator | test files + TEST_LOG.md |
| Round N+1 | Close — Evaluator | 6-dim rubric | evaluator.md PASS/FAIL |
| Close | Retrospection + scribe + handback | — | MEMORY.md updated |

## Cross-team handoff: Engineering → Testing

Invoke with engineering DIFF_LOG.md:
```
Agent({
  subagent_type: "testing-lead",
  prompt: "Validate engineering changes <engineering-slug>. Read DIFF_LOG.md.",
})
```

## Prior art

- Meta TestGen-LLM (FSE 2024), Meta ACH (FSE 2025), ASTER (IBM ICSE 2025)
- LLM flakiness study (arxiv 2601.08998) — 3x run pattern
- PBT effectiveness (arxiv 2510.25297) — PBT+EBT hybrid 81.25% bug detection
- Engineering Team PROTOCOL v1 — two-phase structure, staging merge
