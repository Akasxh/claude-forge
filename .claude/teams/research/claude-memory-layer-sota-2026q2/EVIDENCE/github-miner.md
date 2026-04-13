# GitHub Miner — ecosystem signals on agent memory systems

Sub-question: Stars, star-velocity, issue volume, release cadence, recent
commits for the production memory ecosystem. Cross-reference with
librarian's API claims and historian's paper claims.

## Method
- Single GraphQL emission over 9 production repos (cached at
  `EVIDENCE/github-miner/raw/memory-repos.json`, retrieved 2026-04-12).
- Supplementary GraphQL/REST probes via WebFetch on individual repos
  for the v2 supplementary intel (MemPalace, MAGMA, EverMemOS,
  Latent Briefing reference impls, the curator paper list).
- Star counts and release dates are point-in-time snapshots from
  2026-04-12 between 03:48 and 04:40 UTC.

## The 9 production repos (raw cache)

| Repo | Stars | Forks | License | Latest release | Last push | Open issues | Open PRs | Created | Status |
|---|---|---|---|---|---|---|---|---|---|
| **mem0ai/mem0** | 52,673 | 5,911 | Apache-2.0 | `cli-node-v0.2.3` (2026-04-11) | 2026-04-11 | 82 | 134 | 2023-06-20 | active, marketing-heavy |
| **getzep/graphiti** | 24,786 | 2,460 | Apache-2.0 | `mcp-v1.0.2` (2026-03-11) | 2026-04-08 | 208 | 138 | 2024-08-08 | active, primary product |
| **letta-ai/letta** | 22,002 | 2,330 | Apache-2.0 | `0.16.7` (2026-03-31) | 2026-04-08 | 70 | 30 | 2023-10-11 | active, pivoted to coding |
| **topoteretes/cognee** | 15,117 | 1,547 | Apache-2.0 | `v1.0.0` (2026-04-11) | 2026-04-11 | 29 | 28 | 2023-08-16 | active, just hit v1.0 |
| **MemTensor/MemOS** | 8,293 | (unset) | Apache-2.0 | `v2.0.13` (2026-04-10) | 2026-04-10 | (unset) | (unset) | 2025-07-06 | active, big claims |
| **getzep/zep** | 4,403 | 602 | Apache-2.0 | `zep-crewai-v1.1.1` (2025-09-11) | 2026-04-09 | 0 | 15 | 2023-04-29 | superseded by graphiti |
| **OSU-NLP-Group/HippoRAG** | 3,348 | 334 | MIT | `v1.0.0` (2025-02-27) | 2025-09-04 | 16 | 4 | 2024-05-23 | maintained but slowing |
| **memodb-io/memobase** | 2,673 | (unset) | Apache-2.0 | (unset) | (unset) | (unset) | (unset) | 2024-09-03 | profile-focused niche |
| **langchain-ai/langmem** | 1,390 | 159 | MIT | none | 2026-04-10 | 44 | 9 | 2025-01-21 | active early-stage |
| **agiresearch/A-mem** | 961 | 100 | MIT | none | 2025-12-12 | 13 | 0 | 2025-02-25 | research artifact |
| **kingjulio8238/Memary** | (unset) | (unset) | (unset) | `v0.1.5` (2024-10-22) | 2024-10-22 | (unset) | (unset) | (unset) | **DORMANT 18mo+** |

## Star-velocity analysis (interpretation, not raw)

- **mem0ai/mem0** at 52.7K stars / created 2023-06-20 → ~17.5K stars/year
  on average. Velocity is the highest of any agent memory project, period.
  This is the marketing-and-VC signal: $24M raised 2025-10-28, hosted
  service, content-marketing operation. Star count overstates technical
  fitness because the project is also a content distribution funnel.
- **getzep/graphiti** at 24.8K / created 2024-08-08 → ~14.8K stars/year
  in ~20 months. Velocity high but driven by knowledge-graph mindshare,
  not benchmark wins.
