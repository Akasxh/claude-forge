# Historian — prior art on LLM agent memory

Sub-question: Chronological layering of the academic literature on LLM
agent memory, from 2023 foundational to 2026-Q2 frontier. Tagged by
primary claim, benchmark used, methodology, year, credibility.

## Canonical names for this topic
- "Agent memory" — most common in 2025-2026
- "Long-term memory for LLMs" — common in 2024
- "Context engineering" — ACE paper's framing (arxiv 2510.04618)
- "Memory-augmented generation (MAG)" — MemOS paper's framing
- "Agentic RAG" — retrieval-framed with tool-based access (Letta)
- "Personalized continual learning" — HippoRAG 2's framing
- "Stateful agents" — Letta's product positioning
- "Memory OS / memory management" — MemGPT / MemOS framing

## Foundational layer (2023-2024)

### 2023-10-12 — MemGPT: Towards LLMs as Operating Systems
- **Authors**: Charles Packer, Sarah Wooders, Kevin Lin, Vivian Fang,
  Shishir G. Patil, Ion Stoica, Joseph E. Gonzalez — UC Berkeley
- **URL**: https://arxiv.org/abs/2310.08560 — retrieved 2026-04-12
- **Abstract verbatim**:
  > "Large language models (LLMs) have revolutionized AI, but are
  > constrained by limited context windows, hindering their utility in
  > tasks like extended conversations and document analysis."
- **Core innovation**: hierarchical memory (core + recall + archival)
  with **LLM-directed self-editing** via tool calls. The LLM decides
  what to remember, not an external classifier.
- **Credibility**: high (UC Berkeley, Ion Stoica's group, 363-point HN
  Show HN 2023-10-16 thread 37901902, 85 comments)
- **Relevance**: foundational for the "memory as tools" paradigm.
  Letta is the production descendant.

### 2023-05-17 — MemoryBank: Enhancing LLMs with Long-Term Memory
- **Authors**: Wanjun Zhong, Lianghong Guo, Qiqi Gao, He Ye, Yanlin Wang
- **URL**: https://arxiv.org/abs/2305.10250 — retrieved 2026-04-12
- **Abstract verbatim** (partial):
  > "Revolutionary advancements in Large Language Models have drastically
  > reshaped our interactions with artificial intelligence systems...
  > deficiency of a long-term memory mechanism."
- **Credibility**: medium (early paper, widely cited but superseded)
- **Relevance**: introduced the Ebbinghaus forgetting-curve approach
  that later papers (FadeMem 2026, SuperLocalMemory V3.3 2026) build on.

### 2024-02-27 — LoCoMo: Evaluating Very Long-Term Conversational Memory of LLMs
- **Authors**: Adyasha Maharana, Dong-Ho Lee, Sergey Tulyakov, Mohit
  Bansal, Francesco Barbieri, Yuwei Fang — Snap Inc + UNC Chapel Hill
- **URL**: https://arxiv.org/abs/2402.17753 — retrieved 2026-04-12
- **What it is** (verbatim):
  > "a dataset of very long-term conversations, each encompassing 300
  > turns and 9K tokens on avg., over up to 35 sessions"
- **Method** (verbatim):
  > "a machine-human pipeline to generate high-quality, very long-term
  > dialogues... LLM-based agent architectures grounded in personas and
  > temporal event graphs... verified and edited by human annotators
  > for long-range consistency"
- **Tasks**: question answering, event summarization, multi-modal
  dialogue generation
- **Key finding** (verbatim):
  > "LLMs exhibit challenges in understanding lengthy conversations and
  > comprehending long-range temporal and causal dynamics"
- **Credibility**: high (published, human-annotated)
- **CRITICAL CAVEAT**: LoCoMo has become the near-universal benchmark
  for agent memory (used by Mem0, Zep, MemOS, A-MEM, Memori, Cortex,
  Engram, VAC, Forensic, MemForge, etc.) and is therefore **saturated**.
  Per Zep's rebuttal to Mem0 (blog.getzep.com, 2025-05-06,
  retrieved 2026-04-12): a trivial **full-context baseline achieved
  ~73% on LoCoMo**, beating Mem0's best ~68%. Average conversation
  length "16,000-26,000 tokens... easily within the context window
  capabilities of modern LLMs." This invalidates benchmark leadership
  claims based on LoCoMo alone — see `EVIDENCE/adversary.md`.

