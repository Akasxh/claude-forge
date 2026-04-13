# research-lead — persistent agent memory

This file is curated by `research-retrospector` (appends) and `research-scribe`
(dedup / merge). The research-lead reads the first 200 lines / 25KB at the
start of every session — either via the Claude Code runtime's `memory: user`
auto-injection if enabled, or explicitly as Step 3 of the intake protocol
in `research-lead.md`.

These lessons are **binding on dispatch decisions**. If a lesson contradicts
a static instruction in `~/.claude/agents/research/research-lead.md`, follow
the lesson and surface the contradiction in `LOG.md`.

---

## Starter playbook (seeded 2026-04-12 from Round 2 prior-art sweep)

### Dispatch breadth follows Anthropic's published scaling rule
- **Observed in**: self-evolve-v2 (2026-04-12) via prior-art sweep
- **Failure mode addressed**: FM-1.1 (task specification)
- **Lesson**: Anthropic's own multi-agent research system reports that simple
  fact-finding needs 1 agent with 3-10 tool calls, comparisons need 2-4
  subagents with 10-15 calls each, and complex research needs 10+.
  Deviating in either direction degrades quality. "50 subagents for a simple
  query" is their single most-cited failure mode.
- **Rule of thumb**: Dispatch the planner BEFORE the opener. Read its
  recommendation and only override with a logged reason.
- **Counter-example / bounds**: When the question is a single fact check with
  a known authoritative source, skip the team entirely and look it up yourself.
  Over-dispatch on trivial questions is itself a failure mode.

### Parallel tool calling is a 10x force multiplier
- **Observed in**: self-evolve-v2 (2026-04-12)
- **Failure mode addressed**: FM-1.3 (step repetition) inverted — serial
  dispatch is time waste.
- **Lesson**: Anthropic reports 90% research-time reduction from spawning
  3-5 subagents in parallel AND having each subagent make 3+ parallel tool
  calls. Serial dispatch within a round is a bug, not a safe default.
- **Rule of thumb**: Every round-N dispatch must be a single `Agent()`
  emission with all specialists spawned concurrently. If you find yourself
  writing a second `Agent()` call in the same round, ask whether the
  second specialist actually depends on the first's output — if not,
  combine them.
- **Counter-example / bounds**: When specialist B literally needs
  specialist A's output to formulate its sub-question, serial is correct.

### The skeptic attacks reasoning; the adversary attacks the corpus
- **Observed in**: self-evolve-v2 (2026-04-12)
- **Failure mode addressed**: FM-3.3 (incorrect verification)
- **Lesson**: Anthropic's published failure list includes "choosing
  SEO-optimized content farms over authoritative sources" — a failure the
  skeptic, looking at a paraphrased claim, literally cannot see. The
  adversary (corpus-level red team) owns this failure mode as a separate
  lens. In v2 we dispatch both, not one or the other.
- **Rule of thumb**: If the evidence for a claim came from a URL, the
  adversary must clear it before "high confidence". Skeptic clearing
  alone is not enough.
- **Counter-example / bounds**: For questions grounded entirely in a local
  codebase (no web sources), the adversary pass is optional.

