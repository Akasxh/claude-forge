# Historian — SWE-bench prior art, production engineering agents, plan-vs-ReAct debate

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: prior art, academic + production + market, 2023-2026 arc
Mode: adopted persona — arXiv + WebFetch + Semantic Scholar + aider leaderboard

## Scope

Every production or semi-production engineering-agent system visible in the public record as of 2026-04-12. For each: architecture, public benchmark, known failure modes, current status, how it handles the plan-vs-ReAct question. This is the corpus the adversary will audit separately.

## Academic lineage (2022-2024)

### ReAct — Yao et al. 2022 (arxiv 2210.03629)
The ur-pattern for reasoning + acting interleaved. Thought → Action → Observation trace, unbounded length. Every coding-agent inherits this as its inner loop, whether they call it ReAct or not.

### Reflexion — Shinn et al. 2023 (arxiv 2303.11366)
Adds "verbal reinforcement learning" — after a failed attempt, the agent generates a self-reflection that becomes context for the next attempt. This is the academic precedent for the retrospector's MEMORY.md lesson-accumulation pattern.

### Plan-and-Solve Prompting — Wang et al. 2023 (arxiv 2305.04091)
The canonical "plan-first-then-execute" pattern. Produces an explicit plan before any tool use, then executes the plan step by step. Engineering-team's Phase A is this pattern at team scale. Phase B is where we DEPART — Plan-and-Solve's "execute the plan step by step" is too rigid for multi-file coding, so we replace it with evaluator-optimizer + inner ReAct.

### Self-Refine — Madaan et al. 2023 (arxiv 2303.17651)
Generator → feedback → refiner loop within a single agent. Direct precedent for evaluator-optimizer. Published result: iterative refinement improves code generation.

### SWE-agent — Yang et al. 2024 (arxiv 2405.15793, Princeton)

**Key finding (verbatim from abstract)**:
> "LM agents represent a new category of end users with their own needs and abilities, and would benefit from specially-built interfaces to the software they use."
> "The design of the ACI can impact agents' behavior and performance"
> Achieved "a pass@1 rate of 12.5%" on SWE-bench, "far exceeding the previous state-of-the-art achieved with non-interactive LMs."

**Architecture**: single agent, custom Agent-Computer Interface (ACI) exposing file-edit, file-view, bash, find. The ACI design is the load-bearing innovation, not the agent loop itself (which is standard ReAct).

**Position on plan-vs-execute**: SWE-agent does NOT have an explicit plan phase. It runs straight ReAct with the ACI as the leverage point. This is the same conclusion Anthropic's SWE-bench blog reaches independently: **don't over-structure the inner loop; put the effort into tool design**.

**Key lesson for engineering-team**: engineering-executor's tool set (Edit, Write, Bash, Read) needs the same ACI care SWE-agent put into their ACI. Tool spec is load-bearing.

### OpenHands / OpenDevin — Wang et al. 2024 (arxiv 2407.16741, All-Hands.dev)

**Key finding from abstract**:
> "AI agents that interact with the world in similar ways to those of a human developer: by writing code, interacting with a command line, and browsing the web"
> "Released under the permissive MIT license... more than 2.1K contributions from over 188 contributors"
> Evaluated "over 15 challenging tasks, including software engineering (e.g., SWE-BENCH) and web browsing (e.g., WEBARENA)"

**Architecture**: CodeAct agent is the primary coding agent; adds browsing agent, Jupyter agent, and others as sub-agents. Uses an event stream as the shared coordination substrate. Later versions added multi-agent patterns where agents specialize on different sub-tasks.

**Position on plan-vs-execute**: started as a Devin clone (OpenDevin) with explicit plan-execute-verify phases, evolved toward a more flexible event-stream architecture. The 2024 paper claims the event-stream design beats fixed pipelines.

**Key lesson for engineering-team**: event-stream coordination is an alternative to file-backed coordination. The tradeoff is that event streams live in memory (lost on crash) while files persist. Engineering-team v1 uses files for durability.

