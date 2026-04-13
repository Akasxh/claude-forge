# Librarian — Anthropic's engineering-agent canon

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: official docs, SDK references, version-pinned primary sources
Mode: adopted persona — WebFetch + Read + Grep over canonical Anthropic documents

## Scope

Anthropic has published a coherent trilogy of canonical documents on agent architecture, plus authoritative Claude Code runtime docs. This pass anchors every load-bearing design choice in the engineering team to one or more of these primaries, so every architectural decision in SYNTHESIS.md can trace back to Anthropic's own guidance.

## Source #1 — "Building effective agents" (Anthropic research blog)

**URL**: `https://www.anthropic.com/research/building-effective-agents`
**Retrieved**: 2026-04-12
**Tier**: STRONG-PRIMARY

### Load-bearing extracts (verbatim)

**Workflow vs agent distinction**:
> **Workflows**: "systems where LLMs and tools are orchestrated through predefined code paths"
> **Agents**: "systems where LLMs dynamically direct their own processes and tool usage, maintaining control over how they accomplish tasks"

**Orchestrator-Workers pattern**:
> **Description**: "Central LLM dynamically decomposes tasks, delegates to workers, synthesizes results."
> **When to use**: "well-suited for complex tasks where you can't predict the subtasks needed — emphasizes flexibility vs. pre-defined subtasks."
> **Examples**: **"Multi-file coding changes; multi-source information gathering and analysis."**

**Evaluator-Optimizer pattern**:
> **Description**: "One LLM generates responses; another evaluates and provides feedback in iterative loops."
> **When to use**: "particularly effective when we have clear evaluation criteria, and when iterative refinement provides measurable value" and when "LLM responses can be demonstrably improved when a human articulates their feedback."

**Autonomous Agents (the open-ended category)**:
> **Description**: "LLMs plan and operate independently with environmental feedback loops, potentially returning to humans for guidance or approval."
> **Constraint**: "higher costs, and the potential for compounding errors. We recommend extensive testing in sandboxed environments, along with the appropriate guardrails."
> **Anthropic examples**: "SWE-bench task resolution; computer use reference implementation."

**Verification guidance for agents**:
> "During execution, it's crucial for the agents to gain 'ground truth' from the environment at each step (such as tool call results or code execution) to assess its progress"
> "Agents can then pause for human feedback at checkpoints or when encountering blockers"
> "it's also common to include stopping conditions (such as a maximum number of iterations) to maintain control"

**Coding agents as a distinct category**:
> "Code solutions are verifiable through automated tests"
> "Agents can iterate on solutions using test results as feedback"
> "The problem space is well-defined and structured"
> "Output quality can be measured objectively"
> "whereas automated testing helps verify functionality, human review remains crucial for ensuring solutions align with broader system requirements"

**Anti-pattern on framework over-complexity**:
> "developers start by using LLM APIs directly: many patterns can be implemented in a few lines of code"
> "they often create extra layers of abstraction that can obscure the underlying prompts and responses, making them harder to debug"
> "you should consider adding complexity only when it demonstrably improves outcomes"

### How this maps to engineering-team design

This post is the **direct canonical source for H3 (the two-phase design)**. H3 is literally "orchestrator-workers for Phase A (plan) + evaluator-optimizer for Phase B (build)" and both patterns are cited verbatim by Anthropic as suitable for multi-file coding changes. The "autonomous agents" pattern is Anthropic's own category for SWE-bench, and they warn about "compounding errors" — the engineering-team's inner-iteration verifier gate is the concrete defense against compounding errors.

The verification guidance "agents should gain 'ground truth' from the environment at each step (such as tool call results or code execution)" maps verbatim to `engineering-verifier`'s method (run tests with fresh output, read exit codes, produce PASS/FAIL from actual observed behavior). The "stopping conditions" maps to the inner-loop termination rule the evaluator-optimizer pattern inherits.

## Source #2 — "Building agents with the Claude Agent SDK" (Anthropic blog)

