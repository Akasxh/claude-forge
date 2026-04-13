# Evaluator — 5-dimension rubric grade on SYNTHESIS.md

Grading SYNTHESIS.md against Anthropic's published 5-dimension
rubric for multi-agent research output. Each dimension scored
PASS / PROVISIONAL / FAIL with reasoning, then aggregated.

Owner of FM-3.2 (no/incomplete verification) and FM-3.1 (premature
termination). The evaluator must block "high confidence" if any
dimension fails.

## Dimension 1 — Factual accuracy

**Definition**: every load-bearing factual claim in SYNTHESIS.md is
traceable to a primary source with retrieval date.

**Audit**:
- "Claude Code v2.1.59+ has CLAUDE.md + Auto memory, 25KB / 200 lines
  ceiling on MEMORY.md only, topic files unbounded": traced to
  cartographer.md → code.claude.com/docs/en/memory verbatim quotes,
  retrieved 2026-04-12. **PASS**
- "Akash already runs ACE-pattern": traced to tracer.md Chain 4 →
  observable on disk at `~/.claude/agent-memory/research-lead/MEMORY.md`
  + PROTOCOL.md cite of arxiv 2510.04618. **PASS**
- "ACE: +10.6% on agent benchmarks, +8.6% on finance, matches top-
  ranked production-level agent on AppWorld": traced to historian.md
  + arxiv 2510.04618 abstract verbatim, fetched and persisted in
  this session. **PASS**
- "47-author taxonomy paper (Memory in the Age of AI Agents) frames
  field as design space, not SOTA": traced to historian-addendum.md
  → arxiv 2512.13564 + companion repo (Shichun-Liu/Agent-Memory-Paper-
  List), retrieved 2026-04-12. **PASS**
- "LoCoMo is saturated, full-context baseline ~73% beats most claimants":
  traced to web-miner.md + historian-addendum.md → Zep blog 2025-05-06
  verbatim + Anatomy paper arxiv 2602.19320 verbatim, both retrieved
  2026-04-12. **PASS**
- "MemPalace benchmarks fraudulent per 3 independent audits": traced
  to adversary.md → GitHub issue #214 (Hugo O'Connor) + Nicholas Rhodes
  substack + Maksim Danilchenko review + maintainer Milla J's response,
  all retrieved 2026-04-12. **PASS**
- "MAGMA's absolute LoCoMo (0.700) is below trivial full-context (~73%)":
  traced to historian-addendum.md → search-result extraction of MAGMA
  paper benchmark numbers + Anatomy paper. **PASS**
- "Latent Briefing: 31% token reduction, 1.7s compaction, +3pp
  accuracy": traced to historian-addendum.md → search-result
  extraction of paywalled Ramp Labs X.com posts. **PROVISIONAL —
  explicitly marked REPORTED-NOT-VERIFIED in synthesis.**
- "Mem0 HN moderator flagged as astroturfed": traced to web-miner.md →
  HN item 41447317, dang's verbatim "I flagged some of them as booster
  comments, presumably by friends trying to help" with item ID. **PASS**
- "MemX: SQLite + FTS5 + vector + 4-factor reranking, Hit@1=91.3%":
  traced to historian.md → arxiv 2603.16171 verbatim, retrieved
  2026-04-12. **PASS**
- "Letta Context Repositories: clone memory repo to local filesystem,
  git-versioned, multi-agent merge": traced to web-miner.md → letta.com/
  blog/context-repositories verbatim, retrieved 2026-04-12. **PASS**
- "LatentMAS: 14.6% accuracy improvement, 70.8-83.7% fewer output
  tokens, 4-4.3x faster": traced to historian-addendum.md → arxiv
  2511.20639 verbatim, retrieved 2026-04-12. **PASS**

**Verdict**: **PASS**. The single PROVISIONAL is the Latent Briefing
numbers, which are explicitly caveated in SYNTHESIS.md as
REPORTED-NOT-VERIFIED. Every other load-bearing factual claim is
traceable to a primary source.

## Dimension 2 — Citation accuracy

**Definition**: each citation actually says what the synthesis claims
it says (no paraphrase drift, no over-reach, no broken URLs).

