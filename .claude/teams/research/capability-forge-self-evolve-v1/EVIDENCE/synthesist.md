# Synthesist — cross-cut of round 1

## Claim matrix

| Claim | Planner | Cartographer | Librarian | Historian | Github-miner | Web-miner | Linguist | Adversary |
|---|---|---|---|---|---|---|---|---|
| **C1**: The official `skill-creator` plugin is already installed and is the canonical authoring harness Anthropic ships | — | S | S | S | S | S | — | S |
| **C2**: `self-improving-agent` from alirezarezvani is an on-disk reference for MEMORY.md → skill extraction | — | S | — | — | S | S | — | S |
| **C3**: The MCP Registry at `registry.modelcontextprotocol.io/v0/servers` is a production public REST endpoint with cursor pagination | — | — | S | — | S | S | — | S |
| **C4**: There is NO Hacker News or Semantic Scholar MCP in the registry today | — | — | — | — | S | — | — | — |
| **C5**: There ARE multiple arxiv MCP servers; blazickjp and cyanheads are HIGH-trust | — | — | — | — | S | S | — | S |
| **C6**: **Agent Teams is a real 2026 experimental primitive** with cross-session parallel coordination, lead + teammates + mailbox + shared task list | — | — | S | — | — | S | — | S |
| **C7**: Subagents cannot spawn subagents; agent-team teammates can reference subagent definitions as behavioral templates | — | — | S | — | — | S | — | S |
| **C8**: The `context: fork` skill frontmatter field lets a skill run in an isolated subagent without main-thread lock-in | — | — | S | — | — | S | — | — |
| **C9**: Voyager's 3-component architecture (curriculum / skill library / iterative prompting with self-verify) is the reference impl for self-improving skill libraries | — | — | — | S | — | — | — | S |
| **C10**: ACE's 3-role architecture (Generator / Reflector / Curator) is the reference impl for evolving playbooks with counter-based dedup | — | — | — | S | — | — | — | S |
| **C11**: Akash's `~/.claude/agents/` flat dir has 24 agents, with 4 overlapping the Research Team (critic, explore, researcher, tracer) | — | S | — | — | — | — | — | — |
| **C12**: Akash's major capability gaps are: automatic curriculum, MCP Registry scout, value tracking, tool-need-vs-skill diff, research handoff protocol | — | S | — | — | — | — | — | — |
| **C13**: Akash's substrate has **91 personal "skill" directories** but only 3 have true local SKILL.md — most are populated from the ai-research-skills marketplace | — | S | — | — | — | — | — | — |
| **C14**: VoltAgent/awesome-claude-code-subagents has 130+ specialists in 10 categories; meta-orchestration category (13 specialists) is entirely missing from Akash's roster | — | S | — | — | S | — | — | S |
| **C15**: ComposioHQ, travisvn, BehiSecc three "awesome-claude-skills" repos with 50k/11k/8k stars show SEO-farm behavior pattern (but not dishonest content) | — | — | — | — | S | S | — | S |
| **C16**: `mcp-builder` skill exists in anthropics/skills — Anthropic has an official MCP-authoring skill | — | — | — | S | S | — | — | S |
| **C17**: SKILL.md max description length is 1024 chars hard, 250 chars before truncation in skill listing; name ≤64 chars, no reserved words "anthropic"/"claude" | — | — | S | — | — | — | S | — |
| **C18**: Anthropic recommends "pushy" descriptions to counter Claude's undertriggering tendency; description must be third-person | — | — | S | — | — | — | S | — |
| **C19**: The skill-creator eval loop is the canonical critic — evaluation-driven development (gaps → evals → minimal instructions → iterate) | — | — | S | S | — | — | — | — |
| **C20**: Agent Skills is an open cross-vendor standard at agentskills.io adopted by ≥30 agent tools including Cursor, Gemini CLI, OpenCode, VS Code, Copilot, OpenAI Codex | — | — | — | S | — | S | — | S |

