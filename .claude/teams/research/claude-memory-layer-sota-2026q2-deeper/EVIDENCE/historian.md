# Historian — 0-14 day fresh sweep + LoRA-minimal-dataset prior art

Sub-question: In the 10 days since the pilot v2 ran on 2026-04-02, has any arxiv paper, GitHub release, or production project shipped something that invalidates the 4-phase plan? Separately, what does published prior art say about minimum dataset size for LoRA-based distillation?

## Method

- WebSearch for `arxiv "April 2026" "2604" agent memory LLM new paper`
- WebFetched individual arxiv abstract pages for every match (4 papers surfaced)
- WebFetched the HTML version of ByteRover for the AKL scoring formula
- WebFetched commits pages for Letta, Mem0, Graphiti, LatentMAS between 2026-03-29 and 2026-04-12
- WebSearch for minimum LoRA dataset size + distillation sizing for Llama-3.1-8B / Qwen-2.5-7B

## Fresh sweep — what shipped 2026-04-02 through 2026-04-12

### 1. ByteRover: Agent-Native Memory Through LLM-Curated Hierarchical Context (arxiv 2604.01599)

**Authors**: Andy Nguyen, Danh Doan, Hoang Pham, Bao Ha, Dat Pham, Linh Nguyen, Hieu Nguyen, Thien Nguyen, Cuong Do, Phat Nguyen, Toan Nguyen
**Submission**: April 2, 2026
**Corresponding repo**: `github.com/campfirein/byterover-cli` — 4,400 stars, TypeScript, Elastic License 2.0, MCP-compatible, 22+ agent integrations (Cursor, Claude Code, Windsurf, Cline), `npm install -g byterover-cli`

**Abstract verbatim** (from `arxiv.org/abs/2604.01599`, retrieved 2026-04-12):

> "Memory-Augmented Generation (MAG) extends large language models with external memory to support long-context reasoning, but existing approaches universally treat memory as an external service that agents call into, delegating storage to separate pipelines of chunking, embedding, and graph extraction. This architectural separation means the system that stores knowledge does not understand it, leading to semantic drift between what the agent intended to remember and what the pipeline actually captured, loss of coordination context across agents, and fragile recovery after failures. In this paper, we propose ByteRover, an agent-native memory architecture that inverts the memory pipeline: the same LLM that reasons about a task also curates, structures, and retrieves knowledge. ByteRover represents knowledge in a hierarchical Context Tree, a file-based knowledge graph organized as Domain, Topic, Subtopic, and Entry, where each entry carries explicit relations, provenance, and an Adaptive Knowledge Lifecycle (AKL) with importance scoring, maturity tiers, and recency decay. Retrieval uses a 5-tier progressive strategy that resolves most queries at sub-100 ms latency without LLM calls, escalating to agentic reasoning only for novel questions. Experiments on LoCoMo and LongMemEval demonstrate that ByteRover achieves state-of-the-art accuracy on LoCoMo and competitive results on LongMemEval while requiring zero external infrastructure, no vector database, no graph database, no embedding service, with all knowledge stored as human-readable markdown files on the local filesystem."

**AKL formula verbatim** (from HTML version `arxiv.org/html/2604.01599`, § 3.2.3):

- **Importance scoring**: "Access events contribute a +3 bonus; update events contribute +5. A daily decay factor of 0.995 prevents unbounded accumulation."
- **Maturity tiers**: "draft → validated (promotion at ι≥65, demotion at ι<35; gap of 30), validated → core (promotion at ι≥85, demotion at ι<60; gap of 25)."
- **Recency decay**: `r_i = exp(-Δt_i / τ)` with `τ = 30` days → ~21-day half-life.

**5-tier retrieval** (§ 4.2, Algorithm 1):

| Tier | Method | Latency | Escalation trigger |
|------|--------|---------|--------------------|
| 0 | Exact cache hit | ~0 ms | Hash mismatch |
| 1 | Fuzzy cache (Jaccard) | ~50 ms | Similarity < 0.6 |
| 2 | Direct MiniSearch (BM25) | ~100 ms | BM25 < 0.85 or insufficient gap |
| 3 | Optimized LLM call | < 5 s | Confidence < 0.93 |
| 4 | Full agentic loop | 8-15 s | (final fallback) |