### Contradictions go to the moderator, not to your own judgment
- **Observed in**: self-evolve-v2 (2026-04-12)
- **Failure mode addressed**: FM-2.5 (ignored other agent's input)
- **Lesson**: Claude Code's agent-teams documentation explicitly recommends
  debate-structured investigation for contradictions: "once one theory is
  explored, subsequent investigation is biased toward it." You, the lead,
  have the same bias because you're also the synthesizer. When two
  specialists disagree on a load-bearing claim, dispatch the moderator for
  a 3-round debate. Your verdict is not trustworthy because you're not
  disinterested.
- **Rule of thumb**: Any contradiction flagged in `synthesist.md` that
  affects the final answer gets a moderator dispatch, no exceptions.
- **Counter-example / bounds**: Trivial or scope-mismatch "contradictions"
  (same word, different meanings) go to the linguist first; only real
  evidential disagreements warrant a full debate.

### End-state evaluation beats path evaluation
- **Observed in**: self-evolve-v2 (2026-04-12)
- **Failure mode addressed**: FM-3.1 (premature termination)
- **Lesson**: Anthropic: "end-state evaluation for stateful systems, not
  turn-by-turn analysis. Success means agents achieved the correct final
  state regardless of path taken." The evaluator grades the synthesis, not
  the process. A messy but correct path passes. A clean but wrong path fails.
- **Rule of thumb**: Do not optimize for short LOG.md. Optimize for a
  SYNTHESIS.md that the evaluator's 5-dim rubric can pass.
- **Counter-example / bounds**: For cost-constrained sessions, watch
  tool-efficiency (dim 5) — it's the only rubric dimension that indirectly
  grades the path.

### Self-improvement lives in MEMORY.md, not in ad-hoc prompt edits
- **Observed in**: self-evolve-v2 (2026-04-12) via ACE paper
- **Failure mode addressed**: cross-session learning gap
- **Lesson**: The ACE (Agentic Context Engineering, arxiv 2510.04618) paper
  shows that evolving-playbook approaches (generation/reflection/curation)
  beat fine-tuning for agent self-improvement: +10.6% on agent benchmarks,
  +8.6% on finance, with no labeled supervision. Our retrospector + scribe
  pair is literally an ACE implementation. Trust the process: write
  lessons here, don't patch agent files mid-session.
- **Rule of thumb**: When you notice a process bug during a session,
  note it in `OPEN_QUESTIONS.md` for the retrospector to distill at
  session close. Do not try to fix the static agent files mid-session.
- **Counter-example / bounds**: If the bug is a frontmatter error (e.g. a
  specialist file missing `effort: max`), fix it immediately — that's a
  config bug, not a lesson.

### Subagents cannot spawn subagents — plan accordingly
- **Observed in**: self-evolve-v2 (2026-04-12) — skeptic pass attack #5
- **Failure mode addressed**: architectural constraint, not a MAST mode
- **Lesson**: Claude Code subagents cannot spawn other subagents. When
  research-lead is invoked as a subagent of the main Claude Code session,
  it cannot actually dispatch the 17 specialists — it must execute the
  protocol itself by reading the specialist files as reference prompts and
  running the tool calls directly. The specialist files are then behavioral
  contracts, not independent processes. For a "true" multi-agent run,
  invoke research-lead via `claude --agent research-lead` OR have the main
  session adopt research-lead as its behavioral contract and dispatch the
  specialists via its own Agent tool.
- **Rule of thumb**: If you find yourself running a multi-round investigation
  as a subagent, the specialist files become reference prompts — read them,
  execute their method, write their output files yourself. The gate order
  (planner → wide → synthesist → moderator → skeptic → adversary → evaluator
  → retrospector) still holds.
- **Counter-example / bounds**: When invoked via `claude --agent research-lead`
  (main thread), the allowlist and sub-dispatching work normally.

### When the user prompt is short, distrust your initial sub-question list to catch the latest 14 days
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) — v1 missed Latent Briefing, MemPalace, MAGMA, EverMemOS, and the 47-author taxonomy paper that ended up structuring the synthesis
- **Failure mode addressed**: FM-1.1 (disobey task specification) at the literal-reading layer
- **Lesson**: short user prompts on fast-moving topics ("research X", "check HN about Y") deserve dispatch breadth that includes "what shipped in the last 14 days that I might not know about?" as its own explicit sub-question. v1 of the memory-layer session missed the entire April 2026 release window because the planner's sub-question list was based on prior knowledge of canonical papers, not on a fresh-window scan. The user had to point out the gap to trigger a v2 relaunch. Don't make the user do that work.
- **Rule of thumb**: at the planner stage, if the topic is producing arxiv submissions weekly (agent memory, LLM serving, RL post-training, multi-agent infra are current 2026 examples), add a "newest 14 days" sub-question dispatched to web-miner OR historian as a structural sweep. NOT discretionary.
- **Counter-example / bounds**: for slow-moving topics (canonical CS, stable libraries, established protocols), the 14-day sweep finds nothing and is waste. Skip.

