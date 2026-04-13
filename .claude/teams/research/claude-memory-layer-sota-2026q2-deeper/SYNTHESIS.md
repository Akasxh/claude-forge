# SYNTHESIS — Memory layer for Claude: implementation-grade (deeper round)

**Lead**: research-lead (adopted-persona mode, v2 protocol full)
**Slug**: `claude-memory-layer-sota-2026q2-deeper`
**Session date**: 2026-04-12
**Pilot workspace**: `~/.claude/teams/research/claude-memory-layer-sota-2026q2/`
**Confidence**: HIGH on all deliverables; all 5 evaluator dimensions PASS

## Answer in one paragraph

The pilot's 4-phase plan (Hook A topic files, Hook B SQLite+FTS5+sqlite-vec MCP, Hook C LatentMAS spike, parametric LoRA) survives the deeper round's fresh sweep, skeptic attacks, and adversary audit of 10 new sources. The plan is refined — not changed — by three material findings from the 14-day fresh sweep: **(1) ByteRover's published AKL scoring formula** (arxiv 2604.01599, April 2, 2026) is borrowed verbatim into Hook A's optional YAML frontmatter schema with explicit citation; **(2) LatentMAS's actual code uses HuggingFace Transformers' `past_key_values` for the latent compaction, vLLM only for text generation** — the Hook C spike must keep HF in the stack, not port to a vLLM-only pipeline; **(3) the user's `<leader>/topic/<topic>.md` phrasing was a slip** — Claude Code's documented convention is flat topic files at `~/.claude/agent-memory/<agent>/<topic>.md`, and the scribe-edit-plan reflects that correction. The deliverables are: **exact Edit-tool-ready diffs** for research-scribe.md (5 edits) and research-lead.md (2 edits); a **Python MCP server scaffold** with complete schema DDL, ranker.py with MemX exact default weights and per-factor logging, settings.json registration, backup script, and 5 documented failure-mode recoveries; a **one-evening LatentMAS spike plan** with 8 time-allocated steps, file-level code map (`methods/latent_mas.py:57-72 _truncate_past`, `methods/latent_mas.py:289-420 run_batch_vllm`, `models.py:291-339 generate_latent_batch_hidden_state`), and concrete go/no-go ratios; a **parametric LoRA distillation spec** with Qwen3-8B base + rank 16 + SFT + stability gate (`reinforced_by_count ≥ 3 AND maturity ≥ validated AND days_since_creation ≥ 30`) and a 4-6 year solo / 12-18 month multi-team timeline honest assessment; and an **ordered IMPLEMENTATION_SEQUENCE.md** of 30 steps across 4 phases with owner / prerequisites / acceptance / rollback per step. The forthcoming Engineering Team can execute from these artifacts without blocking on further research.

## Confidence justification

**HIGH confidence** rests on:
- Every factual claim in the deliverables traces to a primary source with 2026-04-12 retrieval date: Claude Code docs verbatim (cartographer), MemX paper § 3.4 verbatim (librarian), ByteRover paper § 3.2.3 verbatim (historian), LatentMAS raw source files with line numbers (github-miner), sqlite-vec PyPI + docs + demo (librarian), MCP Python SDK PyPI (librarian)
- The 4-phase plan and its structural backbone (the ACE pattern on token-level/experiential cell, the taxonomy frame from arxiv 2512.13564) are inherited from the pilot's HIGH-confidence evaluator PASS
- The 14-day fresh sweep found 4 new arxiv papers — 1 material refinement (ByteRover AKL adoption), 2 corroborating (PRIME, Memory in LLM Era), 1 MIXED irrelevant (MemMachine). The plan is not invalidated.
- Two moderator debates (C-deeper-1: `AND` vs `OR` in scribe routing; C-deeper-2: MemX defaults vs empiricist's adjustment) both resolved to conservative middle-ground positions
- Skeptic pass produced 6 in-session corrections applied directly to the deliverable files: ByteRover explicit-attribution scope, distinct-miss-events metric refinement, scribe session-start catch-up pass (Edit 1.5), MCP embedder background warmup, SFT-MVP-then-DPO-v2, `has_table` threshold 5→10
- Adversary audit classified 10 new sources; 5 are STRONG-PRIMARY load-bearing; 5 are MIXED with explicit attribution scope; 0 are REJECTED used as load-bearing
- Evaluator PASS on all 5 rubric dimensions (factual accuracy, citation accuracy, completeness, source quality, tool efficiency)

**No MEDIUM or LOW zones remain** on implementation decisions. The one residual uncertainty is the parametric phase's empirical applicability (LoRA distillation of agent playbooks has no published benchmark on Akash's specific task family), which is correctly framed as a 6-month-plus direction with explicit evaluation criteria rather than a this-quarter commitment.