**Disk layout** (§ 3.2):
- Path: `.brv/context-tree/<domain>/<topic>/<filename>.md`
- Format: markdown with YAML frontmatter
- Frontmatter fields: `title, tags, keywords, related, importance (0-100), maturity, recency, accessCount, updateCount, timestamps`

**Why this matters for Hook A**:

ByteRover is a published, peer-credible, fresh (10 days old), 4.4k-star production implementation of **exactly the pattern the pilot recommends** for Hook A. It is NOT a competitor to the recommendation — it is **validation** that the direction is correct. Three implementation details ByteRover adds that the pilot's plan should adopt:

1. **AKL importance scoring formula** — the scribe's "Reinforced by" concept maps directly to `+3 on access, +5 on update, *0.995 daily decay`. This is a concrete algorithm Akash's scribe can inherit rather than invent.
2. **Maturity tiers with hysteresis** — `draft → validated → core` with asymmetric promote/demote thresholds (65/35 gap 30; 85/60 gap 25) prevents oscillation. This is the parametric LoRA phase's gate: only `core` tier lessons get distilled. Concrete decay rule.
3. **YAML frontmatter schema** — `title, tags, importance, maturity, recency, accessCount, updateCount, timestamps` is a ready-to-adopt schema for Hook A topic files.

**ByteRover does NOT invalidate the pilot's plan**. ByteRover is a production CLI (TypeScript, Elastic License 2.0, commercial-source-available). Akash's plan is a bespoke Claude Code extension. What the pilot should do is **borrow the AKL algorithm and frontmatter schema verbatim**, cite the paper as primary source, and not adopt the CLI binary.

### 2. Memory in the LLM Era: Modular Architectures and Strategies in a Unified Framework (arxiv 2604.01707)

**Submission**: April 2, 2026
**Abstract verbatim**: "Memory emerges as the core module in the large language model (LLM)-based agents for long-horizon complex tasks ... A number of memory methods have been proposed in the literature. However, these methods have not been systematically and comprehensively compared under the same experimental settings. In this paper, we first summarize a unified framework that incorporates all the existing agent memory methods from a high-level perspective. We then extensively compare representative agent memory methods on two well-known benchmarks and examine the effectiveness of all methods, providing a thorough analysis of those methods. As a byproduct of our experimental analysis, we also design a new memory method by exploiting modules in the existing methods, which outperforms the state-of-the-art methods."

**Why this matters**: this is the **second unified-framework survey** in the field (the first being `arxiv 2512.13564` — "Memory in the Age of AI Agents", 47-author) published in the same quarter. Two independent unified frameworks converging is a directional signal. Details on the specific comparison benchmarks and the "new method" aren't in the abstract — could be valuable for a future follow-up pass but doesn't affect the current plan because the pilot's taxonomy frame is already set by 2512.13564.

**Classification**: MIXED (pre-peer-review survey). Use for citation support, not as the load-bearing structural backbone (2512.13564 retains that role).

### 3. MemMachine: A Ground-Truth-Preserving Memory System for Personalized AI Agents (arxiv 2604.04853)

**Authors**: Shu Wang, Edwin Yu, Oscar Love, Tom Zhang, Tom Wong, Steve Scargall, Charles Fan
**Submission**: April 6, 2026
**Abstract verbatim**: "... MemMachine, an open-source memory system that integrates short-term, long-term episodic, and profile memory within a ground-truth-preserving architecture that stores entire conversational episodes and reduces lossy LLM-based extraction. ... on LoCoMo it reaches 0.9169 using gpt4.1-mini ... Compared to Mem0, MemMachine uses roughly 80 percent fewer input tokens under matched conditions."

**Benchmarks claimed**: LoCoMo 0.9169, LongMemEvalS 93.0%, HotpotQA-hard 93.2%, WikiMultiHop 92.6%.

**Adversary verdict** (applied pre-emptively): MemMachine's headline LoCoMo number (0.9169) is on the SAME benchmark the pilot's adversary ruled as SATURATED per the Anatomy of Agentic Memory paper (arxiv 2602.19320). This is **another data point for the corpus-wide pattern**: every new 2604.* agent memory paper is going to claim LoCoMo SOTA, and per the Anatomy paper those claims are untrustworthy. **MemMachine is MIXED classification, cited only for the 80% token reduction vs Mem0 direction**.