### 2024-05-23 — HippoRAG (v1)
- **URL**: https://github.com/OSU-NLP-Group/HippoRAG — retrieved 2026-04-12
- **Venue**: NeurIPS 2024
- **Core innovation**: Personalized PageRank over OpenIE graph + LLM
  indexing; model of hippocampal pattern-separation/completion
- **Superseded by**: HippoRAG 2 (2025-02-20)

## Recent frontier (2025)

### 2025-02-17 — A-MEM: Agentic Memory for LLM Agents
- **Authors**: Wujiang Xu, Zujie Liang, Kai Mei, Hang Gao, Juntao Tan,
  Yongfeng Zhang — agiresearch.io
- **URL**: https://arxiv.org/abs/2502.12110 — retrieved 2026-04-12
- **Abstract verbatim** (key passage):
  > "Following the basic principles of the Zettelkasten method, we
  > designed our memory system to create interconnected knowledge
  > networks through dynamic indexing and linking. When a new memory is
  > added, we generate a comprehensive note containing multiple
  > structured attributes, including contextual descriptions, keywords,
  > and tags. The system then analyzes historical memories to identify
  > relevant connections... this process enables memory evolution — as
  > new memories are integrated, they can trigger updates to the
  > contextual representations and attributes of existing historical
  > memories."
- **Method**: "empirical experiments on six foundation models show
  superior improvement against existing SOTA baselines" (specific
  numbers not in abstract — flagged for empiricist)
- **Credibility**: medium-high (recent, has reference impl, 961 GH stars)
- **Relevance**: validates "memory as an evolving knowledge graph
  constructed by the LLM itself" — converges with ACE's reflection loop

### 2025-02-20 — HippoRAG 2: Non-Parametric Continual Learning for LLMs
- **Authors**: Bernal Jiménez Gutiérrez, Yiheng Shu, Weijian Qi, Sizhe
  Zhou, Yu Su — OSU NLP
- **URL**: https://arxiv.org/abs/2502.14802 — retrieved 2026-04-12
- **Venue**: ICML 2025
- **Abstract verbatim** (key passages):
  > "Recent RAG approaches augment vector embeddings with various
  > structures like knowledge graphs to address some of these gaps,
  > namely sense-making and associativity. However, their performance
  > on more basic factual memory tasks drops considerably below standard
  > RAG. We address this unintended deterioration and propose HippoRAG 2,
  > a framework that outperforms standard RAG comprehensively on factual,
  > sense-making, and associative memory tasks."
  > "HippoRAG 2 builds upon the Personalized PageRank algorithm used in
  > HippoRAG and enhances it with deeper passage integration and more
  > effective online use of an LLM. This combination pushes this RAG
  > system closer to the effectiveness of human long-term memory,
  > achieving a 7% improvement in associative memory tasks over the
  > state-of-the-art embedding model"
- **Three long-term memory competence tests**: factual, sense-making,
  associative
- **Credibility**: high (peer-reviewed ICML 2025, modest 7% claim,
  reference impl open)
- **Relevance**: the strongest academic pedigree for "graph + vector
  hybrid retrieval" among the 2025 crop. Unlike Mem0/Zep/MemOS, the
  claim is bounded and the methodology is academic.

### 2025-04-28 — Mem0: Building Production-Ready AI Agents with Scalable LTM
- **Authors**: Prateek Chhikara, Dev Khant, Saket Aryan, Taranjeet Singh,
  Deshraj Yadav — Mem0 Inc (company-authored)
- **URL**: https://arxiv.org/abs/2504.19413 — retrieved 2026-04-12
- **Abstract verbatim**:
  > "Mem0, a scalable memory-centric architecture that addresses this
  > issue by dynamically extracting, consolidating, and retrieving
  > salient information from ongoing conversations. Building on this
  > foundation, we further propose an enhanced variant [Mem0-g] that
  > leverages graph-based memory representations to capture complex
  > relational structures among conversational elements."
