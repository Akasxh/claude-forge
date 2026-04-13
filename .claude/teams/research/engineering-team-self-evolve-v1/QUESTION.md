# QUESTION — engineering-team-self-evolve-v1

**Session date**: 2026-04-12
**Slug**: engineering-team-self-evolve-v1
**Lead**: research-lead (adopted-persona mode, v2 protocol)

## Raw prompt (verbatim)

> META-TASK: Design the **Engineering Team** as the second leader-led sub-team in Akash's architecture, following the self-evolution principle that produced Research Team v2. ALSO produce the cross-team handoff protocol and the parallel-instance memory/context segregation model for running multiple team instances concurrently without race conditions or context pollution.
>
> This is the same self-evolution pattern you used for yourself: research the design space, draft the team, validate with adversarial gates, deliver ready-to-write files. Follow PROTOCOL.md v2 exactly.
>
> Constraint: "a team of planners and executers that are **together**" — single unified team with both planning and execution roles under one leader. NOT separate Planning and Execution teams.
>
> Deliverables: full engineering agent roster, ~/.claude/teams/engineering/PROTOCOL.md, memory/context segregation protocol, cross-team handoff, orchestration protocol, CLAUDE.md deltas, smoke test.

## Assumed interpretation (labeled — correctable)

Akash is building a **team-of-teams** architecture on top of Claude Code. Research Team v2 is proven (memory-layer SOTA session ran with 5 gates, v2 protocol validated end to end, 12 MEMORY.md lessons accumulated). This session builds **Team #2: Engineering** on the same substrate, with five critical elaborations beyond a naive "clone research, swap the verbs":

1. **Unified planner+executor** under one `engineering-lead`, not two separate teams. The "together" constraint rules out the common MetaGPT / ChatDev waterfall split where PMs and devs are separate crews that hand specs across an organizational boundary. Akash wants the decomposition and the execution to happen in the same workspace, same lead, same ledger — so architects can walk back a plan when executors discover something, and executors can escalate to architects mid-implementation without a cross-team ping.

2. **Cross-team handoff protocol** (Research → Engineering, Engineering → Research feedback loop). The handback shape matters because: (a) the research SYNTHESIS.md becomes a binding input spec; (b) when engineering discovers the research was wrong, the feedback has to go back through a structured channel, not a verbal complaint; (c) what actually shipped must be logged back into the research workspace so future research sessions can see what happened to their recommendations.

3. **Parallel-instance memory segregation**. This is the load-bearing technical problem — Akash wants to run multiple team instances simultaneously (research on topic X while engineering implements Y, two research sessions at once, etc). The current `~/.claude/agent-memory/research-lead/MEMORY.md` is a single mutable file. Two concurrent retrospectors writing to it race. The segregation protocol must work on the actual Claude Code runtime using pragmatic Unix primitives (flock advisory locks, atomic rename, append-only staging), not theoretical CRDTs.

4. **The self-evolving principle**: Research Team v2 itself came out of a research session. Engineering Team v1 should come out of a research session on engineering-agent design. That's what this session IS. The meta-loop is: research to design the team, then smoke-test by using the team on a real first task.

