# Cartographer — internal agent/skill/plugin substrate inventory + gap table

## Substrate totals (2026-04-12)

- `~/.claude/agents/` flat agents: **24** (analyst, architect, architect-planner, code-reviewer, code-simplifier, critic, debugger, designer, document-specialist, executor, explore, git-manager, git-master, planner, qa-tester, researcher, scientist, security-reviewer, test-engineer, test-writer, tracer, verifier, writer, + 1 `research.v1.bak/` backup dir).
- `~/.claude/agents/research/` team specialists: **18** (research-lead + 17 per PROTOCOL.md v2).
- `~/.claude/skills/` personal skills: **91 directories**; only **3 have a local SKILL.md** (0-autoresearch-skill, vllm, omc-reference). The other 88 are **names-only shells** — likely symlinked to or copies of skills from the `ai-research-skills` marketplace at `~/.claude/plugins/marketplaces/ai-research-skills/**/<name>/SKILL.md`.
- `~/.claude/plugins/installed_plugins.json`: **17 plugins installed** from `claude-plugins-official` marketplace: claude-code-setup, frontend-design, code-simplifier, ralph-loop, claude-md-management, **skill-creator**, code-review, feature-dev, pr-review-toolkit, hookify, commit-commands, playground, context7, security-guidance, pyright-lsp, rust-analyzer-lsp, typescript-lsp.
- `~/.claude/plugins/marketplaces/`: **4 marketplaces registered** — claude-plugins-official (Anthropic official), huggingface-skills, ai-research-skills, claude-code-skills (alirezarezvani).
- `~/.claude/teams/`: `research/` (only live team), `forge/` not present, `engineering/` not present.
- `~/.claude/agent-memory/`: `research-lead/MEMORY.md` live; no `forge-lead/MEMORY.md` yet.

## Existing flat-agents taxonomy

| Agent | Primary capability | Maps to VoltAgent category | Overlap with Research Team? |
|---|---|---|---|
| analyst | requirements clarity, hidden constraints | 01-core / 08-business-product | no |
| architect | system design, boundaries, long-horizon tradeoffs | 01-core | partial (research-cartographer covers structure lens) |
| architect-planner | planning + architecture combo | 01-core + 09-meta-orchestration | no |
| code-reviewer | code review | 04-quality-security | no |
| code-simplifier | simplification / refactoring | 06-developer-experience | no |
| critic | critique (scope unclear — possibly duplicate of research-skeptic) | — | **yes, research-skeptic owns this at the team level** |
| debugger | root-cause analysis | 04-quality-security | no |
| designer | UX and interaction design | 01-core | no |
| document-specialist | SDK/API/framework doc lookup | 06-dev-experience | partial (research-librarian covers this in research context) |
| executor | implementation, refactoring | 01-core | no |
| explore | fast codebase search/mapping (haiku model per omc-reference — **model downgrade, violates doctrine**) | 10-research | **yes, research-cartographer covers this** — AND explore is marked haiku, needs auditing |
| git-manager | git hygiene | 06-dev-experience | no |
| git-master | git mastery | 06-dev-experience | **yes, duplicate of git-manager** |
| planner | sequencing and execution plans | 09-meta-orchestration | partial (research-planner is team-scoped) |
| qa-tester | runtime/manual validation | 04-quality-security | no |
| researcher | (scope unclear — predates Research Team v2) | 10-research | **yes, duplicate of research-lead entry point** — needs deprecation |
| scientist | data analysis, statistical reasoning | 05-data-ai | no |
| security-reviewer | trust boundaries, vulnerabilities | 03-infra / 04-qa-sec | partial |
| test-engineer | testing strategy, regression | 04-qa-sec | no |
| test-writer | writing tests | 04-qa-sec | duplicate of test-engineer? |
| tracer | trace gathering, evidence capture | — | **yes, research-tracer duplicates at team level** |
| verifier | completion evidence, validation | 04-qa-sec | partial (research-evaluator at team level) |
| writer | docs, concise content | 08-business-product | no |

**Overlap flags from above**: `critic`, `explore`, `researcher`, `tracer` have direct research-team duplicates. The `omc-reference` skill confirms some are haiku-tier (`explore`, `writer`) — this **violates Akash's all-Opus doctrine** and is a pre-existing tech-debt item to flag.

## Capability classification by type

**Reasoning-heavy** (no tool-heavy): analyst, architect, critic, planner, researcher, scientist.

**Tool-heavy read-only**: explore, tracer, document-specialist, security-reviewer.

**Tool-heavy write**: executor, code-simplifier, git-manager, git-master, test-writer, writer, debugger.

**Multi-lens quality gates**: code-reviewer, qa-tester, test-engineer, verifier.