Legend: S = supports, R = refutes, — = silent (not in specialist's scope).

## Convergent claims (strong signal)

- **C1-C2-C3-C6 form a cluster** supported by 4+ specialists each: Anthropic's primitives (skills, plugins, sub-agents, agent-teams, MCP Registry) are **production and mature**. Eight specialists converge on this.
- **C9-C10-C19**: the canonical self-improvement loops from literature (Voyager, ACE) and from skill-creator itself all converge on **gap → draft → eval/critic → commit on pass**. No refutations.
- **C12** (Akash's gaps) is unique to cartographer — but it's load-bearing and no one refutes it.
- **C14** (VoltAgent's taxonomy) — the meta-orchestration gap has 3 converging supporters.
- **C16** (`mcp-builder` exists) — important for the Forge's §4 first-batch: instead of building MCP-authoring, wrap the Anthropic one.

## Contradictions

**No hard contradictions surfaced**, but three **scope-mismatch tensions** to surface:

### Tension 1 — H1 vs H2 architecture debate (for the moderator)

- **Cartographer** (C12): leans H1-plus-subskills — "`self-improving-agent` already demonstrates a multi-sub-skill plugin pattern; a single-agent-with-skills model is cleaner than a team with 5 separate agent files."
- **Planner** (implied from the opening dispatch recommendation): was neutral, but the planner's instruction to use adopted-persona mode implies a team pattern (H2) because it recommends dispatching 8 specialists in round 1, which mirrors the Research Team pattern.
- **Librarian** (C6-C7-C8): the new Agent Teams primitive **changes the game**. If the Forge is designed today as a single specialist (H1), it can be upgraded to a team later by just writing a team config file — agent-teams use subagent definitions as teammate behavioral templates. So H1 is forward-compatible with H2; picking H1 now does NOT lock in single-agent permanently.

**Synthesist verdict on the tension**: this is a **REFRAME candidate** per MEMORY.md lesson 9. Both positions are defensible primary-source-backed. The real question is: *at which scale does a team beat a single specialist?* For first-session smoke test + the four immediate capability gaps, H1 is right. At scale (Forge operating on a 100+ agent workforce), H2 is right. Recommendation: **REFRAME to "start with H1, design for graceful upgrade to H2"**.

### Tension 2 — Forge vs Research Team scope overlap

- **Cartographer**: Forge is downstream of research, must not duplicate research-lead's wide-dispatch work.
- **Github-miner**: the Forge's scout role queries the MCP Registry and community rosters, which is overlap with research-github-miner.
- **Adversary**: Forge must delegate deep adversarial work back to research-lead's adversary specialist.

**Synthesist verdict**: **not a real contradiction** — it's a **collaboration contract**. The Forge **owns** routine registry queries and roster inventory. The Forge **delegates** to research-lead when a question requires >3 rounds of investigation. The contract is clear: the Forge has its own scout lens for day-to-day work, but research-lead is the wide-dispatch specialist for ambiguous gaps. This goes to the collaboration-contract deliverable (§6).

### Tension 3 — Skill, plugin, or MCP? The decision tree for closing a gap

- **Librarian**: default to **skill** per Simon Willison's "Skills > MCP" argument.
- **Github-miner**: MCPs are needed when the capability requires OAuth, shared state, websockets, or cross-client portability.
- **Historian**: Voyager's skill library is code-based; skill-creator's eval loop matches the Claude Code skill primitive; the Claude Code 2026 stack has distinct layers for skill / plugin / MCP.

**Synthesist verdict**: **not a contradiction, but a decision tree** that the Forge must encode. The decision tree is:

```
Question: what primitive to build for this capability gap?
  ├─ Is the capability purely instructions (playbook, checklist, reference)?
  │    → SKILL.md (simplest, cheapest)
  │
  ├─ Is the capability a reusable script Claude will execute?
  │    → SKILL.md with bundled scripts/ (progressive disclosure)
  │
  ├─ Does the capability need cross-session state (persistent DB, shared cache)?
  │    → MCP server (stateful service)
  │
  ├─ Does it need to run in non-Claude environments (Cursor, VS Code, Gemini CLI)?
  │    → open-standard skill (agentskills.io) OR MCP server (for non-skill-aware tools)
  │
  ├─ Is it a coherent bundle of multiple related capabilities (skills + agents + hooks + MCP)?
  │    → Plugin with plugin.json manifest
  │
  └─ Is it a behavioral contract for a new role in the workforce?
       → Subagent definition (.claude/agents/<name>.md)
```

This decision tree belongs in the Forge's SKILL.md reference content.

## Emergent patterns (named for discussability)

### Pattern 1: **"Wrap, don't rewrite"**

Four specialists independently point to already-existing primitives:
- skill-creator already does draft + eval + iterate (librarian, historian, cartographer).
- self-improving-agent already does promote + extract (cartographer, github-miner).
- mcp-builder already does MCP server authoring (github-miner).
- MCP Registry already does server discovery (librarian, github-miner, web-miner).
- Research Team already does deep investigation (cartographer, planner).

**Implication**: the Forge's code should be **glue**, not **core**. It orchestrates calls to existing primitives. This dramatically reduces the persona file size and implementation effort.

### Pattern 2: **"Voyager + ACE + Toolformer composite is the canonical self-improvement loop"**

Three papers, three roles, one composite pattern:
- Voyager: automatic curriculum + skill library + iterative prompting (adds a self-proposing curriculum).
- ACE: Generator + Reflector + Curator with counter-based dedup (adds a playbook data structure).
- Toolformer: self-supervised filter that keeps only helpful tool calls (adds a value metric).

Combined, these define **six roles** for the Forge:
1. **Curriculum** (proposes what to build)
2. **Scout** (queries internet for existing implementations)
3. **Generator** (drafts SKILL.md)
4. **Reflector/Critic** (runs eval loop)
5. **Curator** (commits to library, updates MEMORY.md)
6. **Scorer** (tracks value via counters across sessions)

Whether these are 6 specialists in a team (H2) or 6 sub-skills under one agent (H1) is the open architectural question. Either way, these six roles must exist.

### Pattern 3: **"Agent Teams changes the runtime model"**

The new Agent Teams primitive (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) is a **cross-session parallel collaboration primitive** with:
- Shared task list at `~/.claude/tasks/<team-name>/`.
- Lead + teammates pattern.
- Mailbox messaging.
- Hooks: `TeammateIdle`, `TaskCreated`, `TaskCompleted`.
- **Teammates can reference subagent definitions by name**, so a `forge-lead.md` file in `~/.claude/agents/` can be instantiated as either a subagent OR a team teammate.

**Implication**: Akash's existing `~/.claude/teams/research/` workspace pattern is NOT the runtime pattern for agent-teams (which uses `~/.claude/teams/<team-name>/config.json`). The two paths collide. **This is a minor conflict for the moderator or scribe to resolve** — the Research Team's file-based workspace is independent of the agent-teams primitive, which is fine, but document it clearly.

### Pattern 4: **"Meta-orchestration is the biggest community category Akash lacks"**

13 specialists in VoltAgent's `09-meta-orchestration` category (agent-installer, agent-organizer, context-manager, knowledge-synthesizer, multi-agent-coordinator, error-coordinator, workflow-orchestrator, task-distributor, performance-monitor, pied-piper, airis-mcp-gateway, it-ops-orchestrator, taskade). **Akash has zero.** The parallel `orchestration-full-activation-v1` session is addressing this category. **The Forge should not duplicate that work**; it should author the *skills* the orchestrators will need.

## Blind spots the team cannot answer with current lenses

1. **Does `self-improving-agent` actually work in practice?** On-disk inspection shows it's a real plugin, but neither adversary nor cartographer has actually run `/si:promote` end-to-end. **Suggest dispatching research-empiricist in round 3** to smoke-test it on a real MEMORY.md entry.

2. **What is the exact retrieval mechanism in Voyager's skill library?** Historian hit WebFetch's 10MB limit on the full PDF. Not blocking the Forge architecture decision but would inform the scorer role design. **Flag for research-historian follow-up if §4 skill priorities depend on it.**

3. **How many sessions-per-week would the Forge run?** If it's bursty (once a month), H1 is fine forever. If it's daily, H2's separation of concerns becomes valuable sooner. **Flag for Akash to answer in round 3 or post-session.**

4. **Should the Forge maintain a human-readable index of all authored skills?** None of the specialists addressed this, but it's implied by the value-tracking requirement. **Suggest adding to §8 workspace layout.**

## Candidate synthesis (for research-lead to adopt/edit)

> The Capability Forge should be a **single specialist agent** (`forge-lead`) with **six sub-skills** covering Voyager's curriculum + ACE's Generator/Reflector/Curator + Toolformer's value scoring, wrapping existing primitives (official `skill-creator`, `self-improving-agent` from alirezarezvani, Anthropic's `mcp-builder`, and the MCP Registry REST API) rather than re-implementing them. It reads Akash's agent/skill/plugin substrate on session start, diffs against community rosters (VoltAgent's 130-specialist taxonomy, wshobson's 182-agent collection, anthropics/skills' 17 official skills) to detect gaps, and authors new SKILL.md files (and occasionally MCP servers or plugin bundles) to close those gaps. Its memory lives at `~/.claude/agent-memory/forge-lead/MEMORY.md` using ACE's append-with-counters pattern. When a gap requires deep investigation (e.g., "is there an authoritative source for X?"), it drops a file into `~/.claude/teams/research/inbox/` and delegates to research-lead rather than duplicating the research team's work. This is architecturally H1 (single agent + sub-skills), not H2 (mini-team) — the decisive arguments are: (a) the `self-improving-agent` reference implementation is exactly this pattern at smaller scale, (b) the Agent Teams 2026 primitive lets the Forge upgrade to H2 later without rewriting anything, (c) six related sub-skills under one namespace match Akash's linguistic preference for `/forge:scout`, `/forge:gap`, `/forge:draft`, etc. The first-batch skills the Forge should build are grounded in C4 (no HN/Semantic Scholar MCP exists) and the C12 gap list: (1) HN MCP server via mcp-builder, (2) Semantic Scholar MCP via mcp-builder, (3) arxiv MCP install + wrapper skill using blazickjp's registry entry, (4) `forge-curriculum` internal skill implementing the gap-detection algorithm, (5) `forge-scout` internal skill wrapping the MCP Registry API with the 6-rule trust heuristic. Open confidence: HIGH on architecture, HIGH on reuse pattern, MEDIUM on the moderator debate verdict (REFRAME to "H1 now, H2 later"), LOW on the exact MEMORY.md counter schema (ACE's paper doesn't specify the JSON/bulleted format precisely enough to adopt verbatim).

## Blind spots for the lead

- **Moderator debate on H1 vs H2**: recommend running the moderator explicitly on this since the REFRAME verdict is actively the right call — force the decision to be argued, not assumed.
- **Skeptic pass**: attack the "wrap, don't rewrite" claim. What if the existing primitives have blockers we haven't tested? (e.g., `/si:extract` may only work when MEMORY.md is populated by Claude's auto-memory, not by the Forge's own curator pass).
- **Evaluator pass**: check that each deliverable §1-§10 is writable verbatim, not hand-wavy.
