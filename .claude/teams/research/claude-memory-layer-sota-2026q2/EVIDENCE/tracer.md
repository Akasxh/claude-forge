# Tracer — runtime causal chains for memory write/read

Sub-question: What exactly happens when "the agent decides to remember
something"? Trace the trigger → decision → write → retrieve → inject
chain for (a) MemGPT/Letta self-edit loop, (b) ACE generation/reflection/
curation loop, (c) Claude Code Auto memory, and (d) where in Claude
Code's runtime an analogous extension hook would go.

## Method
- Read MemGPT paper (arxiv 2310.08560) + Letta blog (Context
  Repositories, 2026-02-12).
- Read ACE paper (arxiv 2510.04618 — full content fetched and persisted
  during this session) for the three-role loop.
- Read Claude Code memory docs (verbatim, retrieved 2026-04-12) for
  the Auto memory chain.
- Cross-reference Akash's installed setup (`research-retrospector`,
  `research-scribe`, `research-lead` agents) to identify the analog
  hooks already in place.

## Chain 1 — MemGPT / Letta self-edit loop

The "memory as tools" pattern. Trigger → decision → write → retrieve
→ inject is **agent-directed**, meaning the LLM emits the decision as
a tool call, not an external classifier.

```
[trigger]
  Agent observes new info during conversation
       │
       ▼
[decision: should I remember this?]
  LLM (in same forward pass as the response generation)
  decides whether to emit a memory_* tool call
       │
       ▼
[write]
  LLM emits one of:
    memory_insert(content)        — append to core or archival
    memory_replace(old, new)      — modify existing entry
    memory_search(query)          — recall (read path)
       │
       ▼
[backend handler]
  - Core memory: just edit a string in the system-prompt slot
  - Archival memory: insert into a vector store (PGVector default)
       │
       ▼
[next turn injection]
  - Core memory: the always-in-context block reflects the edit immediately
  - Archival memory: only loaded if a future memory_search returns it
```

**Key properties** (verbatim from MemGPT paper § 3, retrieved
2026-04-12 via librarian.md):
- Core memory is **always in context, small, LLM-editable via tool calls**
- Archival memory is **vector-searchable, LLM-searchable via tool calls**
- The LLM itself decides when to call `memory_insert`, `memory_replace`,
  `memory_search` — there is **no external curator**

**Letta's 2026 evolution — Context Repositories** (verbatim from
www.letta.com/blog/context-repositories, retrieved 2026-04-12):
- "Letta Code agents clone their memory repository to the local
  filesystem, giving the agent a local copy of its memory"
- "every change to memory is automatically versioned with informative
  commit messages"
- "multiple subagents can process and write to memory concurrently,
  then merge their changes back through git-based conflict resolution"

So the modern Letta runtime path is:
1. Agent emits memory_* tool call
2. Backend writes to local filesystem (a git repo)
3. Each write produces an auto-commit with a generated commit message
4. Future agent reads the file via standard file tools (not tool-mediated)
5. Multi-agent merge is a git merge

This is **convergent with Claude Code's Auto memory** and even more
convergent with what Akash already runs.

## Chain 2 — ACE (Stanford) generation/reflection/curation

The "memory as evolving playbook" pattern. Trigger → decision → write
→ retrieve → inject is **separated across three roles**, not collapsed
into one LLM forward pass.

```
[trigger]
  Generator (the working agent) executes a task
       │
       ▼
[execution + feedback]
  Generator produces output + receives execution feedback
       │
       ▼
[reflection]
  Reflector reads (task, output, feedback) trace
  Identifies what should be added/refined/removed in the playbook
       │
       ▼
[curation]
  Curator merges Reflector's deltas into the playbook
  Applies "structured, incremental updates that preserve detail"
  Prevents brevity bias and context collapse
       │
       ▼
[next session injection]
  Generator's next session reads the updated playbook
  Cycle repeats
```

**Key properties** (verbatim from ACE paper, arxiv 2510.04618, fetched
during this session and persisted to project memory):
- "ACE prevents collapse with structured, incremental updates that
  preserve detailed knowledge and scale with long-context models"
