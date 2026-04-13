# SYNTHESIS — Memory layer for Claude (SOTA 2026-Q2)

**Lead**: research-lead (adopted-persona mode, v2 protocol)
**Slug**: claude-memory-layer-sota-2026q2
**Session date**: 2026-04-12
**Confidence**: HIGH on the architecture, MEDIUM on Hook C numbers
(Latent Briefing primary source paywalled)

## Answer in one paragraph

Claude Code's existing `memory: user` mechanism + Akash's research-team
ACE-pattern (research-lead generator, retrospector reflector, scribe
curator, MEMORY.md playbook) is **already a working implementation of
the strongest published agent-memory pattern** (ACE, arxiv 2510.04618,
Stanford). The recommendation is **not** to replace it. The
recommendation is to **extend it along the cells of the
Memory-in-the-Age-of-AI-Agents 3-axis taxonomy** (arxiv 2512.13564)
that his current setup partially or doesn't cover, in three
time-boxed phases:

- **This week**: Hook A — extend `research-scribe` to write topic files
  for cold-tier facts, not just dedupe `MEMORY.md`. Zero new infra.
- **This month (conditional)**: Hook B — local SQLite + FTS5 + small
  embedding column over the topic files, exposed to specialists via a
  custom tool. Only build if Hook A's filename-navigation proves
  empirically insufficient.
- **Q3 spike**: Hook C — prototype Latent Briefing / LatentMAS-style
  KV-cache handoff between specialists, using Akash's existing vLLM
  background with a self-hosted Qwen-14B / Llama-3.1-70B worker.
  Time-box to one evening; ship the prototype only if it shows
  measurable savings on his actual workload.
- **6-month direction**: parametric memory — distill stable lessons
  from `MEMORY.md` into a small LoRA fine-tune of a worker model,
  hybridizing token-level + parametric storage.

This is both "more than just SQL" (it adds cold-tier search, latent-
state sharing, and a parametric direction) and a defense of what
Akash already shipped (he doesn't throw away the ACE-pattern that
already works for him).

## Confidence justification

**HIGH confidence** rests on:
- All 4 v2 round-2 gates ran (synthesist, moderator on 5 contradictions,
  skeptic, adversary)
- Multiple independent sources converge on the recommendation:
  ACE paper (Stanford), Letta Context Repositories, Beads (Steve
  Yegge), Claude Code official docs, multiple Show-HN SQLite projects
- The "no single SOTA, frame as design space" position is the
  curator's own framing for the canonical 47-author taxonomy paper
- All load-bearing benchmark contestations are independently
  triangulated (Anatomy paper + Zep rebuttal + MemPalace fraud +
  full-context baseline finding)
- The MemPalace fraud case is documented across 3 independent audits
  + maintainer acknowledgment; the corpus pattern of "celebrity /
  funding lift correlates with benchmark inflation" is observable
- Adversary rejected only marketing-flavored benchmark numbers;
  every synthesis claim cites an ACCEPTED source

**MEDIUM confidence on Hook C numbers** because the Latent Briefing
primary source (X.com) is paywalled. The direction (latent-state
sharing for multi-agent context) is converged across LatentMAS
(arxiv 2511.20639, peer-credible), LRAgent (arxiv 2602.01053,
peer-credible), and MemOS MemCubes (arxiv 2507.03724) — these
provide directional validation. Specific numbers from Ramp Labs
(31% token reduction, 1.7s compaction, +3pp accuracy) are REPORTED,
not VERIFIED.

## The taxonomy frame (load-bearing structural backbone)

From "Memory in the Age of AI Agents" (arxiv 2512.13564, 47-author
consortium led by Yuyang Hu, retrieved 2026-04-12):

**Three axes**:
1. **Forms** (storage substrate): token-level, parametric, latent
2. **Functions** (purpose): factual, experiential, working
3. **Dynamics** (lifecycle): formation, evolution, retrieval

**Critical curator framing** (verbatim from the companion paper-list
repo, github.com/Shichun-Liu/Agent-Memory-Paper-List, retrieved
2026-04-12):
> "The curators explicitly frame this as a design space rather than
> identifying a SOTA."

**This is the load-bearing prior**: the answer is not "use system X."
The answer is "map the workload onto the cells of the design space
and pick what fits each cell."

### Where every system sits in the grid