## Fresh sweep findings (0-14 day window, 2026-04-02 to 2026-04-12)

### Material: ByteRover (arxiv 2604.01599, 2026-04-02)

ByteRover is a published + production-grade implementation of **exactly the pattern the pilot recommends** for Hook A: LLM-curated markdown files with a hierarchical context tree, Adaptive Knowledge Lifecycle scoring, maturity tiers, recency decay, zero external infrastructure, everything as human-readable markdown. Stars: 4,400. License: Elastic License 2.0. The paper formalizes three algorithms the pilot's plan can borrow verbatim:

1. **AKL importance scoring**: `importance += 3 on access, += 5 on update, *= 0.995 daily`. The scribe's "Reinforced by" concept maps directly.
2. **Maturity tier hysteresis**: `draft → validated at ι ≥ 65, validated → core at ι ≥ 85` with asymmetric demote thresholds preventing oscillation. This IS the parametric phase's stability gate.
3. **YAML frontmatter schema** (§ Appendix C): `title, tags, keywords, related, importance, maturity, recency, accessCount, updateCount, timestamps` — ready to adopt.

**Handling**: Hook A's optional frontmatter schema (scribe-edit-plan Edit 1.3) adopts these formulas verbatim **with citation to arxiv 2604.01599 § 3.2.3 and § Appendix C**. ByteRover's CLI binary is NOT adopted (Elastic License 2.0, architectural delta, different MCP pattern).

### Corroborating: PRIME (arxiv 2604.07645, 2026-04-08)

PRIME's "three semantic zones" (successful strategies, failure patterns, user preferences) is a refinement of the ACE evolving-playbook pattern. The paper is epistemically honest (no LoCoMo claim, 2 authors, bounded claims). Classification: STRONG-PRIMARY-ACADEMIC. Cited as further corroboration for the ACE direction.

### Corroborating: Memory in the LLM Era (arxiv 2604.01707, 2026-04-02)

A second unified-framework survey this quarter (the first is the 47-author arxiv 2512.13564 that the pilot uses as structural backbone). Two independent unified frameworks converging is a directional signal. Not load-bearing; tracked.

### MIXED (not used as load-bearing): MemMachine (arxiv 2604.04853, 2026-04-06)

Episode-preserving vector-RAG with LoCoMo 0.9169 claim. Saturated benchmark per pilot adversary — treat as directional "80% token reduction vs Mem0" only.

### Commit sweeps (Mem0, Letta, Graphiti, MemPalace, MemX, LatentMAS)

- **LatentMAS**: repo alive, last code commit 2026-02-09. Safe to clone for spike.
- **Letta**: actively maintaining Context Repositories pattern. Convergent with Hook A. Classification strengthens: HEALTHY fallback.
- **Mem0**: commits shipping but NOT addressing benchmark methodology critiques. Classification unchanged: MIXED.
- **Graphiti**: routine maintenance, no architecture changes.
- **MemPalace**: no benchmark-fraud fix. New 2026-04-11 issue #649 "Hidden network dependency violates offline-first guarantees" is a SECOND methodology violation. Classification strengthens: REJECTED.
- **MemX**: reference repo is a code drop (2 stars, 2 commits). Paper is the primary source; repo verifies the weight defaults match.

**Fresh-sweep verdict**: the pilot's 4-phase plan is **not invalidated**. It is **refined** by ByteRover's AKL adoption and corroborated by PRIME. The architecture is stable.

## Deliverables summary (what the Engineering Team takes)

### 1. Hook A — exact Edit-tool-ready diffs

File: `EVIDENCE/scribe-edit-plan.md`

- **Edit 1.1**: research-scribe.md Hard rules — add "only scribe + retrospector write to `~/.claude/agent-memory/research-lead/`"
- **Edit 1.2**: research-scribe.md Method step 4 — new topic-file routing predicate with machine-evaluable `AND` boolean (length ≥ 1500 AND type condition), with the `has_table` threshold at 10 rows (post-skeptic Attack 7 correction)
- **Edit 1.3**: research-scribe.md — optional YAML frontmatter schema for topic files, adopting ByteRover AKL formula with citation
- **Edit 1.4**: research-scribe.md — Hook A → Hook B trigger metric instrumentation (`scribe-metric:` LOG lines, **distinct miss events ≥ 3 over 10 sessions** per skeptic Attack 2 refinement)
- **Edit 1.5**: research-scribe.md Method step 1 — session-start catch-up routing pass (post-skeptic Attack 3, recovers missed closes)
- **Edit 2.1**: research-lead.md Step 3 of intake protocol — "lazy pointer protocol" for topic file references
- **Edit 2.2**: research-lead.md Rules — topic files are read-only for the lead