- "ACE optimizes contexts both offline (e.g., system prompts) and
  online (e.g., agent memory)"
- "+10.6% on agents and +8.6% on finance, while significantly reducing
  adaptation latency and rollout cost"
- "ACE could adapt effectively without labeled supervision and instead
  by leveraging natural execution feedback"
- "On the AppWorld leaderboard, ACE matches the top-ranked
  production-level agent"
- "Building on the adaptive memory introduced by Dynamic Cheatsheet"

The three-role separation is the load-bearing innovation: **decoupling
"who decides what to remember" from "who writes the memory" from
"who reads the memory"** prevents brevity bias and context collapse.

## Chain 3 — Claude Code Auto memory

Claude Code's mechanism is between MemGPT's "all-in-one tool call" and
ACE's "explicit three-role separation." It is **single-LLM agentic, not
externally curated, and the index is the load-bearing primitive**.

```
[trigger]
  During a session, Claude observes:
    - a correction by the user
    - a build command that worked
    - a debugging insight
    - a workflow preference
       │
       ▼
[decision: is this worth remembering?]
  Claude decides "based on whether the information would be useful in
  a future conversation" (verbatim from
  code.claude.com/docs/en/memory § "Auto memory")
       │
       ▼
[write]
  Claude opens MEMORY.md (or a new topic file) with its standard file
  tools (Read/Edit/Write) and updates content. The UI shows
  "Writing memory" when this happens.
       │
       ▼
[during-session retrieval]
  Claude reads topic files on demand using standard file tools when
  the relevant context is needed
       │
       ▼
[next session injection]
  Session start: first 200 lines / 25KB of MEMORY.md is loaded into
  context. Topic files are NOT loaded — only loaded on demand later.
```

**Key properties**:
- Auto memory requires Claude Code v2.1.59+ (released early 2026)
- Storage: `~/.claude/projects/<project>/memory/` for project-scope,
  `~/.claude/agent-memory/<agent>/` for subagent user-scope
- Survives `/compact`: project-root CLAUDE.md is re-injected
  automatically. Nested files reload on next file read.
- The LLM (Claude itself) is the generator, reflector, AND curator
  — there is no separation. This is the simplification and the limitation.
- Topic files = the cold-tier substrate; MEMORY.md = the hot-tier index

## Chain 4 — Akash's research-team setup (already in place)

```
[trigger: end of research session]
  research-lead has finished a multi-round investigation
       │
       ▼
[reflection]
  research-lead dispatches research-retrospector
  research-retrospector reads the full session
  Extracts "3-7 durable lessons"
       │
       ▼
[write]
  research-retrospector writes lessons to
    ~/.claude/agent-memory/research-lead/MEMORY.md
       │
       ▼
[curation]
  research-lead dispatches research-scribe
  research-scribe dedupes new entries against existing entries
  (the ACE "curator" role)
       │
       ▼
[next session injection]
  Next research session: research-lead reads MEMORY.md at session start
  via Claude Code's `memory: user` mechanism. First 200 lines / 25KB
  binding lessons go into the system prompt.
```

**This is literally an ACE-pattern implementation.** The mapping:

| ACE role | Akash's role |
|---|---|
| Generator | research-lead (dispatches specialists, runs the protocol) |
| Reflector | research-retrospector (reads the session, extracts lessons) |
| Curator | research-scribe (dedupes/merges into MEMORY.md) |
| Playbook | `~/.claude/agent-memory/research-lead/MEMORY.md` |

The protocol document (`teams/research/PROTOCOL.md`) explicitly cites
ACE (arxiv 2510.04618) as the prior art. Akash has shipped an ACE
implementation as the lead's memory layer — this is not theoretical.

## Where the extension hooks would go

Given the four chains above, the question for the recommendation is:
**which extra hooks does Akash need to extend Claude Code beyond what
he already has?** Three concrete hook points emerge:

### Hook A — Topic-file curator (factual cell)
**Where it goes**: in the curator role (research-scribe), but extended
to also write topic files (not just dedup MEMORY.md).

**What it does**: when the retrospector identifies a fact that is too
detailed for the index but worth keeping (e.g. a long code snippet, a
benchmark result, a verbatim quote from a paper), the curator routes
it to a topic file rather than the index. The index references the
topic file by filename.