### Adversary catches what skeptic cannot: corpus-level fraud
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) — MemPalace case study
- **Failure mode addressed**: FM-3.3 (incorrect verification), corpus-capture variant
- **Lesson**: the skeptic, attacking the synthesis from inside, ratifies "the source claims X" if the synthesis correctly paraphrases X. Fraudulent benchmarks live one layer below: the source claims X but X is not what the source measured. MemPalace is the cleanest 2026 case — 21.7K stars in a week, 1.5M X.com views, 96.6% LongMemEval claim that actually measured ChromaDB's default embedding (not MemPalace), 100% LongMemEval claim that was hand-tuned with 3 patches for the 3 failing dev-set questions, 100% LoCoMo claim that used `top_k=50` on 19-32 item haystacks (retrieving the whole pool). Three independent audits exposed it; the maintainer acknowledged. The skeptic could not have caught this. The adversary did.
- **Rule of thumb**: when a source presents a benchmark headline, adversary checks (a) is the benchmark the right one, (b) was the test run honestly, (c) is there an independent audit or reproduction. Skeptic checks if the synthesis follows from the source. Both must run on heavily-SEO-gamed topics; one is not enough.
- **Counter-example / bounds**: for sources with no quantitative claims (architectural blog posts, opinion pieces), adversary shrinks to provenance + corpus-capture checks; skeptic alone is sufficient.

### REFRAME is a valid moderator verdict — don't force winner-take-all on mis-posed debates
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) — debate C4 "is Claude Code's existing memory mechanism insufficient?"
- **Failure mode addressed**: FM-2.5 (ignored other agent's input) + FM-2.3 (task derailment)
- **Lesson**: moderator debate verdict types should be {A_WINS, B_WINS, COMPLEMENTARITY, REFRAME, DEFER} — not just A_WINS or B_WINS. C4 was the most important debate of the memory-layer session, and the right verdict was REFRAME — both sides were partially right, the question itself was mis-posed. If the moderator had been forced to pick A or B, the synthesis would have either thrown away Akash's working ACE-pattern (wrong) or denied that any cells were uncovered (also wrong). The reframe to "what cells of the forms × functions × dynamics taxonomy are partially or not covered" produced the actionable answer.
- **Rule of thumb**: when both sides make defensible primary-source arguments, ask "is the question being asked the right one?" before forcing a verdict. REFRAME is the highest-value moderator output when available.
- **Counter-example / bounds**: for clean empirical disagreements ("did benchmark X return Y or Z?"), REFRAME is a dodge — insist on a winner backed by a primary measurement.

### Reuse v1 evidence on rerun; append addenda, don't rewrite
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) — v2 relaunch reused v1's planner.md, librarian.md, historian.md, web-miner.md, github-miner raw cache; added historian-addendum.md instead of rewriting historian.md
- **Failure mode addressed**: FM-1.3 (step repetition) + tool efficiency
- **Lesson**: when a session is relaunched (user-triggered correction, evaluator FAIL re-dispatch, or supplementary intel addition), the lead's first action is to inventory every existing EVIDENCE/*.md file and classify as REUSE, EXTEND, or REWRITE. Reused files saved ~20 tool calls in the memory-layer relaunch. Extension via addenda (historian-addendum.md) is preferred over rewrites because it preserves provenance and shows the additive scope cleanly.
- **Rule of thumb**: REUSE if the file passes adversary classification and the gap is "missing X," not "wrong about X." REWRITE only if the file has factual errors. EXTEND via `<file>-addendum.md` if you're adding new content but want to preserve the original's audit trail.
- **Counter-example / bounds**: if v1's claim matrix or contradictions list is wrong, the synthesist file should be rewritten — claim matrices are forward-looking and don't preserve well across appends.