All 7 edits use unique `old_string` markers. Verification checklist included (7 grep assertions). Rollback procedure specified.

### 2. Hook B — Python MCP server scaffold

File: `EVIDENCE/mcp-scaffold.md`

- **Language**: Python (adjudicated by empiricist comparison table; Python wins on MCP SDK maturity + sqlite-vec wheel + stdlib FTS5 + Akash's Python stack)
- **Directory layout**: `~/.claude/memory-mcp/{src/memory_mcp/{server,db,ranker,embedder,handlers/{search,insert,update,delete,temporal,graph_neighbors},schema.sql},tests/,scripts/{bootstrap,backup}}`
- **Schema DDL**: 7 tables (memory + memory_edges + memory_events), 1 FTS5 virtual table, 1 vec0 virtual table (1024-dim for Qwen3-Embedding-0.6B), 3 sync triggers, 5 indexes, 3 pragmas (WAL, synchronous=NORMAL, foreign_keys=ON)
- **API MVP**: `memory.search`, `memory.insert`, `memory.update`, `memory.delete`. **v2**: `memory.temporal`, `memory.graph_neighbors`
- **Ranker**: MemX 4-factor hybrid (semantic 0.45 + recency 0.25 + frequency 0.05 + importance 0.10, reject threshold 0.15), **MemX exact defaults per moderator C-deeper-2**, recency = `2^(-age_days/30)` with 30-day half-life, RRF over FTS5 + vec0 at K=60. The `rank()` function returns per-factor breakdown for observability so retuning after 50 real queries is data-driven.
- **settings.json registration**: subagent-frontmatter form (preferred) and user-scope settings.json form (alternative)
- **Failure modes**: F1 SQLite corruption + recovery, F2 daily backup schedule, F3 MCP crash mid-session, F4 embedder download failure, F5 sqlite-vec load failure — each with specific mitigation and detection
- **Embedder warm-up**: background thread on `__main__` startup (post-skeptic Attack 4)
- **Build trigger**: distinct miss events ≥ 3 over 10 sessions (skeptic Attack 2 refinement of the original miss-rate > 20%)
- **Estimated effort**: 3 person-days for MVP

### 3. Hook C — one-evening LatentMAS spike plan

File: `EVIDENCE/hook-c-spike-plan.md`

- **Time budget**: 3-5 hours with explicit 8-step allocation (0:00-0:15 pre-flight, 0:15-0:30 clone, 0:30-0:45 install, 0:45-1:15 code read, 1:15-2:15 reference run, 2:15-3:15 baseline comparison, 3:15-3:45 go/no-go, 3:45-4:30 report)
- **LatentMAS code map**: exact function line numbers from `methods/latent_mas.py` (`_truncate_past` 57-72, `run_batch` 75-196, `run_batch_vllm` 289-420) and `models.py` (`_past_length` 19-24, `ModelWrapper.__init__` 27-67, `generate_latent_batch_hidden_state` 291-339). The architectural fact: **latent compact uses HF Transformers, vLLM only for text generation** — the spike must keep HF in the environment.
- **Go criteria**: (1) run completes, (2) token_savings ≥ 0.20, (3) wall_time_ratio ≥ 1.5, (4) accuracy_delta ≥ -0.05, (5) peak VRAM < 40GB
- **No-go criteria**: catastrophic failures or token_savings < 0.05 or accuracy_delta < -0.10
- **Fallback plan**: minimal vLLM prefix-caching demo (1-hour build) if LatentMAS repo is unusable
- **Out of scope (explicit)**: production integration, custom vLLM prefix-caching port, research-session workload, hyperparameter tuning

### 4. Parametric — LoRA distillation spec

File: `EVIDENCE/parametric-spec.md`

- **Base model**: **Qwen3-8B** (base, not instruct), Apache 2.0, top of distil-labs fine-tune benchmark, vLLM-native
- **LoRA config**: rank 16, target all 7 linear modules, dropout 0.05, lora_alpha 32
- **Training config**: 3 epochs, LR 5e-5 cosine, warmup 100 steps, batch 4 × 2 GA, seq 2048, bf16 + bnb 4-bit quant, ~45-90 min on 4090
- **Dataset format**: SFT with synthetic paraphrased prompts, 3-5 prompts per stable lesson, JSONL for TRL SFTTrainer
- **Synthetic prompt generator**: Python script calling Claude Opus for paraphrasing, ~$9 one-time cost for 300 lessons
- **Stability gate**: `reinforced_by_count ≥ 3 AND maturity ≥ validated (AKL ≥ 65) AND days_since_creation ≥ 30`
- **Target dataset size**: 300-500 stable lessons → 1500-2500 training pairs (LIMA-grounded)
- **Evaluation**: 2-part — (1) lesson recall: 30 held-out paraphrased questions, ≥80% must contain the rule; (2) capability regression: GSM8K/HumanEval/MMLU/IFEval subsets within 3-5pp of base
- **Deployment**: vLLM dynamic LoRA serving, `--enable-lora --lora-modules research-lead-playbook=<path>`
- **Timeline**: **4-6 years solo pace** (at observed ~1 new lesson per 2-3 sessions × 2-3 sessions/week × stability filter), **12-18 months with 5 active teams** (rate scales with team count). Parametric is correctly a 6-month+ direction, NOT a quarter-2 build.
- **DPO as v2 upgrade**: once MVP LoRA is deployed, collect real preference pairs (lessons where LoRA produced wrong answer) and train a DPO refinement. SFT for MVP; DPO for v2.
- **Failure modes**: P1 contradicted lessons, P2 session-specific detail leaking into weights, P3 capability regression, P4 stale distilled lessons — each with mitigation

### 5. IMPLEMENTATION_SEQUENCE.md — 30-step ordered checklist

File: `IMPLEMENTATION_SEQUENCE.md`

- **Phase 1 (Hook A)**: Steps 1-10. 1-2 hours of edits + 1 smoke-test session. Start this week.
- **Phase 2 (Hook B)**: Steps 11-20. ~3 person-days. Gated on `distinct miss events ≥ 3 over 10 sessions`. Earliest ~5 weeks out.
- **Phase 3 (Hook C)**: Steps 21-24. 1 evening + 1 day of proposal writing. Gated on Akash's availability + GPU access.
- **Phase 4 (Parametric)**: Steps 25-30. ~1 month of build when triggered. Gated on `stable lessons ≥ 300`. Earliest 6 months out; realistic 12-18 months.
- Every step has: owner placeholder (the Engineering Team lead reassigns to their specialists), prerequisites, acceptance criteria, rollback procedure.

## Corrections applied in this round

From skeptic Attacks 1-7 (6 in-session corrections + 1 retrospector lesson):

1. **ByteRover handled as "borrowed spec, not adopted product"** with explicit citation scope. Prevents the skeptic's Attack 1 ("just adopt ByteRover CLI") from re-surfacing in a future session.
2. **Trigger metric refined**: `distinct miss events ≥ 3 over 10 sessions` replaces `miss_rate > 20%`. Noise-robust for small samples.
3. **Scribe session-start catch-up routing pass (Edit 1.5)** added so a missed session close doesn't orphan new lessons.
4. **MCP embedder background warm-up thread** added to server.py `__main__` so first query doesn't stall on 5-15 second model load.
5. **Parametric DPO deferred to v2**, SFT is the MVP format.
6. **`has_table` threshold raised 5 → 10 rows** in the scribe routing predicate. Prevents summary tables (5-rowers) from being over-routed.
7. **"Continuous 14-day sweep" filed as a retrospector lesson / v2.3 protocol candidate**, not a deliverable change.

From moderator debates (2 resolutions):

1. **C-deeper-1**: Routing predicate `AND` (length AND type), length threshold 1500 initially, tunable.
2. **C-deeper-2**: Hook B ships with **MemX exact defaults** (0.45/0.25/0.05/0.10, not empiricist's adjustment) + per-factor logging. Retune after 50 real queries.

From cartographer correction:

1. **Topic files live at `~/.claude/agent-memory/<agent>/<topic>.md` (flat)**, NOT `<agent>/topic/<topic>.md` (nested). The user's brief's phrasing was a slip; the scribe-edit-plan uses the correct flat layout per `code.claude.com/docs/en/memory` § "Storage location" verbatim.

## What the v2 gates caught (this round's retrospective preview)

- **Synthesist claim matrix**: surfaced 2 load-bearing contradictions requiring moderator. Both resolved to conservative middle ground.
- **Moderator**: reverted empiricist's ranker weight adjustment in favor of MemX defaults + observability. Also ratified `AND` predicate with tunable threshold.
- **Skeptic**: **7 attacks, 6 in-session corrections applied directly to the deliverable files**, 1 filed as protocol improvement. The skeptic was the most productive gate this round — producing material edits to scribe-edit-plan.md, mcp-scaffold.md, linguist.md, and parametric-spec.md.
- **Adversary**: caught MemPalace's second methodology violation (2026-04-11 issue #649 offline-first), strengthening REJECTED. Classified 10 new sources with explicit MIXED/STRONG-PRIMARY distinctions. Cleared the deliverables' citations for audit.
- **Evaluator**: all 5 rubric dimensions PASS. Factual accuracy + citation accuracy + completeness + source quality + tool efficiency verified end-to-end.

## Open questions and explicit caveats

1. **Parametric timeline is multi-year at solo pace**. Akash should not expect LoRA distillation to become actionable in 2026-Q3. With 5 active teams it becomes viable ~12-18 months out. The parametric phase is in the plan for architectural completeness, NOT as a near-term build. Documented in empiricist.md § "Decay gate re-visited".

2. **LatentMAS's HF+vLLM hybrid is under-documented**. The paper and README suggest vLLM integration; the actual code uses HF Transformers for the compact step. Anyone porting LatentMAS to a vLLM-only stack is going to be surprised. Filed as retrospector Lesson 17.

3. **ByteRover is 10 days old**. No independent audit yet (no issue-214-style reproduction). The AKL formula + schema borrowings are based on the paper + cross-check with the CLI README. If ByteRover is later audited and found to have methodology issues, the borrowed specs remain architecturally sound (they're simple formulas with no embedded benchmark claims) but the source classification could slip from MIXED to REJECTED.

4. **The empirical trigger for Hook B depends on scribe diligence**. If Akash skips end-of-session retrospector/scribe dispatches, the miss-event counter never updates and Hook B never triggers. The catch-up routing pass (Edit 1.5) partially mitigates this by recovering orphaned lessons, but it doesn't recover orphaned MISS events. Mentioned in scribe-edit-plan.md rollback section.

5. **The MCP server's sqlite-vec 0.1.9 stable** ships with alphas (0.1.10a1-a3) active on 2026-04-01. If the Engineering Team builds Hook B weeks from now, they should re-check whether 0.1.10 is stable by then and upgrade. Mentioned in librarian.md.

## NEXT STEPS

1. **This week**: Apply the 7 Edit diffs from `EVIDENCE/scribe-edit-plan.md` to research-scribe.md and research-lead.md. Run a smoke-test research session to verify Hook A routing fires correctly on a deliberate long-tail lesson.

2. **Over the next 4-5 weeks**: Run research sessions as normal. The scribe logs `scribe-metric:` lines. After 10 sessions, run the distinct-miss-event count. If ≥ 3, trigger Phase 2 (Hook B build).

3. **Q3 2026 (or whenever Akash has an evening)**: Execute the LatentMAS spike per `EVIDENCE/hook-c-spike-plan.md`. Produce SPIKE_REPORT.md with GO/DEFER/NO-GO. Gate Hook C production proposal on GO.

4. **Continuous**: The retrospector's lesson-writing continues to populate MEMORY.md. When the stable-lesson count approaches 300 (monthly count), the parametric phase triggers. Realistically 6-18 months out.

5. **Continuous monitoring**: v2.3 protocol revision — consider adding a continuous 7-day fresh sweep at session start for fast-moving topics. Filed as retrospector process improvement, not a deliverable for this round.

## Definition-of-done check

- [x] Hook A full edit diffs (old/new pairs) ready for the Edit tool — `EVIDENCE/scribe-edit-plan.md` has 7 edits
- [x] Hook B MCP server scaffold + schema DDL + ranker + settings.json + failure modes — `EVIDENCE/mcp-scaffold.md`
- [x] Hook C spike plan with gh clone commands, file map, go/no-go — `EVIDENCE/hook-c-spike-plan.md`
- [x] Parametric phase data spec, training config, evaluation, timeline — `EVIDENCE/parametric-spec.md`
- [x] IMPLEMENTATION_SEQUENCE.md ordered 30-step checklist — `IMPLEMENTATION_SEQUENCE.md`
- [x] 0-14 day fresh sweep results + plan invalidation check — `EVIDENCE/historian.md` + `EVIDENCE/adversary.md`
- [x] Skeptic deeper pass + 6 in-session corrections — `EVIDENCE/skeptic.md`
- [x] Adversary corpus verdict on 10 new sources — `EVIDENCE/adversary.md`
- [x] Evaluator PASS on all 5 rubric dimensions — `EVIDENCE/evaluator.md`
- [x] Retrospector lessons for deeper rounds appended to MEMORY.md — `EVIDENCE/retrospector.md` (lessons 14-18)
- [x] SYNTHESIS.md summarizing deliverables — this file