- **Claimed numbers**: "26% relative improvements in LLM-as-a-Judge
  over OpenAI"; "91% lower p95 latency"; "more than 90% token cost"
  savings
- **Benchmark**: LOCOMO
- **Credibility**: **contested**. Company-authored paper. Zep
  demonstrated implementation errors in the Zep baseline; trivial
  full-context beats it. See `EVIDENCE/adversary.md` and Zep rebuttal.
- **Relevance**: widely-cited, commercially successful (raised $24M
  from YC + Peak XV + Basis Set, 2025-10-28 TechCrunch announcement),
  but benchmark claim not cleanly defensible.

### 2025-05-28 / 2025-07-04 — MemOS: A Memory OS for AI System
- **Authors**: Zhiyu Li, Shichao Song, Chenyang Xi, Hanyu Wang + many
  (Shanghai-adjacent research groups, MemTensor)
- **URL**: https://arxiv.org/abs/2507.03724 — retrieved 2026-04-12 (long
  version). Short version arxiv 2505.22101 (2025-05-28).
- **Abstract verbatim** (key passages):
  > "we propose MemOS, a memory operating system that treats memory as
  > a manageable system resource... introducing an explicit memory layer
  > between parameter memory and external retrieval can substantially
  > reduce these costs by externalizing specific knowledge."
  > "plaintext, activation-based, and parameter-level memories"
  > "A MemCube encapsulates both memory content and metadata such as
  > provenance and versioning. MemCubes can be composed, migrated, and
  > fused over time, enabling flexible transitions between memory types
  > and bridging retrieval with parameter-based learning."
- **Claimed numbers** (from official README, not the paper):
  > "+43.70% Accuracy vs. OpenAI Memory • LoCoMo 75.80 • LongMemEval
  > +40.43% • PrefEval-10 +2568% • PersonaMem +40.75%"
- **Credibility**: **medium-contested**. Academic paper exists with
  reasonable theoretical framing. Marketing numbers are even larger
  than Mem0's (+43.7% vs Mem0's +26%), which in a saturated-benchmark
  setting is suspicious. Also self-published on LoCoMo, the saturated
  benchmark. Adversary gate mandatory.

### 2025-10-06 — ACE: Agentic Context Engineering
- **Authors**: Qizheng Zhang, Changran Hu, Shubhangi Upasani, Boyuan Ma,
  Fenglu Hong, Vamsidhar Kamanuru, Jay Rainton, Chen Wu, Mengmeng Ji,
  Hanchen Li, Urmish Thakker, James Zou, Kunle Olukotun — **Stanford**
  (including James Zou and Kunle Olukotun)
- **URL**: https://arxiv.org/abs/2510.04618 — retrieved 2026-04-12
- **Abstract verbatim** (key passages):
  > "Large language model (LLM) applications such as agents and domain-
  > specific reasoning increasingly rely on context adaptation: modifying
  > inputs with instructions, strategies, or evidence, rather than weight
  > updates."
  > "treats contexts as evolving playbooks that accumulate, refine, and
  > organize strategies through a modular process of generation,
  > reflection, and curation."
  > "+10.6% on agents and +8.6% on finance"
  > "Matches top-ranked production-level agent on AppWorld leaderboard
  > overall average... Surpasses competing approaches on harder test-
  > challenge split using smaller open-source model."
  > "prevents two key failures: brevity bias, which drops domain
  > insights for concise summaries, and context collapse, where
  > iterative rewriting erodes details over time."
  > "works without labeled supervision and instead by leveraging natural
  > execution feedback... significantly reducing adaptation latency and
  > rollout cost."
- **Three roles**: generator, reflector, curator. Operates **offline
  (system prompts) and online (agent memory)**.
- **Credibility**: **high**. Stanford (James Zou, Kunle Olukotun are
  named authors), concrete reproducible metrics, bounded claims, works
  on both closed and open-source models. Peer review status: not
  stated; arxiv only.