| | Token-level | Parametric | Latent |
|---|---|---|---|
| **Factual** | Mem0, Cognee, Graphiti, MAGMA, HippoRAG 2 | NVIDIA "context as training data" | KV-cache for facts (rare) |
| **Experiential** | **ACE, MemGPT/Letta, A-MEM, EverMemOS, Claude Code MEMORY.md** | Learned policies / MemSkill | **Latent Briefing, LatentMAS, LRAgent** |
| **Working** | session context window | (N/A — working = transient) | KV cache for current session |

### Where Akash's existing setup sits

- **Token-level / experiential**: COVERED. Research-lead/retrospector/
  scribe is an ACE implementation. `MEMORY.md` (7,260 bytes, 7 lessons)
  is the playbook.
- **Token-level / factual**: PARTIALLY COVERED. CLAUDE.md and project
  files cover entity-rich domain knowledge that is human-authored;
  durable lessons from sessions live in MEMORY.md but long-tail facts
  with low recency don't have an obvious home.
- **Token-level / working**: COVERED by the Claude Code session
  context window itself.
- **Latent / experiential**: NOT COVERED. Becomes relevant when
  multi-agent fanout is wide.
- **Parametric**: NOT COVERED. Far-future for high-update-rate workloads.

### What "extend, don't replace" means concretely

The three hooks below are the cells the recommendation adds.

## Architecture recommendation (≤400 words)

**Phase 1 — Hook A (this week, zero new infrastructure)**

Extend `research-scribe`'s curator behavior in
`~/.claude/agents/research/research-scribe.md` to additionally route
overflow detail to topic files when the retrospector emits a lesson
that is too long-tail for the 25KB index. The topic files live at
`~/.claude/agent-memory/research-lead/<topic>.md`, alongside the
existing `MEMORY.md`. The MEMORY.md index references topic files by
filename so that `research-lead` (and other specialists at user scope)
can read them on demand via standard file tools. **This is a
behavior change to one agent file; no new infrastructure, no new
dependencies.** It implements the cold-tier-factual cell that the
existing ACE pattern doesn't naturally fill.

**Phase 2 — Hook B (this month, conditional)**

If Phase 1 proves empirically insufficient (e.g. specialists routinely
fail to find topic files via filename navigation, or cold-tier search
becomes a bottleneck), add a local SQLite database at
`~/.claude/agent-memory/research-lead/index.sqlite` with an FTS5
table over topic file contents and an optional embedding column via
`sqlite-vec` (single-file extension, no server). Expose it to
specialists via a small Python or Node MCP server (the same pattern
Akash uses for Playwright / Context7 MCPs today). The reference
architecture is the **MemX paper** (arxiv 2603.16171, retrieved
2026-04-12): Rust + libSQL + FTS5 + vector + 4-factor reranking,
"Hit@1 = 91.3%, FTS5 reduces keyword search latency 1,100x at
100k records, end-to-end search under 90ms." Akash can prototype the
SQLite + FTS5 piece in an afternoon and add the vector column if
keyword recall is insufficient. **Build only if needed.**

**Phase 3 — Hook C (Q3 spike, time-boxed prototype)**

Spike a Latent Briefing / LatentMAS-style KV-cache handoff between
research-lead and one specialist using Akash's existing vLLM
background. Self-host a Qwen-14B or Llama-3.1-70B worker, implement
the compact-then-attend cycle from the Ramp Labs description (with
the LatentMAS open-source code at github.com/Gen-Verse/LatentMAS as
the reference impl), measure savings vs token-level handoff on his
actual research-team workload. **Time-box to one evening.** Ship if
the prototype shows the published direction holds on his shape; defer
if it doesn't.

**6-month direction — parametric memory**

Distill stable lessons from `MEMORY.md` into a small LoRA fine-tune
of a worker model. Per NVIDIA's "Context as Training Data Unlocks
Test-Time Learning" framing: stable lessons that don't churn (e.g.
"the moderator owns contradictions, not the lead") are better baked
into weights than re-injected at session start. High-update-rate
lessons stay in MEMORY.md. **Hybrid token+parametric** is the right
6-month landing zone.

## Component-level choices (SOTA pointer for each)