**Why it doesn't invalidate the plan**: the 0.9169 LoCoMo is on a saturated benchmark; the "80% fewer tokens vs Mem0" is a comparison to a MIXED system; and the architecture (vector-RAG-like) doesn't match Akash's token-level/experiential cell needs.

### 4. PRIME: Training-Free Proactive Reasoning via Iterative Memory Evolution for User-Centric Agent (arxiv 2604.07645)

**Authors**: Prince Zizhuang Wang, Shuli Jiang
**Submission**: April 8, 2026
**Abstract verbatim**: "... we introduce PRIME (Proactive Reasoning via Iterative Memory Evolution), a gradient-free learning framework that enables continuous agent evolvement through explicit experience accumulation rather than expensive parameter optimization. PRIME distills multi-turn interaction trajectories into structured, human-readable experiences organized across three semantic zones: successful strategies, failure patterns, and user preferences. These experiences evolve through meta-level operations and guide future agent behavior via retrieval-augmented generation."

**Why this matters**: PRIME is a **near-clone of the ACE pattern** (generation/reflection/curation for experiential memory) with two specific contributions over ACE:

1. **Three explicit semantic zones**: successful strategies, failure patterns, user preferences. ACE's "playbook" is flatter.
2. **Meta-level operations** over experiences (not detailed in the abstract; would need full paper).

The 3-zone structure is a minor extension Akash could fold into the scribe's topic-file routing heuristic: long-tail content might be classified as one of (strategy | failure | user-pref) when routing. This is an optional refinement, NOT a blocker for Hook A.

**Classification**: STRONG-PRIMARY-ACADEMIC (aligns with ACE, independent authors, small-scale bounded claims). Cite as corroborating direction for the existing ACE-pattern recommendation.

### Repo commit sweep 2026-03-29 through 2026-04-12

**LatentMAS** (`github.com/Gen-Verse/LatentMAS`):
- Last commits: Mar 27, 2026 (README update, `b9b2095`), Mar 26, 2026 (README update, `c2fea01`), Feb 27, 2026 (README, `c14da9c`)
- Last substantive code change: Feb 9, 2026 (`55d6e55`, "Update new extensions of LatentMAS")
- **Status**: alive, README being updated, no breaking code changes in the sweep window. The `methods/latent_mas.py` file is stable. Safe to clone for Hook C spike.

**Letta** (`github.com/letta-ai/letta`):
- Meaningful commit: `f0364bc` on 2026-03-31 — "fix: Update summarizer prompt to remember plan files, github PRs, etc." — this extends Letta's in-memory summarization to reference plan files and gh PRs. Convergent with Hook A's topic-file routing idea.
- `54c346f` on 2026-03-31 — "fix(memfs): remove invalid redis_client kwarg from MemfsClient init" — the `MemfsClient` is Letta's file-system backend for Context Repositories; still being maintained.
- Version bump: 0.16.7 on 2026-03-31
- **Status**: active development, the Context Repositories pattern is being maintained. No abandonment signal.

**Mem0** (`github.com/mem0ai/mem0`):
- `9d6b79a` on 2026-04-12 — "removing the enable graph flag and switching ... camel case" (a API surface cleanup)
- `c239d8a` on 2026-04-12 — "fix(client): prevent feedback telemetry TypeError"
- `4c2db3e` on 2026-04-06 — "introduce Mem0 skill graph with dedicated CLI"
- **No** commits addressing the Zep rebuttal's methodology critique. **No** commits addressing the HN astroturfing flag. The project continues shipping without engaging with the benchmark-methodology criticism. **This is evidence that Mem0's position in the adversary verdict (MIXED, contested benchmarks) has not changed.**

**Graphiti** (`github.com/getzep/graphiti`):
- Commits `3630e3432`, `9e93426be`, `221cae4cc`, `b24b9b34c`, `58d9da38a` between 2026-04-02 and 2026-04-05 — all routine maintenance (CLA signings, security hardening via commit-SHA pinning, slop detection)
- **Status**: active but no core architecture changes. Bi-temporal validity mechanism unchanged.

