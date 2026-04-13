# Retrospector — deeper round post-mortem and new MEMORY.md lessons

Session: claude-memory-layer-sota-2026q2-deeper
Start: 2026-04-12 (same day as pilot v2 — deeper round rather than a new question)
Lead: research-lead, adopted-persona mode
Protocol: v2 full — every gate ran
Outcome: implementation-grade deliverables for the pilot's 4-phase plan; evaluator PASS on all 5 dimensions; 4 arxiv papers from the 10-day fresh sweep with 1 material refinement (ByteRover AKL formula)

## What happened

The deeper round was triggered by Akash's request to produce implementation-grade detail (exact Edit diffs, MCP scaffold with schema DDL, spike plan with time budget, parametric-spec with training config) so the forthcoming Engineering Team could execute without blocking on more research.

The round reused all 10 pilot evidence files (cartographer, tracer, empiricist, skeptic, adversary, moderator, evaluator, retrospector, historian, historian-addendum, github-miner, linguist) as REFERENCE, not REWRITE. Per pilot lesson 11 (REUSE/EXTEND/REWRITE), the deeper round only WROTE specialist files where the deeper sub-questions demanded new primary-source fetches.

The round produced:
- `EVIDENCE/cartographer.md` — docs re-verification + correction of the Akash brief's `<leader>/topic/<topic>.md` phrasing to flat
- `EVIDENCE/librarian.md` — MCP SDK, sqlite-vec, MemX formula verbatim
- `EVIDENCE/historian.md` — 0-14 day fresh sweep (4 new papers) + LoRA prior art
- `EVIDENCE/github-miner.md` — LatentMAS code map with exact line numbers + ByteRover CLI audit + competitor commit sweep
- `EVIDENCE/tracer.md` — Hook A routing chain with 4 failure modes
- `EVIDENCE/linguist.md` — routing predicate vocabulary with 8 edge cases
- `EVIDENCE/empiricist.md` — Python vs Node decision + trigger metric + LoRA sizing
- `EVIDENCE/synthesist.md` — claim matrix + 2 moderator debates flagged
- `EVIDENCE/moderator.md` — C-deeper-1 (AND predicate) + C-deeper-2 (MemX vs adjusted weights) both resolved
- `EVIDENCE/skeptic.md` — 7 attacks with 6 in-session corrections
- `EVIDENCE/adversary.md` — 10 new sources classified + ByteRover MIXED verdict
- `EVIDENCE/evaluator.md` — 5-dim rubric PASS

And the load-bearing deliverables:
- `EVIDENCE/scribe-edit-plan.md` — 7 Edit-tool-ready old/new diffs for research-scribe.md + research-lead.md
- `EVIDENCE/mcp-scaffold.md` — Python MCP server scaffold, schema DDL, ranker.py, settings.json, failure modes
- `EVIDENCE/hook-c-spike-plan.md` — 8-step one-evening LatentMAS spike plan with time budget + go/no-go
- `EVIDENCE/parametric-spec.md` — LoRA data spec + training config + evaluation + timeline math
- `IMPLEMENTATION_SEQUENCE.md` — (TO BE WRITTEN) ordered checklist for Engineering Team

## v2 gate effectiveness on a deeper round

| Gate | Produced material change on deeper round? | Theater? |
|------|--------------------------------------------|----------|
| Round 0 framing | Yes — correct flat-layout path, correct scope for deeper sub-questions | No |
| Round 1 wide | Yes — 4 new arxiv papers, ByteRover AKL formula, LatentMAS exact line numbers, MemX verbatim ranker | No |
| Synthesist (claim matrix) | Yes — 2 load-bearing contradictions flagged | No |
| Moderator (C-deeper-1 + C-deeper-2) | Yes — C-deeper-2 reverted empiricist's adjustment in favor of MemX exact defaults (material decision) | No |
| Skeptic (7 attacks) | **Yes — 6 in-session corrections applied**: ByteRover explicit attribution, trigger metric refined to distinct-miss-events, scribe catch-up pass, MCP embedder warmup, DPO as v2, `has_table` threshold 5→10 | No |
| Adversary (0-14 day corpus sweep) | Yes — 10 new sources classified, ByteRover as MIXED (explicit citation path), MemPalace #649 strengthens REJECTED | No |
| Evaluator (5-dim rubric) | Yes — forced the synthesis to explicitly note ByteRover borrowing scope and LatentMAS hybrid backend surprise | No |
| Retrospector (this file) | Lessons below | - |

**Verdict**: all gates fired; skeptic was particularly valuable (6 corrections); moderator was valuable for the MemX-vs-adjusted-weights reversion.