| Component | Recommendation | Source | Why this over alternatives |
|---|---|---|---|
| **Store (hot)** | `~/.claude/agent-memory/<agent>/MEMORY.md` (existing) | code.claude.com/docs/en/memory, retrieved 2026-04-12 | already shipped, two-tier design, LLM-curated, survives /compact |
| **Store (cold)** | topic files in same directory | same | unbounded, on-demand reads, no infra |
| **Store (factual long-tail)** | Phase 2: SQLite with FTS5 + sqlite-vec | MemX arxiv 2603.16171, retrieved 2026-04-12 | local-first, sub-100ms, no server, builds in an afternoon |
| **Index** | `MEMORY.md` as LLM-curated table of contents | Claude Code docs | the LLM is the search engine for navigation |
| **Retriever (hot)** | session-start auto-injection (built-in) | Claude Code docs | zero added latency |
| **Retriever (cold)** | Claude's own file tools (existing) → Phase 2 SQLite/FTS5/vector | Claude Code docs + MemX | hybrid retrieval is the documented winner for local-first |
| **Writer (in-session)** | LLM via Edit tool (existing) | Claude Code docs | no separation needed for in-session writes |
| **Reflector** | `research-retrospector` (existing) | ACE arxiv 2510.04618 | ACE three-role separation prevents brevity bias |
| **Curator** | `research-scribe` (existing, extended Hook A) | ACE arxiv 2510.04618 | curator role prevents context collapse; extension routes overflow to topic files |
| **Forgetter** | implicit (oldest entries fall out of 200-line ceiling) | Claude Code docs | adequate for now; ACT-R style decay is a research direction |
| **Graph layer** | NOT recommended this quarter | moderator C1 verdict | low entity count in Akash's workload; revisit if domain shifts |
| **Latent layer** | Hook C prototype, Q3 spike | LatentMAS arxiv 2511.20639, Ramp Labs Latent Briefing (REPORTED) | converging across 3 independent groups; buildable on self-hosted vLLM |
| **Parametric layer** | 6-month direction, hybrid with token-level | NVIDIA "context as training data" framing | for stable lessons only; high-update lessons stay in MEMORY.md |
| **Bi-temporal validity** | `git log` over `~/.claude/agent-memory/` directory | Letta Context Repositories blog 2026-02-12 | free, no graph DB, LLM-readable diffs |
| **Contradiction detection** | NOT included | Anatomy paper arxiv 2602.19320 | nobody has this working in production despite claims; not solved |

## What got considered and rejected

### REJECTED for Akash this quarter
- **Mem0** — benchmarks contested (Zep rebuttal + full-context-baseline
  finding), HN moderator-flagged astroturfing on launch thread, vector-
  centric where Akash needs experiential
- **MemPalace** — fraudulent benchmarks (3 independent audits +
  maintainer acknowledgment); see adversary.md for full case study
- **MemOS** — interesting MemCubes architecture but +43.7% claim is
  larger than Mem0's on the same broken LoCoMo benchmark, suspicious
  pattern; track for ideas, not for adoption
- **MAGMA** — novel 4-orthogonal-graph architecture but absolute LoCoMo
  score (0.700) is below trivial full-context baseline (~73%); same
  authors wrote the meta-criticism saying their own benchmarks are
  broken; track for ideas
- **Graphiti / Cognee** — graph DBs win the high-entity factual cell,
  not Akash's experiential cell; revisit if domain shifts
- **HippoRAG 2** — strongest academic pedigree (ICML 2025), but
  task-mismatched (Wikipedia QA shape, not coding-agent playbook
  shape); track

### TRACKED (could become relevant)
- **Letta self-edit pattern** — fallback if ACE-pattern curator
  overhead becomes problematic; Charles Packer's group is the
  closest production-shop competitor
- **EverMemOS engram lifecycle** — principled architecture, claims
  not verified; revisit if reference impl proves benchmark honesty
- **Latent Briefing / LatentMAS / LRAgent** — Hook C prototype target
- **Parametric memory via LoRA** — 6-month direction

## The MemPalace case study (the adversary gate's headline catch)

Reproduced in full from `EVIDENCE/adversary.md`. This is what the v2
adversary gate exists to catch.

**MemPalace** (github.com/milla-jovovich/mempalace, created April 5,
2026) gained ~21,700 GitHub stars in its first week and ~1.5M X.com
views, on the back of these claims:
- **96.6% LongMemEval R@5** in raw mode across 500 questions
- **100% LongMemEval** hybrid
- **100% LoCoMo**
- "First perfect score on LongMemEval, 500/500"

**Three independent audits show the benchmarks are fraudulent**:

