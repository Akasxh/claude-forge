# Librarian — official docs for production memory systems

Sub-question: What does each production agent-memory system *actually*
document, versus what it *claims*, as of 2026-04-12? Version, API,
backends, license, self-hosted support, recommended usage.

## Scope and method

Docs pulled via WebFetch on the canonical README/homepage of each
system, cross-referenced against GitHub's latest release tag (see
`EVIDENCE/github-miner.md` for the version ground truth). Claude Code's
memory mechanism pulled from `https://code.claude.com/docs/en/memory`
and `https://code.claude.com/docs/en/sub-agents`, all retrieved
2026-04-12.

## System inventory

### 1. Claude Code — Auto memory + CLAUDE.md (v2.1.59+)
- **Primary URL**: https://code.claude.com/docs/en/memory — retrieved 2026-04-12
- **Docs verbatim** (§ "How it works"):
  > "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes
  > first, are loaded at the start of every conversation. Content beyond
  > that threshold is not loaded at session start. Claude keeps `MEMORY.md`
  > concise by moving detailed notes into separate topic files. This limit
  > applies only to `MEMORY.md`. CLAUDE.md files are loaded in full regardless
  > of length, though shorter files produce better adherence. Topic files like
  > `debugging.md` or `patterns.md` are not loaded at startup. Claude reads
  > them on demand using its standard file tools when it needs the information."
- **Two mechanisms** (§ "CLAUDE.md vs auto memory"):
  1. **CLAUDE.md files**: user-authored, loaded in full at session start
  2. **Auto memory**: Claude-authored, per-project, two-tier (hot index +
     cold topic files)