- **Relevance**: directly describes a generation → reflection →
  curation loop that matches Akash's *existing* Research Team setup
  (research-retrospector = reflector, research-scribe = curator,
  research-lead = generator-consumer). This paper is the theoretical
  justification for H1.

### 2025-12-15 / 2026-01-13 — Memory in the Age of AI Agents: A Survey
- **Authors**: 47-author consortium including Yuyang Hu, Shichun Liu,
  Yanwei Yue, Guibin Zhang + many
- **URL**: https://arxiv.org/abs/2512.13564 — retrieved 2026-04-12
- **Taxonomy proposed**: three lenses
  - **Forms**: token-level, parametric, latent memory
  - **Functions**: factual, experiential, working memory
  - **Dynamics**: formation, evolution, retrieval
- **Key claim** (paraphrased from WebFetch summary):
  > "traditional taxonomies such as long/short-term memory have proven
  > insufficient to capture modern agent memory diversity"
- **Credibility**: high (47 authors, comprehensive survey, recent)
- **Relevance**: most current consensus framing of what "agent memory"
  means. Differs from HIPPORAG 2's factual/sense-making/associative
  framing and from Letta's core/recall/archival framing — suggesting
  the taxonomic landscape is still unsettled.

## Frontier 2026 — the firehose

The arxiv torrent of Jan-Apr 2026 papers on agent memory shows the
field is **not converged**. 30+ papers surfaced in 12 weeks. Notable:

### 2026-02-22 — Anatomy of Agentic Memory: Taxonomy and Empirical Analysis of Evaluation and System Limitations
- **URL**: https://arxiv.org/abs/2602.19320 — retrieved 2026-04-12
- **Abstract verbatim** (key passages):
  > "Despite rapid architectural development, the empirical foundations
  > of these systems remain fragile: existing benchmarks are often
  > underscaled, evaluation metrics are misaligned with semantic utility,
  > performance varies significantly across backbone models, and
  > system-level costs are frequently overlooked."
  > "benchmark saturation effects, metric validity and judge sensitivity,
  > backbone-dependent accuracy, and the latency and throughput overhead
  > introduced by memory maintenance."
  > "clarifies why current agentic memory systems often underperform
  > their theoretical promise"
- **Credibility**: high (independent critical survey, meta-analysis)
- **Relevance**: **load-bearing for the recommendation**. This paper
  explicitly says the benchmarks Mem0/Zep/MemOS all cite are broken.
  Any recommendation that leans on published LoCoMo numbers is weak.

### 2026-03-08 — Memory for Autonomous LLM Agents: Mechanisms, Evaluation, and Emerging Frontiers
- **Author**: Pengfei Du
- **URL**: https://arxiv.org/abs/2603.07670 — retrieved 2026-04-12
- **Proposed three-dim taxonomy**: temporal scope, representational
  substrate, control policy
- **Five mechanism families**:
  1. Context-resident compression
  2. Retrieval-augmented stores
  3. Reflective self-improvement
  4. Hierarchical virtual context
  5. Policy-learned management
- **Credibility**: high (independent, comprehensive)
- **Relevance**: orthogonal to "Memory in the Age of AI Agents" —
  different taxonomy, but both valid. Reflective self-improvement maps
  to H1 (ACE). Retrieval-augmented maps to H2/H3 (Zep/HippoRAG).
  Hierarchical virtual context maps to MemGPT/Letta (H4).

### 2026-03-17 — MemX: Local-First Long-Term Memory System for AI Assistants
- **URL**: https://arxiv.org/abs/2603.16171 — retrieved 2026-04-12
- **Architecture** (verbatim):
  > "implemented in Rust on top of libSQL and an OpenAI-compatible
  > embedding API, providing persistent, searchable, and explainable
  > memory for conversational agents"
  > "vector recall, keyword recall, Reciprocal Rank Fusion (RRF),
  > four-factor re-ranking, and a low-confidence rejection rule"
- **Benchmark** (verbatim): "Hit@1=91.3%... FTS5 full-text indexing
  reduces keyword search latency by 1,100x at 100k-record scale,
  keeping end-to-end search under 90 ms."
