# Planner — dispatch recommendation for orchestration-full-activation-v1

## Question classification

- **Question class**: hybrid — **prior-art sweep** (what do production multi-agent systems do?) + **decisional** (which enforcement strategy to adopt) + **diagnostic** (why does the current protocol allow smear?) + **meta-design** (write the protocol edits). The dominant shape is **decisional with heavy prior-art foundation**, because the four H1–H4 hypotheses must be selected-among using evidence from the literature and the Claude Code runtime.
- **Complexity**: **complex research**. Anthropic's scaling rule says 5–10+ specialists, multi-round. This matches what Akash explicitly requested ("Round 1: 8 specialists wide").
- **Anthropic scaling rule says**: 8 specialists on the opener, 3+ parallel tool calls per specialist, 2–3 rounds to high confidence.
- **Past lessons from MEMORY.md that apply**:
  - *"Dispatch breadth follows Anthropic's published scaling rule"* — go wide on complex, use 8+ specialists in round 1.
  - *"Parallel tool calling is a 10x force multiplier"* — all round-1 specialists must be dispatched in ONE inline block; all WebFetch/WebSearch calls per specialist must be parallel where the content is independent.
  - *"Subagents cannot spawn subagents — plan accordingly"* — THIS session is running as a subagent; the specialist files become behavioral contracts, the lens-passes execute inline, the evidence files are written by the lead under each specialist's contract. **This is the exact failure mode being investigated.**
  - *"The skeptic attacks reasoning; the adversary attacks the corpus"* — both run; corpus-level adversary pass on the "AI agent frameworks" literature is required because MetaGPT/CrewAI/AutoGen/LangGraph benchmark claims are an SEO-gamed space.
  - *"Reuse v1 evidence on rerun; append addenda, don't rewrite"* — not applicable (first run).
  - *"REFRAME is a valid moderator verdict"* — applicable: the 4 hypotheses may not be mutually exclusive; moderator likely reframes to composition.
  - *"When the user prompt is short, distrust your initial sub-question list to catch the latest 14 days"* — applicable: multi-agent infra is producing weekly arxiv submissions. Add a "newest 14 days" probe for LangGraph 2.0 / AutoGen 0.5 / Magentic-One-v2 / Anthropic agent-teams Apr 2026 drops.
  - *"REPORTED-NOT-VERIFIED is a valid evidence tier"* — applicable: some Claude Code hook semantics may only be documented in changelog snippets or community posts; evidence tiering matters.

## Recommended opening dispatch (Round 1)

**Parallel dispatch of 8 specialists in ONE lens-pass block** (within
adopted-persona mode, this means 8 distinct method executions written
to 8 distinct evidence files with 8 distinct vocabularies and tool-call
profiles — the gate being designed here will enforce this on future sessions).

1. **research-historian** — Multi-agent framework landscape survey. Find concrete mechanisms for worker-execution enforcement in AutoGen v0.4+ (actor model), LangGraph (state machine), CrewAI (task contracts), Magentic-One (ledger), MetaGPT (SOP), ChatDev (waterfall), Anthropic's published multi-agent research system, and any Apr 2026 arXiv prior art on "verification of agent execution" / "file-based agent contracts" / "evidence-as-contract." Owned MAST: FM-1.1 prior-art gap.

2. **research-github-miner** — Code-level survey of how the frameworks above actually implement worker-execution enforcement. Read AutoGen runtime source for actor ack/nack, LangGraph source for state-node completion checks, CrewAI source for task-result validation, any relevant GitHub issues about "agent didn't run" or "worker skipped" with resolution commits. Star velocity + release cadence as health signal. Owned MAST: FM-1.1 GitHub corpus gap.

3. **research-librarian** — Official Claude Code docs on hooks (PreToolUse, PostToolUse, Stop, SessionEnd, UserPromptSubmit), background agents, `run_in_background`, session telemetry, `/cost`, and any published rate-limit guidance. Need exact semantics: do hooks fire for subagent tool calls? Does a SessionEnd hook see sibling-session files? This is the load-bearing technical unknown for H3. Owned MAST: FM-1.1 version-drift.

