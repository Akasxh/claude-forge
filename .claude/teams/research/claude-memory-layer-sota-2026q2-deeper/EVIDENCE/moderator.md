# Moderator — structured debates for deeper round

Two flagged contradictions from synthesist.md: C-deeper-1 (AND vs OR in scribe routing) and C-deeper-2 (Hook B MVP weights — MemX defaults or empiricist's adjustment). Run each as a 3-round structured debate.

## Debate C-deeper-1 — Scribe routing: `AND` vs `OR`

### Round 1 — Position A: `AND` is correct (too conservative is safer)

**Argument**: The `AND` predicate requires BOTH length ≥1500 AND a type-indicator (code block, quote, table, ref dump, file map). This is the linguist's proposed rule. The safety argument: false positives (over-routing) ruin the index; false negatives (under-routing) only delay the topic-routing until the lesson grows. Mistakes that stay in the index are recoverable; mistakes that move to topic files can orphan the rule of thumb.

**Cite**: `EVIDENCE/linguist.md` § "The Boolean predicate" + § "Edge cases and their rulings" (8 examples).

### Round 1 — Position B: `OR` is correct (long OR reference-heavy both deserve routing)

**Argument**: `OR` would route any lesson that is EITHER long (>1500 chars) OR contains significant reference content (10+ line code block, 300+ char quote, etc.). The generosity argument: topic files are cheap to create, and a 2000-char rule-of-thumb prose is BOTH a rule AND a reference — splitting the distinction is unnecessary. If a long pure-prose lesson ends up in a topic file, the stub still preserves the rule of thumb per the scribe-edit-plan.

### Round 2 — A rebuts

"Position B ignores the **stub schema**. The stub preserves Rule of thumb and a 1-2 sentence Lesson summary. For a long-pure-prose lesson, the 'summary' compression is lossy — the texture of the original prose (the subtle counter-examples, the nuance) gets flattened. For a short code-snippet lesson, the code block IS the lesson and has to move together.

Specifically: Lesson 8 in MEMORY.md ("When user prompt is short, distrust your initial sub-question list to catch the latest 14 days") is ~1900 chars, no code blocks, no tables. Under `OR`, it gets topic-routed because `len >= 1500`. But it's a PURE rule that the lead needs every session. Moving it loses the rule's shape.

Under `AND`, Lesson 8 stays in the index — correctly."

### Round 2 — B rebuts

"Fair point on Lesson 8. But consider Lesson 12 ('REPORTED-NOT-VERIFIED is a valid evidence-quality tier'): ~2100 chars, contains a 4-tier list but no 300-char quote. Under `AND`, it stays in the index because the type conditions are borderline (list-of-4 is less than the ref-dump threshold of 5 items). Under `OR` it would route (len >= 1500 triggers).

Is Lesson 12 better in the index or better as a topic file? Honestly debatable. It's long enough that its prose contributes to the 25KB ceiling; short enough that routing feels wasteful.

My position softens: maybe `AND` is right for MVP, but the threshold (1500) should be lower. `len >= 1000 AND type` would catch Lesson 12 while still respecting Lesson 8."

### Round 3 — A closes

"I accept B's concession on the threshold. The right framing is: `AND` is the predicate, and the THRESHOLD for length should be tuned based on observed routing failures. Start at 1500 for MVP (conservative, low false-positive risk). If the scribe's routing metric shows the index is accumulating lessons that should have been routed, lower the threshold to 1200 or 1000.

The predicate stays `AND`. The threshold is a parameter."

### Round 3 — B closes

"Agreed. `AND` with a tunable threshold is the right answer. Start at 1500 for MVP."

### Moderator verdict — C-deeper-1

**A WINS on the predicate (AND); both sides agree the 1500 threshold is tunable.**

Final ruling:
- Scribe routing predicate: **`AND`** (length AND type)
- Initial length threshold: **1500 characters**
- Threshold is **tunable** — if the scribe metric shows lessons stuck in the index that should have been routed (manual audit or a higher-than-expected 25KB-ceiling hit rate), lower the threshold toward 1200 or 1000 in a future edit.
- All type sub-predicates from linguist.md remain.

**Confidence**: high. Both sides converged. The prophylactic debate was cheap and surfaced the threshold-tuning insight.

---

## Debate C-deeper-2 — Hook B MVP weights: MemX defaults or empiricist adjustment?

### Round 1 — Position A: Use MemX defaults exactly (0.45 / 0.25 / 0.05 / 0.10)

**Argument**: MemX's weights were empirically tuned on a benchmark with published numbers (Hit@1 = 91.3%, < 90ms end-to-end). Adjusting without measurement is speculation. The MVP should reproduce MemX exactly and then calibrate on observed behavior. Akash can swap weights later with a config change; no code edits.

**Cite**: `librarian.md` § "MemX 4-factor reranking" verbatim from paper § 3.4.

### Round 1 — Position B: Use empiricist's adjusted weights (0.45 / 0.30 / 0.13 / 0.02)

**Argument**: MemX's target corpus is 100K+ records (per § 5.1). Akash's corpus will be 100-1000 records at the Hook B build trigger. At that scale:
- **Frequency is nearly useless**: access counts in a 500-entry corpus top out at ~10, which doesn't discriminate. Frequency at 0.05 weight contributes noise, not signal.
- **Importance is high-signal**: Akash's scribe maintains a "Reinforced by" field that tracks cross-session reinforcement. This is a cleaner importance signal than MemX's implicit scheme.
- **Recency matters more**: Akash's sessions have multi-week gaps; memories from 6 months ago are more often stale than memories from 6 months ago in a user assistant (MemX's target user).

