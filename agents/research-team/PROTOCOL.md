# Research Team Protocol v2

The Research Team is the first fully-collaborative subagent team in this
setup. It is a **leader + 17 specialists** hierarchy, **all running on
Opus 4.6 with `effort: max`** (hard contract, no downgrades ever),
coordinating through **files on disk** rather than through conversational
context.

This document is the contract every team member reads before acting.
It supersedes Protocol v1 (2026-04-12).

## Scope model (v2.1)

The Research Team separates global infrastructure from per-project sessions:

**Global (~/.claude/) — shared across all projects:**
- `~/.claude/teams/research/PROTOCOL.md` — this document
- `~/.claude/agents/research/*.md` — all 18 agent personas
- `~/.claude/agent-memory/research-lead/` — institutional memory (cross-project)
- `~/.claude/scripts/` — audit_evidence.py, team_status.sh
- `~/.claude/hooks/` — PostToolUse evidence-write logger

**Per-project (<cwd>/.claude/) — isolated per project directory:**
- `.claude/teams/research/INDEX.md` — session index for THIS project only
- `.claude/teams/research/<slug>/` — all session artifacts (QUESTION, HYPOTHESES, EVIDENCE/, SYNTHESIS, LOG, etc.)

This means:
- When you switch to a vLLM repo, research sessions about vLLM live under
  that repo's `.claude/teams/research/`, not mixed with other projects.
- Institutional lessons in `~/.claude/agent-memory/research-lead/MEMORY.md`
  transfer across projects — a lesson learned on project A helps project B.
- Protocols are shared — the v2.1 protocol applies everywhere.
- The audit script (`~/.claude/scripts/audit_evidence.py`) searches CWD's
  `.claude/teams/research/<slug>/` first, then falls back to the global path.

## What changed from v1

v1 was a flat dispatch-and-synthesize loop. v2 mechanizes the failure-mode
safeguards published in the 2025-2026 multi-agent literature:

- **+5 new specialists**: `research-planner`, `research-adversary`,
  `research-moderator`, `research-evaluator`, `research-retrospector`
  (bringing specialist count from 12 to 17).
- **Hard pre-flight phase**: `research-planner` runs before the first
  dispatch, applying Anthropic's published scaling rule to prevent over-
  and under-scoping (the #1 reported failure in Anthropic's own
  multi-agent research post).
- **Structured debate for contradictions**: when `research-synthesist`
  reports a contradiction, `research-moderator` runs a 3-round debate
  instead of the lead arbitrating. This imports the DebateCV pattern
  and Claude Code agent-teams' explicit recommendation.
- **Separate evaluator from skeptic**: skeptic attacks reasoning,
  evaluator grades output against Anthropic's published 5-dimension
  rubric. Both must pass before "high confidence".
- **Adversarial corpus pass**: `research-adversary` attacks the sources
  themselves, catching SEO-farm / astroturf / citation-laundering
  attacks that skeptic (which points inward at the synthesis) cannot see.
- **Cross-session learning via agent memory**: `research-retrospector`
  writes session lessons to `~/.claude/agent-memory/research-lead/MEMORY.md`.
  The research-lead reads the first 200 lines at session start (either
  via Claude Code runtime's `memory: user` auto-injection, or explicitly
  as Step 3 of the intake protocol). No hand-rolled scheduler, no separate
  "lessons file".
- **Frontmatter hardening**: every agent file adds `effort: max`, moving
  the "all Opus max effort" doctrine from prose into runtime enforcement.
- **End-state evaluation**: synthesis confidence is judged by whether
  the final state is correct, not by path quality. Imports Anthropic's
  published guidance verbatim.
- **MAST failure-mode map**: every specialist role now names the MAST
  failure category it owns, so the lead can dispatch by failure mode,
  not just by lens.

## Roster

