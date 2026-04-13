# Planner — dispatch recommendation for engineering-team-self-evolve-v1

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Author: research-planner (adopted-persona mode)

## Question classification

- **Question class**: **meta-design** (cross between prior-art + decisional + structural). The lead is not asking "what is the truth about X" — it's asking "design artifact Y using published prior art, validate with gates, deliver files." This shape is rare. It is closest to "Should we adopt Y?" (decisional) crossed with "What's the prior art on approach W?" (prior-art).
- **Complexity**: **complex research**, Anthropic scaling rule lower bound 5+, upper bound 10+. The prior-art sweep alone touches 8 distinct corpora (Anthropic docs, SWE-bench agents, multi-agent frameworks, plan-vs-ReAct literature, code-review tools, test-gen tools, concurrency patterns, human-factors) and the output is a design that must survive an adversarial gate. Under-dispatch (< 6) would guarantee a session the adversary can tear apart.
- **Anthropic scaling rule says**: dispatch 8-12 specialists parallel on the opener, aim for high end.
- **Past lessons from MEMORY.md applicable**:
  - **Dispatch breadth follows Anthropic's published scaling rule** — go wide, planner runs before opener, opener is one parallel emission. Confirmed applicable.
  - **Parallel tool calling is a 10x force multiplier** — every specialist runs parallel tool calls. Confirmed applicable.
  - **Skeptic attacks reasoning, adversary attacks corpus** — "AI engineering agents" corpus is contested (SWE-bench gaming, Devin demo scandal); adversary pass is NOT optional. Confirmed applicable.
  - **Contradictions go to moderator** — phase-vs-flat will almost certainly produce a synthesist-flagged contradiction. Mod gate will run.
  - **End-state evaluation beats path evaluation** — final output must be ready-to-write files, not a plan-for-a-plan. Confirmed applicable.
  - **Self-improvement lives in MEMORY.md** — retrospector will extract lessons. Confirmed applicable.
  - **Subagents cannot spawn subagents** — this session runs in adopted-persona mode. Engineering-lead must inherit this constraint and its persona file must document it.
  - **Short prompts on fast-moving topics deserve 14-day freshness sweep** — "AI engineering agents" is exactly that. MANDATORY web-miner sub-question: "what did Devin/SWE-agent/OpenHands/Aider ship in the last 14 days, and did SWE-bench-verified leaderboard move."
  - **Adversary catches corpus-level fraud that skeptic cannot** — SWE-bench gaming is the engineering-agent analogue of MemPalace fraud. Pre-emptively dispatch adversary.
  - **REFRAME is a valid moderator verdict** — phase-vs-flat may be mis-posed ("they're not mutually exclusive in the same way we think"). Moderator must be allowed REFRAME.
  - **Reuse v1 evidence on rerun; append addenda, don't rewrite** — N/A this is v1 of engineering-team, but the protocol pattern for adoption is set: if a future rerun happens, addenda files are preferred.
  - **REPORTED-NOT-VERIFIED is a valid evidence tier on paywalled primaries** — Devin's internal design is partially paywalled (blog posts + demo videos, no technical whitepaper as of retrieval date). Apply this tier.

## Recommended opening dispatch (Round 1)

Parallel dispatch of **10 specialists** in ONE message, per the scaling rule's upper-end recommendation for complex multi-corpus research.