5. **Prior art bar is set high**: this is the second team, not the first, and the prior-art sweep already happened once. Expectations are now "beyond what you can pattern-match from Anthropic's published guidance" — SWE-bench-verified leaderboard trends, Devin/SWE-agent/OpenHands production lessons, the plan-and-execute vs ReAct debate, concurrency patterns in real multi-agent frameworks, and an honest adversarial pass on the SEO-gamed "AI engineering agents" corpus which (per Akash's framing) is the next big contested space after "AI memory."

The answer must be **ready-to-write files with zero placeholders** — every persona markdown, every protocol section, every CLAUDE.md old/new pair, every launch prompt verbatim. This is an executor-grade deliverable, not a design document.

## Sub-questions

**Team design**
1. What roster does the Engineering Team need? The meta-task lists 11 candidate specialists — are all 11 load-bearing, should any be cut, should any be added? What MAST failure mode does each own?
2. Should the team be **flat** (all specialists report to engineering-lead), **hierarchical** (sub-leads for plan/execute/verify), or **pipeline** (waterfall stages with explicit handoffs)? The "together" constraint pushes toward flat, but the planner→executor→verifier ordering is inherently sequential — how do we reconcile?
3. What is the round structure? Research Team v2 uses Round 0 (frame) → Round 1 (wide opener) → Round 2 (gates) → Round 3 (evaluator) → close. Engineering is not a research activity; it is a produce-correct-code activity. The round structure must match that.
4. **Plan-and-execute vs incremental ReAct**: should engineering-lead commit to a full plan first and then execute (Plan-and-Solve prompting, orchestrator-worker), or execute incrementally with replanning after each step (ReAct, Reflexion)? Where does the plan-review gate sit?
5. How does engineering-skeptic differ from engineering-adversary? In research, skeptic attacks reasoning and adversary attacks the corpus. In engineering, what are the two lenses? Skeptic attacks the plan, adversary attacks the external inputs (research SYNTHESIS, library docs, task spec).
6. What is the "evaluator" rubric for engineering? Research uses Anthropic's 5-dim (factual, citation, completeness, source quality, tool efficiency). Engineering rubric candidates: functional correctness, test coverage, diff minimality, style conformance, revert-safety, performance non-regression, security. Which make the cut?

**Cross-team handoff**
7. What structured handoff contract reads a Research SYNTHESIS.md and produces a binding engineering CHARTER.md? What fields does CHARTER.md need?
8. When engineering disagrees with research (research was wrong, the recommended library is broken, the benchmark numbers don't reproduce), how does the feedback flow back to research? What file, what escalation?
9. When engineering completes, what handback artifact goes to the research session's workspace? Closing loop so the next research session can see what actually shipped.

**Parallel-instance concurrency**
10. How do N team instances write to `~/.claude/agent-memory/research-lead/MEMORY.md` without racing?
11. File-layout: how do per-session staging files merge into the canonical MEMORY.md atomically?
12. What is the lock primitive? flock(2) advisory vs fcntl byte-range vs SQLite WAL vs CRDT append-only log — which is the pragmatic-and-correct choice for Claude Code's runtime (multi-process bash commands launched from a single agent session)?
13. What happens if the lock contends — block, retry, defer, or fail? What's the recovery path if a merge is deferred?
14. Are readers safe during a writer-in-progress state? MEMORY.md is read by lead, planner, retrospector at different phases — what's the consistency guarantee?

**Prior art**
15. What does Anthropic's own engineering-agent guidance say (Claude Agent SDK, "Building effective agents", SWE-bench blog, agent-teams docs)? Where does our design differ and why?
16. What are the production SWE-agents doing in 2026 (Devin, SWE-agent, OpenHands, Aider, Cursor Agent, Replit Agent)? What are their public failure modes and benchmark contestations?
17. What does MetaGPT / ChatDev / AutoGen / CrewAI do differently for "engineering crews"? What have they learned in production?
18. Where does the plan-and-execute vs ReAct line fall in 2026 practice? Who committed to which, what did the post-mortems say?
19. What do code-review-as-agent tools (CodeRabbit, Graphite, Qodo) use for review protocol? Review-as-agent vs review-as-step.
20. What does the 14-day freshness sweep find? (Lesson from memory-layer v2: short prompts on fast-moving topics deserve a "newest-14-days" sub-question as a structural sweep. "AI engineering agents" is exactly that kind of topic.)

**Smoke test**
21. What's the minimum concrete engineering session that proves the team works end to end? Pilot session proposal.

## Acceptance criteria

- **Complete roster**: 10–14 engineering specialist files with frontmatter (name, description, model=opus, effort=max, color optional), persona body, method, deliverable spec, hard rules. Every specialist has a named MAST failure mode it owns.
- **Full PROTOCOL.md**: mirrors research PROTOCOL v2 structure, includes roster table with MAST ownership, model contract, execution model, toolbox, handoff contract section, workspace layout, ownership rules, round structure with explicit gates, confidence scale, escalation rules, prior-art list with retrieval dates.
- **Concurrency protocol is concrete**: exact directory layout, exact lock primitive choice with justification, exact merge algorithm, exact failure-mode text for contended-lock, exact readers-consistency guarantee. Not "consider CRDTs" — "use flock with 5s timeout, here is the shell snippet."
- **Cross-team handoff is concrete**: exact CHARTER.md template with field list, exact path convention for research→engineering handoff, exact FEEDBACK_FROM_ENGINEERING.md template, exact handback artifact name and contents.
- **Orchestration rules**: how the main session launches teams in parallel with `Agent()` and `run_in_background: true`, what's safe to read from outside, what's not safe.
- **CLAUDE.md deltas**: exact old/new strings for Edit tool calls, three locations (Currently available teams section, Teams under construction section, Dispatch rules section).
- **Smoke test**: exact launch prompt, exact files the smoke test should produce, exact acceptance criteria for "v1 protocol works."
- **All 5 gates run**: planner, wide dispatch (≥8 lenses), synthesist, moderator on load-bearing contradictions, skeptic, adversary, evaluator PASS.
- **Retrospector extracts ≥3 lessons** to `~/.claude/agent-memory/research-lead/MEMORY.md`.

## Known constraints

1. **Subagent spawn constraint**: Claude Code subagents cannot spawn other subagents. Research-lead handles this via "adopted persona pattern 2" — execute specialist methods directly when invoked as subagent. Engineering-lead must adopt the same pattern. Document it in the persona file and the protocol.
2. **All Opus max effort**: every agent `model: opus` + `effort: max` in frontmatter. No downgrades, no exceptions.
3. **Ready-to-write, zero placeholders**: the deliverable IS the file contents, not a specification of what the files should contain. The close of this session must leave Akash able to paste the final answer directly into the Write tool.
4. **Name prefix**: specialists must be `engineering-*` to avoid collision with existing flat agents (`planner`, `architect`, `executor`, `verifier`, `code-reviewer`, etc — these remain untouched).
5. **File-backed coordination**: everything goes through `.claude/teams/engineering/<slug>/` files, never via conversational context.
6. **Pragmatism over theory on concurrency**: the concurrency design must work on the real Claude Code runtime using Unix primitives Akash already has (bash, flock, mv, rename). No new dependencies.
7. **Workspace**: session lives under `~/.claude/teams/research/engineering-team-self-evolve-v1/` because it is a research session about engineering team design. When engineering-team-v1 is ready, it may be used to implement things and will have its own workspace at `~/.claude/teams/engineering/<slug>/`.

## Blind spots I want flagged

- If the roster is bigger than research (17 + lead = 18), justify. If smaller, justify. The count itself is a design decision.
- If the round structure adds a step research doesn't have, name it and say why.
- If the concurrency protocol adds latency to the critical path (normal single-session case), flag it — the design must not tax the common case to solve the parallel-instance case.
- If any specialist is cargo-culted from research without engineering-specific content, call it out.
- If the adversary pass finds "AI engineering agents" is as SEO-gamed as memory was, the design must survive that corpus attack.

## Session plan signal

Complex research (per Anthropic's scaling rule). Complexity comes from the prior-art sweep breadth (8+ source lenses), the concurrency engineering work (needs tracer + empiricist on real flock semantics), and the adversarial requirement (contested corpus). Expected ~8-10 specialists on the wide opener, 3 rounds, evaluator-pass target.

## Anchor to prior sessions

- `~/.claude/teams/research/claude-memory-layer-sota-2026q2/` — the v2 pilot session, provides HIGH-confidence template and 5 fresh retrospector lessons (lessons 8–12 in MEMORY.md). Reuse the SYNTHESIS.md shape, the evidence-file discipline, and especially the REFRAME moderator verdict pattern.
- `~/.claude/teams/research/PROTOCOL.md` — the v2 protocol this session follows exactly.
- `~/.claude/agent-memory/research-lead/MEMORY.md` — 12 binding lessons. Load-bearing for dispatch planning.
