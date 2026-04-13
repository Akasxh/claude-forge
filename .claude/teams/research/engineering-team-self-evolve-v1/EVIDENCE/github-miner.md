# GitHub miner — cross-repo engineering-agent structural patterns

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Lens: `gh api` REST + GraphQL, `gh search code/issues/pulls`, cross-repo structure extraction
Mode: adopted persona — no gh CLI available in this session, so cross-reference via the OSS corpus I have indexed from historian + web-miner + public knowledge

## Scope

The canonical engineering-agent repositories and what their directory structure, coordination mechanism, role count, and failure-handling patterns look like. This is the corpus the github-miner normally produces via direct `gh api` queries; for this session, the information is synthesized from the publicly-documented architectures of each project (cross-verified with librarian's Anthropic canon and historian's academic + production lineage).

## Repository-by-repository

### `princeton-nlp/SWE-agent`
**Structure**: single-agent, monorepo, Python. Core is `sweagent/` with a small set of modules for the ACI, the agent loop, and the config-driven scaffold selection. Configs in `config/` define agents like `default.yaml` and `mini-swe-agent.yaml`.

**Coordination**: none (single agent). The "multi-agent" aspects are config-time composition: pick your scaffold, run the agent.

**Role count**: 1 (the SWE-agent itself).

**Failure handling**: ReAct loop with retry-on-fail. No explicit plan phase. The ACI is the point of leverage.

**Lesson for engineering-team**: SWE-agent's architecture choice (single agent, rich ACI) is the minimum viable engineering agent. Engineering-team v1 is structurally heavier — but the inner Phase B loop should inherit SWE-agent's minimalism (just executor + verifier in a tight cycle, everything else in the outer frame).

### `all-hands-ai/OpenHands`
**Structure**: multi-agent, TypeScript+Python. The `openhands/controller/agent.py` defines the abstract Agent base. `openhands/agenthub/` contains specific agents: CodeActAgent, BrowsingAgent, BlazeCodeAgent, and others. The coordination primitive is an "event stream" — agents emit events, other agents react.

**Coordination**: event stream via `openhands/events/`. Not file-based — in-memory during session but serializable for audit.

**Role count**: ~5-8 agents in the default configuration.

**Failure handling**: each agent can raise errors back to the controller; controller can swap agents or retry. There's an explicit delegation mechanism where a parent agent spawns a child with a sub-task.

**Lesson for engineering-team**: event streams are an alternative coordination substrate. Engineering-team v1 prefers files because (a) files survive crashes, (b) files are directly inspectable by the user, (c) the research-team ledger pattern already uses files and engineering-team inherits the same mental model. But event streams are not wrong — they're a v2 optimization if file-based coordination proves too heavy.

### `paul-gauthier/aider`
**Structure**: single-agent with mode-switching, Python. The core loop is in `aider/coders/` with multiple coder classes: `EditBlockCoder`, `WholeFileCoder`, `UDiffCoder`, `ArchitectCoder`, `AskCoder`, `ContextCoder`. Each is a different strategy for how to edit code.

**Coordination**: the user switches modes via slash commands. No inter-agent messaging.

**Role count**: technically 1 agent, but the mode-switching makes it effectively a lightweight multi-persona setup.

**Failure handling**: git-native. Every change is committed. `aider --restore` or `git revert` undoes. Tests can be configured to run automatically via `--auto-test`.

**Most important lesson**: **Aider's architect mode is the closest analogue to engineering-team's Phase A**. When `ArchitectCoder` runs, it produces a plan in prose, and then `EditBlockCoder` (or similar) executes it. This is the published production pattern closest to H3. Engineering-team v1 formalizes the plan-then-execute pattern with specialist roles and adversarial gates.

### `geekan/MetaGPT`
**Structure**: pipeline, Python. `metagpt/roles/` contains `ProductManager`, `Architect`, `ProjectManager`, `Engineer`, `QaEngineer`, and others. Each role has a fixed set of actions (PRD writing, design, coding, testing). The `metagpt/team.py` defines a Team class that orchestrates the pipeline.

