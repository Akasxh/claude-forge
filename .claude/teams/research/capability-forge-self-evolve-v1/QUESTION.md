# QUESTION.md — Capability Forge self-evolve v1

## Raw prompt (verbatim)

> Research on making sure or making a agent or something that knows and reads other agents and teams and make really good good skills and plugins for our workforce. This should be able to also aggregate from internet and collaborate with the research team to get more research on all the skills and develop its own skills to help our team work better.

Plus the formal meta-task brief expanding this into 10 deliverables.

## Assumed interpretation

Akash has built (and is mid-build) a leader-led sub-team architecture. The Research Team v2 (17 specialists + lead) is the only team fully live. Three parallel sessions are designing the remaining teams (Engineering, Memory Layer, Orchestration). The **Capability Forge** is the meta-layer that feeds all of these: it reads the agent roster, identifies capability gaps, produces SKILL.md files / plugin bundles / MCP configs that close those gaps, and collaborates with research-lead when deep investigation is needed. It is **downstream** of research, not a competing research agent.

## Sub-questions (amplified from the one-line seed)

1. Ecosystem state (skills): canonical Claude Code Skills format in 2026, triggering mechanics, patterns across the 4 installed marketplaces.
2. Ecosystem state (plugins): what a plugin bundle can ship, install/version/update flow, overlap with existing installed plugins.
3. MCP ecosystem map: top 30-50 MCP servers by relevance to Akash's workforce; next-to-install priorities.
4. Existing skill-authoring agents in the wild: official skill-creator, Voyager skill library, MetaGPT SkillLibrary, AutoGen tool generation, Toolformer/Gorilla.
5. Community agent rosters: wshobson/agents, VoltAgent/awesome-claude-code-subagents, vijaythecoder; patterns Akash's flat agents/ dir lacks.
6. Skill composition academic prior art: Toolformer, Gorilla, ToolLLM, STaR, Voyager, Eureka, ACE; metric for "this skill produced value".
7. Internal gap analysis: top 5-10 missing capabilities the Forge should build first.
8. Collaboration protocol design: file-drop vs synchronous handoff with research-lead.
9. Architecture debate: single meta-agent vs mini-team vs skill-loop vs orthogonal meta-layer.
10. Adversary sweep: SEO / astroturf risk on skill marketplaces, MCP server lists, agent roster repos. Trust model per source.

## Acceptance criteria

- Round 1 wide evidence to `EVIDENCE/*.md` covering all 10 sub-questions.
- HYPOTHESES.md with 4 architectures scored on 5 dimensions.
- SYNTHESIS.md locks architecture choice with ≥3 primary-source citations per load-bearing claim.
- Moderator debate on single-agent-vs-team if synthesist reports contradictions.
- Skeptic + adversary + evaluator all clear before "high confidence".
- Final deliverables §1-10 writable verbatim: persona frontmatter, workspace layout, CLAUDE.md delta, smoke test launch prompt.

## Known constraints (binding on design)

- All Opus max effort. Every agent file MUST have `model: opus` + `effort: max`.
- No sub-sub-spawning. If Forge is a team, lead operates in adopted-persona mode when called as subagent.
- Names must not collide with existing `~/.claude/agents/**` files.
- Downstream of research, not a competitor.
- File-based memory contract: `~/.claude/agent-memory/<agent>/MEMORY.md`.
- All §1-10 deliverables must be writable verbatim.

## Definition of done

Downstream executor can, reading only SYNTHESIS.md's "Ready-to-write artifacts" section:
1. Write N persona files.
2. Write PROTOCOL.md (or skip if single agent).
3. Create workspace scaffold.
4. Apply CLAUDE.md delta.
5. Run smoke test that produces a working SKILL.md for the top-priority gap.

No TBD. No "recommended: consider X or Y".
