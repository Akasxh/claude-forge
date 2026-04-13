# GitHub-miner — community skill/agent rosters, plugin marketplaces, MCP Registry sweep

## Source provenance

All results from `gh` CLI against github.com and `registry.modelcontextprotocol.io` REST API. Retrieved 2026-04-12.

## Community Claude Code agent/skill rosters — star-ranked

| Repo | Stars | Last updated | Structure | Tier |
|---|---|---|---|---|
| **ComposioHQ/awesome-claude-skills** | **53003** | 2026-04-11 | Awesome-list curation | MIXED (SEO risk — adversary flag) |
| **VoltAgent/awesome-claude-code-subagents** | **16983** | 2026-04-11 | 130+ specialists, 10 categories | STRONG-SECONDARY |
| **travisvn/awesome-claude-skills** | **11034** | 2026-04-11 | Awesome-list curation | MIXED (SEO risk) |
| **alirezarezvani/claude-skills** | **10536** | 2026-04-11 | 232+ skills + agents; **ALREADY INSTALLED** in Akash's marketplaces | STRONG-PRIMARY (on-disk) |
| **BehiSecc/awesome-claude-skills** | **8350** | 2026-04-11 | Awesome-list | MIXED (SEO risk) |
| **Jeffallan/claude-skills** | **8105** | 2026-04-11 | 66 full-stack specialist skills | STRONG-SECONDARY |
| **SawyerHood/dev-browser** | **5690** | 2026-04-11 | Single skill (web browser for agent) | STRONG-PRIMARY |
| **vijaythecoder/awesome-claude-agents** | **4140** | 2026-04-11 | Orchestrated sub-agent dev team | STRONG-SECONDARY |
| **mrgoonie/claudekit-skills** | **1967** | 2026-04-11 | Curated skill bundle | MIXED |
| **simonw/claude-skills** | **922** | 2026-04-10 | Contents of `/mnt/skills` in Claude's code interpreter | STRONG-PRIMARY (primary source, dumped from production) |
| **SynaLinks/synalinks-skills** | **898** | 2026-04-08 | Vendor-specific | SCOPED |
| **0xfurai/claude-code-subagents** | **826** | 2026-04-11 | 100+ production-ready subagents | STRONG-SECONDARY |
| **coleam00/second-brain-skills** | **664** | 2026-04-11 | Second-brain focused | STRONG-SECONDARY |
| **dgreenheck/webgpu-claude-skill** | **584** | 2026-04-11 | Single specialty skill | STRONG-PRIMARY |
| **chujianyun/skills** | **464** | 2026-04-11 | Personal collection | SCOPED |
| **instavm/open-skills** | **398** | 2026-04-11 | Run Claude Skills locally with any LLM | SCOPED |
| **staruhub/ClaudeSkills** | **349** | 2026-04-10 | Learning-focused | SCOPED |
| **rahulvrane/awesome-claude-agents** | **305** | 2026-04-04 | Awesome-list | MIXED (dormant relative to others) |
| **NTCoding/claude-skillz** | **299** | 2026-04-11 | Simple programming skills | SCOPED |
| **wshobson/agents** | **33400** (from Substack query earlier) | 2026-04-11 | 182 agents, 16 orchestrators, 149 skills, 96 commands, 77 plugins | STRONG-SECONDARY |

## Pattern analysis across rosters

### VoltAgent/awesome-claude-code-subagents (17k stars, 130+ specialists)

Ten categories — this is the canonical "what specialists should a workforce have" taxonomy from the community:

