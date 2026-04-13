# Linguist — SKILL.md description triggering patterns + naming conventions

## Method

Sampled 15+ SKILL.mds across Akash's on-disk substrate: 3 from `~/.claude/skills/` (local), 3 from `huggingface-skills/`, 5 from `claude-code-skills/engineering-team/`, 3 from `ai-research-skills/` + the official `skill-creator` reference. Extracted: (a) description opening phrase, (b) trigger phrase structure, (c) length, (d) pushy-ness level, (e) naming convention.

## Description patterns — what Claude responds to

### Pattern 1: "Use when X" imperative (most common, Anthropic best-practice compliant)

Examples:
- `omc-reference`: "Auto-loads when delegating to agents, using OMC tools, orchestrating teams, making commits, or invoking skills."
- `vllm` (serving-llms-vllm): "...Use when deploying production LLM APIs, optimizing inference latency/throughput, or serving models with limited GPU memory."
- `autogpt-agents`: "...Use when creating visual workflow agents, deploying persistent autonomous agents, or building complex multi-step AI automation systems."
- `adversarial-reviewer`: "...Use when you want a genuinely critical review of recent changes, before merging a PR, or when you suspect Claude is being too agreeable about code quality."
- `skill-creator`: "...Use when users want to create a skill from scratch, update or optimize an existing skill, run evals to test a skill, benchmark skill performance..."

**Shared shape**: `[what the skill does, 1 sentence]. Use when [context A], [context B], or [context C].`

### Pattern 2: Third-person gerund + capability (Anthropic's recommended form)