- **Storage location**:
  - Session-level project auto-memory: `~/.claude/projects/<project>/memory/MEMORY.md`
  - Subagent user scope: `~/.claude/agent-memory/<name-of-agent>/`
  - Subagent project scope: `.claude/agent-memory/<name-of-agent>/`
  - Subagent local scope: `.claude/agent-memory-local/<name-of-agent>/`
  (retrieved https://code.claude.com/docs/en/sub-agents § "Enable persistent memory", 2026-04-12)
- **Version**: Auto memory requires Claude Code ≥ 2.1.59 (docs retrieved 2026-04-12)
- **License**: Proprietary (Claude Code client), MEMORY.md files are
  user-owned markdown
- **Key primitive**: Two-tier memory — `MEMORY.md` as hot index under
  25KB, arbitrary topic files under it, read on demand by Claude's
  own file tools. The LLM curates its own index.
- **Installed-code cross-check**: Akash's own `~/.claude/agent-memory/research-lead/MEMORY.md`
  already uses this pattern — 7260 bytes, 7 durable lessons seeded by
  the retrospector (verified by direct read during this session).
- **Critical correction to my own prior assumption**: I assumed the
  Claude Code memory story is "25KB flat ceiling, no vector search, no
  topic files." This was wrong. The 25KB/200-line limit applies only
  to the *index*. Arbitrary topic files can exist alongside it and are
  read on demand. This is effectively a primitive vector-less
  retrieval layer over files — not semantic, but LLM-curated.
- **Confidence**: high (primary source, official docs)

### 2. Mem0 — `mem0ai/mem0`
- **Primary URL**: https://github.com/mem0ai/mem0 — retrieved 2026-04-12
- **Description**: "Universal memory layer for AI Agents"
- **Latest release**: `cli-node-v0.2.3` (2026-04-11) — 52,673 stars, Apache-2.0
- **Architecture** (from `EVIDENCE/historian.md § 1`, the published paper
  arxiv 2504.19413 "Mem0: Building Production-Ready AI Agents with
  Scalable Long-Term Memory", Chhikara et al., 2025-04-28):
  > "Mem0, a scalable memory-centric architecture that addresses this
  > issue by dynamically extracting, consolidating, and retrieving
  > salient information from ongoing conversations... we further propose
  > an enhanced variant [Mem0-g] that leverages graph-based memory
  > representations to capture complex relational structures among
  > conversational elements."
- **Install**: `pip install mem0ai` / `npm install mem0ai` / hosted
- **Backends**: OpenAI default (`gpt-4.1-nano-2025-04-14`), vector store
  unspecified in README (must consult extended docs)
- **Benchmark claim** (from official homepage, retrieved 2026-04-12):
  > "+26% Accuracy vs. OpenAI Memory • 91% Faster • 90% Fewer Tokens"
  on LOCOMO.
- **Corpus capture flag** (handoff to adversary):
  - HN moderator `dang` **publicly flagged** some positive comments on
    the Mem0 Show HN as "booster comments, presumably by friends trying
    to help" (HN thread 41447317, retrieved 2026-04-12 via Algolia). This
    is a moderator-verified case of community-corpus manipulation. The
    adversary must audit.
  - Zep published a rebuttal "Lies, Damn Lies & Statistics: Is Mem0 SOTA
    in Agent Memory?" (https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/,
    retrieved 2026-04-12) — see § `adversary: please verify`.
- **Confidence**: medium (docs verified, benchmarks contested)

### 3. Letta (formerly MemGPT) — `letta-ai/letta`
- **Primary URL**: https://github.com/letta-ai/letta — retrieved 2026-04-12
- **Latest release**: `0.16.7` (2026-03-31) — 22,002 stars, Apache-2.0
- **Description** (from GitHub): "Letta is the platform for building
  stateful agents: AI with advanced memory that can learn and self-
  improve over time."
- **Rebranding lineage**: Letta was MemGPT (arxiv 2310.08560, Packer et
  al., UC Berkeley, 2023-10-12), rebranded to Letta in 2024.
- **Install**:
  - CLI: `npm install -g @letta-ai/letta-code` (requires Node 18+)
  - Client (Python): `pip install letta-client`
  - Client (TS): `npm install @letta-ai/letta-client`
- **Architectural primitive** (from MemGPT paper § 3): core memory
  (always in context, small, LLM-editable via tool calls) + recall memory
  (conversation history) + archival memory (vector-searchable, LLM-
  searchable via tool calls). The LLM itself calls `memory_insert`,
  `memory_replace`, `memory_search` tools; memory operations are agent-
  directed, not externally managed.
- **2026 pivot**: Letta has pivoted hard toward coding agents. Post
  series in Dec 2025-Apr 2026:
  - "Letta Code: a memory-first coding agent" (2025-12-16, HN 46294274)
  - "Context Repositories: Git-Based Memory for Coding Agents"
    (https://www.letta.com/blog/context-repositories, 2026-02-12, retrieved 2026-04-12)
  - "Our Next Phase" (2026-03-16, HN 47406067)
  - "The Letta Code App" (2026-04-10, HN 47718214)
- **Context Repositories architecture** (verbatim from blog, retrieved
  2026-04-12):
  > "Letta Code agents clone their memory repository to the local
  > filesystem, giving the agent a local copy of its memory that stays
  > in sync regardless of where the client is running."
  > "The filetree structure is always in the system prompt, so folder
  > hierarchy and file names act as navigational signals."
  > "every change to memory is automatically versioned with informative
  > commit messages."
  > "multiple subagents can process and write to memory concurrently,
  > then merge their changes back through git-based conflict resolution."
  > "[prior approaches] limited agents to MemGPT-style memory tools or
  > virtual filesystem operations."
  > "[/init] can learn from existing Claude Code and Codex histories by
  > fanning out processing across concurrent subagents."
- **Local-first**: yes, `letta-code` runs locally; Letta Cloud is a
  separate hosted API option.
- **Confidence**: high (primary source, recent, actively maintained)

### 4. Zep + Graphiti — `getzep/zep` + `getzep/graphiti`
- **Primary URLs**:
  - https://github.com/getzep/zep — retrieved 2026-04-12 (4,403 stars,
    last release Sep 2025; the product has mostly moved upstream to
    Graphiti)
  - https://github.com/getzep/graphiti — retrieved 2026-04-12 (24,786 stars,
    Apache-2.0, latest release `mcp-v1.0.2` 2026-03-11)
- **Description** (Graphiti): "Build Real-Time Knowledge Graphs for AI Agents"
- **Architectural primitive — bi-temporal knowledge graph** (verbatim):
  > "each fact in a context graph has a validity window: when it became
  > true, and when (if ever) it was superseded."
- **Backends**: Neo4j (≥ 5.26), FalkorDB (≥ 1.1.2), Kuzu (≥ 0.11.2),
  Amazon Neptune