### REPORTED-NOT-VERIFIED is a valid evidence tier on paywalled / unreachable primaries
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) — Ramp Labs Latent Briefing primary X.com source returned HTTP 402, but direction was triangulated by LatentMAS (arxiv 2511.20639) + LRAgent (arxiv 2602.01053) + MemOS MemCubes (arxiv 2507.03724)
- **Failure mode addressed**: FM-3.2 (incomplete verification) inverted as binary "verified or omit"
- **Lesson**: source quality is a 4-tier scale: STRONG-PRIMARY → MIXED → REPORTED-NOT-VERIFIED → REJECTED. When a primary is unreachable but the direction has ≥2 independent corroborating sources, cite the primary, mark numbers as REPORTED-NOT-VERIFIED, and let the synthesis use the direction (not the specific numbers) as load-bearing. Don't omit; don't pretend verification.
- **Rule of thumb**: a single REPORTED-NOT-VERIFIED source can support a directional claim ("latent-state sharing reduces multi-agent token cost") but not a numerical claim ("by exactly 31%"). For numerical claims, downgrade the relevant section's confidence to MEDIUM and explicitly caveat in SYNTHESIS.md.
- **Counter-example / bounds**: if no independent corroboration exists, REPORTED-NOT-VERIFIED collapses to NOT_USABLE — drop the source. Single-witness paywalled claims are not evidence.

### Deeper rounds reuse pilot evidence; only write specialists for NEW sub-questions
- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12)
- **Failure mode addressed**: FM-1.3 (step repetition) + tool efficiency
- **Lesson**: when a deeper round follows a pilot on the same question (not a new question), the lead's first action is to classify each pilot evidence file as REUSE (read as reference, cite from), EXTEND (add an `-addendum.md`), or REWRITE (only if wrong). The deeper round of the memory-layer question reused ALL 10 pilot evidence files as REUSE; no addenda were needed because the pilot files answered the strategic question and the deeper sub-questions were implementation-grade additions. Specialists for the deeper round wrote their own files for the new sub-questions only. Estimated savings: ~25+ tool calls vs starting from scratch.
- **Rule of thumb**: on a deeper round, enumerate pilot evidence files at Round 0. For each, decide REUSE / EXTEND / REWRITE based on whether the deeper sub-questions require new primary-source fetches. Default to REUSE for any file that answered a strategic question; write new files only for NEW sub-questions. Use a new slug like `<pilot-slug>-deeper` or `<pilot-slug>-implementation` and a new workspace — do not extend the pilot workspace in place.
- **Counter-example / bounds**: a "deeper" round that turns out to be a NEW question (different scope, different answer shape) is actually a new session — use a new slug, new workspace, and do not pretend to reuse evidence from a different question. Conversely, for tiny corrections to a pilot synthesis (typos, one-sentence fixes), just patch the pilot SYNTHESIS.md directly and note the patch in its LOG.md — don't bother with a new workspace.

### Borrow published specs, don't adopt commercial-source-available products
- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — skeptic Attack 1 on ByteRover (arxiv 2604.01599 + campfirein/byterover-cli 4.4K stars Elastic License 2.0)
- **Failure mode addressed**: FM-3.3 (corpus capture, commercial-source-available edition)
- **Lesson**: a published paper + a 4.4K-star production CLI can BOTH be valuable reference architectures without being adopted as dependencies. The right level of borrowing is: cite the paper's specific technical contributions (AKL formula, maturity tier thresholds, YAML frontmatter schema) verbatim with attribution, and do NOT adopt the CLI binary or the Elastic License 2.0 code. Mixing ELv2 into an MIT/Apache stack introduces a commercial-service restriction that constrains future team sharing.
- **Rule of thumb**: when a source is simultaneously a paper AND a product (arxiv + commercial CLI), classify it as MIXED and borrow at the SPEC level not the PRODUCT level. Cite the paper with section numbers; do not install the CLI. Every formula/algorithm/schema borrowed must include attribution to the paper's section.
- **Counter-example / bounds**: if a product is pure OSS (Apache/MIT) with published benchmarks that survive adversary audit, direct adoption is fine. The ELv2 case is specifically commercial-source-available.