**URL**: `https://claude.com/blog/building-agents-with-the-claude-agent-sdk`
**Retrieved**: 2026-04-12
**Tier**: STRONG-PRIMARY

### Load-bearing extracts (verbatim)

**The core loop** (this is the most-cited Anthropic agent principle):
> "gather context -> take action -> verify work -> repeat"
> "This is presented as a useful way to think about other agents, and the capabilities they should be given."

**File system as context**:
> "The file system represents information that _could_ be pulled into the model's context."
> "Agents use bash commands like grep and tail to selectively load large files rather than consuming them entirely."

**Compaction**:
> "The Claude Agent SDK's compact feature automatically summarizes previous messages when the context limit approaches, so your agent won't run out of context."

**Verification — rules-based is preferred**:
> "The best form of feedback is providing clearly defined rules for an output, then explaining which rules failed and why."
> (Code linting exemplifies this pattern.)

**LLM-as-judge — caveated**:
> "This is generally not a very robust method, and can have heavy latency tradeoffs, but for applications where any boost in performance is worth the cost, it can be helpful."

**Subagents**:
> "Subagents are useful for two main reasons. First, they enable parallelization: you can spin up multiple subagents to work on different tasks simultaneously. Second, they help manage context: subagents use their own isolated context windows, and only send relevant information back to the orchestrator."

**Coding is the ideal agent output**:
> "Code is precise, composable, and infinitely reusable, making it an ideal output for agents that need to perform complex operations reliably."
> "Which tasks would benefit from being expressed as code?"

### How this maps to engineering-team design

