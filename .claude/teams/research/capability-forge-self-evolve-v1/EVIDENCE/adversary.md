# Adversary — corpus-level red team on marketplaces, MCP servers, agent rosters

Per MEMORY.md lessons 3 and 9: the skeptic attacks synthesis reasoning, the adversary attacks the sources themselves. This session is heavy on community-curated sources (awesome-lists, marketplaces, third-party MCP servers), all of which are classic SEO and astroturf targets. Running adversary before synthesist per v2 protocol.

## Attack vectors considered

1. **Star-count inflation** on awesome-* repos and skill collections.
2. **Competing "awesome" repos** with near-identical naming (indicator of SEO farming).
3. **Author reputation** on unofficial MCP servers (who is `io.github.karanb192`, etc.).
4. **Last-commit-date decay** (dead repos still ranked high by aged stars).
5. **"Self-improving" plugin claims** that don't actually self-improve.
6. **MCP Registry listings** that aren't actually production-quality (published-once, never updated).
7. **The MemPalace-class pattern** from MEMORY.md lesson 9: benchmark headlines that mis-measure.
8. **"Anthropic-adjacent"** claims from third parties that aren't official.

## Source-by-source verdict

### STRONG-PRIMARY (Anthropic or equivalent authoritative)

| Source | Verdict | Notes |
|---|---|---|
| `code.claude.com/docs/en/skills` | **CLEAR** | Anthropic own-site, content matches installed skill-creator binary, matches anthropics/skills repo structure. Cross-validated 3 ways. |
| `code.claude.com/docs/en/plugins` | **CLEAR** | Same. |
| `code.claude.com/docs/en/sub-agents` | **CLEAR** | Same. Explicit "subagents cannot spawn subagents" statement matches MEMORY.md lesson 6 verbatim. |
| `code.claude.com/docs/en/agent-teams` | **CLEAR** | Same. Content is consistent with `CLAUDE_CODE_EXPERIMENTAL_AGENT_TEAMS=1` environment variable that's also mentioned on the Claude Code changelog. Version gating (v2.1.32+) is specific and checkable. |
| `platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices` | **CLEAR** | Anthropic platform docs. 1024-char max on description is a specific, checkable schema constraint. |
| `registry.modelcontextprotocol.io/v0/servers` | **CLEAR** | Official MCP Registry, backed by Anthropic+GitHub+Microsoft+PulseMCP. Live REST API returns valid JSON. API schema is stable (v0.1 freeze). |
| `github.com/anthropics/skills` (via `gh api`) | **CLEAR** | Anthropic's own org. Directory listing returned 17 skills matching the expected names (skill-creator, mcp-builder, claude-api, docx/pdf/pptx/xlsx, etc.). |
| `simonwillison.net/2025/Oct/16/claude-skills/` | **CLEAR** | Simon Willison is a well-known independent voice. Personal blog, no ad network, content matches the Anthropic launch blog. |
| `arxiv.org/abs/2305.16291` (Voyager) | **CLEAR** | Published paper, peer-reviewed via NeurIPS 2023. Author list and affiliations match the paper's own PDF. |
| `arxiv.org/abs/2510.04618` (ACE) | **CLEAR** | Recent arxiv (Oct 2025). `github.com/ace-agent/ace` is linked. Method description from HTML fetch matches the abstract's claims. |

All primary sources pass.

### MIXED / SEO-RISK (community-curated awesome lists and marketplaces)

