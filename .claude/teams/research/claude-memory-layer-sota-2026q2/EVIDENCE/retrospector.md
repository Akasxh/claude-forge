# Retrospector — session post-mortem and lessons for MEMORY.md

Session: claude-memory-layer-sota-2026q2 (relaunched as v2 pilot
with supplementary intel)
Start: 2026-04-12 (v1) → relaunched same day (v2)
Lead: research-lead, adopted-persona mode
Protocol: v2 (first live application of all gates with adversary
catching a real fraud case)
Outcome: SYNTHESIS.md, evaluator PASS on all 5 dimensions, HIGH
confidence on architecture, MEDIUM on Hook C numbers

## What happened

This is the first true v2 protocol pilot on a real user question
(the prior pilot was self-evolve-v2, which was a meta-question about
the team itself). The v2 relaunch was triggered by the user pointing
out that v1's brief had missed several load-bearing recent items
(Ramp Labs Latent Briefing, MemPalace fraud case, MAGMA, EverMemOS,
Memory-in-the-Age-of-AI-Agents as the structural backbone).

The relaunch reused v1's already-written evidence files (planner,
librarian, historian, web-miner, github-miner raw cache) and
extended them with:
- Round 1 missing files: github-miner.md, cartographer.md, tracer.md,
  empiricist.md, linguist.md, historian-addendum.md
- Round 2 gates: synthesist.md, moderator.md, skeptic.md, adversary.md
- Round 3 evaluator: evaluator.md
- Close: this file + scribe ledger update

The synthesis converged on **extend-don't-replace**: keep Akash's
existing ACE-pattern (which is already a working implementation of
the strongest published pattern in the literature), add Hook A
(topic-file routing in the curator) this week, Hook B (SQLite + FTS5
+ vector) conditionally this month, Hook C (Latent Briefing prototype)
in Q3, and a 6-month parametric direction.

The adversary gate produced the canonical agent-memory-fraud case
study (MemPalace, with 21K stars in a week and three independent
audits showing fraudulent benchmarks).

## v2 gate effectiveness — was anything theater?

| Gate | Did it produce material change? | Was it theater? |
|---|---|---|
| **Planner** | Yes — recommended 9-specialist round-1, planner's complexity assessment matched actual rounds run | No |
| **Round 1 wide** | Yes — 10 evidence files, 5 written from scratch in v2 phase | No |
| **Synthesist (claim matrix)** | Yes — 5 load-bearing contradictions surfaced, all sent to moderator | No |
| **Moderator (5 debates)** | Yes — C4 reframe (most important call) was a moderator-only result; C2 reframe ("don't pick by LoCoMo") was moderator-only | No |
| **Skeptic (post-synthesis)** | Yes — 7 corrections to the pre-skeptic synthesis, including upgrading Hook C from "track" to "prototype-as-spike" | No |
| **Adversary (corpus)** | Yes — caught the MemPalace fraud (the skeptic, attacking the synthesis from inside, would never have seen this); rejected 4 source categories; produced REPORTED-NOT-VERIFIED caveat on Latent Briefing | **No — this is the load-bearing v2 catch** |
| **Evaluator (5-dim)** | Yes — the source-quality dimension forced the synthesis to keep MIXED sources out of load-bearing positions and explicitly classify everything | No |
| **Retrospector (this file)** | TBD | TBD |

**Verdict**: v2 gates worked. The MemPalace case alone justifies the
adversary specialist as a permanent fixture. The moderator's C4
reframe (what counts as "more than SQL"?) is the most important
single decision in the synthesis and would not have happened with
lead-only arbitration.

## Lessons for MEMORY.md (durable across sessions)

These are the additions the retrospector proposes for
`~/.claude/agent-memory/research-lead/MEMORY.md`. The scribe will
dedupe against existing entries.

### Lesson 8 — When a user prompt is short and deceptively simple, the supplementary intel is the synthesis backbone
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12)
- **Failure mode addressed**: FM-1.1 (disobey task specification)
  inverted as "obey task specification only at the literal level"
- **Lesson**: Akash's prompt was 19 words. v1 ran with the literal
  reading and missed Ramp Labs Latent Briefing, MemPalace, MAGMA, the
  Memory-in-the-Age-of-AI-Agents taxonomy, and the structural framing
  the synthesis ultimately needed. v2 relaunch had to come from
  the user surfacing the gap. The lesson: **on a question in a
  fast-moving topic, do not trust your initial sub-question list to
  catch the latest 2-week window of releases.** Run a search for
  "newest 14 days" in addition to the planned arxiv/HN/GitHub sweep.