| Role | Agent name | Primary MAST failure owned | New in v2 |
|------|------------|---------------------------|-----------|
| Leader | `research-lead` | orchestration (FM-1.1, FM-1.5) | rewrite |
| Specialist | `research-planner` | scaling / breadth (FM-1.1) | yes |
| Specialist | `research-cartographer` | structural gap (FM-1.2) | — |
| Specialist | `research-archaeologist` | historical gap (FM-1.1) | — |
| Specialist | `research-librarian` | version-drift (FM-1.1) | — |
| Specialist | `research-tracer` | causal gap (FM-1.2) | — |
| Specialist | `research-empiricist` | untested claim (FM-3.2) | — |
| Specialist | `research-skeptic` | internal inconsistency (FM-3.3) | clarified |
| Specialist | `research-adversary` | corpus capture / SEO farms (FM-3.3) | yes |
| Specialist | `research-historian` | prior-art gap (FM-1.1) | handoff added |
| Specialist | `research-linguist` | polysemy (FM-2.6) | — |
| Specialist | `research-web-miner` | web corpus gap (FM-1.1) | — |
| Specialist | `research-github-miner` | GH corpus gap (FM-1.1) | — |
| Specialist | `research-synthesist` | silent contradiction (FM-2.5) | — |
| Specialist | `research-moderator` | contradiction arbitration bias (FM-2.5) | yes |
| Specialist | `research-evaluator` | no quality gate (FM-3.2, FM-3.3) | yes |
| Specialist | `research-retrospector` | no cross-session learning | yes |
| Specialist | `research-scribe` | ledger drift + playbook dedup (FM-1.4) | scope expanded |

## Model contract (non-negotiable)

Every agent in this team runs on `opus` with `effort: max`.
This is enforced at the frontmatter level; it is not a prose aspiration.
If you see an agent file in `~/.claude/agents/research/` without these two
fields, it is a bug — report it to the lead and do not proceed.

Never dispatch a specialist with a model override. Never "temporarily"
downgrade for budget reasons — there is no budget to save on Max plan,
and quality is the only optimization target.

## Execution model (read this before your first session)

Claude Code subagents cannot spawn other subagents. There are two valid
ways to run this team:

1. **Main-thread invocation** (`claude --agent research-lead`): research-lead
   is the main thread and dispatches specialists via the `Agent` tool in
   parallel. This is the canonical pattern.
2. **Adopted persona** (default when invoked via Agent from another session):
   research-lead reads each specialist's persona as a behavioral contract and
   executes its method directly, writing the output to the specialist's
   evidence file. The protocol's gates (planner → wide → synthesist →
   moderator → skeptic → adversary → evaluator → retrospector) still hold;
   they are procedural, not tool-dependent.

In both modes, the specialist *files* are the specs. The difference is
whether the specialists are literal processes or lens-passes within a
single thread.

## MAST failure-mode map (from Cemri et al. 2025, arxiv 2503.13657)

This team organizes its safeguards around the 14 MAST failure modes.
Every specialist role names the mode it primarily owns; the protocol's
gates enforce the 3 MAST categories as first-class checks.

### FC1. Specification and System Design (41.77% of all observed failures)
- FM-1.1 Disobey task specification — **owned by planner + lead**
- FM-1.2 Disobey role specification — **owned by cartographer + tracer**
- FM-1.3 Step repetition — **owned by planner + retrospector**
- FM-1.4 Loss of conversation history — **owned by scribe** (ledger)
- FM-1.5 Unaware of termination conditions — **owned by lead + evaluator**

### FC2. Inter-Agent Misalignment (36.94% of all observed failures)
- FM-2.1 Conversation reset — **owned by scribe** (LOG.md)
- FM-2.2 Fail to ask for clarification — **owned by lead** (intake & amplification protocol)
- FM-2.3 Task derailment — **owned by synthesist + moderator**
- FM-2.4 Information withholding — **owned by synthesist + scribe**
- FM-2.5 Ignored other agent's input — **owned by moderator**
- FM-2.6 Reasoning-action mismatch — **owned by linguist + moderator**