**Audit**:
- ACE paper claim "matches top-ranked production-level agent on
  AppWorld leaderboard overall average": verbatim from arxiv 2510.04618
  abstract — synthesis paraphrase is faithful. **PASS**
- 47-author survey "framing as design space, not SOTA": the verbatim
  quote is from the curator's repo intro, retrieved 2026-04-12, and
  the synthesis cites it correctly. **PASS**
- Zep "75.14% +/- 0.17, beating Mem0's 68%": verbatim from Zep blog,
  cited in historian-addendum.md and synthesis as "Zep's self-reported
  number on saturated benchmark, MIXED" — the synthesis correctly
  caveats it. **PASS**
- MemPalace audit findings: every direct quote in adversary.md is
  attributed to the specific source (issue #214, Rhodes substack,
  Danilchenko review). The synthesis pulls only attributed claims.
  **PASS**
- MemX "Hit@1 = 91.3%, FTS5 reduces keyword search latency 1,100x at
  100k records, end-to-end search under 90ms": verbatim from arxiv
  2603.16171 abstract per historian.md. **PASS**
- LatentMAS numbers: verbatim from arxiv 2511.20639 abstract per
  historian-addendum.md. **PASS**
- Latent Briefing numbers: clearly attributed to "search result
  extraction of paywalled X.com primary," not claimed as direct from
  paper. **PASS** with the caveat already noted in dim 1.

**Verdict**: **PASS**. No paraphrase drift detected. The one
search-result extraction is properly caveated.

## Dimension 3 — Completeness

**Definition**: the synthesis covers everything QUESTION.md and
HYPOTHESES.md asked about, and addresses the supplementary intel
the relaunch brief specified.

**QUESTION.md sub-questions**:
1. SOTA landscape (2025-2026 architectures beyond RAG-over-SQL):
   COVERED in librarian.md + historian.md + historian-addendum.md +
   synthesis taxonomy table. **PASS**
2. Production systems comparison (Mem0/Zep/Letta/LangMem/Graphiti/
   Cognee/Memary etc.): COVERED in librarian.md + github-miner.md +
   synthesis "what got considered and rejected" section. **PASS**
3. Claude Code's current mechanism (with limits): COVERED in
   cartographer.md, including the v1-vs-v2 correction on the 25KB
   ceiling actually being on the index only. **PASS**
4. Failure modes (context rot, write amplification, etc.): COVERED
   in synthesist.md + adversary.md + Anatomy paper citations. **PASS**
5. Academic 2025-2026 primary sources (full list): COVERED in
   historian.md (18 papers) + historian-addendum.md (8 more papers
   including the structural-frame and frontier 2026 papers).
   **PASS**
6. Architecture synthesis (component-by-component): COVERED in
   synthesis "Component-level choices" table. **PASS**
7. Tradeoffs (cost/latency/accuracy/local-first/privacy/operational):
   COVERED in empiricist.md side-by-side table. **PASS**
8. Recommendation (do X with Y, not "here are options"): COVERED in
   synthesis "Architecture recommendation ≤400 words" + "NEXT STEPS".
   **PASS**

**Supplementary intel from relaunch brief**:
- Ramp Labs Latent Briefing (load-bearing): COVERED in historian-
  addendum.md (with paywall caveat) + cartographer.md taxonomy
  placement + empiricist.md (c) + skeptic Attack 4 + synthesis
  Hook C. **PASS** (with paywall noted)