1. **01-core-development** — api-designer, backend-developer, frontend-developer, fullstack-developer, graphql-architect, microservices-architect, mobile-developer, ui-designer, websocket-engineer, electron-pro, design-bridge (11 specialists)
2. **02-language-specialists** — typescript-pro, python-pro, rust-engineer, golang-pro, java-architect, kotlin-specialist, swift-expert, cpp-pro, csharp-developer, fastapi-developer, django-developer, dotnet-core-expert, dotnet-framework-4.8-expert, elixir-expert, expo-react-native-expert, flutter-expert, javascript-pro, laravel-specialist, nextjs-developer, php-pro, powershell-5.1-expert, powershell-7-expert, rails-expert, react-specialist, spring-boot-engineer, symfony-specialist, sql-pro, vue-expert, angular-architect (29 specialists)
3. **03-infrastructure** — azure-infra-engineer, cloud-architect, database-administrator, docker-expert, deployment-engineer, devops-engineer, devops-incident-responder, incident-responder, kubernetes-specialist, network-engineer, platform-engineer, security-engineer, sre-engineer, terraform-engineer, terragrunt-expert, windows-infra-admin (16)
4. **04-quality-security** — accessibility-tester, ad-security-reviewer, ai-writing-auditor, architect-reviewer, chaos-engineer, code-reviewer, compliance-auditor, debugger, error-detective, penetration-tester, performance-engineer, powershell-security-hardening, qa-expert, security-auditor, test-automator (15)
5. **05-data-ai** — ai-engineer, data-analyst, data-engineer, data-scientist, database-optimizer, llm-architect, machine-learning-engineer, ml-engineer, mlops-engineer, nlp-engineer, postgres-pro, prompt-engineer, reinforcement-learning-engineer (13)
6. **06-developer-experience** — build-engineer, cli-developer, dependency-manager, documentation-engineer, dx-optimizer, git-workflow-manager, legacy-modernizer, **mcp-developer**, powershell-ui-architect, powershell-module-architect, readme-generator, refactoring-specialist, slack-expert, tooling-engineer (14)
7. **07-specialized-domains** — api-documenter, blockchain-developer, embedded-systems, fintech-engineer, game-developer, iot-engineer, m365-admin, mobile-app-developer, payment-integration, quant-analyst, risk-manager, seo-specialist (12)
8. **08-business-product** — business-analyst, content-marketer, customer-success-manager, legal-advisor, license-engineer, product-manager, project-manager, sales-engineer, scrum-master, technical-writer, ux-researcher, wordpress-master (12)
9. **09-meta-orchestration** — **airis-mcp-gateway, agent-installer, agent-organizer, context-manager, error-coordinator, it-ops-orchestrator, knowledge-synthesizer, multi-agent-coordinator, performance-monitor, pied-piper, task-distributor, taskade, workflow-orchestrator** (13) — **this is the category most relevant to the Forge**
10. **10-research-analysis** — research-analyst, search-specialist, trend-analyst, competitive-analyst, market-researcher, project-idea-validator, data-researcher, scientific-literature-researcher (8)

**Notable for the Forge's design**:
- **`agent-installer`** — "Browse and install agents from repository via GitHub." This is a gap Akash's workforce has — no specialist for installing agents from remote rosters.
- **`knowledge-synthesizer`** — "Knowledge aggregation expert." Overlaps with research-synthesist but scoped to general knowledge, not research findings.
- **`agent-organizer`** — "Multi-agent coordinator." Overlaps with research-lead.
- **`airis-mcp-gateway`** — "Docker-based MCP multiplexer aggregating 60+ tools behind 7 meta-tools." This is literally the pattern Akash's orchestration session is designing.
- **`mcp-developer`** (under dev-experience) — "Model Context Protocol specialist." The workforce has no MCP authoring specialist today.

### wshobson/agents (33.4k stars)

"A comprehensive production-ready system combining **182 specialized AI agents, 16 multi-agent workflow orchestrators, 149 agent skills, and 96 commands organized into 77 focused, single-purpose plugins**."

- Three-tier model strategy (Opus for critical, Sonnet for complex, Haiku for operations) — Akash's doctrine is all-Opus-max-effort, so the wshobson tier strategy is informational, not adoptable.
- **PluginEval framework** for quality certification with multi-layer evaluation — this IS a certification pipeline, directly relevant to the Forge's testing phase.
- Progressive disclosure via 149 specialized skills.
- No explicit "capability forge" term, but the 77-plugin architecture demonstrates what scale a workforce can grow to.

### alirezarezvani/claude-skills (10.5k, ON-DISK)

Already installed in `~/.claude/plugins/marketplaces/claude-code-skills/`. Contains:
- `agents/` — business-growth, c-level, engineering-team, engineering, finance, marketing, personas, product, project-management, ra-qm-team (across 10 departments)
- `commands/` — 23 slash commands (a11y-audit, changelog, code-to-prd, competitive-matrix, financial-health, focused-fix, google-workspace, okr, persona, pipeline, plugin-audit, prd, project-health, retro, rice, saas-health, seo-auditor, sprint-health, sprint-plan, tdd, tech-debt, user-story)
- `engineering-team/` — a full plugin bundle with pre-built skills: a11y-audit, ai-security, adversarial-reviewer, aws-solution-architect, azure-cloud-architect, cloud-security, code-reviewer, email-template-builder, epic-design, gcp-cloud-architect, google-workspace-cli, incident-commander, and more. Each has `SKILL.md + references/ + scripts/ + assets/ + expected_outputs/`. This is **a production example of a plugin bundle Akash can study**.
- `orchestration/ORCHESTRATION.md` — orchestration patterns doc.