### FC3. Task Verification (21.30% of all observed failures)
- FM-3.1 Premature termination — **owned by evaluator**
- FM-3.2 No or incomplete verification — **owned by evaluator + skeptic**
- FM-3.3 Incorrect verification — **owned by skeptic + adversary + evaluator**

## Toolbox (who owns what)

| Capability | Primary tool | Owner(s) |
|------------|--------------|----------|
| Static codebase Grep/Read | Grep, Read, Glob | cartographer, tracer, linguist, archaeologist |
| Local git history | `git log/blame/show` via Bash | archaeologist |
| Official library docs | `mcp__plugin_context7_context7__*` | librarian |
| Hugging Face papers | `huggingface-skills:huggingface-papers` | librarian, historian |
| HF datasets / hub | `huggingface-skills:huggingface-datasets`, `hf-cli` | historian, empiricist |
| Browser automation | `mcp__playwright__*` | web-miner |
| JS-rendered scraping | Playwright | web-miner |
| Public JSON APIs | WebFetch | web-miner, historian, adversary |
| GitHub REST/GraphQL | `gh api` | github-miner |
| GitHub code/issue/PR search | `gh search *` | github-miner, historian |
| Running real experiments | Bash + runtime | empiricist |
| Persistent cross-session memory | `~/.claude/agent-memory/research-lead/MEMORY.md` | lead reads, retrospector writes, scribe curates |
| Parallel dispatch | one-message multi-Agent call | lead only |
| Debate cycles | 3-round structured-debate protocol | moderator |
| Citation verification | WebFetch, Read, Grep | evaluator, adversary |

## Entry point

You never talk to a specialist directly. You talk to `research-lead`.

```
Agent({ subagent_type: "research-lead", prompt: "<your question>" })
```

Or for main-thread invocation:

```
claude --agent research-lead
```

## Shared workspace

Session workspaces are created at `<cwd>/.claude/teams/research/<slug>/`
where `<cwd>` is the current working directory at session start (per-project).
Protocols and agent personas are read from `~/.claude/` (global).

```
.claude/teams/research/<slug>/
├── QUESTION.md              # owned by lead
├── HYPOTHESES.md            # owned by lead + skeptic
├── EVIDENCE/
│   ├── planner.md           # NEW — dispatch recommendation
│   ├── cartographer.md
│   ├── archaeologist.md
│   ├── librarian.md
│   ├── tracer.md
│   ├── empiricist.md
│   ├── skeptic.md
│   ├── adversary.md         # NEW — corpus attack
│   ├── historian.md
│   ├── linguist.md
│   ├── web-miner.md
│   ├── github-miner.md
│   ├── synthesist.md
│   ├── moderator.md         # NEW — debate verdicts (one per contradiction)
│   ├── evaluator.md         # NEW — 5-dim rubric grade
│   └── retrospector.md      # NEW — session post-mortem
├── EXPECTED_EVIDENCE.md     # NEW v2.1 — file-contract written by lead at Round 0
├── SYNTHESIS.md             # owned by lead ONLY
├── LOG.md                   # everyone appends
├── OPEN_QUESTIONS.md        # lead + any specialist
└── _write_audit.log         # NEW v2.1 — PostToolUse hook trail, retrospector reads at close
```

Team-wide files:

```
<cwd>/.claude/teams/research/INDEX.md    # scribe-owned, one line per past session (per-project)
<cwd>/.claude/teams/research/_archive/  # sessions > 90 days (per-project)
~/.claude/agent-memory/research-lead/MEMORY.md           # retrospector writes, scribe curates (global)
~/.claude/agent-memory/research-retrospector/MEMORY.md   # retrospector's meta-lessons (global)
```

## Ownership rules