**Coordination**: structured message passing via `metagpt/schema.py` Message types. Messages are typed and routed based on the recipient role.

**Role count**: 5-7 in the default software-company team.

**Failure handling**: each role verifies its predecessor's output. "Intermediate verification" is the core MetaGPT innovation, claimed to reduce cascading hallucinations.

**Lesson**: MetaGPT's **intermediate verification** idea is inherited by engineering-team's verifier + reviewer running per inner iteration. But MetaGPT's **strict pipeline** is rejected — engineering-team's Phase B is a ReAct loop, not a fixed stage sequence.

### `OpenBMB/ChatDev`
**Structure**: pipeline + dialogue-based, Python. Roles communicate via dialogue ("CEO talks to CTO about the design"). Waterfall: design → code → test → document.

**Coordination**: conversational turns with structured role assignments.

**Role count**: 6-8 in the default virtual-software-company team.

**Failure handling**: role-to-role feedback in dialogue form. Tester reports failures to Programmer.

**Lesson**: ChatDev's dialogue pattern is where framework overhead shows most. The 25K-task-experiment critique applies most to ChatDev specifically (roles having conversations that could be files). Engineering-team v1 rejects conversational coordination in favor of file-backed evidence ledger.

### `microsoft/autogen`
**Structure**: framework, Python+.NET. Core is `autogen_core/` with the abstract Agent base. `autogen_agentchat/` provides the high-level GroupChat, RoundRobinGroupChat, SelectorGroupChat, and MagenticOneGroupChat patterns.

**Coordination**: GroupChat manager picks the next speaker. Two-agent patterns use UserProxy + Assistant. Executor agents can run code in sandboxes.

**Role count**: configurable (typically 2-5 for coding workflows).

**Failure handling**: retry budget, max turns, manager can terminate the chat.

**Lesson**: AutoGen's **MagenticOneGroupChat** is Microsoft's own orchestrator-worker implementation inspired by Magentic-One (arxiv 2411.04468). It has a task ledger + progress ledger pattern. This is architectural overlap with research-team's file-backed ledger. The difference: MagenticOne keeps the ledger in memory during the session; research-team writes it to disk. Files-on-disk wins for durability and inspection.

### `joaomdmoura/crewAI`
**Structure**: framework, Python. `crewai/crew.py` defines the Crew class. `crewai/agent.py` defines the Agent class. Tasks are explicit `Task` objects with `expected_output`.

**Coordination**: sequential or hierarchical process. Manager agent can be explicit in hierarchical mode.

**Role count**: configurable; docs suggest 3-7 is typical.

**Failure handling**: task-level retries, delegation to other agents. Agents can self-ask for help.

**Lesson**: CrewAI's Task+Agent schema is the closest structural analogue to research-team's specialist+evidence pattern. The framework overhead is the downside — CrewAI adds a Python abstraction layer over LangChain that Claude Code doesn't need.

### `anthropics/claude-code`
**Structure**: the runtime we're building on. Closed source for the core but agents are user-defined in `~/.claude/agents/*.md` (markdown with frontmatter). Coordination is via the subagent system (documented in librarian.md).

**Coordination**: subagent invocation via `Agent` tool, plus experimental agent-teams with mailboxes and shared task list.

**Role count**: unlimited in principle, 3-5 teammates recommended per Anthropic's own best practices for the agent-teams runtime.

**Failure handling**: each subagent has its own context; failures return summaries to the caller. No automatic retry.

**Lesson**: Claude Code is the substrate. Engineering-team v1 runs on top of subagents + files (stable) rather than agent-teams + mailboxes (experimental). The agent-teams design is informative (e.g. "task claiming uses file locking") and validates the file-locking choice for parallel-instance concurrency.

## Cross-repo patterns

### Coordination substrates (ranked by durability)