**Research Team (separate hierarchy)**: 18 specialists covering all lenses above — lead + planner + 6 structural lenses (cartographer, archaeologist, tracer, linguist) + 4 evidence sources (librarian, historian, web-miner, github-miner) + empiricist + synthesist + 3 adversarial gates (skeptic, adversary, evaluator) + moderator + scribe + retrospector.

## Gap table (cross-reference against the 10 sub-questions)

| Capability needed by the Forge mission | Covered? | By what? | Gap severity |
|---|---|---|---|
| Read and classify agent roster | **Yes** | research-cartographer (for local dirs), github-miner (for community rosters) | **covered** — no new work |
| Read installed plugins | **Partial** | Manual Read tool — no specialist. Could be a new **`forge-inventory`** specialist or a skill. | **small** |
| Read installed skills + detect format | **Partial** | Same as above | **small** |
| Draft new SKILL.md | **Yes** | `skill-creator` plugin (installed) + alirezarezvani's `self-improving-agent/skills/extract` | **covered — reuse, don't rebuild** |
| Run eval loop on new skill | **Yes** | `skill-creator`'s eval-viewer + aggregator scripts | **covered — reuse** |
| Propose skills without user prompting (curriculum) | **No** | No specialist or skill does this | **MAJOR GAP** — the Forge's signature capability |
| Query MCP Registry for candidate servers | **No** | No specialist. Must build via `gh api` or WebFetch wrapping registry.modelcontextprotocol.io | **MAJOR GAP** — scout role needed |
| Query anthropics/skills + community rosters | **Partial** | research-github-miner covers ad-hoc queries | **small** — can reuse github-miner method |
| Vet marketplace sources (SEO/astroturf filtering) | **Yes** | research-adversary | **covered — delegate to research-lead** |
| Deep research on "is there an authoritative source for X?" | **Yes** | research-lead + full 17-specialist team | **covered — delegate** |
| Track which authored skills actually got used | **No** | No mechanism exists | **MAJOR GAP** — needs hook or MEMORY.md counter |
| Curate Forge's own lessons across sessions | **Partial** | MEMORY.md pattern exists for research-lead; none for forge | **small** — replicate the pattern |
| Discover gaps by reading existing agent tool needs | **No** | No specialist does a "tool need → skill coverage" diff | **MAJOR GAP** |

## What this gap table implies

Four **major gaps**, all outside what research-lead already covers:

1. **Automatic curriculum** — nobody proposes new skills to build. This is a Voyager-class capability that skill-creator does NOT implement (skill-creator waits for the user to say "make me a skill").

2. **Scout for external sources** — querying MCP Registry programmatically, filtering, vetting, suggesting installs. Research-github-miner does ad-hoc GH queries, but is not parameterized for the MCP Registry API or the "should we install this" judgment.

3. **Value tracking** — no mechanism captures "did this skill help?" across sessions. Closest is `self-improving-agent`'s promotion flow but it's manually triggered, not automatic.

4. **Tool-need-to-skill-coverage diff** — a specialist that reads every agent file's tool list and every skill's description, then diffs them: "research-web-miner uses Playwright but only via MCP — if MCP goes down, there's no skill fallback" kind of reasoning. No specialist does this.

These four gaps define what the Forge must add **beyond** existing infrastructure. Everything else (authoring, evaluating, promoting, curating MEMORY.md) has an existing reusable implementation.

## Architectural implication

The Forge should be **downstream of skill-creator and self-improving-agent**, not a replacement. It orchestrates:

1. **Gap detection** (new capability)
2. → Research request to research-lead (existing)
3. → Authoring via skill-creator or self-improving-agent/extract (existing)
4. → Registration + MEMORY.md logging (reuse ACE pattern from research-lead)
5. → Value tracking across sessions (new capability — hook or manual counter bump)

This maps most cleanly to **H1 (single specialist)** OR **H2 (mini-team of 3-4 specialists)**. H3 (retrospector-internal) is too scoped. H4 (no workspace) loses the memory loop.

**Cartographer recommendation to the synthesist**: the architecture decision should be between H1 and H2, and the deciding factor is whether the scout role (MCP Registry + anthropics/skills + community rosters) is big enough to warrant its own specialist file. Given that `self-improving-agent` already demonstrates a multi-sub-skill plugin pattern (`remember`/`promote`/`extract`/`review`/`status` as 5 sub-skills under one umbrella), a **single-agent-with-skills** model (H1 with 5-6 sub-skills) is the cleanest, not a team with 5 separate agent files.

## Note on 88 "empty" skills in `~/.claude/skills/`