**Takeaway**: this marketplace is a ready-to-study reference. For the Forge's smoke test, the Forge should read one of alirezarezvani's engineering-team SKILL.mds (say `adversarial-reviewer` or `code-reviewer`) as the template format.

### simonw/claude-skills (922, primary source)

"The contents of /mnt/skills in Claude's code interpreter environment." This is **dumped directly from Claude's production environment** — it shows what skills Anthropic ships in the code interpreter. These are STRONG-PRIMARY references for the canonical SKILL.md format.

### Trust adjudication (preview — full writeup in adversary.md)

**ComposioHQ/awesome-claude-skills at 53k, travisvn at 11k, BehiSecc at 8.4k** — three competing "awesome" lists, all updated in the same day (2026-04-11), all with similar names. This is textbook SEO farm behavior. Flag for adversary pass.

## MCP Registry sweep — what exists, what's missing

Query pattern: `GET https://registry.modelcontextprotocol.io/v0/servers?search=<keyword>&limit=N`.

| Category | Search term | Count | Top servers | Forge action |
|---|---|---|---|---|
| arXiv | `arxiv` | 5 | `io.github.blazickjp/arxiv-mcp-server` (0.4.9, pypi/uvx), `io.github.cyanheads/arxiv-mcp-server` (0.1.7, npm/bun), `ai.smithery/shoumikdc-arxiv-mcp` (remote, smithery auth) | **INSTALL blazickjp — mature, pypi, stdio, no auth** |
| Semantic Scholar | `semantic scholar` | **0** | — | **GAP — Forge should author or find elsewhere** |
| Hacker News | `hacker news` | **0** | — | **GAP — Forge should author or find elsewhere** |
| Reddit | `reddit` | 10+ | `io.github.jordanburke/reddit-mcp-server` (1.4.4, read+write, npm, auth optional for read) | **INSTALL jordanburke — read-only mode works anonymously** |
| Playwright | `playwright` | 6 | Official `microsoft/playwright-mcp` (already used via MCP config), plus test/reporting variants | **ALREADY HAVE** |
| Context7 | `context7` | 4 | `io.github.upstash/context7` (1.0.31, npm, API key required) | **ALREADY HAVE** (installed via claude-plugins-official marketplace) |
| Memory / vector | `memory` | 20+ | Too many — Letta, VaultCrux, Memory Nexus, etc. High SEO variance. | **FLAG for research on which to trust** — this is the memory-layer session's domain |

**Critical gaps to fill first** (from this sweep):
1. **No Hacker News MCP** — Akash's research team's web-miner uses WebFetch against HN Algolia. An MCP would give first-class integration.
2. **No Semantic Scholar MCP** — research-historian currently uses WebFetch. An MCP would unlock API-batched retrieval.
3. **No arxiv MCP installed** (but 3 candidates exist in registry) — low-hanging fruit for the Forge's first batch.

### MCP Registry API details (captured from nordicapis.com + registry.modelcontextprotocol.io)

**Base**: `https://registry.modelcontextprotocol.io/v0` (v0.1 API freeze since Oct 24, 2025).

**Endpoints**:
- `GET /v0/servers?limit=N&cursor=OPAQUE&search=KEYWORD` — list with cursor pagination, 100/page max.
- `GET /v0/servers?updated_since=RFC3339` — filter by update time.

**Response shape** (verbatim):
```json
{
  "servers": [
    {
      "server": {
        "name": "io.github.org/slug",
        "description": "string",
        "repository": {"url": "string", "source": "github"},
        "version": "string",
        "packages": [
          {
            "registryType": "npm|pypi|nuget|oci|mcpb|...",
            "identifier": "string",
            "version": "string",
            "transport": {"type": "stdio|sse|streamable-http", "url": "string?"}
          }
        ],
        "remotes": [
          {"type": "streamable-http", "url": "string", "headers": [...]}
        ]
      },
      "_meta": {
        "io.modelcontextprotocol.registry/official": {
          "status": "active|deprecated",
          "publishedAt": "ISO8601",
          "updatedAt": "ISO8601",
          "isLatest": true
        }
      }
    }
  ],
  "metadata": {"count": N, "nextCursor": "opaque|null"}
}
```

