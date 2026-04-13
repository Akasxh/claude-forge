# Librarian — canonical Claude Code Skills / Plugins / MCP spec (2026)

All load-bearing schemas and conventions extracted from Anthropic-primary sources. No inference, no paraphrase where quotes suffice.

## Source provenance

| Source | URL | Retrieved | Tier |
|---|---|---|---|
| Claude Code Skills docs | `https://code.claude.com/docs/en/skills` | 2026-04-12 | STRONG-PRIMARY (Anthropic) |
| Claude Code Plugins docs | `https://code.claude.com/docs/en/plugins` | 2026-04-12 | STRONG-PRIMARY (Anthropic) |
| Claude Code Sub-agents docs | `https://code.claude.com/docs/en/sub-agents` | 2026-04-12 | STRONG-PRIMARY (Anthropic) |
| Agent Skills best practices | `https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` | 2026-04-12 | STRONG-PRIMARY (Anthropic) |
| Official MCP Registry | `https://registry.modelcontextprotocol.io` | 2026-04-12 | STRONG-PRIMARY (Anthropic+GitHub+Microsoft+PulseMCP) |
| Agent Skills open standard | `https://agentskills.io` | 2026-04-12 | STRONG-PRIMARY (cross-vendor) |
| Official skill-creator plugin (on disk) | `~/.claude/plugins/cache/claude-plugins-official/skill-creator/d53f6ca4cdb0/` | read 2026-04-12 | STRONG-PRIMARY (Anthropic) |

## SKILL.md frontmatter schema — exact, from `code.claude.com/docs/en/skills`

All fields optional. Only `description` is **recommended** (not required).

| Field | Required | Description (verbatim) |
|---|---|---|
| `name` | No | "Display name for the skill. If omitted, uses the directory name. Lowercase letters, numbers, and hyphens only (max 64 characters)." |
| `description` | Recommended | "What the skill does and when to use it. Claude uses this to decide when to apply the skill. If omitted, uses the first paragraph of markdown content. Front-load the key use case: descriptions longer than 250 characters are truncated in the skill listing to reduce context usage." |
| `argument-hint` | No | "Hint shown during autocomplete to indicate expected arguments. Example: `[issue-number]` or `[filename] [format]`." |
| `disable-model-invocation` | No | "Set to `true` to prevent Claude from automatically loading this skill. Use for workflows you want to trigger manually with `/name`. Default: `false`." |
| `user-invocable` | No | "Set to `false` to hide from the `/` menu. Use for background knowledge users shouldn't invoke directly. Default: `true`." |
| `allowed-tools` | No | "Tools Claude can use without asking permission when this skill is active. Accepts a space-separated string or a YAML list." |
| `model` | No | "Model to use when this skill is active." |
| `effort` | No | "Effort level when this skill is active. Overrides the session effort level. Default: inherits from session. Options: `low`, `medium`, `high`, `max` (Opus 4.6 only)." |
| `context` | No | "Set to `fork` to run in a forked subagent context." |
| `agent` | No | "Which subagent type to use when `context: fork` is set." |
| `hooks` | No | "Hooks scoped to this skill's lifecycle. See [Hooks in skills and agents] for configuration format." |
| `paths` | No | "Glob patterns that limit when this skill is activated. Accepts a comma-separated string or a YAML list. When set, Claude loads the skill automatically only when working with files matching the patterns." |
| `shell` | No | "Shell to use for `` !`command` `` and ` ```! ` blocks in this skill. Accepts `bash` (default) or `powershell`." |

**Stricter schema from `platform.claude.com/.../best-practices`**:
- `name`: max 64 chars, lowercase/number/hyphen, no XML tags, **no reserved words "anthropic" or "claude"**.
- `description`: max 1024 chars, non-empty, no XML tags.

**Triggering rule**: "Each entry is capped at 250 characters regardless of budget." Front-load use case keywords or they're truncated.

**Triggering-budget math**: "All skill names are always included, but if you have many skills, descriptions are shortened to fit the character budget, which can strip the keywords Claude needs to match your request. The budget scales dynamically at 1% of the context window, with a fallback of 8,000 characters. To raise the limit, set the `SLASH_COMMAND_TOOL_CHAR_BUDGET` environment variable."

## Skill location scope table (verbatim)

| Location | Path | Applies to |
|---|---|---|
| Enterprise | See managed settings | All users in organization |
| Personal | `~/.claude/skills/<skill-name>/SKILL.md` | All your projects |
| Project | `.claude/skills/<skill-name>/SKILL.md` | This project only |
| Plugin | `<plugin>/skills/<skill-name>/SKILL.md` | Where plugin is enabled |

Priority: **enterprise > personal > project**. Plugin skills use `plugin-name:skill-name` namespace and cannot conflict with other levels.

## Skill directory layout (canonical)

