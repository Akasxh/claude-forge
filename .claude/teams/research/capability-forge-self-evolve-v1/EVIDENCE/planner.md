# Planner — dispatch recommendation for capability-forge-self-evolve-v1

## Question classification

- **Question class**: **compound** — (a) decisional (architecture: 1-agent vs team vs loop vs meta-layer), (b) definitional (what is the Claude Code Skills/Plugins substrate in 2026), (c) prior-art (skill-authoring agents in the wild, Voyager/ACE/Toolformer frame), (d) gap analysis (read Akash's agent roster, diff against community rosters, spot holes). Multi-class question, not single-shape.
- **Complexity**: **complex** — Anthropic scaling rule says 5-10+ specialists, parallel, multi-round. Akash's meta-task brief already prescribed 8 round-1 specialists; that matches the scaling rule exactly.
- **Anthropic scaling rule says**: 8-10 specialists round 1, 2-3 rounds to high confidence.
- **Past lessons from MEMORY.md applied**:
  - **"Dispatch breadth follows Anthropic scaling rule"** — 8 specialists is the right number; less would under-dispatch given the 10 sub-questions.
  - **"When the user prompt is short, distrust initial sub-question list to catch latest 14 days"** — librarian MUST hit `docs.claude.com` / `code.claude.com` for current skills spec. The skill spec format may have evolved since the 2025 posts; don't trust memorized schemas.
  - **"Adversary catches what skeptic cannot: corpus-level fraud"** — AI skill marketplaces are SEO targets. Akash already called this out in the brief. Adversary must run mandatorily, not conditionally.
  - **"Reuse v1 evidence on rerun; append addenda"** — the three parallel sessions launched today may produce overlapping evidence. If engineering-team-self-evolve's cartographer already inventoried the flat agents/ dir, flag that for REUSE. Check `~/.claude/teams/research/engineering-team-self-evolve-v1/EVIDENCE/` before double-dispatching cartographer.
  - **"Subagents cannot spawn subagents"** — since this session is running as a subagent, the specialists must be adopted-persona lens-passes, not real dispatches. The lead reads each specialist file as a contract and executes the method itself, writing to the specialist's evidence file.
  - **"The skeptic attacks reasoning; the adversary attacks the corpus"** — both mandatory for this session.
  - **"REFRAME is a valid moderator verdict"** — the single-agent-vs-team debate may reframe to "single-agent now, team later when a second gap type appears" rather than force A or B.
  - **"REPORTED-NOT-VERIFIED tier exists"** — MCP server star counts and marketplace download stats are not always reachable; use the tiered scale.

## Recommended opening dispatch (Round 1) — 8 specialists in parallel adopted-persona passes

1. **cartographer** — Structural inventory. Read `~/.claude/agents/**` (flat + research/), `~/.claude/skills/**` (sample 10 random SKILL.mds + count total), `~/.claude/plugins/**` (installed_plugins.json + marketplace dirs). Classify each by capability type: tool-using, code-writing, reasoning, orchestrating, reviewing, documenting. Cross-reference against the 10 sub-questions and the Research Team v2 roster. Output a gap table: capability needed → is it covered? → by what? Do NOT duplicate engineering-team-self-evolve's cartographer work — check that workspace first and CITE its evidence file if it already did the inventory.

2. **librarian** — Canonical Claude Code Skills spec. Primary source = the official `skill-creator` plugin I already read (SKILL.md, analyzer.md, grader.md, schemas.md). Secondary = `docs.claude.com` and `code.claude.com` via WebFetch for any 2026 updates to the SKILL.md frontmatter schema, plugin manifest format, and triggering rules. Tertiary = `modelcontextprotocol.io` for the official MCP spec. Report: (a) exact SKILL.md frontmatter fields and what each does, (b) progressive disclosure mechanics (metadata / body / bundled resources), (c) plugin.json manifest format, (d) how MCP servers are registered and invoked.

3. **github-miner** — Community agent/skill/plugin rosters and MCP server registries via `gh api`. Targets: `anthropics/skills`, `anthropics/claude-code`, `wshobson/agents`, `VoltAgent/awesome-claude-code-subagents`, `vijaythecoder/awesome-claude-agents`, `punkpeye/awesome-mcp-servers`, `modelcontextprotocol/servers`, `modelcontextprotocol/registry`, `alirezarezvani/claude-skills`, `huggingface/skills`, `Orchestra-Research/AI-Research-SKILLs`. For each: star count, last commit date, structure (flat vs hierarchical), and top 5-10 items. Specifically compare against Akash's flat agents/ dir to flag specialists other rosters have that Akash lacks.

4. **historian** — Academic and industry prior art on self-improving skill libraries and tool synthesis. Primary targets: Voyager (Wang et al. 2023 arxiv 2305.16291, skill library for Minecraft agents — the reference impl), ACE (arxiv 2510.04618, already known, cite it and note the retrospector-pipeline parallel), Toolformer (Schick et al. 2023 arxiv 2302.04761, self-taught API use), Gorilla (Patil et al. 2023 arxiv 2305.15334, tool selection via retrieval), ToolLLM (Qin et al. 2023 arxiv 2307.16789), STaR (arxiv 2203.14465), Eureka (arxiv 2310.12931, LLM-designed reward function = LLM-designed skill), MetaGPT SkillLibrary (arxiv 2308.00352). Include HF daily papers for the last 14 days for any 2026 releases on skill authoring. Report: what metric each uses to score "this skill produced value", what triggers adding a new skill, what the self-improvement loop looks like.

5. **web-miner** — Marketplace scraping and MCP directory enumeration via WebFetch. Targets: (a) `https://docs.claude.com/en/docs/claude-code/plugins` and `https://docs.claude.com/en/docs/claude-code/sub-agents` for the official spec; (b) `https://modelcontextprotocol.io/registry` or equivalent for the MCP registry if it exists in 2026; (c) `https://github.com/punkpeye/awesome-mcp-servers` raw README for the curated list; (d) any plugin marketplace index page. Dump raw HTML/markdown to `raw/marketplaces/`. Do NOT try to JS-render if plain HTML suffices — save Playwright for a follow-up if simpler approaches fail.

6. **linguist** — SKILL.md description triggering patterns. Read 15 SKILL.mds from the three installed marketplaces (5 each from ai-research-skills, huggingface-skills, claude-code-skills) and extract: what triggering phrases are used ("Use when X", "Expert guidance for Y"), how length correlates with specificity, how "pushy" language (the skill-creator reference explicitly recommends pushy descriptions) affects trigger probability. Report the pattern library + the top 5 anti-patterns. This feeds directly into the Forge's SKILL.md-author specialist.

7. **adversary** — Corpus-level red team on every marketplace, registry, and agent roster the other specialists reference. Attack: (a) star-count inflation on `awesome-*` repos (who gamed what), (b) author reputation on unofficial MCP servers, (c) last-commit-date decay (dead repos still ranked), (d) SEO-farm patterns on "best claude code skills 2026" blog posts, (e) plausible astroturf patterns on community rosters. Must flag any source that fails the trust test with a REJECTED or REPORTED-NOT-VERIFIED tier before it gets into synthesis. Akash already called this out as mandatory.

8. **synthesist** (round 1 EXIT pass, not opener) — Wait for round 1 specialists to write, then merge, build the claim matrix, flag contradictions, and hand contradictions to the moderator. You are ROUND 2 but I'm scheduling you now because the lead needs you immediately after the wide round, not after a gate delay.

## Recommended follow-ups (Round 2)

- **synthesist** — unconditional, always after round 1.
- **moderator** — conditional on synthesist reporting a contradiction. Specifically: if cartographer and github-miner disagree on what "capability gaps" means, moderator runs 3-round debate. Equally likely to hit single-agent-vs-team question directly.
- **empiricist** — conditional on any testable hypothesis (e.g., "does skill-creator's trigger-optimizer actually improve trigger rate?"). Defer to round 3 unless the gap is small enough to run in-session.

## Recommended gates

- **skeptic** — after round 2 (post-synthesist, post-moderator). Mandatory before high confidence. Attacks reasoning in SYNTHESIS.md's architecture choice.
- **adversary** — after round 1, parallel to synthesist if possible. Blocking on any architectural claim sourced from a non-Anthropic repository.
- **evaluator** — always last, after skeptic AND adversary. Grades against Anthropic's 5-dim rubric.
- **retrospector** — at session close, unconditional. Lessons to `~/.claude/agent-memory/research-lead/MEMORY.md`.

## Blind spots I flag

- **tracer not recommended** — no execution-path question here. Flag for second-guess: if synthesist finds the Forge needs to trace a runtime invocation of skill-creator to understand how it's actually loaded at session start, tracer becomes load-bearing. Revisit in round 2.
- **archaeologist not recommended** — no git-history question. Flag for second-guess: if the debate is "does skill-creator's architecture represent recent Anthropic preference, or was it frozen in 2025?", archaeologist reads the commits on the plugin repo. Revisit conditionally.
- **empiricist deferred** — the cleanest test of this session would be to actually run skill-creator on a gap and see if it produces a usable SKILL.md. But that's a *smoke test deliverable*, not a round-1 evidence pass. Keep it in §10 of the deliverable, not in round 1.

## Expected rounds to high confidence

**2-3 rounds**. Round 1 wide, round 2 synthesist + moderator + skeptic + adversary, round 3 optional empiricist if a testable claim surfaces + evaluator + retrospector.

## Budget check

Complex research: 8 specialists round 1 × ~15 tool calls each + round 2 (synthesist + moderator + skeptic + adversary = 4 × ~10 calls) + round 3 (evaluator + retrospector = 2 × ~5 calls) ≈ 150 tool calls. Akash's Max plan budget is not the constraint; context is the constraint. At 1M context, we are nowhere near limits.

Approved.

## Confidence in this plan

**HIGH** — the scaling rule, the memory lessons, the specialist personas, and the question shape all align on the same recommendation. The only live uncertainty is whether round 2's moderator debate will REFRAME the single-agent-vs-team question into something different (likely, per MEMORY.md lesson 9).
