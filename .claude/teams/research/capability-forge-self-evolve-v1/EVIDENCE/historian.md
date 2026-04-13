# Historian — academic prior art and industry parallels for self-improving skill libraries

## Source provenance

| Source | URL | Retrieved | Tier |
|---|---|---|---|
| Voyager (Wang et al. 2023) | `arxiv.org/abs/2305.16291` + voyager.minedojo.org | 2026-04-12 | STRONG-PRIMARY |
| ACE (Zhang et al. 2025) | `arxiv.org/abs/2510.04618` + HTML `/html/2510.04618v1` | 2026-04-12 | STRONG-PRIMARY |
| Anthropic Agent Skills launch | `claude.com/blog/skills` (Oct 16, 2025) | 2026-04-12 | STRONG-PRIMARY |
| Simon Willison: Claude Skills > MCP (Oct 16, 2025) | `simonwillison.net/2025/Oct/16/claude-skills/` | 2026-04-12 | STRONG-SECONDARY |
| Toolformer (Schick et al. 2023) | `arxiv.org/abs/2302.04761` | 2026-04-12 | STRONG-PRIMARY (abstract only; full pdf > 10MB limit) |
| Anthropic makes Skills open standard | SD Times Dec 19, 2025 + `agentskills.io` | 2026-04-12 | MIXED |

## Voyager (arxiv 2305.16291) — the reference impl for self-improving skill libraries

**Architecture**: three components.
1. **Automatic curriculum**: maximizes exploration by proposing next task.
2. **Ever-growing skill library of executable code**: stores and retrieves complex behaviors.
3. **Iterative prompting mechanism**: feedback from (a) environment, (b) execution errors, (c) self-verification.

**Skill library mechanics** (from paper secondary sources — primary PDF >10MB):
- Stored as **executable code** (Minecraft javascript skills), not natural language.
- Retrieved by embedding-based semantic search over task descriptions.
- Commit trigger: **only after self-verification passes** — a separate LLM agent ("critic") checks whether the program accomplishes the task goal. Only successful programs are committed to the library.
- Skills are **temporally extended, interpretable, and compositional**.
- Metric: 3.3x unique items, 2.3x longer distance traveled, 15.3x faster tech-tree milestones vs prior SOTA.
- **Ablation**: removing the skill library catastrophically degrades performance on novel tasks. The library is the load-bearing element.

**Key Voyager lesson for the Forge**: skills must be executable code (or instructions with bundled scripts), not pure natural language. The Claude Code Skills primitive already matches this — `SKILL.md` + bundled `scripts/` is directly analogous.

**Second Voyager lesson**: the critic / self-verification step is non-negotiable. A skill that doesn't pass self-verification must not be committed to the library. This maps directly to the skill-creator's eval loop (draft → test → grade → commit only if pass).

**Third Voyager lesson**: retrieval by embedding, not by name. For the Forge's internal catalog, description-based retrieval (which is what Claude Code's own skill triggering already uses) should be the discovery primitive.

## ACE (arxiv 2510.04618) — evolving playbooks, the meta-architecture

**Three-role division of labor**:
- **Generator** — produces reasoning trajectories for new queries. Surfaces effective strategies AND recurring pitfalls.
- **Reflector** — critiques traces, extracts lessons, refines across up to 5 iterations.
- **Curator** — synthesizes lessons into compact delta entries. Merges into existing context deterministically.

**Playbook data structure**:
- Organized as "structured, itemized bullets."
- Each bullet has two parts:
  - **Metadata**: unique ID + counters (`helpful_count`, `harmful_count`).
  - **Content**: a small unit — reusable strategy, domain concept, or common failure mode.
- **Delta updates are append-mostly**: new bullets are appended, existing ones have their counters updated in-place. Dedup via semantic embedding similarity.

**Performance**:
- +10.6% on agent benchmarks, +8.6% on finance.
- Works offline (system prompts) AND online (agent memory).
- No labeled supervision; uses natural execution feedback.
- Reduces adaptation latency and rollout cost.