| File | Who writes | Who reads |
|------|------------|-----------|
| `QUESTION.md` | `research-lead` | everyone |
| `HYPOTHESES.md` | `research-lead` + `research-skeptic` | everyone |
| `EVIDENCE/<name>.md` | only the named specialist | everyone |
| `EVIDENCE/moderator.md` | `research-moderator` (one per contradiction) | everyone |
| `SYNTHESIS.md` | `research-lead` ONLY | everyone |
| `LOG.md` | everyone (append-only) | everyone |
| `OPEN_QUESTIONS.md` | `research-lead` + any specialist | everyone |
| `INDEX.md` | `research-scribe` only | everyone |
| `EXPECTED_EVIDENCE.md` | `research-lead` only | everyone + audit_evidence.py |
| `_write_audit.log` | PostToolUse hook | `research-retrospector` at close |
| `~/.claude/agent-memory/research-lead/MEMORY.md` | `research-retrospector` writes, `research-scribe` dedupes | `research-lead` at session start, `research-planner` at plan time |

**Nobody edits another specialist's evidence file.** Contradictions go to
`research-moderator`, not direct edits. Schema fixes go through `research-scribe`.

## Evidence-file-as-contract (v2.1, additive)

v2.1 adds a file-contract enforcement layer on top of v2's round structure.
The addition is backward-compatible: v2-legacy sessions without the new
frontmatter continue to pass audit gates via grandfathering.

### EXPECTED_EVIDENCE.md (new Round 0 artifact)

At the end of Round 0 (after planner dispatch), the lead writes
`EXPECTED_EVIDENCE.md` listing every specialist file that MUST exist by
session close. Format:

```
# Expected evidence — <slug>
# One specialist name per line. Lines starting with '#' are comments.
# Optional '-' bullet prefix stripped.

- planner
- cartographer
- archaeologist         # skip if session has no git history to examine
- librarian
- historian
- web-miner
- github-miner
- tracer
- empiricist
- linguist
- synthesist
- skeptic
- adversary             # required if any web/community sources
- moderator             # conditional on contradictions
- evaluator
- retrospector
- scribe
```

The lead may customize per session (add custom specialists, skip ones that
don't apply). If the file is absent, the audit script falls back to the
team-default roster.

### Audit script at gate points

Before Round 2 synthesist dispatch, the lead runs:

```bash
python3 ~/.claude/scripts/audit_evidence.py <slug> --gate=mid-flight
```

Before writing SYNTHESIS.md, the lead runs:

```bash
python3 ~/.claude/scripts/audit_evidence.py <slug> --gate=synthesis --strict
```

Both calls must return exit 0. Exit 1 means re-dispatch the specialists
named in the violation list. Exit 2 is a script error (escalate to user).

### Evidence file schema (v2.1)

Every new evidence file SHOULD include a YAML frontmatter block at the top:

```yaml
---
specialist: research-<name>
slug: <session-slug>
started: <ISO-8601 timestamp>
completed: <ISO-8601 timestamp>
tool_calls_count: <integer>
citations_count: <integer>
confidence: high | medium | low
---
```

Frontmatter is OPTIONAL for backward compatibility. Files without it are
treated as v2-legacy and grandfathered through the audit gate.

Body requirements (enforced for all roles):
- Minimum size: 2000 bytes for lens roles, 1500 bytes for ledger roles
- Minimum H2 sections: 4 for lens roles, 3 for ledger roles
- Minimum distinct citations per role category:
  - Local lens (cartographer, archaeologist, tracer, linguist): >= 1 path / command / inline code ref
  - External lens (librarian, historian, web-miner, github-miner, empiricist): >= 3 URLs / arxiv / issue # / retrieved dates
  - Integration (synthesist, skeptic, adversary, moderator, evaluator, retrospector): >= 2 cross-file refs
  - Ledger (scribe, planner): >= 0 citations
- Terminal section: every file must end with `## Confidence`, `## Handoff`, or `## Verdict` header

### Smear detection (strict mode)

The audit script's `--strict` flag enables Jaccard similarity checking
across all evidence file pairs. Pairs exceeding threshold T=0.60 are
flagged as possible "lead-generalist-smear" (see linguist §2 for the
empirical calibration). Honest-but-related pairs observed at 0.25-0.45;
0.60 sits in the gap.

### Magentic-One stall counter (bounded re-dispatch)

If the mid-flight audit gate fails 3 times in a row on the same session
(`max_stalls = 3`, per Magentic-One production default), the lead re-plans
by rewriting `planner.md` rather than re-running the same specialists.
This imports Magentic-One's dual-ledger pattern (arxiv 2411.04468 + source
at github.com/microsoft/autogen).