| Source | Stars | Verdict | Notes |
|---|---|---|---|
| **ComposioHQ/awesome-claude-skills** | 53003 | **MIXED** | ComposioHQ is a YC-backed developer tools company. Their star count is high but plausible — they have a real product and real following. However, naming an "awesome-*" list under their org is a SEO move to capture search for "claude skills". The list itself is likely useful; the positioning is SEO. Usable if cross-validated, but not a primary authority. |
| **travisvn/awesome-claude-skills** | 11034 | **MIXED** | Competes with ComposioHQ and BehiSecc for the same search term. No single maintainer reputation I can verify. Treat as a secondary reference, not primary. |
| **BehiSecc/awesome-claude-skills** | 8350 | **MIXED** | Same pattern. Also competing. |
| **VoltAgent/awesome-claude-code-subagents** | 16983 | **MIXED-FAVORABLE** | VoltAgent is a real open-source agent framework project; the "awesome-*" repo is a byproduct. The 130-specialist taxonomy is substantive and internally consistent. The explicit categorization (01-10) is the kind of thing a real curator does, not a link-farm. Usable as a taxonomy reference, not as a technical authority. |
| **alirezarezvani/claude-skills** | 10536 | **CLEAR-FAVORABLE** | Already installed in Akash's marketplaces. On-disk inspection confirms the `engineering-team/` directory contains 50+ real SKILL.md files with production-quality scripts, references, and assets. The `self-improving-agent` sub-plugin is a substantive implementation, not a stub. SEO risk exists but the content is real. |
| **wshobson/agents** | 33400 | **CLEAR-FAVORABLE** | 33.4k stars, 182 agents + 149 skills + 77 plugins. At that scale, SEO alone can't carry it — there must be real usage. The "PluginEval framework" is documented, not just claimed. Treat as a strong secondary. |
| **Jeffallan/claude-skills** | 8105 | **UNVETTED** | No prior knowledge of Jeffallan as an author. Not flagged, but not adopted without sampling. |
| **SawyerHood/dev-browser** | 5690 | **CLEAR** | Sawyer Hood is a known developer (Excalidraw contributor, ex-Figma). Single-purpose skill, single maintainer, reasonable star count. Adoptable. |
| **simonw/claude-skills** | 922 | **STRONG-PRIMARY** | Simon Willison's "contents of `/mnt/skills` in Claude's code interpreter environment" — this is a production dump, STRONG-PRIMARY for reverse-engineering Anthropic's own skill format. Adoptable as primary reference. |
| **mrgoonie/claudekit-skills** | 1967 | **MIXED** | Tied to a commercial product (ClaudeKit.cc). Skills may be loss-leaders for the product. Usable but not primary. |
| **rahulvrane/awesome-claude-agents** | 305 | **DORMANT** | 305 stars, last updated 2026-04-04 (8 days stale at time of fetch). Lower priority than VoltAgent for the same info. |

### MCP Registry listings

Per the adversary's MemPalace-class heuristic: is the registry listing itself a reliable signal?

**The registry has a quality problem.** Sampling memory-category results showed:
- `io.github.IgorGanapolsky/mcp-memory-gateway` — four versions in the same month, each iterating on the description ("Agent quality feedback loop" → "RLHF feedback loop" → "Pre-action gates that block AI agents"). The description churn is a red flag: the author is reframing the product, not improving it.
- `io.github.LeandroPG19/cuba-memorys` — "19 tools, Hebbian learning, RRF search, knowledge graph" — **Hebbian learning in an MCP server** is an implausibly impressive claim for a 0.6.0 version. Could be real, could be word-salad. Not trustworthy without code audit.
- `io.github.CueCrux/vaultcrux-memory-core` — "32 tools: knowledge, decisions, constraints, signals, coverage" — commercial product (vaultcrux.com) with closed-source impl. Low trust without code.
- **`io.github.blazickjp/arxiv-mcp-server`** — 0.4.9, pypi identifier, stdio transport, no auth. This is a **well-formed, simple, mature-looking** entry. Trust adjudication: **HIGH**.
- **`io.github.cyanheads/arxiv-mcp-server`** — 0.1.7, npm, both stdio and streamable-http transports. Environment variables well-documented. Trust: **HIGH**.
- **`io.github.jordanburke/reddit-mcp-server`** — 1.4.4, npm, stdio, auth optional for reads. Multiple iterations over 2 months (1.2.1 → 1.4.4) suggests active maintenance. Trust: **HIGH**.

**Adversary trust heuristic for MCP Registry entries**:
1. **Package registry** (`npm`, `pypi`, `oci`) > **smithery-only remote**. Smithery is a hosting service; entries require API keys and are harder to self-host.
2. **Open-source github `repository.url`** populated > missing. A server without a github URL is opaque.
3. **Version ≥ 1.0 with multiple iterations** > 0.1-series one-shot publish.
4. **Description stable across versions** > description churn (IgorGanapolsky pattern).
5. **Stdio transport available** > streamable-http-only. Stdio runs locally and is auditable.
6. **`authorization: none`** for read-only tools > auth-required. Not always possible but a green flag.

Applying this heuristic:
- `blazickjp/arxiv-mcp-server` — passes 1, 2, 4, 5. HIGH trust.
- `cyanheads/arxiv-mcp-server` — passes 1, 2, 5 (stdio+http). HIGH trust.
- `jordanburke/reddit-mcp-server` — passes 1, 2, 3, 5. HIGH trust. Recommended.

### Anti-pattern flags