## Production agents — market leaders 2025-2026

### Cognition AI Devin (2024-2026)

**Architecture (per public blog + demo videos)**: autonomous agent with an internal planner, a shell, a browser, and a code editor. Closed-source. No published paper. The architecture details are reverse-engineered from demos and blog posts, marked **REPORTED-NOT-VERIFIED** per MEMORY.md lesson 12.

**SWE-bench score evolution**:
- Initial demo (March 2024): claimed 13.86% on SWE-bench
- Controversial: independent observers on HN and X noted that the public demo tasks were a subset the agent was known to handle and that failures were edited out of the published video
- 2025-2026: Cognition moved primarily to SWE-bench Pro and Devin-Bench (their own eval), making direct comparison harder

**Known failure modes from community reports**:
- Time-to-solution inflation on complex tasks (days-long sessions)
- Inability to recover from a wrong initial plan without human intervention
- Cost explosion (reported $20-50/task on complex SWE-bench instances)

**Lesson for engineering-team**: an autonomous agent without explicit plan-gate + verifier-gate + reviewer-gate creates unbounded runs. The v1 engineering-team design's gate structure (plan-skeptic, plan-adversary, verifier per iteration, reviewer per iteration, evaluator at close) is direct defense against the Devin failure pattern.

### Aider — Paul Gauthier (2023-2026)

**Architecture (public)**: not a ReAct agent — Aider uses a deliberate **three-mode pattern**: `code` mode (executor), `architect` mode (plans changes), `ask` mode (discusses). The user can explicitly switch modes. Recent versions added an `auto-mode` that routes automatically.

**Git-native**: every Aider change is a git commit. Rollback = git revert. This is the operational model engineering-team should adopt: the executor produces commits, verifier runs tests against the current HEAD, reviewer reviews the diff, evaluator reads git log for the session.

**Polyglot leaderboard (retrieved 2026-04-12 from aider.chat/docs/leaderboards/)**:
- gpt-5 (high): 88.0% correct @ $29.08
- gpt-5 (medium): 86.7% @ $17.69
- o3-pro (high): 84.9% @ $146.32
Tests 225 Exercism exercises across C++, Go, Java, JS, Python, Rust. NOT SWE-bench — independent benchmark.

**Position on plan-vs-execute**: Aider's `architect` mode IS the plan-first pattern. When used, architect runs, emits a plan, then the user approves and code mode executes it. This is the closest public product analogue to engineering-team's Phase A + Phase B split. Paul Gauthier has written in release notes that architect mode outperforms single-pass mode on complex tasks but adds latency.

**Key lesson for engineering-team**: architect-then-execute is a published production pattern that works. The plan-gate (engineering-skeptic + engineering-adversary) between Phase A and Phase B is essentially Aider's architect-mode approval step formalized with adversarial review.

### Cursor Agent (2024-2026)

**Architecture (per public blog + in-product experience)**: "Agent mode" runs autonomous multi-step coding tasks inside the Cursor editor. No published paper. Uses a tree-search-ish pattern: tries multiple approaches in parallel, picks the best. Recent versions added "plan mode" that shows the agent's intended steps before execution.

**SWE-bench position**: Cursor has not published their own SWE-bench numbers but appears on the full-system leaderboard via third-party evaluations.

**Failure modes (community reports)**: diff confusion on large files, unbounded context growth, occasional silent test failures.

**Lesson**: tree-search is an orthogonal architecture we are not adopting in v1. Engineering-team v1 uses a single trajectory per executor pass, not branching parallel attempts. v2 could add branching if needed; for v1 it's YAGNI.

### Replit Agent (2024-2026)

**Architecture**: hosted environment, integrated with Replit's cloud IDE. Agent has full environment access (shell, package manager, deploy). Focused on end-to-end app building more than individual file edits.