- **Credibility**: medium (paper exists, not widely cited yet, Chinese
  language benchmarks)
- **Relevance**: **direct match for Akash's local-first constraint**.
  Rust implementation, SQLite + FTS5 + vector + re-ranking. A
  concrete reference architecture.

### 2026-03-20 — Memori: A Persistent Memory Layer for Efficient, Context-Aware LLM Agents
- **URL**: https://arxiv.org/abs/2603.19935 — retrieved 2026-04-12
- **Architecture** (verbatim):
  > "memory as a data structuring problem... Advanced Augmentation
  > pipeline that converts unstructured dialogue into compact semantic
  > triples and conversation summaries."
- **Benchmark** (verbatim): "81.95% accuracy [on LoCoMo] with only 1,294
  tokens per query (~5% of full context)... 67% fewer tokens than
  competing approaches and over 20x savings compared to full-context
  methods"
- **Credibility**: medium (on LoCoMo, which is saturated)

### Additional 2026 notables (paper-title-level capture, not full abstract):
- **2026-04-09**: MemReader — "active memory extraction using GRPO
  optimization... state-of-the-art results on LOCOMO" (arxiv 2604.07877)
- **2026-04-09**: LightMem — "short-term, mid-term, and long-term" tiers
  (arxiv 2604.07798)
- **2026-04-08**: HingeMem — "event segmentation theory... 20% improvement
  on LOCOMO" (arxiv 2604.06845)
- **2026-04-06**: SuperLocalMemory V3.3 — "Fisher-Rao Quantization-Aware
  Distance" + "Ebbinghaus Adaptive Forgetting", zero-LLM memory
  (arxiv 2604.04514). Name-series (V3, V3.3) suggests single group
  publishing rapidly.
- **2026-03-17**: Chronos — "subject-verb-object event tuples with
  resolved datetime ranges, 95.60% accuracy" (arxiv 2603.16862)
- **2026-03-13**: Structured Distillation — "11x compression of
  conversation history to 38 tokens per exchange with 96% retrieval
  preservation" (arxiv 2603.13017)
- **2026-03-11**: Structured Linked Data as Memory Layer —
  "Schema.org markup and Linked Data with +29.6% accuracy"
  (arxiv 2603.10700)
- **2026-03-01**: Semantic XPath — "Tree-structured memory improving
  176.7% over flat-RAG while using 9.1% of tokens" (arxiv 2603.01160)
- **2026-03-02**: Diagnosing Retrieval vs. Utilization Bottlenecks —
  "retrieval is dominant factor spanning 20 points accuracy"
  (arxiv 2603.02473)

## Dissenting voices

### Zep's critique of Mem0 (2025-05-06, 2025-07-04)
- Zep published "Lies, Damn Lies, & Statistics: Is Mem0 SOTA in Agent
  Memory?" directly attacking Mem0's 26% claim. Details in
  `EVIDENCE/adversary.md`. Key claim: trivial full-context beats
  both, invalidating benchmark leadership claims.
- Also: "The AI memory wallet fallacy" (blog.getzep.com/the-ai-memory-wallet-fallacy/,
  HN 44458081, 2025-07-04, 12 points) — Zep argues against the
  "private memory layer" framing that Mem0 pushes.

### Letta's critique of RAG-as-memory (2025-02-13)
- Letta published "RAG is not agent memory" (www.letta.com/blog/rag-vs-agent-memory,
  retrieved 2026-04-12, HN 43039467). Key claim:
  > "RAG gets 'one shot' at retrieving the most relevant data and
  > generating a response."
  > "RAG is purely reactive" — won't retrieve "personalization
  > information that isn't semantically similar."
  > "RAG often places irrelevant data into the context window,
  > resulting in context pollution."
- Letta advocates: agent-directed tool-based memory access (their own
  MemGPT architecture). Self-interested, but the critique is technically
  sound.

### "Anatomy" paper (2026-02-22)
- The independent "Anatomy of Agentic Memory" paper (arxiv 2602.19320)
  is the most devastating: benchmarks saturated, metrics misaligned,
  backbone-dependent, cost-ignored. It names no specific systems but
  the critique lands on everyone publishing LoCoMo numbers.

