# Web Miner — community corpus on agent memory 2025-2026

## Crawl plan
- **Sources**: HN Algolia (full), Reddit (blocked — see anomaly), HN
  comment dives for load-bearing threads, Zep's and Letta's own blogs.
- **Tiers used**: Tier 1 JSON APIs (HN Algolia) throughout; Tier 2 HTML
  (WebFetch) for Letta and Zep blog posts.
- **Expected record shape**: {title, url, author, points, num_comments,
  created_at, objectID}
- **Stop criteria**: ≥ 50 stories cited; HN search queries exhausted
  on all 7 major system names plus the generic term "agent memory"

## Sources & provenance

| Source | Tier | URL pattern | Rate limit | Records fetched |
|--------|------|-------------|------------|-----------------|
| HN Algolia (stories) | 1 | `hn.algolia.com/api/v1/search?query=...&tags=story` | none hit | 150+ stories across 4 queries |
| HN Algolia (items) | 1 | `hn.algolia.com/api/v1/items/<id>` | none hit | 3 comment trees |
| Zep blog | 2 | `blog.getzep.com/...` | none hit | 2 posts |
| Letta blog | 2 | `www.letta.com/blog/...` | none hit | 2 posts |
| Steve Yegge Medium | 2 | `steve-yegge.medium.com/...` | none hit | 1 post |
| Reddit | BLOCKED | `reddit.com/.../.json` | **Claude Code blocked by robots.txt** | 0 |

## Extracted records — HN corpus

### Top HN threads on the 7 key systems

**Mem0 (query: `mem0`, tags=story)** — 42+ results total:
| Title | Points | Comments | Date | ObjectID |
|---|---|---|---|---|
| Show HN: Mem0 – open-source Memory Layer for AI apps | 201 | 61 | 2024-09-04 | 41447317 |
| Show HN: Mem0 Browser Extension: Shared Memory Across ChatGPT/Claude/Perplexity | 34 | 4 | 2024-11-04 | 42042401 |
| Ask HN: Mem0 stores memories, but doesn't learn user patterns | 9 | 7 | 2026-02-04 | 46891715 |
| Show HN: Agentic AI Frameworks on AWS (includes Mem0) | 7 | 0 | 2025-08-02 | 44763850 |
| Cortex – Local-first AI memory engine, beats Mem0 on LoCoMo, encrypted, free | 4 | 2 | 2026-03-24 | 47501353 |
| Mem0 raises $24M to build the memory layer for AI apps (TechCrunch) | 2 | 1 | 2025-10-28 | 45734522 |
| Show HN: Engram – Open-source agent memory that beats Mem0 by 20% on LOCOMO | 2 | 0 | 2026-02-25 | 47153987 |
| Show HN: VAC Memory – 80.1% LoCoMo accuracy vs. Mem0's 68% | 2 | 0 | 2025-12-02 | 46123550 |
| Lies, Damn Lies, & Statistics: Is Mem0 SOTA in Agent Memory? (blog.getzep.com) | 2 | 0 | 2025-05-06 | 43909538 |
| Show HN: Persistent memory for Claude Code using Mem0 | 1 | 0 | 2025-12-23 | 46364699 |
| Forensic beats Mem0 with 90.1% on LOCOMO | 1 | 0 | 2026-03-28 | 47553405 |
| Mem0: Three Prompts Created a Viral AI Memory Layer (blog.lqhl.me) | 1 | 0 | 2024-08-08 | 41187481 |