**SWE-bench position**: primarily evaluated on their own eval (Replit Agent Eval), which focuses on app-building tasks rather than bug-fix tasks.

**Lesson**: Replit Agent is a different problem shape — "build a new app" rather than "fix this bug in an existing repo." Engineering-team v1 is designed for the SWE-bench-like shape (fix/modify existing code), not the Replit shape. A future v2 could add an "engineering-greenfield" variant for new-app work.

### Claude Code's own agent

**Architecture**: the runtime we are building on. Published via the sub-agents and agent-teams docs (cited in librarian.md). Uses subagents for focused tasks and agent-teams (experimental) for coordinated parallel work. Its own SWE-bench results are reported via Claude Opus 4.5 / 4.6 on the Scale AI SEAL leaderboard.

**Claude Opus 4.5 on SWE-Bench Verified**: 80.9%
**Claude Opus 4.5 on SWE-Bench Pro**: 45.9%
**Gap**: "80.9% on SWE-Bench Verified and 45.9% on SWE-Bench Pro. Same model, half the score." (Quoted from Morph LLM analysis, retrieved 2026-04-12.)

**Lesson**: Claude Opus 4.6 (our session model) is at or near the top of both leaderboards but shows a substantial gap between contaminated Verified and clean Pro. Engineering-team must not design around the 80% Verified number — design around the 45% Pro number, which represents actual capability on uncontaminated benchmarks.

## Multi-agent frameworks

### MetaGPT — Hong et al. 2023 (arxiv 2308.00352)

**Key findings (verbatim from abstract)**:
> "Standardized Operating Procedures (SOPs) into prompt sequences for more streamlined workflows"
> "an assembly line paradigm to assign diverse roles to various agents"
> "generates more coherent solutions than previous chat-based multi-agent systems"
> Addresses "logic inconsistencies due to cascading hallucinations caused by naively chaining LLMs" via structured procedures and intermediate verification
> Agents have "human-like domain expertise to verify intermediate results and reduce errors"

**Architecture**: pipeline of PM → Architect → PjM → Engineer → QA, each emitting structured artifacts (PRD, design, plan, code, tests).

**Position**: strict pipeline. Rejects flat multi-agent chat as insufficient. The H3 design disagrees structurally — we inherit MetaGPT's **"intermediate verification"** idea but reject the strict pipeline in favor of flat roster + phase gates.

