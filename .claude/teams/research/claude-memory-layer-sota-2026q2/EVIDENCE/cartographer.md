# Cartographer — map of Claude Code's current memory mechanism + position in the taxonomy

Sub-question: What does Claude Code's `memory: user` + `~/.claude/agent-memory/`
mechanism actually do? What are its real limits? Where does it sit in the
"Memory in the Age of AI Agents" three-axis taxonomy? Where does Latent
Briefing sit? Where does the team's Research-Lead playbook sit?

## Method
- Fetched the full official docs at `https://code.claude.com/docs/en/memory`
  (verbatim, retrieved 2026-04-12).
- Cross-referenced with Akash's installed setup at `~/.claude/agent-memory/`,
  `~/.claude/agents/research/`, and `~/.claude/teams/research/PROTOCOL.md`.
- Mapped each mechanism into the Memory-in-the-Age-of-AI-Agents 3-axis
  framework (forms × functions × dynamics) so the recommendation has a
  coherent structural frame.

## What Claude Code actually has, today

### Two memory mechanisms, one architecture

Per the official docs, Claude Code has **two** memory mechanisms that
both inject at session start:

| Mechanism | Who writes | Loaded into | Purpose |
|---|---|---|---|
| `CLAUDE.md` files | the human | every session, **in full** | persistent instructions, project conventions |
| Auto memory (`MEMORY.md`) | Claude itself | every session, **first 200 lines / 25KB whichever first** | learnings, patterns, build commands, debugging insights |

The 25KB ceiling is **only** on auto memory. CLAUDE.md is loaded in
full, with a docs-recommended soft target of "under 200 lines" for
adherence quality but no hard cap.

> "The first 200 lines of `MEMORY.md`, or the first 25KB, whichever
> comes first, are loaded at the start of every conversation. Content
> beyond that threshold is not loaded at session start. Claude keeps
> `MEMORY.md` concise by moving detailed notes into separate topic
> files." — code.claude.com/docs/en/memory § "How it works", retrieved
> 2026-04-12.

> "This limit applies only to `MEMORY.md`. CLAUDE.md files are loaded
> in full regardless of length, though shorter files produce better
> adherence." — same source

### Topic files: the on-demand cold tier

The single most important piece of structural information v1 missed
about Claude Code memory: **topic files exist and are read on demand
by Claude's standard file tools**. This effectively gives Claude Code
a primitive but real two-tier memory:

> "Topic files like `debugging.md` or `patterns.md` are not loaded at
> startup. Claude reads them on demand using its standard file tools
> when it needs the information." — same source

The directory layout for auto memory is:

```
~/.claude/projects/<project>/memory/
├── MEMORY.md          # concise index, loaded into every session (25KB)
├── debugging.md       # detailed notes, on-demand
├── api-conventions.md
└── ...
```

`MEMORY.md` is **literally an index**. Claude reads and writes files in
the directory throughout the session, using `MEMORY.md` to keep track
of what's stored where. This is a **navigable filesystem with an
LLM-curated table of contents**, not a flat blob.

### Subagent memory: the same primitive, scoped per agent

Per `code.claude.com/docs/en/sub-agents` § "Enable persistent memory":

```
User scope:    ~/.claude/agent-memory/<agent-name>/
Project scope: .claude/agent-memory/<agent-name>/
Local scope:   .claude/agent-memory-local/<agent-name>/
```

Each subagent gets its own MEMORY.md + topic files at its scope. The
frontmatter field is `memory: user` (or `project` / `local`).

Akash's installed setup uses this:
- `~/.claude/agent-memory/research-lead/MEMORY.md` — 7,260 bytes,
  7 lessons, written by `research-retrospector`, deduped by
  `research-scribe`. Read at session start by research-lead.
- `~/.claude/agent-memory/research-retrospector/MEMORY.md` — meta-lessons
- `~/.claude/agent-memory/architect-planner/MEMORY.md` — present, planner team

### What survives `/compact`

Per the docs § "Instructions seem lost after /compact":

> "Project-root CLAUDE.md survives compaction: after `/compact`,
> Claude re-reads it from disk and re-injects it into the session.
> Nested CLAUDE.md files in subdirectories are not re-injected
> automatically; they reload the next time Claude reads a file in
> that subdirectory."

