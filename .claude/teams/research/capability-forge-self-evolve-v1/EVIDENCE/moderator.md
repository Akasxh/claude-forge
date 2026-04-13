# Moderator — debate on Tension 1: H1 vs H2 architecture

Dispatched because synthesist flagged a REFRAME candidate contradiction affecting the primary architecture decision. Per MEMORY.md lesson 9, I run a 3-round structured debate with verdict types {A_WINS, B_WINS, COMPLEMENTARITY, REFRAME, DEFER}.

## The question

**Should the Capability Forge be (A) a single `forge-lead` specialist with 6 sub-skills, or (B) a mini-team `teams/forge/` with lead + 5 specialists?**

## Evidence sources

- Cartographer (`EVIDENCE/cartographer.md`): leans H1 based on on-disk `self-improving-agent` pattern.
- Historian (`EVIDENCE/historian.md`): supplies Voyager + ACE + Toolformer composite which could go either way.
- Librarian (`EVIDENCE/librarian.md`): supplies `context: fork` and `agent-teams` primitives which make H1 forward-compatible.
- Synthesist (`EVIDENCE/synthesist.md`): explicitly flagged as REFRAME candidate.

## Round 1 — opening positions

### Position A (H1): single specialist with sub-skills

**Primary argument**: Minimal complexity, maximal reuse. The on-disk `alirezarezvani/claude-skills/engineering-team/self-improving-agent` pattern **proves this architecture works at first-session scale** — it has 5 sub-skills (remember/promote/status/extract/review) under one parent SKILL.md and shares one memory store.

**Supporting primary sources**:
- **`self-improving-agent/SKILL.md`** (on disk) — a real running example of the 5-subskill-under-one-agent pattern.
- **`code.claude.com/docs/en/skills`** — the `name` + `command:` frontmatter combo supports `/forge:scout`, `/forge:gap`, etc. namespacing.
- **`context: fork` in the skill spec** — lets a sub-skill run in an isolated subagent context when the Forge's scorer pass needs to grade a newly-authored skill without polluting the main context.
- **MEMORY.md pattern from research-lead** — a single MEMORY.md per specialist is the doctrine, and H1 gives a single `~/.claude/agent-memory/forge-lead/MEMORY.md` to curate.

**Secondary benefit**: First-session ergonomics. The executor can write 1-2 agent files + 6 SKILL.md files in one pass, plus a CLAUDE.md delta. H2 requires 5 agent files + a PROTOCOL.md + 6 SKILL.md files + the same workspace scaffolding. 2-3x the files, same functionality.

### Position B (H2): mini-team with lead + specialists

**Primary argument**: Clean separation of concerns, parallel dispatch compatibility, and symmetry with the successful Research Team v2 pattern.

**Supporting primary sources**:
- **Research Team v2 PROTOCOL.md** — Akash's own 17-specialist team has proven that the team-of-specialists pattern works at Opus+max-effort scale. The Research Team v2 pilot produced a HIGH-confidence PASS on the memory-layer session (per MEMORY.md). Precedent.
- **Anthropic scaling rule** (via planner.md) — complex decisions benefit from parallel specialist dispatch. The Forge's six roles (curriculum, scout, generator, reflector, curator, scorer) are six separate concerns that **could** be dispatched in parallel.
- **Agent Teams primitive** (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) — supports lead-plus-teammates natively at the runtime level; H2 is the runtime-supported primitive, H1 is the "everything-in-one-specialist" fallback pattern.
- **wshobson/agents precedent** — 182-agent, 77-plugin system shows that at scale, decomposition into specialists beats monolithic agents.

**Secondary benefit**: Scales naturally. When Akash's workforce grows from 24+18 to 50+ agents, a team of forge specialists can absorb the increased load without refactoring. A single forge-lead agent would need to be rewritten or split when the memory doc balloons.

## Round 2 — attacks and rebuttals

### Attack on A (H1):
- **"You're concentrating too many responsibilities in one agent file. Voyager, ACE, and Toolformer are three *separate* papers for a reason — the roles are orthogonal. One prompt can't do all three well at Opus max effort."**
- **"The `self-improving-agent` reference is actually more limited than you claim — it doesn't do gap detection or internet aggregation, only memory curation. You're hand-waving its relevance."**

### A's rebuttal:
- The ACE paper itself shows that **a single LLM can play the Generator / Reflector / Curator roles sequentially at Opus-class quality** — the ablation showed removing multi-epoch adaptation only cost 2.6 points, not a collapse. ACE's three roles are *procedurally* separable, not *agentically* separable.
- The `self-improving-agent` limitations are real, but they're **the parts the Forge replaces**, not **the parts it keeps**. The Forge reuses the pattern (sub-skills under one parent, MEMORY.md integration) and adds the missing pieces (gap detection, scout, scorer). This is the "wrap, don't rewrite" pattern Pattern 1 in synthesist.md.