**Why we don't clone MetaGPT directly**: the pipeline's stage boundaries become bureaucratic overhead on small tasks (a simple bug fix doesn't need a PRD). MetaGPT's published results are on full-app generation, not SWE-bench-shape bug fixes.

### ChatDev — Qian et al. 2023 (arxiv 2307.07924)

**Architecture**: virtual software company with CEO, CTO, Programmer, Reviewer, Tester, Designer roles. Waterfall pipeline: design → code → test → document. Communication via structured dialogue.

**Position**: strict waterfall. Rejects flat coordination. Like MetaGPT, optimized for full-app generation, not bug fixes.

**Why we don't clone**: waterfall pipeline is the H2 hypothesis we examined and ranked below H3. The "together" constraint from Akash explicitly rules out strict stage-owned handoffs between PMs and programmers.

### AutoGen — Wu et al. 2023 (Microsoft Research)

**Architecture**: flexible multi-agent conversation framework. Agents can be LLM-backed, tool-backed, or human. Default pattern is "GroupChat" with an orchestrator that picks the next speaker. Coding crews typically use UserProxy + Assistant + Executor agents.

**Position**: more flexible than MetaGPT/ChatDev — supports flat, hierarchical, and pipeline shapes. But published GroupChat failures are documented: speakers can deadlock, converge on wrong answers, or run unbounded.

**Lesson**: AutoGen's flexibility is its weakness — too many valid topologies, no canonical pattern. Engineering-team v1 picks ONE topology (flat + two-phase) and commits. AutoGen's flexibility is more suited to research experimentation, not production workflow.

### CrewAI — João Moura (2023-2026)

**Architecture**: role-based team. You define each agent with role, backstory, goal, then assemble as "crew" with tasks. Supports sequential or hierarchical processes.

**Position**: closest in spirit to the research-team and engineering-team designs — role-based, configurable, file-backed. But CrewAI is a framework layer over LangChain, adding abstraction that Anthropic's "Building effective agents" explicitly warns against.

**Lesson**: CrewAI's role-based pattern validates the structural direction. The framework overhead is what we avoid — engineering-team uses Claude Code's native subagents as the primitive, not CrewAI's agent class.

### The viral X claim — "25,000-task experiment proved the entire multi-agent framework industry is built on the wrong assumption"

**Source**: `x.com/sukh_saroy/status/2039381283999293799`, retrieved 2026-04-12, claimed "25,000-task experiment"
**Tier**: **REPORTED-NOT-VERIFIED** per MEMORY.md lesson 12. Single-witness claim, X.com post, no linked paper or dataset. The direction (role-based multi-agent frameworks have fundamental coordination overhead) IS corroborated by MAST (arxiv 2503.13657) and by our own internal observation, but the "25K task" methodology is not published anywhere I can locate.

**Usage**: adversary should flag this. Direction is usable; numbers are not.

## The benchmark integrity crisis (critical finding)

### SWE-Bench Verified contamination

**Primary source**: Morph LLM analysis at `morphllm.com/swe-bench-pro`, retrieved 2026-04-12.

**Verbatim**:
> "OpenAI's audit found that every frontier model tested (GPT-5.2, Claude Opus 4.5, Gemini 3 Flash) could reproduce verbatim gold patches"
> "59.4% of the hardest unsolved problems had flawed test cases"
> "The best model scores 46% on Pro but 81% on Verified, because Verified is contaminated."

**The score gap**:
- Claude Opus 4.5 on SWE-Bench Verified: **80.9%**
- Claude Opus 4.5 on SWE-Bench Pro: **45.9%**
- "Same model, half the score."

**What SWE-Bench Pro is (verbatim)**:
> "1,865 tasks across 41 repositories in multiple languages"
> "Pro tasks average 107 lines of changes across 4.1 files, versus Verified's median of 4 lines in single files"
> "Pro uses GPL licensing and proprietary codebases to resist data contamination"
> "Scale AI runs every model through identical tooling with a 250-turn limit"

**Top Pro scores (March 2026, SEAL leaderboard)**:
- Claude Opus 4.5: 45.9%
- Claude Sonnet 4.5: 43.6%
- Gemini 3 Pro: 43.3%
- Agent systems with custom scaffolding: GPT-5.3-Codex 57%, Opus 4.6 + WarpGrep v2 57.5%

**Position**: OpenAI has stopped reporting Verified scores and recommends Pro. Engineering-team must treat any Verified score above ~50% with strong suspicion, and design around Pro numbers.

**What this means for our design**:
- Even the best coding agents score ~50% on uncontaminated benchmarks. **Engineering-team must not assume the inner-ReAct loop will "just work" most of the time — it will fail roughly half the time on hard tasks.** This is the failure-mode budget that the verifier + reviewer + plan-skeptic gates exist to catch.
- The "hidden test failure" problem from Anthropic's SWE-bench blog is the mechanism: **"the model cannot see the tests it's being graded against, it often 'thinks' that it has succeeded when the task actually is a failure."** engineering-verifier's "run tests with fresh output, no belief propagation from executor" is the direct defense.
- No amount of clever prompt engineering or gate design can make a ~50% base-rate agent reach 95% without external verification. The team structure exists to raise the base rate, not to replace it.

## Position on plan-vs-execute debate (2026 synthesis)

After reading the prior art, the "plan-and-execute vs ReAct" debate is effectively **settled as a false dichotomy**:

- **For small/bounded tasks**: ReAct alone works. SWE-agent, Anthropic's own SWE-bench agent, Aider's default mode all use it.
- **For large/multi-file tasks**: plan-first is better because it commits to a structure before compounding errors. MetaGPT, ChatDev, Aider architect mode, Devin's internal planner all do some variant of this.
- **For anything in between (most SWE-bench tasks)**: **hybrid** is the winning pattern. Commit to a high-level plan, execute in ReAct, replan if the execution reveals a plan error. Plan-and-Solve with ReAct fallback.

Engineering-team v1's H3 design is exactly this hybrid. Phase A commits to a plan. Phase B executes in a ReAct loop with back-edges to Phase A if the plan is wrong. **This is not a novel synthesis — it's what the prior art has been converging on since 2023.**

## Key lessons for engineering-team design

1. **The plan-then-execute-via-ReAct hybrid is the prior art winner**. H3's design is confirmed by multiple independent sources.
2. **Tool spec matters more than workflow spec**. SWE-agent + Anthropic SWE-bench blog agree. Engineering-executor's tool documentation is a load-bearing quality lever.
3. **Benchmarks are contaminated**. Engineering-team must be designed for ~50% base-rate reality, not 80% headline reality. Gates exist to catch the other 50%.
4. **Hidden test failure is the central coding-agent failure mode**. Verifier + reviewer as separate specialists from executor is the direct defense.
5. **Git-native coordination works** (Aider). Engineering-team v1 adopts git as the audit trail substrate — DIFF_LOG.md records what changed, git records the actual change.
6. **Framework overhead is the enemy**. Anthropic warns about over-abstraction; CrewAI/MetaGPT/ChatDev add framework layers we avoid. Engineering-team v1 uses Claude Code's native subagents + files, not a framework.
7. **Autonomous agents without gates produce unbounded runs**. Devin's cost/time failures are the direct motivation for engineering-team's gate structure.

## Load-bearing citations (STRONG-PRIMARY unless marked)

- **SWE-agent**: Yang et al., arxiv 2405.15793, retrieved 2026-04-12, STRONG-PRIMARY
- **OpenHands**: Wang et al., arxiv 2407.16741, retrieved 2026-04-12, STRONG-PRIMARY
- **MetaGPT**: Hong et al., arxiv 2308.00352, retrieved 2026-04-12, STRONG-PRIMARY
- **ChatDev**: Qian et al., arxiv 2307.07924, retrieved 2026-04-12, STRONG-PRIMARY
- **ReAct**: Yao et al., arxiv 2210.03629, STRONG-PRIMARY (canonical reference, no retrieval needed)
- **Plan-and-Solve**: Wang et al., arxiv 2305.04091, STRONG-PRIMARY
- **Self-Refine**: Madaan et al., arxiv 2303.17651, STRONG-PRIMARY
- **Reflexion**: Shinn et al., arxiv 2303.11366, STRONG-PRIMARY
- **MAST**: Cemri et al., arxiv 2503.13657, STRONG-PRIMARY (already cited in research PROTOCOL)
- **SWE-Bench Pro / SEAL leaderboard**: morphllm.com/swe-bench-pro, retrieved 2026-04-12, MIXED (aggregator but primary for the contamination claim)
- **Aider polyglot leaderboard**: aider.chat/docs/leaderboards/, retrieved 2026-04-12, STRONG-PRIMARY (maintainer's own site)
- **X.com 25K-task experiment claim**: `x.com/sukh_saroy/status/2039381283999293799`, retrieved 2026-04-12, REPORTED-NOT-VERIFIED (single-witness)

## Confidence

**HIGH** on the prior-art synthesis and the hybrid-wins conclusion. **MEDIUM** on specific SWE-bench numbers for individual agents (Devin especially — numbers are contested). **HIGH** on the benchmark contamination finding (primary-sourced via Morph LLM / SEAL / OpenAI audit chain). **HIGH** that Anthropic's SWE-bench minimal-ReAct approach and MetaGPT's strict pipeline represent the two poles of the design space and H3 composes rather than picks.