### 1. `research-librarian` — Anthropic's engineering-agent canon
**Sub-question**: What does Anthropic itself publish about engineering-agent design? Specifically load `anthropic.com/engineering/multi-agent-research-system`, `anthropic.com/research/building-effective-agents`, `claude.com/blog/building-agents-with-the-claude-agent-sdk`, `code.claude.com/docs/en/sub-agents`, `code.claude.com/docs/en/agent-teams`, and any Claude Code blog post about SWE-bench. Extract the canonical patterns: orchestrator-worker, evaluator-optimizer, workflow-vs-agent distinction, gather-act-verify-repeat, rules-based verification, subagent constraint. Map each pattern to which of our 5 hypotheses it supports. Write to `EVIDENCE/librarian.md`.
**Owns failure mode**: FM-1.1 (version-drift on Anthropic's published guidance).
**Tool calls expected**: 10-15 WebFetch + citation lookups.

### 2. `research-historian` — SWE-bench production agents and plan-vs-ReAct debate
**Sub-question**: What does the prior art on production SWE-bench agents look like in 2026? Investigate Devin (Cognition), SWE-agent (Princeton), OpenHands (formerly OpenDevin, All-Hands.dev), Aider (Paul Gauthier), Cursor Agent, Replit Agent, Windsurf Cascade, Claude Code's own agent. For each, collect: (a) public architecture description, (b) SWE-bench-verified score (most recent), (c) known failure modes from issue trackers, (d) plan-vs-ReAct positioning. Cross-reference with the Plan-and-Solve prompting, ReAct, Reflexion, Self-Refine papers. Secondary: MetaGPT, ChatDev, AutoGen, CrewAI engineering crews — what SOPs did they commit to and why? Write to `EVIDENCE/historian.md`.
**Owns failure mode**: FM-1.1 (prior-art gap).
**Tool calls expected**: 20-30 searches + WebFetch + paper-abstract reads.

### 3. `research-web-miner` — 14-day freshness sweep + HN/Reddit sentiment
**Sub-question**: What shipped in the last 14 days in AI engineering agents? SWE-bench-verified leaderboard changes since March 29, 2026? New SWE-agent release? Devin 2.0? Aider weekly releases? HN front page discussions about SWE-bench gaming in the last 30 days? Reddit r/LocalLLaMA / r/MachineLearning threads? X.com search for "SWE-bench leaderboard 2026" (logged-in Playwright)? Also: what does the community say about plan-and-execute vs ReAct in practice, not theory? Apply MEMORY.md lesson 9: "short prompts on fast-moving topics deserve 14-day freshness sweep as structural sub-question, not discretionary." Write to `EVIDENCE/web-miner.md`.
**Owns failure mode**: FM-1.1 (web corpus gap), FM-3.3 (staleness).
**Tool calls expected**: 15-25 Playwright navigate + HN Algolia + Reddit JSON + arXiv.

### 4. `research-github-miner` — cross-repo engineering-agent patterns
**Sub-question**: What do the top production engineering-agent repos look like structurally? `gh api` and `gh search` for: princeton-nlp/SWE-agent, all-hands-ai/OpenHands, paul-gauthier/aider, geekan/MetaGPT, OpenBMB/ChatDev, microsoft/autogen, joaomdmoura/crewAI, anthropics/claude-code. For each: (a) directory structure of agent personas, (b) coordination mechanism (files? messages? mailboxes? tasks?), (c) number of agent roles, (d) how they handle "planner wants to change the plan mid-execution", (e) how they handle failure recovery, (f) star velocity + issue volume as a sentiment signal. Cross-repo compare. Write to `EVIDENCE/github-miner.md`.
**Owns failure mode**: FM-1.1 (GH corpus gap).
**Tool calls expected**: 20-30 gh api + gh search calls. Use GraphQL where helpful to batch. Cache raw responses to `EVIDENCE/github-miner/raw/`.

### 5. `research-tracer` — Unix concurrency primitives for MEMORY.md segregation
**Sub-question**: What is the pragmatic-and-correct concurrency primitive for "N Claude Code sessions running bash commands that read and write `~/.claude/agent-memory/research-lead/MEMORY.md` without racing"? Investigate: (a) `flock(1)` vs `flock(2)` semantics on Linux — advisory vs mandatory, timeout behavior, inheritance across exec; (b) `fcntl(F_SETLK)` byte-range locks; (c) atomic rename via `mv` on same filesystem (POSIX guarantee); (d) SQLite WAL mode; (e) CRDT append-only log on-disk; (f) git as storage layer (plumbing commands). For each, answer: does it work for multi-process bash launched from separate Claude Code sessions? What's the failure mode? What's the recovery? Recommend the primitive, write the exact shell snippet. Trace the actual runtime path: Claude Code session A calls Bash tool → spawns `flock -w 5 .lock -c 'merge.sh'` → what happens if session B is mid-merge? Write to `EVIDENCE/tracer.md`.
**Owns failure mode**: FM-1.2 (causal gap in concurrency reasoning).
**Tool calls expected**: 10-15 `man` page WebFetch + POSIX spec lookup + Linux-manpages.org.

### 6. `research-empiricist` — test flock semantics on this actual system
**Sub-question**: Does `flock -w 5` actually work on this Linux box? Run real experiments: (a) two terminals, both try to acquire the same lock file with `flock -w 3 /tmp/test.lock -c 'sleep 2; echo done'` — does the second wait 3s then fail, or succeed? (b) what happens if the holder dies mid-critical-section — does the lock auto-release? (c) does `mv /tmp/x.tmp /tmp/x.final` atomically replace on ext4 / btrfs? (d) can a subprocess spawned from a Claude Code bash call hold a lock after the bash call returns? (e) what's the maximum safe timeout before the user notices a stall? Produce a table of observed behaviors, raw-output blocks. Flag any unexpected behavior that contradicts the tracer's manpage-based reasoning. Write to `EVIDENCE/empiricist.md`.
**Owns failure mode**: FM-3.2 (untested claim about concurrency).
**Tool calls expected**: 5-10 Bash experiments with raw outputs captured.
**NOTE**: Empiricist runs in Round 1b (after tracer delivers), because the empiricist's experiments need the tracer's primitive-choice to target. Serial dependency.

### 7. `research-cartographer` — existing flat agents + research team structure map
**Sub-question**: Inventory the existing agent ecosystem in `~/.claude/agents/`. What flat agents exist that could be wrapped or imitated? What naming collisions would occur if we use `engineering-*`? What structure does `~/.claude/agents/research/` use that we should mirror? What does `~/.claude/teams/research/` vs `~/.claude/teams/engineering/` layout look like today, and what needs to change? Produce a dependency graph: engineering-lead → engineering-*, existing flat `planner`/`executor`/`verifier` → unchanged (parallel ecosystem). Write to `EVIDENCE/cartographer.md`.
**Owns failure mode**: FM-1.2 (structural gap in existing ecosystem).
**Tool calls expected**: 10-15 Read + Glob.

### 8. `research-linguist` — vocabulary of the 5 hypotheses and existing flat agents
**Sub-question**: Polysemy audit. "Planner" is an overloaded word: oh-my-claudecode's `planner.md` is an interview-and-save-plan role; `architect-planner.md` is a blueprint-writer; research uses `research-planner` as a dispatch-advisor. Engineering-team "planner" must pick one meaning and commit. Same for "executor", "verifier", "reviewer". Produce a glossary: for each term, the meanings in the existing corpus, the meaning engineering-team should commit to, and why. Also audit the hypothesis names for semantic drift — "flat" vs "pipeline" vs "phase" — what do these actually mean in the multi-agent literature? Prevent synthesist from reporting a false contradiction rooted in polysemy. Write to `EVIDENCE/linguist.md`.
**Owns failure mode**: FM-2.6 (polysemy, reasoning-action mismatch).
**Tool calls expected**: 5-10 Read + Grep.

### 9. `research-archaeologist` — git history of research-team self-evolution
**Sub-question**: Read `~/.claude/teams/research/PROTOCOL.md` and `~/.claude/teams/research/PROTOCOL.v1.bak`. What changed from v1 to v2, and why? What lessons from the v2 self-evolution apply to v1-of-engineering? Walk the git history of `~/.claude/agents/research/` if there is one. Check `~/.claude/teams/research/claude-memory-layer-sota-2026q2/LOG.md` + `SYNTHESIS.md` for evolutionary pressure — what did the pilot session reveal that changed the team design? Also audit whether there's anything in `~/.claude/teams/research/INDEX.md` to learn from. Write to `EVIDENCE/archaeologist.md`.
**Owns failure mode**: FM-1.1 (historical gap — missing the lessons v2 itself encoded).
**Tool calls expected**: 5-10 Read + Glob.

### 10. `research-skeptic` — pre-emptive red team on H3 (unified hybrid)
**Sub-question**: The leading hypothesis is H3 (unified hybrid: flat roster, two-phase Plan/Build round structure, plan-skeptic gate at phase boundary, verifier+reviewer per inner iteration). Produce ≥ 3 competing hypotheses that are consistent with what we know so far. Audit H3's unstated assumptions: what if Phase A discovers it needs Phase A again? What if the "variable N" inner loop drifts? What if the plan-skeptic gate is weak because the skeptic doesn't have executable verification? What if MAST FM-1.5 (termination unawareness) eats the inner loop? Produce a red-team report that the Round 2 skeptic will be able to refine after the wide opener returns. Pre-emptive, not final skeptic — final skeptic runs AFTER synthesist in Round 2. Write a **preliminary** `EVIDENCE/skeptic-preliminary.md` (not skeptic.md, which is reserved for the Round 2 pass).
**Owns failure mode**: FM-3.3 (incorrect verification via premature convergence).
**Tool calls expected**: 5-10 Read of hypothesis file + prior art as it arrives.

## Recommended follow-ups (Round 2)

- **`research-synthesist`** (unconditional — always after Round 1): builds a claim matrix across all Round 1 evidence, flags load-bearing contradictions. Produces `EVIDENCE/synthesist.md`.
- **`research-moderator`** (conditional — if synthesist flags a contradiction): run 3-round debate on each load-bearing contradiction. My prediction: the biggest debate will be "should the build phase be a fixed-N pipeline OR a variable-N ReAct loop" — this is the H2 vs H3 crux. Moderator must be allowed REFRAME (per MEMORY.md lesson 11).
- **`research-skeptic`** (unconditional — MANDATORY round 2): full pass on the synthesis draft, not the preliminary pass. Attacks the leading design post-wide-opener.
- **`research-adversary`** (unconditional — MANDATORY round 2): the engineering-agent corpus is contested. SWE-bench gaming is real. Devin benchmark claims have been disputed on X / Twitter. "AI engineering agents" Medium content is AI-generated SEO. Run corpus audit, reject weak sources, produce MIXED / REJECTED / REPORTED-NOT-VERIFIED classifications for every URL the historian + web-miner + github-miner cited.
- **`research-empiricist`** (Round 1b serial — after tracer): runs the flock experiments on this system.

## Recommended gates

- **Synthesist**: Round 2 opener, mandatory.
- **Moderator**: Round 2, conditional on synthesist-flagged contradictions. Expect 1-3 debates.
- **Skeptic**: Round 2, mandatory before "high confidence" stamp.
- **Adversary**: Round 2, mandatory. "AI engineering agents" corpus quality is not optional.
- **Evaluator**: Round 3, mandatory, always last before delivery.
- **Retrospector**: session close, unconditional.

## Blind spots I flag

- **I did not recommend a dedicated "design-empiricist"** specialist to actually build a prototype of the engineering team and dry-run it. The reason: that's what the smoke test at session close is for, not a round-1 dispatch. But the lead should second-guess this if the final design has no "is this buildable at all" validation.
- **I recommended only one concurrency specialist (tracer) + one experimentalist (empiricist)**. If the wide-opener reveals the flock choice is non-obvious (e.g. flock has weird NFS semantics that breaks on some setups), a second concurrency specialist may be needed. Flag for lead.
- **I did not recommend an adversarial pass ON the linguist's work**. Rationale: linguist is a clarifying lens, not a claim-maker — adversary doesn't typically bite here. But if the glossary produces contested definitions, route them through moderator, not adversary.
- **I recommended historian + web-miner + github-miner in parallel**, which will produce overlapping citations (HN threads, arxiv papers, GitHub repos will be seen by more than one). Synthesist must dedupe. This is intentional: three independent sweeps over the same topic catch more than one merged sweep, even at the cost of deduplication effort.

## Expected rounds to high confidence

**3 rounds** (Round 0 done; Round 1 = 10 specialists + empiricist serial; Round 2 = synthesist + moderator + skeptic + adversary; Round 3 = evaluator + retrospector + scribe). Hard cap is 4 per protocol.

If evaluator FAILs Round 3, most likely failure is "tool efficiency" (over-dispatched on a too-wide opener) or "completeness" (missing one of the 21 sub-questions in the final SYNTHESIS.md). Targeted re-dispatch rather than a full Round 4.

## Budget check

- 10 specialists × avg 15 tool calls × Opus max = ~150k tool-call budget for Round 1 + 4 specialists × 10 calls × Opus for Round 2 + 2 specialists × 5 calls × Opus for Round 3 = ~230k tool calls total. Well within Max plan budget.
- File ledger footprint: ~20 evidence files × avg 5KB each + SYNTHESIS.md ~20KB + 10 agent markdown files × 4KB each + PROTOCOL.md ~15KB = ~175KB in workspace. Fine.
- Context footprint for the lead's 1M window: all evidence files + all persona files + MEMORY.md + synthesis + QUESTION/HYPOTHESES = ~250KB = 60-80k tokens. Well within 1M.

## Confidence in this plan

**HIGH** — the question class is well-covered by the dispatch pattern, the prior-art breadth is matched by the specialist count, the adversarial gates are mandatory rather than discretionary, and MEMORY.md's lessons 1-12 all apply cleanly. The only medium-confidence call is the 10-specialist breadth — could be 8 if historian + web-miner + github-miner are partially redundant; could be 12 if the concurrency section needs more than one tracer. I chose 10 as the best mid-point with the lead authorized to +/- 1 based on initial framing.