4. **research-cartographer** — Structural mapping of the existing research team workspace. Inventory how every sibling in-flight session actually uses `EVIDENCE/` (what files, what structure, what naming). Document the de-facto schema the 3 siblings already follow so v2.1 is backward-compatible. Map `~/.claude/teams/`, `~/.claude/agents/research/`, `~/.claude/agent-memory/`, `~/.claude/lib/`, `~/.claude/hooks/` to understand the host filesystem. Owned MAST: FM-1.2 structural gap.

5. **research-empiricist** — Runs **three live experiments**: (a) does a PreToolUse hook on Write fire when a subagent invokes Write, or only for main-thread? (b) what's the concurrent rate-limit behavior with N Python subprocesses calling an Anthropic-style endpoint fast? (c) does a stdlib-only Python audit script against a real in-flight session workspace execute cleanly and produce correct PASS/FAIL? Each experiment has a prototype script, a raw-output block, and a conclusion. Owned MAST: FM-3.2 untested claim.

6. **research-linguist** — MAST failure-mode map. Read the MAST paper's FM-1.2, FM-1.3, FM-2.4, FM-3.2 definitions and map each to specific observable behaviors in our team. Define a vocabulary-signature metric for H2 ("lead-generalist-smear detected when Jaccard similarity across N evidence files > T") — what's T, and what's the false-positive rate on honest-but-related specialists? Owned MAST: FM-2.6 polysemy.

7. **research-web-miner** — 2026 prior art and industry discussion. HN Algolia search for "agent verification" / "multi-agent observability" / "worker execution contract" / "agent teams" / "Claude Code hooks". Reddit r/LocalLLaMA + r/LangChain + r/LLMDevs on agent orchestration. X.com for Anthropic engineering threads, Magentic-One authors, any Apr 2026 framework announcements. Raw corpora cached under `EVIDENCE/web-miner/raw/`. Owned MAST: FM-1.1 web corpus gap.

8. **research-tracer** — Runtime execution trace through the current v2 protocol. Take the sibling `engineering-team-self-evolve-v1` workspace as a live example; trace exactly which evidence files were written, what token-proxy they represent, and simulate the "lead-generalist-smear" failure mode against it — if the audit script being designed here ran against that workspace, would it PASS or FAIL? This is the live-fire diagnosis of the current protocol's enforcement gap. Owned MAST: FM-1.2 causal gap, FM-3.2 untested verification.

## Recommended follow-ups (Round 2)