- **Install**: `pip install graphiti-core` + Docker Compose for Neo4j/FalkorDB
- **Local-first**: "self-hosted only" per the Zep-vs-Graphiti comparison.
  Graphiti runs on your own graph DB.
- **Benchmark claim** (from Zep's rebuttal to Mem0, see Mem0 entry):
  - Zep corrected LoCoMo score: **75.14% (±0.17)**
  - Mem0's best: ~**68%**
  - Trivial full-context baseline: **~73%**
  - Zep p95 latency: 0.632s
- **Confidence**: high (primary source), medium on benchmark (self-
  interested; adversary must audit)

### 5. MemOS (MemTensor) — `MemTensor/MemOS`
- **Primary URL**: https://github.com/MemTensor/MemOS — retrieved 2026-04-12
- **Latest release**: `v2.0.13` (2026-04-10) — 8,293 stars, Apache-2.0,
  created 2025-07-06
- **Description**: "AI memory OS for LLM and Agent systems, enabling
  persistent Skill memory for cross-task skill reuse and evolution"
- **Paper**: arxiv 2507.03724 "MemOS: A Memory OS for AI System", Li et
  al., 2025-07 (preview), Dec 2025 v2.0 "Stardust" full release
- **Three memory types** (verbatim from paper abstract, retrieved 2026-04-12):
  > "plaintext, activation-based, and parameter-level memories"
- **MemCube primitive** (verbatim):
  > "A MemCube encapsulates both memory content and metadata such as
  > provenance and versioning. MemCubes can be composed, migrated, and
  > fused over time, enabling flexible transitions between memory types
  > and bridging retrieval with parameter-based learning."
- **Benchmark claim** (from README, retrieved 2026-04-12):
  > "+43.70% Accuracy vs. OpenAI Memory"
  > "LoCoMo 75.80 • LongMemEval +40.43% • PrefEval-10 +2568% • PersonaMem +40.75%"
- **Local plugin** (100% on-device, verbatim):
  > "Zero cloud dependency — all data stays on your machine, persistent
  > local SQLite storage" · "FTS5 + vector search, auto task summarization,
  > reusable skills that self-upgrade"
- **Backends supported**: OpenAI, Azure OpenAI, Qwen (DashScope), DeepSeek,
  MiniMax, Ollama, HuggingFace, vLLM; Neo4j + Qdrant for storage
- **Install** (self-hosted local, verbatim):
  ```bash
  git clone https://github.com/MemTensor/MemOS.git
  cd MemOS && pip install -r ./docker/requirements.txt
  cd docker && docker compose up
  ```
- **Confidence**: medium (primary source + recent release, benchmark
  claim bigger than Mem0's — must go through adversary; also Chinese-
  lab origin which is not inherently suspicious but warrants cross-check)

### 6. Cognee — `topoteretes/cognee`
- **Primary URL**: https://github.com/topoteretes/cognee — retrieved 2026-04-12
- **Latest release**: `v1.0.0` (2026-04-11) — 15,117 stars, Apache-2.0
- **Description**: "Knowledge Engine for AI Agent Memory in 6 lines of code"
- **Architecture** (verbatim):
  > "unified ingestion, graph/vector search, runs locally, ontology
  > grounding, multimodal"
- **Core operations** (verbatim):
  - `remember` — "Store permanently in the knowledge graph (runs add +
    cognify + improve)"
  - `recall` — query with auto-routing
  - `forget` — delete
  - `improve` — feedback-based learning
- **Install**: `uv pip install cognee`
- **Local-first**: yes, but also offers Cognee Cloud; deploys to Modal,
  Railway, Fly.io, Render, Daytona
- **Benchmark claim**: none explicit in README (flag: suspicious absence
  given the competitive space)
- **Confidence**: medium-high (primary source, actively maintained, just
  hit v1.0)

### 7. LangMem — `langchain-ai/langmem`
- **Primary URL**: https://github.com/langchain-ai/langmem — retrieved 2026-04-12
- **Latest release**: none (no releases published) — 1,390 stars, MIT,
  created 2025-01-21, latest commit 2026-04-10
- **Description** (from README): "agents learn and adapt from their
  interactions over time" via "tooling to extract important information
  from conversations, optimize agent behavior through prompt refinement,
  and maintain long-term memory."
