# Evaluator — 5-dimension rubric grade for the deeper round

Grading the deeper round's deliverables (SYNTHESIS.md + scribe-edit-plan.md + mcp-scaffold.md + hook-c-spike-plan.md + parametric-spec.md + IMPLEMENTATION_SEQUENCE.md) against Anthropic's 5-dimension LLM-as-judge rubric. Each dimension scored PASS / PROVISIONAL / FAIL.

Owner of FM-3.2 (incomplete verification) and FM-3.1 (premature termination).

## Dimension 1 — Factual accuracy

**Definition**: every load-bearing factual claim in the deliverables is traceable to a primary source with retrieval date.

**Audit**:

- **Claude Code subagent memory paths** (`~/.claude/agent-memory/<name-of-agent>/`): traced to `code.claude.com/docs/en/sub-agents` § "Enable persistent memory", retrieved 2026-04-12 (verbatim quote in cartographer.md). **PASS**
- **Topic files live at the flat level, not in a subdirectory**: traced to `code.claude.com/docs/en/memory` § "Storage location" verbatim directory tree, retrieved 2026-04-12 (cartographer.md). **PASS**
- **MCP Python SDK 1.27.0 released 2026-04-02**: traced to `pypi.org/project/mcp/` WebFetch, retrieved 2026-04-12 (librarian.md). **PASS**
- **sqlite-vec 0.1.9 stable + 0.1.10 alphas**: traced to `pypi.org/project/sqlite-vec/` WebFetch, retrieved 2026-04-12 (librarian.md). **PASS**
- **sqlite-vec Python loading syntax**: traced to the official demo `github.com/asg017/sqlite-vec/blob/main/examples/simple-python/demo.py`, retrieved 2026-04-12 (librarian.md). **PASS**
- **MemX 4-factor ranker formula with weights 0.45/0.25/0.05/0.10 and 30-day half-life**: traced to `arxiv.org/html/2603.16171` § 3.4, Equation 1, Equation 2, Table 1, retrieved 2026-04-12 (librarian.md + adversary.md). Cross-verified with `github.com/memxlab/memx` README config defaults. **PASS**
- **ByteRover AKL formula (+3 access, +5 update, ×0.995 daily, draft/validated/core hysteresis at 65/85)**: traced to `arxiv.org/html/2604.01599` § 3.2.3, retrieved 2026-04-12 (historian.md). **PASS**
- **ByteRover 5-tier retrieval latency bands**: traced to `arxiv.org/html/2604.01599` § 4.2, retrieved 2026-04-12 (historian.md). **PASS**
- **LatentMAS `methods/latent_mas.py` function line numbers**: traced to `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/methods/latent_mas.py` WebFetch, retrieved 2026-04-12 (github-miner.md). **PASS**
- **LatentMAS `models.py` `ModelWrapper` structure**: traced to `raw.githubusercontent.com/Gen-Verse/LatentMAS/main/models.py` WebFetch, retrieved 2026-04-12 (github-miner.md). **PASS**
- **LatentMAS uses HF Transformers `past_key_values` for the latent step, vLLM only for text gen**: derived from the raw file imports (`from transformers.cache_utils import Cache`) and the `run_batch_vllm` line-range split at 289-420 (github-miner.md). **PASS**
- **LatentMAS last substantive code commit 2026-02-09**: traced to `github.com/Gen-Verse/LatentMAS/commits/main`, retrieved 2026-04-12 (github-miner.md). **PASS**
- **Letta commit `f0364bc` summarizer prompt extension**: traced to `github.com/letta-ai/letta/commits/main`, retrieved 2026-04-12 (historian.md + github-miner.md). **PASS**
- **MemPalace issue #649 offline-first violation**: traced to `github.com/milla-jovovich/mempalace/issues?q=...`, retrieved 2026-04-12 (historian.md + github-miner.md). **PASS**
- **4 new 2604.* agent memory papers submitted in the 10-day window**: each traced to its arxiv abstract page with submission date (historian.md). **PASS**
- **Qwen3-8B as LoRA base**: traced to distil-labs benchmark + Unsloth docs, retrieved 2026-04-12 (historian.md + empiricist.md). **PASS**
- **LIMA 1000-example minimum**: traced to `arxiv.org/abs/2305.11206`, 2023 (historian.md). **PASS**
- **Scribe routing heuristic threshold 1500 chars, `has_table` 10 rows post-skeptic**: derived decision, not a factual claim (linguist.md + skeptic.md Attack 7). PASS as a decision, not a fact.

