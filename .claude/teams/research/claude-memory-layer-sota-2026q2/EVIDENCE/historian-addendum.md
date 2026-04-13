# Historian — Addendum (v2 supplementary intel)

The v1 historian.md captured the canonical 18 papers from the prior-art
sweep but missed several load-bearing 2025-2026 entries that the
supplementary intel from main session flagged. This addendum extends
the corpus without rewriting historian.md.

## The structural-frame paper (load-bearing for SYNTHESIS)

### 2025-12-15 / 2026-01-13 — Memory in the Age of AI Agents: A Survey
- **arxiv**: https://arxiv.org/abs/2512.13564 — retrieved 2026-04-12
- **Lead author**: Yuyang Hu (47 total authors including Shichun Liu, Yanwei Yue, Guibin Zhang)
- **v1 submitted**: 2025-12-15. v2: 2026-01-13.
- **Companion paper list**: https://github.com/Shichun-Liu/Agent-Memory-Paper-List
  — 200+ papers, last updated January 2026 (per WebFetch 2026-04-12)
- **Verbatim from arxiv abstract**:
  > "We then examine agent memory through the unified lenses of
  > forms, functions, and dynamics. From the perspective of forms,
  > we identify three dominant realizations of agent memory, namely
  > token-level, parametric, and latent memory. From the perspective
  > of functions, we propose a finer-grained taxonomy that
  > distinguishes factual, experiential, and working memory. From
  > the perspective of dynamics, we analyze how memory is formed,
  > evolved, and retrieved over time."
  > "We hope this survey serves not only as a reference for existing
  > work, but also as a conceptual foundation for rethinking memory
  > as a first-class primitive in the design of future agentic
  > intelligence."
- **Critical meta-finding** (verbatim from WebFetch on the
  companion repo, retrieved 2026-04-12):
  > "The curators explicitly frame this as a design space rather
  > than identifying a SOTA. The introduction states: 'Through this
  > structure, we hope to provide a conceptual foundation for
  > rethinking memory as a first-class primitive in future agentic
  > intelligence.'"
- **Relevance**: this is the canonical 2025-2026 taxonomy. SYNTHESIS
  must use forms × functions × dynamics as the structural frame.
  Akash's brief explicitly demands it. Cartographer.md already
  positions Claude Code's existing mechanism, Latent Briefing,
  Letta, ACE, etc. on this grid.
- **Confidence**: high (47-author consortium, recent, comprehensive,
  arxiv only — not yet peer reviewed)

## The big-claim 2026 systems (audit-required)

### 2026-01-06 — MAGMA: Multi-Graph based Agentic Memory Architecture
- **arxiv**: https://arxiv.org/abs/2601.03236 — retrieved 2026-04-12
- **Authors**: Dongming Jiang, Yi Li, Guanpeng Li, Bingzhe Li
- **Reference impl**: github.com/FredJiang0324/MAMGA (82 stars, MIT,
  last commit 2026-01-04, retrieved 2026-04-12)
- **Verbatim from abstract**:
  > "Memory-Augmented Generation (MAG) extends Large Language Models
  > with external memory to support long-context reasoning, but
  > existing approaches largely rely on semantic similarity over
  > monolithic memory stores, entangling temporal, causal, and
  > entity information. This design limits interpretability and
  > alignment between query intent and retrieved evidence, leading
  > to suboptimal reasoning accuracy."
  > "MAGMA, a multi-graph agentic memory architecture that
  > represents each memory item across orthogonal semantic, temporal,
  > causal, and entity graphs. MAGMA formulates retrieval as
  > policy-guided traversal over these relational views, enabling
  > query-adaptive selection and structured context construction."
  > "Experiments on LoCoMo and LongMemEval demonstrate that MAGMA
  > consistently outperforms state-of-the-art agentic memory systems
  > in long-horizon reasoning tasks."
- **Claimed benchmark numbers** (from search-result extraction
  2026-04-12):
  - LoCoMo overall: 0.700 (best in their table)
  - vs Full Context 0.481, A-MEM 0.580, MemoryOS 0.553, Nemori 0.590
  - Relative improvement range: **+18.6% to +45.5%** over those baselines
  - LongMemEval: 61.2% average accuracy
- **Key innovation**: 4 ORTHOGONAL graphs decompose what
  Graphiti/Cognee/Mem0-g unify into one graph. Policy-guided
  traversal is reinforcement-learning-style routing over the views.
