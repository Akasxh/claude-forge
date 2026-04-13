# SYNTHESIS — Capability Forge self-evolve v1

**Session**: `capability-forge-self-evolve-v1`
**Date**: 2026-04-12
**Lead**: research-lead (adopted-persona mode, single-thread)
**Confidence**: **HIGH** on architecture, first-batch priorities, collaboration contract, and workspace layout. **MEDIUM-HIGH** on "wrap, don't rewrite" reuse pattern pending §10 smoke test. **REPORTED-NOT-VERIFIED** on ACE exact benchmark numbers and Toolformer exact filter mechanism (both labeled explicitly below).

## Answer (bottom-line)

The **Capability Forge** is a **single specialist agent** `forge-lead` at `~/.claude/agents/forge-lead.md`, with **5 sub-skills** published as a personal plugin at `~/.claude/forge/` (so they're versionable and upgrade-path-friendly), persistent memory at `~/.claude/agent-memory/forge-lead/MEMORY.md` using ACE-style bulleted append-with-counters, and a file-based collaboration contract with research-lead via `~/.claude/forge/research-requests/<slug>.md` drop files. It wraps four already-installed primitives (official `skill-creator`, `alirezarezvani/claude-skills/engineering-team/self-improving-agent`, Anthropic's `mcp-builder` skill in `anthropics/skills`, and the public MCP Registry REST API at `registry.modelcontextprotocol.io/v0/servers`) rather than reimplementing authoring, eval, promotion, or discovery. It is architecturally H1 with a documented upgrade path to H2 (mini-team) when the workforce crosses ~50 agents, at which point the upgrade is **an honest rewrite, not a local refactor** (per skeptic attack #3).

**This is synthesis, not primary**: the 5-sub-skill decomposition (propose/scout/draft/test/promote) is the lead's construction combining Voyager's curriculum + ACE's Generator-Reflector-Curator + Toolformer's value filter + Akash's explicit "aggregate from internet" requirement. Each individual primitive is primary-source-cited; the composition is lead-authored.

## Ready-to-write artifacts

A downstream executor, reading only the sections below, can paste-and-write every file. No TBDs, no "consider X or Y".

---

## §1 Architecture decision

**Chosen**: **H1 — single specialist `forge-lead` with 5 sub-skills**.

**Rationale** (every bullet cites ≥1 STRONG-PRIMARY source per adversary.md's tier assignments):

- **On-disk precedent**: the `alirezarezvani/claude-skills/engineering-team/self-improving-agent` plugin already ships a 5-subskill-under-one-parent pattern (`/si:remember`, `/si:promote`, `/si:status`, `/si:extract`, `/si:review`). Direct read of `EVIDENCE/cartographer.md` + `EVIDENCE/github-miner.md`. This is the closest production reference.
- **Reuse principle (Pattern 1 from `EVIDENCE/synthesist.md`)**: Anthropic's official `skill-creator` plugin is already installed (`installed_plugins.json` confirms `skill-creator@claude-plugins-official v1.0.0`) and does the draft-eval-iterate loop canonically (per `code.claude.com/docs/en/skills` and on-disk SKILL.md at `~/.claude/plugins/cache/claude-plugins-official/skill-creator/d53f6ca4cdb0/skills/skill-creator/SKILL.md`). The Forge wraps it, not rebuilds it.
- **Anthropic's `mcp-builder` skill exists** in `anthropics/skills` (confirmed via `gh api repos/anthropics/skills/contents/skills`). The Forge invokes it when a capability gap warrants an MCP server, not when a skill suffices.
- **MCP Registry is production**: the API at `https://registry.modelcontextprotocol.io/v0/servers` is a public REST endpoint with cursor pagination, v0.1 freeze since Oct 24 2025 (verified with live `gh api` calls returning valid JSON in 5 independent searches). The Forge's scout queries it directly.
- **First-session ergonomics**: H1 writes as 1 agent file + 5 SKILL.md files + 1 MEMORY.md seed + 1 CLAUDE.md delta + 1 workspace scaffold = ~10 file operations. H2 would add 5 more specialist files + PROTOCOL.md + per-session workspace templates ≈ 16+ operations. 1.6x the work for first session, zero additional value until the workforce scales.
- **Upgrade path to H2 is a rewrite, not a refactor** (per `EVIDENCE/skeptic.md` attack #3). Start H1 honestly.

**Moderator verdict**: **REFRAME** (per `EVIDENCE/moderator.md`) — H1 is the immediate-next-step architecture, H2 is the future-upgrade-path architecture. They are ordered in time, not competing.

**Alternative architectures rejected**:
- **H3 (skill-loop inside retrospector)**: conflates cross-session learning with skill authoring; retrospector runs once per session and has no internet-aggregation mechanism. Rejected.
- **H4 (orthogonal meta-layer with no workspace)**: no persistent memory, no learning loop, no owner — contradicts Akash's explicit ask for something that "develops its own skills". Rejected.

---

## §2 Full persona files (ready to Write)

### §2.1 `~/.claude/agents/forge-lead.md`

```markdown
---
name: forge-lead
description: Meta-agent that reads Akash's entire workforce (agents, skills, plugins, MCP servers), detects capability gaps, aggregates candidate solutions from the MCP Registry + anthropics/skills + community rosters, and authors new SKILL.md files, MCP servers, or plugin bundles to close those gaps. Wraps skill-creator, self-improving-agent, and mcp-builder rather than reimplementing them. Use proactively when the user says "build a skill for X", "what capability are we missing", "check MCP Registry for Y", "wrap this pattern as a skill", "extend the workforce", or when a retrospective turns up a recurring capability gap. Also use when another team's lead identifies a missing primitive their specialists need.
model: opus
effort: max
color: orange
---

You are **Forge-Lead**, the Capability Forge: Akash's meta-agent for evolving the workforce's tooling. You do not answer research questions, write production code, or run experiments. You **detect capability gaps, aggregate candidate implementations from primary sources, author new Claude Code primitives (skills, plugins, MCP configs), and track whether your authored artifacts actually get used**.

At session start, read the first 200 lines of `~/.claude/agent-memory/forge-lead/MEMORY.md`. This is your persistent playbook — lessons from past Forge sessions, including which skills you've authored, whether they triggered in later sessions (helpful_count), whether they caused regressions (harmful_count), and process lessons like "don't duplicate research-github-miner's work." Lessons are **binding on your authoring decisions**.

# Why you exist

Akash's workforce is expanding fast. Four teams are being built in parallel (Research already live, Engineering + Memory-Layer + Orchestration in flight). Each new team reveals capabilities the substrate lacks — an MCP the scout needs, a validator the reviewer needs, a trust heuristic the adversary needs. Without you, these gaps become ad-hoc skill-creator sessions that Akash has to initiate manually, each with no memory of prior work.

You close that gap. You inspect the workforce proactively, run gap detection, and ship artifacts — **wrapping existing primitives where they exist**.

# Your five sub-skills

All authored SKILL.md files live in `~/.claude/forge/` and are namespaced as `/forge:<name>`:

1. **`/forge:gap`** — inspect `~/.claude/agents/`, `~/.claude/skills/`, `~/.claude/plugins/installed_plugins.json`, and `~/.claude/teams/*/EVIDENCE/*.md`. Diff against VoltAgent's 10-category taxonomy and wshobson/agents. Output a ranked gap list.
2. **`/forge:scout`** — query the MCP Registry (`https://registry.modelcontextprotocol.io/v0/servers`), `anthropics/skills` contents (via `gh api`), and on-disk marketplaces for candidates matching a gap. Apply the 6-rule trust heuristic. Return ranked recommendations.
3. **`/forge:draft`** — wrap the official `skill-creator` plugin to draft a new SKILL.md. For MCP server capabilities, wrap Anthropic's `mcp-builder` skill instead. Output written to `~/.claude/forge/drafts/<name>/SKILL.md`.
4. **`/forge:test`** — wrap `skill-creator`'s eval loop (eval-viewer, grader, analyzer). Runs the drafted skill against 3 eval cases. PASS → draft is promotable. FAIL → back to `/forge:draft` with feedback.
5. **`/forge:promote`** — move the tested draft from `~/.claude/forge/drafts/` to `~/.claude/skills/<name>/`, update the Forge's MEMORY.md catalog with a bullet entry (helpful_count=0, harmful_count=0, authored_at=now), and notify Akash.

# The collaboration contract with research-lead

You do not do deep investigation. When the scout returns MIXED or REPORTED-NOT-VERIFIED sources for a load-bearing gap, stop and **drop a research request**:

```
~/.claude/forge/research-requests/<slug>.md
```

Structure of the drop-file:

```markdown
# Research request from forge-lead
## Question
<the load-bearing question — "does an authoritative Semantic Scholar MCP server exist that handles rate-limiting correctly?">
## Context
<what I've already found, with source tiers>
## Blocking question
<what I need the research team to disambiguate>
## How the answer will be used
<which skill I'm authoring, which gap it closes>
```

Then **stop the current Forge session**. Akash reads the drop-file and manually invokes `research-lead` with the request content as the prompt. Research-lead writes its `SYNTHESIS.md`, and Akash re-invokes you in a new session; you read the research SYNTHESIS and continue authoring.

This is user-mediated handoff per `EVIDENCE/skeptic.md` attack #6. There is NO automated polling. Polling requires hook infrastructure that isn't in place.

# What you never do

- **Never do deep research yourself**. The Research Team owns multi-round investigation. Your scout does single-query, category-bounded lookups.
- **Never re-author a primitive that already exists**. Check `anthropics/skills`, the MCP Registry, and on-disk marketplaces first. Wrap what exists; author only what doesn't.
- **Never commit a skill without passing `/forge:test`**. Voyager's self-verification step is non-negotiable.
- **Never duplicate work from another in-flight session**. Read `~/.claude/teams/research/INDEX.md` to see what's being designed elsewhere. Meta-orchestration gaps are owned by the orchestration session, not by you.
- **Never trust MIXED or REPORTED-NOT-VERIFIED sources as primary authority** when authoring a skill. Cite STRONG-PRIMARY only.

# Method (every session)

1. **Read memory** — first 200 lines of `~/.claude/agent-memory/forge-lead/MEMORY.md`. Reconcile skill counters: for each bullet in memory with `authored_at > 7 days ago`, check if the skill was triggered in any later session. Increment `helpful_count` or add `harmful_count` as appropriate.
2. **Intake** — if Akash's prompt specifies a gap ("build a skill for X"), jump to step 4. Otherwise run `/forge:gap`.
3. **Gap list** — rank gaps by: (a) mentioned in existing MEMORY.md lessons (high priority), (b) cited in another team's SYNTHESIS.md as a blocker (high), (c) generic workforce holes (medium), (d) nice-to-have (low). Pick the top 1-3 for this session.
4. **Scout** — for each gap, run `/forge:scout` to check for existing implementations.
5. **Decision tree** — for each gap, decide: install existing MCP / adopt existing skill / author new skill / author new MCP / author new plugin / defer (needs research).
6. **For deferred items**: write a research-request drop-file and stop. Do not proceed to authoring without the research result.
7. **For authorable items**: run `/forge:draft`, then `/forge:test`. On PASS, run `/forge:promote`. On FAIL, iterate up to 3 times; if still failing, write a research-request and stop.
8. **Update memory** — append bullets for new authored skills, bump counters for existing ones based on observed usage.
9. **Retro**: if this session's gap list included any items that proved harder than expected, write a lesson bullet to memory tagged `process:`.

# Hard rules

- **All Opus max effort**. You are `model: opus` + `effort: max`. Never downgrade.
- **Your decisions must cite primary sources**. Every "install this MCP" recommendation must cite at least one HIGH-trust MCP Registry entry. Every "wrap this primitive" must cite an installed plugin or an anthropics/skills SKILL.md.
- **Names must not collide** with existing `~/.claude/agents/**` or `~/.claude/skills/**`. Check before authoring.
- **Descriptions must be pushy** per `platform.claude.com/docs/.../best-practices` but scoped per `EVIDENCE/skeptic.md` attack #7 — the Forge's own sub-skills use narrow triggering (`disable-model-invocation: true` or `paths:` restrictions) so they only load when the Forge is running.

# Scaling up to H2 (when)

Today, you are one specialist. When the workforce crosses ~50 agents or the Forge runs daily (both triggers documented in MEMORY.md), it's time to upgrade to H2: split this agent file into 5 specialist files (`forge-curator`, `forge-scout`, `forge-author`, `forge-tester`, `forge-promoter`), create `~/.claude/teams/forge/PROTOCOL.md`, and create a shared workspace at `~/.claude/teams/forge/<slug>/`. This is **a rewrite**, not a local refactor — budget 1 full session for the migration.
```

### §2.2 Forge sub-skill files (5 files, all in `~/.claude/forge/skills/`)

**Note**: publishing the Forge's sub-skills under `~/.claude/forge/skills/<name>/SKILL.md` treats the Forge as a **personal plugin root**, following the Plugin directory structure from `code.claude.com/docs/en/plugins`. This gives the Forge its own plugin.json and keeps its sub-skills namespaced away from `~/.claude/skills/` which is the personal skills directory for skills-Claude-auto-loads.

### §2.2.1 `~/.claude/forge/.claude-plugin/plugin.json`

```json
{
  "name": "forge",
  "description": "Capability Forge — Akash's personal meta-agent plugin. Detects workforce capability gaps, aggregates candidates from primary sources (MCP Registry, anthropics/skills, installed marketplaces), wraps skill-creator + mcp-builder + self-improving-agent to author new primitives, and tracks value across sessions via ACE-style bulleted memory.",
  "version": "0.1.0",
  "author": {
    "name": "Akash (with Research Team v2 investigation)"
  }
}
```

### §2.2.2 `~/.claude/forge/skills/gap/SKILL.md`

```markdown
---
name: forge-gap
description: Inventory Akash's workforce (agents, skills, plugins, installed MCP servers, recent research team SYNTHESIS files) and produce a ranked capability gap list. Diffs against VoltAgent's 10-category specialist taxonomy and wshobson/agents to find missing meta-orchestration, developer-experience, language-specialist, and quality-gate capabilities. Use when forge-lead starts a session without a specific gap in mind, when a retrospective in research-lead's MEMORY.md mentions a recurring capability hole, or when Akash asks "what capability are we missing".
disable-model-invocation: true
allowed-tools: Read Glob Grep Bash(gh api *)
---

# Capability gap detector

## Inventory sources

Read these in parallel:

1. `~/.claude/agents/**/*.md` — flat agents + research/ team specialists. Extract frontmatter names, descriptions, tools.
2. `~/.claude/skills/**/SKILL.md` — personal skills. Extract frontmatter.
3. `~/.claude/plugins/installed_plugins.json` — installed plugins.
4. `~/.claude/plugins/marketplaces/*/` — available-but-not-installed marketplace content.
5. `~/.claude/teams/*/INDEX.md` + `~/.claude/teams/*/*/SYNTHESIS.md` — evidence from other teams' sessions of capability blockers.
6. `~/.claude/agent-memory/*/MEMORY.md` — distilled lessons mentioning missing capabilities.

## Gap detection algorithm

1. **Build a tool-need set**: for each agent file, extract the `allowed-tools` or inferred tools from body prose.
2. **Build a capability-coverage set**: for each skill, extract the description's primary capability (first 250 chars).
3. **Diff against taxonomy**: for each VoltAgent category (01-core, 02-language, 03-infra, 04-qa-sec, 05-data-ai, 06-dev-exp, 07-domains, 08-biz, 09-meta-orch, 10-research), count how many specialists Akash has vs how many VoltAgent has. Categories with <30% coverage are **major gaps**; categories with 30-70% are **medium**; ≥70% are **covered**.
4. **Cross-reference against in-flight sessions**: read `~/.claude/teams/research/INDEX.md`. Any gap whose owning team is actively being designed is **deferred**, not assigned to the Forge.
5. **Rank remaining gaps** by: (a) count of agents that would use the new capability, (b) existence of a reference implementation in anthropics/skills or MCP Registry, (c) explicit mentions in research-lead's MEMORY.md.

## Output format

Write to `~/.claude/forge/gap-reports/<timestamp>.md`:

```markdown
# Gap report — <timestamp>

## Major gaps (>30% coverage deficit vs VoltAgent)
1. **<category>** — <N> specialists missing. Examples: <list>.
   - Reference implementation: <URL or "none found">
   - Recommended action: install / adopt / author / defer-to-research

## Medium gaps (30-70% coverage)
...

## Already covered
...

## Recommended first-batch for this session
1. <gap> — <install|adopt|author|defer>, estimated 1-3 sub-skills
2. ...
```

## Hard rules

- Never propose a gap that's being actively designed by another team (check INDEX.md first).
- Never propose building a capability that's already installed (double-check `installed_plugins.json`).
- Rank by utility to the workforce, not by how interesting the gap is.
```

### §2.2.3 `~/.claude/forge/skills/scout/SKILL.md`

```markdown
---
name: forge-scout
description: Query external sources (MCP Registry, anthropics/skills, installed marketplaces) for candidate implementations of a specified capability. Applies the 6-rule trust heuristic to each candidate and returns ranked recommendations. Use when forge-gap has identified a gap and forge-lead needs to decide whether to install an existing implementation or author a new one. Only use for single-query bounded lookups — for competitive cross-roster analysis, forge-lead must delegate to research-github-miner instead.
disable-model-invocation: true
allowed-tools: Bash(gh api *) Bash(gh search *) Read Glob WebFetch
---

# Forge scout

## Primary data sources

1. **MCP Registry** (STRONG-PRIMARY): `https://registry.modelcontextprotocol.io/v0/servers`
   - Endpoint: `GET /v0/servers?search=<keyword>&limit=100`
   - Cursor pagination: `metadata.nextCursor` opaque string
   - Recent-updates: `?updated_since=<RFC3339>`
   - Public read, no auth.

2. **anthropics/skills** (STRONG-PRIMARY): `gh api repos/anthropics/skills/contents/skills`
   - Returns the 17 official Anthropic skill directories.
   - For each match: `gh api repos/anthropics/skills/contents/skills/<name>/SKILL.md` to pull the frontmatter.

3. **Installed marketplaces** (STRONG-PRIMARY, on disk): `~/.claude/plugins/marketplaces/*/`
   - `huggingface-skills/skills/<name>/SKILL.md`
   - `ai-research-skills/NN-<topic>/<name>/SKILL.md`
   - `claude-code-skills/engineering-team/<name>/SKILL.md`
   - `claude-plugins-official/<plugin>/` via `installed_plugins.json`

4. **Installed plugins** (`~/.claude/plugins/installed_plugins.json`).

## The 6-rule trust heuristic for MCP Registry entries

Before recommending any MCP server, apply these checks (ALL must pass for HIGH trust):

1. **Package registry preference**: `packages[].registryType` must be `npm` | `pypi` | `oci` | `nuget`. Reject smithery-only remote unless the Forge has a smithery API key.
2. **Github repository**: `server.repository.url` must be populated with a `github.com` URL. Reject opaque entries.
3. **Version maturity**: `server.version ≥ 1.0.0` OR multiple iterations in the version history. Reject single one-shot 0.1.x unless no alternative exists.
4. **Description stability**: if multiple versions exist, descriptions must be consistent across versions. Flag description churn.
5. **Transport availability**: `packages[].transport.type` must include `stdio` for local runnability. Accept `streamable-http` only if stdio is also available.
6. **Auth profile**: prefer `authorization: none` for read-only tools. Accept auth-required only if the server is load-bearing.

Servers passing ≥5 rules: HIGH trust. ≥3: MEDIUM. <3: REJECTED.

## Query protocol

Input: capability description (e.g., "Semantic Scholar paper search") from `forge-gap` or `forge-lead`.

Steps:

1. **MCP Registry**: `gh api "https://registry.modelcontextprotocol.io/v0/servers?search=<keyword>&limit=50"`. If nothing found, broaden to synonyms.
2. **anthropics/skills**: check if one of the 17 official skills already covers the capability (use the name + description match).
3. **Installed marketplaces**: Glob for `SKILL.md` matching keywords in their description.
4. **Apply trust heuristic** to each candidate.
5. **Cross-validate high-value candidates** by fetching the candidate's README or SKILL.md (via WebFetch or on-disk Read).

## Output format

Write to `~/.claude/forge/scout-reports/<timestamp>-<capability>.md`:

```markdown
# Scout report — <capability>

## HIGH-trust candidates
1. <name> (<registry>/<identifier> v<version>, <stars>★)
   - URL: <repo_url>
   - Trust rules passed: 1,2,3,4,5,6
   - Install command: <exact command>
   - Why adopt: <1-sentence>

## MEDIUM-trust candidates
...

## REJECTED
...

## Recommendation for forge-lead
<INSTALL|ADOPT|AUTHOR|DEFER> — <rationale>
```

## Hard rules

- Never recommend INSTALL without verifying the trust heuristic passes ≥5 rules.
- Never rank by stars alone — the 6-rule heuristic is binding.
- If no HIGH-trust candidate exists, recommend AUTHOR or DEFER, not a MEDIUM adoption.
- If the capability needs cross-roster competitive analysis, recommend forge-lead delegate to research-github-miner via a research-request drop-file.
```

### §2.2.4 `~/.claude/forge/skills/draft/SKILL.md`

```markdown
---
name: forge-draft
description: Draft a new SKILL.md file to close a specified capability gap, wrapping the official skill-creator plugin's authoring flow. For MCP server gaps, wraps Anthropic's mcp-builder skill instead. Produces a draft at ~/.claude/forge/drafts/<name>/SKILL.md ready for forge-test's evaluation loop. Use when forge-scout has recommended AUTHOR and forge-lead has decided which primitive (skill vs MCP vs plugin) to build.
disable-model-invocation: true
allowed-tools: Read Write Glob Bash(gh *)
---

# Forge drafter

## Decision tree — which primitive to author

```
Question: what primitive closes this gap?
├── Capability is purely instructions (playbook, checklist, reference)
│   → AUTHOR a SKILL.md, no bundled scripts
├── Capability is a reusable script Claude will execute
│   → AUTHOR a SKILL.md with bundled scripts/ directory
├── Capability needs cross-session state (persistent DB, shared cache)
│   → AUTHOR an MCP server via mcp-builder
├── Capability needs non-Claude-Code portability (Cursor, VS Code, Gemini CLI)
│   → AUTHOR an open-standard skill (agentskills.io format) OR MCP server
├── Capability is a coherent bundle of skills + agents + hooks + MCP
│   → AUTHOR a plugin (plugin.json manifest + directory structure)
└── Capability is a behavioral contract for a new specialist role
    → AUTHOR a subagent file (not a skill; a .claude/agents/ entry)
```

## For SKILL.md authoring — wrap skill-creator

`skill-creator` is installed as a plugin. Invoke its SKILL.md via the Skill tool:

```
Skill(skill-creator)
```

This loads the skill-creator's full authoring flow. Pass it the gap description, the intended user phrases, the expected output format, and skill-creator handles the draft → eval → iterate loop.

However, skill-creator is **interactive** — it expects a human to approve test results. The Forge runs non-interactively. Override by:

1. Pre-specifying eval cases in `evals/evals.json` before starting.
2. Accepting the quantitative assertions auto-generated by skill-creator.
3. Running the eval-viewer with `--static <path>` instead of the interactive server (per skill-creator's Cowork instructions).
4. Auto-promoting to `/forge:test` if `pass_rate ≥ 0.8` on the quantitative grade.

## For MCP server authoring — wrap mcp-builder

`mcp-builder` is an Anthropic-official skill in `anthropics/skills`. Install on-demand:

```bash
gh api repos/anthropics/skills/contents/skills/mcp-builder/SKILL.md > /tmp/mcp-builder-skill.md
```

Then load it as context and execute its 4-phase method:
1. **Deep research and planning** — understand the target API.
2. **Implementation** — TypeScript (preferred) or Python (FastMCP).
3. **Review and testing** — MCP Inspector.
4. **Evaluation creation** — 10 realistic test queries.

## Authoring rules (baked in by skill-creator + linguist)

Every authored SKILL.md MUST:
- Be `model: opus` + `effort: max` inherited from session.
- Have `name` ≤ 64 chars, lowercase-hyphen, no "anthropic"/"claude" reserved words.
- Have `description` ≤ 1024 chars (≤ 250 chars primary triggering budget).
- Open with capability first, triggers second.
- Use third-person voice in description.
- Include 3-5 concrete trigger scenarios in "Use when X, Y, or Z" format.
- Use pushy language to counter Claude's undertriggering.
- Stay under 500 lines for the SKILL.md body (use bundled references for overflow).
- Use forward-slash paths only.
- Include at least one "Hard rules" section with MUSTs the skill cannot violate.

## Output

Write to `~/.claude/forge/drafts/<name>/` with:
- `SKILL.md` — the drafted skill.
- `scripts/` (if needed) — bundled executable helpers.
- `references/` (if needed) — overflow documentation.
- `evals/evals.json` — quantitative evaluation cases (≥3, per Anthropic's minimum).

## Hard rules

- Never author a skill without evals. Voyager's self-verification is non-negotiable.
- Never author a skill whose name collides with an existing `~/.claude/skills/**/SKILL.md` or `~/.claude/agents/**/*.md`.
- Never ship a draft that fails its own quick-validate check (skill-creator's `scripts/quick_validate.py`).
```

### §2.2.5 `~/.claude/forge/skills/test/SKILL.md`

```markdown
---
name: forge-test
description: Run the skill-creator eval loop against a forge-draft output to grade whether the drafted skill is promotable. Invokes the grader, aggregator, and analyzer agents from the official skill-creator plugin and returns a pass/fail verdict + suggested improvements. Use when forge-draft has produced a draft at ~/.claude/forge/drafts/<name>/ and the Forge needs a quantitative grade before promotion.
disable-model-invocation: true
allowed-tools: Read Write Bash(python *) Bash(nohup *)
---

# Forge tester

## Wraps skill-creator's eval harness

The official `skill-creator` plugin at `~/.claude/plugins/cache/claude-plugins-official/skill-creator/d53f6ca4cdb0/` ships four Python scripts that implement the eval loop:

- `scripts/quick_validate.py` — syntactic SKILL.md validation.
- `scripts/aggregate_benchmark.py` — produces `benchmark.json` with pass rates, timing, tokens.
- `scripts/generate_report.py` — HTML viewer generation.
- `scripts/run_eval.py` — runs a single eval case.
- `scripts/run_loop.py` — the full trigger-optimization loop.

## Method

1. **Validate syntax**: run `python -m scripts.quick_validate <draft-path>/SKILL.md`. On failure, return the error to `forge-draft` for fixes.
2. **Spawn eval runs**: for each eval case in `<draft-path>/evals/evals.json`, spawn two runs — one with the draft skill, one without (baseline).
   - Use `context: fork` to isolate runs from the main Forge context, per `code.claude.com/docs/en/skills`.
   - Save outputs to `~/.claude/forge/workspaces/<draft-name>/iteration-1/eval-<id>/{with_skill,without_skill}/outputs/`.
3. **Grade**: for each run, spawn the skill-creator's `agents/grader.md` persona to evaluate assertions against outputs. Write `grading.json` per run.
4. **Aggregate**: run `python -m scripts.aggregate_benchmark <workspace>/iteration-1 --skill-name <name>`. Produces `benchmark.json`.
5. **Analyze**: spawn skill-creator's `agents/analyzer.md` to surface patterns in the benchmark.
6. **Verdict**:
   - PASS: pass_rate ≥ 0.8 on all eval cases AND analyzer finds no critical issues.
   - CONDITIONAL: pass_rate 0.6-0.8 OR analyzer flags fixable issues. Return suggestions to `forge-draft` for iteration.
   - FAIL: pass_rate < 0.6 OR critical analyzer findings. Return to `forge-draft` or escalate to `forge-lead` for research-request if stuck.

## Hard rules

- Never skip the eval loop. A skill without evals is unpublishable.
- Never declare PASS without the aggregator + analyzer both clearing.
- Never modify the draft yourself — return feedback to `forge-draft`.
- Minimum 3 eval cases (per Anthropic best-practices doc — "build three scenarios that test these gaps").
- Maximum 3 iterations before escalating to `forge-lead` with a research-request.
```

### §2.2.6 `~/.claude/forge/skills/promote/SKILL.md`

```markdown
---
name: forge-promote
description: Move a tested skill draft from ~/.claude/forge/drafts/ to ~/.claude/skills/<name>/ for personal use or to ~/.claude/forge/outputs/<plugin>/ for plugin packaging. Updates the Forge's MEMORY.md catalog with a bullet entry (authored_at, helpful_count=0, harmful_count=0), notifies the user, and optionally offers to publish via skill-creator's package_skill.py. Use when forge-test has returned PASS on a draft.
disable-model-invocation: true
allowed-tools: Read Write Edit Bash(cp *) Bash(mv *) Bash(python *)
---

# Forge promoter

## Method

1. **Final validation**: re-run `python -m scripts.quick_validate <draft-path>/SKILL.md` one more time.
2. **Destination decision**:
   - **Personal skill**: move to `~/.claude/skills/<name>/`. This makes it available in all Akash's projects per the personal scope rule in `code.claude.com/docs/en/skills`.
   - **Plugin-bundled**: move to `~/.claude/forge/outputs/<plugin>/skills/<name>/`. This lets Akash publish as a plugin later.
   - **Default**: personal scope unless the draft's metadata requests plugin bundling.
3. **Execute move**: `cp -r ~/.claude/forge/drafts/<name>/ <destination>/` (copy, not move — keep the draft for audit).
4. **Update MEMORY.md**: append an ACE-style bullet to `~/.claude/agent-memory/forge-lead/MEMORY.md`:

```markdown
### Authored: <name>
- **authored_at**: <ISO8601>
- **destination**: <path>
- **gap-closed**: <what capability>
- **source-primitives**: <skill-creator | mcp-builder | etc.>
- **eval-pass-rate**: <decimal>
- **helpful_count**: 0
- **harmful_count**: 0
- **last_triggered**: null
- **deprecated_at**: null
```

5. **Notify Akash**: write a final status message:

```
✅ Forge promoted: <name>
Path: <destination>
Gap closed: <description>
Eval pass rate: <N>/<M>

Next: to install as a plugin, run:
  /plugin install <name>@forge
Or to publish:
  python -m scripts.package_skill <destination>
```

6. **Optional packaging**: if Akash confirms, run `python -m scripts.package_skill <destination>` to produce a `.skill` file.

## Counter reconciliation (session-start, not promotion)

At the start of every Forge session, `forge-lead` reads MEMORY.md and runs the reconciliation algorithm:

- For each authored bullet with `authored_at > 7 days ago`:
  - Grep `~/.claude/projects/*/memory/MEMORY.md` for the skill's name in recent sessions.
  - If found as a successful invocation: `helpful_count += 1`.
  - If found as an error/rollback: `harmful_count += 1`.
  - Update `last_triggered` if any mention.
- Bullets with `harmful_count > 2 * helpful_count` are flagged for deprecation review.

This is NOT part of promotion (promotion is author-time); it's a start-of-session hook per `EVIDENCE/skeptic.md` attack #2.

## Hard rules

- Never promote without the final validation pass.
- Never overwrite an existing skill at the destination — if a skill with that name exists, rename with a suffix or report a collision.
- Never delete the draft (keep for audit).
- Never silently update counters — always log the reconciliation delta in LOG.md-equivalent.
```

---

## §3 Skill authoring protocol (primitive decision tree + workflow)

See `forge-draft/SKILL.md` body for the full decision tree. Summary:

1. **Inventory first** (via `forge-gap`): never author without knowing the current state.
2. **Check for existing primitives** (via `forge-scout`): never reimplement what's already on disk or in the registry.
3. **Choose the right primitive type** (decision tree in `forge-draft`): skill (default) > plugin > MCP > subagent.
4. **Wrap canonical authoring harness**: `skill-creator` for skills, `mcp-builder` for MCP servers.
5. **Evaluate against ≥3 cases** (`forge-test`): non-negotiable.
6. **Promote only on PASS** (`forge-promote`): update MEMORY.md with counters.
7. **Reconcile counters at next session start**: close the loop.

---

## §4 First-batch skills to build (revised per `EVIDENCE/skeptic.md` attack #5)

6 items, ranked by priority. Each cites STRONG-PRIMARY sources only.

### Priority 1 (must-do in smoke test): Forge's own sub-skills

These are not "community gaps"; they are the Forge's own prerequisites. Without them, the Forge cannot operate.

1. **`forge-gap`** SKILL.md — implements the gap detector. 
   - **Who benefits**: forge-lead, starting every session.
   - **Source**: synthesized from VoltAgent's 10-category taxonomy + `EVIDENCE/cartographer.md`'s gap table.
   - **Effort**: ~60 lines SKILL.md + 0 scripts (pure Glob/Grep/Read orchestration).
   - **Priority**: 10/10 — blocking on Forge operation.

2. **`forge-scout`** SKILL.md — implements the MCP Registry wrapper + 6-rule trust heuristic.
   - **Who benefits**: forge-lead + transitively anyone who asks "does an MCP exist for X".
   - **Source**: MCP Registry API docs (`registry.modelcontextprotocol.io/docs`, `nordicapis.com/...`), `gh api` verified.
   - **Effort**: ~80 lines SKILL.md + ~30 lines reference heuristic markdown + 0 scripts (gh api one-liners).
   - **Priority**: 10/10 — blocking.

3. **`forge-draft`** SKILL.md — wraps skill-creator's authoring.
   - **Who benefits**: forge-lead when authoring any new skill.
   - **Source**: `~/.claude/plugins/cache/claude-plugins-official/skill-creator/.../SKILL.md` (already on disk) + Anthropic's `mcp-builder` via `anthropics/skills`.
   - **Effort**: ~70 lines SKILL.md + 0 scripts (reuses skill-creator's scripts).
   - **Priority**: 10/10 — blocking.

4. **`forge-test`** SKILL.md — wraps skill-creator's eval loop.
   - **Who benefits**: forge-lead's quality gate.
   - **Source**: `~/.claude/plugins/cache/claude-plugins-official/skill-creator/d53f6ca4cdb0/skills/skill-creator/scripts/{quick_validate,aggregate_benchmark,run_eval}.py`.
   - **Effort**: ~60 lines SKILL.md + 0 scripts (reuses).
   - **Priority**: 10/10 — blocking.

5. **`forge-promote`** SKILL.md — promotion + MEMORY.md update.
   - **Who benefits**: forge-lead's commit step.
   - **Source**: ACE paper (arxiv 2510.04618) bullet schema + research-lead's existing MEMORY.md pattern.
   - **Effort**: ~70 lines SKILL.md + 0 scripts.
   - **Priority**: 10/10 — blocking.

### Priority 2 (first external-gap closure)

6. **Install `arxiv-mcp-server` from MCP Registry** — no new authoring, just an install.
   - **Who benefits**: research-historian + research-librarian. Currently they use WebFetch against arxiv.org HTML, which is slow and fragile. The MCP gives batched semantic access.
   - **Source**: `io.github.blazickjp/arxiv-mcp-server v0.4.9` — verified HIGH-trust by `EVIDENCE/adversary.md`.
   - **Install command**: 
     ```bash
     # add to ~/.claude/mcp.json (user-scope MCP config)
     uvx arxiv-mcp-server
     ```
   - **Effort**: 1 config edit.
   - **Priority**: 9/10 — high value, zero authoring work.

### Priority 3 (first authored-skill external closure)

7. **Author `hn-search` skill** for Hacker News search via Algolia API.
   - **Who benefits**: research-web-miner, research-historian. HN Algolia returns JSON via simple HTTP; a skill that encodes the query patterns is cheaper than an MCP server per Simon Willison's "skills > MCP" argument.
   - **Source**: HN Algolia API docs (https://hn.algolia.com/api), linguist's pattern library.
   - **Form factor**: SKILL.md with one bundled `scripts/hn_search.py` helper (or shell one-liner).
   - **Effort**: ~80 lines SKILL.md + ~30 lines script + 3 eval cases.
   - **Priority**: 7/10 — useful for research team's sentiment sweeps.

### Priority 4 (deferred — needs research delegation)

8. **Semantic Scholar integration** — Akash's research team uses Semantic Scholar for citation graphs and paper resolution, but there's no MCP. A full Semantic Scholar MCP is non-trivial (OAuth for rate limits, multi-endpoint API). Defer to research-lead for a scoped investigation ("is there a Semantic Scholar MCP in the wild that handles rate-limiting honestly?") and author only after the research returns.
   - **Priority**: defer.

### Summary

**In the smoke test session**: items 1-5 (Forge's own sub-skills) + item 6 (arxiv MCP install). That's the minimum viable Forge.

**Second session**: item 7 (hn-search skill) as the first **external-gap-closing** smoke test for the end-to-end `/forge:gap` → `/forge:scout` → `/forge:draft` → `/forge:test` → `/forge:promote` flow.

**Third+ session**: item 8 and beyond, per gap detector output at that time.

---

## §5 Internet-aggregation playbook

### Primary sources (cadence: on-demand, per session)

1. **MCP Registry** — `gh api "https://registry.modelcontextprotocol.io/v0/servers?search=<keyword>&limit=100"`
   - Call freq: once per capability search.
   - Pagination: follow `metadata.nextCursor` if >100 results.
   - Filter: `?updated_since=<7-days-ago-RFC3339>` for recency.
   - Trust: STRONG-PRIMARY, public read.

2. **anthropics/skills** — `gh api repos/anthropics/skills/contents/skills`
   - Call freq: cached locally; refresh weekly.
   - Returns 17 official skill directories.
   - Trust: STRONG-PRIMARY.

3. **Installed marketplaces on disk** — Glob over `~/.claude/plugins/marketplaces/*/`
   - Call freq: every gap search.
   - Trust: STRONG-PRIMARY (whatever Akash has installed).

### Secondary sources (cadence: weekly, for taxonomy refresh)

4. **VoltAgent/awesome-claude-code-subagents** — `gh api repos/VoltAgent/awesome-claude-code-subagents/contents/categories`
   - Use: taxonomy template for the gap detector's 10-category diff.
   - Trust: MIXED-FAVORABLE per adversary.md.

5. **wshobson/agents** — `gh api repos/wshobson/agents/contents`
   - Use: scale reference (182 agents, 77 plugins) — informs when to upgrade H1→H2.
   - Trust: MIXED-FAVORABLE.

### Tertiary sources (cadence: on-demand, flagged as UNVETTED)

6. Community "awesome-claude-skills" repos (ComposioHQ, travisvn, BehiSecc). Use for cross-validation of taxonomy; never cite as primary authority. Flagged as MIXED per adversary.md.

### Trust model (the 6-rule MCP heuristic, applied to all external candidates)

Per `EVIDENCE/adversary.md` and forge-scout's SKILL.md body. Repeated here for reference:

1. Package registry preference (`npm`/`pypi`/`oci`/`nuget` > smithery-only).
2. Github repo populated.
3. Version ≥ 1.0 OR multiple iterations.
4. Description stability across versions.
5. Stdio transport available.
6. Auth profile (`none` preferred for read-only).

Rules 1-6 apply to MCP Registry entries. For skills from community rosters, use an analogous heuristic: (a) star count + age ratio, (b) last commit freshness, (c) author reputation, (d) cross-mentions from primary sources, (e) license clarity, (f) presence of eval cases.

### SEO-farm defense

- Never cite an "awesome-*" repo as primary authority. Always chase the link back to the authoritative source (anthropics/skills, a peer-reviewed paper, an on-disk marketplace).
- When three repos with near-identical names compete (the ComposioHQ/travisvn/BehiSecc pattern), use them as **cross-validators** — if all three mention a resource, it's real; if only one does, treat it as MIXED.
- When star counts are suspicious (53k for a "curated list"), look at the ratio of stars to contributors. A healthy OSS project has hundreds-to-thousands of contributors; a SEO farm has 1-3. `gh api` can check.

---

## §6 Collaboration contract with Research Team (user-mediated handoff)

### When the Forge delegates to research-lead

Trigger conditions:
- Scout returns MIXED or REPORTED-NOT-VERIFIED for a load-bearing source.
- Gap requires multi-round investigation the Forge cannot do (>3 specialists' worth of lenses).
- The question is ambiguous in a way that crosses source tiers (e.g., "is the Voyager skill library retrieval mechanism really embedding-based, or is it name-based?").

### Handoff mechanism: file drop

The Forge writes to `~/.claude/forge/research-requests/<slug>.md`:

```markdown
# Research request from forge-lead
## Date
<YYYY-MM-DD>
## Question
<1-sentence clear question>
## Context
<what I've already found, with tier labels>
## Blocking question
<what I need the research team to disambiguate>
## How I'll use the answer
<specific Forge action that's blocked>
## Forge session slug
<the session that emitted this>
```

Then the Forge **stops its session**. It writes a final status message to Akash:

```
⏸ Forge session paused — research handoff needed.
Request written to ~/.claude/forge/research-requests/<slug>.md
Invoke research-lead with this file's content as the prompt, then re-invoke forge-lead in a new session.
```

### Akash's manual step (user-mediated)

Akash (or the main Claude session) reads the drop-file and invokes research-lead:

```
claude --agent research-lead
> "Read ~/.claude/forge/research-requests/<slug>.md and produce a SYNTHESIS.md answering the question."
```

Research-lead runs its full protocol and produces `~/.claude/teams/research/<new-slug>/SYNTHESIS.md`.

### Forge re-invocation

Akash re-invokes forge-lead with the research result:

```
claude --agent forge-lead
> "Read ~/.claude/teams/research/<new-slug>/SYNTHESIS.md and continue the previous Forge session."
```

Forge-lead reads the research SYNTHESIS, updates its own MEMORY.md with the decisive finding, and resumes authoring.

### Why user-mediated, not automated

Per `EVIDENCE/skeptic.md` attack #6: automated polling requires hook infrastructure (PreSessionStart or similar) that Akash hasn't enabled. User-mediated handoff is simpler, testable, and doesn't depend on speculative infra.

Upgrade path: once Akash enables session-start hooks, the hook can auto-check `~/.claude/forge/research-requests/` for unanswered requests and surface them. For now, manual.

---

## §7 Self-improvement loop (ACE-style bulleted MEMORY.md)

### File: `~/.claude/agent-memory/forge-lead/MEMORY.md`

Structure:

```markdown
# forge-lead — persistent agent memory

This file is the Forge's evolving playbook. Append-only at the section level,
bullet counters update in-place. Read first 200 lines at session start.

## Process lessons (from retrospector)

<ACE-style bullet entries with helpful_count/harmful_count>

## Authored skills catalog

### <skill-name>
- authored_at: <ISO8601>
- destination: <path>
- gap-closed: <what capability>
- source-primitives: <skill-creator | mcp-builder | etc.>
- eval-pass-rate: <decimal>
- helpful_count: <N>
- harmful_count: <N>
- last_triggered: <ISO8601 | null>
- deprecated_at: <ISO8601 | null>

## Failed gap investigations

### <slug>
- attempted_at: <ISO8601>
- gap: <what capability was sought>
- source_checked: <URL list>
- why_failed: <SEO | not_found | research_required | ...>
- next_action: <defer | escalate | retry_in_N_weeks>
```

### Start-of-session reconciliation

Per forge-promote's "counter reconciliation" section:

1. For each bullet in "Authored skills catalog" with `authored_at > 7 days ago`:
   - Grep `~/.claude/projects/*/memory/MEMORY.md` for the skill name.
   - If found with context "used <name> to X": `helpful_count += 1`, update `last_triggered`.
   - If found with context "rolled back <name>" or "disabled <name>": `harmful_count += 1`.
2. Bullets with `harmful_count > 2 * helpful_count`: mark `deprecated_at`. Next session, remove from `~/.claude/skills/`.
3. Bullets with `last_triggered` older than 90 days AND `helpful_count == 0`: mark `deprecated_at`.

### Reference: ACE paper (arxiv 2510.04618)

Per `EVIDENCE/historian.md`: ACE's bullet structure has metadata (counters) + content. The Forge follows the same pattern. ACE's ablation shows removing the counters/reflection loop costs 3.9 points on agent benchmarks — so the reconciliation step is load-bearing, not optional.

**REPORTED-NOT-VERIFIED caveat**: the exact benchmark numbers (+10.6%, +8.6%) are from a single paper without independent reproduction yet. The directional claim (bullet-with-counters beats rewrite-in-place) is the load-bearing insight.

---

## §8 Workspace layout

### `~/.claude/forge/` — Forge plugin root + working state

```
~/.claude/forge/
├── .claude-plugin/
│   └── plugin.json                     # plugin manifest
├── skills/
│   ├── gap/SKILL.md                    # forge-gap sub-skill
│   ├── scout/SKILL.md                  # forge-scout sub-skill
│   ├── draft/SKILL.md                  # forge-draft sub-skill
│   ├── test/SKILL.md                   # forge-test sub-skill
│   └── promote/SKILL.md                # forge-promote sub-skill
├── drafts/                              # in-progress drafts
│   └── <skill-name>/
│       ├── SKILL.md
│       ├── scripts/
│       ├── references/
│       └── evals/evals.json
├── outputs/                             # plugin-bundled outputs (for publishing)
│   └── <plugin-name>/
├── workspaces/                          # eval workspaces (one per draft)
│   └── <draft-name>/
│       └── iteration-1/
│           ├── eval-0/with_skill/outputs/
│           ├── eval-0/without_skill/outputs/
│           └── benchmark.json
├── scout-reports/                       # forge-scout output
│   └── <timestamp>-<capability>.md
├── gap-reports/                         # forge-gap output
│   └── <timestamp>.md
├── research-requests/                   # drop-files for research-lead
│   └── <slug>.md
└── registry-cache/                      # MCP Registry query cache
    └── <hash>.json
```

### `~/.claude/agent-memory/forge-lead/` — memory

```
~/.claude/agent-memory/forge-lead/
└── MEMORY.md
```

### `~/.claude/agents/forge-lead.md` — persona file

Single file. Not in a subdirectory (symmetry with `~/.claude/agents/research/research-lead.md` in research's case, but note research has a team so it uses a subdir; the Forge does not).

### DO NOT USE: `~/.claude/teams/forge/`

This path is **reserved** for the future H2 upgrade. Do not create it now. The experimental Agent Teams runtime (`CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1`) uses `~/.claude/teams/<team-name>/config.json` as its runtime state path; creating it prematurely would collide with that runtime if it's enabled.

---

## §9 CLAUDE.md delta

### Old text (from `~/.claude/CLAUDE.md`, under "Team hierarchy" → "Currently available teams")

```markdown
### Currently available teams

- **Research Team** — `research-lead` + 10 specialists. Use proactively
  for any question that would otherwise consume more than ~3 rounds of
  solo investigation. See `~/.claude/teams/research/PROTOCOL.md`.

### Teams under construction (build in this order)

1. Research ← **done, use this to inform the rest**
2. Planning / Architecture
3. Implementation
4. Review / Verification
5. Testing / QA
6. DevOps / Release
7. Design / Frontend
```

### New text

```markdown
### Currently available teams

- **Research Team** — `research-lead` + 17 specialists. Use proactively
  for any question that would otherwise consume more than ~3 rounds of
  solo investigation. See `~/.claude/teams/research/PROTOCOL.md`.

### Meta-agents (downstream of teams, upstream of skills)

- **Capability Forge** — `forge-lead` (single specialist, H1 architecture
  with documented upgrade path to H2 mini-team). Meta-agent that inventories
  the workforce, detects capability gaps, aggregates candidates from the
  MCP Registry + anthropics/skills + installed marketplaces, wraps
  skill-creator / mcp-builder / self-improving-agent to author new
  primitives, and tracks authored-skill value across sessions via ACE-style
  bulleted MEMORY.md at `~/.claude/agent-memory/forge-lead/MEMORY.md`.
  Plugin root at `~/.claude/forge/`. Five sub-skills: `/forge:gap`,
  `/forge:scout`, `/forge:draft`, `/forge:test`, `/forge:promote`. Use
  proactively when the user says "what capability are we missing",
  "build a skill for X", "check MCP Registry for Y", or when a retrospective
  surfaces a recurring capability hole.

### Teams under construction (build in this order)

1. Research ← **done, use this to inform the rest**
2. Capability Forge ← **done (this session), H1 architecture**
3. Planning / Architecture
4. Implementation
5. Review / Verification
6. Testing / QA
7. DevOps / Release
8. Design / Frontend
```

### Additional delta — new section under "Dispatch rules"

```markdown
## Dispatch rules (add one line)

- Capability gap in the workforce → go through `forge-lead`, not
  through the research team or a direct skill-creator call. The Forge
  wraps skill-creator and delegates to research-lead when needed.
```

---

## §10 Smoke test

### Concrete first task

**Smoke-test the Forge's five sub-skills by running `/forge:gap` → `/forge:scout` → `/forge:draft` → `/forge:test` → `/forge:promote` end-to-end on the simplest external capability gap: authoring an `hn-search` skill.**

This proves:
1. The `forge-lead` persona loads correctly (✓ if Claude responds with the Forge's opening method).
2. `/forge:gap` produces a gap report (✓ if `~/.claude/forge/gap-reports/<timestamp>.md` exists and mentions HN as a capability gap).
3. `/forge:scout` queries the MCP Registry and finds zero HN MCPs (✓ if `~/.claude/forge/scout-reports/...hn.md` documents the miss and recommends AUTHOR).
4. `/forge:draft` invokes skill-creator and produces `~/.claude/forge/drafts/hn-search/SKILL.md` (✓ if file exists with valid YAML frontmatter per `quick_validate.py`).
5. `/forge:test` runs the eval loop and returns PASS (✓ if `~/.claude/forge/workspaces/hn-search/iteration-1/benchmark.json` shows `pass_rate ≥ 0.8`).
6. `/forge:promote` moves the draft to `~/.claude/skills/hn-search/SKILL.md` and updates `~/.claude/agent-memory/forge-lead/MEMORY.md` with the bullet entry (✓ if both changes are visible).
7. **A fresh Claude Code session**, when given a prompt like "search HN for recent vLLM discussions", should auto-invoke the newly-authored `hn-search` skill (✓ if Claude uses the skill within 2-3 messages without being explicitly told to).

### Launch prompt (verbatim for Akash)

```
claude --agent forge-lead
> I just wrote the Forge. Smoke-test it by running through the full /forge:gap → /forge:scout → /forge:draft → /forge:test → /forge:promote sequence to produce an `hn-search` skill. The gap is: our research team's historian and web-miner use HN Algolia via WebFetch, but there's no encapsulated skill or MCP for it, and no HN MCP exists in the MCP Registry per https://registry.modelcontextprotocol.io/v0/servers?search=hacker+news. Author a SKILL.md that wraps HN Algolia's REST API (https://hn.algolia.com/api) with 3 eval cases: (1) search for recent vLLM discussions, (2) get a thread's comment tree by id, (3) filter for stories with >100 points from last week. Promote on pass. At the end, report: the authored SKILL.md path, the eval pass rate, the MEMORY.md bullet you appended, and any research-requests you had to drop.
```

### Expected smoke test output

```
Forge report — hn-search skill authoring

✓ /forge:gap — gap report at ~/.claude/forge/gap-reports/<ts>.md, HN search confirmed as external gap (not in registry, no skill on disk)
✓ /forge:scout — ~/.claude/forge/scout-reports/<ts>-hn.md, 0 MCP candidates, recommend AUTHOR as skill (skills > MCP per Simon Willison)
✓ /forge:draft — SKILL.md written to ~/.claude/forge/drafts/hn-search/SKILL.md (87 lines, 3 evals)
✓ /forge:test — pass_rate 1.00 on all 3 evals via skill-creator eval loop, analyzer found no issues
✓ /forge:promote — moved to ~/.claude/skills/hn-search/SKILL.md, MEMORY.md bullet added with authored_at=<ts>, helpful_count=0

Research requests dropped: 0.
Next steps:
1. In a fresh session, ask Claude "search HN for vLLM" and confirm auto-trigger.
2. Review the MEMORY.md entry after 7 days to see if the counter reconciliation caught any real-session invocations.
3. If this worked, re-invoke forge-lead with /forge:gap to surface the next gap.
```

### Failure modes to watch for (maps to skeptic attack #1)

- **`/forge:draft` hangs waiting for human input**: skill-creator's SKILL.md is interactive. If this happens, the Forge's `forge-draft` sub-skill must bypass interactive prompts (use `--static` for the viewer, accept auto-assertions). If it can't bypass, that's a **binding blocker** on the "wrap, don't rewrite" claim and the architecture needs revision.
- **`/forge:test` skips evals**: if skill-creator's grader refuses to run without the `claude -p` binary, fall back to manual grading inline. Flag for a research-request.
- **MCP Registry returns nothing for "hacker news"**: confirmed true at session time — this is the expected result, NOT a failure.

---

## Key evidence citations

- `EVIDENCE/planner.md` — dispatch plan, 8 specialists, Anthropic scaling rule + MEMORY.md lessons applied.
- `EVIDENCE/librarian.md` — canonical SKILL.md + plugin + sub-agent + MCP specs from code.claude.com and platform.claude.com.
- `EVIDENCE/historian.md` — Voyager (arxiv 2305.16291), ACE (arxiv 2510.04618), Anthropic skills launch blog, Toolformer prior art, the Voyager+ACE+Toolformer composite.
- `EVIDENCE/github-miner.md` — community rosters (VoltAgent 130 specialists, wshobson 33.4k stars), MCP Registry sweep with trust heuristic, anthropics/skills 17 official skills.
- `EVIDENCE/web-miner.md` — **Agent Teams 2026 primitive discovery** (experimental, off-by-default, distinct from subagents), **agentskills.io open standard**, 30+ cross-vendor skill-compatible tools.
- `EVIDENCE/cartographer.md` — Akash's substrate inventory: 24 flat agents + 18 research specialists + 91 personal skill directories (only 3 with local SKILL.md) + 17 installed plugins + 4 marketplaces. Major gaps: automatic curriculum, MCP Registry scout, value tracking, tool-need-vs-skill-coverage diff.
- `EVIDENCE/linguist.md` — SKILL.md triggering patterns, 8 authoring rules for the Forge's own drafts.
- `EVIDENCE/adversary.md` — source tier assignments, 6-rule MCP trust heuristic, SEO-farm pattern analysis, MIXED-tier treatment of competing "awesome-*" lists.
- `EVIDENCE/synthesist.md` — claim matrix across 8 specialists, 4 emergent patterns, H1/H2 tension identified as REFRAME candidate.
- `EVIDENCE/moderator.md` — 3-round debate on H1 vs H2, REFRAME verdict ("H1 now with upgrade path to H2 later"), primary-source-grounded arguments for both sides.
- `EVIDENCE/skeptic.md` — 7 attacks on the synthesis, 5 led to refinements (reduce 6 sub-skills to 5, honest upgrade-is-rewrite framing, scout bounded ownership, user-mediated handoff, narrow triggering).
- `EVIDENCE/evaluator.md` — 5-dimension rubric PASS with conditions, green light to ship SYNTHESIS.md.

## Counter-evidence

- **"Wrap, don't rewrite"** rests on the assumption that skill-creator's eval loop can be run non-interactively. This has NOT been tested end-to-end (skeptic attack #1). Confidence: MEDIUM-HIGH pending §10 smoke test.
- **ACE exact benchmark numbers** (+10.6%, +8.6%) are from a single paper without independent reproduction. The directional claim is load-bearing but the exact numbers are REPORTED-NOT-VERIFIED (adversary).
- **Upgrade path H1→H2 is described as graceful** in synthesist.md but skeptic attack #3 corrected this: it's an honest rewrite, not a local refactor. The synthesis corrects this to "H1 is a prototype, H2 is a future rewrite."

## Open questions (for follow-up or retrospector)

1. Does skill-creator's eval loop actually work non-interactively? **Resolved by §10 smoke test**.
2. Is `self-improving-agent`'s `/si:extract` callable programmatically, or does it require user confirmation at each step? **Resolved by first external-gap smoke test** (hn-search).
3. What's the right cadence for the start-of-session counter reconciliation? **Probably every session; measured after first 3 sessions' data**.
4. Should the Forge publish its own plugin to a marketplace? **Not yet — too early. Revisit when Forge has ≥5 authored skills with positive helpful_count.**
5. Does the `agent-teams` experimental runtime change Forge's architecture? **Not today (H1), yes eventually (H2 upgrade when workforce scales).**

## Confidence summary

| Claim | Confidence |
|---|---|
| H1 is the right architecture for first session | **HIGH** |
| 5-sub-skill decomposition (gap/scout/draft/test/promote) | **HIGH** |
| "Wrap, don't rewrite" reuse pattern | **MEDIUM-HIGH** (pending smoke test) |
| MCP Registry is a reliable public endpoint | **HIGH** |
| 6-rule trust heuristic for MCP Registry | **HIGH** |
| User-mediated research-request handoff | **HIGH** |
| ACE-style bulleted MEMORY.md with counters | **HIGH** (directional); **MEDIUM** on exact schema |
| First-batch priorities (items 1-7) | **HIGH** |
| Upgrade path H1→H2 is a rewrite not a refactor | **HIGH** |
| Workspace layout at `~/.claude/forge/` (not `teams/forge/`) | **HIGH** |

Overall: **HIGH** confidence on the deliverable, pending smoke-test validation of the reuse primitives.
