# Planner — dispatch recommendation for claude-memory-layer-sota-2026q2

## Question classification
- **Question class**: hybrid — **competitive analysis** (SOTA production
  systems: Mem0, Zep, Letta, LangMem, Graphiti, Cognee, HippoRAG 2) +
  **prior-art sweep** (2025-2026 academic literature on agent memory) +
  **decisional** (what should Akash build/adopt this week).
- **Complexity**: complex. Multiple open systems, heavy SEO terrain,
  actionable recommendation required. This is not a fact-finding query
  or a direct comparison — it is an architecture decision with breadth.
- **Anthropic scaling rule says**: complex research → 5-10+ specialists,
  multi-round. Err toward the high end on the opener (per MEMORY.md
  lesson "Dispatch breadth follows Anthropic's published scaling rule").
- **Past lessons from MEMORY.md that apply**:
  - "Dispatch breadth follows Anthropic's published scaling rule" →
    this is complex, open with 7+ specialists.
  - "Parallel tool calling is a 10x force multiplier" → round 1 must be
    a single-message parallel dispatch (or in adopted-persona mode, a
    single batch of inline executions).
  - "The skeptic attacks reasoning; the adversary attacks the corpus" →
    MANDATORY adversary pass. "AI memory" topic is one of the most SEO-
    gamed spaces of 2025-2026 (Mem0/Zep/Letta all have content marketing
    operations); the adversary is load-bearing here, not optional.
  - "Contradictions go to the moderator, not to your own judgment" →
    the benchmark-dispute contradictions that WILL emerge (Mem0's paper
    claims 26% better than OpenAI memory, Zep claims 18.5% better than
    MemGPT on LoCoMo) need the moderator, not lead arbitration.
  - "Subagents cannot spawn subagents — plan accordingly" → this run is
    in adopted-persona mode. The lead executes each specialist's method
    inline, writes the evidence file, moves on. The gate order still
    holds; the method is procedural not process-based.
  - "End-state evaluation beats path evaluation" → do not optimize for
    short LOG.md. Optimize for a SYNTHESIS.md the 5-dim evaluator passes.

## Recommended opening dispatch (Round 1)

Parallel dispatch of **9 specialists** in a single batch. For each, the
lead (adopted persona) runs the specialist's method inline and writes
the specialist's evidence file before moving to the next:

1. **librarian** — Official docs for the 7 production memory systems.
   Sub-question: "What does Mem0, Zep/Graphiti, Letta, LangMem, Cognee,
   Memary, Memobase, and Claude Code's own `memory: user` mechanism
   *actually* document as of April 2026? Version, API, backends, license,
   self-hosted support, quickstart shape." Context7 first, then WebFetch
   on official docs.

2. **historian** — Academic papers, chronological. Sub-question:
   "2023-2026 papers on LLM agent memory — foundational (MemGPT, Reflexion,
   Generative Agents, Voyager), recent (A-MEM arxiv 2502.12110, Mem0
   arxiv 2504.19413, HippoRAG 2 arxiv 2502.14802, ACE arxiv 2510.04618,
   Memobase/Memory in Age of AI Agents). Use arXiv + Semantic Scholar +
   Hugging Face papers. Tag each paper with primary claim, benchmark
   used, methodology, year, credibility.

3. **web-miner** — Community discussion corpus. Sub-question: "HN, Reddit
   (r/LocalLLaMA, r/MachineLearning, r/ChatGPTPromptGenius), Medium,
   Substack, dev.to blogs on agent memory in 2025-2026. Use HN Algolia,
   Reddit .json, dev.to API. Dump raw JSON to EVIDENCE/web-miner/raw/."

4. **github-miner** — Ecosystem signals at scale. Sub-question: "Stars,
   star-velocity, issue volume, release cadence, recent commits for
   mem0ai/mem0, letta-ai/letta, getzep/zep, getzep/graphiti, topoteretes/
   cognee, langchain-ai/langmem, kingjulio8238/Memary, OSU-NLP-Group/
   HippoRAG, theresearchsquad/memobase. Cross-reference with the
   librarian and historian. Raw JSON caches under EVIDENCE/github-
   miner/raw/."

5. **cartographer** — Claude Code's current memory mechanism. Sub-question:
   "Read Claude Code sub-agents/memory docs + any local evidence in
   ~/.claude/ showing how `memory: user` actually works. Where does the
   file get read, how does it get injected, what's the real ceiling
   (25KB? 200 lines? both?), is there a vector index layer?" This is a
   structural / mechanism question, hence cartographer not librarian.

6. **tracer** — MemGPT/Letta self-edit loop and ACE reflection loop —
   runtime mechanics. Sub-question: "What exactly happens when MemGPT/
   Letta executes a memory write? What's the causal chain from 'LLM
   emits memory_insert tool call' to 'the next turn sees the update'?
   Same for ACE: what's the generator → reflector → curator loop in
   concrete terms? Cite the papers + any open-source impls."