- `hugging-face-tool-builder`: "Use this skill when the user wants to build tool/scripts or achieve a task where using data from the Hugging Face API would help." (imperative, second-person — violates Anthropic's third-person rule; a mild anti-pattern per best-practices doc)
- `serving-llms-vllm`: "Serves LLMs with high throughput using vLLM's PagedAttention and continuous batching." (gerund, third-person — ✓)
- `code-reviewer`: "Code review automation for TypeScript, JavaScript, Python, Go, Swift, Kotlin. Analyzes PRs for complexity..." (noun phrase + third-person — ✓)

### Pattern 3: Problem-solution framing

- `self-improving-agent`: "Curate Claude Code's auto-memory into durable project knowledge. Analyze MEMORY.md for patterns, promote proven learnings..."

Opens with the action (curate), follows with the decomposition (analyze, promote, extract), ends with "Use when: (1) reviewing, (2) graduating, (3) turning debugging into a skill..."

### Pushy-ness calibration

The official skill-creator documentation explicitly says:

> "Claude has a tendency to 'undertrigger' skills — to not use them when they'd be useful. To combat this, please make the skill descriptions a little bit 'pushy'."

Example from the docs:
- **Undertriggering**: "How to build a simple fast dashboard to display internal Anthropic data."
- **Pushy fix**: "How to build a simple fast dashboard to display internal Anthropic data. Make sure to use this skill whenever the user mentions dashboards, data visualization, internal metrics, or wants to display any kind of company data, even if they don't explicitly ask for a 'dashboard.'"

**Observed pushy examples in Akash's substrate**:
- `omc-reference` uses "Auto-loads when..." — ✓ pushy
- `adversarial-reviewer` enumerates 3 triggers + explicit "when you suspect Claude is being too agreeable" — ✓ pushy
- `autogpt-agents` lists 4 scenario triggers — ✓ pushy
- `hugging-face-tool-builder` uses "especially useful when chaining or combining API calls" — ✓ pushy
- `self-improving-agent` enumerates 4 numbered triggers — ✓ pushy

**Missing pushy** (anti-pattern examples):
- Generic names like `tools`, `helper`, `utils` (found in some older marketplace skills sampled, not in this set).

## Length distribution

- Shortest sampled: `omc-reference` — 23 words. Borderline.
- Longest sampled: `skill-creator` — 56 words with multiple "or" clauses. Above the 250-char truncation limit means everything after ~250 chars may be stripped in the skill listing per Anthropic's docs. **Action**: the Forge should author descriptions under 250 chars for the primary trigger list and let the body carry anything else.
- Sweet spot from the sample: **30-45 words, 2 sentences, 3-5 triggers**.

## Front-loading rule

Per Anthropic docs: "Front-load the key use case: descriptions longer than 250 characters are truncated in the skill listing to reduce context usage."

**Observed compliance**:
- `vllm`: ✓ opens with "Serves LLMs with high throughput" — primary capability first.
- `autogpt-agents`: ✓ opens with "Autonomous AI agent platform" — category first.
- `hugging-face-tool-builder`: × opens with "Use this skill when the user wants to build tool/scripts..." — triggers before capability, which wastes the first 250 chars on context.

**Lesson for the Forge**: author descriptions with capability first, triggers second. The first 250 chars are the primary signal; put them to work.

## Naming convention observations

Per Anthropic docs, naming should be:
- Lowercase, numbers, hyphens only.
- Max 64 chars.
- No reserved words `anthropic`, `claude`.
- Preferred form: **gerund** (`processing-pdfs`, `analyzing-spreadsheets`).
- Acceptable: noun phrases (`pdf-processing`), action-oriented (`process-pdfs`).

**Observed**:
- `skill-creator` — action form. ✓
- `omc-reference` — noun phrase. ✓
- `adversarial-reviewer` — noun phrase. ✓
- `self-improving-agent` — gerund-adjectival + noun. ✓
- `serving-llms-vllm` — gerund + noun + tech. ✓ (the internal name differs from the directory name `vllm` — the directory is informal, the `name:` field is canonical)
- `autogpt-agents` — noun phrase. ✓
- `hugging-face-tool-builder` — noun phrase. ✓

**Anti-patterns seen nowhere in sample** but flagged in docs to avoid: `helper`, `utils`, `tools`, `documents`, `data`, `files`.

## The `self-improving-agent/skills/*` sub-skill naming pattern

The `self-improving-agent` plugin uses **single-verb sub-skill names**:
- `remember`
- `promote`
- `status`
- `extract`
- `review`

Each with a `command: /si:<name>` field in frontmatter, mapping to `/si:remember` etc. This is a **namespaced slash-command pattern** that lets one plugin expose multiple commands with a shared prefix.

**Implication for the Forge**: if the Forge is a single plugin with sub-skills (the H1-plus-subskills architecture I'm leaning toward), its sub-skills should use the same pattern: `forge-scout`, `forge-gap`, `forge-draft`, `forge-test`, `forge-promote` OR more concise `/forge:scout`, `/forge:gap`, etc. via the `command:` field.

## Anti-patterns observed in community skills (from earlier Glob sweep — to be confirmed in round 2)

- Multiple competing "awesome-claude-skills" repos with near-identical naming (ComposioHQ, travisvn, BehiSecc) — flag for adversary.
- Some marketplace skills use `command:` frontmatter as a slash command shortcut (not in the official spec table but appears in alirezarezvani marketplace). This may be a Claude Code extension — verify in round 2.

## Dispatch to synthesist

**Authoring rules the Forge must encode** (for its own SKILL.md output):

1. **First 250 chars**: capability first, triggers second. Gerund name if possible.
2. **Triggers**: 3-5 concrete scenarios, "Use when X, Y, or Z" format.
3. **Pushy tone**: include an explicit "even if the user doesn't explicitly ask for X" clause when the skill is prone to undertrigger.
4. **Third-person**: never "I" or "you" in description — always third person.
5. **Reserved words**: no `anthropic` or `claude` in `name`. `claude-api` is an apparent exception but uses `claude-api` not just `claude`; the rule is no bare reserved word, prefixing/compounding is fine.
6. **Length**: 30-45 words, 2 sentences, under 250 char primary budget.
7. **`user-invocable: false`**: use for reference-only skills the Forge ships (like a catalog of agents) that should be auto-loaded but not slash-invoked.
8. **`disable-model-invocation: true`**: use for explicit commands that must be manually triggered (e.g., the Forge's actual build command `/forge:build`).

These 8 rules should be baked into the Forge's SKILL.md template for all authored skills.