1. **GitHub issue #214** (Hugo O'Connor, 2026-04-08): the published
   96.6% R@5 score measures **ChromaDB's default embedding model**,
   not MemPalace. The `build_palace_and_retrieve()` function calls
   only ChromaDB's `collection.add()` and `collection.query()`
   without invoking any palace architecture components (wings, rooms,
   closets, drawers). Independent Rust reproduction (zetl-bench)
   produced 93.8% R@5 / 98.4% R@10 with **zero MemPalace code**.
   When palace logic IS exercised, performance degrades: rooms mode
   89.4%, AAAK mode 84.2%. **Maintainer Milla J responded 2026-04-09**:
   "Your audit is right and deserves a direct response. Retiring
   `recall_any@5` as headline metric."

2. **Nicholas Rhodes substack** (2026-04-08, updated 2026-04-11):
   the 100% LongMemEval was **hand-tuned**. The team identified the
   3 specific dev-set questions the system failed on, then engineered
   3 targeted patches: a quoted-phrase boost for one question
   containing "sexual compulsions," a person-name boost for a question
   about "Rachel," and pattern matching for "I still remember" /
   "high school reunion" patterns. Three patches for three questions.
   Re-tested. Reported "first perfect score." Auditor's verdict:
   "BENCHMARKS.md has an entire integrity section asking them not to
   do what they did."

3. **Maksim Danilchenko review** (2026-04-10): 100% LoCoMo was
   achieved using `top_k=50` on datasets containing only 19-32 items
   — retrieving the entire pool. One developer integrating MemPalace
   with an LLM reported actual question-answering accuracy at "about
   17% of the time."

**The takeaways**:

For Akash: **do not adopt MemPalace**. The architecture (wings/halls/
rooms hierarchical namespace + typed cross-references) is genuinely
innovative; the benchmark numbers are unreliable.

For the corpus: when celebrity attribution + viral marketing produce
21K stars in a week, the prior probability of benchmark inflation
is high. The same pattern applies to other high-velocity entrants.

For the v2 protocol: this is exactly the failure mode the adversary
gate exists to catch. The skeptic (attacking the synthesis from
inside) would never have caught MemPalace; the adversary (attacking
the corpus from outside) caught it on the second source crosscheck.
**v2 gates work on a real question.**

## Open questions and explicit caveats

1. **Latent Briefing primary source paywalled** — the X.com posts
   from Ramp Labs returned HTTP 402. Numbers (31% token reduction,
   1.7s compaction, +3pp accuracy) are REPORTED-NOT-VERIFIED.
   Direction is corroborated by LatentMAS + LRAgent + MemOS MemCubes.
   Resolution path: track for paywall release; treat numbers as
   estimates until then.