- **Install**: `pip install -U langmem`
- **Core API**:
  - `create_manage_memory_tool` — LLM tool for writing memory
  - `create_search_memory_tool` — LLM tool for reading memory
- **Backend**: `InMemoryStore` for dev; "use AsyncPostgresStore or
  similar DB-backed store to persist memories across server restarts"
  for prod. Native integration with LangGraph's storage layer.
- **License**: MIT
- **Benchmark claim**: none
- **Confidence**: medium (primary source but smaller footprint; no
  releases + small star count signal early-stage)

### 8. A-MEM — `agiresearch/A-mem`
- **Primary URL**: https://github.com/agiresearch/A-mem — retrieved 2026-04-12
- **Stars**: 961, MIT, created 2025-02-25, last push 2025-12-12
- **Paper**: arxiv 2502.12110 "A-MEM: Agentic Memory for LLM Agents",
  Xu et al., 2025-02-17
- **Architecture** (verbatim):
  > "Zettelkasten method... dynamic indexing and linking... each new
  > memory generates a comprehensive note containing multiple structured
  > attributes, including contextual descriptions, keywords, and tags...
  > memory evolution — as new memories are integrated, they can trigger
  > updates to the contextual representations and attributes of existing
  > historical memories"
- **Confidence**: high (paper + reference impl)

### 9. Memobase — `memodb-io/memobase`
- **Primary URL**: https://github.com/memodb-io/memobase — retrieved 2026-04-12
- **Stars**: 2,673, Apache-2.0, created 2024-09-03
- **Description**: "User Profile-Based Long-Term Memory for AI Chatbot Applications"
- **Confidence**: medium (mid-tier signal, profile-focused, not a
  general memory layer)

### 10. Memary — `kingjulio8238/Memary` (DORMANT)
- **Primary URL**: https://github.com/kingjulio8238/Memary — retrieved 2026-04-12
- **Last release**: `v0.1.5` (2024-10-22). **Last push: 2024-10-22.**
- **Status**: **DORMANT**. Not maintained.
- **Confidence**: high on dormancy (18+ months since last push as of 2026-04)

### 11. HippoRAG 2 — `OSU-NLP-Group/HippoRAG`
- **Primary URL**: https://github.com/OSU-NLP-Group/HippoRAG — retrieved 2026-04-12
- **Stars**: 3,348, MIT, last release v1.0.0 (2025-02-27), last push 2025-09-04
- **Venue**: NeurIPS 2024 (HippoRAG) + ICML 2025 (HippoRAG 2, arxiv 2502.14802)
- **Architecture primitive**: Personalized PageRank over an open-
  information-extraction graph, LLM-driven online indexing
- **Benchmark claim** (paper abstract, retrieved 2026-04-12):
  > "7% improvement in associative memory tasks over the state-of-the-art
  > embedding model while also exhibiting superior factual knowledge and
  > sense-making memory capabilities"
- **Confidence**: high (peer-reviewed venue, modest claim, reproducible)

## Version caveats
- Mem0's `gpt-4.1-nano-2025-04-14` default assumes OpenAI as backend,
  which is not local-first.
- Letta 0.16.x is the current major line; the framework + `letta-code`
  CLI are separate packages.
- MemOS v2.0 "Stardust" (Dec 2025) introduced knowledge-base and
  multi-modal memory; v1.0 "Stellar" (Jul 2025) was preview.
- Graphiti: the Zep brand is mostly on the Graphiti repo now, not the
  `zep` repo (which hasn't had a release since Sep 2025).

## Installed-code cross-check
Akash's own `~/.claude/agent-memory/research-lead/MEMORY.md` (7260 bytes,
read at session start) demonstrates that Claude Code's subagent-memory
mechanism *already works as documented*: I, the research-lead subagent,
am reading it right now as behavioral context. The 7 seeded lessons are
present in the `MEMORY.md` file verbatim and are being applied to
dispatch decisions this session.

## Confidence
**High**. Every claim above is backed by a primary URL retrieved
2026-04-12 with verbatim quotes where load-bearing. The two areas of
uncertainty (Mem0 benchmark, MemOS benchmark) are flagged for the
adversary gate.