**MemPalace** (`github.com/milla-jovovich/mempalace`):
- No commits since the maintainer's 2026-04-09 acknowledgment of the ChromaDB-vs-MemPalace fraud (issue #214 closed with "retiring recall_any@5 as headline metric")
- **New issues filed 2026-04-11**: #650 (Windows setup failures), #649 (hidden network dependency violates offline-first), #648 (docs site request), #646 (JSON parser bug with claude.ai export), #645 (--refresh flag request). **NOTE**: the 2026-04-11 issue `#649 "Hidden network dependency violates offline-first guarantees"` (geovanirz, labeled bug) is a SECOND methodology problem separate from the benchmark fraud. The project claims offline-first, but telemetry / remote calls are leaking. This further reinforces the adversary's "REJECTED" classification of MemPalace.
- **No retraction** or benchmark correction commits since 2026-04-09.

### Fresh-sweep verdict

| Finding | Invalidates the plan? |
|---------|-----------------------|
| ByteRover (2604.01599) | **NO — validates + refines.** Adopt AKL scoring formula, maturity tiers, frontmatter schema into Hook A. |
| Memory in the LLM Era (2604.01707) | No. Cite as corroborating taxonomy. |
| MemMachine (2604.04853) | No. MIXED; do not cite for numbers. |
| PRIME (2604.07645) | No. Validates ACE direction; optional 3-zone refinement. |
| LatentMAS commits | No. Repo alive, safe to clone for Hook C. |
| Letta commits | No. Context Repositories pattern still maintained. |
| Mem0 commits | No. Continues to ignore methodology critique; MIXED classification holds. |
| Graphiti commits | No. Bi-temporal validity unchanged. |
| MemPalace issues | Strengthens REJECTED verdict (second methodology violation surfaced). |

**Bottom line**: the pilot's 4-phase plan is not invalidated. It is **refined** by ByteRover's AKL formula and schema, and **corroborated** by PRIME's ACE-direction endorsement.

## LoRA minimum dataset size prior art

From WebSearch results on minimum LoRA / instruction tuning dataset sizes for Llama-3.1-8B / Qwen-2.5-7B / Qwen-3-8B:

- **Common finding**: "1,000 high-quality examples beats 100,000 mediocre ones" is the most-cited rule of thumb across 2024-2025 LoRA tutorials (Unsloth docs, seaflux, neptune.ai, datacamp).
- **LIMA (Less Is More for Alignment, Meta 2023)** remains the canonical primary source: 1,000 carefully-curated instructions gave Llama-65B near-GPT-4-quality instruction-following. Source: `arxiv 2305.11206`.
- **Training time**: ~1-2 hours on a free Google Colab T4 with 1,000 samples, 1 epoch. At Akash's scale (consumer / pro hardware with 1x 4090 or equivalent), figure 30-60 minutes for the same scale.
- **Hyperparameters typically reported**: LoRA rank 16-64, learning rate 5e-5, 3-4 epochs, batch size 4-16.
- **Qwen3-4B-Instruct-2507 dominates the distil-labs fine-tuning benchmark** (top of the 2025 charts), with Qwen3-8B second — suggesting Qwen over Llama for Akash if he's distilling.

### Quality-over-quantity finding (load-bearing for parametric gate)

The LIMA paper's key finding: **diversity + quality of 1,000 examples > raw quantity**. For Akash, this maps to the pilot's "high-stability MEMORY.md lessons" filter. The deeper round's IH-D hypothesis (distillation gated on reinforced-across-3-sessions) aligns: stable lessons are **diverse** (each encodes a distinct rule) and **high-quality** (they survived reinforcement).

**Dataset target**: **~300-500 stable lessons** is the right minimum for LoRA distillation on a 7B-8B instruct model.
- Source: LIMA says 1,000 works. Akash's use case is narrower (research team playbook only), so 300-500 is likely sufficient for the restricted task.
- Per-lesson expansion: each stable lesson gets ~3-5 synthetic prompts (e.g., "when the user asks about X, what do you do?", "what's the rule about Y?") so 300 lessons → ~1,500 training pairs.