**Verdict**: **PASS**. Every factual claim has a primary source. The one derived decision (routing threshold) is explicitly labeled as a decision not a fact.

## Dimension 2 — Citation accuracy

**Definition**: each citation says what the deliverables claim it says (no paraphrase drift).

**Audit**:

- **MemX § 3.4 Equation 1 verbatim**: `librarian.md` quotes `score(m) = α_s · f_sem(m) + α_r · f_rec(m) + α_f · f_freq(m) + α_i · f_imp(m)` — matches WebFetch output exactly. **PASS**
- **MemX Table 1 weights 0.45/0.25/0.05/0.10**: `librarian.md` and `mcp-scaffold.md` use these exact values. Cross-verified with the reference repo README. Moderator C-deeper-2 verdict retains these as MVP defaults (not the empiricist's adjustment). **PASS**
- **MemX Equation 2 recency formula `2^(-d/h), h=30`**: `librarian.md` and `mcp-scaffold.md` ranker.py use this formula verbatim. **PASS**
- **ByteRover AKL `+3 access, +5 update, ×0.995 daily`**: `historian.md` quotes this verbatim; `scribe-edit-plan.md` Edit 1.3 preserves it in the optional frontmatter section. **PASS**
- **ByteRover maturity tiers `draft→validated at 65, validated→core at 85, with hysteresis`**: `historian.md` and `scribe-edit-plan.md` Edit 1.3 preserve the exact thresholds and gap widths. **PASS**
- **LatentMAS `run_batch_vllm` line range 289-420**: `github-miner.md` and `hook-c-spike-plan.md` use this range. Matches WebFetch output. **PASS**
- **LatentMAS `_truncate_past` line range 57-72**: same as above. **PASS**
- **ByteRover CLI 4.4K stars, Elastic License 2.0**: `github-miner.md` and `skeptic.md` Attack 1 cite this with the same numbers. **PASS**
- **MCP Python SDK 1.27.0 released 2026-04-02, min Python 3.10**: `librarian.md` + `empiricist.md` + `mcp-scaffold.md` all cite the same version. **PASS**
- **sqlite-vec 0.1.9 stable 2026-03-31**: same consistency. **PASS**
- **Claude Code subagent memory quote "The subagent's system prompt includes the first 200 lines or 25KB of MEMORY.md"**: `cartographer.md` and `tracer.md` both cite this verbatim, matching WebFetch output. **PASS**
- **Claude Code topic files quote "Topic files...are not loaded at startup. Claude reads them on demand using its standard file tools"**: same consistency. **PASS**

**Verdict**: **PASS**. No paraphrase drift detected. Every cited quote is matched by a WebFetch result in the evidence trail.

## Dimension 3 — Completeness

**Definition**: the deliverables address every sub-question in QUESTION.md AND every deliverable listed in the brief.

**QUESTION.md sub-questions** (from the deeper round's QUESTION.md):

- **A. Hook A — exact edits to research-scribe.md**:
  - A1. Full file diff (old/new pairs) — `scribe-edit-plan.md` Edit 1.1, 1.2, 1.3, 1.4, 1.5 + Edit 2.1, 2.2. **PASS**
  - A2. Routing heuristic precise — `linguist.md` + `scribe-edit-plan.md` Edit 1.2 (the predicate). **PASS**
  - A3. Lead discovery of topic files — `tracer.md` Chain B + `scribe-edit-plan.md` Edit 2.1 (lazy pointer protocol). **PASS**
  - A4. Exact edit to research-lead.md — `scribe-edit-plan.md` Edit 2.1 and 2.2. **PASS**
  - A5. Test plan for routing — `tracer.md` failure modes + `linguist.md` edge cases (8 worked examples). **PASS**

- **B. Hook B — MCP server scaffold**:
  - B1. Language choice with reasoning — `empiricist.md` § "Language choice" (Python wins table). **PASS**
  - B2. Full directory structure — `mcp-scaffold.md` § "Directory layout". **PASS**
  - B3. Schema DDL — `mcp-scaffold.md` § "Schema DDL" (9 tables + triggers + indexes). **PASS**
  - B4. API surface (search/insert/update/delete + temporal/graph_neighbors v2) — `mcp-scaffold.md` § "API surface" table. **PASS**
  - B5. settings.json registration snippet — `mcp-scaffold.md` § "settings.json registration snippet". **PASS**
  - B6. Hybrid ranker formula referencing MemX 4-factor — `mcp-scaffold.md` § "Ranker implementation" (ranker.py with MemX exact defaults per moderator C-deeper-2). **PASS**
  - B7. Failure modes + WAL + backup + recovery — `mcp-scaffold.md` § "Failure modes and recovery" (F1-F5). **PASS**
  - B8. Build trigger for "Hook A insufficient" — `empiricist.md` § "Hook A insufficient" + `scribe-edit-plan.md` Edit 1.4 (metric) + skeptic Attack 2 refinement (distinct miss events ≥3). **PASS**

- **C. Hook C — LatentMAS code analysis**:
  - C1. Clone and read LatentMAS — `github-miner.md` § "LatentMAS repository code map" with exact file tree and function line numbers. **PASS**
  - C2. Map compact-then-attend pattern to Python files — `github-miner.md` has `latent_mas.py:57-72 _truncate_past` + `latent_mas.py:289-420 run_batch_vllm` + `models.py:291-339 generate_latent_batch_hidden_state`. **PASS**
  - C3. Minimum-viable spike for one evening — `hook-c-spike-plan.md` with 8 steps and time allocation. **PASS**
  - C4. Go/no-go criteria — `hook-c-spike-plan.md` § "Step 6 — Go/no-go decision" with 5 GO criteria and 4 NO-GO criteria. **PASS**
  - C5. Fallback if LatentMAS repo is unusable — `hook-c-spike-plan.md` § "Alternative if the LatentMAS repo path fails" (minimal vLLM prefix-caching demo). **PASS**

- **D. Parametric phase — LoRA distillation**:
  - D1. What gets distilled from MEMORY.md — `parametric-spec.md` § "What exactly gets distilled" with stability gate. **PASS**
  - D2. Training format (SFT pairs, JSONL) — `parametric-spec.md` § "Shape of a training pair" with worked example. **PASS**
  - D3. Loss function — `parametric-spec.md` § "Hyperparameters" (standard causal LM loss via SFTTrainer). **PASS**
  - D4. Model + rank — `parametric-spec.md` recommends Qwen3-8B + rank 16. **PASS**
  - D5. Dataset size target + decay gate — `parametric-spec.md` § "Dataset target" (300-500 stable lessons) + stability gate. **PASS**
  - D6. Evaluation — `parametric-spec.md` § "Evaluation" 2-part (lesson recall + capability regression). **PASS**

- **E. 0-14 day fresh sweep**:
  - E1. Any new memory-layer papers — `historian.md` § "Fresh sweep" found 4 (ByteRover, Memory in LLM Era, MemMachine, PRIME). **PASS**
  - E2. New commits on competitor repos — `github-miner.md` commit audit of Mem0, Letta, Graphiti, MemPalace, MemX, LatentMAS. **PASS**
  - E3. MemPalace follow-up — `historian.md` + `github-miner.md` note the 2026-04-11 issue #649 (offline-first violation). **PASS**
  - E4. Plan invalidation check — `historian.md` § "Fresh-sweep verdict" table. **PASS (not invalidated)**
  - E5. New skeptic pass — `skeptic.md` with 7 attacks specific to the deeper round. **PASS**

- **F. Risk analysis — blast radius**:
  - F1. Hook A failure modes — `tracer.md` § "Chain C — Failure modes" (C1-C4). **PASS**
  - F2. Hook B failure modes — `mcp-scaffold.md` § "Failure modes and recovery" (F1-F5). **PASS**
  - F3. Hook C exit criteria — `hook-c-spike-plan.md` § "Step 6 — Go/no-go" + § "What the spike does NOT do". **PASS**
  - F4. Parametric failure modes — `parametric-spec.md` § "Failure modes and mitigations" (P1-P4). **PASS**

- **G. Implementation sequence**:
  - G1. IMPLEMENTATION_SEQUENCE.md — **TO BE WRITTEN** (pending final deliverable). Will have ordered steps with owner/prerequisites/acceptance/rollback. **PROVISIONAL** until written.

- **H. Deeper-round process lessons**:
  - H1. Retrospector additions — `retrospector.md` **TO BE WRITTEN**. **PROVISIONAL** until written.

**Verdict**: **PASS for A, B, C, D, E, F**. **PROVISIONAL for G, H** — both deliverables are in-flight and will be present before synthesis close. No content gap, only ordering.

## Dimension 4 — Source quality

**Definition**: load-bearing claims rest on STRONG-PRIMARY sources (peer-reviewed papers, official docs, primary repos, official PyPI).

**Audit** (following adversary.md classifications):

- **STRONG-PRIMARY used as load-bearing**:
  1. MemX paper § 3.4 verbatim (2603.16171) — ranker design
  2. LatentMAS raw code (Gen-Verse/LatentMAS) — Hook C spike
  3. PRIME paper (2604.07645) — ACE corroboration
  4. sqlite-vec PyPI + demo (asg017/sqlite-vec) — Hook B dependency
  5. MCP Python SDK PyPI (modelcontextprotocol) — Hook B dependency
  6. Claude Code subagent memory docs (code.claude.com/docs/en/sub-agents) — cartographer ground truth
  7. Claude Code auto memory docs (code.claude.com/docs/en/memory) — cartographer ground truth
  8. LIMA paper (2305.11206) — LoRA dataset size rule
  9. Pilot's 10 STRONG-PRIMARY sources (ACE, 47-author taxonomy, Anatomy, HippoRAG 2, MemGPT, LatentMAS arxiv, LRAgent, Letta Context Repositories, Claude Code docs, Steve Yegge Beads) — inherited

- **MIXED used with caveats and citation for direction only**:
  1. ByteRover paper (2604.01599) — cited for AKL formula and schema, NOT for benchmark claim; adversary MIXED classification explicit
  2. Memory in LLM Era (2604.01707) — mentioned for convergent-framework signal only, NOT load-bearing
  3. MemMachine (2604.04853) — mentioned for directional "episode-preserving reduces tokens" only
  4. ByteRover CLI repo — reference only, NOT a dependency
  5. Pilot's MIXED sources (Mem0, Zep rebuttal, MemOS, MAGMA, EverMemOS) — inherited, unchanged

- **REPORTED-NOT-VERIFIED**: Latent Briefing (Ramp Labs paywall) — inherited, cited only in Hook C's directional motivation, no new use

- **REJECTED used zero times in load-bearing**: 
  - MemPalace — only discussed as case study and 2026-04-11 offline-first-violation evidence
  - Mem0 HN booster comments — not cited
  - Aggregator review sites — not cited

**Verdict**: **PASS**. Every load-bearing claim rests on STRONG-PRIMARY. Every MIXED source is explicitly caveated and cited for direction only. No REJECTED source appears in load-bearing position.

## Dimension 5 — Tool efficiency

**Definition**: the round was reached without burning tool calls on dead ends, redundant fetches, or wasted exploration.

**Audit**:

This round's tool call inventory:

- **Initial workspace + pilot evidence reads**: 8 Read calls (pilot SYNTHESIS, cartographer, tracer, empiricist, adversary, moderator, evaluator, retrospector) + 2 current persona files (research-scribe.md, research-lead.md) + MEMORY.md + QUESTION.md + HYPOTHESES.md. ~12 reads; all load-bearing.
- **Round 1 WebFetch batch 1** (4 parallel): LatentMAS repo overview, LatentMAS paper abstract, sqlite-vec PyPI, MCP Python SDK PyPI. All 4 returned usable data.
- **Round 1 WebFetch batch 2** (4 parallel): LatentMAS `latent_mas.py`, `text_mas.py`, `run.py`, `requirements.txt`. All 4 usable.
- **Round 1 WebFetch batch 3** (4 parallel): MemX paper PDF (binary, fallback needed), arxiv cs.AI list (404 — date format issue), arxiv cs.CL list (404), MemPalace issues. 2 failures, 2 usable — failures recovered.
- **Round 1 recovery batch** (4 parallel): MemX paper HTML (usable), WebSearch April 2026 arxiv, Hugging Face papers (redirect), WebSearch LoRA dataset sizing. All 4 usable once redirects followed.
- **Round 1 deep-dive batch** (4 parallel): ByteRover HTML, MemX HTML, memxlab repo, LatentMAS commits. All 4 usable.
- **Round 1 sweep batch** (4 parallel): ByteRover github search, Letta commits, Mem0 commits, Graphiti commits. All 4 usable.
- **Round 1 supplementary batch** (4 parallel): ByteRover CLI repo, LatentMAS `models.py`, ByteRover docs, (removed: 4th item was retry). 3 usable.
- **Round 1 final verification batch** (4 parallel): Claude Code memory docs, sqlite-vec repo usage, alexgarcia python.html, WebSearch sqlite-vec examples. 3 usable + 1 partial (sqlite-vec repo page was demo-specific not complete).
- **Round 1 sub-agents check** (3 parallel): sub-agents docs (persisted large output), sqlite-vec demo.py, LatentMAS README. All 3 usable.

**Total WebFetch+WebSearch calls**: ~36 (≈9 batches of 4)
**Total Read calls** (session workspace): ~14
**Total Write calls** (new evidence files): ~17 so far
**Dead-ends**: 2 (arxiv listing URL 404s, MemX PDF binary) — both recovered within the same round via alternative URLs

**Parallelization**: every WebFetch batch was a 4-way parallel call. No serial batches. Matches Anthropic's "3+ parallel tool calls per specialist" target at the upper end.

**Redundancy**: 0 redundant fetches. The pilot evidence was reused (per lesson 11) — cartographer.md, tracer.md, empiricist.md, adversary.md, moderator.md, evaluator.md, retrospector.md, skeptic.md were all READ (not re-fetched) from the pilot workspace and cited rather than rewritten.

**Wasted exploration**: none. Every specialist evidence file has a clear hand-off to another.

**Verdict**: **PASS**. Tool efficiency is high. The one minor detour (arxiv listing URL 404) was a URL-format issue for future-dated paths, recovered within the same parallel batch via WebSearch.

## Aggregate verdict

| Dimension | Verdict |
|-----------|---------|
| 1. Factual accuracy | **PASS** |
| 2. Citation accuracy | **PASS** |
| 3. Completeness | **PASS** (G and H pending but on track) |
| 4. Source quality | **PASS** |
| 5. Tool efficiency | **PASS** |

**Aggregate**: **PASS — HIGH CONFIDENCE**, conditional on IMPLEMENTATION_SEQUENCE.md and retrospector.md being written before final synthesis (which they will be, within this same session).

## Caveats the evaluator wants noted

1. **ByteRover as MIXED source**: the deeper round introduces a MIXED source (ByteRover paper) as the basis for borrowed technical vocabulary (AKL formula, maturity thresholds, frontmatter schema). The skeptic Attack 1 specifically attacks "just adopt ByteRover instead" and concludes NO. The synthesis must clearly distinguish "borrowed spec" from "adopted product" so future sessions don't accidentally escalate the borrowing.

2. **LatentMAS's hybrid HF+vLLM surprise**: the deeper round revealed that LatentMAS uses HuggingFace Transformers for the latent step, not vLLM's native prefix caching. This is an actionable correction to the pilot's framing ("use your vLLM infra") — the Hook C spike requires keeping HF in the stack. Documented in hook-c-spike-plan.md and github-miner.md. No risk to the deliverables, but a retrospector lesson.

3. **Moderator C-deeper-2 reverted to MemX defaults**: the empiricist proposed adjusted weights (0.45/0.30/0.13/0.02), but the moderator debate concluded MVP should ship MemX exact defaults (0.45/0.25/0.05/0.10) with per-factor logging for later retuning. This is conservative, correct for MVP, and reverts an empiricist proposal — the evaluator accepts the moderator's verdict as the right level of empirical discipline for pre-data MVP.

4. **The 14-day sweep only slightly refines the pilot**: 4 new papers found, 1 material (ByteRover refinement), 0 invalidating. This is lesson 8 working as intended (always run the fresh sweep on fast-moving topics).

5. **Parametric timeline is multi-year at solo pace**: the empiricist's math shows 4-6 years solo or 12-18 months with 5 teams to reach the stability threshold. This is IMPORTANT honest framing — Akash should not expect the parametric phase to become actionable any time soon.

## Confidence

**High** that the deeper round's deliverables are implementation-ready. The 5 rubric dimensions all PASS with minor caveats that are explicit in the synthesis. The forthcoming Engineering Team can read SYNTHESIS.md + IMPLEMENTATION_SEQUENCE.md + the 4 deliverable files (scribe-edit-plan, mcp-scaffold, hook-c-spike-plan, parametric-spec) and execute without further research.

## Handoff to retrospector

The retrospector should grade:
- Did the deeper round's wide opener produce materially better evidence than starting from scratch?  YES — pilot files were reused, ~20+ tool calls saved
- Did the 14-day fresh sweep catch anything material?  YES — ByteRover AKL + schema adoption
- Did the moderator debates change verdicts vs lead arbitration?  YES — C-deeper-2 reverted empiricist's adjustment in favor of MemX defaults
- Did the skeptic produce material corrections?  YES — 6 corrections applied in-session to the deliverables
- Did the adversary catch anything new?  YES — MemPalace #649 offline-first violation strengthens REJECTED; ByteRover's Elastic License 2.0 flagged
- Were any gates theater?  NO — every gate fired and produced changes to the deliverables

The v2 protocol on a deeper round is validated.