```
my-skill/
├── SKILL.md           # required, entrypoint, YAML frontmatter + markdown
├── reference.md       # loaded when needed
├── examples.md        # loaded when needed
└── scripts/
    └── helper.py      # executed, not loaded
```

## Progressive disclosure — three levels (verbatim from skill-creator SKILL.md)

1. **Metadata** (name + description) — Always in context (~100 words per skill)
2. **SKILL.md body** — In context whenever skill triggers (< 500 lines ideal)
3. **Bundled resources** — As needed (unlimited, scripts can execute without loading)

## Skill lifecycle in session (verbatim)

"When you or Claude invoke a skill, the rendered SKILL.md content enters the conversation as a single message and stays there for the rest of the session. Claude Code does not re-read the skill file on later turns, so write guidance that should apply throughout a task as standing instructions rather than one-time steps."

"Auto-compaction carries invoked skills forward within a token budget. When the conversation is summarized to free context, Claude Code re-attaches the most recent invocation of each skill after the summary, keeping the first 5,000 tokens of each. Re-attached skills share a combined budget of 25,000 tokens."

## Writing-style guidance (from best-practices, verbatim)

**Conciseness bar**: "Only add context Claude doesn't already have. Challenge each piece of information: 'Does Claude really need this explanation?' 'Can I assume Claude knows this?' 'Does this paragraph justify its token cost?'"

**Description must be third person**: "The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems."
- Good: "Processes Excel files and generates reports"
- Avoid: "I can help you process Excel files"
- Avoid: "You can use this to process Excel files"

**Naming convention**: gerund form preferred — `processing-pdfs`, `analyzing-spreadsheets`. Acceptable alternatives: noun phrases (`pdf-processing`), action-oriented (`process-pdfs`). Avoid vague: `helper`, `utils`, `tools`.

**Degrees of freedom**: match specificity to task fragility.
- **High freedom** (text instructions) — multiple valid approaches, context-dependent.
- **Medium freedom** (pseudocode/parametric scripts) — preferred pattern exists, variation okay.
- **Low freedom** (specific scripts, no params) — fragile, error-prone, consistency critical.

**Evaluation-driven development** (verbatim):
1. Identify gaps: run Claude on representative tasks without a Skill; document failures.
2. Create evaluations: build three scenarios that test these gaps.
3. Establish baseline: measure Claude's performance without the Skill.
4. Write minimal instructions: create just enough content to address gaps and pass evals.
5. Iterate.

**The "Claude A / Claude B" iteration loop** (critical for the Forge architecture):
- Claude A = helper, refines the skill.
- Claude B = agent using the skill, reveals gaps through real usage.
- Observe Claude B behavior → feed insights back to Claude A → revise → re-test.
- This is the reference loop the Forge must implement.

**"Pushy" descriptions** (cross-reference from skill-creator SKILL.md): Claude "undertriggers" skills — describes tendency to not use them when they'd be useful. Counter by writing pushy descriptions: "Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"

## Plugin spec — exact, from `code.claude.com/docs/en/plugins`

### Plugin manifest (`.claude-plugin/plugin.json`)

```json
{
  "name": "my-first-plugin",
  "description": "A greeting plugin to learn the basics",
  "version": "1.0.0",
  "author": {"name": "Your Name"}
}
```

Fields (verbatim):
- `name` — Unique identifier and skill namespace. Skills prefixed with this (e.g., `/my-first-plugin:hello`).
- `description` — Shown in plugin manager.
- `version` — Semantic versioning.
- `author` — Optional.

Additional fields exist: `homepage`, `repository`, `license` — see plugin manifest schema.

### Plugin directory structure (canonical)

| Directory | Location | Purpose |
|---|---|---|
| `.claude-plugin/` | plugin root | Contains `plugin.json` manifest |
| `skills/` | plugin root | Skills as `<name>/SKILL.md` directories |
| `commands/` | plugin root | Skills as flat Markdown files (legacy; use `skills/` for new plugins) |
| `agents/` | plugin root | Custom agent definitions |
| `hooks/` | plugin root | Event handlers in `hooks.json` |
| `.mcp.json` | plugin root | MCP server configurations |
| `.lsp.json` | plugin root | LSP server configurations |
| `bin/` | plugin root | Executables added to Bash `PATH` while plugin is enabled |
| `settings.json` | plugin root | Default settings applied when plugin is enabled |

**Critical warning from docs**: "Don't put `commands/`, `agents/`, `skills/`, or `hooks/` inside the `.claude-plugin/` directory. Only `plugin.json` goes inside `.claude-plugin/`. All other directories must be at the plugin root level."

### Plugin install flow

- Dev: `claude --plugin-dir ./my-plugin` for local testing.
- Production: install via marketplace, listed in `~/.claude/plugins/installed_plugins.json`.
- Reload without restart: `/reload-plugins`.
- Skills namespace: `plugin-name:skill-name` (e.g., `/my-first-plugin:hello`).