**Why it matters**: gives Akash a cold-tier "factual" store that the
LLM can navigate via standard file tools — the cell Claude Code's pure
"experiential lessons" pattern doesn't naturally fill. Zero new
infrastructure: just an extended scribe behavior.

### Hook B — Cross-session SQLite + FTS5 + vector index over topic files
**Where it goes**: in `~/.claude/agent-memory/<agent>/` as a sibling
file to MEMORY.md.

**What it does**: the curator (or a new sub-curator) maintains a
SQLite database with FTS5 + a small embedding column over the
contents of topic files. The LLM can query this via a custom tool
when the standard "scan filenames" approach is insufficient (e.g.
"have I ever seen a specialist talk about X?")

**Why it matters**: the MemX paper (arxiv 2603.16171, "Local-First
Long-Term Memory System for AI Assistants", retrieved 2026-04-12) is
exactly this — Rust + libSQL + FTS5 + vector + 4-factor reranking,
"Hit@1=91.3%, FTS5 reduces keyword search latency by 1,100x at 100k
records, end-to-end search under 90ms." This is the load-bearing
reference for the local-first / SQLite-as-index path.

### Hook C — Latent-tier briefing for cross-specialist handoff
**Where it goes**: at the orchestrator/worker boundary in
`research-lead`'s dispatch to specialists.

**What it does**: when research-lead dispatches a specialist with a
large workspace context (e.g. round-3 dispatch to evaluator with 12
evidence files in scope), the specialist's first action would be to
load a compacted KV cache of the orchestrator's trajectory rather than
read every file.

**Why it matters**: this is the Latent Briefing / LatentMAS / LRAgent
pattern. **It is currently unbuildable on Claude Code's hosted API**
because the API does not expose KV cache primitives. It is a future
direction tracking item, not a this-quarter recommendation. But it is
load-bearing for the answer to "what comes after files-on-disk for
multi-agent memory" — and the answer is "latent-space cache reuse,
which requires self-hosted inference."

## Causal chain summary table

| Chain | Trigger | Decision-maker | Write site | Retrieval | Curator separation |
|---|---|---|---|---|---|
| MemGPT/Letta | LLM observation | Same LLM in same turn | tool call | tool call (search) | none (LLM does all) |
| Letta Context Repos | LLM observation | Same LLM | filesystem write + auto-commit | filesystem read | git is the curator |
| ACE | Task execution | Reflector (separate role) | Curator (separate role) | Generator reads at session start | yes — three-role split |
| Claude Code Auto memory | LLM observation | Same LLM | filesystem write via Edit tool | session-start injection + on-demand topic-file read | none (LLM does all) |
| Akash's Research Team | End of session | retrospector (separate) | retrospector writes + scribe dedupes | research-lead reads at session start | yes — ACE-pattern |

## Confidence
**High**. Each chain has primary-source documentation for at least the
trigger, write, and retrieval steps. ACE is the cleanest because the
paper is explicit about the three-role decomposition. MemGPT is the
oldest and most-cited. Claude Code's chain is from official docs.
Akash's setup is verifiable on disk.

## Handoff to empiricist
Empiricist should compute the cost/latency/accuracy numbers for each
of the four chains under Akash's actual workload (multi-round research
sessions, ~4 specialists per round, ~10K tokens of evidence per
specialist). The relevant axes are: (a) write cost — how much LLM
work is needed per "remember" decision, (b) read cost at session start
— how much context budget the retrieved memory consumes, (c) latency
of a memory_search at runtime when needed, (d) accuracy of recall on
adversarial queries (the LongMemEval task family).

## Handoff to skeptic
The "ACE pattern is already SOTA" claim (H1) hinges on the ACE paper's
+10.6% / +8.6% numbers and the AppWorld leaderboard match. Skeptic
should attack: (1) is the ACE paper peer-reviewed (it is currently
arxiv-only), (2) what's the strongest counter-argument from H4 (Letta's
self-edit loop), and (3) is "matches Akash's setup" enough validation
when the benchmark task family (AppWorld, finance) is not the same as
"durable lessons for a research team"?