**Avoids two failure modes**:
- **Brevity bias**: "drops domain insights for concise summaries." ACE resists by keeping bullets concrete and counted, not summarized.
- **Context collapse**: "iterative rewriting erodes details over time." ACE resists with the append-with-counter pattern (vs rewrite-in-place).

**Ablation**:
- Removing Reflector → -3.9 points on average.
- Omitting multi-epoch adaptation → -2.6 points.
- Both are load-bearing.

**Key ACE lesson for the Forge**: the self-improvement loop MUST separate (a) who generates skill candidates, (b) who critiques them, (c) who commits them. Putting all three in one role causes brevity bias and context collapse. The Forge architecture must have these three roles — whether as three agents in a team (H2) or three lens-passes in a single agent (H1).

**Second ACE lesson**: the memory structure for the Forge's own lessons should be bulleted, with helpful/harmful counters. This maps 1:1 to Akash's existing `~/.claude/agent-memory/research-lead/MEMORY.md` pattern — the research-lead lessons are already close to this format, just missing the counters.

**Third ACE lesson**: dedup via semantic similarity. The Forge's curator must not commit a skill-lesson if a semantically similar one already exists; update its counter instead.

## Toolformer (arxiv 2302.04761) — self-taught tool use

**Key idea** (from abstract): model decides which APIs to call, when, what arguments, how to incorporate results — "trained in a self-supervised way, requiring nothing more than a handful of demonstrations for each API." Tools: calculator, QA, two search engines, translation, calendar.

**Filtering criterion** (inferred from literature summaries, not primary due to PDF size limit): a candidate API call is kept in the training set only if incorporating it reduces the loss on the subsequent tokens. This is the self-supervised signal. Calls that don't help are discarded.

**Key Toolformer lesson for the Forge**: the **value metric for a skill** is "does invoking it improve the outcome?" Measure by comparing with-skill vs without-skill runs. This is exactly what the official `skill-creator`'s eval loop already does (iteration-N/with_skill/ vs without_skill/).

**Toolformer vs Voyager**: Toolformer teaches the model to use *existing* tools better. Voyager teaches the model to *create new* tools (skills). Akash's Forge is Voyager-class — it authors new skills. But the skill-creator's eval loop, which scores whether a new skill helps, is Toolformer-class filtering applied to the new skills.

## Anthropic Agent Skills launch (Oct 16, 2025)

**Rationale from the blog post**:
- Skills are folders of instructions + scripts + resources that Claude loads when needed.
- Purpose: "package expertise, making Claude a specialist on what matters most to you."
- Composable, portable, efficient (load only when relevant), executable (can include deterministic scripts).

**Specific launch examples**:
- Excel spreadsheet with formulas
- PowerPoint presentations
- Word documents
- Fillable PDFs
- Org brand guideline adherence
- Box integration for content transformation

**Skill-creator tool** (verbatim from blog): "The 'skill-creator' skill provides interactive guidance: Claude asks about your workflow, generates the folder structure, formats the SKILL.md file, and bundles the resources you need. No manual file editing required."

**Roadmap**:
- Organization-wide skill management (Dec 2025 update).
- Partner-built skills directory (`claude.com/connectors`).
- Agent Skills as open standard for cross-platform portability (Dec 19, 2025).

**Key launch lesson for the Forge**: **the skill-creator plugin is already canonical**. It is Anthropic's official approach to skill authoring, and Akash's `installed_plugins.json` shows it's installed. The Forge's job is to **wrap skill-creator with a gap-detection + internet-aggregation + curation loop**, not to reinvent the authoring or eval mechanics.

## Simon Willison — "Skills > MCP" take (Oct 16, 2025)

**Core argument**: MCP is a protocol specification with heavy token overhead ("tens of thousands of tokens of context"). Skills just use the LLM's existing filesystem + exec tools, progressive-disclosure-style. "Almost everything I might achieve with an MCP can be handled by a CLI tool instead."

**Examples**:
- `slack-gif-creator` skill — generates optimized animated GIFs.
- Envisioned "data journalism agent" composed of multiple skills (census access, SQLite/DuckDB load, S3/Datasette publish, D3 viz) — "a folder full of Markdown files."