This is a load-bearing behavior for any session-spanning memory
strategy: the root index always survives, the leaves don't.

## The limits Akash actually faces (corrected from v1)

| v1 claimed limit | Actual limit (per docs) | Implication |
|---|---|---|
| 25KB hard ceiling | 25KB only on `MEMORY.md` index; topic files unbounded | No ceiling on cold-tier knowledge, only on hot-tier index |
| 200 lines limit | 200 lines on `MEMORY.md`, recommended 200 for `CLAUDE.md` | Same — applies to the index, not the topic files |
| No vector search | No native vector search | True, but topic-file navigation via filename + content scan partially substitutes |
| No graph | No native graph | True; would need an external layer if the recommendation requires one |
| No temporal queries | No native temporal queries | True; but `git log` over an auto-memory git repo gives bi-temporal validity for free |
| No cross-agent sharing | True — each subagent has its own `agent-memory/<name>/` scope | This is the gap Latent Briefing addresses for parametric/latent forms |
| No forgetting calibration | True | Akash would have to bolt on |
| No contradiction detection | True | The Anatomy paper says nobody else really does this either, despite claims |

## Position in the Memory-in-the-Age-of-AI-Agents 3-axis taxonomy

The arxiv 2512.13564 taxonomy (47-author survey, retrieved 2026-04-12)
is the structural frame Akash's brief explicitly demands. The three axes:

1. **Forms** (storage substrate): token-level, parametric, latent
2. **Functions** (purpose): factual, experiential, working
3. **Dynamics** (lifecycle): formation, evolution, retrieval

### Where Claude Code's existing mechanism sits

| Axis | Claude Code today | Notes |
|---|---|---|
| Form | **Token-level** (markdown text) | No parametric (no fine-tuning at memory write), no latent (no KV-cache reuse) |
| Function | **Experiential** primarily (durable lessons, build commands, patterns), some **factual** (project layout, conventions) | Pure experiential when written by retrospector; pure factual when human authors a CLAUDE.md |
| Dynamics — Formation | LLM-decided ("Claude decides what's worth remembering") | Implicit reflection at the agent level |
| Dynamics — Evolution | Curator (research-scribe in Akash's case) dedupes/compresses | The ACE curator pattern |
| Dynamics — Retrieval | Index-then-navigate (MEMORY.md as ToC, topic files on demand) | Filesystem-native, LLM-driven |

This places Claude Code's existing setup **squarely in the
token-level/experiential cell**, with all three dynamics covered by
the LLM's own behavior + Akash's retrospector/scribe pair. **It is
already a working ACE (arxiv 2510.04618) implementation** —
generation/reflection/curation realized as research-lead /
research-retrospector / research-scribe.

### The cells Claude Code does NOT cover

| Cell | Status | Could matter for Akash? |
|---|---|---|
| **Token-level / factual** | partially covered (CLAUDE.md, project files) | YES — for entity-rich domain knowledge that doesn't fit "lessons" form |
| **Token-level / working** | covered by Claude Code's session context window | already handled |
| **Parametric / any** | not covered | YES eventually — fine-tuning a small model on the curated MEMORY.md is the test-time-learning frontier (NVIDIA "Context as Training Data") |
| **Latent / factual** | not covered | maybe — for Akash's single-user case, low priority |
| **Latent / experiential** | not covered | YES when multi-agent teams grow beyond ~5 specialists in parallel, because token-level message-passing is the bottleneck Latent Briefing (Ramp Labs) and LatentMAS (arxiv 2511.20639) attack |
| **Latent / working** | not covered | hardware-level, vLLM territory |

### Where Latent Briefing sits in the taxonomy

Per Ramp Labs' description (relayed via WebSearch 2026-04-12, X.com
primary source paywalled): the worker maintains a **persistent KV cache
of the orchestrator's trajectory across calls**. Compaction finds a
compact KV cache of size t < S that produces nearly identical attention
outputs. Task-guided query vectors prioritize information relevant to
the worker's task.