### PostToolUse observational hook (auxiliary)

A non-blocking PostToolUse hook on Write|Edit matchers is OPTIONAL.
`~/.claude/hooks/log-evidence-writes.sh` writes a tab-delimited entry
to `<workspace>/_write_audit.log` for each evidence write:
`<ts>\t<tool_name>\t<size>\t<agent_id>\t<agent_type>\t<file_path>`.
The retrospector reads this log at session close to grade enforcement
compliance (did the lead call audit_evidence.py before SYNTHESIS.md?).

Install in `~/.claude/settings.json`:
```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "$HOME/.claude/hooks/log-evidence-writes.sh"
          }
        ]
      }
    ]
  }
}
```

**IMPORTANT**: this hook is best-effort, not a blocking gate. Per
anthropics/claude-code#43612, #43772, #40580, #34692, PreToolUse hooks do
NOT reliably fire for subagent tool calls in v2.1.101, especially under
`bypassPermissions` mode. PostToolUse IS reported working in v2.1.89+
per issue #34692 community comment. The hook is observational only;
enforcement happens at the lead's Bash audit calls.

### Retrospector close-audit (social enforcement)

At session close, the retrospector runs:
1. `python3 ~/.claude/scripts/audit_evidence.py <slug> --gate=synthesis --strict` — final audit, grade PASS/FAIL
2. Read `<workspace>/_write_audit.log` (if PostToolUse hook was enabled),
   verify that a Bash invocation of audit_evidence.py appears BEFORE the
   SYNTHESIS.md write event.
3. Write the grade to MEMORY.md as a new lesson if the session was
   non-compliant, e.g.:

   > Previous session <slug> wrote SYNTHESIS.md without first calling
   > audit_evidence.py at the synthesis gate. This is a v2.1 protocol
   > violation. Next session must include 'verify audit-before-synthesis'
   > in its pre-flight checklist explicitly.

The retrospector's grade is a SOFT signal, not a HARD gate. A session can
close successfully without the audit log entry if the primary enforcement
(lead Bash calls) ran. The PostToolUse hook presence is an ENHANCEMENT,
not a REQUIREMENT.

## Round structure (v2)

v2 adds explicit gates between rounds. The lead may not skip a gate.

### Round 0 — Pre-flight (NEW)
1. **Frame**: lead runs the intake & amplification protocol, writes
   `QUESTION.md` with an explicit "Assumed interpretation" section.
2. **Seed**: lead writes 2-4 hypotheses to `HYPOTHESES.md` BEFORE dispatching.
3. **Plan**: lead dispatches `research-planner` (single specialist, synchronous).
   Planner reads QUESTION, HYPOTHESES, and the lead's MEMORY.md, then
   writes `EVIDENCE/planner.md` with the dispatch recommendation.
4. **Commit**: lead reads `planner.md` and commits to a dispatch plan.
   If the lead overrides the planner, it must note why in `LOG.md`.

### Round 1 — Wide opener
5. **Dispatch** 6-10 specialists in parallel in a single message.
   Anthropic's published parallelization target: 3-5 parallel subagents
   for comparisons, 10+ for complex research. Err toward the high end
   on the opener; narrow in subsequent rounds.
6. **Return**: each specialist writes to `EVIDENCE/<name>.md` and appends
   to `LOG.md`.
7. **Synthesize pass 1**: `research-synthesist` runs over all round-1 evidence,
   produces a claim matrix and flags contradictions.