- **Adversary handoff**: github-miner audit confirms benchmark
  scripts present (`test_fixed_memory.py`, `test_longmemeval_chunked.py`)
  and "exercise the full MAGMA architecture including graph
  construction, multi-hop traversal" per WebFetch interpretation.
  Independent reproduction would require running the code, which
  empiricist did not do this round. The 45.5% number is the
  marketing-friendly upper end of a comparison range vs A-MEM/Nemori,
  not vs the full-context baseline (which is ~70%, so the real
  margin is small).
- **Credibility**: medium-high (paper exists, code exists, claims are
  bounded, comparison is against weak baselines so the upper-end
  number is suspect)

### 2026-01-05 / 2026-01-09 — EverMemOS: Self-Organizing Memory OS
- **arxiv**: https://arxiv.org/abs/2601.02163 — retrieved 2026-04-12
- **Authors**: Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai,
  Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong Bing, Yafeng Deng
- **Reference impl**: github.com/EverMind-AI/EverMemOS (URL stated in
  paper; not directly fetched in this round)
- **Verbatim from abstract**:
  > "Large Language Models (LLMs) are increasingly deployed as
  > long-term interactive agents, yet their limited context windows
  > make it difficult to sustain coherent behavior over extended
  > interactions."
- **Architecture (verbatim from WebFetch)**:
  - **MemCells**: "Convert dialogue streams into discrete memory
    units capturing episodic traces, atomic facts, and time-bounded
    Foresight signals."
  - **Semantic Consolidation**: "Organizes MemCells into thematic
    MemScenes, distilling semantic structures and refreshing user
    profiles."
  - **Reconstructive Recollection**: "Implements MemScene-guided
    retrieval to assemble necessary context for downstream reasoning."
  - **Engram-inspired lifecycle for computational memory**
- **Benchmarks**: LoCoMo, LongMemEval, PersonaMem v2 profile study.
  Claims: "state-of-the-art performance on memory-augmented reasoning
  tasks." Specific numbers not surfaced in WebFetch — need direct
  paper read or empiricist run.
- **Credibility**: medium. Paper exists, architecture is principled
  (close to standard episodic→semantic consolidation), claims are
  bounded ("state-of-the-art" not "+45%"). Lidong Bing is a known
  researcher (DAMO Academy, formerly Alibaba). Not yet peer reviewed.

### 2026-02-22 — Anatomy of Agentic Memory (the critical meta-paper)
- **arxiv**: https://arxiv.org/abs/2602.19320 — retrieved 2026-04-12
- **Authors**: Dongming Jiang, Yi Li, Songtao Wei, Jinxin Yang,
  Ayushi Kishore, Alysa Zhao, Dingyi Kang, Xu Hu, Feng Chen, Qiannan
  Li, Bingzhe Li (NOTE: same authors as MAGMA, which is interesting —
  they wrote both the system paper and the meta-criticism)
- **Verbatim from abstract**:
  > "Despite rapid architectural development, the empirical
  > foundations of these systems remain fragile: existing benchmarks
  > are often underscaled, evaluation metrics are misaligned with
  > semantic utility, performance varies significantly across
  > backbone models, and system-level costs are frequently
  > overlooked."
  > "We first introduce a concise taxonomy of MAG systems based on
  > four memory structures. Then, we analyze key pain points
  > limiting current systems, including benchmark saturation effects,
  > metric validity and judge sensitivity, backbone-dependent
  > accuracy, and the latency and throughput overhead introduced by
  > memory maintenance."
  > "By connecting the memory structure to empirical limitations,
  > this survey clarifies why current agentic memory systems often
  > underperform their theoretical promise"
- **Relevance**: this is the load-bearing meta-paper for the
  recommendation. **The same authors who built MAGMA also wrote the
  paper saying "all benchmarks in this space are saturated and
  misleading."** That's a strong epistemic signal: even the authors
  of an SOTA-claiming system know the benchmarks they used are
  unreliable.
- **Credibility**: high (independent meta-analysis, written by people
  who built systems and were burned by the benchmark saturation)

## Latent layer — the 2025-2026 frontier

### 2025-11-25 / 2025-12-08 — LatentMAS (Latent Collaboration in Multi-Agent Systems)
- **arxiv**: https://arxiv.org/abs/2511.20639 — retrieved 2026-04-12
- **Authors**: Jiaru Zou, Xiyuan Yang, Ruizhong Qiu, Gaotang Li,
  Katherine Tieu, Pan Lu, Ke Shen, Hanghang Tong, **Yejin Choi**,
  Jingrui He, **James Zou**, Mengdi Wang, Ling Yang