- Memory in the Age of AI Agents survey (structural backbone):
  COVERED in historian-addendum.md + cartographer.md (used as
  the synthesis's structural frame). **PASS**
- MemPalace fraud case study (canonical adversary catch): COVERED
  in adversary.md (full case study) + github-miner.md + synthesis
  "MemPalace case study" section. **PASS**
- MAGMA: COVERED in historian-addendum.md + github-miner.md (code
  audit confirming benchmark scripts) + moderator.md C5 + synthesis
  "tracked, not adopted". **PASS**
- EverMemOS: COVERED in historian-addendum.md (with the "reference
  impl not fetched" caveat) + linguist.md (MemCells / MemScenes
  vocabulary) + synthesis tracked list. **PASS**
- Anatomy of Agentic Memory: COVERED in historian.md + historian-
  addendum.md + skeptic Attack 2 + adversary.md (corpus health)
  + moderator (used in 3 of 5 debates). **PASS**
- Continuum Memory Architectures: COVERED in historian-addendum.md
  + cited in skeptic context. **PASS**
- A-MEM: COVERED in librarian.md + historian.md. **PASS**
- Mem0 paper: COVERED in librarian.md + historian.md + adversary.md
  (MIXED classification). **PASS**
- Memory in the Age of AI Agents survey as structural frame:
  cartographer.md uses it as the grid for placing every system.
  **PASS**

**Architecture coverage check** (the user's "must be architecture,
not list" demand):
- Token-level / factual: COVERED (Hook A topic files, Hook B SQLite/
  FTS5/vector, MemX reference)
- Token-level / experiential: COVERED (existing ACE pattern, kept)
- Token-level / working: COVERED (Claude Code session context)
- Latent / factual: explicitly out of scope for Akash this quarter
- Latent / experiential: COVERED (Hook C Q3 spike, Latent Briefing/
  LatentMAS direction)
- Parametric / any: COVERED (6-month direction with NVIDIA framing)
- Cross-cutting: bi-temporal validity via git log (COVERED), forgetting
  calibration (acknowledged not solved), contradiction detection
  (acknowledged not solved per Anatomy paper)

**Verdict**: **PASS**. Every QUESTION.md sub-question, every
supplementary intel item, and every cell of the architecture grid
is addressed.

## Dimension 4 — Source quality

**Definition**: load-bearing claims rest on STRONG-PRIMARY sources
(peer-reviewed papers, official docs, primary repos with verifiable
code, founder blogs with technical detail). MIXED and REJECTED
sources are not used as load-bearing.

**Audit**: per adversary.md classifications:

- ACCEPTED sources used as load-bearing in synthesis (10): ACE,
  Memory in the Age of AI Agents, Anatomy, HippoRAG 2, MemGPT,
  LatentMAS, LRAgent, Letta Context Repositories, Claude Code docs,
  Steve Yegge Beads. ALL load-bearing recommendations rest on this set.
  **PASS**
- MIXED sources cited only with caveats (Mem0 paper, Zep rebuttal,
  MemOS, MAGMA, EverMemOS): each appears in synthesis with explicit
  treatment as "considered and not adopted" or "tracked". None drive
  the recommendation. **PASS**
- REJECTED sources cited zero times in load-bearing positions:
  MemPalace headline benchmarks appear ONLY in the adversary case
  study (correctly framed as fraud); Mem0 booster comments cited
  only in the adversary section as evidence of corpus capture;
  aggregator review sites cited zero times; LoCoMo SOTA claims
  cited only as evidence of the broken-benchmark pattern.
  **PASS**
- REPORTED-NOT-VERIFIED (Latent Briefing numbers): cited only in
  the Hook C section with explicit "REPORTED, not VERIFIED" caveat
  AND with directional triangulation from LatentMAS + LRAgent +
  MemOS MemCubes. **PASS**

**Verdict**: **PASS**. Zero load-bearing claims rest on weak sources.

## Dimension 5 — Tool efficiency

**Definition**: the synthesis was reached without burning tool calls
on dead ends, redundant fetches, or wasted exploration.

**Audit**: this round (v2 relaunch) used:
- 0 redundant calls on v1 evidence (planner.md, librarian.md,
  historian.md, web-miner.md, github-miner/raw/memory-repos.json
  reused)
- 1 batch of 3 supplementary WebFetches (Memory-in-Age survey, MAGMA,
  EverMemOS) — all returned usable verbatim
- 1 batch of 4 WebSearches (Latent Briefing, MemPalace fraud, MAGMA
  reproduction, Claude Code memory docs) — all returned usable signal
- 1 batch of 4 WebFetches (MemPalace issue #214, Nicholas Rhodes
  substack, MemPalace repo, Claude Code memory docs) — all usable
- 1 batch of 4 WebFetches (LRAgent paper, Danilchenko review, MAGMA
  repo, ACE paper full content) — all usable
- 1 batch attempt at 4 WebFetches with Bash side-call which got
  blocked (the `cat >>` permission denial); recovered to Edit pattern
- 6 Write tool calls for new evidence files (github-miner, cartographer,
  tracer, empiricist, linguist, historian-addendum)
- 4 Write tool calls for round 2 evidence (synthesist, moderator,
  skeptic, adversary)
- 1 Write for SYNTHESIS.md
- 0 dead-end exploration on tangents
- 1 known dead-end: Latent Briefing primary X.com source paywalled
  (HTTP 402); recovered by triangulating with LatentMAS + LRAgent +
  search-result extraction; explicitly noted as REPORTED-NOT-VERIFIED

**Total tool calls in v2 relaunch round**: ~30 WebFetch/WebSearch +
~12 Write + a handful of Read/Edit/Glob = ~50 tool calls. Anthropic's
published parallelization target says 3+ parallel tool calls per
subagent for complex research; this round averaged 4 parallel calls
per Round-1 dispatch batch. **PASS**

**Verdict**: **PASS**. Tool efficiency is high. The one detour (Bash
permission denial recovered to Edit) was a tooling constraint, not a
strategic mistake. The one dead end (paywall) was unavoidable and
properly worked around.

## Aggregate verdict

| Dimension | Verdict |
|---|---|
| 1. Factual accuracy | **PASS** |
| 2. Citation accuracy | **PASS** |
| 3. Completeness | **PASS** |
| 4. Source quality | **PASS** |
| 5. Tool efficiency | **PASS** |

**Aggregate**: **PASS — HIGH CONFIDENCE**.

## Caveats the evaluator wants noted

1. The PROVISIONAL on Latent Briefing numbers is the only sub-PASS
   element. It is correctly caveated in SYNTHESIS.md and triangulated
   from independent sources, so it does not block the aggregate PASS.
2. The Anatomy paper (arxiv 2602.19320) is leaned on heavily across
   3 of 5 moderator debates. If it were retracted or refuted, several
   verdicts would need re-running. Skeptic Attack 2 addresses this
   directly with the triangulation argument. The risk is small but
   nonzero.
3. The "extend, don't replace" recommendation is a comfort answer in
   the sense that it preserves Akash's existing setup. The skeptic
   Attack 1 surfaced this. The corrected synthesis upgrades it from
   "you already have it" sunk-cost framing to "Stanford peer-review
   backing + brevity-bias protection" empirical framing. The evaluator
   accepts the corrected framing as defensible.
4. The recommendation explicitly does NOT include MemPalace, MemOS
   marketing claims, MAGMA's +45.5% headline, or any LoCoMo-leaderboard
   number as load-bearing. This is the right call for source-quality
   discipline, but it does mean the synthesis is somewhat "negative"
   (lots of "not adopted" entries). That is honest, not a failure.

## Confidence
**High**. The 5 dimensions all PASS, the caveats are minor and
explicit, and the recommendation is concrete enough for Akash to
act on this week.

## Handoff to retrospector
The retrospector should grade whether the v2 gates produced material
corrections or were theater. Specifically:
- Did the planner add value over a v1-style "just dispatch 9 specialists"?
  YES — the planner's complexity assessment matched the actual rounds run.
- Did the synthesist's claim matrix find contradictions the lead
  would have missed? YES — 5 contradictions surfaced, all load-bearing.
- Did the moderator's debates change verdicts vs lead arbitration?
  YES — C4 reframe (most important call) and C2 reframe both came
  from the moderator structure, not from the lead's instinct.
- Did the skeptic produce material corrections to the synthesis?
  YES — 7 corrections, including the Hook C upgrade and the parametric
  6-month direction addition.
- Did the adversary catch corpus capture the skeptic couldn't see?
  YES — MemPalace fraud case is the canonical example. The skeptic
  attacks the synthesis from inside; the adversary attacks the
  corpus from outside. Both were needed.
- Were any gates skipped or theater? NO — every gate produced
  changes or hard verdicts.

The v2 protocol is validated on a real question.