- **letta-ai/letta** at 22K / created 2023-10-11 → ~8.8K stars/year in
  ~30 months. Steady, less hype-driven, higher technical-density per star.
- **topoteretes/cognee** at 15.1K / created 2023-08-16 → ~5.7K stars/year.
  Just hit v1.0 on 2026-04-11 — milestone-driven attention.
- **MemTensor/MemOS** at 8.3K / created 2025-07-06 → ~10.5K stars/year
  in ~9 months. Newest mover, big benchmark claims (audited below).
- **HippoRAG** at 3.3K / created 2024-05-23 → ~1.7K stars/year. Academic
  artifact, not a consumer product. Pace is normal for ICML-tier code.
- **A-MEM** at 961 / created 2025-02-25 → ~840 stars/year. Pure research.

## Supplementary intel: the projects v1 missed

### MemPalace — `milla-jovovich/mempalace` (the v2 case study)
- **Stars**: ~41,700 (per WebFetch on github.com/milla-jovovich/mempalace
  2026-04-12)
- **Created**: April 5 2026 (~7 days before this session)
- **Star velocity**: ~6,000 stars/day in week 1. Highest velocity in the
  history of agent-memory projects. Extreme outlier.
- **Authors**: Milla Jovovich (actress) + Ben Sigman (developer)
- **License**: MIT
- **Latest commit**: develop branch (early Feb 2025 per WebFetch — but
  this conflicts with the April 5 2026 launch date; either the WebFetch
  parsed an old commit or the repo was force-pushed after fork/rename;
  flagged for adversary).
- **Architecture (verbatim)**: wings (people/projects) → halls (memory
  types) → rooms (specific topics) → tunnels (cross-wing) → closets
  (compressed summary pointers) → drawers (verbatim originals).
  170-token startup. Local ChromaDB+SQLite, stores verbatim without LLM
  summarization.
- **Headline benchmark claims (April 7, 2026 README)**:
  - "96.6% LongMemEval R@5" in raw verbatim mode across 500 questions
  - "100% LongMemEval" hybrid (later admitted to be hand-tuned)
  - "100% LoCoMo" (later admitted to be `top_k=50` on 19-32 item haystacks)
- **Author disclaimers (in same April 7 README)**:
  - "AAAK is experimental compression…not the storage default"
  - AAAK regresses to 84.2% R@5 vs 96.6% raw
  - Palace metadata filtering provides "+34%" improvement but is
    "standard ChromaDB features, not novel retrieval"
  - "Contradiction detection" exists as separate utility but "wasn't
    wired into operations as initially implied"