### Attack on B (H2):
- **"H2 duplicates Research Team mechanics — it needs its own QUESTION.md / HYPOTHESES.md / EVIDENCE/ / SYNTHESIS.md / LOG.md / OPEN_QUESTIONS.md workspace. But the Forge's sessions are short, not multi-round investigations. You're importing heavy ceremony where none is needed."**
- **"The Agent Teams primitive is experimental and off-by-default. Building the Forge on top of it today is premature — you'd be gambling on a 2026-experimental feature for the core architecture."**

### B's rebuttal:
- Agent Teams is off-by-default but the *pattern* of lead+teammates is Akash's declared doctrine in CLAUDE.md ("leader agents that orchestrate sub-teams"). H2 uses the pattern without depending on the experimental runtime — the Forge-team workspace is file-based like the Research Team's is, not agent-teams-runtime-based.
- Workspace ceremony is real overhead, but it's **diagnostically valuable**: when a Forge session produces a bad skill, the evidence trail shows which specialist's reasoning failed. H1 has no such trail.

## Round 3 — reframes and compromises

**A's reframe**: **H1 is a special case of H2 with one specialist**. If the Forge starts with a single `forge-lead` specialist that has 6 sub-skills in its own `~/.claude/agents/forge/` directory, it can be **upgraded** to H2 by adding more specialist files later. The upgrade path is: move sub-skills into separate specialist files, add a PROTOCOL.md, instantiate them as agent-team teammates under the experimental runtime OR as parallel Agent-tool dispatches under the main-thread pattern. The upgrade is **graceful** — no rewrite of existing content.

**B's reframe**: **H2 is a distraction for the first session**. The immediate deliverables (§1-§10) only need one working Forge instance to smoke-test on one capability gap. The team structure is a forward-looking concern, not a blocking one.

**Moderator observation**: Both reframes converge. H1 is the **immediate-next-step** architecture, and H2 is the **future-upgrade-path** architecture. Neither is wrong; they're ordered in time.

## Verdict: **REFRAME**

**Primary verdict**: Ship H1 **now**, with the explicit upgrade path to H2 documented in the Forge's SKILL.md body. Specifically:

- **Now (first session)**: `~/.claude/agents/forge-lead.md` (one persona file, `model: opus`, `effort: max`) with 6 sub-skills in `~/.claude/skills/forge-*/SKILL.md` OR as plugin-bundled skills in `~/.claude/forge/` plugin structure.
- **MEMORY**: `~/.claude/agent-memory/forge-lead/MEMORY.md` (one file, ACE-style bulleted, append-with-counters).
- **Workspace for authored artifacts**: `~/.claude/forge/outputs/` (where drafted SKILL.md files are staged before promotion) and `~/.claude/forge/registry-cache/` (where MCP Registry query results are cached between sessions).
- **Upgrade path**: when Akash needs the Forge to run parallel scout + author + test passes, split `forge-lead.md` into `forge-scout.md`, `forge-author.md`, `forge-tester.md`, `forge-curator.md`, `forge-curriculum.md` and add `teams/forge/PROTOCOL.md`. The sub-skills stay in place; only the agent files change. Upgrade is documented explicitly in the Forge's SKILL.md under a "Scaling up" section.

## Why this verdict

1. **First-session ergonomics**: H1 gives us a writable smoke test in one file round. H2 requires 5-6 files + a PROTOCOL.md.
2. **Reuse principle (Pattern 1 "wrap, don't rewrite")**: H1 stays closer to the `self-improving-agent` reference which is already a single plugin with sub-skills.
3. **Upgrade compatibility**: H1 → H2 is a local refactor, not a rewrite. The sub-skills are the load-bearing content; specialist decomposition is reversible.
4. **Doctrine alignment**: Akash's CLAUDE.md says "leader agents that orchestrate sub-teams" but also says "non-trivial → go through a team leader". The Forge can be "a team of one" — it's still a leader, still has a team (the 6 sub-skills), just not a distributed one.
5. **Agent Teams 2026 primitive** is experimental and off-by-default. Building on it now would be premature.
6. **MEMORY.md lesson 9 REFRAME verdict is explicitly valid** — "when both sides make defensible primary-source arguments, ask 'is the question being asked the right one?' before forcing a verdict." Here the question collapsed once we realized H1 → H2 is an upgrade path, not an alternative.

## Consequences for the synthesis

- §1 Architecture decision: **H1 with upgrade path to H2**. Ship 1 agent file, 6 sub-skills, 1 MEMORY.md, 1 workspace dir. Document the H2 upgrade in the `forge-lead.md` body as a "Scaling up" section.
- §8 Workspace layout: single-agent layout, not team-workspace layout. But the directory naming should NOT collide with `~/.claude/teams/forge/` (which is reserved for the future H2 upgrade). Use `~/.claude/forge/` for the Forge's own working state.
- §9 CLAUDE.md delta: add a new section "Meta-agents" under "Currently available teams", list the forge-lead as the single entry. Not a team yet.

Moderator dispatch is complete.