**Caveat**: "Skills mechanism is entirely dependent on the model having access to a filesystem, tools to navigate it and the ability to execute commands." Security risks: prompt injection via skill content, sandboxing of skill-launched execution.

**Key Willison lesson for the Forge**: when deciding whether to build a skill or an MCP server for a gap, **default to skill**. MCP is for cases where (a) the capability needs a running service (OAuth, websocket, shared state across sessions), or (b) the tool needs cross-client portability (use outside Claude Code too). Everything else is a skill.

## Self-improvement loop synthesis (the Voyager + ACE + Toolformer composite)

The canonical loop for the Forge, derived from these three papers:

```
┌─────────────────────────────────────────────────────────────────────┐
│  1. GAP DETECTOR (Voyager "curriculum"):                            │
│     Read existing agents + skills + plugins. Propose next skill     │
│     that would close an observed capability gap.                    │
│                                                                     │
│  2. SCOUT (the "environment" in Voyager; the "internet" in Akash):  │
│     For the proposed skill, query MCP Registry + anthropics/skills  │
│     + community rosters. If a good one exists, adopt it. If not,    │
│     gather reference material for authoring.                        │
│                                                                     │
│  3. GENERATOR (ACE "Generator"):                                    │
│     Draft SKILL.md + bundled scripts. Use `skill-creator` as the    │
│     canonical authoring harness.                                    │
│                                                                     │
│  4. REFLECTOR (ACE "Reflector"; Voyager "self-verify"):             │
│     Run the skill against eval cases (the skill-creator's eval      │
│     loop). Refine up to N times. Fail = don't commit.               │
│                                                                     │
│  5. CURATOR (ACE "Curator"; Voyager "skill library"):               │
│     On pass, commit SKILL.md to ~/.claude/skills/ (personal) or     │
│     ~/.claude/forge/drafts/<name>/ (plugin-bound). Update an index. │
│     Log the lesson to MEMORY.md as a bulleted entry with counters.  │
│                                                                     │
│  6. SCORER (Toolformer filter):                                     │
│     On later sessions, detect skill invocations. Update             │
│     helpful/harmful counters. Prune skills that never trigger or    │
│     trigger harmfully.                                              │
└─────────────────────────────────────────────────────────────────────┘
```

This is the blueprint. The architecture debate (H1 vs H2 vs H3 vs H4) is now: **how many agents implement these 6 roles?**

## Cross-source patterns

| Paper | Curriculum | Generator | Critic | Library | Metric |
|---|---|---|---|---|---|
| Voyager | auto-curriculum (explore) | GPT-4 blackbox | self-verify agent | skill code-base | task success |
| ACE | (offline) | Generator role | Reflector role | bulleted playbook | benchmark accuracy |
| Toolformer | none (static API list) | model inserts calls | loss reduction filter | fine-tuned model weights | downstream task |
| skill-creator | user/Claude identifies gap | draft SKILL.md | eval + grader + analyzer | filesystem | pass_rate |

The **skill-creator** row is the one Akash's Forge must wrap, because it's (a) the canonical Anthropic pattern, (b) already installed, (c) already implements critic + library correctly for the Claude Code world.

The **Voyager + ACE + Toolformer** rows supply what skill-creator alone does not:
- Voyager: **automatic curriculum** — skill-creator waits for the user to say "make me a skill"; the Forge must propose skills without being asked, based on gap detection.
- ACE: **counter-based playbook dedup** — skill-creator has no concept of "this skill got used 100 times vs 0"; the Forge must track invocations.
- Toolformer: **helpful-vs-unhelpful filtering** — skill-creator measures pass_rate on eval cases, not real-session value. The Forge must also track whether authored skills actually trigger in real sessions.

## Remaining open questions for follow-up

- [ ] Full Voyager skill library retrieval details (embedding model used, top-k, rerank) — PDF too large for WebFetch; may need to read Voyager's github if empiricism matters.
- [ ] Toolformer's exact filter formula — need primary source.
- [ ] Does anthropics/skills have a meta-skill that wraps skill-creator with gap detection? README says no, but sampling the repo contents directly would confirm.
- [ ] Does agentskills.io (the open standard site) define a richer schema than Claude Code's? — check in round 2.