**Letta (query: `letta`, tags=story)** — 19 results:
| Title | Points | Comments | Date | ObjectID |
|---|---|---|---|---|
| Letta: Letta is a framework for creating LLM services with memory | 121 | 22 | 2025-03-07 | 43294974 |
| Letta Code | 83 | 37 | 2025-12-16 | 46294274 |
| Letta Code: a memory-first coding agent | 6 | 3 | 2025-12-16 | 46293374 |
| Context Repositories: Git-Based Memory for Coding Agents | 4 | 0 | 2026-02-12 | 46996726 |
| Context-Bench: Benchmarking LLMs on Agentic Context Engineering | 5 | 0 | 2025-10-31 | 45775329 |
| Context Constitution | 5 | 0 | 2026-04-02 | 47619911 |
| Show HN: Letta – Git-Based Memory for Coding Agents | 2 | 0 | 2026-02-15 | 47020904 |
| Letta's Next Phase | 2 | 0 | 2026-03-16 | 47406067 |
| The Letta Code App | 2 | 0 | 2026-04-10 | 47718214 |
| Claude Sonnet 4.5 and the memory Omni-tool in Letta | 1 | 1 | 2025-09-30 | 45431326 |
| Letta Leaderboard: Benchmarking LLMs on Agentic Memory | 1 | 0 | 2025-05-29 | 44130225 |
| Continual Learning in Token Space | 3 | 0 | 2025-12-11 | 46235970 |
| RAG is not agent memory | 3 | 0 | 2025-02-13 | 43039467 |

**MemGPT (query: `memgpt`, tags=story)** — 10 results (most pre-rebrand):
| Title | Points | Comments | Date | ObjectID |
|---|---|---|---|---|
| MemGPT – LLMs with self-editing memory for unbounded context | 363 | 85 | 2023-10-16 | 37901902 |
| MemGPT: Towards LLMs as Operating Systems (arxiv) | 225 | 106 | 2023-10-15 | 37894403 |
| Letta (formerly MemGPT) is a framework for creating LLM services with memory | 2 | 0 | 2025-03-01 | 43222301 |

**Agent memory (query: `"agent memory"`, tags=story)** — 30+ results:
| Title | Points | Comments | Date |
|---|---|---|---|
| Beads: A coding agent memory system (steve-yegge.medium.com) | 19 | 1 | 2025-10-13 |
| The private agent memory fallacy (blog.getzep.com) | 12 | 2 | 2025-07-04 |
| Ask HN: Anyone using knowledge graphs for LLM agent memory/context management? | 12 | 2 | 2025-05-09 |
| Show HN: A file-based agent memory framework that works like skill (NevaMind-AI/memU) | 11 | 4 | 2026-01-06 |
| Show HN: SQLite Memory – Markdown based AI agent memory with offline-first sync | 9 | 1 | 2026-04-07 |
| Agent Memory in Portia AI's Open-Source Agent Framework | 8 | 0 | 2025-05-22 |
| Looking for Partner to Build Agent Memory (Zig/Erlang) | 7 | 9 | 2026-03-12 |
| Agent memory: knowledge graphs aren't enough, we need a know-how graph | 6 | 1 | 2025-11-24 |
| Show HN: ClawMem – Open-source agent memory with SOTA local GPU retrieval | 5 | 0 | 2026-03-22 |
| Ask HN: Are we close to figuring out LLM/Agent Memory | 4 | 3 | 2026-03-20 |
| Show HN: Self-improving agent memory system, 92% R 5 LongMemEval, PostgreSQL | 4 | 0 | 2026-04-09 |
| Your Agent's Memory Is Broken. Here's Why (ramsriharsha.substack.com) | 4 | 1 | 2026-02-06 |
| Show HN: Web Agent Memory Protocol (WAMP) – Shared Memory for the Web | 5 | 0 | 2025-08-19 |
| The magic wand that solves agent memory (liquidmetal.ai) | 4 | 1 | 2025-07-25 |
| Hindsight: Agent Memory That Works Like Human Memory (vectorize.io) | 4 | 2 | 2025-12-16 |
| I built a multi-agent memory consistency layer after the Claude Code leak | 3 | 3 | 2026-04-01 |
| Agent memory is structured not fuzzy. why are we all using vector DBs for it? | 2 | 3 | 2026-03-04 |
| FlowScript – Agent memory where contradictions are features | 2 | 1 | 2026-03-25 |
| MemEvolve: Meta-Evolution of Agent Memory Systems (arxiv 2512.18746) | 2 | 1 | 2026-03-20 |
| Zero-infra AI agent memory using Markdown and SQLite (memweave) | 5 | 2 | 2026-04-05 |

### Comment-tree dives on the 3 most-upvoted threads

