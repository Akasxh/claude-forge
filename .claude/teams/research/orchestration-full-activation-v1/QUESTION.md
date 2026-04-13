# QUESTION — orchestration-full-activation-v1

**Session date**: 2026-04-12
**Slug**: orchestration-full-activation-v1
**Lead**: research-lead (adopted-persona mode, v2 protocol)
**Sibling sessions in flight**: engineering-team-self-evolve-v1, claude-memory-layer-sota-2026q2-deeper, capability-forge-self-evolve-v1

## Raw prompt (verbatim)

> META-TASK: Design the **Orchestration & Full-Activation Protocol** — a concrete mechanism that (a) guarantees EVERY specialist in a running team actually executes, produces evidence, and consumes tokens — not just "the lead being smart and synthesizing mentally" — AND (b) efficiently manages 3-10 teams running in parallel so Akash gets the maximum possible specialist-hours active at once.
>
> This is Akash's explicit pain point: "Many times they just have the smartest guy active but no I want everyone active at all times consuming tokens and credits and etc. I want you to research properly on the same and do this research so we can self-evolve ourselves after it."

## Assumed interpretation (labeled — correctable)

Akash has identified a **real and specific failure mode** in the team protocol: when research-lead runs as an adopted persona (the default, because subagents cannot spawn subagents), it can **short-circuit** by letting a single "smart generalist" lens answer everything while writing perfunctory placeholder-shaped evidence files that satisfy the letter but not the spirit of "every specialist ran." The user is paying on Max plan for 17 × full-Opus lenses and is getting 1 × full-Opus plus 16 × copies of the same lens with different labels.

This failure is invisible because:
- The protocol currently says "write to `EVIDENCE/<name>.md`" without saying what the file must contain.
- No runtime gate checks that the file exists before SYNTHESIS.md is written.
- No audit catches that `EVIDENCE/cartographer.md` and `EVIDENCE/tracer.md` and `EVIDENCE/historian.md` were all written in a single 2000-token stretch of thinking, which statistically cannot represent 3 distinct lens passes.
- Token attribution is not currently exposed per-specialist — the main session sees "research-lead used N tokens" but not "cartographer used X, tracer used Y."
- The retrospector grades outcomes, not activation depth.

The meta-goal is to **weaponize the evidence file as a contract**: every specialist MUST produce a file that meets a schema check before the lead can write SYNTHESIS.md. The schema is tuned to "prevents shortcut, allows efficient honesty" — not so strict that a brief but genuine specialist pass fails, not so loose that a generalist smear passes.

The second goal is **parallel orchestration**: with 3-10 teams running in parallel, the main session needs concrete patterns for launching, tracking, reconciling, and rate-limiting. The current approach ("launch a few background agents and hope") has no observability.

This question has **four delivery dimensions**:
1. **Theory**: what patterns do real multi-agent systems use to guarantee worker execution? What does the research literature say about verification-as-contract? (Historian, github-miner, librarian, linguist domains.)
2. **Design**: name the winning pattern, write the protocol text, write the schema, write the audit script. (Synthesist + skeptic + cartographer domains.)
3. **Integration**: specific PROTOCOL.md v2.1 edits (old/new pairs), research-lead persona edits, CLAUDE.md deltas, engineering-team PROTOCOL.md forward-port. (Lead + scribe domains.)
4. **Validation**: smoke test that proves the enforcement works, token-budget target with numbers. (Empiricist + evaluator domains.)

## Sub-questions

### Theory of multi-agent worker enforcement

1. **How do production multi-agent frameworks guarantee each worker actually runs?**
   AutoGen v0.4+ actor model, LangGraph state machine traversal, CrewAI task assignment, Magentic-One ledger-based orchestration, MetaGPT SOP/role-contract, ChatDev waterfall enforcement, Anthropic's own multi-agent research system — what's the specific mechanism in each, and what's transferable to a file-based persona-dispatch runtime like ours?

2. **What's the precedent for evidence-file-as-contract?**
   GNU Make, Bazel, Snakemake — target existence + hash = task complete. CI systems — job output artifacts as proof-of-execution. Can we port this to "every specialist's markdown file must exist AND pass a schema check before the downstream synthesis is allowed"?

3. **What schema is strict enough to catch shortcuts but loose enough to allow honest efficiency?**
   Minimum line count? Minimum distinct citations? Required sections (Method, Findings, Citations, Confidence)? YAML frontmatter with started/completed/tool_calls_count? What does each threshold catch, and what does each threshold spuriously fail?

### Claude Code runtime enforceability

4. **Can Claude Code hooks enforce "all specialists ran" at runtime?**
   PreToolUse / PostToolUse / Stop / SessionEnd hooks — can a hook block `Write` to `SYNTHESIS.md` if `EVIDENCE/<name>.md` is missing or shallow for any expected specialist? What's the file format, the timing, the failure mode?

5. **Is there a per-agent token attribution mechanism in Claude Code?**
   `/cost` command, session telemetry, the .output JSONL — what's exposed? If nothing, what's the best proxy (file size × token-per-byte estimate, tool call count per specialist section, LOG.md timestamp deltas)?

6. **What's the subagent dispatch model and its limits for parallel teams?**
   Background agents, the `Agent` tool's `run_in_background` option (if exists), rate limits on concurrent API calls, context-isolation guarantees. With 4 concurrent research-lead background agents each running 17 specialists worth of lens passes, are we saturating Anthropic's rate limits? What's the back-pressure behavior?