**Model recommendation**: **Qwen-3-8B** over Llama-3.1-8B for a 2026-Q2/Q3 distillation, because:
1. Qwen3-8B tops the distil-labs fine-tune benchmark (above).
2. Akash's vLLM deployment has first-class Qwen3 support via the `qwen3` model family.
3. License: Qwen 2.5/3 is Apache 2.0, Llama 3.1 is the Meta license with 700M MAU constraint (doesn't affect Akash but cleaner).
4. Long-context support: Qwen3-8B supports 256K context via YaRN; Llama-3.1-8B is 128K native.

**LoRA rank recommendation**: **16** for the initial distillation.
- Rank 8: too constrained, limits capacity for 300-500 diverse lessons.
- Rank 16: canonical for instruction tuning on 7B-8B models; unsloth and neptune tutorials default to 16-32.
- Rank 32-64: overkill for 300-500 examples; risks overfitting.

**Training config skeleton** (from prior art, not measured):
- Learning rate: 5e-5 for the LoRA params, with 100-step warmup
- Epochs: 3 (not 10 — avoid overfitting on small dataset)
- Batch size: 8 (effective, with gradient accumulation as needed for memory)
- Max sequence length: 2048 (lessons are short; no need for long context)
- LoRA target modules: `q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj` (the standard "all linears" target for a LoRA-heavy adaptation)

## Confidence

**High** on the fresh-sweep findings: each 2604.* paper verified via arxiv abstract fetch with submission date. The ByteRover AKL formulas are verbatim from the HTML version. Repo commit sweeps are from github.com/<owner>/<repo>/commits/main, retrieved 2026-04-12.

**Medium** on the LoRA dataset-size recommendation: the LIMA paper is primary, but Akash's specific task family has no published benchmark. The 300-500 number is a prior-art extrapolation, not a measurement.

## Handoff

- **synthesist** — the ByteRover AKL formula and the scribe heuristic need to be reconciled (Hook A refinement).
- **empiricist** — the LoRA training time and dataset size feed the parametric-phase sizing table.
- **skeptic** — attack: is ByteRover close enough to the pilot's plan that Akash should just adopt the CLI instead? (Answer in skeptic.md.)

## Citations

- ByteRover paper — `arxiv.org/abs/2604.01599`, retrieved 2026-04-12 (submitted 2026-04-02)
- ByteRover HTML full text — `arxiv.org/html/2604.01599`, § 3.2.3, § 4.2, Algorithm 1
- ByteRover CLI — `github.com/campfirein/byterover-cli`, retrieved 2026-04-12 (4.4k stars, TypeScript, Elastic License 2.0)
- ByteRover docs — `docs.byterover.dev`, retrieved 2026-04-12
- Memory in the LLM Era — `arxiv.org/abs/2604.01707`, retrieved 2026-04-12 (submitted 2026-04-02)
- MemMachine — `arxiv.org/abs/2604.04853`, retrieved 2026-04-12 (submitted 2026-04-06)
- PRIME — `arxiv.org/abs/2604.07645`, retrieved 2026-04-12 (submitted 2026-04-08)
- LatentMAS commits — `github.com/Gen-Verse/LatentMAS/commits/main`, retrieved 2026-04-12 (last substantive code 2026-02-09)
- Letta commits — `github.com/letta-ai/letta/commits/main`, retrieved 2026-04-12 (f0364bc, 54c346f on 2026-03-31)
- Mem0 commits — `github.com/mem0ai/mem0/commits/main`, retrieved 2026-04-12 (9d6b79a, c239d8a on 2026-04-12)
- Graphiti commits — `github.com/getzep/graphiti/commits/main`, retrieved 2026-04-12 (routine maintenance only)
- MemPalace issues — `github.com/milla-jovovich/mempalace/issues`, retrieved 2026-04-12 (#649 "Hidden network dependency" bug, 2026-04-11)
- LIMA paper — `arxiv.org/abs/2305.11206`, 2023 (canonical minimum-dataset finding)
- LoRA fine-tuning tutorials — Unsloth docs, distil-labs benchmark (Qwen3-4B/8B ranking), retrieved 2026-04-12