2. **EverMemOS reference impl not fetched** — the github.com/EverMind-AI
   /EverMemOS repo was not directly retrieved. The recommendation
   does not depend on EverMemOS specifically (its engram lifecycle
   contribution is captured by ACE's reflection-curation pattern).
3. **Reddit corpus blocked** — WebFetch on reddit.com fails (web-miner
   anomaly). r/LocalLLaMA and r/MachineLearning not represented. HN
   + arxiv + GitHub corpus is comprehensive enough that this gap
   does not change the conclusion.
4. **No published benchmark with Akash's actual workload** — every
   benchmark in the corpus (LoCoMo, LongMemEval, AppWorld, finance)
   is for a different task family than "evolving research team
   playbook over months of sessions." The recommendation is grounded
   in convergent direction + Akash's actual constraints, not in
   benchmark numbers.

## What the v2 gates caught (process retrospective preview)

- **Synthesist (claim matrix)**: surfaced 5 load-bearing contradictions
  worth moderator debate; the v1 plan would have collapsed these
  into the lead's own arbitration.
- **Moderator (5 debates)**: reframed C4 to taxonomy cells (most
  important call), reframed C2 to workload-fit, resolved C1/C3 as
  conditional complementarity, deferred C5 to tracking.
- **Skeptic (post-synthesis attack)**: produced 7 corrections to the
  pre-skeptic synthesis, including upgrading Hook C from "track" to
  "prototype-as-spike" (Akash's vLLM background) and adding the
  parametric direction as 6-month item.
- **Adversary (corpus audit)**: produced the MemPalace case study,
  rejected 4 source categories (MemPalace headlines, Mem0 booster
  comments, aggregator review sites, all LoCoMo SOTA claims),
  marked 5 sources as MIXED (cite for direction, not numbers),
  caught the Latent Briefing paywall and forced REPORTED-NOT-VERIFIED
  caveat.

The v2 gates produced material corrections to the synthesis at every
stage. None were theater.

## Citations (load-bearing only; full list in adversary.md)

### STRONG-PRIMARY (use as load-bearing)
- ACE: Agentic Context Engineering — Zhang et al., Stanford / SambaNova,
  arxiv 2510.04618, retrieved 2026-04-12
- Memory in the Age of AI Agents: A Survey — Hu et al. (47 authors),
  arxiv 2512.13564, retrieved 2026-04-12
- Anatomy of Agentic Memory — Jiang et al., arxiv 2602.19320,
  retrieved 2026-04-12
- HippoRAG 2: Non-Parametric Continual Learning for LLMs — Jiménez
  Gutiérrez et al., OSU NLP, ICML 2025, arxiv 2502.14802,
  retrieved 2026-04-12
- MemGPT: Towards LLMs as Operating Systems — Packer et al., UC
  Berkeley, arxiv 2310.08560, retrieved 2026-04-12
- LatentMAS: Latent Collaboration in Multi-Agent Systems — Zou et al.
  (incl. Yejin Choi, James Zou), arxiv 2511.20639, retrieved 2026-04-12
- LRAgent: Efficient KV Cache Sharing for Multi-LoRA LLM Agents —
  arxiv 2602.01053, retrieved 2026-04-12
- Letta Context Repositories — letta.com/blog/context-repositories,
  2026-02-12, retrieved 2026-04-12
- Claude Code memory documentation — code.claude.com/docs/en/memory,
  retrieved 2026-04-12
- Steve Yegge: Beads — steve-yegge.medium.com/introducing-beads-a-coding-
  agent-memory-system-637d7d92514a, 2025-10-13, retrieved 2026-04-12

### MIXED (cite for direction, not for numbers)
- Mem0 paper — Chhikara et al., arxiv 2504.19413
- Zep "Lies Damn Lies" rebuttal — blog.getzep.com 2025-05-06
- MemOS paper — Li et al., arxiv 2507.03724
- MAGMA paper — Jiang et al., arxiv 2601.03236
- EverMemOS paper — Hu et al., arxiv 2601.02163

### REPORTED-NOT-VERIFIED
- Latent Briefing — Ramp Labs, X.com (paywalled), 2026-04-11

### REJECTED
- MemPalace headline benchmarks — fraudulent per 3 audits
- Mem0 HN booster comments — astroturf flagged
- Aggregator review sites — AI-generated SEO content
- Any LoCoMo SOTA claim — benchmark saturated per Anatomy paper

## NEXT STEPS

1. **This week**: Edit `~/.claude/agents/research/research-scribe.md`
   to add the Hook A topic-file routing behavior. Test on the next
   research session.
2. **This month (conditional)**: If Hook A's filename navigation
   proves insufficient, prototype Hook B (SQLite + FTS5 + sqlite-vec)
   following the MemX architecture as reference.
3. **Q3**: Time-boxed evening prototype of Hook C (Latent Briefing
   / LatentMAS-style KV-cache handoff) using self-hosted Qwen-14B
   or Llama-3.1-70B via Akash's existing vLLM setup. Measure savings;
   ship if the direction holds.
4. **6 months**: Distill stable lessons from `MEMORY.md` into a small
   LoRA fine-tune of a worker model. Hybridize token-level + parametric.
5. **Continuous**: track the latent layer (Latent Briefing paper
   release, LatentMAS open-source updates), the Anatomy paper's
   evolution, MAGMA's reference impl reproducibility, and Letta's
   coding-agent pivot for fallback patterns.

## Definition-of-done check

- [x] Architecture sketch with store / index / retriever / writer /
      curator / reflector / forgetter / graph / latent / parametric for
      the recommendation — DONE in component-level table
- [x] 15+ primary sources cited — 10 STRONG + 5 MIXED + 1 REPORTED + ~10
      others in evidence files = 26+ primary citations
- [x] Adversary corpus verdict — MIXED leaning HEALTHY for primary
      sources, COMPROMISED for marketing claims
- [ ] Evaluator PASS verdict on all 5 rubric dimensions — pending
      evaluator gate
- [ ] Retrospector lessons written to MEMORY.md — pending close