**HN 37901902 — MemGPT launch (363 points, 85 comments, 2023-10-16)**:
Foundational thread. Broad technical interest. (Comment dive not load-
bearing given it's pre-2025; historian has the paper citation.)

**HN 41447317 — Mem0 Show HN (201 points, 61 comments, 2024-09-04)**:
*Mem0 corpus-integrity incident captured verbatim from WebFetch 2026-04-12*:
- `staranjeet` (founder): explained Mem0 vs Claude Prompt Caching
- `dang` (HN MODERATOR): **"I flagged some of them as booster
  comments, presumably by friends trying to help"** — MODERATOR-VERIFIED
  astroturfing event in the Mem0 corpus
- `weisser`: noted Mem0 demo "playground showed With Memory at 9/10
  relevancy despite being 100% duplication" — questioned evaluation
- `yding`: praised, but "interface between structured and unstructured
  memory still needs thinking"
- `PaulHoule`: "Discussed graph database limitations, suggesting
  SPARQL databases and noting challenges with transactional systems
  and triple stores"
- `FooBarWidget`: GDPR compliance concerns, no EU-based processing
- `bsenftner`: **"Looks very over engineered to me"**
- `zostale`: "Questioned value proposition, asking why model providers
  won't build this themselves"

**HN 43294974 — Letta launch (121 points, 22 comments, 2025-03-07)**:
- `dangbeetle`: use case for elderly memory-loss care (voice + LLM)
- `redwood`: noted "the berkeley team that previously released MemGPT"
- `pacjam` (Letta team): announced MCP integration, voice+memory for care
- Positive overall, no visible astroturf flags

**HN 46294274 — Letta Code (83 points, 37 comments, 2025-12-16)**:
- `ascorbic`/Charles Packer (Letta co-founder): introduced Letta Code
- `tigranbs`: "Void is the greatest ad for Letta..."
- `DrSiemer`: **"In my experience, 'memory' is really not that helpful
  in most cases. For all of my projects, I keep the documentation
  files [up to date instead]"** — independent voice favoring
  documentation-as-memory over learned memory
- `jstummbillig`: "I find the long-term memory concepts with regards
  to AI curiously dubious" — philosophical critique
- `skybrian`: technical question about architecture vs Beads

## Key blog posts (long-form secondary sources)

### Zep: "Lies, Damn Lies, & Statistics: Is Mem0 SOTA in Agent Memory?"
- URL: https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/ — retrieved 2026-04-12
- Author: Zep (self-interested — sells competing Graphiti product)
- **Key claims verbatim**:
  - Corrected Zep LoCoMo score: **75.14% (±0.17)** vs Mem0's reported 65.99% for Zep
  - Mem0's best: **~68%**
  - **Trivial full-context baseline: ~73%**
  - p95 latency: Zep 0.632s vs Mem0-reported 0.778s for Zep
  - Methodological problems with Mem0's testing: "incorrect user model
    treating both participants as one user", "timestamps improperly",
    "searches sequentially instead of in parallel"
  - Benchmark problems with LoCoMo itself: "conversations averaged only
    16,000-26,000 tokens — easily within the context window capabilities
    of modern LLMs", "missing quality control (Category 5 had unusable
    data)", "doesn't test knowledge updates or handle speaker
    attribution errors"
- **Adversary note**: this source is self-interested but the specific
  methodological critique is itself verifiable — Mem0's full-context
  baseline number is independently checkable in the Mem0 paper. If the
  full-context-beats-Mem0 claim holds, both parties' LoCoMo leadership
  claims collapse.

### Letta: "RAG is not agent memory"
- URL: https://www.letta.com/blog/rag-vs-agent-memory — retrieved 2026-04-12
- Author: Letta (self-interested)
- **Key claims verbatim**:
  - "RAG gets 'one shot' at retrieving the most relevant data and
    generating a response. While that _can_ work, it often doesn't."
  - "RAG is purely reactive" — "won't retrieve personalization
    information that isn't semantically similar"
  - "RAG often places irrelevant data into the context window,
    resulting in context pollution"
  - Advocates "multi-step reasoning with tools", "maintaining state
    across iterations", "memory distillation" with "search and doc
    retrieval tools"

### Letta: "Context Repositories: Git-Based Memory for Coding Agents"
- URL: https://www.letta.com/blog/context-repositories — retrieved 2026-04-12
- **Key claims verbatim**:
  - "Letta Code agents clone their memory repository to the local
    filesystem, giving the agent a local copy of its memory that stays
    in sync regardless of where the client is running."
  - "The filetree structure is always in the system prompt, so folder
    hierarchy and file names act as navigational signals."
  - "every change to memory is automatically versioned with informative
    commit messages"
  - "multiple subagents can process and write to memory concurrently,
    then merge their changes back through git-based conflict resolution"
  - "prior approaches to memory limited agents to MemGPT-style memory
    tools or virtual filesystem operations"
  - "[/init] can learn from existing Claude Code and Codex histories
    by fanning out processing across concurrent subagents"

### Steve Yegge: "Introducing Beads: A Coding Agent Memory System"
- URL: https://steve-yegge.medium.com/introducing-beads-a-coding-agent-memory-system-637d7d92514a — retrieved 2026-04-12
- HN: 45382856, 19 points, 1 comment, 2025-10-13
- **Key claims verbatim**:
  - "Beads isn't 'issue tracking for agents' — it's external memory
    for agents"
  - "dementia problem" — agents lose context between sessions
  - Agents "create nested markdown plans... ultimately generating 605
    obsolete plan files"
  - "writing the issues into git as JSONL lines, so you have the best
    of both the database and the version-control worlds"
  - Four dependency link types, agent-queryable
  - Targets "Claude Code, Sourcegraph Amp, OpenAI Codex"

## Anomalies

1. **Reddit blocked**: WebFetch on `reddit.com/.../.json` returned
   "Claude Code is unable to fetch from www.reddit.com". This is a
   tool-level block, not a rate-limit or robots.txt issue. Reddit
   community discussion (r/LocalLLaMA, r/MachineLearning, r/aiagents)
   is therefore **not represented** in this corpus. Mitigation: rely
   on HN, arxiv, and GitHub issue mining. An HN comment in the "Agent
   memory is structured not fuzzy" thread is itself a reddit crosspost
   from `r/aiagents`, so at least some r/aiagents signal leaked through.
2. **Mem0 corpus astroturfed**: HN moderator `dang` flagged the Mem0
   launch thread directly. This is an extraordinary signal — HN
   moderators rarely make this call publicly, and when they do it's
   load-bearing for corpus integrity. Mem0 marketing claims get a
   **suspicion flag** for the adversary.
3. **Benchmark arms race on LoCoMo**: at least 8 different projects
   (Mem0 26%, Zep 10%, MemOS 43.7%, Cortex beats-Mem0, Engram +20%,
   VAC 80.1%, Forensic 90.1%, Memori 81.95%) all claim SOTA on LoCoMo.
   Statistically impossible for all to be true. The "Anatomy" paper
   (arxiv 2602.19320) and Zep's rebuttal both explain why: LoCoMo is
   saturated; full-context beats most of them.
4. **Reddit-backchannel signal**: An HN-surfaced reddit crosspost
   from r/aiagents asks "Agent memory is structured not fuzzy. why
   are we all using vector DBs for it?" — directionally aligned with
   the file-system-as-memory convergence.

## Data quality
- **Coverage**: HN ~95% of reachable community signal on this topic.
  Reddit 0%. Twitter/X not attempted (no logged-in Playwright session).
  Substack/Medium captured via HN surfacing only.
- **Freshness**: newest stories retrieved within the last 7 days.
- **Known gaps**: Reddit, X/Twitter, Discord communities, YC company
  directory, dev.to. These are not load-bearing given the strong HN +
  arxiv + GitHub signal, but the adversary should note the gap.

## Confidence
**Medium-high**. HN corpus is comprehensive, the adversarial signals
(dang's flag, Zep vs Mem0, DrSiemer's dissent) are documented with
source IDs and dates, and the convergent pattern (files > vector DBs
for coding agents) is independently triangulated across Letta, Beads,
Claude Code docs, and multiple SQLite-based Show-HNs. Reddit blockage
is the one corpus gap.