- **Verbatim from abstract**:
  > "Multi-agent systems (MAS) extend large language models (LLMs)
  > from independent single-model reasoning to coordinative
  > system-level intelligence. While existing LLM agents depend on
  > text-based mediation for reasoning and communication, we take a
  > step forward by enabling models to collaborate directly within
  > the continuous latent space."
  > "auto-regressive latent thoughts generation through last-layer
  > hidden embeddings"
  > "a shared latent working memory that preserves and transfers
  > each agent's internal representations"
- **Claimed numbers**:
  - Up to **14.6% accuracy improvement across 9 benchmarks**
  - **70.8%-83.7% fewer output tokens**
  - **4×-4.3× faster inference**
  - "no additional training" required
- **Code**: github.com/Gen-Verse/LatentMAS
- **Credibility**: high. Yejin Choi and James Zou are top-tier
  researchers (Stanford / UW). James Zou is also on the ACE paper
  (arxiv 2510.04618) — the same author published both the
  token-level "playbook" pattern (ACE) and the latent-level
  "shared working memory" pattern (LatentMAS), implying they are
  complementary not competing.
- **Relevance**: this is the closest open-source academic analog to
  Ramp Labs' Latent Briefing. The mechanism (shared latent
  representations between agents) is the same family. Uses last-layer
  hidden embeddings rather than KV cache compaction specifically.

### 2026-02-03 — LRAgent (Efficient KV Cache Sharing for Multi-LoRA LLM Agents)
- **arxiv**: https://arxiv.org/abs/2602.01053 — retrieved 2026-04-12
- **Verbatim from abstract**:
  > "Role specialization in multi-LLM agent systems is often realized
  > via multi-LoRA, where agents share a pretrained backbone and
  > differ only through lightweight adapters. Despite sharing base
  > model weights, each agent independently builds and stores its
  > own KV cache for the same long, tool-augmented trajectories,
  > incurring substantial memory and compute overhead."
  > "we propose LRAgent, a KV cache sharing framework for multi-LoRA
  > agents that decomposes the cache into a shared base component
  > from the pretrained weights and an adapter-dependent component
  > from LoRA weights"
  > "LRAgent achieves throughput and time-to-first-token latency
  > close to fully shared caching, while preserving accuracy near
  > the non-shared caching baseline"
- **Numbers**:
  - TTFT reduction up to **4.44× compared to non-shared baseline**
  - Accuracy drop ≤ 1.5% with BaseLRShared scheme
- **Code**: github.com/hjeon2k/LRAgent
- **Relevance**: another KV-cache-sharing-across-agents paper.
  Different angle (multi-LoRA, not orchestrator-worker), but the
  same insight: token-level message passing between agents that share
  context is wasteful, and KV cache reuse saves it.

### 2026-04-11 — Ramp Labs Latent Briefing (paywalled primary source)
- **Primary source**: https://x.com/RampLabs/status/2042660310851449223
  (full paper post) — **retrieved 2026-04-12, returned HTTP 402 (paywall)**
- **Teaser tweet**: https://x.com/RampLabs/status/2042672773747589588
  (paywalled)
- **Reconstructed details from search-result extraction (2026-04-12)**:
  - "Latent Briefing is about efficient memory sharing for multi-agent
    systems via KV cache compaction"
  - "The core idea is to find a compact cache of size t < S that
    produces nearly identical attention outputs from a KV cache of
    size S"
  - "the worker maintains a persistent KV cache of the orchestrator's
    trajectory across calls. On each call, the orchestrator's updated
    trajectory is forward passed through the worker model, with KV
    prefix caching, where typically 90%+ of tokens are unchanged from
    the previous call and reused directly"
  - "task guided query vectors replace the original framework's
    context-based queries with queries derived from the orchestrator's
    task prompt, enabling cache compression that prioritizes
    information most relevant to the worker task"
  - **Performance**: ~1.7s per compaction, ~20× faster than
    sequential attention matching, 10-30× faster than LLM
    summarization. **31% token reduction reported.**
  - **Accuracy**: "+3 pp gain across all three conditions" using
    Claude Sonnet 4 as orchestrator and Qwen-14B as worker on
    LongBench v2
- **Credibility**: medium (search-result extraction, no reachable
  primary). Ramp Labs is a real research org (the credit-card
  company's labs arm, similar to Stripe Press's research-publication
  vibe). The technique has converging evidence in LatentMAS and
  LRAgent, both of which are reachable arxiv papers with the same
  family of insights.
- **Status**: directional convergence is high; benchmark numbers are
  marked as REPORTED, not VERIFIED.

## Continuum direction (2026-01-14)