The top-level `ls ~/.claude/skills/` returned 91 names but only 3 have `SKILL.md` files at the top of their own directory. The 88 others (accelerate, audiocraft, autogpt, awq, axolotl, bigcode-evaluation-harness, bitsandbytes, blip-2, brainstorming-research-ideas, chroma, clip, constitutional-ai, cosmos-policy, creative-thinking-for-research, crewai, deepspeed, dspy, faiss, flash-attention, gguf, gptq, grpo-rl-training, guidance, hqq, huggingface-tokenizers, instructor, knowledge-distillation, lambda-labs, langchain, langsmith, litgpt, llama-cpp, llama-factory, llamaguard, llamaindex, llava, lm-evaluation-harness, long-context, mamba, megatron-core, miles, mlflow, modal, model-merging, model-pruning, moe-training, nanogpt, nemo-curator, nemo-evaluator, nemo-guardrails, nnsight, openpi, openrlhf, openvla-oft, outlines, peft, phoenix, pinecone, prompt-guard, pytorch-fsdp2, pytorch-lightning, pyvene, qdrant, ray-data, ray-train, rwkv, saelens, segment-anything, sentence-transformers, sentencepiece, sglang, simpo, skypilot, slime, speculative-decoding, stable-diffusion, swanlab, tensorboard, tensorrt-llm, torchforge, torchtitan, transformer-lens, trl-fine-tuning, unsloth, verl, vllm, weights-and-biases, whisper, 20-ml-paper-writing) map 1:1 to the `ai-research-skills/01-*` ... `ai-research-skills/20-*` directory structure.

**Hypothesis**: Akash's `~/.claude/skills/` is populated from `ai-research-skills/`, either via symlink, file copy, or the Claude Code runtime's plugin-skill-to-personal-skill discovery.

**Action**: not in scope for Forge session — it's a plumbing observation. Flag for a future cartography pass if relevant.

## Notable finding: the three local SKILL.mds

The only three personal skills with true local SKILL.md files are:
- **`0-autoresearch-skill`** — Orchestra Research, autonomous research orchestration, two-loop architecture.
- **`vllm`** (name: `serving-llms-vllm`) — Orchestra Research, vLLM serving skill.
- **`omc-reference`** — the OMC agent catalog reference skill (marked `user-invocable: false`, loads on-demand only).

The `omc-reference` one is interesting: it uses `user-invocable: false`, which means Claude decides when to load it but users can't `/omc-reference` it. This is **the right frontmatter for the Forge's own "I know the catalog" sub-skill** — reference content, not a user command.

## Cross-reference: what Akash has from `ai-research-skills` vs `claude-code-skills`

The `ai-research-skills` marketplace has a **Voyager-style numbered topic taxonomy** (01-model-architecture, 02-tokenization, 03-fine-tuning, ..., 21-research-ideation). This is an ML-research-focused skill library. ≈91 skills total.

The `claude-code-skills` marketplace (alirezarezvani) has **departmental organization** (agents/business-growth, agents/c-level, agents/engineering, agents/engineering-team, agents/finance, agents/marketing, agents/personas, agents/product, agents/project-management, agents/ra-qm-team) AND a production plugin bundle (`engineering-team/` with 50+ skill directories, some nested).

**Takeaway**: Akash's substrate is **research/ML-heavy** (ai-research-skills) + **departmental skill bundle** (claude-code-skills) + **official Anthropic tooling** (skill-creator, commit-commands, etc.). The Forge sits above all three — it's the meta-layer that authors new entries for any of them based on observed gaps.

## Deliverable to synthesist

**Five concrete gaps** the Forge must close, in priority order:

| # | Gap | Who else has solved it | Forge's method |
|---|---|---|---|
| 1 | **Automatic curriculum** — propose new skills without being asked | Voyager (not directly reusable) | Read agents/* tool needs, diff against skills/*, diff against registry; propose top-N |
| 2 | **MCP Registry scout** — query, filter, vet, recommend | Nobody | Wrap `gh api https://registry.modelcontextprotocol.io/v0/servers?search=X`; pass results to research-adversary for vetting |
| 3 | **Value tracking** — did the authored skill trigger later? | ACE (bullet counters) | MEMORY.md bullets with helpful/harmful counters, ACE-style |
| 4 | **Tool-need-vs-skill-coverage diff** — spot uncovered capabilities | Nobody at agent level | Read every agent file's frontmatter `tools:` and every skill's `description`, diff |
| 5 | **Research handoff protocol** — request deep research when gap is ambiguous | Nobody | Drop a file into `teams/research/inbox/forge-request-<slug>.md` that research-lead polls on session start |

Everything else (authoring SKILL.md, running eval loop, promoting to CLAUDE.md, extracting patterns) is already covered by skill-creator + self-improving-agent. **The Forge must reuse them**, not rebuild.