| Axis | Latent Briefing |
|---|---|
| Form | **Latent** (KV-cache, hidden state) |
| Function | **Experiential** (orchestrator's trajectory, mid-task working state) |
| Dynamics — Formation | Triggered by orchestrator handoff |
| Dynamics — Evolution | Compaction step (1.7s, ~20× faster than sequential attention matching, 10-30× faster than LLM summarization) |
| Dynamics — Retrieval | Implicit — the cache IS the retrieval, no token-level lookup |

This is **fundamentally different** from Mem0/Zep/Letta, all of which
operate in the token-level form. Latent Briefing attacks the
**inter-agent context-passing bottleneck**, not the persistence
problem. The relevant analog open-source paper is **LatentMAS** (arxiv
2511.20639, Gen-Verse/LatentMAS, retrieved 2026-04-12) which reports
"up to 14.6% accuracy improvement across 9 benchmarks, 70.8%-83.7%
fewer output tokens, 4×-4.3× faster inference" via shared latent
working memory.

### The full grid: where every system sits

| | Token-level | Parametric | Latent |
|---|---|---|---|
| **Factual** | RAG, Mem0 (vector), Memori, MemX, Cognee, Graphiti (KG) | fine-tuning, NVIDIA "context as training data" | KV-cache for facts (rare, mostly research) |
| **Experiential** | **ACE (Stanford), MemGPT/Letta, A-MEM, EverMemOS, MAGMA, Claude Code MEMORY.md** | learned policies, MemSkill | **Latent Briefing (Ramp), LatentMAS, LRAgent** |
| **Working** | session context window | n/a (working = transient) | KV cache for current session |

The clusters:
- **Token/factual cluster** is the noisiest — Mem0, Zep, Cognee, Memori,
  HippoRAG, MemOS all live here, all with conflicting benchmark claims.
- **Token/experiential cluster** is where Akash already lives, and
  where ACE/MemGPT/A-MEM/EverMemOS/MAGMA/Claude Code converge.
- **Latent/experiential cluster** is the new frontier (2025-2026) that
  attacks multi-agent context cost directly.

## Architectural observations for the recommendation

1. **Claude Code's existing mechanism is a working ACE implementation
   in the token/experiential cell.** The retrospector/scribe pair in
   Akash's research team is literally what the ACE paper calls
   "reflector" and "curator." The research-lead is the "generator-
   consumer." H1 from `HYPOTHESES.md` is therefore already validated.
2. **The 25KB ceiling is misframed as a problem.** It is a ceiling on
   the hot-tier index, not on total memory. Topic files give an
   unbounded cold tier accessed via filesystem read tools. The thing
   that needs to extend Claude Code is not "more bytes in MEMORY.md"
   — it is **better cold-tier organization** (better topic-file
   structure) and possibly **a parallel store optimized for
   factual/entity recall** (the cell Claude Code's experiential
   storage doesn't handle natively).
3. **Cross-agent sharing is the next bottleneck.** Akash already has
   17 specialists in his Research Team. Today they share through
   files (the workspace under `.claude/teams/research/<slug>/`). This
   works because the team is small and synchronous. As teams grow
   wide (10+ parallel), token-level message-passing across them
   becomes the cost bottleneck — exactly what Latent Briefing /
   LatentMAS / LRAgent attack at the latent layer. This is
   non-trivial to integrate with Claude Code's runtime (which is a
   black box at the hosted-API layer), but worth tracking.
4. **Git over the auto-memory directory gives bi-temporal validity
   for free.** Letta's "Context Repositories" blog (2026-02-12)
   makes this point explicitly: "every change to memory is automatically
   versioned with informative commit messages." Bi-temporal validity
   ("when did we believe this; when did it stop being true") is the
   feature Graphiti charges a graph database to provide. `git log` on
   `~/.claude/agent-memory/research-lead/` provides the same thing for
   free, with the LLM as the consumer of the history.

## Confidence
**High**. The Claude Code memory mechanism is documented in primary
sources (verbatim quoted), Akash's installed setup is verifiable on
disk, the taxonomy frame is from the canonical 2512.13564 survey,
and the Latent Briefing taxonomy placement is supported by multiple
converging public sources (search results + LatentMAS arxiv +
LRAgent arxiv as related work).

## Handoff to tracer
- The "what happens at the moment Claude decides to remember something"
  question is the next chain. Tracer: walk the runtime path from
  trigger → decision → write → retrieve → inject for both Claude Code's
  Auto memory mechanism and the MemGPT self-edit loop, and propose
  where in Akash's setup an extension hook would go.