- **Rule of thumb**: open Round 1 with one specialist (web-miner)
  explicitly tasked with "what shipped in the last 14 days that
  wasn't in the planner's brief?" — independent of the other Round
  1 dispatches. Treat it as a structural sweep, not an opportunistic
  find.
- **Counter-example / bounds**: for stable topics with long-cycle
  prior art (e.g. "how does PagedAttention work?"), the 14-day sweep
  is unnecessary. Apply only to topics where the field is producing
  new arxiv submissions weekly.

### Lesson 9 — The adversary catches what the skeptic cannot
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) —
  MemPalace fraud case
- **Failure mode addressed**: FM-3.3 (incorrect verification),
  specifically the corpus-capture variant
- **Lesson**: the skeptic, attacking the synthesis from inside,
  cannot see fraudulent benchmarks because the synthesis correctly
  paraphrases what the source claims. The fraud is at the source-
  vs-reality layer, which the adversary owns. MemPalace is the
  cleanest example: 21K stars, 1.5M views, fraudulent benchmarks,
  three independent audits, maintainer acknowledgment. The skeptic
  would have ratified "MemPalace claims X" because MemPalace does
  claim X. The adversary asks "is X true at the source level?" and
  found it isn't.
- **Rule of thumb**: any time a source presents a benchmark claim,
  the adversary's job is to (a) check if the benchmark is the right
  one, (b) check if the test was run honestly, (c) cross-reference
  against independent audits or reproductions. The skeptic's job is
  to check if the synthesis follows from the source.
- **Counter-example / bounds**: for sources with no quantitative
  claims (e.g. an architectural blog post), the adversary's role
  shrinks to provenance / corpus-capture checks; the skeptic role
  is enough.

### Lesson 10 — Reframe is a valid moderator verdict; "winner take all" is not always available
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) —
  C4 ("is Claude Code's existing memory mechanism insufficient?")
- **Failure mode addressed**: FM-2.5 (ignored other agent's input)
  and FM-2.3 (task derailment)
- **Lesson**: the moderator debates are 3-round structured but the
  verdict types must include REFRAME and COMPLEMENTARITY, not just
  A_WINS / B_WINS. C4 was the most important debate of the session,
  and the right verdict was "neither A nor B is right; the question
  is mis-posed; reframe to taxonomy cells." If the moderator had
  been forced to pick a winner, the synthesis would have become
  either "yes throw away ACE" (wrong) or "no your setup is fine"
  (also wrong, because there ARE cells the existing setup doesn't
  cover).
- **Rule of thumb**: when both sides of a moderator debate make
  defensible arguments, ask "is the question being asked the right
  one?" before forcing a verdict. REFRAME is a valid output type.
- **Counter-example / bounds**: for clearly empirical disagreements
  (e.g. "did benchmark X return Y or Z?"), reframe is a dodge —
  insist on a winner.

### Lesson 11 — Reuse evidence files across reruns; do not redo Round 1 if v1 produced acceptable output
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12)
  v2 relaunch
- **Failure mode addressed**: FM-1.3 (step repetition) and tool
  efficiency
- **Lesson**: v1 produced 5 evidence files (planner, librarian,
  historian, web-miner, github-miner raw cache) before stopping.
  The v2 relaunch reused these and added 6 new files plus the
  Round 2 gates plus Round 3 evaluator. **Reuse saved an estimated
  20+ tool calls** vs starting from scratch. The lesson: when a
  session is relaunched (whether by the user pointing out gaps or
  by the protocol forcing a re-dispatch on evaluator FAIL),
  evidence files that were already written and pass adversary
  audit should be **augmented** (e.g. historian-addendum.md), not
  rewritten.
