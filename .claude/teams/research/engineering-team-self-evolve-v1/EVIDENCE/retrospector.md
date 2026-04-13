# Retrospector — session post-mortem for engineering-team-self-evolve-v1

Session: engineering-team-self-evolve-v1
Date: 2026-04-12
Mode: adopted persona — ACE reflector role

## Session summary

Meta-design session: designed Engineering Team v1 as the second leader-led sub-team under the research-team v2 protocol. Output: complete 12-specialist + lead flat roster, two-phase round structure (orchestrator-worker plan + evaluator-optimizer build), cross-team handoff protocol to/from research, parallel-instance MEMORY.md concurrency protocol (flock + atomic rename + staging + timeout(1) for child-process safety), CLAUDE.md deltas, research PROTOCOL v2.1 update, and smoke test launch prompt. Evaluator PASS on all 5 dimensions (factual 1.0, citation 1.0, completeness 0.95, source quality 0.92, tool efficiency 0.85). HIGH confidence on the design, on the concurrency protocol (empirically validated with 10-concurrent-scribe race test showing 0.07s total with zero lost/duplicate writes), and on the cross-team handoff. MEDIUM confidence on specific SWE-Bench numerical claims (benchmark is contaminated per OpenAI audit; numbers downgraded to REPORTED-NOT-VERIFIED tier where primary source was not directly retrieved).

## Lessons extracted (for MEMORY.md staging)

### Lesson A — Empiricist finds what tracer misses on concurrency

- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — Test 3f revealed `flock -c` leaks lock on child-process inheritance when parent is killed
- **Failure mode addressed**: FM-3.2 (untested claim) — specifically, "reasoned from man pages" vs "verified on actual system"
- **Lesson**: when the tracer designs a concurrency primitive from man pages, the empiricist MUST test the actual runtime semantics. Man pages describe the primitive; they don't describe how `flock -c '<cmd>'` composes with child processes inheriting file descriptors. In this session, tracer's pseudocode omitted `timeout(1)` wrapping, and bare `flock -c 'sleep 30'` — when the parent is killed — leaks the lock via the sleep child holding the inherited fd. Empiricist caught this in Test 3f, proposed the fix in Test 3g (`timeout --signal=KILL --kill-after=1 <N> bash -c`), verified the fix works. The canonical merge pattern in SYNTHESIS.md is the empirically-validated version, not the tracer's paper version.
- **Rule of thumb**: any concurrency or filesystem protocol that crosses process boundaries needs both a tracer (paper reasoning) pass AND an empiricist (real-system) pass. Skipping the empiricist is how "looks right on paper" ships with a race.
- **Counter-example / bounds**: for purely-in-process reasoning (no fork/exec), tracer alone is sufficient. The rule applies when the protocol involves multiple processes or signal handling.

### Lesson B — Mod REFRAME applies to meta-design debates too

- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — C1 debate "engineering-synthesist as specialist vs lead-absorbed"
- **Failure mode addressed**: FM-2.5 (ignored other agent's input) + FM-2.3 (task derailment)
- **Lesson**: MEMORY.md lesson 10 (REFRAME is a valid moderator verdict) was seeded from the memory-layer v2 session on a domain-level debate (C4 about memory sufficiency). This session re-used REFRAME on a META-design debate (should engineering-team have a synthesist specialist?). The REFRAME verdict held: "neither specialist nor lead-absorbed — the lead runs a structural-consistency-check protocol STEP, and dispatches moderator only when that check flags a contradiction." The reframe converted a roster question into a protocol question. This broadens the lesson: REFRAME is valid whenever a binary yes/no debate is really a question about the right level of abstraction.
- **Rule of thumb**: when a debate sounds like "should we add X specialist?" the REFRAME answer is often "the capability is load-bearing but the delivery mechanism is wrong — name the capability, dispatch it conditionally via an existing role or protocol step." Don't grow the roster without capacity-check first.
- **Counter-example / bounds**: if a genuine NEW failure mode has no existing owner, adding a specialist is the right answer, not REFRAME.

### Lesson C — Adopted-persona pattern 2 generalizes to every team leader

- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — ran the full v2 protocol as adopted-persona because the session itself is a research-lead subagent, which cannot sub-dispatch
- **Failure mode addressed**: FM-1.2 (role specification) — specifically, the architectural constraint that subagents cannot spawn subagents
- **Lesson**: research-lead's adopted-persona pattern 2 ("when invoked as subagent, read specialist files as behavioral contracts and execute their methods directly") is not research-specific. Engineering-lead inherits it verbatim. Every future team leader (planning-lead, qa-lead, devops-lead, etc.) will inherit it. The pattern is a universal load-bearing defense against the Claude Code runtime's "subagents cannot spawn other subagents" constraint. It belongs in every team-lead persona file as a first-class method, not as a footnote.
- **Rule of thumb**: when writing a new team leader persona, copy the adopted-persona pattern 2 section verbatim. Do not "adapt" it — the pattern is protocol-procedural, not persona-specific.
- **Counter-example / bounds**: this only applies while subagent-spawn is architecturally blocked. If Claude Code ever adds nested subagent spawning, the pattern becomes optional and sub-dispatch becomes first-class.

### Lesson D — Self-evolving team design starts from a research session on the target team's design space

- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — this session itself was research on "how should an engineering team be structured"
- **Failure mode addressed**: cross-session learning gap + premature team design
- **Lesson**: research-team v2 came out of a research session. Engineering-team v1 came out of a research session. This is the canonical self-evolving principle: to build a new team, first run the research team on "how should this team be structured, what specialists does it need, what are failure modes of similar designs in the wild?" The research-team's adversarial gates catch design flaws before they ship into a new team's protocol. This is strictly better than writing a new team from direct prior-knowledge because (a) it forces prior-art reading, (b) adversary gate catches benchmark-gaming or SEO-corpus traps, (c) empiricist validates any runtime claims, (d) the meta-loop compounds across teams: every subsequent team benefits from the accumulated MEMORY.md lessons.
- **Rule of thumb**: do NOT write a new team's PROTOCOL.md directly from a prompt. Run research-lead first with "design team X" as the question. Use research SYNTHESIS.md as binding input to the new team's personas and PROTOCOL. Every team's v1 is a downstream engineering session of its own research session.
- **Counter-example / bounds**: for single-persona updates or trivial specialist changes, full research is overkill. But for NEW TEAM design, always research first.

### Lesson E — The 14-day freshness sweep catches benchmark integrity crises

- **Observed in**: engineering-team-self-evolve-v1 (2026-04-12) — web-miner's 14-day sweep surfaced the SWE-Bench Verified contamination finding from OpenAI's audit, Pro/Verified score gap (80.9% vs 45.9% for same Claude Opus 4.5), and the Morph LLM summary. Without the sweep, historian would have designed around the ~80% Verified number and the engineering-team gate structure would have been calibrated for the wrong base rate.
- **Failure mode addressed**: FM-1.1 (task specification) at the "wrong reality model" layer
- **Lesson**: MEMORY.md lesson 8 (14-day freshness sweep) paid for itself again in this session. For fast-moving topics, the sweep catches not just "new releases you missed" but "benchmark results you thought were authoritative are contested." The engineering-agent corpus is even more adversarial than the memory-layer corpus was — benchmark gaming is an ongoing issue, marketing content is heavy. Without the sweep, the synthesis would have been calibrated for 80% Verified (contaminated) instead of 45% Pro (real).
- **Rule of thumb**: for topics where benchmarks are cited, the 14-day freshness sweep MUST include "has this benchmark been audited / disputed / re-evaluated in the last 30 days." Not just "what shipped."
- **Counter-example / bounds**: for stable canonical CS (type theory, algorithms textbooks, etc), benchmarks don't evolve week-to-week. Skip the sweep.

## Lessons considered and rejected

- **"12 specialists is the right count for engineering teams"** — rejected as SESSION-SPECIFIC. This is a design decision for THIS team, not a transferable lesson. A future QA team might need 8. A future DevOps team might need 15. Roster-size is not a durable lesson.
- **"Two-phase structure beats strict pipeline"** — rejected as DOMAIN-SPECIFIC. This is engineering-team specific; a different team (e.g. release team) might use a strict pipeline correctly. Not transferable.
- **"CHARTER.md template"** — rejected as ARTIFACT-SPECIFIC. The template is useful, but it's a deliverable, not a process lesson.
- **"Empirical pre-flight before committing to library behavior"** — tempted, but this is really a restatement of lesson 9 (adversary catches corpus fraud) applied to runtime. Don't duplicate; strengthen lesson 9.

## Meta-observations

- **Skeptic quality this session: HIGH**. Preliminary skeptic generated 6 competing hypotheses; full skeptic produced 7 enhancements of which 6 became load-bearing SYNTHESIS sections. No rubber-stamping.
- **Adversary quality this session: HIGH**. Produced 1 rejection (content farm), 2 REPORTED-NOT-VERIFIED (X claim, Mythos number), 1 downgrade (Simon Willison retrieval anomaly), and validated the Morph LLM triangulation. Non-trivial yield.
- **Moderator quality this session: MEDIUM-HIGH**. 1 debate (C1), resolved via REFRAME per lesson 10. Produced a cleaner Phase A close protocol than either Position A or B alone. But this is only 1 debate vs the memory-layer session's 5 — relatively light moderator load, because the engineering-team design was more convergent than the memory-layer design space.
- **Empiricist quality this session: VERY HIGH**. Caught a critical flaw in tracer's pseudocode that paper reasoning missed. Ran 6 tests with raw outputs captured. Proposed and verified the `timeout(1)` correction. Without the empiricist, engineering-team v1 would have shipped with a lock-leak bug in the concurrency protocol.
- **Evaluator quality this session: HIGH**. 5-dim rubric applied consistently, 5 claims sampled, 5 citations sampled, 21 sub-questions walked. PASS verdict with documented deductions.
- **Any process bug the lead should know about**: the Simon Willison URL retrieval returned unexpected content. This may be a cache issue, URL mismatch, or genuine source drift. In future sessions, when a reputable author's URL returns unexpected content, dispatch a re-retrieval with a cache-busting parameter OR retrieve the sibling page (author's RSS, index) before downgrading.

## Handoff

Scribe should:
1. Run the MEMORY.md merge protocol (flock + timeout + atomic rename) to fold this session's staging file into `~/.claude/agent-memory/research-lead/MEMORY.md`. 5 new lessons (A-E above) added or strengthened (some strengthen existing lessons 8, 9, 10).
2. Write session entry to `~/.claude/teams/research/INDEX.md`.
3. Archive this session to `_archive/` after 90 days (standard rotation).
4. NOTE: this session does not commit code; no git-identity.sh invocation needed.

## Lessons format for MEMORY.md (5 new entries to append via staging)

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
- **Reinforced by**: strengthens existing MEMORY.md lesson 10 — add "including meta-design debates" to its bounds clause.

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
- **Reinforced by**: strengthens existing MEMORY.md lesson 8 with an explicit benchmark-integrity sub-rule.