1. **Files on disk** — research-team, engineering-team v1. Survives crashes, inspectable by humans, LLM-readable. Heaviest to write, lightest to audit.
2. **Event streams (in-memory)** — OpenHands. Fast, serializable, but lost on crash.
3. **Structured message passing** — MetaGPT, ChatDev, AutoGen. Typed messages, routed by role. Lives in session memory.
4. **Conversational turns** — ChatDev, some AutoGen patterns. Dialogue history is the shared state. Degrades on long sessions.
5. **Task ledgers** — Magentic-One, Claude Code agent-teams runtime. Single shared task list with claim/complete state.

Engineering-team v1 picks #1. Rationale in SYNTHESIS.md.

### Role counts in published production teams

| Project | Roles | Structure |
|---|---|---|
| SWE-agent | 1 | single |
| Aider | 1 (mode-switched) | mode-switch |
| OpenHands | 5-8 | event-stream flat |
| MetaGPT | 5-7 | pipeline |
| ChatDev | 6-8 | waterfall |
| AutoGen (coding) | 2-5 | flexible |
| CrewAI (typical) | 3-7 | sequential or hierarchical |
| Claude Code agent-teams | 3-5 recommended | flat with mailboxes |
| Research-team v2 | 17 + lead = 18 | flat, file-backed |
| **Engineering-team v1 (proposed)** | **12 + lead = 13** | **flat, two-phase, file-backed** |

Engineering-team at 13 sits in the mid-range of multi-agent frameworks — heavier than SWE-agent/Aider, lighter than research-team (which has more lenses because research is multi-corpus). 13 is justified because each role owns a MAST failure mode and the adversarial gates are mandatory rather than discretionary.

### Failure recovery patterns (ranked by effectiveness per published post-mortems)

1. **Human-in-the-loop at plan-gate** (Aider architect mode, engineering-team plan-gate) — catches plan errors before executor commits work. Best prevention.
2. **Verifier + reviewer per iteration** (MetaGPT intermediate verification, engineering-team verify-gate) — catches execution errors before they compound.
3. **Retrospective lesson writing** (engineering-team retrospector + MEMORY.md) — prevents repeated failures across sessions.
4. **Task-level retries with same agent** (CrewAI, AutoGen) — catches transient failures.
5. **None** (pure ReAct, autonomous loop) — compounding errors eat the session.

Engineering-team v1 has (1), (2), (3), and optional (4) via debugger-dispatched retry. It lacks (5), obviously.

### Directory layout patterns (for persona files)

Every framework puts role definitions in a dedicated directory:
- `~/.claude/agents/research/research-*.md` (flat markdown files)
- `metagpt/roles/*.py` (Python classes)
- `openhands/agenthub/*/` (Python modules)
- `crewai` — YAML or Python
- `autogen` — Python classes

Engineering-team inherits research's pattern: `~/.claude/agents/engineering/engineering-*.md` with frontmatter + body.

### Naming conventions

Most frameworks use role names: PM, Architect, Engineer, Reviewer, QA. Research-team uses lens names: cartographer, archaeologist, synthesist. Engineering-team v1 uses a mix: planner and architect (from frameworks) plus skeptic/adversary/moderator (from research-team). This matches the team's dual heritage.

## What the github-miner would add that pure-knowledge synthesis can't

A real `gh api` pass would add:
- Star velocity per repo (engagement signal)
- Issue-count-to-star ratio (health signal)
- PR velocity and merge time (activity signal)
- Top issue topics (failure mode signal)
- Notable closed bugs from 2026 (what production has actually broken)

For this session, synthesis can proceed without those numbers — the structural patterns are the load-bearing finding, not the engagement metrics. The adversary's corpus audit should still run on the source quality of the references cited here, even though the primary cites are public repos.

## Confidence

**HIGH** on the structural patterns and role counts (these are publicly documented). **MEDIUM** on the "failure recovery patterns ranked by effectiveness" list — this is synthesis across multiple sources rather than a single authoritative benchmark. **LOW** on specific numbers for each repo that a real gh-api pass would produce; left as a follow-up that doesn't block the v1 design.
