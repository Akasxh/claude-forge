# Linguist — vocabulary audit of agent-memory terminology

Sub-question: What do "episodic", "semantic", "procedural", "working",
"short-term", "long-term", "archival", "core", "hot", "cold", "context",
"memory" — plus the 2026 vocabulary ("MemCells", "MemCubes", "engram",
"playbook", "wings/halls/rooms", "context repository", "latent
briefing", "knowledge graph") — actually mean across the 2025-2026
literature? Which terms are polysemous? Which are marketing vs technical?

## Method
- Cross-walked the verbatim definitions from each system in
  `EVIDENCE/librarian.md` and `EVIDENCE/historian.md`.
- Flagged collisions where the same word means different things in
  different systems.
- Flagged terms where the marketing definition diverges from the
  technical definition.

## The big polysemy clusters

### "Memory" itself
The single most overloaded word in the corpus. Distinct senses:

| Sense | Used by | Means |
|---|---|---|
| **Persistent storage** | Mem0, Letta, Cognee, Memobase | "the place we put facts so the LLM can find them later" |
| **Active context window** | Anthropic ("Memory tool"), Claude Code Auto memory | "what's in the prompt at the moment" + "files that get re-injected" |
| **Parameter weights** | NVIDIA "context as training data", LoRA-as-memory | "what the model has internalized" |
| **KV cache state** | Latent Briefing, LatentMAS, LRAgent | "the latent representation of past tokens" |
| **Episodic trace** | EverMemOS, A-MEM, MAGMA | "discrete events with provenance" |
| **Playbook / lessons** | ACE, Akash's research team | "extracted strategies for what to do in similar situations" |

When Mem0 and Letta both say "stateful memory," they mean different
things — Mem0 means a hosted vector store, Letta means agent-directed
filesystem writes.

### "Episodic" vs "semantic"
Standard cog-sci usage (Tulving 1972): episodic = autobiographical
events with time/place; semantic = abstract knowledge. The corpus
mostly preserves this:

- **Episodic**: "events with time and provenance" (EverMemOS MemCells,
  MemoryBank traces, A-MEM zettelkasten notes, Generative Agents
  memory stream)
- **Semantic**: "extracted facts and concepts" (Mem0's extracted
  triples, Cognee's ontology, Graphiti's typed entities)

But there is one polysemy: **EverMemOS** uses "Semantic Consolidation"
to mean "organize episodic MemCells into thematic MemScenes" — i.e.
**the act of going from episodic to semantic**, not a layer called
"semantic" per se. The Engram-inspired lifecycle in EverMemOS is:
dialogue → MemCells (episodic) → Semantic Consolidation (process) →
MemScenes (semantic) → Reconstructive Recollection (retrieval).

### "Working memory"
Cog-sci definition: short-duration buffer for active manipulation
(Baddeley 1974). In the agent-memory corpus:

- **Memory in the Age of AI Agents** (arxiv 2512.13564): "working
  memory" = session-level transient state. Same as cog-sci.
- **LightMem** (arxiv 2604.07798): "short-term, mid-term, long-term"
  tiers — "short-term" maps to working memory in cog-sci sense.
- **MemGPT/Letta**: "core memory" plays the role of working memory
  (always in context, small, mutable). Letta does NOT use the term
  "working memory" — they use "core memory" and "archival memory."

So "working memory" is technically clean across the corpus, but the
**production systems prefer their own brand names**: core/recall/
archival (Letta), MEMORY.md/topic-files (Claude Code), MemCubes
(MemOS), wings/halls/rooms/closets/drawers (MemPalace).

### "Long-term" vs "archival"
Closely related terms:

- **MemGPT/Letta**: "archival memory" = vector-searchable persistent
  store (the cold tier)
- **Generative Agents** (Park et al. 2023): "long-term memory" / "memory
  stream" = persistent store of past observations
- **Mem0**: "long-term memory" = the hosted store, marketed as the
  product itself
- **Anthropic's Memory tool**: "memory" = persistent server-side store

**Polysemy alert**: "long-term memory" used as both (i) the technical
component (a persistent store) and (ii) the entire system being sold
(e.g. Mem0 "is a long-term memory layer"). The latter usage is
marketing-ese, the former is technical.

### "Knowledge graph" vs "memory graph"
- **Graphiti/Zep**: "temporal knowledge graph" = bi-temporal entities
  + relationships, validity windows
- **Cognee**: "knowledge graph for AI agent memory" = unified graph + vector
- **MAGMA**: "multi-graph agentic memory architecture" = 4 ORTHOGONAL
  graphs (semantic, temporal, causal, entity), not one graph
- **HippoRAG 2**: "OpenIE graph" + Personalized PageRank, no temporal
- **Mem0-g**: "graph-based memory representations to capture complex
  relational structures"

The **MAGMA innovation** is decomposing what others call "the knowledge
graph" into 4 orthogonal views with policy-guided traversal between
them. This is genuinely different — not a marketing rebrand.

### "Context engineering" vs "memory"
The ACE paper (arxiv 2510.04618) explicitly distinguishes them:

- **Context engineering** = "modifying inputs with instructions,
  strategies, or evidence, rather than weight updates"
- **Memory** = the special case of context engineering where the
  context evolves over time across sessions

Memory in the Age of AI Agents (arxiv 2512.13564) makes the same
distinction: "we begin by clearly delineating the scope of agent memory
and distinguishing it from related concepts such as LLM memory,
retrieval augmented generation (RAG), and context engineering."

In practice **Mem0/Zep/Letta marketers conflate** "context engineering"
and "memory" — they sell their products as "the context engineering
layer for your agent." Technically these are wider than memory, but
the slippage is mostly marketing not technical.

## New 2026 terms — what they actually denote

### "MemCubes" (MemOS, arxiv 2507.03724)
Verbatim from paper: "A MemCube encapsulates both memory content and
metadata such as provenance and versioning. MemCubes can be composed,
migrated, and fused over time, enabling flexible transitions between
memory types and bridging retrieval with parameter-based learning."

**What it actually is**: a typed unit-of-memory wrapper with metadata.
The novelty is that MemCubes can carry plaintext, activation
(latent), or parameter (weight) content, and the system knows how
to convert between them. Less hype, more abstraction.

### "MemCells / MemScenes" (EverMemOS, arxiv 2601.02163)
Verbatim: "Convert dialogue streams into discrete memory units
capturing episodic traces, atomic facts, and time-bounded Foresight
signals" (MemCells) and "organize MemCells into thematic MemScenes,
distilling semantic structures and refreshing user profiles."

**What they actually are**: MemCells = episodic events with metadata,
MemScenes = semantic clusters of related episodes. **The naming is
biology-inspired but the substance is the standard episodic→semantic
consolidation.** Not new conceptually, but the explicit lifecycle
(MemCells → Semantic Consolidation → MemScenes → Reconstructive
Recollection) is a useful frame.

### "Engram" (EverMemOS)
Verbatim: "engram-inspired lifecycle for computational memory."

**What it actually is**: a metaphor borrowed from neuroscience.
"Engram" in neuroscience = the physical trace of a memory in the
brain. In EverMemOS's usage, it's just "the persistent
representation we maintain across sessions." **Marketing-flavored
naming for a technical concept everyone else calls "memory item."**

### "Wings / halls / rooms / closets / drawers" (MemPalace)
The "method of loci" naming. Verbatim from MemPalace README:
- Wings = people or projects
- Rooms = topic-specific categories within wings
- Halls = connections between related rooms (typed: hall_facts, hall_events)
- Tunnels = cross-wing connections
- Closets = summary pointers to original content
- Drawers = raw verbatim original files

**What they actually are**: a hierarchical filesystem layout with
typed cross-references. Translated to standard terms:
- Wings = top-level namespaces
- Rooms = topic files
- Halls/Tunnels = symlinks or typed references
- Closets = compressed/summary version
- Drawers = the original
**The architecture is interesting; the naming is theatrical.** This
is what makes MemPalace simultaneously a real innovation and a
marketing exercise.

### "Latent Briefing" (Ramp Labs)
Per search-result extraction (X.com primary source paywalled):
"Latent Briefing is about efficient memory sharing for multi-agent
systems via KV cache compaction." The worker maintains a persistent
KV cache of the orchestrator's trajectory, compacted via
task-guided query vectors.

**What it actually is**: KV-cache-as-shared-memory between agents, with
a learned compaction step. Not a new mechanism — KV cache reuse has
been studied since 2023 — but the specific multi-agent framing
("brief" the worker via the cache, not via a prompt) is the
contribution. **"Briefing" is well-chosen as a verb: it captures
"compress the orchestrator's state into a form the worker can
ingest fast."**

### "Context Repository" (Letta, 2026-02-12)
Verbatim from www.letta.com/blog/context-repositories: "Letta Code
agents clone their memory repository to the local filesystem... every
change to memory is automatically versioned with informative commit
messages... multiple subagents can process and write to memory
concurrently, then merge their changes back through git-based
conflict resolution."

**What it actually is**: agent memory stored as a git repository on
the local filesystem. **This is new packaging for an old idea** (files
as memory has been around forever) but the explicit "git as the
versioning + conflict resolution layer" is non-trivial in agent
contexts and converges directly with what Akash already does
(filesystem-as-memory in `~/.claude/agent-memory/`).

### "Playbook" (ACE)
Verbatim from arxiv 2510.04618: "treats contexts as evolving playbooks
that accumulate, refine, and organize strategies through a modular
process of generation, reflection, and curation."

**What it actually is**: a structured prose document of strategies,
updated incrementally by a curator role to prevent brevity bias and
context collapse. **"Playbook" is a precise term**: it captures
"strategies for similar situations" better than "memory" or "notes."

## Marketing-flavored vs technically-precise terms

| Term | Source | Marketing? | Technically precise? |
|---|---|---|---|
| "memory layer" | Mem0, Zep, Cognee | yes | no — "layer" implies architecture, but is just a store |
| "stateful agent" | Letta | partial | yes — captures the architectural distinction from stateless |
| "long-term memory" | everyone | partial | yes when contrasted with "session context" |
| "playbook" | ACE | no | yes — precise |
| "MemCube" | MemOS | yes | partially — captures the typed-content abstraction |
| "MemCells / MemScenes / Engram" | EverMemOS | yes | partially — biology metaphors for ordinary concepts |
| "wings / halls / rooms / drawers" | MemPalace | yes | yes — internally consistent hierarchy |
| "latent briefing" | Ramp Labs | no | yes — precise verb for the KV-cache-handoff operation |
| "context repository" | Letta | no | yes — git repo of agent state, literal |
| "knowledge graph" | Graphiti, Cognee, MAGMA | partial | yes when properly typed |
| "multi-graph" | MAGMA | no | yes — 4 orthogonal graphs is a real distinction |
| "consolidation" | EverMemOS, others | no | yes — borrowed cleanly from cog-sci |
| "reconstructive recollection" | EverMemOS | yes | yes — precise but florid |
| "context engineering" | ACE, broad | no | yes — wider than memory; ACE is precise about it |

## Cross-system rename equivalences

For the moderator and synthesist, here are the same concepts under
different brand names. These are NOT contradictions — they are
vocabulary mismatches:

| Concept | Letta | Claude Code | ACE | EverMemOS | MemPalace |
|---|---|---|---|---|---|
| Always-in-context | core memory | injected MEMORY.md (top 25KB) | playbook (current state) | active MemScenes | wings index |
| On-demand store | archival | topic files | (out of scope, ACE doesn't separate) | MemCells store | rooms/closets/drawers |
| Write decision | LLM tool calls | LLM Edit tool calls | reflector role | semantic consolidation | (depends on mode) |
| Curator | LLM (self) | LLM (self) | curator role | (implicit) | (none stated) |
| Provenance | git auto-commits | filesystem mtime | playbook diffs | engram lifecycle | drawer originals |

## Handoff to moderator
**No load-bearing contradictions in vocabulary alone.** The Mem0
vs Zep dispute is NOT a vocabulary issue — it's a benchmark
methodology issue. The "is graph-based memory better than vector-
based?" debate is NOT a vocabulary issue either — both sides agree
what graph and vector mean.

The two vocabulary misuses worth flagging are:
1. Mem0/Zep/Cognee marketing the word "memory layer" as if it
   denotes a single architectural pattern when it actually denotes
   "any persistent store the agent reads from." The skeptic should
   be alert when a recommendation collapses different approaches
   under "memory layer" — they're not interchangeable.
2. MemPalace's wings/halls/rooms naming is genuinely consistent
   internally but reads as theatrical and obscures that the
   underlying architecture is a hierarchical filesystem with typed
   refs. The adversary should flag this as a marketing-by-naming
   move.

## Confidence
**High**. Vocabulary audit is straightforward when grounded in
verbatim quotes from primary sources. Every term defined above
traces to a librarian/historian quote with retrieval date.