- **Rule of thumb**: on any rerun, the lead's first action is to
  read every existing EVIDENCE/*.md file and decide which to reuse,
  which to extend, and which to rewrite. Append-only addenda are
  preferred over rewrites.
- **Counter-example / bounds**: if a v1 evidence file has factual
  errors (vs "missed something"), rewrite — don't append.

### Lesson 12 — REPORTED-NOT-VERIFIED is a valid evidence-quality tier
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12) —
  Latent Briefing primary X.com source paywalled (HTTP 402)
- **Failure mode addressed**: FM-3.2 (incomplete verification)
  inverted as "all-or-nothing verification"
- **Lesson**: when a primary source is unreachable but the direction
  is corroborated by multiple independent sources, the right move
  is to cite the primary and explicitly mark the numbers as
  REPORTED-NOT-VERIFIED, NOT to omit the source entirely or to
  pretend it's verified. The Latent Briefing 31% / 1.7s / +3pp
  numbers fall into this tier — directionally validated by
  LatentMAS (arxiv 2511.20639) and LRAgent (arxiv 2602.01053),
  specifically sourced from search-result extraction of a
  paywalled primary.
- **Rule of thumb**: source quality is a 4-tier scale, not a binary:
  STRONG-PRIMARY → MIXED → REPORTED-NOT-VERIFIED → REJECTED. The
  evaluator's source-quality dimension should accept REPORTED-NOT-
  VERIFIED for direction claims if there's independent triangulation,
  but reject it for headline numbers without caveat.
- **Counter-example / bounds**: if the only support for a load-bearing
  number is a single REPORTED-NOT-VERIFIED source, downgrade the
  whole synthesis confidence. Latent Briefing's case has independent
  triangulation, so it doesn't downgrade overall confidence — only
  the Hook C numbers specifically.

### Lesson 13 — When the user's domain is fast-moving, the v1 brief should explicitly include "newest 14 days" as a sub-question
- **Observed in**: claude-memory-layer-sota-2026q2 (2026-04-12)
- **Failure mode addressed**: FM-1.1 (disobey task specification)
  failure to anticipate the latest releases
- **Lesson**: agent memory had 4 major papers (arxiv 2601.02163,
  2601.03236, 2601.09913, 2602.19320) submitted in the 8 weeks
  before this session. Plus MemPalace (April 5) and Ramp Labs
  Latent Briefing (April 11). Plus Cognee v1.0 (April 11) and MemOS
  v2.0.13 (April 10). For a topic moving this fast, "the newest 14
  days" is its own dispatch worth one specialist's attention. v1
  missed all of these; v2 had to be relaunched to include them.
- **Rule of thumb**: at the planner stage, ask "is the field producing
  primary sources weekly?" — if yes, add a "what shipped in the last
  14 days?" sub-question to the wide opener. This is in addition to
  (not a replacement for) the historian's full-corpus sweep.
- **Counter-example / bounds**: for slow-moving topics (e.g. "what
  is the canonical SQL injection mitigation?"), the 14-day sweep
  finds nothing and is wasted effort. Skip.

## v2.1 candidates (process improvements for the protocol itself)

These are NOT durable lessons (those go to MEMORY.md). These are
suggestions for editing PROTOCOL.md or the specialist files.

1. **Add an explicit "14-day fast-moving topic sweep" sub-task to
   the planner's checklist.** This was the missed structural piece
   in v1; it should not be a discretionary call.

2. **Promote REPORTED-NOT-VERIFIED to a named tier in the citation
   schema.** Right now PROTOCOL.md § "Citation schema" lists 7 tiers
   but doesn't explicitly accommodate "primary unreachable, direction
   triangulated." Add as a named tier with the rule "must have ≥2
   independent corroborating sources."

3. **Add an explicit instruction that the lead should reuse v1
   evidence on rerun.** The Lesson 11 pattern was applied
   instinctively this session but isn't documented in PROTOCOL.md.
   The "Round 0 - pre-flight" or "Escalation" sections should mention
   it.

4. **The moderator's verdict types should be enumerated in PROTOCOL.md.**
   REFRAME and COMPLEMENTARITY were used in this session and the
   moderator file documents them, but PROTOCOL.md only mentions
   "verdict" generically. Adding the enum would prevent future
   moderators from forcing winner-take-all on debates that don't
   support it.

5. **Adversary should run BEFORE the synthesist on heavily-SEO-gamed
   topics**, not after. Currently the adversary is in Round 2 after
   synthesist. For topics like agent memory where the adversary
   gate is the load-bearing catch, running it earlier saves the
   synthesist from cataloguing claims that will be rejected anyway.
   This is debatable — the current order has the advantage that the
   synthesist's claim matrix gives the adversary a target list. But
   for the most-SEO-gamed topics, switching the order would be worth
   piloting.

## Score for v2 protocol on this question

| Aspect | Grade | Reasoning |
|---|---|---|
| Did v2 catch real failures v1 wouldn't have? | A+ | MemPalace fraud + Latent Briefing paywall handling + 7 skeptic corrections |
| Were any gates skipped? | None | Every gate fired and produced changes |
| Were any gates theater? | None | Every gate's verdict was acted upon |
| Did the relaunch waste effort? | Minimal | Reused 5 v1 evidence files; only added missing pieces |
| Was the synthesis actionable? | Yes | "This week / this month / Q3 / 6 months" structure with concrete components |
| Was the confidence calibration honest? | Yes | HIGH on architecture, MEDIUM on Hook C numbers, with the source-quality reasoning explicit |

**Overall**: v2 protocol PASSED its first real-question pilot. The
gate order, the role separation, the citation schema, and the
adversary specialist are all validated.

## Confidence
**High** that the lessons above are durable and worth adding to
MEMORY.md. The v2 protocol grades and v2.1 candidate suggestions
are a separate output for the next protocol revision discussion.