## Subagent spec — exact, from `code.claude.com/docs/en/sub-agents`

Key excerpt (from persisted output `toolu_01Up6id8fw338DiHs2eQAWZy.txt`, to be re-read if needed):

- Subagents defined as `.md` files in `.claude/agents/` (project) or `~/.claude/agents/` (personal).
- Frontmatter fields: `name`, `description`, `tools` (optional whitelist), `model`, `effort`, `color`.
- **Preload skills into subagents** — there's a `skills` field in subagent frontmatter that pre-injects skill content at subagent startup (vs on-demand in main session).
- **Subagents cannot spawn subagents** — confirmed architectural constraint in the docs and in MEMORY.md lesson 6.
- **Agent teams vs sub-agents**: "If you need multiple agents working in parallel and communicating with each other, see [agent teams] instead. Subagents work within a single session; agent teams coordinate across separate sessions." **This is a new 2026 primitive I must flag for the Forge architecture — agent teams is distinct from subagents, with cross-session coordination.** Need follow-up on `docs.claude.com/en/agent-teams`.

## MCP spec (2026 state)

- **Official MCP Registry at `https://registry.modelcontextprotocol.io`**, launched in preview Sep 8, 2025, backed by Anthropic + GitHub + PulseMCP + Microsoft.
- As of Oct 24, 2025: API freeze at v0.1. No breaking changes for ≥1 month, validation window for v1 GA.
- Registry API is open-source; parent OpenAPI spec is open-source; sub-registries can be built.
- In the Claude Code plugin system: MCP servers live in `.mcp.json` at the plugin root, same format as top-level `~/.claude/mcp_servers.json`.

## Agent Skills open standard

- Claude Code skills follow the **Agent Skills open standard** at `https://agentskills.io`.
- "Works across multiple AI tools."
- Claude Code extends with: invocation control, subagent execution, dynamic context injection.
- The standard itself is cross-vendor — an open spec skill should work in Claude Code, Cursor, Continue.dev, etc.

## What this means for the Forge architecture

**Critical for §1-§10 deliverables**:

1. **Skill files are cheap** — metadata-only cost until triggered, SKILL.md body < 500 lines, bundled resources are free until read. The Forge should prefer fine-grained skills (one concern each) over mega-skills.

2. **Description is load-bearing** — it's the triggering mechanism, capped at 250 chars for primary budget, 1024 chars hard max. First 250 chars must contain keywords Claude will match. The Forge must author descriptions with "pushy" language to counter Claude's undertriggering tendency.

3. **Reserved words** — `name` cannot be `anthropic`, `claude`. Forge's own naming must avoid these.

4. **Effort: max** — the `effort` field in SKILL.md supports `low|medium|high|max` where max is Opus-4.6-only. Akash's doctrine is max everywhere; the Forge's authored skills should inherit (not set) effort, since the session will already be at max.

5. **`context: fork` is new 2026 primitive** — allows a skill to run in a forked subagent context with a specified `agent` type. **This is a game-changer**: the Forge's "run skill-creator eval loop" step can use `context: fork` to spawn an isolated subagent with the right agent config, without needing a real subagent-subagent spawn. This may let the Forge operate as a single agent (H1) more easily than the no-sub-sub-spawning rule implies.

6. **Skill lifecycle is one-shot-load-and-persist** — skills don't re-read on later turns. Write instructions as standing contracts, not one-time steps.

7. **Plugin directory is cleanly separable from agent directory** — the Forge can output to two places: (a) SKILL.md files in `~/.claude/skills/<name>/` for personal skills, (b) full plugin bundles in `~/.claude/forge-outputs/<plugin>/` for marketplace-bound skills.

8. **MCP registry exists** — the Forge's "aggregate from internet" step has a single canonical endpoint: `registry.modelcontextprotocol.io` with an OpenAPI spec. This replaces scraping awesome-lists. Sub-registries can be built on top.

9. **Agent teams are a distinct 2026 primitive** — needs follow-up in round 2. If agent teams support cross-session coordination natively, the Forge's research-handoff protocol may simplify.

10. **Official `skill-creator` plugin is already installed** — the Forge should **invoke it as a skill**, not rewrite its eval loop. Akash's `installed_plugins.json` shows `skill-creator@claude-plugins-official` active. The Forge's job is to wrap skill-creator with: (a) gap detection, (b) internet aggregation, (c) research handoff, (d) curation — the authoring + testing loop is already solved by skill-creator.

## Remaining follow-up

- [ ] Agent teams doc (`docs.claude.com/en/agent-teams` or equivalent) — for cross-session coordination.
- [ ] MCP Registry API OpenAPI spec — for the Forge scout to query programmatically.
- [ ] `plugins-reference` full doc — for the full plugin.json schema, marketplace.json schema.
