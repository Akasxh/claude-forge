# Web-miner — marketplace landing pages, registries, Anthropic announcements

## Source provenance

| URL | Retrieved | Content captured |
|---|---|---|
| `https://code.claude.com/docs/en/skills` | 2026-04-12 | Full Skills docs, frontmatter schema, progressive disclosure, shell injection, context-fork, lifecycle — captured to librarian.md |
| `https://code.claude.com/docs/en/plugins` | 2026-04-12 | Full Plugins docs, plugin.json manifest, directory structure, install flow — captured to librarian.md |
| `https://code.claude.com/docs/en/sub-agents` | 2026-04-12 (persisted to `/home/akash/.claude/projects/-home-akash-PROJECTS-claude/9ab200b7-d049-4ed8-b247-afb6a329ac93/tool-results/toolu_01Up6id8fw338DiHs2eQAWZy.txt`) | Subagent spec, 51KB; excerpt captured below |
| `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` | 2026-04-12 | Skill authoring best practices in full — captured to librarian.md |
| `https://registry.modelcontextprotocol.io/v0/servers?*` | 2026-04-12 (via `gh api`) | MCP Registry queries — captured to github-miner.md |
| `https://nordicapis.com/getting-started-with-the-official-mcp-registry-api/` | 2026-04-12 | MCP Registry API spec — captured to github-miner.md + librarian.md |
| `https://simonwillison.net/2025/Oct/16/claude-skills/` | 2026-04-12 | Simon Willison's take — captured to historian.md |
| `https://claude.com/blog/skills` | 2026-04-12 | Anthropic skills launch blog — captured to historian.md |
| `https://arxiv.org/abs/2305.16291` | 2026-04-12 | Voyager abstract — captured to historian.md |
| `https://arxiv.org/abs/2510.04618` + `/html/2510.04618v1` | 2026-04-12 | ACE method + ablation — captured to historian.md |
| `https://raw.githubusercontent.com/VoltAgent/awesome-claude-code-subagents/main/README.md` | 2026-04-12 | Full 130+ specialist taxonomy — captured to github-miner.md |
| `https://github.com/wshobson/agents` | 2026-04-12 | 33.4k stars, 182 agents + 149 skills + 77 plugins — captured to github-miner.md |

## Subagent spec key facts (from the persisted capture)

From `/home/akash/.claude/projects/-home-akash-PROJECTS-claude/9ab200b7-d049-4ed8-b247-afb6a329ac93/tool-results/toolu_01Up6id8fw338DiHs2eQAWZy.txt` (51KB, full spec):

- Subagents are `.md` files in `.claude/agents/` (project) or `~/.claude/agents/` (personal).
- Frontmatter: `name`, `description`, `model`, `tools` (optional allowlist), `color`, `effort`.
- Invocation: via `Task` tool with `subagent_type: <name>`, OR automatic based on description match.
- **Preload skills** — there IS a `skills` field in subagent frontmatter. Syntax pre-injects skill bodies at subagent startup. This matters: the Forge's smoke test can use `skills: [skill-creator]` in its own frontmatter to guarantee skill-creator is loaded when Forge dispatches.
- **Cross-session coordination not in sub-agents, in `agent-teams`** — the doc explicitly says "If you need multiple agents working in parallel and communicating with each other, see agent teams instead. Subagents work within a single session; agent teams coordinate across separate sessions."
- This **agent-teams** primitive is distinct from subagents. Confirms what librarian flagged — needs follow-up on the exact docs page. This is new-to-me 2026 primitive.

## Claude.ai launch timeline for Skills (cross-source)

- **Oct 16, 2025**: Anthropic announces Agent Skills, `claude.com/blog/skills`.
- **Oct 16, 2025**: Simon Willison posts "Claude Skills are awesome, maybe a bigger deal than MCP."
- **Oct 24, 2025**: MCP Registry API enters v0.1 freeze (1+ month no breaking changes window).
- **Dec 19, 2025**: Anthropic makes Agent Skills an open standard at `agentskills.io` (cross-vendor).
- **Mar 2026**: Skill-creator updated with eval loop enhancements per Medium article "Anthropic (New) Skill-Creator Measures If Your Agent Skills Work."
- **Current (Apr 2026)**: Akash's installed `skill-creator@claude-plugins-official` dates to `2026-03-21` per installed_plugins.json with last update `2026-04-09`. Fresh.