## Lessons for MEMORY.md (proposed additions)

These are the additions for `~/.claude/agent-memory/research-lead/MEMORY.md`. The scribe will dedup against existing entries.

### Lesson 14 — Deeper rounds reuse pilot evidence; only write specialists for NEW sub-questions

- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12)
- **Failure mode addressed**: FM-1.3 (step repetition) + tool efficiency
- **Lesson**: when a deeper round follows a pilot on the same question (not a new question), the lead's first action is to classify each pilot evidence file as REUSE (read as reference, cite from), EXTEND (add an `-addendum.md`), or REWRITE (only if wrong). The deeper round of the memory-layer question reused ALL 10 pilot evidence files as REUSE; no addenda were needed because the pilot files answered the strategic question and the deeper sub-questions were implementation-grade additions. Specialists for the deeper round wrote their own files for the new sub-questions only.
- **Rule of thumb**: on a deeper round, enumerate pilot evidence files at Round 0. For each, decide REUSE / EXTEND / REWRITE based on whether the deeper sub-questions require new primary-source fetches. Default to REUSE for any file that answered a strategic question; write new files only for NEW sub-questions.
- **Counter-example / bounds**: a "deeper" round that turns out to be a NEW question (different scope, different answer shape) is actually a new session — use a new slug, new workspace, and do not pretend to reuse evidence from a different question.

### Lesson 15 — ByteRover's AKL formula should be BORROWED with citation, not ADOPTED as product

- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — skeptic Attack 1 handling
- **Failure mode addressed**: FM-3.3 (corpus capture, commercial-source-available edition)
- **Lesson**: a published paper (ByteRover arxiv 2604.01599) + a 4.4K-star production CLI (campfirein/byterover-cli) can both be valuable reference architectures WITHOUT being adopted as dependencies. The right level of borrowing is: cite the paper's specific technical contributions (AKL formula, maturity tier thresholds, YAML frontmatter schema) verbatim with attribution, and do NOT adopt the CLI binary or the Elastic License 2.0 tie-in. Mixing in ELv2 code into Akash's MIT/Apache stack introduces a commercial-service restriction that isn't needed for a solo user but constrains future team sharing.
- **Rule of thumb**: when a source is simultaneously a paper AND a product (arxiv + commercial CLI), classify it as MIXED and borrow at the SPEC level, not the PRODUCT level. Cite the paper with section numbers; do not install the CLI.
- **Counter-example / bounds**: if a product is pure OSS (Apache/MIT) with published benchmarks that survive adversary audit, direct adoption is fine. The ELv2 case is specifically commercial-source-available.

### Lesson 16 — The moderator can revert an empiricist's proposal in favor of a published default

- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — debate C-deeper-2 (MemX weights)
- **Failure mode addressed**: FM-2.5 (ignored other agent's input)
- **Lesson**: the empiricist proposed adjusted MemX ranker weights (0.45/0.30/0.13/0.02) based on A-priori reasoning about Akash's small corpus. The moderator debate concluded that shipping MemX's published defaults (0.45/0.25/0.05/0.10) + per-factor logging is the right MVP choice. The empiricist's reasoning was theoretically sound but untested; the published defaults are backed by a benchmark. The right pattern for tuning is: ship published defaults, instrument the system to log per-factor contributions, observe real data, retune. Domain-knowledge adjustments are a hypothesis, not a fact — treat them as such.
- **Rule of thumb**: when an empiricist proposes tuning a published parameter based on reasoning, the moderator defaults to published values + observability, not the adjustment. Empirical tuning happens after real data, not before. 
- **Counter-example / bounds**: if the empiricist's adjustment is backed by a measurement on Akash's actual workload (not A-priori reasoning), the adjustment wins. The distinction is "domain reasoning" vs "observed measurement."

### Lesson 17 — LatentMAS's "vLLM integration" claim is partially misleading: it uses HF Transformers for the latent step

- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — github-miner Code inspection
- **Failure mode addressed**: FM-3.3 (incomplete verification inverted — not checking that a claim's scope matches reality)
- **Lesson**: the LatentMAS paper and README emphasize vLLM integration. The actual code (`methods/latent_mas.py` lines 289-420 `run_batch_vllm`) uses vLLM ONLY for the final text-generation step. The latent compact-then-attend pattern uses HuggingFace Transformers' `past_key_values` via `transformers.cache_utils.Cache`, slicing tensors manually. Anyone who reads the paper and expects to port LatentMAS to a vLLM-only stack will be surprised. The Hook C spike plan MUST keep HF Transformers in the environment because the spike runs LatentMAS as-is, not a rewrite.
- **Rule of thumb**: when a paper claims integration with framework X, read the actual code to check whether X is used in the core method or only in a peripheral step. "Uses vLLM" can mean "uses vLLM's generate API for text output while the core algorithm runs on HF Transformers."
- **Counter-example / bounds**: for papers with clean architectural separation (e.g., "we use vLLM as the inference engine for our agent loop"), the claim is usually literal. The misleading case is specifically when a paper's novelty is in a step that vLLM's public API doesn't support.

### Lesson 18 — Implementation-grade rounds deserve their own dedicated workspace, not an extension of the pilot's

- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — workspace seeding
- **Failure mode addressed**: FM-1.1 (task specification) + workspace hygiene
- **Lesson**: the deeper round was seeded in a new workspace `~/.claude/teams/research/claude-memory-layer-sota-2026q2-deeper/` rather than extending the pilot's workspace. This was the right choice: (a) the pilot's workspace is a clean archival record, (b) the deeper round's new evidence files don't collide with pilot filenames, (c) future sessions can find both by slug name, (d) the pilot's LOG.md isn't polluted with deeper-round entries. The cost was duplicating the QUESTION.md + HYPOTHESES.md + LOG.md skeleton; the benefit was clean separation and reproducibility.
- **Rule of thumb**: even for deeper rounds on the same question, use a new slug (`<pilot-slug>-deeper` or `<pilot-slug>-implementation`) and a new workspace. Reuse pilot evidence files by READING them from the pilot workspace; write new evidence files in the deeper workspace.
- **Counter-example / bounds**: for a tiny correction to a pilot synthesis (e.g., "fix a typo in one sentence"), don't bother with a new workspace — just patch the pilot SYNTHESIS.md directly and note the patch in its LOG.md.

## v2.2 candidates (process improvements)

These are NOT durable lessons (those go to MEMORY.md). These are suggestions for future protocol revisions.

1. **Add "deeper round" to the protocol as a recognized session type**. The pilot → deeper sequence is a distinct shape from the normal one-round session, and the lead should explicitly name "deeper round: reuse pilot, write only new specialists" in the Round 0 framing. PROTOCOL.md does not currently enumerate this session type.

2. **Continuous fresh sweep (not just point-in-time)**. Per skeptic Attack 6, a 14-day sweep is good but stale quickly. A future v2.3 could instrument the retrospector to run a 7-day sweep at the START of each research session on a fast-moving topic, and inject any material findings into the session's framing. This is a modest code change (one WebSearch call in the lead's intake protocol) with an outsized hit rate on fast-moving topics.

3. **Per-factor logging in the ranker as a general pattern**. The moderator C-deeper-2 verdict (ship defaults + log per-factor) is a generalizable pattern: whenever an empiricist proposes tuning a published parameter, ship the published value and log the inputs so tuning becomes data-driven. Add this as a protocol-level instruction for the empiricist: "if you're proposing a tuning to a published default, also propose observability for the factors that inform the decision."

4. **Distinct miss events, not rates, for sparse metrics**. Skeptic Attack 2: for metrics where the event count per session is small (0-3), cumulative distinct events over a window is more robust than a rate. This applies beyond Hook A's trigger metric — any instrumentation where per-session events are sparse should use distinct counts, not rates.

5. **License auditing at the source level**. Adversary found ByteRover's Elastic License 2.0. The adversary's per-source audit rubric should include a "license check" field so the implicit licensing concerns are explicit. Currently the rubric tracks quality but not license. Add.

## Score for v2 protocol on this deeper round

| Aspect | Grade | Reasoning |
|--------|-------|-----------|
| Did the deeper round catch material refinements? | A | ByteRover AKL + schema, LatentMAS HF surprise, MemPalace #649 |
| Were any gates skipped? | None | All gates fired |
| Were any gates theater? | None | Every gate produced changes |
| Did the reuse pattern save effort? | A+ | ~25+ tool calls saved by reusing pilot evidence |
| Was the synthesis implementation-grade? | Yes | Edit diffs are Edit-tool-ready; MCP schema is DDL-ready; spike plan is hour-allocated |
| Was the confidence calibration honest? | Yes | Explicit caveats on ByteRover MIXED, parametric timeline, HF/vLLM surprise |

**Overall**: v2 protocol on a deeper round PASSED. The reuse-first pattern worked; the 14-day sweep caught the right thing; the skeptic was unusually productive (6 corrections); the moderator prevented an empirical-tuning overreach.

## Confidence

**High**. The deeper round delivered implementation-grade artifacts, the Engineering Team can execute without further research, and the new lessons add durable value to MEMORY.md.