7. **linguist** — Taxonomic clarification. Sub-question: "What do
   'episodic', 'semantic', 'procedural', 'working', 'short-term',
   'long-term', 'archival', 'core', 'hot', 'cold', 'context', 'memory'
   actually mean in the 2025-2026 literature? Which terms are polysemous?
   Which are marketing vs technical?" This prevents the moderator from
   having to adjudicate language-mismatch contradictions later.

8. **empiricist** — Back-of-envelope cost/latency tradeoff. Sub-question:
   "Compare (a) 25KB-file injection as Claude Code does today, (b) vector-
   RAG retrieval with 100K-token store and 5 retrieved passages, (c)
   temporal-graph hybrid retrieval (Zep/Graphiti-style) — what do the
   published benchmarks say about latency, accuracy, cost? Do not invent
   numbers; cite or flag 'estimate'. Focus on what can be answered without
   running actual code, since this is a literature-grounded question."

9. **skeptic** — Pre-emptive adversary of my own H1 (ACE). Sub-question:
   "I (the lead) am going into this strongly prior-biased toward H1
   (ACE evolving-playbook) because it matches Akash's existing setup.
   Attack that bias. What would make H1 wrong? What are the strongest
   arguments for H2/H3/H4 that I'm underweighting?" (Note: this is
   pre-emptive because a lead-biased synthesis is easier to catch early.)

## Recommended follow-ups (Round 2)

- **synthesist** (unconditional): after round 1, cross-cut the 9 evidence
  files, build claim matrix, identify contradictions. Benchmark disputes
  are the most likely contradictions (Mem0 vs Zep vs HippoRAG 2 all
  claim to be SOTA on overlapping metrics).
- **moderator** (conditional on ≥1 load-bearing contradiction): the
  benchmark-dispute contradictions should be debated, not arbitrated by
  me. Expected: 1-3 moderator debates.
- **adversary** (mandatory — high-SEO terrain): audit every URL cited in
  librarian.md, historian.md, web-miner.md, github-miner.md. Flag SEO
  farms, paid newsletter reposts, LinkedIn-influencer-style Medium posts,
  astroturfed HN threads. This is the biggest gate on this session.
- **archaeologist** (conditional, probably not needed): only if we find
  an interesting historical pivot in one of the open-source projects.
  Likely skip unless round 1 surfaces one.

## Recommended gates

- **skeptic**: runs in round 1 (pre-emptive, on lead bias) AND round 2
  (post-synthesis). Mandatory before "high confidence."
- **adversary**: runs in round 2. Mandatory — topic is heavily SEO-gamed.
- **moderator**: runs in round 2 conditional on synthesist flagging
  contradictions. Almost certain to fire.
- **evaluator**: runs last, after skeptic AND adversary. Mandatory
  before "high confidence."
- **retrospector**: at session close, unconditional.

## Blind spots I flag

- **archaeologist**: I did not schedule him. If any project has a
  dramatic rewrite/pivot history (e.g., Letta rebranding from MemGPT,
  Zep 2.x → 3.x architecture change), archaeology could shed light on
  whether current marketing matches current code. The github-miner
  should surface this as a side-finding; if it does, dispatch the
  archaeologist in round 2.
- **linguist in round 2**: I put linguist in round 1. If the moderator
  hits polysemy contradictions (e.g., Mem0's "memory" vs Letta's
  "memory" vs ACE's "context playbook" all being the same word for
  different concepts), re-dispatch linguist with a cross-product vocab
  audit.
- **empiricist real experiments**: I scoped empiricist to back-of-envelope
  literature comparison because running actual Mem0/Zep/Letta locally
  has setup tax. If the evaluator fails dim 1 (factual accuracy) on
  benchmark claims, re-dispatch empiricist with "clone repo X, run
  bench, capture output."

## Expected rounds to high confidence

**3 rounds** minimum (round 1 wide → round 2 gates → round 3 evaluator).
**4 rounds** if the evaluator FAILS round 1 gates and forces re-work.
Hard cap: 4. If we can't close in 4, publish SYNTHESIS.md at medium
confidence with an OPEN_QUESTIONS.md entry.

## Budget check

9 specialists round 1 × ~3-6 tool calls each (inline, not independent
agents), plus ~4 specialists round 2, plus synthesis + evaluator +
retrospector = roughly ~60-100 tool calls total, mostly WebFetch. All
Opus, all max effort, no downgrades. Budget is fine — Max plan, quality
over speed.

## Confidence in this plan

**High**. The plan maps cleanly to Anthropic's scaling rule for complex
research, invokes every round-2 gate (moderator + skeptic + adversary)
that MEMORY.md says is load-bearing, and pre-emptively addresses the
two biggest failure modes for this question class (lead bias toward H1,
SEO-capture of the corpus). The one risk is adopted-persona mode
(no parallel dispatch) — each specialist will run sequentially inside
this thread rather than concurrently. That's a time cost, not a quality
cost, and the MEMORY.md lesson "Subagents cannot spawn subagents"
explicitly covers this case.