- **research-synthesist** — unconditional. Reads all 8 round-1 evidence files, builds claim matrix, flags contradictions between hypotheses (e.g., if linguist says vocabulary signatures have 30% false-positive rate but historian says Magentic-One uses exactly that metric successfully, that's a load-bearing contradiction).
- **research-moderator** — conditional on synthesist flagging a contradiction. Most likely contradiction: H3 (hook-based) vs H1+H4 (contract-based) on "what's actually implementable in Claude Code subagent runtime." 3-round structured debate with REFRAME available.
- **research-skeptic** — unconditional. Red-teams the winning composition: "is any of this actually enforceable within the Claude Code subagent runtime given the specific failure mode Akash named?" Attacks the leading hypothesis and identifies unstated assumptions in the synthesis.
- **research-adversary** — unconditional. Audits the prior-art corpus: are the Magentic-One / LangGraph / AutoGen claims in the historian/github-miner/web-miner evidence files actually first-party and reproducible? Any astroturf? Any "my new agent framework is 10x better" posts that need to be marked REPORTED-NOT-VERIFIED?

## Recommended gates

- **skeptic**: after Round 1 evidence + synthesist, mandatory before "high confidence."
- **adversary**: after Round 1, mandatory because 3 of 8 specialists (historian, github-miner, web-miner) pull from web/community sources. Adversary writes once, may run in parallel with skeptic since they operate on disjoint targets.
- **evaluator**: always last, after skeptic AND adversary AND moderator. 5-dimension rubric.
- **retrospector**: session close, unconditional. Writes the lessons from THIS session to MEMORY.md — and this session's lessons are high-priority since they're about the memory/enforcement mechanism itself (meta-reflective entries).

## Blind spots I flag

- **I did NOT recommend research-archaeologist**. Rationale: this session is not about the git history of any specific repo; the "evolutionary pressure" frame doesn't apply to a greenfield protocol design. But: if the sibling engineering-team session already shipped a lock-protocol design, the archaeologist could read its git history to identify what failed in v1 attempts. **Lead should second-guess this if time permits.**
- **I did NOT recommend research-adversary in Round 1**. Rationale: adversary normally runs after synthesist so it has a consolidated corpus to attack. Moving it to Round 1 would be premature. Standard order.
- **I did NOT explicitly call out Context7/HF library skills**. Librarian will reach for them if applicable, but the target ("Claude Code hooks") may not be in Context7. The librarian's method already falls back to WebFetch on the official docs URL.
- **I did NOT flag a 14-day fresh window scan as a separate specialist**. Rationale: the historian's prior-art sweep naturally includes recent arXiv; the web-miner's HN/Reddit sweep naturally includes recent posts. If both miss a high-signal Apr 2026 release, that's a legitimate Round 2 re-dispatch target.

## Expected rounds to high confidence

**2 rounds** (range: 2–3).

- Round 1 (wide opener: 8 specialists parallel, lens-passes inline) produces the raw evidence base.
- Round 2 (synthesist → moderator on H1/H2/H3/H4 contest → skeptic → adversary → empiricist smoke test → evaluator) closes the gates.
- Round 3 only if evaluator FAILs a dimension, typically citation-accuracy or tool-efficiency.

This is a meta-design session: the evaluator rubric grades the *artifacts* (schema, script, protocol edits, smoke test), not a factual answer. Expect tool-efficiency to be the tight dimension because we're producing runnable code.

## Budget check

- Complex research dispatch: 8 specialists × ~2 rounds × Opus = ~150K–300K tokens depending on how much tool-call volume each specialist needs (empiricist has bash experiments, web-miner has WebFetch caches, github-miner has `gh api` calls).
- **Explicit per-specialist token-proxy target (to ALSO validate the enforcement protocol being designed)**:
  - Each evidence file: **2 KB minimum, 10 KB typical, 30 KB maximum**
  - Total EVIDENCE/ for Round 1: **80–150 KB** expected
  - LOG.md: **2–5 KB** (one line per event)
  - SYNTHESIS.md: **15–40 KB** (this is the meta-design deliverable)
- Okay for this question? **Yes** — this is a high-value self-evolution session. Akash explicitly wants tokens consumed.

## Confidence in this plan

**High**. The 8-specialist roster cleanly covers prior-art (historian, github-miner, web-miner), runtime unknown (librarian, empiricist, tracer), structural grounding (cartographer), and MAST theory (linguist). Round 2 is unconditional-mandatory with synthesist + skeptic + adversary, optional-contingent with moderator (almost certainly triggered by H1-vs-H3 contradiction). The budget is high but justified — this session's output is a protocol that will be applied to every subsequent research session.

**One lesson I'm watching out for**: the *lead-generalist-smear* failure mode I'm designing against IS THE EXACT FAILURE MODE this session is at risk of committing during its own Round 1. If the 8 lens-passes below all read identical and have overlapping vocabulary, the session itself will fail the audit script when it's applied against this workspace. **The smoke test at the end should include running the new audit against THIS session's own EVIDENCE/ directory — if my own work fails the gate, the gate is correctly calibrated; if it passes, I'll need to tighten thresholds.**