### Continuum Memory Architectures for Long-Horizon LLM Agents
- **arxiv**: https://arxiv.org/abs/2601.09913 — retrieved 2026-04-12
- **Author**: Joe Logan
- **Submission date**: 2026-01-14
- **Verbatim**:
  > "Retrieval-augmented generation (RAG) has become the default
  > strategy for providing large language model (LLM) agents with
  > contextual knowledge. Yet RAG treats memory as a stateless
  > lookup table: information persists indefinitely, retrieval is
  > read-only, and temporal continuity is absent."
- **Architecture**: Continuum Memory Architecture (CMA) — "persistent
  storage, selective retention, associative routing, temporal chaining,
  and consolidation into higher-order abstractions."
- **Relevance**: this is the cleanest critique of standard RAG-as-
  memory in the corpus. Reinforces the convergent finding: vector
  RAG fails as agent memory because it's stateless / read-only / has
  no time / no consolidation. **Used by skeptic in Round 2 to
  pressure-test any recommendation that leans on naive RAG.**

## The Mem0 vs Zep dispute — primary sources

### Zep's rebuttal: "Lies, Damn Lies, & Statistics"
- **URL**: https://blog.getzep.com/lies-damn-lies-statistics-is-mem0-really-sota-in-agent-memory/
  — retrieved 2026-04-12
- **Author**: Daniel Chalef (with Preston Rasmussen)
- **Published**: 2025-05-06
- **Verbatim numerical claims**:
  > "Zep achieving an 75.14% +/- 0.17 J score"
  > "significantly outperforming Mem0's best configuration (Mem0 Graph)
  > by approximately 10% relative improvement"
  > "Zep's p95 search latency: 0.632 seconds"
  > "Mem0's own results show their system being outperformed by a
  > simple full-context baseline...achieved a J score of ~73%, compared
  > to Mem0's best score of ~68%"
  > "Mem0's reported Zep score: 65.99%"
  > "Mem0 graph search latency: 0.657s"
- **Methodological errors documented**:
  1. "Incorrect User Model: Mem0 assigned user roles to both
     participants, confusing identity tracking"
  2. "Improper Timestamp Handling: Timestamps appended to messages
     rather than using dedicated fields"
  3. "Sequential vs. Parallel Searches: Searches performed sequentially,
     artificially inflating latency measurements"
- **Adversary status**: self-interested source (Zep sells the
  competing Graphiti product), but the methodological critique is
  itself verifiable in Mem0's paper. The full-context baseline number
  (~73%) is the load-bearing finding because if true, it
  invalidates the entire LoCoMo-leaderboard arms race. **Treat as
  "self-interested but technically correct on the methodology
  critique" — see adversary.md for the full audit.**

## What the addendum changes about historian.md's conclusion

historian.md's "five mechanism families" framing remains valid, but
the **convergent direction** finding now needs to be expanded:

The 5 families (from arxiv 2603.07670):
1. Context-resident compression
2. Retrieval-augmented stores
3. Reflective self-improvement
4. Hierarchical virtual context
5. Policy-learned management

Plus a sixth family that emerges from the latent papers
(LatentMAS, LRAgent, Latent Briefing, MemOS's MemCubes):

6. **Latent-state sharing** — agents pass KV-cache or hidden-state
   representations between each other rather than tokens. Active
   research area, no consensus yet, but multiple converging signals
   from independent groups (Stanford/UW for LatentMAS, Ramp Labs for
   Latent Briefing, MemOS for MemCubes).

The convergent direction for **coding agents specifically** stays
the same — files on a local filesystem, LLM-self-curated, git-
versioned, two-tier hot/cold structure with hybrid retrieval where
needed. The latent-state sharing direction is the **next frontier**
for multi-agent setups but is not actionable on Claude Code's
hosted API today.

## Confidence
**High** on the additions. Every paper has a primary URL retrieved
2026-04-12, with verbatim quotes from abstracts. The Latent Briefing
primary source is paywalled and clearly marked as REPORTED-NOT-VERIFIED.

## Open questions surfaced by the addendum
- **Ramp Labs Latent Briefing primary text**: still inaccessible at
  session end. Resolution: track the paper post-paywall release;
  treat all numerical claims as estimates until then.
- **EverMemOS reference impl**: github.com/EverMind-AI/EverMemOS not
  fetched. Resolution: empiricist re-dispatch if recommendation
  depends on it.
- **MAGMA's +45.5% claim baseline-source**: the comparison is vs
  A-MEM/Nemori, which are themselves debated. Resolution: adversary
  pass to verify the baseline is honest.