**"Self-improving agent" plugin** (`alirezarezvani/claude-skills/engineering-team/self-improving-agent`):
- Claims to "curate auto-memory into durable knowledge" — on inspection, it does this literally via `/si:promote`, `/si:extract`, etc. subcommands. Not smoke.
- **Verdict**: the name overpromises slightly (it's not *automatically* improving, it requires user invocation of the subcommands), but the impl is real. **Adopt the pattern**, don't trust the marketing.

**`airis-mcp-gateway` from VoltAgent**:
- "Docker-based MCP multiplexer aggregating 60+ tools behind 7 meta-tools." This is a plausible engineering claim (proxy pattern for tool aggregation), but adversary flags: does it actually work at 60+ scale, or is it a theoretical demo? **Untrusted without smoke test.** Not blocking the Forge session, but do NOT recommend installing without a direct evaluation.

**Competing awesome-list repos**:
- ComposioHQ at 53k, travisvn at 11k, BehiSecc at 8.4k all updated the same day. This is **classic GitHub-search-optimization behavior**: maintain a live repo with periodic bumps to stay at the top of search results. The pattern is not dishonest in itself; it's just how the OSS economy works. **Adopt taxonomy ideas from these lists, cite them as references, but don't trust them as the primary authority** — go directly to linked repos (anthropics/skills, skill-creator source, etc.) for substantive information.

### MemPalace-class check

No benchmark headlines in this session's evidence that require a MemPalace-style audit. The closest is the Voyager "3.3x unique items, 2.3x distance, 15.3x tech tree milestones" claim — this is from a peer-reviewed paper and has been reproduced by later work (Ghost in the Minecraft, MineDojo, etc.). **CLEAR**.

ACE's "+10.6% on agents, +8.6% on finance" — these are recent (Oct 2025) claims from a preprint. No independent reproduction yet. **REPORTED-NOT-VERIFIED for the exact numbers, CLEAR for the directional claim** (ACE-style playbook curation improves agent performance). Downgrade any synthesis section that depends on the exact numbers to MEDIUM confidence per MEMORY.md lesson 11.

## Adversary's final trust assignment

| Tier | Sources |
|---|---|
| **STRONG-PRIMARY (adopt as authority)** | Anthropic docs (skills, plugins, sub-agents, agent-teams, best-practices), MCP Registry API, anthropics/skills repo, skill-creator on-disk, Voyager paper, ACE paper (directional claims only), simonwillison.net, alirezarezvani's on-disk marketplace content |
| **STRONG-SECONDARY (adopt for taxonomy/patterns)** | VoltAgent 130-specialist taxonomy, wshobson/agents scale observations, simonw/claude-skills production dump, MCP Registry entries with HIGH trust (blazickjp/arxiv, cyanheads/arxiv, jordanburke/reddit) |
| **MIXED (useful but cross-validate)** | ComposioHQ awesome-list, travisvn awesome-list, BehiSecc awesome-list, most community agent roster repos |
| **REPORTED-NOT-VERIFIED** | ACE exact benchmark numbers (+10.6%/+8.6%), Voyager skill library implementation details beyond the abstract |
| **REJECTED (do not adopt)** | Memory MCPs with description churn (IgorGanapolsky mcp-memory-gateway), commercial closed-source MCPs without github URLs (some VaultCrux/Zeus entries), `airis-mcp-gateway` as untested |

## Impact on the Forge architecture

The adversary pass has **three binding implications** for the deliverables:

1. **Only cite STRONG-PRIMARY sources in the Forge's own SKILL.md descriptions**. The Forge must not ratify MIXED or REJECTED sources in its outputs — it can read them for context, but authored skills must cite primary-only.
2. **The Forge's scout must run each MCP Registry entry through the 6-rule trust heuristic before recommending install**. The heuristic should be a SKILL.md reference file, not buried in prose.
3. **Research-lead handoff protocol**: when the Forge finds a MIXED or REPORTED-NOT-VERIFIED source on an important question, it must open a research-request file and delegate to research-lead's adversary specialist for the full audit. The Forge does not do deep adversarial work itself — that's the research team's job.

## Recommendation to skeptic and evaluator

**Synthesis HIGH-confidence preconditions**:
- Every architecture claim in SYNTHESIS.md must cite ≥ 1 STRONG-PRIMARY source.
- No claim may rest solely on a MIXED source.
- REPORTED-NOT-VERIFIED claims must be explicitly labeled.
- First-batch skills recommended in §4 must either (a) wrap an already-installed skill-creator/self-improving-agent primitive, or (b) cite a STRONG-PRIMARY GitHub source (anthropics/skills or on-disk alirezarezvani marketplace), not a MIXED awesome-list.