### Awesome-AI-Memory curator's neutral stance
- The IAAR-Shanghai/Awesome-AI-Memory curator, when asked (via README
  meta-language) to identify "current best", explicitly **refuses** —
  frames memory as "a multidimensional design space balancing cost,
  accuracy, and architectural constraints." This is epistemic humility.

### Community voices on agent memory = files, not vector DBs
- Steve Yegge, "Beads: A coding agent memory system" (steve-yegge.medium.com,
  2025-10-13, HN 45382856, 19 points). Framing:
  > "Beads isn't 'issue tracking for agents' — it's external memory
  > for agents"
  > "writing the issues into git as JSONL lines, so you have the best
  > of both the database and the version-control worlds"
- HN Show-HN: "Agent memory is structured not fuzzy. why are we all
  using vector DBs for it?" (reddit.com crosspost, surfaced via HN,
  2026-03-04, 2 points — small signal but directionally convergent)
- Multiple SQLite-based projects: sqliteai/sqlite-memory (2026-04-07,
  9 points), sachinsharma9780/memweave (2026-04-05, 5 points).
- Letta's **Context Repositories** (2026-02-12, www.letta.com/blog/context-repositories)
  converges on the same pattern: agent memory is git-versioned files
  on local filesystem, LLM-curated.

## Synthesis — what prior art actually says

There are **five mechanism families** (borrowing the 2603.07670 survey
taxonomy), not one consensus answer:

1. **Context-resident compression**: fit more into a single context
   window via compression (Structured Distillation 2603.13017,
   LightThinker, gist tokens). Good for single-session long history.
2. **Retrieval-augmented stores**: Mem0, classic RAG, Memori, MemX.
   Vector + keyword + re-ranking. Industry-standard but broken on
   LoCoMo saturation.
3. **Reflective self-improvement**: ACE (2510.04618). LLM writes its
   own evolving playbook. Closest to Claude Code's Auto memory.
4. **Hierarchical virtual context**: MemGPT / Letta. Core (always in
   context) + archival (on-demand tool calls). Letta has pivoted to
   git-based file memory for coding agents.
5. **Policy-learned management**: BudgetMem (2602.06025), MemSkill
   (2602.02474), DeltaMem (2604.01560). Meta-learns what to remember.

The **convergent direction** for *coding agents specifically* (not
customer-support chatbots, not personal assistants) is:

- Memory = **files on a local filesystem**, not a vector DB
- **LLM self-curated** (reflection loop), not externally classified
- **Git-versioned**, not database-transacted
- A **two-tier structure** with a hot index + on-demand cold topic files
- **Hybrid retrieval** (FTS + vector + re-ranking) where retrieval is
  needed, but retrieval is *not the dominant operation* — navigation
  via filenames/folder structure is

This convergence is visible in: Claude Code Auto memory, Letta Context
Repositories, Steve Yegge's Beads, ACE (when used as "agent memory"
online mode), and the Claude Code skills mechanism that Akash already
runs. It is **not** the direction Mem0/Zep/MemOS are going (they are
all cloud-service-backed graph + vector databases).

## Confidence
**High**. 18 primary-source papers cited with verbatim quotes,
chronological ordering, credibility tagged, and convergent-vs-divergent
direction made explicit. The "benchmarks are broken" finding
(2602.19320, Zep's rebuttal of Mem0) is independently triangulated and
load-bearing for the recommendation.

## Handoff notes for adversary
- Mem0's 26% and MemOS's 43.7% claims on LoCoMo both need auditing.
  The Zep rebuttal is itself self-interested but surfaces real
  methodological holes.
- The Mem0 HN launch had a moderator-flagged astroturf cluster —
  corpus trust for Mem0 marketing is compromised.
- ACE's +10.6% is modest, bounded, and from a Stanford team not
  selling a product — highest trust.
- HippoRAG 2's +7% is from OSU NLP (Yu Su's group), peer-reviewed at
  ICML 2025 — high trust.