### Parallel orchestration patterns

7. **How do CI systems and dataflow schedulers handle 100s of parallel jobs?**
   GitHub Actions matrix, Bazel remote execution, Buildkite parallelism groups, Airflow DAG scheduling, Snakemake cluster mode — what are their primitives for launch + track + reconcile + rate-limit, and which translate to "4 Claude Code background agents writing to a shared filesystem"?

8. **What can the main session safely read from a running session without overflowing?**
   LOG.md (append-only, small), evidence file counts, SYNTHESIS.md existence — yes. The .output JSONL (grows unboundedly) — probably not. What's the polling budget?

### MAST failure modes directly applicable here

9. **Which MAST failure modes does "lead-generalist-smear" map to, and which existing v2 gates catch each?**
   FM-1.2 (disobey role specification) — lead ignores the specialist lens.
   FM-1.3 (step repetition) — same lens pass under different names.
   FM-2.4 (information withholding) — findings exist in thinking but never surface.
   FM-3.2 (no or incomplete verification) — SYNTHESIS.md written before evidence exists.
   Which does the v2 protocol already address? Which does it let through?

### Human-factors translation

10. **How do engineering managers enforce "everyone contributes" in human teams?**
    Stand-ups, definition-of-done per role, peer review, acceptance criteria per deliverable, visible artifacts. Which of these translate into LLM-runtime patterns we can actually implement?

## Deliverables (in order of implementation priority)

**D1. Full-activation enforcement protocol** — name the pattern, specify pre-flight (EXPECTED_EVIDENCE.md) + mid-flight (schema-conformant evidence files) + gate (audit before SYNTHESIS.md) + post-session audit. Full protocol text as an update to `~/.claude/teams/research/PROTOCOL.md` (section edits, verbatim old/new pairs).

**D2. Evidence file schema** — exact minimum structure: YAML frontmatter + body sections + thresholds. Enforcement delta over v2's current rule.

**D3. Audit script** — full Python (stdlib only) script `~/.claude/scripts/audit_evidence.py <slug>` returning PASS/FAIL with specific violations. Callable from lead's gate step and from main session for spot checks.

**D4. Orchestration layer design** — main session's launch + track + wait + reconcile + rate-limit + context-safety patterns for N parallel teams. Concrete primitives, not abstractions.

**D5. Cost dashboard** — single-file script `~/.claude/scripts/team_status.sh` listing running teams, workspaces, last modified evidence files, rough token attribution via file sizes.

**D6. PROTOCOL.md v2.1 edits** — exact old/new pairs for research PROTOCOL and for the forthcoming engineering PROTOCOL.

**D7. research-lead.md persona edits** — workflow section enforcing full activation as hard rule + hard gate.

**D8. CLAUDE.md delta** — new "Parallel team orchestration" section.

**D9. Token-budget target** — minimum/maximum spend per session, measurement method.

**D10. Smoke test** — test that proves the enforcement actually catches shortcut. Positive and negative runs.

## Acceptance criteria

- **Full activation**: after applying the protocol, a deliberate short-circuit (lead writes SYNTHESIS.md with 1 real evidence file and 16 stubs) is caught at the gate with specific violation names.
- **Audit script runs**: `python3 ~/.claude/scripts/audit_evidence.py <slug>` on any existing session returns structured PASS/FAIL without tracebacks.
- **Parallel orchestration**: main session has a documented pattern for launching 4 teams, tracking progress via filesystem polls only (no JSONL reads), and reconciling outputs without context overflow.
- **Backward compat**: no currently-in-flight session (the 3 siblings) is broken by the new protocol. All edits additive or opt-in for v2.1 adoption.
- **Token-budget target**: numerical, enforceable, measurable (e.g., "≥ 80KB total EVIDENCE/ contents for a complex research round, with no specialist file < 2KB").
- **Runs within subagent runtime**: no new runtime features, no async spawning, no hook that depends on unimplemented Claude Code primitives. Works today.

## Known constraints

- Subagents cannot spawn subagents. Adopted-persona mode must remain viable; enforcement must work inside it.
- Python stdlib only for the audit script. No pip install, no external deps.
- Must be backward-compatible with v2 protocol so the 3 siblings in flight don't break.
- Must handle the `EVIDENCE/` layout actually in use by the 3 siblings (look at what they wrote) — don't invent a new layout.
- The gate must not be so strict that "honest but brief" specialist output (e.g. a specialist that legitimately found 2 citations and wrote 40 clear lines) fails. Tune for signal, not length.
- Retrospector + scribe close-close races on MEMORY.md are a parallel concern handled by the engineering-team session in flight. Reference their lock protocol, don't duplicate it.

## Scope boundaries

- **In scope**: enforcement protocol, evidence schema, audit script, orchestration patterns, cost dashboard, protocol/persona/CLAUDE edits, token budgets, smoke test.
- **Out of scope**: redesigning the 17 specialist personas, rewriting the v2 round structure, memory-layer design (handled by memory-layer session), capability-forge/skill-meta-agent design (handled by capability-forge session), engineering-team roster (handled by engineering session).

## Why 4 sessions in parallel is itself a validation test

Running this session concurrently with 3 siblings is deliberate: the parallel-team orchestration pattern being designed here IS being validated by the 4-way concurrent run. If all 4 retrospectors race `~/.claude/agent-memory/research-lead/MEMORY.md` at close, we get empirical evidence for the locking protocol the engineering-team session is designing. This session's "parallel orchestration" deliverable must plan for the race and document what happens.