Therefore: decrease frequency (0.05 → 0.02), increase importance (0.10 → 0.13), increase recency (0.25 → 0.30), keep semantic (0.45).

**Cite**: `empiricist.md` § "Hook B hybrid ranker implementation recommendation" + back-reference to `librarian.md` for the starting point.

### Round 2 — A rebuts

"B's argument is theoretically sound but untested. The MemX paper is backed by a published benchmark. B's adjusted weights are backed by A-priori reasoning. For an MVP that can be calibrated later, reproducing published defaults is the conservative choice. If frequency contributes noise, the noise floor is 5% — negligible.

Second concern: B is solving a problem that doesn't exist yet. Hook B's build trigger requires miss_rate > 20%. If Hook A is working, Hook B may never be built. Tuning weights for a phase that might not ship is premature optimization."

### Round 2 — B rebuts

"Two counters:

1. The 'premature optimization' concern applies equally to the MVP choice itself. Either way Akash writes Python code with SOME weights. The cost of shipping B's adjusted weights vs MemX's is ZERO additional code — same ranker file, different constants.

2. B's reasoning is NOT untested. It's DOMAIN-KNOWLEDGE-GROUNDED. Akash HAS a small corpus; Akash's scribe DOES track Reinforced-by. These are observable facts, not speculation. The MemX paper's optimality proof is conditional on a large corpus; its weights are not guaranteed to transfer to a small one.

But I'll concede a middle ground: ship MemX defaults in the MVP, BUT instrument the ranker to log the contribution of each factor to the final score. After 50 queries with real data, Akash can observe whether frequency is adding signal or noise and tune accordingly. The instrumentation cost is 1-2 extra LOG lines per query."

### Round 3 — A closes

"I accept B's middle ground. Ship MemX defaults for MVP with per-factor score logging. Retune after 50 real queries."

### Round 3 — B closes

"Agreed."

### Moderator verdict — C-deeper-2

**REFRAME to middle ground.**

Final ruling:
- Hook B MVP ships with **MemX exact defaults**: `W_SEMANTIC=0.45, W_RECENCY=0.25, W_FREQUENCY=0.05, W_IMPORTANCE=0.10` (sum = 0.85, threshold 0.15)
- The ranker logs **per-factor contribution** alongside each query result, so Akash can observe whether any factor is dominating or contributing noise
- After **50 real queries** of observed behavior, Akash or the Engineering Team re-evaluates the weights. Likely adjustments in the direction of the empiricist's position (down-weight frequency, up-weight importance), but NOT without data.
- **Update to `EVIDENCE/mcp-scaffold.md`**: the ranker.py code changes the constants to MemX exact defaults, and adds a debug dict returned from the `rank` function showing per-factor scores. The updated version is in the NEXT STEPS section of synthesis.

**Confidence**: high. The middle ground is empirically defensible and costs nothing extra.

---

## Cross-debate observations

1. **Both debates converged on middle-ground positions**, not winner-take-all. This is consistent with pilot lesson 10 ("REFRAME is a valid moderator verdict"). In this deeper round, the REFRAME was toward "empirical tuning after MVP ships" in both cases, which is a healthy pattern.

2. **No debate required pulling the Anatomy paper** (arxiv 2602.19320) — this is different from the pilot where 3 of 5 debates leaned on it. The deeper round is implementation-focused; the benchmarks are not the load-bearing concern.

3. **No debate required changing the pilot's 4-phase plan** structurally. Both debates tuned parameters within the plan, not the plan itself. The strategic architecture is stable.

## Handoff

- **skeptic** — the two moderator verdicts are now the lead's position; attack them and the rest of the synthesis
- **scribe-edit-plan** — update the length threshold rationale (1500 is tunable)
- **mcp-scaffold** — update the ranker constants to MemX defaults + add per-factor logging

## Confidence

**High** on both verdicts. Both debates ran full 3 rounds with both positions defending primary evidence. The middle-ground reframes are practical and reversible.