**Auth**: public read, no auth needed for list endpoints.

**Trust signal in the schema**: the `_meta.io.modelcontextprotocol.registry/official.status` field is the registry's canonical "is this server vetted" marker. The Forge's scout should filter by `status: "active"` and prefer servers with a populated `repository.url` (github.com links cross-validate).

## anthropics/skills official repo contents (inference from sampled sources)

- `skills/skill-creator/` — canonical skill authoring harness (on-disk, read).
- `skills/claude-api/` — one of the bundled skills mentioned in WebSearch; teaches Claude to use the Anthropic API / SDK (already surfaced in session tool list).
- `skills/docx/`, `skills/pdf/`, `skills/pptx/`, `skills/xlsx/` — document creation skills, **source-available not open source**, shared as reference implementations. These power Claude's production document features. READ these in round 2 for full schema.
- Other categories from README: Creative & Design, Development & Technical, Enterprise & Communication.
- **Install command** (from README): `/plugin marketplace add anthropics/skills` — then `/plugin install document-skills` or `/plugin install example-skills`.

**Action for Forge**: the Forge should propose Akash add the anthropics/skills marketplace (it's the official one) alongside the existing marketplaces.

## Top community specialist categories Akash's flat `~/.claude/agents/` lacks

Cross-referencing VoltAgent's 10 categories against Akash's `ls ~/.claude/agents/`:

| VoltAgent category | Akash has | Akash lacks |
|---|---|---|
| core-development | architect, executor | backend-developer, frontend-developer, api-designer, fullstack-developer, websocket-engineer, microservices-architect, ui-designer |
| language-specialists | — (none) | every single one (typescript-pro, python-pro, rust-engineer, etc.) |
| infrastructure | security-reviewer | cloud-architect, devops-engineer, kubernetes-specialist, terraform-engineer, incident-responder, sre-engineer |
| quality-security | code-reviewer, qa-tester, security-reviewer | accessibility-tester, chaos-engineer, compliance-auditor, debugger, error-detective, penetration-tester |
| data-ai | scientist | ai-engineer, data-engineer, mlops-engineer, prompt-engineer, llm-architect |
| developer-experience | git-manager, git-master | build-engineer, cli-developer, dependency-manager, documentation-engineer, dx-optimizer, **mcp-developer**, readme-generator, refactoring-specialist, tooling-engineer |
| specialized-domains | — | all (12) |
| business-product | — | all (12) |
| meta-orchestration | — | **all (13) — complete gap** — agent-installer, agent-organizer, context-manager, knowledge-synthesizer, multi-agent-coordinator, performance-monitor, workflow-orchestrator, etc. |
| research-analysis | research-lead + 17 specialists (strongly staffed) | nothing missing — Akash's research team is already deeper than VoltAgent's |

**Major finding**: Akash's flat `agents/` is **strongly research-covered** (via the 18 research-* agents) but **catastrophically under-staffed** on meta-orchestration, language specialists, and developer experience. The meta-orchestration gap is the most relevant to the Forge because orchestration is what the parallel "orchestration-full-activation-v1" session is designing. The Forge should not duplicate that work; it should author the *skills* orchestrators need.

## Key findings summary (for synthesist)

1. Community rosters converge on 10-category taxonomy. Akash has strong research, thin everywhere else.
2. The single biggest capability gap vs community is **meta-orchestration** — 13 specialists Akash lacks. The parallel orchestration session is addressing this; Forge should not duplicate.
3. The MCP Registry API is production-ready, v0.1 frozen, public read. It is the scout's primary endpoint.
4. Three arxiv MCP servers exist; Akash has none installed. Easy install.
5. Hacker News and Semantic Scholar MCPs **do not exist in the registry**. Forge should either build them or find third-party ones.
6. alirezarezvani's marketplace (ON DISK) has `engineering-team/` with 15+ full plugin bundles that are gold standard examples to study for format/structure.
7. simonw/claude-skills is the only "production dump" roster — STRONG-PRIMARY reference for the canonical SKILL.md format.
8. VoltAgent's `agent-installer`, `mcp-developer`, and `airis-mcp-gateway` are three specialists the Forge or an adjacent team should adopt.
9. Anthropic's official anthropics/skills marketplace is NOT in Akash's known_marketplaces.json. Adding it is the cheapest first move.