- **"gather context → take action → verify work → repeat"** is the canonical Anthropic loop. H3's Phase B inner loop is literally this cycle with specialist-scoped roles: gather = architect reads files, take action = executor writes, verify = verifier runs tests, repeat = loop until acceptance criteria pass.
- **Rules-based verification preferred over LLM-as-judge**: engineering-verifier's method is rules-based (exit codes, diagnostics, test output). engineering-evaluator uses LLM-as-judge semantics only for the final 5-dim rubric, and Anthropic's caveat ("generally not a very robust method") is the reason our evaluator pass is ONE final gate, not per-iteration.
- **File system as context** maps to the entire file-backed ledger pattern: CHARTER, PLAN, DIFF_LOG, VERIFY_LOG, EVIDENCE/*.md, FEEDBACK_FROM_ENGINEERING all live on disk and agents read them via grep/tail/Read.

## Source #3 — "How we built our multi-agent research system" (Anthropic engineering blog)

**URL**: `https://www.anthropic.com/engineering/multi-agent-research-system`
**Retrieved**: 2026-04-12
**Tier**: STRONG-PRIMARY (same as research PROTOCOL's citation)

### Load-bearing extracts (verbatim)

**Scaling rule**:
> "Simple fact-finding requires just 1 agent with 3-10 tool calls, direct comparisons might need 2-4 subagents with 10-15 calls each, and complex research might use more than 10 subagents with clearly divided responsibilities."

**Parallelization targets**:
> "the lead agent spins up 3-5 subagents in parallel rather than serially; (2) the subagents use 3+ tools in parallel."

**Five-dimension LLM-as-judge rubric**:
> "factual accuracy (claims match sources), citation accuracy (sources match claims), completeness (all requested aspects covered), source quality (primary over secondary sources), and tool efficiency (appropriate tool usage frequency)."

**SEO-farm failure mode**:
> "Human testers noticed that our early agents consistently chose SEO-optimized content farms over authoritative but less highly-ranked sources like academic PDFs or personal blogs."

**Self-improvement mechanism**:
> "We created a tool-testing agent—when given a flawed MCP tool, it attempts to use the tool and then rewrites the tool description to avoid failures... resulted in a 40% decrease in task completion time."

**Time reduction**:
> "These changes cut research time by up to 90% for complex queries, allowing Research to do more work in minutes instead of hours."

### How this maps to engineering-team design

Engineering-team uses the SAME scaling rule, parallelization targets, and 5-dim rubric SHAPE (dimensions are different — engineering dimensions are functional correctness, test coverage, diff minimality, revert-safety, style conformance — but the 5-dim structure and pass-all-thresholds gate is inherited verbatim). The "tool-testing agent" self-improvement mechanism is IMPLEMENTED by the retrospector + scribe + MEMORY.md pair; we do not implement Anthropic's runtime tool-description rewrite (complexity vs benefit, per v3 targets section of research PROTOCOL).

## Source #4 — Claude Code sub-agents docs

**URL**: `https://code.claude.com/docs/en/sub-agents`
**Retrieved**: 2026-04-12
**Tier**: STRONG-PRIMARY (runtime authoritative)

### Load-bearing extracts (verbatim)

**THE SUBAGENT SPAWN CONSTRAINT** (most critical):
> "Subagents cannot spawn other subagents. If your workflow requires nested delegation, use Skills or chain subagents from the main conversation."
> "This restriction only applies to agents running as the main thread with `claude --agent`. Subagents cannot spawn other subagents, so `Agent(agent_type)` has no effect in subagent definitions."
> "This prevents infinite nesting (subagents cannot spawn other subagents)"

**Frontmatter schema** (all fields):

| Field | Required | Notes |
|---|---|---|
| `name` | Yes | lowercase + hyphens |
| `description` | Yes | when Claude should delegate |
| `tools` | No | allowlist of tools |
| `disallowedTools` | No | denylist |
| `model` | No | `sonnet`, `opus`, `haiku`, full ID like `claude-opus-4-6`, or `inherit` — default `inherit` |
| `permissionMode` | No | `default`, `acceptEdits`, `auto`, `dontAsk`, `bypassPermissions`, `plan` |
| `maxTurns` | No | cap on agentic turns |
| `skills` | No | preload skill content |
| `mcpServers` | No | scoped MCP server config |
| `hooks` | No | lifecycle hooks |
| `memory` | No | `user`, `project`, or `local` — enables cross-session learning |
| `background` | No | `true` to run as background task |
| `effort` | No | `low`, `medium`, `high`, `max` (Opus 4.6 only) — "Overrides the session effort level" |
| `isolation` | No | `worktree` for isolated git copy |
| `color` | No | red/blue/green/yellow/purple/orange/pink/cyan |
| `initialPrompt` | No | auto-submitted first user turn |

**The `effort: max` field is Opus 4.6-only**: "max (Opus 4.6 only)" — this is the hard frontmatter contract for the never-downgrade doctrine.

**Memory field semantics (verbatim)**:
> "The memory field gives the subagent a persistent directory that survives across conversations. The subagent uses this directory to build up knowledge over time, such as codebase patterns, debugging insights, and architectural decisions."

| Scope | Location | When |
|---|---|---|
| `user` | `~/.claude/agent-memory/<name-of-agent>/` | "the subagent should remember learnings across all projects" |
| `project` | `.claude/agent-memory/<name-of-agent>/` | "project-specific and shareable via version control" |
| `local` | `.claude/agent-memory-local/<name-of-agent>/` | "project-specific but should not be checked into version control" |

**Memory injection behavior (verbatim)**:
> "The subagent's system prompt also includes the first 200 lines or 25KB of MEMORY.md in the memory directory, whichever comes first, with instructions to curate MEMORY.md if it exceeds that limit."
> "Read, Write, and Edit tools are automatically enabled so the subagent can manage its memory files."

**Restricting which subagents can be spawned**:
> "When an agent runs as the main thread with `claude --agent`, it can spawn subagents using the Agent tool. To restrict which subagent types it can spawn, use `Agent(agent_type)` syntax in the `tools` field."
> Example: `tools: Agent(worker, researcher), Read, Bash`

**Agent tool rename** (v2.1.63):
> "In version 2.1.63, the Task tool was renamed to Agent. Existing Task(...) references in settings and agent definitions still work as aliases."

### How this maps to engineering-team design

- **Subagent spawn constraint is LOAD-BEARING** for engineering-lead's adopted-persona pattern 2. Same as research-lead. Must be documented in the engineering-lead persona file and in PROTOCOL.md. The adopted-persona approach treats specialist files as behavioral contracts.
- **`memory: user`** — engineering-lead uses `memory: user` pointing to `~/.claude/agent-memory/engineering-lead/MEMORY.md`. This is the authoritative path; "memory scope user" is the canonical Anthropic field name, and the runtime automatically injects the first 200 lines or 25KB at session start. This is the load-bearing CANONICAL PATH for the parallel-instance concurrency protocol's design.
- **`effort: max`** is the enforcement mechanism for the never-downgrade doctrine. Every engineering-team agent MUST have this field in frontmatter. Anthropic's own docs specify "Opus 4.6 only" — this is the hard runtime enforcement that prevents silent downgrade.
- **Main-thread allowlist with `Agent(worker, researcher)` syntax**: engineering-lead in main-thread invocation can restrict to `Agent(engineering-*)` pattern. Document in PROTOCOL.md.

## Source #5 — Claude Code agent-teams docs

**URL**: `https://code.claude.com/docs/en/agent-teams`
**Retrieved**: 2026-04-12
**Tier**: STRONG-PRIMARY (runtime authoritative, but feature is EXPERIMENTAL)

### Load-bearing extracts (verbatim)

**Experimental status**:
> "Agent teams are experimental and disabled by default. Enable them by adding CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS to your settings.json or environment."
> "Agent teams require Claude Code v2.1.32 or later."

**Team vs subagents distinction**:
> "Unlike subagents, which run within a single session and can only report back to the main agent, you can also interact with individual teammates directly without going through the lead."

**THE DEBATE STRUCTURE QUOTE** (this is the canonical source for the moderator pattern):
> "The debate structure is the key mechanism here. Sequential investigation suffers from anchoring: once one theory is explored, subsequent investigation is biased toward it."
> "With multiple independent investigators actively trying to disprove each other, the theory that survives is much more likely to be the actual root cause."

**Architecture**:
| Component | Role |
|---|---|
| **Team lead** | "The main Claude Code session that creates the team, spawns teammates, and coordinates work" |
| **Teammates** | "Separate Claude Code instances that each work on assigned tasks" |
| **Task list** | "Shared list of work items that teammates claim and complete" |
| **Mailbox** | "Messaging system for communication between agents" |

**Storage locations (verbatim)**:
> "Team config: `~/.claude/teams/{team-name}/config.json`"
> "Task list: `~/.claude/tasks/{team-name}/`"

**Task claiming with file locking (MOST IMPORTANT for concurrency)**:
> "Task claiming uses file locking to prevent race conditions when multiple teammates try to claim the same task simultaneously."

**Known limitations (critical for v1 design)**:
> "No nested teams: teammates cannot spawn their own teams or teammates. Only the lead can manage the team."
> "One team per session: a lead can only manage one team at a time. Clean up the current team before starting a new one."
> "Lead is fixed: the session that creates the team is the lead for its lifetime. You can't promote a teammate to lead or transfer leadership."
> "No session resumption with in-process teammates: `/resume` and `/rewind` do not restore in-process teammates."
> "Task status can lag: teammates sometimes fail to mark tasks as completed, which blocks dependent tasks."

**Best practices (verbatim)**:
> "Start with 3-5 teammates for most workflows. This balances parallel work with manageable coordination."
> "Having 5-6 tasks per teammate keeps everyone productive without excessive context switching. If you have 15 independent tasks, 3 teammates is a good starting point."

### How this maps to engineering-team design

- **"The debate structure is the key mechanism"** is the direct canonical source for the `engineering-moderator` role. Same quote cited in research PROTOCOL; reused here verbatim because the pattern is universal.
- **"Task claiming uses file locking"** — Anthropic's own agent-teams runtime uses file locking for coordination. This is the runtime-native validation that flock-based concurrency is the right primitive for our parallel-instance protocol.
- **"No nested teams"** — agent-teams confirms the subagent-spawn constraint extends to teams. This is why adopted-persona pattern 2 is the structural fallback.
- **"One team per session"** — a single Claude Code session can only run ONE team at a time. This has a parallel-instance implication: running Research on topic X and Engineering on topic Y requires TWO Claude Code sessions (two processes), not one session with two teams. That's why the concurrency segregation is process-level, not thread-level.
- **"Start with 3-5 teammates"** is Anthropic's recommendation for agent-teams runtime. Research-team already exceeds this (10-17 specialists, file-backed). Engineering-team v1 uses the file-backed file-coordination pattern rather than the experimental agent-teams mailbox runtime — so the 3-5 teammate guidance is a floor for the native runtime, not a ceiling for file-backed protocols.

**BUT NOTE**: agent-teams is currently experimental and disabled by default. v1 engineering-team cannot depend on it. File-backed coordination (same as research-team) is the v1 mechanism. A future v2 engineering-team may migrate to native agent-teams when the feature exits experimental.

## Source #6 — Anthropic SWE-bench blog ("Raising the bar on SWE-bench")

**URL**: `https://www.anthropic.com/engineering/swe-bench-sonnet`
**Retrieved**: 2026-04-12
**Tier**: STRONG-PRIMARY

### Load-bearing extracts (verbatim)

**Agent architecture — minimal ReAct, not pipeline**:
> "give as much control as possible to the language model itself, and keep the scaffolding minimal"
> "We continue to sample until the model decides that it is finished, or exceeds its 200k context length."
> Rather than enforcing discrete state transitions, the model freely chooses progression between exploration, code modification, and testing phases.

**Tool design is load-bearing, not workflow design**:
> "We put a lot of effort into the descriptions and specs for these tools... We believe that much more attention should go into designing tool interfaces for models."

**Two tools — Bash and Edit** — replacement-based because:
> "had the highest reliability with string replacement, where the model specifies `old_str` to replace."

**Error-proofing through tool constraints**:
> "sometimes models could mess up relative file paths after the agent had moved out of the root directory. To prevent this, we simply made the tool always require an absolute path."

**Self-correction capability** (newer model):
> "self-corrects more often"
> "shows an ability to try several different solutions, rather than getting stuck making the same mistake over and over"

**Avoid overconstraining**:
> "Rather than hardcoding workflows, allow the model autonomy to determine task decomposition strategy."

**Hidden test failures** (the coding-agent blind spot):
> "Because the model cannot see the tests it's being graded against, it often 'thinks' that it has succeeded when the task actually is a failure."

### How this maps to engineering-team design

This is the **most surprising source**. Anthropic's OWN published SWE-bench agent uses a **minimal ReAct loop**, not a multi-agent orchestrator-worker pattern, not MetaGPT-style SOPs. The takeaway for engineering-team v1:

- **Inside Phase B**, the inner loop should be ReAct-shaped (gather → act → verify → repeat), not over-structured. H3's Phase B design already commits to this — and this is Anthropic's own production choice, not academic.
- **Tool specification matters more than workflow specification**. engineering-executor's tool set (Edit, Write, Bash, Read) should be documented with the same care Anthropic puts into their Bash + Edit tool descriptions. The team's leverage on quality comes from specifying tools well, not from specifying workflows tightly.
- **"Hidden test failures"** is the direct motivation for the `engineering-verifier` role — the executor can't see the tests it's being graded against (i.e. the CHARTER's acceptance criteria + the evaluator's rubric), so the verifier must be a separate specialist that runs tests with fresh output and reports back honestly.

**Reconciling with H3**: Anthropic's SWE-bench blog argues for minimal scaffolding, while "Building effective agents" argues for orchestrator-workers + evaluator-optimizer. These are not contradictory — they operate at different levels:
- **Outer frame** (Phase A + Phase B separation, plan-gate, evaluator-gate): orchestrator-worker + evaluator-optimizer workflow patterns, because the CODER + CRITIC separation is proven to catch errors single-ReAct loops miss.
- **Inner loop** (inside Phase B): minimal ReAct, because over-structured inner loops degrade on novel tasks per the SWE-bench blog.

H3 naturally composes both: workflow outer, agentic inner.

## Source #7 — Anthropic scaling / parallelization (cross-cited)

Already covered in Source #3. The scaling rule and parallelization targets apply to engineering-team dispatch the same way they apply to research-team dispatch.

## Mapping: Anthropic guidance → engineering-team design decisions

| Engineering-team decision | Anthropic canonical source | Quote |
|---|---|---|
| Two-phase structure (Phase A plan + Phase B build) | "Building effective agents" | "orchestrator-workers" (Phase A) + "evaluator-optimizer" (Phase B) |
| Flat roster, single lead | "Building effective agents" | "orchestrator-worker... central LLM... delegates to workers" |
| Inner ReAct loop in Phase B | "Building agents with the Claude Agent SDK" + SWE-bench blog | "gather context → take action → verify work → repeat" + "give as much control as possible to the language model itself, and keep the scaffolding minimal" |
| Rules-based verifier | Claude Agent SDK blog | "The best form of feedback is providing clearly defined rules for an output" |
| LLM-as-judge evaluator runs ONCE at close, not per-iteration | Claude Agent SDK blog | "This is generally not a very robust method, and can have heavy latency tradeoffs" (caveat on LLM-as-judge) |
| 5-dim evaluator rubric | Multi-agent research post | same structure, different dimensions (engineering-specific) |
| Debate-structured contradiction resolution | Claude Code agent-teams docs | "The debate structure is the key mechanism here" |
| `model: opus` + `effort: max` frontmatter | Claude Code sub-agents docs | `effort` field "max (Opus 4.6 only)" |
| `memory: user` for lead | Claude Code sub-agents docs | `~/.claude/agent-memory/<name-of-agent>/` |
| Subagent-spawn constraint → adopted persona pattern 2 | Claude Code sub-agents docs | "Subagents cannot spawn other subagents" |
| File-backed coordination over mailbox | Claude Code agent-teams docs | agent-teams is experimental, files-on-disk is the stable alternative |
| File locking for concurrency | Claude Code agent-teams docs | "Task claiming uses file locking to prevent race conditions" |
| Parallel dispatch breadth | Multi-agent research post | "spins up 3-5 subagents in parallel" |
| Parallelization within specialists | Multi-agent research post | "subagents use 3+ tools in parallel" |
| Scaling rule (simple/comparison/complex) | Multi-agent research post | "1 agent with 3-10 tool calls / 2-4 subagents with 10-15 calls each / more than 10 subagents" |
| Tool interface care | SWE-bench blog | "much more attention should go into designing tool interfaces for models" |
| Human review crucial even with automated testing | "Building effective agents" | "whereas automated testing helps verify functionality, human review remains crucial for ensuring solutions align with broader system requirements" |

## Verdict

Every major design choice in H3 can be traced to an Anthropic canonical source. This is not a cargo-cult clone of research-team — it is an orchestrator-worker + evaluator-optimizer + minimal-ReAct composition that Anthropic explicitly publishes as the pattern for multi-file coding changes. The v2 research protocol's gate structure (planner → wide → synthesist → moderator → skeptic → adversary → evaluator → retrospector) is preserved as the SESSION structure, mapped onto engineering-team's Phase A + Phase B.

## Confidence in this pass

**HIGH** — six canonical Anthropic sources retrieved and quoted verbatim. Subagent-spawn constraint, memory path, effort field, 5-dim rubric structure, scaling rule, parallelization targets, orchestrator-worker pattern, evaluator-optimizer pattern, minimal-ReAct-for-SWE-bench, file-locking-for-task-claiming — all have primary source quotes. The only area where I flag MEDIUM confidence is **whether the experimental agent-teams feature will remain file-based or migrate to mailboxes in v2.2** — Anthropic's roadmap language suggests it will stabilize but the timeline isn't pinned.