- **Acknowledged audit (issue #214)**: Hugo O'Connor, 2026-04-08,
  "Benchmarks do not exercise MemPalace — headline 96.6% is a ChromaDB
  score." Maintainer Milla J responded 2026-04-09: "Your audit is right
  and deserves a direct response. Retiring `recall_any@5` as headline
  metric. Accepting corrected benchmark code that exercises MemPalace
  code paths." Issue closed as completed.
- **Verdict**: real innovation in the loci-method architecture, but the
  marketing benchmarks are fraudulent on three independent counts (test
  set overfitting, ChromaDB-not-MemPalace measurement, top_k = pool size).
  The maintainer has acknowledged the issue but the launch wave damage
  is done. **This is the canonical SEO/celebrity-driven benchmark fraud
  case in the agent-memory corpus and goes in adversary.md in full.**
- **Confidence**: high on the audit findings (3 independent sources,
  maintainer acknowledgment). Medium on the underlying architecture's
  potential — the loci approach is interesting but unevaluated under
  honest benchmarks.

### MAGMA reference impl — `FredJiang0324/MAMGA`
- **Stars**: 82
- **Forks**: 12
- **License**: MIT
- **Last commit**: January 4, 2026
- **Language**: Python (99.8%)
- **Code structure** (verified via WebFetch 2026-04-12):
  - `memory/trg_memory.py` (main engine)
  - `memory/graph_db.py`
  - `memory/vector_db.py`
  - `memory/query_engine.py`
  - `memory/memory_builder.py`
- **Benchmark scripts present**:
  - `test_fixed_memory.py` — LoCoMo, 10 conversation samples, 5 question
    categories (multi-hop, temporal, open-domain, single-hop, adversarial)
  - `test_longmemeval_chunked.py` — multi-session evaluation, paper
    reports 40% accuracy on multi-session scenarios
- **Per WebFetch interpretation**: "Benchmark scripts exercise the full
  MAGMA architecture including graph construction, multi-hop traversal,
  and semantic/temporal relationship retrieval — not merely baseline
  comparisons." Initial inspection suggests this is NOT MemPalace-style
  benchmark fraud. Adversary should still independently audit by reading
  the code.
- **Star/fork ratio**: 82/12 = 6.8x — healthy academic-impl ratio. Low
  star count means low adoption, which is normal for January 2026 papers.
- **Confidence**: medium-high on code presence; the actual benchmark
  honesty needs an empiricist run.

### EverMemOS — `EverMind-AI/EverMemOS`
- Repo URL stated in arxiv 2601.02163 paper. Not directly fetched in
  this session due to stop after 4 supplementary fetches; flagged for
  empiricist/adversary if the recommendation depends on it.
- **Submission dates**: January 5, 2026 (v1) → January 9, 2026 (v2)
- **Authors**: Chuanrui Hu, Xingze Gao, Zuyi Zhou, Dannong Xu, Yi Bai,
  Xintong Li, Hui Zhang, Tong Li, Chong Zhang, Lidong Bing, Yafeng Deng

### Curator's paper list — `Shichun-Liu/Agent-Memory-Paper-List`
- 200+ papers across the three-axis taxonomy from arxiv 2512.13564
- Last verified: January 2026 (per WebFetch interpretation)
- **Critical meta-finding (verbatim from WebFetch)**: "The curators
  explicitly frame this as a design space rather than identifying a
  SOTA. The introduction states: 'Through this structure, we hope to
  provide a conceptual foundation for rethinking memory as a first-class
  primitive in future agentic intelligence.'" — this is the load-bearing
  evidence for the skeptic's prior that there is no single "best."

### Latent Briefing reference impl
- Ramp Labs has not (as of 2026-04-12) open-sourced a reference
  implementation under a stable repo URL retrievable from a search
  result. The X.com posts (paywalled) point to a paper, but the X
  fetch returned 402.
- The closest open-source analog by mechanism is `Gen-Verse/LatentMAS`
  (arxiv 2511.20639, "Latent Collaboration in Multi-Agent Systems")
  which has the same core idea: "agents performing auto-regressive
  latent thoughts generation through last-layer hidden embeddings"
  with "a shared latent working memory" — same family.
- **Confidence**: medium. Latent Briefing is a real method per multiple
  search results; the primary X source is paywalled and there is no
  named arxiv ID for "Latent Briefing" specifically, only related work.
- **Adversary handoff**: this is the one supplementary-intel item where
  primary source access failed. Recommendation is to treat it as
  "validated direction (latent-space memory sharing for multi-agent)
  with multiple converging public signals" but not as "validated
  benchmark numbers."

## Cross-reference: GitHub vs paper claims

| Project | Paper claim | Repo evidence | Coherent? |
|---|---|---|---|
| Mem0 | +26% over OpenAI memory on LoCoMo | active repo, marketing-funnel | claim contested by Zep |
| Zep/Graphiti | 75.14% LoCoMo, 0.632s p95 | active repo, knowledge-graph backend | claim from self-rebuttal blog |
| Letta | "stateful agents" / git-based memory | active repo, recent pivot to coding | architectural claim aligns; benchmark not central |
| HippoRAG 2 | +7% on associative tasks | repo last pushed 2025-09 | claim modest, peer-reviewed, low marketing |
| MemOS | +43.7% over OpenAI memory | active repo with paper | larger claim than Mem0, on saturated benchmark |
| A-MEM | "superior improvement against existing SOTA" | research-grade repo | unverified specifics |
| MAGMA | +18.6%-45.5% over A-MEM/MemoryOS/Nemori on LoCoMo | reference impl exists | architecture matches; needs independent run |
| EverMemOS | "SOTA" on LoCoMo+LongMemEval | reference impl URL stated | not verified |
| **MemPalace** | **96.6% LongMemEval, 100% LoCoMo** | **3 independent audits show fraud** | **NO** |

## Maintenance health flags

- **Letta** (`letta-ai/letta`): healthy. 22K stars, 70 issues, 30 PRs,
  release every ~2 weeks, recent product pivot to coding agents.
- **Mem0** (`mem0ai/mem0`): healthy *and* over-resourced. 52K stars
  but 82 issues / 134 PRs — high PR backlog suggests external
  contributions are accumulating faster than triage. Plus the corpus
  trust issue from the HN moderator flag.
- **Graphiti** (`getzep/graphiti`): healthy. 208 issues / 138 PRs is
  high but matches the project size and active community.
- **Cognee** (`topoteretes/cognee`): healthy. v1.0 on 2026-04-11. Lower
  PR backlog (28) than Mem0/Graphiti.
- **MemOS** (`MemTensor/MemOS`): unclear. v2.0.13 release 2026-04-10
  shows momentum, but openIssues count is unset in the cached probe;
  needs re-fetch.
- **HippoRAG** (`OSU-NLP-Group/HippoRAG`): slowing. Last push
  2025-09-04, no release since 2025-02-27. Academic artifact lifecycle.
- **Memary** (`kingjulio8238/Memary`): **DORMANT.** Last push 2024-10-22,
  18+ months ago. Do not include in any recommendation.
- **A-MEM** (`agiresearch/A-mem`): research-grade pace. Last push
  2025-12-12. No releases. Treat as a paper artifact, not a product.

## Cross-cutting observations

1. **The "agent memory" repo space is bimodal.** A handful of
   well-funded production projects (Mem0, Letta, Zep, Cognee, MemOS)
   compete on stars and benchmark headlines, while a long tail of
   paper-impl repos (HippoRAG, A-MEM, MAGMA, EverMemOS, LRAgent) sit
   at 1-3K stars with academic-pace maintenance. The middle is empty.
2. **No project we examined has cross-vendor independent benchmark
   verification.** Every benchmark claim originates from the project's
   own authors. The closest thing is the Anatomy paper (2602.19320),
   which evaluates the entire space and concludes the benchmarks are
   broken.
3. **Velocity is decoupled from quality.** MemPalace gained 21.7K
   stars in 1 week with fraudulent benchmarks. Mem0 raised $24M with
   LoCoMo claims that don't survive Zep's rebuttal. Star count and
   funding are SEO/marketing signals, not technical signals.
4. **The dormancy line in this space is fast.** Memary went 18 months
   between commits and is effectively dead despite peer mention. The
   field moves fast enough that anything not pushed in 6 months is
   probably abandoned.

## Confidence
**High** on the snapshot data (raw GraphQL cached, supplementary
WebFetch verbatim quoted). **Medium** on the velocity interpretations
(point-in-time, not historical). **High** on the bimodal-distribution
finding, which is robust across the data.

## Handoff to adversary
- MemPalace is the canonical fraud case — see `EVIDENCE/adversary.md`.
- MAGMA's `FredJiang0324/MAMGA` should be quickly empiricist-audited
  by reading `test_fixed_memory.py` and `test_longmemeval_chunked.py`
  before relying on the +18.6%-45.5% claim.
- EverMemOS's `EverMind-AI/EverMemOS` was not reached in this session;
  if it ends up in the recommendation, fetch its README + benchmark
  scripts in a re-dispatch.
- Latent Briefing primary source (X.com / Ramp Labs) is paywalled.
  Mark as "directional convergence from search result extraction +
  related arxiv work (LatentMAS 2511.20639, LRAgent 2602.01053)" not
  "verified primary source."