### Round 2 — Adversarial gates
7b. **Mid-flight audit gate (v2.1)**: BEFORE dispatching synthesist, lead runs
    `bash -c 'python3 ~/.claude/scripts/audit_evidence.py <slug> --gate=mid-flight'`.
    Exit 0 = proceed. Exit 1 = re-dispatch specific specialists named in the
    violation list. Exit 2 = escalate to user. If the gate fails 3 times in a
    row on the same session, re-plan via `planner.md` rewrite (Magentic-One
    stall counter pattern, max_stalls=3).
8. **Moderator**: for every load-bearing contradiction in
   `synthesist.md`, lead dispatches `research-moderator`. Moderator writes
   one `moderator.md` debate per contradiction (or appends sections to a
   single file if multiple).
9. **Skeptic**: lead dispatches `research-skeptic`. Skeptic reads full
   workspace, attacks the leading hypothesis, produces competing
   hypotheses, identifies unstated assumptions.
10. **Adversary**: lead dispatches `research-adversary` if any evidence
    came from web/community sources. Adversary audits the corpus for
    SEO farms, citation laundering, staleness, astroturf, corpus capture.

### Round 3 — Evaluator gate (NEW)
10b. **Synthesis audit gate (v2.1)**: BEFORE drafting `SYNTHESIS.md`, lead runs
    `bash -c 'python3 ~/.claude/scripts/audit_evidence.py <slug> --gate=synthesis --strict'`.
    Exit 0 required. Exit 1 = re-dispatch missing/shallow specialists and re-run
    the gate. Exit 2 = escalate. The `--strict` flag enables Jaccard smear
    detection (T=0.60).
11. Lead drafts `SYNTHESIS.md` incorporating skeptic and moderator verdicts.
12. Lead dispatches `research-evaluator`. Evaluator runs the 5-dimension
    rubric (factual accuracy, citation accuracy, completeness, source
    quality, tool efficiency). Must pass all 5 thresholds for
    "high confidence".
13. **If evaluator PASSES**: proceed to delivery.
14. **If evaluator FAILS**: return to step 5 with re-dispatch targeting
    the dimension(s) that failed. Hard cap: 4 total dispatch rounds.

### Session close — Retrospection (NEW)
15. Lead dispatches `research-retrospector`. Retrospector reads the full
    session, extracts 3-7 durable lessons, writes them to
    `~/.claude/agent-memory/research-lead/MEMORY.md`, and writes a session
    post-mortem to `EVIDENCE/retrospector.md`.
16. Lead dispatches `research-scribe` for final ledger normalization and
    INDEX.md entry. Scribe also dedupes the retrospector's new entries
    in MEMORY.md against existing entries (ACE "curator" role).
17. Lead delivers trimmed SYNTHESIS.md content to the user.

## Confidence scale (v2)

- **High**: all of the following are true:
  - Multiple independent specialists converge on the claim
  - Skeptic ran and failed to break it
  - Moderator's verdict is final (no underdetermined contradictions)
  - Adversary's corpus audit is "healthy" or "mixed" with no rejections on load-bearing citations
  - Evaluator's 5-dimension rubric passes all thresholds
- **Medium**: specialists agree but one or more of the above gates has
  not yet run, OR evaluator verdict is PROVISIONAL.
- **Low**: single-source, unresolved contradiction, evaluator FAIL, or
  adversary marked corpus "compromised".

**No "high confidence" without all four of skeptic + moderator (if contradictions) + adversary (if web sources) + evaluator.**

## Parallelization targets (from Anthropic's post)

- **3-5 subagents spawned in parallel** on the opener, not serially.
- **3+ parallel tool calls per subagent** where the specialist's method
  supports it.
- **90% reduction** in research time is the reported Anthropic gain from
  these two rules. We should match or exceed it.
- **Single-message dispatch**: all round-N specialists must be spawned in
  ONE `Agent(...)` call emission by the lead. Serial dispatch is a bug
  unless one specialist's output is literally required as input to the next.

## Citation schema (enforced by `research-scribe`)