### The moderator can revert an empiricist's proposal in favor of a published default + observability
- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — debate C-deeper-2 (MemX ranker weights)
- **Failure mode addressed**: FM-2.5 (ignored other agent's input) + empirical-tuning overreach
- **Lesson**: the empiricist proposed adjusted MemX ranker weights based on a-priori reasoning about Akash's small corpus. The moderator debate concluded that shipping MemX's published defaults + per-factor logging is the right MVP choice. The empiricist's reasoning was theoretically sound but untested; the published defaults are backed by a benchmark. The right pattern for tuning is: ship published defaults, instrument the system to log per-factor contributions, observe real data, retune. Domain-knowledge adjustments are a hypothesis not a fact.
- **Rule of thumb**: when an empiricist proposes tuning a published parameter based on reasoning (not measurement), the moderator defaults to published values + observability, not the adjustment. Empirical tuning happens after real data, not before. The empiricist may still be right — ship observability so the data decides.
- **Counter-example / bounds**: if the empiricist's adjustment is backed by a measurement on Akash's actual workload (not a-priori reasoning), the adjustment wins. The distinction is "domain reasoning" vs "observed measurement."

### Verify "integrates with framework X" claims by reading the actual code
- **Observed in**: claude-memory-layer-sota-2026q2-deeper (2026-04-12) — LatentMAS (github.com/Gen-Verse/LatentMAS) code inspection
- **Failure mode addressed**: FM-3.3 (incomplete verification — not checking that a claim's scope matches reality)
- **Lesson**: the LatentMAS paper and README emphasize vLLM integration. The actual code (`methods/latent_mas.py` lines 289-420 `run_batch_vllm`) uses vLLM ONLY for the final text-generation step. The compact-then-attend latent pattern uses HuggingFace Transformers' `past_key_values` via `transformers.cache_utils.Cache`, slicing tensors manually. Anyone who reads the paper and expects to port LatentMAS to a vLLM-only stack will be surprised. When a paper claims "uses framework X", verify whether X is used in the CORE method or only in a PERIPHERAL step.
- **Rule of thumb**: for any paper whose novelty depends on integrating with a specific framework, read the actual code (not just the README) before scoping an integration or spike. "Uses vLLM" can mean "uses vLLM's generate API for text output while the core algorithm runs on HF Transformers." When in doubt, the github-miner specialist should map the function-by-function import graph.
- **Counter-example / bounds**: for papers with clean architectural separation (e.g. "we use vLLM as the inference engine for our agent loop"), the claim is usually literal. The misleading case is specifically when a paper's novelty is in a step that the claimed framework's public API doesn't support — then the paper quietly falls back to another framework for that step.

## Added from engineering-team-self-evolve-v1.md at 2026-04-12

### Empiricist finds what tracer misses on concurrency
- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — flock child-process inheritance leak caught in Test 3f
- **Failure mode addressed**: FM-3.2 (untested claim), concurrency variant
- **Lesson**: when the tracer designs a cross-process primitive from man pages, the empiricist MUST test on the actual runtime. Man pages describe primitives; they don't describe composition. In this session, `flock -c 'sleep 30'` leaks the lock via child-fd inheritance when the parent is killed. Empiricist caught it, proposed `timeout --signal=KILL --kill-after=1 <N> bash -c`, verified the fix. Canonical merge pattern uses the corrected wrapping.
- **Rule of thumb**: any concurrency or filesystem protocol that crosses process boundaries needs both tracer (paper) and empiricist (real-system). Skipping the empiricist ships races that look right on paper.
- **Counter-example / bounds**: pure-in-process reasoning (no fork/exec) can rely on tracer alone.

### Mod REFRAME applies to meta-design debates
- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — C1 "engineering-synthesist as specialist vs lead-absorbed"
- **Failure mode addressed**: FM-2.5 (ignored other agent's input) + FM-2.3 (task derailment)
- **Lesson**: the REFRAME verdict (from MEMORY.md lesson 10) generalizes from domain-level debates to META-design debates. C1's reframe converted a roster question ("add a synthesist specialist?") into a protocol question ("add a structural-consistency-check STEP that dispatches moderator conditionally"). This broadens lesson 10: REFRAME is valid whenever a binary yes/no debate is really a question about the right level of abstraction — roster vs protocol, specialist vs step, role vs capability.
- **Rule of thumb**: when a debate sounds like "should we add X specialist?", the REFRAME answer is often "the capability is load-bearing but the delivery mechanism is wrong — name the capability, dispatch it conditionally via an existing role or protocol step." Grow protocol before roster.
- **Counter-example / bounds**: if a genuinely new failure mode has no existing owner, add a specialist; REFRAME is inappropriate.
- **Reinforced by**: strengthens MEMORY.md lesson 10 — "REFRAME is a valid moderator verdict" now has "including meta-design debates" in its scope.

### Adopted-persona pattern 2 is universal to team leaders
- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — ran full v2 protocol in adopted-persona mode from within a research-lead subagent invocation
- **Failure mode addressed**: architectural constraint (not a MAST mode) — subagents cannot spawn subagents
- **Lesson**: the adopted-persona pattern 2 from research-lead is not research-specific. It is the universal load-bearing defense against Claude Code's "subagents cannot spawn subagents" constraint, and it applies to every team leader. Engineering-lead inherits it verbatim. Every future team leader (planning-lead, qa-lead, devops-lead, etc.) should inherit it verbatim. Copy, don't adapt.
- **Rule of thumb**: when writing a new team leader persona, copy the adopted-persona pattern 2 section verbatim from research-lead (or engineering-lead). Do not paraphrase — the pattern is protocol-procedural.
- **Counter-example / bounds**: only applies while subagent-spawn is architecturally blocked. If Claude Code adds nested subagent spawning, the pattern becomes optional.

### Self-evolving team design starts from a research session
- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — this session IS the canonical self-evolving pattern for team design
- **Failure mode addressed**: premature team design, missing prior art, single-source design
- **Lesson**: research-team v2 and engineering-team v1 both came out of a research session on their own design space. To build a new team, run the research team first with "design team X" as the question. Research's adversarial gates catch design flaws before they ship into the new team's protocol. Strictly better than writing a new team from direct prior knowledge because (a) forces prior-art sweep, (b) adversary catches benchmark-gaming, (c) empiricist validates runtime claims, (d) the MEMORY.md meta-loop compounds across teams.
- **Rule of thumb**: do NOT write a new team's PROTOCOL.md directly from a prompt. Always run `research-lead` first on "design team X" as a research session. Use research SYNTHESIS.md as binding input to the new team's personas and PROTOCOL.
- **Counter-example / bounds**: for single-persona updates or trivial specialist changes, full research is overkill. But for NEW TEAM design, research first is mandatory.

### 14-day freshness sweep catches benchmark integrity crises
- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — web-miner's sweep surfaced OpenAI's SWE-Bench Verified contamination audit and the 80.9% → 45.9% Pro score gap
- **Failure mode addressed**: FM-1.1 (task specification) at "wrong reality model" layer
- **Lesson**: the 14-day freshness sweep (from lesson 8) pays for itself again on benchmark-laden topics. For fast-moving topics where benchmark-gaming is ongoing, the sweep must include "has the benchmark been audited or disputed in the last 30 days" — not just "what shipped." Without this sweep, this session would have calibrated the engineering-team gate structure for the wrong base rate (80% Verified contamination) instead of the real ~45% Pro.
- **Rule of thumb**: for topics where benchmarks are load-bearing, the 14-day sweep MUST include benchmark-integrity checks (audits, disputes, re-evaluations), not just release activity.
- **Counter-example / bounds**: for stable canonical domains (type theory, algorithms textbooks, long-frozen standards), benchmarks don't evolve week-to-week; skip.
- **Reinforced by**: strengthens MEMORY.md lesson 8 — "14-day freshness sweep" now has a benchmark-integrity sub-rule.

## Added from orchestration-full-activation-v1.md at 2026-04-12

### Evidence-file-as-contract is the full-activation enforcement pattern
- **Observed in**: orchestration-full-activation-v1 (2026-04-12) — designed to solve Akash's "smartest guy active" / "want everyone active" failure mode
- **Failure mode addressed**: FM-1.2 (disobey role specification) + FM-1.3 (step repetition) + FM-2.4 (information withholding) + FM-3.2 (no verification) — 5 simultaneous MAST modes per linguist §1
- **Lesson**: the winning pattern for enforcing "every specialist actually runs with its distinct lens" is a port of the 50-year-old Make / Snakemake target-as-contract model adapted to LLM multi-agent workflows. Components: (1) pre-flight `EXPECTED_EVIDENCE.md` contract at Round 0, (2) `~/.claude/scripts/audit_evidence.py` called via Bash at two gate points (mid-flight and synthesis), (3) per-role citation/structural-depth schema calibrated against 49 real evidence files (MIN_LENS_BYTES=2000, MIN_H2=4, role-specific citation thresholds), (4) Magentic-One `max_stalls=3` bounded retry, (5) optional PostToolUse observational hook `log-evidence-writes.sh` for audit-trail telemetry, (6) retrospector grades compliance in MEMORY.md as SOFT social enforcement.
- **Rule of thumb**: at Round 0 end, write `EXPECTED_EVIDENCE.md`. At Round 1→Round 2 boundary, run `audit_evidence.py --gate=mid-flight`. Before drafting SYNTHESIS.md, run `audit_evidence.py --gate=synthesis --strict`. Both calls must return exit 0. The primary enforcement is discipline, structurally scaffolded by the audit script. Full spec in `~/.claude/teams/research/PROTOCOL.md` v2.1 § "Evidence-file-as-contract".
- **Counter-example / bounds**: for engineering teams (not research), social enforcement delayed by one session is unacceptable. Engineering should use runtime-level enforcement (main-thread git pre-commit hooks, CI gates) that block at tool-call time. The research v2.1 model is social-enforcement-tolerable because research errors are recoverable.

### Claude Code subagent PreToolUse hooks do NOT reliably fire in v2.1.101
- **Observed in**: orchestration-full-activation-v1 (2026-04-12) — 8+ OPEN issues on anthropics/claude-code vs docs that say the opposite
- **Failure mode addressed**: FM-3.2 (no verification) inverted — trusting docs without runtime verification
- **Lesson**: Anthropic docs at `code.claude.com/docs/en/hooks` describe PreToolUse hooks firing for subagent tool calls with `agent_id`/`agent_type` in the payload and `exit 2` blocking the call. The runtime does NOT reliably honor this. anthropics/claude-code#43612 (filed 2026-04-04, OPEN) traced the bug into `cli.js` v2.1.92: `_R()` has `if (U6(process.env.CLAUDE_CODE_SIMPLE)) return;` that short-circuits the hook runner in subagent context. anthropics/claude-code#43772 (2026-04-05): subagents with `bypassPermissions: default` (Akash's mode) bypass hooks entirely — 3 unauthorized commits documented. anthropics/claude-code#40580 (2026-03-29): hook is called, returns exit 2, runtime ignores the exit code. anthropics/claude-code#34692 comment: PostToolUse IS working in v2.1.89+ (non-blocking, observational only). Do NOT build runtime enforcement on subagent hook firing in the current runtime.
- **Rule of thumb**: when librarian cites a Claude Code doc claim about hooks or subagent behavior, cross-check with `gh api search issues` on anthropics/claude-code. If there are recent OPEN issues contradicting the doc, treat the doc as REPORTED-NOT-VERIFIED per lesson 13. Main-thread PreToolUse hooks DO work reliably — the bug is subagent-specific. PostToolUse works for observation.
- **Counter-example / bounds**: if the runtime bug closes in a future Claude Code version, revisit. Main-thread pre-commit-style enforcement is always reliable. This lesson targets the specific v2.1.101 runtime as of 2026-04-12.

### 4 concurrent background subagents is the parallel-team empirical ceiling
- **Observed in**: orchestration-full-activation-v1 (2026-04-12) — 4 sibling sessions ran concurrently during this session; 3 closed successfully (engineering-team-self-evolve-v1, claude-memory-layer-sota-2026q2-deeper, capability-forge-self-evolve-v1) while this one was still running
- **Failure mode addressed**: under-dispatch AND over-dispatch — running more than 4 parallel causes silent deaths via 529 Overloaded
- **Lesson**: for parallel team orchestration via `Agent(background: true)` subagents, the practical ceiling is 4 concurrent teams. anthropics/claude-code#41911 (OPEN): 3+ parallel subagents under peak API load hit 529 Overloaded errors and die silently with lost work. anthropics/claude-code#36195 (OPEN): 3-4 parallel foreground subagents freeze after 15-30 min, unblock on Ctrl+B (move to background). anthropics/claude-code#46421 (OPEN): cache reads accumulate multiplicatively across parallel subagents, inflating API spend 3-5x vs evidence file size. Use `background: true` (mandatory, not optional) and cap at 4. If 529 errors appear within 5 min of launch, reduce concurrent ceiling by 1 with exponential backoff.
- **Rule of thumb**: main session dispatch pattern is `Agent(subagent_type="<lead>", prompt="<amplified question with slug>", background: true)` with ≤ 4 concurrent. Queue additional teams. Never use foreground parallel dispatch for > 2 teams. Dashboard via `bash ~/.claude/scripts/team_status.sh` (stateless, filesystem-only). Context safety: per-team context budget in main session is ~50 KB (read QUESTION/HYPOTHESES/LOG tail/SYNTHESIS — do NOT read full evidence files or transcript JSONL).
- **Counter-example / bounds**: off-peak API load may tolerate > 4, but not reliably. Akash's Linux environment matched the issue reporters' claims empirically during this session.

### Dogfood the design session against its own running sibling sessions
- **Observed in**: orchestration-full-activation-v1 (2026-04-12) — 4-session parallel meta-test Akash designed empirically validated PH1-PH4 as BYPRODUCTS of this session's running
- **Failure mode addressed**: over-reliance on theoretical predictions without empirical ground truth
- **Lesson**: when designing infrastructure for parallel or concurrent multi-agent workflows, RUN IT during the design session itself. Dogfooding produces empirical signal that theoretical analysis misses: specific size distributions of evidence files across honest sessions, specific timing of sibling-session closures, specific cache-read inflation ratios, specific 529 thresholds. Akash's 4-session parallel meta-test validated the parallel orchestration pattern as a side effect of running this session. This was not a separate empirical experiment; it was continuous observation during the main session with tracer §1 and empiricist §4 capturing the data.
- **Rule of thumb**: for any protocol-design session about multi-agent or multi-session coordination, dispatch ≥ 2 sibling sessions in parallel BEFORE writing the synthesis. Reference their live state in tracer / empiricist / cartographer evidence files. Use the 4-session meta-test pattern from this session as canonical.
- **Counter-example / bounds**: for protocol designs about single-agent or single-session flows (code quality, citation schemas, etc.), the sibling-session overhead is unjustified — dogfood the single session instead.

### Retrospector-as-social-enforcement is delayed by one session and only works for research
- **Observed in**: orchestration-full-activation-v1 (2026-04-12) — skeptic A1 attack on v2.1 lead-discipline design
- **Failure mode addressed**: FM-3.2 (no or incomplete verification) at the protocol's own enforcement layer
- **Lesson**: when enforcement is structural (not runtime-blocking), the safety net is the retrospector reading the close-audit and writing lessons to MEMORY.md that influence the NEXT session's dispatch. This correction is DELAYED by one session. A skipping lead gets flagged after the fact, not mid-session. This is acceptable for research where failure cost is "low-quality session output" (recoverable). It is NOT acceptable for engineering where failure cost is "bad code shipped" (irreversible). The research v2.1 enforcement model should NOT be copy-pasted to engineering team without hardening. Engineering needs runtime-level enforcement via main-thread git pre-commit hooks and CI gates.
- **Rule of thumb**: social enforcement (retrospector MEMORY.md grades) is acceptable when errors are recoverable; use runtime enforcement where errors are not. For research: lead-discipline + audit script + retrospector grade is sufficient. For engineering: must add main-thread PreToolUse hook enforcement (which DOES fire reliably per the bug being subagent-specific) plus pre-commit git hooks plus CI gates.
- **Counter-example / bounds**: a session where a human user is actively in the loop (the user reads SYNTHESIS.md immediately upon close) gets real-time enforcement because the user catches gaps on first read. That's still social enforcement, but real-time instead of delayed-by-one-session.