## Competing awesome-list gaming pattern

Observed three competing "awesome-claude-skills" repos, all in the high-thousands-to-low-tens-of-thousands star range, updated on the same day:

| Repo | Stars | Last commit |
|---|---|---|
| ComposioHQ/awesome-claude-skills | 53003 | 2026-04-11 |
| travisvn/awesome-claude-skills | 11034 | 2026-04-11 |
| BehiSecc/awesome-claude-skills | 8350 | 2026-04-11 |

Plus `alirezarezvani/claude-skills` (10.5k, already installed, non-awesome naming) and `vijaythecoder/awesome-claude-agents` (4.1k). The `ComposioHQ` repo has 53k stars, which is suspicious for a "curated list" format. ComposioHQ is a YC-backed company — their star count may reflect authentic developer interest in their SDK, which makes it less of an astroturf red flag than naive scraping would suggest, but the pattern **warrants adversary pass**.

## Marketplaces already on-disk that the Forge can use as reference libraries

1. **claude-plugins-official** — Anthropic's official: 17 plugins including skill-creator, hookify, commit-commands, etc. Gold standard.
2. **huggingface-skills** — HF: 12 skills wrapping HF Hub + datasets + training + papers. Good for ML-research patterns.
3. **ai-research-skills** (Orchestra-Research) — 91 ML skills in numbered taxonomy. Akash's personal `~/.claude/skills/` appears populated from this.
4. **claude-code-skills** (alirezarezvani) — 10.5k stars, contains `engineering-team/` with 50+ production skill bundles, `agents/` across 10 departments, `commands/`, `orchestration/`. **This is the closest reference implementation for what Akash is building.**

## Reference: self-improving-agent sub-skills (from claude-code-skills)

The alirezarezvani marketplace includes `engineering-team/self-improving-agent/` which is a **production reference** for MEMORY.md → rules → skill extraction pipeline. Akash should cite this when designing the Forge. See cartographer.md and linguist.md for details.

## Missing primary sources (round 2 follow-ups)

- [ ] Full Voyager PDF — > 10MB limit on WebFetch. Either wget+local read or grab summary from voyager.minedojo.org.
- [ ] `code.claude.com/docs/en/agent-teams` — confirm existence and read the spec.
- [ ] `agentskills.io` — read the open standard spec.
- [ ] `anthropics/skills` repo directory listing via `gh api repos/anthropics/skills/contents/skills` — get actual skill list.

## Key finding for synthesist

**The Claude Code 2026 primitive stack**:

```
┌──────────────────────────────────────────────────────────────┐
│  Agent Teams (cross-session parallel collaboration)          │  <-- NEW 2026 primitive, need to understand
├──────────────────────────────────────────────────────────────┤
│  Subagents (within-session delegation)                       │  <-- mature
├──────────────────────────────────────────────────────────────┤
│  Plugins (packaged bundles: commands + agents + hooks + MCP) │  <-- mature
├──────────────────────────────────────────────────────────────┤
│  Skills (progressive-disclosure playbooks)                   │  <-- Oct 2025 primitive
├──────────────────────────────────────────────────────────────┤
│  MCP Servers (external tool protocol)                        │  <-- mature
├──────────────────────────────────────────────────────────────┤
│  Hooks (deterministic event handlers)                        │  <-- mature
├──────────────────────────────────────────────────────────────┤
│  Commands (legacy, merged into skills)                       │  <-- deprecated
└──────────────────────────────────────────────────────────────┘
```

Each layer has a distinct role. The Forge lives at the **Skills layer primarily**, but reads the **Agent** and **Plugin** layers to understand what's there, and writes to the **Skills** and **Plugins** layers (via SKILL.md files and plugin bundles).

The **Agent Teams** primitive is the one I don't yet fully understand, and it matters because Akash's CLAUDE.md says "the Research Team is the first fully-collaborative subagent team in this setup" — suggesting agent-teams might be the runtime primitive that powers his planned teams, not just the metaphor. Round 2 must resolve this.