- Code: `path/to/file.ts:123`
- Commit: 12+ char sha + quoted message
- Doc: `URL + § section + retrieved <ISO-date>`
- Experiment: `EVIDENCE/empiricist.md#<anchor>` + raw-output block
- Prior art: URL + author + year + retrieval date
- Agent-memory reference: `~/.claude/agent-memory/research-lead/MEMORY.md#<lesson-title>`
- Web fetch: URL + retrieved `<ISO-date>`, raw content cached if load-bearing
- GraphQL: raw query text + response cached at `EVIDENCE/github-miner/raw/<name>.json`

## Git identity

Before any commit or push, run:
```bash
bash ~/.claude/lib/git-identity.sh
```
The `PreToolUse` hook runs it automatically on `git commit` / `git push` /
`gh pr create`, but run it explicitly if you want to be sure.

## Session naming

`<slug>` is chosen by `research-lead` from the question. Examples:
- `vllm-paged-attention-semantics`
- `why-auth-middleware-leaks-tokens`
- `should-we-adopt-turbopack`
- `self-evolve-v2` (this session)

If the user is continuing a previous investigation, reuse the slug and
append to existing files.

## Escalation

If the mid-flight or synthesis audit gate (v2.1) fails 3 times in a row
(`max_stalls = 3` per Magentic-One), `research-lead` must re-plan by
rewriting `planner.md` before continuing.

If after 4 dispatch rounds the evaluator has not issued PASS,
`research-lead` must:
1. Deliver the best-available SYNTHESIS.md at current confidence
2. Publish `OPEN_QUESTIONS.md` with what's unresolved
3. Propose a concrete next probe that would raise confidence (new source,
   user decision, a running experiment, an access grant)
4. Dispatch `research-retrospector` to capture why the gate didn't close

Never loop silently past 4 rounds.

## Prior art this protocol imports

- **Anthropic "How we built our multi-agent research system"**
  (https://www.anthropic.com/engineering/multi-agent-research-system,
  retrieved 2026-04-12) — orchestrator-worker pattern, 5-dim LLM-as-judge
  rubric, scaling rules (1 / 2-4 / 10+), parallelization targets,
  self-improvement via tool-description rewrites, "SEO farms" failure.
- **Anthropic "Building effective agents"**
  (https://www.anthropic.com/research/building-effective-agents,
  retrieved 2026-04-12) — workflow/agent distinction, orchestrator-workers,
  evaluator-optimizer, anti-patterns on framework complexity.
- **Anthropic "Building agents with the Claude Agent SDK"**
  (https://claude.com/blog/building-agents-with-the-claude-agent-sdk,
  retrieved 2026-04-12) — agent loop "gather context → take action →
  verify work → repeat", file-system as context engineering, rules-based
  verification pattern, LLM-as-judge caveat.
- **Claude Code sub-agents docs**
  (https://code.claude.com/docs/en/sub-agents, retrieved 2026-04-12) —
  frontmatter schema, `effort: max`, `memory: user`, `Agent()` allowlist,
  "subagents cannot spawn subagents" constraint.
- **Claude Code agent-teams docs**
  (https://code.claude.com/docs/en/agent-teams, retrieved 2026-04-12) —
  debate-structured investigation, mailbox/task-list mechanics (v3 target).
- **MAST: "Why Do Multi-Agent LLM Systems Fail?"** Cemri et al.,
  arxiv 2503.13657, NeurIPS 2025 — 14 failure modes, 3 categories,
  prevalence distribution.
- **DebateCV: "Debating Truth"** arxiv 2507.19090 — debate-driven
  claim verification, moderator pattern.
- **Magentic-One** (Microsoft Research, arxiv 2411.04468) — ledger-based
  orchestration (task ledger + progress ledger).
- **ACE: "Agentic Context Engineering"** arxiv 2510.04618 — evolving
  playbook, generation/reflection/curation loop, grow-and-refine
  deduplication mechanism.
- **"Justice or Prejudice? Quantifying Biases in LLM-as-a-Judge"**
  arxiv 2410.02736 — 12 judge-bias types, including length bias and
  agreeableness bias — informs evaluator rubric hardening.
